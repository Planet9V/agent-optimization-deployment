// ========================================
// OT/ICS Neo4j Schema Design
// Property-based sector differentiation
// Purdue Model integration (L0-L5)
// ========================================

// ========================================
// 1. FIELD DEVICE (Purdue L0-L1)
// ========================================

CREATE CONSTRAINT field_device_id IF NOT EXISTS
FOR (fd:FieldDevice) REQUIRE fd.id IS UNIQUE;

// Sample FieldDevice with comprehensive properties
CREATE (plc:FieldDevice {
  // Identity
  id: "PLC-SUBSTATION-001-PRIMARY",
  name: "Primary Control PLC - Substation 001",
  deviceType: "PLC", // PLC, RTU, IED, Sensor, Actuator, HMI, Remote_IO

  // Vendor/Model
  vendor: "Schneider Electric",
  model: "Modicon M580",
  firmwareVersion: "3.20",
  hardwareRevision: "Rev C",

  // Purdue Model Level
  purdueLevel: 1, // 0=Process, 1=Control, 2=Supervisory, 3=Operations, 4=Enterprise, 5=Corporate

  // Safety Integrity Level (IEC 61508)
  safetyLevel: "SIL-2", // SIL-1, SIL-2, SIL-3, SIL-4, NONE
  safetyFunction: "EMERGENCY_SHUTDOWN",

  // Network Configuration
  ipAddress: "10.100.50.10",
  macAddress: "00:1A:2B:3C:4D:5E",
  subnetMask: "255.255.0.0",
  defaultGateway: "10.100.0.1",

  // Criticality Assessment
  criticalityScore: 9, // 1-10 scale
  criticalityJustification: "Controls primary circuit breakers for 345kV transmission",
  singlePointOfFailure: true,

  // Operational State
  operationalState: "RUNNING", // RUNNING, IDLE, MAINTENANCE, OFFLINE, FAULT
  lastStateChange: datetime("2025-11-20T14:30:00Z"),
  uptimeHours: 8760, // Annual uptime

  // SECTOR DIFFERENTIATION (Property-based)
  sector: "ENERGY", // WATER, ENERGY, TRANSPORTATION, HEALTHCARE, FINANCIAL, NUCLEAR, etc.
  subSector: "ELECTRIC_TRANSMISSION",
  cisaCriticalFunction: "GENERATION_TRANSMISSION_DISTRIBUTION",

  // Location Context
  facilityId: "SUBSTATION-001",
  physicalLocation: "Building A, Control Room 2, Rack 3",
  gpsCoordinates: {latitude: 40.7128, longitude: -74.0060},

  // Asset Management
  assetOwner: "Regional Utility Corp",
  assetTag: "ASSET-2024-00451",
  purchaseDate: "2020-03-15",
  warrantyExpiration: "2025-03-15",
  maintenanceSchedule: "QUARTERLY",
  lastMaintenanceDate: "2025-10-15",
  nextMaintenanceDate: "2026-01-15",

  // Compliance & Standards
  complianceFrameworks: ["NERC-CIP-007", "IEC-62443-4-2", "NIST-800-82"],
  certifications: ["UL-508", "CSA-C22.2"],

  // Redundancy
  redundancyType: "HOT_STANDBY", // NONE, COLD_STANDBY, HOT_STANDBY, N+1, 2N
  redundantDeviceId: "PLC-SUBSTATION-001-BACKUP",

  // Metadata
  createdAt: datetime("2025-11-26T12:00:00Z"),
  updatedAt: datetime("2025-11-26T18:30:00Z"),
  createdBy: "system_import",
  dataSource: "ASSET_MANAGEMENT_SYSTEM"
});

// ========================================
// 2. CONTROL SYSTEM (Purdue L2)
// ========================================

CREATE CONSTRAINT control_system_id IF NOT EXISTS
FOR (cs:ControlSystem) REQUIRE cs.id IS UNIQUE;

CREATE (scada:ControlSystem {
  // Identity
  id: "SCADA-REGIONAL-001",
  name: "Regional SCADA Master Station",
  systemType: "SCADA", // SCADA, DCS, PCS, EMS, DMS, BMS, PLC_NETWORK

  // Vendor/Version
  vendor: "GE Digital",
  productName: "iFIX",
  version: "6.5",
  operatingSystem: "Windows Server 2019",

  // Purdue Level
  purdueLevel: 2,

  // Operational Scope
  managedDeviceCount: 450,
  geographicScope: "REGIONAL", // LOCAL, REGIONAL, NATIONAL, INTERNATIONAL
  coverageAreaKm2: 5000,

  // Sector Context
  sector: "ENERGY",
  subSector: "TRANSMISSION",
  cisaCriticalFunction: "GRID_OPERATIONS",

  // Network Configuration
  primaryServerIp: "10.100.1.10",
  secondaryServerIp: "10.100.1.11",
  networkZone: "DMZ-SCADA",

  // Redundancy
  redundancyLevel: "HOT_STANDBY",
  failoverTimeSeconds: 5,

  // Criticality
  criticalityScore: 10,
  populationImpact: 500000, // People affected if offline
  economicImpactUSD: 50000000, // Per-day estimate

  // Compliance
  complianceFrameworks: ["NERC-CIP-005", "NERC-CIP-007", "IEC-62443-3-3"],

  // Metadata
  createdAt: datetime("2025-11-26T12:00:00Z"),
  updatedAt: datetime("2025-11-26T18:30:00Z")
});

// ========================================
// 3. INFRASTRUCTURE FACILITY
// ========================================

CREATE CONSTRAINT facility_id IF NOT EXISTS
FOR (f:InfrastructureFacility) REQUIRE f.id IS UNIQUE;

CREATE (substation:InfrastructureFacility {
  // Identity
  id: "SUBSTATION-001",
  name: "Main Street Substation",
  facilityType: "SUBSTATION", // SUBSTATION, PLANT, TREATMENT_FACILITY, PUMP_STATION, DATA_CENTER, CONTROL_CENTER

  // Sector Classification
  sector: "ENERGY",
  subSector: "ELECTRIC_TRANSMISSION",

  // Physical Location
  address: "123 Main St, Springfield, IL 62701",
  gpsCoordinates: {latitude: 39.7817, longitude: -89.6501},
  countryCode: "US",
  stateProvince: "Illinois",

  // Capacity & Scale
  capacity: "500 MW",
  voltageLevel: "345 kV",
  transformerCount: 3,
  circuitBreakerCount: 12,

  // Operational Status
  operationalStatus: "ACTIVE", // ACTIVE, MAINTENANCE, DECOMMISSIONED, PLANNED
  commissionDate: "2015-06-01",

  // Criticality
  criticalityTier: "HIGH", // HIGH, MEDIUM, LOW
  populationServed: 50000,
  backupPowerAvailable: true,

  // Physical Security
  physicalSecurityLevel: "HIGH",
  perimeterFencing: true,
  accessControlType: "BIOMETRIC",
  cameraCount: 24,
  securityPersonnel: true,

  // Environmental
  floodRisk: "LOW",
  earthquakeZone: "MODERATE",
  environmentalHazards: [],

  // Compliance
  complianceFrameworks: ["NERC-CIP-006", "NERC-CIP-014"],

  // Metadata
  createdAt: datetime("2025-11-26T12:00:00Z"),
  updatedAt: datetime("2025-11-26T18:30:00Z")
});

// ========================================
// 4. ICS PROTOCOL
// ========================================

CREATE CONSTRAINT protocol_id IF NOT EXISTS
FOR (p:ICSProtocol) REQUIRE p.id IS UNIQUE;

CREATE (modbus:ICSProtocol {
  // Identity
  id: "MODBUS-TCP",
  name: "Modbus TCP/IP",
  protocolFamily: "MODBUS",
  protocolVariant: "TCP", // TCP, RTU, ASCII, PLUS

  // Security Characteristics
  hasAuthentication: false,
  hasEncryption: false,
  hasIntegrityCheck: false,
  defaultPort: 502,
  usesPlaintext: true,

  // Known Weaknesses
  knownWeaknesses: ["LACK_OF_AUTHENTICATION", "PLAINTEXT_COMMUNICATION", "NO_ENCRYPTION"],
  owasp_iot_risks: ["I1_WEAK_PASSWORDS", "I5_INSECURE_COMMUNICATIONS"],

  // Usage Context
  commonSectors: ["ENERGY", "WATER", "MANUFACTURING"],
  purdueLevel: [0, 1, 2], // Can span multiple levels

  // Standards Reference
  standardReference: "MODBUS Application Protocol V1.1b3",
  rfc: null,
  ieee: null,
  iec: "IEC-60870-5",

  // Mitigation Recommendations
  securityRecommendations: [
    "Implement firewall rules to restrict access",
    "Use VPN or encrypted tunnels",
    "Deploy protocol-aware IDS/IPS",
    "Implement network segmentation"
  ],

  // Metadata
  createdAt: datetime("2025-11-26T12:00:00Z"),
  updatedAt: datetime("2025-11-26T18:30:00Z")
});

// ========================================
// 5. NETWORK SEGMENT (IEC-62443 Zones)
// ========================================

CREATE CONSTRAINT network_segment_id IF NOT EXISTS
FOR (ns:NetworkSegment) REQUIRE ns.id IS UNIQUE;

CREATE (scadaDmz:NetworkSegment {
  // Identity
  id: "ZONE-SCADA-DMZ",
  name: "SCADA DMZ Zone",
  segmentType: "DMZ", // DMZ, PRODUCTION, CORPORATE, SAFETY, WIRELESS, REMOTE_ACCESS

  // Purdue Model
  purdueLevel: 2,

  // IEC-62443 Security Zones
  securityZone: "LEVEL-2", // LEVEL-0 (process) to LEVEL-4 (enterprise)
  conduitConnections: ["CONDUIT-1", "CONDUIT-3"],

  // Network Configuration
  vlanId: 100,
  ipRange: "10.100.0.0/16",
  subnetMask: "255.255.0.0",
  defaultGateway: "10.100.0.1",

  // Security Posture
  firewallRules: "RESTRICTIVE",
  firewallType: "STATEFUL_INSPECTION",
  idpsEnabled: true,
  idpsVendor: "Nozomi Networks",

  // Asset Inventory
  assetCount: 45,
  assetTypes: ["FieldDevice", "ControlSystem"],

  // Monitoring
  networkMonitoringEnabled: true,
  anomalyDetectionEnabled: true,
  logRetentionDays: 365,

  // Sector Context
  sector: "ENERGY",

  // Compliance
  complianceFrameworks: ["NERC-CIP-005", "IEC-62443-3-3"],

  // Metadata
  createdAt: datetime("2025-11-26T12:00:00Z"),
  updatedAt: datetime("2025-11-26T18:30:00Z")
});

// ========================================
// 6. ICS VULNERABILITY (CVE Extended)
// ========================================

CREATE CONSTRAINT ics_vuln_id IF NOT EXISTS
FOR (v:ICSVulnerability) REQUIRE v.id IS UNIQUE;

CREATE (vuln:ICSVulnerability {
  // CVE Identity
  id: "CVE-2021-22779",
  cveId: "CVE-2021-22779",

  // ICS Advisory
  icsAdvisory: "ICSA-21-154-01",
  cisaAdvisoryUrl: "https://www.cisa.gov/news-events/ics-advisories/icsa-21-154-01",

  // CWE Mapping
  cweId: "CWE-798",
  cweName: "Use of Hard-coded Credentials",

  // Description
  description: "Schneider Electric Modicon controllers contain hard-coded credentials that could allow remote attackers to gain unauthorized access",

  // Affected Components
  affectedVendors: ["Schneider Electric"],
  affectedProducts: ["Modicon M580", "Modicon M340", "Modicon M580 BMExNO0300"],
  affectedVersions: ["< 3.30"],
  affectedProtocols: ["MODBUS"],

  // Purdue Level Impact
  purdueImpact: [0, 1, 2],

  // Sector Targeting
  targetedSectors: ["ENERGY", "WATER", "CRITICAL_MANUFACTURING"],

  // CVSS v3.1
  cvssScore: 9.8,
  cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  cvssAttackVector: "NETWORK",
  cvssAttackComplexity: "LOW",
  cvssPrivilegesRequired: "NONE",
  cvssUserInteraction: "NONE",
  cvssScope: "UNCHANGED",
  cvssConfidentialityImpact: "HIGH",
  cvssIntegrityImpact: "HIGH",
  cvssAvailabilityImpact: "HIGH",

  // ICS-Specific Impact Assessment
  processImpact: "HIGH", // Loss of view, loss of control
  safetyImpact: "MEDIUM",
  availabilityImpact: "HIGH",
  environmentalImpact: "MEDIUM",
  economicImpact: "HIGH",

  // Exploitability
  remotelyExploitable: true,
  requiresAuthentication: false,
  userInteractionRequired: false,
  exploitPubliclyAvailable: true,
  exploitComplexity: "LOW",

  // Mitigation
  patchAvailable: true,
  patchVersion: ">= 3.30",
  workaroundAvailable: true,
  workaroundDescription: "Implement firewall rules to restrict access to port 502. Deploy network segmentation. Use VPN for remote access.",
  mitigationComplexity: "MEDIUM",

  // References
  references: [
    "https://www.cisa.gov/news-events/ics-advisories/icsa-21-154-01",
    "https://nvd.nist.gov/vuln/detail/CVE-2021-22779",
    "https://www.se.com/ww/en/download/document/SEVD-2021-159-01/"
  ],

  // Timeline
  publishedDate: datetime("2021-06-04T00:00:00Z"),
  lastModifiedDate: datetime("2021-06-10T00:00:00Z"),
  discoveryDate: datetime("2021-05-15T00:00:00Z"),

  // Threat Intelligence
  exploitInTheWild: false,
  ransomwareAssociation: [],
  aptGroups: [],

  // Metadata
  createdAt: datetime("2025-11-26T12:00:00Z"),
  updatedAt: datetime("2025-11-26T18:30:00Z")
});

// ========================================
// 7. PROCESS (Industrial Process)
// ========================================

CREATE CONSTRAINT process_id IF NOT EXISTS
FOR (p:Process) REQUIRE p.id IS UNIQUE;

CREATE (process:Process {
  // Identity
  id: "PROCESS-TRANSMISSION-001",
  name: "345kV Transmission Switching",
  processType: "POWER_TRANSMISSION", // GENERATION, TRANSMISSION, DISTRIBUTION, WATER_TREATMENT, etc.

  // Description
  description: "Automated circuit breaker control for 345kV transmission lines",

  // Operational Parameters
  normalOperatingRange: "340-350 kV",
  criticalThreshold: "355 kV",
  emergencyShutdownThreshold: "360 kV",

  // Safety Classification
  safetyClassification: "SAFETY_CRITICAL",
  safetyIntegrityLevel: "SIL-2",

  // Sector Context
  sector: "ENERGY",
  subSector: "TRANSMISSION",

  // Criticality
  criticalityScore: 10,
  populationImpact: 500000,

  // Metadata
  createdAt: datetime("2025-11-26T12:00:00Z"),
  updatedAt: datetime("2025-11-26T18:30:00Z")
});

// ========================================
// 8. SAFETY SYSTEM
// ========================================

CREATE CONSTRAINT safety_system_id IF NOT EXISTS
FOR (ss:SafetySystem) REQUIRE ss.id IS UNIQUE;

CREATE (sis:SafetySystem {
  // Identity
  id: "SIS-SUBSTATION-001",
  name: "Emergency Shutdown System - Substation 001",
  systemType: "SIS", // SIS, ESD, HIPPS, BMS

  // Safety Level
  safetyIntegrityLevel: "SIL-3",

  // Vendor
  vendor: "Honeywell",
  model: "Safety Manager",
  version: "R160",

  // Purdue Level
  purdueLevel: 1,

  // Operational
  testFrequency: "MONTHLY",
  lastProofTest: "2025-10-01",
  nextProofTest: "2025-12-01",

  // Sector
  sector: "ENERGY",

  // Metadata
  createdAt: datetime("2025-11-26T12:00:00Z"),
  updatedAt: datetime("2025-11-26T18:30:00Z")
});

// ========================================
// RELATIONSHIP DEFINITIONS
// ========================================

// Asset Hierarchy
MATCH (cs:ControlSystem {id: "SCADA-REGIONAL-001"})
MATCH (fd:FieldDevice {id: "PLC-SUBSTATION-001-PRIMARY"})
CREATE (cs)-[:MANAGES {
  managementProtocol: "MODBUS_TCP",
  pollingIntervalSeconds: 5,
  lastPollTime: datetime("2025-11-26T18:30:00Z")
}]->(fd);

// Physical Location
MATCH (fd:FieldDevice {id: "PLC-SUBSTATION-001-PRIMARY"})
MATCH (facility:InfrastructureFacility {id: "SUBSTATION-001"})
CREATE (fd)-[:LOCATED_IN {
  rack: "3",
  room: "Control Room 2",
  building: "A"
}]->(facility);

// Network Connectivity
MATCH (fd:FieldDevice {id: "PLC-SUBSTATION-001-PRIMARY"})
MATCH (ns:NetworkSegment {id: "ZONE-SCADA-DMZ"})
CREATE (fd)-[:CONNECTED_TO {
  ipAddress: "10.100.50.10",
  vlanId: 100,
  connectionType: "ETHERNET",
  bandwidth: "100 Mbps"
}]->(ns);

// Protocol Usage
MATCH (fd:FieldDevice {id: "PLC-SUBSTATION-001-PRIMARY"})
MATCH (proto:ICSProtocol {id: "MODBUS-TCP"})
CREATE (fd)-[:USES_PROTOCOL {
  port: 502,
  direction: "BIDIRECTIONAL",
  role: "SERVER"
}]->(proto);

// Process Control
MATCH (fd:FieldDevice {id: "PLC-SUBSTATION-001-PRIMARY"})
MATCH (process:Process {id: "PROCESS-TRANSMISSION-001"})
CREATE (fd)-[:CONTROLS {
  controlType: "AUTOMATED",
  responseTimeMs: 50,
  criticality: "HIGH"
}]->(process);

// Safety Protection
MATCH (sis:SafetySystem {id: "SIS-SUBSTATION-001"})
MATCH (process:Process {id: "PROCESS-TRANSMISSION-001"})
CREATE (sis)-[:PROTECTS {
  protectionType: "EMERGENCY_SHUTDOWN",
  activationThreshold: "360 kV",
  responseTimeMs: 100
}]->(process);

// Vulnerability Affects Asset
MATCH (vuln:ICSVulnerability {id: "CVE-2021-22779"})
MATCH (fd:FieldDevice {id: "PLC-SUBSTATION-001-PRIMARY"})
CREATE (vuln)-[:AFFECTS {
  severity: "CRITICAL",
  exploitAvailable: true,
  patchRequired: true,
  discoveredDate: datetime("2021-06-04T00:00:00Z"),
  mitigationStatus: "PENDING"
}]->(fd);

// Vulnerability Exploits Protocol
MATCH (vuln:ICSVulnerability {id: "CVE-2021-22779"})
MATCH (proto:ICSProtocol {id: "MODBUS-TCP"})
CREATE (vuln)-[:EXPLOITS_PROTOCOL {
  weakness: "CWE-798",
  attackVector: "NETWORK",
  authRequired: false,
  exploitComplexity: "LOW"
}]->(proto);

// ========================================
// INDEXES FOR PERFORMANCE
// ========================================

CREATE INDEX sector_criticality IF NOT EXISTS
FOR (fd:FieldDevice) ON (fd.sector, fd.criticalityScore);

CREATE INDEX vuln_cvss IF NOT EXISTS
FOR (v:ICSVulnerability) ON (v.cvssScore);

CREATE INDEX purdue_level IF NOT EXISTS
FOR (fd:FieldDevice) ON (fd.purdueLevel);

CREATE INDEX facility_sector IF NOT EXISTS
FOR (f:InfrastructureFacility) ON (f.sector);

CREATE INDEX protocol_name IF NOT EXISTS
FOR (p:ICSProtocol) ON (p.name);

CREATE INDEX network_zone IF NOT EXISTS
FOR (ns:NetworkSegment) ON (ns.securityZone);
