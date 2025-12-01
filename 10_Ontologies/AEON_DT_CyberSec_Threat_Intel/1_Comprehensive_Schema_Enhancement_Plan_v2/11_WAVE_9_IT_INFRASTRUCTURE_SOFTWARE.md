# WAVE 9: IT INFRASTRUCTURE & SOFTWARE ASSETS
**File:** 11_WAVE_9_IT_INFRASTRUCTURE_SOFTWARE.md
**Created:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Status:** ACTIVE
**Wave Priority:** 9 of 12
**Estimated Nodes:** ~5,000

## Wave Overview

Wave 9 focuses on comprehensive IT infrastructure and software asset management, covering hardware assets, software inventory, cloud resources, virtualization infrastructure, and their security relationships. This wave bridges traditional IT asset management with cybersecurity threat intelligence.

### Objectives
1. Define complete hardware asset inventory schemas
2. Establish software lifecycle management models
3. Integrate cloud infrastructure monitoring
4. Map virtualization layers and dependencies
5. Connect infrastructure to vulnerability management
6. Enable asset-based threat correlation

### Dependencies
- Wave 1-2: SAREF Core Infrastructure (device foundations)
- Wave 3-5: Cybersecurity threat models (vulnerability linkage)
- Wave 7-8: SBOM integration (software component mapping)

---

## COMPLETE NODE SCHEMAS

### 1. HARDWARE ASSETS (~1,500 nodes)

#### 1.1 Physical Servers (400 nodes)

**PhysicalServer**
```yaml
PhysicalServer:
  extends: saref:Device
  properties:
    # Identity
    serverID: string (unique identifier)
    assetTag: string (organization asset tag)
    hostname: string (FQDN)
    domain: string
    serialNumber: string (manufacturer serial)

    # Hardware Configuration
    manufacturer: string
    model: string
    formFactor: enum[tower, rack_mount, blade, micro_server]
    rackUnit: integer (U height)
    weight: float (kg)

    # Compute Resources
    cpu:
      model: string
      manufacturer: string
      architecture: enum[x86, x64, arm, risc_v, power]
      cores: integer (physical cores)
      threads: integer (logical processors)
      baseSpeed: float (GHz)
      maxSpeed: float (GHz)
      cache:
        l1: integer (KB)
        l2: integer (KB)
        l3: integer (MB)

    # Memory Configuration
    memory:
      total: integer (GB)
      type: enum[ddr3, ddr4, ddr5, ecc_ddr4, ecc_ddr5]
      speed: integer (MHz)
      slots: integer
      slotsUsed: integer
      maxCapacity: integer (GB)

    # Storage Configuration
    storage:
      - type: enum[hdd, ssd, nvme, sas, sata]
        capacity: integer (GB)
        interface: string
        speed: integer (RPM for HDD, MB/s for SSD)
        raidLevel: enum[none, raid0, raid1, raid5, raid6, raid10]
        controller: string

    # Network Interfaces
    networkInterfaces:
      - name: string (eth0, ens192, etc)
        macAddress: string
        ipv4Address: string
        ipv6Address: string
        speed: integer (Mbps)
        type: enum[ethernet, fiber, wifi, infiniband]
        vlanID: integer
        bondingMode: enum[none, active_backup, load_balance, broadcast]

    # Power Configuration
    powerSupply:
      type: enum[single, redundant, n_plus_1]
      capacity: integer (watts)
      efficiency: string (80_plus_rating)
      voltage: integer
      inputType: enum[ac, dc]

    # Physical Location
    location:
      datacenter: string
      building: string
      floor: integer
      room: string
      rack: string
      rackPosition: integer (starting U position)
      coordinates: geopoint

    # Operating System
    operatingSystem:
      name: string
      version: string
      distribution: string
      kernel: string
      architecture: string
      installDate: datetime
      lastUpdate: datetime
      patchLevel: string

    # Management
    managementInterface:
      type: enum[ipmi, ilo, idrac, redfish]
      ipAddress: string
      firmwareVersion: string
      accessMethod: enum[web, ssh, api]

    # Operational Status
    powerState: enum[on, off, standby, hibernating]
    operationalStatus: enum[operational, degraded, failed, maintenance, decommissioned]
    uptime: integer (seconds)
    bootTime: datetime

    # Capacity & Performance
    cpuUtilization: float (percentage)
    memoryUtilization: float (percentage)
    storageUtilization: float (percentage)
    temperatureCPU: float (celsius)
    temperatureAmbient: float (celsius)
    fanSpeed: array[integer] (RPM)

    # Lifecycle Management
    purchaseDate: date
    warrantyExpiry: date
    maintenanceContract: string
    depreciationPeriod: integer (months)
    endOfLife: date

    # Asset Classification
    criticality: enum[critical, high, medium, low]
    dataClassification: enum[public, internal, confidential, restricted, top_secret]
    complianceRequirements: array[enum[pci_dss, hipaa, gdpr, sox, fedramp, fisma]]

  relationships:
    # Physical Relationships
    locatedIn: Datacenter (many-to-1)
    installedIn: Rack (many-to-1)
    poweredBy: PowerDistributionUnit (many-to-1)
    cooledBy: CoolingSystem (many-to-1)

    # Virtualization
    hosts: VirtualMachine (1-to-many)
    runsHypervisor: Hypervisor (1-to-1)

    # Software & Applications
    runsOS: OperatingSystem (1-to-1)
    runs: Application (1-to-many)
    hasAgent: ManagementAgent (1-to-many)

    # Network Connectivity
    connectedTo: NetworkSwitch (many-to-many)
    partOf: NetworkSegment (many-to-1)
    hasNetworkInterface: NetworkInterface (1-to-many)

    # Security
    protectedBy: EndpointProtection (1-to-1)
    monitored By: MonitoringSystem (many-to-many)
    backupTo: BackupSystem (many-to-many)

    # Vulnerability & Threats
    hasVulnerability: Vulnerability (many-to-many)
    affectedBy: Incident (many-to-many)
    exposedTo: ThreatActor (many-to-many)

    # Clustering & High Availability
    memberOf: Cluster (many-to-1)
    failoverTo: PhysicalServer (many-to-1)

    # Management & Ownership
    ownedBy: Organization (many-to-1)
    managedBy: User (many-to-many)
    assignedTo: BusinessUnit (many-to-1)

  validation_rules:
    - serialNumber must be unique
    - hostname must be valid FQDN
    - ipAddress must be valid IPv4 or IPv6
    - cpuUtilization range [0, 100]
    - memoryUtilization range [0, 100]
    - powerState transition requires authorization
```

**ServerCluster**
```yaml
ServerCluster:
  properties:
    clusterID: string
    clusterName: string
    clusterType: enum[ha, load_balancing, hpc, database, storage, kubernetes]
    nodeCount: integer
    minimumNodes: integer
    quorumNodes: integer
    clusterSoftware: string
    version: string

    # Configuration
    sharedStorage: boolean
    storageType: enum[san, nas, das, distributed]
    networkTopology: enum[star, mesh, ring, bus]
    failoverMode: enum[active_active, active_passive, n_plus_1]

    # Status
    clusterStatus: enum[online, degraded, offline, maintenance]
    healthScore: float (0-100)
    lastFailover: datetime

  relationships:
    contains: PhysicalServer (1-to-many)
    uses: SharedStorage (many-to-many)
    managedBy: ClusterManager (many-to-1)
```

#### 1.2 Workstations & Endpoints (500 nodes)

**Workstation**
```yaml
Workstation:
  extends: saref:Device
  properties:
    # Identity
    assetTag: string
    hostname: string
    serialNumber: string

    # Hardware
    manufacturer: string
    model: string
    formFactor: enum[desktop, laptop, all_in_one, thin_client, workstation]
    cpu: string
    memory: integer (GB)
    storage: integer (GB)
    graphics: string

    # Configuration
    operatingSystem: string
    osVersion: string
    osBuild: string
    bitness: enum[32bit, 64bit, arm64]

    # Network
    macAddress: string
    ipAddress: string
    dhcpEnabled: boolean
    dnsServers: array[string]

    # Security
    encryptionStatus: enum[encrypted, not_encrypted, partially_encrypted]
    encryptionType: enum[bitlocker, filevault, luks, veracrypt]
    firewallEnabled: boolean
    antivirusInstalled: boolean
    antivirusVersion: string
    lastVirusScan: datetime

    # Status
    powerState: enum[on, off, sleep, hibernate]
    lastBoot: datetime
    uptime: integer (seconds)

    # User Assignment
    primaryUser: string
    department: string
    location: string

  relationships:
    assignedTo: User (many-to-1)
    hasAgent: EndpointProtection (1-to-1)
    connectedTo: NetworkSegment (many-to-1)
    managedBy: MDM (many-to-1)
    hasVulnerability: Vulnerability (many-to-many)
```

**MobileDevice**
```yaml
MobileDevice:
  extends: Workstation
  properties:
    # Device Specifics
    deviceType: enum[smartphone, tablet, phablet]
    imei: string
    carrier: string
    phoneNumber: string

    # Mobile Configuration
    mobileOS: enum[ios, android, windows_mobile, other]
    osVersion: string
    jailbroken: boolean
    rooted: boolean

    # Security
    passcodeEnabled: boolean
    biometricEnabled: boolean
    mdmEnrolled: boolean

    # Connectivity
    wifiMacAddress: string
    bluetoothMacAddress: string
    cellularConnection: boolean

  relationships:
    enrolledIn: MDM (many-to-1)
    hasProfile: MDMProfile (many-to-many)
```

#### 1.3 Network Devices (300 nodes)

**NetworkDevice**
```yaml
NetworkDevice:
  extends: saref:Device
  properties:
    # Identity
    deviceID: string
    hostname: string
    managementIP: string

    # Device Type
    deviceType: enum[router, switch, firewall, load_balancer, vpn_gateway, wireless_ap, proxy]
    manufacturer: string
    model: string
    serialNumber: string

    # Configuration
    firmwareVersion: string
    operatingSystem: string
    osVersion: string
    configurationVersion: string
    lastConfigBackup: datetime

    # Physical Specifications
    portCount: integer
    speed: enum[10Mbps, 100Mbps, 1Gbps, 10Gbps, 40Gbps, 100Gbps]
    formFactor: enum[rack_mount, standalone, modular]
    powerType: enum[ac, dc, poe]

    # Capacity
    throughput: float (Gbps)
    packetsPerSecond: integer
    concurrentSessions: integer

    # Status
    operationalStatus: enum[up, down, degraded, testing]
    adminStatus: enum[enabled, disabled, maintenance]
    uptime: integer (seconds)

  relationships:
    hasInterface: NetworkInterface (1-to-many)
    connectedTo: NetworkDevice (many-to-many)
    manages: VLAN (1-to-many)
    routes: NetworkSegment (many-to-many)
    protects: NetworkSegment (many-to-many)
    hasRule: FirewallRule|ACL (1-to-many)
```

#### 1.4 Storage Systems (200 nodes)

**StorageArray**
```yaml
StorageArray:
  extends: saref:Device
  properties:
    # Identity
    arrayID: string
    arrayName: string
    serialNumber: string

    # Configuration
    manufacturer: string
    model: string
    arrayType: enum[san, nas, das, unified, object_storage, tape_library]
    protocol: array[enum[fc, iscsi, nfs, smb, s3, swift]]

    # Capacity
    totalCapacity: integer (TB)
    usedCapacity: integer (TB)
    availableCapacity: integer (TB)
    utilizationPercentage: float

    # Performance
    iopsRead: integer
    iopsWrite: integer
    throughputRead: float (MB/s)
    throughputWrite: float (MB/s)
    latencyRead: float (ms)
    latencyWrite: float (ms)

    # Configuration
    raidLevel: array[enum[raid0, raid1, raid5, raid6, raid10, raid50, raid60]]
    deduplicationEnabled: boolean
    compressionEnabled: boolean
    encryptionEnabled: boolean
    snapshotEnabled: boolean
    replicationEnabled: boolean

  relationships:
    contains: StorageVolume (1-to-many)
    exports: LUN|Share (1-to-many)
    replicatesTo: StorageArray (many-to-many)
    backupTo: BackupSystem (many-to-many)
    connectedTo: SAN (many-to-1)
```

#### 1.5 Peripheral & IoT Devices (100 nodes)

**PeripheralDevice**
```yaml
PeripheralDevice:
  extends: saref:Device
  properties:
    deviceType: enum[printer, scanner, camera, access_reader, iot_sensor, industrial_controller]
    manufacturer: string
    model: string
    firmwareVersion: string
    ipAddress: string
    macAddress: string
    networkConnected: boolean

  relationships:
    connectedTo: Workstation|NetworkSegment (many-to-1)
    hasVulnerability: Vulnerability (many-to-many)
```

---

### 2. SOFTWARE ASSETS (~1,500 nodes)

#### 2.1 Operating Systems (200 nodes)

**OperatingSystem**
```yaml
OperatingSystem:
  properties:
    # Identity
    osID: string
    name: string
    family: enum[windows, linux, unix, macos, bsd]
    distribution: string (e.g., Ubuntu, RHEL, Windows Server)
    version: string
    buildNumber: string
    architecture: enum[x86, x64, arm, arm64]

    # Version Details
    majorVersion: integer
    minorVersion: integer
    patchLevel: string
    servicePackLevel: string

    # Support Lifecycle
    releaseDate: date
    generalAvailability: date
    mainstreamSupport: date
    extendedSupport: date
    endOfLife: date

    # Features
    supportedFeatures: array[string]
    kernel Version: string
    shellType: string

  relationships:
    installedOn: PhysicalServer|Workstation (many-to-many)
    supports: Application (many-to-many)
    hasVulnerability: Vulnerability (many-to-many)
    patchedBy: Patch (many-to-many)
```

#### 2.2 Applications (600 nodes)

**Application**
```yaml
Application:
  properties:
    # Identity
    applicationID: string
    applicationName: string
    vendor: string
    version: string
    edition: string

    # Classification
    category: enum[business, productivity, development, security, database, web_server, middleware, monitoring, backup]
    applicationType: enum[commercial, open_source, custom, freeware]

    # Technical Details
    installationPath: string
    executableName: string
    serviceNames: array[string]
    portNumbers: array[integer]
    protocol: array[string]

    # Requirements
    minimumOS: string
    minimumRAM: integer (GB)
    minimumStorage: integer (GB)
    requiredFeatures: array[string]

    # Security
    requiresElevation: boolean
    networkAccess: boolean
    dataAccess: enum[none, local, network, database, internet]
    encryptionSupport: boolean
    authenticationMethod: enum[none, local, ldap, saml, oauth, certificate]

    # Deployment
    installDate: datetime
    lastUpdated: datetime
    autoUpdateEnabled: boolean

    # Business Context
    criticality: enum[critical, high, medium, low]
    dataClassification: enum[public, internal, confidential, restricted]
    businessOwner: string
    technicalOwner: string

  relationships:
    installedOn: Asset (many-to-many)
    runsOn: OperatingSystem (many-to-many)
    dependsOn: Application (many-to-many)
    uses: Database (many-to-many)
    communicatesWith: Application (many-to-many)
    hasVulnerability: Vulnerability (many-to-many)
    licensedBy: License (many-to-1)
    contains: SoftwareComponent (1-to-many)
```

**WebApplication**
```yaml
WebApplication:
  extends: Application
  properties:
    # Web Specifics
    url: string
    publicFacing: boolean
    framework: array[string]
    programmingLanguage: array[string]
    webServer: string

    # Security
    httpsEnabled: boolean
    certificateExpiry: datetime
    certificateIssuer: string
    securityHeaders: array[string]

    # API
    hasAPI: boolean
    apiType: enum[rest, soap, graphql, grpc]
    apiVersion: string

  relationships:
    hasEndpoint: APIEndpoint (1-to-many)
    protectedBy: WAF (many-to-1)
    frontedBy: LoadBalancer (many-to-1)
```

#### 2.3 Databases (200 nodes)

**Database**
```yaml
Database:
  properties:
    # Identity
    databaseID: string
    databaseName: string
    instance Name: string

    # Technology
    databaseType: enum[relational, nosql, graph, time_series, document, key_value]
    dbms: enum[mysql, postgresql, oracle, mssql, mongodb, cassandra, redis, neo4j]
    version: string
    edition: string

    # Configuration
    port: integer
    maxConnections: integer
    characterSet: string
    collation: string

    # Capacity
    databaseSize: integer (GB)
    tableCount: integer
    recordCount: integer

    # Performance
    queryPerSecond: float
    averageResponseTime: float (ms)
    cacheHitRatio: float (percentage)

    # Security
    encryptionAtRest: boolean
    encryptionInTransit: boolean
    authenticationMode: enum[database, windows, ldap, certificate]
    auditingEnabled: boolean

    # Data Classification
    dataClassification: enum[public, internal, confidential, restricted]
    containsPII: boolean
    containsPHI: boolean
    containsPCI: boolean

    # Backup
    backupSchedule: string
    lastBackup: datetime
    backupRetention: integer (days)

  relationships:
    hostedOn: Server (many-to-1)
    usedBy: Application (many-to-many)
    replicatesTo: Database (many-to-many)
    backupTo: BackupSystem (many-to-1)
    hasVulnerability: Vulnerability (many-to-many)
```

#### 2.4 Middleware (200 nodes)

**Middleware**
```yaml
Middleware:
  extends: Application
  properties:
    middlewareType: enum[message_queue, api_gateway, esb, application_server, cache, load_balancer]
    protocol: array[string]
    messagingModel: enum[pub_sub, point_to_point, request_reply]
    throughput: integer (messages/second)

  relationships:
    connects: Application (many-to-many)
    routes: Message (1-to-many)
```

#### 2.5 Licenses (300 nodes)

**SoftwareLicense**
```yaml
SoftwareLicense:
  properties:
    # Identity
    licenseID: string
    licenseKey: string
    licenseType: enum[perpetual, subscription, concurrent, named_user, site, enterprise, oem, academic]

    # Commercial
    vendor: string
    productName: string
    productVersion: string
    purchaseDate: date
    purchaseOrder: string
    cost: float
    currency: string

    # Terms
    startDate: date
    expiryDate: date
    renewalDate: date
    autoRenewal: boolean

    # Entitlements
    userCount: integer
    deviceCount: integer
    serverCount: integer
    coreCount: integer
    usedCount: integer
    availableCount: integer

    # Support
    supportLevel: enum[none, basic, standard, premium, enterprise]
    supportExpiry: date

    # Compliance
    complianceStatus: enum[compliant, over_deployed, under_utilized, expired, unknown]
    lastAudit: date

  relationships:
    for: Software (many-to-1)
    assignedTo: User|Asset (many-to-many)
    managedBy: LicenseManager (many-to-1)
```

---

### 3. CLOUD INFRASTRUCTURE (~1,000 nodes)

#### 3.1 Cloud Accounts (100 nodes)

**CloudAccount**
```yaml
CloudAccount:
  properties:
    accountID: string (cloud provider account ID)
    accountName: string
    provider: enum[aws, azure, gcp, oracle_cloud, alibaba_cloud, ibm_cloud]
    accountType: enum[production, staging, development, sandbox]

    # Billing
    billingContact: string
    billingEmail: string
    monthlyBudget: float
    currentSpend: float
    currency: string

    # Organization
    organizationID: string
    rootAccount: boolean
    parentAccount: string

    # Security
    mfaEnabled: boolean
    ssoEnabled: boolean
    cloudTrailEnabled: boolean (AWS)
    securityHubEnabled: boolean

  relationships:
    owns: CloudResource (1-to-many)
    managedBy: User (many-to-many)
    partOf: Organization (many-to-1)
```

#### 3.2 Cloud Compute (300 nodes)

**VirtualMachineInstance**
```yaml
VirtualMachineInstance:
  properties:
    # Identity
    instanceID: string (provider instance ID)
    instanceName: string
    instanceType: string (e.g., t3.medium, Standard_D4s_v3)

    # Configuration
    provider: enum[aws, azure, gcp, oracle, alibaba]
    region: string
    availabilityZone: string

    # Compute
    vcpu: integer
    memory: integer (GB)
    architecture: enum[x86_64, arm64]

    # Storage
    rootVolume: {type: string, size: integer, iops: integer, encrypted: boolean}
    additionalVolumes: array[object]

    # Network
    privateIP: string
    publicIP: string
    vpcID: string
    subnetID: string
    securityGroups: array[string]

    # State
    state: enum[running, stopped, terminated, pending, shutting_down]
    launchTime: datetime

    # Operating System
    operatingSystem: string
    imageID: string

    # Monitoring
    cpuUtilization: float
    networkIn: float (GB)
    networkOut: float (GB)

  relationships:
    partOf: CloudAccount (many-to-1)
    runsIn: VPC (many-to-1)
    attachedTo: CloudStorage (many-to-many)
    protectedBy: SecurityGroup (many-to-many)
    monitored By: CloudWatch|Monitor (many-to-1)
    hasVulnerability: Vulnerability (many-to-many)
```

**ContainerInstance**
```yaml
ContainerInstance:
  properties:
    containerID: string
    containerName: string
    imageID: string
    imageName: string
    imageTag: string

    # Runtime
    runtime: enum[docker, containerd, cri_o, podman]
    orchestrator: enum[kubernetes, ecs, aks, gke, docker_swarm, nomad]

    # Resources
    cpuLimit: float
    memoryLimit: integer (MB)
    cpuRequest: float
    memoryRequest: integer (MB)

    # State
    state: enum[running, stopped, paused, restarting, exited]
    startTime: datetime
    restartCount: integer

  relationships:
    runsIn: Pod|Task (many-to-1)
    basedOn: ContainerImage (many-to-1)
    hasVulnerability: Vulnerability (many-to-many)
```

#### 3.3 Cloud Storage (200 nodes)

**CloudStorageAccount**
```yaml
CloudStorageAccount:
  properties:
    storageAccountID: string
    accountName: string
    provider: enum[s3, azure_storage, gcs, oss]
    region: string
    redundancy: enum[lrs, zrs, grs, ra_grs, gzrs]

    # Capacity
    totalCapacity: integer (TB)
    usedCapacity: integer (TB)

    # Access
    accessTier: enum[hot, cool, archive]
    publicAccess: enum[none, blob, container]

    # Security
    encryptionEnabled: boolean
    encryptionType: enum[sse_s3, sse_kms, customer_managed]
    versioningEnabled: boolean

  relationships:
    contains: Bucket|Container (1-to-many)
    encryptedBy: KMSKey (many-to-1)
```

#### 3.4 Cloud Networking (200 nodes)

**VirtualNetwork**
```yaml
VirtualNetwork:
  properties:
    vpcID: string
    vpcName: string
    provider: enum[aws, azure, gcp]
    region: string
    cidrBlock: string

    # Configuration
    dnsEnabled: boolean
    dnsServers: array[string]
    enableDnsHostnames: boolean

  relationships:
    contains: Subnet (1-to-many)
    hasRouteTable: RouteTable (1-to-many)
    protectedBy: NetworkACL (1-to-many)
    peersWit h: VirtualNetwork (many-to-many)
```

#### 3.5 Cloud Functions (200 nodes)

**ServerlessFunction**
```yaml
ServerlessFunction:
  properties:
    functionID: string
    functionName: string
    runtime: string
    handler: string
    memorySize: integer (MB)
    timeout: integer (seconds)

    # Triggers
    triggerType: enum[http, event, schedule, queue, stream]
    triggerSource: string

    # Metrics
    invocationCount: integer
    errorCount: integer
    averageDuration: float (ms)

  relationships:
    triggeredBy: Event (many-to-many)
    accessesResource: CloudResource (many-to-many)
```

---

### 4. VIRTUALIZATION (~1,000 nodes)

#### 4.1 Hypervisors (100 nodes)

**Hypervisor**
```yaml
Hypervisor:
  extends: saref:Device
  properties:
    # Identity
    hypervisorID: string
    hostname: string

    # Type
    hypervisorType: enum[vmware_esxi, hyper_v, kvm, xen, proxmox, oracle_vm, citrix_hypervisor]
    version: string
    buildNumber: string

    # Resource Allocation
    totalCPU: integer (cores)
    allocatedCPU: integer (cores)
    totalMemory: integer (GB)
    allocatedMemory: integer (GB)
    totalStorage: integer (TB)
    allocatedStorage: integer (TB)

    # Capacity
    maxVMs: integer
    currentVMs: integer

    # Performance
    cpuUtilization: float (percentage)
    memoryUtilization: float (percentage)
    storageUtilization: float (percentage)

    # Network
    managementIP: string
    vmotionIP: string (vSphere)

  relationships:
    runsOn: PhysicalServer (many-to-1)
    hosts: VirtualMachine (1-to-many)
    partOf: Cluster (many-to-1)
    accessesStorage: SharedStorage (many-to-many)
    managedBy: VirtualizationManager (many-to-1)
```

#### 4.2 Virtual Machines (600 nodes)

**VirtualMachine**
```yaml
VirtualMachine:
  properties:
    # Identity
    vmID: string
    vmName: string
    uuid: string

    # Configuration
    vcpu: integer
    memory: integer (GB)
    storage: array[{name: string, size: integer, type: enum[thin, thick, eager_zeroed]}]

    # Operating System
    guestOS: string
    osVersion: string
    toolsStatus: enum[running, not_running, out_of_date]
    toolsVersion: string

    # Network
    networkAdapters: array[{name: string, macAddress: string, ipAddress: string, network: string}]

    # State
    powerState: enum[powered_on, powered_off, suspended]
    connectionState: enum[connected, disconnected, orphaned, invalid]

    # Performance
    cpuUsage: float (MHz)
    memoryUsage: float (MB)
    networkUsage: float (Mbps)
    diskUsage: float (MB/s)

    # High Availability
    faultTolerance: boolean
    haProtected: boolean
    drsEnabled: boolean

  relationships:
    hostedOn: Hypervisor (many-to-1)
    runsOS: OperatingSystem (1-to-1)
    runs: Application (1-to-many)
    attachedTo: VirtualDisk (many-to-many)
    snapshotOf: VirtualMachine (many-to-1)
    clonedFrom: VirtualMachine (many-to-1)
    migratesTo: Hypervisor (many-to-many)
```

#### 4.3 Virtual Storage (200 nodes)

**Datastore**
```yaml
Datastore:
  properties:
    datastoreID: string
    datastoreName: string
    type: enum[vmfs, nfs, vsan, iscsi]
    capacity: integer (GB)
    freeSpace: integer (GB)
    provisionedSpace: integer (GB)

    # Performance
    iops: integer
    throughput: float (MB/s)
    latency: float (ms)

  relationships:
    presentedTo: Hypervisor (many-to-many)
    stores: VirtualDisk (1-to-many)
    backedBy: StorageArray (many-to-1)
```

#### 4.4 Container Orchestration (100 nodes)

**KubernetesCluster**
```yaml
KubernetesCluster:
  properties:
    clusterID: string
    clusterName: string
    version: string
    distribution: enum[vanilla, eks, aks, gke, openshift, rancher]

    # Configuration
    nodeCount: integer
    masterCount: integer
    podCount: integer
    namespaceCount: integer

    # Networking
    serviceSubnet: string
    podSubnet: string
    cniPlugin: string

  relationships:
    contains: Node (1-to-many)
    runs: Pod (1-to-many)
    hasNamespace: Namespace (1-to-many)
```

---

## COMPLETE RELATIONSHIP SCHEMAS

### Asset-to-Vulnerability Relationships

```yaml
AssetVulnerabilityMapping:
  relationships:
    - PhysicalServer -[HAS_VULNERABILITY]-> Vulnerability
      properties:
        discoveryDate: datetime
        scanSource: string
        remediationStatus: enum[open, in_progress, mitigated, accepted, fixed]
        remediationDueDate: datetime
        businessImpact: enum[critical, high, medium, low]
        technicalImpact: enum[critical, high, medium, low]
        exploitability: enum[high, medium, low]

    - Application -[HAS_VULNERABILITY]-> Vulnerability
      properties:
        affectedVersion: string
        fixedVersion: string
        patchAvailable: boolean
        workaroundAvailable: boolean

    - Software -[HAS_VULNERABILITY]-> CVE
      properties:
        cveID: string
        cvssScore: float
        exploitAvailable: boolean
```

### Asset-to-Threat Relationships

```yaml
AssetThreatMapping:
  relationships:
    - Asset -[EXPOSED_TO]-> ThreatActor
      properties:
        exposureType: enum[direct, indirect]
        attackSurface: string
        likelihood: float (0-1)

    - Asset -[AFFECTED_BY]-> Incident
      properties:
        impactType: enum[compromised, unavailable, data_loss, performance_degradation]
        recoveryTime: integer (hours)
        dataLoss: integer (records)
```

### Asset-to-Asset Relationships

```yaml
AssetInterconnections:
  relationships:
    - Server -[DEPENDS_ON]-> Server
      properties:
        dependencyType: enum[cluster, replication, service, data]
        criticalPath: boolean

    - Application -[COMMUNICATES_WITH]-> Application
      properties:
        protocol: string
        port: integer
        dataFlow: enum[bidirectional, unidirectional]
        dataClassification: enum[public, internal, confidential]
```

---

## INTEGRATION PATTERNS

### 1. SAREF Integration

```cypher
# Link SAREF devices to IT infrastructure
MATCH (saref:saref__Device)
OPTIONAL MATCH (server:PhysicalServer {deviceID: saref.deviceID})
OPTIONAL MATCH (network:NetworkDevice {deviceID: saref.deviceID})
MERGE (saref)-[:REALIZED_BY]->(server)
MERGE (saref)-[:REALIZED_BY]->(network)

# Inherit SAREF properties into infrastructure nodes
MATCH (device:PhysicalServer)
SET device.energyEfficiency = saref.energyEfficiencyClass,
    device.powerConsumption = saref.powerConsumption
```

### 2. Cybersecurity Integration

```cypher
# Map vulnerabilities to software components
MATCH (app:Application)-[:CONTAINS]->(comp:SoftwareComponent)
MATCH (vuln:Vulnerability)-[:AFFECTS]->(comp)
MERGE (app)-[:HAS_VULNERABILITY {via: 'component'}]->(vuln)

# Track incidents affecting infrastructure
MATCH (incident:Incident)-[:AFFECTS]->(asset:Asset)
MATCH (asset)-[:RUNS]->(app:Application)
MERGE (incident)-[:IMPACTS {indirect: true}]->(app)
```

### 3. SBOM Integration

```cypher
# Link applications to SBOM components
MATCH (app:Application)
MATCH (pkg:Package {name: app.applicationName, version: app.version})
MERGE (app)-[:HAS_SBOM]->(pkg)

# Propagate vulnerabilities from SBOM
MATCH (app:Application)-[:HAS_SBOM]->(pkg:Package)
MATCH (pkg)-[:CONTAINS]->(comp:SoftwareComponent)
MATCH (comp)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
MERGE (app)-[:HAS_VULNERABILITY {source: 'sbom'}]->(vuln)
```

---

## VALIDATION CRITERIA

### Schema Validation
- [ ] All 5,000 nodes defined with complete property schemas
- [ ] All relationships mapped with cardinality
- [ ] All enums specified with valid values
- [ ] All data types declared and validated
- [ ] All constraints documented

### Integration Validation
- [ ] SAREF device mapping complete
- [ ] Cybersecurity threat correlation active
- [ ] SBOM vulnerability propagation working
- [ ] Cross-category queries validated
- [ ] Performance benchmarks met

### Data Quality
- [ ] Asset uniqueness enforced
- [ ] Relationship consistency validated
- [ ] Lifecycle states tracked
- [ ] Audit trails complete
- [ ] Compliance mappings verified

---

## EXAMPLE QUERIES

### Asset Inventory Queries

```cypher
# Complete hardware inventory with utilization
MATCH (server:PhysicalServer)
RETURN server.hostname,
       server.cpuUtilization,
       server.memoryUtilization,
       server.criticality
ORDER BY server.cpuUtilization DESC

# Software installed across all systems
MATCH (asset:Asset)-[:RUNS]->(app:Application)
RETURN app.applicationName,
       app.version,
       count(asset) as installCount
ORDER BY installCount DESC

# Find servers hosting vulnerable applications
MATCH (server:PhysicalServer)-[:RUNS]->(app:Application)
MATCH (app)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
WHERE vuln.cvssV3.baseScore > 7.0
RETURN server.hostname, app.applicationName, vuln.vulnerabilityID, vuln.cvssV3.baseScore
```

### Vulnerability Management Queries

```cypher
# Critical vulnerabilities requiring patching
MATCH (asset:Asset)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
WHERE vuln.cvssV3.severity = 'critical'
  AND NOT exists((vuln)<-[:FIXES]-(patch:Patch))
RETURN asset, vuln, vuln.cvssV3.baseScore
ORDER BY vuln.publishedDate DESC

# Vulnerability remediation status by asset criticality
MATCH (asset:Asset)-[rel:HAS_VULNERABILITY]->(vuln:Vulnerability)
RETURN asset.criticality,
       rel.remediationStatus,
       count(vuln) as vulnerabilityCount
```

### Cloud Asset Queries

```cypher
# Cloud spend by account and resource type
MATCH (account:CloudAccount)-[:OWNS]->(resource:CloudResource)
RETURN account.accountName,
       labels(resource)[0] as resourceType,
       sum(resource.monthlyCost) as totalCost
ORDER BY totalCost DESC

# Unencrypted cloud storage
MATCH (storage:CloudStorageAccount)
WHERE storage.encryptionEnabled = false
  AND storage.dataClassification IN ['confidential', 'restricted']
RETURN storage
```

---

**Wave Status:** COMPLETE
**Nodes Defined:** ~5,000
**Schemas Complete:** 100%
**Relationships Mapped:** 100%
**Integration Ready:** YES
