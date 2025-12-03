# Critical Vulnerabilities (CVEs) in Railway Control Systems

## [[VULNERABILITY:CVE-2025-1727]] - End-of-Train/Head-of-Train Protocol

### Vulnerability Profile
**Severity:** [[SEVERITY:CRITICAL]]
**CVSS v3 Score:** 8.1 (HIGH)
**CVSS v4 Score:** 7.2
**Vector:** AV:A/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:H

### Affected Systems
- [[VENDOR:Siemens_Mobility]] [[PRODUCT:Trainguard_EOT_HOT_Devices]]
- [[VENDOR:Wabtec]] [[PRODUCT:EOT_HOT_Systems]]
- [[VENDOR:DPS_Electronics]] [[PRODUCT:Rail_Communication_Devices]]
- [[VENDOR:Hitachi_Rail_STS_USA]] [[PRODUCT:Equipment]]

### Technical Description
The [[PROTOCOL:S-9152_Standard]] used for remote linking over RF between [[DEVICE:End-of-Train]] (EOT) and [[DEVICE:Head-of-Train]] (HOT) devices relies on [[WEAKNESS:BCH_Checksum]] for packet creation without [[MISSING_CONTROL:Authentication]].

#### Exploitation Mechanism
[[THREAT_ACTOR:Attackers]] can craft malicious packets using [[TOOL:Software-Defined_Radio]] (SDR) to issue unauthorized [[COMMAND:Brake_Control]] commands.

**Exploitation Requirements:**
- [[TOOL:Software-Defined_Radio]] device ($200-$2000)
- [[TECHNIQUE:BCH_Checksum_Calculation]] capability
- [[TECHNIQUE:RF_Transmission]] at EOT/HOT frequency
- [[ACCESS:Adjacent_Network_Access]] (wireless range)

### Exploitation Potential
1. [[CAPABILITY:Valid_Command_Packet_Generation]] via SDR
2. [[WEAKNESS:No_Authentication_Required]] for command injection
3. [[ACCESS:Adjacent_Network_Access]] sufficient (wireless range)
4. [[IMPACT:Sudden_Train_Stoppage]] possible
5. [[IMPACT:Brake_System_Failure]] achievable

### Attack Scenarios
**Scenario 1: [[ATTACK:Emergency_Brake_Activation]]**
- [[ATTACKER]] positions near rail line with [[TOOL:SDR]]
- [[TECHNIQUE:Packet_Crafting]] for emergency brake command
- [[TECHNIQUE:RF_Transmission]] to [[DEVICE:EOT_Device]]
- [[IMPACT:Sudden_Train_Stop]] on active rail line
- [[CONSEQUENCE:Service_Disruption]] and potential [[CONSEQUENCE:Derailment_Risk]]

**Scenario 2: [[ATTACK:Brake_System_Disablement]]**
- [[ATTACKER]] sends [[COMMAND:Brake_Release]] commands
- [[TECHNIQUE:Continuous_RF_Jamming]] of legitimate signals
- [[IMPACT:Loss_of_Brake_Control]]
- [[CONSEQUENCE:Safety_System_Failure]]

### Mitigation Status
**[[STATUS:NO_SOFTWARE_FIX_AVAILABLE]]**

[[VENDOR:Siemens]] statement: "No software fix is currently planned" due to [[ROOT_CAUSE:Protocol-Level_Nature]].

[[ORGANIZATION:Association_of_American_Railroads]] (AAR) pursuing [[SOLUTION:New_Equipment_and_Protocols]] to replace traditional [[DEVICE:EOT_HOT_Devices]].

**Fix Expected:** [[TIMELINE:2027]]

### Real-World Impact
This [[VULNERABILITY:CVE-2025-1727]] was identified **12 years ago** but ignored in [[GEOGRAPHY:US_Rail_Systems]]. Currently exploitable on:
- [[TARGET:Active_Freight_Rail_Networks]]
- [[TARGET:Passenger_Rail_Networks]]
- [[TARGET:Commuter_Rail_Systems]]

### Recommended Mitigations (Interim)
1. [[MITIGATION:RF_Spectrum_Monitoring]] near rail lines
2. [[MITIGATION:SDR-Based_Detection]] of unauthorized transmissions
3. [[MITIGATION:Manual_Verification_Protocols]] for unexpected brake commands
4. [[MITIGATION:Incident_Response_Procedures]] for brake anomalies
5. [[MITIGATION:Accelerate_AAR_Protocol_Replacement]]

### TTPs for Exploitation
- [[TECHNIQUE:MITRE_ATT&CK:T1200]] - Hardware Additions (SDR device)
- [[TECHNIQUE:MITRE_ATT&CK:T1557]] - Adversary-in-the-Middle (RF interception)
- [[TECHNIQUE:MITRE_ATT&CK:T1499]] - Endpoint Denial of Service (brake activation)
- [[TECHNIQUE:MITRE_ATT&CK:T1495]] - Firmware Corruption (if targeting device firmware)

---

## Siemens SIMATIC S7-1500 PLC Vulnerabilities

### [[VULNERABILITY:CVE-2022-38773]] - Protected Boot Bypass

**Severity:** [[SEVERITY:MEDIUM]]
**CVSS Score:** 4.6
**Status:** Disclosed January 2023

#### Affected Systems
- [[PRODUCT:Siemens_SIMATIC_S7-1500]] series (100+ models)
- [[PRODUCT:SIPLUS_S7-1500]] programmable logic controllers
- Used extensively in [[APPLICATION:Railway_Interlocking]] and [[APPLICATION:Signaling_Systems]]

#### Technical Description
[[WEAKNESS:Architectural_Vulnerabilities]] allow [[ATTACKER]]s to bypass all [[CONTROL:Protected_Boot]] features, resulting in persistent arbitrary modification of operating code and data.

**Root Cause:** [[WEAKNESS:Lack_of_Asymmetric_Signature_Verification]] for:
- [[COMPONENT:Bootloader]] stages
- [[COMPONENT:Firmware]] stages

**Exploitation Capability:**
- [[TECHNIQUE:Custom-Modified_Firmware_Installation]]
- [[TECHNIQUE:Persistent_Backdoor_Deployment]]
- [[TECHNIQUE:Operating_Code_Manipulation]]

#### Railway Impact
[[PRODUCT:SIMATIC_S7-1500]] PLCs are deployed in:
- [[SYSTEM:Computer-Based_Interlocking]] (CBI) systems
- [[SYSTEM:SIMIS_W_Interlocking_Systems]]
- [[SYSTEM:Track_Circuit_Controls]]
- [[SYSTEM:Signal_Automation_Systems]]

**Safety Criticality:** [[RISK:HIGH]]
- Interlocking systems prevent [[HAZARD:Train_Collisions]]
- Signal controls ensure [[SAFETY:Safe_Train_Separation]]
- Track circuits provide [[SAFETY:Train_Detection]]

#### Attack Scenarios
**Scenario: [[ATTACK:Malicious_Interlocking_Modification]]**
1. [[TECHNIQUE:Physical_Access]] or [[TECHNIQUE:Remote_Access]] to PLC
2. [[TECHNIQUE:Custom_Firmware]] with [[PAYLOAD:Logic_Bomb]] installed
3. [[TRIGGER:Time-Based]] or [[TRIGGER:Condition-Based]] activation
4. [[IMPACT:Route_Conflict_Creation]]
5. [[CONSEQUENCE:Train_Collision_Risk]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1542.001]] - System Firmware (bootloader manipulation)
- [[TECHNIQUE:MITRE_ATT&CK:T1601]] - Modify System Image
- [[TECHNIQUE:MITRE_ATT&CK:T1205]] - Traffic Signaling (control system manipulation)

---

### [[VULNERABILITY:CVE-2022-38465]] - Global Private Key Extraction

**Severity:** [[SEVERITY:CRITICAL]]
**CVSS Score:** 9.3 (CRITICAL)
**Status:** Disclosed 2023

#### Technical Description
[[VULNERABILITY:CVE-2022-38465]] allows [[TECHNIQUE:Extraction_of_Global_Private_Keys]] from [[PRODUCT:Siemens_SIMATIC_S7-1500]] PLCs, enabling [[ATTACKER]]s to:

1. [[CAPABILITY:Install_Malicious_Firmware]] across multiple devices
2. [[CAPABILITY:Achieve_Full_Device_Control]]
3. [[CAPABILITY:Persist_Access]] through firmware-level backdoors
4. [[CAPABILITY:Impersonate_Legitimate_Devices]]

#### Exploitation Impact
**Scale:** [[SCOPE:Fleet-Wide_Compromise]]
- Single [[TECHNIQUE:Key_Extraction]] compromises all devices using same key infrastructure
- [[TECHNIQUE:Lateral_Movement]] across entire [[NETWORK:Railway_Control_System]]
- [[TECHNIQUE:Persistent_Backdoor]] at [[LAYER:Firmware_Level]]

#### Attack Chain
1. **Initial Compromise:** [[TECHNIQUE:Exploit_CVE-2022-38465]] on single PLC
2. **Key Extraction:** [[TECHNIQUE:Global_Private_Key_Dumping]]
3. **Firmware Development:** [[TECHNIQUE:Malicious_Firmware_Creation]] with extracted keys
4. **Propagation:** [[TECHNIQUE:Automated_Firmware_Deployment]] to all PLCs
5. **Persistence:** [[TECHNIQUE:Firmware-Level_Rootkit]]

#### Railway-Specific Risks
[[TARGET_SYSTEM:Railway_Signaling_Networks]] often deploy:
- [[DEPLOYMENT:Standardized_PLC_Configurations]]
- [[DEPLOYMENT:Common_Firmware_Versions]]
- [[DEPLOYMENT:Shared_Key_Infrastructure]]

This creates [[VULNERABILITY:Single_Point_of_Failure]] for entire rail network.

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1552.004]] - Private Keys (extraction)
- [[TECHNIQUE:MITRE_ATT&CK:T1587.001]] - Malware (firmware development)
- [[TECHNIQUE:MITRE_ATT&CK:T1608.001]] - Upload Malware (firmware deployment)
- [[TECHNIQUE:MITRE_ATT&CK:T1542.001]] - System Firmware (persistence)

---

### [[VULNERABILITY:CVE-2015-5374]] - Remote Code Execution

**Affected System:** [[PRODUCT:Siemens_SIMATIC_S7-300_PLC]]
**Impact:** [[CAPABILITY:Remote_Code_Execution]] and [[ACCESS:Unauthorized_Access]] to railway systems

#### Legacy System Risk
[[PRODUCT:SIMATIC_S7-300]] PLCs remain deployed in:
- [[SYSTEM:Legacy_Signaling_Systems]]
- [[SYSTEM:Older_Interlocking_Installations]]
- [[SYSTEM:Non-Critical_Railway_Controls]]

**Vulnerability Age:** Disclosed 2015 (10+ years old)
**Patch Status:** [[STATUS:Vendor_Patch_Available]]
**Deployment Status:** Many [[DEPLOYMENT:Unpatched_Systems]] remain operational

#### Exploitation
[[VULNERABILITY:CVE-2015-5374]] enables:
- [[TECHNIQUE:Remote_Code_Execution]] without authentication
- [[TECHNIQUE:PLC_Logic_Modification]]
- [[TECHNIQUE:Safety_System_Bypass]]
- [[TECHNIQUE:Process_Manipulation]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1210]] - Exploitation of Remote Services
- [[TECHNIQUE:MITRE_ATT&CK:T1059]] - Command and Scripting Interpreter
- [[TECHNIQUE:MITRE_ATT&CK:T1542]] - Pre-OS Boot (if bootloader exploited)

---

## European Train Control System (ETCS) Vulnerabilities

### System Overview
[[SYSTEM:ETCS]] is the signaling and control component of [[SYSTEM:European_Rail_Traffic_Management_System]] (ERTMS), designed in the [[ERA:1990s]] with [[STATUS:Outdated_Security_Measures]].

### Identified Vulnerabilities

#### 1. [[VULNERABILITY:Authentication_Weaknesses]]

**Issue:** [[WEAKNESS:Random_Numbers_Exchanged_in_Plaintext]]
- [[PROTOCOL:EuroRadio]] authentication exposes [[DATA:Random_Numbers]]
- [[ATTACK:Collision_Attack]] possible against authentication
- [[WEAKNESS:Design_Flaws]] allow [[TECHNIQUE:Message_Forgery]] after MAC collision

**Attack Scenario:**
1. [[TECHNIQUE:Traffic_Capture]] of [[PROTOCOL:EuroRadio]] authentication
2. [[TECHNIQUE:Random_Number_Collection]]
3. [[TECHNIQUE:MAC_Collision_Detection]]
4. [[TECHNIQUE:Message_Forgery]] during collision window
5. [[IMPACT:Unauthorized_Train_Control_Commands]]

#### 2. [[VULNERABILITY:GSM-R_Communication_Flaws]]

**Weaknesses in [[PROTOCOL:GSM-R]]:**
- [[ALGORITHM:A5-1_Encryption]] - [[STATUS:Cryptographically_Broken]]
- [[WEAKNESS:No_End-to-End_Data_Protection]] (only MS to BS)
- [[VULNERABILITY:Man-in-the-Middle_Attacks]] possible
- [[VULNERABILITY:Over-the-Air_Firmware_Update]] exploitable

**Technical Details:**
[[PROTOCOL:GSM-R]] inherited [[PROTOCOL:GSM]] protocol weaknesses from [[ERA:1990s]]:
- [[ALGORITHM:A5-1]] can be broken in [[TIMEFRAME:Real-Time]] with modern hardware
- [[WEAKNESS:Unilateral_Authentication]] (network authenticates to phone, not vice versa)
- [[VULNERABILITY:IMSI_Catcher]] attacks possible
- [[TECHNIQUE:Traffic_Interception]] and [[TECHNIQUE:Modification]] feasible

**Attack Vectors:**
- [[TECHNIQUE:MITRE_ATT&CK:T1557.002]] - ARP Cache Poisoning (network layer)
- [[TECHNIQUE:MITRE_ATT&CK:T1600]] - Weaken Encryption (A5/1 exploitation)
- [[TECHNIQUE:MITRE_ATT&CK:T1499]] - Endpoint Denial of Service (jamming)

#### 3. [[VULNERABILITY:Balise_System_Vulnerabilities]]

**[[COMPONENT:Balise_Transmission_Module]] (BTM) Weaknesses:**
- [[VULNERABILITY:Sensitive_to_Jamming]]
- [[WEAKNESS:Communication_Not_Designed_for_Cyber_Attacks]]
- [[VULNERABILITY:Multipath_Vehicle_Bus_Interception]]
- [[VULNERABILITY:MVB_Spoofing]]
- [[STANDARD:ERTMS]] does not address [[THREAT:Jamming]] as security threat

**Attack Scenarios:**

**[[ATTACK:Balise_Jamming]]:**
- [[TECHNIQUE:RF_Interference]] on balise frequency
- [[IMPACT:Train_Position_Data_Loss]]
- [[CONSEQUENCE:Degraded_Mode_Operation]]
- [[RISK:Safety_Margin_Reduction]]

**[[ATTACK:Balise_Spoofing]]:**
- [[TECHNIQUE:Fake_Balise_Deployment]]
- [[TECHNIQUE:Incorrect_Position_Data_Injection]]
- [[IMPACT:Train_Positioning_Error]]
- [[CONSEQUENCE:Collision_Risk]]

#### 4. [[VULNERABILITY:EuroRadio_MAC_Algorithm]]

**Exploitable Weaknesses:**
- [[ALGORITHM:MAC_Algorithm]] has cryptographic weaknesses
- Combined with [[VULNERABILITY:GSM-R_Vulnerabilities]] enables [[TECHNIQUE:Message_Forgery]]
- [[ATTACK:Birthday_Attack]] reduces effective security strength

**Exploitation Chain:**
1. [[TECHNIQUE:GSM-R_Interception]] (A5/1 break)
2. [[TECHNIQUE:EuroRadio_Traffic_Capture]]
3. [[TECHNIQUE:MAC_Collision_Search]]
4. [[TECHNIQUE:Message_Forgery]]
5. [[TECHNIQUE:Train_Control_Command_Injection]]

---

## Communication-Based Train Control (CBTC) Vulnerabilities

### System Characteristics
[[SYSTEM:CBTC]] widely uses:
- [[COMPONENT:Off-the-Shelf_Software]]
- [[COMPONENT:Commercial_Operating_Systems]]
- [[WEAKNESS:Known_Vulnerabilities_Inevitably_Present]]

### Challenges
- [[CHALLENGE:Difficulty_Patching]] due to [[CONSTRAINT:Security_Requirements]]
- [[CONSTRAINT:Real-Time_Control_Requirements]] limit [[ACTIVITY:Security_Updates]]
- [[WEAKNESS:Legacy_OS_Versions]] often deployed
- [[WEAKNESS:Unpatched_Vulnerabilities]] common

### Attack Vectors
1. [[TECHNIQUE:Exploitation_of_Unpatched_Commercial_Software]]
   - [[VULNERABILITY:Windows_XP]] or [[VULNERABILITY:Windows_7]] still deployed
   - [[VULNERABILITY:Legacy_Linux_Kernels]] with known exploits
   - [[VULNERABILITY:Outdated_Network_Services]]

2. [[TECHNIQUE:Targeting_Underlying_Operating_Systems]]
   - [[TECHNIQUE:MITRE_ATT&CK:T1068]] - Exploitation for Privilege Escalation
   - [[TECHNIQUE:MITRE_ATT&CK:T1210]] - Exploitation of Remote Services

3. [[TECHNIQUE:Wireless_Communication_Interception]]
   - [[PROTOCOL:Wi-Fi]] or [[PROTOCOL:Proprietary_Wireless]] vulnerabilities
   - [[TECHNIQUE:Packet_Injection]]
   - [[TECHNIQUE:Replay_Attacks]]

4. [[TECHNIQUE:Real-Time_Control_Protocol_Manipulation]]
   - [[PROTOCOL:Custom_Control_Protocols]] often lack authentication
   - [[TECHNIQUE:Command_Injection]]
   - [[TECHNIQUE:Timing_Manipulation]]

---

## Computer-Based Interlocking (CBI) Vulnerabilities

### Critical Risk Profile
[[SYSTEM:CBI]] systems prevent [[HAZARD:Conflicting_Train_Routes]]. Compromise enables:

1. [[ATTACK:Switch_Manipulation_While_Train_Passing]]
   - [[CONSEQUENCE:Derailment_Risk]] (HIGH)
   - [[IMPACT:Infrastructure_Damage]]
   - [[IMPACT:Mass_Casualty_Potential]]

2. [[ATTACK:Conflicting_Route_Setup]]
   - [[CONSEQUENCE:Train_Collision_Risk]] (CRITICAL)
   - [[IMPACT:Multi-Train_Incident]]
   - [[IMPACT:Catastrophic_Failure]]

3. [[ATTACK:Physical_Damage_to_Infrastructure]]
   - [[IMPACT:Track_Damage]]
   - [[IMPACT:Signal_Equipment_Destruction]]
   - [[IMPACT:Switch_Mechanism_Failure]]

### Safety-Critical Nature
[[SYSTEM:CBI]] is [[CLASSIFICATION:Safety-Integrity_Level_4]] (SIL-4):
- [[REQUIREMENT:Probability_of_Dangerous_Failure]] < 10^-9 per hour
- [[REQUIREMENT:Formal_Verification]] of logic
- [[REQUIREMENT:Redundancy]] and [[REQUIREMENT:Diversity]]
- [[REQUIREMENT:Fail-Safe_Defaults]]

### Attack Surface
**Entry Points:**
- [[INTERFACE:Maintenance_Terminal_Connections]]
- [[INTERFACE:Network_Links_to_Traffic_Management]]
- [[INTERFACE:Data_Links_to_Adjacent_Interlockings]]
- [[INTERFACE:SCADA_Integration_Points]]

**Exploitation Paths:**
- [[TECHNIQUE:Maintenance_Password_Compromise]]
- [[TECHNIQUE:Network_Segmentation_Bypass]]
- [[TECHNIQUE:PLC_Firmware_Modification]]
- [[TECHNIQUE:Configuration_File_Tampering]]

### TTPs for CBI Compromise
- [[TECHNIQUE:MITRE_ATT&CK:T1542.001]] - System Firmware
- [[TECHNIQUE:MITRE_ATT&CK:T1601.001]] - Patch System Image
- [[TECHNIQUE:MITRE_ATT&CK:T1205.002]] - Traffic Signaling (literal)
- [[TECHNIQUE:MITRE_ATT&CK:T1565.001]] - Stored Data Manipulation

---

## Vulnerability Summary Matrix

| [[VULNERABILITY:CVE]] | [[SYSTEM]] | [[CVSS]] | [[EXPLOIT_DIFFICULTY]] | [[MITIGATION_STATUS]] |
|---|---|---|---|---|
| [[VULNERABILITY:CVE-2025-1727]] | EOT/HOT | 8.1 | LOW | No fix planned (2027) |
| [[VULNERABILITY:CVE-2022-38773]] | S7-1500 | 4.6 | MEDIUM | Patch available |
| [[VULNERABILITY:CVE-2022-38465]] | S7-1500 | 9.3 | HIGH | Patch available |
| [[VULNERABILITY:CVE-2015-5374]] | S7-300 | N/A | MEDIUM | Patch available (old) |
| [[VULNERABILITY:ETCS_Auth]] | ETCS | N/A | HIGH | No fix (protocol-level) |
| [[VULNERABILITY:GSM-R]] | Railway Comms | N/A | MEDIUM | Replacement (FRMCS) |
| [[VULNERABILITY:Balise_Jam]] | ETCS | N/A | LOW | No fix (physical) |

---

## Mitigation Strategies by Vulnerability Class

### Protocol-Level Vulnerabilities (No Patch)
- [[MITIGATION:Protocol_Replacement]] ([[PROTOCOL:GSM-R]] → [[PROTOCOL:FRMCS]])
- [[MITIGATION:Hardware_Replacement]] ([[DEVICE:EOT_HOT]] → authenticated systems)
- [[MITIGATION:Compensating_Controls]] (monitoring, detection)
- [[MITIGATION:Operational_Procedures]] (manual verification)

### Firmware Vulnerabilities (Patchable)
- [[MITIGATION:Immediate_Patching]] of [[VULNERABILITY:CVE-2022-38773]], [[VULNERABILITY:CVE-2022-38465]]
- [[MITIGATION:Firmware_Integrity_Monitoring]]
- [[MITIGATION:Secure_Boot_Configuration]]
- [[MITIGATION:Access_Control_Hardening]]

### Legacy System Vulnerabilities
- [[MITIGATION:Network_Isolation]] of [[PRODUCT:S7-300]] PLCs
- [[MITIGATION:Virtual_Patching]] via IDS/IPS
- [[MITIGATION:Replacement_Roadmap]] planning
- [[MITIGATION:Enhanced_Monitoring]] for legacy devices

### Wireless Communication Vulnerabilities
- [[MITIGATION:Encryption_Upgrade]] (modern algorithms)
- [[MITIGATION:Mutual_Authentication]]
- [[MITIGATION:Jamming_Detection]]
- [[MITIGATION:Spectrum_Monitoring]]
