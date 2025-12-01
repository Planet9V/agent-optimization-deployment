# Broadcast Television Transmitters - Communications Sector

## Entity-Rich Introduction

Harris Maxiva UAXT UHF television transmitter delivers 60 kW peak visual power on channels 14-51 (470-698 MHz) utilizing liquid-cooled Doherty amplifier technology achieving 40% AC-to-RF efficiency with ATSC 3.0 modulation supporting 4K UHD broadcasts at 25 Mbps with HEVC encoding. Rohde & Schwarz THU9 high-power UHF transmitter implements solid-state broadband amplification generating 10 kW digital output across entire UHF band (470-860 MHz) with DVB-T2 COFDM modulation utilizing 256-QAM constellation and LDPC forward error correction achieving 45 Mbps throughput in 8 MHz channel bandwidth. GatesAir Maxiva ULXT liquid-cooled UHF transmitter operates ATSC 1.0 8-VSB modulation at 19.39 Mbps (6 MHz channel) delivering 1080i HD video streams with Dolby AC-3 5.1 surround audio, utilizing IOT (Inductive Output Tube) final amplifier stage producing 55 kW peak sync power with <1.5:1 VSWR into broadband UHF antenna systems (Dielectric TFU series).

## Technical Specifications

**Harris Maxiva UAXT Specifications**:
- Model: Harris Maxiva UAXT UHF Transmitter (ATSC 3.0 compliant)
- Frequency Range: 470-698 MHz (UHF channels 14-51)
- Output Power: 60 kW peak visual (digital), 55 kW average
- Modulation: ATSC 3.0 with OFDM, 256-QAM, LDPC FEC code rates 2/15 to 13/15
- Efficiency: 40% AC-to-RF (Doherty amplifier), 35% overall including auxiliary systems
- Amplifier Technology: Liquid-cooled solid-state modules, N+1 redundancy
- Spurious Emissions: <-60 dBc (in-band), <-80 dBc (out-of-band) meeting FCC mask
- Input: ASI (Asynchronous Serial Interface) 270 Mbps, IP/Ethernet 1 Gbps
- Modulator: Integrated ATSC 3.0 exciter, GPS synchronization, SFN operation
- Cooling: Closed-loop liquid cooling, glycol/water mixture, 15 GPM flow rate
- Power Consumption: 150 kW at full power, 208/480 VAC 3-phase input
- Dimensions: 72" H × 84" W × 48" D, weight 2200 lbs
- MTBF: 50,000 hours, hot-swappable amplifier modules

**Rohde & Schwarz THU9 Technical Details**:
- Model: R&S THU9 High-Power UHF Transmitter
- Frequency: 470-860 MHz (entire UHF band), software-tunable
- Output Power: 10 kW digital (DVB-T2), scalable to 40 kW with combiners
- Modulation Standards: DVB-T2, DVB-T, ATSC 1.0, ATSC 3.0, ISDB-T
- DVB-T2 Modes: 256-QAM, 64-QAM, 16-QAM, QPSK with rotated constellations
- Bandwidth: 1.7 MHz to 10 MHz (DVB-T2), 6/7/8 MHz standard configurations
- MISO/MIDO: 2-transmitter diversity, PLP (Physical Layer Pipe) multiplexing
- Efficiency: 35% typical (DVB-T2 256-QAM), N+1 amplifier redundancy
- SFN Capability: GPS/GNSS synchronization, <1 μs timing accuracy, distributed transmission
- Precorrection: Adaptive linear and nonlinear predistortion, ACLR >45 dB
- Remote Control: SNMP v3, web interface HTTPS, Modbus TCP monitoring

**GatesAir Maxiva ULXT Specifications**:
- Model: GatesAir Maxiva ULXT UHF Transmitter (ATSC 1.0)
- Technology: IOT (Inductive Output Tube) final amplifier
- Power Output: 55 kW peak sync, 11 kW average (ATSC 8-VSB)
- Frequency Range: 470-806 MHz (channels 14-69, legacy UHF allocation)
- Modulation: ATSC 1.0 8-VSB (8-level Vestigial Sideband)
- Data Rate: 19.39 Mbps payload (6 MHz channel bandwidth)
- Video Encoding: MPEG-2 MP@HL (1080i) or H.264 AVC (720p/1080p)
- Audio: Dolby Digital AC-3 5.1 surround, 384 kbps bitrate
- Exciter: Integrated solid-state exciter, 10W RF output to IOT driver
- Cooling: Liquid cooling for IOT, forced air for exciter
- Efficiency: 28% IOT efficiency, 25% overall system
- Input Interfaces: ASI (SMPTE 310M), IP (UDP/RTP), RF loop-through

**Broadcast Antenna Systems**:
- Dielectric TFU-25G/VP-R: UHF panel antenna, circular polarization, 485-700 MHz
- Antenna Gain: 40 (16 dBd), directional pattern ±30° horizontal beamwidth
- VSWR: <1.1:1 across channel, <1.5:1 across full UHF band
- Power Rating: 80 kW average, 200 kW peak (per bay)
- Polarization: Vertical, horizontal, or circular (switchable)
- Combiner: Starpoint or corporate feed, 4-port or 8-port configurations
- Transmission Line: EIA 8-3/16" rigid coaxial, 50-ohm impedance, 0.5 dB/100ft loss at 600 MHz
- Tower Installation: Side-mount or top-mount, wind survival 125 mph, ice loading 2 inches

**ATSC 3.0 Advanced Features**:
- Channel Bonding: Aggregation of 2-4 RF channels (up to 32 MHz bandwidth)
- MIMO: 2×2 spatial multiplexing (dual-polarization antennas)
- Non-Uniform Constellation: Optimized SNR thresholds for mobile vs fixed reception
- LDM (Layered Division Multiplexing): Core layer (robust) + enhanced layer (high capacity)
- Bootstrap: 0.5 ms preamble, BPSK modulation, coarse synchronization
- Subframe Structure: Variable time interleaving (50-5000 ms), frequency interleaving

## Integration & Operations

Broadcast transmitter installation at television station WXYZ-TV (RF channel 25, 536-542 MHz) implements Harris Maxiva UAXT transmitter delivering 60 kW ERP (Effective Radiated Power) from 1200-foot tower site (SITE-TRANSMIT-01) providing Grade A coverage 60-mile radius serving 5 million population in metro market. ATSC 3.0 modulation configuration utilizes 256-QAM with LDPC code rate 10/15 (effective spectral efficiency 4.2 bits/Hz) encoding three UHD program streams: primary 4K channel (18 Mbps HEVC Main 10 profile), secondary HD channel (6 Mbps AVC High profile), mobile SD channel (1.5 Mbps AVC Baseline) multiplexed in single 6 MHz RF channel with combined 25.5 Mbps payload. SFN (Single Frequency Network) operation synchronizes main transmitter with two 1 kW gap-filler translators (GAP-NORTH-02, GAP-SOUTH-03) utilizing GPS timing receivers (Symmetricom TimeProvider 1000) maintaining <1 μs timing accuracy enabling constructive RF interference in overlap areas increasing coverage area 25%. Studio-to-transmitter link utilizes IP-based transport with SMPTE 2022-6 encapsulation of ATSC 3.0 transport stream over 1 Gbps fiber connection (dark fiber lease), implementing forward error correction (Pro-MPEG Code of Practice #3) tolerating 15% packet loss, with automatic failover to 100 Mbps microwave STL (Moseley SL9003Q) within 2-second switchover. Transmitter monitoring system tracks critical parameters every 10 seconds: forward power (target 60 kW ±5%), reflected power (<300W indicating VSWR <1.1:1), PA module temperatures (target 45°C, alarm at 65°C), coolant flow rate (target 15 GPM, shutdown at 12 GPM), and modulation error ratio MER (target >35 dB for 256-QAM, alarm at <30 dB). Adaptive precorrection system compensates for PA nonlinearity utilizing digital predistortion (DPD) algorithm sampling transmitter output via RF coupler, analyzing spectral regrowth (ACLR >50 dB required), and applying inverse distortion to exciter input achieving <-40 dBc in-band spurious emissions meeting FCC 73.687 mask requirements. Antenna system maintenance includes quarterly VSWR sweeps (Anritsu Site Master S820E) verifying <1.15:1 across 6 MHz channel bandwidth, annual tower climbing inspections detecting mechanical damage or corrosion on panel elements, and 5-year rigid line pressurization system checks maintaining 5 PSI nitrogen pressure preventing moisture ingress. Emergency Alert System (EAS) integration implements SCTE 18 EAS protocol decoder monitoring NOAA weather radio and state/local authorities, automatically interrupting programming with CAP (Common Alerting Protocol) messages transmitted via ATSC 3.0 emergency alert table providing geo-targeted warnings with polygon boundary definitions and multi-language text. Redundancy architecture deploys N+1 solid-state amplifier configuration with 8 active PA modules contributing 7.5 kW each (total 60 kW), automatic switchover removing failed module within 100 ms with graceful power degradation to 52.5 kW maintaining on-air operation during module replacement, and hot-swappable design enabling maintenance without transmitter shutdown.

## Security Implementation

Broadcast transmitter security implements multi-layer access control with SCADA network isolation in dedicated VLAN 200 (192.168.200.0/24) separated from studio network by Cisco ASA 5516-X firewall enforcing rules permitting only essential protocols: SNMP monitoring (UDP 161/162), Modbus TCP control (TCP 502), HTTPS remote access (TCP 443), blocking lateral movement and preventing ransomware propagation from corporate network. Physical access control restricts transmitter building entry through biometric authentication (HID iCLASS SE reader with fingerprint verification) logging all access attempts with timestamp, video surveillance (Axis P1435-LE cameras) providing 4K resolution monitoring with 90-day retention, and intrusion detection system (Honeywell VISTA-250BPT) with door contacts, motion sensors, and environmental monitors detecting temperature excursions (>85°F triggers alarm). Transmitter remote control security implements Cisco AnyConnect SSL VPN requiring two-factor authentication (RSA SecurID hardware tokens) for engineer access from home/office, session timeout after 30 minutes inactivity, and privileged access management (CyberArk PAM) recording all CLI commands and configuration changes for forensic analysis with 7-year retention. SCADA security hardens transmitter controller (Harris FlexStar exciter running embedded Linux) through OS hardening (disabling unnecessary services, applying security patches monthly), firewall configuration (iptables rules blocking inbound connections except from authorized monitoring systems), and secure protocols (SSH v2 for CLI access, HTTPS for web interface, SNMPv3 with authentication/privacy). Supply chain security validates equipment authenticity through manufacturer certificates of conformity, anti-counterfeiting measures (holographic labels on amplifier modules, serialized components), and firmware integrity verification using cryptographic signatures (Harris public key stored in hardware security module) preventing malicious firmware installation. FCC compliance monitoring ensures adherence to technical rules 47 CFR Part 73 including: authorized power limits (ERP not exceeding license authorization ±5%), out-of-band emissions (meeting spectral mask), tower lighting and painting (FAA obstruction marking), and EAS participation (monthly required test transmission). Cybersecurity incident response plan addresses broadcast-specific scenarios: EAS false activation (immediate transmission cessation, FCC notification within 24 hours), transmitter control system compromise (isolate SCADA network, revert to manual control, engage third-party incident response), and ransomware encryption of automation systems (restore from offline backups maintained in Faraday cage preventing crypto-locking). Electromagnetic interference (EMI) mitigation implements RF shielding (transmitter building with copper mesh in walls, conductive paint, filtered HVAC penetrations), power line filtering (Corcom EMI filters on all AC inputs), and grounding system (ground ring with 10Ω resistance, lightning protection via surge arrestors) preventing interference with adjacent emergency services (700 MHz public safety band, 698-806 MHz cellular uplink). Compliance certifications include FCC equipment authorization (Grant of Equipment Authorization verifying compliance with technical standards), UL 1419 listing for professional video and audio equipment (safety certification), CE marking for European installations, and ISO 9001 quality management system certification for manufacturing facilities producing transmitter equipment ensuring consistent quality and reliability in critical broadcast infrastructure.
