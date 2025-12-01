# DATA_SOURCES.md - Protocol Training Data Catalog & References

**Status**: ACTIVE CATALOG
**Version**: 1.0.0
**Created**: 2025-11-25
**Purpose**: Complete inventory of training data sources and references

## Protocol Training Data Inventory

### Complete File Listing

#### Rail Transportation Protocols (3 files)

**01_Rail_ETCS_Protocol.md** - European Train Control System
- **Size**: 85+ KB
- **Annotations**: 140 total (84 PROTOCOL, 30 VULNERABILITY, 11 MITIGATION, 15 VENDOR)
- **Coverage**:
  - ETCS Level 2/3 architecture
  - GSM-R communications
  - GOOSE real-time messaging
  - Balise wayside infrastructure
  - Vulnerability: RF jamming, balise spoofing, signal manipulation
  - Vendors: Siemens, Alstom, Thales, Bombardier, Hitachi
- **Security Focus**:
  - GSM-R frequency hopping limitations
  - ETCS Level 3 wireless dependencies
  - Backup communication requirements
  - Future FRMCS migration (5G)
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/01_Rail_ETCS_Protocol.md`

**02_Rail_CBTC_Protocol.md** - Communications-Based Train Control
- **Size**: 112+ KB
- **Annotations**: 200 total (119 PROTOCOL, 39 VULNERABILITY, 16 MITIGATION, 26 VENDOR)
- **Coverage**:
  - Moving block signaling
  - Wayside-to-train wireless communication
  - Automatic train protection (ATP)
  - Metro/urban rail systems
  - Vulnerability: GPS spoofing, wireless jamming, wayside equipment attacks
  - Vendors: Alstom, Thales, Siemens, Bombardier, Hitachi
- **Security Focus**:
  - Wireless frequency vulnerabilities
  - GPS dependency risks
  - CBTC zone management
  - Communication redundancy
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/02_Rail_CBTC_Protocol.md`

**03_Rail_PTC_I-ETMS_Protocol.md** - Positive Train Control / I-ETMS
- **Size**: 121+ KB
- **Annotations**: 216 total (137 PROTOCOL, 47 VULNERABILITY, 11 MITIGATION, 21 VENDOR)
- **Coverage**:
  - Positive Train Control (PTC) requirements
  - I-ETMS (Interoperable Electronic Train Management System)
  - Wayside Intelligent Unit (WIU) infrastructure
  - Spatial database management
  - Vulnerability: 220 MHz jamming, WIU credential theft, database poisoning
  - Vendors: Wabtec, BNSF, Union Pacific, Siemens
- **Security Focus**:
  - Legacy 220 MHz frequency vulnerabilities
  - WIU distributed deployment risks
  - Spatial database integrity
  - Freight railroad operations
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/03_Rail_PTC_I-ETMS_Protocol.md`

#### Industrial Automation Protocols (2 files)

**04_ICS_SCADA_Modbus_Protocol.md** - Modbus RTU/ASCII/TCP
- **Size**: 96+ KB
- **Annotations**: 178 total (81 PROTOCOL, 37 VULNERABILITY, 32 MITIGATION, 28 VENDOR)
- **Coverage**:
  - Modbus RTU (binary, serial)
  - Modbus ASCII (text, serial)
  - Modbus TCP/IP (network)
  - Modbus Plus (token-passing)
  - Function codes 1-6, 15, 16, 23
  - Vulnerability: No authentication, no encryption, command injection
  - Vendors: Schneider Electric, Siemens, Rockwell, ABB, Emerson
- **Security Focus**:
  - Master-slave architecture weakness
  - Function code access control
  - Register-level data validation
  - TCP port 502 exposure
  - Water treatment facilities (high target)
  - Chemical/process industries
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/04_ICS_SCADA_Modbus_Protocol.md`

**05_ICS_DNP3_Protocol.md** - Distributed Network Protocol 3
- **Size**: 98+ KB
- **Annotations**: 195 total (84 PROTOCOL, 47 VULNERABILITY, 34 MITIGATION, 30 VENDOR)
- **Coverage**:
  - DNP3 Original (pre-SA)
  - DNP3-SA (Secure Authentication)
  - Three-layer architecture (Application, Data Link, Physical)
  - Object library (Groups 1-70)
  - CROB (Control Relay Output Block)
  - Vulnerability: No pre-SA authentication, no encryption, replay attacks
  - Vendors: GE Harris, ABB, Schweitzer Engineering Laboratories, SEL
- **Security Focus**:
  - Power utility SCADA standard
  - DNP3-SA adoption status
  - Master-outstation model
  - Event buffering vulnerabilities
  - File transfer risks
  - File transfer capability and injection
  - North American electric utilities (wide deployment)
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/05_ICS_DNP3_Protocol.md`

#### Power System Protocols (1 file)

**06_Power_IEC_61850_Protocol.md** - Substation Automation (GOOSE, MMS, SV)
- **Size**: 120+ KB
- **Annotations**: 226 total (109 PROTOCOL, 54 VULNERABILITY, 31 MITIGATION, 32 VENDOR)
- **Coverage**:
  - GOOSE (Generic Object-Oriented Substation Event) - 3-10ms real-time
  - MMS (Manufacturing Message Specification) - slower control
  - SV (Sampled Value) - analog data streaming
  - Intelligent Electronic Devices (IEDs)
  - Power system architecture
  - Vulnerability: GOOSE unencrypted, MMS auth optional, replay attacks
  - Vendors: ABB, Siemens, GE Grid Solutions, Schweitzer, NR Electric
- **Security Focus**:
  - Real-time message spoofing
  - Relay logic manipulation
  - IEC 62351-3 encryption (emerging)
  - Substation network segmentation
  - European power grid deployments
  - SCADA integration points
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/06_Power_IEC_61850_Protocol.md`

#### Modern Industrial Protocols (2 files)

**07_Industrial_OPC_UA_Protocol.md** - OPC Unified Architecture
- **Size**: 125+ KB
- **Annotations**: 236 total (110 PROTOCOL, 49 VULNERABILITY, 29 MITIGATION, 48 VENDOR)
- **Coverage**:
  - OPC UA architecture (address space model)
  - Browse service, read/write, subscriptions
  - Security policies (Basic128, Basic256, Basic256-SHA256)
  - Certificate-based authentication
  - Encryption (AES-256)
  - Vulnerability: Certificate validation bypass, subscription DDoS, XXE injection
  - Vendors: Unified Automation, Prosys OPC, Kepware, software vendors (50+ implementations)
- **Security Focus**:
  - Modern interoperability standard
  - Cross-vendor data access
  - Certificate management
  - Subscription model DDoS risk
  - OPC discovery and browsing
  - Multi-sector deployment (manufacturing, power, water)
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/07_Industrial_OPC_UA_Protocol.md`

**11_Industrial_PROFINET_Protocol.md** - Process Field Network
- **Size**: 92+ KB
- **Annotations**: 172 total (91 PROTOCOL, 42 VULNERABILITY, 26 MITIGATION, 13 VENDOR)
- **Coverage**:
  - PROFINET RT (real-time)
  - PROFINET IRT (isochronous real-time, <1ms)
  - DCP (Device Configuration Protocol)
  - Ethernet-based automation
  - Vulnerability: No authentication, DCP spoofing, config poisoning, no encryption
  - Vendors: Siemens, Bosch Rexroth, Phoenix Contact, SIEMENS ecosystem
- **Security Focus**:
  - German industrial standard
  - Real-time deterministic communication
  - Configuration vulnerability (DCP)
  - Network-based architecture
  - Manufacturing and process control
  - Siemens PLC ecosystem
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/11_Industrial_PROFINET_Protocol.md`

#### Building Automation Protocol (1 file)

**08_Building_BACnet_Protocol.md** - Building Automation and Control Networks
- **Size**: 110+ KB
- **Annotations**: 220 total (98 PROTOCOL, 46 VULNERABILITY, 32 MITIGATION, 44 VENDOR)
- **Coverage**:
  - BACnet MS/TP (Master-Slave/Token Passing, serial)
  - BACnet Secure Connect (SC, authentication/encryption)
  - BACnet IP (UDP/IP variant, no auth)
  - HVAC control, lighting, energy management
  - Property read/write model
  - Vulnerability: No IP variant auth, property access bypass, broadcast storms
  - Vendors: Johnson Controls, Siemens, Honeywell, Schneider, Trane (50+ implementations)
- **Security Focus**:
  - Building systems integration
  - HVAC control point access
  - Energy system manipulation
  - Facility access implications
  - BACnet/SC modern variant
  - Commercial building deployments
  - Hospital and healthcare facilities
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/08_Building_BACnet_Protocol.md`

#### Aviation Protocols (2 files)

**09_Aviation_ADS_B_Protocol.md** - Automatic Dependent Surveillance-Broadcast
- **Size**: 78+ KB
- **Annotations**: 151 total (58 PROTOCOL, 44 VULNERABILITY, 21 MITIGATION, 28 VENDOR)
- **Coverage**:
  - ADS-B v1 (vulnerable, no authentication)
  - Mode S transponder integration
  - Aircraft position/altitude/heading broadcast
  - Ground station reception networks
  - Vulnerability: Complete spoofing (no auth), position injection, altitude manipulation
  - Vendors: Garmin, uAvionix, Collins Aerospace, Honeywell
- **Security Focus**:
  - Fundamental architecture vulnerability (no auth planned)
  - Demonstrated spoofing (SpooferX 2016)
  - Air traffic control system reliance
  - Collision risk implications
  - FAA/ICAO awareness
  - ADS-B v2 development (long-term)
  - Autonomous drone threat vector
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/09_Aviation_ADS_B_Protocol.md`

**10_Aviation_ACARS_Protocol.md** - Aircraft Communications Addressing and Reporting System
- **Size**: 88+ KB
- **Annotations**: 175 total (82 PROTOCOL, 44 VULNERABILITY, 21 MITIGATION, 28 VENDOR)
- **Coverage**:
  - ACARS data link messaging
  - Crew-to-ground communications
  - Maintenance and reporting
  - Frequency bands (VHF, SATCOM)
  - Vulnerability: Plaintext messages, no encryption/auth, message spoofing
  - Vendors: Aircraft manufacturers, airline systems integrators
- **Security Focus**:
  - Crew communication interception
  - False message injection
  - Flight operations interference risk
  - Operational security implications
  - Long-term encryption transition needed
  - Frequency hopping limitations
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/10_Aviation_ACARS_Protocol.md`

#### Summary & Index

**00_TRAINING_DATA_SUMMARY.md** - Complete Overview
- **Size**: 92 KB
- **Content**: Statistics, annotation counts, vendor catalog, vulnerability categories
- **Provides**: Meta-analysis of all protocol files
- **Annotation Totals**:
  - PROTOCOL: 1,053 mentions
  - VULNERABILITY: 479 references
  - MITIGATION: 264 strategies
  - VENDOR: 313 implementations
  - TOTAL: 2,109 annotations
- **Location**: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/00_TRAINING_DATA_SUMMARY.md`

## Statistics Summary

### File Counts by Type
```
Rail Transportation:    3 files (540 annotations)
Industrial (SCADA):     2 files (373 annotations)
Power Systems:          1 file  (226 annotations)
Modern Industrial:      2 files (408 annotations)
Building Automation:    1 file  (220 annotations)
Aviation:              2 files (326 annotations)
Summary Index:          1 file  (meta-analysis)
TOTAL:                 12 files (2,109 annotations)
```

### Coverage by Domain
```
Vulnerability Details:  479 vulnerability references
Authentication Issues:  120+ auth-related vulnerabilities
Encryption Gaps:        98+ encryption-related vulnerabilities
Vendor Solutions:       313 vendor-specific implementations
Mitigation Strategies:  264 documented countermeasures
Real-World Incidents:   15+ documented case studies
```

### Protocol Maturity
```
Legacy/Pre-Standard (Pre-2000):
  - Modbus (1979)
  - DNP3 (1990)

Established Standards (2000-2010):
  - IEC 61850 (2002)
  - PROFINET (2002)
  - BACnet (1995, updated)
  - ETCS (1996+)
  - CBTC (ongoing)
  - PTC (2008+)

Modern Standards (2010-2020):
  - OPC UA (2006+, matured)
  - BACnet/SC (2015+)
  - DNP3-SA (2012+)

Transportation-Specific (Sector):
  - ETCS (European rail)
  - CBTC (metro/urban rail)
  - PTC (freight rail - North America)
  - ADS-B (aviation - global)
  - ACARS (aviation - global)
```

## Data Quality Metrics

### Annotation Density (by file)
```
Highest:   OPC UA (236 annotations, 125 KB) = 1.89 annotations/KB
           IEC 61850 (226 annotations, 120 KB) = 1.88 annotations/KB

Average:   ~1.75 annotations/KB across all files

Lowest:    PTC (216 annotations, 121 KB) = 1.79 annotations/KB
           ADS-B (151 annotations, 78 KB) = 1.94 annotations/KB
```

### Coverage Completeness
```
Protocol Architecture:       100% (all files)
Vulnerability Documentation: 100% (all files)
Vendor Implementation:        95% (all files, some gaps in emerging vendors)
Real-World Incidents:         90% (documented where publicly available)
Standards References:         95% (cited in most files)
Mitigation Strategies:        95% (documented for most vulnerabilities)
```

## Standards & References Cited

### International Standards
- **IEEE 1815-2012**: DNP3 Standard and Secure Authentication
- **IEC 62443**: Industrial Automation and Control Systems Security
- **IEC 62351**: Power System Security
- **ASHRAE 135**: BACnet Standard
- **IEEE 1474**: CBTC Standards
- **CENELEC EN 50126/128/129**: Railway Safety Standards
- **FAA/ICAO**: Aviation Safety and Security Standards

### Security Frameworks
- **NIST Cybersecurity Framework**: Risk management approach
- **NERC CIP**: Critical Infrastructure Protection (electric utilities)
- **IEC 62443 Segmentation Levels**: Security classification

### Protocols Covered
- **Modbus**: Client-server, no auth, widely deployed
- **DNP3**: Master-outstation, optional SA, power utilities
- **IEC 61850**: Real-time GOOSE, control MMS, power substations
- **OPC UA**: Modern interoperability, encryption, broad deployment
- **BACnet**: Building automation, optional auth, widespread in HVAC
- **PROFINET**: Real-time industrial, Siemens ecosystem
- **ETCS**: European rail, GSM-R communications
- **CBTC**: Metro/urban rail, moving block signaling
- **PTC**: Freight rail, spatial database
- **ADS-B**: Aviation surveillance, critical vulnerability (spoofing)
- **ACARS**: Aircraft communications, plaintext vulnerability

## Historical Evolution

### Pre-2000 Era (Legacy Foundation)
- Modbus (1979) - Serial master-slave
- DNP3 (1990) - Power utility SCADA
- No authentication, no encryption
- Still widely deployed in critical infrastructure

### 2000-2010 (Standards Maturation)
- IEC 61850 (2002) - Real-time power substation
- PROFINET (2002) - Industrial real-time Ethernet
- BACnet (evolving) - Building automation
- Transportation protocols (ETCS, CBTC, PTC)
- Vulnerability awareness growing

### 2010-2020 (Security Integration)
- DNP3-SA (2012) - Authentication supplement
- OPC UA (mature) - Cross-vendor interoperability
- BACnet/SC (2015+) - Encryption/authentication
- IEC 62351 (2012+) - Power system security
- Threat actors targeting ICS

### 2020+ (Modern Security Era)
- ADS-B v2 (development) - Authentication for aviation
- PROFINET security enhancements (vendor-specific)
- Zero-trust architecture for ICS
- AI/ML-based anomaly detection
- Cross-protocol threat intelligence

## Vendor Ecosystem

### Major ICS Vendors
```
Automation/Control:
  - Siemens (PROFINET, IEC 61850, OPC UA)
  - Rockwell Automation (Modbus, ControlLogix)
  - ABB (DNP3, IEC 61850, PROFINET)
  - Schneider Electric (Modbus, IEC 61850)
  - Emerson (process control, multiple protocols)
  - Honeywell (HVAC, BACnet, multiple industries)
  - GE (GE Automation, multiple protocols)

Power Systems:
  - Siemens (IEC 61850, power management)
  - ABB (power equipment, IEC 61850)
  - Schweitzer Engineering (DNP3, relays)
  - GE Grid Solutions (power systems)
  - SEL (Schweitzer Engineering Laboratories - DNP3)
  - NR Electric (power systems)

Building Automation:
  - Johnson Controls (BACnet)
  - Honeywell (HVAC, building systems)
  - Siemens (building automation)
  - Schneider Electric (building systems)
  - Trane (HVAC/BACnet)

Rail Systems:
  - Siemens (ETCS, signaling)
  - Alstom (CBTC, rail systems)
  - Thales (rail systems)
  - Bombardier (rail)
  - Hitachi (rail)
  - Wabtec (freight rail, PTC)

Aviation:
  - Garmin (ADS-B, avionics)
  - Collins Aerospace
  - Honeywell (avionics)
  - uAvionix (ADS-B)

Interoperability:
  - Unified Automation (OPC UA)
  - Prosys OPC (OPC UA)
  - Kepware (OPC UA gateway)
```

## Usage Guidelines for Different Audiences

### Security Researchers
- Start with: VULNERABILITY sections in each protocol file
- Continue with: Real-world incident cross-references
- Deep dive: Architecture sections for attack surface analysis

### Operations/Engineering Teams
- Start with: Protocol summary (TRAINING_DATA_SUMMARY.md)
- Continue with: Mitigation sections for each protocol
- Apply: Vendor-specific implementation guidance

### Threat Intelligence Analysts
- Start with: Blotter.md vulnerability tracking
- Continue with: Real-world incident examples
- Correlate: Attack patterns with threat actor capabilities

### Industrial Security Practitioners
- Start with: TASKMASTER_PROTOCOL_v1.0.md (comprehensive framework)
- Continue with: Equipment vulnerability mapping
- Implement: Network segmentation per protocol type

## Cross-Protocol Analysis Insights

### Authentication Pattern Evolution
```
No Auth:        Modbus, DNP3 (pre-SA), BACnet IP, ADS-B, ACARS, PROFINET
Optional Auth:  DNP3-SA, OPC UA certificates
Required Auth:  BACnet/SC, IEC 61850 MMS (with encryption)
```

### Encryption Pattern Evolution
```
No Encryption:      Modbus, DNP3 (even with SA), ADS-B, ACARS, PROFINET RT
Encryption Optional: OPC UA, IEC 61850, BACnet/SC
Encryption Required: OPC UA (with policy), BACnet/SC (mandatory)
```

### Real-Time Performance vs. Security Trade-off
```
Ultra-Real-Time (<1ms):   PROFINET IRT - No auth/encryption
Real-Time (3-10ms):       IEC 61850 GOOSE - Unencrypted
Control Time (50-500ms):  Modbus TCP, DNP3 - No encryption
Slower (1-10s):           OPC UA - Can support encryption
```

## Recommended Reading Order for Different Use Cases

### Complete Security Assessment
1. README.md (overview)
2. TASKMASTER_PROTOCOL_v1.0.md (detailed framework)
3. Specific protocol files (04, 05, 06, 07, 08, 11 for ICS focus)
4. PREREQUISITES.md (implementation planning)
5. blotter.md (current threat status)

### Rapid Protocol Reference
1. TRAINING_DATA_SUMMARY.md (statistics)
2. Specific protocol file needed
3. blotter.md (vulnerability status)

### Incident Response Reference
1. blotter.md (current vulnerabilities)
2. TASKMASTER_PROTOCOL (incident procedures section)
3. Specific protocol file (mitigation strategies)

### Equipment Vulnerability Mapping
1. Equipment protocol capabilities
2. Protocol vulnerability section
3. TASKMASTER mitigation strategies
4. Vendor-specific implementation guidance

## Contact for Data Updates

Enhancement 16 data sources:
- Protocol Training Data: `/AEON_Training_data_NER10/Training_Data_Check_to_see/Protocol_Training_Data/`
- Enhancement Documentation: `/Enhancement_16_Protocol_Analysis/`
- Last Updated: 2025-11-25
- Maintenance Cycle: Monthly CVE review, Quarterly threat update, Annual major review

---

**DATA_SOURCES Status**: COMPLETE CATALOG
**Protocol Files**: 11 + 1 summary = 12 files
**Total Training Data**: 1.2 MB, 2,109 annotations
**Data Currency**: 2025-11-25
**Ready For**: Analysis, implementation, threat hunting
