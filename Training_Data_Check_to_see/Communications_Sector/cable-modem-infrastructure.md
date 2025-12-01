# Cable Modem Infrastructure Equipment - Communications Sector

## Entity-Rich Introduction

Arris E6000 Converged Edge Router (CER) serves as CMTS (Cable Modem Termination System) supporting DOCSIS 3.1 specifications with 32 downstream OFDM channels (192 MHz total) and 8 upstream OFDMA channels (96 MHz), enabling multi-gigabit service delivery to 20,000+ cable modems per chassis. Cisco cBR-8 Converged Broadband Router integrates DOCSIS 3.1 capability with 10 Gbps per downstream port capacity, utilizing Modular Cable Interface Line Card (MC-88V) supporting 88 downstream channels and 176 upstream channels with MPEG-2 Single Program Transport Stream (SPTS) video delivery. Casa Systems CCAP C100G platform implements Distributed CCAP architecture with Remote PHY Devices (RPD) extending fiber-deep architecture to 1 Gbps per subscriber, employing DEPI (Downstream External PHY Interface) and UEPI (Upstream EPHI) protocols over 10 Gbps Ethernet backhaul. Harmonic VOS Media Platform integrates with CableLabs DOCSIS-provisioning specifications, providing video-on-demand and broadcast services through MPEG-4 AVC and HEVC encoding at bitrates ranging from 3 Mbps (SD) to 15 Mbps (4K UHD).

## Technical Specifications

**Arris E6000 CER Specifications**:
- Model: Arris E6000 Converged Edge Router (DOCSIS 3.1 compliant)
- Downstream Capacity: 32 OFDM channels, 4096-QAM modulation, 50 kHz subcarrier spacing
- Downstream Bandwidth: 192 MHz total (6 MHz bonded channels)
- Upstream Capacity: 8 OFDMA channels, 1024-QAM modulation, 25-50 kHz subcarriers
- Upstream Bandwidth: 96 MHz total (6.4 MHz bonded channels)
- Subscriber Capacity: 20,000 cable modems per chassis, 100,000 per system
- Throughput: 10 Gbps downstream per port, 2 Gbps upstream per port
- Protocols: DOCSIS 3.1 (CM-SP-MULPIv3.1), DOCSIS 3.0 backward compatible, EuroDOCSIS
- Network Interfaces: 100 Gbps Ethernet uplinks (CFP2 optics), 10 Gbps management
- Power Consumption: 2400W typical, N+1 redundant PSU (3000W total)
- Environmental: Operating temp 0°C to +45°C, 10-90% humidity non-condensing
- MTBF: 200,000 hours, hot-swappable modules

**Cisco cBR-8 Technical Details**:
- Model: Cisco cBR-8 Converged Broadband Router (IOS-XE 16.x)
- Line Card: MC-88V Modular Cable Interface (88 DS, 176 US channels)
- DOCSIS Version: 3.1 full duplex, DOCSIS 3.0/2.0 legacy support
- Modulation: Downstream 4096-QAM (12 bits/symbol), Upstream 1024-QAM (10 bits/symbol)
- Spectrum: Extended spectrum DOCSIS (ESD) 108 MHz - 1218 MHz
- Service Groups: 128 service groups per chassis, dynamic bonding group assignment
- Video Integration: QAM video (MPEG-2 TS), EQAM, narrowcast switched digital video
- Timing: DOCSIS Timing Interface (DTI) server, GPS/BITS synchronization
- Management: SNMP v3, CLI (SSH v2), NETCONF/YANG, Cisco Prime provisioning
- Redundancy: 1+1 supervisor redundancy, N+1 PSU, graceful supervisor switchover <1 second

**Casa Systems C100G CCAP Specifications**:
- Model: Casa Systems C100G Converged Cable Access Platform
- Architecture: Distributed CCAP with Remote PHY/MAC-PHY split
- RPD Support: 500 Remote PHY Devices per core, 10 Gbps per RPD
- DEPI/UEPI: L2TPv3 tunneling over IP/MPLS backhaul, sub-10ms latency
- Capacity: 100 Gbps total throughput, 1 Gbps per subscriber DOCSIS 3.1
- Node Split: 1:1 node splitting capability, fiber-deep to 50-100 homes passed
- Protocols: DOCSIS 3.1, CableLabs Remote PHY specification MHAv2
- Network Functions: Integrated CMTS, EQAM, switched digital video
- Management: CasaOS provisioning, TR-069 CPE management, SNMP v2c/v3

**Harmonic VOS Media Platform Details**:
- Model: Harmonic VOS 360 Media SaaS Platform
- Video Codecs: MPEG-2, MPEG-4 AVC (H.264), HEVC (H.265), AV1 support
- Bitrate Profiles: SD 3-5 Mbps, HD 8-12 Mbps, 4K UHD 15-25 Mbps
- Adaptive Bitrate: HLS (HTTP Live Streaming), MPEG-DASH with 6-10 quality ladders
- DRM: Widevine, PlayReady, FairPlay Streaming, multi-DRM workflow
- Encryption: AES-128 CTR mode for HLS, CENC (Common Encryption) for DASH

## Integration & Operations

Arris E6000 deployment in regional headend facilities (HE-CENTRAL-01, HE-NORTH-02, HE-SOUTH-03) aggregates 150,000+ subscribers across 50 fiber nodes, with each service group supporting 400-600 cable modems sharing 10 Gbps downstream capacity. DOCSIS provisioning integrates with Incognito DOCSIS Provisioning Server using DHCP Option 122 (CableLabs client configuration), TFTP for configuration file delivery, and ToD (Time of Day) protocol for modem clock synchronization. Cisco cBR-8 routers connect to core network via 100 Gbps QSFP28 fiber uplinks, implementing policy-based routing with Cisco Service Control Engine (SCE) for subscriber traffic management at Layer 7, enforcing bandwidth policies (50 Mbps economy tier, 500 Mbps standard, 1 Gbps premium). Casa C100G Remote PHY architecture deploys RPD nodes at fiber concentration points 5-10 km from headend, with DEPI tunnels encapsulating QAM RF signals over IP transport utilizing Juniper MX960 edge routers with MPLS VPN segmentation. Performance monitoring through Cisco Broadband Network Gateway (BNG) tracks per-subscriber metrics: average throughput (target 85% of provisioned speed), latency (target <15ms to local CDN cache), packet loss (target <0.1%), and utilization (target 60-75% channel loading). Video delivery via Harmonic Electra X3 encoders generates MPEG-4 AVC streams at 1080p60 (10 Mbps), distributed through QAM modulators (Harmonic NSG 9000) occupying channels 79-135 (549-867 MHz) with 256-QAM modulation. Cable modem firmware upgrades utilize DOCSIS TFTP mechanism, pushing Broadcom BCM3390 chipset firmware to 50,000 modems nightly during 2-5 AM maintenance window, monitored through Arris CHP Max provisioning system with rollback capability if <95% success rate.

## Security Implementation

DOCSIS network security implements Baseline Privacy Plus Interface (BPI+) specification with 128-bit AES encryption for downstream traffic and 56-bit DES encryption for upstream (legacy DOCSIS 2.0), with DOCSIS 3.1 mandating AES-256 for all traffic flows. Cable modem authentication utilizes X.509 digital certificates issued by CableLabs DOCSIS Root CA, with modem manufacturers (Arris TG3482G, Netgear CM1200, Motorola MB8600) embedding unique RSA 2048-bit key pairs in secure element hardware. Network access control enforces per-subscriber VLANs (VLAN 100-65535 range) with Dynamic Host Configuration Protocol Security (DHCP Snooping) preventing rogue DHCP servers, integrated with Arris CHP Max authentication database validating subscriber entitlements. Upstream spectrum monitoring deploys Cisco Spectrum Management System analyzing 5-42 MHz return path for ingress noise and interference, automatically triggering pre-equalization coefficients in cable modem upstream transmitters to compensate for plant impairments. Physical layer security includes CommScope hardline trunk cable with quad-shield construction (RG-11 equivalent), encrypted node-to-headend fiber utilizing 100GBASE-LR4 optics with MACsec encryption (IEEE 802.1AE), preventing optical tap attacks. Harmonic VOS platform implements multi-DRM key rotation every 30 seconds for premium video content, with Google Widevine Level 1 hardware-backed DRM requiring secure video path through HDCP 2.2 protected HDMI outputs on set-top boxes (Arris VIP5662W, Cisco 9865HDC). Compliance certifications include CableLabs DOCSIS certification, FCC Part 76 (cable television service), and SCTE standards adherence for network interface specifications.
