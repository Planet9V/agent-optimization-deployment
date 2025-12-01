# Government Sector - Communication Protocols and Technical Standards

## Building Automation Protocols

### BACnet (Building Automation and Control Networks)
**BACnet Overview**
- ASHRAE/ANSI Standard 135
- ISO 16484-5 international standard
- Open protocol for building automation
- Developed by ASHRAE in 1995
- Most widely adopted building automation protocol

**BACnet Physical Layers**
- **BACnet/IP**: Ethernet/IP networks (most common)
- **BACnet MS/TP**: Master-Slave/Token-Passing over RS-485
- **BACnet/SC**: Secure Connect (websocket-based, encrypted)
- **BACnet Ethernet**: ISO 8802-3 (legacy)
- **BACnet ARCNET**: Legacy token-passing network
- **BACnet LonTalk**: LonWorks integration
- **BACnet/WS**: Web services (SOAP/XML)

**BACnet Objects**
- Analog Input (AI) - Temperature, pressure sensors
- Analog Output (AO) - Valve/damper control
- Analog Value (AV) - Setpoints, calculated values
- Binary Input (BI) - Status switches, door contacts
- Binary Output (BO) - On/off control (pumps, fans)
- Binary Value (BV) - Status flags, boolean values
- Multi-State Input (MI) - Mode status (heat/cool/auto)
- Multi-State Output (MO) - Mode commands
- Schedule Objects - Time-based control
- Trend Log Objects - Historical data storage
- Alarm and Event Objects - Alarming and notifications
- Device Object - Controller identification

**BACnet Services**
- ReadProperty, WriteProperty, WritePropertyMultiple
- SubscribeCOV (Change of Value notification)
- Who-Is, I-Am (device discovery)
- CreateObject, DeleteObject
- GetAlarmSummary, GetEnrollmentSummary
- TimeSynchronization
- ReinitializeDevice
- DeviceCommunicationControl

**BACnet Interoperability**
- BACnet Testing Laboratories (BTL) certification
- BIBBs (BACnet Interoperability Building Blocks)
- PICS (Protocol Implementation Conformance Statement)
- Standardized device profiles (B-BC, B-AAC, B-ASC, B-SS, B-SA)
- Guaranteed interoperability between BTL-listed devices

### LonWorks (Local Operating Network)
**LonWorks Overview**
- ISO/IEC 14908 standard
- Developed by Echelon Corporation (1990s)
- Peer-to-peer distributed control architecture
- Neuron chip-based devices
- Legacy protocol (being replaced by BACnet)

**LonWorks Components**
- **Neuron Chip**: Embedded controller with built-in networking
- **LonTalk Protocol**: Communication protocol
- **LNS (LonWorks Network Services)**: Network management software
- **SNVT (Standard Network Variable Types)**: Standardized data types
- **LonMark Certification**: Interoperability certification

**Physical Layers**
- TP/FT-10 (Twisted Pair Free Topology) - Most common, RS-485-like
- PL (Power Line) - Communication over AC power lines
- IP-852 - LonWorks over IP/Ethernet

**Applications**
- HVAC control (legacy installations)
- Lighting control
- Access control
- Fire alarm systems
- Integration with BACnet (via gateways)

### Modbus
**Modbus Overview**
- Developed by Modicon (now Schneider Electric) in 1979
- Simple, robust, widely supported
- Master-slave communication
- Open standard (no licensing fees)

**Modbus Variants**
- **Modbus RTU**: Serial (RS-485, RS-232), binary format
- **Modbus ASCII**: Serial, ASCII character format
- **Modbus TCP/IP**: Ethernet/IP, most common in modern BAS

**Modbus Protocol Details**
- **Registers**: Holding registers (read/write), input registers (read-only)
- **Coils**: Digital outputs (read/write)
- **Discrete Inputs**: Digital inputs (read-only)
- **Function Codes**: Read coils (01), read holding registers (03), write single coil (05), write single register (06), write multiple registers (16)
- **Slave Addressing**: 1-247 device addresses

**Applications in Building Automation**
- Energy meters and power monitoring
- VFD (Variable Frequency Drive) control
- HVAC equipment integration
- Chiller and boiler monitoring
- Lighting control (DALI gateways)
- Integration with BACnet systems (via gateways)

### KNX (Konnex)
**KNX Overview**
- European standard for home and building automation
- EN 50090, ISO/IEC 14543
- Convergence of EIB, EHS, and BatiBus protocols
- Popular in Europe, growing globally
- Certified training and products

**Physical Media**
- KNX TP (Twisted Pair) - 9.6 kbps, bus topology
- KNX PL (Power Line) - Communication over AC power
- KNX RF (Radio Frequency) - Wireless 868 MHz
- KNX IP (Ethernet) - KNXnet/IP tunneling and routing

**Applications**
- Lighting control (dimming, switching, scene control)
- Shading and blind control
- HVAC control
- Security systems integration
- Energy management
- Building visualization

### DALI (Digital Addressable Lighting Interface)
**DALI Overview**
- IEC 62386 standard
- Two-wire communication for lighting control
- Up to 64 devices per DALI line
- Bi-directional communication
- No polarity requirement (twisted pair)

**DALI Features**
- Individual luminaire addressing (0-63)
- Dimming control (0-100%, 254 steps)
- Group addressing (up to 16 groups)
- Scene control (up to 16 scenes)
- Status feedback (lamp failure, ballast status)
- Broadcast commands
- Query commands (status, configuration)

**DALI-2 Enhancements**
- Backward compatible with DALI-1
- Input devices (switches, sensors)
- Color control (tunable white, RGB)
- Emergency lighting testing
- Improved device types and certification

**Integration**
- DALI gateways to BACnet, Modbus, KNX
- Integration with BAS for whole-building control
- Lighting management software

### OPC UA (Open Platform Communications Unified Architecture)
**OPC UA Overview**
- IEC 62541 standard
- Platform-independent (Windows, Linux, embedded)
- Secure communication (encryption, authentication)
- Successor to OPC Classic (OPC DA, OPC HDA, OPC A&E)
- Service-oriented architecture (SOA)

**OPC UA Features**
- Unified data model
- Publish-subscribe and client-server models
- Historical data access
- Alarms and events
- Security (user authentication, message encryption)
- Scalability (embedded to enterprise)
- Platform independence

**Applications in Building Automation**
- Integration of IT and OT systems
- Building automation to enterprise systems integration
- SCADA integration
- Data analytics platforms
- Cloud connectivity
- IoT gateways

## Access Control Protocols

### Wiegand Protocol
**Wiegand Overview**
- De facto standard for card reader communication
- Developed in the 1970s
- Simple, one-way communication (reader to controller)
- Not encrypted (security concern)

**Wiegand Formats**
- **26-bit Wiegand**: Most common (8-bit facility code, 16-bit card number, 2 parity bits)
- **37-bit Wiegand**: 16-bit facility code, 19-bit card number
- **35-bit Corporate 1000**: HID proprietary
- Custom formats (up to 128 bits on some systems)

**Wiegand Limitations**
- One-way communication (no reader feedback)
- Limited cable distance (typically 500 feet)
- No encryption (card data transmitted in clear)
- Susceptible to tampering (man-in-the-middle attacks)

### OSDP (Open Supervised Device Protocol)
**OSDP Overview**
- SIA (Security Industry Association) standard
- Secure, bi-directional communication
- Replacement for Wiegand
- Encrypted communication (AES-128)
- Tamper detection and supervision

**OSDP Features**
- Two-way communication (reader to/from controller)
- Secure Channel (OSDP Secure) - AES-128 encryption
- Device authentication
- Tamper detection
- LED and beeper control (from controller)
- Biometric data transmission
- Multi-drop RS-485 bus
- Longer cable distances (up to 4,000 feet)

**OSDP Advantages Over Wiegand**
- Secure encrypted communication
- Bi-directional (controller can control reader LEDs/beeper)
- Supervision (detects tampering, cable cut)
- Standardized (vendor interoperability)
- Future-proof

### Clock and Data (C&D) Protocols
**Proprietary Reader Protocols**
- HID proprietary protocols (over RS-485)
- Mercury Security SCP (Secure Communication Protocol)
- ASSA ABLOY Aperio wireless protocol
- Salto wireless protocol
- Allegion NDE wireless protocol

**Features**
- Encrypted communication
- Wireless credential support
- Mobile credential data transfer
- Biometric template transmission
- Diagnostics and health monitoring

## Video Surveillance Protocols

### ONVIF (Open Network Video Interface Forum)
**ONVIF Overview**
- Open industry standard for IP video products
- Founded by Axis, Bosch, and Sony (2008)
- Ensures interoperability between IP cameras and VMS
- Profiles define specific functionalities

**ONVIF Profiles**
- **Profile S**: Streaming (video, audio, metadata)
- **Profile G**: Edge storage (SD card recording)
- **Profile C**: Access control (door control integration)
- **Profile Q**: Device discovery, configuration, and management
- **Profile T**: Advanced video streaming (H.265, metadata)
- **Profile A**: Access control systems
- **Profile D**: Door control (readers, locks, REX)
- **Profile M**: Metadata and analytics

**ONVIF Features**
- Device discovery (WS-Discovery)
- Media streaming (RTSP)
- PTZ control
- Event handling (analytics, motion detection)
- Configuration management
- User authentication
- Metadata streaming

**ONVIF Conformance**
- ONVIF Conformant (self-declared)
- ONVIF Certified (third-party tested)

### RTSP (Real-Time Streaming Protocol)
**RTSP Overview**
- IETF RFC 2326 standard
- Used for streaming video from IP cameras
- Client-server protocol (VMS client requests stream from camera)
- Control protocol (not transport protocol)

**RTSP Commands**
- DESCRIBE (get media description)
- SETUP (transport setup)
- PLAY (start streaming)
- PAUSE (pause streaming)
- TEARDOWN (stop streaming and release resources)

**Transport Protocols**
- **RTP/RTCP** (Real-time Transport Protocol): Actual media streaming
- **UDP**: Low latency, possible packet loss
- **TCP**: Reliable, higher latency
- **Multicast**: One-to-many streaming

### HTTP/HTTPS for Video Streaming
**MJPEG (Motion JPEG) over HTTP**
- Series of JPEG images
- High bandwidth consumption
- Easy to implement
- No specialized codecs required

**HLS (HTTP Live Streaming)**
- Apple developed
- Adaptive bitrate streaming
- Works through firewalls (HTTP/HTTPS)
- Latency (6-30 seconds)

**MPEG-DASH (Dynamic Adaptive Streaming over HTTP)**
- ISO standard (ISO/IEC 23009-1)
- Adaptive bitrate streaming
- Codec-agnostic

## Fire Alarm Protocols

### Fire Alarm Communication Protocols
**Proprietary Addressable Protocols**
- Simplex IDNet, 4-wire multiplex
- Notifier FlashScan (proprietary)
- Edwards Signature Loop (proprietary)
- Fire-Lite SLC (Signaling Line Circuit)
- Hochiki ESP (Enhanced Systems Protocol)

**Standard Protocols**
- Modbus (monitoring and control)
- BACnet (integration with BAS)
- SNMP (network monitoring)
- Email and SMS notifications
- XML/SOAP web services

**Digital Alarm Communicator**
- DACT (Digital Alarm Communicator Transmitter)
- Contact ID (Ademco Contact ID, SIA DC-03)
- SIA (Security Industry Association) protocols
- Cellular communication (LTE, 4G)
- IP-based reporting (to central station)

### Fire Alarm Supervision
**End-of-Line Resistor (EOLR)**
- Verifies circuit integrity
- Detects opens and shorts
- Typical values: 4.7kΩ, 10kΩ
- Used in conventional fire alarm systems

**Addressable Loop Polling**
- Controller polls each device periodically
- Device reports status (normal, alarm, trouble, supervisory)
- Loop voltage and current monitoring
- Detects device removal, wiring faults

## Network and Cybersecurity Protocols

### Network Security Protocols
**TLS/SSL (Transport Layer Security)**
- Encrypts web traffic (HTTPS)
- TLS 1.2 (minimum recommended)
- TLS 1.3 (latest standard, faster, more secure)
- Certificate-based authentication

**IPsec (Internet Protocol Security)**
- Network layer encryption
- VPN (Virtual Private Network) tunneling
- Authentication Header (AH)
- Encapsulating Security Payload (ESP)
- IKE (Internet Key Exchange) for key management

**SSH (Secure Shell)**
- Secure remote login and command execution
- Replaces Telnet (insecure)
- Public key authentication
- Port forwarding and tunneling

**SNMP (Simple Network Management Protocol)**
- SNMPv1 (legacy, unencrypted)
- SNMPv2c (community strings, unencrypted)
- SNMPv3 (authentication and encryption, recommended)
- Network device monitoring
- Trap notifications

### Authentication Protocols
**802.1X (Port-Based Network Access Control)**
- IEEE standard for network authentication
- EAP (Extensible Authentication Protocol)
- RADIUS (Remote Authentication Dial-In User Service) backend
- Certificates or username/password authentication
- Prevents unauthorized network access

**RADIUS (Remote Authentication Dial-In User Service)**
- Centralized authentication server
- AAA (Authentication, Authorization, Accounting)
- Used for VPN, wireless, and network access
- Challenge-response authentication

**LDAP (Lightweight Directory Access Protocol)**
- Directory services (Active Directory, OpenLDAP)
- User and group management
- Centralized authentication
- LDAPS (LDAP over SSL/TLS) for secure communication

**SAML (Security Assertion Markup Language)**
- Single Sign-On (SSO) standard
- XML-based authentication
- Identity provider (IdP) and service provider (SP)
- Web-based authentication

**OAuth 2.0 / OpenID Connect**
- Authorization framework
- Delegated access (third-party app access)
- Token-based authentication
- Used for cloud services and mobile apps

### Industrial Control System (ICS) Protocols
**Modbus (see Building Automation section)**
**DNP3 (Distributed Network Protocol 3)**
- Used in SCADA and utility applications
- Electric power, water, wastewater
- Secure DNP3 (Secure Authentication v5)

**IEC 61850**
- Substation automation standard
- Communication in electrical substations
- GOOSE (Generic Object Oriented Substation Event) messaging

**BACnet (see Building Automation section)**

## Wireless Communication Protocols

### Short-Range Wireless
**Bluetooth Low Energy (BLE)**
- Low power consumption
- Mobile access control credentials
- Beacon technology (proximity detection)
- Range: 10-100 meters

**NFC (Near Field Communication)**
- Very short range (< 4 inches)
- ISO/IEC 14443 (contactless smart cards)
- Mobile payments and access control
- Tap-to-connect pairing

**Zigbee**
- IEEE 802.15.4 standard
- Low power, mesh networking
- Building automation sensors
- Range: 10-100 meters
- Frequency: 2.4 GHz (global), 915 MHz (Americas), 868 MHz (Europe)

**Z-Wave**
- Low power mesh networking
- Home and building automation
- Frequency: 908 MHz (US), 868 MHz (Europe)
- Range: 30 meters (per hop)

### Long-Range Wireless
**LoRaWAN (Long Range Wide Area Network)**
- Long-range, low-power communication
- Range: 2-15 km (urban), 15+ km (rural)
- Low data rate
- IoT sensor networks
- Unlicensed ISM bands

**Cellular (LTE, 5G)**
- Wide area connectivity
- 4G LTE, 5G NR
- Alarm communication (fire, intrusion)
- Remote monitoring and control
- Backup communication path

**Wi-Fi (IEEE 802.11)**
- 802.11n (2.4 GHz, 5 GHz, up to 600 Mbps)
- 802.11ac (5 GHz, up to 3.5 Gbps)
- 802.11ax (Wi-Fi 6, 2.4/5/6 GHz, up to 9.6 Gbps)
- WPA3 encryption (latest security standard)
- Enterprise authentication (802.1X)

## Data Formats and Information Models

### JSON (JavaScript Object Notation)
- Lightweight data interchange format
- Human-readable text
- RESTful API communication
- Configuration files
- IoT data exchange

### XML (Extensible Markup Language)
- Structured data format
- SOAP web services
- Configuration files (BACnet/WS, ONVIF)
- Data exchange between systems

### CSV (Comma-Separated Values)
- Tabular data export
- Energy data, alarm logs
- Import/export for spreadsheets and databases

### MQTT (Message Queuing Telemetry Transport)
- Lightweight publish-subscribe messaging
- IoT communication protocol
- Low bandwidth, low power
- Topics and message brokers
- QoS (Quality of Service) levels

### CoAP (Constrained Application Protocol)
- RESTful protocol for IoT
- UDP-based (low overhead)
- Designed for constrained devices
- Observe (push notifications)

## Standards and Compliance

### Industry Standards
**NFPA (National Fire Protection Association)**
- NFPA 70 (National Electrical Code - NEC)
- NFPA 72 (National Fire Alarm and Signaling Code)
- NFPA 101 (Life Safety Code)
- NFPA 110 (Emergency and Standby Power Systems)
- NFPA 13 (Installation of Sprinkler Systems)
- NFPA 25 (Inspection, Testing, and Maintenance of Water-Based Fire Protection Systems)

**ASHRAE (American Society of Heating, Refrigerating and Air-Conditioning Engineers)**
- ASHRAE 90.1 (Energy Standard for Buildings)
- ASHRAE 62.1 (Ventilation for Acceptable Indoor Air Quality)
- ASHRAE 135 (BACnet)
- ASHRAE 55 (Thermal Environmental Conditions for Human Occupancy)
- ASHRAE 189.1 (Standard for the Design of High-Performance Green Buildings)

**UL (Underwriters Laboratories)**
- UL 294 (Access Control System Units)
- UL 681 (Installation and Classification of Burglar and Hold-up Alarm Systems)
- UL 864 (Control Units and Accessories for Fire Alarm Systems)
- UL 916 (Energy Management Equipment)
- UL 1076 (Proprietary Burglar Alarm Units and Systems)
- UL 2050 (National Industrial Security and Supervision Standards)

**IEEE (Institute of Electrical and Electronics Engineers)**
- IEEE 802.3 (Ethernet)
- IEEE 802.11 (Wi-Fi)
- IEEE 802.1X (Port-Based Network Access Control)
- IEEE 1588 (Precision Time Protocol)

**ISO/IEC (International Organization for Standardization)**
- ISO/IEC 11801 (Cabling standards)
- ISO/IEC 14443 (Contactless smart cards - NFC)
- ISO/IEC 15693 (Vicinity cards)
- ISO 16484 (Building Automation and Control Systems)
- ISO/IEC 27001 (Information Security Management)

**ANSI (American National Standards Institute)**
- ANSI/BHMA (Builders Hardware Manufacturers Association)
  - Grade 1 (heavy-duty commercial)
  - Grade 2 (medium-duty commercial)
  - Grade 3 (residential)
- ANSI/TIA (Telecommunications Industry Association)
  - TIA-568 (Commercial Building Cabling)
  - TIA-569 (Pathways and Spaces)
  - TIA-606 (Administration Standard for Telecommunications Infrastructure)
  - TIA-607 (Grounding and Bonding)

### Federal Standards and Guidelines
**NIST (National Institute of Standards and Technology)**
- NIST Cybersecurity Framework
- NIST SP 800-53 (Security and Privacy Controls)
- NIST SP 800-171 (Protecting Controlled Unclassified Information)
- NIST FIPS 140-2/140-3 (Cryptographic Module Validation)
- NIST FIPS 201 (Personal Identity Verification - PIV)
- NIST SP 800-82 (Guide to ICS Security)

**FISMA (Federal Information Security Management Act)**
- Federal agency information security
- Risk-based approach
- NIST SP 800-53 controls implementation
- Annual compliance reporting

**HSPD-12 (Homeland Security Presidential Directive 12)**
- Federal employee identity verification
- PIV cards (FIPS 201 compliant)
- Common Identification Standard

**ISC (Interagency Security Committee)**
- Facility Security Level (FSL) determination
- Risk Management Process for Federal Facilities
- Design-Basis Threat Report
- Physical security standards for federal facilities

**GSA (General Services Administration)**
- P100 Facilities Standards (Physical Security)
- PBS (Public Buildings Service) standards
- Facility security design criteria

**DoD (Department of Defense)**
- UFC (Unified Facilities Criteria)
  - UFC 4-010-01 (DoD Minimum Antiterrorism Standards for Buildings)
  - UFC 4-020-01 (Security Engineering)
  - UFC 3-600-01 (Fire Protection Engineering for Facilities)
- DIACAP/RMF (DoD Information Assurance Certification and Accreditation Process / Risk Management Framework)
- JAFAN (Joint Air Force-Army-Navy) standards (physical security)

**NERC CIP (North American Electric Reliability Corporation - Critical Infrastructure Protection)**
- CIP-002 through CIP-014
- Bulk Electric System cybersecurity
- Critical Cyber Assets protection
- Physical security of critical facilities

### International Standards
**IEC (International Electrotechnical Commission)**
- IEC 60364 (Electrical Installations of Buildings)
- IEC 60839 (Alarm and Electronic Security Systems)
- IEC 62305 (Protection Against Lightning)
- IEC 62443 (Industrial Automation and Control Systems Security)
- IEC 61850 (Substation Automation)

**EN (European Norm)**
- EN 50131 (Intrusion and Hold-up Alarm Systems)
- EN 50133 (Access Control Systems)
- EN 50134 (Alarm Transmission Systems)
- EN 54 (Fire Detection and Alarm Systems)
- EN 50090 (Home and Building Electronic Systems - HBES)

**ISO Standards**
- ISO 7240 (Fire Detection and Alarm Systems)
- ISO 9001 (Quality Management)
- ISO 14001 (Environmental Management)
- ISO 45001 (Occupational Health and Safety)
- ISO 50001 (Energy Management)

### Green Building and Sustainability Standards
**LEED (Leadership in Energy and Environmental Design)**
- LEED BD+C (Building Design and Construction)
- LEED O+M (Operations and Maintenance)
- Energy and atmosphere credits
- Indoor environmental quality credits
- Innovation in design

**ENERGY STAR**
- EPA energy efficiency program
- Building energy performance rating (1-100)
- Portfolio Manager (benchmarking tool)
- Certification for top 25% energy performers

**Green Globes**
- Alternative to LEED
- Online assessment and rating system
- Energy, water, indoor environment, site, materials

**WELL Building Standard**
- Focus on human health and wellness
- Air, water, nourishment, light, fitness, comfort, mind
- WELL certification (Silver, Gold, Platinum)

**Living Building Challenge**
- Most rigorous green building standard
- Net zero energy, water, waste
- Regenerative design
- Petals: Place, Water, Energy, Health & Happiness, Materials, Equity, Beauty

### Accessibility Standards
**ADA (Americans with Disabilities Act)**
- ADA Standards for Accessible Design (2010)
- Accessible routes and entrances
- Door hardware and operation
- Signage and wayfinding
- Toilet and bathing facilities
- Communication systems (visual alarms, TTY)

**ICC/ANSI A117.1**
- Accessible and Usable Buildings and Facilities
- Referenced by building codes
- Technical specifications for accessibility

### Testing and Certification
**UL Listing**
- Product safety certification
- Tested to UL standards
- Ongoing factory inspections
- UL mark on certified products

**FM Approvals (Factory Mutual)**
- Property loss prevention certification
- Fire protection equipment
- Burglar alarm systems
- Building materials

**ETL Listed (Intertek)**
- Product safety testing and certification
- Alternative to UL
- OSHA-recognized NRTL (Nationally Recognized Testing Laboratory)

**CE Marking (European Conformity)**
- Indicates compliance with EU directives
- Required for products sold in European Economic Area
- Health, safety, environmental protection

**FCC (Federal Communications Commission)**
- FCC Part 15 (RF devices, unintentional radiators)
- FCC Part 68 (Telecommunications equipment)
- EMI/RFI compliance

**BTL (BACnet Testing Laboratories)**
- BACnet device interoperability testing
- BTL listing ensures BACnet conformance
- Maintains listed products database

**LonMark International**
- LonWorks device certification
- Interoperability testing
- LonMark certified products

**ONVIF Conformance**
- IP video device interoperability
- Profile compliance testing
- ONVIF conformant or certified products
