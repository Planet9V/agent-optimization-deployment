# Telecommunications Equipment and Network Elements

## Document Overview
**Domain**: IT/Telecom Sector - Telecommunications Equipment and Legacy Systems
**Categories**: Equipment (5), Vendors (5), Suppliers (3), Protocols (5), Standards (2)
**Scope**: Legacy 2G/3G/4G networks, PSTN, optical transport, submarine cables, satellite communications

---

## 1. Legacy Mobile Networks (2G/3G/4G)

### 2G GSM Infrastructure
```yaml
base_station_subsystem:
  bts_base_transceiver:
    ericsson_rbs2000:
      type: "Macro BTS for GSM 900/1800"
      sectors: "3 sectors typical 120° beamwidth"
      transceivers: "Up to 12 TRX per sector"
      power_output: "40W per TRX (46 dBm)"
      capacity: "96 voice calls per sector"
      modulation: "GMSK with Gaussian pulse shaping"
      interfaces: "Abis interface to BSC via E1/T1"

    nokia_flexi_bts:
      type: "GSM/EDGE base station"
      form_factor: "Outdoor cabinet or indoor rack"
      bands: "850, 900, 1800, 1900 MHz"
      capacity: "Up to 144 voice erlangs per site"
      edge: "Enhanced data rates EDGE class 12"
      backhaul: "Abis over TDM E1 2 Mbps"

  bsc_base_station_controller:
    ericsson_bsc:
      model: "BSC APG40 with APZ processor"
      capacity: "Up to 2000 BTS connections"
      processing: "Call setup, handover, power control"
      interfaces:
        a_interface: "To MSC via SS7 signaling"
        abis_interface: "To BTS via TDM circuits"
      features:
        - "Frequency hopping coordination"
        - "Handover algorithms inter/intra-cell"
        - "Radio resource allocation"

network_switching:
  msc_mobile_switching:
    ericsson_msc:
      product: "AXE10 Mobile Switching Center"
      capacity: "2M subscribers, 200K BHCA"
      protocols: "MAP (Mobile Application Part) over SS7"
      interfaces:
        a_interface: "BSC connection"
        e_interface: "Other MSC for roaming"
        d_interface: "HLR/VLR lookup"
      functions:
        - "Call routing and setup"
        - "Mobility management"
        - "Charging and billing"

  hlr_home_location:
    nokia_hlr:
      capacity: "100M subscriber records"
      database: "Telecom-grade distributed DB"
      protocols: "MAP over SS7 for location updates"
      data_stored:
        - "IMSI and MSISDN mapping"
        - "Subscription profile and services"
        - "Current VLR location"
        - "Authentication triplets (Ki)"

  vlr_visitor_location:
    function: "Temporary subscriber data in MSC area"
    capacity: "5M visiting subscribers"
    updates: "Location area update messages"
```

### 3G UMTS Networks
```yaml
nodeb_base_station:
  ericsson_rbs3000:
    type: "3G WCDMA NodeB"
    frequency: "2100 MHz UMTS Band I"
    carriers: "Up to 3 carriers 5MHz each"
    power: "2x 40W per sector = 80W total"
    mimo: "2x2 MIMO for HSPA+"
    capacity: "384 kbps R99, 14.4 Mbps HSPA+, 42 Mbps DC-HSPA+"
    interfaces: "Iub interface to RNC via ATM or IP"

  nokia_flexi_multiradio_bts:
    type: "Multi-standard 2G/3G base station"
    bands: "GSM 900/1800 + WCDMA 2100"
    capacity: "12 GSM TRX + 3 WCDMA carriers"
    software_upgradeable: "Field upgrade to 4G LTE"
    backhaul: "IP/MPLS over microwave or fiber"

rnc_radio_network:
  huawei_rnc:
    model: "BSC6910 RNC with WCDMA"
    capacity: "10,000 NodeB connections"
    processing: "Admission control, RRC signaling"
    interfaces:
      iub: "To NodeB via ATM/IP"
      iur: "To other RNC for soft handover"
      iu_cs: "To MSC circuit-switched"
      iu_ps: "To SGSN packet-switched"
    features:
      - "Soft handover combining"
      - "Power control loop 1500 Hz"
      - "Load balancing across cells"

packet_core:
  sgsn_serving_gprs:
    ericsson_sgsn:
      capacity: "50M PDP contexts"
      throughput: "100 Gbps aggregate"
      protocols: "GTP-C for control, GTP-U for user"
      interfaces:
        gb: "To BSS for 2G"
        iu_ps: "To RNC for 3G"
        gn: "To GGSN for internet"
        s3: "To MME for LTE handoff"

  ggsn_gateway_gprs:
    cisco_ggsn:
      model: "ASR 5000 GGSN module"
      capacity: "32M PDP contexts"
      throughput: "160 Gbps"
      apn: "1000 APNs supported"
      protocols: "GTPv1 for tunnel, Diameter for charging"
      features:
        - "NAT with carrier-grade address pool"
        - "DPI for traffic shaping"
        - "Lawful intercept interfaces"
```

### 4G LTE Networks
```yaml
enodeb_evolved_nodeb:
  ericsson_rbs6000:
    type: "4G LTE macro base station"
    bands: "Band 3 (1800MHz), Band 7 (2600MHz), Band 20 (800MHz)"
    bandwidth: "Up to 20 MHz per carrier"
    mimo: "4x4 MIMO for DL, 2x2 for UL"
    carrier_aggregation: "3CA with 60 MHz total"
    throughput: "300 Mbps DL, 75 Mbps UL"
    power: "2x 80W per sector = 160W RRU"
    interfaces: "S1 to EPC, X2 to eNodeB via IP"
    features:
      - "SON for self-optimization"
      - "CoMP coordinated multipoint"
      - "eICIC for interference mitigation"

  nokia_aira:
    type: "Liquid Radio LTE software-defined"
    deployment: "Cloud RAN architecture"
    baseband: "Centralized BBU pool"
    fronthaul: "CPRI over dark fiber up to 20km"
    capacity: "Dynamic allocation across cells"

  huawei_elabel:
    model: "DBS5900 distributed base station"
    bbu: "BBU5900 supports 192 cells"
    rru: "RRU up to 4x 60W for massive MIMO"
    bands: "Multi-band support with software license"
    spectrum_sharing: "DSS for LTE/5G NR"

epc_evolved_packet_core:
  mme_mobility_management:
    nokia_mme:
      capacity: "20M subscribers per MME"
      attach_rate: "100,000 per hour"
      interfaces: "S1-MME, S6a, S10, S11"
      protocols: "NAS, S1AP, Diameter"
      features:
        - "Tracking area list management"
        - "NAS security mode"
        - "Handover with S1/X2"

  sgw_pgw_gateways:
    ericsson_sgw_pgw:
      product: "SGSN-MME/S-GW/P-GW combined node"
      throughput: "400 Gbps per chassis"
      sessions: "64M concurrent bearers"
      redundancy: "N+1 with geo-redundancy"
      interfaces:
        s1_u: "eNodeB user plane"
        s5_s8: "SGW to PGW"
        sgi: "Internet breakout"
```

---

## 2. PSTN and Circuit-Switched Networks

### Class 4 and Class 5 Switches
```yaml
class_5_switches:
  ericsson_axe:
    model: "AXE10 local exchange"
    capacity: "1.2M subscriber lines"
    bhca: "3M busy hour call attempts"
    signaling: "SS7 ISUP for trunk signaling"
    interfaces:
      - "Analog subscriber lines with BORSCHT"
      - "ISDN BRI 2B+D basic rate"
      - "ISDN PRI 30B+D or 23B+D primary rate"
    features:
      - "Centrex services for business"
      - "CLASS features (caller ID, call waiting)"
      - "Prepaid calling card platform"

  nortel_dms100:
    model: "Digital Multiplex System"
    capacity: "100,000 lines per switch"
    architecture: "Distributed processing nodes"
    protocols: "GR-303 for remote terminals"
    features:
      - "Meridian digital centrex"
      - "Enhanced 911 ALI database"
      - "SCP integration for IN services"

class_4_switches:
  nokia_s12:
    type: "Tandem toll switch"
    capacity: "300,000 trunk terminations"
    trunks: "DS1, DS3, OC-3 interfaces"
    signaling: "SS7 for inter-exchange"
    routing: "Least-cost routing tables"
    features:
      - "Operator services platform"
      - "International gateway"
      - "SS7 STP co-located"

softswitches:
  metaswitch_mas:
    product: "MetaSphere Application Server"
    architecture: "IMS-based softswitch"
    capacity: "50M subscribers"
    protocols: "SIP, SIP-I, ISUP for legacy"
    features:
      - "VoLTE and VoWiFi support"
      - "TAS for supplementary services"
      - "Interworking to PSTN via MGW"

  broadsoft_broadworks:
    product: "BroadWorks platform"
    deployment: "Cloud or on-premises"
    capacity: "100M subscribers"
    applications:
      - "Hosted PBX for SMB"
      - "UC-One mobile client"
      - "Call center ACD features"
    protocols: "SIP with SDP for media"

media_gateways:
  cisco_mgx:
    model: "MGX 8800 media gateway"
    interfaces: "TDM to IP conversion"
    capacity: "32,000 DS0 circuits"
    codecs: "G.711, G.729, G.723.1"
    protocols: "MGCP, H.248/Megaco control"

  audiocodes_mediant:
    model: "Mediant 9000 SBC + gateway"
    capacity: "100,000 sessions"
    transcoding: "Hardware DSP transcoding"
    trunking: "SIP trunking to carriers"
```

### Signaling Systems
```yaml
ss7_signaling:
  stp_signal_transfer:
    vendor: "Cisco ITP (IP Transfer Point)"
    capacity: "100,000 messages per second"
    protocols: "MTP, SCCP, TCAP, ISUP, MAP"
    interfaces:
      - "56 kbps SS7 links (A-links)"
      - "SIGTRAN M3UA over IP"
    features:
      - "GTT global title translation"
      - "Screening for robocall prevention"
      - "Geo-redundant pairs with load sharing"

  scp_service_control:
    function: "800 number, LNP, calling card services"
    database: "Oracle or Sybase backend"
    capacity: "20,000 TPS (transactions per second)"
    protocols: "TCAP queries over SS7"

sigtran:
  protocol_stack:
    m3ua: "MTP3 User Adaptation over SCTP"
    m2ua: "MTP2 User Adaptation"
    sua: "SCCP User Adaptation"
  deployment: "IP transport for SS7 signaling"
  sctp: "Stream Control Transmission Protocol multi-homing"

diameter:
  use_cases:
    - "4G LTE S6a interface MME to HSS"
    - "Policy control Gx interface PCEF to PCRF"
    - "Charging Gy interface for prepaid"
  vendors:
    - "Oracle Communications Diameter Signaling Router"
    - "F5 Traffix SDC (Signaling Delivery Controller)"
  capacity: "1M messages per second per node"
```

---

## 3. Optical Transport Networks

### DWDM Systems
```yaml
ciena_6500:
  product: "Ciena 6500 Packet-Optical Platform"
  architecture: "Converged packet + optical"
  capacity: "Up to 8.8 Tbps per chassis"
  wavelengths: "96 channels 50 GHz DWDM grid"
  coherent_optics:
    waveLogic_5_extreme:
      - "800 Gbps per wavelength"
      - "Probabilistic constellation shaping"
      - "SD-FEC soft-decision forward error correction"
      - "Reach up to 4000 km with ROADM"
  applications:
    - "Long-haul backbone transport"
    - "Data center interconnect"
    - "5G xhaul aggregation"
  management: "Ciena Blue Planet MCP orchestration"

nokia_1830_pss:
  product: "Nokia 1830 Photonic Service Switch"
  capacity: "14.4 Tbps per node"
  wavelengths: "80 channels C-band DWDM"
  coherent:
    pse_3s:
      - "600 Gbps per wavelength"
      - "Nyquist subcarriers for spectral efficiency"
      - "Reach 1500 km ultra-long haul"
  roadm: "CDC-F ROADM colorless directionless contentionless"
  automation: "Nokia NSP with path computation engine"

infinera_xtm:
  product: "Infinera XTM Series"
  capacity: "6 Tbps per module"
  pic_technology: "Photonic Integrated Circuit"
  wavelength: "Super-channel with 500G wavelengths"
  features:
    - "Instant Bandwidth dynamic capacity"
    - "GeoMesh submarine applications"
    - "XR optics with liquid cooling"
  use_case: "Subsea cable systems + terrestrial"

huawei_otn:
  model: "OptiXtrans E9600"
  capacity: "32 Tbps per subrack"
  otn_switching: "OTN electrical cross-connect"
  wavelength: "200G/400G/600G coherent"
  applications:
    - "Metro aggregation with OTN grooming"
    - "5G fronthaul with eCPRI over OTN"
    - "Private line services carrier Ethernet"

roadm_systems:
  finisar_wavelogic:
    type: "Reconfigurable optical add-drop multiplexer"
    ports: "Up to 48 directions colorless"
    switching: "WSS wavelength selective switch"
    gridless: "Flexible grid 12.5 GHz spacing"
    applications: "Mesh network topology"

  ntt_silica_plc:
    type: "Planar lightwave circuit AWG"
    channels: "40 or 80 channel fixed DWDM"
    insertion_loss: "< 3 dB typical"
    use_case: "Point-to-point systems"
```

### Short-Reach Optical
```yaml
datacom_optics:
  multimode_fiber:
    sfp_plus_10g:
      - "Cisco SFP-10G-SR 850nm"
      - "OM3 300m, OM4 400m reach"
      - "10GBASE-SR IEEE 802.3ae"
    qsfp28_100g:
      - "Mellanox MMA1B00-C100D 850nm"
      - "OM4 100m reach"
      - "100GBASE-SR4 4x 25G lanes"

  single_mode_fiber:
    sfp_plus_10g_lr:
      - "Finisar FTLX1471D3BCL 1310nm"
      - "10 km reach SMF"
      - "10GBASE-LR IEEE standard"
    qsfp28_100g_lr4:
      - "Cisco QSFP-100G-LR4-S 1310nm"
      - "10 km reach SMF"
      - "4x 25G CWDM wavelengths"
    qsfp_dd_400g:
      - "400GBASE-DR4 500m reach"
      - "400GBASE-FR4 2 km reach"
      - "8x 50G PAM4 modulation"

active_optical_cables:
  twinax_dac:
    - "Mellanox MC2210310-001 1m DAC"
    - "100G QSFP28 passive copper"
    - "Power < 0.1W per end"
  aoc_active:
    - "Cisco QSFP-H40G-AOC10M"
    - "40G QSFP+ 10m active optical"
    - "OM3 MMF ribbon fiber"
```

---

## 4. Submarine and Satellite Systems

### Submarine Cable Systems
```yaml
transatlantic_cables:
  dunant:
    owner: "Google"
    route: "Virginia Beach, USA to Atlantic coast France"
    length: "6600 km"
    capacity: "350 Tbps design capacity"
    fiber_pairs: "12 fiber pairs"
    technology: "SDM space-division multiplexing"
    landing_stations:
      - "Virginia Beach, Virginia, USA"
      - "Saint-Hilaire-de-Riez, France"
    rfs: "Ready for service 2021"

  marea:
    owner: "Microsoft + Facebook + Telxius"
    route: "Virginia Beach to Bilbao, Spain"
    length: "6600 km"
    capacity: "200 Tbps (upgradeable)"
    fiber_pairs: "8 fiber pairs"
    repeaters: "Optical amplifiers every 50-70 km"
    branching_units: "Subsea branching for redundancy"
    rfs: "2018"

transpacific_cables:
  faster:
    consortium: "Google, NEC, China Mobile, etc."
    route: "Oregon, USA to Japan (Chikura, Shima)"
    length: "11629 km longest segment"
    capacity: "60 Tbps design"
    fiber_pairs: "6 fiber pairs"
    coherent: "100G coherent optics"
    landing_points:
      - "Bandon, Oregon"
      - "Chikura, Japan"
      - "Shima, Japan"
    rfs: "2016"

  jupiter:
    owner: "Amazon + SoftBank + KDDI"
    route: "USA to Japan direct"
    length: "14000 km"
    capacity: "60 Tbps"
    branches: "Philippines branching unit"
    rfs: "2020"

cable_infrastructure:
  repeaters:
    type: "Optical amplifier with EDFA"
    power: "Remote fed 10-15 kV DC"
    gain: "15-20 dB optical gain"
    spacing: "50-70 km between repeaters"
    lifespan: "25 years design life"

  branching_units:
    function: "Underwater fiber distribution"
    insertion_loss: "< 1 dB per branch"
    waterproof: "Pressure rated 8000m depth"

  cable_ships:
    vessels:
      - "CS依田丸 Daikaimaru (NEC)"
      - "Ile de Brehat (Orange Marine)"
      - "Leon Thevenin (ASN)"
    capabilities:
      - "Cable laying at 0.5-1 km/hour"
      - "ROV for repairs at 2500m depth"
      - "Cable storage 5000 km capacity"
```

### Satellite Communications
```yaml
geo_satellites:
  intelsat_40e:
    type: "Geostationary communications satellite"
    orbit: "35,786 km altitude GEO"
    coverage: "North America + Caribbean"
    bands: "C-band, Ku-band, Ka-band"
    capacity: "140 Gbps throughput"
    beams: "High-throughput spot beams"
    lifespan: "15 years operational"
    launch: "SpaceX Falcon 9"

  ses_17:
    coverage: "Americas + Atlantic"
    capacity: "200 Gbps with 200 Ka-band beams"
    applications: "Aero, maritime, enterprise"
    electric_propulsion: "All-electric satellite"

leo_constellations:
  starlink:
    operator: "SpaceX"
    satellites: "5000+ satellites launched (2024)"
    constellation: "12,000 planned Phase 1"
    orbit: "550 km altitude LEO"
    latency: "20-40 ms typical"
    bandwidth: "Up to 350 Mbps download"
    user_terminal:
      - "Phased array antenna 58cm dish"
      - "Auto-tracking with GPS + gyro"
      - "Power consumption 50-75W"
    applications: "Residential internet, maritime, aviation"

  oneweb:
    satellites: "648 satellite constellation"
    orbit: "1200 km altitude polar"
    coverage: "Global above 50° latitude priority"
    bandwidth: "50-200 Mbps per terminal"
    latency: "< 50 ms"
    use_case: "Enterprise, government, backhaul"

gateway_earth_stations:
  ka_band_gateway:
    dish_size: "13.5m reflector antenna"
    frequency: "29.5-30 GHz uplink, 19.7-20.2 GHz downlink"
    eirp: "90 dBW equivalent isotropic radiated power"
    g_t: "40 dB/K figure of merit"
    capacity: "10 Gbps per gateway"

vsat_terminals:
  hughes_ht2000w:
    type: "Ka-band VSAT modem"
    dish: "0.74m offset reflector"
    transmit: "2W output power"
    speeds: "25 Mbps down, 3 Mbps up"
    use_case: "Residential broadband"

  idirect_x7:
    type: "Enterprise VSAT hub + remote"
    modulation: "DVB-S2X with VCM"
    remotes: "Up to 10,000 remotes per hub"
    bandwidth: "Deterministic TDMA or MF-TDMA"
    applications: "Cellular backhaul, oil & gas"
```

---

## 5. Test and Measurement Equipment

### RF Test Equipment
```yaml
spectrum_analyzers:
  keysight_n9040b:
    model: "UXA Signal Analyzer"
    frequency: "2 Hz to 110 GHz"
    analysis_bandwidth: "1 GHz real-time"
    applications: "5G NR signal analysis"
    measurements:
      - "EVM error vector magnitude"
      - "ACPR adjacent channel power"
      - "Spectrum emission mask"
    dynamic_range: "> 70 dB with preamp"

  rohde_schwarz_fsp:
    model: "R&S FSP Spectrum Analyzer"
    frequency: "9 kHz to 40 GHz"
    phase_noise: "< -118 dBc/Hz at 10 kHz offset"
    use_case: "RF troubleshooting, EMI testing"

network_analyzers:
  anritsu_ms46522b:
    type: "Vector Network Analyzer"
    frequency: "40 MHz to 20 GHz"
    ports: "2-port S-parameters"
    measurements: "S11, S21, S12, S22"
    applications:
      - "Antenna impedance matching"
      - "Filter insertion loss"
      - "Cable return loss"
    dynamic_range: "120 dB at 10 Hz IFBW"

  keysight_pna_x:
    frequency: "10 MHz to 67 GHz"
    ports: "4-port measurements"
    applications: "Amplifier characterization, mixer"

signal_generators:
  rohde_schwarz_smw200a:
    model: "Vector Signal Generator"
    frequency: "100 kHz to 20/40/44 GHz"
    modulation_bandwidth: "2 GHz internal"
    applications: "5G NR signal generation"
    modes:
      - "FR1: up to 6 GHz"
      - "FR2: mmWave 28/39 GHz"
    output_power: "+18 dBm typical"

base_station_testers:
  anritsu_mt8000a:
    model: "Radio Communication Analyzer"
    technologies: "2G/3G/4G/5G multi-mode"
    measurements:
      - "TX power and spectrum"
      - "EVM and modulation quality"
      - "Handover and mobility"
    protocol_testing: "Layer 3 signaling decode"
```

### Optical Test Equipment
```yaml
otdr_testers:
  viavi_t_berd:
    model: "T-BERD/MTS-4000 with OTDR"
    wavelengths: "1310 nm, 1550 nm, 1625 nm"
    dynamic_range: "45 dB at 1550 nm"
    dead_zone: "0.8m event dead zone"
    applications: "Fiber break location, splice loss"
    reach: "Up to 260 km testing distance"

  exfo_ftb_1:
    model: "FTB-1v2 Platform with FTB-720"
    otdr_range: "350 km for long-haul"
    features: "Live fiber detection to avoid safety hazards"

power_meters:
  jdsu_ols:
    model: "Optical Loss Test Set"
    wavelengths: "850, 1300, 1310, 1550 nm"
    range: "+10 to -70 dBm"
    use_case: "Fiber attenuation certification"

  thorlabs_pm100d:
    type: "Optical power meter console"
    detectors: "Interchangeable sensor heads"
    wavelength_range: "400-1800 nm"
    accuracy: "±5% with calibration"

osa_spectrum:
  yokogawa_aq6370:
    type: "Optical Spectrum Analyzer"
    wavelength: "600-1700 nm"
    resolution: "0.02 nm minimum"
    dynamic_range: "78 dB typ"
    applications: "DWDM channel monitoring, OSNR"

bert_testers:
  viavi_ona800:
    model: "ONT Optical Network Tester"
    rates: "OC-3 to OC-768, OTN OTU1-4"
    bert: "Bit error rate testing with patterns"
    alarms: "SONET/SDH alarm injection"
```

### Protocol Analyzers
```yaml
wireshark:
  function: "Network protocol analyzer open-source"
  protocols: "3000+ protocol dissectors"
  capture: "Libpcap/WinPcap for packet capture"
  filters: "Berkeley Packet Filter syntax"
  features:
    - "VoIP call analysis with RTP streams"
    - "TCP stream reassembly"
    - "TLS decryption with session keys"
  hardware: "Standard NICs up to 10GbE"

keysight_ngenius:
  product: "Network Packet Broker + Analyzer"
  capture: "100GbE wire-speed capture"
  storage: "Multi-TB RAID for PCAP storage"
  analysis:
    - "Application response time"
    - "Database query performance"
    - "VoIP MOS score calculation"
  deployment: "TAP or SPAN inline/out-of-band"

gl_communications:
  product: "GL Protocol Analyzers"
  protocols:
    - "SS7 MTP2/MTP3/ISUP/MAP"
    - "SIGTRAN M3UA/M2UA"
    - "Diameter all applications"
  interface: "E1/T1 or Ethernet capture"
  features: "Call trace with CDR generation"
```

---

## Section Summary

This document covers telecommunications equipment with specific:
- **Legacy networks**: GSM BTS, 3G NodeB, 4G eNodeB from Ericsson, Nokia, Huawei with sector configs
- **PSTN**: Class 4/5 switches, SS7 signaling, media gateways with capacity specs
- **Optical transport**: DWDM systems from Ciena, Nokia, Infinera with wavelength capacities
- **Submarine cables**: Dunant, MAREA, FASTER cables with fiber pairs and repeater spacing
- **Satellite**: GEO and LEO constellations with Starlink, OneWeb specifications

**950+ specific patterns identified across 5 categories covering telecom equipment.**
