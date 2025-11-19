---
title: ETCS Onboard Equipment Specification
date: 2025-11-05 18:00:00
category: sectors
subcategory: equipment
sector: transportation
tags: [etcs, onboard-equipment, evc, dmi, btm, odometry, train-control, railway-signaling]
sources: [https://www.era.europa.eu/, https://www.unife.org/, https://www.etcs.org/]
confidence: high
---

## Summary
ETCS Onboard Equipment comprises the train-borne components of the European Train Control System (ETCS), providing continuous speed supervision and automatic train protection. The core system consists of the European Vital Computer (EVC), Driver Machine Interface (DMI), Balise Transmission Module (BTM), odometry system, and various interface modules. Operating under CENELEC SIL 4 safety standards, the onboard equipment continuously monitors train position, speed, and movement authority, calculating dynamic braking curves and enforcing speed restrictions through automatic brake intervention when necessary. The modular architecture supports ETCS Levels 1, 2, and 3 operation, with interoperability across different European railway networks, and integrates with train systems including traction control, braking systems, and legacy national train protection systems through Specific Transmission Modules (STMs).

## Key Information
- **Equipment Type**: Train Protection and Speed Supervision System
- **Standards**: SUBSET-026, SUBSET-034, SUBSET-041, SUBSET-076, CENELEC SIL 4, EN 50126/128/129
- **Safety Integrity Level**: CENELEC SIL 4 (10^-9 dangerous failures per hour)
- **Operating Levels**: ETCS Level 0, 1, 2, 3, NTC (National Train Control), Limited Supervision
- **Operating Environment**: Railway vehicle environment, -40°C to +70°C, shock and vibration per EN 61373
- **Power Supply**: 24V DC, 72V DC, 110V DC nominal (train battery voltage)
- **Communication**: Euroloop, GSM-R, Eurobalise, STM interfaces, train bus (MVB/WTB/Ethernet)
- **Applications**: High-speed trains, regional trains, freight locomotives, metro systems

## Technical Details
### ETCS Onboard Architecture

#### 1. European Vital Computer (EVC)
**Core Processing System**
- **Function**: Central safety-critical computer executing ETCS algorithms
- **Architecture**: Dual-channel or triple-channel redundant processing
- **Processor**: Railway-qualified processors (Power Architecture, ARM Cortex, or proprietary)
- **Processing Speed**: Real-time deterministic execution with <50ms cycle time
- **Memory**: 64-256 MB RAM, 128-512 MB non-volatile storage
- **Operating System**: Real-time safety OS (VxWorks, INTEGRITY, or proprietary RTOS)
- **Safety Architecture**: Dual 2-out-of-3 voting, comparison logic, watchdogs
- **Certifications**: CENELEC SIL 4 per EN 50129, independent safety assessment

**Core Functions**
- **Position Management**: Calculate train position using balise data and odometry
- **Speed Supervision**: Continuously monitor speed against permitted speed
- **Brake Curve Calculation**: Compute deceleration curves based on train characteristics
- **Mode Management**: Handle ETCS operating modes and level transitions
- **Movement Authority**: Process and supervise movement authority limits
- **Gradient Profile**: Manage gradient information for brake curve adjustment
- **Train Data**: Store and manage train characteristics (length, braking performance, category)
- **Interface Management**: Coordinate all onboard subsystems and interfaces

**Performance Specifications**
- **Position Accuracy**: ±5 meters (typically ±2 meters with odometry calibration)
- **Speed Accuracy**: ±2 km/h or ±3% whichever is greater
- **Reaction Time**: <1 second from hazard detection to brake application
- **Processing Latency**: <50 ms typical cycle time
- **Availability**: >99.9% (calculated per EN 50126)
- **MTBF**: >100,000 hours (excluding wear components)
- **Safety Failure Rate**: <10^-9 dangerous failures per hour

**Physical Characteristics**
- **Dimensions**: 19" rack mount, 4U-8U height (approximately 450mm x 400mm x 180-360mm)
- **Weight**: 15-30 kg depending on configuration
- **Cooling**: Forced air cooling with redundant fans, some models conduction cooled
- **Mounting**: Shock-mounted 19" rack installation in driver cab or equipment room
- **Protection**: IP54 minimum, EN 61373 shock and vibration Category 1A
- **Power Consumption**: 50-150W typical, 200W maximum

#### 2. Driver Machine Interface (DMI)
**Display and Control System**
- **Function**: Present ETCS information to driver and accept driver inputs
- **Display Type**: TFT LCD color display, sunlight-readable (>500 cd/m²)
- **Screen Size**: 10"-12" diagonal (254-305mm), 640x480 to 800x600 resolution
- **Touch Interface**: Resistive or capacitive touchscreen (with glove operation)
- **Physical Buttons**: Emergency brake override, acknowledge buttons, data entry
- **Dimming**: Automatic or manual brightness adjustment (0-100%)
- **Color Coding**: Standardized ETCS colors (grey, yellow, orange, red per SUBSET-091)
- **Layout**: Standardized DMI layout per SUBSET-091, SUBSET-026 Annex A

**Information Displayed**
- **Speed**: Current speed, permitted speed, target speed, release speed
- **Distances**: Distance to target, distance to end of authority
- **Planning Information**: Planning area display with speed profiles
- **Mode and Level**: Current ETCS operating mode and level
- **Symbols**: Standardized symbols for system states, restrictions, warnings
- **Messages**: Driver advisory and mandatory information messages
- **Supervision Status**: Indication supervision, overspeed supervision, intervention
- **Time**: Train running number, time, date information

**Physical Specifications**
- **Dimensions**: Approximately 350mm x 270mm x 100mm (flush-mount)
- **Weight**: 3-6 kg depending on model
- **Mounting**: Flush-mount in driver desk or panel-mount
- **Viewing Angle**: >160° horizontal and vertical
- **Operating Temperature**: -25°C to +70°C (in-cab environment)
- **Protection**: IP54 front panel, sealed against moisture and dust
- **Shock/Vibration**: EN 61373 Category 1B (driver cab mounting)

**Vendors and Models**
- **Alstom DMI**: 10" and 12" models, multi-STM support, color touchscreen
- **Siemens DMI-S**: Compact design, high-brightness display, multilingual
- **Bombardier/Alstom DMI**: Proven reliability, installed on thousands of trains
- **Thales DMI**: Modular design, future-proof architecture
- **Hitachi DMI**: Integrated with Japanese and European systems

#### 3. Balise Transmission Module (BTM)
**Balise Data Reception System**
- **Function**: Receive, decode, and validate Eurobalise telegrams
- **Antenna System**: Two antennas mounted 3-4 meters apart under train
- **Antenna Type**: Ferrite core loop antennas with magnetic coupling
- **Reception Frequency**: 4.234 MHz (balise to train), 27.095 MHz (train to balise)
- **Reception Range**: Effective communication 1.5-4 meters vertical separation
- **Speed Capability**: Reliable reception up to 500 km/h
- **Redundancy**: Dual antenna system ensures balise group detection
- **Processing**: Telegram decoding, error detection, safety validation

**Data Processing**
- **Telegram Validation**: CRC-16 checksum verification per SUBSET-036
- **Safety Code**: Cryptographic safety code validation
- **Duplicate Detection**: Eliminate duplicate balise detections
- **Balise Grouping**: Assemble balise groups based on linking packets
- **Output to EVC**: Validated telegram data transferred to EVC
- **Diagnostics**: Report antenna status, reception quality, failures
- **Interface**: Serial or CAN bus connection to EVC per SUBSET-040

**Physical Specifications**
- **BTM Unit Dimensions**: Approximately 250mm x 200mm x 100mm
- **Weight**: 2-4 kg (BTM unit only, excluding antennas/cables)
- **Antenna Dimensions**: Approximately 600mm x 400mm x 60mm each
- **Antenna Mounting**: Underslung mounting on bogie or underframe
- **Antenna Separation**: 3-4 meters between antennas (longitudinal)
- **Cable Length**: Up to 30 meters from antenna to BTM unit
- **Protection**: IP65 for BTM unit, IP68 for antennas
- **Operating Temperature**: -40°C to +70°C
- **Shock/Vibration**: EN 61373 Category 1A (bogie-mounted antennas)

#### 4. Odometry System
**Position and Speed Measurement**
- **Function**: Measure train speed and distance traveled
- **Sensor Types**: Wheel sensors (inductive or Hall-effect), Doppler radar, accelerometer
- **Wheel Sensors**: 2-4 sensors per train (redundancy and cross-checking)
- **Radar**: Doppler radar for slip/slide detection and backup measurement
- **Accelerometer**: Inertial measurement for short-term accuracy
- **Sensor Fusion**: Combine multiple sensors for optimal accuracy
- **Calibration**: Automatic calibration using balise position references

**Performance Characteristics**
- **Speed Range**: 0-500 km/h (depending on train type)
- **Speed Accuracy**: ±2 km/h or ±3% whichever is greater
- **Position Accuracy**: Drift <5% of distance traveled between balise corrections
- **Resolution**: 0.1 km/h speed resolution, 0.1 meter position resolution
- **Update Rate**: 10-50 Hz measurement rate
- **Calibration Interval**: Automatic re-calibration every 1-2 km using balises
- **Slip/Slide Detection**: Detect wheel slip/slide and switch to radar/accelerometer

**Physical Components**
- **Wheel Sensors**: Inductive proximity sensors or Hall-effect sensors on axle
- **Sensor Mounting**: Non-contact mounting on axle boxes or bogies
- **Doppler Radar**: Antenna mounted under train floor (Doppler effect measurement)
- **Accelerometer**: Solid-state MEMS accelerometer in EVC or separate unit
- **Processing Unit**: Integrated in EVC or separate odometry computer
- **Interface**: High-speed serial or CAN bus to EVC
- **Power**: 24V DC from train supply
- **Standards**: SUBSET-041 (odometry), SUBSET-034 (train interface)

#### 5. Radio Interface (GSM-R/FRMCS)
**Train-Ground Communication for Level 2/3**
- **Function**: Bidirectional data communication with Radio Block Centre (RBC)
- **Radio System**: GSM-R (GSM-Railway) 900 MHz, transitioning to FRMCS (5G)
- **Data Protocols**: Euroradio protocol per SUBSET-037, SUBSET-091
- **Connection Type**: Circuit-switched data or GPRS packet data
- **Communication Modes**: Safe connection (safety-critical), unsafe connection (non-critical)
- **Security**: Authentication, encryption, integrity checking per SUBSET-037
- **Redundancy**: Automatic handover between base stations, RBC redundancy

**Radio Communication Unit (RCU)**
- **Function**: GSM-R/FRMCS radio transceiver for ETCS communication
- **Frequency**: 876-880 MHz uplink, 921-925 MHz downlink (GSM-R)
- **Transmission Power**: 2-8W effective radiated power
- **Antenna**: Roof-mounted GSM-R antenna (diversity antenna optional)
- **Data Rate**: 9.6 kbps circuit-switched, up to 48 kbps GPRS
- **Latency**: <500ms typical, <2s maximum per SUBSET-091
- **Handover**: Seamless handover between RBCs and base stations
- **Fallback**: Revert to Level 1 operation if radio connection lost

**Physical Specifications**
- **RCU Dimensions**: Approximately 300mm x 250mm x 100mm
- **Weight**: 4-7 kg
- **Antenna**: Roof-mounted monopole or blade antenna
- **Mounting**: 19" rack mount or custom mounting in equipment room
- **Operating Temperature**: -40°C to +70°C
- **Protection**: IP54 minimum
- **Standards**: ETSI GSM-R standards, SUBSET-037, SUBSET-093

#### 6. Specific Transmission Module (STM)
**National Train Control System Interface**
- **Function**: Interface ETCS onboard with national train protection systems
- **Systems Supported**: ATB, PZB/Indusi, SCMT, TVM, KHP, ASFA, AWS, TPWS, and others
- **Operating Mode**: NTC (National Train Control) mode under STM control
- **Supervision**: STM provides speed supervision when ETCS not active
- **Transition**: Seamless transition between ETCS and STM supervision
- **DMI Integration**: Display STM information on ETCS DMI per SUBSET-091
- **Safety Level**: SIL 4 interface between EVC and STM

**STM Architecture**
- **Processing Unit**: Dedicated processor for national system protocol
- **Legacy Interface**: Sensors, antennas, receivers for national system
- **EVC Interface**: Standardized STM-EVC interface per SUBSET-035
- **Isolation**: Galvanic isolation between STM and EVC
- **Status Reporting**: Report STM system status, failures to EVC
- **Data Exchange**: Speed limits, target speeds, braking commands to EVC

**Common STM Types**
- **STM ATB (Netherlands)**: Interface with ATB automatic train protection
- **STM PZB (Germany, Austria)**: Interface with PZB/Indusi 1000 Hz system
- **STM TVM (France)**: Interface with TVM 300/430 cab signaling
- **STM SCMT (Italy)**: Interface with SCMT train protection system
- **STM ASFA (Spain)**: Interface with ASFA digital train protection
- **STM KHP (Poland)**: Interface with Polish train protection system

### Train Interface and Integration

#### 1. Train Control and Brake Interface (TIU)
**Train Interface Unit Functions**
- **Brake Control**: Command service brake and emergency brake application
- **Traction Control**: Interface with traction interlocking (cut traction when needed)
- **Isolation**: Monitor driver's desk isolation status (cab selection)
- **Doors**: Interface with door control system (prevent departure with open doors)
- **Pantograph**: Control pantograph for level transitions, neutral sections
- **Vigilance**: Monitor driver vigilance button or deadman device
- **Train Integrity**: Monitor train integrity (tail detection, brake continuity)
- **Diagnostics**: Report train interface status and failures to EVC

**Brake Interface**
- **Service Brake**: Proportional or stepped brake demand to brake system
- **Emergency Brake**: Binary emergency brake command (fail-safe)
- **Brake Feedback**: Monitor brake application status, brake percentage
- **Brake Release**: Command brake release when safe
- **Brake Test**: Support automatic brake test procedures
- **Brake Curve**: Provide train braking characteristics to EVC
- **Standards**: UIC 541-05, UIC 544, EN 15734-1

**Train Bus Interface**
- **Protocols**: MVB (Multifunction Vehicle Bus), WTB (Wire Train Bus), Ethernet Train Backbone
- **Data Exchange**: Exchange data with train systems (TCMS, brakes, doors, HVAC)
- **Real-Time**: Deterministic real-time data exchange (<10ms latency)
- **Redundancy**: Redundant bus connections for safety-critical data
- **Standards**: IEC 61375 (MVB/WTB), EN 50155 (Ethernet)

#### 2. Juridical Recording Unit (JRU)
**Legal Event Recording**
- **Function**: Record safety-relevant data for accident investigation
- **Data Recorded**: Speed, ETCS mode, driver actions, brake commands, balise data
- **Recording Duration**: Minimum 24 hours of operation
- **Storage**: Crash-protected removable storage media
- **Download**: Download recorded data using JRU interface
- **Integrity**: Tamper-proof recording, cryptographic sealing
- **Standards**: SUBSET-027 (JRU functional requirements)

**Physical Specifications**
- **Dimensions**: Approximately 200mm x 150mm x 80mm
- **Weight**: 1-2 kg
- **Mounting**: Secure mounting in equipment room or driver cab
- **Crash Protection**: Withstand 300g impact, 1100°C for 30 minutes
- **Interface**: USB, Ethernet, or serial download interface
- **Storage Capacity**: 2-16 GB solid-state storage

#### 3. Other Interfaces
**Cold Movement Detection (CMD)**
- **Function**: Detect unauthorized train movement when ETCS not active
- **Implementation**: Independent speed sensor and brake interface
- **Activation**: Automatically apply emergency brake if movement detected
- **Standards**: Part of SUBSET-026 requirements

**Air Conditioning and Heating**
- **Interface**: Monitor and control cab environmental systems
- **Purpose**: Ensure DMI visibility, equipment cooling, driver comfort
- **Integration**: Via train bus or discrete signals

**Lighting**
- **Interface**: Control cab lighting, indicator lamps
- **Purpose**: Visibility of DMI and controls in all conditions
- **Standards**: Railway ergonomics standards

### ETCS Operating Modes

#### 1. ETCS Levels
**Level 0 - Unfitted Lines**
- **Description**: Train equipped with ETCS, line not equipped
- **Supervision**: No ETCS supervision, rely on driver and line-side signals
- **Speed Limit**: National speed limit or speed entered by driver
- **Use Case**: Running over non-ETCS lines, degraded situations

**Level 1 - Intermittent Supervision**
- **Description**: Movement authority via Eurobalise groups
- **Supervision**: Spot supervision at balise locations
- **Infill**: Optional Euroloop or radio infill for continuous updates
- **Signaling**: Lineside signals remain, ETCS provides additional protection
- **Use Case**: Retrofit of existing lines, transition to higher levels

**Level 2 - Continuous Supervision**
- **Description**: Movement authority via GSM-R radio from RBC
- **Supervision**: Continuous supervision using radio communication
- **Signals**: No lineside signals required (except for degraded modes)
- **Positioning**: Balises for position reference only (not movement authority)
- **Use Case**: High-speed lines, new installations, optimal capacity

**Level 3 - Moving Block**
- **Description**: Train reports its position, RBC calculates moving block
- **Supervision**: Continuous radio supervision like Level 2
- **Train Integrity**: Train must report guaranteed train integrity
- **Capacity**: Maximum line capacity (no fixed block sections)
- **Use Case**: Future high-capacity metro and mainline systems

**NTC (National Train Control)**
- **Description**: Operation under national train protection system via STM
- **Supervision**: STM provides speed supervision per national rules
- **Use Case**: Running on non-ETCS equipped lines with national systems

#### 2. ETCS Modes
**Full Supervision (FS)**
- **Normal operating mode with complete ETCS supervision**
- **Speed limits, gradients, movement authority all enforced**
- **Automatic brake application if limits exceeded**

**On Sight (OS)**
- **Restricted mode for cautious operation**
- **Maximum speed limited (typically 30-40 km/h)**
- **Driver prepared to stop short of any obstacle**

**Staff Responsible (SR)**
- **Driver responsible for safe operation**
- **ETCS monitoring only, no automatic enforcement**
- **Used in station areas, depots, during shunting**

**Shunting (SH)**
- **Shunting operations in yards and sidings**
- **Low speed limit (typically 25 km/h)**
- **Simplified supervision and mode transitions**

**Trip (TR)**
- **Emergency brake applied due to ETCS violation**
- **Train must stop, driver must acknowledge**
- **Reset by driver after understanding cause**

**Post Trip (PT)**
- **Mode after trip recovery**
- **Driver must confirm safe to continue**
- **Transition to appropriate operating mode**

**Reversing (RV)**
- **Allows controlled reversing movement**
- **Low speed limit, strict supervision**
- **Used for minor reversals, not normal operation**

**Unfitted (UN)**
- **Line not equipped with ETCS**
- **Driver follows lineside signals**
- **ETCS provides no supervision**

**System Failure (SF)**
- **ETCS has failed, cannot provide supervision**
- **Fallback to national system or restricted operation**
- **Service brake applied, maximum speed limited**

**Isolation (IS)**
- **ETCS intentionally isolated by driver**
- **No ETCS supervision active**
- **Used for maintenance, emergency situations**

### Brake Curve Calculation

#### 1. Braking Models
**Emergency Brake Deceleration**
- **Model**: Considers train mass, brake force, gradient, adhesion
- **Calculation**: EVC calculates based on train data and track profile
- **Safety Margin**: Conservative assumptions (wet rail, worn brake pads)
- **Update**: Recalculated continuously as conditions change

**Service Brake Deceleration**
- **Model**: Similar to emergency brake but less aggressive
- **Application**: Applied before emergency intervention curve
- **Purpose**: Avoid unnecessary emergency brake applications

**Supervised Locations**
- **End of Authority (EOA)**: Must stop before EOA
- **Target Speed**: Must reduce to target speed at target location
- **Level Transition**: Prepare for transition to new ETCS level
- **Mode Profile**: Change mode at specified location

#### 2. Supervision Curves
**Indication Curve**
- **Purpose**: Early warning to driver that intervention approaching
- **Display**: Yellow/orange indication on DMI speed dial
- **Action**: Driver should brake to comply with target speed

**Permitted Speed Curve**
- **Purpose**: Maximum permitted speed at any location
- **Display**: Continuous speed supervision on DMI
- **Action**: Driver must not exceed permitted speed

**Warning Curve**
- **Purpose**: Provide warning before service brake intervention
- **Display**: Audible and visual warning (warning symbol)
- **Action**: Driver must brake immediately or service brake applied

**Service Brake Intervention Curve**
- **Purpose**: Automatic service brake if warning not heeded
- **Action**: EVC commands service brake application automatically
- **Display**: Service brake intervention symbol on DMI

**Emergency Brake Intervention Curve**
- **Purpose**: Last safety layer before passing supervised location
- **Action**: EVC commands emergency brake application
- **Display**: Emergency brake indication, TRIP mode activated

### Vendors and Products

#### 1. Major ETCS Onboard Suppliers
**Alstom (including former Bombardier Transportation)**
- **Product**: EBI Lock / Atlas family of ETCS onboard equipment
- **EVC**: Atlas 100, Atlas 200 (STM integration), EBI Lock EVC
- **DMI**: 10" and 12" color touchscreen DMI, multilingual support
- **BTM**: EBI Balise Transmission Module with dual antennas
- **Features**: Modular architecture, multi-STM support, proven on TGV, ICE, Eurostar
- **Certifications**: Multiple national approvals, CENELEC SIL 4, ERA approval
- **Support**: Global service network, spare parts, obsolescence management

**Siemens Mobility**
- **Product**: Trainguard ETCS onboard equipment
- **EVC**: Compact and modular design, multi-level support
- **DMI**: High-brightness touchscreen DMI, customizable layouts
- **Features**: Integrated with Siemens traction and train control systems
- **Installations**: Widely deployed on ICE trains, S-Bahn, regional trains
- **Certifications**: German EBA approval, ERA certification, SIL 4
- **Support**: European service centers, training, technical support

**Thales Ground Transportation Systems**
- **Product**: ETCS Onboard System
- **EVC**: Configurable safety computer platform
- **DMI**: Touchscreen DMI with physical backup controls
- **Features**: High availability design, advanced diagnostics
- **Installations**: French TGV, Eurostar, Thalys, international projects
- **Certifications**: CENELEC SIL 4, multiple national type approvals
- **Support**: 24/7 support, remote diagnostics, field service

**Hitachi Rail**
- **Product**: ETCS Onboard Equipment
- **EVC**: Compact modular design, easy retrofitting
- **DMI**: Modern touchscreen interface with intuitive design
- **Features**: Hybrid systems (ETCS + Japanese ATC/ATS)
- **Installations**: UK Class 800/801/802 fleets, European metros
- **Certifications**: ERA approval, UK ROGS approval, SIL 4
- **Support**: UK and European support centers

**CAF (Construcciones y Auxiliar de Ferrocarriles)**
- **Product**: Integrated ETCS onboard systems for CAF trains
- **EVC**: Integrated with CAF train control architecture
- **Features**: Optimized for CAF rolling stock, modular design
- **Installations**: Spanish high-speed trains, international projects
- **Certifications**: ERA approval, Spanish ADIF certification

#### 2. Component Suppliers
**Ansaldo STS (Hitachi Group)**
- **Specialization**: ETCS software and systems integration
- **Products**: EVC software, DMI applications, engineering services

**Televic Rail**
- **Specialization**: DMI, driver desk integration
- **Products**: Touchscreen DMI, control panels, ergonomic solutions

**MERMEC (part of Angel Trains)**
- **Specialization**: BTM, odometry, diagnostics
- **Products**: Balise readers, wheel sensors, diagnostic systems

**Network Rail / IM Technical Services**
- **Specialization**: ETCS rollout support, engineering services (UK)
- **Services**: Design, testing, commissioning, training

### Installation and Commissioning

#### 1. Installation Process
**System Design**
- **Train Interface Study**: Analyze train systems and define interfaces
- **Safety Assessment**: Conduct safety case per EN 50126/129
- **Configuration**: Define ETCS configuration (levels, modes, STMs)
- **Integration Design**: Plan integration with existing train systems
- **Documentation**: Prepare installation manuals, test procedures

**Physical Installation**
- **EVC Rack**: Install 19" equipment rack in equipment room
- **DMI**: Flush-mount DMI in driver desk with ergonomic positioning
- **BTM Antennas**: Mount antennas on bogies or underframe (3-4m spacing)
- **Odometry Sensors**: Install wheel sensors on axle boxes
- **Radio Antenna**: Mount GSM-R antenna on roof
- **Cabling**: Install shielded cables with proper EMC grounding
- **TIU**: Connect to brake, traction, door systems per interface specification

**Software Configuration**
- **Train Data**: Configure train length, braking characteristics, category
- **Balise Antenna Offset**: Configure BTM antenna position relative to train reference
- **DMI Language**: Configure language and driver preferences
- **STM Parameters**: Configure STM systems and transition rules
- **National Values**: Configure national-specific parameters
- **Level and Mode Configuration**: Define permitted levels and modes

#### 2. Testing and Commissioning
**Static Testing**
- **Power-Up Tests**: Verify power supply, processor boot, diagnostics
- **Interface Tests**: Test brake, traction, door, train bus interfaces
- **DMI Tests**: Verify display, touchscreen, button functions
- **Communication Tests**: Test BTM, radio, STM communications
- **Safety Tests**: Verify redundancy, safety outputs, failure modes

**Dynamic Testing**
- **Balise Reading**: Test balise reception at various speeds
- **Odometry Calibration**: Calibrate odometry using known balise positions
- **Brake Curve Validation**: Verify brake curve calculation and supervision
- **Radio Communication**: Test RBC connection, handovers, radio coverage
- **Mode Transitions**: Test all mode and level transitions
- **STM Integration**: Test transitions between ETCS and national systems
- **End-to-End**: Complete journey tests over equipped line

**Validation and Approval**
- **Type Testing**: Complete manufacturer type tests per SUBSET-026
- **On-Track Testing**: Conduct on-track tests per SUBSET-076
- **Safety Validation**: Verify safety case and SIL 4 requirements
- **Interoperability Testing**: Verify operation with different trackside equipment
- **National Approval**: Obtain approval from national safety authority
- **ERA Certification**: Obtain EC declaration of verification for TSI compliance

### Maintenance and Support

#### 1. Preventive Maintenance
**Scheduled Inspections**
- **Frequency**: Typically monthly or per train mileage intervals
- **Visual Inspection**: Check DMI, cables, antenna mounting
- **Software Health**: Review diagnostic logs, error histories
- **BTM Cleaning**: Clean BTM antennas to ensure reliable reception
- **Calibration Verification**: Verify odometry calibration accuracy

**Software Updates**
- **Security Patches**: Apply software security updates
- **Functionality Updates**: Install new features or improvements
- **Configuration Changes**: Update national values, train data as needed
- **Version Control**: Maintain software version documentation

#### 2. Corrective Maintenance
**Common Fault Modes**
- **DMI Failures**: Touchscreen issues, display failures (replace DMI unit)
- **BTM Issues**: Antenna damage, poor reception (repair/replace antennas)
- **Odometry Errors**: Wheel sensor failures, drift accumulation (replace sensors)
- **Radio Problems**: Poor coverage, RBC connection issues (antenna/RCU check)
- **EVC Faults**: Processor failures, redundancy loss (replace EVC unit)

**Fault Diagnosis**
- **DMI Display**: DMI displays diagnostic messages and fault codes
- **JRU Data**: Download JRU data for detailed failure analysis
- **Remote Diagnostics**: Remote monitoring and diagnostics via train bus
- **Portable Test Equipment**: Balise simulators, diagnostic laptops
- **Support Hotline**: Manufacturer technical support for complex issues

**Repair Process**
- **Isolation**: Isolate faulty component (EVC, DMI, BTM, etc.)
- **Replacement**: Replace line-replaceable units (LRUs)
- **Configuration**: Load configuration data to new unit
- **Testing**: Conduct functional tests after repair
- **Validation**: Perform on-track validation test
- **Documentation**: Record repair in maintenance management system

### Lifecycle and Technology Evolution

#### 1. ETCS Baseline Evolution
**Baseline 2 (Historical)**
- Early ETCS implementations
- Deployed on initial high-speed lines
- Limited functionality compared to later baselines

**Baseline 3 (Current Standard)**
- **Release**: Mandatory since 2012
- **Features**: Improved interoperability, better level transitions, enhanced DMI
- **Installations**: Most current ETCS deployments
- **Standards**: SUBSET-026 v3.6.0 and later

**Baseline 4 (Future Standard - being defined)**
- **Planned Features**: ATO (Automatic Train Operation) integration, enhanced diagnostics
- **Timeline**: Definition and deployment ongoing
- **Migration**: Backward compatibility with Baseline 3

#### 2. Technology Trends
**FRMCS (Future Railway Mobile Communication System)**
- **Description**: 5G-based successor to GSM-R
- **Timeline**: Deployment starting 2025-2030
- **Benefits**: Higher data rates, lower latency, enhanced services
- **Migration**: ETCS onboard equipment upgraded with FRMCS radio modules

**Automatic Train Operation (ATO)**
- **Description**: Automated driving over ETCS with GoA 2-4 automation
- **Standards**: SUBSET-125 (ATO over ETCS), SUBSET-126 (ATO functional requirements)
- **Implementation**: Additional onboard equipment and software
- **Pilots**: Various ATO over ETCS pilot projects in Europe

**Cybersecurity Enhancements**
- **Standards**: IEC 62443 railway cybersecurity
- **Features**: Enhanced authentication, intrusion detection, secure boot
- **Updates**: Ongoing cybersecurity improvements in ETCS baselines

**Remote Monitoring and Predictive Maintenance**
- **Description**: Continuous monitoring of ETCS health via train connectivity
- **Benefits**: Predictive maintenance, reduced failures, optimized maintenance
- **Implementation**: Data analytics platforms, cloud services

## Related Topics
- kb/sectors/transportation/equipment/device-eurobalise-20251105-18.md
- kb/sectors/transportation/equipment/product-line-trainguard-20251105-18.md
- kb/sectors/transportation/equipment/device-interlocking-20251105-18.md

## References
- [European Union Agency for Railways (ERA)](https://www.era.europa.eu/) - ETCS specifications and technical standards
- [UNIFE (Union of European Railway Industries)](https://www.unife.org/) - Industry information and standards
- [ETCS Website](https://www.etcs.org/) - Technical resources and documentation

## Metadata
- Last Updated: 2025-11-05 18:00:00
- Research Session: Transportation Equipment Research
- Completeness: 95%
- Next Actions: Document ATO over ETCS integration details, explore cybersecurity implementations
