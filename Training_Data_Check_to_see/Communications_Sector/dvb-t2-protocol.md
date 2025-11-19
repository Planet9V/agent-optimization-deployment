# DVB-T2 Digital Terrestrial Television Protocol - Communications Sector

## Entity-Rich Introduction

Digital Video Broadcasting - Terrestrial Second Generation (DVB-T2) standard published by ETSI EN 302 755 V1.4.1 revolutionizes terrestrial broadcasting with OFDM modulation supporting 256-QAM constellation achieving 45 Mbps throughput in 8 MHz UHF channel (470-862 MHz), utilizing LDPC forward error correction with code rates 1/2 to 5/6 providing 3-5 dB coding gain over DVB-T Reed-Solomon/convolutional codes. Rohde & Schwarz DVB-T2 modulator implements rotated QPSK/16-QAM/64-QAM/256-QAM constellations with I/Q component separation reducing impulse noise sensitivity 3 dB, Multiple-Input Single-Output (MISO) transmission from 2 transmitters providing diversity gain 5 dB improving mobile reception, and Physical Layer Pipe (PLP) multiplexing enabling differentiated robustness/capacity trade-offs for fixed rooftop vs mobile handheld services within single RF channel. Harris Maxiva UAX transmitter broadcasts DVB-T2 with 32K OFDM mode (32768 carriers) utilizing guard interval 1/128 (7 μs) enabling Single Frequency Network (SFN) operation with transmitters spaced 50 km apart, synchronized via GPS to <1 μs timing accuracy creating constructive interference expanding coverage area 40% compared to multi-frequency networks.

## Technical Specifications

**DVB-T2 Modulation Parameters**:
- FFT Sizes: 1K, 2K, 4K, 8K, 16K, 32K (extended mode for large SFN)
- Carriers: 853 (1K) to 27841 (32K) active subcarriers
- Guard Intervals: 1/128, 1/32, 1/16, 19/256, 1/8, 19/128, 1/4 (symbol duration fraction)
- Pilot Pattern: PP1-PP8 scattered pilots, continual pilots, edge pilots
- Constellation: QPSK, 16-QAM, 64-QAM, 256-QAM with rotation angles
- Rotation: 29° (QPSK), 16.8° (16-QAM), 8.6° (64-QAM), no rotation (256-QAM)
- Interleaving: Bit interleaver, cell interleaver, time interleaver (up to 70 ms)

**Forward Error Correction (FEC)**:
- Outer Code: BCH (Bose-Chaudhuri-Hocquenghem) for error detection
- Inner Code: LDPC (Low-Density Parity-Check) block length 16200 or 64800 bits
- Code Rates: 1/2, 3/5, 2/3, 3/4, 4/5, 5/6 (normal mode), 1/3, 2/5 (short frames)
- Coding Gain: 3-5 dB improvement vs DVB-T at BER 10^-11 after RS decoding
- Iterations: 50 LDPC iterations typical in receiver for maximum performance

**Physical Layer Pipe (PLP) Architecture**:
- PLP Types: Type 1 (continuous), Type 2 (time-sliced for power saving)
- Multiple PLPs: Up to 255 PLPs per RF channel with independent modulation/coding
- Common PLP: Shared data across all PLPs (EPG, signaling)
- Robustness Modes: PLP1 (QPSK 1/2 for mobile), PLP2 (256-QAM 5/6 for fixed)
- Time Interleaving: 0-250 ms per PLP, receiver buffer management

**Frame Structure**:
- Super Frame: Contains multiple T2 frames (up to 255 frames)
- T2 Frame: Preamble (P1) + L1 signaling (P2) + data symbols
- P1 Symbol: 1K FFT, 7-bit S1/S2 fields (transmission parameters)
- P2 Symbols: L1-pre and L1-post signaling (BPSK/16-QAM), robust FEC
- Data Symbols: Payload data organized in frequency/time interleaved cells
- FEF (Future Extension Frames): Reserved capacity for future services (DVB-NGH)

**Bandwidth and Throughput**:
- Channel Bandwidth: 1.7, 5, 6, 7, 8, 10 MHz (variable bandwidth tuning)
- Maximum Bitrate: 50.3 Mbps (8 MHz, 256-QAM, code rate 5/6, GI 1/128, 32K FFT)
- Typical HD Service: 12-15 Mbps H.264, 18-22 Mbps HEVC (1080p50)
- 4K UHD Service: 25-40 Mbps HEVC Main 10 profile with HDR
- Multiplexing: MPEG-2 TS (188-byte packets) or GSE (Generic Stream Encapsulation)

**MISO and SFN Features**:
- MISO (Multiple-Input Single-Output): Alamouti coding, 2-transmitter diversity
- SFN (Single Frequency Network): Co-channel operation of multiple transmitters
- GPS Synchronization: <1 μs timing accuracy via 10 MHz reference and 1 PPS
- Guard Interval: Must exceed maximum delay spread in SFN (e.g., 224 μs for GI 1/4 in 8K)
- SFN Gain: 3-6 dB improvement in coverage fringe areas

**Receiver Requirements**:
- Minimum C/N (Carrier-to-Noise): 3.5 dB (QPSK 1/2) to 22.8 dB (256-QAM 5/6)
- Doppler Tolerance: 80 Hz (32K FFT) to 2500 Hz (1K FFT) for mobile reception
- Time Interleaver Memory: 219 Mbit for maximum interleaving depth
- Decoding Latency: 50-250 ms depending on interleaver settings
- Channel Estimation: 2D interpolation of scattered/continual pilots

## Integration & Operations

DVB-T2 transmitter deployment across nationwide broadcast network (NETWORK-DTT-01) implements SFN architecture with 150 high-power transmitter sites operating on RF channel 25 (506-514 MHz UHF) synchronized via GPS timing receivers (Symmetricom TimeProvider 1000) maintaining <500 ns timing accuracy enabling constructive interference in overlap coverage zones. Rohde & Schwarz TX9 transmitter at main site (SITE-MAIN-01) generates 10 kW ERP utilizing 32K FFT mode with guard interval 1/16 (112 μs) accommodating maximum transmitter separation 33.6 km (speed of light × guard interval), modulation profile configured for three PLPs: PLP-0 (QPSK 2/3, 4 Mbps for mobile SD services), PLP-1 (64-QAM 3/4, 18 Mbps for fixed HD services), PLP-2 (256-QAM 4/5, 25 Mbps for fixed 4K UHD services). Content delivery network distributes MPEG-2 Transport Stream from national playout center via IP multicast (UDP/RTP) to transmitter sites over managed MPLS network with sub-50ms latency, utilizing Pro-MPEG FEC (SMPTE 2022-1) implementing XOR-based forward error correction tolerating 20% packet loss, monitoring with SMPTE 2022-4 TR 101 290 analysis detecting continuity counter errors, PMT/PAT inconsistencies, and PCR jitter >500 ns. DVB-T2 gateway equipment (Ateme Titan Live encoder/multiplexer) aggregates 5 HD program streams encoded with H.264 AVC High Profile (10 Mbps average, 15 Mbps peak VBR), 3 SD streams (3 Mbps MPEG-2), and 2 radio services (192 kbps AAC-LC), multiplexing into single 42 Mbps transport stream with PSI/SI tables (NIT, BAT, SDT, EIT) updated every 1 second providing EPG data 7 days in advance. Modulator configuration implements time interleaving 250 ms providing impulse noise protection against car ignition interference (5-10 ms duration), cell interleaving scrambling data across OFDM carriers preventing frequency-selective fading degradation, and L1-post signaling transmitting modulation parameters enabling fast channel scan completing in 150 ms (P1 symbol detection + L1 decoding). Coverage planning utilizes ITU-R P.1546 propagation model predicting field strength with terrain database (SRTM 90m resolution), building clutter data (urban/suburban/rural classifications), and frequency-dependent diffraction losses, designing network to achieve 99% location probability at 95% time availability within service area requiring median field strength 58 dBμV/m for portable indoor reception (QPSK 1/2 modulation, assumed 10 dB building penetration loss). Receiver compatibility testing validates interoperability with consumer equipment (Samsung, LG, Sony integrated digital TVs, set-top boxes) ensuring demodulation performance: measuring C/N thresholds matching theoretical values ±1 dB, verifying Doppler tolerance >100 Hz for vehicular mobile reception at 100 km/h, and validating time-interleaver de-interleaving reconstructing original bit stream after 250 ms delay. Network monitoring system (Qligent Vision) performs 24/7 RF and content quality analysis: spectrum monitoring (PROMAX Ranger Neo field strength meter) detecting co-channel interference from adjacent countries, MER (Modulation Error Ratio) measurement requiring >30 dB for 256-QAM reception, LDPC decoder iterations tracking with target <30 iterations indicating adequate C/N margin, and A/V quality monitoring (PEVQ scores >4.0 for HD, lip-sync tolerance <40ms).

## Security Implementation

DVB-T2 broadcast security implements conditional access integration with DVB-SimulCrypt architecture enabling pay-TV services: ECM (Entitlement Control Messages) transmitted in-band within transport stream every 1-10 seconds containing control words encrypted with subscriber-specific keys, EMM (Entitlement Management Messages) distributed via separate PID updating subscriber entitlements (channel packages, expiration dates), and Viaccess, Nagravision, or Conax CAS (Conditional Access System) smart cards decrypting scrambled content using AES-128 or proprietary algorithms. Content protection implements DVB-CSA (Common Scrambling Algorithm) version 3 with 128-bit AES-CBC encryption scrambling video/audio PES packets every 8-16 packets, control word rotation every 10-30 seconds preventing cryptanalysis, and two-tier encryption architecture with transmission key protecting control words stored in smart card secure element. Signal integrity monitoring detects unauthorized transmitters via spectrum surveillance (Rohde & Schwarz EB500 monitoring receiver) performing 24/7 sweeps of UHF band 470-862 MHz identifying rogue signals within ±1 MHz of licensed frequency, measuring EIRP exceeding 1W threshold triggering investigation, and direction-finding triangulation localizing interference sources for regulatory enforcement (FCC or Ofcom action). Studio-to-transmitter link security protects IP delivery infrastructure with IPsec VPN tunnels (IKEv2 with X.509 authentication, ESP with AES-256-GCM) encrypting transport stream between playout center and 150 transmitter sites, dedicated MPLS Layer 3 VPN (RFC 4364) isolating broadcast traffic from internet services, and QoS policies (DSCP EF marking) prioritizing real-time video preventing packet loss during network congestion. Transmitter access control restricts physical entry through biometric authentication (fingerprint + iris scan), 24/7 video surveillance (Axis P1428-E 4K cameras with 90-day retention), and intrusion detection (Honeywell Galaxy Dimension alarm panel) with duress codes alerting security operations center. SCADA network security isolates transmitter control systems (Rohde & Schwarz TMU9evo transmitter controller) in dedicated VLAN separated from corporate network by firewall (Cisco ASA 5516-X) permitting only SNMP monitoring (UDP 161), Modbus TCP control (TCP 502), and HTTPS remote access (TCP 443), blocking lateral movement preventing ransomware propagation. Emergency Alert System integration implements CAP (Common Alerting Protocol) message insertion via T2-MI (T2 Modulator Interface) protocol, pre-empting regular programming with emergency warnings (severe weather, AMBER alerts, civil emergencies), delivering geo-targeted alerts using DVB-T2 local service insertion capability selecting affected transmission sites within polygon boundary definitions. Compliance certifications include CE marking (RED 2014/53/EU radio equipment directive) demonstrating electromagnetic compatibility and efficient spectrum use, FCC Part 74 Subpart E certification for low-power TV and translator stations, ITU-R BT.1306 error correction performance standards, and ETSI TS 102 831 implementation guidelines validation ensuring interoperability between manufacturer equipment (transmitters, modulators, receivers). Cybersecurity incident response addresses broadcast-specific threats: transport stream injection attacks (validating digital signatures on TS packets using MPEG-2 DSM-CC), GPS spoofing prevention (multi-constellation GNSS receivers with anti-jamming, crosschecking GPS time against NTP servers), and modulator firmware validation (verifying cryptographic signatures against Rohde & Schwarz public key stored in hardware security module preventing malicious firmware installation).
