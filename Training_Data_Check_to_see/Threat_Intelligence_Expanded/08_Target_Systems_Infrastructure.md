# Target Systems and Railway Infrastructure

## Railway Control Systems

### [[SYSTEM:European_Train_Control_System]] (ETCS)

**Classification:** [[TYPE:Signaling_and_Control_System]]
**Standard:** [[STANDARD:ERTMS_Component]]
**Design Era:** [[ERA:1990s]]
**Security Posture:** [[STATUS:Outdated_Security_Measures]]

#### System Components

**[[COMPONENT:Onboard_Equipment]]:**
- [[DEVICE:European_Vital_Computer]] (EVC)
- [[DEVICE:Balise_Transmission_Module]] (BTM)
- [[DEVICE:GSM-R_Radio_Module]]
- [[DEVICE:Driver_Machine_Interface]] (DMI)
- [[DEVICE:Juridical_Recording_Unit]] (JRU)

**[[COMPONENT:Trackside_Equipment]]:**
- [[DEVICE:Balises]] (position markers)
- [[DEVICE:Euroloop]] (continuous positioning)
- [[DEVICE:Radio_Block_Center]] (RBC)
- [[DEVICE:LEU]] (Lineside Electronic Unit)

**[[COMPONENT:Control_Centers]]:**
- [[FACILITY:Traffic_Management_System]]
- [[FACILITY:Radio_Block_Center]]
- [[FACILITY:Interlocking_Systems]]

#### Vulnerabilities

**[[VULNERABILITY:Authentication_Weaknesses]]:**
- [[WEAKNESS:Plaintext_Random_Numbers]] in [[PROTOCOL:EuroRadio]]
- [[ATTACK:Collision_Attack_Possible]]
- [[WEAKNESS:Design_Flaws]] enable [[TECHNIQUE:Message_Forgery]]

**[[VULNERABILITY:GSM-R_Communication_Flaws]]:**
- [[ALGORITHM:A5-1_Encryption]] - [[STATUS:Cryptographically_Broken]]
- [[WEAKNESS:No_End-to-End_Protection]]
- [[VULNERABILITY:Man-in-the-Middle_Susceptible]]
- [[VULNERABILITY:OTA_Firmware_Updates]] exploitable

**[[VULNERABILITY:Balise_System]]:**
- [[VULNERABILITY:Sensitive_to_Jamming]]
- [[WEAKNESS:No_Cyber_Attack_Design_Consideration]]
- [[VULNERABILITY:MVB_Interception]] possible
- [[VULNERABILITY:MVB_Spoofing]] achievable

#### Attack Scenarios

**Scenario 1: [[ATTACK:Authentication_Bypass]]**
1. [[TECHNIQUE:Traffic_Capture]] of [[PROTOCOL:EuroRadio]] authentication
2. [[TECHNIQUE:Random_Number_Collection]]
3. [[TECHNIQUE:MAC_Collision_Detection]]
4. [[TECHNIQUE:Message_Forgery]]
5. [[IMPACT:Unauthorized_Train_Control]]

**Scenario 2: [[ATTACK:GSM-R_MITM]]**
1. [[TOOL:Rogue_Base_Station]] deployment
2. [[TECHNIQUE:A5-1_Real-Time_Decryption]]
3. [[TECHNIQUE:Message_Interception]]
4. [[TECHNIQUE:Command_Modification]]
5. [[IMPACT:Train_Control_Manipulation]]

**Scenario 3: [[ATTACK:Balise_Jamming]]**
1. [[TECHNIQUE:RF_Interference]] on balise frequency
2. [[IMPACT:Position_Data_Loss]]
3. [[IMPACT:Degraded_Operation_Mode]]
4. [[RISK:Safety_Margin_Reduction]]

#### Safety-Critical Nature
- [[CLASSIFICATION:SIL-4]] (Safety Integrity Level 4)
- [[REQUIREMENT:Fail-Safe_Defaults]]
- [[REQUIREMENT:Redundancy]]
- [[CONSEQUENCE:Collision_Risk]] if compromised

---

### [[SYSTEM:Communication-Based_Train_Control]] (CBTC)

**Classification:** [[TYPE:Automatic_Train_Control]]
**Technology:** [[TECH:Wireless_Communication_Based]]
**Deployment:** [[DEPLOYMENT:Urban_Transit_Systems]]

#### System Architecture

**[[COMPONENT:Wayside_Equipment]]:**
- [[DEVICE:Zone_Controllers]]
- [[DEVICE:Access_Points]] (wireless)
- [[DEVICE:Object_Controllers]]
- [[DEVICE:Interlocking_Interfaces]]

**[[COMPONENT:Onboard_Equipment]]:**
- [[DEVICE:Vehicle_Onboard_Controller]] (VOBC)
- [[DEVICE:Wireless_Communication_Module]]
- [[DEVICE:Odometry_Systems]]
- [[DEVICE:Train_Detection_Systems]]

**[[COMPONENT:Central_Systems]]:**
- [[SYSTEM:Automatic_Train_Supervision]] (ATS)
- [[SYSTEM:Data_Communication_System]]
- [[SYSTEM:Centralized_Traffic_Control]]

#### Characteristics Creating Vulnerability

**[[WEAKNESS:Off-the-Shelf_Software]]:**
- [[PLATFORM:Windows]] or [[PLATFORM:Linux]] base
- [[ISSUE:Known_Vulnerabilities_Present]]
- [[CHALLENGE:Difficult_to_Patch]]
- [[CONSTRAINT:Real-Time_Requirements]]

**[[WEAKNESS:Commercial_Operating_Systems]]:**
- [[OS:Windows_Embedded]]
- [[OS:Linux_Distributions]]
- [[ISSUE:Legacy_OS_Versions]]
- [[ISSUE:Unpatched_Systems]]

#### Attack Vectors

**[[VECTOR:Unpatched_Software_Exploitation]]:**
- [[VULNERABILITY:Windows_XP]] still deployed
- [[VULNERABILITY:Windows_7]] common
- [[VULNERABILITY:Legacy_Linux_Kernels]]

**[[VECTOR:Wireless_Communication_Interception]]:**
- [[PROTOCOL:Wi-Fi]] vulnerabilities
- [[PROTOCOL:Proprietary_Wireless]] weaknesses
- [[TECHNIQUE:Packet_Injection]]
- [[TECHNIQUE:Replay_Attacks]]

**[[VECTOR:Control_Protocol_Manipulation]]:**
- [[WEAKNESS:Lack_of_Authentication]]
- [[TECHNIQUE:Command_Injection]]
- [[TECHNIQUE:Timing_Manipulation]]

#### Target Value
- [[DEPLOYMENT:High-Traffic_Urban_Transit]]
- [[IMPACT:Mass_Transit_Disruption]]
- [[IMPACT:Safety_Risk]]
- [[IMPACT:Economic_Impact]]

---

### [[SYSTEM:Computer-Based_Interlocking]] (CBI)

**Classification:** [[TYPE:Safety-Critical_Control]]
**Function:** [[PURPOSE:Prevent_Conflicting_Routes]]
**Safety Level:** [[CLASSIFICATION:SIL-4]]

#### Critical Function
[[SYSTEM:CBI]] prevents:
- [[HAZARD:Train_Collisions]]
- [[HAZARD:Derailments]]
- [[HAZARD:Switch_Conflicts]]
- [[HAZARD:Signal_Conflicts]]

#### System Components

**[[COMPONENT:Processing_Units]]:**
- [[DEVICE:Vital_Processors]] (redundant)
- [[DEVICE:Safety_PLCs]]
- [[DEVICE:Fail-Safe_Computers]]

**[[COMPONENT:Input_Systems]]:**
- [[DEVICE:Track_Circuits]]
- [[DEVICE:Axle_Counters]]
- [[DEVICE:Signal_Status_Inputs]]
- [[DEVICE:Switch_Position_Detectors]]

**[[COMPONENT:Output_Systems]]:**
- [[DEVICE:Signal_Controls]]
- [[DEVICE:Switch_Motors]]
- [[DEVICE:Level_Crossing_Gates]]
- [[DEVICE:Track_Circuit_Transmitters]]

#### Attack Surface

**[[INTERFACE:Maintenance_Terminal]]:**
- [[ACCESS:Engineering_Workstations]]
- [[ACCESS:Configuration_Tools]]
- [[VULNERABILITY:Weak_Authentication]]
- [[VULNERABILITY:Network_Connectivity]]

**[[INTERFACE:Network_Connections]]:**
- [[CONNECTION:Traffic_Management_Links]]
- [[CONNECTION:Adjacent_Interlocking_Interfaces]]
- [[CONNECTION:SCADA_Integration]]
- [[VULNERABILITY:Poor_Segmentation]]

**[[INTERFACE:Data_Interfaces]]:**
- [[PROTOCOL:Proprietary_Protocols]]
- [[PROTOCOL:Standard_Industrial_Protocols]]
- [[WEAKNESS:Limited_Encryption]]

#### Exploitation Consequences

**[[ATTACK:Switch_Manipulation_During_Passage]]:**
- [[CONSEQUENCE:Derailment_Risk]] - [[SEVERITY:CRITICAL]]
- [[IMPACT:Infrastructure_Damage]]
- [[IMPACT:Mass_Casualty_Potential]]

**[[ATTACK:Conflicting_Route_Setup]]:**
- [[CONSEQUENCE:Train_Collision]] - [[SEVERITY:CATASTROPHIC]]
- [[IMPACT:Multi-Train_Incident]]
- [[IMPACT:System-Wide_Failure]]

**[[ATTACK:Signal_State_Manipulation]]:**
- [[CONSEQUENCE:Unexpected_Train_Movement]]
- [[IMPACT:Collision_Risk]]
- [[IMPACT:Safety_System_Compromise]]

#### Defense Requirements
- [[DEFENSE:Physical_Security]] of cabinets
- [[DEFENSE:Network_Segmentation]]
- [[DEFENSE:Access_Control]]
- [[DEFENSE:Integrity_Monitoring]]
- [[DEFENSE:Formal_Verification]]

---

## Railway SCADA Systems

### [[SYSTEM:Supervisory_Control_and_Data_Acquisition]]

**Function:** [[PURPOSE:Railway_Infrastructure_Monitoring]]
**Coverage:** [[SCOPE:Network-Wide_Operations]]

#### Monitored Systems
- [[MONITORED:Electric_Traction_Power]]
- [[MONITORED:Tunnel_Ventilation]]
- [[MONITORED:Platform_Systems]]
- [[MONITORED:Environmental_Monitoring]]
- [[MONITORED:Security_Systems]]
- [[MONITORED:Passenger_Information]]

#### SCADA Architecture

**[[LAYER:Control_Center]]:**
- [[COMPONENT:HMI_Workstations]]
- [[COMPONENT:SCADA_Servers]]
- [[COMPONENT:Historians]]
- [[COMPONENT:Engineering_Workstations]]

**[[LAYER:Communication]]:**
- [[NETWORK:Wide_Area_Network]]
- [[NETWORK:Control_Network]]
- [[NETWORK:Field_Network]]

**[[LAYER:Field_Devices]]:**
- [[DEVICE:PLCs]] (Programmable Logic Controllers)
- [[DEVICE:RTUs]] (Remote Terminal Units)
- [[DEVICE:IEDs]] (Intelligent Electronic Devices)
- [[DEVICE:Sensors_and_Actuators]]

#### Common Vulnerabilities

**[[VULNERABILITY:Web_Application_Flaws]] (67% of attacks):**
- [[EXPLOIT:SQL_Injection]] against [[COMPONENT:HMI_Interfaces]]
- [[EXPLOIT:Arbitrary_File_Upload]]
- [[EXPLOIT:Remote_Command_Execution]]
- [[EXPLOIT:Cross-Site_Scripting]]

**[[VULNERABILITY:Protocol_Weaknesses]]:**
- [[PROTOCOL:Modbus_TCP/IP]] - [[WEAKNESS:Unencrypted]]
- [[PROTOCOL:DNP3]] - [[WEAKNESS:Limited_Authentication]]
- [[PROTOCOL:IEC_60870-5-104]] - [[VULNERABILITY:Replay_Attacks]]

**[[VULNERABILITY:Configuration_Flaws]] (67% penetration rate):**
- [[ISSUE:Poor_Network_Segmentation]]
- [[ISSUE:Default_Credentials]]
- [[ISSUE:Exposed_Services]]
- [[ISSUE:Corporate-to-ICS_Bridges]]

#### Attack Paths

**Path 1: [[PATH:Web_Application_to_SCADA]]**
1. [[EXPLOIT:SQL_Injection]] on [[COMPONENT:HMI_Web_Interface]]
2. [[TECHNIQUE:Web_Shell_Upload]]
3. [[TECHNIQUE:Lateral_Movement]] to [[COMPONENT:SCADA_Server]]
4. [[IMPACT:Full_SCADA_Control]]

**Path 2: [[PATH:Corporate_Network_Bridge]]**
1. [[TECHNIQUE:Phishing]] on [[NETWORK:Corporate_Network]]
2. [[TECHNIQUE:Lateral_Movement]] to [[NETWORK:ICS_Network]]
3. [[EXPLOIT:Configuration_Weakness]] exploitation
4. [[ACCESS:SCADA_System_Compromise]]

**Path 3: [[PATH:Search_Engine_Discovery]]**
1. [[TOOL:Shodan]] discovery of exposed [[DEVICE:PLC]]
2. [[ACCESS:Direct_Internet_Access]]
3. [[EXPLOIT:Default_Credentials]]
4. [[IMPACT:Remote_Control]]

---

## Specific Vendor Systems

### [[VENDOR:Siemens]] Systems

#### [[PRODUCT:SIMATIC_S7-1500]] PLC

**Deployment:** [[APPLICATION:Railway_Interlocking]], [[APPLICATION:Signaling]]

**Known Vulnerabilities:**
- [[VULNERABILITY:CVE-2022-38773]] - Protected Boot Bypass
- [[VULNERABILITY:CVE-2022-38465]] - Global Private Key Extraction
- [[VULNERABILITY:CVE-2023-6932]] - Linux kernel (used in S7-1500)

**Impact if Compromised:**
- [[SYSTEM:Computer-Based_Interlocking]] compromise
- [[SYSTEM:SIMIS_W_Interlocking]] failure
- [[SYSTEM:Track_Circuit_Controls]] manipulation
- [[SYSTEM:Signal_Automation]] disruption

#### [[PRODUCT:SIMATIC_S7-300]] PLC

**Status:** [[STATUS:Legacy_System]]
**Vulnerability:** [[VULNERABILITY:CVE-2015-5374]] - Remote Code Execution

**Deployment:**
- [[SYSTEM:Legacy_Signaling]]
- [[SYSTEM:Older_Interlocking]]
- [[SYSTEM:Non-Critical_Controls]]

**Risk:** [[RISK:HIGH]] - 10+ year old vulnerability, many unpatched

---

### [[VENDOR:Alstom]] Systems

**Railway Solutions:**
- [[PRODUCT:ETCS_Onboard_Equipment]]
- [[PRODUCT:Interlocking_Systems]]
- [[PRODUCT:Traffic_Management_Systems]]

**Vulnerability Disclosure:** [[STATUS:Limited_Public_Information]]

---

### [[VENDOR:Hitachi_Rail]] Systems

**Target Systems:**
- [[PRODUCT:Rail_Signaling_Systems]]
- [[PRODUCT:Traffic_Management]]
- [[PRODUCT:Communication_Systems]]

---

### [[VENDOR:Wabtec]] Systems

**EOT/HOT Equipment:**
- [[PRODUCT:End-of-Train_Devices]]
- [[PRODUCT:Head-of-Train_Devices]]
- **Critical Vulnerability:** [[VULNERABILITY:CVE-2025-1727]]

---

## Communication Systems

### [[SYSTEM:GSM-R]] (GSM for Railways)

**Function:** [[PURPOSE:Railway_Voice_and_Data_Communication]]
**Standard:** [[STANDARD:ERTMS_Component]]
**Status:** [[STATUS:Being_Replaced]] by [[SYSTEM:FRMCS]]

#### Technical Specifications
- **Frequency:** 876-880 MHz (uplink), 921-925 MHz (downlink)
- **Technology:** [[TECH:GSM_Based]] (2G)
- **Encryption:** [[ALGORITHM:A5-1]] (broken)

#### Vulnerabilities

**[[VULNERABILITY:A5-1_Encryption]]:**
- [[STATUS:Cryptographically_Broken]]
- [[TECHNIQUE:Real-Time_Decryption]] possible
- [[TOOL:Kraken]] can break in [[TIME:Minutes]]

**[[VULNERABILITY:Unilateral_Authentication]]:**
- Network authenticates to phone
- Phone doesn't authenticate network
- [[ATTACK:Rogue_Base_Station]] possible

**[[VULNERABILITY:OTA_Firmware_Updates]]:**
- [[TECHNIQUE:Malicious_Update_Injection]]
- [[TECHNIQUE:Modem_Compromise]]
- [[TECHNIQUE:Persistent_Backdoor]]

#### Attack Capabilities
- [[ATTACK:Jamming]] - Network-wide disruption
- [[ATTACK:MITM]] - Traffic interception/modification
- [[ATTACK:IMSI_Catching]] - Device identification
- [[ATTACK:Location_Tracking]]

**Attack Impact:**
- [[IMPACT:Train-to-Control_Communication_Loss]]
- [[IMPACT:Voice_Call_Disruption]]
- [[IMPACT:Data_Service_Failure]]
- [[IMPACT:Automatic_Train_Control_Degradation]]

---

### [[SYSTEM:RADIOSTOP]] (Poland)

**Type:** [[TYPE:Analog_Radio_Emergency_Stop]]
**Frequency:** [[FREQUENCY:~150_MHz]]
**Status:** [[STATUS:Legacy_Being_Replaced]]

#### Characteristics
- [[WEAKNESS:No_Encryption]]
- [[WEAKNESS:No_Authentication]]
- [[TRIGGER:Tone-Sequence]] activation
- [[SKILL:Low_Exploitation_Complexity]]

#### Exploitation
**Requirements:**
- [[TOOL:Basic_Radio_Transmitter]] ($50-$500)
- [[KNOWLEDGE:Tone_Sequence]] (public)
- [[ACCESS:Physical_Proximity]]

**Impact:**
- [[IMPACT:Emergency_Brake_Activation]]
- [[IMPACT:Service_Disruption]]
- [[IMPACT:Network-Wide_Effect]]

**Real-World:** [[INCIDENT:Poland_August_2023]] - 20+ trains stopped

---

## Enterprise Systems

### [[SYSTEM:Ticketing_Platforms]]

**Function:** [[PURPOSE:Passenger_Ticketing_Revenue_Management]]
**Connectivity:** [[NETWORK:Internet-Facing]]

#### Components
- [[COMPONENT:Web_Frontend]]
- [[COMPONENT:Application_Servers]]
- [[COMPONENT:Database_Servers]]
- [[COMPONENT:Payment_Processing]]
- [[COMPONENT:Mobile_Applications]]

#### Attack Vectors
- [[VECTOR:Web_Application_Vulnerabilities]]
- [[VECTOR:Database_Injection]]
- [[VECTOR:Payment_Card_Data_Theft]]
- [[VECTOR:Customer_Data_Breach]]

**Recent Incidents:**
- [[INCIDENT:Transport_for_London]] - 5000+ bank accounts
- [[INCIDENT:Ukrzaliznytsia]] - Ticketing wiper attack

---

### [[SYSTEM:Fleet_Management_Systems]]

**Function:** [[PURPOSE:Train_Fleet_Tracking_Maintenance]]

#### Data Managed
- [[DATA:Train_Locations]]
- [[DATA:Maintenance_Schedules]]
- [[DATA:Asset_Inventory]]
- [[DATA:Performance_Metrics]]
- [[DATA:Crew_Assignments]]

#### Threat Actor Interest
- [[ACTOR:Volt_Typhoon]] - [[OBJECTIVE:Logistics_Intelligence]]
- [[ACTOR:APT41]] - [[OBJECTIVE:Operational_Data]]
- [[ACTOR:Salt_Typhoon]] - [[OBJECTIVE:Fleet_Communications]]

---

### [[SYSTEM:Enterprise_Asset_Management]]

**Function:** [[PURPOSE:Maintenance_Work_Order_Management]]

#### Supply Chain Risk
**[[INCIDENT:Danish_Railways_2022]]:**
- [[VENDOR:Supeo]] EAM platform compromised
- [[IMPACT:Train_Driver_Software_Failure]]
- [[IMPACT:Network-Wide_Disruptions]]

**Lesson:** [[RISK:Third-Party_Software]] creates [[VULNERABILITY:Cascading_Risk]]

---

## Target System Priority Matrix

| [[SYSTEM]] | [[SAFETY_CRITICALITY]] | [[ACCESSIBILITY]] | [[THREAT_ACTOR_INTEREST]] | [[OVERALL_RISK]] |
|---|---|---|---|---|
| [[SYSTEM:CBI]] | CRITICAL | LOW | HIGH | CRITICAL |
| [[SYSTEM:ETCS]] | CRITICAL | MEDIUM | HIGH | CRITICAL |
| [[SYSTEM:CBTC]] | CRITICAL | MEDIUM | MEDIUM | HIGH |
| [[SYSTEM:SCADA]] | HIGH | MEDIUM | HIGH | HIGH |
| [[SYSTEM:GSM-R]] | HIGH | HIGH | HIGH | HIGH |
| [[SYSTEM:Ticketing]] | LOW | HIGH | MEDIUM | MEDIUM |
| [[SYSTEM:Fleet_Management]] | MEDIUM | MEDIUM | MEDIUM | MEDIUM |
| [[SYSTEM:EAM]] | MEDIUM | MEDIUM | HIGH | HIGH |

---

## Geographic Vulnerability Distribution

### [[GEOGRAPHY:United_States]]
- [[VULNERABILITY:CVE-2025-1727]] - EOT/HOT unpatched
- [[VULNERABILITY:Legacy_Systems]] widespread
- [[TARGET:Freight_Rail_Networks]]
- [[TARGET:Commuter_Rail_Systems]]

### [[GEOGRAPHY:Europe]]
- [[VULNERABILITY:ETCS_Protocol_Weaknesses]]
- [[VULNERABILITY:GSM-R_Deployment]]
- [[SYSTEM:Cross-Border_Operations]] complexity

### [[GEOGRAPHY:Poland]]
- [[VULNERABILITY:RADIOSTOP_Analog_System]]
- [[STATUS:Migration_to_GSM-R_Ongoing]]

### [[GEOGRAPHY:Ukraine]]
- [[THREAT:Active_Cyber_Warfare]]
- [[THREAT:Physical_and_Cyber_Combined]]
- [[THREAT:State-Sponsored_Attacks]]

---

## Interconnected Systems Risk

### [[RISK:Cascading_Failures]]

**Scenario:** [[ATTACK:SCADA_Compromise]]
- [[IMPACT:Traction_Power_Loss]] → [[IMPACT:Train_Stoppages]]
- [[IMPACT:Tunnel_Ventilation_Failure]] → [[IMPACT:Passenger_Safety]]
- [[IMPACT:Signaling_Disruption]] → [[IMPACT:Network_Paralysis]]

### [[RISK:OT-IT_Convergence]]

**Vulnerability:** [[WEAKNESS:Corporate_to_Control_System_Bridges]]
- [[PATH:Email_Phishing]] → [[PATH:Corporate_Network]] → [[PATH:ICS_Network]] → [[PATH:Control_Systems]]

### [[RISK:Supply_Chain_Dependencies]]

**Single Points of Failure:**
- [[VENDOR:Critical_Software_Providers]]
- [[VENDOR:Maintenance_Service_Providers]]
- [[VENDOR:Cloud_Service_Providers]]

**Impact:** [[INCIDENT:Danish_Railways]] - Single vendor compromise affects national network
