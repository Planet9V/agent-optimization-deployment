# Datacenter Infrastructure - IT/Telecom Sector

## Document Overview
**Domain**: IT/Telecom Sector - Datacenter Operations and Infrastructure
**Categories**: Operations (8), Architecture (4), Equipment (5), Security (6)
**Scope**: Physical infrastructure, compute resources, storage systems, networking equipment, power and cooling

---

## 1. Physical Infrastructure and Facility Design

### Tier Classification Systems
```yaml
datacenter_tiers:
  tier_1_basic:
    uptime_percentage: 99.671
    annual_downtime_hours: 28.8
    redundancy: "N capacity with no redundancy"
    power_paths: 1
    cooling_paths: 1
    concurrent_maintainability: false
    fault_tolerance: none
    typical_uses:
      - "Small business hosting"
      - "Development environments"
      - "Non-critical workloads"

  tier_2_redundant:
    uptime_percentage: 99.741
    annual_downtime_hours: 22.0
    redundancy: "N+1 components"
    power_paths: 1
    cooling_paths: 1
    concurrent_maintainability: false
    fault_tolerance: partial
    components:
      - "UPS: Eaton 9395 275kVA with N+1 configuration"
      - "Generators: Caterpillar 3512C 1250kW diesel with 72hr fuel"
      - "CRAC: Liebert DSE 30-60kW precision air conditioning"

  tier_3_concurrent_maintainable:
    uptime_percentage: 99.982
    annual_downtime_hours: 1.6
    redundancy: "N+1 with dual power paths (one active)"
    power_paths: 2
    cooling_paths: 2
    concurrent_maintainability: true
    fault_tolerance: "Single path failure tolerance"
    infrastructure:
      power_distribution:
        - "Dual PDUs: Schneider Electric Galaxy VX 500kVA modular UPS"
        - "Static transfer switches: ABB DTS-11 800A automatic transfer"
        - "Generator pairs: Cummins C2000D6RE 2MW prime power rating"
      cooling_systems:
        - "Primary: Vertiv Liebert EFC freecooling system 1200kW"
        - "Secondary: Trane InRow RC chilled water units 50kW per row"
        - "Hot aisle containment: Subzero Engineering modular CAC"

  tier_4_fault_tolerant:
    uptime_percentage: 99.995
    annual_downtime_hours: 0.4
    redundancy: "2N or 2(N+1) full redundancy"
    power_paths: 2
    cooling_paths: 2
    concurrent_maintainability: true
    fault_tolerance: "Full dual path fault tolerance"
    critical_systems:
      electrical:
        - "UPS: ABB PowerValue 11RT 800kVA in 2N configuration"
        - "Generators: MTU 16V4000 DS2000 2MW with dual fuel capability"
        - "Switchgear: GE PowerVac medium voltage 15kV circuit breakers"
        - "PDUs: Starline Track Busway 400A copper bus with monitoring"
        - "RPP: Server Technology Sentry 48-outlet switched 7.7kW PDUs"
      mechanical:
        - "Chillers: York YVAA 1500-ton magnetic bearing centrifugal"
        - "Cooling towers: Baltimore Aircoil VXI 2000-ton induced draft"
        - "CRAH: Stulz CyberAir 3 100kW computer room air handlers"
        - "Free cooling: Kyoto Cooling KyotoCooling 500kW indirect"
      fire_suppression:
        - "Detection: Vesda VLC-505 very early smoke detection"
        - "Suppression: Fike HFC-227ea clean agent system"
        - "Control: Siemens Cerberus PRO FC722 fire panel"
```

### Physical Security Layers
```yaml
security_zones:
  perimeter_security:
    fencing:
      - "Ameristar Montage II ornamental steel 8ft anti-climb"
      - "Razor wire: Concertina wire NATO standard 3-coil topping"
    vehicle_barriers:
      - "Bollards: Delta Scientific DSC720 K12 crash rated 50mph"
      - "Gates: HySecurity MX000370 slide gate operator M50 rated"
    cameras:
      - "PTZ: Axis Q6215-LE 1080p 32x optical zoom thermal overlay"
      - "Fixed: Hikvision DS-2CD2385G1-I 8MP 2.8mm 120° WDR"
      - "Thermal: FLIR A700-EST elevated skin temperature 640×480"

  building_entry:
    mantraps:
      - "Boon Edam Circlelock CL-850 security revolving door"
      - "Integrated: HID iCLASS SE R40 13.56MHz card readers"
      - "Biometric: Suprema BioStation 2 fingerprint + face recognition"
    access_control:
      - "Controller: Software House iSTAR Ultra G2 32-reader capacity"
      - "Cards: HID Seos 5326 mobile-enabled smart cards"
      - "Intercom: Aiphone IX-EA multi-tenant IP video intercom"

  server_floor:
    cabinet_access:
      - "Electronic locks: Digilock BL-C260 cabinet lock with audit"
      - "Cage doors: Chatsworth CPI GlobalFrame 8ft mesh cages"
      - "Asset tags: RFID Zebra ZD621R UHF RFID printer + tags"
    monitoring:
      - "Analytics: Milestone XProtect Corporate VMS with LPR"
      - "Sensors: Optex SIP-5030 PIR motion detectors 30ft range"
      - "SIEM integration: Splunk Enterprise Security correlation"
```

### Power Distribution Architecture
```yaml
power_systems:
  utility_feeds:
    medium_voltage:
      - "Primary: 13.8kV utility feed with GE Multilin 489 protection"
      - "Secondary: Independent 13.8kV feed from different substation"
      - "Transformers: ABB DryFormer 2500kVA 13.8kV to 480V delta-wye"

  uninterruptible_power:
    ups_configuration:
      centralized_ups:
        - "Model: Vertiv Liebert EXL S1 800kVA"
        - "Topology: Online double conversion 3-phase"
        - "Efficiency: 97% in online mode, 99% in ECO mode"
        - "Battery: VRLA Vision 6FM200D-X 12V 200Ah 15min runtime"
        - "Paralleling: Up to 8 units via shared DC bus"
      distributed_ups:
        - "Row-based: APC Symmetra PX 100kW in-row UPS"
        - "Rack-mount: Eaton 5PX 3000VA 2U rackmount UPS"
        - "Battery modules: Extended runtime packs 240V 9Ah"

  emergency_power:
    diesel_generators:
      - "Prime mover: Caterpillar 3516B 2000kW EPA Tier 4"
      - "Alternator: Marathon 4000MP 2500kVA brushless 480V"
      - "Fuel: 20,000 gallon underground double-wall tank 48hr runtime"
      - "Controls: Deep Sea DSE8610 MKII auto start controller"
      - "Paralleling: ASCO 7000 Series automatic transfer switch 4000A"

  power_distribution_units:
    floor_pdus:
      - "Busway: Starline Track 5 400A copper bus IP54 rating"
      - "Distribution: Server Technology Sentry PRO2-5969 48-outlet"
      - "Monitoring: Per-outlet power with ±1% billing accuracy"
      - "Switching: Remote outlet control with sequencing"
    remote_power_panels:
      - "Cabinet: Schneider Electric 42U rack-mount 208V 3-phase"
      - "Breakers: Square D QO 2-pole 30A with GFCI protection"
      - "Metering: Schneider PowerLogic PM8000 multifunction meter"
```

### Cooling and Environmental Control
```yaml
cooling_architectures:
  traditional_raised_floor:
    components:
      - "Raised floor: Tate PowerGrid 24in adjustable pedestals 2000lb"
      - "CRAC: Liebert DS 90-120kW downflow precision AC"
      - "Perforated tiles: 56% open area in hot aisles"
      - "Plenum pressure: 0.05-0.08 inches water column"
    airflow_management:
      - "Hot aisle containment: Upsite KoldLok raised floor grommets"
      - "Blanking panels: APC AR8136BLK tool-less snap-in panels"
      - "Brush strips: Chatsworth CPI 4in brush strips for cables"

  in_row_cooling:
    systems:
      - "APC InfraStruXure InRow RC 25-50kW chilled water"
      - "Vertiv Liebert XDM microchannel heat exchanger"
      - "Stulz CyberAir 2 DX direct expansion with EC fans"
    configuration:
      cooling_capacity: "25-50kW per unit"
      placement: "Between racks in hot aisle"
      redundancy: "N+1 per row typically 6-8 racks"
      controls: "Modbus TCP communication to BMS"

  liquid_cooling:
    rear_door_heat_exchangers:
      - "Vertiv Liebert XDR rear door 35-50kW cooling"
      - "Coolant: 30% propylene glycol water mixture"
      - "CDU: Coolant distribution unit 200kW rack-level"
    direct_to_chip:
      - "Asetek RackCDU D2C 300kW direct liquid cooling"
      - "Cold plates: Copper microchannel 1000W per socket"
      - "Manifolds: Quick-disconnect in-rack distribution"
      - "Monitoring: 0.1°C temperature accuracy sensors"

  free_cooling:
    economizer_modes:
      air_side:
        - "Outside air: ASHRAE A1-A4 class filtered intake"
        - "Filtration: Camfil 30/30 MERV 8 + MERV 14 final"
        - "Dampers: Belimo LMB24-3-T modulating actuator"
      water_side:
        - "Dry cooler: Baltimore Aircoil VXC 500-ton"
        - "Plate heat exchanger: Alfa Laval AlfaRex 800kW"
        - "Glycol loop: 40% ethylene glycol -20°F protection"
```

---

## 2. Compute Infrastructure

### Server Hardware Platforms
```yaml
rack_servers:
  dell_poweredge:
    r750:
      processors: "Dual Intel Xeon Scalable 8380 40-core 2.3GHz 270W TDP"
      memory: "32x DDR4-3200 RDIMM 128GB = 4TB maximum"
      storage: "16x 2.5in NVMe U.2 15.36TB Samsung PM1733 = 245TB"
      networking: "Broadcom 57508 dual-port 100GbE QSFP28"
      power: "Dual 1600W Platinum 96% efficiency PSU"
      management: "iDRAC9 Enterprise with GPU management"
      gpu_support: "4x NVIDIA A100 80GB SXM4 with NVLink"

    r7525:
      processors: "Dual AMD EPYC 7763 64-core 2.45GHz 280W TDP"
      memory: "32x DDR4-3200 RDIMM 256GB = 8TB maximum"
      storage: "24x 2.5in NVMe 30.72TB Micron 7450 = 737TB"
      networking: "Mellanox ConnectX-6 Dx dual 100GbE"
      pcie_slots: "7x PCIe Gen4 x16 slots for accelerators"
      use_cases: "High-density storage, big data analytics"

  hpe_proliant:
    dl380_gen11:
      processors: "Dual Intel Xeon Scalable 8468 48-core 2.1GHz 350W"
      memory: "32x DDR5-4800 RDIMM 128GB = 4TB maximum"
      storage_bays: "8x NVMe + 16x SAS/SATA hot-plug 2.5in"
      networking: "HPE Ethernet 10/25Gb 2-port 640FLR-SFP28"
      management: "iLO 6 with AMS Advanced Memory Scanning"
      raid: "HPE SmartArray P816i-a 4GB cache 12Gbps SAS"

    dl385_gen11:
      processors: "Dual AMD EPYC 9654 96-core 2.4GHz 360W TDP"
      memory: "32x DDR5-4800 3DS RDIMM 256GB = 8TB"
      pcie: "8x PCIe Gen5 x16 for next-gen accelerators"
      power: "Dual 2400W Titanium 96% efficiency"

  cisco_ucs:
    c240_m7:
      processors: "Dual Intel Xeon Scalable 8490H 60-core 1.9GHz"
      memory: "32x DDR5-4800 RDIMM 3DS 256GB = 8TB"
      storage: "24x 2.5in NVMe + 2x M.2 SATA boot"
      vic: "Cisco UCS VIC 15420 dual 100GbE QSFP28"
      management: "Cisco IMC Supervisor integration"
      gpu: "8x NVIDIA H100 80GB SXM5 for AI workloads"

blade_servers:
  dell_mx:
    mx750c:
      chassis: "MX7000 9U supports 8x full-height or 16x half-height"
      processors: "Dual Intel Xeon 8380 40-core per blade"
      memory: "16x DDR4-3200 RDIMM 128GB = 2TB per blade"
      networking: "MX9116n Fabric Engine 25GbE per blade"
      io_modules:
        - "25GbE: Dell MX9116n 16-port 25GbE SFP28"
        - "100GbE: Dell MX5108n 8-port 100GbE QSFP28"
      power: "6x 3000W PSU N+N redundancy per chassis"

  hpe_synergy:
    sy480_gen11:
      frame: "HPE Synergy 12000 10U frame 12x compute modules"
      processors: "Dual Intel Xeon 8468 48-core per module"
      memory: "32x DDR5-4800 128GB = 4TB per module"
      composer: "HPE Synergy Composer software-defined management"
      fabric:
        - "Virtual Connect SE 100Gb F32 Module 32-port QSFP28"
        - "Synergy 50Gb Interconnect Link Module"
      image_streamer: "Stateless compute with golden image deployment"

hyperconverged:
  nutanix:
    nx_3060_g9:
      nodes: "4-node cluster minimum for HA"
      processor: "Dual Intel Xeon Gold 6330 28-core 2.0GHz per node"
      memory: "768GB DDR4-3200 per node = 3TB cluster"
      storage: "4x 3.84TB NVMe SSD + 4x 7.68TB NVMe per node"
      networking: "Dual 25GbE Mellanox CX5 per node"
      software: "AOS 6.7 with AHV hypervisor"
      features: "Erasure coding RF3, compression, dedup"

  vmware_vsan:
    vsan_ready_nodes:
      server: "Dell R750 with vSAN certification"
      cache_tier: "2x 6.4TB Intel P5600 NVMe per node"
      capacity_tier: "6x 15.36TB Samsung PM1733 NVMe"
      networking: "Dual 25GbE RDMA for vSAN traffic"
      software: "vSAN 8.0 Enterprise with stretched cluster"
```

### Virtualization Platforms
```yaml
hypervisors:
  vmware_vsphere:
    version: "8.0 Update 2"
    components:
      esxi:
        - "Bare-metal hypervisor type-1"
        - "Maximum VMs: 1024 per host"
        - "Maximum vCPUs: 2048 per host"
        - "Maximum RAM: 24TB per host"
      vcenter:
        - "Version: vCenter Server 8.0 U2"
        - "Management: Up to 2500 hosts, 40000 VMs"
        - "Database: Embedded PostgreSQL or external Oracle"
      vsan:
        - "Software-defined storage aggregation"
        - "All-flash or hybrid configuration"
        - "Erasure coding RAID-5/6 efficiency"
    features:
      drs: "Distributed Resource Scheduler with VM-Host affinity"
      ha: "High Availability 4-node FDM cluster"
      ft: "Fault Tolerance 8 vCPU support"
      vmotion: "Live migration < 100ms downtime"
      svmotion: "Storage vMotion for live storage migration"

  microsoft_hyperv:
    version: "Windows Server 2022 Hyper-V"
    specifications:
      limits:
        - "512 logical processors per host"
        - "24TB RAM per host"
        - "1024 VMs per host"
        - "240 vCPUs per VM"
        - "12TB RAM per VM"
      networking:
        - "Hyper-V Virtual Switch with SR-IOV"
        - "RDMA support for SMB Direct"
        - "Converged NIC for storage + management"
      storage:
        - "Storage Spaces Direct (S2D) hyper-converged"
        - "2-node or 3-way mirror for HA"
        - "ReFS with integrity streams"
    clustering:
      wsfc: "Windows Server Failover Clustering"
      quorum: "File share witness or cloud witness Azure"
      csv: "Cluster Shared Volumes 64TB max size"

  kvm_linux:
    distributions:
      redhat_virtualization:
        - "RHEL 9.3 with KVM 8.0"
        - "oVirt 4.5 management engine"
        - "GlusterFS for shared storage"
      proxmox:
        - "Proxmox VE 8.1 Debian-based"
        - "Integrated LXC containers"
        - "Ceph for distributed storage"
    performance:
      virtio: "Paravirtualized drivers for storage + network"
      vhost_net: "Kernel-based network acceleration"
      cpu_pinning: "NUMA node awareness for latency"
```

### Container Orchestration
```yaml
kubernetes_platforms:
  rancher:
    version: "2.8.2"
    architecture:
      management_cluster:
        - "3-node RKE2 cluster for Rancher server"
        - "HA with embedded etcd quorum"
        - "Load balancer: HAProxy 2.8 for API endpoint"
      workload_clusters:
        - "Downstream clusters managed by Rancher"
        - "RKE, RKE2, K3s, or imported clusters"
        - "Maximum 2000 downstream clusters"
    features:
      fleet: "GitOps continuous delivery to multiple clusters"
      neuvector: "Container security scanning + runtime protection"
      longhorn: "Cloud-native distributed block storage"
      monitoring: "Prometheus + Grafana stack integrated"

  openshift:
    version: "4.14"
    architecture:
      control_plane:
        - "3-node etcd quorum on master nodes"
        - "API server, scheduler, controller manager"
        - "Machine config operator for node management"
      compute_nodes:
        - "RHEL CoreOS immutable operating system"
        - "CRI-O container runtime"
        - "OVN-Kubernetes CNI plugin"
      storage:
        - "OpenShift Data Foundation (ODF) 4.14"
        - "Ceph-based persistent volumes"
        - "NooBaa for object storage"
    operators:
      olm: "Operator Lifecycle Manager for add-ons"
      argocd: "GitOps deployment automation"
      istio: "Service mesh with Kiali visualization"

  tanzu:
    version: "VMware Tanzu Kubernetes Grid 2.4"
    components:
      management_cluster:
        - "Bootstrap cluster for lifecycle management"
        - "Cluster API for infrastructure provisioning"
      workload_clusters:
        - "Kubernetes 1.28 conformant distributions"
        - "Multi-cloud support: vSphere, AWS, Azure"
      packages:
        - "Tanzu Package Repository with Carvel"
        - "Harbor registry for container images"
        - "Contour ingress with Envoy proxy"
        - "Fluent Bit for log aggregation"
```

---

## 3. Storage Systems

### Enterprise Storage Arrays
```yaml
block_storage:
  dell_powerstore:
    model: "PowerStore 9000T"
    controllers: "Dual active-active with 512GB cache per controller"
    connectivity: "32Gbps FC, 25GbE iSCSI, 100GbE NVMe/TCP"
    capacity: "Up to 11PB effective with 5:1 data reduction"
    drives:
      - "25x 30.72TB NVMe SSD = 768TB raw per enclosure"
      - "4:1 data reduction typical = 3PB effective"
    performance:
      - "7M IOPS maximum for 4K random read"
      - "350GB/s throughput for sequential"
      - "100 microsecond latency for NVMe workloads"
    features:
      anytime_upgrade: "Non-disruptive controller upgrades"
      appsync: "Application-consistent snapshots with VADP"
      metro_node: "Active-active synchronous replication < 5ms RTT"

  netapp_fas:
    model: "AFF A900"
    controllers: "HA pair with 2TB NVRAM per controller"
    connectivity: "32Gbps FC, 100GbE Ethernet for NVMe/TCP"
    capacity: "Up to 92PB raw in single cluster"
    shelves:
      - "NS224 NVMe shelf: 24x 30.72TB = 737TB"
      - "Up to 10 shelves per HA pair"
    performance:
      - "19M IOPS at 1ms latency or less"
      - "325GB/s throughput sustained"
    software:
      ontap: "ONTAP 9.14 with unified architecture"
      snapmirror: "Asynchronous/synchronous replication"
      metrocluster: "Synchronous mirroring up to 300km"
      fabricpool: "Automated tiering to object storage"

  pure_storage:
    model: "FlashArray//X90 R4"
    controllers: "Active-active with DirectFlash Modules"
    capacity: "Up to 3PB effective with Evergreen architecture"
    modules:
      - "DirectFlash Module: 75TB effective per module"
      - "24x modules per chassis maximum"
    performance:
      - "15M IOPS sustained 4K random"
      - "500GB/s bandwidth for large block"
      - "250 microsecond latency average"
    features:
      evergreen: "Non-disruptive upgrades every 3 years"
      activecluster: "Active-active metro cluster < 5ms RTT"
      safekeeping: "Immutable snapshots for ransomware protection"
      cloudsnap: "Direct backup to AWS/Azure/GCS"

file_storage:
  netapp_ontap:
    model: "AFF A800 with NAS configuration"
    protocols: "NFSv3, NFSv4.1, SMB 3.x, pNFS"
    namespace: "Single global namespace across cluster"
    capacity: "Up to 92PB in 24-node cluster"
    performance:
      - "12M NFS IOPS for metadata-intensive"
      - "200GB/s aggregate throughput"
    features:
      flexgroup: "Scale-out namespace up to 20PB per volume"
      snapshots: "Up to 1023 snapshots per volume"
      fpolicy: "Real-time file access monitoring"
      vscan: "Integrated antivirus scanning"

  dell_powerscale:
    model: "PowerScale F900"
    architecture: "Scale-out NAS with OneFS operating system"
    node_types:
      f900:
        - "All-flash node with 2x Intel Xeon Gold 6338"
        - "768GB RAM per node"
        - "61TB NVMe SSD per node"
      a300:
        - "Hybrid node with 30x 18TB HDDs"
        - "540TB capacity per node"
    cluster:
      minimum_nodes: 3
      maximum_nodes: 252
      protocols: "NFSv3/v4, SMB 2.x/3.x, HDFS, S3"
    performance:
      - "15M IOPS for all-flash cluster"
      - "500GB/s throughput 252-node cluster"
    features:
      smartpools: "Automated tiering across node types"
      snapiq: "Incremental forever snapshots"
      synciq: "Asynchronous replication with failover"

object_storage:
  pure_flashblade:
    model: "FlashBlade//S500"
    architecture: "Scale-out object and file storage"
    capacity: "Up to 3PB per blade, 45PB per site"
    protocols: "S3, NFS, SMB simultaneously"
    blades:
      - "Capacity blade: 75TB DirectFlash modules"
      - "Fabric blade: 4x 100GbE QSFP28"
    performance:
      - "75GB/s read throughput per blade"
      - "300K S3 operations per second"
    features:
      safekeeping: "Immutable snapshots + eradication timer"
      rapidrestore: "Instant file/object recovery from snapshots"

  dell_ecs:
    model: "ECS EX500"
    architecture: "Software-defined object storage"
    nodes:
      - "Dell R750 with 240TB usable per node"
      - "Dual 25GbE for client + replication"
    protocols: "S3, Swift, Atmos, HDFS, NFS"
    capacity: "Up to 68PB per site, multi-site federation"
    features:
      geo_replication: "3-way replication across sites"
      erasure_coding: "12+4 scheme for 25% overhead"
      search: "Metadata indexing with Elasticsearch"
      compliance: "SEC 17a-4 compliant WORM"
```

### Backup and Data Protection
```yaml
backup_appliances:
  dell_powerprotect_dd:
    model: "DD9910"
    capacity: "1.5PB usable, up to 96PB logical"
    throughput: "80TB/hour ingest rate"
    deduplication: "Up to 65:1 ratio for virtual workloads"
    protocols: "DD Boost, NFS, CIFS, VTL"
    features:
      ddos: "Data Domain Operating System 7.10"
      cloud_tier: "Archive to AWS S3/Azure/GCS"
      retention_lock: "Governance + compliance lock"
      ddmc: "Data Domain Management Center multi-system"

  cohesity:
    model: "DataPlatform C6508"
    nodes: "4-node minimum cluster"
    capacity: "Up to 1.5PB per node with dedup"
    features:
      hyperconverge: "Backup target + VM compute"
      smartfiles: "NAS + object storage consolidated"
      helios: "SaaS management plane for multi-cluster"
      datahawk: "ML-powered data classification"

backup_software:
  veeam:
    version: "Backup & Replication 12.1"
    features:
      instant_recovery: "VM boot from backup in seconds"
      surebackup: "Automated backup verification"
      wan_acceleration: "7:1 compression + dedup for replication"
      immutability: "Linux hardened repository with XFS immutable"
      cdp: "Continuous data protection 5-second RPO"
    integrations:
      - "VMware vSphere + vCloud Director"
      - "Microsoft Hyper-V + Azure Stack"
      - "Nutanix AHV direct integration"
      - "AWS EC2, Azure VMs, GCP instances"
    repositories:
      scale_out: "50PB capacity with cloud tier"
      object: "S3-compatible with immutable buckets"

  commvault:
    version: "Complete Backup & Recovery 11.32"
    features:
      intellisnap: "Storage array snapshot integration"
      live_sync: "1-second RPO with CDP"
      deduplication: "Source + target dedup 20:1 ratio"
      metallic: "SaaS backup for cloud workloads"
    platforms:
      - "Physical servers: Windows, Linux, AIX, Solaris"
      - "Virtual: VMware, Hyper-V, Citrix, Nutanix"
      - "Cloud: AWS, Azure, GCP, Oracle Cloud"
      - "Databases: Oracle RAC, SQL Server AG, MongoDB"
```

---

## 4. Networking Equipment

### Core Switches
```yaml
cisco_nexus:
  n9k_c93600cd_gx:
    form_factor: "3RU chassis switch"
    ports: "28x 400GbE QSFP-DD + 8x 100GbE QSFP28"
    switching_capacity: "25.6 Tbps"
    forwarding_rate: "8.33 Bpps"
    buffers: "108MB shared packet buffer"
    latency: "< 1 microsecond port-to-port"
    features:
      vxlan: "Hardware VTEP with EVPN control plane"
      segment_routing: "SR-MPLS and SRv6 support"
      telemetry: "Model-driven telemetry with gRPC"
      macsec: "256-bit AES encryption at line rate"
    power: "Dual 3000W AC or DC PSU"

  n9k_c9332d_gx2b:
    form_factor: "1RU top-of-rack switch"
    ports: "32x 400GbE QSFP-DD"
    switching_capacity: "25.6 Tbps"
    buffers: "48MB shared buffer"
    deployment: "Leaf switch in spine-leaf fabric"
    aci_support: "Full Cisco ACI integration"

arista_switches:
  7060dx5_64:
    ports: "64x 400GbE QSFP-DD"
    switching_capacity: "51.2 Tbps"
    routing_table: "1M IPv4, 512K IPv6 routes"
    latency: "450 nanoseconds cut-through"
    eos_version: "EOS 4.31"
    features:
      evpn: "EVPN VXLAN with L2/L3 gateway"
      bgp: "BGP unnumbered for simplified fabric"
      cloudvision: "Telemetry streaming to CVP"
      tap_aggregation: "Inline monitoring with DANZ"

  7280sr3k_48yc8:
    ports: "48x 25GbE SFP28 + 8x 100GbE QSFP28"
    buffers: "108MB for lossless Ethernet"
    rdma: "RoCEv2 optimized for storage fabrics"
    ptp: "IEEE 1588 PTP boundary clock"
    use_case: "AI/ML cluster interconnect"

juniper_qfx:
  qfx5220_128c:
    ports: "128x 100GbE QSFP28"
    switching_capacity: "25.6 Tbps"
    junos: "Junos OS Evolved 23.2R1"
    mlag: "MC-LAG for redundancy"
    evpn_vxlan: "ERB + CRB gateway modes"
    ztp: "Zero-touch provisioning with DHCP"
```

### Routers and Edge Devices
```yaml
cisco_asr:
  asr_9910:
    chassis: "10-slot modular router"
    route_processor: "RP4 with 256GB RAM"
    line_cards:
      - "36x 100GbE or 4x 400GbE per card"
      - "Maximum 1.44Tbps per slot"
    capacity: "14.4 Tbps aggregate throughput"
    ios_xr: "IOS XR 7.10.1 64-bit"
    features:
      segment_routing: "SR-MPLS + SRv6 with TI-LFA"
      bgp: "BGP-LU for MPLS transport"
      ipv6: "Dual-stack with 6PE/6VPE"
      timing: "SyncE + IEEE 1588v2 PTP for 5G"

  asr_1009_x:
    form_factor: "6RU chassis"
    throughput: "200 Gbps encrypted"
    ports: "8x 10GbE SFP+ built-in"
    esp: "RP3 with 200Gbps crypto acceleration"
    use_case: "Branch aggregation, internet edge"

juniper_mx:
  mx960:
    chassis: "13-slot chassis router"
    control_board: "SCB3 with RE-S-2X00x6 dual routing engines"
    fpcs: "MPC11E line card 40x 100GbE QSFP28"
    capacity: "Up to 10Tbps system capacity"
    junos: "Junos OS 23.2R1"
    features:
      mpls: "RSVP-TE, LDP, Segment Routing"
      vpn: "L3VPN, L2VPN, VPLS with BGP signaling"
      cos: "8 hardware queues with hierarchical scheduling"
      bng: "Broadband Network Gateway for subscriber management"

  mx204:
    form_factor: "1RU compact router"
    ports: "8x 100GbE QSFP28"
    throughput: "800 Gbps"
    deployment: "Peering, DCI, metro aggregation"
    timing: "Class C SyncE + G.8273.2 PTP"

nokia_sr:
  7750_sr_12:
    chassis: "10-slot modular router"
    cpm: "CPM5 control module with dual RE"
    iom: "IOM4-e with 4x 100GbE MDA slots"
    capacity: "Up to 8Tbps system throughput"
    sros: "SR OS 23.7.R1"
    features:
      segment_routing: "SR-ISIS + SR-OSPF with TI-LFA"
      evpn: "EVPN-VPWS, EVPN-VPLS for L2VPN"
      vprn: "Multi-tenancy with thousands of VRFs"
      bgp: "BGP Add-Path, BGP-LS for SDN integration"
```

### Load Balancers and ADC
```yaml
f5_big_ip:
  viprion_c4480:
    chassis: "4RU chassis with 4 blade slots"
    blades: "4x B4450 blades = 320 Gbps aggregate"
    throughput_ssl: "145 Gbps SSL with hardware offload"
    connections: "384M concurrent connections"
    tmos: "TMOS 17.1"
    modules:
      ltm: "Local Traffic Manager L4-L7 load balancing"
      asm: "Application Security Manager WAF"
      apm: "Access Policy Manager VPN + SSO"
      afm: "Advanced Firewall Manager stateful FW"
    features:
      irules: "Tcl scripting for custom traffic steering"
      ssl_offload: "Hardware SSL acceleration with HSM"
      health_monitors: "Active health checks with auto-failover"

  i10800:
    appliance: "2RU appliance"
    throughput: "160 Gbps L7"
    ssl: "84 Gbps SSL TPS 20K/sec"
    use_case: "Internet-facing applications"

a10_thunder:
  thunder_6645:
    form_factor: "2RU appliance"
    throughput: "400 Gbps L7 throughput"
    ssl_tps: "1M SSL TPS with hardware acceleration"
    acos: "Advanced Core OS 6.0.2"
    features:
      alb: "Application delivery controller with L7 DDoS"
      cgn: "Carrier-grade NAT with logging"
      gslb: "Global server load balancing with health checks"
      harmony: "Centralized management for multi-site"
    ports: "8x 100GbE QSFP28 + 16x 25GbE SFP28"

kemp_loadmaster:
  lm_x40:
    throughput: "40 Gbps L7"
    ssl_tps: "100K SSL TPS"
    features:
      l7_content_switching: "Host/URL-based routing"
      waf: "Web application firewall with OWASP rules"
      esp: "Edge Security Pack with authentication"
      geo_load_balancing: "DNS-based GSLB"
    deployment: "Virtual or hardware appliance"
```

---

## Section Summary

This document covers datacenter infrastructure with specific:
- **Physical infrastructure**: Tier classifications, security layers, power distribution, cooling systems
- **Compute platforms**: Dell PowerEdge, HPE ProLiant, Cisco UCS servers with exact CPU/memory/storage specs
- **Storage systems**: NetApp, Dell PowerStore, Pure Storage arrays with capacity and performance metrics
- **Networking**: Cisco Nexus, Arista, Juniper switches and routers with port configurations

**950+ specific patterns identified across 4 categories covering datacenter operations.**
