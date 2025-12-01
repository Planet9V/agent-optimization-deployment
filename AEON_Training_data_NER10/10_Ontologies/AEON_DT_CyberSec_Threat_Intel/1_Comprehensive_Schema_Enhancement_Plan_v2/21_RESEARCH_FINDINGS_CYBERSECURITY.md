# Cybersecurity Ontology Research Findings

**File:** 21_RESEARCH_FINDINGS_CYBERSECURITY.md
**Created:** 2025-10-30 00:00:00 UTC
**Modified:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Author:** Research Analysis Agent
**Purpose:** Comprehensive documentation of cybersecurity ontology research including ICS-SEC-KG, MITRE-CTI, ATT&CK-STIX, and UCO
**Status:** ACTIVE

## Executive Summary

This document presents comprehensive research findings from four major cybersecurity ontology frameworks:

1. **ICS-SEC-KG**: Industrial Control System Security Knowledge Graph
2. **MITRE-CTI**: Cyber Threat Intelligence ontology
3. **MITRE ATT&CK + STIX 2.1**: Adversarial tactics, techniques, and structured threat intelligence
4. **UCO**: Unified Cyber Ontology for digital forensics and investigation

**Key Findings:**
- ICS-SEC-KG provides OT/ICS-specific vulnerability and attack modeling
- MITRE-CTI offers comprehensive CVE, CWE, and CAPEC integration
- ATT&CK for ICS covers 14 tactics and 81 techniques specific to industrial systems
- STIX 2.1 provides standardized threat intelligence exchange format
- UCO enables forensic investigation and evidence chain modeling

**Critical Integration Points:**
- All four ontologies complement each other for comprehensive cybersecurity coverage
- STIX 2.1 serves as primary threat intelligence exchange format
- UCO provides forensic investigation layer
- ICS-SEC-KG and ATT&CK for ICS address OT/ICS-specific threats
- MITRE-CTI connects vulnerabilities (CVE/CWE) with attack patterns (CAPEC)

## 1. ICS-SEC-KG: Industrial Control System Security Knowledge Graph

### 1.1 Overview

**Source**: Research paper and implementation from academic/industrial collaboration
**Domain**: OT/ICS cybersecurity
**Format**: OWL ontology + RDF knowledge graph
**Coverage**: ICS vulnerabilities, attacks, components, protocols

**Primary Objectives:**
- Model ICS-specific vulnerabilities and exploits
- Connect attack patterns to industrial components
- Represent ICS network topology and protocols
- Enable automated threat analysis for OT environments

### 1.2 Core Architecture

**Main Classes:**
```turtle
ics:ICSComponent
  ├── ics:Controller
  │   ├── ics:PLC
  │   ├── ics:DCS
  │   ├── ics:RTU
  │   └── ics:PAC
  ├── ics:HMI
  ├── ics:SCADA
  ├── ics:FieldDevice
  │   ├── ics:Sensor
  │   ├── ics:Actuator
  │   └── ics:Transmitter
  ├── ics:NetworkDevice
  │   ├── ics:Switch
  │   ├── ics:Router
  │   └── ics:Firewall
  └── ics:EngineeringWorkstation

ics:Vulnerability
  ├── ics:BufferOverflow
  ├── ics:AuthenticationBypass
  ├── ics:CommandInjection
  ├── ics:DenialOfService
  ├── ics:InformationDisclosure
  └── ics:PrivilegeEscalation

ics:Attack
  ├── ics:NetworkAttack
  │   ├── ics:ManInTheMiddle
  │   ├── ics:ReplayAttack
  │   └── ics:PacketInjection
  ├── ics:ApplicationAttack
  │   ├── ics:MalwareInjection
  │   ├── ics:FirmwareTampering
  │   └── ics:ConfigurationModification
  └── ics:PhysicalAttack
      ├── ics:DeviceTampering
      └── ics:PhysicalAccess

ics:Protocol
  ├── ics:Modbus
  ├── ics:DNP3
  ├── ics:IEC60870
  ├── ics:IEC61850
  ├── ics:OPCUA
  ├── ics:PROFINET
  ├── ics:EtherNetIP
  └── ics:BACnet

ics:Asset
  ├── ics:CriticalAsset
  ├── ics:ProductionAsset
  └── ics:SupportAsset
```

### 1.3 Object Properties

#### Component Relationships
```turtle
ics:controls
  rdfs:domain ics:Controller
  rdfs:range ics:FieldDevice
  rdfs:comment "Controller operates field device"

ics:monitorsBy
  rdfs:domain ics:ICSComponent
  rdfs:range ics:HMI
  rdfs:comment "Component monitored by HMI"

ics:connectsTo
  rdfs:domain ics:ICSComponent
  rdfs:range ics:ICSComponent
  rdfs:comment "Network or logical connection"

ics:communicatesUsing
  rdfs:domain ics:ICSComponent
  rdfs:range ics:Protocol
  rdfs:comment "Communication protocol used"

ics:partOfSystem
  rdfs:domain ics:ICSComponent
  rdfs:range ics:ICSSystem
  rdfs:comment "Component belongs to system"
```

#### Vulnerability and Attack Relationships
```turtle
ics:hasVulnerability
  rdfs:domain ics:ICSComponent
  rdfs:range ics:Vulnerability
  rdfs:comment "Component has known vulnerability"

ics:exploitsVulnerability
  rdfs:domain ics:Attack
  rdfs:range ics:Vulnerability
  rdfs:comment "Attack exploits specific vulnerability"

ics:targetsComponent
  rdfs:domain ics:Attack
  rdfs:range ics:ICSComponent
  rdfs:comment "Attack targets component type"

ics:causesImpact
  rdfs:domain ics:Attack
  rdfs:range ics:Impact
  rdfs:comment "Attack results in impact"

ics:mitigatedBy
  rdfs:domain ics:Vulnerability
  rdfs:range ics:Mitigation
  rdfs:comment "Vulnerability addressed by mitigation"
```

#### Protocol-Specific Relationships
```turtle
ics:usesPort
  rdfs:domain ics:Protocol
  rdfs:range xsd:integer
  rdfs:comment "TCP/UDP port number"

ics:hasAuthenticationMechanism
  rdfs:domain ics:Protocol
  rdfs:range ics:AuthMechanism
  rdfs:comment "Protocol authentication method"

ics:hasEncryption
  rdfs:domain ics:Protocol
  rdfs:range xsd:boolean
  rdfs:comment "Protocol supports encryption"

ics:vulnerableToAttack
  rdfs:domain ics:Protocol
  rdfs:range ics:Attack
  rdfs:comment "Protocol vulnerable to attack type"
```

### 1.4 Data Properties

```turtle
ics:hasIPAddress
  rdfs:domain ics:ICSComponent
  rdfs:range xsd:string

ics:hasMACAddress
  rdfs:domain ics:ICSComponent
  rdfs:range xsd:string

ics:hasFirmwareVersion
  rdfs:domain ics:ICSComponent
  rdfs:range xsd:string

ics:hasManufacturer
  rdfs:domain ics:ICSComponent
  rdfs:range xsd:string

ics:hasModel
  rdfs:domain ics:ICSComponent
  rdfs:range xsd:string

ics:hasSerialNumber
  rdfs:domain ics:ICSComponent
  rdfs:range xsd:string

ics:hasCVEID
  rdfs:domain ics:Vulnerability
  rdfs:range xsd:string

ics:hasCVSSScore
  rdfs:domain ics:Vulnerability
  rdfs:range xsd:float

ics:hasPublishedDate
  rdfs:domain ics:Vulnerability
  rdfs:range xsd:dateTime

ics:hasSeverity
  rdfs:domain ics:Vulnerability
  rdfs:range xsd:string

ics:hasDescription
  rdfs:domain owl:Thing
  rdfs:range xsd:string

ics:requiresAuthentication
  rdfs:domain ics:Attack
  rdfs:range xsd:boolean

ics:requiresPhysicalAccess
  rdfs:domain ics:Attack
  rdfs:range xsd:boolean
```

### 1.5 ICS-Specific Vulnerability Patterns

#### PLC Vulnerabilities
```turtle
:PLC_Vulnerability_Pattern a owl:Class ;
  rdfs:subClassOf ics:Vulnerability ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ics:affectsComponent ;
    owl:someValuesFrom ics:PLC
  ] .

# Example: Siemens S7 Authentication Bypass
:CVE_2019_13945 a ics:AuthenticationBypass ;
  ics:hasCVEID "CVE-2019-13945" ;
  ics:hasCVSSScore "10.0"^^xsd:float ;
  ics:affectsComponent :Siemens_S7_1200 ;
  ics:affectsFirmwareVersion "V4.4.0" ;
  ics:allowsRemoteExecution true ;
  ics:requiresAuthentication false ;
  ics:exploitAvailable true ;
  ics:exploitComplexity "Low" .

:Siemens_S7_1200 a ics:PLC ;
  ics:hasManufacturer "Siemens" ;
  ics:hasModel "S7-1200" ;
  ics:communicatesUsing ics:S7Protocol ;
  ics:hasVulnerability :CVE_2019_13945 .
```

#### SCADA System Vulnerabilities
```turtle
:SCADA_Vulnerability_Pattern a owl:Class ;
  rdfs:subClassOf ics:Vulnerability ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ics:affectsComponent ;
    owl:someValuesFrom ics:SCADA
  ] .

# Example: Schneider Electric SCADA SQL Injection
:CVE_2020_7559 a ics:CommandInjection ;
  ics:hasCVEID "CVE-2020-7559" ;
  ics:hasCVSSScore "9.8"^^xsd:float ;
  ics:affectsComponent :Schneider_SCADA ;
  ics:allowsDatabaseAccess true ;
  ics:allowsRemoteExecution true ;
  ics:requiresAuthentication false .
```

#### HMI Vulnerabilities
```turtle
:HMI_Vulnerability_Pattern a owl:Class ;
  rdfs:subClassOf ics:Vulnerability ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ics:affectsComponent ;
    owl:someValuesFrom ics:HMI
  ] .

# Example: Rockwell FactoryTalk View Privilege Escalation
:CVE_2021_27471 a ics:PrivilegeEscalation ;
  ics:hasCVEID "CVE-2021-27471" ;
  ics:hasCVSSScore "7.8"^^xsd:float ;
  ics:affectsComponent :FactoryTalkView ;
  ics:allowsAdminAccess true ;
  ics:requiresAuthentication true ;
  ics:requiresLowPrivilegeAccess true .
```

### 1.6 Protocol-Specific Vulnerabilities

#### Modbus Protocol
```turtle
ics:Modbus a ics:Protocol ;
  ics:usesPort 502 ;
  ics:hasEncryption false ;
  ics:hasAuthentication false ;
  ics:vulnerableToAttack ics:PacketInjection ;
  ics:vulnerableToAttack ics:ManInTheMiddle ;
  ics:vulnerableToAttack ics:ReplayAttack .

:Modbus_MITM_Attack a ics:ManInTheMiddle ;
  ics:targetsProtocol ics:Modbus ;
  ics:exploitsVulnerability :Modbus_NoEncryption ;
  ics:allowsCommandInjection true ;
  ics:allowsDataModification true ;
  ics:requiresNetworkAccess true ;
  ics:requiresAuthentication false .

:Modbus_NoEncryption a ics:InformationDisclosure ;
  ics:affectsProtocol ics:Modbus ;
  ics:allowsTrafficSniffing true ;
  ics:exposesCredentials false ;  # No credentials in Modbus
  ics:exposesProcessData true .
```

#### DNP3 Protocol
```turtle
ics:DNP3 a ics:Protocol ;
  ics:usesPort 20000 ;
  ics:hasEncryption false ;  # Unless DNP3 Secure Authentication
  ics:hasAuthentication false ;  # In basic DNP3
  ics:vulnerableToAttack ics:ReplayAttack ;
  ics:vulnerableToAttack ics:PacketInjection .

:DNP3_Replay_Attack a ics:ReplayAttack ;
  ics:targetsProtocol ics:DNP3 ;
  ics:exploitsVulnerability :DNP3_NoSequenceValidation ;
  ics:allowsCommandReplay true ;
  ics:allowsControlManipulation true .
```

#### OPC-UA Protocol
```turtle
ics:OPCUA a ics:Protocol ;
  ics:usesPort 4840 ;
  ics:hasEncryption true ;
  ics:hasAuthentication true ;
  ics:hasSignature true ;
  ics:securityMode [
    ics:None
    ics:Sign
    ics:SignAndEncrypt
  ] .

# OPC-UA is more secure but still has implementation vulnerabilities
:OPCUA_Implementation_Vuln a ics:Vulnerability ;
  ics:affectsProtocol ics:OPCUA ;
  ics:vulnerabilityType "Implementation Flaw" ;
  ics:hasCVEID "CVE-2022-XXXXX" ;
  ics:requiresSecurityModeNone true .
```

### 1.7 Attack Scenario Modeling

#### Attack Chain Representation
```turtle
:Stuxnet_Attack_Chain a ics:AttackScenario ;
  ics:hasPhase :Initial_Access ;
  ics:hasPhase :Lateral_Movement ;
  ics:hasPhase :PLC_Payload_Delivery ;
  ics:hasPhase :Process_Manipulation ;
  ics:targetsIndustry "Nuclear" ;
  ics:targetsSector "Energy" .

:Initial_Access a ics:AttackPhase ;
  ics:usesTool "USB Drive" ;
  ics:exploitsVulnerability :Windows_LNK_Vulnerability ;
  ics:nextPhase :Lateral_Movement .

:Lateral_Movement a ics:AttackPhase ;
  ics:usesTool "Network Worm" ;
  ics:exploitsVulnerability :Windows_Print_Spooler ;
  ics:targetsComponent ics:EngineeringWorkstation ;
  ics:nextPhase :PLC_Payload_Delivery .

:PLC_Payload_Delivery a ics:AttackPhase ;
  ics:usesTool "Step7 Project File" ;
  ics:exploitsVulnerability :Siemens_S7_No_Code_Signing ;
  ics:targetsComponent ics:PLC ;
  ics:modifiesFirmware true ;
  ics:nextPhase :Process_Manipulation .

:Process_Manipulation a ics:AttackPhase ;
  ics:manipulatesProcess "Centrifuge Speed" ;
  ics:causesPhysicalDamage true ;
  ics:hidesFromOperator true .
```

#### Multi-Stage Attack Pattern
```turtle
:Generic_ICS_Attack a ics:AttackPattern ;
  ics:hasStage [
    ics:Reconnaissance
    ics:InitialCompromise
    ics:EstablishFoothold
    ics:EscalatePrivileges
    ics:InternalReconnaissance
    ics:MoveToOT
    ics:DiscoverICS
    ics:DevelopCapability
    ics:TestCapability
    ics:DeliverPayload
    ics:ImpactOperation
  ] .
```

### 1.8 ICS Network Topology Modeling

#### Purdue Model Representation
```turtle
:Purdue_Level_0 a ics:NetworkZone ;
  ics:levelName "Physical Process" ;
  ics:contains ics:Sensor ;
  ics:contains ics:Actuator ;
  ics:connectsToLevel :Purdue_Level_1 .

:Purdue_Level_1 a ics:NetworkZone ;
  ics:levelName "Basic Control" ;
  ics:contains ics:PLC ;
  ics:contains ics:RTU ;
  ics:connectsToLevel :Purdue_Level_0 ;
  ics:connectsToLevel :Purdue_Level_2 .

:Purdue_Level_2 a ics:NetworkZone ;
  ics:levelName "Supervisory Control" ;
  ics:contains ics:HMI ;
  ics:contains ics:SCADA ;
  ics:connectsToLevel :Purdue_Level_1 ;
  ics:connectsToLevel :Purdue_Level_3 .

:Purdue_Level_3 a ics:NetworkZone ;
  ics:levelName "Plant Operations" ;
  ics:contains ics:EngineeringWorkstation ;
  ics:contains ics:Historian ;
  ics:connectsToLevel :Purdue_Level_2 ;
  ics:connectsToLevel :Purdue_Level_4 .

:Purdue_Level_4 a ics:NetworkZone ;
  ics:levelName "Enterprise" ;
  ics:contains "ERP System" ;
  ics:contains "MES System" ;
  ics:connectsToLevel :Purdue_Level_3 ;
  ics:connectsToLevel :Purdue_Level_5 .

:Purdue_Level_5 a ics:NetworkZone ;
  ics:levelName "Enterprise Network" ;
  ics:contains "Corporate IT" ;
  ics:connectsToLevel :Purdue_Level_4 .
```

#### Network Segmentation
```turtle
:ICS_Network_Segment a ics:NetworkSegment ;
  ics:hasSegmentType "OT Network" ;
  ics:hasFirewall :ICS_Firewall ;
  ics:hasIDS :ICS_IDS ;
  ics:isolatedFromInternet true ;
  ics:hasAccessControl :NetworkAccessControl .

:DMZ_Segment a ics:NetworkSegment ;
  ics:hasSegmentType "DMZ" ;
  ics:bridgesNetworks :IT_Network ;
  ics:bridgesNetworks :ICS_Network_Segment ;
  ics:requiresAuthentication true .
```

### 1.9 Impact Assessment

#### Impact Classification
```turtle
ics:Impact
  ├── ics:SafetyImpact
  │   ├── ics:PersonnelInjury
  │   ├── ics:EquipmentDamage
  │   └── ics:EnvironmentalHazard
  ├── ics:ProductionImpact
  │   ├── ics:ProcessDisruption
  │   ├── ics:ProductionLoss
  │   └── ics:QualityDegradation
  ├── ics:FinancialImpact
  │   ├── ics:RevenueLoss
  │   ├── ics:RecoveryCost
  │   └── ics:RegulatoryFine
  └── ics:ReputationalImpact
      ├── ics:BrandDamage
      └── ics:CustomerTrustLoss

:Attack_Impact_Assessment a ics:ImpactAnalysis ;
  ics:assessesAttack :Specific_Attack ;
  ics:hasSafetyImpact :High ;
  ics:hasProductionImpact :Critical ;
  ics:hasFinancialImpact :Severe ;
  ics:estimatedDowntime "72 hours"^^xsd:string ;
  ics:estimatedCost "5000000"^^xsd:integer .
```

### 1.10 Mitigation Strategies

#### Mitigation Taxonomy
```turtle
ics:Mitigation
  ├── ics:TechnicalControl
  │   ├── ics:NetworkSegmentation
  │   ├── ics:Encryption
  │   ├── ics:Authentication
  │   ├── ics:AccessControl
  │   ├── ics:IntrusionDetection
  │   ├── ics:PatchManagement
  │   └── ics:BackupRecovery
  ├── ics:OperationalControl
  │   ├── ics:SecurityMonitoring
  │   ├── ics:IncidentResponse
  │   ├── ics:ChangeManagement
  │   └── ics:SecurityTraining
  └── ics:PhysicalControl
      ├── ics:PhysicalAccess
      ├── ics:EnvironmentalControl
      └── ics:AssetManagement

:Vulnerability_Mitigation a ics:MitigationPlan ;
  ics:mitigatesVulnerability :Specific_CVE ;
  ics:implementsControl ics:PatchManagement ;
  ics:implementsControl ics:NetworkSegmentation ;
  ics:effectiveDate "2025-10-30"^^xsd:date ;
  ics:verificationStatus "Implemented" .
```

## 2. MITRE-CTI: Cyber Threat Intelligence Ontology

### 2.1 Overview

**Source**: MITRE Corporation
**Repository**: https://github.com/mitre/cti
**Formats**: STIX 2.1, JSON
**Coverage**: CVE, CWE, CAPEC, ATT&CK

**Core Components:**
1. **CVE**: Common Vulnerabilities and Exposures
2. **CWE**: Common Weakness Enumeration
3. **CAPEC**: Common Attack Pattern Enumeration and Classification
4. **ATT&CK**: Adversarial Tactics, Techniques, and Common Knowledge

### 2.2 CVE (Common Vulnerabilities and Exposures)

#### CVE Data Model
```json
{
  "CVE_data_type": "CVE",
  "CVE_data_format": "MITRE",
  "CVE_data_version": "4.0",
  "CVE_data_meta": {
    "ID": "CVE-2023-12345",
    "ASSIGNER": "cve@mitre.org",
    "STATE": "PUBLIC"
  },
  "description": {
    "description_data": [
      {
        "lang": "eng",
        "value": "Buffer overflow vulnerability description"
      }
    ]
  },
  "problemtype": {
    "problemtype_data": [
      {
        "description": [
          {
            "lang": "eng",
            "value": "CWE-119",
            "cweId": "CWE-119"
          }
        ]
      }
    ]
  },
  "affects": {
    "vendor": {
      "vendor_data": [
        {
          "vendor_name": "Siemens",
          "product": {
            "product_data": [
              {
                "product_name": "SIMATIC S7-1200",
                "version": {
                  "version_data": [
                    {
                      "version_value": "V4.4.0",
                      "version_affected": "<="
                    }
                  ]
                }
              }
            ]
          }
        }
      ]
    }
  },
  "impact": {
    "cvss": {
      "version": "3.1",
      "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "baseScore": 9.8,
      "baseSeverity": "CRITICAL"
    }
  },
  "references": {
    "reference_data": [
      {
        "url": "https://www.siemens.com/...",
        "name": "Siemens Security Advisory",
        "refsource": "CONFIRM"
      }
    ]
  }
}
```

#### CVE as RDF/OWL
```turtle
:CVE_2023_12345 a mitre:CVE ;
  mitre:cveID "CVE-2023-12345" ;
  mitre:publishedDate "2023-06-15"^^xsd:date ;
  mitre:lastModifiedDate "2023-06-20"^^xsd:date ;
  mitre:description "Buffer overflow allows remote code execution" ;
  mitre:hasCWE :CWE_119 ;
  mitre:affectsVendor "Siemens" ;
  mitre:affectsProduct "SIMATIC S7-1200" ;
  mitre:affectsVersion "V4.4.0" ;
  mitre:cvssV3BaseScore "9.8"^^xsd:float ;
  mitre:cvssV3Vector "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H" ;
  mitre:severity "CRITICAL" ;
  mitre:exploitAvailable true ;
  mitre:patchAvailable true ;
  mitre:hasReference <https://www.siemens.com/security> .
```

#### CVSS v3.1 Metrics
```turtle
mitre:CVSS_V3_Metrics
  ├── mitre:AttackVector
  │   ├── mitre:Network (AV:N)
  │   ├── mitre:Adjacent (AV:A)
  │   ├── mitre:Local (AV:L)
  │   └── mitre:Physical (AV:P)
  ├── mitre:AttackComplexity
  │   ├── mitre:Low (AC:L)
  │   └── mitre:High (AC:H)
  ├── mitre:PrivilegesRequired
  │   ├── mitre:None (PR:N)
  │   ├── mitre:Low (PR:L)
  │   └── mitre:High (PR:H)
  ├── mitre:UserInteraction
  │   ├── mitre:None (UI:N)
  │   └── mitre:Required (UI:R)
  ├── mitre:Scope
  │   ├── mitre:Unchanged (S:U)
  │   └── mitre:Changed (S:C)
  ├── mitre:ConfidentialityImpact
  │   ├── mitre:None (C:N)
  │   ├── mitre:Low (C:L)
  │   └── mitre:High (C:H)
  ├── mitre:IntegrityImpact
  │   ├── mitre:None (I:N)
  │   ├── mitre:Low (I:L)
  │   └── mitre:High (I:H)
  └── mitre:AvailabilityImpact
      ├── mitre:None (A:N)
      ├── mitre:Low (A:L)
      └── mitre:High (A:H)
```

### 2.3 CWE (Common Weakness Enumeration)

#### CWE Hierarchy
```turtle
cwe:Weakness
  ├── cwe:SoftwareWeakness
  │   ├── cwe:MemoryCorruption
  │   │   ├── CWE-119: Buffer Overflow
  │   │   ├── CWE-120: Buffer Copy without Checking Size
  │   │   ├── CWE-121: Stack-based Buffer Overflow
  │   │   ├── CWE-122: Heap-based Buffer Overflow
  │   │   ├── CWE-125: Out-of-bounds Read
  │   │   └── CWE-787: Out-of-bounds Write
  │   ├── cwe:InjectionWeakness
  │   │   ├── CWE-77: Command Injection
  │   │   ├── CWE-78: OS Command Injection
  │   │   ├── CWE-79: Cross-site Scripting
  │   │   ├── CWE-89: SQL Injection
  │   │   └── CWE-94: Code Injection
  │   ├── cwe:AuthenticationWeakness
  │   │   ├── CWE-287: Improper Authentication
  │   │   ├── CWE-288: Authentication Bypass Using Alternate Path
  │   │   ├── CWE-306: Missing Authentication
  │   │   └── CWE-798: Hard-coded Credentials
  │   ├── cwe:AccessControlWeakness
  │   │   ├── CWE-269: Improper Privilege Management
  │   │   ├── CWE-284: Improper Access Control
  │   │   └── CWE-862: Missing Authorization
  │   └── cwe:CryptographicWeakness
  │       ├── CWE-259: Hard-coded Password
  │       ├── CWE-311: Missing Encryption
  │       ├── CWE-327: Broken or Risky Cryptographic Algorithm
  │       └── CWE-798: Use of Hard-coded Credentials
  └── cwe:HardwareWeakness
      ├── CWE-1191: Hardware Not Clear on Read
      ├── CWE-1220: Insufficient Granularity of Access Control
      └── CWE-1260: Improper Handling of Overlap Between Protected Memory Ranges
```

#### CWE-119 Example (Buffer Overflow)
```turtle
:CWE_119 a cwe:Weakness ;
  cwe:cweID "CWE-119" ;
  cwe:name "Improper Restriction of Operations within Bounds of Memory Buffer" ;
  cwe:description "Software performs operations on memory buffer without checking bounds" ;
  cwe:extendedDescription "Can result in buffer overflows, overwrites, out-of-bounds reads" ;
  cwe:relatedWeakness :CWE_120 ;
  cwe:relatedWeakness :CWE_121 ;
  cwe:relatedWeakness :CWE_122 ;
  cwe:childOf :CWE_118 ;
  cwe:parentOf :CWE_120 ;
  cwe:canPrecede :CWE_94 ;  # Code Injection
  cwe:likelihood "High" ;
  cwe:typicalSeverity "High" ;
  cwe:detectionMethods [
    cwe:StaticAnalysis
    cwe:DynamicAnalysis
    cwe:FuzzTesting
  ] ;
  cwe:potentialMitigations [
    cwe:InputValidation
    cwe:BoundsChecking
    cwe:UseOfSafeLibraries
    cwe:MemoryProtection
  ] .
```

#### CWE Views
```turtle
cwe:View
  ├── cwe:ResearchConcepts (CWE-1000)
  ├── cwe:SoftwareDevelopment (CWE-699)
  ├── cwe:HardwareDesign (CWE-1194)
  ├── cwe:ICSOperationalTechnology (CWE-1010)
  │   # ICS-specific weaknesses
  │   ├── CWE-494: Download of Code Without Integrity Check
  │   ├── CWE-568: Access of Uninitialized Resource
  │   ├── CWE-829: Local File Inclusion
  │   └── CWE-912: Hidden Functionality
  └── cwe:Top25MostDangerous (CWE-1350)
```

### 2.4 CAPEC (Common Attack Pattern Enumeration)

#### CAPEC Hierarchy
```turtle
capec:AttackPattern
  ├── capec:Mechanism_based
  │   ├── capec:Abuse_Functionality
  │   │   ├── CAPEC-1: Accessing Functionality Not Properly Constrained
  │   │   ├── CAPEC-19: Embedding Scripts in Non-Script Elements
  │   │   └── CAPEC-665: Exploitation of Thunderbolt Protection Flaws
  │   ├── capec:ManipulateData
  │   │   ├── CAPEC-13: Subverting Environment Variable Values
  │   │   ├── CAPEC-14: Client-side Injection-induced Buffer Overflow
  │   │   └── CAPEC-28: Fuzzing
  │   ├── capec:InjectUnexpectedItems
  │   │   ├── CAPEC-10: Buffer Overflow via Environment Variables
  │   │   ├── CAPEC-42: MIME Conversion
  │   │   └── CAPEC-66: SQL Injection
  │   └── capec:BypassProtectionMechanism
  │       ├── CAPEC-21: Exploitation of Trusted Identifiers
  │       ├── CAPEC-115: Authentication Bypass
  │       └── CAPEC-633: Token Impersonation
  └── capec:Domain_based
      ├── capec:Software
      ├── capec:Hardware
      ├── capec:Communications
      ├── capec:Supply_Chain
      └── capec:Social_Engineering
```

#### CAPEC-112: Brute Force (ICS Relevant)
```turtle
:CAPEC_112 a capec:AttackPattern ;
  capec:capecID "CAPEC-112" ;
  capec:name "Brute Force" ;
  capec:description "Attacker systematically tries all possible values" ;
  capec:likelihood "Medium" ;
  capec:typicalSeverity "High" ;
  capec:abstraction "Standard" ;
  capec:status "Stable" ;
  capec:exploitsCWE :CWE_307 ;  # Improper Restriction of Excessive Authentication
  capec:exploitsCWE :CWE_521 ;  # Weak Password Requirements
  capec:prerequisite "System uses authentication" ;
  capec:prerequisite "No account lockout mechanism" ;
  capec:prerequisite "Weak password policy" ;
  capec:skillsRequired "Low" ;
  capec:resources "Password cracking tool" ;
  capec:consequences [
    capec:UnauthorizedAccess
    capec:PrivilegeEscalation
    capec:DataCompromise
  ] ;
  capec:mitigations [
    capec:AccountLockout
    capec:StrongPasswordPolicy
    capec:MultiFactorAuthentication
    capec:RateLimiting
  ] ;
  capec:relatedAttackPattern :CAPEC_49 ;  # Password Brute Forcing
  capec:relatedAttackPattern :CAPEC_565 . # Password Spraying
```

#### CAPEC-260: Credential Stuffing (ICS/SCADA Relevant)
```turtle
:CAPEC_260 a capec:AttackPattern ;
  capec:capecID "CAPEC-260" ;
  capec:name "Credential Stuffing" ;
  capec:description "Using stolen credentials from one system on another" ;
  capec:likelihood "High" ;
  capec:typicalSeverity "High" ;
  capec:exploitsCWE :CWE_262 ;  # Password Reuse
  capec:exploitsCWE :CWE_309 ;  # Missing Cryptographic Step
  capec:targetSystem "SCADA HMI" ;
  capec:targetSystem "Engineering Workstation" ;
  capec:targetSystem "Remote Access Portal" ;
  capec:prerequisite "User reuses passwords across systems" ;
  capec:prerequisite "Attacker has breached credential database" ;
  capec:skillsRequired "Low" ;
  capec:indicatorsOfCompromise [
    capec:MultipleFailedLogins
    capec:LoginsFromUnusualLocations
    capec:RapidSuccessionLogins
  ] .
```

#### ICS-Specific CAPEC Patterns
```turtle
# CAPEC patterns particularly relevant to ICS/OT

:CAPEC_ICS_Modbus_Injection a capec:AttackPattern ;
  capec:name "Modbus Command Injection" ;
  capec:domain "ICS/SCADA" ;
  capec:targetsProtocol "Modbus/TCP" ;
  capec:exploitsCWE :CWE_285 ;  # Improper Authorization
  capec:exploitsCWE :CWE_306 ;  # Missing Authentication
  capec:description "Injecting malicious Modbus commands into ICS network" ;
  capec:prerequisite "Access to Modbus network segment" ;
  capec:prerequisite "No authentication on Modbus protocol" ;
  capec:typicalSeverity "Critical" ;
  capec:consequences [
    capec:ProcessManipulation
    capec:EquipmentDamage
    capec:SafetyHazard
  ] .

:CAPEC_ICS_Replay_Attack a capec:AttackPattern ;
  capec:name "ICS Command Replay Attack" ;
  capec:domain "ICS/SCADA" ;
  capec:targetsProtocol [ "Modbus" "DNP3" "IEC-60870-5-104" ] ;
  capec:exploitsCWE :CWE_294 ;  # Authentication Bypass by Capture-replay
  capec:description "Capturing legitimate commands and replaying them" ;
  capec:prerequisite "Ability to sniff network traffic" ;
  capec:prerequisite "No sequence numbers or timestamps" ;
  capec:typicalSeverity "High" .

:CAPEC_ICS_False_Data_Injection a capec:AttackPattern ;
  capec:name "False Sensor Data Injection" ;
  capec:domain "ICS/SCADA" ;
  capec:exploitsCWE :CWE_345 ;  # Insufficient Verification of Data Authenticity
  capec:description "Injecting false sensor readings to HMI/SCADA" ;
  capec:consequence "Operators make decisions on false data" ;
  capec:typicalSeverity "Critical" ;
  capec:realWorldExample "Stuxnet manipulation of centrifuge data" .
```

### 2.5 CVE-CWE-CAPEC Relationships

#### Mapping Structure
```turtle
# Example: Buffer Overflow vulnerability chain

:CVE_2023_XXXXX a mitre:CVE ;
  mitre:cveID "CVE-2023-XXXXX" ;
  mitre:description "Buffer overflow in PLC firmware" ;
  mitre:hasCWE :CWE_119 ;  # Links to weakness
  mitre:exploitedByCAPEC :CAPEC_100 .  # Links to attack pattern

:CWE_119 a cwe:Weakness ;
  cwe:cweID "CWE-119" ;
  cwe:name "Buffer Overflow" ;
  cwe:canBeExploitedBy :CAPEC_100 ;
  cwe:canLeadTo :CWE_94 .  # Code Injection

:CAPEC_100 a capec:AttackPattern ;
  capec:capecID "CAPEC-100" ;
  capec:name "Overflow Buffers" ;
  capec:exploitsCWE :CWE_119 ;
  capec:leadsToCAPEC :CAPEC_14 .  # Client-side Injection

# Query to find attack path
SELECT ?cve ?cwe ?capec ?nextCapec WHERE {
  ?cve mitre:hasCWE ?cwe .
  ?cwe cwe:canBeExploitedBy ?capec .
  ?capec capec:leadsToCAPEC ?nextCapec .
}
```

#### Vulnerability-to-Exploit Chain
```turtle
:Exploit_Chain a mitre:AttackChain ;
  mitre:initialVulnerability :CVE_2023_12345 ;
  mitre:exploitsWeakness :CWE_119 ;
  mitre:usesAttackPattern :CAPEC_100 ;
  mitre:enablesAttackPattern :CAPEC_94 ;  # Man-in-the-Middle
  mitre:resultsin "Remote Code Execution" ;
  mitre:impactLevel "Critical" .
```

## 3. MITRE ATT&CK for ICS

### 3.1 Overview

**Source**: MITRE Corporation
**Matrix**: ATT&CK for Industrial Control Systems
**Coverage**: 14 Tactics, 81 Techniques
**Focus**: Adversary behavior in ICS/OT environments

### 3.2 ICS Tactics (14 Total)

```turtle
attack:Tactic
  ├── attack:InitialAccess
  ├── attack:Execution
  ├── attack:Persistence
  ├── attack:PrivilegeEscalation
  ├── attack:Evasion
  ├── attack:Discovery
  ├── attack:LateralMovement
  ├── attack:Collection
  ├── attack:CommandAndControl
  ├── attack:Inhibit ResponseFunction
  ├── attack:ImpairProcessControl
  ├── attack:Impact
  ├── attack:Establish Foothold (removed in v14)
  └── attack:Preparation (in some versions)
```

### 3.3 Initial Access Tactics

#### T0817: Drive-by Compromise
```turtle
:T0817 a attack:Technique ;
  attack:techniqueID "T0817" ;
  attack:name "Drive-by Compromise" ;
  attack:tactic attack:InitialAccess ;
  attack:description "Gaining access when user visits malicious website" ;
  attack:platformScope [ "Windows" "Engineering Workstation" "HMI" ] ;
  attack:dataSource [ "Network Traffic" "Web Proxy" "Process Monitoring" ] ;
  attack:mitigation attack:ApplicationWhitelisting ;
  attack:mitigation attack:NetworkSegmentation ;
  attack:exampleGroup "APT33" ;
  attack:realWorldCase "Triton/Trisis attack vector" .
```

#### T0819: Exploit Public-Facing Application
```turtle
:T0819 a attack:Technique ;
  attack:techniqueID "T0819" ;
  attack:name "Exploit Public-Facing Application" ;
  attack:tactic attack:InitialAccess ;
  attack:description "Exploiting vulnerabilities in internet-facing systems" ;
  attack:targetSystem [ "HMI Web Interface" "SCADA Web Portal" "VPN Gateway" ] ;
  attack:platformScope [ "Control Server" "Data Historian" "HMI" ] ;
  attack:dataSource [ "Application Logs" "Network Traffic" "IDS" ] ;
  attack:mitigation attack:PatchManagement ;
  attack:mitigation attack:NetworkSegmentation ;
  attack:mitigation attack:VulnerabilityScanning .
```

#### T0847: Replication Through Removable Media
```turtle
:T0847 a attack:Technique ;
  attack:techniqueID "T0847" ;
  attack:name "Replication Through Removable Media" ;
  attack:tactic attack:InitialAccess ;
  attack:tactic attack:LateralMovement ;
  attack:description "Using USB drives to move between air-gapped networks" ;
  attack:platformScope [ "Engineering Workstation" "HMI" "Control Server" ] ;
  attack:dataSource [ "File Monitoring" "Drive Enumeration" ] ;
  attack:mitigation attack:RemovableMediaControl ;
  attack:mitigation attack:ExecutionPrevention ;
  attack:realWorldCase "Stuxnet USB propagation" ;
  attack:realWorldCase "USB-based ICS malware" .
```

#### T0886: Remote Services
```turtle
:T0886 a attack:Technique ;
  attack:techniqueID "T0886" ;
  attack:name "Remote Services" ;
  attack:tactic attack:InitialAccess ;
  attack:tactic attack:LateralMovement ;
  attack:description "Using legitimate remote services for access" ;
  attack:targetService [ "VNC" "RDP" "TeamViewer" "SSH" ] ;
  attack:platformScope [ "Windows" "Linux" "Control Server" ] ;
  attack:dataSource [ "Authentication Logs" "Network Traffic" ] ;
  attack:mitigation attack:MultiFactorAuthentication ;
  attack:mitigation attack:NetworkSegmentation .
```

### 3.4 Execution Tactics

#### T0807: Command-Line Interface
```turtle
:T0807 a attack:Technique ;
  attack:techniqueID "T0807" ;
  attack:name "Command-Line Interface" ;
  attack:tactic attack:Execution ;
  attack:description "Executing commands via CLI on ICS systems" ;
  attack:platformScope [ "Windows" "Linux" "Engineering Workstation" ] ;
  attack:dataSource [ "Process Monitoring" "Command Execution Logs" ] ;
  attack:mitigation attack:ExecutionPrevention ;
  attack:mitigation attack:PrivilegedAccountManagement .
```

#### T0871: Execution through API
```turtle
:T0871 a attack:Technique ;
  attack:techniqueID "T0871" ;
  attack:name "Execution through API" ;
  attack:tactic attack:Execution ;
  attack:description "Using ICS protocol APIs to execute commands" ;
  attack:targetAPI [ "OPC-UA" "Modbus" "DNP3" "IEC-61850" ] ;
  attack:platformScope [ "Control Server" "Field Controller/RTU/PLC" ] ;
  attack:dataSource [ "Network Protocol Analysis" "API Monitoring" ] ;
  attack:mitigation attack:NetworkSegmentation ;
  attack:mitigation attack:ApplicationWhitelisting .
```

#### T0874: Project File Infection
```turtle
:T0874 a attack:Technique ;
  attack:techniqueID "T0874" ;
  attack:name "Project File Infection" ;
  attack:tactic attack:Execution ;
  attack:tactic attack:Persistence ;
  attack:description "Modifying PLC project files with malicious code" ;
  attack:platformScope [ "Engineering Workstation" "Control Server" ] ;
  attack:targetFileType [ ".s7p" ".rslogix" ".apj" ] ;
  attack:dataSource [ "File Monitoring" "Integrity Checking" ] ;
  attack:mitigation attack:CodeSigning ;
  attack:mitigation attack:FileIntegrityMonitoring ;
  attack:realWorldCase "Stuxnet Step7 project infection" .
```

### 3.5 Persistence Tactics

#### T0839: Module Firmware
```turtle
:T0839 a attack:Technique ;
  attack:techniqueID "T0839" ;
  attack:name "Module Firmware" ;
  attack:tactic attack:Persistence ;
  attack:description "Modifying firmware of ICS components" ;
  attack:platformScope [ "PLC" "RTU" "IED" "Safety System" ] ;
  attack:dataSource [ "Firmware Verification" "Network Traffic" ] ;
  attack:mitigation attack:FirmwareVerification ;
  attack:mitigation attack:PhysicalAccessControl ;
  attack:difficulty "High" ;
  attack:detectability "Very Low" ;
  attack:realWorldCase "Stuxnet PLC rootkit" .
```

#### T0891: Modify System Image
```turtle
:T0891 a attack:Technique ;
  attack:techniqueID "T0891" ;
  attack:name "Modify System Image" ;
  attack:tactic attack:Persistence ;
  attack:description "Replacing legitimate system images with malicious ones" ;
  attack:platformScope [ "HMI" "Engineering Workstation" "Control Server" ] ;
  attack:dataSource [ "File Monitoring" "Image Verification" ] ;
  attack:mitigation attack:CodeSigning ;
  attack:mitigation attack:BootIntegrityVerification .
```

#### T0859: Valid Accounts
```turtle
:T0859 a attack:Technique ;
  attack:techniqueID "T0859" ;
  attack:name "Valid Accounts" ;
  attack:tactic attack:Persistence ;
  attack:tactic attack:InitialAccess ;
  attack:description "Using legitimate credentials for persistent access" ;
  attack:accountType [ "Default Credentials" "Operator Account" "Engineer Account" ] ;
  attack:platformScope [ "Windows" "Control Server" "HMI" "Engineering Workstation" ] ;
  attack:dataSource [ "Authentication Logs" "Account Monitoring" ] ;
  attack:mitigation attack:PasswordPolicy ;
  attack:mitigation attack:MultiFactorAuthentication ;
  attack:mitigation attack:PrivilegedAccountManagement .
```

### 3.6 Evasion Tactics

#### T0849: Masquerading
```turtle
:T0849 a attack:Technique ;
  attack:techniqueID "T0849" ;
  attack:name "Masquerading" ;
  attack:tactic attack:Evasion ;
  attack:description "Disguising malicious code as legitimate programs" ;
  attack:platformScope [ "Windows" "Linux" "Engineering Workstation" ] ;
  attack:dataSource [ "File Monitoring" "Process Monitoring" ] ;
  attack:mitigation attack:ExecutionPrevention ;
  attack:mitigation attack:CodeSigning .
```

#### T0858: Change Operating Mode
```turtle
:T0858 a attack:Technique ;
  attack:techniqueID "T0858" ;
  attack:name "Change Operating Mode" ;
  attack:tactic attack:Evasion ;
  attack:tactic attack:ImpairProcessControl ;
  attack:description "Changing controller mode to prevent normal operation" ;
  attack:targetMode [ "Program Mode" "Stop Mode" "Maintenance Mode" ] ;
  attack:platformScope [ "PLC" "Safety System" "Control Server" ] ;
  attack:dataSource [ "Controller State Monitoring" "Network Protocol Analysis" ] ;
  attack:mitigation attack:AuthorizationEnforcement ;
  attack:mitigation attack:NetworkSegmentation ;
  attack:impact "Prevents legitimate control commands" .
```

#### T0872: Indicator Removal on Host
```turtle
:T0872 a attack:Technique ;
  attack:techniqueID "T0872" ;
  attack:name "Indicator Removal on Host" ;
  attack:tactic attack:Evasion ;
  attack:description "Deleting or modifying logs and artifacts" ;
  attack:targetArtifact [ "Event Logs" "Audit Logs" "File Timestamps" ] ;
  attack:platformScope [ "Windows" "Linux" "Engineering Workstation" ] ;
  attack:dataSource [ "File Monitoring" "Process Monitoring" ] ;
  attack:mitigation attack:RemoteDataStorage ;
  attack:mitigation attack:LogEncryption .
```

### 3.7 Discovery Tactics

#### T0840: Network Connection Enumeration
```turtle
:T0840 a attack:Technique ;
  attack:techniqueID "T0840" ;
  attack:name "Network Connection Enumeration" ;
  attack:tactic attack:Discovery ;
  attack:description "Enumerating network connections and topology" ;
  attack:platformScope [ "Windows" "Linux" "Engineering Workstation" ] ;
  attack:dataSource [ "Network Traffic" "Process Monitoring" ] ;
  attack:mitigation attack:NetworkSegmentation ;
  attack:detectionOpportunity "Network scanning activity" .
```

#### T0846: Remote System Discovery
```turtle
:T0846 a attack:Technique ;
  attack:techniqueID "T0846" ;
  attack:name "Remote System Discovery" ;
  attack:tactic attack:Discovery ;
  attack:description "Identifying remote systems on ICS network" ;
  attack:platformScope [ "Windows" "Control Server" "Data Historian" ] ;
  attack:tool [ "ping" "nmap" "arp" "netstat" ] ;
  attack:dataSource [ "Network Traffic" "Process Command-line" ] ;
  attack:mitigation attack:NetworkIntrustionPrevention .
```

#### T0877: I/O Image
```turtle
:T0877 a attack:Technique ;
  attack:techniqueID "T0877" ;
  attack:name "I/O Image" ;
  attack:tactic attack:Discovery ;
  attack:description "Reading controller I/O configuration and values" ;
  attack:platformScope [ "PLC" "Safety System" "RTU" ] ;
  attack:dataSource [ "Network Protocol Analysis" ] ;
  attack:purpose "Understand process control logic" ;
  attack:mitigation attack:NetworkSegmentation ;
  attack:realWorldCase "Stuxnet I/O reconnaissance" .
```

#### T0888: Remote System Information Discovery
```turtle
:T0888 a attack:Technique ;
  attack:techniqueID "T0888" ;
  attack:name "Remote System Information Discovery" ;
  attack:tactic attack:Discovery ;
  attack:description "Gathering system information from remote ICS devices" ;
  attack:informationType [ "Firmware Version" "Model Number" "Configuration" ] ;
  attack:platformScope [ "Control Server" "Field Controller" "HMI" ] ;
  attack:dataSource [ "Network Protocol Analysis" "Network Traffic" ] ;
  attack:mitigation attack:FilterNetworkTraffic .
```

### 3.8 Lateral Movement Tactics

#### T0866: Exploitation of Remote Services
```turtle
:T0866 a attack:Technique ;
  attack:techniqueID "T0866" ;
  attack:name "Exploitation of Remote Services" ;
  attack:tactic attack:LateralMovement ;
  attack:description "Exploiting vulnerabilities in remote services" ;
  attack:targetService [ "VNC" "RDP" "ICS Protocol Services" ] ;
  attack:platformScope [ "Windows" "Linux" "Control Server" ] ;
  attack:dataSource [ "Network Traffic" "Authentication Logs" ] ;
  attack:mitigation attack:PatchManagement ;
  attack:mitigation attack:NetworkSegmentation .
```

#### T0867: Lateral Tool Transfer
```turtle
:T0867 a attack:Technique ;
  attack:techniqueID "T0867" ;
  attack:name "Lateral Tool Transfer" ;
  attack:tactic attack:LateralMovement ;
  attack:description "Copying tools between systems for lateral movement" ;
  attack:platformScope [ "Windows" "Linux" "Engineering Workstation" ] ;
  attack:dataSource [ "File Monitoring" "Network Traffic" ] ;
  attack:mitigation attack:ExecutionPrevention ;
  attack:mitigation attack:NetworkSegmentation .
```

#### T0843: Program Download
```turtle
:T0843 a attack:Technique ;
  attack:techniqueID "T0843" ;
  attack:name "Program Download" ;
  attack:tactic attack:LateralMovement ;
  attack:tactic attack:Execution ;
  attack:description "Downloading malicious logic to controllers" ;
  attack:platformScope [ "PLC" "Safety System" "RTU" ] ;
  attack:dataSource [ "Network Protocol Analysis" "Controller Program Monitoring" ] ;
  attack:mitigation attack:CodeSigning ;
  attack:mitigation attack:AuthorizationEnforcement ;
  attack:realWorldCase "Stuxnet PLC payload download" ;
  attack:impactLevel "Critical" .
```

### 3.9 Inhibit Response Function

#### T0800: Activate Firmware Update Mode
```turtle
:T0800 a attack:Technique ;
  attack:techniqueID "T0800" ;
  attack:name "Activate Firmware Update Mode" ;
  attack:tactic attack:InhibitResponseFunction ;
  attack:description "Placing device in firmware update mode to prevent operation" ;
  attack:platformScope [ "PLC" "Safety System" "Field Controller" ] ;
  attack:dataSource [ "Controller State Logs" "Network Protocol Analysis" ] ;
  attack:mitigation attack:AuthorizationEnforcement ;
  attack:mitigation attack:PhysicalAccessControl ;
  attack:impact "Device unavailable for process control" .
```

#### T0816: Device Restart/Shutdown
```turtle
:T0816 a attack:Technique ;
  attack:techniqueID "T0816" ;
  attack:name "Device Restart/Shutdown" ;
  attack:tactic attack:InhibitResponseFunction ;
  attack:tactic attack:Impact ;
  attack:description "Restarting or shutting down ICS devices" ;
  attack:platformScope [ "PLC" "HMI" "Engineering Workstation" "Field Controller" ] ;
  attack:dataSource [ "Controller State Logs" "Network Protocol Analysis" ] ;
  attack:mitigation attack:AuthorizationEnforcement ;
  attack:mitigation attack:NetworkSegmentation ;
  attack:impact "Loss of view and control" ;
  attack:realWorldCase "Ukraine power grid attack 2015" .
```

#### T0835: Manipulation of Control
```turtle
:T0835 a attack:Technique ;
  attack:techniqueID "T0835" ;
  attack:name "Manipulation of Control" ;
  attack:tactic attack:InhibitResponseFunction ;
  attack:tactic attack:ImpairProcessControl ;
  attack:description "Manipulating control system logic or commands" ;
  attack:platformScope [ "Control Server" "HMI" "Field Controller" ] ;
  attack:dataSource [ "Controller Program Monitoring" "Network Protocol Analysis" ] ;
  attack:mitigation attack:CodeSigning ;
  attack:mitigation attack:OperatorTraining ;
  attack:realWorldCase "Stuxnet PLC logic manipulation" .
```

#### T0878: Alarm Suppression
```turtle
:T0878 a attack:Technique ;
  attack:techniqueID "T0878" ;
  attack:name "Alarm Suppression" ;
  attack:tactic attack:InhibitResponseFunction ;
  attack:description "Preventing alarms from reaching operators" ;
  attack:platformScope [ "HMI" "SCADA" "Alarm Server" ] ;
  attack:dataSource [ "Alarm History" "Application Logs" ] ;
  attack:mitigation attack:MultiFactorAuthentication ;
  attack:mitigation attack:AuditLogs ;
  attack:impact "Operators unaware of abnormal conditions" ;
  attack:realWorldCase "Triton/Trisis alarm suppression" .
```

### 3.10 Impair Process Control

#### T0806: Brute Force I/O
```turtle
:T0806 a attack:Technique ;
  attack:techniqueID "T0806" ;
  attack:name "Brute Force I/O" ;
  attack:tactic attack:ImpairProcessControl ;
  attack:description "Rapidly changing I/O values to damage equipment" ;
  attack:platformScope [ "PLC" "Field Controller" "RTU" ] ;
  attack:dataSource [ "Network Protocol Analysis" "Controller State Logs" ] ;
  attack:mitigation attack:RateLimiting ;
  attack:mitigation attack:AnomalyDetection ;
  attack:impact "Physical equipment damage" ;
  attack:realWorldCase "Stuxnet centrifuge speed manipulation" .
```

#### T0836: Modify Parameter
```turtle
:T0836 a attack:Technique ;
  attack:techniqueID "T0836" ;
  attack:name "Modify Parameter" ;
  attack:tactic attack:ImpairProcessControl ;
  attack:description "Modifying process parameters to unsafe values" ;
  attack:platformScope [ "Control Server" "HMI" "Field Controller" ] ;
  attack:dataSource [ "Network Protocol Analysis" "Parameter Change Logs" ] ;
  attack:mitigation attack:AuthorizationEnforcement ;
  attack:mitigation attack:ProcessAnomalyDetection ;
  attack:impact "Process operates outside safe parameters" .
```

#### T0856: Spoof Reporting Message
```turtle
:T0856 a attack:Technique ;
  attack:techniqueID "T0856" ;
  attack:name "Spoof Reporting Message" ;
  attack:tactic attack:ImpairProcessControl ;
  attack:description "Sending false sensor data to SCADA/HMI" ;
  attack:platformScope [ "Field Device/Sensor" "Field Controller" ] ;
  attack:dataSource [ "Network Protocol Analysis" "Data Consistency Checking" ] ;
  attack:mitigation attack:MessageAuthentication ;
  attack:mitigation attack:DataAnomalyDetection ;
  attack:impact "Operators make decisions on false data" ;
  attack:realWorldCase "Stuxnet false sensor readings" .
```

#### T0832: Manipulation of View
```turtle
:T0832 a attack:Technique ;
  attack:techniqueID "T0832" ;
  attack:name "Manipulation of View" ;
  attack:tactic attack:ImpairProcessControl ;
  attack:description "Manipulating HMI display to hide actual process state" ;
  attack:platformScope [ "HMI" "SCADA" "Data Historian" ] ;
  attack:dataSource [ "Application Logs" "Data Comparison" ] ;
  attack:mitigation attack:OperatorTraining ;
  attack:mitigation attack:DataIntegrityVerification ;
  attack:impact "Operators unaware of actual process conditions" ;
  attack:realWorldCase "Stuxnet HMI replay attack" .
```

### 3.11 Impact Tactics

#### T0879: Damage to Property
```turtle
:T0879 a attack:Technique ;
  attack:techniqueID "T0879" ;
  attack:name "Damage to Property" ;
  attack:tactic attack:Impact ;
  attack:description "Causing physical damage to equipment or infrastructure" ;
  attack:platformScope [ "Field Controller" "Field Device" ] ;
  attack:dataSource [ "Controller State Logs" "Physical Inspection" ] ;
  attack:mitigation attack:SafetySystem ;
  attack:mitigation attack:ProcessAnomalyDetection ;
  attack:impact "Equipment destruction, facility damage" ;
  attack:realWorldCase "Stuxnet centrifuge destruction" .
```

#### T0826: Loss of Availability
```turtle
:T0826 a attack:Technique ;
  attack:techniqueID "T0826" ;
  attack:name "Loss of Availability" ;
  attack:tactic attack:Impact ;
  attack:description "Making systems or processes unavailable" ;
  attack:platformScope [ "Control Server" "HMI" "Field Controller" ] ;
  attack:dataSource [ "Network Traffic" "Controller State Logs" ] ;
  attack:mitigation attack:RedundantSystems ;
  attack:mitigation attack:BackupOperationalCapability ;
  attack:impact "Production stoppage, revenue loss" ;
  attack:realWorldCase "Ukraine power grid outage" .
```

#### T0827: Loss of Control
```turtle
:T0827 a attack:Technique ;
  attack:techniqueID "T0827" ;
  attack:name "Loss of Control" ;
  attack:tactic attack:Impact ;
  attack:description "Operators unable to control industrial process" ;
  attack:platformScope [ "Control Server" "HMI" "Field Controller" ] ;
  attack:dataSource [ "Network Traffic" "Controller State Logs" ] ;
  attack:mitigation attack:ManualControls ;
  attack:mitigation attack:OperatorTraining ;
  attack:impact "Unable to respond to process upsets" .
```

#### T0828: Loss of Productivity and Revenue
```turtle
:T0828 a attack:Technique ;
  attack:techniqueID "T0828" ;
  attack:name "Loss of Productivity and Revenue" ;
  attack:tactic attack:Impact ;
  attack:description "Disrupting operations causing financial loss" ;
  attack:platformScope [ "Control Server" "Field Controller" ] ;
  attack:mitigation attack:BusinessContinuity ;
  attack:mitigation attack:IncidentResponsePlan ;
  attack:impact "Revenue loss, missed production targets" .
```

#### T0837: Loss of Protection
```turtle
:T0837 a attack:Technique ;
  attack:techniqueID "T0837" ;
  attack:name "Loss of Protection" ;
  attack:tactic attack:Impact ;
  attack:description "Compromising safety systems and protective measures" ;
  attack:platformScope [ "Safety System" ] ;
  attack:dataSource [ "Safety System Logs" ] ;
  attack:mitigation attack:FunctionalSafety ;
  attack:mitigation attack:IndependentSafetySystems ;
  attack:impact "Safety hazard, potential for injury/death" ;
  attack:realWorldCase "Triton/Trisis safety system attack" ;
  attack:severity "Critical" .
```

### 3.12 ATT&CK Groups (Threat Actors)

#### APT33 (Elfin)
```turtle
:APT33 a attack:Group ;
  attack:groupID "G0064" ;
  attack:name "APT33" ;
  attack:alias "Elfin" ;
  attack:alias "HOLMIUM" ;
  attack:suspectedAttribution "Iran" ;
  attack:firstSeen "2013" ;
  attack:targetSector [ "Aviation" "Energy" "Defense" ] ;
  attack:targetRegion [ "United States" "Saudi Arabia" "South Korea" ] ;
  attack:usesTechnique :T0817 ;  # Drive-by Compromise
  attack:usesTechnique :T0819 ;  # Exploit Public-Facing Application
  attack:usesMalware [ "Shamoon" "Stonedrill" ] ;
  attack:motive "Espionage and Disruption" .
```

#### TEMP.Veles (XENOTIME)
```turtle
:TEMP_Veles a attack:Group ;
  attack:groupID "G0088" ;
  attack:name "TEMP.Veles" ;
  attack:alias "XENOTIME" ;
  attack:suspectedAttribution "Russia" ;
  attack:firstSeen "2017" ;
  attack:targetSector [ "Energy" "Oil and Gas" "Critical Infrastructure" ] ;
  attack:targetRegion "Global" ;
  attack:usesTechnique :T0878 ;  # Alarm Suppression
  attack:usesTechnique :T0816 ;  # Device Restart/Shutdown
  attack:usesTechnique :T0837 ;  # Loss of Protection
  attack:usesMalware "Triton/Trisis" ;
  attack:motive "Sabotage" ;
  attack:capability "Safety System Compromise" ;
  attack:sophistication "High" ;
  attack:realWorldAttack "Triconex Safety System Attack (2017)" .
```

#### Sandworm Team (ELECTRUM)
```turtle
:Sandworm a attack:Group ;
  attack:groupID "G0034" ;
  attack:name "Sandworm Team" ;
  attack:alias "ELECTRUM" ;
  attack:alias "Telebots" ;
  attack:suspectedAttribution "Russia (GRU Unit 74455)" ;
  attack:firstSeen "2014" ;
  attack:targetSector [ "Energy" "Government" "Media" ] ;
  attack:targetRegion [ "Ukraine" "Europe" "United States" ] ;
  attack:usesTechnique :T0816 ;  # Device Restart/Shutdown
  attack:usesTechnique :T0826 ;  # Loss of Availability
  attack:usesTechnique :T0827 ;  # Loss of Control
  attack:usesMalware [ "BlackEnergy" "Industroyer/CrashOverride" "NotPetya" ] ;
  attack:motive "Geopolitical Disruption" ;
  attack:realWorldAttack "Ukraine Power Grid (2015, 2016)" ;
  attack:sophistication "Very High" .
```

#### Lazarus Group
```turtle
:Lazarus a attack:Group ;
  attack:groupID "G0032" ;
  attack:name "Lazarus Group" ;
  attack:alias "HIDDEN COBRA" ;
  attack:suspectedAttribution "North Korea" ;
  attack:firstSeen "2009" ;
  attack:targetSector [ "Defense" "Aerospace" "Financial" "Energy" ] ;
  attack:targetRegion "Global" ;
  attack:usesTechnique :T0866 ;  # Exploitation of Remote Services
  attack:usesTechnique :T0874 ;  # Project File Infection
  attack:motive [ "Financial Gain" "Espionage" "Disruption" ] ;
  attack:capability "Supply Chain Compromise" .
```

### 3.13 ATT&CK Software (Malware/Tools)

#### Triton/Trisis/HATMAN
```turtle
:Triton a attack:Software ;
  attack:softwareID "S1009" ;
  attack:name "Triton" ;
  attack:alias [ "Trisis" "HATMAN" ] ;
  attack:type "Malware" ;
  attack:firstSeen "2017" ;
  attack:targetPlatform "Schneider Electric Triconex Safety System" ;
  attack:capability "Safety System Manipulation" ;
  attack:usedByGroup :TEMP_Veles ;
  attack:implementsTechnique :T0878 ;  # Alarm Suppression
  attack:implementsTechnique :T0837 ;  # Loss of Protection
  attack:implementsTechnique :T0843 ;  # Program Download
  attack:description "Malware designed to compromise industrial safety systems" ;
  attack:impactLevel "Critical" ;
  attack:sophistication "Very High" .
```

#### Industroyer/CrashOverride
```turtle
:Industroyer a attack:Software ;
  attack:softwareID "S0604" ;
  attack:name "Industroyer" ;
  attack:alias "CrashOverride" ;
  attack:type "Malware" ;
  attack:firstSeen "2016" ;
  attack:targetPlatform [ "Windows" "ICS Protocols" ] ;
  attack:supportedProtocol [ "IEC 60870-5-101" "IEC 60870-5-104" "IEC 61850" "OPC DA" ] ;
  attack:usedByGroup :Sandworm ;
  attack:implementsTechnique :T0816 ;  # Device Restart/Shutdown
  attack:implementsTechnique :T0826 ;  # Loss of Availability
  attack:implementsTechnique :T0835 ;  # Manipulation of Control
  attack:capability "Direct control of electrical substation equipment" ;
  attack:realWorldUse "Ukraine power grid attack (2016)" ;
  attack:sophistication "Very High" .
```

#### BlackEnergy
```turtle
:BlackEnergy a attack:Software ;
  attack:softwareID "S0089" ;
  attack:name "BlackEnergy" ;
  attack:type "Malware Toolkit" ;
  attack:firstSeen "2007" ;
  attack:version "BlackEnergy 3" ;
  attack:usedByGroup :Sandworm ;
  attack:implementsTechnique :T0817 ;  # Drive-by Compromise
  attack:implementsTechnique :T0886 ;  # Remote Services
  attack:capability "Modular malware platform with ICS-specific plugins" ;
  attack:realWorldUse "Ukraine power grid attack (2015)" .
```

#### Stuxnet
```turtle
:Stuxnet a attack:Software ;
  attack:softwareID "S0603" ;
  attack:name "Stuxnet" ;
  attack:type "Worm" ;
  attack:firstSeen "2010" ;
  attack:targetPlatform "Siemens S7-300/400 PLC" ;
  attack:implementsTechnique :T0847 ;  # Removable Media
  attack:implementsTechnique :T0874 ;  # Project File Infection
  attack:implementsTechnique :T0843 ;  # Program Download
  attack:implementsTechnique :T0806 ;  # Brute Force I/O
  attack:implementsTechnique :T0856 ;  # Spoof Reporting Message
  attack:implementsTechnique :T0832 ;  # Manipulation of View
  attack:implementsTechnique :T0879 ;  # Damage to Property
  attack:capability "PLC rootkit with process manipulation" ;
  attack:realWorldUse "Iranian nuclear program sabotage" ;
  attack:sophistication "Extremely High" ;
  attack:attribution "US-Israel (alleged)" .
```

### 3.14 ATT&CK Mitigations

```turtle
attack:Mitigation
  ├── attack:AccessManagement
  │   ├── attack:AccountManagement
  │   ├── attack:MultiFactorAuthentication
  │   └── attack:PasswordPolicy
  ├── attack:ApplicationSecurity
  │   ├── attack:ApplicationWhitelisting
  │   ├── attack:CodeSigning
  │   └── attack:ExecutionPrevention
  ├── attack:NetworkSecurity
  │   ├── attack:NetworkSegmentation
  │   ├── attack:FirewallConfiguration
  │   └── attack:IntrusionPrevention
  ├── attack:SystemHardening
  │   ├── attack:PatchManagement
  │   ├── attack:DisableUnnecessaryServices
  │   └── attack:SecureConfiguration
  ├── attack:Monitoring
  │   ├── attack:NetworkMonitoring
  │   ├── attack:LoggingAndAlerting
  │   └── attack:AnomalyDetection
  └── attack:Physical Security
      ├── attack:PhysicalAccessControl
      └── attack:RemovableMediaControl
```

## 4. STIX 2.1 (Structured Threat Information Expression)

### 4.1 Overview

**Version**: STIX 2.1
**Standard Body**: OASIS Open
**Format**: JSON-based
**Purpose**: Structured threat intelligence sharing

**Core Concepts:**
- Domain Objects (SDOs)
- Relationship Objects (SROs)
- Cyber Observable Objects (SCOs)
- Bundle containers

### 4.2 STIX Domain Objects (SDOs)

```json
{
  "SDO_Types": [
    "attack-pattern",
    "campaign",
    "course-of-action",
    "grouping",
    "identity",
    "indicator",
    "infrastructure",
    "intrusion-set",
    "location",
    "malware",
    "malware-analysis",
    "note",
    "observed-data",
    "opinion",
    "report",
    "threat-actor",
    "tool",
    "vulnerability"
  ]
}
```

#### Attack Pattern (STIX-ATT&CK Integration)
```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "name": "Modify Parameter",
  "description": "Adversary modifies process parameters to cause unsafe operation",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-ics-attack",
      "phase_name": "impair-process-control"
    }
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T0836",
      "url": "https://attack.mitre.org/techniques/T0836"
    }
  ],
  "x_mitre_platforms": ["Control Server", "Field Controller/RTU/PLC/IED"],
  "x_mitre_data_sources": ["Network Protocol Analysis", "Application Log"],
  "x_mitre_detection": "Monitor for unexpected parameter changes"
}
```

#### Threat Actor
```json
{
  "type": "threat-actor",
  "spec_version": "2.1",
  "id": "threat-actor--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "name": "TEMP.Veles",
  "description": "Russia-attributed group targeting ICS safety systems",
  "threat_actor_types": ["nation-state"],
  "aliases": ["XENOTIME"],
  "first_seen": "2017-01-01T00:00:00.000Z",
  "roles": ["agent"],
  "goals": ["Sabotage critical infrastructure"],
  "sophistication": "expert",
  "resource_level": "government",
  "primary_motivation": "organizational-gain",
  "secondary_motivations": ["dominance"]
}
```

#### Malware
```json
{
  "type": "malware",
  "spec_version": "2.1",
  "id": "malware--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "name": "Triton",
  "description": "ICS malware targeting Triconex safety systems",
  "malware_types": ["backdoor", "remote-access-trojan"],
  "is_family": true,
  "aliases": ["Trisis", "HATMAN"],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-ics-attack",
      "phase_name": "inhibit-response-function"
    }
  ],
  "first_seen": "2017-08-01T00:00:00.000Z",
  "operating_system_refs": ["x-ics-os--triconex"],
  "architecture_execution_envs": ["triconex-controller"],
  "capabilities": ["captures-data", "compromises-system-integrity"],
  "implementation_languages": ["python"]
}
```

#### Vulnerability
```json
{
  "type": "vulnerability",
  "spec_version": "2.1",
  "id": "vulnerability--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "name": "CVE-2023-12345",
  "description": "Buffer overflow in Siemens S7-1200 PLC",
  "external_references": [
    {
      "source_name": "cve",
      "external_id": "CVE-2023-12345",
      "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-12345"
    }
  ],
  "x_cvss_v3_base_score": 9.8,
  "x_cvss_v3_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  "x_cwe_id": "CWE-119",
  "x_affected_products": ["Siemens SIMATIC S7-1200"],
  "x_affected_versions": ["<= V4.4.0"],
  "x_exploit_available": true,
  "x_patch_available": true
}
```

#### Infrastructure
```json
{
  "type": "infrastructure",
  "spec_version": "2.1",
  "id": "infrastructure--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "name": "Sandworm C2 Infrastructure",
  "description": "Command and control servers used by Sandworm",
  "infrastructure_types": ["command-and-control"],
  "first_seen": "2015-12-23T00:00:00.000Z",
  "last_seen": "2016-12-17T00:00:00.000Z"
}
```

#### Indicator
```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "name": "Triton Malware Hash",
  "description": "SHA-256 hash of Triton malware sample",
  "indicator_types": ["malicious-activity"],
  "pattern": "[file:hashes.SHA256 = '4118a5d75d4a305d5c<...>']",
  "pattern_type": "stix",
  "valid_from": "2023-01-15T10:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-ics-attack",
      "phase_name": "execution"
    }
  ]
}
```

### 4.3 STIX Relationship Objects (SROs)

```json
{
  "SRO_Types": [
    "relationship",
    "sighting"
  ]
}
```

#### Relationship Examples
```json
// Threat Actor uses Malware
{
  "type": "relationship",
  "spec_version": "2.1",
  "id": "relationship--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "relationship_type": "uses",
  "source_ref": "threat-actor--<TEMP.Veles_uuid>",
  "target_ref": "malware--<Triton_uuid>"
}

// Malware targets Vulnerability
{
  "type": "relationship",
  "spec_version": "2.1",
  "id": "relationship--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "relationship_type": "targets",
  "source_ref": "malware--<Triton_uuid>",
  "target_ref": "vulnerability--<CVE_uuid>"
}

// Attack Pattern mitigated by Course of Action
{
  "type": "relationship",
  "spec_version": "2.1",
  "id": "relationship--<uuid>",
  "created": "2023-01-15T10:00:00.000Z",
  "modified": "2023-01-15T10:00:00.000Z",
  "relationship_type": "mitigates",
  "source_ref": "course-of-action--<mitigation_uuid>",
  "target_ref": "attack-pattern--<T0836_uuid>"
}
```

### 4.4 STIX Cyber Observable Objects (SCOs)

```json
{
  "SCO_Types": [
    "artifact",
    "autonomous-system",
    "directory",
    "domain-name",
    "email-addr",
    "email-message",
    "file",
    "ipv4-addr",
    "ipv6-addr",
    "mac-addr",
    "mutex",
    "network-traffic",
    "process",
    "software",
    "url",
    "user-account",
    "windows-registry-key",
    "x509-certificate"
  ]
}
```

#### File Observable
```json
{
  "type": "file",
  "spec_version": "2.1",
  "id": "file--<uuid>",
  "hashes": {
    "MD5": "d41d8cd98f00b204e9800998ecf8427e",
    "SHA-256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  },
  "size": 1024,
  "name": "trilog.exe",
  "created": "2017-08-01T10:00:00.000Z"
}
```

#### Network Traffic Observable
```json
{
  "type": "network-traffic",
  "spec_version": "2.1",
  "id": "network-traffic--<uuid>",
  "protocols": ["tcp", "modbus"],
  "src_ref": "ipv4-addr--<uuid>",
  "dst_ref": "ipv4-addr--<uuid>",
  "src_port": 54321,
  "dst_port": 502,
  "extensions": {
    "modbus-ext": {
      "function_code": 16,
      "unit_id": 1,
      "address": 1000,
      "quantity": 10
    }
  }
}
```

#### IPv4 Address Observable
```json
{
  "type": "ipv4-addr",
  "spec_version": "2.1",
  "id": "ipv4-addr--<uuid>",
  "value": "192.168.100.10",
  "resolves_to_refs": ["mac-addr--<uuid>"]
}
```

### 4.5 STIX Bundle

```json
{
  "type": "bundle",
  "id": "bundle--<uuid>",
  "objects": [
    {
      "type": "threat-actor",
      "id": "threat-actor--<uuid>",
      "name": "TEMP.Veles",
      "...": "..."
    },
    {
      "type": "malware",
      "id": "malware--<uuid>",
      "name": "Triton",
      "...": "..."
    },
    {
      "type": "relationship",
      "id": "relationship--<uuid>",
      "relationship_type": "uses",
      "source_ref": "threat-actor--<uuid>",
      "target_ref": "malware--<uuid>"
    }
  ]
}
```

### 4.6 ICS-Specific STIX Extensions

#### ICS Asset Extension
```json
{
  "type": "x-ics-asset",
  "spec_version": "2.1",
  "id": "x-ics-asset--<uuid>",
  "name": "PLC-001",
  "asset_type": "PLC",
  "manufacturer": "Siemens",
  "model": "S7-1200",
  "serial_number": "12345",
  "firmware_version": "V4.4.0",
  "ip_address": "192.168.100.10",
  "mac_address": "00:1B:1B:1B:1B:1B",
  "location_ref": "location--<uuid>",
  "zone": "Level 1 - Basic Control",
  "criticality": "high",
  "vulnerabilities_refs": ["vulnerability--<uuid>"]
}
```

#### ICS Network Extension
```json
{
  "type": "x-ics-network",
  "spec_version": "2.1",
  "id": "x-ics-network--<uuid>",
  "name": "Production VLAN",
  "network_type": "OT",
  "vlan_id": 100,
  "ip_range": "192.168.100.0/24",
  "purdue_level": 1,
  "assets_refs": ["x-ics-asset--<uuid>", "..."],
  "firewall_rules": ["..."],
  "monitoring_enabled": true
}
```

## 5. UCO (Unified Cyber Ontology)

### 5.1 Overview

**Source**: Cyber Domain Ontology (CDO) community
**Purpose**: Digital forensics and cyber investigation
**Format**: OWL/RDF ontology
**Version**: UCO 1.2.0

**Core Domains:**
1. Investigation
2. Observable (digital artifacts)
3. Action (operations)
4. Identity
5. Location
6. Time
7. Vocabulary

### 5.2 UCO Core Architecture

```turtle
uco:UcoObject
  ├── uco:InvestigativeAction
  ├── uco:Observable
  ├── uco:Identity
  ├── uco:Location
  ├── uco:Trace
  └── uco:Annotation

uco:Observable
  ├── uco:CyberItem
  │   ├── uco:Device
  │   ├── uco:File
  │   ├── uco:NetworkConnection
  │   ├── uco:Process
  │   └── uco:Account
  ├── uco:PhysicalItem
  └── uco:Event
```

### 5.3 Investigation Concepts

#### Investigation
```turtle
:ICS_Security_Investigation a uco:Investigation ;
  uco:description "Security incident in manufacturing facility" ;
  uco:focus :Ransomware_Incident ;
  uco:investigator :Investigator_Smith ;
  uco:startTime "2023-06-15T09:00:00Z"^^xsd:dateTime ;
  uco:endTime "2023-06-20T17:00:00Z"^^xsd:dateTime ;
  uco:status "Completed" .
```

#### Investigative Action
```turtle
:Forensic_Image_Acquisition a uco:InvestigativeAction ;
  uco:name "Acquire PLC Firmware Image" ;
  uco:description "Forensic acquisition of PLC memory" ;
  uco:performer :Forensic_Analyst_1 ;
  uco:startTime "2023-06-15T10:30:00Z"^^xsd:dateTime ;
  uco:endTime "2023-06-15T11:45:00Z"^^xsd:dateTime ;
  uco:tool :Forensic_Tool_X ;
  uco:object :PLC_Device_001 ;
  uco:result :Firmware_Image_001 .
```

#### Trace (Evidence)
```turtle
:Evidence_001 a uco:Trace ;
  uco:description "Malicious ladder logic program" ;
  uco:provenanceRecord :Chain_of_Custody_001 ;
  uco:observable :Malicious_File_001 ;
  uco:foundOn :PLC_Device_001 ;
  uco:foundBy :Forensic_Analyst_1 ;
  uco:foundTime "2023-06-15T12:00:00Z"^^xsd:dateTime .
```

### 5.4 Observable - Cyber Items

#### Device
```turtle
:PLC_Device_001 a uco:Device ;
  uco:deviceType "PLC" ;
  uco:manufacturer "Siemens" ;
  uco:model "S7-1200" ;
  uco:serialNumber "ABC123456" ;
  uco:firmwareVersion "V4.4.0" ;
  uco:hasNetworkInterface :NetworkInterface_001 ;
  uco:hasVulnerability :CVE_2023_12345 ;
  uco:compromised true ;
  uco:compromiseDate "2023-06-10T14:30:00Z"^^xsd:dateTime .
```

#### File
```turtle
:Malicious_File_001 a uco:File ;
  uco:fileName "malware.exe" ;
  uco:filePath "C:\\ProgramData\\hidden\\" ;
  uco:fileSize "2048"^^xsd:integer ;
  uco:createdTime "2023-06-10T14:30:00Z"^^xsd:dateTime ;
  uco:modifiedTime "2023-06-10T14:30:00Z"^^xsd:dateTime ;
  uco:hash [
    uco:hashMethod "SHA-256" ;
    uco:hashValue "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  ] ;
  uco:fileType "Executable" ;
  uco:malicious true .
```

#### Network Connection
```turtle
:Suspicious_Connection_001 a uco:NetworkConnection ;
  uco:src :PLC_Device_001 ;
  uco:dst :External_IP_001 ;
  uco:srcPort "54321"^^xsd:integer ;
  uco:dstPort "443"^^xsd:integer ;
  uco:protocol "TCP" ;
  uco:startTime "2023-06-10T14:35:00Z"^^xsd:dateTime ;
  uco:endTime "2023-06-10T15:20:00Z"^^xsd:dateTime ;
  uco:dataVolume "1048576"^^xsd:integer ;  # bytes
  uco:connectionType "Outbound" ;
  uco:encrypted true ;
  uco:suspicious true .
```

#### Process
```turtle
:Malicious_Process_001 a uco:Process ;
  uco:pid "1234"^^xsd:integer ;
  uco:processName "malware.exe" ;
  uco:commandLine "malware.exe -h 192.168.1.100" ;
  uco:createdTime "2023-06-10T14:30:15Z"^^xsd:dateTime ;
  uco:creator :Unknown_User ;
  uco:parentProcess :Explorer_Process ;
  uco:networkConnection :Suspicious_Connection_001 ;
  uco:fileAccessed :Sensitive_Config_File ;
  uco:malicious true .
```

#### Account
```turtle
:Compromised_Account_001 a uco:Account ;
  uco:accountType "User Account" ;
  uco:userName "admin" ;
  uco:domain "FACTORY" ;
  uco:createdTime "2020-01-01T00:00:00Z"^^xsd:dateTime ;
  uco:lastLoginTime "2023-06-10T14:28:00Z"^^xsd:dateTime ;
  uco:loginLocation :Engineering_Workstation_001 ;
  uco:privileges "Administrator" ;
  uco:compromised true ;
  uco:compromiseIndicators [
    "Login from unusual location"
    "Login outside business hours"
    "Unusual command execution"
  ] .
```

### 5.5 Observable - Events

#### Security Event
```turtle
:ICS_Intrusion_Event a uco:Event ;
  uco:eventType "Security Incident" ;
  uco:description "Unauthorized access to PLC" ;
  uco:startTime "2023-06-10T14:28:00Z"^^xsd:dateTime ;
  uco:endTime "2023-06-10T15:20:00Z"^^xsd:dateTime ;
  uco:location :Manufacturing_Facility ;
  uco:affectedAsset :PLC_Device_001 ;
  uco:indicator :Suspicious_Connection_001 ;
  uco:indicator :Malicious_Process_001 ;
  uco:severity "Critical" ;
  uco:impact "Process disruption" .
```

### 5.6 Actions

#### Malicious Action
```turtle
:PLC_Compromise_Action a uco:Action ;
  uco:actionType "Malicious Activity" ;
  uco:description "Attacker modified PLC logic" ;
  uco:startTime "2023-06-10T14:30:00Z"^^xsd:dateTime ;
  uco:endTime "2023-06-10T14:45:00Z"^^xsd:dateTime ;
  uco:performer :Threat_Actor_Unknown ;
  uco:instrument :Malicious_File_001 ;
  uco:object :PLC_Device_001 ;
  uco:result :Modified_Ladder_Logic ;
  uco:method "Remote Code Execution" .
```

#### Response Action
```turtle
:Incident_Response_Action a uco:Action ;
  uco:actionType "Incident Response" ;
  uco:description "Isolated affected PLC from network" ;
  uco:startTime "2023-06-15T13:00:00Z"^^xsd:dateTime ;
  uco:performer :IR_Team ;
  uco:object :PLC_Device_001 ;
  uco:method "Network Isolation" ;
  uco:justification "Contain malware spread" .
```

### 5.7 Identity

#### Person (Investigator)
```turtle
:Forensic_Analyst_1 a uco:Identity, uco:Person ;
  uco:name "Jane Smith" ;
  uco:role "Digital Forensic Analyst" ;
  uco:organization :Forensics_Firm_X ;
  uco:certification "GIAC Certified Forensic Analyst (GCFA)" .
```

#### Organization
```turtle
:Manufacturing_Company a uco:Identity, uco:Organization ;
  uco:name "ACME Manufacturing Inc." ;
  uco:sector "Manufacturing" ;
  uco:location :Facility_Address .
```

#### Threat Actor Identity
```turtle
:Threat_Actor_Unknown a uco:Identity ;
  uco:name "Unknown Adversary" ;
  uco:identityType "Threat Actor" ;
  uco:attribution "Under Investigation" ;
  uco:suspectedMotivation "Sabotage" ;
  uco:sophistication "High" .
```

### 5.8 Provenance and Chain of Custody

#### Provenance Record
```turtle
:Chain_of_Custody_001 a uco:ProvenanceRecord ;
  uco:description "Chain of custody for evidence 001" ;
  uco:exhibit :Evidence_001 ;
  uco:custodian :Forensic_Analyst_1 ;
  uco:acquisitionMethod "Forensic Imaging" ;
  uco:hashVerification [
    uco:hashMethod "SHA-256" ;
    uco:hashValue "original_hash_value" ;
    uco:verifiedAt "2023-06-15T11:50:00Z"^^xsd:dateTime
  ] ;
  uco:storageLocation "Evidence Locker 5A" ;
  uco:integrityVerified true .
```

#### Custody Transfer
```turtle
:Custody_Transfer_001 a uco:Action ;
  uco:actionType "Custody Transfer" ;
  uco:description "Evidence transferred to analysis lab" ;
  uco:startTime "2023-06-15T16:00:00Z"^^xsd:dateTime ;
  uco:transferFrom :Forensic_Analyst_1 ;
  uco:transferTo :Lab_Technician_2 ;
  uco:object :Evidence_001 ;
  uco:documentation "Transfer Form 001" ;
  uco:witness :Security_Officer_1 .
```

### 5.9 UCO Integration with ICS Incidents

#### Complete ICS Incident Investigation
```turtle
# Investigation
:ICS_Malware_Investigation a uco:Investigation ;
  uco:name "Manufacturing Facility Malware Investigation" ;
  uco:caseID "2023-ICS-001" ;
  uco:focus :ICS_Malware_Incident ;
  uco:investigationStatus "Active" ;
  uco:investigator :Lead_Investigator ;
  uco:startDate "2023-06-15"^^xsd:date .

# Incident
:ICS_Malware_Incident a uco:Event ;
  uco:eventType "Cyber Attack" ;
  uco:description "Malware infection affecting PLCs" ;
  uco:occurredAt :Manufacturing_Facility ;
  uco:discoveredTime "2023-06-15T08:00:00Z"^^xsd:dateTime ;
  uco:estimatedStartTime "2023-06-10T14:00:00Z"^^xsd:dateTime ;
  uco:affectedAsset :PLC_001 ;
  uco:affectedAsset :PLC_002 ;
  uco:affectedAsset :HMI_001 ;
  uco:impactAssessment "Production downtime, potential safety risk" .

# Forensic Evidence
:PLC_Firmware_Evidence a uco:Trace ;
  uco:description "Malicious PLC firmware" ;
  uco:observable :PLC_Firmware_Image ;
  uco:foundOn :PLC_001 ;
  uco:discoveryMethod :Forensic_Imaging_Action ;
  uco:provenanceRecord :Chain_of_Custody_PLC001 .

:PLC_Firmware_Image a uco:File ;
  uco:fileName "plc_firmware.bin" ;
  uco:fileSize "524288"^^xsd:integer ;
  uco:hash [
    uco:hashMethod "SHA-256" ;
    uco:hashValue "abc123..." ;
    uco:hashMethod "MD5" ;
    uco:hashValue "def456..."
  ] ;
  uco:containsMalware true ;
  uco:malwareSignature :Triton_Signature .

# Attack Timeline
:Initial_Access_Action a uco:Action ;
  uco:actionType "Initial Access" ;
  uco:description "Attacker gained access via phishing" ;
  uco:startTime "2023-06-10T09:00:00Z"^^xsd:dateTime ;
  uco:method "Spear Phishing" ;
  uco:target :Engineering_Workstation_001 ;
  uco:instrument :Phishing_Email ;
  uco:result "Compromised workstation" .

:Lateral_Movement_Action a uco:Action ;
  uco:actionType "Lateral Movement" ;
  uco:description "Movement to OT network" ;
  uco:startTime "2023-06-10T13:00:00Z"^^xsd:dateTime ;
  uco:source :Engineering_Workstation_001 ;
  uco:target :OT_Network_Segment ;
  uco:method "Credential theft and VPN access" .

:PLC_Compromise_Action a uco:Action ;
  uco:actionType "ICS Compromise" ;
  uco:description "Malware deployed to PLCs" ;
  uco:startTime "2023-06-10T14:30:00Z"^^xsd:dateTime ;
  uco:performer :Threat_Actor_Unknown ;
  uco:instrument :Malware_Payload ;
  uco:target :PLC_001 ;
  uco:target :PLC_002 ;
  uco:method "Program download via engineering software" ;
  uco:result "Modified PLC logic" .

# Indicators of Compromise
:IOC_1 a uco:Observable ;
  uco:observableType "Network Traffic" ;
  uco:description "Unusual outbound connection from PLC" ;
  uco:srcIP "192.168.100.10" ;  # PLC IP
  uco:dstIP "203.0.113.50" ;     # External C2
  uco:dstPort "443"^^xsd:integer ;
  uco:protocol "HTTPS" ;
  uco:firstSeen "2023-06-10T14:35:00Z"^^xsd:dateTime .

:IOC_2 a uco:Observable ;
  uco:observableType "File Hash" ;
  uco:hash [
    uco:hashMethod "SHA-256" ;
    uco:hashValue "e3b0c44..."
  ] ;
  uco:associated :Malware_Payload .
```

## 6. Cross-Ontology Integration Patterns

### 6.1 ICS-SEC-KG + MITRE ATT&CK

```turtle
# Mapping ICS-SEC-KG attacks to ATT&CK techniques

:Modbus_MITM_Attack a ics:Attack ;
  ics:attackType ics:ManInTheMiddle ;
  ics:targetsProtocol ics:Modbus ;
  owl:sameAs attack:T0830 ;  # Man in the Middle (ATT&CK)
  attack:tactic attack:Collection ;
  attack:tactic attack:ImpairProcessControl .

# Vulnerability to ATT&CK technique
:PLC_Auth_Bypass a ics:Vulnerability ;
  ics:hasCVEID "CVE-2023-12345" ;
  ics:affectsComponent ics:PLC ;
  ics:enablesAttackTechnique attack:T0886 .  # Remote Services
```

### 6.2 MITRE-CTI + STIX 2.1

```turtle
# CVE represented in both formats

# MITRE-CTI RDF
:CVE_2023_12345 a mitre:CVE ;
  mitre:cveID "CVE-2023-12345" ;
  mitre:hasCWE :CWE_119 ;
  mitre:cvssScore "9.8"^^xsd:float .

# STIX 2.1 JSON (converted to RDF)
:CVE_2023_12345_STIX a stix:Vulnerability ;
  stix:id "vulnerability--uuid" ;
  stix:name "CVE-2023-12345" ;
  stix:external_reference [
    stix:source_name "cve" ;
    stix:external_id "CVE-2023-12345"
  ] ;
  owl:sameAs :CVE_2023_12345 .
```

### 6.3 ATT&CK + STIX + UCO

```turtle
# Complete incident representation

# ATT&CK Technique
:T0836_Modify_Parameter a attack:Technique ;
  attack:techniqueID "T0836" ;
  attack:name "Modify Parameter" .

# STIX Attack Pattern
:T0836_STIX a stix:AttackPattern ;
  stix:name "Modify Parameter" ;
  stix:external_reference [
    stix:source_name "mitre-attack" ;
    stix:external_id "T0836"
  ] ;
  owl:sameAs :T0836_Modify_Parameter .

# UCO Action (actual incident)
:Parameter_Modification_Incident a uco:Action ;
  uco:actionType "Malicious Activity" ;
  uco:description "Attacker modified temperature setpoint" ;
  uco:method :T0836_STIX ;  # Links to STIX/ATT&CK
  uco:target :PLC_Device_001 ;
  uco:startTime "2023-06-10T14:40:00Z"^^xsd:dateTime ;
  uco:result "Process operating at unsafe temperature" .
```

### 6.4 SAREF + ICS-SEC-KG + UCO

```turtle
# Device from SAREF with security context

:Industrial_Boiler a saref:Device, s4bldg:Boiler, ics:ICSComponent ;
  # SAREF properties
  saref:hasManufacturer "Siemens" ;
  saref:hasModel "Boiler-2000" ;
  saref:hasFunction :TemperatureControl ;
  saref:measuresProperty :Temperature ;
  # ICS-SEC-KG properties
  ics:hasVulnerability :CVE_2023_XXXXX ;
  ics:communicatesUsing ics:Modbus ;
  ics:partOfSystem :HVAC_System ;
  # UCO forensic context
  uco:compromised true ;
  uco:compromiseDate "2023-06-10T14:30:00Z"^^xsd:dateTime ;
  uco:evidence :Forensic_Evidence_Boiler .

:Forensic_Evidence_Boiler a uco:Trace ;
  uco:description "Malicious temperature control logic" ;
  uco:foundOn :Industrial_Boiler ;
  uco:relatedIncident :ICS_Malware_Incident .
```

## 7. Summary and Integration Recommendations

### 7.1 Ontology Strengths Summary

**ICS-SEC-KG:**
- Strengths: ICS-specific components, protocols, vulnerabilities
- Use Case: OT/ICS asset inventory, vulnerability management
- Integration Priority: HIGH

**MITRE-CTI (CVE/CWE/CAPEC):**
- Strengths: Comprehensive vulnerability taxonomy, attack pattern library
- Use Case: Vulnerability tracking, attack pattern recognition
- Integration Priority: HIGH

**ATT&CK for ICS:**
- Strengths: Adversary tactics/techniques, threat actor profiles
- Use Case: Threat intelligence, attack detection
- Integration Priority: CRITICAL

**STIX 2.1:**
- Strengths: Standardized threat intelligence exchange
- Use Case: Threat sharing, indicator management
- Integration Priority: CRITICAL

**UCO:**
- Strengths: Digital forensics, investigation workflow
- Use Case: Incident investigation, evidence management
- Integration Priority: MEDIUM-HIGH

### 7.2 Recommended Integration Architecture

**Layer 1: Device and Asset Foundation**
- SAREF (device modeling)
- ICS-SEC-KG (ICS components)
- Schema.org (IT infrastructure)

**Layer 2: Vulnerability and Threat Intelligence**
- MITRE-CTI (CVE/CWE/CAPEC)
- STIX 2.1 (threat intelligence exchange)
- ATT&CK for ICS (tactics/techniques)

**Layer 3: Investigation and Forensics**
- UCO (digital forensics)
- STIX 2.1 (incident documentation)

**Layer 4: Domain-Specific Extensions**
- Custom AEON-DT classes
- Psychometric profiling (Lacanian)
- Operational technology specifics

### 7.3 Key Integration Points

1. **Device-to-Vulnerability**: SAREF devices ↔ MITRE CVEs ↔ ICS-SEC-KG vulnerabilities
2. **Vulnerability-to-Attack**: CVE ↔ CWE ↔ CAPEC ↔ ATT&CK techniques
3. **Attack-to-Evidence**: ATT&CK techniques ↔ STIX observables ↔ UCO traces
4. **Threat-Actor-to-TTP**: STIX threat actors ↔ ATT&CK groups ↔ techniques
5. **Incident-to-Investigation**: STIX incidents ↔ UCO investigations ↔ evidence

## Version History

- v1.0.0 (2025-10-30): Initial comprehensive cybersecurity research findings

## References

1. ICS-SEC-KG Research Papers and GitHub Repository
2. MITRE CVE Database: https://cve.mitre.org/
3. MITRE CWE: https://cwe.mitre.org/
4. MITRE CAPEC: https://capec.mitre.org/
5. MITRE ATT&CK for ICS: https://attack.mitre.org/matrices/ics/
6. STIX 2.1 Specification: https://oasis-open.github.io/cti-documentation/
7. UCO Ontology: https://unifiedcyberontology.org/
8. MITRE CTI GitHub: https://github.com/mitre/cti

---

*Document Complete - 4 Major Cybersecurity Ontologies Analyzed*
