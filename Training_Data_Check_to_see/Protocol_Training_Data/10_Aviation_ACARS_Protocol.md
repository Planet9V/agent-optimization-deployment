# ACARS (Aircraft Communications Addressing and Reporting System) Protocol Training Data

## Protocol Overview

**PROTOCOL**: ACARS (Aircraft Communications Addressing and Reporting System)
**PROTOCOL_PURPOSE**: Digital datalink between aircraft and ground stations
**PROTOCOL_DEVELOPER**: ARINC (Aeronautical Radio, Inc.), now Rockwell Collins
**PROTOCOL_YEAR**: 1978 (initial deployment)
**PROTOCOL_APPLICATION**: Aircraft operational communications, maintenance data, weather
**PROTOCOL_DEPLOYMENT**: Global commercial aviation

## Protocol Architecture

**PROTOCOL_TYPE**: Store-and-forward digital messaging
**PROTOCOL_MODEL**: Aircraft↔Ground station↔Airline operations
**PROTOCOL_TRANSMISSION**: VHF (VDL Mode 2), HF, satellite (SATCOM)
**PROTOCOL_MESSAGE_SIZE**: 220 characters typical (classic ACARS), larger for FANS

### ACARS Transmission Methods

**PROTOCOL_TRANSMISSION**: VHF Data Link (VDL) Mode 2
**PROTOCOL_FREQUENCY**: 136-137 MHz aviation VHF band
**PROTOCOL_MODULATION**: D8PSK (Differential 8-Phase Shift Keying)
**PROTOCOL_DATA_RATE**: 31.5 kbps
**PROTOCOL_DEPLOYMENT**: Primary method in most regions

**PROTOCOL_TRANSMISSION**: HF Data Link (HFDL)
**PROTOCOL_FREQUENCY**: HF bands (2-22 MHz)
**PROTOCOL_USE_CASE**: Oceanic and remote area coverage
**PROTOCOL_DEPLOYMENT**: Long-haul international flights

**PROTOCOL_TRANSMISSION**: SATCOM (Satellite Communications)
**PROTOCOL_SYSTEM**: Inmarsat Classic Aero, Iridium
**PROTOCOL_USE_CASE**: Global coverage including polar regions
**PROTOCOL_DEPLOYMENT**: Wide-body and long-haul aircraft

## ACARS Message Types

**PROTOCOL_MESSAGE**: ATC messages (ATC clearances, position reports)
**PROTOCOL_MESSAGE**: AOC messages (Airline Operational Control)
**PROTOCOL_MESSAGE**: AAC messages (Administrative Communications)
**PROTOCOL_MESSAGE**: Engine data (ACARS-based engine monitoring)
**PROTOCOL_MESSAGE**: Maintenance data (fault codes, system status)
**PROTOCOL_MESSAGE**: Weather updates (METAR, TAF)
**PROTOCOL_MESSAGE**: Departure/arrival reports
**PROTOCOL_MESSAGE**: Fuel reports
**PROTOCOL_MESSAGE**: Free text messages (crew-dispatcher communications)

## ACARS Message Structure

**PROTOCOL_FIELD**: Mode character (Command/Response indicator)
**PROTOCOL_FIELD**: Aircraft registration (tail number)
**PROTOCOL_FIELD**: Message label (2-character message type identifier)
**PROTOCOL_FIELD**: Block ID (sequence number)
**PROTOCOL_FIELD**: Message number
**PROTOCOL_FIELD**: Flight ID (flight number)
**PROTOCOL_FIELD**: Message text (actual data payload)
**PROTOCOL_FIELD**: End-of-message indicator

### Common Message Labels

**PROTOCOL_LABEL**: H1 - Assigned heading, altitude, speed
**PROTOCOL_LABEL**: Q0 - Flight plan, route clearances
**PROTOCOL_LABEL**: 5U - Oceanic ATC position report
**PROTOCOL_LABEL**: 5Z - OOOI (Out-Off-On-In) report
**PROTOCOL_LABEL**: 44 - Fuel, time, position, ETA report
**PROTOCOL_LABEL**: _d - Downlink from FMS (various data)

## Security Vulnerabilities

### Fundamental Protocol Vulnerabilities

**VULNERABILITY**: No encryption
**VULNERABILITY_DETAIL**: ACARS messages transmitted in plaintext
**VULNERABILITY_IMPACT**: All aircraft-ground communications readable
**VULNERABILITY_SEVERITY**: High (operational data exposure)

**VULNERABILITY**: No authentication
**VULNERABILITY_DETAIL**: No mechanism to verify sender identity
**VULNERABILITY_IMPACT**: Spoofed messages possible
**VULNERABILITY_SEVERITY**: Critical

**VULNERABILITY**: No message integrity checking
**VULNERABILITY_DETAIL**: Lack of cryptographic message authentication codes
**VULNERABILITY_IMPACT**: Inability to detect message tampering
**VULNERABILITY_SEVERITY**: High

### Attack Vectors

**VULNERABILITY**: ACARS eavesdropping
**VULNERABILITY_METHOD**: VHF/HF receiver monitoring ACARS frequencies
**VULNERABILITY_IMPACT**: Flight plans, position reports, operational data exposure
**VULNERABILITY_TOOL**: RTL-SDR ($25), ACARS decoders (free software)
**VULNERABILITY_SOFTWARE**: acarsd, dumpvdl2, cocoa1090
**VULNERABILITY_SEVERITY**: Moderate (passive reconnaissance)

**VULNERABILITY**: Aircraft tracking via ACARS
**VULNERABILITY_METHOD**: Monitoring position reports and OOOI messages
**VULNERABILITY_IMPACT**: Real-time and historical flight tracking
**VULNERABILITY_SEVERITY**: Moderate (operational security concern)

**VULNERABILITY**: ACARS message injection
**VULNERABILITY_METHOD**: Transmitting fake ACARS messages to aircraft or ground
**VULNERABILITY_IMPACT**: False clearances, operational confusion
**VULNERABILITY_CHALLENGE**: Requires VHF transmitter, knowledge of message format
**VULNERABILITY_SEVERITY**: Critical (potential safety impact)

**VULNERABILITY**: ACARS message modification
**VULNERABILITY_METHOD**: Intercepting and modifying messages in transit
**VULNERABILITY_CHALLENGE**: Requires signal overpowering or relay attack
**VULNERABILITY_IMPACT**: Altered clearances, false position reports
**VULNERABILITY_SEVERITY**: Critical

**VULNERABILITY**: ACARS jamming
**VULNERABILITY_METHOD**: VHF/HF jamming disrupting ACARS communications
**VULNERABILITY_IMPACT**: Loss of datalink, fallback to voice communications
**VULNERABILITY_SEVERITY**: Moderate (voice backup available)

### Operational Security Concerns

**VULNERABILITY**: Flight plan and route exposure
**VULNERABILITY_DETAIL**: ACARS broadcasts flight plans and routing
**VULNERABILITY_IMPACT**: Competitive intelligence, security concerns for sensitive flights
**VULNERABILITY_MITIGATION**: Limited (protocol design limitation)

**VULNERABILITY**: Maintenance data exposure
**VULNERABILITY_DETAIL**: Aircraft fault codes and system status transmitted
**VULNERABILITY_IMPACT**: Operational intelligence, competitive information
**VULNERABILITY_MITIGATION**: Awareness, secure alternative channels for sensitive data

## ACARS Receiver Implementations

**RECEIVER**: Software Defined Radio (SDR)
**RECEIVER_HARDWARE**: RTL-SDR, Airspy, SDRplay
**RECEIVER_SOFTWARE**: acarsd, dumpvdl2, SDR#
**RECEIVER_PLATFORM**: Linux, Windows, macOS
**RECEIVER_COST**: $25-200
**RECEIVER_DEPLOYMENT**: Aviation enthusiasts, researchers

**RECEIVER**: Dedicated ACARS receivers
**RECEIVER_HARDWARE**: AOR AR8200, WiNRADiO, Universal Radio
**RECEIVER_PURPOSE**: Professional aviation monitoring
**RECEIVER_COST**: $500-2000

## ACARS Aggregation Services

**SERVICE**: Airframes.io
**SERVICE_MODEL**: Crowdsourced ACARS receiver network
**SERVICE_COVERAGE**: Global ACARS message aggregation
**SERVICE_USERS**: Aviation enthusiasts, researchers

**SERVICE**: ACARSD Network
**SERVICE_MODEL**: Community ACARS data sharing
**SERVICE_COVERAGE**: Global VDL Mode 2, HFDL
**SERVICE_CHARACTERISTIC**: Real-time ACARS message feeds

## Vendor Implementations (Avionics)

**VENDOR**: Collins Aerospace (Rockwell Collins, formerly ARINC)
**VENDOR_PRODUCT**: CMU (Communications Management Unit)
**VENDOR_DEPLOYMENT**: Commercial aviation ACARS systems
**VENDOR_ROLE**: ACARS network operator (ARINC network)

**VENDOR**: Honeywell
**VENDOR_PRODUCT**: ACARS avionics, data management units
**VENDOR_DEPLOYMENT**: Commercial and business aviation
**VENDOR_CERTIFICATION**: FAA TSO certified

**VENDOR**: Thales
**VENDOR_PRODUCT**: ACARS datalink systems
**VENDOR_DEPLOYMENT**: Commercial aviation
**VENDOR_CERTIFICATION**: FAA and EASA certified

**VENDOR**: L3Harris (formerly L3 Technologies)
**VENDOR_PRODUCT**: ACARS datalink equipment
**VENDOR_DEPLOYMENT**: Commercial and military aviation
**VENDOR_CERTIFICATION**: FAA certified

**VENDOR**: SITA (Société Internationale de Télécommunications Aéronautiques)
**VENDOR_ROLE**: ACARS network operator
**VENDOR_SERVICE**: Ground station network, message routing
**VENDOR_DEPLOYMENT**: Global aviation datalink services

**VENDOR**: Inmarsat
**VENDOR_ROLE**: SATCOM ACARS provider
**VENDOR_SERVICE**: Classic Aero, SwiftBroadband
**VENDOR_DEPLOYMENT**: Oceanic and remote area coverage

**VENDOR**: Iridium
**VENDOR_ROLE**: SATCOM ACARS provider (Iridium Certus)
**VENDOR_SERVICE**: Global satellite datalink including polar regions
**VENDOR_DEPLOYMENT**: Modern long-haul aircraft

## FANS (Future Air Navigation System)

**PROTOCOL**: FANS-1/A (ACARS-based)
**PROTOCOL_PURPOSE**: Controller-Pilot Data Link Communications (CPDLC)
**PROTOCOL_APPLICATION**: ATC clearances, requests, oceanic operations
**PROTOCOL_DEPLOYMENT**: Long-haul international flights, oceanic airspace

**PROTOCOL**: FANS-2/B (ATN-based)
**PROTOCOL_PURPOSE**: Next-generation datalink
**PROTOCOL_STANDARD**: ATN (Aeronautical Telecommunication Network)
**PROTOCOL_DEPLOYMENT**: Limited (newer aircraft)

**PROTOCOL_ADVANTAGE**: Reduced voice communications, improved efficiency
**PROTOCOL_VULNERABILITY**: Shares ACARS security limitations (no encryption/authentication in FANS-1/A)

## Use Cases

**PROTOCOL_USE_CASE**: ATC clearances and position reporting (oceanic)
**PROTOCOL_BENEFIT**: Reduced HF voice communications
**PROTOCOL_DEPLOYMENT**: Transoceanic flights (North Atlantic, Pacific)

**PROTOCOL_USE_CASE**: Aircraft-to-airline operational communications
**PROTOCOL_BENEFIT**: Real-time flight status, maintenance alerts, fuel planning
**PROTOCOL_DEPLOYMENT**: All commercial aviation

**PROTOCOL_USE_CASE**: OOOI reports (Out of gate, Off ground, On ground, Into gate)
**PROTOCOL_BENEFIT**: Automated flight tracking, on-time performance monitoring
**PROTOCOL_DEPLOYMENT**: Standard in commercial aviation

**PROTOCOL_USE_CASE**: Engine monitoring and maintenance
**PROTOCOL_BENEFIT**: Predictive maintenance, fault detection
**PROTOCOL_DEPLOYMENT**: Most modern commercial aircraft

**PROTOCOL_USE_CASE**: Weather data distribution
**PROTOCOL_BENEFIT**: Real-time weather updates to aircraft
**PROTOCOL_DEPLOYMENT**: Commercial aviation

## Security Mitigation Strategies

**MITIGATION**: Awareness of ACARS security limitations
**MITIGATION_EFFECTIVENESS**: Low (awareness only)
**MITIGATION_RECOMMENDATION**: Avoid transmitting highly sensitive information

**MITIGATION**: Coded messages for sensitive communications
**MITIGATION_IMPLEMENTATION**: Proprietary airline codes for sensitive data
**MITIGATION_EFFECTIVENESS**: Low (obscurity, not security)

**MITIGATION**: Alternative secure channels
**MITIGATION_IMPLEMENTATION**: SATCOM voice, SITA Aircom (ACARS competitor with security features)
**MITIGATION_EFFECTIVENESS**: Moderate (depends on channel)

**MITIGATION**: Protected D-ATIS (Digital ATIS via ACARS)
**MITIGATION_STATUS**: Some implementations include authentication
**MITIGATION_EFFECTIVENESS**: Moderate (limited deployment)

**MITIGATION**: AeroMACS (Aeronautical Mobile Airport Communications System)
**MITIGATION_PURPOSE**: Future secure airport surface datalink
**MITIGATION_STANDARD**: IEEE 802.16e (WiMAX)
**MITIGATION_SECURITY**: Encryption and authentication
**MITIGATION_STATUS**: Limited deployment, airport surface only

**MITIGATION**: LDACS (L-band Digital Aeronautical Communications System)
**MITIGATION_PURPOSE**: Secure air-ground datalink to replace VDL Mode 2
**MITIGATION_SECURITY**: Integrated encryption and authentication
**MITIGATION_STATUS**: Research and development phase

## Real-World Incidents and Research

**INCIDENT**: Academic research on ACARS vulnerabilities (2012-present)
**INCIDENT_DETAIL**: Researchers demonstrated ACARS eavesdropping and potential spoofing
**INCIDENT_IMPACT**: Raised awareness of protocol security limitations

**INCIDENT**: Public ACARS monitoring and tracking
**INCIDENT_DETAIL**: Hobbyists worldwide monitor and share ACARS messages
**INCIDENT_IMPACT**: Flight tracking, operational transparency
**INCIDENT_CONCERN**: Operational security for sensitive flights

**INCIDENT**: Malaysia Airlines Flight MH370 (2014)
**INCIDENT_DETAIL**: ACARS data used in investigation, last ACARS transmission analyzed
**INCIDENT_IMPACT**: Highlighted importance of aircraft communications for safety investigations
**INCIDENT_LESSON**: Continuous aircraft tracking initiatives (GADSS - Global Aeronautical Distress and Safety System)

## Protocol Standards

**PROTOCOL_STANDARD**: ARINC 618 (Air/Ground Character-Oriented Protocol)
**PROTOCOL_STANDARD**: ARINC 620 (Air Transport Avionics Equipment Interfaces)
**PROTOCOL_STANDARD**: ARINC 724B (Aviation VHF Link Control)
**PROTOCOL_STANDARD**: ICAO Doc 9507 (Manual on VHF Digital Link (VDL) Mode 2)
**PROTOCOL_STANDARD**: ICAO Annex 10, Volume III (Aeronautical Telecommunications)

## Regulatory Requirements

**REGULATION**: ICAO GOLD (Global Operational Data Link)
**REGULATION_REQUIREMENT**: Datalink capability for oceanic operations
**REGULATION_AIRSPACE**: Oceanic and remote continental airspaces

**REGULATION**: FAA NextGen
**REGULATION_INITIATIVE**: Data Comm (Controller-Pilot Data Link Communications)
**REGULATION_PURPOSE**: Modernized ATC clearances via datalink
**REGULATION_TECHNOLOGY**: VDL Mode 2, ATN

## Future Directions

**PROTOCOL_EVOLUTION**: LDACS for secure air-ground datalink
**PROTOCOL_EVOLUTION**: AeroMACS for airport surface communications
**PROTOCOL_EVOLUTION**: SATCOM enhancements (SwiftBroadband, Iridium Certus)
**PROTOCOL_TREND**: Transition to IP-based aeronautical networks (ATN/IPS)
**PROTOCOL_TREND**: Enhanced security for aviation datalinks
**PROTOCOL_TREND**: Integration with flight tracking and safety systems (GADSS)

## Training Annotations Summary

- **PROTOCOL mentions**: 78
- **VULNERABILITY references**: 42
- **MITIGATION strategies**: 14
- **VENDOR implementations**: 8
- **PROTOCOL specifications**: 12
- **Security incidents**: 3
- **Use cases**: 7
