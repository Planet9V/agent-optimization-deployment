# P25 Infrastructure and Network Architecture - Emergency Services

## P25 Infrastructure Components

### P25 Base Station / Repeater
- **Function**: Receive and retransmit radio signals to extend coverage
- **Power Output**: 50W to 250W typical (VHF/UHF), 30W to 100W (700/800 MHz)
- **Receiver Sensitivity**: 0.22 µV @ 12 dB SINAD (analog), 0.25 µV @ 5% BER (P25)
- **Frequency Bands**: VHF (136-174 MHz), UHF (380-520 MHz), 700 MHz (764-776/794-806 MHz), 800 MHz (806-824/851-869 MHz)
- **Duplex Spacing**: VHF 6 MHz, UHF 5 MHz, 700 MHz 30 MHz, 800 MHz 45 MHz
- **Duplexer**: Cavity duplexer or circulator-based duplexer for simultaneous TX/RX
- **Antenna System**: Base station antenna with 6-12 dBd gain
- **Coverage Area**: 5-30 mile radius depending on terrain, frequency, antenna height
- **Antenna Height**: 100-500 feet AGL (Above Ground Level) on tower
- **Tower Type**: Self-supporting, guyed, monopole towers
- **Grounding**: Single-point ground for lightning protection
- **Power Supply**: 48V DC or 120/240V AC with battery backup (8-24 hours)
- **Backup Generator**: Automatic transfer switch to generator during power outage
- **Environmental**: NEMA 4 or IP65 rated enclosure for outdoor installation
- **Operating Temp**: -40°C to +60°C for outdoor base stations
- **Cooling**: Forced air cooling or passive heat sinks
- **Remote Monitoring**: SNMP monitoring for status and alarms

### Motorola Solutions Base Stations

#### Motorola GTR 8000 P25 Base Station
- **Product Line**: GTR 8000 Series Base Station/Repeater
- **Vendor**: Motorola Solutions
- **P25 Capability**: Phase 1 FDMA, Phase 2 TDMA (2-slot TDMA)
- **Frequency Bands**: VHF (136-174 MHz), UHF (380-520 MHz), 700 MHz, 800 MHz
- **Power Output**: VHF/UHF 25W/50W/100W/110W, 700/800 MHz 25W/50W/100W
- **Modulation**: C4FM (Phase 1), H-DQPSK (Phase 2 TDMA)
- **Receiver Sensitivity**: 0.22 µV @ 12 dB SINAD (analog), 0.25 µV @ 5% BER (P25)
- **Selectivity**: Adjacent channel 70 dB, co-channel 10 dB
- **Frequency Stability**: ±0.5 ppm over operating temperature range
- **Encryption**: AES-256, DES-OFB with OTAR
- **Trunking**: P25 Phase 1 and Phase 2 trunking (SmartZone)
- **GPS**: Integrated GPS receiver for time synchronization (simulcast)
- **Network Interface**: Dual Gigabit Ethernet with 802.1Q VLAN support
- **Audio Encoding**: IMBE vocoder (Phase 1), AMBE+2 vocoder (Phase 2)
- **Audio Quality**: 16-bit digital audio, <50ms latency
- **Duplexer**: Internal high-Q cavity duplexer
- **Antenna Connector**: N-type female connector (50-ohm)
- **VSWR Protection**: Automatic power reduction on high VSWR
- **Dimensions**: 19" rack-mount, 3U height (5.25" H x 19" W x 20" D)
- **Weight**: 25 kg (55 lbs)
- **Power Input**: 120/240V AC or -48V DC
- **Power Consumption**: 350W typical at full power output
- **Battery Backup**: External 48V battery backup (not included)
- **Operating Temp**: -30°C to +60°C (base station configuration)
- **Humidity**: 5% to 95% non-condensing
- **Cooling**: Internal forced-air cooling with front-to-rear airflow
- **MTBF**: >60,000 hours
- **Configuration**: Remote configuration via IP network (Element Manager)
- **Monitoring**: SNMP v2/v3 for remote monitoring and alarming
- **Software**: Motorola GTR 8000 firmware (field-upgradable)
- **Redundancy**: 1+1 redundancy with automatic failover
- **Hot Swap**: Hot-swappable power supplies and modules

#### Motorola Quantar Base Station (Legacy)
- **Product Line**: Quantar Base Station/Repeater (legacy product)
- **P25 Capability**: Phase 1 FDMA only
- **Frequency Bands**: VHF, UHF, 700 MHz, 800 MHz
- **Power Output**: 25W to 110W depending on model
- **Modulation**: C4FM for P25
- **Receiver Sensitivity**: 0.25 µV @ 5% BER
- **Encryption**: DES-OFB, AES-256 (with upgrade)
- **Trunking**: SmartZone trunking support
- **Dimensions**: 19" rack-mount, 3U or 5U
- **Status**: End-of-life, replaced by GTR 8000
- **Installed Base**: Still widely deployed in legacy systems

### L3Harris Base Stations

#### L3Harris XG-100P Base Station
- **Product Line**: XG-100 Series Base Station
- **Vendor**: L3Harris Technologies
- **P25 Capability**: Phase 1 FDMA, Phase 2 TDMA
- **Frequency Bands**: VHF (136-174 MHz), UHF (380-470 MHz), 700 MHz, 800 MHz
- **Power Output**: VHF/UHF 25W/50W/100W/110W, 700/800 MHz 30W/50W/100W
- **Modulation**: C4FM (Phase 1), H-DQPSK (Phase 2)
- **Receiver Sensitivity**: 0.22 µV @ 5% BER
- **Selectivity**: 70 dB adjacent channel rejection
- **Frequency Stability**: ±0.5 ppm
- **Encryption**: AES-256 (FIPS 140-2 Level 3), DES-OFB, DVP
- **Trunking**: P25 Phase 1 and Phase 2 trunking
- **GPS**: Integrated GPS for simulcast synchronization
- **Network Interface**: Dual Gigabit Ethernet
- **Audio Encoding**: IMBE (Phase 1), AMBE+2 (Phase 2)
- **Duplexer**: High-isolation cavity duplexer (>80 dB isolation)
- **Antenna Connector**: N-type female, 50-ohm
- **Dimensions**: 19" rack-mount, 3U (5.25" H)
- **Weight**: 23 kg
- **Power Input**: 120/240V AC or -48V DC
- **Power Consumption**: 300W typical
- **Operating Temp**: -30°C to +60°C
- **Cooling**: Forced-air cooling
- **MTBF**: >65,000 hours
- **Configuration**: IP-based configuration via Unity Network Manager
- **Monitoring**: SNMP monitoring and alarming
- **Redundancy**: Hot-standby redundancy support

### Kenwood Base Stations

#### Kenwood NXR-710/810/910 P25 Base Station/Repeater
- **Product Line**: NEXEDGE NXR Series
- **Vendor**: Kenwood USA
- **P25 Capability**: Phase 1 FDMA, Phase 2 TDMA
- **Frequency Bands**: NXR-710 (VHF 136-174 MHz), NXR-810 (UHF 400-470 MHz), NXR-910 (700/800 MHz)
- **Power Output**: VHF/UHF 25W/50W/100W, 700/800 MHz 25W/50W
- **Modulation**: C4FM, H-DQPSK
- **Receiver Sensitivity**: 0.22 µV @ 5% BER
- **Encryption**: AES-256, DES-OFB, ARC4
- **Trunking**: P25 conventional and trunked
- **GPS**: Optional GPS module for synchronization
- **Network Interface**: Ethernet 10/100/1000 Mbps
- **Duplexer**: Internal cavity duplexer
- **Dimensions**: 19" rack-mount, 2U (3.5" H)
- **Weight**: 18 kg
- **Power Input**: 13.8V DC (11-16V range)
- **Power Consumption**: 200W at 50W output
- **Operating Temp**: -30°C to +60°C
- **MTBF**: >50,000 hours
- **Mixed Mode**: Simultaneous P25 and analog/DMR operation
- **Remote Management**: Web-based management interface

### Tait Communications Base Stations

#### Tait TB9400 P25 Base Station
- **Product Line**: TB9400 Series
- **Vendor**: Tait Communications
- **P25 Capability**: Phase 1 FDMA, Phase 2 TDMA
- **Frequency Bands**: VHF (136-174 MHz), UHF (380-470 MHz), 700/800 MHz
- **Power Output**: 25W/50W/100W/150W selectable
- **Modulation**: C4FM, H-DQPSK
- **Receiver Sensitivity**: 0.20 µV @ 5% BER
- **Encryption**: AES-256, DES with OTAR
- **Trunking**: P25 trunking support
- **GPS**: Integrated GPS for simulcast
- **Network Interface**: Dual Gigabit Ethernet
- **Duplexer**: High-Q cavity duplexer
- **Dimensions**: 19" rack-mount, 2U
- **Weight**: 20 kg
- **Power Input**: -48V DC or 120/240V AC
- **Operating Temp**: -40°C to +60°C
- **MTBF**: >70,000 hours
- **Modular Design**: Hot-swappable modules
- **TrueVoice**: Enhanced audio processing

## P25 Trunking Infrastructure

### P25 Trunking Controller (Site Controller)
- **Function**: Manage trunked radio resources at a single site
- **Channel Management**: Allocate voice and control channels dynamically
- **Talk Group Management**: Manage talk group assignments and priorities
- **Call Processing**: Process group calls, private calls, emergency calls
- **Registration**: Handle subscriber unit registration
- **Affiliation**: Manage talk group affiliation and de-affiliation
- **Queuing**: Queue calls during busy periods
- **Priority**: Prioritize emergency calls and high-priority talk groups
- **Network Interface**: IP connectivity to central controller and other sites
- **Redundancy**: Redundant site controller for failover
- **Database**: Local database synchronized with central controller
- **Control Channel**: Manage outbound and inbound control channel signaling

### Motorola SmartZone System

#### SmartZone Omnilink Controller
- **Product Name**: SmartZone Omnilink System Controller
- **Vendor**: Motorola Solutions
- **Architecture**: Distributed IP-based trunking architecture
- **System Capacity**: 200,000+ subscribers, 15,000+ talk groups
- **Site Capacity**: Up to 250 sites per system
- **Channels per Site**: Up to 96 RF channels per site
- **Control Channel**: Dedicated control channel (outbound) or inbound signaling
- **P25 Capability**: Phase 1 FDMA, Phase 2 TDMA
- **Trunking Type**: P25 trunking with SmartZone features
- **Roaming**: Automatic roaming between sites and systems
- **Call Setup Time**: <500ms average call setup
- **Priority Levels**: 16 priority levels for calls and users
- **Emergency Handling**: Priority emergency call processing with preemption
- **Group Call**: Instant group calling with PTT
- **Private Call**: Individual subscriber calling
- **Telephone Interconnect**: PSTN/VoIP telephone patch capability
- **Patches**: Dynamic and static patches between talk groups
- **Failsoft**: Site failsoft operation if connection to controller lost
- **Wide Area**: Wide-area system with automatic site selection
- **Simulcast**: Support for simulcast sites
- **Voting**: Voting receivers for improved coverage
- **Database**: Centralized subscriber and talk group database
- **Provisioning**: Centralized provisioning and Over-The-Air Service Provisioning (OTASP)
- **Network Interface**: IP network connectivity (Gigabit Ethernet)
- **Redundancy**: N+1 or 2N redundancy for controllers
- **Geographic Redundancy**: Support for geographically diverse backup controllers
- **SNMP**: SNMP monitoring and management
- **Software**: Motorola Network Manager for system configuration
- **Logging**: Comprehensive call logging and system event logging
- **Integration**: Integration with Motorola PremierOne CAD, consoles

#### SmartZone Elite
- **Product Name**: SmartZone Elite Multi-Site Trunking System
- **Enhanced Features**: Enhanced over Omnilink with additional capabilities
- **Multi-Agency**: Support for multiple independent agency systems on shared infrastructure
- **Scalability**: Higher scalability (500+ sites, 500,000+ subscribers)
- **Performance**: Lower call setup time (<300ms)
- **LTE Integration**: LTE push-to-talk integration
- **ISSI**: Inter-RF Subsystem Interface (ISSI) for multi-vendor interoperability
- **Virtualization**: Support for virtualized controllers

### L3Harris OpenSky System

#### OpenSky Core Controller
- **Product Name**: L3Harris OpenSky Trunking System
- **Vendor**: L3Harris Technologies
- **Architecture**: Centralized IP-based TETRA-like architecture
- **System Capacity**: 100,000+ subscribers
- **Site Capacity**: Up to 100 sites per system
- **P25 Capability**: Phase 1 FDMA, Phase 2 TDMA (via gateway)
- **Native Protocol**: EDACS (Enhanced Digital Access Communications System)
- **P25 Gateway**: P25 CAI gateway for interoperability
- **Roaming**: Automatic roaming
- **Call Types**: Group call, private call, emergency, broadcast
- **Failsoft**: Site failsoft capability
- **Network**: IP-based network connectivity
- **Redundancy**: Redundant core controllers
- **Database**: Centralized database

### Kenwood NEXEDGE Trunking

#### NEXEDGE Trunking System
- **Product Name**: Kenwood NEXEDGE NX-5000 Trunking System
- **Vendor**: Kenwood USA
- **P25 Capability**: P25 Phase 1 and Phase 2 trunking
- **Mixed Mode**: Simultaneous P25, NXDN, and analog trunking
- **System Capacity**: 10,000+ subscribers
- **Sites**: Up to 48 sites per system
- **Channels per Site**: Up to 32 channels
- **Network**: IP-based networking
- **Redundancy**: Redundant system controller
- **Database**: Centralized provisioning

## P25 Simulcast Systems

### Simulcast Overview
- **Definition**: Multiple transmitters broadcasting same signal simultaneously on same frequency
- **Purpose**: Provide wide-area coverage with single frequency
- **Advantage**: Frequency efficiency (one frequency for large area)
- **Challenge**: Requires precise timing synchronization between transmitters
- **Overlap Area**: Areas receiving signals from multiple transmitters
- **Delay Spread**: Time difference between arriving signals (<3 µs ideal, <7 µs acceptable)
- **Synchronization**: GPS-based time synchronization (accurate to <1 µs)
- **Voting Receivers**: Multiple receivers vote on best signal quality

### Motorola SmartZone Simulcast

#### SmartZone Simulcast Configuration
- **GPS Reference**: GPS receivers at each transmitter for time synchronization
- **Time Alignment**: Transmitters synchronized to GPS time within 1 microsecond
- **Delay Compensation**: Automatic delay compensation for propagation differences
- **Audio Distribution**: IP-based audio distribution to simulcast transmitters
- **Transmitter Spacing**: Typically 10-30 miles between simulcast transmitters
- **Coverage Overlap**: 6-12 dB signal differential in overlap areas
- **BER Performance**: <5% Bit Error Rate in simulcast coverage area
- **Simulcast Controller**: Centralized simulcast controller for timing management
- **Test Equipment**: Viavi TM500, Bird SiteMaster for simulcast tuning

### Simulcast Network Components

#### GPS Timing Reference
- **GPS Receiver**: High-precision GPS receiver at each site
- **Antenna**: Roof-mounted GPS antenna with clear sky view
- **Accuracy**: <100 nanosecond time accuracy
- **Holdover**: Rubidium or OCXO (Oven-Controlled Crystal Oscillator) for GPS loss
- **Holdover Duration**: 24-72 hours without GPS signal

#### Simulcast Audio Distribution
- **Audio Transport**: IP multicast audio distribution to all simulcast sites
- **Encoding**: G.711 (64 kbps) or proprietary encoding
- **Latency**: <50ms audio distribution latency
- **Jitter Buffer**: Adaptive jitter buffer for network delay variation
- **Sync Pulse**: GPS-derived sync pulse for transmitter keying

## P25 Voting Receiver Systems

### Voting Receiver Concept
- **Definition**: Multiple receivers at different locations vote on best received signal
- **Purpose**: Improve portable radio coverage in wide-area systems
- **Voting Algorithm**: Select receiver with strongest RSSI (Received Signal Strength Indicator) or best BER
- **Voting Types**: Hard voting (RSSI-based), soft voting (audio quality-based), digital voting (BER-based)
- **Receiver Spacing**: Receivers spaced 5-15 miles apart
- **Number of Receivers**: Typically 3-6 voting receivers per channel

### Motorola Comparator (Voting System)
- **Product**: Motorola Wireline Comparator
- **Function**: Compare signals from multiple receivers and select best
- **Inputs**: Up to 12 receiver inputs per comparator
- **Output**: Selected audio output to transmitter
- **Voting Speed**: <20ms voting decision time
- **Audio Quality**: Automatic gain control and audio leveling
- **Interface**: Analog audio or IP-based digital audio

### IP-Based Voting (Distributed Receivers)
- **Architecture**: IP-connected distributed receivers
- **Audio Transport**: RTP/UDP audio streams from receivers to voting server
- **Voting Server**: Centralized server performs voting algorithm
- **Scalability**: Support for 100+ receivers across wide area
- **Latency**: <100ms total voting latency
- **Backup**: Redundant voting servers

## P25 Network Connectivity

### Microwave Backhaul
- **Frequency Bands**: 6 GHz, 11 GHz, 18 GHz, 23 GHz licensed microwave
- **Capacity**: 10 Mbps to 1 Gbps depending on band and configuration
- **Antenna**: Parabolic dish antennas (0.6m to 3.6m diameter)
- **Path Length**: 5-30 miles typical microwave path
- **Availability**: 99.99% or 99.999% link availability
- **Latency**: <5ms microwave latency
- **Equipment**: Aviat Networks, Ceragon, DragonWave, Cambium Networks

### Fiber Optic Connectivity
- **Fiber Type**: Single-mode fiber (9/125 µm)
- **Capacity**: 1 Gbps to 100 Gbps
- **Latency**: ~5 µs per kilometer
- **Distance**: Up to 80 km without repeaters (1310 nm), 120 km (1550 nm)
- **Interface**: Gigabit Ethernet (1000BASE-LX/SX), 10 Gigabit Ethernet
- **Redundancy**: Diverse fiber paths for redundancy
- **Equipment**: Cisco, Juniper, Ciena, Adva Optical

### Leased Circuits (T1/T3, Metro Ethernet)
- **T1 Circuit**: 1.544 Mbps point-to-point circuit
- **T3 Circuit**: 44.736 Mbps (28 T1s bonded)
- **Metro Ethernet**: 10 Mbps to 10 Gbps Ethernet over carrier network
- **Latency**: 10-30ms depending on distance
- **Availability**: 99.9% or 99.99% SLA
- **Providers**: AT&T, Verizon, Lumen (CenturyLink), Windstream

### IP Network Architecture
- **Protocol**: IPv4 or IPv6
- **QoS**: DiffServ or MPLS for voice prioritization
- **VLANs**: 802.1Q VLAN tagging for traffic segregation
- **Routing**: OSPF or BGP dynamic routing protocols
- **Security**: IPsec VPN for encrypted tunnels
- **Firewall**: Stateful firewall for security
- **Bandwidth**: Typically 10-100 Mbps per site

## P25 System Redundancy

### Geographic Redundancy
- **Primary Site**: Main system controller and core infrastructure
- **Backup Site**: Geographically separated backup site (50-200 miles)
- **Database Replication**: Real-time database replication between sites
- **Failover**: Automatic failover to backup site (<30 seconds)
- **Disaster Recovery**: RTO (Recovery Time Objective) <1 hour, RPO (Recovery Point Objective) <15 minutes

### Component Redundancy
- **Controllers**: N+1 or 2N redundant controllers
- **Network**: Diverse network paths
- **Power**: Redundant power supplies, UPS, generator backup
- **Cooling**: Redundant HVAC systems
- **Transmitters**: 1+1 transmitter redundancy at critical sites

### Backup Power
- **UPS (Uninterruptible Power Supply)**: Online double-conversion UPS (5-30 kVA)
- **Battery Runtime**: 8-24 hours battery backup
- **Generator**: Diesel or natural gas generator (20-500 kW)
- **Automatic Transfer Switch (ATS)**: <10 second transfer time to generator
- **Fuel Storage**: 48-72 hour fuel supply on-site
- **Generator Runtime**: Unlimited with fuel delivery
