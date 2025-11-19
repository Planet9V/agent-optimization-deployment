# Threat Campaigns and Operations

## [[CAMPAIGN:Critical_Infrastructure_Pre-Positioning]]

### Campaign Overview
**Primary Actor:** [[THREAT_ACTOR:Volt_Typhoon]]
**Attribution:** [[COUNTRY:China]]
**Timeline:** 2023 - Present (Ongoing)
**Objective:** [[STRATEGIC_GOAL:Wartime_Disruption_Capability]]

### Campaign Characteristics
[[CAMPAIGN:Critical_Infrastructure_Pre-Positioning]] represents [[COUNTRY:China]]'s strategic effort to establish persistent access within [[GEOGRAPHY:U.S._Critical_Infrastructure]] for potential [[SCENARIO:Wartime_Disruption]].

#### Target Sectors
- [[TARGET_SECTOR:Transportation]] (railways, ports, aviation)
- [[TARGET_SECTOR:Energy]] (power grid, pipelines)
- [[TARGET_SECTOR:Water_Treatment]]
- [[TARGET_SECTOR:Communications]]
- [[TARGET_SECTOR:Defense_Industrial_Base]]

#### Railway-Specific Targets
- [[TARGET_SYSTEM:Railway_Control_Systems]]
- [[TARGET_SYSTEM:Fleet_Management_Platforms]]
- [[TARGET_SYSTEM:Port_Automation_Systems]]
- [[TARGET_SYSTEM:Transit_Scheduling_Systems]]
- [[TARGET_SYSTEM:SCADA_Networks]]

### TTPs Employed
**[[TECHNIQUE:Living-off-the-Land]] (Primary Tactic):**
- [[TOOL:PsExec]] for lateral movement
- [[TOOL:WMI]] for remote execution
- [[TOOL:PowerShell]] for scripting
- [[TOOL:Netsh]] for network configuration
- [[TOOL:BITSAdmin]] for file transfers

**[[TECHNIQUE:Credential_Harvesting]]:**
- [[TECHNIQUE:MITRE_ATT&CK:T1003.001]] - LSASS Memory dumping
- [[TECHNIQUE:MITRE_ATT&CK:T1003.002]] - Security Account Manager
- [[TECHNIQUE:MITRE_ATT&CK:T1003.003]] - NTDS dumping
- [[TECHNIQUE:MITRE_ATT&CK:T1552]] - Unsecured Credentials

**[[TECHNIQUE:Persistent_Access]]:**
- [[TECHNIQUE:Valid_Account_Abuse]]
- [[TECHNIQUE:VPN_Credential_Reuse]]
- [[TECHNIQUE:Remote_Access_Tool_Installation]]
- [[TECHNIQUE:Scheduled_Task_Persistence]]

### Intelligence Assessments
**[[SOURCE:Office_of_Director_of_National_Intelligence]] (2023):**
> "[[COUNTRY:China]] almost certainly is capable of launching cyber attacks that could disrupt critical infrastructure services within the [[COUNTRY:United_States]], including against oil and gas pipelines, and [[TARGET_SECTOR:Rail_Systems]]."

### Strategic Intent
1. **[[OBJECTIVE:Impede_National_Response]]:** Delay military mobilization during [[SCENARIO:Taiwan_Conflict]]
2. **[[OBJECTIVE:Degrade_Logistics]]:** Disrupt troop deployment and materiel distribution
3. **[[OBJECTIVE:Civilian_Disruption]]:** Affect civilian mobility and morale
4. **[[OBJECTIVE:Economic_Coercion]]:** Leverage access for geopolitical objectives

### Detection and Mitigation
**Detection Indicators:**
- [[INDICATOR:Unusual_LOLBIN_Usage]] (PsExec, WMI from non-admin accounts)
- [[INDICATOR:Off-hours_Administrative_Activity]]
- [[INDICATOR:Lateral_Movement_Patterns]]
- [[INDICATOR:Credential_Dumping_Attempts]]

**Recommended Mitigations:**
- [[MITIGATION:Enhanced_Logging]] of administrative tools
- [[MITIGATION:Application_Whitelisting]]
- [[MITIGATION:Privileged_Access_Management]]
- [[MITIGATION:Network_Segmentation]]

---

## [[CAMPAIGN:Ukraine_Railway_Attacks]]

### Campaign Profile
**Primary Actor:** [[THREAT_ACTOR:APT28]] (Fancy Bear)
**Attribution:** [[COUNTRY:Russia]], [[ORGANIZATION:GRU_Unit_26165]]
**Timeline:** 2022 - 2025 (Ongoing)
**Objective:** [[STRATEGIC_GOAL:Railway_Infrastructure_Disruption]]

### Major Operations

#### [[OPERATION:Ukrzaliznytsia_Data_Wiper]] (March 2025)

**Target:** [[ORGANIZATION:Ukrzaliznytsia]] (Ukrainian State Railways)
**Attack Type:** [[MALWARE:Custom_Data_Wiper]]
**Execution Date:** March 2025 (Sunday night)

**Attack Timeline:**
1. **Sunday Evening:** [[TECHNIQUE:Initial_Compromise]] and [[TECHNIQUE:Access_Establishment]]
2. **Sunday Night:** [[TECHNIQUE:Lateral_Movement]] across ticketing infrastructure
3. **Monday Morning:** [[TECHNIQUE:Wiper_Execution]] synchronized across systems
4. **Monday-Wednesday:** [[IMPACT:Service_Degradation]] and recovery operations

**Technical Analysis:**
[[MALWARE:Custom_Railway_Wiper]] characteristics:
- [[FEATURE:Target-Specific_Customization]] for [[ORGANIZATION:Ukrzaliznytsia]] infrastructure
- [[FEATURE:Multi-Stage_Payload]]
- [[FEATURE:Anti-Recovery_Mechanisms]]
- [[FEATURE:Data_Destruction_Focus]] (not encryption)

**Impact Assessment:**
- **[[METRIC:Zero_Operational_Stoppages]]** - Trains continued running
- **[[IMPACT:Ticket_Sales_Significantly_Slowed]]**
- **[[IMPACT:Large_Queues]]** at physical stations nationwide
- **[[IMPACT:Online_Ticketing_Disabled]]** for 48+ hours
- **[[IMPACT:Passenger_Frustration]]** and inconvenience

**Resilience Factors:**
[[ORGANIZATION:Ukrzaliznytsia]] demonstrated strong [[CAPABILITY:Operational_Resilience]]:
- [[FEATURE:Segmented_Systems]] (operations separated from ticketing)
- [[FEATURE:Manual_Fallback_Procedures]]
- [[FEATURE:Rapid_Response_Teams]]
- [[FEATURE:Backup_Ticketing_Processes]]

### Historical Operations

#### [[OPERATION:2022-2023_Railway_Disruptions]]
- Multiple [[ATTACK:Cyber_Attacks]] against [[TARGET:Ukrainian_Railways]]
- [[TECHNIQUE:Coordination]] with [[ATTACK_TYPE:Physical_Sabotage]]
- [[TECHNIQUE:Information_Operations]] amplification
- [[OBJECTIVE:Logistics_Degradation]] during war

### TTPs

**Preparation Phase:**
- [[TECHNIQUE:MITRE_ATT&CK:T1592]] - Gather Victim Host Information
- [[TECHNIQUE:MITRE_ATT&CK:T1589]] - Gather Victim Identity Information
- [[TECHNIQUE:MITRE_ATT&CK:T1590]] - Gather Victim Network Information

**Execution Phase:**
- [[TECHNIQUE:MITRE_ATT&CK:T1486]] - Data Encrypted for Impact (wipers, not ransomware)
- [[TECHNIQUE:MITRE_ATT&CK:T1485]] - Data Destruction
- [[TECHNIQUE:MITRE_ATT&CK:T1490]] - Inhibit System Recovery
- [[TECHNIQUE:MITRE_ATT&CK:T1561]] - Disk Wipe

**Supporting Operations:**
- [[TECHNIQUE:Physical_Infrastructure_Attacks]] (sabotage)
- [[TECHNIQUE:Disinformation_Campaigns]]
- [[TECHNIQUE:Psychological_Operations]]

### [[MALWARE:GooseEgg_Exploit]] Usage
[[THREAT_ACTOR:APT28]] utilized [[MALWARE:GooseEgg]] against:
- [[GEOGRAPHY:Ukraine]] transportation sector
- [[GEOGRAPHY:Western_Europe]] rail networks
- [[GEOGRAPHY:North_America]] transit systems

---

## [[CAMPAIGN:Poland_Railway_Radio_Sabotage]]

### Campaign Profile
**Suspected Actor:** [[THREAT_ACTOR:Russian_State_Proxies]]
**Timeline:** August 25-27, 2023
**Attack Type:** [[ATTACK_TYPE:RF_Signal_Exploitation]]
**Target:** [[SYSTEM:RADIOSTOP_Emergency_System]]

### Incident Chronology

**August 25, 2023 - 21:23 (9:23 PM):**
- **Location:** [[LOCATION:Szczecin_Region]], [[COUNTRY:Poland]]
- **Impact:** 20+ trains received unauthorized [[COMMAND:Emergency_Stop_Signals]]
- **Response:** Freight traffic halted preventatively
- **Duration:** Services restored within hours

**August 26, 2023 - 18:00 (6:00 PM):**
- **Location:** [[LOCATION:Gdynia_Region]]
- **Targets:** Freight trains (primary)
- **Impact:** Evening passenger services disrupted

**August 27, 2023:**
- **Location:** [[LOCATION:Białystok_Region]]
- **Targets:** 5 passenger trains, 1 freight train
- **Impact:** Regional network disruption

### Technical Exploitation

**[[SYSTEM:RADIOSTOP]] Vulnerabilities:**
- [[WEAKNESS:Analog_Radio-Based]] emergency stop
- [[FREQUENCY:~150_MHz]] transmission
- [[WEAKNESS:No_Authentication_Mechanism]]
- [[WEAKNESS:No_Encryption]]
- [[TRIGGER:Three-Tone_Sequence]] activates braking

**Attack Implementation:**
1. [[TOOL:Basic_Radio_Transmitter]] acquisition ($50-$500)
2. [[CONFIGURATION:Frequency_Programming]] to 150 MHz
3. [[KNOWLEDGE:Tone_Sequence_Transmission]]
4. [[IMPACT:Emergency_Brake_Activation]]

**Cost-Benefit Analysis:**
- **Attack Cost:** < $500 (commercial radio equipment)
- **Technical Skill:** [[LEVEL:Low]] - No sophisticated knowledge required
- **Impact:** [[LEVEL:High]] - National railway network disruption

### Psychological Operations Component

**[[TECHNIQUE:Attribution_Messaging]]:**
- [[INDICATOR:Russian_National_Anthem]] broadcast on railway radio
- [[INDICATOR:Vladimir_Putin_Speech_Excerpts]] played
- [[INTENT:Clear_Attribution_Signaling]]
- [[OBJECTIVE:Intimidation_and_Destabilization]]

### Attribution Analysis

**Evidence Indicators:**
- [[INDICATOR:Russian_Propaganda_Broadcast]]
- [[INDICATOR:Coordination_with_Destabilization_Efforts]]
- [[INDICATOR:Geographic_Pattern]] (Russian/Belarus border regions)
- [[INDICATOR:Timing]] (geopolitical tensions)

**Arrests:**
- Two individuals arrested by [[ORGANIZATION:Polish_Intelligence]]
- One suspect: [[OCCUPATION:Police_Officer]] (insider threat)
- Investigation ongoing into [[ATTRIBUTION:Russian_Belarusian_State_Links]]

### Remediation

**Short-term:**
- [[RESPONSE:Increased_Radio_Monitoring]]
- [[RESPONSE:Enhanced_Physical_Security]]
- [[RESPONSE:Operator_Awareness_Training]]

**Long-term:**
- [[SOLUTION:Migration_to_GSM-R_System]]
- [[FEATURE:Digital_Encryption_Implementation]]
- [[FEATURE:Authentication_Mechanism_Deployment]]
- **Target Completion:** End of 2024

---

## [[CAMPAIGN:Ransomware_Against_Transportation_Sector]]

### Campaign Statistics
**Timeline:** 2020 - Present (Ongoing)
**Primary Threat:** [[THREAT:Ransomware_Groups]]

### Growth Metrics
- **[[STATISTIC:220%_Increase]]** in railway cyber attacks
- **[[STATISTIC:108_Incidents]]** against [[SECTOR:Transportation_Logistics]] in Q1 2025
- Up from **[[STATISTIC:69_Incidents]]** in Q4 2024
- **[[STATISTIC:15%]]** of total ransomware activity targets [[SECTOR:Transportation]]
- **[[STATISTIC:48%_Overall_Increase]]** (2020-2025)

### Major Incidents

#### [[INCIDENT:Pittsburgh_Regional_Transit]] (December 19, 2024)

**Attack Profile:**
- **Attacker:** [[THREAT_ACTOR:Unidentified_Ransomware_Group]]
- **Target:** [[ORGANIZATION:Pittsburgh_Regional_Transit]]
- **Primary System:** [[TARGET:Rail_Tracking_System]]

**Operational Impact:**
- [[IMPACT:Rail_Car_Location_Tracking_Disabled]]
- [[IMPACT:Operators_Unable_to_Locate_Rail_Cars]]
- [[IMPACT:Manual_Coordination_Required]]
- [[IMPACT:Multi-Day_Service_Disruptions]]

**Data Breach:**
- [[DATA_TYPE:Customer_Financial_Information]] compromised
- [[DATA_TYPE:Personal_Identification_Data]] exposed
- [[STATUS:Scope_Under_Investigation]]

**Systemic Implications:**
- Demonstrated [[RISK:OT_IT_Convergence]]
- [[IMPACT:Real-Time_Operational_Visibility_Loss]]
- [[IMPACT:Reduced_Safety_Margins]]
- [[RISK:Public_Transportation_Dependency]]

#### [[INCIDENT:Transport_for_London]] (September 2024)

**Scale:**
- **[[METRIC:5000+_Passengers]]** bank account details compromised
- **[[METRIC:30000_Employees]]** affected
- **[[REQUIREMENT:In-Person_Password_Reset]]** for all staff

**Response:**
- [[ACTION:Enterprise-Wide_Credential_Reset]]
- [[ACTION:Physical_Security_Modifications]]
- [[ACTION:Manual_Procedure_Activation]]
- [[ACTION:Multi-Week_Forensic_Investigation]]

**Lessons:**
- [[INSIGHT:Large_Urban_Transit_High-Value_Targets]]
- [[VULNERABILITY:Credential_Management_Critical]]
- [[CONSIDERATION:Insider_Threat_Post-Breach]]
- [[IMPACT:Public_Confidence_Erosion]]

#### [[INCIDENT:Port_of_Seattle]] (August 2024)

**Attacker:** [[THREAT_ACTOR:Rhysida_Ransomware]]
**Scope:** [[FACILITY_TYPE:Dual-Mode_Transportation_Hub]]

**Impact:**
- [[SYSTEM:Airport_Operations_Affected]]
- [[SYSTEM:Seaport_Operations_Disrupted]]
- [[IMPACT:Maritime_Cargo_Delays]]
- [[IMPACT:Aviation_Support_Disruptions]]

#### [[INCIDENT:Danish_State_Railways]] (2022)

**Attack Vector:** [[TECHNIQUE:Supply_Chain_Compromise]]
**Compromised Vendor:** [[ORGANIZATION:Supeo]]
**Affected System:** [[SOFTWARE:Enterprise_Asset_Management]]

**Impact:**
- [[SYSTEM:Train_Driver_Software_Failed]]
- [[IMPACT:Network-Wide_Service_Disruptions]]
- [[IMPACT:Cascading_Vendor_Effects]]

**Supply Chain Lessons:**
- **[[STATISTIC:64.33%]]** of supply chain threats target [[SECTOR:Transportation_Warehousing]]
- **[[STATISTIC:1_in_5]]** supply chain businesses experience breaches
- [[RISK:Cascading_Vulnerabilities]]

### Primary Threat Groups

**[[THREAT_ACTOR:Rhysida]]:**
- [[TECHNIQUE:Double_Extortion]]
- [[TARGET_FOCUS:Critical_Infrastructure]]
- [[EXAMPLE:Port_of_Seattle_2024]]

**[[THREAT_ACTOR:DragonForce]]:**
- [[SPECIALIZATION:Logistics_Supply_Chain]]
- [[MODEL:Ransomware-as-a-Service]]
- [[TARGET:Transportation_Warehousing]]

**[[THREAT_ACTOR:LockBit]]:**
- [[STATUS:Disrupted_Feb_2024]]
- [[LEGACY:Affiliates_Still_Active]]
- [[HISTORY:Multiple_Railway_Compromises]]

**[[THREAT_ACTOR:BlackCat_ALPHV]]:**
- [[STATUS:Exit_Scam_March_2024]]
- [[SUCCESSOR:Rebranded_Operations]]
- [[TECHNIQUE:Triple_Extortion]]

**[[THREAT_ACTOR:Royal]]:**
- [[ORIGIN:Conti_Dissolution]]
- [[FOCUS:Critical_Infrastructure]]
- [[TECHNIQUE:Callback_Phishing]]

---

## [[CAMPAIGN:Multi-Sector_Espionage]] - APT41

### Campaign Profile
**Actor:** [[THREAT_ACTOR:APT41]] (Winnti, BARIUM, Double Dragon)
**Attribution:** [[COUNTRY:China]]
**Timeline:** 2012 - Present
**Nature:** [[ACTIVITY:Dual_Mission]] (State espionage + financial crime)

### Target Sectors
- [[SECTOR:Transportation]]
- [[SECTOR:Healthcare]]
- [[SECTOR:Telecommunications]]
- [[SECTOR:Technology]]
- [[SECTOR:Gaming_Industry]]
- [[SECTOR:Higher_Education]]

### Railway Sector Operations

**Target Systems:**
- [[TARGET:Enterprise_Asset_Management_Systems]]
- [[TARGET:Operational_Databases]]
- [[TARGET:Fleet_Management_Platforms]]
- [[TARGET:Logistics_Software]]
- [[TARGET:Railway_Communications]]

**Objectives:**
- [[OBJECTIVE:Intellectual_Property_Theft]]
- [[OBJECTIVE:Operational_Intelligence]]
- [[OBJECTIVE:Strategic_Positioning]]
- [[OBJECTIVE:Financial_Gain]]

### TTPs

**Initial Access:**
- [[TECHNIQUE:MITRE_ATT&CK:T1190]] - Exploit Public-Facing Application
- [[TECHNIQUE:MITRE_ATT&CK:T1566]] - Phishing
- [[TECHNIQUE:MITRE_ATT&CK:T1195]] - Supply Chain Compromise

**Malware Arsenal:**
- [[MALWARE:HIGHNOON]] - Backdoor
- [[MALWARE:HOMEUNIX]] - Trojan
- [[MALWARE:CROSSWALK]] - Modular backdoor
- [[MALWARE:DUSTPAN]] - Credential stealer
- [[MALWARE:MESSAGETAP]] - SMS interception

**Persistence:**
- [[TECHNIQUE:MITRE_ATT&CK:T1053]] - Scheduled Task/Job
- [[TECHNIQUE:MITRE_ATT&CK:T1543]] - Create or Modify System Process
- [[TECHNIQUE:MITRE_ATT&CK:T1574]] - Hijack Execution Flow

**Exfiltration:**
- [[TECHNIQUE:MITRE_ATT&CK:T1041]] - Exfiltration Over C2 Channel
- [[TECHNIQUE:MITRE_ATT&CK:T1567]] - Exfiltration Over Web Service
- [[TECHNIQUE:MITRE_ATT&CK:T1048]] - Exfiltration Over Alternative Protocol

---

## [[CAMPAIGN:Communications_Infrastructure_Compromise]] - Salt Typhoon

### Campaign Profile
**Actor:** [[THREAT_ACTOR:Salt_Typhoon]]
**Attribution:** [[COUNTRY:China]]
**Timeline:** 2023 - Present
**Primary Focus:** [[SECTOR:Communications]]
**Secondary Focus:** [[SECTOR:Transportation_Logistics]]

### Target Profile

**Primary Targets:**
- [[SYSTEM:Telecommunications_Networks]]
- [[SYSTEM:5G_Infrastructure]]
- [[SYSTEM:Satellite_Communications]]

**Transportation Targets:**
- [[SYSTEM:Transit_Scheduling_Systems]]
- [[SYSTEM:Fleet_Communication_Networks]]
- [[SYSTEM:GSM-R_Railway_Communications]]
- [[SYSTEM:Logistics_Management_Platforms]]

### Technical Capabilities

**Protocol Exploitation:**
- [[PROTOCOL:GSM-R]] vulnerabilities
- [[PROTOCOL:LTE]] weaknesses
- [[PROTOCOL:5G]] security gaps

**Communication System Understanding:**
- [[SYSTEM:Railway_Communications_Systems]]
- [[SYSTEM:TETRA]] (Terrestrial Trunked Radio)
- [[SYSTEM:DMR]] (Digital Mobile Radio)

### TTPs

**Initial Access:**
- [[TECHNIQUE:MITRE_ATT&CK:T1071]] - Application Layer Protocol
- [[TECHNIQUE:MITRE_ATT&CK:T1090]] - Proxy
- [[TECHNIQUE:MITRE_ATT&CK:T1133]] - External Remote Services

**Collection:**
- [[TECHNIQUE:MITRE_ATT&CK:T1056]] - Input Capture
- [[TECHNIQUE:MITRE_ATT&CK:T1113]] - Screen Capture
- [[TECHNIQUE:MITRE_ATT&CK:T1557]] - Man-in-the-Middle

**Impact:**
- [[TECHNIQUE:MITRE_ATT&CK:T1498]] - Network Denial of Service
- [[TECHNIQUE:MITRE_ATT&CK:T1565]] - Data Manipulation

---

## Cross-Campaign Analysis

### Common Patterns

**Nation-State Campaigns:**
- [[PATTERN:Long-Term_Persistence]] (years)
- [[PATTERN:Strategic_Objectives]] over immediate gain
- [[PATTERN:Advanced_Customization]]
- [[PATTERN:Resource-Intensive_Operations]]

**Ransomware Campaigns:**
- [[PATTERN:Short_Attack_Cycles]] (days to weeks)
- [[PATTERN:Financial_Motivation]]
- [[PATTERN:Volume_Operations]]
- [[PATTERN:Opportunistic_Targeting]]

### Evolution Trends

**2020-2022:**
- [[TREND:Opportunistic_Ransomware]]
- [[TREND:Basic_TTPs]]
- [[TREND:Limited_OT_Targeting]]

**2023-2024:**
- [[TREND:Targeted_Critical_Infrastructure]]
- [[TREND:Advanced_TTPs]]
- [[TREND:OT_Specific_Operations]]
- [[TREND:Supply_Chain_Focus]]

**2025-Present:**
- [[TREND:AI-Enhanced_Attacks]]
- [[TREND:Multi-Vector_Campaigns]]
- [[TREND:Coordinated_Cyber-Physical]]
- [[TREND:Geopolitically_Motivated]]

### Defensive Priorities by Campaign Type

**Against Nation-State Campaigns:**
1. [[DEFENSE:Advanced_Threat_Hunting]]
2. [[DEFENSE:Behavioral_Analytics]]
3. [[DEFENSE:Deception_Technology]]
4. [[DEFENSE:Threat_Intelligence_Integration]]

**Against Ransomware Campaigns:**
1. [[DEFENSE:Immutable_Backups]]
2. [[DEFENSE:Network_Segmentation]]
3. [[DEFENSE:EDR_Deployment]]
4. [[DEFENSE:Incident_Response_Readiness]]

**Against Supply Chain Campaigns:**
1. [[DEFENSE:Vendor_Risk_Management]]
2. [[DEFENSE:Software_Bill_of_Materials]]
3. [[DEFENSE:Third-Party_Assessments]]
4. [[DEFENSE:Secure_Update_Mechanisms]]
