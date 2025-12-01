# Attack Vectors and Exploitation Techniques

## Wireless Communication Attacks

### [[ATTACK_VECTOR:GSM-R_Network_Exploitation]]

#### Vulnerability Characteristics
[[PROTOCOL:GSM-R]] inherited [[PROTOCOL:GSM]] protocol weaknesses from [[ERA:1990s_Design]]:
- [[ALGORITHM:A5-1_Encryption]] - [[STATUS:Cryptographically_Broken]]
- [[WEAKNESS:No_End-to-End_Encryption]] (only MS to BS)
- [[VULNERABILITY:Over-the-Air_Firmware_Updates]] exploitable
- [[WEAKNESS:Unilateral_Authentication]]

#### Attack Scenarios

**[[ATTACK:Jamming_Attack]]:**
- [[TECHNIQUE:Powerful_RF_Interference]] disables [[PROTOCOL:GSM-R]] links network-wide
- [[TOOL:SDR]] or [[TOOL:Commercial_Jammer]] deployment
- [[IMPACT:Train-to-Control_Communication_Loss]]
- [[CONSEQUENCE:Automatic_Train_Control_System_Failure]]

**Technical Implementation:**
1. [[TECHNIQUE:Frequency_Identification]] - Locate [[PROTOCOL:GSM-R]] frequencies (876-880 MHz uplink, 921-925 MHz downlink)
2. [[TECHNIQUE:Power_Amplification]] - Deploy [[TOOL:High-Power_Transmitter]]
3. [[TECHNIQUE:Broadband_Noise_Generation]]
4. [[IMPACT:Network-Wide_GSM-R_Disruption]]

**[[ATTACK:Man-in-the-Middle]]:**
- [[TECHNIQUE:Rogue_Base_Station_Deployment]] ([[TOOL:IMSI_Catcher]])
- [[TECHNIQUE:A5-1_Decryption]] using [[TOOL:Kraken]] or [[TOOL:Rainbow_Tables]]
- [[TECHNIQUE:Traffic_Interception_and_Manipulation]]
- [[TECHNIQUE:Command_Injection]]

**Attack Chain:**
1. [[TECHNIQUE:Rogue_BTS_Setup]] using [[TOOL:OpenBTS]] or commercial [[TOOL:IMSI_Catcher]]
2. [[TECHNIQUE:Target_Train_Modem_Attraction]] (signal strength manipulation)
3. [[TECHNIQUE:Authentication_Relay]] to legitimate network
4. [[TECHNIQUE:A5-1_Real-Time_Decryption]]
5. [[TECHNIQUE:Command_Modification]] or [[TECHNIQUE:Message_Injection]]
6. [[IMPACT:Train_Control_Compromise]]

**[[ATTACK:Firmware_Compromise]]:**
- [[TECHNIQUE:Malicious_OTA_Update_Injection]]
- [[TECHNIQUE:Train_Control_Modem_Hijacking]]
- [[TECHNIQUE:Persistent_Backdoor_Installation]]

**Implementation:**
1. [[TECHNIQUE:OTA_Update_Protocol_Reverse_Engineering]]
2. [[TECHNIQUE:Malicious_Firmware_Development]]
3. [[TECHNIQUE:Rogue_Update_Server_Deployment]]
4. [[TECHNIQUE:Update_Packet_Injection]]
5. [[IMPACT:Permanent_Modem_Compromise]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1200]] - Hardware Additions (SDR, jammer)
- [[TECHNIQUE:MITRE_ATT&CK:T1557.002]] - ARP Cache Poisoning (network MITM)
- [[TECHNIQUE:MITRE_ATT&CK:T1499.002]] - Service Exhaustion Flood (jamming)
- [[TECHNIQUE:MITRE_ATT&CK:T1542.001]] - System Firmware (OTA exploitation)
- [[TECHNIQUE:MITRE_ATT&CK:T1600]] - Weaken Encryption (A5/1 attack)

---

### [[ATTACK_VECTOR:RADIOSTOP_System_Exploitation]]

#### System Characteristics
- [[PROTOCOL:Analog_Radio-Based]] emergency stop system
- [[FREQUENCY:150_MHz]] range
- [[WEAKNESS:No_Encryption]]
- [[WEAKNESS:No_Authentication]]
- [[TRIGGER:Tone-Sequence_Activated_Braking]]

#### Exploitation Requirements
- [[TOOL:Basic_Radio_Transmitter]] ($50-$500)
- [[KNOWLEDGE:Tone_Sequence]] (publicly available)
- [[ACCESS:Physical_Proximity]] to rail lines
- [[SKILL_LEVEL:Low]] - No technical sophistication required

#### Attack Implementation
1. [[TOOL:Commercial_Radio_Purchase]] (e.g., Baofeng UV-5R)
2. [[CONFIGURATION:Frequency_Programming]] to [[FREQUENCY:150_MHz]]
3. [[TECHNIQUE:Tone_Sequence_Transmission]]
4. [[IMPACT:Emergency_Brake_Activation]]

#### Geographic Vulnerability
- [[GEOGRAPHY:Poland]] (legacy systems)
- [[GEOGRAPHY:Eastern_European_Rail_Networks]]
- [[GEOGRAPHY:Other_Legacy_Systems]] worldwide

#### Real-World Incident
**[[INCIDENT:Poland_Railway_Radio_Sabotage]]** (August 2023):
- **August 25:** 20+ trains affected near [[LOCATION:Szczecin]]
- **August 26:** Freight trains near [[LOCATION:Gdynia]]
- **August 27:** 5 passenger, 1 freight near [[LOCATION:Białystok]]
- **Psychological Ops:** [[PROPAGANDA:Russian_National_Anthem]], [[PROPAGANDA:Putin_Speeches]]
- **Attribution:** [[THREAT_ACTOR:Russian_Belarusian_State_Actors]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1200]] - Hardware Additions (radio transmitter)
- [[TECHNIQUE:MITRE_ATT&CK:T1499]] - Endpoint Denial of Service (emergency stop)
- [[TECHNIQUE:MITRE_ATT&CK:T1078.004]] - Cloud Accounts (if remote control)

---

## SCADA Network Attack Vectors

### [[ATTACK_VECTOR:Web_Application_Vulnerabilities]]

**Prevalence:** [[STATISTIC:67%_of_Attacks]] target web applications

#### Common Exploits Against [[SYSTEM:SCADA_HMI]]

**[[ATTACK:SQL_Injection]]:**
- [[TARGET:HMI_Web_Interfaces]]
- [[TECHNIQUE:Database_Query_Manipulation]]
- [[IMPACT:Unauthorized_Data_Access]]
- [[IMPACT:Authentication_Bypass]]

**Example Attack:**
```sql
-- [[TECHNIQUE:SQL_Injection_Authentication_Bypass]]
username: admin' OR '1'='1'--
password: [anything]
-- Result: [[IMPACT:Unauthorized_HMI_Access]]
```

**[[ATTACK:Arbitrary_File_Upload]]:**
- [[TECHNIQUE:Malicious_File_Upload]] to [[TARGET:HMI_Server]]
- [[TECHNIQUE:Web_Shell_Deployment]]
- [[TECHNIQUE:Remote_Command_Execution]]

**Attack Chain:**
1. [[TECHNIQUE:Upload_PHP_Web_Shell]] disguised as image
2. [[TECHNIQUE:File_Extension_Bypass]] (.php.jpg)
3. [[TECHNIQUE:Web_Shell_Access]] via browser
4. [[IMPACT:Full_Server_Control]]

**[[ATTACK:Remote_Command_Execution]]:**
- [[TECHNIQUE:OS_Command_Injection]] in [[COMPONENT:HMI_Parameters]]
- [[TECHNIQUE:Arbitrary_System_Commands]]
- [[IMPACT:SCADA_Server_Compromise]]

**[[ATTACK:Cross-Site_Scripting]]:**
- [[TECHNIQUE:XSS_Injection]] into [[COMPONENT:Operator_Dashboards]]
- [[TECHNIQUE:Credential_Theft]] via [[TECHNIQUE:Session_Hijacking]]
- [[TECHNIQUE:Operator_Workstation_Compromise]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1190]] - Exploit Public-Facing Application
- [[TECHNIQUE:MITRE_ATT&CK:T1505.003]] - Web Shell
- [[TECHNIQUE:MITRE_ATT&CK:T1059]] - Command and Scripting Interpreter
- [[TECHNIQUE:MITRE_ATT&CK:T1055]] - Process Injection

---

### [[ATTACK_VECTOR:Protocol_Weaknesses]]

#### [[PROTOCOL:Modbus_TCP/IP]] Exploitation

**Design Weaknesses:**
- [[WEAKNESS:Unencrypted_by_Design]]
- [[WEAKNESS:No_Authentication]]
- [[WEAKNESS:Cleartext_Commands]]

**Attack Techniques:**
1. [[TECHNIQUE:Function_Code_Manipulation]]
   - [[FUNCTION_CODE:0x05]] - Force Single Coil (outputs)
   - [[FUNCTION_CODE:0x06]] - Preset Single Register (control values)
   - [[FUNCTION_CODE:0x0F]] - Force Multiple Coils
   - [[FUNCTION_CODE:0x10]] - Preset Multiple Registers

2. [[TECHNIQUE:Register_Value_Modification]]
   - [[TARGET:Setpoint_Values]]
   - [[TARGET:Control_Parameters]]
   - [[TARGET:Safety_Thresholds]]

3. [[TECHNIQUE:Network_Traffic_Interception]]
   - [[TOOL:Wireshark]] for [[TECHNIQUE:Packet_Capture]]
   - [[TECHNIQUE:Command_Replay]]
   - [[TECHNIQUE:Command_Modification]]

**Attack Example:**
```python
# [[TECHNIQUE:Modbus_TCP_Attack_Example]]
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('[[TARGET:PLC_IP_ADDRESS]]')
# [[TECHNIQUE:Write_Malicious_Register_Value]]
client.write_register([[ADDRESS:40001]], [[VALUE:9999]])  # Safety threshold bypass
# [[IMPACT:Safety_System_Compromise]]
```

#### [[PROTOCOL:DNP3]] Vulnerabilities

**Weaknesses:**
- [[WEAKNESS:Limited_Authentication]]
- [[VULNERABILITY:Replay_Attacks]]
- [[WEAKNESS:Timestamp_Manipulation]]

**[[ATTACK:DNP3_Replay_Attack]]:**
1. [[TECHNIQUE:Legitimate_Command_Capture]]
2. [[TECHNIQUE:Command_Storage]]
3. [[TECHNIQUE:Replay_During_Unauthorized_Window]]
4. [[TECHNIQUE:Critical_Command_Injection]]

#### [[PROTOCOL:IEC_60870-5-104]] Exploitation

**Vulnerabilities:**
- [[VULNERABILITY:Replay_Attack_Susceptibility]]
- [[WEAKNESS:Weak_Authentication_Mechanisms]]
- [[VULNERABILITY:Command_Injection]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1071.001]] - Web Protocols
- [[TECHNIQUE:MITRE_ATT&CK:T1040]] - Network Sniffing
- [[TECHNIQUE:MITRE_ATT&CK:T1557]] - Adversary-in-the-Middle
- [[TECHNIQUE:MITRE_ATT&CK:T1205]] - Traffic Signaling

---

### [[ATTACK_VECTOR:Configuration_Flaws]]

**Prevalence:** [[STATISTIC:67%_of_Network_Penetration]] via configuration weaknesses

#### Common Misconfigurations

**[[WEAKNESS:Poor_Network_Segmentation]]:**
- [[ISSUE:Corporate-to-ICS_Network_Bridges]]
- [[ISSUE:Flat_Network_Architecture]]
- [[ISSUE:Insufficient_VLAN_Separation]]
- [[IMPACT:Easy_Lateral_Movement]]

**[[WEAKNESS:Default_Credentials]]:**
- [[CREDENTIAL:admin/admin]]
- [[CREDENTIAL:root/root]]
- [[CREDENTIAL:service/service]]
- [[DATABASE:Vendor_Default_Passwords]] publicly available

**[[WEAKNESS:Exposed_Services]]:**
- [[SERVICE:Remote_Desktop_Protocol]] (TCP 3389)
- [[SERVICE:VNC]] (TCP 5900)
- [[SERVICE:Telnet]] (TCP 23)
- [[SERVICE:FTP]] (TCP 21)
- [[SERVICE:SCADA_Protocols]] directly internet-accessible

#### Exploitation Statistics
- [[STATISTIC:67%]] of corporate-to-industrial network compromises require [[SKILL_LEVEL:Low_or_Trivial]] skill
- [[METHOD:Existing_Configuration_Flaws]] leveraged
- [[AVAILABILITY:Online_Exploit_Tools]] readily available for [[VULNERABILITY:OS_Vulnerabilities]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1078]] - Valid Accounts (default credentials)
- [[TECHNIQUE:MITRE_ATT&CK:T1021.001]] - Remote Desktop Protocol
- [[TECHNIQUE:MITRE_ATT&CK:T1046]] - Network Service Discovery
- [[TECHNIQUE:MITRE_ATT&CK:T1133]] - External Remote Services

---

### [[ATTACK_VECTOR:Search_Engine_Discovery]]

#### Internet-Exposed SCADA Systems

**[[TOOL:Shodan]] Discovery:**
- [[SEARCH_QUERY:"SCADA"]]
- [[SEARCH_QUERY:"Siemens PLC"]]
- [[SEARCH_QUERY:"port:502"]] (Modbus)
- [[SEARCH_QUERY:"Schneider Electric"]]

**[[TOOL:Censys]] Identification:**
- [[TECHNIQUE:SSL_Certificate_Analysis]]
- [[TECHNIQUE:Banner_Grabbing]]
- [[TECHNIQUE:Service_Fingerprinting]]

**[[TOOL:ZoomEye]] Mapping:**
- [[TECHNIQUE:Industrial_Network_Mapping]]
- [[TECHNIQUE:Control_System_Enumeration]]
- [[TECHNIQUE:Vulnerability_Correlation]]

#### Exposed Systems Commonly Found
- [[SYSTEM:HMI_Web_Interfaces]]
- [[DEVICE:PLCs]] with web servers
- [[SYSTEM:SCADA_Historians]]
- [[DEVICE:RTUs]] (Remote Terminal Units)
- [[SYSTEM:Engineering_Workstations]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1593.002]] - Search Engines
- [[TECHNIQUE:MITRE_ATT&CK:T1590]] - Gather Victim Network Information
- [[TECHNIQUE:MITRE_ATT&CK:T1595]] - Active Scanning

---

## Supply Chain Attack Vectors

### [[ATTACK_VECTOR:Pre-Shipment_Compromise]]

#### Attack Methods
1. [[TECHNIQUE:Malware_Insertion_During_Manufacturing]]
   - [[TECHNIQUE:Firmware_Backdoor_Implantation]]
   - [[TECHNIQUE:Hardware_Trojan_Installation]]
   - [[TECHNIQUE:Supply_Chain_Infiltration]]

2. [[TECHNIQUE:Hardware_Implants]]
   - [[DEVICE:Rogue_Network_Cards]]
   - [[DEVICE:Modified_Motherboards]]
   - [[DEVICE:Compromised_CPUs]]

3. [[TECHNIQUE:Firmware_Backdoors_Pre-Deployment]]
   - [[TECHNIQUE:BIOS_Modification]]
   - [[TECHNIQUE:BMC_Compromise]]
   - [[TECHNIQUE:NIC_Firmware_Backdoors]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1195.002]] - Compromise Software Supply Chain
- [[TECHNIQUE:MITRE_ATT&CK:T1195.003]] - Compromise Hardware Supply Chain
- [[TECHNIQUE:MITRE_ATT&CK:T1542]] - Pre-OS Boot

---

### [[ATTACK_VECTOR:Maintenance_Window_Exploitation]]

#### Vulnerability Windows
[[EVENT:System_Updates]] and [[EVENT:Maintenance_Activities]] create [[OPPORTUNITY:Attack_Windows]]:

**[[ATTACK:Compromise_During_Updates]]:**
- [[TECHNIQUE:Update_Server_Compromise]]
- [[TECHNIQUE:Malicious_Patch_Injection]]
- [[TECHNIQUE:Update_Package_Modification]]

**[[ATTACK:Third-Party_Technician_Credential_Theft]]:**
- [[TECHNIQUE:Vendor_Access_Account_Compromise]]
- [[TECHNIQUE:Remote_Maintenance_Credential_Harvesting]]
- [[TECHNIQUE:VPN_Credential_Theft]]

**[[ATTACK:Remote_Maintenance_Session_Hijacking]]:**
- [[TECHNIQUE:TeamViewer_Session_Hijacking]]
- [[TECHNIQUE:VNC_Connection_Interception]]
- [[TECHNIQUE:RDP_Session_Takeover]]

#### Real-World Example
**[[INCIDENT:Danish_State_Railways]]** (2022):
- [[VECTOR:Supply_Chain_Compromise]] via [[VENDOR:Supeo]]
- [[TARGET:Enterprise_Asset_Management_System]]
- [[IMPACT:Train_Driver_Software_Failure]]
- [[IMPACT:Network-Wide_Service_Disruptions]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1195.001]] - Supply Chain Compromise: Managed Service Provider
- [[TECHNIQUE:MITRE_ATT&CK:T1199]] - Trusted Relationship
- [[TECHNIQUE:MITRE_ATT&CK:T1550]] - Use Alternate Authentication Material

---

### [[ATTACK_VECTOR:Software_Supply_Chain]]

**Statistics:**
- [[STATISTIC:64.33%]] of [[THREAT:Supply_Chain_Threats]] target [[SECTOR:Transportation_and_Warehousing]]
- [[STATISTIC:1_in_5]] supply chain businesses experience [[INCIDENT:Data_Breaches]]
- [[RISK:Cascading_Vulnerabilities]] through vendor dependencies

#### Attack Patterns

**[[ATTACK:Third-Party_Vendor_Compromise]]:**
1. [[TARGET:Software_Vendor_Compromise]] ([[EXAMPLE:Supeo]])
2. [[TECHNIQUE:Malicious_Update_Deployment]]
3. [[IMPACT:Customer_Compromise]] ([[EXAMPLE:Danish_Railways]])
4. [[IMPACT:Cascading_Effects]]

**[[ATTACK:Shared_Service_Provider_Exploitation]]:**
- [[TARGET:Cloud_Service_Provider]]
- [[TARGET:Managed_Service_Provider]]
- [[TARGET:SaaS_Platform]]
- [[IMPACT:Multi-Customer_Compromise]]

#### Recent Incidents
- **[[INCIDENT:Danish_State_Railways]]** (2022) - [[VENDOR:Supeo]] EAM compromise
- **[[INCIDENT:London_North_Eastern_Railway]]** (2025) - Third-party data access breach
- **[[INCIDENT:Canadian_Pacific_Rail]]** - Insider threat (former IT employee)

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1195]] - Supply Chain Compromise
- [[TECHNIQUE:MITRE_ATT&CK:T1584.001]] - Domains (for C2)
- [[TECHNIQUE:MITRE_ATT&CK:T1608.001]] - Upload Malware

---

## Insider Threat Vectors

### [[THREAT:Malicious_Insiders]]

#### Threat Categories

**[[INSIDER_TYPE:Former_IT_Employees]]:**
- [[ACCESS:Retained_Access]] to systems
- [[KNOWLEDGE:System_Architecture]] understanding
- [[MOTIVATION:Revenge]] or [[MOTIVATION:Financial_Gain]]

**[[INSIDER_TYPE:Railway_Personnel_Saboteurs]]:**
- [[EXAMPLE:Police_Officers]] involved ([[INCIDENT:Poland_Arrests]])
- [[ACCESS:Physical_Access]] to critical systems
- [[KNOWLEDGE:Operational_Procedures]]

**[[INSIDER_TYPE:Employees_with_Critical_System_Access]]:**
- [[ROLE:System_Administrators]]
- [[ROLE:Maintenance_Technicians]]
- [[ROLE:Control_Room_Operators]]

#### Attack Examples

**[[INCIDENT:Canadian_Pacific_Rail_Insider]]:**
- [[ACTOR:Former_IT_Employee]]
- [[ATTACK:Network_Switch_Configuration_Deletion]]
- [[IMPACT:Core_Network_Infrastructure_Compromise]]
- [[IMPACT:Multi-System_Outage]]

**[[INCIDENT:UK_Railway_Stations_Hack]]** (2024):
- [[ATTRIBUTION:Insider-Linked]]
- [[ATTACK:Terror_Message_Display]] on 19 stations
- [[IMPACT:Public_Panic]]
- [[IMPACT:Security_System_Compromise]]

### [[THREAT:Unintentional_Insiders]]

#### Risk Factors

**[[VECTOR:Phishing_Campaign_Victims]]:**
- [[TECHNIQUE:Spear_Phishing]] targeting railway employees
- [[TECHNIQUE:Credential_Harvesting]]
- [[TECHNIQUE:Malware_Delivery]]

**[[VECTOR:Poor_Security_Hygiene]]:**
- [[WEAKNESS:Password_Reuse]]
- [[WEAKNESS:Weak_Passwords]]
- [[WEAKNESS:Unpatched_Personal_Devices]]

**[[VECTOR:Social_Engineering_Targets]]:**
- [[TECHNIQUE:Pretexting]] (fake vendor calls)
- [[TECHNIQUE:Tailgating]] into secure areas
- [[TECHNIQUE:Baiting]] (infected USB drives)

**[[VECTOR:Credential_Compromise_Through_Negligence]]:**
- [[ISSUE:Passwords_Written_Down]]
- [[ISSUE:Shared_Accounts]]
- [[ISSUE:Unattended_Workstations]]

### Privilege Escalation Paths

**[[PATH:IT_Administrative_Access]]:**
- [[ACCESS:IT_Network]] → [[ACCESS:SCADA_Network]] traversal
- [[TECHNIQUE:Credential_Reuse]]
- [[TECHNIQUE:Poor_Segmentation_Exploitation]]

**[[PATH:Maintenance_Personnel_Credentials]]:**
- [[ACCESS:Vendor_VPN]]
- [[ACCESS:Engineering_Workstation]]
- [[ACCESS:PLC_Programming_Software]]

**[[PATH:Railway_Operations_Staff]]:**
- [[ACCESS:Control_Room_Systems]]
- [[ACCESS:Dispatch_Terminals]]
- [[ACCESS:Communication_Systems]]

**[[PATH:Physical_Security_Badge_Exploitation]]:**
- [[ACCESS:Server_Rooms]]
- [[ACCESS:Equipment_Closets]]
- [[ACCESS:Signaling_Cabinets]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1078.002]] - Domain Accounts
- [[TECHNIQUE:MITRE_ATT&CK:T1078.003]] - Local Accounts
- [[TECHNIQUE:MITRE_ATT&CK:T1098]] - Account Manipulation
- [[TECHNIQUE:MITRE_ATT&CK:T1136]] - Create Account
- [[TECHNIQUE:MITRE_ATT&CK:T1531]] - Account Access Removal

---

## Software-Defined Radio (SDR) Attacks

### [[ATTACK_TECHNIQUE:SDR_Exploitation]]

#### Target Systems
- [[SYSTEM:EOT_HOT_Devices]] ([[VULNERABILITY:CVE-2025-1727]])
- [[SYSTEM:GSM-R_Communications]]
- [[SYSTEM:RADIOSTOP_Emergency_Systems]]
- [[SYSTEM:Wireless_Train_Control_Signals]]

#### Equipment Requirements
**[[TOOL:Commercial_SDR_Hardware]]:**
- [[DEVICE:HackRF_One]] ($300)
- [[DEVICE:USRP_B200]] ($1000-$2000)
- [[DEVICE:RTL-SDR]] ($20-$50)
- [[DEVICE:BladeRF]] ($420)

**[[TOOL:Software_Platforms]]:**
- [[SOFTWARE:GNU_Radio]]
- [[SOFTWARE:gr-gsm]]
- [[SOFTWARE:Universal_Radio_Hacker]]
- [[SOFTWARE:Gqrx]]

#### Attack Workflow

**Phase 1: [[TECHNIQUE:Signal_Capture_and_Analysis]]**
```bash
# [[TECHNIQUE:RF_Spectrum_Analysis]]
hackrf_transfer -r capture.bin -f [[FREQUENCY:150000000]] -s 20000000
# [[TECHNIQUE:Signal_Demodulation]]
gqrx capture.bin
```

**Phase 2: [[TECHNIQUE:Protocol_Reverse_Engineering]]**
- [[ACTIVITY:Signal_Pattern_Analysis]]
- [[ACTIVITY:Modulation_Scheme_Identification]]
- [[ACTIVITY:Packet_Structure_Analysis]]
- [[ACTIVITY:Checksum_Algorithm_Discovery]]

**Phase 3: [[TECHNIQUE:Packet_Crafting]]**
- [[TECHNIQUE:BCH_Checksum_Calculation]]
- [[TECHNIQUE:Command_Packet_Generation]]
- [[TECHNIQUE:Encoding_and_Modulation]]

**Phase 4: [[TECHNIQUE:Command_Injection_via_RF]]**
```python
# [[TECHNIQUE:Malicious_Command_Transmission]]
from gnuradio import blocks, gr, uhd

# [[CONFIGURATION:Transmitter_Setup]]
tb = gr.top_block()
src = blocks.vector_source_b([[DATA:Malicious_Packet]])
sink = uhd.usrp_sink()
sink.set_center_freq([[FREQUENCY:EOT_Frequency]])
tb.connect(src, sink)
tb.run()
```

**Phase 5: [[TECHNIQUE:Exploitation_Verification]]**
- [[MONITORING:Train_Behavior_Observation]]
- [[MONITORING:Response_Validation]]
- [[MONITORING:Impact_Assessment]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1200]] - Hardware Additions
- [[TECHNIQUE:MITRE_ATT&CK:T1588.006]] - Vulnerabilities (protocol weakness exploitation)
- [[TECHNIQUE:MITRE_ATT&CK:T1071]] - Application Layer Protocol
- [[TECHNIQUE:MITRE_ATT&CK:T1499]] - Endpoint Denial of Service

---

## Network Penetration Techniques

### [[TECHNIQUE:Initial_Access]]

**[[TECHNIQUE:Spear_Phishing]]:**
- [[TARGET:Railway_Employees]]
- [[PAYLOAD:Malicious_Attachments]]
- [[PAYLOAD:Credential_Harvesting_Links]]
- [[TECHNIQUE:Domain_Spoofing]]

**[[TECHNIQUE:Watering_Hole_Attacks]]:**
- [[TARGET:Industry_Websites]]
- [[TARGET:Vendor_Portals]]
- [[TARGET:Professional_Forums]]
- [[TECHNIQUE:Drive-by_Download]]

**[[TECHNIQUE:VPN_Credential_Theft]]:**
- [[TECHNIQUE:Credential_Stuffing]]
- [[TECHNIQUE:Password_Spraying]]
- [[TECHNIQUE:Brute_Force]]
- [[SOURCE:Dark_Web_Credential_Purchase]]

**[[TECHNIQUE:Remote_Access_Tool_Exploitation]]:**
- [[VULNERABILITY:Unpatched_VPN_Appliances]]
- [[VULNERABILITY:RDP_Vulnerabilities]]
- [[VULNERABILITY:Citrix_Exploits]]
- [[VULNERABILITY:TeamViewer_Compromise]]

### [[TECHNIQUE:Lateral_Movement]]

**[[TECHNIQUE:Corporate-to-ICS_Network_Traversal]]:**
1. [[STAGE:Initial_Corporate_Network_Compromise]]
2. [[STAGE:Network_Mapping_and_Discovery]]
3. [[STAGE:Segmentation_Control_Bypass]]
4. [[STAGE:ICS_Network_Access]]

**[[TECHNIQUE:Poor_Network_Segmentation_Exploitation]]:**
- [[WEAKNESS:Firewall_Misconfigurations]]
- [[WEAKNESS:Unnecessary_Trust_Relationships]]
- [[WEAKNESS:Shared_VLANs]]

**[[TECHNIQUE:Credential_Harvesting_and_Reuse]]:**
- [[TOOL:Mimikatz]] for [[TECHNIQUE:Credential_Dumping]]
- [[TECHNIQUE:LSASS_Memory_Extraction]]
- [[TECHNIQUE:SAM_Database_Extraction]]
- [[TECHNIQUE:Cached_Credentials]]

**[[TECHNIQUE:Trust_Relationship_Abuse]]:**
- [[RELATIONSHIP:Domain_Trusts]]
- [[RELATIONSHIP:Service_Accounts]]
- [[RELATIONSHIP:Vendor_Access_Accounts]]

### [[TECHNIQUE:Privilege_Escalation]]

**[[TECHNIQUE:Unpatched_OS_Vulnerabilities]]:**
- [[VULNERABILITY:Windows_Privilege_Escalation]]
- [[VULNERABILITY:Linux_Kernel_Exploits]]
- [[VULNERABILITY:Zero-Day_Exploitation]]

**[[TECHNIQUE:Misconfigured_Service_Accounts]]:**
- [[ISSUE:Excessive_Permissions]]
- [[ISSUE:Domain_Admin_Service_Accounts]]
- [[ISSUE:Weak_Service_Account_Passwords]]

**[[TECHNIQUE:Default_Credentials_on_SCADA]]:**
- [[DATABASE:Vendor_Default_Passwords]]
- [[CREDENTIAL:admin/admin]]
- [[CREDENTIAL:Administrator/Administrator]]

**[[TECHNIQUE:Legacy_System_Exploitation]]:**
- [[SYSTEM:Windows_XP_SCADA_Servers]]
- [[SYSTEM:Unpatched_Linux_2.6_Kernels]]
- [[SYSTEM:End-of-Life_Operating_Systems]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1566.001]] - Spearphishing Attachment
- [[TECHNIQUE:MITRE_ATT&CK:T1189]] - Drive-by Compromise
- [[TECHNIQUE:MITRE_ATT&CK:T1078]] - Valid Accounts
- [[TECHNIQUE:MITRE_ATT&CK:T1021]] - Remote Services
- [[TECHNIQUE:MITRE_ATT&CK:T1003]] - OS Credential Dumping
- [[TECHNIQUE:MITRE_ATT&CK:T1068]] - Exploitation for Privilege Escalation

---

## Data Wiper Attacks

### [[ATTACK_TYPE:Russian_TTP_Analysis]] - Ukraine Railway Attacks

#### Preparation Phase

**[[STAGE:Infrastructure_Reconnaissance]]:**
- [[ACTIVITY:Network_Topology_Mapping]]
- [[ACTIVITY:System_Architecture_Analysis]]
- [[ACTIVITY:Critical_Asset_Identification]]
- [[ACTIVITY:Backup_System_Discovery]]

**[[STAGE:Malware_Customization]]:**
- [[DEVELOPMENT:Target_Environment_Analysis]]
- [[DEVELOPMENT:Wiper_Payload_Development]]
- [[DEVELOPMENT:Anti-Detection_Features]]
- [[DEVELOPMENT:Propagation_Mechanisms]]

**[[STAGE:Access_Persistence]]:**
- [[TECHNIQUE:Backdoor_Installation]]
- [[TECHNIQUE:Multiple_Access_Paths]]
- [[TECHNIQUE:Credential_Stockpiling]]
- [[TECHNIQUE:Staging_Infrastructure]]

**[[STAGE:Multi-Stage_Payload_Delivery]]:**
- [[TECHNIQUE:Staged_Malware_Deployment]]
- [[TECHNIQUE:Time-Delayed_Activation]]
- [[TECHNIQUE:Redundant_Deployment]]

#### Execution Phase

**[[STAGE:Coordinated_Multi-System_Targeting]]:**
- [[TARGET:Ticketing_Systems]]
- [[TARGET:Operational_Databases]]
- [[TARGET:Backup_Systems]]
- [[TARGET:Recovery_Infrastructure]]

**[[STAGE:Rapid_Propagation]]:**
- [[TECHNIQUE:Network_Share_Propagation]]
- [[TECHNIQUE:Lateral_Movement]]
- [[TECHNIQUE:Automated_Deployment]]

**[[STAGE:Data_Destruction]]:**
- [[TECHNIQUE:Master_Boot_Record_Overwrite]]
- [[TECHNIQUE:File_System_Corruption]]
- [[TECHNIQUE:Database_Deletion]]
- [[TECHNIQUE:Partition_Table_Destruction]]

**[[STAGE:Recovery_Prevention]]:**
- [[TECHNIQUE:Backup_Deletion]]
- [[TECHNIQUE:Shadow_Copy_Removal]]
- [[TECHNIQUE:Restore_Point_Elimination]]
- [[TECHNIQUE:Recovery_Tool_Disablement]]

#### Impact Characteristics
- [[IMPACT:Ticketing_System_Destruction]]
- [[IMPACT:Operational_Database_Corruption]]
- [[IMPACT:Backup_System_Targeting]]
- [[IMPACT:Multi-Day_Recovery_Requirements]]

#### TTPs
- [[TECHNIQUE:MITRE_ATT&CK:T1485]] - Data Destruction
- [[TECHNIQUE:MITRE_ATT&CK:T1490]] - Inhibit System Recovery
- [[TECHNIQUE:MITRE_ATT&CK:T1561.001]] - Disk Content Wipe
- [[TECHNIQUE:MITRE_ATT&CK:T1561.002]] - Disk Structure Wipe
- [[TECHNIQUE:MITRE_ATT&CK:T1489]] - Service Stop
