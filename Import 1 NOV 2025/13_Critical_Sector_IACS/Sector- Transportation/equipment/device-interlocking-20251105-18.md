---
title: Railway Interlocking System Equipment Specification
date: 2025-11-05 18:00:00
category: sectors
subcategory: equipment
sector: transportation
tags: [interlocking, railway-signaling, point-machine, signal-control, safety-system, route-setting, fail-safe]
sources: [https://www.railway-signaling.eu/, https://www.era.europa.eu/, https://www.irse.org/]
confidence: high
---

## Summary
Railway interlocking systems provide the fundamental safety logic that prevents conflicting train movements by controlling signals, points (switches), and level crossings according to rigorous safety rules. Modern electronic interlockings replace traditional relay-based systems with programmable fail-safe computers that enforce route compatibility, signal sequencing, and track occupancy logic while maintaining CENELEC SIL 4 safety integrity. These systems implement geographic interlocking (based on physical track layout) or route-based interlocking (based on predefined routes), controlling hundreds of trackside objects across stations and yards. Interlockings interface with train detection systems (track circuits, axle counters), point machines, signals, level crossing equipment, and train control systems (ETCS, ATP), providing vital safety functions including approach locking, time locking, and sequential release while supporting both automatic and manual route setting modes for railway operations.

## Key Information
- **Equipment Type**: Railway Interlocking System (Electronic or Relay-Based)
- **Standards**: EN 50126, EN 50128, EN 50129, CENELEC SIL 4, national railway standards
- **Safety Integrity**: CENELEC SIL 4 (10^-9 dangerous failures per hour)
- **Architecture**: Geographic or route-based interlocking logic
- **Operating Environment**: Controlled equipment room (wayside) and outdoor field equipment
- **Control Objects**: Signals, points, track circuits, axle counters, level crossings, derailers
- **Interfaces**: Train control systems (ETCS, ATP), signaler workstations, adjacent interlockings
- **Applications**: Main line stations, yards, junctions, terminals, depot facilities

## Technical Details
### Interlocking Architecture

#### 1. Central Interlocking Computer
**Processing Platform**
- **Architecture**: Dual-channel or triple-modular redundant fail-safe computers
- **Processors**: Railway-qualified safety processors (2oo3 voting, dual 2oo2 comparison)
- **Processing Cycle**: 100-500ms deterministic cycle time for safety logic
- **Memory**: 1-16 GB RAM, 64-256 GB solid-state storage
- **Operating System**: Real-time safety OS (VxWorks, RTOS, proprietary safety kernel)
- **Safety Certification**: CENELEC SIL 4 per EN 50129, independent safety assessment
- **Redundancy**: Hot-standby or active-active redundancy with automatic failover
- **Availability**: >99.95% availability for revenue service

**Safety Logic Functions**
- **Route Setting**: Establish safe routes for train movements
- **Conflict Detection**: Prevent conflicting routes and opposing signals
- **Point Control**: Lock points in position for established routes
- **Signal Control**: Display correct signal aspects based on route and occupancy
- **Track Occupancy**: Monitor track sections via track circuits or axle counters
- **Approach Locking**: Lock routes when trains approach (prevents route cancellation)
- **Time Locking**: Enforce time delays before route cancellation
- **Sequential Release**: Release route sections as trains clear them
- **Level Crossing Control**: Interface with level crossing barrier systems

**Performance Characteristics**
- **Route Setting Time**: 3-10 seconds typical (depending on complexity)
- **Processing Latency**: <500ms for safety-critical decisions
- **Capacity**: Control 50-500 track objects (signals, points, track sections)
- **Scalability**: Modular expansion for larger installations
- **MTBF**: >200,000 hours (excluding field equipment)
- **Dangerous Failure Rate**: <10^-9 per hour (SIL 4 requirement)

**Physical Specifications**
- **Dimensions**: 19" rack-mount system, 20U-42U rack height
- **Weight**: 100-300 kg for complete system (including racks and UPS)
- **Mounting**: Equipment room with environmental controls
- **Power Supply**: 110/230V AC with UPS backup (minimum 30-minute autonomy)
- **Power Consumption**: 500W-2kW depending on system size
- **Operating Environment**: 15-30°C, 20-80% RH (controlled environment)
- **Protection**: IP20 (equipment room installation)

#### 2. Object Controllers
**Point Controllers**
- **Function**: Interface with point machines to control switch positions
- **Control Outputs**: Energize point machine coils for normal/reverse movement
- **Position Detection**: Monitor point position via detection contacts
- **Lock Verification**: Verify mechanical lock engagement before route setting
- **Supervision**: Continuous monitoring of point machine current and position
- **Diagnostics**: Detect point machine failures, obstruction, loss of detection
- **Interface**: Direct wired connection or digital field bus (ASI, Profibus)

**Signal Controllers**
- **Function**: Control signal lamp circuits based on interlocking commands
- **Lamp Control**: Energize appropriate signal lamps (red, yellow, green, white)
- **Lamp Monitoring**: Monitor lamp current and detect lamp failures
- **Fail-Safe**: Ensure safe aspect (red or dark) on controller failure
- **LED Signals**: Support LED signal control with pulse-width modulation
- **Multi-Aspect**: Control multi-aspect signals (2, 3, 4, or 5 aspect)
- **Interface**: Direct wired or digital field bus connection

**Track Occupation Controllers**
- **Function**: Interface with track circuits or axle counters
- **Track Circuit**: Monitor track circuit voltage/current for train detection
- **Axle Counter**: Process axle counter pulses to determine section occupancy
- **Supervision**: Continuous monitoring of detection system health
- **Fail-Safe**: Report occupied on detection system failure
- **Diagnostics**: Detect broken rails, shunting failures, equipment faults
- **Interface**: Analog (track circuits) or digital (axle counters)

#### 3. Interlocking Logic Types
**Geographic Interlocking**
- **Principle**: Based on physical track layout and object relationships
- **Data Model**: Track topology database with spatial relationships
- **Route Setting**: Automatic route calculation based on requested origin/destination
- **Flexibility**: Easily adapted to track layout changes
- **Applications**: Modern electronic interlockings, complex stations
- **Advantages**: Simplified configuration, reduced engineering effort
- **Standards**: EULYNX standard for geographic data model (Europe)

**Route-Based Interlocking**
- **Principle**: Predefined routes with stored control sequences
- **Data Model**: Route table database with control commands for each route
- **Route Setting**: Execute stored control sequence for selected route
- **Configuration**: Each route explicitly configured during engineering phase
- **Applications**: Traditional systems, simple stations, legacy replacements
- **Advantages**: Predictable behavior, well-understood by operators
- **Standards**: National standards (varies by country)

**Hybrid Interlocking**
- **Principle**: Combines geographic and route-based approaches
- **Core Routes**: Predefined routes for common movements
- **Ad-Hoc Routes**: Geographic engine for unusual or emergency routes
- **Flexibility**: Optimized for both normal and exceptional operations
- **Applications**: Large stations with complex and variable traffic patterns

### Field Equipment Interfaces

#### 1. Point Machines (Switch Machines)
**Electromechanical Point Machines**
- **Type**: AC or DC motor-driven point machines
- **Voltage**: 110V AC, 230V AC, or 24V DC typical
- **Throwing Force**: 3-10 kN depending on point type and environment
- **Throwing Time**: 3-8 seconds for point movement
- **Position Detection**: Mechanical or electrical contact detection
- **Lock Mechanism**: Mechanical lock engaged after point movement
- **Lock Verification**: Electrical contacts verify lock engagement
- **Heaters**: Electric heaters to prevent ice and snow obstruction
- **Vendors**: Voestalpine, Alstom, Siemens, Vossloh, Ansaldo STS

**Clamp Lock Point Machines**
- **Type**: Clamp-style mechanical lock for trailing-point security
- **Function**: Prevents point movement when locked
- **Detection**: Electrical contacts verify clamp lock position
- **Unlock**: Must be unlocked before point can be moved
- **Standards**: Required by some national standards for main-line points

**Hydraulic Point Machines**
- **Type**: Hydraulic actuator for heavy-duty or high-speed points
- **Throwing Force**: 10-30 kN for heavy turnouts
- **Speed**: Fast throwing time (1-3 seconds) for high-speed turnouts
- **Position Detection**: Hydraulic pressure and position sensors
- **Applications**: High-speed turnouts, heavy freight turnouts, switches in harsh environments

**Point Machine Interface**
- **Control Outputs**: Normal and reverse coil energization (AC/DC)
- **Detection Inputs**: Normal position, reverse position, lock detection
- **Current Monitoring**: Monitor motor current for obstruction detection
- **Heater Control**: Control point heater circuits based on temperature
- **Diagnostics**: Detect point machine failures, obstructions, loss of detection
- **Fail-Safe**: Prevent route setting if point position not verified

#### 2. Signal Equipment
**Color Light Signals**
- **Type**: Multi-aspect color light signals (2, 3, 4, or 5 aspect)
- **Lamp Type**: Incandescent lamps (legacy) or LED arrays (modern)
- **Voltage**: 12V, 24V, 110V AC, or 230V AC depending on design
- **Aspects**: Red (stop), yellow (caution), double-yellow (preliminary caution), green (clear)
- **Luminous Intensity**: 500-3000 cd depending on ambient light and viewing distance
- **Visibility Range**: 200-2000 meters depending on signal type and environment
- **Lamp Monitoring**: Monitor lamp current to detect lamp failures
- **Fail-Safe**: Dark or red aspect displayed on lamp failure

**LED Signal Units**
- **Technology**: LED arrays replacing incandescent lamps
- **Advantages**: Lower power consumption, longer lifespan (10-15 years), higher reliability
- **Power**: 10-30W per aspect (vs. 100-150W for incandescent)
- **Control**: Pulse-width modulation (PWM) for brightness control
- **Monitoring**: LED current monitoring and individual LED failure detection
- **Phantom Aspect Prevention**: Prevent false aspects from LED failures
- **Vendors**: Siemens, Alstom, Thales, Bombardier, GE Transportation

**Searchlight Signals (Legacy)**
- **Type**: Single incandescent lamp with rotating colored lenses
- **Mechanism**: Electromagnetic mechanism rotates lens turret
- **Advantages**: Single lamp simplifies monitoring
- **Disadvantages**: Mechanical complexity, slower aspect changes
- **Status**: Being phased out in favor of LED signals

**Dwarf Signals (Ground-Level)**
- **Type**: Low-profile signals for yard and low-speed areas
- **Height**: 0.5-1.5 meters above rail level
- **Aspects**: 2 or 3 aspects (red, yellow, green)
- **Applications**: Yard limits, shunting signals, depot areas
- **Design**: Compact weatherproof housing

#### 3. Train Detection Systems
**Track Circuits**
- **Function**: Detect train presence by electrical shunting of rail circuit
- **Types**: Audio frequency (AF), DC, AC, coded, impulse track circuits
- **Frequency Range**: 50 Hz - 10 kHz depending on track circuit type
- **Voltage**: 1-24V typical signaling voltage on rails
- **Detection Principle**: Train axles shunt track circuit, dropping relay voltage
- **Fail-Safe**: Broken rail detected as occupied section
- **Limitations**: Affected by rail contamination, poor bonding, weather conditions
- **Advantages**: Detects broken rails, well-established technology
- **Standards**: EN 50238, national standards

**Axle Counters**
- **Function**: Count axles entering and leaving track section
- **Sensors**: Inductive or magnetic sensors mounted on rails
- **Detection Principle**: Wheel passage generates pulse, compare in/out counts
- **Occupied Logic**: Section occupied if in-count > out-count
- **Reset**: Manual or automatic reset when counts balanced
- **Fail-Safe**: Report occupied on sensor failure or communication loss
- **Advantages**: Not affected by rail contamination, lower maintenance
- **Disadvantages**: Cannot detect broken rails, requires reset after faults
- **Vendors**: Frauscher, Siemens, Alstom, Thales
- **Standards**: EN 50617, CENELEC SIL 4

**Axle Counter Components**
- **Wheel Sensors**: Inductive sensors detect ferromagnetic wheel passage
- **Sensor Spacing**: 72mm standard spacing (between rails)
- **Evaluator**: Central processor counts pulses and determines occupancy
- **Communication**: Serial or field bus communication to interlocking
- **Power**: 24V DC typical, low power consumption
- **Operating Temperature**: -40°C to +70°C
- **Protection**: IP68 for trackside sensors

#### 4. Level Crossing Equipment
**Barrier Machines**
- **Type**: Electromechanical or hydraulic barrier actuators
- **Lowering Time**: 8-15 seconds (regulated by national standards)
- **Raising Time**: 6-10 seconds typical
- **Position Detection**: Reed switches or proximity sensors detect barrier position
- **Obstruction Detection**: Detect obstacles preventing barrier closure
- **Power**: 230V AC or 24V DC with battery backup
- **Fail-Safe**: Barriers remain down on power failure (with UPS)

**Warning Lights and Bells**
- **Lights**: Red flashing lights (LED) to warn road users
- **Flash Rate**: 40-60 flashes per minute (national standard)
- **Audible Warning**: Bells or electronic tones
- **Activation**: Activate before barriers lower, continue until train clears
- **Monitoring**: Monitor lamp and bell operation

**Crossing Control Logic**
- **Approach Detection**: Track circuits or axle counters detect approaching trains
- **Prediction**: Calculate crossing lowering time based on train speed
- **Strike-In Time**: Typically 25-40 seconds warning before train arrival
- **Sequential Control**: Activate warnings, lower barriers, verify closure
- **Train Clear**: Raise barriers after train clears crossing and track section
- **Fail-Safe**: Keep crossing closed on failure, alert train operator

**Road Traffic Detection**
- **Obstacle Detection**: Detect vehicles or pedestrians on crossing
- **Technologies**: Radar, lidar, induction loops, infrared sensors
- **Response**: Alert train operator, prevent barrier raising if occupied
- **Integration**: Interface with crossing control logic and interlocking

### Signaler Interface and Control

#### 1. Signaler Workstation
**Control Panel Components**
- **Track Schematic Display**: LED or LCD mimic panel showing track layout
- **Route Buttons**: Push buttons to request route setting
- **Indication Lights**: LEDs showing signal aspects, point positions, track occupancy
- **Emergency Controls**: Emergency stop buttons, emergency route cancel
- **Telephone**: Integrated communication with train crews and maintenance
- **Ergonomics**: Designed per railway human factors standards

**Graphical User Interface (GUI)**
- **Display Type**: Multi-monitor workstation with graphical track display
- **Interaction**: Mouse, keyboard, or touchscreen for route setting
- **Track Display**: Real-time track schematic with train positions
- **Route Setting**: Point-and-click route setting or keyboard commands
- **Alarms**: Visual and audible alarms for faults and conflicts
- **CCTV Integration**: Display station CCTV cameras on same workstation
- **Customization**: Configurable layouts per signaler preferences

**Control Modes**
- **Automatic Mode**: Automatic route setting based on train schedule (ARS)
- **Semi-Automatic**: Signaler confirms automatically proposed routes
- **Manual Mode**: Signaler manually sets all routes
- **Emergency Mode**: Degraded operation with restricted functionality
- **Maintenance Mode**: Access for testing and diagnostics

#### 2. Automatic Route Setting (ARS)
**Function and Operation**
- **Schedule Integration**: Interface with train timetable database
- **Automatic Decisions**: Automatically set routes based on scheduled train movements
- **Conflict Resolution**: Resolve conflicting route requests based on priorities
- **Headway Optimization**: Optimize route setting to minimize train delays
- **Regulation**: Adjust route setting to regulate train service
- **Override**: Signaler can override automatic decisions

**Performance Benefits**
- **Capacity Increase**: Improve line capacity by optimizing route setting
- **Delay Reduction**: Reduce train delays through proactive route setting
- **Workload Reduction**: Reduce signaler workload, especially during peak hours
- **Consistency**: Consistent route setting decisions
- **Safety**: Eliminate human errors in route setting

#### 3. Remote Control and Centralization
**Traffic Control Centers**
- **Centralization**: Control multiple stations from single traffic control center
- **Remote Control**: Remote signaling workstations controlling distant interlockings
- **Communication**: Fiber optic or IP networks linking control center to interlockings
- **Redundancy**: Redundant communication paths for resilience
- **Fail-Safe**: Local fallback control if communication to control center lost
- **Benefits**: Reduced staffing, improved oversight, faster response to incidents

**Distributed Interlocking**
- **Architecture**: Multiple interlocking computers distributed along line
- **Communication**: Interlockings communicate via secure data network
- **Route Coordination**: Coordinate routes spanning multiple interlocking boundaries
- **Handover**: Automatic handover of trains between interlocking areas
- **Resilience**: Failure of one interlocking does not affect others

### Safety Principles and Logic

#### 1. Fundamental Safety Rules
**Route Locking**
- **Principle**: Once route set and signal cleared, route locked until train passes
- **Approach Locking**: Route locked when train within approach locking distance
- **Time Locking**: Minimum time delay before route can be cancelled after signal cleared
- **Prevention**: Prevents route cancellation causing unsafe conditions
- **Override**: Override only allowed via explicit safety procedure

**Conflicting Route Prevention**
- **Principle**: Interlocking prevents setting of conflicting routes
- **Conflict Detection**: Analyze track occupancy and route compatibility
- **Flank Protection**: Set flank points to protect route from side collisions
- **Facing Point Lock**: Ensure facing points locked before clearing signal
- **Opposing Signals**: Prevent clearing opposing signals on same track

**Signal Aspect Sequencing**
- **Principle**: Signals display aspects according to distance to next restrictive aspect
- **Automatic**: Interlocking automatically calculates correct aspects
- **Overlap**: Ensure sufficient overlap (safe braking distance) beyond red signal
- **Approach Control**: Yellow/double-yellow aspects provide sufficient warning
- **Distant Signals**: Distant signals repeat aspect of next stop signal

**Track Occupancy Logic**
- **Detection Required**: Route can only be set if track sections available (unoccupied)
- **Continuous Monitoring**: Continuous monitoring of track occupancy during route
- **Track Clear**: Route released only when train completely clears all sections
- **Sequential Release**: Release route sections progressively as train advances
- **Fail-Safe**: Assume occupied if detection system fails

#### 2. Fail-Safe Design Principles
**Safety Processor Architecture**
- **Redundancy**: Dual or triple redundant processors with voting or comparison
- **Diversity**: Different processor types to prevent common-cause failures
- **Self-Diagnostics**: Continuous self-testing with >95% fault coverage
- **Watchdogs**: Hardware and software watchdogs detect processor failures
- **Safe Outputs**: Fail to safe state (restrictive) on processor failure
- **Standards**: EN 50129 fail-safe computer requirements

**Vital Relay Outputs**
- **Relay Logic**: Safety-critical outputs controlled via vital relays
- **Relay Voting**: Multiple relay contacts in series for fail-safe output
- **Contact Monitoring**: Monitor relay contact position for failures
- **Fail-Safe**: De-energized relays produce safe state (signals red, points locked)
- **Proven Technology**: Relay logic has proven reliability record

**Field Equipment Interfaces**
- **Wired Connections**: Hardwired connections to critical field equipment
- **Redundant Circuits**: Duplicate wiring for critical functions
- **Supervision**: Continuous supervision of field equipment status
- **Fault Detection**: Detect wire breaks, short circuits, field equipment failures
- **Fail-Safe**: Assume safe state on communication or equipment failure

**Software Safety**
- **Development Process**: Rigorous development per EN 50128 (SIL 4 software)
- **Verification**: Independent verification and validation
- **Static Analysis**: Automated static code analysis to detect errors
- **Testing**: Extensive testing including formal methods and simulation
- **Change Control**: Strict change control and version management
- **Certification**: Independent assessment by notified body

#### 3. Degraded Mode Operation
**Interlocking Failure Modes**
- **Partial Failure**: Isolate failed components, continue with reduced capacity
- **Communication Loss**: Local control if communication to control center lost
- **Detection Failure**: Assume track occupied, operate with restricted routes
- **Complete Failure**: Revert to emergency procedures, manual signaling

**Emergency Procedures**
- **Telephone Block**: Manual block working using telephone authorization
- **Pilotman**: Physical token or authority for single-line sections
- **Absolute Block**: Manual absolute block for double-track sections
- **Speed Restrictions**: Impose speed restrictions during degraded operation
- **Signaler Authority**: Signaler issues written authorities to train drivers

### Integration with Train Control Systems

#### 1. ETCS Integration
**ETCS Level 1 Interface**
- **Balise Data**: Interlocking provides movement authority data to Lineside Electronic Units (LEU)
- **LEU Interface**: Digital interface between interlocking and LEU (SUBSET-040)
- **Telegram Selection**: Interlocking commands LEU to select appropriate balise telegrams
- **Signal Aspects**: Balise data reflects current signal aspect and route
- **Real-Time**: Telegram updates within <1 second of signal aspect change
- **Safety**: Safety-critical interface per CENELEC SIL 4

**ETCS Level 2 Interface**
- **RBC Interface**: Interlocking interfaces with Radio Block Centre (RBC)
- **Movement Authority**: Interlocking provides track availability to RBC
- **Route Status**: Real-time route and track occupancy status
- **Point Position**: Point positions communicated to RBC
- **Timely Updates**: Sub-second updates for safety-critical data
- **Standards**: SUBSET-098 (RBC-interlocking interface)

**ETCS Level 3 Considerations**
- **Train Integrity**: Interlocking relies on train-reported integrity
- **Moving Block**: No fixed block sections, dynamic separation
- **Reduced Trackside**: Fewer track circuits or axle counters required
- **Future Development**: ETCS Level 3 specifications under development

#### 2. ATP/ATC Integration
**National ATP Systems**
- **Interface Types**: Digital I/O, serial communication, or dedicated protocols
- **Data Provided**: Route status, signal aspects, speed limits, track occupancy
- **Continuous Update**: Real-time updates to ATP/ATC systems
- **Safety Integrity**: Safety-critical interface per national standards
- **Examples**: LZB (Germany), TVM (France), ATB (Netherlands), SCMT (Italy)

**CBTC Integration**
- **Zone Controller Interface**: Interlocking interfaces with CBTC Zone Controllers
- **Route Requests**: CBTC requests routes from interlocking for train movements
- **Point Control**: Interlocking controls points, CBTC manages train separation
- **Track Occupancy**: CBTC provides train position, interlocking monitors detection
- **Hybrid Systems**: Combination of traditional interlocking and CBTC train control

### Vendors and Products

#### 1. Major Interlocking Suppliers
**Siemens Mobility**
- **Product**: Simis (Siemens Interlocking System)
- **Variants**: Simis D, Simis W, Simis S7, Simis Vicos
- **Architecture**: Geographic and route-based interlocking
- **Capacity**: Small to very large installations (10-500+ objects)
- **Certifications**: CENELEC SIL 4, EN 50126/128/129, national approvals
- **Installations**: Worldwide installations in Europe, Asia, Americas
- **Support**: Global service network, 24/7 support

**Alstom (including Bombardier Transportation)**
- **Product**: Smartlock (formerly EBI Lock)
- **Architecture**: Object-oriented geographic interlocking
- **Capacity**: Modular scalability for all station sizes
- **Features**: EULYNX-compliant interfaces, modern graphical engineering
- **Certifications**: ERA approval, CENELEC SIL 4, multiple national approvals
- **Installations**: Major European installations including UK, France, Germany
- **Support**: European service centers, technical training

**Thales Ground Transportation Systems**
- **Product**: Thales Interlocking System
- **Architecture**: Geographic and route-based variants
- **Features**: Modular design, easy expansion, legacy integration
- **Certifications**: Multiple national approvals, CENELEC SIL 4
- **Installations**: France, Netherlands, UK, international projects
- **Support**: Regional support centers, remote diagnostics

**Hitachi Rail (Ansaldo STS)**
- **Product**: ACC (Advanced Computer-Based Interlocking)
- **Architecture**: Object-oriented modular design
- **Features**: Geographic interlocking, SCADA integration
- **Certifications**: CENELEC SIL 4, Italian and international approvals
- **Installations**: Italy, Middle East, Asia-Pacific
- **Support**: Regional service centers

**CAF (Construcciones y Auxiliar de Ferrocarriles)**
- **Product**: ENCLAVITREN interlocking system
- **Architecture**: Route-based and geographic interlocking
- **Focus**: Spanish and Latin American markets
- **Certifications**: Spanish ADIF certification, SIL 4
- **Installations**: Spain, Portugal, Latin America

#### 2. Relay Interlocking Suppliers (Legacy)
**Westinghouse (now Alstom)**
- **Type**: Relay interlocking systems
- **Status**: Legacy systems still in operation
- **Maintenance**: Spare parts and maintenance support available

**General Railway Signal (GRS)**
- **Type**: Relay interlocking systems
- **Status**: Large installed base in North America
- **Migration**: Many being replaced with electronic interlockings

**Union Switch & Signal (US&S, now Alstom)**
- **Type**: Relay interlocking systems
- **Status**: Widely deployed in North America
- **Support**: Ongoing support and spare parts

### Installation and Commissioning

#### 1. Engineering and Design Phase
**Interlocking Design**
- **Track Layout**: Define track topology, signals, points, detection sections
- **Route Table**: Define all possible routes (route-based) or geographic data model
- **Control Table**: Specify control sequences for each route
- **Timing Parameters**: Define locking times, approach distances, clearing times
- **Safety Rules**: Implement conflict prevention, flank protection, approach locking
- **Testing**: Extensive simulation and formal verification of logic

**Interface Design**
- **Field Equipment**: Define interfaces to points, signals, detection, level crossings
- **Train Control**: Design interfaces to ETCS, ATP, CBTC systems
- **Signaler Interface**: Design control panels or graphical workstations
- **Adjacent Systems**: Define interfaces to neighboring interlockings
- **Standards Compliance**: Verify compliance with EN 50126/128/129 and national standards

**Safety Case**
- **Hazard Analysis**: Systematic hazard identification and risk assessment
- **Fault Tree Analysis**: Quantitative analysis of failure modes
- **FMEA**: Failure Modes and Effects Analysis for all components
- **Safety Requirements**: Define safety requirements and verification methods
- **Independent Assessment**: Third-party safety assessment per EN 50129

#### 2. Installation Phase
**Equipment Room Installation**
- **Racks and Cabinets**: Install 19" equipment racks in signaling equipment room
- **Interlocking Computer**: Install redundant interlocking computers
- **Object Controllers**: Install point, signal, and detection controllers
- **Power Supply**: Install UPS and redundant power supplies
- **Cabling**: Install control cabling to field equipment (conduits, cable trays)
- **Grounding**: Proper grounding and lightning protection per EMC standards

**Field Equipment Installation**
- **Signals**: Install signals at designed locations along track
- **Point Machines**: Install and align point machines on turnouts
- **Detection Equipment**: Install track circuits or axle counters
- **Level Crossings**: Install barriers, lights, detection equipment
- **Cabling**: Run cables from field equipment to equipment room

#### 3. Testing and Commissioning
**Static Testing**
- **Factory Testing**: Component testing at manufacturer facilities
- **Integration Testing**: Verify interfaces between subsystems
- **Control Sequence Testing**: Test all route setting sequences
- **Safety Function Testing**: Verify all safety functions (conflicts, locking, detection)
- **Failure Mode Testing**: Test behavior under simulated failures
- **Documentation**: Test reports documenting all test results

**Dynamic Testing**
- **Field Equipment Testing**: Test signals, points, detection with actual trains
- **Route Setting**: Test all routes with train movements
- **Degraded Mode**: Test operation under simulated failures
- **Emergency Procedures**: Test emergency override and degraded operation
- **Performance**: Verify route setting times, system response times
- **Integration**: Test with train control systems (ETCS, ATP)

**Validation and Approval**
- **Safety Validation**: Independent safety validation per EN 50129
- **Signaling Principles**: Verify compliance with signaling principles
- **Rule Book**: Verify compliance with operating rule book
- **Regulatory Approval**: Obtain approval from national railway safety authority
- **Commissioning**: Gradual commissioning with trial operations before full service

### Maintenance and Lifecycle

#### 1. Preventive Maintenance
**Scheduled Maintenance**
- **Frequency**: Monthly to annual depending on equipment type
- **Interlocking Computer**: Review logs, backup data, test failover, software updates
- **Object Controllers**: Test control outputs, verify monitoring functions
- **Field Equipment**: Inspect signals, points, detection equipment, level crossings
- **Cabling**: Visual inspection for damage, insulation testing
- **UPS Batteries**: Test battery capacity, replace aged batteries

**Condition Monitoring**
- **Real-Time Monitoring**: Continuous monitoring of interlocking health
- **Diagnostics**: Review diagnostic logs for early failure warnings
- **Performance Metrics**: Track route setting times, failure rates
- **Predictive Maintenance**: Predict failures based on trending data
- **Remote Monitoring**: Remote diagnostics via secure network connection

#### 2. Corrective Maintenance
**Fault Detection and Diagnosis**
- **Automatic Alarms**: Real-time alarms for detected faults
- **Fault Localization**: Diagnostics isolate faults to specific components
- **Remote Diagnosis**: Remote diagnosis by support engineers
- **Spare Parts**: Maintain inventory of critical spare parts
- **Redundancy**: Automatic switchover to redundant systems during maintenance

**Common Failure Modes and Repairs**
- **Point Machine Failure**: Motor failure, obstruction, detection loss (replace or repair point machine)
- **Signal Lamp Failure**: Lamp burnout (replace lamp or LED unit)
- **Track Circuit Failure**: Broken bonds, insulation failure (repair track circuit)
- **Axle Counter Failure**: Sensor damage, evaluator failure (replace sensor or evaluator)
- **Computer Failure**: Processor fault, power supply failure (automatic failover, replace failed unit)
- **Communication Failure**: Cable damage, interface failure (repair cable, replace interface card)

**Repair Process**
- **Fault Notification**: Automatic alarm or signaler report
- **Diagnosis**: Determine failure mode using diagnostics
- **Isolation**: Isolate faulty component if possible (continue with degraded operation)
- **Repair**: Replace line-replaceable unit (LRU) or repair in-situ
- **Testing**: Functional testing after repair
- **Documentation**: Record repair in maintenance management system

#### 3. System Upgrades and Migration
**Software Upgrades**
- **Security Patches**: Apply software security updates
- **Functionality Updates**: New features and improvements
- **Configuration Changes**: Modify routes, add objects, adjust parameters
- **Testing Required**: Revalidation testing after software changes
- **Approval**: Regulatory approval may be required for significant changes

**Hardware Refresh**
- **Obsolescence**: Replace aging computers and components
- **Capacity Expansion**: Add controllers for new track sections or objects
- **Technology Upgrade**: Migrate to newer interlocking platform
- **Phased Migration**: Incremental migration to minimize disruption

**Legacy System Replacement**
- **Relay to Electronic**: Replace relay interlockings with electronic systems
- **Parallel Operation**: Operate new system in parallel during transition (if feasible)
- **Cut-Over**: Planned cut-over during track possession
- **Testing**: Extensive testing before putting into service
- **Training**: Comprehensive training for signalers and maintainers

### Standards and Certifications

#### 1. European Standards (CENELEC)
**EN 50126 - Railway Applications: Specification and Demonstration of Reliability, Availability, Maintainability and Safety (RAMS)**
- **Purpose**: Framework for RAMS throughout system lifecycle
- **Application**: Interlocking RAMS requirements and verification
- **Methods**: Reliability modeling, availability calculation, safety assessment

**EN 50128 - Railway Applications: Software for Railway Control and Protection Systems**
- **Purpose**: Software development and verification for safety systems
- **SIL 4 Requirements**: Rigorous development process for SIL 4 software
- **Methods**: Formal methods, static analysis, extensive testing
- **Documentation**: Complete software lifecycle documentation

**EN 50129 - Railway Applications: Safety-Related Electronic Systems for Signaling**
- **Purpose**: Safety requirements for electronic signaling systems
- **Safety Case**: Comprehensive safety case requirements
- **Fail-Safe Principles**: Design principles for fail-safe systems
- **Independent Assessment**: Third-party assessment requirements

**EN 50159 - Railway Applications: Communication, Signaling and Processing Systems - Safety-Related Communication in Transmission Systems**
- **Purpose**: Secure communication for safety-critical data
- **Application**: Interlocking communication interfaces
- **Methods**: Cryptography, timestamps, sequence numbers, integrity checks

#### 2. National Standards and Regulations
**UK Railway Standards**
- **Railway Group Standards (RGS)**: Comprehensive UK signaling standards
- **ROGS (Railways and Other Guided Transport Systems)**: UK safety regulations
- **Approval**: UK Railway Safety and Standards Board (RSSB) approval required

**German Railway Standards**
- **EBA (Eisenbahn-Bundesamt)**: German railway authority approval
- **VV BAU (Verwaltungsvorschrift Bau)**: German construction standards
- **Ril 819 (Richtlinie 819)**: Interlocking principles and requirements

**French Railway Standards**
- **RFN (Réseau Ferré National)**: French railway infrastructure standards
- **SNCF IN-xxx**: SNCF interlocking and signaling standards
- **EPSF (Établissement Public de Sécurité Ferroviaire)**: French safety authority approval

**North American Standards**
- **AREMA (American Railway Engineering and Maintenance-of-Way Association)**: Railway engineering standards
- **AAR (Association of American Railroads)**: Railway equipment standards
- **FRA (Federal Railroad Administration)**: US regulatory approval

## Related Topics
- kb/sectors/transportation/equipment/device-eurobalise-20251105-18.md
- kb/sectors/transportation/equipment/device-etcs-onboard-20251105-18.md
- kb/sectors/transportation/equipment/product-line-trainguard-20251105-18.md
- kb/sectors/transportation/equipment/device-atp-system-20251105-18.md

## References
- [Railway Signaling Resource](https://www.railway-signaling.eu/) - Comprehensive signaling and interlocking information
- [European Union Agency for Railways (ERA)](https://www.era.europa.eu/) - European railway standards and technical specifications
- [Institution of Railway Signal Engineers (IRSE)](https://www.irse.org/) - Professional body for railway signaling engineers

## Metadata
- Last Updated: 2025-11-05 18:00:00
- Research Session: Transportation Equipment Research
- Completeness: 95%
- Next Actions: Document EULYNX standardized interfaces, explore modern geographic interlocking algorithms
