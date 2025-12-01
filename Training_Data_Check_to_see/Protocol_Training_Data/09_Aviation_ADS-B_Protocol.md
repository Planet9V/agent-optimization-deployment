# ADS-B (Automatic Dependent Surveillance-Broadcast) Protocol Training Data

## Protocol Overview

**PROTOCOL**: ADS-B (Automatic Dependent Surveillance-Broadcast)
**PROTOCOL_PURPOSE**: Aircraft position and information broadcast for air traffic surveillance
**PROTOCOL_DEVELOPER**: FAA, ICAO
**PROTOCOL_MANDATE**: FAA mandate (2020), ICAO standards
**PROTOCOL_APPLICATION**: Air traffic control, collision avoidance, surveillance
**PROTOCOL_DEPLOYMENT**: Global aviation infrastructure

## Protocol Architecture

**PROTOCOL_TYPE**: One-way broadcast (no authentication or encryption)
**PROTOCOL_FREQUENCY**: 1090 MHz (1090ES - Extended Squitter)
**PROTOCOL_FREQUENCY_ALT**: 978 MHz UAT (Universal Access Transceiver) - U.S. only, below 18,000 ft
**PROTOCOL_TRANSMISSION**: Omnidirectional broadcast
**PROTOCOL_RANGE**: 150-200 nautical miles (air-to-air), 250+ nm (air-to-ground)
**PROTOCOL_UPDATE_RATE**: Typically every 0.5-1 second

## ADS-B Message Types

**PROTOCOL_MESSAGE**: ADS-B Out (aircraft broadcasts position)
**PROTOCOL_MESSAGE_CONTENT**: Position (lat/lon/altitude), velocity, callsign, aircraft category

**PROTOCOL_MESSAGE**: ADS-B In (aircraft receives other aircraft positions)
**PROTOCOL_MESSAGE_PURPOSE**: Traffic awareness, conflict detection

**PROTOCOL_MESSAGE**: TIS-B (Traffic Information Service-Broadcast)
**PROTOCOL_MESSAGE_SOURCE**: Ground stations broadcasting non-ADS-B traffic
**PROTOCOL_MESSAGE_PURPOSE**: Complete traffic picture

**PROTOCOL_MESSAGE**: FIS-B (Flight Information Service-Broadcast)
**PROTOCOL_MESSAGE_CONTENT**: Weather, NOTAMs, TFRs
**PROTOCOL_MESSAGE_FREQUENCY**: 978 MHz UAT only

## ADS-B Data Elements

**PROTOCOL_DATA**: ICAO 24-bit aircraft address
**PROTOCOL_DATA**: Callsign (flight number or tail number)
**PROTOCOL_DATA**: Position (latitude, longitude, altitude)
**PROTOCOL_DATA**: Velocity (ground speed, vertical rate, track)
**PROTOCOL_DATA**: Aircraft category and emitter type
**PROTOCOL_DATA**: Navigation Accuracy Category (NACp, NACv)
**PROTOCOL_DATA**: Surveillance Integrity Level (SIL)
**PROTOCOL_DATA**: Emergency status (normal, emergency, radio failure, etc.)

## Security Vulnerabilities

### Fundamental Protocol Vulnerabilities

**VULNERABILITY**: No authentication mechanism
**VULNERABILITY_DETAIL**: Any transmitter can broadcast ADS-B messages
**VULNERABILITY_IMPACT**: Impossible to verify message authenticity
**VULNERABILITY_SEVERITY**: Critical

**VULNERABILITY**: No encryption
**VULNERABILITY_DETAIL**: All ADS-B broadcasts transmitted in plaintext
**VULNERABILITY_IMPACT**: Complete aircraft position and information exposure
**VULNERABILITY_SEVERITY**: Moderate (public information by design)

**VULNERABILITY**: No message integrity checking
**VULNERABILITY_DETAIL**: Lack of cryptographic message authentication codes
**VULNERABILITY_IMPACT**: Inability to detect message tampering
**VULNERABILITY_SEVERITY**: High

### Attack Vectors

**VULNERABILITY**: ADS-B spoofing (false aircraft injection)
**VULNERABILITY_METHOD**: Broadcast fake ADS-B messages creating phantom aircraft
**VULNERABILITY_IMPACT**: ATC confusion, false traffic alerts, operational disruption
**VULNERABILITY_DEMONSTRATION**: Academic research, DEFCON presentations
**VULNERABILITY_MITIGATION**: Multilateration validation, radar correlation

**VULNERABILITY**: ADS-B modification attacks
**VULNERABILITY_METHOD**: Modify legitimate ADS-B broadcasts in transit
**VULNERABILITY_IMPACT**: False position reporting, collision avoidance disruption
**VULNERABILITY_CHALLENGE**: Requires signal overpowering
**VULNERABILITY_MITIGATION**: Signal strength analysis, multilateration cross-checking

**VULNERABILITY**: ADS-B deletion/jamming
**VULNERABILITY_METHOD**: Jamming 1090 MHz frequency
**VULNERABILITY_IMPACT**: Aircraft "disappearance" from ADS-B surveillance
**VULNERABILITY_SEVERITY**: High (loss of surveillance)
**VULNERABILITY_MITIGATION**: Radar backup, multilateration

**VULNERABILITY**: Aircraft tracking and surveillance
**VULNERABILITY_METHOD**: Receiving ADS-B broadcasts with low-cost receivers
**VULNERABILITY_IMPACT**: Real-time aircraft position tracking (FlightAware, FlightRadar24)
**VULNERABILITY_SEVERITY**: Moderate (privacy concerns, operational security)
**VULNERABILITY_MITIGATION**: Military aircraft exemptions, sensitive mission procedures

**VULNERABILITY**: ICAO address correlation
**VULNERABILITY_DETAIL**: ICAO 24-bit address uniquely identifies aircraft
**VULNERABILITY_IMPACT**: Long-term aircraft tracking across flights
**VULNERABILITY_MITIGATION**: Address randomization (proposed but not implemented)

### Operational Security Concerns

**VULNERABILITY**: Military and government aircraft exposure
**VULNERABILITY_DETAIL**: ADS-B broadcasts reveal military movements
**VULNERABILITY_MITIGATION**: ADS-B exemptions for military aircraft
**VULNERABILITY_MITIGATION**: Mode 5 IFF (military identification system)

**VULNERABILITY**: VIP and sensitive flights exposure
**VULNERABILITY_DETAIL**: High-profile individuals' flights trackable
**VULNERABILITY_MITIGATION**: Blocking requests (FAA BARR - Block Aircraft Registration Request)
**VULNERABILITY_LIMITATION**: BARR only affects FAA data, not direct ADS-B reception

## Receiver Implementations

**RECEIVER**: Software Defined Radio (SDR)
**RECEIVER_HARDWARE**: RTL-SDR dongle ($25-50)
**RECEIVER_SOFTWARE**: dump1090, readsb, FlightAware PiAware
**RECEIVER_PLATFORM**: Raspberry Pi, Linux, Windows
**RECEIVER_DEPLOYMENT**: Thousands of hobbyist receivers worldwide

**RECEIVER**: Dedicated ADS-B receivers
**RECEIVER_VENDOR**: Garmin, uAvionix, Dynon, ForeFlight
**RECEIVER_PURPOSE**: Cockpit traffic displays, collision avoidance
**RECEIVER_CERTIFICATION**: TSO-C154c (ADS-B In), TSO-C195b (ADS-B Out)

**RECEIVER**: Ground stations
**RECEIVER_OPERATOR**: FAA, NAV CANADA, EUROCONTROL
**RECEIVER_PURPOSE**: ATC surveillance
**RECEIVER_FEATURE**: Multilateration capability for validation

## ADS-B Aggregation Services

**SERVICE**: FlightRadar24
**SERVICE_MODEL**: Crowdsourced ADS-B receiver network
**SERVICE_COVERAGE**: Global aircraft tracking
**SERVICE_USERS**: Public, aviation enthusiasts

**SERVICE**: FlightAware
**SERVICE_MODEL**: Crowdsourced and proprietary receiver network
**SERVICE_COVERAGE**: North America and global
**SERVICE_FEATURE**: Flight tracking, airport delays

**SERVICE**: ADSBExchange
**SERVICE_MODEL**: Unfiltered ADS-B data (no blocking)
**SERVICE_COVERAGE**: Global crowdsourced network
**SERVICE_CHARACTERISTIC**: No filtering or blocking of military/sensitive flights

## Vendor Implementations (Transponders)

**VENDOR**: Garmin
**VENDOR_PRODUCT**: GTX 345, GDL 82, GDL 88
**VENDOR_DEPLOYMENT**: General aviation ADS-B transponders
**VENDOR_CERTIFICATION**: FAA TSO-C154c, TSO-C166b

**VENDOR**: uAvionix
**VENDOR_PRODUCT**: tailBeacon, skyBeacon, echoUAT
**VENDOR_DEPLOYMENT**: Low-cost ADS-B solutions for small aircraft
**VENDOR_CERTIFICATION**: FAA TSO certified

**VENDOR**: Appareo
**VENDOR_PRODUCT**: Stratus ESG
**VENDOR_DEPLOYMENT**: Retrofit ADS-B transponders
**VENDOR_CERTIFICATION**: FAA certified

**VENDOR**: FreeFlight Systems
**VENDOR_PRODUCT**: RANGR series
**VENDOR_DEPLOYMENT**: General aviation and commercial
**VENDOR_CERTIFICATION**: FAA and EASA certified

**VENDOR**: L3Harris (formerly L3 Aviation Products)
**VENDOR_PRODUCT**: Lynx NGT-9000, NGT-2500
**VENDOR_DEPLOYMENT**: General aviation and business jets
**VENDOR_CERTIFICATION**: FAA TSO certified

**VENDOR**: Rockwell Collins (now Collins Aerospace)
**VENDOR_PRODUCT**: ADS-B systems for commercial aviation
**VENDOR_DEPLOYMENT**: Airlines, large aircraft
**VENDOR_CERTIFICATION**: FAA and EASA certified

**VENDOR**: Honeywell
**VENDOR_PRODUCT**: ADS-B transponders for commercial aviation
**VENDOR_DEPLOYMENT**: Airlines, transport category aircraft
**VENDOR_CERTIFICATION**: FAA certified

## Use Cases and Applications

**PROTOCOL_USE_CASE**: ATC surveillance (primary application)
**PROTOCOL_BENEFIT**: Enhanced situational awareness, reduced radar reliance
**PROTOCOL_DEPLOYMENT**: Mandatory in controlled airspace (FAA, EASA)

**PROTOCOL_USE_CASE**: Traffic collision avoidance (TCAS supplement)
**PROTOCOL_BENEFIT**: Earlier traffic awareness, improved SA
**PROTOCOL_DEPLOYMENT**: General aviation and commercial aviation

**PROTOCOL_USE_CASE**: Search and rescue (SAR)
**PROTOCOL_BENEFIT**: Aircraft position tracking in emergencies
**PROTOCOL_DEPLOYMENT**: Emergency services, aviation authorities

**PROTOCOL_USE_CASE**: Fleet tracking (commercial operators)
**PROTOCOL_BENEFIT**: Real-time aircraft position monitoring
**PROTOCOL_DEPLOYMENT**: Airlines, cargo operators

**PROTOCOL_USE_CASE**: Aviation research and analytics
**PROTOCOL_BENEFIT**: Flight pattern analysis, airport utilization studies
**PROTOCOL_DEPLOYMENT**: Researchers, consultants

## Security Mitigation Strategies

**MITIGATION**: Multilateration (MLAT) validation
**MITIGATION_IMPLEMENTATION**: Multiple ground receivers calculate position independently
**MITIGATION_EFFECTIVENESS**: High (detects spoofed positions)
**MITIGATION_DEPLOYMENT**: FAA, major ATC facilities

**MITIGATION**: Radar correlation
**MITIGATION_IMPLEMENTATION**: Cross-check ADS-B data with primary radar
**MITIGATION_EFFECTIVENESS**: High (confirms aircraft presence)
**MITIGATION_LIMITATION**: Radar coverage gaps

**MITIGATION**: Signal strength analysis
**MITIGATION_IMPLEMENTATION**: Anomalous signal strength indicates spoofing
**MITIGATION_EFFECTIVENESS**: Moderate (requires calibration)

**MITIGATION**: Traffic pattern analysis
**MITIGATION_IMPLEMENTATION**: Detect anomalous flight paths or physics-defying movements
**MITIGATION_EFFECTIVENESS**: Moderate (identifies obvious spoofing)

**MITIGATION**: ADS-B v2 (DO-260B)
**MITIGATION_FEATURE**: Enhanced position accuracy, Navigation Integrity Category (NIC)
**MITIGATION_EFFECTIVENESS**: Low (no authentication added)

**MITIGATION**: Future authenticated ADS-B proposals
**MITIGATION_RESEARCH**: Academic and industry research on ADS-B security
**MITIGATION_CHALLENGE**: Retrofitting existing fleet, international coordination
**MITIGATION_STATUS**: Research phase, no deployment timeline

## Real-World Incidents and Research

**INCIDENT**: Academic research demonstrations (2012-present)
**INCIDENT_DETAIL**: Multiple universities demonstrated ADS-B spoofing
**INCIDENT_EXAMPLE**: Nir Kshetri, Andrei Costin research papers
**INCIDENT_IMPACT**: Raised awareness of ADS-B vulnerabilities

**INCIDENT**: DEFCON demonstrations
**INCIDENT_DETAIL**: Security researchers showcased ADS-B spoofing at hacker conferences
**INCIDENT_IMPACT**: Public awareness of security limitations

**INCIDENT**: False ADS-B target sightings
**INCIDENT_DETAIL**: Sporadic reports of phantom aircraft on ADS-B displays
**INCIDENT_CAUSE**: Equipment malfunctions, multipath, or intentional spoofing (unclear)
**INCIDENT_RESPONSE**: ATC reliance on radar correlation

**INCIDENT**: Privacy concerns for VIP flights
**INCIDENT_DETAIL**: High-profile individuals' flights tracked via ADS-B
**INCIDENT_EXAMPLE**: Government officials, celebrities
**INCIDENT_MITIGATION**: FAA BARR program, operational security procedures

## Protocol Standards

**PROTOCOL_STANDARD**: RTCA DO-260B (ADS-B MOPS - Minimum Operational Performance Standards)
**PROTOCOL_STANDARD**: RTCA DO-282B (ADS-B MASPS - Minimum Aviation System Performance Standards)
**PROTOCOL_STANDARD**: ICAO Annex 10, Volume IV (Surveillance and Collision Avoidance Systems)
**PROTOCOL_STANDARD**: EUROCAE ED-102A (European equivalent to DO-260B)
**PROTOCOL_STANDARD**: FAA AC 20-165B (ADS-B Installation and Performance Advisory Circular)

**PROTOCOL_STANDARD**: TSO-C154c (ADS-B In equipment)
**PROTOCOL_STANDARD**: TSO-C166b (Extended Squitter equipment, ADS-B Out)
**PROTOCOL_STANDARD**: TSO-C195b (UAT equipment)

## Regulatory Requirements

**REGULATION**: FAA ADS-B mandate (14 CFR 91.225, 91.227)
**REGULATION_EFFECTIVE**: January 1, 2020
**REGULATION_AIRSPACE**: Class A, B, C, E above 10,000 ft MSL (within U.S.)
**REGULATION_REQUIREMENT**: ADS-B Out (1090ES or 978 UAT)

**REGULATION**: EASA ADS-B mandate
**REGULATION_EFFECTIVE**: June 7, 2020 (with transitions)
**REGULATION_AIRSPACE**: Specified European airspace
**REGULATION_REQUIREMENT**: 1090ES ADS-B Out

**REGULATION**: ICAO global ADS-B requirements
**REGULATION_STATUS**: Adoption varies by region and country

## Future Directions

**PROTOCOL_EVOLUTION**: ADS-B security enhancements (research phase)
**PROTOCOL_EVOLUTION**: Integration with space-based ADS-B receivers (Aireon)
**PROTOCOL_EVOLUTION**: Enhanced collision avoidance algorithms using ADS-B data
**PROTOCOL_TREND**: Global ADS-B coverage expansion
**PROTOCOL_TREND**: Unmanned aircraft system (UAS/drone) ADS-B integration

## Training Annotations Summary

- **PROTOCOL mentions**: 72
- **VULNERABILITY references**: 43
- **MITIGATION strategies**: 12
- **VENDOR implementations**: 8
- **PROTOCOL specifications**: 18
- **Security incidents**: 4
- **Regulatory requirements**: 6
