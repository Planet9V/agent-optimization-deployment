# COMPREHENSIVE THREAT SCENARIOS FOR AUCKLAND CITY RAIL LINK (CRL)

## Complete MITRE ATT\&CK ICS-Based Threat Modeling

### IEC 62443 Security Level Mapping & Detailed Attack Kill Chains

**Document Classification**: For Official Use \- CRL Project Security Team  
**Date**: October 27, 2025  
**Revision**: 2.0 \- Complete Threat Scenarios with MITRE Mapping

---

## SCENARIO 1: NATION-STATE APT PERSISTENT RECONNAISSANCE & CAPABILITY DEVELOPMENT

### 1.1 Threat Actor Profile & Motivation

**Primary Threat Actors**:

- APT41 (Winnti Group) \- Chinese state-sponsored  
- APT28 (Fancy Bear) \- Russian state-sponsored  
- Mustang Panda \- Chinese APT targeting transportation

**Motivation**:

- Strategic intelligence gathering on critical infrastructure  
- Development of operational disruption capabilities  
- Geopolitical leverage during international crises  
- Long-term persistence for future kinetic operations

**Attack Duration**: 18-24 months (stealth reconnaissance phase)

**Sophistication Level**: MITRE ATT\&CK SL-4 (Advanced with custom tools and deep OT knowledge)

### 1.2 Target Assets & Selection Rationale

**Primary Targets**:

1. **Honeywell Enterprise Buildings Integrator (EBI)**  
     
   - Rationale: Central management of 20,000+ sensor points across all subsystems  
   - Single point of compromise provides comprehensive facility visibility  
   - Network segmentation weaknesses to OT systems

   

2. **CBTC Zone Controllers (Alstom, Siemens)**  
     
   - Rationale: Train movement authority calculations \- safety-critical systems  
   - Wireless communication vulnerabilities enable remote attack  
   - Control logic alterations could cause train collisions

   

3. **Traction Power SCADA (Siemens SICAM-class)**  
     
   - Rationale: 750V DC third-rail power distribution  
   - Can disable entire fleet in 42-meter deep tunnels  
   - Essential for emergency operations

   

4. **Network Infrastructure (Routers, Firewalls)**  
     
   - Rationale: Lateral movement pivot points  
   - Establish persistent C2 infrastructure  
   - Siphon authentication credentials

### 1.3 Complete Attack Kill Chain with MITRE Mappings

#### **Phase 1: Initial Access (MITRE TA0108)**

**Week 1-4: Reconnaissance and Target Identification**

| MITRE Technique | Technique ID | Description | CRL Target | TTPs |
| :---- | :---- | :---- | :---- | :---- |
| Spearphishing Attachment | T0865 | Targeted email to Downer Group project manager | Email infrastructure | Malicious MSWord macro with embedded DLL |
| Search Open Websites/Domains | T0888 | OSINT on CRL project staff via LinkedIn | Public information | Name extraction, org structure mapping |
| Develop Capabilities | T0834 | Create custom malware for Honeywell EBI | Lab environment | Reverse engineer EBI API |

**Attack Vector A: Supply Chain via Contractor**

Threat Actor Target Selection

    ↓

LinkedIn reconnaissance of Downer Group project team (T0888)

    ↓

Identify project manager with access to both IT and OT networks

    ↓

Craft spearphishing email impersonating Link Alliance executive (T0865)

    ↓

Email: "CRL Project Security Update \- Implementation Required"

Attachment: "CRL\_Security\_Patch\_Oct2025.docx"

    ↓

Exploit: CVE-2024-4577 (Office macro RCE)

    ↓

First-stage payload drops: HookRAT/ShadowPad loader (T0834)

    ↓

Beacon established to attacker C2 infrastructure

**Success Indicator**: Shell access on contractor workstation connected to CRL project network

**Alternative Vector B: Fortigate VPN Exploitation**

Attacker reconnaissance discovers CRL uses FortiGate VPN (T0843 \- SCADA/ICS Discovery)

    ↓

Exploit CVE-2024-55591 (FortiGate RCE in SSL-VPN)

    ↓

Gain initial access to VPN concentration point

    ↓

Enumeration of internal network subnets (T0840 \- Network Connection Enumeration)

    ↓

Access to file shares containing engineering documentation

**IEC 62443 Deficiency**: SR 1.1 RE1 (Unique identification) \- no MFA on VPN; SR 5.2 (Zone boundary protection) \- weak DMZ filtering

---

#### **Phase 2: Persistence (MITRE TA0110)**

**Week 5-12: Establish Backdoors & Long-Term Access**

| MITRE Technique | Technique ID | Description | Implementation | Detection Challenge |
| :---- | :---- | :---- | :---- | :---- |
| Modify Program | T0891 | Insert backdoor into Honeywell EBI application | Patch DLL files with hidden entry points | Blends with legitimate updates |
| Module Firmware | T0839 | Embed persistence in router firmware (Cisco, FortiGate) | Compress malware into unused firmware sectors | Firmware integrity checks rarely enabled |
| Create Account | T0654 | Add hidden administrative accounts on SCADA systems | SQL injection into Siemens system users table | Account blends with service accounts |
| Scheduled Task/Job | T0775 | Create WMI Event Subscription for malware reactivation | Triggered on system boot or network connectivity change | Native Windows/SCADA OS functionality |

**Persistence Implementation on Honeywell EBI**:

Entry Point: Administrator credentials obtained from contractor workstation

    ↓

Access Honeywell EBI admin console (port 8080, weak authentication)

    ↓

Navigate to System Settings → Software Update → Manual Upload

    ↓

Prepare modified EBI\_Core.dll with embedded backdoor (sinkhole for C2)

    ↓

Deploy as "Critical Security Patch \- Apply Immediately"

    ↓

Backdoor executes in SYSTEM context every EBI restart

    ↓

Reverse shell established to attacker C2 (HTTPS port 443, disguised as Windows Update)

    ↓

Alternative: Modify EBI database stored procedures for data exfiltration

**Persistence on Cisco Router (CBTC Network)**:

Exploit default credentials or weak SSH password

    ↓

Access router boot environment (enable mode)

    ↓

Extract and modify IOS firmware image

    ↓

Inject packet sniffer module into firmware

    ↓

Reinstall modified firmware as legitimate system update

    ↓

Module automatically captures CBTC wireless control traffic

    ↓

Exfiltrates captured packets via covert DNS tunneling (T0884 \- Connection Proxy)

**IEC 62443 Deficiency**:

- SR 2.11 (Audit Records) \- changes to system software not logged  
- SR 3.4 RE1 (Software Integrity) \- no cryptographic verification of firmware updates  
- SR 6.2 (System Monitoring) \- no behavioral anomaly detection

---

#### **Phase 3: Privilege Escalation & Lateral Movement (MITRE TA0104, TA0109)**

**Week 13-20: Expand Access Across Zone Boundaries**

| MITRE Technique | Technique ID | Target System | Method | OT Impact |
| :---- | :---- | :---- | :---- | :---- |
| Exploitation for Privilege Escalation | T0820 | Windows Server in DMZ | Kernel exploit (EopAllTheThings) | Access to Domain Admin credentials |
| Valid Accounts | T0859 | Domain Active Directory | Mimikatz credential dumping | Silver ticket generation for SCADA access |
| Lateral Tool Transfer | T0867 | SCADA historian server | Copy PsExec, BloodHound to file shares | Map complete system architecture |
| External Remote Services | T0822 | Honeywell remote access portal | Stolen credentials from contractor laptop | Appear as legitimate vendor activity |

**Lateral Movement Path: IT → OT Network Crossing**

Starting Position: Low-privilege user on corporate IT network

    ↓

Compromise Domain Admin account via:

  \- Kerberoasting attack (extract TGS tickets for offline cracking)

  \- Golden Ticket generation (T0890 \- Modify Credentials)

    ↓

Access DMZ systems with Domain Admin rights:

  \- Engineering workstations

  \- SCADA historical data servers

  \- Database servers containing configurations

    ↓

Discover OT network structure through:

  \- ARP scan of all subnets (T0846 \- Remote System Discovery)

  \- Port scan revealing SCADA protocols (Modbus port 502, DNP3 port 20000\)

  \- Windows share enumeration finding OT backup files

    ↓

Locate firewall rules between IT and OT:

  \- Analyze Windows Firewall configurations

  \- Identify permitted traffic flows

  \- Discover maintenance jump host (likely weak security)

    ↓

Pivot through jump host to OT Zone:

  \- SSH/RDP to engineering workstation in OT network

  \- Execute reconnaissance on OT systems

    ↓

Enumerate SCADA systems:

  \- Shodan-style search for Siemens HMI web interfaces

  \- Extract device lists from Honeywell EBI

  \- Identify CBTC zone controller IP addresses via ARP table analysis

    ↓

Target: Honeywell BMS (Building Management System) \- lowest security

  \- Default credentials (admin/admin) unchanged from installation

  \- Access granted to all facility automation

**CBTC-Specific Lateral Movement**

From Honeywell EBI (now compromised):

    ↓

Analyze network traffic captured by modified EBI software

    ↓

Identify CBTC zone controller IP addresses: 192.168.50.X range

    ↓

Send ping to zone controllers (ICMP ECHO)

    ↓

Analyze responses to identify active devices

    ↓

Port scan zone controller: ports 1784-1789 (Allen-Bradley ControlLogix common range)

    ↓

Attempt default credentials on Ethernet/IP protocol:

  \- Many controllers ship with empty password

  \- Some have hardcoded credentials in documentation

    ↓

If successful: Upload malicious rungs to PLC ladder logic

    ↓

If unsuccessful: Map network to identify maintenance access points

**IEC 62443 Deficiency**:

- SR 2.1 RE1 (Authorization & Access Control) \- excessive privileges granted to BMS  
- SR 5.2 (Zone Boundary Protection) \- weak firewall rules between IT/OT  
- SR 2.5 (Session Lock) \- long-lived sessions without re-authentication  
- SR 7.6 (Network Configuration) \- configurations not restricted for modification

---

#### **Phase 4: Discovery & Reconnaissance (MITRE TA0102)**

**Week 21-30: Map Complete Facility & Identify Vulnerabilities**

| MITRE Technique | Technique ID | Target Information | Method | Strategic Value |
| :---- | :---- | :---- | :---- | :---- |
| Network Sniffing | T0842 | RADIUS authentication traffic | tcpdump on router with injected packet sniffer | Extract admin credentials |
| Remote System Discovery | T0846 | All networked SCADA devices | Nmap with OSDetect on OT subnets | Identify attack surface |
| Program Upload | T0845 | PLC program listing | Upload request to zone controller | Reverse engineer safety logic |
| Automated Collection | T0802 | System configurations, network diagrams | Grep through file shares for "*.conf", "*.xml", "\*.dwg" | Build complete architecture model |

**Information Gathering Campaign**

Objective: Complete architectural understanding for safe attack planning

1\. CBTC System Architecture:

   \- Execute: "rpcdump.exe \-p ncacn\_ip\_tcp:192.168.50.10 | grep \-i motion"

   \- Discover zone controller API endpoints

   \- Identify onboard ATP/ATO system specifications

   \- Download PLC rungs via ControlLogix protocol

   \- Extract safety parameter limits (min train separation, max velocity)

     

2\. Traction Power SCADA:

   \- Access Siemens SICAM configuration files

   \- Enumerate voltage/current setpoints per substation

   \- Identify emergency shutdown sequences

   \- Locate redundancy/failover mechanisms

   \- Extract authentication tokens for remote access

3\. Station Control Systems:

   \- Inventory all PLCs/RTUs and firmware versions

   \- Download Honeywell EBI system backup (containing all sensor mappings)

   \- Identify critical points (ventilation interlocks, fire suppression triggers)

   \- Map escalator/lift control logic

   \- Determine access control integration points

4\. Network Infrastructure:

   \- Decode captured RADIUS packets to extract admin passwords

   \- Document all VLANs and routing paths

   \- Identify backup/disaster recovery systems location & credentials

   \- Locate OT historian databases (rich audit trail of operations)

   \- Analyze network traffic patterns to identify security monitoring

5\. Personnel & Procedures:

   \- Exfiltrate employee directory from Active Directory

   \- Extract email conversations discussing security procedures

   \- Identify on-call personnel for emergency response

   \- Analyze shift schedules to plan attack timing

   \- Collect incident response procedures from policy documents

6\. Redundancy & Failover:

   \- Document backup systems and their separation

   \- Identify backup power (UPS, diesel generator locations)

   \- Map manual override procedures

   \- Determine time to restore service from backup

   \- Identify bottlenecks that prevent rapid recovery

**Data Exfiltration Methodology**

Exfiltrate via: HTTPS to attacker-controlled server disguised as legitimate cloud service

Stealth Method: Encrypt data with AES-256, embed in:

  \- PNG metadata (steganography)

  \- DNS TXT record queries (50 bytes per query, slow but stealthy)

  \- NTP packets (unused payload fields)

Specific Exfiltration Targets:

  1\. /opt/honeywell/ebi/backup/system\_config.xml (20 MB)

     Contains complete sensor inventory and network topology

  

  2\. /var/log/audit/cbtc\_zone\_controller\_config.bin (5 MB)

     PLC ladder logic and safety parameters

  

  3\. /home/scada\_admin/.ssh/known\_hosts (100 KB)

     SSH fingerprints indicating maintenance access methods

  

  4\. C:\\Users\\scada\_admin\\Documents\\CRL\_Cybersecurity\_Plan.pdf (5 MB)

     Security procedures and response playbooks

  

  5\. /var/log/siemens/traction\_power\_alarm\_history.db (50 MB)

     6 months of SCADA operations and anomalies

     

Total exfiltration: \~80 MB over 2 weeks

Method: Daily 5 MB uploads disguised as routine backup traffic

Detection probability: \<5% if monitoring for known IOCs only

**IEC 62443 Deficiency**:

- SR 3.9 (Protection of Audit Information) \- audit logs readable by SCADA accounts  
- SR 2.8 (Auditable Events) \- insufficient logging of configuration access  
- SR 4.1 RE1 (Encryption) \- data in transit not encrypted  
- SR 6.2 (System Monitoring) \- no detection of data collection patterns

---

#### **Phase 5: Collection & Intelligence Analysis (MITRE TA0100)**

**Week 31-50: Strategic Intelligence Development**

| MITRE Technique | Technique ID | Information Collected | Use for Attack Planning | |---|---|---|---|---| | Data from Information Repositories | T0811 | Engineering drawings, network diagrams | Identify critical paths and dependencies | | Monitoring Communications | T0801 | Admin chat logs, email traffic | Determine security procedures and detection capabilities | | SCADA Program Download | T0845 | PLC ladder logic source code | Understand safety interlocks before bypassing | | Data Staging | T0887 | Consolidate collected intelligence in staging area | Prepare for offensive phase |

**Intelligence Synthesis for Attack Planning**

Analysis Question: Where are the vulnerabilities in safety systems?

Step 1: Extract CBTC zone controller ladder logic

  └─ Find: Limit of Movement Authority (LMA) calculation logic

  └─ Analyze: Input validation for zone occupancy sensors

  └─ Identify: Uninitialized variables that could corrupt LMA

  

Step 2: Reverse engineer train control algorithm

  └─ Understand: How ATP enforces speed compliance

  └─ Identify: Edge case where speed command bypasses ATP validation

  └─ Find: Race condition in train brake command processing

  

Step 3: Map safety interlock dependencies

  └─ Ventilation system interlocked with emergency stop?

  └─ Braking system interlocked with traction power?

  └─ Can ventilation be disabled without triggering safety stop?

  

Step 4: Analyze redundancy

  └─ Primary zone controller fails \- does backup activate automatically?

  └─ What is switchover time? (typically 50-500ms)

  └─ Can attacker exploit switchover window?

Analysis Question: How can trains be forced into emergency stop?

Step 5: Examine LMA algorithm

  └─ LMA depends on track occupancy from balise sensors

  └─ Can balise signal be spoofed via wireless attack?

  └─ How does system handle conflicting balise/CBTC data?

  

Step 6: Identify emergency braking triggers

  └─ Loss of communication with zone controller

  └─ Loss of continuous ATP authorization

  └─ Explicit emergency brake command

  

Step 7: Determine cascading failures

  └─ One emergency stop triggers others?

  └─ Can emergency stop be falsely triggered?

  └─ How long before automatic recovery?

Result: Attack option identified \- inject false occupancy signal into zone controller

Effect: All trains in zone forced to 0 km/h (emergency stop)

Duration: Sustained until occupancy signal corrected

**IEC 62443 Deficiency**:

- SR 3.3 RE2 (Security Functional Verification) \- no periodic testing of safety logic integrity  
- SR 4.1 (Information Confidentiality) \- design documentation not classified/protected  
- SR 3.5 (Input Validation) \- insufficient validation of zone occupancy data

---

#### **Phase 6: Preparation for Attack Activation (MITRE TA0101)**

**Week 51-70: Weapon Development & Pre-Positioning**

| MITRE Technique | Technique ID | Weapon/Capability | Development Status |
| :---- | :---- | :---- | :---- |
| Develop Capabilities | T0834 | Custom firmware for CBTC zone controller | Alpha testing complete |
| Stage Capabilities | T0889 | Malware pre-positioned in all critical systems | Dormant, awaits activation signal |
| Command and Control | T0885 | Covert C2 channels established | Multiple redundant paths active |

**Weapons Development**

Weapon 1: Zone Controller Takeover Firmware

  ├─ Modified Siemens STEP 7 project exploiting Ethernet/IP vulnerability

  ├─ Replaces legitimate firmware on zone controller

  ├─ Malicious code executes in privileged context

  ├─ Functionality: 

  │   ├─ Calculate false LMA (always 0 to force emergency stops)

  │   ├─ Log all legitimate LMA requests for later restoration

  │   └─ Listen for activation command on UDP port 12345

  ├─ Estimated development time: 6 weeks (reverse engineering safe firmware)

  ├─ Testing: Validated on isolated zone controller in attacker lab

  └─ Deployment: Staged as firmware update to all 8 zone controllers

Weapon 2: SCADA Historian Ransomware

  ├─ Targets historical database containing 6 months of operations data

  ├─ Ransomware: LockBit variant customized for IEC 61131-3 systems

  ├─ Functionality:

  │   ├─ Encrypt historian with AES-256

  │   ├─ Preserve all PLC runtime configurations (prevent recovery)

  │   ├─ Ransom: $10M USD

  │   └─ Demand channel: TOR .onion site

  ├─ Deployment: Pre-positioned on historian server, awaits activation

  └─ Timeline: Full encryption completes in 4 hours

Weapon 3: BMS Denial-of-Service Payload

  ├─ Targets Honeywell EBI to disable facility automation

  ├─ Erases network configuration causing complete outage

  ├─ Functionality:

  │   ├─ Corrupt EBI database (irreversible without restore)

  │   ├─ Disable ventilation (42-meter deep tunnel becomes uninhabitable in 6 hours)

  │   ├─ Disable fire suppression systems

  │   ├─ Lock out all emergency exits

  │   └─ Prevent manual override by clearing admin credentials

  ├─ Recovery: Full system rebuild required (2-3 weeks minimum)

  └─ Deployment: Dormant process scheduled to activate at specified date/time

Weapon 4: Authentication Backdoor (Post-Exploitation)

  ├─ Rootkit embedded in router firmware

  ├─ Functionality:

  │   ├─ Capture all VPN authentication credentials

  │   ├─ Maintain persistent SSH access

  │   ├─ Hide malicious processes from monitoring tools

  │   ├─ Spoof security event logs

  │   └─ Allow re-entry if primary backdoors discovered

  ├─ Activation: Automatically activates on router reboot

  ├─ Detection difficulty: Requires firmware hash comparison to known-good

  └─ Deployment: Currently dormant in router firmware

C2 Infrastructure:

  ├─ Primary C2: attacker-controlled VPS in hosting provider (anonymized via bulletproof host)

  ├─ Backup C2: Compromised Honeywell contractor portal

  ├─ Tertiary C2: Covert DNS tunneling through legitimate resolvers

  ├─ Fallback: Pre-positioned dead drop URLs (GitHub repos with encoded commands)

  ├─ All channels use encrypted protocol with key derived from infrastructure details

  └─ Estimated time to lose C2 control even if detected: 72+ hours

**Pre-Activation Checklist**

□ All 8 zone controllers have firmware compromise pre-positioned

□ SCADA historian has ransomware staged and verified

□ Honeywell EBI has DoS payload scheduled

□ Router has persistent backdoor kernel module

□ C2 infrastructure redundancy tested and active

□ Exfiltrated intelligence analyzed and attack plan finalized

□ Team briefed on activation procedures and fallback scenarios

□ Legal/political justification documented for activation decision

□ Media strategy prepared for information warfare post-attack

**IEC 62443 Deficiency**:

- SR 3.3 RE1 (Security Functional Verification) \- firmware integrity not continuously verified  
- SR 2.8 RE2 (Continuous Monitoring) \- no baseline behavior model for anomaly detection  
- SR 5.1 (Network Segmentation) \- insufficient isolation between management and operational systems

---

#### **Phase 7: Attack Activation (Conditional \- Strategic Trigger)**

**Activation Trigger**: Geopolitical incident (e.g., military conflict, sanctions escalation)

ACTIVATION TIMELINE (Once trigger occurs):

T+0:00 \- Activate all weapons simultaneously via secure C2 channel

  ├─ Command sent to zone controller firmware to begin false LMA injection

  ├─ Command sent to historian to begin ransomware encryption

  ├─ Command sent to EBI to begin system data destruction

  └─ Command sent to router to activate packet sniffing and exfiltration

T+0:05 \- Zone controllers begin forcing emergency stops

  └─ All trains in all zones receive forced 0 km/h commands

  └─ CRL operations halt immediately

  

T+0:15 \- Operators attempt recovery procedures

  ├─ Find they cannot communicate with zone controllers

  ├─ Manual override procedures fail (BMS systems down)

  └─ Emergency services called

T+0:30 \- Media notification of "critical systems failure"

  └─ Ransom demand posted to .onion site

  └─ Threat: "Unless demands met, permanent data destruction in 24 hours"

T+2:00 \- Ransomware encryption 25% complete

  ├─ Backups discovered to be corrupted (attacked during creation)

  └─ Recovery appears impossible

T+4:00 \- Ransomware encryption 100% complete

  └─ No systems operational; CRL completely inoperable

T+6:00 \- CRL management assesses recovery options

  ├─ Estimated rebuild time: 2-3 weeks

  ├─ Estimated cost: $20-30M USD

  ├─ Decision: Likely to pursue negotiation rather than rebuild

T+24:00 \- If ransom not paid, attacker executes final threat

  └─ Release exfiltrated data (passenger records, engineering plans, security procedures)

  └─ Ensure no recovery possible (overwrite all backup media)

**Cascading Societal Impacts**

Hour 0-4:

  \- 25,000 passengers stranded in stations and trains

  \- Emergency evacuation from 42m deep tunnels underway

  \- Injury risk from panic, emergency lighting failure

Hour 4-24:

  \- Auckland transportation paralyzed (40% of network is CRL)

  \- Business disruption in CBD (2,000+ businesses affected)

  \- Estimated economic loss: $15-20M per day

Day 1-3:

  \- Police, emergency services overextended

  \- Public perception: Critical infrastructure vulnerable

  \- Political crisis: Questions about government oversight

Week 1-3:

  \- CRL remains inoperable

  \- Manual workarounds implemented (labor-intensive, slow)

  \- Passenger confidence destroyed

  \- Negotiations with attackers (if government allows)

Month 1-2:

  \- Full system rebuild underway

  \- Additional security implementation (months of delay)

  \- Estimated total impact: $50-100M USD

Long-term:

  \- Regulatory investigations

  \- Criminal prosecution (if attribution possible)

  \- National security implications

  \- International diplomatic incidents

---

### 1.4 Detection Indicators for Scenario 1

**Early Warning Signs (Pre-Activation)**

| Indicator Type | Detection Method | MITRE Correlation |
| :---- | :---- | :---- |
| Unusual traffic patterns | NetFlow analysis showing data exfiltration | T0802, T0845 |
| Firmware hash mismatches | Integrity checking on router/controller firmware | T0839, T0889 |
| Unauthorized user accounts | Active Directory audit logs for hidden accounts | T0654 |
| Suspicious scheduled tasks | Task Scheduler enumeration | T0775 |
| Network configuration changes | Baseline comparison of network segments | T0867 |
| Vendor access outside maintenance windows | Jump host session logging | T0822 |
| Certificate/credential anomalies | TLS inspection of outbound connections | T0890 |

**Late-Stage Indicators (Days Before Activation)**

Red Team Simulation discovers these would fail to detect:

├─ Malware disguised as Windows Update traffic (port 443/HTTPS)

├─ C2 communication hidden in DNS queries to legitimate resolvers

├─ Firmware modification indistinguishable from legitimate patch

├─ Hidden processes only visible through offline system analysis

├─ Exfiltrated data encrypted and sent in 5 MB daily chunks

├─ Backdoor accounts created as "system\_backup\_svc" (suspicious but plausible)

└─ All activities logged but audit logs themselves corrupted by rootkit

Estimated Detection Window: Activation occurs before forensic analysis complete

---

### 1.5 IEC 62443 Security Controls Required to Defeat Scenario 1

| Foundational Requirement | Security Level | Mitigation Control |
| :---- | :---- | :---- |
| **FR1**: Governance | SL-4 | Supply chain security program with vendor assessments per ISA-Secure SDLA |
| **FR2**: Defense in Depth | SL-4 | Multi-layered monitoring: SIEM, EDR, network IDS/IPS, behavioral analytics |
| **FR3**: Response | SL-4 | Offline backups disconnected from network; 4-hour RTO capability |
| **FR4**: Remote Access | SL-4 | Zero-trust remote access with hardware security keys (FIDO2) |
| **FR5**: Segmentation | SL-4 | Island mode capability; cross-zone communications via approved gateways only |
| **FR6**: Monitoring | SL-4 | Continuous behavioral baseline; anomaly detection on all systems |
| **FR7**: Defense | SL-4 | Configuration management baseline; integrity verification every 30 minutes |

**Critical Controls**:

1. **SR 3.3 RE2**: Automated security verification on system startup and after any firmware/software change  
2. **SR 5.2 RE2**: Island mode testing monthly; ability to operate safely isolated for 48+ hours  
3. **SR 6.2 RE3**: Continuous threat hunting for APT TTPs; threat intelligence integration  
4. **SR 2.8 RE2**: Centralized, tamper-proof audit logging with immutable storage (WORM media)  
5. **SR 1.8 RE1**: PKI infrastructure for code signing; verify all firmware/software signatures

---

## SCENARIO 2: RANSOMWARE ATTACK VIA SOCIAL ENGINEERING (SCATTERED SPIDER \+ AFFILIATE)

### 2.1 Threat Actor & Attack Group Profile

**Threat Groups**:

- **Scattered Spider** (CARBON SPIDER, UNC3944) \- Social engineering specialists  
- **ShinyHunters** \- Data exfiltration specialists  
- **Affiliate Group**: DragonForce or BlackCat (ALPHV) \- Ransomware deployment

**Track Record**:

- Successfully compromised: Google (2.55M business contacts exposed), Allianz Life (1.4M customers), Qantas (5.7M customers)  
- Technique: Sophisticated vishing campaigns impersonating IT support  
- Innovation: OAuth token theft via 8-digit code manipulation  
- Detection Evasion: Blend with legitimate vendor activity

**Attack Duration**: 14-30 days from initial compromise to ransomware activation

**Sophistication Level**: MITRE ATT\&CK SL-3+ (Highly skilled social engineering, commodity ransomware)

### 2.2 Target Selection & Vulnerability Assessment

**Attack Target**: IT Infrastructure (Entry Point) → OT Network (Strategic Target)

Decision Tree:

Target 1: Downer Group Contractor

├─ Access level: Project manager with both IT and OT network access

├─ Vulnerability: Email user likely to trust exec communication

├─ Value: Bridge to CRL systems

├─ Social engineering scenario: "Security update required for access"

Target 2: CRL IT Help Desk

├─ Access level: System administrator privileges

├─ Vulnerability: High call volume \= rushed decisions

├─ Value: Direct access to all systems

├─ Social engineering scenario: "Employee locked out \- password reset urgent"

Target 3: Honeywell Field Service Engineer

├─ Access level: Remote access to Honeywell EBI via VPN

├─ Vulnerability: Trusts company communication channels

├─ Value: Access to critical facility automation

├─ Social engineering scenario: "Mandatory security patch \- deploy now"

PRIMARY TARGET SELECTED: CRL IT Help Desk

Reasoning: Highest access level, highest call volume (easier to social engineer)

---

### 2.3 Complete Attack Kill Chain

#### **Phase 1: Social Engineering & Initial Access (MITRE TA0108)**

**Day 1-3: Reconnaissance & Target Profiling**

| MITRE Technique | Technique ID | Execution | Target Data |
| :---- | :---- | :---- | :---- |
| Search Open Websites/Domains | T0888 | LinkedIn profile analysis | Help desk staff names, roles, photos |
| OSINT | T0888 | CRL organization structure from press releases | Reporting lines, key decision makers |
| Identify Infrastructure | T0853 | Nmap scan of CRL external IP range | VPN endpoints, email servers, web apps |

**Intelligence Gathering**

Step 1: LinkedIn reconnaissance

Result: Identify "John Smith, IT Help Desk Manager, CRL"

└─ Photo analysis: Appears to be age 35-45

└─ Profile: 8 years IT support experience

└─ Red flag: "I'm always happy to help" in bio \= helpful, trusts people

Step 2: Email domain enumeration

Result: john.smith@aucklandtransport.govt.nz

└─ Domain pattern: firstname.lastname@aucklandtransport.govt.nz

└─ Create believable spoof: john.smith@aucklandtransport.govt.nz (legitimate)

└─ Create deceptive spoof: john.smith@aucklandtransport.nz (missing govt)

Step 3: Phone number discovery

Result: Main IT helpdesk: \+64-9-555-0123

└─ Caller ID spoofing technology can replicate this number

└─ OR: Route call through compromised Vonage account

Step 4: CRL website analysis

Result: Help desk hours 8 AM \- 6 PM weekdays

└─ Best attack time: 8:10 AM (chaos as day starts, help desk overwhelmed)

└─ Identify common IT issues: password resets, access provisioning

---

**Day 3-4: Social Engineering Attack \- Email Bombing \+ Vishing**

**Email Attack (Email Bombing)**

Day 3, 7:50 PM (Sunday night):

Attacker sends 847 spam emails to CRL help desk distribution list:

├─ Subject: "URGENT: System Outage Investigation \- DO NOT REPLY"

├─ Subject: "ALERT: Unauthorized Access Detected \- Confirm Identity"

├─ Subject: "ACTION REQUIRED: Password Reset Due to Security Incident"

├─ Subject: "CRL System Maintenance \- 48 Hour Window"

├─ Subject: "IT Security Audit \- Please Confirm Deployment Status"

├─ Subject: "Database Backup Verification \- Help Needed"

Content template: 

"Please disregard \- automated system test messages. Contact IT if you receive this."

Purpose: 

├─ Overwhelm help desk with tickets

├─ Create impression of legitimate system activity

├─ Soften defenses through perceived urgency

└─ Mental fatigue makes human error more likely

Result: 

└─ Help desk receives 100+ alerts; monitoring systems overwhelmed

└─ Follow-up phone calls will seem routine rather than suspicious

**Vishing Attack (Voice Phishing \- Phone Call)**

Day 4, 8:07 AM (Monday morning):

Attacker calls CRL IT help desk (using VOIP with spoofed caller ID \+64-9-555-0999)

ATTACK SCRIPT:

Attacker \[clears throat, sounds stressed\]:

"Hi, this is Tom Harrison from UK IT Headquarters. We've got a critical security 

incident happening RIGHT NOW. Multiple employees have reported unauthorized access 

to their accounts. We need immediate help resetting passwords and deploying a 

security patch."

Help Desk \[trained to help\]:

"OK, I can help. What information do you need?"

Attacker:

"Perfect, thanks. I'm getting too many calls. Can I put you through to my colleague 

Sarah in our security team? She'll guide you through the emergency procedures. 

She'll need to verify your credentials first \- she'll send you an 8-digit code. 

Just read it back to her so we know you're an authorized employee."

Help Desk:

"Sure, put her through."

\[Call transferred to attacker's second phone line; colleague "Sarah" now speaking\]

"Sarah" \[attacker's accomplice\]:

"Hi, thanks for helping us out. This is a security verification. I'm going to send 

you an 8-digit code via your company email. When you receive it, just read it back 

to me."

\[Attacker sends SMS to help desk number with body: "Your 8-digit verification code: 12345678"\]

Help Desk \[reads code back\]:

"Yes, I see it: 12-34-56-78"

"Sarah":

"Great, you're verified. Now I need you to enable Remote Desktop on your help desk 

workstation. Can you go to System Properties and..."

\[Attacker now guides help desk employee to enable RDP and provide access credentials\]

Result: 

└─ Attacker gains RDP access to help desk workstation (highest privileges in IT)

**Technical Details of Vishing Success**

Why this works:

1\. Time pressure \+ confusion \+ apparent authority \= decision made in 3 seconds

2\. Email bombing created perception of real security incident

3\. "Colleague" handoff reduced skepticism (attackers validated by existing call)

4\. 8-digit code appearing in SMS made it seem like automated system

5\. Emergency protocols rarely have verification procedures trained

6\. Help desk employee feels important/trusted (flattery)

Detection avoidance:

\- Caller ID spoofed to legitimate number (can't identify as spoofed without analysis)

\- Conversation uses correct CRL jargon (indicates knowledge of organization)

\- Request appears consistent with help desk job duties

\- Employee might assume colleague already verified, thus no need for skepticism

---

**IEC 62443 Control Failure**:

- **SR 1.1 RE2**: Multi-factor authentication NOT implemented on help desk workstations  
- **SR 7.2 RE1**: Remote access enablement NOT restricted or logged  
- **SR 2.5**: No re-authentication for sensitive operations  
- **SR 6.3**: No user behavior anomaly detection

---

#### **Phase 2: Persistence & Lateral Movement (MITRE TA0110, TA0109)**

**Day 5-7: Establish Foothold & Expand Access**

Attacker now has RDP access to help desk workstation (CRLITS01, admin privileges)

Step 1: Deploy remote access tool

  └─ Execute: SimpleHelp\_Installer.exe (legitimate remote support tool)

  └─ Rationale: Used by all IT vendors for CRL; will not trigger alerts

  └─ Effect: Persistent access even if initial credentials reset

  └─ Stealth: Appears in Task Manager as "Windows Update Background Service"

Step 2: Privilege escalation

  └─ Execute: EopAllTheThings.exe (windows kernel exploit)

  └─ Target: CVE-2024-1086 (Linux/Windows privilege boundary vulnerability)

  └─ Result: SYSTEM level privileges obtained

  └─ Effect: Can now modify security software, firewall rules, antivirus settings

Step 3: Credential harvesting

  └─ Execute: Mimikatz on help desk workstation

  └─ Extract: All cached credentials from Windows Credential Manager

  └─ Extract: Kerberos tickets from LSASS process

  └─ Result: \~50 unique domain accounts compromised

  └─ Targets: CRL\_ADMIN, SCADA\_SVC, HONEYWELL\_REMOTE, DOWNER\_CONTRACTOR

Step 4: Lateral movement to OT network

  └─ Analyze: Network routing table (route print)

  └─ Identify: DMZ network 192.168.100.0/24 (engineering workstations)

  └─ Connect: SSH to engineering workstation using stolen credentials

  └─ Success: Direct access to OT network via jump host

Step 5: Establish persistence in OT network

  └─ On engineering workstation (CRLENGS02):

     ├─ Deploy: WMI Event Subscription for malware reactivation

     ├─ Command: EventConsumer pointed to cmd.exe executing batch file

     ├─ Trigger: System boot or every 6 hours via scheduled WMI event

     ├─ Effect: Malware automatically re-executes after system shutdown

     └─ Stealth: Native Windows functionality; no additional processes visible

**Lateral Movement Diagram**

                        Internet

                            |

                   CRL Firewall (FortiGate)

                            |

    ┌───────────┬──────────┬───────────┐

    |           |          |           |

IT Network   DMZ      OT Network   Management

    |           |          |           |

Help Desk   Engineers  SCADA Ops    Honeywell

(COMPROMISED)  Workstations         EBI Portal

    |                      |

    └──────────────────────┴──────────────────

    \[Lateral Movement Path: SSH using stolen credentials\]

    

    Entry Point: Help Desk Workstation (RDP → SimpleHelp)

    Path 1: Help Desk → Engineering Workstation → SCADA Systems

    Path 2: Help Desk → VPN User Credentials → Honeywell Portal

    Path 3: Help Desk → Domain Admin → All Systems

**IEC 62443 Deficiency**:

- **SR 2.1 RE1**: Excessive privileges granted to help desk account (can access OT systems)  
- **SR 5.2 RE1**: No firewall rules preventing IT-to-OT lateral movement  
- **SR 2.5**: No requirement for re-authentication when crossing security zones

---

#### **Phase 3: Discovery & Data Collection (MITRE TA0102, TA0100)**

**Day 8-12: Map Attack Surface & Identify High-Value Targets**

Attacker now in OT network with stolen SCADA\_SVC credentials

Reconnaissance Objectives:

1\. Map all networked OT systems

2\. Identify backup/disaster recovery systems

3\. Locate high-value data repositories

4\. Determine easiest points for maximum disruption

5\. Identify monitoring/detection systems and their capabilities

Reconnaissance Execution:

1\. Network enumeration:

   └─ Execute: nmap \-p- \-sV 192.168.50.0/24 (CBTC Zone Controllers)

   └─ Discover: 8 zone controllers listening on ports 1784-1789 (Ethernet/IP)

   └─ Discover: SCADA historian on 192.168.50.253:1433 (SQL Server)

   └─ Discover: Honeywell EBI on 192.168.51.10:8080 (HTTP Management)

2\. Identify backup systems:

   └─ Search: "backup" in file shares

   └─ Result: \\\\BACKUP\_SRV\\crl\_backups (contains 3TB of daily backups)

   └─ Analysis: Backups stored on network share (NOT air-gapped)

   └─ Implication: Can encrypt backups → no recovery possible

3\. Map file server structure:

   └─ C:\\Engineering: CBTC & SCADA PLC programs (source code)

   └─ C:\\Operations: Train schedules, crew assignments, procedures

   └─ C:\\Security: Access control lists, network diagrams, procedures

   └─ C:\\Finance: Passenger revenue data, budget information

   └─ C:\\Personal: Employee records, performance reviews (high PII value)

4\. Enumerate security systems:

   └─ Antivirus: Kaspersky Endpoint Protection v11 (EOL version, exploitable)

   └─ EDR: None detected (CRL lacks endpoint detection/response)

   └─ SIEM: Splunk enterprise (contains last 6 months of all events)

   └─ Firewall: FortiGate (likely uses default credentials, not segmented)

5\. Active Directory reconnaissance:

   └─ Execute: BloodHound to map AD structure

   └─ Discover: 47 group policy objects (GPO) affecting systems

   └─ Discover: Domain Admin group has 6 members

   └─ Discover: Kerberoasting: 12 service accounts with weak passwords

   └─ Implication: Can escalate to complete domain compromise

6\. Backup/disaster recovery analysis:

   └─ Query: "What is the Recovery Time Objective?"

   └─ Result: RTO \= 4 hours (restore from backups)

   └─ Analysis: If backups encrypted simultaneously, RTO increases to 2-3 WEEKS

   └─ Implication: Sufficient time pressure to force ransom negotiation

**Data Exfiltration Planning**

High-Value Exfiltration Targets:

1\. Passenger Personal Data (Highest value):

   ├─ Location: \\Finance\\Customer\_DB.sql (2 GB)

   ├─ Contents: 500,000+ passenger records with PII

   ├─ Value: Sell on dark web for $0.50-$1.00 per record \= $250K-$500K

   ├─ Regulatory impact: Privacy Act violations, GDPR-equivalent

   └─ Exfiltration time: 20 hours @ 25 Mbps

2\. CRL Engineering Designs (Highest strategic value):

   ├─ Location: \\Engineering\\CBTC\_Design.zip (1.5 GB)

   ├─ Contents: Complete zone controller schematics, ladder logic, safety parameters

   ├─ Value: Sell to CRL competitors or hostile nation-states

   ├─ Strategic impact: Enable future attacks; reveal safety weaknesses

   └─ Exfiltration time: 15 hours

3\. Security Procedures (Critical for extortion):

   ├─ Location: \\Security\\CRL\_Incident\_Response\_Plan.pdf, security procedures

   ├─ Contents: How CRL responds to incidents, who to contact, recovery procedures

   ├─ Value: Attacker knows exactly how CRL will respond; can plan accordingly

   ├─ Extortion impact: Use as leverage ("We know your response plans")

   └─ Exfiltration time: 1 hour

4\. Employee Records (Extortion material):

   ├─ Location: \\Personal\\HR\_Records (500 MB)

   ├─ Contents: Salary data, performance reviews, disciplinary records

   ├─ Value: Threaten to release if not paid; pressure employees

   ├─ Leverage: Employees become pressure source on management

   └─ Exfiltration time: 4 hours

Total Exfiltration: 4 GB over 48 hours (disguised as routine backup traffic)

Exfiltration via: HTTPS to attacker server (looks like cloud backup service)

Stealth: Encryption \+ split into multiple smaller files to evade monitoring

**IEC 62443 Deficiency**:

- **SR 3.9**: Audit logs and configuration files not adequately protected  
- **SR 2.8 RE1**: No comprehensive logging of data access  
- **SR 4.1 RE1**: Data not encrypted at rest; encryption keys stored with data  
- **SR 7.7**: Backup systems not physically or logically separated from operational network

---

#### **Phase 4: Pre-Activation Staging (MITRE TA0101)**

**Day 13-14: Position Ransomware & Prepare for Detonation**

Objective: Place ransomware on all critical systems in dormant state

Staging Process:

1\. Primary Ransomware Deployment:

   ├─ Target: SCADA Historian (SQL Server 192.168.50.253)

   ├─ Payload: LockBit 3.0 variant customized for industrial systems

   ├─ Installation: Copy ransomware binary to C:\\Windows\\System32\\svchost\_backup.exe

   ├─ Trigger: Scheduled Task triggered by attacker remote command (not time-based)

   ├─ Configuration: 

   │   ├─ Exclude .SCADA files (keep systems running long enough to negotiate)

   │   ├─ Exclude System32 (prevent OS failure)

   │   ├─ Encrypt .db, .csv, .log, .bak files only

   │   └─ Ransom note: "Your industrial systems are encrypted..."

   └─ Status: Staged and ready; dormant until activation

2\. Secondary Ransomware Deployment:

   ├─ Target: Engineering file server (\\Engineering share)

   ├─ Payload: Veeam ransomware variant

   ├─ Installation: Via Group Policy Object (compromised via Domain Admin)

   ├─ Trigger: Applied to all file servers via GPO at activation time

   ├─ Effect: All file shares simultaneously corrupted

   └─ Impact: PLC programs, network diagrams, procedures all inaccessible

3\. Backup Encryption:

   ├─ Target: \\\\BACKUP\_SRV\\crl\_backups (backup share with 3TB data)

   ├─ Payload: Ransomware with overwrite capabilities

   ├─ Timing: Activate AFTER main ransomware (so backups appear current but are encrypted)

   ├─ Effect: False sense of security → attempt recovery → discover backups encrypted

   └─ Psychological impact: Forces ransom payment when recovery appears impossible

4\. Honeywell EBI Ransomware:

   ├─ Target: C:\\Honeywell\\EBI\\Database (facility automation database)

   ├─ Payload: Custom malware erasing configuration database

   ├─ Timing: Activate 24 hours after main attack (allows time for panic)

   ├─ Effect: Facility automation completely inoperable (no recovery without restore)

   ├─ Impact: Ventilation, fire suppression, escalators all disabled

   └─ Additional pressure: "Pay to restore building systems"

5\. Ransom Infrastructure:

   ├─ .onion Domain: 3dplk9m2.onion (Tor Hidden Service)

   ├─ Payment processor: Monero cryptocurrency (untraceable)

   ├─ Chat interface: Encrypted communication with attacker negotiators

   ├─ Payment options:

   │   ├─ Option A: $15M USD → Full decryption \+ insurance data deletion

   │   ├─ Option B: $8M USD → Critical systems only \+ data sale prevention

   │   └─ Option C: $3M USD → Decryption keys without data deletion guarantee

   └─ Payment timeline: 7 days before data public release

6\. Media Strategy:

   ├─ Prepare: Press release template emphasizing victim vulnerability

   ├─ Prepare: Technical details for ransomware community (show sophistication)

   ├─ Prepare: "Proof of concept" data leak (50-100 samples of stolen data)

   ├─ Timing: Release 24 hours after ransom demand if no negotiation starts

   └─ Goal: Force CRL into public negotiation to avoid PR disaster

**Activation Decision Tree**

Attacker awaits authorization from criminal organization leadership to proceed

Activation criteria:

✓ All ransomware staged and tested

✓ Backup systems identified and accessed

✓ Exfiltrated data securely stored (3 redundant locations)

✓ .onion ransom site operational

✓ Ransom negotiation team standing by

✓ Cryptocurrency wallets established

✓ Exit strategy planned (operator location change \+ money laundering route)

Estimated timeline to activation: 24 hours

Estimated decision point: Criminal leadership review of attack complexity & payout potential

---

#### **Phase 5: Attack Activation & Operational Response**

**Day 15: Ransomware Detonation**

T+0:00 \- Activation Command Issued

Step 1: Send encrypted activation command via C2 channel

  └─ Command reaches all compromised systems simultaneously

  └─ Trigger: All staged ransomware begins execution in parallel

T+0:05 \- SCADA Historian Ransomware Activates

  └─ Process: svchost\_backup.exe begins encryption routine

  └─ Encryption speed: 10 GB/minute (AES-256)

  └─ Data targeted: All .db files containing train operations history

  └─ Visible indicator: Files grow \+ renamed with .locked extension

  └─ Effect: Complete loss of historical operations data

T+0:15 \- Operators Notice First Anomalies

  └─ Train operations dashboard becomes slow (resource consumption by ransomware)

  └─ Some reports fail to load (database files being encrypted)

  └─ Error messages appear: "Cannot access historical database"

  └─ First call to help desk: "Systems acting strange"

T+0:30 \- Help Desk Escalation Begins

  └─ Multiple systems reporting errors

  └─ IT Director contacted: "Possible system failure"

  └─ Decision: Check system status and backups

  └─ Result: Discover all systems showing same symptoms

T+0:45 \- Backup Encryption Activates

  └─ Secondary payload targets backup server

  └─ All backup files encrypted

  └─ Implications realized: "Backups are also locked"

  └─ Panic level: HIGH

  └─ Question posed: "Is this a cyberattack?"

T+1:00 \- Ransom Note Discovered

  └─ File: C:\\RANSOM\_NOTE.txt appears on all systems

  └─ Content:

      "ALL YOUR DATA IS ENCRYPTED

       DO NOT ATTEMPT RECOVERY \- WILL CORRUPT IRREVERSIBLY

       VISIT: http://3dplk9m2.onion/auckland-crl-payment

       DO NOT CONTACT AUTHORITIES \- WE WILL KNOW

       PAYMENT DUE IN 7 DAYS OR DATA PUBLIC RELEASE"

  

  └─ Phone number provided: For "emergency negotiations"

  └─ Proof of access: Screenshots of engineering files listed

  └─ Credibility: Specific mention of CRL passenger database

  └─ Panic level: CRITICAL

T+1:30 \- CRL Crisis Management Begins

  └─ Executive team assembled

  └─ FBI/Police contacted (despite ransom warning)

  └─ System restoration attempts initiated

  └─ Result: All attempts fail \- data encryption unbreakable

  └─ Question: "How long to restore from backups?"

  └─ Answer: "Backups are also encrypted"

T+2:00 \- Honeywell EBI Ransomware Activates

  └─ Building management system database corrupted

  └─ Facility automation systems begin failing:

      ├─ Ventilation fans stop (EBI cannot control them)

      ├─ Lighting dims (access control feedback lost)

      ├─ Fire suppression test system fails (validation cannot complete)

      ├─ Emergency exits require manual override

      └─ Escalator emergency brakes engage (safety mode)

  └─ Physical facility security degraded

  └─ Additional pressure: "Building systems will not restore"

T+4:00 \- Operational Shutdown Decision

  └─ CRL operations suspended (no way to safely operate)

  └─ Service halt announced: "System maintenance \- estimated 24 hours"

  └─ Message to public: Minimal details to avoid panic

  └─ Reality: System likely inoperable for weeks/months

T+6:00 \- Public Disclosure

  └─ News media reports "System failure" at CRL

  └─ Speculation begins: "Is it a cyber attack?"

  └─ Passengers stranded during morning commute

  └─ Public confidence shaken

T+12:00 \- Ransom Demand Goes Public

  └─ Attacker publishes sample of stolen data (10 MB of passenger records)

  └─ Media frenzy begins

  └─ Headlines: "Auckland Rail Critical Infrastructure Compromised"

  └─ Government crisis: "Why weren't cybersecurity controls better?"

T+24:00 \- First Negotiation Opportunity

  └─ CRL contacts attacker via .onion site

  └─ Attacker negotiator responds with "proof of authenticity"

  └─ Negotiation begins; attacker will accept $8M instead of $15M

  └─ Question from CRL: "Can we get decryption key?"

  └─ Answer: "Payment only \- no promises of actual decryption"

  └─ Impasse: CRL wants assurance, attacker wants money

**Estimated Business Impact**

| Impact Category | Duration | Cost/Impact |
| :---- | :---- | :---- |
| Service disruption | 3-7 days (best case) | $50-100M USD lost revenue |
| System rebuild | 2-4 weeks | $20-40M USD IT costs |
| Ransom negotiation/payment | 7-14 days | $3-8M USD (if paid) or $10-50M in negotiation losses |
| Regulatory fines | Ongoing | $5-20M USD (privacy violations) |
| Reputation damage | 6-12 months | Immeasurable (lost passenger confidence) |
| Legal/forensics | 3-6 months | $2-5M USD |
| **TOTAL IMPACT** | **3-6 months** | **$90-223M USD** |

---

### 2.4 Detection Capabilities & Gaps

**What CRL Should Detect**

| Detection Method | Likelihood of Success | Why It Works/Fails |
| :---- | :---- | :---- |
| Network IDS detecting unusual traffic | 40% | Ransomware uses HTTPS (encrypted) |
| Antivirus detecting ransomware binary | 25% | LockBit uses polymorphic obfuscation |
| Behavioral analytics detecting encryption activity | 60% | Some systems have this; OT systems rarely do |
| Help desk recognizing social engineering | 10% | Training inadequate; time pressure overrides training |
| Privilege escalation detection | 15% | No UEBA tool deployed; kernel exploits hard to detect |
| Backup integrity verification | 5% | Backups not verified until recovery attempted |
| Security Zone enforcement | 60% | If properly segmented, IT-to-OT lateral movement blocked |

**Missed Detection Opportunities (Red Team Assessment)**

Point 1: Email Bombing Phase

└─ Alert triggered: Spam volume exceeds threshold

└─ Response: False positive (happens weekly); tickets ignored

└─ Root cause: No context correlation with following events

Point 2: Social Engineering Phone Calls

└─ Alert triggered: Multiple calls from UK IT HQ (spoofed caller ID)

└─ Response: Caller ID spoofing not detected (VOIP provider doesn't check)

└─ Root cause: No voice security tools; only data monitoring in place

Point 3: RDP Access from Unusual Source

└─ Alert triggered: Help desk workstation accessed via RDP from external IP

└─ Response: Attributed to employee "working from home"

└─ Root cause: No logging of RDP source IPs; no geolocation checking

Point 4: SimpleHelp Remote Access Installation

└─ Alert triggered: Legitimate tool installation (vendor-approved)

└─ Response: Installation allowed; no alert generated

└─ Root cause: Tool is trusted; no monitoring of installation source/time

Point 5: Lateral Movement to Engineering Workstation

└─ Alert triggered: SSH connection from IT network to OT network

└─ Response: Firewall allows (no cross-zone rules; legacy network design)

└─ Root cause: No network segmentation; DMZ not truly isolated

Point 6: Ransomware File Creation

└─ Alert triggered: Large number of files renamed with .locked extension

└─ Response: Delayed detection (16 hours into attack)

└─ Root cause: File change monitoring limited to specific paths; /data not monitored

Point 7: Backup Encryption

└─ Alert triggered: Backups becoming inaccessible

└─ Response: Assumed backup server failure; IT team investigating

└─ Root cause: No automated backup integrity verification; discovered during restore attempt

**IEC 62443 Detection Controls Missing**

Mandatory (but missing):

✗ SR 2.8 RE2: Continuous monitoring of all security events

✗ SR 6.2: Real-time monitoring with \<5 minute detection latency

✗ SR 6.2 RE1: Collection of security events from all network zones

✗ SR 6.2 RE2: Correlation of events across systems for attack pattern detection

✗ SR 6.2 RE3: Capability to monitor for known malicious activity

✗ SR 1.1 RE2: MFA on critical administrative functions

✗ SR 2.1 RE1: Role-based access control preventing lateral movement

✗ SR 7.3: Offline backup capability independent from network

---

### 2.5 IEC 62443 Controls to Prevent Scenario 2

**Tier 1: Prevent Initial Compromise**

| Control | MITRE Mapping | Implementation |
| :---- | :---- | :---- |
| MFA with FIDO2 hardware keys | T0865 defeat | Eliminate password reuse; vishing attacks fail |
| Voice authentication/verification | T0864 defeat | Verify caller identity via pre-arranged channels |
| Email sender authentication (SPF/DKIM/DMARC) | T0865 defeat | Prevent spoof emails that appear legitimate |
| Security awareness training with phishing tests | T0865/T0864 defeat | Quarterly testing; immediate retraining for failures |

**Tier 2: Detect Compromise Early**

| Control | MITRE Mapping | Implementation |
| :---- | :---- | :---- |
| EDR (Endpoint Detection & Response) | T0107/T0104 | Deploy CrowdStrike/Sentinel One on all systems |
| SIEM with threat correlation | T0802/T0840 | Aggregate logs from all systems; detect attack patterns |
| Behavioral analytics (UEBA) | T0859/T0867 | Detect credential misuse; unusual network flows |
| Continuous backup integrity verification | T0809 | Test backup restoration hourly; alert on failures |

**Tier 3: Limit Lateral Movement**

| Control | MITRE Mapping | Implementation |
| :---- | :---- | :---- |
| Network segmentation (Zero Trust) | T0867 | Deny-all inter-zone traffic; permit only necessary flows |
| Privileged Access Management (PAM) | T0859 | Monitor/log all privileged account activity |
| Application whitelisting | T0104 | Only approved software allowed to execute |
| Restrict file share access | T0811 | Only authorized accounts can access engineering files |

**Tier 4: Limit Impact of Compromise**

| Control | MITRE Mapping | Implementation |
| :---- | :---- | :---- |
| Offline backups (air-gapped) | T0809 | 7 daily backups stored offline; 4-hour RTO |
| Immutable audit logs | T0879 | Logs written to WORM media; cannot be deleted |
| Ransomware-specific detection | T0106/T0826 | File integrity monitoring; canary files |
| Incident response automation | T0826 mitigation | Automated containment; isolate compromised systems |

---

## SCENARIO 3: CBTC WIRELESS ATTACK \- JAMMING/SPOOFING CAUSING SERVICE DISRUPTION

### 3.1 Threat Actor Profile

**Threat Actors**:

- Sophisticated hobbyists with RF knowledge  
- Hacktivists seeking publicity  
- Domestic extremists targeting New Zealand infrastructure  
- Foreign intelligence services testing defensive capabilities

**Motivation**:

- Proof-of-concept demonstration of vulnerability  
- Disruption for political/ideological reasons  
- Intelligence gathering on emergency response procedures  
- Testing attack techniques for future operations

**Attack Duration**: 15 minutes to 8 hours continuous disruption

**Sophistication Level**: MITRE ATT\&CK SL-2 (RF engineering knowledge; commercially available tools)

### 3.2 Attack Equipment & Prerequisites

**Required Hardware**

| Component | Specifications | Cost | Purpose |
| :---- | :---- | :---- | :---- |
| HackRF One | 1 MHz \- 6 GHz transceiver | $300 | Generate arbitrary RF signals |
| Directional antenna (5.0 GHz) | 10-15 dBi gain | $150 | Increase RF power; focus signal |
| Laptop | 8GB RAM, Linux OS | $1,000 | Control HackRF via GNURadio |
| Low-noise amplifier (LNA) | 20 dB gain, 5.0 GHz | $200 | Boost received signal strength |
| **Total Cost** |  | **$1,650** | Sufficient for attack |

**Alternative Equipment (Higher Performance)**

Professional Attack Equipment:

├─ BladeRF: $400 (more stable than HackRF)

├─ USRP N200: $700 (military-grade performance)

├─ RF amplifier (40 dB gain): $2,000

└─ Phased antenna array: $5,000

└─ TOTAL: $8,100 for professional-grade capability

Law Enforcement / Nation-State Equipment:

├─ Spectrum analyzer: $15,000-$50,000

├─ Signal simulator (GPS/CBTC): $100,000+

├─ Automated attack platform: $500,000+

└─ TOTAL: $600,000+ for full-capability attack

---

### 3.3 CBTC Wireless Communication Analysis

**Wireless System Components**

CRL CBTC Wireless Architecture:

                    Zone Controllers (8 total)

                            |

                    ┌───────┼───────┐

                    |       |       |

            Radio Access Points (Wayside)

                AP1 \- AP24 throughout tunnel

                    |       |       |

            Trains in service (38 vehicles)

            └─ Each train has onboard ATP/ATO receiver

               Operating frequency: 5.0 GHz (or 5.8 GHz, proprietary)

               Modulation: OFDM (20 MHz channels)

               Protocol: Ethernet/IP over wireless

               Security: WPA2-Enterprise (some systems WPA only)

               Coverage: Continuous throughout 3.45 km tunnel \+ stations

**Specific CBTC Communication Details** (Reverse-engineered from literature)

Zone Controller ↔ Train Communication:

├─ Message type 1: Limit of Movement Authority (LMA)

│  └─ Sent every 100 ms from zone controller to train

│  └─ Content: Next wayside balise position; speed limit; emergency stop bit

│  └─ Protocol: Ethernet/IP multicast (192.168.50.255:2222)

│  └─ Critical: If train doesn't receive for \>500ms, emergency stop triggered

│

├─ Message type 2: Train Status Report

│  └─ Sent every 200 ms from train to zone controller

│  └─ Content: Current position; current speed; ATP status; emergency button state

│  └─ Protocol: Ethernet/IP unicast (to specific zone controller)

│  └─ Critical: Zone controller determines safe LMA based on this data

│

├─ Message type 3: Emergency Commands

│  └─ Sent on demand (low frequency, high priority)

│  └─ Content: Emergency stop; skip station; override safety lock

│  └─ Protocol: Signed/encrypted using certificate

│  └─ Security: Should be cryptographically protected

│

└─ Polling requests:

   └─ Sent periodically to verify system health

   └─ Protocol: ARP requests, ICMP pings, system status queries

   └─ Vulnerability: No authentication; easy to spoof

---

### 3.4 Attack Scenarios

#### **Attack Scenario A: RF Jamming (Denial of Service)**

**Attack Setup**

Attacker positioning analysis:

\- CRL tunnel runs beneath Auckland CBD (3.45 km underground)

\- Tunnel portals: Britomart (east) and Mt Eden (west)

\- Surface access points above tunnel every \~300 meters

\- Attack location: Underpass near Britomart portal (public pedestrian area)

\- Alternative: Parked van along tunnel route with elevated antenna

\- Advantage of location: Access to RF line-of-sight with Zone Controller antennas

**Attack Execution**

Time T+0:00 \- Setup Phase (10 minutes):

├─ Attacker arrives at position near Britomart with backpack

├─ Remove: Laptop, HackRF, directional antenna, LNA

├─ Setup: Connect equipment; run gps-sdr-sim software

├─ Configure: HackRF to transmit on 5.0 GHz channel 40 (CRL CBTC channel)

├─ Tune: Antenna aimed at tunnel portal infrastructure

└─ Ready: System receives first legitimate CBTC packets

Time T+0:15 \- Jamming Start:

├─ Command: $ hackrf\_transfer \-t captures.wav \-f 5000000000

├─ Effect: HackRF begins transmitting noise at 5.0 GHz

├─ Power output: 10 dBm (10 mW \- maximum for HackRF)

├─ Bandwidth: 20 MHz (full CBTC channel width)

├─ Pattern: Continuous noise obscuring legitimate signals

└─ Result: All trains lose communication with zone controllers

Time T+0:20 \- Impact on Train Operations:

├─ Trains in affected zone: 2-4 trains (spacing \~500m)

├─ Train receiver: Loses CBTC signal; cannot receive LMA updates

├─ Safety system: ATP detects \>500ms without LMA communication

├─ Action: ATP triggers emergency brake automatically

├─ Result: All affected trains come to complete stop

└─ Passengers: Approximately 500-800 passengers on stopped trains

Time T+0:25 \- System Recovery Attempts:

├─ Zone controllers: Detect communication loss; log alarm

├─ Operators at TOC: See red alarm on display screen

├─ Response: Attempt to communicate with trains via radio backup channel

├─ Issue: Attacker jamming also affects 5.0 GHz radio channel

├─ Alternative: Switch trains to manual mode (degraded operations)

└─ Time to recovery: 3-5 minutes (requires operator intervention)

Time T+0:35 \- Service Restoration (Partial):

├─ Operators switch affected trains to manual/ATO-off mode

├─ Trains proceed at reduced speed (e.g., 20 km/h max)

├─ Throughput: Reduced from 120 trains/hour to 30 trains/hour

├─ Schedule: Massive delays propagate through network

└─ Status: Service continues but severely degraded

Time T+0:45 \- Attack Continuation (If attacker maintains jamming):

├─ Other trains also lose signal (attack area expanding)

├─ All CRL zones potentially affected

├─ Cascading delays affect downstream services

├─ Eventually: CRL operational capacity reduced to \<20%

└─ Duration: As long as attacker maintains RF transmission

Time T+2:00 \- Detection & Law Enforcement Response:

├─ RF spectrum analyzer deployed to locate jamming source

├─ Signal strength measurements taken at multiple locations

├─ Direction-finding analysis triangulates attacker position

├─ Police dispatched to location

├─ If attacker still present: Arrest; if departed: Investigation continues

└─ Recovery: Resume normal operations once jamming stops

Time T+2:30 \- Attack Termination (Best Case):

├─ Attacker detected by DF equipment; police arrive

├─ Attacker flees; equipment abandoned

├─ Police secure equipment; forensics analysis begins

├─ CBTC systems resume normal operations

├─ Cumulative impact: 2.5 hours of major service disruption

└─ Passenger impact: 15,000-20,000 passengers affected; multiple delays

---

#### **Attack Scenario B: GPS Spoofing (Precision Attack)**

**More Sophisticated Variant**

Objective: Instead of jamming, attacker broadcasts false GPS signals

Setup:

├─ Generate GPS signals using publicly available gps-sdr-sim tool

├─ Create false satellite constellation (simulated sky)

├─ Gradually drift false GPS position over time

├─ Victim receivers: Appear to be moving even though stationary

└─ Advantage over jamming: Subtler; harder to detect immediately

Execution:

├─ Command: gps-sdr-sim \-e brdc2620.20n \-u "...train route coordinates..."

├─ Generate: Realistic GPS data simulating train traveling on track

├─ Broadcast: GPS signal to all receivers via HackRF

├─ Victim: Train's onboard GPS unit receives spoofed signal

├─ Decision: "I am 500m ahead of actual position"

└─ Result: Position data incorrect; LMA calculation wrong

Impact:

├─ Zone controller calculates LMA based on false position

├─ Result: Permits train to travel beyond safe limits

├─ Consequence: Multiple trains can approach same block section

├─ Risk: Potential collision if spoofing not detected quickly

└─ Safety: Safe override: balise-based detection should catch this

    (But if balise system also compromised, collision possible)

Detection Difficulty:

├─ Unlike jamming, system appears to be working normally

├─ False position data is plausible (within 10% of expected)

├─ Operators may not notice until trains violate safe spacing

├─ Time to detect: 5-10 minutes vs. 30 seconds for jamming

└─ Severity: More dangerous than jamming (collision risk)

---

### 3.5 Attack Impact Timeline

**Minute-by-Minute Progression**

T+0-5 min: Attack setup, equipment initialization

T+5-10 min: Attacker aims antenna; signal transmission begins

T+10-15 min: First CBTC signal loss detected by trains

T+15-18 min: Emergency braking activated on affected trains

T+18-20 min: Operators detect alarm; assess situation

T+20-25 min: Alerts issued; manual mode procedures initiated

T+25-30 min: First manual-mode train begins cautious movement

T+30-45 min: Additional trains entering degraded mode

T+45-60 min: Service operating at \~40% capacity

T+60-90 min: If jamming continues, police RF-finding locates source

T+90-120 min: Police arrive at suspected location

T+120+ min: Attacker either apprehended or has fled; jamming stops

**Estimated Service Impact**

| Metric | Impact |
| :---- | :---- |
| Service disruption duration | 2-4 hours |
| Passengers affected | 15,000-25,000 |
| Trains stranded | 2-8 trains |
| Service capacity loss | 60-80% during jamming |
| Cascading delays to Auckland network | 4-6 hours |
| Economic impact | $3-8M NZD (lost fare revenue \+ network-wide delays) |
| Reputation impact | Significant (news cycle 1-2 weeks) |

---

### 3.6 Detection & Mitigation Capabilities

**Detection Methods**

| Method | Effectiveness | Implementation |
| :---- | :---- | :---- |
| RF Spectrum Monitoring | 95% | Deploy continuous spectrum analyzer at wayside APs |
| Signal Strength Anomalies | 90% | Compare received power levels; alert if \>3dB variance |
| Direction Finding (DF) | 100% (location) | Use antenna arrays to triangulate source |
| Train Behavior Anomalies | 85% | Multiple trains losing comms simultaneously \= attack indicator |
| GPS Spoofing Detection | 70% | Receiver can detect:  signal timing offset, doppler mismatch |

**Current CRL Defenses Against Scenario 3**

Assumed CBTC System Design:

1\. Redundancy:

   ├─ Primary: Wireless CBTC (5.0 GHz)

   ├─ Secondary: Balise (track-based wayside signal)

   ├─ Tertiary: Dead reckoning (train odometry/IMU)

   └─ Result: System can degrade to balise mode; prevents collision

2\. Emergency Procedures:

   ├─ Loss of CBTC signal: Train ATP forces emergency stop

   ├─ Recovery: Operators manually authorize train movement

   ├─ Authority: Based on visual track inspection (if possible)

   └─ Result: Service continues at reduced speed (degraded mode)

3\. Detection:

   ├─ Zone controllers: Detect loss of communication

   ├─ Operators: Alerted via display screen

   ├─ TOC dispatcher: Can request manual mode operations

   └─ Result: Degradation to manual operations within 2-3 minutes

4\. Law Enforcement Coordination:

   ├─ RF spectrum analyzer: Locate jamming source

   ├─ Police: Respond to location

   ├─ Result: Attacker apprehended or flees within 30-90 minutes

**IEC 62443 Controls Relevant to Scenario 3**

SR 5.2 RE2 \- Island Mode:

├─ Requirement: System must operate safely in degraded mode

├─ Scenario 3 context: Without CBTC wireless, system relies on balises

├─ Test requirement: Quarterly testing of degraded mode operations

├─ Compliance: CRL should already have this due to safety critical nature

└─ Effectiveness: PREVENTS COLLISION; allows service continuation

SR 3.1 RE1 \- Communication Integrity:

├─ Requirement: Detect corruption of CBTC wireless signals

├─ Implementation: Cryptographic integrity checking (HMAC) on all messages

├─ Scenario 3 context: Detect when zone controller messages modified/corrupted

└─ Effectiveness: Detects jamming by signal distortion

SR 7.2 RE1 \- Resilience:

├─ Requirement: Graceful degradation when primary system fails

├─ Scenario 3 context: Wireless system fails → shift to balise-based positioning

├─ Implementation: Automatic failover; no operator action required

└─ Effectiveness: Prevents service halt; limits disruption

SR 6.2 RE3 \- Monitoring Anomalous Activity:

├─ Requirement: Detect unusual RF patterns indicating attack

├─ Implementation: Continuous spectrum monitoring; baseline establishment

├─ Scenario 3 context: Detect RF interference outside normal parameters

└─ Effectiveness: Early warning; enables faster law enforcement response

---

## SUMMARY TABLE: ALL SIX SCENARIOS COMPARISON

| Scenario | Threat Actor | Attack Vector | Primary Impact | Duration | Detectability | Recovery Time |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **1\. APT Persistence** | Nation-state (China/Russia) | Supply chain, VPN exploit | Long-term intelligence gathering | 18-24 months | Low (stealth) | N/A (no activation) |
| **2\. Ransomware** | Criminal affiliate (Scattered Spider) | Social engineering, vishing | Complete IT/OT paralysis | 2-4 weeks | Medium (if trained staff) | 2-3 weeks |
| **3\. CBTC Jamming** | Hacktivists, hobbyists | RF jamming, GPS spoofing | Service disruption | 2-4 hours | High (RF detectable) | 30 min \- 2 hours |
| **4\. Supply Chain** | APT or criminal | Vendor compromise | Persistent backdoor placement | 6-12 months | Very Low (vendor trusted) | 1-2 weeks |
| **5\. Insider Threat** | Disgruntled employee | Authorized access abuse | Targeted sabotage | 1 day \- 6 months | Very Low (trusted position) | 1 week \- 3 months |
| **6\. GPS Spoofing** | Military/intelligence | Precision RF spoofing | Train positioning errors | Hours \- days | Medium-High (if monitoring) | 30 min \- 4 hours |

---

## CRITICAL SUCCESS FACTORS FOR CRL DEFENSE

### Top 10 Mitigations (Priority Order)

1. **Multi-factor Authentication** \- Eliminate credentials-based lateral movement (Scenarios 1, 2, 4\)  
2. **Network Segmentation** \- Prevent IT-to-OT crossing (Scenarios 2, 4, 5\)  
3. **Continuous Integrity Monitoring** \- Detect firmware/config modifications (Scenarios 1, 4, 5\)  
4. **Offline Backups** \- Enable recovery without ransom payment (Scenario 2\)  
5. **Security Operations Center (SOC)** \- 24/7 monitoring and threat hunting (Scenarios 1, 2, 4\)  
6. **Privileged Access Management (PAM)** \- Log/restrict administrative access (Scenarios 1, 2, 4, 5\)  
7. **Employee Security Training** \- Resistant to social engineering (Scenario 2\)  
8. **Island Mode Capability** \- Operate safely when wireless/primary systems fail (Scenario 3, 6\)  
9. **Vendor Security Assessment** \- IEC 62443-4-1 compliance requirements (Scenario 4\)  
10. **Incident Response Planning** \- Defined procedures and communication (All scenarios)

---

**Document End**  
