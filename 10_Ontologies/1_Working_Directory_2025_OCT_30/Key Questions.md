

# Objective: cyber-physical threat intelligence, threat actor profiling, vulnerability and impact analysis for all critical infrastrucutre sectors (multiple)and be able to mark or label specicic customer/client infromation

# Key Questions That Must Be Answered

1."Does this CVE impact my equipment?"

2 "Is there an attack path to vulnerability?"

3."Does this new CVE released today, impact any of my equipment in my facility?" (Assuming SBOMs for all components)

4."Is there a pathway for a threat actor to get to the vulnerability to exploit it?"

5. "For this CVE released today, Is there a pathway for a threat actor to get to the vulnerability to exploit it?"**

6. "How many pieces of a type of equipment do I have"

7. "Do i have a specici application or operation system? 

8. "Tell me the location (on what asset) is a specific application, vulnerability or operating system or library on?


# Key Requirements

FR. Label or mark nodes to help provide security for accessing differnet custome information (nodes) while also supporting differnet sectors and optimzing queries, if we are , for exapmle, focused on a specic sector, a client perhaps. We also need by default to hve "general" knowledge labels, that are accessible for all queries 
FR2. 

F1. Complete SBOM integration (SPDX 2.3, CycloneDX 1.5)
F2. Automated component discovery and tracking
F3. CPE matching for product identification
F4. Package URL (purl) correlation
F5. Automated patch status tracking
F6. Vendor product mapping via CPE
F7. CVE severity scoring (CVSS 3.1)
F8. EPSS (Exploit Prediction Scoring System) integration
F9. Automated impact calculation with asset criticality weighting
F10. Psychometric threat actor profiling (This is very important, refernce)
F11. Academic research integration 
F12. multi-sector design
F12.1 Multi-sector design, inlcude All Critical infrastructure sectors with specific asset models
F12.2 Incude all Subsectors (89 subsectors) with specific asset models (perhaps as labels to optimize quries) think about this
F15  IoT Devices (29 node types)
F16  Energy Grid (68 node types - substations, transformers, generators)
F17  Manufacturing (21 node types - robots, CNC, assembly lines)
F18  Smart Buildings (60 node types - HVAC, lighting, access control)
F19  Water Systems (26 node types - pumps, valves, treatment plants)
F20  Transportation 
F21  Healthcare 
F22 Financial Services 
F23 list each critical sector as a requirement

## Compliance Scheme

FC1 IEC 62443 (complete industrial security standard)
FC2 NIST CSF 2.0 (full framework mapping)
FC3 NVD CVE feed (real-time API)
FC4 CISA KEV (Known Exploited Vulnerabilities)
FC5 STIX/TAXII 2.1 integration
FC6 MITRE ATT&CK Enterprise + ICS (complete)
FC7 Threat intelligence fusion (multi-source correlation)
FC8 Exploit prediction (EPSS scores)
FC9 Threat actor attribution
F10 Attack Campaign analysis
F11 IOC correlation
F12 Academic research, report and publication ingestion
F13 Dark web monitoring, searching and ingestion

# Critical Capabilities

C1. Complete network topology with firewall rules
C2. CVE-to-CWE-to-CAPEC-to-ATT&CK chain
C3. Threat actor TTP correlation
C4. Cyber-physical attack path modeling
C5. Entry point identification (internet-exposed assets)
C6. Firewall rule validation along paths
C7. MITRE ATT&CK technique mapping
C8. Known threat actor analysis
C9. Cascading failure simulation
C10.Operational impact prediction (SIL levels, safety functions)
C11.Network topology mapping (CONNECTED_TO relationships)
C12.Threat actor profiling (unique psychometric approach)
C13 Automatic SBOM scanning across all components
C14 Real-time CVE-to-component matching via CPE/purl
C15 Patch status tracking per component
C16 Criticality-weighted impact assessment

Design Speciciations



Node TYPES
| Domain | Node Count | Examples |
|--------|------------|----------|
| IT Infrastructure | 89 | Server, NetworkDevice, DataCenter, CloudInstance, Container, Hypervisor |
| IoT Devices | 29 | Sensor, Actuator, Gateway, SmartDevice, WearableDevice |
| Energy Grid | 68 | Substation, Transformer, Generator, SolarPanel, WindTurbine, EnergyStorage |
| Manufacturing | 21 | Robot, ConveyorBelt, CNC_Machine, QualityInspection, Assembly_Station |
| Smart Buildings | 60 | HVAC_System, Lighting_Controller, Access_Control, Elevator, Fire_Alarm |
| Water Systems | 26 | Pump, Valve, Tank, Treatment_Plant, Distribution_Network |
| Cybersecurity (MITRE) | 10 types / 2,290 instances | Tactic, Technique, SubTechnique, Software, Group, Mitigation, DataSource |
| Vulnerability Management | 28 | CVE, CWE, CAPEC, SBOM, SoftwareComponent, HardwareComponent, PatchStatus |
| SAREF Core | 85 | Device, Function, Command, State, Service, Property, Measurement |
| Critical Requirements | 35 | SafetyFunction, SecurityZone, RedundancyGroup, EmergencyProcedure |


**Comprehensive Schema - 200+ Relationship Types:**
- All test schema relationships PLUS:
- SUPPLIES_POWER
- CONTROLS_TEMPERATURE
- MONITORS_PRESSURE
- TRIGGERS_ALARM
- INITIATES_SHUTDOWN
- COMMUNICATES_VIA
- BACKED_UP_BY
- FAILS_OVER_TO
- SCALES_HORIZONTALLY
- ORCHESTRATES
- CONTAINS_COMPONENT (SBOM)
- HAS_PATCH_STATUS
- AFFECTS_PRODUCT
- USES_ATTACK_PATTERN
- BELONGS_TO_TACTIC
- MITIGATED_BY_CONTROL
**(100+ additional relationships for multi-sector coverage) - ALL RELATIOSNYOU MUST COMPLETE THIS: Add the additional 100+ types** 


**Designed Data Sources:**
- NVD CVE feed (real-time API integration)
- MITRE ATT&CK Enterprise + ICS (complete frameworks)
- NIST National Vulnerability Database
- CISA Known Exploited Vulnerabilities
- STIX/TAXII 2.1 feeds
- SBOM repositories (SPDX 2.3, CycloneDX 1.5)
- IEC 62443 compliance mappings
- NERC-CIP regulatory data
- Asset discovery tools (automated SBOM generation)
- Network scanning (automated topology mapping)
- SCADA/ICS protocol monitoring
- Building management system integration
- Energy grid SCADA integration

