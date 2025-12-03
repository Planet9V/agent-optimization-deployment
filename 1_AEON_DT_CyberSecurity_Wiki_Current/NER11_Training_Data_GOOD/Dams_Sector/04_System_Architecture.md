# Dams Sector - System Architecture & Infrastructure

**Document Version:** 1.0
**Classification:** Technical Architecture
**Last Updated:** 2025-11-05
**Framework:** ISA/IEC 62443, NIST SP 800-82, IEEE Standards

## Executive Summary

This document details the technical architecture of dam control and monitoring systems, including SCADA infrastructure, control networks, communication systems, and integration architectures. Coverage includes both modern digital systems and legacy infrastructure common in the aging U.S. dam inventory.

---

## 1. SCADA Architecture (90+ Patterns)

### 1.1 Hierarchical Architecture Model

**HAM-001: Three-Layer Architecture**
```
LAYER 1: FIELD DEVICES (Level 0-1)
- Sensors: Level, flow, pressure, temperature, position
- Actuators: Gate motors, valve operators, turbine governors
- Local controllers: PLCs, RTUs
- Protection relays: Generator, transformer protection
- Smart devices: Intelligent electronic devices (IEDs)
- Communication: 4-20mA, Modbus RTU, Profibus, DeviceNet

LAYER 2: CONTROL & SUPERVISION (Level 2)
- SCADA master servers: Primary and backup
- HMI workstations: Operators, engineers
- Historian servers: Process data archiving
- Engineering workstations: Programming, configuration
- Communication: Industrial Ethernet, Modbus TCP, DNP3, IEC 61850
- Services: Alarm management, trending, reporting

LAYER 3: ENTERPRISE (Level 3-4)
- Asset management: Maintenance, work orders
- Business systems: ERP, document management
- Analytics platforms: Performance analysis, optimization
- Reporting: Regulatory compliance, operations
- Communication: Corporate Ethernet, web services
- Security: DMZ, firewalls, VPN servers
```

**HAM-002: Network Segmentation Design**
```
PURDUE MODEL IMPLEMENTATION:

Level 4: Enterprise Network
- Firewall: Stateful inspection, application control
- Services: Email, file servers, business applications
- Access: All corporate users
- Security: Corporate IT standards

Level 3.5: DMZ (Demilitarized Zone)
- Firewall: Dual-homed to Level 4 and Level 3
- Services: Historian replication, web HMI, remote access
- Access: Authenticated users only
- Security: Hardened servers, intrusion detection

Level 3: Manufacturing/Operations Zone
- Firewall: Dedicated OT firewall to Level 2
- Services: Engineering workstations, asset management
- Access: Operations and engineering staff
- Security: Whitelisting, OT-specific security tools

Level 2: Supervisory Control
- Firewall: Industrial firewall to Level 1
- Services: SCADA servers, HMIs, historians
- Access: Control room operators
- Security: Application whitelisting, data diode (optional)

Level 1: Automation Control
- Firewall: None (air-gapped) or industrial firewall
- Services: PLCs, RTUs, protection relays
- Access: Direct from Level 2 only
- Security: Protocol restrictions, unidirectional gateways

Level 0: Process
- Field devices connected to Level 1 controllers
- No IP connectivity
- Analog and serial communications only
```

**HAM-003: Redundancy Architecture**
```
HIGH AVAILABILITY SCADA:
Primary SCADA Server:
- Hot standby: Automatic failover <5 seconds
- Heartbeat monitoring: 1-second intervals
- Data synchronization: Real-time replication
- Location: Primary control room

Backup SCADA Server:
- Identical hardware and software configuration
- Receives all real-time data continuously
- Automatic promotion to primary on failure
- Location: Separate building or remote facility

Disaster Recovery Server:
- Offsite location (50+ miles)
- Updated daily or weekly
- Manual activation process
- Recovery time objective: 4-8 hours

HMI REDUNDANCY:
- Minimum 2 HMI workstations in control room
- Each can connect to primary or backup server
- Independent network connections
- UPS power for continuous operation
```

**HAM-004: Communication Architecture**
```
CONTROL NETWORK (Layer 2-1):
Topology: Redundant ring (IEC 62439-3 HSR or PRP)
Protocol: Industrial Ethernet (EtherNet/IP, Profinet, Modbus TCP)
Speed: 100 Mbps or 1 Gbps
Switches: Managed industrial Ethernet switches
Redundancy: Dual rings, automatic failover <50ms
Security: MAC address filtering, port security

FIELD NETWORK (Layer 1-0):
Topology: Multidrop serial or star Ethernet
Protocols:
- Serial: Modbus RTU, DNP3 serial, Profibus DP
- Ethernet: Modbus TCP, DNP3 TCP, EtherNet/IP
Speed: Serial 9600-115200 bps, Ethernet 10-100 Mbps
Media: RS-485 (serial), Fiber optic or copper (Ethernet)
Distance: RS-485 up to 4000 feet, fiber up to 50 miles

WIDE AREA NETWORK (Multi-site):
Primary: Fiber optic (owned or leased)
Backup: Cellular (4G LTE, 5G)
Tertiary: Satellite (VSAT or low-latency LEO)
VPN: IPsec tunnels for all WAN links
Bandwidth: 10-100 Mbps primary, 5-20 Mbps backup
Latency: <50ms primary, <200ms backup acceptable
```

### 1.2 SCADA Platform Components

**SPC-001: Master Control Servers**
```
TYPICAL PLATFORM:
- Wonderware System Platform (AVEVA)
- Ignition SCADA (Inductive Automation)
- iFIX (GE Digital)
- PcVue SCADA (ARC Informatique)
- ADMS (Advanced Distribution Management System)

SERVER SPECIFICATIONS:
Hardware:
- CPU: Dual Xeon or EPYC, 8-16 cores
- RAM: 32-64 GB ECC
- Storage: RAID 1 or 10, SSD preferred
- Network: Dual 1GbE or 10GbE interfaces
- OS: Windows Server 2019/2022 or Linux (RHEL, Ubuntu)

Software Configuration:
- SCADA engine: Tag database 10,000-50,000 points
- Alarm server: Priority-based, suppression logic
- Trending: Real-time and historical
- Reporting: Automated generation, PDF/Excel export
- Scripting: Python, VBScript, or C# for custom logic

DATABASE:
- Real-time: In-memory database for active tags
- Historical: SQL Server, Oracle, PostgreSQL
- Replication: Primary to backup and DR servers
- Retention: 90 days online, 7 years archived
```

**SPC-002: Human-Machine Interface (HMI)**
```
HMI WORKSTATION SPECS:
- CPU: Intel Core i7 or AMD Ryzen 7
- RAM: 16-32 GB
- Graphics: Dedicated GPU for multiple monitors
- Displays: Dual or triple 27-32 inch monitors
- OS: Windows 10 IoT Enterprise or Windows 11 IoT
- Resolution: 1920x1080 or 2560x1440 per display

HMI SOFTWARE:
- Graphics: High-resolution process graphics
- Navigation: Overview → Detail screens hierarchy
- Alarms: Priority-based display, audio annunciation
- Trending: Real-time and historical trends
- Controls: Operator command entry, authorization

SCREEN HIERARCHY:
Level 1: System Overview
- Single-line diagram of entire dam complex
- Key parameters: Reservoir level, generation, flows
- Active alarm summary
- Navigation buttons to detail screens

Level 2: Subsystem Screens
- Spillway gates: Position, flow, alarms
- Powerhouse: Generator status, MW, MVAr
- Turbines: Speed, flow, efficiency
- Outlet works: Valve positions, flows

Level 3: Equipment Detail
- Individual gate control and status
- Generator detailed parameters and protection
- Turbine governor tuning and setpoints
- Motor control centers

Level 4: Maintenance/Engineering
- Diagnostic screens
- Calibration interfaces
- System configuration
- Trending and analysis tools
```

**SPC-003: Historian Database**
```
HISTORIAN PLATFORMS:
- OSIsoft PI System (market leader in dams sector)
- Wonderware Historian (AVEVA)
- GE Proficy Historian
- Ignition Historian (SQL-based)

DATA COLLECTION:
- Polling rate: 1-10 seconds typical
- Exception reporting: Deadband 0.1-1% of range
- Compression: Swinging door algorithm
- Storage efficiency: 90-95% compression typical

DATA STRUCTURE:
- Tags: 10,000-100,000 per facility
- Attributes: Engineering units, description, limits
- Quality: Good, bad, uncertain flags
- Timestamps: Millisecond resolution

HISTORIAN QUERIES:
- Ad-hoc trending: Any tag, any time range
- Aggregations: Average, min, max, sum
- Calculations: Complex multi-tag calculations
- Exporting: CSV, Excel, database queries

REPLICATION:
- Local site: Hot redundant historian
- Corporate data center: 15-minute replication
- Cloud (if permitted): Encrypted sync daily
- Retention: 3 years local, 7-10 years archived
```

**SPC-004: Engineering Workstations**
```
ENGINEERING WORKSTATION PURPOSE:
- PLC/RTU programming and configuration
- HMI graphics development
- SCADA system configuration
- Network management
- Cybersecurity management

HARDWARE:
- High-performance laptop or desktop
- Multiple vendor programming software licenses
- Serial, Ethernet, USB interfaces for device programming
- Ruggedized laptop for field work
- Isolated from production network (air-gapped or DMZ)

SOFTWARE SUITES:
ABB:
- Control Builder for AC800M PLCs
- Symphony+ Composer for DCS engineering
- PCM600 for protection relay configuration

Siemens:
- TIA Portal for S7-1200/1500 PLCs
- SIMATIC PCS 7 for DCS engineering
- DIGSI for protection relay configuration

Rockwell Automation:
- Studio 5000 for ControlLogix programming
- FactoryTalk View for HMI development
- RSNetWorx for network configuration

GE:
- Mark VIe toolset for turbine controls
- iFIX WorkSpace for HMI development
- Multilin EnerVista for relay configuration

SECURITY MEASURES:
- No email or web browsing
- USB port control and logging
- Application whitelisting
- Antivirus with OT-aware scanning
- Code signing for all PLC uploads
```

### 1.3 Field Device Integration

**FDI-001: Programmable Logic Controllers (PLCs)**
```
PLC APPLICATIONS IN DAMS:
- Spillway gate control: Coordinated gate operation
- Turbine sequencing: Startup, synchronization, shutdown
- Auxiliary systems: Cooling water, drainage pumps
- Fire protection: Detection and suppression
- Access control: Badge readers, interlocks

TYPICAL PLC PLATFORMS:
Siemens S7-1500:
- Applications: Spillway gates, auxiliary systems
- I/O: Distributed I/O via Profinet
- Programming: Ladder logic, function blocks
- Redundancy: H-system (hot standby)

Allen-Bradley ControlLogix:
- Applications: Turbine control, safety systems
- I/O: Distributed I/O via EtherNet/IP
- Programming: Ladder logic, structured text
- Redundancy: Dual processors with hot backup

ABB AC800M:
- Applications: Complex turbine/generator control
- I/O: Profibus DP or Profinet
- Programming: Function blocks, structured text
- Redundancy: Triple modular redundant (TMR) for safety

PLC I/O CONFIGURATION:
Digital Inputs:
- Limit switches: Gate open/closed positions
- Protection relays: Trips and alarms
- Push buttons: Operator start/stop commands
- Level switches: High/low level alarms

Digital Outputs:
- Motor starters: Pump and fan control
- Solenoid valves: Hydraulic and pneumatic control
- Indicator lights: Status indication
- Alarm annunciators: Horn and lights

Analog Inputs:
- 4-20mA: Level, flow, pressure transmitters
- 0-10V: Position feedback from actuators
- Thermocouples/RTDs: Temperature monitoring

Analog Outputs:
- 4-20mA: Valve position commands
- 0-10V: Speed setpoints to drives
```

**FDI-002: Remote Terminal Units (RTUs)**
```
RTU APPLICATIONS:
- Remote monitoring stations
- Unmanned spillway facilities
- Water quality monitoring sites
- Downstream flow measurement
- Weather stations

TYPICAL RTU PLATFORMS:
ABB RTU560:
- I/O: 32-256 points per unit
- Communication: DNP3, IEC 60870-5-101/104, Modbus
- Power: 24-48 VDC, solar panel compatible
- Environmental: -40°C to +70°C operation

Schweitzer Engineering Labs (SEL) RTAC:
- I/O: Modular, expandable
- Communication: DNP3, IEC 61850, Modbus
- Security: Role-based access, encryption
- Integration: Substation automation focus

Emerson/Bristol Babcock ControlWave:
- I/O: 64-512 points
- Communication: DNP3, Modbus, proprietary
- Applications: Flow computers, remote pumping

RTU COMMUNICATION:
Primary: Fiber optic (if available)
- Protocol: DNP3 over TCP/IP
- Speed: 10-100 Mbps
- Latency: <10ms

Backup: Cellular (4G LTE/5G)
- Protocol: DNP3 over TCP/IP, VPN encrypted
- Speed: 1-20 Mbps
- Latency: 50-150ms

Tertiary: Satellite (VSAT)
- Protocol: DNP3, report-by-exception
- Speed: 256 kbps - 2 Mbps
- Latency: 500-700ms (GEO), 20-40ms (LEO)

RTU DATA REPORTING:
- Exception reporting: On significant change
- Periodic reporting: Every 1-15 minutes
- Polled data: On-demand from SCADA master
- Alarms: Immediate unsolicited reports
```

**FDI-003: Intelligent Electronic Devices (IEDs)**
```
PROTECTION RELAYS:
Generator Protection (SEL-700G, GE Multilin 369):
- Functions: Over/under voltage, over/under frequency
- Loss of excitation, reverse power
- Differential protection, ground fault
- Communication: Modbus TCP, DNP3, IEC 61850
- Integration: Direct to SCADA or via gateway

Transformer Protection (SEL-487E, ABB RET615):
- Functions: Differential, overcurrent, overload
- Sudden pressure, temperature monitoring
- Buchholz relay integration
- Communication: IEC 61850 GOOSE for trip signals

Feeder Protection (SEL-751, Siemens 7SJ80):
- Functions: Overcurrent, directional, distance
- Reclosing, sync check
- Fault location
- Communication: DNP3, IEC 61850

POWER QUALITY METERS:
Schweitzer SEL-734 or GE PM880:
- Measurements: Voltage, current, power, energy
- Power quality: Harmonics, flicker, sags/swells
- Waveform capture: High-speed transient recording
- Communication: Modbus TCP, DNP3, IEC 61850
- Applications: Revenue metering, analysis

MOTOR PROTECTION & CONTROL:
ABB ACS880 or Siemens Sinamics G120:
- Variable frequency drives (VFDs) for pumps, fans
- Motor protection: Overload, phase loss, ground fault
- Communication: Profinet, EtherNet/IP, Modbus TCP
- Integration: Direct PLC control and monitoring
```

---

## 2. Control Systems (70+ Patterns)

### 2.1 Turbine-Governor Control

**TGC-001: Governor System Architecture**
```
GOVERNOR TYPES:
Mechanical-Hydraulic:
- Components: Flyball governor, servo motors, oil sump
- Control: Speed droop, dashpot for stability
- Accuracy: ±0.5% of rated speed
- Applications: Small hydro <10 MW, legacy units

Electro-Hydraulic:
- Components: Electronic controller, servo valves, actuators
- Control: PID loops, digital control
- Accuracy: ±0.1% of rated speed
- Applications: Modern units 10-500 MW
- Vendors: Andritz, Voith, Alstom, GE

Digital/Turbine Control System (TCS):
- Components: Redundant PLCs, HMI, servo controllers
- Control: Advanced algorithms, model-based control
- Accuracy: ±0.01% of rated speed
- Applications: Large units >100 MW, pumped storage
- Vendors: ABB, Woodward, TMEIC

GOVERNOR CONTROL MODES:
Speed Control (Isolated Operation):
- Maintains constant turbine speed
- Responds to load changes
- Droop setting: 4-6% typical

Load Control (Grid-Connected):
- Maintains target MW output
- Grid frequency control via AGC signals
- Ramping rates: 1-10 MW/minute

Power Factor Control:
- Coordinated with excitation system
- Maintains target MVAr output
- Often integrated with voltage control

Opening Control:
- Direct wicket gate position command
- Used for testing or manual operation
- Bypasses normal control loops
```

**TGC-002: Wicket Gate Control System**
```
GATE POSITIONING MECHANISM:
Servomotor:
- Type: Hydraulic cylinder or electric motor
- Stroke: Full travel in 30-120 seconds typical
- Force: 50,000 - 500,000 lbf depending on size
- Position feedback: Dual LVDTs or encoders

Distribution Ring:
- Connects servomotor to individual gate linkages
- Converts linear motion to rotary gate motion
- Synchronizes all gates (12-32 gates typical)

Gate Linkage:
- Connects distribution ring to individual wicket gate
- Adjustable for gate position calibration
- Worn linkages cause gate positioning errors

CONTROL LOGIC:
PID Controller:
- Proportional: Fast response to errors
- Integral: Eliminates steady-state error
- Derivative: Damping for stability
- Tuning: Site-specific based on unit characteristics

Rate Limiting:
- Opening rate: Prevents water hammer, pressure surge
- Closing rate: Prevents turbine overspeed
- Typical: 5-10% gate travel per second

Position Feedback:
- Dual sensors: Voting or averaging
- Failsafe: Stop on disagreement >1%
- Calibration: Annual or after maintenance
```

**TGC-003: Excitation System Control**
```
EXCITATION SYSTEM TYPES:
Static Excitation:
- Power source: Generator terminals via transformer
- Control: Thyristor bridge rectifier
- Response: Fast (0.1-0.5 seconds to 95% ceiling)
- Applications: Large modern generators
- Vendors: ABB UNITROL, Basler DECS, GE EX2100

Brushless Excitation:
- Power source: Pilot exciter on generator shaft
- Control: Rotating diodes, stationary thyristors
- Response: Moderate (0.5-1.0 seconds)
- Applications: Mid-size generators
- Maintenance: No brushes to replace

DC Excitation (Legacy):
- Power source: Separate DC generator (exciter)
- Control: Rheostat or SCR-controlled field
- Response: Slow (1-3 seconds)
- Applications: Legacy units, <20 MW
- Maintenance: Brush replacement required

AUTOMATIC VOLTAGE REGULATOR (AVR):
Voltage Control Mode:
- Setpoint: Generator terminal voltage (13.8 kV typical)
- Deadband: ±0.5% of setpoint
- Droop: 3-5% for parallel operation

Power Factor Control Mode:
- Setpoint: Lagging or leading power factor (0.90-0.95)
- Coordination: With turbine governor for MW control
- Applications: System voltage support

Reactive Power Control Mode:
- Setpoint: MVAr output
- Applications: Direct VAR control from system operator

LIMITING FUNCTIONS:
Over-excitation Limiter (OEL):
- Prevents generator overheating
- Time-inverse characteristic
- Coordination with protection relays

Under-excitation Limiter (UEL):
- Prevents loss of synchronism
- Minimum excitation at given MW load
- Stability margin maintained

Volts/Hertz Limiter:
- Prevents core saturation
- Protects during startup or overspeed
- Typical limit: 1.05 per unit V/Hz
```

### 2.2 Spillway Gate Control

**SGC-001: Gate Control System Architecture**
```
CONTROL COMPONENTS:
Local Control Panel (at each gate):
- Manual controls: Raise/lower/stop buttons
- Position indication: Digital readout, dial gauge
- Limit switches: Full open, full closed
- Emergency stop: Kills power to gate motor
- Selector switch: Local / Remote / Off

Central Control System:
- SCADA integration: Remote monitoring and control
- Coordinated control: Multiple gates simultaneously
- Automated sequences: Flood release protocols
- Interlocks: Prevent unsafe operations
- Data logging: Position, operation history

Gate Position Control:
- Setpoint: Desired gate opening (feet or %)
- Feedback: Position sensor (LVDT, encoder, potentiometer)
- Control: On/off or variable speed drive
- Accuracy: ±0.5 inches typical for large gates

GATE ACTUATOR TYPES:
Hydraulic Cylinder:
- Force: 100,000 - 2,000,000 lbf
- Speed: 1-3 feet per minute typical
- Stroke: 10-50 feet depending on gate size
- Control: Servo valve for proportional control
- Power: Hydraulic power unit (diesel or electric)

Electric Motor (Hoist):
- Power: 50-500 HP depending on gate size
- Speed: 1-5 feet per minute
- Mechanism: Wire rope or chain hoist
- Control: VFD for variable speed
- Redundancy: Dual motors on large gates

Rack and Pinion:
- Power: Electric or hydraulic motor
- Speed: 2-6 feet per minute
- Advantages: Positive positioning, no cables
- Applications: Medium-sized gates
```

**SGC-002: Coordinated Gate Control**
```
MULTI-GATE SEQUENCING:
Flood Release Sequence:
1. Verify downstream warnings issued
2. Open Gate 1 to 50%
3. Wait 5 minutes (allow flow to stabilize)
4. Open Gate 2 to 50%
5. Continue sequence for remaining gates
6. Monitor downstream levels continuously
7. Adjust gates to achieve target total flow

Equal Distribution:
- All gates positioned identically
- Prevents uneven loading on structure
- Typical for normal operations

Weighted Distribution:
- Gates opened proportionally to capacity
- Accounts for variations in gate condition
- Used when gates have different ratings

One-at-a-Time:
- Single gate operated at a time
- Prevents simultaneous hydraulic transients
- Required by some operational procedures

INTERLOCKS:
Safety Interlocks:
- Prevent gate operation during maintenance (LOT)
- Require removal of physical lock before operation
- Independent of electronic control system

Operational Interlocks:
- Limit rate of gate opening (prevent pressure surge)
- Prevent closing against high flow (cavitation risk)
- Require confirmation for emergency operations

Position Interlocks:
- Prevent conflicting gate commands
- Verify gate movement before proceeding
- Detect stuck or obstructed gates
```

**SGC-003: Emergency Gate Control**
```
EMERGENCY CLOSURE:
Trigger Conditions:
- Generator runaway (turbine overspeed)
- Main inlet valve failure (cannot close)
- Downstream emergency (flooding, structure damage)
- Dam safety emergency (seepage, structural issue)

Emergency Closure Sequence:
1. Emergency stop button activated
2. All gates commanded to full closed position
3. Normal rate limits bypassed (faster closure)
4. Monitor for equipment damage
5. Typical closure time: 1-3 minutes (vs. 5-10 normal)

Post-Emergency Actions:
- Inspect gates and mechanisms
- Check for cavitation or structural damage
- Verify position sensors accuracy
- Review event logs and recordings
- Update incident documentation

MANUAL OVERRIDE:
Manual Operation Methods:
- Portable motor: Electric or gasoline powered
- Hand crank: Manual wheel (takes hours)
- Hydraulic hand pump: For hydraulic gates

When to Use Manual:
- Power failure (if no backup generator)
- Control system failure
- Testing and maintenance
- Operator training

Manual Operation Precautions:
- Two-person rule for safety
- Verify no automatic control active
- Communication with control room
- Slow operation to avoid water hammer
```

### 2.3 Auxiliary Systems Control

**ASC-001: Cooling Water Systems**
```
GENERATOR STATOR COOLING:
Air-Cooled Generators:
- Fans: Motor-driven or shaft-driven
- Heat exchangers: Air-to-water coolers
- Temperature monitoring: Winding RTDs
- Control: Fan speed based on temperature
- Alarms: High temperature, low flow

Water-Cooled Generators (Large Units):
- Closed-loop system: Demineralized water
- Heat exchanger: Water-to-water or water-to-air
- Flow monitoring: Flow switches, meters
- Temperature control: Valve modulation
- Conductivity monitoring: Detect leaks to ground

Hydrogen-Cooled Generators (Very Large):
- Hydrogen gas cooling: Superior heat transfer
- Purity monitoring: >95% H2 required
- Pressure control: Typically 45-75 psig
- Seal oil system: Prevents H2 leakage
- Explosion protection: CO2 purging system

BEARING COOLING:
Oil Cooling System:
- Oil type: ISO VG 32 turbine oil typical
- Flow rate: 5-20 GPM per bearing
- Temperature control: Setpoint 120°F typical
- Heat exchanger: Oil-to-water or oil-to-air
- Filtration: 10-25 micron filters

Temperature Monitoring:
- RTDs in each bearing
- Alarm setpoint: 180°F typical
- Trip setpoint: 200°F typical
- Trending: Detect gradual increases

Oil Quality Monitoring:
- Particle counters: Detect bearing wear
- Water content: Karl Fischer testing
- Acid number: Detect oil degradation
- Periodic sampling: Monthly or quarterly
```

**ASC-002: Drainage & Dewatering Systems**
```
DRAINAGE SYSTEM COMPONENTS:
Sump Pumps:
- Location: Generator pit, turbine pit, draft tube
- Capacity: 50-500 GPM depending on location
- Type: Submersible or vertical turbine
- Control: Float switches, level transmitters
- Redundancy: Dual pumps, lead-lag operation

Level Monitoring:
- Float switches: High-high, high, low levels
- Ultrasonic level sensors: Continuous monitoring
- Alarms: High level to control room
- Trends: Detect increasing inflow (leakage)

TURBINE DEWATERING:
Dewatering for Maintenance:
1. Close main inlet valve
2. Open turbine drain valve
3. Start dewatering pump
4. Monitor water level drop
5. Verify complete drainage (typically 2-4 hours)
6. Inspect draft tube and runner

Bulkhead Gates (Larger Units):
- Installed upstream and downstream of turbine
- Allow complete isolation for maintenance
- Installation: Typically requires unit shutdown
- Dewatering time reduced: 30-60 minutes

DRAINAGE WATER HANDLING:
Clean Water (Bearing Cooling Leakage):
- Discharge to tailwater directly
- No treatment required

Oil-Contaminated Water (Bearing Seals):
- Oil-water separator treatment
- Monitoring: Oil content <15 ppm
- Discharge: Per NPDES permit

Dirty Water (Sediment, Debris):
- Settling basin
- Filtration if necessary
- Periodic cleaning
```

**ASC-003: Compressed Air Systems**
```
COMPRESSED AIR APPLICATIONS:
Turbine Governor:
- Pressure: 100-150 psig
- Quality: Instrument air (dry, oil-free)
- Redundancy: Dual compressors, receiver tank
- Backup: Nitrogen bottles for emergency

Actuators and Valves:
- Gate operators (some designs)
- Brake systems
- Instrumentation

Service Air:
- Maintenance tools
- Cleaning
- Lower quality requirements (lubricated air OK)

COMPRESSOR SYSTEM:
Compressors:
- Type: Rotary screw or reciprocating
- Capacity: 50-200 CFM @ 125 psig
- Redundancy: N+1 configuration
- Control: Lead-lag operation, VFD speed control

Air Dryers:
- Type: Refrigerated or desiccant
- Dewpoint: -40°F for instrument air
- Regeneration: Heatless or heated (desiccant)

Receiver Tanks:
- Capacity: 500-2000 gallons
- Pressure rating: 200 psig typical
- Purpose: Storage, surge capacity, pressure stabilization

Air Quality Monitoring:
- Dewpoint monitor: Ensure dry air
- Oil content monitor: <1 ppm for instruments
- Particle filter: 0.01 micron
```

---

## 3. Communication Systems (60+ Patterns)

### 3.1 Field Communications

**FCM-001: Serial Communication Networks**
```
MODBUS RTU:
Physical Layer: RS-485 two-wire or four-wire
Topology: Multidrop bus, up to 32 devices (247 with repeaters)
Speed: 9600, 19200, 38400 bps typical
Distance: Up to 4000 feet without repeaters
Protocol: Master-slave, polling-based
Applications: PLC to field devices, RTU to sensors
Message Format: Address (1 byte), function code, data, CRC

DNP3 SERIAL:
Physical Layer: RS-485 or RS-232
Topology: Point-to-point or multidrop
Speed: 9600 - 115200 bps
Protocol: Master-outstation, event-driven reports
Applications: RTU to SCADA master, substation integration
Features: Time synchronization, data prioritization, secure authentication

PROFIBUS DP:
Physical Layer: RS-485 (H1) or fiber optic (H2)
Topology: Line or ring
Speed: 9.6 kbps - 12 Mbps
Distance: 100m @ 12 Mbps, 1200m @ 93.75 kbps
Applications: PLC to distributed I/O, motor drives
Determinism: <10ms cycle time typical

DEVICENET:
Physical Layer: CAN bus (Controller Area Network)
Topology: Trunk-line with drop cables
Speed: 125, 250, 500 kbps
Distance: 500m @ 125 kbps, 100m @ 500 kbps
Applications: Safety PLCs, motor starters, sensors
Power: 24V DC power and data on same cable
```

**FCM-002: Industrial Ethernet Protocols**
```
MODBUS TCP:
Physical Layer: Ethernet 10/100/1000Base-T
Topology: Star, ring with managed switches
Protocol: Client-server over TCP/IP
Port: TCP 502
Applications: Modern SCADA integration
Advantages: Simple, widely supported, IP-based
Limitations: No real-time guarantees, security weaknesses

DNP3 OVER TCP/IP:
Physical Layer: Ethernet
Protocol: DNP3 application over TCP or UDP
Port: TCP/UDP 20000
Applications: Wide-area SCADA communications
Features: Secure authentication (SA), TLS encryption
Performance: Report-by-exception reduces bandwidth

ETHERNET/IP:
Physical Layer: Standard Ethernet
Topology: Star or ring (Device Level Ring)
Protocol: Common Industrial Protocol (CIP) over Ethernet
Ports: TCP 44818, UDP 2222
Applications: Rockwell Automation ecosystems
Real-time: Cyclic data <10ms, prioritized traffic
Integration: Seamless with ControlLogix PLCs

PROFINET:
Physical Layer: Standard Ethernet, fiber optic
Topology: Line, star, ring (Media Redundancy Protocol)
Protocol: Real-time Ethernet (IRT mode <1ms)
Applications: Siemens ecosystems, distributed I/O
Redundancy: Fast failover <200ms (ring) or <50ms (IRT)
Diagnostics: Integrated device diagnostics (I&M functions)

IEC 61850:
Physical Layer: Ethernet (usually fiber optic)
Topology: Station bus, process bus
Protocol: MMS (manufacturing message specification)
Applications: Substation automation, protection relays
GOOSE: Generic Object-Oriented Substation Event (peer-to-peer)
SV: Sampled values (real-time voltage/current data)
Real-time: <4ms for GOOSE trip signals
```

**FCM-003: Wireless Communications**
```
LICENSED RADIO (Private Microwave):
Frequency: 900 MHz, 2.4 GHz, 5.8 GHz, 6 GHz, 11 GHz, 18 GHz, 23 GHz
Bandwidth: 1-100 Mbps depending on frequency/modulation
Distance: Up to 50 miles line-of-sight
Applications: Remote RTU sites, camera backhaul
Advantages: Dedicated spectrum, no interference
Licensing: FCC license required
Equipment: Ceragon, Aviat, DragonWave radios

UNLICENSED RADIO (ISM Band):
Frequency: 900 MHz, 2.4 GHz, 5.8 GHz (ISM bands)
Bandwidth: 1-300 Mbps (802.11ac)
Distance: 1-10 miles with directional antennas
Applications: Temporary links, low-criticality monitoring
Advantages: No licensing, low cost
Limitations: Interference, no QoS guarantees
Security: WPA3 encryption, VPN tunnels

CELLULAR (4G LTE / 5G):
Carriers: AT&T, Verizon, T-Mobile, FirstNet
Bandwidth: 5-100 Mbps (LTE), 100-1000 Mbps (5G)
Latency: 30-50ms (LTE), 10-20ms (5G)
Applications: Backup WAN, remote monitoring, mobile access
Advantages: Wide coverage, no infrastructure cost
Limitations: Shared network, carrier dependency
Security: VPN mandatory, APN (Access Point Name) restrictions

SATELLITE (VSAT / LEO):
GEO Satellite:
- Latency: 500-700ms (unusable for real-time control)
- Bandwidth: 1-50 Mbps
- Applications: Remote sites with no terrestrial options
- Vendors: HughesNet, Viasat, iDirect

LEO Satellite (Starlink, OneWeb):
- Latency: 20-40ms (acceptable for SCADA)
- Bandwidth: 50-200 Mbps
- Applications: Remote dams, emergency backup
- Advantages: Low latency, global coverage
```

### 3.2 Wide Area Networks

**WAN-001: Fiber Optic Networks**
```
FIBER TYPES:
Single-Mode Fiber (SMF):
- Core diameter: 9 microns
- Distance: Up to 100 km without amplification
- Wavelengths: 1310nm, 1550nm
- Applications: Long-distance site-to-site links
- Cost: Higher transceivers, lower installation

Multi-Mode Fiber (MMF):
- Core diameter: 50 or 62.5 microns
- Distance: Up to 2 km @ 1 Gbps
- Wavelengths: 850nm, 1300nm
- Applications: Campus networks, short links
- Cost: Lower transceivers, higher fiber cost

FIBER NETWORK TOPOLOGY:
Point-to-Point:
- Dedicated fiber between two sites
- Simplest, most secure
- No shared bandwidth

Ring:
- Multiple sites connected in ring
- Redundancy: Automatic protection switching (APS)
- Failover: <50ms typical
- Protocol: Resilient Packet Ring (RPR), G.8032

DWDM (Dense Wavelength Division Multiplexing):
- Multiple wavelengths on single fiber
- Capacity: 40-80 channels × 10/100 Gbps
- Applications: High-capacity backbone
- Advantages: Massive bandwidth, future-proof

FIBER MONITORING:
OTDR (Optical Time Domain Reflectometer):
- Locates fiber breaks
- Measures loss, splice quality
- Testing: Pre-installation, troubleshooting

Optical Power Meter:
- Verifies signal strength
- Ensures receiver sensitivity met
- Regular testing: Annual

Fiber Optic Link Budget:
- Transmitter power: -2 dBm typical
- Receiver sensitivity: -28 dBm typical
- Splice/connector loss: 0.5 dB each
- Fiber attenuation: 0.35 dB/km @ 1310nm
- Margin: 3-6 dB recommended
```

**WAN-002: MPLS and Carrier Services**
```
MPLS (Multiprotocol Label Switching):
Network Type: Provider-provisioned VPN
Advantages:
- QoS guarantees (latency, jitter, packet loss)
- Isolation from internet threats
- Scalable multipoint connectivity
- Managed by service provider

Service Classes:
- Real-time: <20ms latency, <1ms jitter (voice, SCADA)
- Business: <40ms latency (data applications)
- Best effort: No guarantees (email, web)

Typical SLA:
- Availability: 99.9% (8.7 hours downtime/year)
- Latency: <30ms regional, <60ms national
- Packet loss: <0.1%
- MTTR: 4 hours (mean time to repair)

DARK FIBER:
Description: Leased fiber optic strand, customer provides electronics
Advantages:
- No recurring bandwidth charges
- Unlimited capacity (customer equipment determines)
- Complete control and security

Considerations:
- Upfront equipment cost
- Maintenance responsibility
- Fiber route availability
```

---

*System architecture documentation continues with protocols, standards, suppliers, and vendors in subsequent sections...*
