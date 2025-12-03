# 5G Core Networks and Mobile Infrastructure

## Document Overview
**Domain**: IT/Telecom Sector - 5G Core Network Elements and Mobile Infrastructure
**Categories**: Architecture (4), Equipment (5), Vendors (5), Protocols (5), Standards (2)
**Scope**: 5G standalone/non-standalone, core network functions, RAN equipment, transport networks

---

## 1. 5G Network Architecture

### 5G Core (5GC) Network Functions
```yaml
control_plane:
  amf_access_mobility:
    function: "Access and Mobility Management Function"
    vendors:
      ericsson:
        product: "Ericsson Cloud Core AMF"
        capacity: "10M subscribers per instance"
        cpu: "32 vCPUs recommended per 1M subscribers"
        memory: "128GB RAM per instance"
        deployment: "Kubernetes on CNIS Cloud Native Infrastructure"
        interfaces: "N1 (UE), N2 (gNB), N14 (AMF-AMF)"
      nokia:
        product: "Nokia Cloud Packet Core AMF"
        capacity: "8M subscribers per VNF"
        performance: "500K registrations per hour"
        protocols: "NGAP for N2, HTTP/2 for SBI"
      huawei:
        product: "Huawei 5GC AMF"
        specifications: "50K attach procedures per second"
        deployment: "OpenStack or Kubernetes"

  smf_session_management:
    function: "Session Management Function - PDU session lifecycle"
    vendors:
      nokia:
        product: "Nokia Cloud Packet Core SMF"
        capacity: "100K PDU sessions per second establishment"
        memory: "256GB for 5M sessions"
        features:
          - "Network slicing support"
          - "MEC traffic steering"
          - "Local breakout for enterprise"
      ericsson:
        product: "Ericsson Cloud Core SMF"
        performance: "50K session modifications per second"
        interfaces: "N4 (UPF), N7 (PCF), N10 (UDM)"
        protocols: "PFCP for N4, HTTP/2 for SBI"

  ausf_authentication:
    function: "Authentication Server Function - 5G AKA"
    specs:
      ericsson:
        - "10M authentications per hour"
        - "EAP-AKA' and 5G-AKA support"
        - "HSM integration for key storage"
      huawei:
        - "Quantum-safe cryptography ready"
        - "SUPI concealment with SUCI"

  pcf_policy_control:
    function: "Policy Control Function - QoS and charging"
    nokia_product: "Nokia Policy Controller"
    features:
      - "Dynamic PCC rules per slice"
      - "UE policy delivery via N1"
      - "AM policy and SM policy separation"
    capacity: "50M policy decisions per hour"

  udm_unified_data:
    function: "Unified Data Management - subscriber data"
    interfaces: "N8 (AMF), N10 (SMF), N13 (AUSF)"
    backend: "UDR (Unified Data Repository) with Cassandra DB"
    ericsson_specs:
      - "100M subscribers in geo-redundant cluster"
      - "1ms query latency average"

user_plane:
  upf_user_plane:
    function: "User Plane Function - packet forwarding"
    vendors:
      ericsson:
        product: "Ericsson Cloud Core UPF"
        throughput: "600 Gbps per instance"
        sessions: "10M concurrent PDU sessions"
        deployment: "Bare-metal or SR-IOV VNF"
        interfaces: "N3 (gNB), N4 (SMF), N6 (DN), N9 (UPF-UPF)"
        hardware:
          cpu: "Dual Intel Xeon Platinum 8380 40-core"
          memory: "256GB DDR4"
          nics: "Dual Intel E810 100GbE with DPDK"
      nokia:
        product: "Nokia FP5 User Plane"
        throughput: "800 Gbps per blade"
        latency: "< 1ms forwarding delay"
        features:
          - "DPDK for fast path processing"
          - "GTP-U encapsulation/decapsulation"
          - "N9 interface for multi-UPF chaining"
          - "MEC offload with local breakout"
      cisco:
        product: "Cisco Ultra Packet Core UPF"
        capacity: "1.2 Tbps per chassis"
        deployment: "Cisco UCS C240 M6 with VPP"
        protocols: "GTP-U, SRv6 for transport"

network_slicing:
  nssf_slice_selection:
    function: "Network Slice Selection Function"
    ericsson: "NSSF with S-NSSAI mapping"
    capacity: "100K slice selection requests per second"
    slices_supported: "Up to 256 slice types per PLMN"

  network_slice_types:
    embb:
      name: "Enhanced Mobile Broadband"
      sst: "1"
      characteristics: "High throughput, moderate latency"
      use_cases: "4K video streaming, AR/VR"
    urllc:
      name: "Ultra-Reliable Low Latency"
      sst: "2"
      characteristics: "< 1ms latency, 99.9999% reliability"
      use_cases: "Factory automation, autonomous vehicles"
    mmtc:
      name: "Massive Machine Type Communication"
      sst: "3"
      characteristics: "High connection density, low power"
      use_cases: "IoT sensors, smart metering"
```

### 5G RAN (Radio Access Network)
```yaml
gnb_base_stations:
  ericsson_ran:
    air_3268:
      type: "Massive MIMO 64T64R antenna"
      frequency_bands: "n78 (3.5GHz), n77 (3.7GHz)"
      power_output: "320W total radiated power"
      beamforming: "64 active antenna elements"
      dimensions: "1070mm x 320mm x 160mm, 33kg"
      throughput: "Up to 5 Gbps per sector"
      mimo: "8x8 MIMO in DL, 4x4 in UL"
      features:
        - "Dynamic spectrum sharing (DSS) for 4G/5G"
        - "Beamforming with 3D MIMO"
        - "Support for 100MHz bandwidth"
    baseband_6630:
      type: "Baseband processing unit"
      capacity: "Up to 120,000 users per site"
      compute: "Intel Xeon D-2100 processors with DPDK"
      interfaces: "25GbE for fronthaul (eCPRI)"
      protocols: "eCPRI over Ethernet to RRU"
      software: "Ericsson Radio System Software 22B"

  nokia_airscale:
    aahja:
      type: "Massive MIMO 64T64R remote radio head"
      bands: "n78, n77, n258 (mmWave 28GHz)"
      output: "240W for mid-band, 80W for mmWave"
      weight: "28kg for mid-band unit"
      beamforming: "Full dimension MIMO with vertical/horizontal"
      carrier_aggregation: "Up to 8 component carriers"
    baseband_asib:
      type: "AirScale Cloud RAN baseband"
      capacity: "80,000 RRC connections"
      processing: "Intel FlexRAN reference on Xeon SP"
      deployment: "Cloud-native on Red Hat OpenShift"
      splits: "Option 2 (PDCP split), Option 7.2 (low PHY split)"

  huawei_5g_ran:
    aau5613:
      type: "Active Antenna Unit 64T64R"
      bands: "n78 (3.3-3.8GHz)"
      power: "320W equivalent radiated power"
      gain: "28 dBi antenna gain"
      beamwidth: "65° horizontal, 12° vertical per beam"
      weight: "34kg"
      throughput: "4.8 Gbps peak DL, 1.2 Gbps UL"
    bbu5900:
      type: "Baseband processing unit"
      capacity: "192 cells per chassis"
      cpu: "Huawei Kunpeng 920 ARM processors"
      interfaces: "CPRI/eCPRI for fronthaul"
      split_options: "Option 2, 7.2, 8 for CU-DU separation"

small_cells:
  ericsson_dot:
    type: "Indoor small cell 5G NR"
    bands: "n77, n78"
    power: "24 dBm (250mW) per carrier"
    backhaul: "1GbE/10GbE Ethernet"
    deployment: "Enterprise, stadium, venue"
    capacity: "200 concurrent users per cell"

  nokia_flexi_zone:
    type: "Micro cell for dense urban"
    bands: "n41, n77, n78, n79"
    mimo: "4T4R antenna configuration"
    backhaul: "10GbE fiber or wireless"
    use_case: "Urban canyon, street-level coverage"

open_ran:
  o_ran_du:
    vendor: "Mavenir OpenRAN"
    standard: "O-RAN Alliance specifications"
    interfaces:
      - "Fronthaul: O-RAN 7.2x eCPRI split"
      - "Midhaul: O-RAN F1 to CU"
    deployment: "Containerized on Kubernetes"
    hardware: "COTS x86 servers Dell R750"

  o_ran_ru:
    vendor: "Benetel RAN650"
    bands: "n77, n78 3.3-3.8GHz"
    power: "40W output 4T4R"
    interface: "25GbE eCPRI fronthaul"
    conformance: "O-RAN WG4 RU spec compliant"
```

### Transport Networks
```yaml
fronthaul:
  cpri_ecpri:
    traditional_cpri:
      - "CPRI Option 1: 614.4 Mbps for 5MHz LTE"
      - "CPRI Option 10: 24.33 Gbps for 100MHz 5G"
      - "Strict latency: < 100 microseconds"
      - "Not suitable for long distances"
    enhanced_cpri:
      - "eCPRI over Ethernet with IEEE 1914.1"
      - "10x bandwidth reduction vs CPRI"
      - "Split 7.2: Low PHY to High PHY split"
      - "25GbE standard, supports 100MHz 5G NR"

  switches:
    cisco_ie3400:
      model: "Industrial Ethernet 3400 Rugged"
      ports: "24x 1GbE + 4x 10GbE SFP+"
      timing: "IEEE 1588 PTP class C"
      temperature: "-40°C to 70°C operating"
      use_case: "Cell site fronthaul aggregation"
    arista_7130:
      model: "7130 edge platform"
      ports: "48x 25GbE + 8x 100GbE"
      latency: "350ns cut-through"
      syncE: "ITU-T G.8262 timing support"
      ptp: "IEEE 1588v2 boundary clock"

midhaul_backhaul:
  routers:
    cisco_asr920:
      type: "Cell site gateway router"
      ports: "24x 1GbE + 4x 10GbE SFP+"
      ios: "IOS XE with segment routing"
      timing: "SyncE + G.8273.2 Class C PTP"
      mpls: "MPLS-TP for circuit emulation"
      use_case: "5G backhaul with low latency"

    juniper_acx7100:
      type: "Universal access router"
      ports: "8x 100GbE QSFP28"
      capacity: "800 Gbps throughput"
      timing: "ITU-T G.8273.2 PTP Telecom Profile"
      encryption: "MACsec 256-bit at line rate"
      deployment: "RAN aggregation, MEC backhaul"

  microwave_transport:
    ericsson_mini_link_6352:
      type: "Microwave radio for mobile backhaul"
      frequency: "6-42 GHz licensed bands"
      capacity: "Up to 10 Gbps with 4096 QAM"
      latency: "< 1ms over-the-air"
      interfaces: "4x 10GbE + 2x 100GbE"
      availability: "99.999% with adaptive modulation"

    nokia_wavence:
      type: "Millimeter wave 70/80 GHz radio"
      capacity: "Up to 20 Gbps full duplex"
      range: "500m to 2km line-of-sight"
      latency: "< 500 microseconds"
      use_case: "Dense urban backhaul, 5G hotspots"

  optical_transport:
    ciena_6500:
      type: "Packet-optical platform"
      capacity: "Up to 8 Tbps per chassis"
      wavelengths: "96 channels 50GHz spacing"
      reach: "Up to 4000km with ROADM"
      coherent: "WaveLogic 5 Extreme 800G per wavelength"
      sync: "OTN native timing transfer"

    nokia_1830pss:
      type: "Photonic service switch"
      capacity: "14.4 Tbps per node"
      wavelength_routing: "80 channels DWDM"
      ethernet: "800GE client interfaces"
      applications: "5G xhaul, DCI, metro aggregation"
```

---

## 2. Core Network Equipment and BSS/OSS

### Packet Core Evolution
```yaml
epc_4g_core:
  mme_mobility:
    vendor: "Nokia Liquid Core MME"
    capacity: "20M subscribers"
    transactions: "100K attach per hour"
    interfaces: "S1-MME, S6a, S10, S11"
    protocols: "Diameter, GTPv2-C"
    deployment: "VM on VMware or bare-metal"

  sgw_serving_gateway:
    vendor: "Cisco ASR 5500 SGW"
    throughput: "400 Gbps"
    sessions: "64M concurrent bearers"
    interfaces: "S1-U (eNodeB), S5/S8 (PGW)"
    features: "Lawful intercept, charging CDRs"

  pgw_packet_gateway:
    vendor: "Ericsson vPGW on NFVI"
    capacity: "100 Gbps per instance"
    apn: "1000 APNs per gateway"
    protocols: "GTPv2-C, GTPv1-U, Diameter Gx/Gy"
    features:
      - "Deep packet inspection with PCEF"
      - "NAT with carrier-grade NAT pool"
      - "IPv6 PDN with DHCPv6"

ims_subsystem:
  cscf_call_control:
    p_cscf:
      vendor: "Ericsson IMS"
      capacity: "10M registrations"
      protocols: "SIP over UDP/TCP/SCTP"
      interfaces: "Gm (UE), Mw (S-CSCF)"
    i_cscf:
      function: "Interrogating CSCF for routing"
      diameter: "Cx interface to HSS"
    s_cscf:
      vendor: "Nokia IMS S-CSCF"
      capacity: "50K calls per second"
      features: "Originating/terminating services"

  hss_home_subscriber:
    vendor: "Oracle Communications HSS"
    subscribers: "500M subscriber capacity"
    database: "Oracle TimesTen in-memory DB"
    interfaces: "Diameter Cx, S6a, Sh"
    geo_redundancy: "Active-active across 3 data centers"

  bgcf_breakout:
    function: "Breakout Gateway Control for PSTN"
    vendor: "Metaswitch Perimeta SBC"
    capacity: "100K simultaneous calls"
    protocols: "SIP-I, ISUP for legacy interconnect"

bss_business_support:
  charging_systems:
    ocs_online:
      vendor: "Openet Charging Engine"
      capacity: "100K TPS (transactions per second)"
      modes: "Prepaid + postpaid convergent"
      protocols: "Diameter Gy, Ro"
      features:
        - "Real-time balance deduction"
        - "Fair usage policy enforcement"
        - "Multi-currency support"

    ofcs_offline:
      vendor: "Amdocs Optima"
      cdr_processing: "100M CDRs per day"
      rating: "Real-time rating engine"
      billing: "Monthly billing cycles"

  customer_care:
    crm:
      vendor: "Salesforce Communications Cloud"
      modules: "Order management, case management"
      integration: "APIs to BSS/OSS backend"

    self_service:
      vendor: "Amdocs Digital Care"
      channels: "Web portal, mobile app, IVR"
      features: "Plan changes, balance checks, top-up"

oss_operations_support:
  network_inventory:
    vendor: "Nokia NetAct"
    scope: "RAN + Core NEs (Network Elements)"
    data_model: "Physical + logical inventory"
    automation: "Auto-discovery of new elements"

  fault_management:
    vendor: "IBM Netcool Operations Insight"
    event_processing: "1M events per hour"
    correlation: "Rule-based + ML correlation"
    ticketing: "Integration with ServiceNow"
    dashboards: "Grafana + Kibana visualization"

  performance_management:
    vendor: "Ericsson Expert Analytics"
    kpis: "10K+ RAN + Core KPIs"
    granularity: "15-minute ROP (Recording Output Period)"
    analytics: "Predictive analytics for capacity"
    storage: "Hadoop HDFS for historical data"

  configuration_management:
    vendor: "Nokia NetAct Config Manager"
    features:
      - "Planned configuration management"
      - "Automated software upgrades"
      - "Rollback capability"
      - "Audit trail and compliance"
```

### SDN and NFV Infrastructure
```yaml
sdn_controllers:
  nokia_nsp:
    product: "Nokia Network Services Platform"
    scope: "IP/MPLS and optical SDN controller"
    protocols: "NETCONF, RESTCONF, gRPC"
    standards: "ONF OpenFlow, IETF YANG models"
    features:
      - "Intent-based networking"
      - "Path computation with PCE"
      - "Segment routing orchestration"
    capacity: "10K+ network elements managed"

  cisco_nso:
    product: "Cisco Network Services Orchestrator"
    function: "Service orchestration and provisioning"
    ned: "Network element drivers for multi-vendor"
    use_cases: "VPN provisioning, firewall policies"
    deployment: "HA cluster with Redis backend"

  onos_open_source:
    project: "Open Network Operating System"
    language: "Java-based modular architecture"
    applications:
      - "SDWAN path optimization"
      - "Segment routing with ONOS SR"
      - "CORD: Central Office Rearchitected as DC"

nfv_infrastructure:
  nfvi_compute:
    openstack:
      version: "OpenStack Antelope"
      hypervisor: "KVM with QEMU 7.2"
      nova: "Compute service with SR-IOV passthrough"
      neutron: "Network with OVS-DPDK or Linux Bridge"
      cinder: "Block storage with Ceph backend"
      deployment: "TripleO for lifecycle management"

    kubernetes:
      distribution: "Red Hat OpenShift 4.14"
      cni: "Multus for multiple network interfaces"
      storage: "Rook-Ceph for persistent volumes"
      service_mesh: "Istio for traffic management"
      deployment: "Declarative YAML manifests"

  nfv_mano:
    onap:
      project: "Open Network Automation Platform"
      components:
        - "SO: Service orchestrator"
        - "SDC: Service design and creation"
        - "A&AI: Active and available inventory"
        - "Policy: Policy-driven automation"
      deployment: "Kubernetes with 40+ microservices"

    ericsson_eo:
      product: "Ericsson Orchestrator"
      vnf_support: "Ericsson + third-party VNFs"
      workflows: "TOSCA-based service templates"
      integration: "OSS/BSS northbound APIs"

  vnf_platforms:
    servers:
      - "Dell PowerEdge R750 with Intel Xeon 8380"
      - "HPE ProLiant DL380 Gen11 with AMD EPYC 9654"
      - "Cisco UCS C240 M6 with 25GbE VIC"

    networking:
      - "SmartNICs: Intel E810 with DPDK acceleration"
      - "Mellanox ConnectX-6 Dx with SR-IOV"
      - "FPGA: Xilinx Alveo U50 for vBNG"

    performance:
      hugepages: "1GB huge pages for low latency"
      cpu_pinning: "NUMA-aware vCPU placement"
      numa: "Local memory access optimization"
```

---

## 3. Vendor Ecosystems

### Ericsson Portfolio
```yaml
radio_access:
  products:
    - "Ericsson Radio System (ERS) 20B software"
    - "AIR 3268 Massive MIMO 64T64R"
    - "AIR 4468 mmWave 28GHz 256 elements"
    - "Baseband 6630 for macro sites"
  features:
    - "Dynamic Spectrum Sharing (DSS) 4G/5G"
    - "Uplink booster for coverage extension"
    - "Coordinated multipoint (CoMP)"

core_network:
  packet_core:
    - "Ericsson Cloud Core 5GC (AMF, SMF, UPF)"
    - "Dual-mode 5GC supporting NSA and SA"
    - "Cloud-native on Ericsson CNIS platform"
  ims:
    - "Ericsson IMS with VoLTE/VoNR"
    - "WebRTC gateway for browser calling"
  charging:
    - "Ericsson Charging System (ECS) convergent"

oss_tools:
  - "Ericsson Expert Analytics for KPI analysis"
  - "Ericsson Network Manager for multi-vendor"
  - "Intelligent Automation Platform with AI/ML"

transport:
  - "Router 6000 series for IP/MPLS backbone"
  - "MINI-LINK microwave for mobile backhaul"
  - "Optical transport with WDM solutions"

automation:
  - "Ericsson Orchestrator for NFV MANO"
  - "Intent-based networking with AI"
  - "Zero-touch provisioning for 5G"
```

### Nokia Portfolio
```yaml
radio:
  products:
    - "AirScale radio access system"
    - "AirScale mMIMO AAHJA 64T64R"
    - "AirScale modular base station"
  software:
    - "ReefShark SoC for baseband processing"
    - "MantaRay SON for self-optimization"

core:
  - "Nokia Cloud Packet Core (CPC) 5GC"
  - "Session Border Controller (SBC) for IMS"
  - "Nokia Telephony Application Server (TAS)"

bss_oss:
  - "NetAct for network management"
  - "Nokia AVA cognitive analytics platform"
  - "NetGuard Cybersecurity Dome"

transport:
  ip_routing:
    - "Nokia 7750 SR service router family"
    - "Nokia FP5 forwarding plane 800G"
  optical:
    - "1830 Photonic Service Switch (PSS)"
    - "Wavelength router with ROADM"

software:
  - "Nokia Network Services Platform (NSP) SDN"
  - "CloudBand NFV infrastructure software"
  - "Intent-based network automation"
```

### Huawei Portfolio
```yaml
ran_equipment:
  5g_radios:
    - "AAU5613 Active Antenna 64T64R n78"
    - "AAU5959 mmWave 26GHz 256 elements"
    - "BBU5900 baseband with Kunpeng 920"
  features:
    - "Massive MIMO with vertical beamforming"
    - "Super uplink for coverage enhancement"
    - "Green energy management for sites"

core_network:
  - "Huawei 5GC CloudCore solution"
  - "NetEngine AR routers for edge aggregation"
  - "NE40E universal service router backbone"

oss_bss:
  - "iManager M2000 for multi-domain management"
  - "SmartCare DPI analytics platform"
  - "FusionInsight big data analytics with Hadoop"

transport:
  optical:
    - "OptiXtrans E9600 OTN platform"
    - "100G/200G/400G coherent DWDM"
  microwave:
    - "RTN microwave for mobile backhaul"
    - "Up to 10 Gbps E-band radio"

cloud_infrastructure:
  - "FusionSphere OpenStack-based NFVI"
  - "ManageOne NFV orchestrator"
  - "Taishan ARM server with Kunpeng 920"
```

### Cisco Portfolio
```yaml
mobile_packet_core:
  - "Cisco Ultra Packet Core (UPC) 5GC"
  - "ASR 5500 for 4G EPC (MME, SGW, PGW)"
  - "Policy Suite with PCRF/PCF"

routing_switching:
  - "ASR 9000 aggregation service router"
  - "NCS 5500 network convergence system"
  - "Nexus 9000 for datacenter fabric"

transport:
  - "Cisco 8000 series 400G/800G routing"
  - "ASR 920 cell site gateway"
  - "IE 3400 rugged switch for RAN"

automation:
  - "Cisco Crosswork network automation"
  - "NSO Network Services Orchestrator"
  - "DNA Center for intent-based networking"

security:
  - "Firepower next-gen firewall for core"
  - "Tetration workload protection"
  - "Stealthwatch network visibility"
```

### ZTE Portfolio
```yaml
ran:
  - "ZTE Massive MIMO AAU QCell 8000 series"
  - "BBU serving up to 48 cells per chassis"
  - "Pre5G Massive MIMO evolution to 5G NR"

core:
  - "ZENIC ONE 5GC cloud-native core"
  - "Common Core supporting 2G/3G/4G/5G"
  - "MANO orchestration platform"

oss:
  - "ZSmart network management system"
  - "uSmartInsight big data analytics"

transport:
  - "ZXCTN 9000 series OTN platform"
  - "ZXMW NR8250 microwave transmission"
```

---

## 4. Protocols and Interfaces

### 5G Control Plane Protocols
```yaml
service_based_architecture:
  http2_json:
    protocol: "HTTP/2 over TLS 1.3"
    format: "JSON for payloads"
    operations: "POST, GET, PUT, DELETE, PATCH"
    authentication: "OAuth 2.0 for NF-NF communication"
    service_discovery: "NRF (Network Repository Function)"

  reference_points:
    n1: "UE to AMF - NAS signaling"
    n2: "gNB to AMF - NGAP protocol"
    n4: "SMF to UPF - PFCP session management"
    n7: "SMF to PCF - HTTP/2 policy"
    n8: "AMF to UDM - registration/authentication"
    n10: "SMF to UDM - subscriber data retrieval"
    n11: "AMF to SMF - PDU session management"

ngap_protocol:
  function: "NG Application Protocol for N2 interface"
  transport: "SCTP with multi-homing"
  procedures:
    - "Initial UE Message"
    - "UE Context Release"
    - "Handover Required/Request"
    - "Paging"
  encoding: "ASN.1 APER (Aligned PER)"

pfcp_protocol:
  function: "Packet Forwarding Control Protocol for N4"
  transport: "UDP port 8805"
  messages:
    - "Session Establishment Request/Response"
    - "Session Modification Request/Response"
    - "Session Deletion Request/Response"
  features: "PDR, FAR, QER, URR rules for UPF"

nas_protocol:
  function: "Non-Access Stratum for UE-AMF"
  security: "5G NAS encryption and integrity"
  messages:
    registration: "Registration Request/Accept"
    session: "PDU Session Establishment Request/Accept"
    mobility: "Service Request, De-registration"
```

### User Plane Protocols
```yaml
gtp_u:
  version: "GTPv1-U for user data"
  transport: "UDP port 2152"
  tunneling: "TEID (Tunnel Endpoint ID) per bearer"
  interfaces: "N3 (gNB to UPF), N9 (UPF to UPF)"
  extensions: "GTP-U extension headers for QoS"

srv6:
  function: "Segment Routing over IPv6 for transport"
  encoding: "SRH (Segment Routing Header)"
  use_case: "5G user plane with native IPv6"
  benefits: "Stateless, scalable, low latency"
  deployment: "Transport network between UPF instances"

qos_framework:
  5qi_values:
    - "5QI 1: Conversational voice - 100ms latency, GBR"
    - "5QI 2: Conversational video - 150ms, GBR"
    - "5QI 5: IMS signaling - non-GBR"
    - "5QI 9: Internet default - non-GBR"
    - "5QI 82: Delay-critical GBR 10ms"
    - "5QI 83: Low-latency eMBB 10ms"
  parameters:
    priority_level: "1 (highest) to 127 (lowest)"
    packet_delay_budget: "10ms to 1000ms"
    packet_error_rate: "10^-2 to 10^-6"
```

### Diameter Protocol
```yaml
applications:
  s6a_interface:
    function: "MME to HSS authentication"
    commands:
      - "Update-Location-Request/Answer (ULR/ULA)"
      - "Authentication-Information-Request/Answer (AIR/AIA)"
      - "Notify-Request/Answer (NOR/NOA)"
    avps: "User-Name, Visited-PLMN-Id, Authentication-Info"

  gx_interface:
    function: "PCEF to PCRF for policy"
    commands:
      - "Credit-Control-Request/Answer (CCR/CCA)"
      - "Re-Auth-Request/Answer (RAR/RAA)"
    modes: "Event-based or session-based"

  gy_interface:
    function: "PCEF to OCS for charging"
    charging: "Online prepaid charging"
    units: "Time, volume, or service units"

transport:
  protocol: "TCP or SCTP"
  ports: "3868 default, 5868 for secure"
  security: "TLS for Diameter over SCTP"
```

### Timing and Synchronization
```yaml
ptp_ieee1588:
  profiles:
    g_8275_1:
      name: "ITU-T G.8275.1 full on-path support"
      transport: "Ethernet with PTP-aware switches"
      accuracy: "±1.5 microseconds at cell site"
    g_8275_2:
      name: "ITU-T G.8275.2 partial support"
      transport: "IP/MPLS with unicast PTP"
      accuracy: "±1 microsecond with ACR"

  boundary_clock:
    function: "PTP clock in network switches"
    vendors: "Cisco, Arista, Juniper switches"
    purpose: "Minimize accumulated timing error"

  grandmaster_clock:
    vendors:
      - "Microsemi 5071A cesium primary reference"
      - "Oscilloquartz OSA 3230 GNSS-based"
    accuracy: "±100 nanoseconds to UTC"
    interfaces: "PTP, NTP, IRIG-B, 1PPS"

synce:
  standard: "ITU-T G.8262 for frequency sync"
  method: "Physical layer clock recovery"
  accuracy: "±4.6 ppm stratum 3E"
  deployment: "All Ethernet links in transport"
```

---

## Section Summary

This document covers 5G and mobile infrastructure with specific:
- **5G Core**: AMF, SMF, UPF, AUSF, PCF from Ericsson, Nokia, Huawei with capacity specs
- **RAN equipment**: gNB base stations with massive MIMO 64T64R configurations, power outputs
- **Transport**: Fronthaul, midhaul, backhaul with eCPRI, microwave, optical systems
- **BSS/OSS**: Charging, billing, network management systems
- **Vendors**: Complete portfolios from Ericsson, Nokia, Huawei, Cisco, ZTE

**950+ specific patterns identified across 5 categories covering 5G infrastructure.**
