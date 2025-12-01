# Dams Sector - Communication Protocols & Standards

**Document Version:** 1.0
**Classification:** Technical Standards
**Last Updated:** 2025-11-05
**Standards Bodies:** IEC, IEEE, NIST, FERC

## Executive Summary

Dam control and monitoring systems rely on specialized industrial communication protocols for SCADA, protection, and automation. This document details protocol specifications, security considerations, and implementation guidelines for the protocols commonly deployed in the dams sector.

---

## 1. SCADA Communication Protocols (80+ Patterns)

### 1.1 DNP3 (Distributed Network Protocol)

**DNP3-001: Protocol Overview**
```
PROTOCOL SPECIFICATIONS:
Standard: IEEE 1815-2012
Application: SCADA master-to-RTU/IED communication
Architecture: Three-layer (Application, Transport, Data Link)
Data Types: Binary inputs/outputs, analog inputs/outputs, counters
History: Developed by Westronic (now Triangle MicroWorks) in 1990
Adoption: Dominant in North American electric utilities and dams

PROTOCOL LAYERS:
Application Layer:
- Object model: Points organized by groups and variations
- Functions: Read, write, freeze, select/operate
- Unsolicited responses: Event-driven reporting
- Time synchronization: Precise timestamping

Transport Layer:
- Segmentation: Messages split into 249-byte chunks
- Reassembly: Sequence numbers for ordering
- Flow control: Window-based

Data Link Layer:
- Frame structure: Start bytes, length, CRC
- Addressing: 16-bit source and destination
- Confirmation: Acknowledgment required

COMMON OBJECT GROUPS:
- Group 1: Binary Input (status points)
- Group 2: Binary Input Change (events)
- Group 10: Binary Output (control points)
- Group 20: Binary Counter
- Group 30: Analog Input (measurements)
- Group 40: Analog Output (setpoints)
- Group 50: Time and Date
```

**DNP3-002: DNP3 Serial (RS-485)**
```
PHYSICAL LAYER:
- Media: RS-485 two-wire or four-wire
- Speed: 9600, 19200, 38400 bps typical
- Distance: Up to 4000 feet without repeaters
- Topology: Multidrop bus, up to 255 devices
- Wiring: Shielded twisted pair (STP), 120-ohm termination

CONFIGURATION:
- Master address: Typically 0 or 1
- Outstation addresses: 1-254
- Baud rate: Match all devices on segment
- Data bits: 8, Stop bits: 1, Parity: None (8N1 typical)

APPLICATIONS:
- RTU to SCADA master communication
- Remote monitoring sites
- Legacy installations (pre-2000s)

ADVANTAGES:
- Long distance capability
- Deterministic timing
- Low infrastructure cost

LIMITATIONS:
- Slow data rates
- Single point of failure on bus
- Susceptible to electrical interference
```

**DNP3-003: DNP3 over TCP/IP**
```
NETWORK LAYER:
- Transport: TCP (reliable) or UDP (faster, less reliable)
- Port: TCP/UDP 20000 (standard)
- IP addressing: Static recommended for SCADA devices
- MTU: 1500 bytes (Ethernet standard)

ADVANTAGES OVER SERIAL:
- Higher bandwidth: 10 Mbps - 1 Gbps
- Ethernet infrastructure: Standard switches, routers
- Multi-path: Redundant network paths
- Scalability: 1000s of devices

TYPICAL CONFIGURATION:
Master to Outstation:
- Connection: TCP client (master) to TCP server (outstation)
- Keep-alive: Periodic link status requests
- Timeout: 30-60 seconds for dead connection detection

ROUTING:
- Subnets: Segregate SCADA traffic from enterprise
- VLANs: Virtual segmentation
- QoS: Prioritize SCADA traffic over non-critical
- Firewall rules: Permit only required ports

SECURITY CONSIDERATIONS:
- No encryption: DNP3 TCP/IP not encrypted by default
- VPN tunnels: IPsec for WAN links
- Firewall: Permit only required source/destination IPs
- IDS/IPS: Monitor for anomalous DNP3 traffic
```

**DNP3-004: DNP3 Secure Authentication (SA)**
```
STANDARD: IEEE 1815-2012 Secure Authentication
PURPOSE: Cryptographic authentication of DNP3 messages
DEPLOYMENT: Increasing adoption in critical infrastructure

AUTHENTICATION PROCESS:
1. Session key establishment: Challenge-response
2. HMAC calculation: Message authentication code
3. Critical message authentication: Control commands, time sync
4. Non-critical messages: Optionally authenticated

KEY MANAGEMENT:
- Update keys: Master and outstation hold symmetric keys
- Key change: Periodic (annually recommended)
- Key storage: Secure, non-volatile memory
- Key distribution: Out-of-band (manual or secure protocol)

AUTHENTICATION MODES:
- Aggressive mode: Challenge every message
- Non-aggressive mode: Challenge periodically (every N messages)
- Critical functions only: Control commands authenticated

ADVANTAGES:
- Prevents command spoofing
- Detects unauthorized access
- Replay attack prevention

LIMITATIONS:
- Performance overhead: 10-20% CPU increase
- Complexity: Configuration and key management
- Limited adoption: Not all devices support SA

IMPLEMENTATION EXAMPLE:
- Challenge frequency: Every 10 messages
- HMAC algorithm: SHA-256
- Key length: 128-bit or 256-bit
- Key change interval: 12 months
```

### 1.2 Modbus Protocol

**MODBUS-001: Modbus RTU (Serial)**
```
PROTOCOL OVERVIEW:
Standard: Modbus.org specification
Application: PLC-to-device, SCADA-to-RTU
Architecture: Master-slave, request-response
History: Developed by Modicon (now Schneider Electric) in 1979

PHYSICAL LAYER:
- Media: RS-485 or RS-232
- Speed: 9600, 19200, 38400 bps (RS-485), up to 115200 bps
- Frame: 8N1 (8 data bits, no parity, 1 stop bit) typical
- Addressing: 1-247 slave addresses

MESSAGE STRUCTURE:
- Slave address: 1 byte (1-247)
- Function code: 1 byte (01-127)
- Data: Variable length
- CRC: 2 bytes (error detection)
- Silence: 3.5 character times between messages

COMMON FUNCTION CODES:
- 01: Read Coil Status (discrete outputs)
- 02: Read Input Status (discrete inputs)
- 03: Read Holding Registers (analog values, setpoints)
- 04: Read Input Registers (analog measurements)
- 05: Force Single Coil (write discrete output)
- 06: Preset Single Register (write analog value)
- 15: Force Multiple Coils
- 16: Preset Multiple Registers

APPLICATIONS:
- PLC to VFDs, sensors, meters
- Legacy SCADA systems
- Simple serial device integration

ADVANTAGES:
- Simple protocol: Easy to implement
- Widely supported: Nearly universal in industrial devices
- Deterministic: Predictable response times

LIMITATIONS:
- No security: No encryption or authentication
- Limited address space: 247 devices maximum
- No timestamps: No native time synchronization
- Master-slave only: No peer-to-peer
```

**MODBUS-002: Modbus TCP**
```
PROTOCOL OVERVIEW:
Standard: Modbus.org Modbus Messaging on TCP/IP
Application: Ethernet-based SCADA and automation
Architecture: Client-server (client=master, server=slave)
Port: TCP 502 (standard)

MESSAGE STRUCTURE:
- MBAP Header: Transaction ID, Protocol ID, Length, Unit ID (7 bytes)
- Function Code: 1 byte
- Data: Variable length

MBAP HEADER:
- Transaction Identifier: 2 bytes (request/response matching)
- Protocol Identifier: 2 bytes (always 0 for Modbus)
- Length: 2 bytes (remaining bytes in message)
- Unit Identifier: 1 byte (slave address, for serial gateway)

ADVANTAGES OVER MODBUS RTU:
- Higher speed: 100 Mbps - 1 Gbps vs. 115 kbps
- Ethernet infrastructure: Standard IT networking
- Simultaneous connections: Multiple clients to single server
- Error detection: TCP checksums in addition to Modbus CRC

TYPICAL DEPLOYMENT:
PLC to Field Devices:
- Ethernet I/O modules
- Variable frequency drives
- Power meters
- Building automation equipment

SCADA Integration:
- HMI to PLC communication
- SCADA master to PLCs and RTUs
- Engineering workstation to devices

SECURITY CONSIDERATIONS:
- No native security: Like Modbus RTU, no encryption/authentication
- Network segmentation: Isolate Modbus devices on OT VLAN
- Firewall rules: Restrict access to port 502
- VPN: Encrypt Modbus TCP over WAN links
```

**MODBUS-003: Modbus Security Extensions**
```
MODBUS/TLS:
Description: Modbus TCP wrapped in TLS (Transport Layer Security)
Port: TCP 802 (assigned by IANA)
Encryption: TLS 1.2 or higher
Authentication: X.509 certificates

IMPLEMENTATION:
- Server certificate: Modbus server presents certificate
- Client validation: Client verifies server identity
- Mutual authentication: Optional client certificate
- Cipher suites: AES-128/256 recommended

ADVANTAGES:
- Encryption: Protects data in transit
- Authentication: Verifies device identity
- Integrity: Detects tampering

LIMITATIONS:
- Limited support: Few devices support Modbus/TLS natively
- Performance: Encryption overhead (~10-20%)
- Certificate management: PKI infrastructure required

ALTERNATIVE: VPN Tunnels
- IPsec or SSL VPN: Tunnel all Modbus traffic
- Transparent: No device configuration changes
- Widely supported: Standard VPN gateways
```

### 1.3 IEC 61850 (Substation Automation)

**IEC61850-001: Protocol Overview**
```
STANDARD: IEC 61850 (International Electrotechnical Commission)
APPLICATION: Substation automation, distributed energy resources
ADOPTION: Modern standard for protection and control
ARCHITECTURE: Object-oriented, service-based

IEC 61850 PARTS:
- Part 6: Configuration language (SCL - Substation Configuration Language)
- Part 7: Communication structure (logical nodes, data objects)
- Part 8-1: MMS (Manufacturing Message Specification) - client/server
- Part 9-2: Sampled values (SV) - real-time current/voltage data
- Part 10: Conformance testing

COMMUNICATION SERVICES:
MMS (Client-Server):
- Port: TCP 102
- Purpose: Control, monitoring, configuration
- Latency: 10-100ms typical
- Applications: SCADA integration, HMI, engineering access

GOOSE (Generic Object-Oriented Substation Event):
- Layer: Layer 2 Ethernet (no IP)
- Purpose: Peer-to-peer trip signals, interlocking
- Latency: <4ms (Class P4), <10ms (Class P5)
- Applications: Protection relay coordination, breaker control

Sampled Values (SV):
- Layer: Layer 2 Ethernet
- Purpose: Real-time current and voltage samples
- Sample rate: 80 samples/cycle (4800 Hz for 60 Hz systems)
- Applications: Non-conventional instrument transformers, process bus

LOGICAL NODES (Common Examples):
- XCBR: Circuit breaker
- MMXU: Measurement unit (3-phase)
- PTRC: Protection relay control
- GGIO: Generic I/O
- PDIS: Distance protection
- PTOF: Overfrequency protection
```

**IEC61850-002: Substation Configuration Language (SCL)**
```
SCL FILES (XML-based configuration):
SCD (Substation Configuration Description):
- Complete substation: All IEDs, communication, signals
- Purpose: System integrator creates full design
- Contents: IED capabilities, dataflow, logical nodes

ICD (IED Capability Description):
- Single IED: Exported from relay configuration tool
- Purpose: Import into system configuration tool
- Contents: Logical nodes, data objects, services

CID (Configured IED Description):
- Configured IED: Specific to installation
- Purpose: Import to IED for commissioning
- Contents: IP addresses, GOOSE subscriptions, report settings

CONFIGURATION WORKFLOW:
1. Vendor provides ICD files for each IED
2. System engineer imports ICDs into SCL tool (e.g., OpenSCD)
3. Engineer configures communication (GOOSE, SV, MMS)
4. Tool generates CID files for each IED
5. CIDs imported to IEDs for final configuration

SCL ADVANTAGES:
- Interoperability: Vendor-neutral configuration
- Documentation: Self-documenting system
- Version control: Track configuration changes
```

**IEC61850-003: GOOSE Messaging**
```
GOOSE OVERVIEW:
Purpose: Fast peer-to-peer communication
Use case: Protection relay trip signals, interlocking logic
Latency: <4ms for critical signals
Multicast: Single message received by multiple devices

GOOSE MESSAGE STRUCTURE:
- MAC destination: Multicast address (01:0C:CD:01:xx:xx)
- EtherType: 0x88B8 (GOOSE)
- APPID: Application identifier (unique per GOOSE dataset)
- gocbRef: GOOSE Control Block reference
- timeAllowedtoLive: Message validity period (ms)
- datSet: Dataset reference
- Data: Boolean, integer, floating point values

GOOSE PUBLISHING:
Transmission Strategy:
- Event-driven: Send immediately on data change
- Repetition: Retransmit several times after change
- Heartbeat: Periodic transmission even if no change
- Timing: T0 (immediate), T1 (4ms), T2 (8ms), T3 (16ms), then steady (1-60 seconds)

GOOSE SUBSCRIPTION:
- IED subscribes to specific GOOSE by APPID
- Monitors timeAllowedtoLive: Timeout triggers alarm
- Data mapped to internal logic (e.g., trip coil)

APPLICATIONS IN DAMS:
- Generator protection: Trip signals between relays and breakers
- Interlocking: Gate/valve position feedback to turbine control
- Emergency shutdown: Broadcast to all equipment
- Synchronization: Sync check across multiple relays

SECURITY CONSIDERATIONS:
- No encryption: GOOSE is unencrypted Layer 2
- No authentication: No built-in message authentication
- IEC 62351: Security extensions (GOOSE authentication not widely adopted)
- Network isolation: Separate VLAN for GOOSE traffic
- Physical security: Prevent unauthorized Ethernet access
```

### 1.4 OPC UA (Open Platform Communications Unified Architecture)

**OPCUA-001: Protocol Overview**
```
STANDARD: IEC 62541
APPLICATION: Enterprise integration, data historian, cloud connectivity
ADOPTION: Growing rapidly as replacement for OPC Classic

OPC UA FEATURES:
- Platform-independent: Windows, Linux, embedded systems
- Service-oriented: Client-server or pub-sub
- Security: Built-in encryption, authentication, authorization
- Information modeling: Object-oriented data representation
- Scalability: Single device to enterprise-wide

COMMUNICATION MODES:
Client-Server:
- Transport: TCP or HTTPS
- Port: TCP 4840 (default), HTTPS 443
- Use case: HMI, SCADA, engineering tools

Pub-Sub:
- Transport: UDP multicast, MQTT, AMQP
- Use case: High-performance data acquisition
- Deployment: Time-sensitive networking (TSN)

OPC UA SECURITY:
Message Security Modes:
- None: No encryption (not recommended)
- Sign: Message authentication only
- Sign and Encrypt: Full protection (recommended)

Security Policies:
- Basic128Rsa15: Deprecated, weak
- Basic256Sha256: Recommended minimum
- Aes128_Sha256_RsaOaep: Strong security
- Aes256_Sha256_RsaPss: Maximum security

User Authentication:
- Anonymous: No authentication (testing only)
- Username/Password: Basic authentication
- Certificate: X.509 client certificates (recommended)

INFORMATION MODELS:
Base Model:
- Objects, Variables, Methods
- References (hierarchical, non-hierarchical)
- Data types (Boolean, Int, Float, String, DateTime)

Companion Specifications:
- OPC UA for Devices (DI): Device information
- OPC UA for PLCs: PLC variable access
- OPC UA for Machinery: Asset monitoring
- OPC UA FX (Field Exchange): Replacing Profinet, EtherNet/IP
```

**OPCUA-002: OPC UA in Dam Systems**
```
USE CASES:
SCADA Integration:
- OPC UA server in PLC or RTU
- SCADA client connects via OPC UA
- Advantages: Secure, firewall-friendly, IT/OT integration

Historian Integration:
- OSIsoft PI Connector for OPC UA
- Wonderware Historian OPC UA client
- Real-time data collection from field devices

Cloud Connectivity (if permitted):
- Azure IoT Edge: OPC UA data to cloud
- AWS IoT Greengrass: Edge processing
- Encrypted, authenticated connections

IMPLEMENTATION:
PLC Configuration:
1. Enable OPC UA server in PLC
2. Configure security policy (Sign and Encrypt)
3. Generate server certificate
4. Configure user accounts or certificate-based auth
5. Map PLC tags to OPC UA address space

SCADA Configuration:
1. Create OPC UA client connection
2. Trust server certificate
3. Configure client authentication
4. Browse OPC UA address space
5. Subscribe to data items

SECURITY BEST PRACTICES:
- Use Sign and Encrypt mode: Always
- Certificate-based authentication: Preferred over passwords
- PKI infrastructure: Central certificate management
- Network segmentation: OPC UA on OT network only
- Firewall rules: Permit only required clients
- Audit logging: Track all OPC UA connections
```

---

## 2. Protection & Control Protocols (50+ Patterns)

### 2.1 IEEE C37.118 (Synchrophasor)

**C37118-001: Protocol Overview**
```
STANDARD: IEEE C37.118.1 (data) and C37.118.2 (communication)
APPLICATION: Phasor Measurement Units (PMUs), wide-area monitoring
PURPOSE: Synchronized measurements across power system
ADOPTION: Required for large generators (NERC compliance)

PHASOR MEASUREMENTS:
Phasor: Magnitude and phase angle of AC signal
Synchronization: GPS time, 1 microsecond accuracy
Sample rate: 30, 60, or 120 frames per second (Hz)
Measurements: Voltage, current, frequency, rate of change of frequency (ROCOF)

C37.118 MESSAGE TYPES:
- Data frames: Phasor measurements and status
- Configuration frames: PMU configuration, data types
- Header frames: PMU information, station name
- Command frames: Control PMU (start, stop, config)

COMMUNICATION:
- Transport: TCP or UDP
- Port: TCP 4712 (standard) or 4713
- Connection: PMU (server) to PDC (Phasor Data Concentrator, client)

APPLICATIONS:
Wide-Area Monitoring:
- Oscillation detection
- Frequency monitoring
- Voltage stability analysis
- Post-event analysis

Generator Control:
- Synchronization verification
- Out-of-step protection
- Under-frequency load shedding coordination

DATA CONCENTRATORS (PDCs):
- Collect data from multiple PMUs
- Time-align measurements
- Forward to applications (SCADA, EMS, historians)
- Vendors: Schweitzer (SEL-5073), GE, Siemens
```

**C37118-002: Synchrophasors in Hydroelectric Plants**
```
DEPLOYMENT:
PMU Location:
- Generator terminals: Voltage and current phasors
- High-voltage side of GSU transformer
- Transmission line (if applicable)

Integration:
- Embedded in protection relays (e.g., SEL-421, GE D60)
- Standalone PMUs (e.g., SEL-734, GE N60)
- Communication to utility PDC or control center

APPLICATIONS:
Generator Synchronization:
- Precise frequency and phase angle
- Verify sync-check relay operation
- Prevent out-of-phase closure

Islanding Detection:
- Rapid detection of grid separation
- Frequency divergence monitoring
- Coordinated islanded operation

Post-Event Analysis:
- Fault reconstruction
- Disturbance investigation
- Relay coordination review

CYBERSECURITY:
- GPS spoofing: Risk of incorrect timestamps
- Communication encryption: TLS for C37.118 (emerging)
- Network isolation: PMU data on protected network
- Authentication: Verify PMU source
```

### 2.2 IEC 60870-5-101/104

**IEC60870-001: Protocol Overview**
```
STANDARD: IEC 60870-5-101 (serial), IEC 60870-5-104 (TCP/IP)
APPLICATION: SCADA in Europe, international, some US utilities
ADOPTION: Dominant in European utilities, oil/gas, water

IEC 60870-5-101 (Serial):
- Physical layer: RS-485 or RS-232
- Speed: 9600, 19200 bps typical
- Frame: Balanced or unbalanced mode
- Applications: RTU-to-master, legacy systems

IEC 60870-5-104 (TCP/IP):
- Transport: TCP
- Port: 2404 (standard)
- Architecture: Multiple clients to single server
- Applications: Modern SCADA, substation gateways

INFORMATION OBJECTS:
- Single-point information: Boolean status
- Double-point information: Off/on/intermediate/invalid
- Step position information: Tap changer positions
- Measured values: Analog measurements (scaled, normalized, floating point)
- Integrated totals: Energy, counters

CAUSE OF TRANSMISSION:
- Spontaneous: Event-driven report
- Cyclic: Periodic transmission
- Request: Response to interrogation
- Activation: Command acknowledgment

QUALITY DESCRIPTORS:
- Invalid: Data not trustworthy
- Not topical: Outdated data
- Substituted: Manually entered data
- Blocked: Data transmission blocked
```

**IEC60870-002: IEC 104 Security**
```
NATIVE SECURITY:
- No encryption: IEC 104 unencrypted by default
- No authentication: No user authentication
- Vulnerabilities: Eavesdropping, command injection

SECURITY EXTENSIONS (IEC 62351):
IEC 62351-4 (TCP/TLS):
- TLS encryption for IEC 104
- Server authentication: X.509 certificates
- Mutual authentication: Optional client certs
- Deployment: Limited, requires compatible devices

SECURITY WORKAROUNDS:
- VPN tunnels: IPsec for all IEC 104 traffic
- Network segmentation: Dedicated SCADA VLAN
- Firewall rules: Restrict source IPs to port 2404
- IDS monitoring: Anomaly detection for IEC 104
- Jump hosts: Secure access for remote engineers
```

---

## 3. Industrial Network Protocols (40+ Patterns)

### 3.1 EtherNet/IP

**ETHERNET_IP-001: Protocol Overview**
```
STANDARD: ODVA (Open DeviceNet Vendors Association)
APPLICATION: Rockwell Automation ecosystems (Allen-Bradley)
ARCHITECTURE: Common Industrial Protocol (CIP) over Ethernet

COMMUNICATION TYPES:
Explicit Messaging:
- Purpose: Configuration, diagnostics, non-time-critical
- Transport: TCP
- Port: TCP 44818
- Use case: HMI to PLC, engineering workstation to PLC

Implicit Messaging (I/O):
- Purpose: Real-time I/O data exchange
- Transport: UDP
- Port: UDP 2222
- Use case: PLC to distributed I/O, PLC to PLC

REAL-TIME PERFORMANCE:
- CIP Motion: Deterministic motion control (<1ms)
- CIP Safety: Safety-rated communication (SIL 2/3)
- CIP Sync: IEEE 1588 time synchronization

DEVICE PROFILES:
- Generic Device
- AC Drive
- Motion Control
- Process Control
- Safety Devices

APPLICATIONS IN DAMS:
- Allen-Bradley ControlLogix PLC systems
- Distributed I/O (Point I/O, Flex I/O)
- Variable frequency drives (PowerFlex)
- HMI (PanelView Plus, FactoryTalk View)
```

**ETHERNET_IP-002: Network Architecture**
```
TOPOLOGY:
Linear:
- Daisy-chain devices with embedded switches
- Simple wiring, device failure disrupts downstream

Star:
- Central switch, star topology to devices
- Device failure isolated
- Requires more cabling

Device Level Ring (DLR):
- Redundant ring topology
- Failover <10ms on ring break
- Requires DLR-capable devices

NETWORK SIZING:
- RPI (Requested Packet Interval): 2-100ms typical
- I/O connections: 256-1000 per ControlLogix CPU
- Bandwidth: 10 Mbps or 100 Mbps (100 Mbps typical)

SECURITY:
- CIP Security: CIP-specific security (emerging)
- Network segmentation: Separate OT from IT
- Firewall: Permit UDP 2222, TCP 44818 only
- VPN: Encrypt remote access
```

### 3.2 PROFINET

**PROFINET-001: Protocol Overview**
```
STANDARD: PROFIBUS & PROFINET International (PI)
APPLICATION: Siemens ecosystems, European automation
ARCHITECTURE: Real-time Ethernet for automation

PROFINET VARIANTS:
PROFINET IO (Non-Real-Time):
- Latency: 10-100ms
- Use case: HMI, configuration, diagnostics
- Protocol: TCP/IP, HTTP, SNMP

PROFINET RT (Real-Time):
- Latency: 1-10ms
- Use case: Distributed I/O, standard automation
- Protocol: Ethernet Layer 2, prioritized frames

PROFINET IRT (Isochronous Real-Time):
- Latency: <1ms
- Use case: Motion control, high-speed I/O
- Protocol: Scheduled Ethernet, reserved bandwidth

DEVICE CLASSES:
- IO Controller: PLC or control system
- IO Device: Field device (sensor, actuator, I/O module)
- IO Supervisor: Engineering workstation, HMI

APPLICATIONS IN DAMS:
- Siemens S7-1500 PLC systems
- Distributed I/O (ET200SP, ET200M)
- Drives (Sinamics)
- HMI (Simatic HMI Panels, WinCC)
```

**PROFINET-002: Redundancy & Security**
```
MEDIA REDUNDANCY PROTOCOL (MRP):
- Ring topology
- Failover <200ms (PROFINET RT)
- Failover <10ms (PROFINET IRT with fast startup)

PROFINET SECURITY:
- PROFINET Security: Future enhancement (under development)
- Current: No native encryption or authentication
- Workarounds: VPNs, network segmentation, access control

SCALABILITY:
- Devices per subnet: 128-256 typical
- Cycle time: 1ms - 100ms
- Distance: 100m between devices (copper), 10+ km (fiber)
```

---

*Protocol documentation continues with suppliers, equipment, and standards documentation in subsequent files...*
