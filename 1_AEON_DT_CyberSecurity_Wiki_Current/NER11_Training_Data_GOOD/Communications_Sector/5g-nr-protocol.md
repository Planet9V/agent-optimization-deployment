# 5G New Radio (NR) Protocol - Communications Sector

## Entity-Rich Introduction

5G New Radio implements 3GPP Release 15/16/17 specifications defining air interface between User Equipment (UE) and gNodeB base station, utilizing OFDM (Orthogonal Frequency Division Multiplexing) with flexible numerology supporting subcarrier spacings of 15 kHz, 30 kHz, 60 kHz, and 120 kHz for sub-6 GHz and mmWave frequency bands. CP-OFDM (Cyclic Prefix OFDM) modulation in downlink achieves spectral efficiency of 30 bits/Hz/cell using 256-QAM with 8-layer MIMO transmission, while DFT-s-OFDM (Discrete Fourier Transform spread OFDM) in uplink reduces peak-to-average power ratio (PAPR) from 12 dB to 6 dB improving UE power amplifier efficiency. 3GPP TS 38.211 physical layer specification defines resource grid structure with 12 subcarriers per Physical Resource Block (PRB), 14 OFDM symbols per slot, and 10ms frame duration containing 10 subframes, enabling flexible TDD (Time Division Duplex) configurations with 2.5ms, 1.25ms, or 0.5ms DL/UL switching periodicity. NR supports bandwidth parts (BWP) allowing UE operation on fraction of total carrier bandwidth (20 MHz BWP within 100 MHz carrier), reducing power consumption by 50% for IoT and eMBB (enhanced Mobile Broadband) use cases.

## Technical Specifications

**5G NR Frequency Bands and Numerology**:
- FR1 (Frequency Range 1): Sub-6 GHz bands n1, n2, n3, n5, n7, n8, n20, n28, n38, n40, n41, n48, n66, n71, n77, n78, n79
- FR2 (Frequency Range 2): mmWave bands n257 (26.5-29.5 GHz), n258 (24.25-27.5 GHz), n260 (37-40 GHz), n261 (27.5-28.35 GHz)
- Subcarrier Spacing: 15 kHz (LTE compatible), 30 kHz (default sub-6 GHz), 60 kHz (high mobility), 120 kHz (mmWave), 240 kHz (mmWave URLLC)
- Slot Duration: 1ms (15 kHz SCS), 0.5ms (30 kHz), 0.25ms (60 kHz), 0.125ms (120 kHz)
- Channel Bandwidth: 5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 90, 100 MHz (FR1), 50-400 MHz (FR2)
- Modulation: QPSK, 16-QAM, 64-QAM, 256-QAM (DL), Pi/2-BPSK (UL coverage extension)
- MIMO Layers: Up to 8 DL layers, 4 UL layers per UE
- SU-MIMO: Single-user up to 8×8, MU-MIMO: Multi-user up to 12 layers total

**Frame Structure and Resource Grid**:
- Frame Duration: 10ms containing 10 subframes (1ms each)
- Slot Configuration: 14 OFDM symbols per slot (normal CP), 12 symbols (extended CP)
- Resource Block: 12 consecutive subcarriers in frequency domain
- Resource Element: One subcarrier for one OFDM symbol duration
- Numerology: μ = 0 (15 kHz), μ = 1 (30 kHz), μ = 2 (60 kHz), μ = 3 (120 kHz), μ = 4 (240 kHz)
- Symbols per Frame: 140 (15 kHz), 280 (30 kHz), 560 (60 kHz), 1120 (120 kHz)

**Protocol Stack (3GPP TS 38.300)**:
- Physical Layer (PHY): OFDM modulation, channel coding (LDPC data, Polar control), HARQ
- MAC (Medium Access Control): Scheduling, HARQ retransmissions, multiplexing, BWP operation
- RLC (Radio Link Control): Segmentation, ARQ, duplicate detection, in-sequence delivery
- PDCP (Packet Data Convergence Protocol): Header compression (ROHC), ciphering, integrity protection
- SDAP (Service Data Adaptation Protocol): QoS flow to DRB mapping, marking QoS flow ID
- RRC (Radio Resource Control): Broadcast, paging, connection management, measurement configuration

**TDD Configuration Patterns**:
- Pattern 1: 7D-2G-1U (7 DL slots, 2 guard, 1 UL per 5ms period)
- Pattern 2: 3D-1S-1U (3 DL, 1 special slot, 1 UL per 2.5ms)
- Pattern 3: 4D-1S-5U (4 DL, 1 special, 5 UL for UL-heavy traffic)
- Slot Format: All DL (D), All UL (U), Flexible (F), Special (S) with configurable GP (Guard Period)
- Dynamic TDD: Slot format indicator (SFI) in DCI format 2_0 enabling sub-millisecond adaptation

**Channel Coding Specifications**:
- Data Channels: LDPC (Low-Density Parity-Check) with code rates 1/5 to 8/9
- Control Channels: Polar coding with code rates 1/12 to 1/2
- CRC: 24-bit CRC for TB >3824 bits, 16-bit CRC for smaller TBs
- Code Block Segmentation: Maximum 8448 bits per code block
- HARQ: Asynchronous adaptive in DL, synchronous non-adaptive in UL, max 16 processes

## Integration & Operations

5G NR gNodeB deployment (gNB-SITE-001 through gNB-SITE-100) implements standalone (SA) architecture with direct connection to 5G Core Network via N2 interface (NG-AP protocol) for control plane and N3 interface (GTP-U encapsulation) for user plane traffic, eliminating LTE anchor dependency. Dual connectivity (EN-DC) configuration enables simultaneous LTE eNB and 5G gNB operation, with LTE serving as master node (MeNB) managing RRC connection while 5G provides secondary cell group (SCG) achieving 2 Gbps peak throughput combining 4G anchor (200 Mbps) and 5G data bearer (1.8 Gbps). Network slicing implementation creates logically isolated networks sharing physical infrastructure: eMBB slice (SST=1) for consumer broadband with best-effort QoS, URLLC slice (SST=2) for industrial automation requiring <1ms latency and 99.9999% reliability, mMTC slice (SST=3) for IoT sensors with 1 million devices per km². Beamforming operation utilizes CSI-RS (Channel State Information Reference Signal) transmission every 5ms enabling UE measurement of 64 beam patterns, reporting PMI (Precoding Matrix Indicator) from 3GPP codebook allowing gNodeB selection of optimal beam weights for 8T8R Massive MIMO antenna. Mobility management executes handover procedure completing RRC reconfiguration within 50ms interruption time, utilizing L3 RSRP (Reference Signal Received Power) measurements with 3 dB hysteresis and 160ms time-to-trigger preventing ping-pong effect between adjacent cells. Ericsson Packet Core implementation provisions network slices with dedicated QoS parameters: eMBB QCI=9 (best effort, no GBR), URLLC QCI=1 (GBR 100 Mbps, latency <10ms), mMTC QCI=8 (delay tolerant, 128 kbps), enforced through Policy and Charging Rules Function (PCRF). Performance monitoring tracks gNodeB KPIs: RRC connection success rate (target >99.5%), average cell spectral efficiency (target 3.5 bits/Hz), handover success rate (target >98%), PRB utilization (target 60-75%), and user-perceived throughput (target 250 Mbps DL median).

## Security Implementation

5G NR security architecture implements 256-bit encryption using NEA2 (SNOW 3G), NEA3 (ZUC), or AES-CTR algorithms for user plane confidentiality, with integrity protection utilizing NIA2 (SNOW 3G) or NIA3 (ZUC) algorithms generating 32-bit MAC-I tags appended to control plane messages. Initial authentication executes 5G-AKA (Authentication and Key Agreement) protocol deriving 256-bit anchor key (KAUSF) from permanent key (K) stored in USIM, subsequently generating intermediate keys KSEAF, KAMF, and base station key (KgNB) through SHA-256 HMAC key derivation functions defined in 3GPP TS 33.501. Subscription Concealed Identifier (SUCI) protection encrypts IMSI using ECIES (Elliptic Curve Integrated Encryption Scheme) with Curve25519 public key, preventing IMSI catcher attacks that plagued 4G LTE networks with fake base stations. Security anchoring in 5G Core network enforces security context establishment before data transmission, with AMF (Access and Mobility Management Function) validating UE security capabilities negotiation ensuring minimum security level (NULL encryption prohibited in commercial networks). Replay protection implements 5-bit HFN (Hyper Frame Number) and 27-bit COUNT value forming 32-bit sequence number preventing replay attacks, with COUNT verification rejecting packets outside 2048-packet window. Fronthaul security between gNodeB CU (Centralized Unit) and DU (Distributed Unit) employs IPsec tunnels with IKEv2 key exchange, ESP protocol providing AES-256-GCM authenticated encryption, protecting NGAP and GTP-U traffic over untrusted transport networks. Physical layer security leverages downlink beamforming reducing signal leakage to unintended receivers by 20 dB, combined with Physical Layer Cell ID scrambling (504 unique IDs) preventing easy signal identification. SIM security mandates 5G-capable USIM (Universal Subscriber Identity Module) supporting TUAK (Tunable Authentication and Key Agreement) algorithm with 256-bit keys, superseding MILENAGE algorithm limited to 128-bit security. Compliance certifications include 3GPP SECAM Security Assurance Specification (SCAS), GSMA NESAS Level 2 certification for network equipment, and Common Criteria EAL4+ for cryptographic modules protecting key material.
