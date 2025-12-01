# Protocol Training Data Summary

## Overview

This directory contains comprehensive training data for industrial, transportation, aviation, and network protocols extracted from protocol-research.md and expanded with extensive vulnerability, mitigation, and vendor information.

## Files Created

### Rail Transportation Protocols
1. **01_Rail_ETCS_Protocol.md** - European Train Control System
2. **02_Rail_CBTC_Protocol.md** - Communications-Based Train Control
3. **03_Rail_PTC_I-ETMS_Protocol.md** - Positive Train Control / I-ETMS

### ICS/SCADA Industrial Protocols
4. **04_ICS_SCADA_Modbus_Protocol.md** - Modbus RTU/ASCII/TCP
5. **05_ICS_DNP3_Protocol.md** - Distributed Network Protocol 3

### Power Utility Protocols
6. **06_Power_IEC_61850_Protocol.md** - Substation Automation (GOOSE, MMS, SV)

### Industrial Automation Protocols
7. **07_Industrial_OPC_UA_Protocol.md** - OPC Unified Architecture
8. **11_Industrial_PROFINET_Protocol.md** - Process Field Network

### Building Automation Protocols
9. **08_Building_BACnet_Protocol.md** - Building Automation and Control Networks

### Aviation Protocols
10. **09_Aviation_ADS-B_Protocol.md** - Automatic Dependent Surveillance-Broadcast
11. **10_Aviation_ACARS_Protocol.md** - Aircraft Communications Addressing and Reporting System

## Annotation Statistics (As of Current Count)

### Total Annotations: 2,109+

| Protocol File | PROTOCOL | VULNERABILITY | MITIGATION | VENDOR | TOTAL |
|--------------|----------|---------------|------------|--------|-------|
| ETCS | 84 | 30 | 11 | 15 | 140 |
| CBTC | 119 | 39 | 16 | 26 | 200 |
| PTC/I-ETMS | 137 | 47 | 11 | 21 | 216 |
| Modbus | 81 | 37 | 32 | 28 | 178 |
| DNP3 | 84 | 47 | 34 | 30 | 195 |
| IEC 61850 | 109 | 54 | 31 | 32 | 226 |
| OPC UA | 110 | 49 | 29 | 48 | 236 |
| BACnet | 98 | 46 | 32 | 44 | 220 |
| ADS-B | 58 | 44 | 21 | 28 | 151 |
| ACARS | 82 | 44 | 21 | 28 | 175 |
| PROFINET | 91 | 42 | 26 | 13 | 172 |

### Annotation Totals by Type

- **PROTOCOL mentions**: 1,053
- **VULNERABILITY references**: 479
- **MITIGATION strategies**: 264
- **VENDOR implementations**: 313
- **GRAND TOTAL**: 2,109 annotations

## Protocol Coverage

### Sectors Covered

1. **Rail Transportation**: ETCS, CBTC, PTC - Complete coverage of modern rail control systems
2. **Electric Utilities**: DNP3, IEC 61850, Modbus - SCADA and substation automation
3. **Manufacturing**: Modbus, OPC UA, PROFINET - Industrial automation
4. **Building Automation**: BACnet - HVAC, lighting, energy management
5. **Aviation**: ADS-B, ACARS - Aircraft communications and surveillance
6. **Cross-Sector**: Modbus, OPC UA used across multiple industries

### Protocol Categories

**Real-Time Control Protocols**:
- ETCS GOOSE (3-10 ms)
- CBTC moving block (<1 second)
- IEC 61850 GOOSE (3-10 ms)
- PROFINET IRT (<1 ms)

**SCADA Protocols**:
- Modbus (RTU, ASCII, TCP)
- DNP3 (serial and TCP)
- IEC 61850 MMS

**Building Automation**:
- BACnet (MS/TP, IP, SC)

**Interoperability Standards**:
- OPC UA (cross-industry)

**Aviation Communication**:
- ADS-B (surveillance)
- ACARS (datalink messaging)

## Vulnerability Categories Covered

### Authentication Weaknesses
- No authentication: Modbus, DNP3 (pre-SA), BACnet (pre-SC), ADS-B, ACARS, PROFINET
- Weak authentication: GSM-R (ETCS), Wi-Fi (CBTC legacy)

### Encryption Gaps
- No encryption: Modbus, BACnet IP, ADS-B, ACARS, PROFINET RT/IRT
- Legacy encryption: GSM-R (ETCS), 220 MHz (PTC)

### Protocol-Specific Attacks
- Jamming: ETCS balises, CBTC wireless, PTC radio, ADS-B, ACARS
- Spoofing: GPS (PTC, CBTC), ADS-B, ACARS, PROFINET DCP
- Replay: DNP3, Modbus, BACnet, IEC 61850 GOOSE
- Man-in-the-middle: All unencrypted protocols

### Physical Security Risks
- Distributed equipment access: WIUs (PTC), balises (ETCS), wayside (CBTC), field devices (all ICS protocols)

## Mitigation Strategies Covered

### Network Security
- Segmentation (all protocols)
- Firewalls (protocol-aware)
- VLANs and VPNs
- Unidirectional gateways

### Protocol Enhancements
- DNP3-SA (Secure Authentication)
- BACnet/SC (Secure Connect)
- IEC 62351 (for IEC 61850)
- OPC UA Security Policies
- FRMCS (future ETCS)

### Intrusion Detection
- ICS-specific IDS (Nozomi, Claroty, Dragos)
- Anomaly detection
- Protocol validation

### Physical Security
- Tamper detection
- Secure enclosures
- Access control

## Vendor Coverage

### Major Vendors by Protocol

**Rail Systems**:
- Siemens, Alstom, Thales, Hitachi, Bombardier (ETCS, CBTC)
- Wabtec, BNSF, Union Pacific (PTC)

**ICS/SCADA**:
- Schneider Electric, Rockwell, Siemens, ABB, Emerson, Honeywell, GE
- SEL, Triangle MicroWorks (DNP3)

**Power Automation**:
- ABB, Siemens, GE Grid, SEL, NR Electric (IEC 61850)

**Industrial Automation**:
- Siemens, Rockwell, Schneider, ABB, Bosch Rexroth, Phoenix Contact (PROFINET)
- Unified Automation, Prosys OPC (OPC UA)

**Building Automation**:
- Johnson Controls, Siemens, Honeywell, Schneider, Trane (BACnet)

**Aviation**:
- Garmin, uAvionix, Collins Aerospace, Honeywell (ADS-B, ACARS)

## Use Case Coverage

### By Industry Vertical

**Transportation**: High-speed rail, metros, freight rail, aviation
**Energy**: Power generation, transmission, distribution, renewables
**Manufacturing**: Automotive, process, packaging, machine tools
**Buildings**: Commercial, healthcare, education, data centers
**Water**: Treatment plants, pump stations, distribution
**Oil & Gas**: Refineries, pipelines, offshore platforms

## Security Standards Referenced

- **IEC 62443**: Industrial Automation and Control Systems Security
- **NERC CIP**: Critical Infrastructure Protection (electric utilities)
- **NIST Cybersecurity Framework**: Risk management
- **CENELEC EN 50126/128/129**: Railway safety standards
- **IEEE 1474**: CBTC standards
- **FAA/ICAO**: Aviation safety and security
- **ASHRAE 135**: BACnet standards

## Training Data Characteristics

### Comprehensiveness
- **60-137 PROTOCOL mentions per file** (avg 96)
- **30-54 VULNERABILITY references per file** (avg 44)
- **11-34 MITIGATION strategies per file** (avg 24)
- **13-48 VENDOR implementations per file** (avg 28)

### Quality Features
- Real-world incident examples
- Specific CVE references where applicable
- Vendor-specific implementation details
- Sector-specific use cases
- Performance characteristics
- Future evolution trends

### Training Value
- Comprehensive protocol specifications
- Security vulnerability taxonomies
- Mitigation strategy effectiveness ratings
- Vendor ecosystem understanding
- Cross-protocol comparison insights
- Industry deployment patterns

## Protocols Identified but Not Yet Extracted

The following protocols were identified in protocol-research.md and are candidates for future training data expansion:

### Power Systems
- IEC 60870-5-104 (SCADA)
- MMS (Manufacturing Message Specification)
- ACSI (IEC 61850 Abstract Communication Service Interface)

### Building/Industrial
- LonWorks (LON/LonTalk)
- KNX (building automation)
- EtherNet/IP (CIP over Ethernet)

### Transportation
- NMEA 0183/2000 (marine navigation)

### Telecommunications
- SS7 (Signaling System 7)
- Diameter protocol
- SIP (Session Initiation Protocol)
- RTP (Real-time Transport Protocol)

### Network Protocols
- MPLS (Multiprotocol Label Switching)
- BGP (Border Gateway Protocol)
- OSPF (Open Shortest Path First)
- Spanning Tree variants

## Next Steps for Expansion

To reach 20 files and 3,000+ annotations, create training data for:

1. **EtherNet/IP** (Allen-Bradley/Rockwell industrial protocol)
2. **IEC 60870-5-104** (European SCADA standard)
3. **SS7/Diameter** (Telecommunications signaling)
4. **SIP/RTP** (VoIP protocols)
5. **BGP/OSPF** (Network routing protocols)
6. **NMEA** (Marine navigation)
7. **LonWorks/KNX** (Building automation alternatives)
8. **HART-IP** (Process instrumentation)

Each additional file would add approximately 150-200 annotations, reaching 3,000+ total across 18-20 files.

## Usage Notes

These training data files are designed for:
- Machine learning model training on protocol analysis
- Security research and vulnerability assessment
- Protocol comparison and selection
- Cybersecurity awareness and education
- Threat modeling and risk analysis
- Industrial control system security

## File Format

Each training file follows a consistent structure:

1. Protocol Overview
2. Architecture and Components
3. Communication Methods
4. Security Vulnerabilities
5. Vendor Implementations
6. Use Cases by Sector
7. Mitigation Strategies
8. Real-World Incidents
9. Standards and Regulations
10. Performance Characteristics
11. Future Directions
12. Annotation Summary

---

**Generated**: 2025-11-06
**Source**: protocol-research.md (49KB comprehensive rail protocol research)
**Coverage**: 11 protocols across 6 industrial sectors
**Total Annotations**: 2,109+
**Status**: Core training data complete, ready for expansion
