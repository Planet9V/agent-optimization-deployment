# P25 (Project 25) Standards and Protocols - Emergency Services

## P25 Standard Overview

### TIA-102 Standard Suite (Telecommunications Industry Association)
- **Standard Name**: Project 25 (P25) Digital Radio Standard
- **Governing Body**: Telecommunications Industry Association (TIA)
- **Development**: Association of Public-Safety Communications Officials (APCO)
- **Purpose**: Interoperable digital land mobile radio for public safety
- **Frequency Bands**: VHF (136-174 MHz), UHF (380-520 MHz), 700 MHz (764-776/794-806 MHz), 800 MHz (806-824/851-869 MHz)
- **Voice Encoding**: IMBE (Improved Multi-Band Excitation) vocoder at 7.2 kbps (Phase 1), AMBE+2 vocoder at 3.6 kbps (Phase 2)
- **Channel Spacing**: 12.5 kHz (narrowband)
- **Modulation**: C4FM (4-level FSK) for Phase 1, H-DQPSK (π/4 DQPSK) for Phase 2 TDMA
- **Data Rate**: 9600 bps (Phase 1 FDMA), 12000 bps (Phase 2 TDMA per timeslot)
- **Access Method**: FDMA (Frequency Division Multiple Access) for Phase 1, TDMA (Time Division Multiple Access) for Phase 2
- **Network Architecture**: Conventional and trunked operation modes

## P25 Phase 1 (FDMA)

### TIA-102.CAAA Common Air Interface (CAI) - Phase 1
- **Standard Document**: TIA-102.CAAA
- **Air Interface Type**: FDMA (Frequency Division Multiple Access)
- **Modulation Scheme**: C4FM (Compatible Four-level Frequency Modulation)
- **Symbol Rate**: 4800 symbols per second
- **Data Rate**: 9600 bps (2 bits per symbol)
- **Channel Bandwidth**: 12.5 kHz
- **Frequency Deviation**: ±1800 Hz for C4FM modulation
- **Voice Coding**: IMBE vocoder (Improved Multi-Band Excitation)
- **Voice Bit Rate**: 7.2 kbps (7200 bps)
- **FEC (Forward Error Correction)**: Rate 1/2 convolutional coding, constraint length 9
- **Interleaving**: 24x24 block interleaver for burst error protection
- **Frame Structure**: 360-bit voice frames, 180ms duration per frame
- **Header Information**: 72-bit Network Access Code (NAC), 16-bit CRC
- **Trellis Coding**: 1/2 rate Trellis Coded Modulation
- **BER Performance**: <5% Bit Error Rate at 12 dB SINAD
- **RF Sensitivity**: Typically 0.25-0.35 µV for 5% BER
- **Adjacent Channel Rejection**: >60 dB
- **Spurious Rejection**: >70 dB
- **Audio Bandwidth**: 300 Hz to 3.4 kHz

### P25 Phase 1 Trunking
- **Standard**: TIA-102.BABA (Trunking Control Channel)
- **Control Channel**: Dedicated control channel (outbound) or inbound signaling
- **Trunking Type**: APCO Project 25 trunking
- **Talk Groups**: Up to 65,535 talk groups per system
- **System ID**: 12-bit Wide Area Communications System Identifier (WACN)
- **Network ID**: 20-bit System ID (Network Address Component)
- **Unit ID**: 24-bit Subscriber Unit Address
- **Call Setup Time**: <500ms for typical call establishment
- **Group Call**: Push-to-talk group calling
- **Private Call**: Individual subscriber calling
- **Emergency Call**: Priority emergency call with preemption
- **All Call**: Broadcast to all units on system
- **Dynamic Regrouping**: Temporary talk group assignment
- **Patches**: Dynamic patching between talk groups
- **Affiliation**: Automatic and manual talk group affiliation
- **Registration**: Unit registration with system on power-up
- **Authentication**: Mutual authentication between unit and system
- **Roaming**: Automatic roaming between sites in wide-area system

## P25 Phase 2 (TDMA)

### TIA-102.CAAB Common Air Interface (CAI) - Phase 2
- **Standard Document**: TIA-102.CAAB
- **Air Interface Type**: TDMA (Time Division Multiple Access)
- **Timeslots**: 2 timeslots per 12.5 kHz channel
- **Slot Duration**: 30ms per timeslot
- **Frame Duration**: 60ms (2 timeslots)
- **Modulation Scheme**: H-DQPSK (π/4 Differential Quadrature Phase Shift Keying)
- **Symbol Rate**: 6000 symbols per second
- **Data Rate**: 12000 bps per channel (6000 bps per timeslot)
- **Voice Coding**: AMBE+2 vocoder (Advanced Multi-Band Excitation)
- **Voice Bit Rate**: 3.6 kbps (3600 bps per timeslot)
- **FEC**: Rate 3/4 Trellis Coded Modulation
- **Voice Frame**: 180-bit superframe (4 voice frames)
- **Spectral Efficiency**: 2x Phase 1 (2 voice channels per 12.5 kHz)
- **Backward Compatibility**: Phase 2 radios support Phase 1 operation
- **BER Performance**: <3% Bit Error Rate at 12 dB SINAD
- **RF Sensitivity**: Typically 0.30-0.40 µV for 5% BER
- **Audio Bandwidth**: 300 Hz to 3.4 kHz
- **Synchronization**: Slot synchronization via sync patterns
- **Guard Time**: 1ms guard time between timeslots

### P25 Phase 2 TDMA Trunking
- **Control Channel**: 2-slot TDMA control channel or H-DQPSK modulation
- **Capacity**: 2x Phase 1 capacity (double voice channels per RF channel)
- **Call Types**: Group call, private call, emergency, all call
- **Dual Watch**: Simultaneous monitoring of 2 timeslots
- **TDMA Slot Assignment**: Dynamic slot assignment by system
- **Migration Path**: Seamless migration from Phase 1 to Phase 2

## P25 Encryption Standards

### AES-256 Encryption (Advanced Encryption Standard)
- **Standard**: FIPS 197 (Federal Information Processing Standard)
- **Algorithm**: Rijndael cipher
- **Key Length**: 256-bit encryption key
- **Block Size**: 128-bit data blocks
- **Rounds**: 14 encryption rounds
- **Key Schedule**: 256-bit master key expansion
- **Mode**: OFB (Output Feedback) mode for voice
- **IV (Initialization Vector)**: 128-bit IV transmitted with each call
- **Key Management**: OTAR (Over-The-Air Rekeying)
- **Key Storage**: Secure key storage with tamper detection
- **Key Zeroization**: Automatic key deletion on tamper
- **FIPS 140-2**: Compliance with FIPS 140-2 Level 2 or Level 3
- **Key Hierarchy**: KEK (Key Encryption Key), TEK (Traffic Encryption Key)
- **Key Lifetime**: Programmable key expiration (hours to months)
- **Rekeying Interval**: Configurable automatic rekeying

### DES-OFB Encryption (Data Encryption Standard - Output Feedback)
- **Standard**: Legacy DES encryption (FIPS 46-3, withdrawn)
- **Algorithm**: DES (Data Encryption Standard)
- **Key Length**: 56-bit encryption key (64-bit with parity)
- **Block Size**: 64-bit data blocks
- **Mode**: OFB (Output Feedback) mode
- **IV**: 64-bit initialization vector
- **Security Level**: Considered weak by modern standards, maintained for legacy compatibility
- **Replacement**: AES-256 recommended for new deployments

### OTAR (Over-The-Air Rekeying)
- **Standard**: TIA-102.AAAD (OTAR Protocol)
- **Purpose**: Remote encryption key distribution and management
- **Key Types**: KEK (Key Encryption Key), TEK (Traffic Encryption Key)
- **KEK Distribution**: Manual distribution or secure key fill device
- **TEK Distribution**: Encrypted TEK transmission over-the-air using KEK
- **Message Indicator**: 16-bit Message Indicator (MI) for TEK identification
- **SLN (Storage Location Number)**: Key storage location identifier (0-255)
- **Activation**: Automatic or manual TEK activation
- **Key Deletion**: Remote key deletion capability
- **Audit Trail**: Key distribution audit logging
- **Rekeying Trigger**: Time-based, event-based, or manual rekeying
- **Group Rekeying**: Simultaneous rekeying of talk group members
- **Key Fill Device (KFD)**: Motorola KVL 4000/5000, Harris KYK-13, Cisco CKR

### OTAP (Over-The-Air Programming)
- **Purpose**: Remote radio provisioning and configuration
- **Parameters**: Talk groups, zones, channels, radio personalities
- **Security**: Encrypted programming commands
- **Authentication**: Mutual authentication before programming

## P25 Network Standards

### TIA-102.BAHA Inter-RF Subsystem Interface (ISSI)
- **Standard**: TIA-102.BAHA
- **Purpose**: Interconnection between P25 RF subsystems (RFSS)
- **Architecture**: IP-based interconnection
- **Protocol**: VoIP (Voice over IP) using RTP/UDP
- **Voice Coding**: IMBE or AMBE+2 vocoder (transported as RTP payload)
- **Call Control**: SIP-based call setup and teardown
- **Interoperability**: Enables roaming between different vendor systems
- **Network Interface**: Standard Ethernet (10/100/1000 Mbps)
- **QoS (Quality of Service)**: DiffServ/ToS markings for voice priority
- **Bandwidth**: ~13 kbps per voice call (IMBE), ~7 kbps per call (AMBE+2)
- **Latency**: <200ms end-to-end latency target
- **Jitter**: <50ms jitter tolerance
- **Packet Loss**: <1% packet loss for acceptable voice quality
- **Encryption**: End-to-end encryption maintained across ISSI
- **Authentication**: Mutual authentication between RFSS

### TIA-102.BABB Console Subsystem Interface (CSSI)
- **Standard**: TIA-102.BABB
- **Purpose**: Interface between dispatch consoles and P25 core
- **Protocol**: IP-based using SIP and RTP
- **Voice Transport**: RTP/UDP with IMBE or AMBE+2 vocoder
- **Call Control**: SIP signaling for call setup
- **Features**: PTT control, emergency alerting, status messaging
- **Network**: Ethernet-based IP connectivity
- **QoS**: Voice prioritization via DiffServ
- **Redundancy**: Redundant console connections for high availability

### TIA-102.BACA Network Management Interface
- **Standard**: TIA-102.BACA
- **Purpose**: System monitoring and management
- **Protocol**: SNMP v2/v3 (Simple Network Management Protocol)
- **Management**: Radio registration, call statistics, alarm monitoring
- **Performance Monitoring**: Channel utilization, call success rate, BER
- **Fault Management**: Alarm generation and notification
- **Security**: SNMPv3 encrypted authentication

## P25 Data Services

### TIA-102.AAAB Data Standards
- **Standard**: TIA-102.AAAB
- **Data Types**: Short data messages, packet data, circuit data
- **Short Data**: Up to 512 bytes per message
- **Packet Data Rate**: Up to 9600 bps (Phase 1), 12000 bps (Phase 2)
- **Circuit Data**: Continuous data connection
- **Applications**: GPS location, status updates, text messaging, telemetry
- **Protocols**: IP, UDP, TCP support over P25 data
- **Addressing**: 24-bit unit ID addressing

### GPS Location Services
- **Standard**: TIA-102.AABF (Location Services)
- **GPS Data Format**: Latitude/longitude in decimal degrees
- **Precision**: Typically 5-10 meter accuracy with GPS
- **Update Rate**: Configurable (every 30 seconds to 5 minutes)
- **Emergency Location**: Automatic GPS transmission on emergency activation
- **Data Transport**: P25 short data service or packet data
- **Datum**: WGS84 (World Geodetic System 1984)

### P25 Text Messaging
- **Message Length**: Up to 512 bytes per message
- **Character Set**: ASCII or Unicode
- **Addressing**: Individual or group text messaging
- **Delivery Confirmation**: Message receipt acknowledgment
- **Status Messages**: Predefined status codes (Available, Busy, En Route, etc.)
- **Emergency Text**: Priority text message delivery

## P25 Radio Frequency (RF) Parameters

### VHF Band (136-174 MHz)
- **Frequency Range**: 136-174 MHz
- **Channel Spacing**: 12.5 kHz (narrowband)
- **Number of Channels**: ~3040 channels (12.5 kHz spacing)
- **Propagation**: Good building penetration, longer range
- **Antenna Length**: ~5 inches (1/4 wave at 150 MHz)
- **Typical Range**: 5-15 miles portable-to-portable, 15-30 miles mobile-to-mobile
- **Power Limits**: Typically 5W portable, 45-110W mobile
- **FCC Part**: Part 90 (Private Land Mobile Radio)

### UHF Band (380-520 MHz)
- **Frequency Range**: 380-520 MHz (UHF R1: 380-470 MHz, UHF R2: 450-520 MHz)
- **Channel Spacing**: 12.5 kHz
- **Number of Channels**: ~11,200 channels total
- **Propagation**: Better in-building coverage than VHF, shorter outdoor range
- **Antenna Length**: ~3 inches (1/4 wave at 450 MHz)
- **Typical Range**: 3-10 miles portable-to-portable, 10-25 miles mobile-to-mobile
- **Power Limits**: Typically 5W portable, 45-110W mobile
- **FCC Part**: Part 90

### 700 MHz Band (764-776/794-806 MHz)
- **Frequency Range**: Public Safety 700 MHz (764-776 MHz base transmit, 794-806 MHz mobile transmit)
- **Channel Spacing**: 12.5 kHz
- **Narrowband Channels**: 764-776 MHz (General Use), 768-769 MHz (Interoperability)
- **Propagation**: Excellent building penetration, good range
- **Antenna Length**: ~2 inches (1/4 wave at 770 MHz)
- **Typical Range**: 4-12 miles portable-to-portable, 15-35 miles mobile-to-mobile
- **Power Limits**: 5W portable, 30-50W mobile
- **FCC Allocation**: Dedicated public safety band
- **Guard Band**: Regional planning required

### 800 MHz Band (806-824/851-869 MHz)
- **Frequency Range**: 806-824 MHz (base transmit), 851-869 MHz (mobile transmit)
- **Channel Spacing**: 12.5 kHz (narrowband)
- **NPSPAC Band**: 806-809/851-854 MHz (National Public Safety Planning Advisory Committee)
- **General Use**: 809-824/854-869 MHz
- **Propagation**: Similar to 700 MHz, good building penetration
- **Antenna Length**: ~1.8 inches (1/4 wave at 850 MHz)
- **Typical Range**: 4-12 miles portable-to-portable, 15-35 miles mobile-to-mobile
- **Power Limits**: 3W portable, 30-50W mobile
- **Rebanding**: Completed 800 MHz rebanding to reduce interference

## P25 Conformance Testing

### P25 CAP (Compliance Assessment Program)
- **Program**: Department of Homeland Security (DHS) P25 CAP
- **Administrator**: DHS SAFECOM Program
- **Testing Lab**: Independent testing laboratories (e.g., JITC, Intertek, TUV)
- **CAP Summary**: Published test results for P25 equipment
- **Test Categories**:
  - **CAI Conformance**: Common Air Interface compliance testing
  - **CAI Performance**: RF performance and voice quality testing
  - **ISSI**: Inter-RF Subsystem Interface testing
  - **CSSI**: Console Subsystem Interface testing
  - **Conventional Performance**: Conventional operation testing
  - **Trunking Performance**: Trunking operation testing
- **Tested Equipment**: Subscriber units (portables, mobiles), infrastructure (base stations, repeaters), consoles
- **Pass/Fail Criteria**: Must meet TIA-102 standard requirements
- **CAP Logo**: Equipment displays P25 CAP logo upon passing
- **Test Report**: Public availability of test results on CAP website

### P25 Interoperability Testing
- **Objective**: Verify multi-vendor interoperability
- **Test Scenarios**: Cross-vendor radio-to-radio, radio-to-infrastructure
- **Voice Quality**: Subjective voice quality testing (MOS score)
- **Data Interoperability**: GPS, text messaging between vendors
- **Encryption**: AES-256 interoperability testing
- **Roaming**: Multi-vendor roaming verification

## P25 Frequency Coordination

### Frequency Licensing (FCC)
- **License Type**: Private Land Mobile Radio (PLMR) license under FCC Part 90
- **Eligibility**: Public safety agencies (police, fire, EMS, emergency management)
- **Application**: FCC Form 601 for new licenses, renewals, modifications
- **Frequency Coordination**: Regional frequency coordinators (e.g., APCO, IAFC, IMSA)
- **Coordination Process**: Frequency coordinator reviews interference potential
- **Interference Protection**: 70 dB separation for co-channel, 50 dB for adjacent channel
- **License Term**: 10-year renewable license
- **Narrowbanding**: FCC mandates 12.5 kHz efficiency (completed 2013)
- **Database**: FCC Universal Licensing System (ULS) database

### Regional Frequency Coordinators
- **APCO**: Association of Public-Safety Communications Officials (police, sheriff, emergency management)
- **IAFC**: International Association of Fire Chiefs (fire service frequencies)
- **IMSA**: International Municipal Signal Association (municipal frequencies)
- **Forestry-Conservation**: Forestry and conservation agencies
- **Coordination Area**: Coordinators cover specific geographic regions
- **Coordination Fee**: Frequency coordination processing fee
- **Processing Time**: Typically 2-6 weeks for coordination

## P25 System Design Parameters

### Coverage Planning
- **Signal Strength Target**: -95 dBm minimum signal strength for portable coverage
- **DAQ (Delivered Audio Quality)**: DAQ 3.4 or higher (5-point scale)
- **Reliability**: 95% coverage probability on building edge, 90% in-building
- **Simulcast Overlap**: >6 dB signal differential for simulcast systems
- **Fade Margin**: 10-15 dB fade margin for mobile, 15-20 dB for portable

### Site Spacing
- **VHF**: Typical 15-25 mile site spacing
- **UHF**: Typical 10-20 mile site spacing
- **700/800 MHz**: Typical 12-22 mile site spacing
- **Terrain Factors**: Adjusted for terrain, foliage, urban density

### Trunking System Capacity
- **Erlang Capacity**: ~20-25 Erlangs per RF channel pair (Phase 1), ~40-50 Erlangs (Phase 2)
- **Busy Hour**: Design for peak busy hour traffic
- **Grade of Service**: Typically P.01 (1% blocking probability) or P.02
- **Queuing**: Call queuing during high traffic periods
