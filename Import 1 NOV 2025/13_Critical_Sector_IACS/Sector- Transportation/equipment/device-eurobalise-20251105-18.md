---
title: Eurobalise Equipment Specification
date: 2025-11-05 18:00:00
category: sectors
subcategory: equipment
sector: transportation
tags: [eurobalise, etcs, railway-signaling, balise, train-control, telecommunications]
sources: [https://www.era.europa.eu/, https://www.etcs.org/, https://www.railwaygazette.com/]
confidence: high
---

## Summary
Eurobalise is a standardized railway telecommunications device used in European Train Control System (ETCS) implementations for trackside-to-train data transmission. These ground-based transponders provide critical positioning information, speed restrictions, and movement authorities to passing trains through magnetic inductive coupling. Operating at 27.095 MHz uplink frequency and 4.234 MHz downlink frequency, Eurobalises enable precise train localization and safe operation in both fixed and switchable configurations. The system provides fail-safe, interference-resistant communication compliant with SUBSET-036 specifications and CENELEC SIL 4 safety standards, making it fundamental infrastructure for European interoperable railway networks.

## Key Information
- **Equipment Type**: Ground-based transponder/beacon (Eurobalise)
- **Standards**: SUBSET-036, EN 50129, EN 50126, EN 50128, CENELEC SIL 4
- **Operating Frequencies**: 27.095 MHz uplink (train to balise), 4.234 MHz downlink (balise to train)
- **Communication Range**: 1.5-4 meters vertical separation, effective at speeds up to 500 km/h
- **Installation**: Mounted between rails or beside track centerline
- **Operating Environment**: -40°C to +70°C, IP68 protection, vibration resistant
- **Applications**: ETCS Level 1, Level 2, Level 3, positioning reference, speed control, movement authority

## Technical Details
### Eurobalise Architecture

#### 1. Physical Characteristics
**Housing and Construction**
- **Dimensions**: Approximately 300mm x 300mm x 80mm (typical installation envelope)
- **Weight**: 4-6 kg depending on model and manufacturer
- **Material**: Reinforced polyurethane or fiberglass-reinforced composite
- **Protection Rating**: IP68 (complete dust tight, continuous immersion up to 3 meters)
- **Impact Resistance**: Designed to withstand ballast impacts and track maintenance equipment
- **Mounting**: Track-mounted (between rails) or offset mounted (beside track)
- **Lifespan**: 15-25 years with minimal maintenance
- **Color Coding**: Yellow housing (fixed data), red housing (switchable data) for visual identification

**Environmental Specifications**
- **Operating Temperature**: -40°C to +70°C ambient
- **Storage Temperature**: -50°C to +85°C
- **Humidity**: 5% to 100% RH with condensation
- **Vibration Resistance**: Compliant with EN 50155 railway vibration standards
- **Shock Resistance**: Withstands rail traffic loads and track maintenance
- **UV Resistance**: UV-stabilized materials for outdoor installation
- **Chemical Resistance**: Resistant to oil, diesel, cleaning agents, de-icing salts

**Installation Requirements**
- **Mounting Surface**: Concrete sleepers, wooden sleepers, or slab track
- **Track Gauge**: Standard gauge (1435mm) typical, adaptable for other gauges
- **Vertical Position**: 100-150mm below rail level (track-center mounting)
- **Horizontal Position**: ±75mm tolerance from track centerline
- **Cable Entry**: IP68 sealed cable glands for power and data connections
- **Accessibility**: Removable cover for maintenance access without special tools

#### 2. Electronic Systems
**Radio Frequency Module**
- **Uplink Frequency**: 27.095 MHz ±100 kHz (train antenna to balise)
- **Downlink Frequency**: 4.234 MHz ±100 kHz (balise to train antenna)
- **Modulation**: FSK (Frequency Shift Keying) for robust data transmission
- **Data Rate**: 564.48 kbps uplink telegram activation
- **Transmission Power**: Compliant with ETSI electromagnetic emission standards
- **Antenna**: Internal loop antenna with magnetic coupling
- **Coupling Range**: Effective communication 1.5-4 meters vertical separation
- **Speed Capability**: Reliable data transfer up to 500 km/h train speed

**Processing and Memory**
- **Microcontroller**: Fail-safe processor with dual-channel redundancy
- **Data Storage**: Non-volatile EEPROM or flash memory for telegram storage
- **Telegram Capacity**: Typically 1023 bits per telegram (variable message length)
- **Programming Interface**: Standardized programming interface per SUBSET-036
- **Diagnostic Memory**: Stores operational statistics and fault records
- **Configuration Storage**: Retains configuration data through power loss
- **Safety Validation**: CRC-16 and safety code validation on all telegrams

**Power Supply**
- **External Power**: 24V DC nominal (18-36V DC range) for switchable balises
- **Power Consumption**: 5-15W depending on configuration and operating mode
- **Energy Harvesting**: Fixed balises derive power from passing train antenna field
- **Battery Backup**: Not required for fixed balises; optional for switchable types
- **Power Protection**: Transient voltage suppression, reverse polarity protection
- **Power Monitoring**: Diagnostic outputs for power supply status
- **Standards**: EN 50155 railway power supply requirements

**Interface Connections**
- **LEU Connection**: RS-485, CAN bus, or Ethernet interface to Lineside Electronic Unit
- **Diagnostic Port**: RS-232 or USB interface for maintenance and programming
- **Signal Inputs**: Digital inputs for switch position, route setting (switchable types)
- **Status Outputs**: Relay contacts or digital outputs for health monitoring
- **Cable Types**: Shielded twisted pair, fiber optic for EMI-sensitive environments
- **Connector Types**: Industrial railway-grade connectors (IP67/IP68 rated)

#### 3. Operational Modes
**Fixed Balise Operation**
- **Function**: Transmit static telegram data on every train passage
- **Activation**: Powered by magnetic field from passing train antenna
- **Data Content**: Position reference, gradient, speed limits, static track data
- **Telegram Frequency**: One telegram per passage (typically 2-3 telegrams/balise group)
- **Power Source**: Energy harvesting from train antenna electromagnetic field
- **Reliability**: No external power required, minimal failure modes
- **Applications**: Position reference points, fixed speed restrictions, level crossings
- **Standards**: SUBSET-036 telegram format, SUBSET-044 balise filling rules

**Switchable Balise Operation**
- **Function**: Transmit variable telegram data based on route and signal state
- **Activation**: Powered by 24V DC external supply and train antenna field
- **Data Content**: Variable movement authorities, temporary speed restrictions, route-specific data
- **Telegram Selection**: Multiple pre-stored telegrams selected by LEU commands
- **Switching Time**: <100ms response time to LEU switching commands
- **Power Source**: External 24V DC supply with power supervision
- **Reliability**: Fail-safe telegram selection, default safe telegram on power loss
- **Applications**: Signal aspects, route-dependent data, temporary restrictions
- **Standards**: SUBSET-036, SUBSET-044, SUBSET-040 (LEU interface)

**Diagnostic and Maintenance Mode**
- **Function**: Enable testing, programming, and diagnostics
- **Access Method**: Physical connection via diagnostic port
- **Operations**: Telegram programming, read-out, transmission tests
- **Monitoring**: Read operational statistics, transmission counts, error logs
- **Reprogramming**: Field-updateable telegram data without replacement
- **Verification**: Transmission quality testing with portable test equipment
- **Security**: Password-protected access, audit logging of changes
- **Tools**: Manufacturer-specific or generic SUBSET-036 compatible tools

### Telegram Structure and Data

#### 1. Telegram Format (SUBSET-036)
**Telegram Components**
- **Header**: 210 bits fixed format with balise identification
- **User Data**: Up to 830 bits variable-length data packets
- **Safety Layer**: 110 bits including CRC and safety code
- **Total Length**: Variable up to 1023 bits depending on information content
- **Bit Encoding**: Manchester encoding for clock recovery
- **Error Detection**: CRC-16 polynomial for data integrity
- **Safety Code**: Cryptographic safety code per SUBSET-036 Appendix A

**National Values and Packets**
- **Packet 0**: Virtual balise cover marker
- **Packet 3**: National values (braking curves, train categories)
- **Packet 5**: Link to balise in group
- **Packet 12**: Level 1 movement authority
- **Packet 21**: Gradient profile
- **Packet 27**: International static speed profile
- **Packet 41**: Level transition order
- **Packet 44**: Data used by applications outside ETCS
- **Packet 255**: End of information

**Balise Group Configuration**
- **Group Size**: Typically 1-8 balises per group (3 balises typical)
- **Spacing**: Balises spaced 3-6 meters apart within group
- **Redundancy**: Multiple balises ensure reliable detection at all speeds
- **Linking**: Balises linked through Packet 5 data (N_PIG and N_TOTAL)
- **Identification**: Unique balise group ID and individual balise position
- **Orientation**: Balises configured for nominal and reverse running directions
- **Consistency**: All balises in group must have consistent timestamp and data

#### 2. Data Content Examples
**Position Reference Telegram**
- **Packet 5**: Link information (balise 2 of 3 in group)
- **Packet 44**: Balise group identifier (NID_BG) for absolute positioning
- **Packet 21**: Gradient profile for next 5 kilometers
- **Packet 27**: Permanent speed restrictions ahead
- **Typical Length**: 400-600 bits
- **Use Case**: Train position calibration every 1-2 kilometers

**Movement Authority Telegram**
- **Packet 12**: End of authority at kilometer 45+750, overlap 200m
- **Packet 21**: Gradient profile to end of authority
- **Packet 27**: Speed profile with temporary restrictions
- **Packet 80**: Mode profile (e.g., Staff Responsible mode at station)
- **Typical Length**: 600-900 bits
- **Use Case**: ETCS Level 1 signal-based movement authority

**Level Transition Telegram**
- **Packet 41**: Transition to ETCS Level 2 at kilometer 50+000
- **Packet 44**: RBC identity and contact information (phone number, RBC ID)
- **Packet 3**: National values for Level 2 operation
- **Typical Length**: 500-700 bits
- **Use Case**: Transition from Level 1 to Level 2 operation

### Integration with ETCS Systems

#### 1. Train-Side Equipment
**Balise Transmission Module (BTM)**
- **Function**: Receive and decode Eurobalise telegrams on-board train
- **Antenna**: Two antennas mounted under leading vehicle (redundancy)
- **Antenna Spacing**: 3-4 meters apart to ensure balise group detection
- **Reception Range**: Effective up to 500 km/h train speed
- **Processing**: Telegram decoding, CRC validation, safety code verification
- **Output**: Validated data to European Vital Computer (EVC)
- **Standards**: SUBSET-036, SUBSET-040, SUBSET-041
- **Vendors**: Alstom, Bombardier, Siemens, Thales

**European Vital Computer (EVC)**
- **Function**: Process balise data and manage ETCS train operation
- **Input Processing**: Validate balise telegrams against onboard data
- **Position Calculation**: Determine train position using balise position reference
- **Speed Supervision**: Calculate permitted speed and braking curves
- **Mode Management**: Handle level transitions and operating modes
- **Driver Interface**: Display information on Driver Machine Interface (DMI)
- **Safety Level**: CENELEC SIL 4 certified
- **Standards**: SUBSET-026, SUBSET-091, SUBSET-108

#### 2. Trackside Equipment
**Lineside Electronic Unit (LEU)**
- **Function**: Control switchable balises based on interlocking commands
- **Interface to Interlocking**: Digital inputs, relay contacts, serial interface
- **Balise Control**: Select appropriate telegram based on route/signal state
- **Telegram Switching**: <100ms response to interlocking state changes
- **Monitoring**: Continuous supervision of balise health and power
- **Diagnostics**: Report balise failures to maintenance systems
- **Power Supply**: 110/230V AC input, 24V DC output to balises
- **Standards**: SUBSET-036, SUBSET-040, SUBSET-085

**Interlocking System**
- **Function**: Provide route and signal state information to LEU
- **Interface Types**: Relay outputs, digital outputs, serial communication
- **Data Provided**: Signal aspect, route setting, temporary speed restrictions
- **Safety Requirements**: Fail-safe outputs, CENELEC SIL 4
- **Integration**: Coordinated with signaling, track circuits, point machines
- **Legacy Systems**: Interface modules for relay-based interlockings
- **Modern Systems**: Direct digital integration with electronic interlockings

**Diagnostic and Monitoring Tools**
- **Portable Balise Reader**: Handheld device to read balise telegrams
- **Onboard Recorder**: Record all balise telegrams during test runs
- **Track-Side Tester**: Simulate train passage to verify balise transmission
- **LEU Diagnostics**: Monitor balise health, transmission statistics
- **Remote Monitoring**: SCADA integration for balise group status
- **Maintenance Planning**: Predict failures based on operational statistics

### Vendors and Models

#### 1. Major Eurobalise Manufacturers
**Alstom (formerly Bombardier Transportation)**
- **Model**: EBI Balise 200
- **Type**: Fixed and switchable configurations
- **Features**: Compact design, field-programmable, proven reliability
- **Certifications**: SUBSET-036 compliant, CENELEC SIL 4
- **Installations**: Thousands of installations across Europe
- **Support**: Global support network, spare parts availability
- **Compatibility**: Interoperable with all ETCS onboard equipment

**Siemens Mobility**
- **Model**: Eurobalise ZUB 200 series
- **Type**: Fixed (ZUB 221) and switchable (ZUB 222)
- **Features**: Rugged construction, easy installation, diagnostic capabilities
- **Certifications**: ERA approval, CENELEC SIL 4, SUBSET-036
- **Installations**: Extensive installations in Germany, Austria, Switzerland
- **Support**: European service centers, technical training programs
- **Compatibility**: Compatible with all ETCS BTM systems

**Thales Ground Transportation Systems**
- **Model**: Thales Eurobalise
- **Type**: Fixed and switchable variants
- **Features**: High-reliability design, extended lifespan, remote diagnostics
- **Certifications**: Multiple national approvals, SUBSET-036, SIL 4
- **Installations**: Major installations in France, Spain, Netherlands
- **Support**: Regional maintenance centers, 24/7 technical support
- **Compatibility**: Proven interoperability with diverse rolling stock

**Mermec Group (part of Angel Trains)**
- **Model**: D50 Eurobalise
- **Type**: Fixed and switchable balise transponders
- **Features**: Modular design, quick installation, field-serviceable
- **Certifications**: ERA type approval, SUBSET-036, SIL 4
- **Installations**: Growing installations in Southern Europe
- **Support**: Service network across Italy and Spain
- **Compatibility**: Full ETCS compatibility verified in multi-vendor projects

#### 2. Lineside Electronic Units (LEU)
**Alstom EBI Switch**
- **Capacity**: Up to 64 switchable balise outputs
- **Interface**: Relay inputs, serial communication, Ethernet
- **Power**: Redundant power supply, battery backup option
- **Diagnostics**: Comprehensive balise monitoring and diagnostics
- **Certifications**: SUBSET-040, CENELEC SIL 4

**Siemens L200**
- **Capacity**: Modular design, 8-64 balise connections
- **Interface**: Digital inputs, PROFIBUS, Ethernet/IP
- **Power**: 110/230V AC, integrated 24V DC balise power
- **Diagnostics**: Remote diagnostics, SCADA integration
- **Certifications**: SUBSET-040, ERA approval

**Thales LEU-E**
- **Capacity**: 16-96 balise control channels
- **Interface**: Relay, digital, serial, fiber optic options
- **Power**: Redundant hot-swap power supplies
- **Diagnostics**: Built-in test, remote monitoring
- **Certifications**: Multiple national approvals, SIL 4

### Installation and Configuration

#### 1. Installation Process
**Site Preparation**
- **Survey**: Verify installation locations per signaling design
- **Track Possession**: Coordinate installation with track maintenance windows
- **Foundation**: Prepare mounting surface on sleepers or slab track
- **Cable Routing**: Install conduits and cables for switchable balises
- **Safety**: Establish protection zones, warning signs, lockout procedures

**Physical Installation**
- **Positioning**: Mount balise at specified chainage with ±75mm tolerance
- **Alignment**: Ensure balise centerline aligned with track centerline
- **Securing**: Bolt balise housing to mounting brackets or sleepers
- **Cable Connection**: Connect LEU cables through IP68 cable glands
- **Sealing**: Verify IP68 integrity of all cable entries
- **Marking**: Install balise markers for maintenance visibility

**Programming and Commissioning**
- **Telegram Programming**: Load telegram data per SUBSET-044 design rules
- **Verification**: Read back telegram data to verify correct programming
- **Functional Testing**: Verify transmission using portable test equipment
- **Integration Testing**: Conduct test runs with equipped train
- **LEU Integration**: Configure LEU telegram switching for switchable balises
- **Documentation**: Record installation parameters, test results, telegram checksums

#### 2. Configuration Management
**Telegram Design**
- **Design Tool**: Use specialized ETCS design software for telegram creation
- **Design Rules**: Follow SUBSET-044 rules for consistent data
- **Safety Validation**: Verify safety code generation per SUBSET-036 Appendix A
- **Consistency Checks**: Ensure consistency across balise groups
- **Version Control**: Maintain telegram database with revision history

**Database Management**
- **Central Database**: Maintain authoritative telegram database
- **Change Control**: Formal approval process for telegram modifications
- **Traceability**: Link telegrams to signaling design documents
- **Backup**: Regular backups of telegram database
- **Audit Trail**: Log all changes to telegram data

**Field Updates**
- **Update Procedure**: Documented procedure for telegram updates
- **Authorization**: Formal authorization required for field changes
- **Testing**: Mandatory testing after any telegram change
- **Rollback**: Ability to restore previous telegram version
- **Documentation**: Update installation records after changes

### Safety Certifications and Standards

#### 1. Safety Integrity Level (SIL)
**CENELEC SIL 4 Requirements**
- **Failure Rate**: <10^-9 dangerous failures per hour
- **Redundancy**: Dual-channel processing with comparison
- **Self-Testing**: Continuous self-diagnostics during operation
- **Safe Failure**: Failure modes result in safe state (no transmission or safe telegram)
- **Certification**: Independent safety assessment per EN 50129
- **Documentation**: Complete safety case with fault tree analysis

**Safety Functions**
- **Data Integrity**: CRC-16 validation prevents corrupted telegrams
- **Telegram Authentication**: Safety code prevents spoofing attacks
- **Position Validation**: Multiple balises in group provide redundancy
- **Fail-Safe Design**: Missing or corrupted data triggers emergency braking
- **Power Supervision**: Switchable balises default to safe telegram on power loss

#### 2. Electromagnetic Compatibility
**EMC Standards**
- **Emission**: EN 50121-3-1 (railway rolling stock emissions)
- **Immunity**: EN 50121-3-2 (railway fixed installations immunity)
- **Testing**: Conducted and radiated emission/immunity tests
- **Protection**: Shielding, filtering, and grounding per EMC requirements

**Interference Mitigation**
- **Frequency Selection**: 4.234 MHz and 27.095 MHz chosen to avoid interference
- **Shielding**: Internal RF shielding prevents external interference
- **Filtering**: Power supply filtering prevents conducted interference
- **Grounding**: Proper grounding prevents EMI coupling

### Maintenance Requirements

#### 1. Preventive Maintenance
**Periodic Inspections**
- **Frequency**: Annual visual inspection minimum
- **Inspection Points**: Housing integrity, cover seal, cable connections
- **Cleaning**: Remove debris, vegetation, accumulated ballast
- **Telegram Verification**: Test read telegram data every 2-3 years
- **Transmission Testing**: Verify transmission quality using test equipment
- **Documentation**: Record inspection findings and maintenance actions

**Predictive Maintenance**
- **Operational Statistics**: Monitor transmission counts, error rates
- **Trend Analysis**: Identify degrading balises before failure
- **Condition Monitoring**: Remote monitoring of switchable balise health
- **Replacement Planning**: Plan replacements based on age and condition

#### 2. Corrective Maintenance
**Common Failure Modes**
- **Water Ingress**: Damaged seals allow moisture entry (replace seals/balise)
- **Cable Damage**: Track maintenance damage to cables (repair/replace cables)
- **Lightning Damage**: Nearby lightning strikes damage electronics (replace balise)
- **Memory Corruption**: Rare EEPROM failures (reprogram or replace)
- **Antenna Failure**: Physical damage to internal antenna (replace balise)

**Fault Detection**
- **Train Reports**: Drivers report missing balise detections
- **LEU Diagnostics**: LEU reports balise communication failures
- **Onboard Recorders**: Balise transmission quality analysis
- **Test Trains**: Dedicated test trains with diagnostic equipment

**Repair Process**
- **Diagnosis**: Determine failure mode using test equipment
- **Access**: Obtain track possession for safe access
- **Replacement**: Replace failed balise or repair cables
- **Testing**: Verify correct operation using portable tester
- **Validation**: Conduct test run with equipped train
- **Documentation**: Update maintenance records

### Lifecycle and Replacement

#### 1. Expected Lifespan
**Design Life**
- **Typical Lifespan**: 15-25 years depending on environment
- **Track-Mounted**: Higher wear due to vibration and ballast impacts
- **Offset-Mounted**: Longer life due to reduced mechanical stress
- **Harsh Environments**: Shorter life in coastal or industrial areas
- **Maintenance Impact**: Proper maintenance significantly extends lifespan

**End-of-Life Indicators**
- **Increasing Failures**: Rising failure rate indicates end of life
- **Housing Degradation**: Cracked or UV-damaged housing
- **Seal Failures**: Repeated water ingress issues
- **Obsolescence**: Difficulty obtaining spare parts
- **Technology Upgrade**: System-wide ETCS upgrades

#### 2. Replacement Strategy
**Planned Replacement**
- **Age-Based**: Replace balises after 20-25 years regardless of condition
- **Condition-Based**: Replace when condition monitoring indicates degradation
- **System Upgrade**: Replace during ETCS system upgrades
- **Track Renewal**: Replace during major track renewal projects

**Disposal and Recycling**
- **Material Recovery**: Separate metal, plastic, and electronic components
- **Electronic Waste**: Dispose electronics per WEEE directive
- **Environmental**: Follow environmental regulations for disposal
- **Security**: Erase telegram data before disposal

## Related Topics
- kb/sectors/transportation/equipment/device-etcs-onboard-20251105-18.md
- kb/sectors/transportation/equipment/product-line-trainguard-20251105-18.md
- kb/sectors/transportation/equipment/device-interlocking-20251105-18.md

## References
- [European Union Agency for Railways (ERA)](https://www.era.europa.eu/) - ETCS standards and specifications
- [ETCS Website](https://www.etcs.org/) - Technical information on European Train Control System
- [Railway Gazette International](https://www.railwaygazette.com/) - Industry news and technical articles

## Metadata
- Last Updated: 2025-11-05 18:00:00
- Research Session: Transportation Equipment Research
- Completeness: 95%
- Next Actions: Document latest Eurobalise model variants, explore ATO integration with balises
