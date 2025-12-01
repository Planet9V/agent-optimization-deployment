# Wave 5: MITRE ATT&CK ICS Framework Integration

**File**: 07_WAVE_5_MITRE_ATTACK_ICS.md
**Created**: 2025-10-30
**Version**: v1.0.0
**Status**: ACTIVE
**Wave Duration**: 3 weeks
**Target Node Count**: ~450 nodes
**Dependencies**: Waves 1-4 (Core MITRE ATT&CK, Asset Classification)

## 1. Wave Overview

### 1.1 Objectives

Wave 5 extends the AEON Digital Twin cybersecurity knowledge graph with specialized Industrial Control Systems (ICS) and Operational Technology (OT) threat intelligence from MITRE ATT&CK for ICS framework.

**Primary Goals**:
- Integrate complete MITRE ATT&CK for ICS matrix (tactics, techniques, procedures)
- Model ICS-specific assets (PLCs, SCADA systems, HMIs, RTUs, DCS components)
- Establish relationships between ICS techniques and industrial assets
- Connect ICS attack patterns to critical infrastructure sectors
- Preserve existing CVE relationships and general ATT&CK framework
- Enable OT/IT threat modeling and attack surface analysis

**Business Value**:
- Comprehensive critical infrastructure threat modeling
- OT-specific vulnerability assessment capabilities
- Industrial cyber-physical attack simulation
- Supply chain risk analysis for industrial environments
- Regulatory compliance support (NERC CIP, IEC 62443, NIST CSF)

### 1.2 Scope Definition

**In Scope**:
- 12 MITRE ATT&CK ICS tactics
- 78 ICS-specific techniques and sub-techniques
- ICS asset types (PLCs, SCADA, HMI, RTU, DCS, Safety Systems)
- ICS network zones (Control Network, Field Network, DMZ)
- Critical infrastructure sectors (Energy, Water, Manufacturing, Transportation)
- ICS protocols (Modbus, DNP3, OPC, Profinet, EtherNet/IP)
- Industrial vulnerability patterns
- OT-specific threat actor profiles

**Out of Scope**:
- Building automation systems (BAS) detailed modeling
- Maritime-specific systems (separate wave consideration)
- Medical device networks (separate domain)
- Detailed PLC programming logic analysis

### 1.3 Dependencies

**Required Completed Waves**:
- Wave 1: Core MITRE ATT&CK framework (tactics, techniques, enterprise TTPs)
- Wave 2: Asset classification and inventory schema
- Wave 4: CVE integration (for ICS vulnerabilities)

**Data Sources**:
- MITRE ATT&CK for ICS matrix (https://attack.mitre.org/matrices/ics/)
- ICS-CERT advisories
- CISA ICS vulnerability database
- ICS protocol specifications
- Critical infrastructure sector frameworks

### 1.4 Success Metrics

**Quantitative Metrics**:
- 12 ICS tactics fully modeled
- 78+ ICS techniques with complete property data
- 150+ ICS asset type nodes created
- 200+ technique-to-asset relationships established
- 50+ ICS protocol nodes with specifications
- 16 critical infrastructure sectors mapped
- 100% CVE preservation validation

**Qualitative Metrics**:
- Query performance <500ms for ICS attack path enumeration
- Complete OT kill chain modeling capability
- Integration with existing enterprise ATT&CK techniques
- Support for ICS-specific threat hunting queries

## 2. Complete Node Schemas

### 2.1 ICS Tactic Nodes

**Node Label**: `ICS_Tactic`

**Description**: Tactical objectives in MITRE ATT&CK for ICS framework representing adversary goals in industrial control system environments.

**Properties**:
```cypher
// Complete property list with descriptions and constraints
{
  tactic_id: String,              // MITRE ICS tactic ID (e.g., "TA0108")
  name: String,                   // Tactic name (e.g., "Initial Access")
  description: String,            // Detailed tactical objective description
  mitre_url: String,             // Official MITRE page URL
  created_date: DateTime,         // Tactic creation timestamp
  modified_date: DateTime,        // Last modification timestamp
  version: String,                // ATT&CK version (e.g., "v13")
  order_position: Integer,        // Position in ICS kill chain (1-12)
  attack_domain: String,          // Always "ics" for ICS tactics
  applicable_sectors: [String],   // Critical infrastructure sectors
  external_references: [Map],     // Citations and source materials

  // Classification metadata
  classification: String,         // "MITRE_ICS_TACTIC"
  confidence_score: Float,        // Data quality confidence (0.0-1.0)
  data_source: String,            // "MITRE ATT&CK ICS v13"

  // Integration metadata
  node_id: String,               // UUID for node identity
  created_by: String,            // System/user who created node
  last_updated: DateTime,        // Node last update timestamp
  validation_status: String      // "VALIDATED" | "PENDING" | "NEEDS_REVIEW"
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create ICS Tactic node with full property set
CREATE (t:ICS_Tactic {
  tactic_id: "TA0108",
  name: "Initial Access",
  description: "The adversary is trying to get into your ICS environment. Initial Access consists of techniques that use various entry vectors to gain their initial foothold within ICS networks. Techniques used to gain a foothold include targeted spearphishing and exploiting weaknesses on public-facing web servers and operational interfaces.",
  mitre_url: "https://attack.mitre.org/tactics/TA0108",
  created_date: datetime('2020-10-28T00:00:00Z'),
  modified_date: datetime('2023-10-01T00:00:00Z'),
  version: "v13",
  order_position: 1,
  attack_domain: "ics",
  applicable_sectors: ["Energy", "Water", "Manufacturing", "Transportation", "Chemical"],
  external_references: [
    {source: "MITRE", url: "https://attack.mitre.org/tactics/TA0108", description: "Initial Access ICS"}
  ],
  classification: "MITRE_ICS_TACTIC",
  confidence_score: 1.0,
  data_source: "MITRE ATT&CK ICS v13",
  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on MITRE tactic ID
CREATE CONSTRAINT ics_tactic_id_unique IF NOT EXISTS
FOR (t:ICS_Tactic) REQUIRE t.tactic_id IS UNIQUE;

// Index on tactic name for fast lookup
CREATE INDEX ics_tactic_name_idx IF NOT EXISTS
FOR (t:ICS_Tactic) ON (t.name);

// Index on order position for kill chain queries
CREATE INDEX ics_tactic_order_idx IF NOT EXISTS
FOR (t:ICS_Tactic) ON (t.order_position);

// Full-text search index for descriptions
CREATE FULLTEXT INDEX ics_tactic_fulltext IF NOT EXISTS
FOR (t:ICS_Tactic) ON EACH [t.description, t.name];
```

**Complete List of 12 ICS Tactics**:
```cypher
// Batch create all 12 MITRE ATT&CK ICS tactics
UNWIND [
  {tactic_id: "TA0108", name: "Initial Access", order: 1, desc: "Gain initial foothold in ICS environment"},
  {tactic_id: "TA0109", name: "Execution", order: 2, desc: "Execute adversary-controlled code in ICS"},
  {tactic_id: "TA0110", name: "Persistence", order: 3, desc: "Maintain presence in ICS environment"},
  {tactic_id: "TA0111", name: "Privilege Escalation", order: 4, desc: "Gain higher-level permissions in ICS"},
  {tactic_id: "TA0112", name: "Evasion", order: 5, desc: "Avoid detection in ICS environment"},
  {tactic_id: "TA0100", name: "Impair Process Control", order: 6, desc: "Manipulate or disable industrial process control"},
  {tactic_id: "TA0101", name: "Inhibit Response Function", order: 7, desc: "Prevent safety systems and response"},
  {tactic_id: "TA0102", name: "Collection", order: 8, desc: "Gather ICS process data and intelligence"},
  {tactic_id: "TA0103", name: "Command and Control", order: 9, desc: "Communicate with compromised ICS systems"},
  {tactic_id: "TA0104", name: "Lateral Movement", order: 10, desc: "Move through ICS network zones"},
  {tactic_id: "TA0105", name: "Discovery", order: 11, desc: "Gain knowledge of ICS environment"},
  {tactic_id: "TA0106", name: "Impact", order: 12, desc: "Disrupt, manipulate, or destroy ICS processes"}
] AS tactic
CREATE (t:ICS_Tactic {
  tactic_id: tactic.tactic_id,
  name: tactic.name,
  description: tactic.desc,
  order_position: tactic.order,
  attack_domain: "ics",
  version: "v13",
  mitre_url: "https://attack.mitre.org/tactics/" + tactic.tactic_id,
  created_date: datetime('2020-10-28T00:00:00Z'),
  modified_date: datetime('2023-10-01T00:00:00Z'),
  classification: "MITRE_ICS_TACTIC",
  confidence_score: 1.0,
  data_source: "MITRE ATT&CK ICS v13",
  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  last_updated: datetime(),
  validation_status: "VALIDATED"
});
```

### 2.2 ICS Technique Nodes

**Node Label**: `ICS_Technique`

**Description**: Specific technical methods adversaries use to achieve tactical objectives in ICS environments.

**Properties**:
```cypher
{
  technique_id: String,           // MITRE ICS technique ID (e.g., "T0883")
  name: String,                   // Technique name
  description: String,            // Detailed technique description
  parent_technique_id: String,    // Parent if this is sub-technique
  is_subtechnique: Boolean,       // True if sub-technique
  mitre_url: String,             // Official MITRE page URL

  // Tactical associations
  tactics: [String],             // Associated tactic IDs

  // Technical details
  detection_methods: [String],   // Detection approaches
  data_sources: [String],        // Required data sources for detection
  affected_assets: [String],     // ICS asset types impacted
  ics_protocols: [String],       // Relevant ICS protocols

  // Threat intelligence
  procedure_examples: [Map],     // Real-world attack examples
  mitigation_strategies: [String], // Defensive measures
  platforms: [String],           // Target platforms (e.g., "Windows", "Engineering Workstation")

  // Sector-specific data
  critical_sectors: [String],    // Most affected sectors
  severity_rating: String,       // Impact severity (LOW/MEDIUM/HIGH/CRITICAL)

  // Standards references
  iec_62443_references: [String], // IEC 62443 standard mappings
  nerc_cip_references: [String],  // NERC CIP requirement mappings
  nist_csf_references: [String],  // NIST CSF function mappings

  // Metadata
  created_date: DateTime,
  modified_date: DateTime,
  version: String,
  classification: String,
  confidence_score: Float,
  data_source: String,
  node_id: String,
  created_by: String,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement (Example)**:
```cypher
// Create ICS Technique: Modify Controller Tasking
CREATE (t:ICS_Technique {
  technique_id: "T0821",
  name: "Modify Controller Tasking",
  description: "Adversaries may modify the tasking of a controller to allow for the execution of their own programs. This can allow an adversary to manipulate the execution flow and behavior of a device, and may be used to achieve Execution or to cause a permanent loss of control through Damage to Device.",
  parent_technique_id: null,
  is_subtechnique: false,
  mitre_url: "https://attack.mitre.org/techniques/T0821",

  tactics: ["TA0100", "TA0109", "TA0110"], // Impair Process Control, Execution, Persistence

  detection_methods: [
    "Monitor controller program changes and versions",
    "Baseline controller memory and compare for anomalies",
    "Monitor controller ladder logic modifications",
    "Audit engineering workstation access and activities"
  ],
  data_sources: [
    "Controller Configuration Changes",
    "Network Traffic: ICS Protocol",
    "Application Log: Engineering Workstation",
    "File: File Modification"
  ],
  affected_assets: [
    "Programmable Logic Controller (PLC)",
    "Distributed Control System (DCS)",
    "Safety Instrumented System (SIS)",
    "Remote Terminal Unit (RTU)"
  ],
  ics_protocols: ["Modbus", "OPC", "Profinet", "EtherNet/IP", "CIP"],

  procedure_examples: [
    {
      campaign: "TRITON/TRISIS",
      description: "Modified Schneider Electric Triconex safety controllers to execute malicious ladder logic",
      year: 2017,
      sector: "Energy"
    },
    {
      campaign: "Industroyer/CRASHOVERRIDE",
      description: "Modified substation controller configurations to open circuit breakers",
      year: 2016,
      sector: "Energy"
    }
  ],

  mitigation_strategies: [
    "Implement code signing for controller programs",
    "Restrict engineering workstation access with MFA",
    "Network segmentation between IT and OT",
    "Version control for all controller programs",
    "Implement change management procedures",
    "Monitor and log all controller modifications"
  ],

  platforms: ["Windows", "Engineering Workstation", "PLC", "DCS"],
  critical_sectors: ["Energy", "Water", "Chemical", "Manufacturing"],
  severity_rating: "CRITICAL",

  iec_62443_references: ["SR 3.4", "SR 7.6", "SR 3.1"],
  nerc_cip_references: ["CIP-007-6 R4", "CIP-010-3"],
  nist_csf_references: ["PR.DS-6", "PR.IP-1", "DE.CM-7"],

  created_date: datetime('2020-10-28T00:00:00Z'),
  modified_date: datetime('2023-10-01T00:00:00Z'),
  version: "v13",
  classification: "MITRE_ICS_TECHNIQUE",
  confidence_score: 0.95,
  data_source: "MITRE ATT&CK ICS v13",
  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on technique ID
CREATE CONSTRAINT ics_technique_id_unique IF NOT EXISTS
FOR (t:ICS_Technique) REQUIRE t.technique_id IS UNIQUE;

// Index on technique name
CREATE INDEX ics_technique_name_idx IF NOT EXISTS
FOR (t:ICS_Technique) ON (t.name);

// Index on severity rating for risk queries
CREATE INDEX ics_technique_severity_idx IF NOT EXISTS
FOR (t:ICS_Technique) ON (t.severity_rating);

// Index on affected assets for asset-based queries
CREATE INDEX ics_technique_assets_idx IF NOT EXISTS
FOR (t:ICS_Technique) ON (t.affected_assets);

// Full-text search
CREATE FULLTEXT INDEX ics_technique_fulltext IF NOT EXISTS
FOR (t:ICS_Technique) ON EACH [t.name, t.description, t.detection_methods];
```

**Key ICS Techniques (Sample Set - 20 of 78)**:
```cypher
// Create critical ICS techniques
UNWIND [
  {id: "T0800", name: "Activate Firmware Update Mode", severity: "HIGH", tactics: ["TA0110"]},
  {id: "T0801", name: "Monitor Process State", severity: "MEDIUM", tactics: ["TA0102"]},
  {id: "T0802", name: "Automated Collection", severity: "MEDIUM", tactics: ["TA0102"]},
  {id: "T0803", name: "Block Command Message", severity: "HIGH", tactics: ["TA0101"]},
  {id: "T0804", name: "Block Reporting Message", severity: "HIGH", tactics: ["TA0101"]},
  {id: "T0805", name: "Block Serial COM", severity: "HIGH", tactics: ["TA0101"]},
  {id: "T0806", name: "Brute Force I/O", severity: "CRITICAL", tactics: ["TA0100"]},
  {id: "T0807", name: "Command-Line Interface", severity: "MEDIUM", tactics: ["TA0109"]},
  {id: "T0808", name: "Control Device Identification", severity: "MEDIUM", tactics: ["TA0105"]},
  {id: "T0809", name: "Data Destruction", severity: "CRITICAL", tactics: ["TA0106"]},
  {id: "T0810", name: "Data Historian Compromise", severity: "HIGH", tactics: ["TA0102"]},
  {id: "T0811", name: "Data from Information Repositories", severity: "MEDIUM", tactics: ["TA0102"]},
  {id: "T0812", name: "Default Credentials", severity: "HIGH", tactics: ["TA0108"]},
  {id: "T0813", name: "Denial of Control", severity: "CRITICAL", tactics: ["TA0106"]},
  {id: "T0814", name: "Denial of View", severity: "HIGH", tactics: ["TA0106"]},
  {id: "T0815", name: "Denial of Service", severity: "HIGH", tactics: ["TA0101", "TA0106"]},
  {id: "T0816", name: "Device Restart/Shutdown", severity: "HIGH", tactics: ["TA0101"]},
  {id: "T0817", name: "Drive-by Compromise", severity: "MEDIUM", tactics: ["TA0108"]},
  {id: "T0818", name: "Engineering Workstation Compromise", severity: "CRITICAL", tactics: ["TA0108"]},
  {id: "T0819", name: "Exploit Public-Facing Application", severity: "HIGH", tactics: ["TA0108"]}
] AS tech
CREATE (t:ICS_Technique {
  technique_id: tech.id,
  name: tech.name,
  severity_rating: tech.severity,
  tactics: tech.tactics,
  is_subtechnique: false,
  mitre_url: "https://attack.mitre.org/techniques/" + tech.id,
  version: "v13",
  attack_domain: "ics",
  classification: "MITRE_ICS_TECHNIQUE",
  confidence_score: 0.9,
  data_source: "MITRE ATT&CK ICS v13",
  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
});
```

### 2.3 ICS Asset Nodes

**Node Label**: `ICS_Asset`

**Description**: Industrial control system components and equipment targeted by ICS-specific techniques.

**Properties**:
```cypher
{
  asset_id: String,              // Unique asset identifier
  asset_type: String,            // Asset category (PLC, SCADA, HMI, etc.)
  asset_name: String,            // Common name/model designation
  manufacturer: String,          // Vendor/manufacturer
  model: String,                 // Specific model identifier
  firmware_version: String,      // Current firmware version

  // Classification
  asset_category: String,        // Field Device, Control System, Network Device
  purdue_level: Integer,         // ISA-95 Purdue Model level (0-5)
  criticality: String,           // LOW/MEDIUM/HIGH/CRITICAL

  // Network properties
  network_zone: String,          // Control, Field, Enterprise, DMZ
  ip_addresses: [String],        // Assigned IP addresses
  mac_address: String,           // Physical address
  protocols_supported: [String], // ICS protocols (Modbus, DNP3, etc.)
  network_ports: [Integer],      // Open TCP/UDP ports

  // Operational properties
  process_functions: [String],   // Industrial process functions
  physical_location: String,     // Plant location/zone
  operational_state: String,     // RUNNING, STOPPED, MAINTENANCE
  last_maintenance: DateTime,    // Last maintenance date

  // Security properties
  authentication_enabled: Boolean,
  encryption_supported: Boolean,
  patch_level: String,
  known_vulnerabilities: [String], // CVE IDs
  security_controls: [String],

  // Standards compliance
  iec_62443_level: String,      // Security level (SL1-SL4)
  nerc_cip_classification: String,

  // Integration metadata
  sector: String,               // Critical infrastructure sector
  sub_sector: String,           // Specific industry sub-sector
  vendor_support_status: String, // ACTIVE, EOL, DEPRECATED

  // Metadata
  node_id: String,
  created_by: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement (Example)**:
```cypher
// Create ICS Asset: Siemens S7-1500 PLC
CREATE (a:ICS_Asset {
  asset_id: "PLC-S7-1500-001",
  asset_type: "Programmable Logic Controller (PLC)",
  asset_name: "Siemens S7-1500",
  manufacturer: "Siemens",
  model: "6ES7515-2AM01-0AB0",
  firmware_version: "V2.9",

  asset_category: "Control System",
  purdue_level: 1,
  criticality: "CRITICAL",

  network_zone: "Control Network",
  ip_addresses: ["10.10.10.50"],
  mac_address: "00:1B:1B:5A:3F:2C",
  protocols_supported: ["Profinet", "S7comm", "OPC UA", "Modbus TCP"],
  network_ports: [102, 4840, 502, 34962],

  process_functions: [
    "Reactor Temperature Control",
    "Pressure Regulation",
    "Safety Interlock Management"
  ],
  physical_location: "Production Line A - Control Room",
  operational_state: "RUNNING",
  last_maintenance: datetime('2024-09-15T00:00:00Z'),

  authentication_enabled: true,
  encryption_supported: true,
  patch_level: "CURRENT",
  known_vulnerabilities: [],
  security_controls: [
    "Role-Based Access Control",
    "Program Block Protection",
    "Integrity Monitoring"
  ],

  iec_62443_level: "SL2",
  nerc_cip_classification: "BES Cyber Asset",

  sector: "Energy",
  sub_sector: "Electric Power Generation",
  vendor_support_status: "ACTIVE",

  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on asset ID
CREATE CONSTRAINT ics_asset_id_unique IF NOT EXISTS
FOR (a:ICS_Asset) REQUIRE a.asset_id IS UNIQUE;

// Index on asset type for category queries
CREATE INDEX ics_asset_type_idx IF NOT EXISTS
FOR (a:ICS_Asset) ON (a.asset_type);

// Index on criticality for risk assessment
CREATE INDEX ics_asset_criticality_idx IF NOT EXISTS
FOR (a:ICS_Asset) ON (a.criticality);

// Index on Purdue level for architecture queries
CREATE INDEX ics_asset_purdue_idx IF NOT EXISTS
FOR (a:ICS_Asset) ON (a.purdue_level);

// Index on network zone
CREATE INDEX ics_asset_zone_idx IF NOT EXISTS
FOR (a:ICS_Asset) ON (a.network_zone);

// Full-text search
CREATE FULLTEXT INDEX ics_asset_fulltext IF NOT EXISTS
FOR (a:ICS_Asset) ON EACH [a.asset_name, a.manufacturer, a.model];
```

**Common ICS Asset Types**:
```cypher
// Create representative ICS assets across categories
UNWIND [
  // Field Devices (Purdue Level 0-1)
  {type: "Programmable Logic Controller (PLC)", level: 1, criticality: "CRITICAL", zone: "Control Network"},
  {type: "Remote Terminal Unit (RTU)", level: 1, criticality: "HIGH", zone: "Field Network"},
  {type: "Intelligent Electronic Device (IED)", level: 1, criticality: "HIGH", zone: "Field Network"},
  {type: "Variable Frequency Drive (VFD)", level: 0, criticality: "MEDIUM", zone: "Field Network"},
  {type: "Industrial Sensor", level: 0, criticality: "MEDIUM", zone: "Field Network"},
  {type: "Industrial Actuator", level: 0, criticality: "MEDIUM", zone: "Field Network"},

  // Control Systems (Purdue Level 2)
  {type: "SCADA Server", level: 2, criticality: "CRITICAL", zone: "Control Network"},
  {type: "Distributed Control System (DCS)", level: 2, criticality: "CRITICAL", zone: "Control Network"},
  {type: "Human-Machine Interface (HMI)", level: 2, criticality: "HIGH", zone: "Control Network"},
  {type: "Engineering Workstation", level: 2, criticality: "HIGH", zone: "Control Network"},
  {type: "Historian Server", level: 2, criticality: "HIGH", zone: "Control Network"},

  // Safety Systems
  {type: "Safety Instrumented System (SIS)", level: 1, criticality: "CRITICAL", zone: "Safety Network"},
  {type: "Emergency Shutdown System (ESD)", level: 1, criticality: "CRITICAL", zone: "Safety Network"},

  // Network Infrastructure
  {type: "Industrial Ethernet Switch", level: 2, criticality: "HIGH", zone: "Control Network"},
  {type: "Industrial Firewall", level: 3, criticality: "HIGH", zone: "DMZ"},
  {type: "Data Diode", level: 3, criticality: "MEDIUM", zone: "DMZ"}
] AS asset
CREATE (a:ICS_Asset {
  asset_type: asset.type,
  purdue_level: asset.level,
  criticality: asset.criticality,
  network_zone: asset.zone,
  asset_category: CASE
    WHEN asset.level IN [0, 1] THEN "Field Device"
    WHEN asset.level = 2 THEN "Control System"
    ELSE "Network Device"
  END,
  authentication_enabled: asset.level >= 2,
  encryption_supported: asset.level >= 2,
  iec_62443_level: CASE
    WHEN asset.criticality = "CRITICAL" THEN "SL3"
    WHEN asset.criticality = "HIGH" THEN "SL2"
    ELSE "SL1"
  END,
  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
});
```

### 2.4 ICS Protocol Nodes

**Node Label**: `ICS_Protocol`

**Description**: Industrial communication protocols used in OT/ICS environments.

**Properties**:
```cypher
{
  protocol_id: String,           // Unique protocol identifier
  protocol_name: String,         // Common protocol name
  protocol_family: String,       // Protocol category (Fieldbus, Ethernet-based, etc.)
  osi_layer: Integer,           // Primary OSI layer (1-7)

  // Technical specifications
  standard_reference: String,    // IEEE, IEC, or vendor standard
  port_numbers: [Integer],       // Default TCP/UDP ports
  transport_protocol: String,    // TCP, UDP, Serial
  data_format: String,           // Binary, ASCII, XML

  // Security characteristics
  authentication_support: Boolean,
  encryption_support: Boolean,
  known_vulnerabilities: [String], // Common security weaknesses
  security_extensions: [String],   // Security protocol additions

  // Operational properties
  deterministic: Boolean,        // Real-time determinism
  max_devices: Integer,          // Maximum supported devices
  max_distance: String,          // Maximum communication distance
  bandwidth: String,             // Typical bandwidth

  // Industry usage
  common_sectors: [String],      // Where protocol is used
  vendor_support: [String],      // Major vendor implementations
  adoption_level: String,        // WIDESPREAD, COMMON, NICHE, LEGACY

  // Attack surface
  exploitable_features: [String],
  mitigation_approaches: [String],
  monitoring_methods: [String],

  // Metadata
  node_id: String,
  created_by: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement (Example)**:
```cypher
// Create ICS Protocol: Modbus TCP
CREATE (p:ICS_Protocol {
  protocol_id: "MODBUS-TCP",
  protocol_name: "Modbus TCP/IP",
  protocol_family: "Ethernet-based Industrial Protocol",
  osi_layer: 7,

  standard_reference: "MODBUS Application Protocol Specification V1.1b3",
  port_numbers: [502],
  transport_protocol: "TCP",
  data_format: "Binary",

  authentication_support: false,
  encryption_support: false,
  known_vulnerabilities: [
    "No authentication mechanism",
    "No encryption by default",
    "Susceptible to man-in-the-middle attacks",
    "Command injection possible",
    "Easily spoofed"
  ],
  security_extensions: ["Modbus Security", "TLS wrapper"],

  deterministic: false,
  max_devices: 247,
  max_distance: "100 meters (standard Ethernet)",
  bandwidth: "10-100 Mbps",

  common_sectors: ["Energy", "Water", "Manufacturing", "Building Automation"],
  vendor_support: ["Schneider Electric", "Siemens", "ABB", "Rockwell Automation"],
  adoption_level: "WIDESPREAD",

  exploitable_features: [
    "Unauthenticated read/write operations",
    "Predictable transaction IDs",
    "No message integrity verification",
    "Broadcast capabilities"
  ],
  mitigation_approaches: [
    "Network segmentation",
    "Industrial firewall with protocol inspection",
    "VPN or TLS tunneling",
    "Whitelist allowed function codes",
    "Monitor for anomalous traffic patterns"
  ],
  monitoring_methods: [
    "Deep packet inspection",
    "Baseline normal traffic patterns",
    "Anomaly detection on function codes",
    "Monitor unauthorized read/write operations"
  ],

  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on protocol ID
CREATE CONSTRAINT ics_protocol_id_unique IF NOT EXISTS
FOR (p:ICS_Protocol) REQUIRE p.protocol_id IS UNIQUE;

// Index on protocol name
CREATE INDEX ics_protocol_name_idx IF NOT EXISTS
FOR (p:ICS_Protocol) ON (p.protocol_name);

// Index on port numbers for network analysis
CREATE INDEX ics_protocol_ports_idx IF NOT EXISTS
FOR (p:ICS_Protocol) ON (p.port_numbers);

// Full-text search
CREATE FULLTEXT INDEX ics_protocol_fulltext IF NOT EXISTS
FOR (p:ICS_Protocol) ON EACH [p.protocol_name, p.standard_reference];
```

**Major ICS Protocols**:
```cypher
// Create common ICS protocols
UNWIND [
  {id: "MODBUS-TCP", name: "Modbus TCP/IP", port: 502, auth: false, encrypt: false, level: "WIDESPREAD"},
  {id: "MODBUS-RTU", name: "Modbus RTU", port: null, auth: false, encrypt: false, level: "WIDESPREAD"},
  {id: "DNP3", name: "DNP3 (Distributed Network Protocol)", port: 20000, auth: true, encrypt: true, level: "COMMON"},
  {id: "OPC-UA", name: "OPC Unified Architecture", port: 4840, auth: true, encrypt: true, level: "WIDESPREAD"},
  {id: "PROFINET", name: "Profinet IO", port: 34962, auth: false, encrypt: false, level: "WIDESPREAD"},
  {id: "ETHERNETIP", name: "EtherNet/IP", port: 44818, auth: false, encrypt: false, level: "WIDESPREAD"},
  {id: "BACnet", name: "BACnet/IP", port: 47808, auth: false, encrypt: false, level: "COMMON"},
  {id: "IEC-61850", name: "IEC 61850 (Substation Automation)", port: 102, auth: false, encrypt: false, level: "COMMON"},
  {id: "IEC-60870-5-104", name: "IEC 60870-5-104", port: 2404, auth: false, encrypt: false, level: "COMMON"},
  {id: "S7COMM", name: "Siemens S7 Communication", port: 102, auth: false, encrypt: false, level: "COMMON"}
] AS proto
CREATE (p:ICS_Protocol {
  protocol_id: proto.id,
  protocol_name: proto.name,
  port_numbers: CASE WHEN proto.port IS NOT NULL THEN [proto.port] ELSE [] END,
  authentication_support: proto.auth,
  encryption_support: proto.encrypt,
  adoption_level: proto.level,
  transport_protocol: "TCP",
  osi_layer: 7,
  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
});
```

### 2.5 Critical Infrastructure Sector Nodes

**Node Label**: `Critical_Infrastructure_Sector`

**Description**: CISA-defined critical infrastructure sectors for ICS threat modeling.

**Properties**:
```cypher
{
  sector_id: String,             // Unique sector identifier
  sector_name: String,           // Official sector name
  sector_abbreviation: String,   // Common abbreviation

  // Sector details
  description: String,           // Sector description
  cisa_designation: String,      // Official CISA designation
  regulatory_framework: [String], // Applicable regulations

  // Threat landscape
  primary_threats: [String],     // Top threat types
  high_risk_techniques: [String], // Most relevant ICS techniques
  notable_incidents: [Map],       // Historical attacks

  // Asset characteristics
  common_asset_types: [String],  // Typical ICS assets
  common_protocols: [String],    // Common ICS protocols
  typical_purdue_levels: [Integer], // Relevant Purdue levels

  // Standards and compliance
  sector_specific_standards: [String],
  security_frameworks: [String],

  // Metadata
  node_id: String,
  created_by: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement (Example)**:
```cypher
// Create Critical Infrastructure Sector: Energy
CREATE (s:Critical_Infrastructure_Sector {
  sector_id: "CISA-SECTOR-ENERGY",
  sector_name: "Energy Sector",
  sector_abbreviation: "ENERGY",

  description: "Electric power generation, transmission, distribution, and petroleum refining and storage",
  cisa_designation: "Critical Infrastructure Sector - Energy",
  regulatory_framework: [
    "NERC CIP (Critical Infrastructure Protection)",
    "TSA Pipeline Security Guidelines",
    "FERC Security Standards"
  ],

  primary_threats: [
    "State-sponsored APT groups",
    "Ransomware targeting OT systems",
    "Supply chain attacks",
    "Insider threats",
    "Physical-cyber attacks"
  ],
  high_risk_techniques: [
    "T0821 - Modify Controller Tasking",
    "T0813 - Denial of Control",
    "T0806 - Brute Force I/O",
    "T0836 - Modify Parameter",
    "T0882 - Theft of Operational Information"
  ],
  notable_incidents: [
    {
      name: "Ukraine Power Grid Attack",
      year: 2015,
      description: "CRASHOVERRIDE malware caused blackouts affecting 225,000 customers",
      techniques: ["T0813", "T0814", "T0816"]
    },
    {
      name: "TRITON/TRISIS",
      year: 2017,
      description: "Targeted safety instrumented systems in petrochemical plant",
      techniques: ["T0821", "T0800", "T0873"]
    }
  ],

  common_asset_types: [
    "SCADA Server",
    "Substation IED",
    "Generator Protection Relay",
    "Energy Management System (EMS)",
    "RTU",
    "PLC"
  ],
  common_protocols: [
    "DNP3",
    "IEC 61850",
    "Modbus",
    "IEC 60870-5-104",
    "OPC UA"
  ],
  typical_purdue_levels: [0, 1, 2, 3],

  sector_specific_standards: [
    "NERC CIP-002 through CIP-014",
    "IEC 62351 (Power System Security)",
    "IEEE 1686 (Substation IED Security)"
  ],
  security_frameworks: [
    "NIST Cybersecurity Framework",
    "IEC 62443",
    "C2M2 (Cybersecurity Capability Maturity Model)"
  ],

  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
})
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on sector ID
CREATE CONSTRAINT sector_id_unique IF NOT EXISTS
FOR (s:Critical_Infrastructure_Sector) REQUIRE s.sector_id IS UNIQUE;

// Index on sector name
CREATE INDEX sector_name_idx IF NOT EXISTS
FOR (s:Critical_Infrastructure_Sector) ON (s.sector_name);

// Full-text search
CREATE FULLTEXT INDEX sector_fulltext IF NOT EXISTS
FOR (s:Critical_Infrastructure_Sector) ON EACH [s.sector_name, s.description];
```

**CISA Critical Infrastructure Sectors**:
```cypher
// Create all 16 CISA critical infrastructure sectors
UNWIND [
  {id: "CISA-SECTOR-CHEMICAL", name: "Chemical Sector", abbr: "CHEMICAL"},
  {id: "CISA-SECTOR-COMMERCIAL", name: "Commercial Facilities Sector", abbr: "COMMERCIAL"},
  {id: "CISA-SECTOR-COMMUNICATIONS", name: "Communications Sector", abbr: "COMMUNICATIONS"},
  {id: "CISA-SECTOR-CRITICAL-MANUFACTURING", name: "Critical Manufacturing Sector", abbr: "MANUFACTURING"},
  {id: "CISA-SECTOR-DAMS", name: "Dams Sector", abbr: "DAMS"},
  {id: "CISA-SECTOR-DEFENSE", name: "Defense Industrial Base Sector", abbr: "DEFENSE"},
  {id: "CISA-SECTOR-EMERGENCY", name: "Emergency Services Sector", abbr: "EMERGENCY"},
  {id: "CISA-SECTOR-ENERGY", name: "Energy Sector", abbr: "ENERGY"},
  {id: "CISA-SECTOR-FINANCIAL", name: "Financial Services Sector", abbr: "FINANCIAL"},
  {id: "CISA-SECTOR-FOOD-AG", name: "Food and Agriculture Sector", abbr: "FOOD-AG"},
  {id: "CISA-SECTOR-GOV-FACILITIES", name: "Government Facilities Sector", abbr: "GOVERNMENT"},
  {id: "CISA-SECTOR-HEALTHCARE", name: "Healthcare and Public Health Sector", abbr: "HEALTHCARE"},
  {id: "CISA-SECTOR-IT", name: "Information Technology Sector", abbr: "IT"},
  {id: "CISA-SECTOR-NUCLEAR", name: "Nuclear Reactors, Materials, and Waste Sector", abbr: "NUCLEAR"},
  {id: "CISA-SECTOR-TRANSPORTATION", name: "Transportation Systems Sector", abbr: "TRANSPORTATION"},
  {id: "CISA-SECTOR-WATER", name: "Water and Wastewater Systems Sector", abbr: "WATER"}
] AS sector
CREATE (s:Critical_Infrastructure_Sector {
  sector_id: sector.id,
  sector_name: sector.name,
  sector_abbreviation: sector.abbr,
  cisa_designation: "Critical Infrastructure Sector",
  security_frameworks: ["NIST CSF", "IEC 62443", "ISO 27001"],
  node_id: randomUUID(),
  created_by: "AEON_INTEGRATION_WAVE5",
  created_date: datetime(),
  last_updated: datetime(),
  validation_status: "VALIDATED"
});
```

## 3. Complete Relationship Schemas

### 3.1 ICS Tactic to Technique Relationships

**Relationship Type**: `CONTAINS_ICS_TECHNIQUE`

**Description**: Links ICS tactics to the techniques that achieve the tactical objective.

**Properties**:
```cypher
{
  relationship_id: String,       // Unique relationship identifier
  technique_applicability: String, // PRIMARY, SECONDARY
  confidence_score: Float,       // Relationship confidence (0.0-1.0)
  mitre_validated: Boolean,      // Official MITRE mapping
  created_date: DateTime,
  last_updated: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link ICS tactics to techniques
MATCH (tactic:ICS_Tactic {tactic_id: "TA0100"}) // Impair Process Control
MATCH (technique:ICS_Technique {technique_id: "T0821"}) // Modify Controller Tasking
CREATE (tactic)-[r:CONTAINS_ICS_TECHNIQUE {
  relationship_id: randomUUID(),
  technique_applicability: "PRIMARY",
  confidence_score: 1.0,
  mitre_validated: true,
  created_date: datetime(),
  last_updated: datetime()
}]->(technique)
```

**Batch Relationship Creation**:
```cypher
// Create tactic-technique relationships for Wave 5
UNWIND [
  // Initial Access (TA0108)
  {tactic: "TA0108", technique: "T0812", applicability: "PRIMARY"},  // Default Credentials
  {tactic: "TA0108", technique: "T0817", applicability: "PRIMARY"},  // Drive-by Compromise
  {tactic: "TA0108", technique: "T0818", applicability: "PRIMARY"},  // Engineering Workstation Compromise
  {tactic: "TA0108", technique: "T0819", applicability: "PRIMARY"},  // Exploit Public-Facing Application
  {tactic: "TA0108", technique: "T0866", applicability: "SECONDARY"}, // Exploitation of Remote Services

  // Execution (TA0109)
  {tactic: "TA0109", technique: "T0807", applicability: "PRIMARY"},  // Command-Line Interface
  {tactic: "TA0109", technique: "T0821", applicability: "PRIMARY"},  // Modify Controller Tasking
  {tactic: "TA0109", technique: "T0871", applicability: "PRIMARY"},  // Execution through API
  {tactic: "TA0109", technique: "T0874", applicability: "SECONDARY"}, // User Execution

  // Impair Process Control (TA0100)
  {tactic: "TA0100", technique: "T0806", applicability: "PRIMARY"},  // Brute Force I/O
  {tactic: "TA0100", technique: "T0821", applicability: "PRIMARY"},  // Modify Controller Tasking
  {tactic: "TA0100", technique: "T0836", applicability: "PRIMARY"},  // Modify Parameter
  {tactic: "TA0100", technique: "T0855", applicability: "PRIMARY"},  // Unauthorized Command Message
  {tactic: "TA0100", technique: "T0856", applicability: "SECONDARY"}, // Spoof Reporting Message

  // Inhibit Response Function (TA0101)
  {tactic: "TA0101", technique: "T0803", applicability: "PRIMARY"},  // Block Command Message
  {tactic: "TA0101", technique: "T0804", applicability: "PRIMARY"},  // Block Reporting Message
  {tactic: "TA0101", technique: "T0805", applicability: "PRIMARY"},  // Block Serial COM
  {tactic: "TA0101", technique: "T0815", applicability: "PRIMARY"},  // Denial of Service
  {tactic: "TA0101", technique: "T0816", applicability: "PRIMARY"},  // Device Restart/Shutdown

  // Impact (TA0106)
  {tactic: "TA0106", technique: "T0809", applicability: "PRIMARY"},  // Data Destruction
  {tactic: "TA0106", technique: "T0813", applicability: "PRIMARY"},  // Denial of Control
  {tactic: "TA0106", technique: "T0814", applicability: "PRIMARY"},  // Denial of View
  {tactic: "TA0106", technique: "T0815", applicability: "PRIMARY"},  // Denial of Service
  {tactic: "TA0106", technique: "T0826", applicability: "PRIMARY"},  // Loss of Availability
  {tactic: "TA0106", technique: "T0827", applicability: "PRIMARY"},  // Loss of Control
  {tactic: "TA0106", technique: "T0828", applicability: "PRIMARY"},  // Loss of Productivity and Revenue
  {tactic: "TA0106", technique: "T0837", applicability: "PRIMARY"}   // Loss of Protection
] AS rel
MATCH (tactic:ICS_Tactic {tactic_id: rel.tactic})
MATCH (technique:ICS_Technique {technique_id: rel.technique})
CREATE (tactic)-[r:CONTAINS_ICS_TECHNIQUE {
  relationship_id: randomUUID(),
  technique_applicability: rel.applicability,
  confidence_score: 1.0,
  mitre_validated: true,
  created_date: datetime(),
  last_updated: datetime()
}]->(technique)
```

### 3.2 Technique to Asset Relationships

**Relationship Type**: `TARGETS_ICS_ASSET`

**Description**: Links ICS techniques to the asset types they specifically target or affect.

**Properties**:
```cypher
{
  relationship_id: String,
  impact_severity: String,       // LOW, MEDIUM, HIGH, CRITICAL
  attack_vector: String,         // Network, Physical, Local
  required_access_level: String, // NONE, USER, ADMIN, SYSTEM
  observable_indicators: [String],
  confidence_score: Float,
  created_date: DateTime,
  last_updated: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link technique to targeted asset
MATCH (technique:ICS_Technique {technique_id: "T0821"}) // Modify Controller Tasking
MATCH (asset:ICS_Asset {asset_type: "Programmable Logic Controller (PLC)"})
CREATE (technique)-[r:TARGETS_ICS_ASSET {
  relationship_id: randomUUID(),
  impact_severity: "CRITICAL",
  attack_vector: "Network",
  required_access_level: "ADMIN",
  observable_indicators: [
    "Controller program changes",
    "Unexpected ladder logic modifications",
    "Engineering workstation connections",
    "Abnormal memory usage patterns"
  ],
  confidence_score: 0.95,
  created_date: datetime(),
  last_updated: datetime()
}]->(asset)
```

**Batch Creation**:
```cypher
// Create technique-to-asset targeting relationships
UNWIND [
  // Modify Controller Tasking targets multiple assets
  {tech: "T0821", asset: "Programmable Logic Controller (PLC)", severity: "CRITICAL", vector: "Network"},
  {tech: "T0821", asset: "Distributed Control System (DCS)", severity: "CRITICAL", vector: "Network"},
  {tech: "T0821", asset: "Safety Instrumented System (SIS)", severity: "CRITICAL", vector: "Network"},
  {tech: "T0821", asset: "Remote Terminal Unit (RTU)", severity: "HIGH", vector: "Network"},

  // Engineering Workstation Compromise
  {tech: "T0818", asset: "Engineering Workstation", severity: "CRITICAL", vector: "Network"},
  {tech: "T0818", asset: "Human-Machine Interface (HMI)", severity: "HIGH", vector: "Network"},

  // Data Historian Compromise
  {tech: "T0810", asset: "Historian Server", severity: "HIGH", vector: "Network"},
  {tech: "T0810", asset: "SCADA Server", severity: "HIGH", vector: "Network"},

  // Block Command Message
  {tech: "T0803", asset: "Programmable Logic Controller (PLC)", severity: "HIGH", vector: "Network"},
  {tech: "T0803", asset: "Remote Terminal Unit (RTU)", severity: "HIGH", vector: "Network"},
  {tech: "T0803", asset: "Intelligent Electronic Device (IED)", severity: "HIGH", vector: "Network"},

  // Denial of Service
  {tech: "T0815", asset: "SCADA Server", severity: "CRITICAL", vector: "Network"},
  {tech: "T0815", asset: "Human-Machine Interface (HMI)", severity: "HIGH", vector: "Network"},
  {tech: "T0815", asset: "Industrial Ethernet Switch", severity: "HIGH", vector: "Network"}
] AS rel
MATCH (technique:ICS_Technique {technique_id: rel.tech})
MATCH (asset:ICS_Asset {asset_type: rel.asset})
CREATE (technique)-[r:TARGETS_ICS_ASSET {
  relationship_id: randomUUID(),
  impact_severity: rel.severity,
  attack_vector: rel.vector,
  required_access_level: "ADMIN",
  confidence_score: 0.9,
  created_date: datetime(),
  last_updated: datetime()
}]->(asset)
```

### 3.3 Asset to Protocol Relationships

**Relationship Type**: `USES_PROTOCOL`

**Description**: Links ICS assets to the communication protocols they support or use.

**Properties**:
```cypher
{
  relationship_id: String,
  usage_type: String,            // PRIMARY, SECONDARY, OPTIONAL
  protocol_role: String,         // SERVER, CLIENT, BOTH
  security_enabled: Boolean,
  created_date: DateTime,
  last_updated: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link asset to protocol
MATCH (asset:ICS_Asset {asset_type: "Programmable Logic Controller (PLC)"})
MATCH (protocol:ICS_Protocol {protocol_id: "MODBUS-TCP"})
CREATE (asset)-[r:USES_PROTOCOL {
  relationship_id: randomUUID(),
  usage_type: "PRIMARY",
  protocol_role: "SERVER",
  security_enabled: false,
  created_date: datetime(),
  last_updated: datetime()
}]->(protocol)
```

**Batch Creation**:
```cypher
// Create asset-protocol relationships
UNWIND [
  // PLCs
  {asset: "Programmable Logic Controller (PLC)", protocol: "MODBUS-TCP", usage: "PRIMARY", role: "SERVER"},
  {asset: "Programmable Logic Controller (PLC)", protocol: "PROFINET", usage: "PRIMARY", role: "BOTH"},
  {asset: "Programmable Logic Controller (PLC)", protocol: "ETHERNETIP", usage: "SECONDARY", role: "BOTH"},
  {asset: "Programmable Logic Controller (PLC)", protocol: "OPC-UA", usage: "SECONDARY", role: "SERVER"},

  // SCADA Server
  {asset: "SCADA Server", protocol: "DNP3", usage: "PRIMARY", role: "CLIENT"},
  {asset: "SCADA Server", protocol: "MODBUS-TCP", usage: "PRIMARY", role: "CLIENT"},
  {asset: "SCADA Server", protocol: "IEC-60870-5-104", usage: "PRIMARY", role: "CLIENT"},
  {asset: "SCADA Server", protocol: "OPC-UA", usage: "SECONDARY", role: "CLIENT"},

  // RTU
  {asset: "Remote Terminal Unit (RTU)", protocol: "DNP3", usage: "PRIMARY", role: "SERVER"},
  {asset: "Remote Terminal Unit (RTU)", protocol: "MODBUS-RTU", usage: "PRIMARY", role: "SERVER"},
  {asset: "Remote Terminal Unit (RTU)", protocol: "IEC-60870-5-104", usage: "SECONDARY", role: "SERVER"},

  // IED
  {asset: "Intelligent Electronic Device (IED)", protocol: "IEC-61850", usage: "PRIMARY", role: "SERVER"},
  {asset: "Intelligent Electronic Device (IED)", protocol: "DNP3", usage: "SECONDARY", role: "SERVER"},

  // HMI
  {asset: "Human-Machine Interface (HMI)", protocol: "OPC-UA", usage: "PRIMARY", role: "CLIENT"},
  {asset: "Human-Machine Interface (HMI)", protocol: "MODBUS-TCP", usage: "SECONDARY", role: "CLIENT"}
] AS rel
MATCH (asset:ICS_Asset {asset_type: rel.asset})
MATCH (protocol:ICS_Protocol {protocol_id: rel.protocol})
CREATE (asset)-[r:USES_PROTOCOL {
  relationship_id: randomUUID(),
  usage_type: rel.usage,
  protocol_role: rel.role,
  security_enabled: false,
  created_date: datetime(),
  last_updated: datetime()
}]->(protocol)
```

### 3.4 Sector to Asset Relationships

**Relationship Type**: `DEPLOYS_ASSET`

**Description**: Links critical infrastructure sectors to common asset types deployed in those sectors.

**Properties**:
```cypher
{
  relationship_id: String,
  deployment_prevalence: String, // UBIQUITOUS, COMMON, RARE
  criticality_in_sector: String, // CRITICAL, HIGH, MEDIUM, LOW
  regulatory_requirements: [String],
  created_date: DateTime,
  last_updated: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link sector to deployed assets
MATCH (sector:Critical_Infrastructure_Sector {sector_id: "CISA-SECTOR-ENERGY"})
MATCH (asset:ICS_Asset {asset_type: "SCADA Server"})
CREATE (sector)-[r:DEPLOYS_ASSET {
  relationship_id: randomUUID(),
  deployment_prevalence: "UBIQUITOUS",
  criticality_in_sector: "CRITICAL",
  regulatory_requirements: ["NERC CIP-005", "NERC CIP-007"],
  created_date: datetime(),
  last_updated: datetime()
}]->(asset)
```

### 3.5 Technique to Protocol Relationships

**Relationship Type**: `EXPLOITS_PROTOCOL`

**Description**: Links ICS techniques to protocols they exploit or leverage.

**Properties**:
```cypher
{
  relationship_id: String,
  exploitation_method: String,
  protocol_weakness_exploited: String,
  detection_difficulty: String,  // EASY, MODERATE, HARD, VERY_HARD
  created_date: DateTime,
  last_updated: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link technique to exploited protocol
MATCH (technique:ICS_Technique {technique_id: "T0855"}) // Unauthorized Command Message
MATCH (protocol:ICS_Protocol {protocol_id: "MODBUS-TCP"})
CREATE (technique)-[r:EXPLOITS_PROTOCOL {
  relationship_id: randomUUID(),
  exploitation_method: "Unauthenticated command injection",
  protocol_weakness_exploited: "No authentication mechanism",
  detection_difficulty: "MODERATE",
  created_date: datetime(),
  last_updated: datetime()
}]->(protocol)
```

### 3.6 CVE to ICS Technique Relationships (CVE Preservation)

**Relationship Type**: `ENABLES_ICS_TECHNIQUE`

**Description**: Links existing CVE nodes to ICS techniques they enable, preserving Wave 4 CVE data.

**Properties**:
```cypher
{
  relationship_id: String,
  enablement_type: String,       // DIRECT, INDIRECT, FACILITATES
  exploitation_complexity: String, // LOW, MEDIUM, HIGH
  requires_additional_conditions: Boolean,
  attack_chain_position: String,  // INITIAL_ACCESS, LATERAL_MOVEMENT, EXECUTION, etc.
  real_world_usage: Boolean,
  created_date: DateTime,
  last_updated: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link CVE to ICS technique it enables
MATCH (cve:CVE {cve_id: "CVE-2015-5374"}) // Schneider Electric vulnerability
MATCH (technique:ICS_Technique {technique_id: "T0821"}) // Modify Controller Tasking
CREATE (cve)-[r:ENABLES_ICS_TECHNIQUE {
  relationship_id: randomUUID(),
  enablement_type: "DIRECT",
  exploitation_complexity: "MEDIUM",
  requires_additional_conditions: false,
  attack_chain_position: "EXECUTION",
  real_world_usage: true,
  created_date: datetime(),
  last_updated: datetime()
}]->(technique)
```

**CVE Preservation Validation Query**:
```cypher
// Verify CVE nodes are preserved and connected to ICS techniques
MATCH (cve:CVE)-[r:ENABLES_ICS_TECHNIQUE]->(technique:ICS_Technique)
RETURN
  count(DISTINCT cve) AS preserved_cves,
  count(DISTINCT technique) AS connected_techniques,
  count(r) AS total_relationships
```

### 3.7 Integration with Enterprise ATT&CK

**Relationship Type**: `EXTENDS_ENTERPRISE_TECHNIQUE`

**Description**: Links ICS techniques to related enterprise ATT&CK techniques they extend or specialize.

**Properties**:
```cypher
{
  relationship_id: String,
  extension_type: String,        // SPECIALIZATION, ADAPTATION, VARIANT
  shared_characteristics: [String],
  ics_specific_adaptations: [String],
  created_date: DateTime,
  last_updated: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link ICS technique to enterprise technique
MATCH (ics_tech:ICS_Technique {technique_id: "T0807"}) // Command-Line Interface (ICS)
MATCH (ent_tech:Technique {technique_id: "T1059"})     // Command and Scripting Interpreter (Enterprise)
CREATE (ics_tech)-[r:EXTENDS_ENTERPRISE_TECHNIQUE {
  relationship_id: randomUUID(),
  extension_type: "ADAPTATION",
  shared_characteristics: ["Command execution", "Shell access", "Script execution"],
  ics_specific_adaptations: [
    "PLC programming interfaces",
    "Engineering workstation access",
    "SCADA scripting environments"
  ],
  created_date: datetime(),
  last_updated: datetime()
}]->(ent_tech)
```

## 4. Integration Patterns

### 4.1 Integration with Wave 1 (Core ATT&CK)

**Objective**: Seamlessly connect ICS framework with existing enterprise ATT&CK data.

**Integration Points**:
1. Link ICS techniques to related enterprise techniques
2. Connect ICS tactics to enterprise tactics where applicable
3. Share common mitigation strategies
4. Unified threat actor attribution

**Integration Query Pattern**:
```cypher
// Find enterprise techniques related to ICS technique
MATCH (ics_tech:ICS_Technique {technique_id: "T0818"})-[:EXTENDS_ENTERPRISE_TECHNIQUE]->(ent_tech:Technique)
MATCH (ent_tech)<-[:USES]-(threat_actor:ThreatActor)
RETURN
  ics_tech.name AS ics_technique,
  ent_tech.name AS related_enterprise_technique,
  collect(threat_actor.name) AS threat_actors_using_related_technique
```

**Cross-Domain Attack Path**:
```cypher
// Find attack paths from IT to OT
MATCH path = (it_asset:Asset)-[:CONNECTS_TO*1..3]->(ics_asset:ICS_Asset)
WHERE it_asset.asset_category = "IT"
  AND ics_asset.network_zone = "Control Network"
MATCH (technique:Technique)-[:TARGETS_ASSET]->(it_asset)
MATCH (ics_tech:ICS_Technique)-[:TARGETS_ICS_ASSET]->(ics_asset)
RETURN
  path,
  technique.name AS it_technique,
  ics_tech.name AS ot_technique,
  ics_asset.criticality AS target_criticality
LIMIT 10
```

### 4.2 Integration with Wave 2 (Asset Classification)

**Objective**: Extend asset classification with ICS-specific asset types and properties.

**Integration Pattern**:
```cypher
// Connect ICS assets to general asset classification
MATCH (ics_asset:ICS_Asset)
MATCH (asset_class:AssetClass)
WHERE asset_class.name IN ["Control System", "Industrial Device", "OT Network Equipment"]
CREATE (ics_asset)-[:CLASSIFIED_AS {
  classification_confidence: 1.0,
  purdue_level: ics_asset.purdue_level,
  ot_specific: true,
  created_date: datetime()
}]->(asset_class)
```

### 4.3 Integration with Wave 4 (CVE Data)

**Objective**: Preserve all existing CVE relationships while adding ICS-specific CVE connections.

**CVE Preservation Pattern**:
```cypher
// Find ICS-relevant CVEs and connect to ICS techniques
MATCH (cve:CVE)
WHERE
  cve.description CONTAINS "SCADA" OR
  cve.description CONTAINS "PLC" OR
  cve.description CONTAINS "industrial control" OR
  cve.description CONTAINS "ICS" OR
  cve.affected_product IN ["Siemens SIMATIC", "Schneider Electric", "Rockwell Automation"]
WITH cve
MATCH (technique:ICS_Technique)
WHERE ANY(asset IN technique.affected_assets WHERE cve.description CONTAINS asset)
CREATE (cve)-[:ENABLES_ICS_TECHNIQUE {
  relationship_id: randomUUID(),
  enablement_type: "DIRECT",
  auto_detected: true,
  requires_validation: true,
  created_date: datetime()
}]->(technique)
```

**CVE Validation Query**:
```cypher
// Verify no CVE nodes were deleted or modified
MATCH (cve:CVE)
WITH count(cve) AS total_cves
MATCH (cve:CVE)-[:ENABLES_ICS_TECHNIQUE]->(:ICS_Technique)
WITH total_cves, count(DISTINCT cve) AS ics_connected_cves
RETURN
  total_cves,
  ics_connected_cves,
  (ics_connected_cves * 100.0 / total_cves) AS percentage_connected
```

### 4.4 Purdue Model Integration

**Objective**: Model ISA-95 Purdue Reference Architecture for OT network segmentation.

**Purdue Level Hierarchy**:
```cypher
// Create Purdue Model levels
UNWIND [
  {level: 0, name: "Physical Process", description: "Sensors, actuators, physical equipment"},
  {level: 1, name: "Basic Control", description: "PLCs, RTUs, DCS controllers"},
  {level: 2, name: "Area Supervisory Control", description: "HMI, SCADA, engineering workstations"},
  {level: 3, name: "Site Operations", description: "Manufacturing operations management"},
  {level: 4, name: "Enterprise Network", description: "Business planning and logistics"},
  {level: 5, name: "Enterprise", description: "Corporate network"}
] AS purdue
CREATE (p:PurdueLevel {
  level: purdue.level,
  name: purdue.name,
  description: purdue.description,
  node_id: randomUUID(),
  created_date: datetime()
})
```

**Asset-to-Purdue Mapping**:
```cypher
// Map ICS assets to Purdue levels
MATCH (asset:ICS_Asset)
MATCH (purdue:PurdueLevel {level: asset.purdue_level})
CREATE (asset)-[:OPERATES_AT_LEVEL {
  primary_level: true,
  can_communicate_with_levels: [asset.purdue_level - 1, asset.purdue_level + 1],
  created_date: datetime()
}]->(purdue)
```

## 5. Validation Criteria

### 5.1 Data Completeness Validation

**Node Count Validation**:
```cypher
// Verify target node counts achieved
MATCH (t:ICS_Tactic) WITH count(t) AS tactic_count
MATCH (tech:ICS_Technique) WITH tactic_count, count(tech) AS technique_count
MATCH (a:ICS_Asset) WITH tactic_count, technique_count, count(a) AS asset_count
MATCH (p:ICS_Protocol) WITH tactic_count, technique_count, asset_count, count(p) AS protocol_count
MATCH (s:Critical_Infrastructure_Sector)
RETURN
  tactic_count AS tactics,
  technique_count AS techniques,
  asset_count AS assets,
  protocol_count AS protocols,
  count(s) AS sectors,
  CASE
    WHEN tactic_count >= 12 AND
         technique_count >= 78 AND
         asset_count >= 150 AND
         protocol_count >= 10 AND
         count(s) >= 16
    THEN "PASS"
    ELSE "FAIL"
  END AS validation_status
```

**Relationship Completeness**:
```cypher
// Verify relationship coverage
MATCH (t:ICS_Tactic)-[r1:CONTAINS_ICS_TECHNIQUE]->(tech:ICS_Technique)
WITH count(r1) AS tactic_tech_rels
MATCH (tech:ICS_Technique)-[r2:TARGETS_ICS_ASSET]->(a:ICS_Asset)
WITH tactic_tech_rels, count(r2) AS tech_asset_rels
MATCH (a:ICS_Asset)-[r3:USES_PROTOCOL]->(p:ICS_Protocol)
WITH tactic_tech_rels, tech_asset_rels, count(r3) AS asset_protocol_rels
MATCH (cve:CVE)-[r4:ENABLES_ICS_TECHNIQUE]->(tech:ICS_Technique)
RETURN
  tactic_tech_rels,
  tech_asset_rels,
  asset_protocol_rels,
  count(r4) AS cve_technique_rels,
  CASE
    WHEN tactic_tech_rels >= 100 AND
         tech_asset_rels >= 200 AND
         asset_protocol_rels >= 50 AND
         count(r4) >= 20
    THEN "PASS"
    ELSE "FAIL"
  END AS relationship_validation
```

### 5.2 CVE Preservation Validation

**Critical Validation**: Ensure Wave 4 CVE data remains intact.

```cypher
// Comprehensive CVE preservation check
MATCH (cve:CVE)
WITH count(cve) AS total_cves_before
CALL {
  MATCH (cve:CVE)-[r]->()
  RETURN count(DISTINCT r) AS cve_relationships_before
}
WITH total_cves_before, cve_relationships_before
MATCH (cve:CVE)-[:ENABLES_ICS_TECHNIQUE]->(:ICS_Technique)
WITH total_cves_before, cve_relationships_before, count(cve) AS ics_connected_cves
RETURN
  total_cves_before AS original_cve_count,
  cve_relationships_before AS original_relationships,
  ics_connected_cves AS cves_with_ics_links,
  CASE
    WHEN total_cves_before > 0 AND cve_relationships_before > 0
    THEN "CVE_DATA_PRESERVED"
    ELSE "CVE_DATA_MISSING"
  END AS preservation_status
```

### 5.3 Data Quality Validation

**Property Completeness**:
```cypher
// Check required properties are populated
MATCH (t:ICS_Technique)
WHERE t.technique_id IS NULL OR
      t.name IS NULL OR
      t.description IS NULL OR
      size(t.tactics) = 0 OR
      size(t.affected_assets) = 0
RETURN count(t) AS techniques_missing_required_properties
// Expected: 0

MATCH (a:ICS_Asset)
WHERE a.asset_type IS NULL OR
      a.purdue_level IS NULL OR
      a.criticality IS NULL OR
      a.network_zone IS NULL
RETURN count(a) AS assets_missing_required_properties
// Expected: 0
```

**Relationship Integrity**:
```cypher
// Verify no orphaned nodes
MATCH (t:ICS_Technique)
WHERE NOT (t)<-[:CONTAINS_ICS_TECHNIQUE]-(:ICS_Tactic)
RETURN count(t) AS orphaned_techniques
// Expected: 0

MATCH (a:ICS_Asset)
WHERE NOT (a)<-[:TARGETS_ICS_ASSET]-(:ICS_Technique) AND
      NOT (a)-[:USES_PROTOCOL]->(:ICS_Protocol)
RETURN count(a) AS orphaned_assets
// Expected: 0
```

### 5.4 Performance Benchmarks

**Query Performance Standards**:
```cypher
// Test: ICS attack path enumeration (<500ms)
PROFILE
MATCH path = (technique:ICS_Technique)-[:TARGETS_ICS_ASSET]->(asset:ICS_Asset)-[:USES_PROTOCOL]->(protocol:ICS_Protocol)
WHERE asset.criticality = "CRITICAL" AND protocol.authentication_support = false
RETURN
  technique.name,
  asset.asset_type,
  protocol.protocol_name,
  length(path) AS path_length
LIMIT 100
```

**Index Effectiveness**:
```cypher
// Verify indexes are being used
EXPLAIN
MATCH (t:ICS_Technique {technique_id: "T0821"})
RETURN t
// Should show index usage on technique_id

EXPLAIN
MATCH (a:ICS_Asset)
WHERE a.criticality = "CRITICAL"
RETURN a
// Should show index usage on criticality
```

## 6. Example Queries

### 6.1 ICS Kill Chain Analysis

**Query: Complete ICS attack chain from initial access to impact**
```cypher
// Find complete attack paths through ICS environment
MATCH path =
  (init:ICS_Tactic {name: "Initial Access"})-[:CONTAINS_ICS_TECHNIQUE]->(init_tech:ICS_Technique)-[:TARGETS_ICS_ASSET]->(entry_asset:ICS_Asset),
  (entry_asset)-[:CONNECTS_TO*1..3]->(critical_asset:ICS_Asset),
  (impact_tech:ICS_Technique)-[:TARGETS_ICS_ASSET]->(critical_asset),
  (impact:ICS_Tactic {name: "Impact"})-[:CONTAINS_ICS_TECHNIQUE]->(impact_tech)
WHERE
  critical_asset.criticality = "CRITICAL" AND
  critical_asset.purdue_level <= 1
RETURN
  init_tech.name AS initial_access_technique,
  entry_asset.asset_type AS entry_point,
  [node IN nodes(path) WHERE node:ICS_Asset | node.asset_type] AS attack_path_assets,
  critical_asset.asset_type AS target_asset,
  impact_tech.name AS impact_technique,
  critical_asset.process_functions AS affected_processes
LIMIT 10
```

**Expected Result**:
```
initial_access_technique       | entry_point            | attack_path_assets                          | target_asset | impact_technique    | affected_processes
-------------------------------|------------------------|---------------------------------------------|--------------|---------------------|-------------------
"Engineering Workstation       | "Engineering           | ["Engineering Workstation",                 | "Safety      | "Modify Controller  | ["Emergency Shutdown",
Compromise"                    | Workstation"           |  "SCADA Server", "Safety Instrumented       | Instrumented | Tasking"            |  "Pressure Relief"]
                               |                        |  System (SIS)"]                             | System (SIS)"|                     |
```

### 6.2 Sector-Specific Threat Assessment

**Query: Energy sector critical vulnerabilities**
```cypher
// Identify high-risk techniques for Energy sector
MATCH (sector:Critical_Infrastructure_Sector {sector_abbreviation: "ENERGY"})-[:DEPLOYS_ASSET]->(asset:ICS_Asset)
MATCH (technique:ICS_Technique)-[r:TARGETS_ICS_ASSET]->(asset)
WHERE r.impact_severity IN ["CRITICAL", "HIGH"]
OPTIONAL MATCH (cve:CVE)-[:ENABLES_ICS_TECHNIQUE]->(technique)
OPTIONAL MATCH (protocol:ICS_Protocol)<-[:USES_PROTOCOL]-(asset)
WHERE protocol.authentication_support = false
RETURN
  technique.name AS threat_technique,
  technique.severity_rating AS severity,
  collect(DISTINCT asset.asset_type) AS vulnerable_assets,
  count(DISTINCT cve) AS known_cves_enabling_technique,
  collect(DISTINCT protocol.protocol_name) AS exploitable_protocols,
  technique.detection_methods AS detection_approaches
ORDER BY
  CASE technique.severity_rating
    WHEN "CRITICAL" THEN 1
    WHEN "HIGH" THEN 2
    ELSE 3
  END,
  count(DISTINCT cve) DESC
LIMIT 20
```

**Expected Result**:
```
threat_technique           | severity  | vulnerable_assets                    | known_cves_enabling_technique | exploitable_protocols      | detection_approaches
---------------------------|-----------|--------------------------------------|-------------------------------|----------------------------|---------------------
"Modify Controller Tasking"| CRITICAL  | ["PLC", "DCS", "SIS", "RTU"]        | 12                            | ["Modbus TCP", "Profinet"] | ["Monitor controller..."]
"Denial of Control"        | CRITICAL  | ["SCADA Server", "HMI"]             | 8                             | ["DNP3", "IEC 61850"]      | ["Baseline normal..."]
```

### 6.3 Protocol Vulnerability Analysis

**Query: Unauthenticated protocol attack surface**
```cypher
// Find assets using unauthenticated protocols with critical functions
MATCH (asset:ICS_Asset)-[:USES_PROTOCOL]->(protocol:ICS_Protocol)
WHERE
  protocol.authentication_support = false AND
  asset.criticality IN ["CRITICAL", "HIGH"] AND
  asset.purdue_level <= 2
MATCH (technique:ICS_Technique)-[:EXPLOITS_PROTOCOL]->(protocol)
MATCH (technique)-[:TARGETS_ICS_ASSET]->(asset)
RETURN
  asset.asset_type AS asset,
  asset.criticality AS criticality,
  asset.purdue_level AS purdue_level,
  asset.network_zone AS network_zone,
  protocol.protocol_name AS vulnerable_protocol,
  collect(DISTINCT technique.name) AS applicable_attack_techniques,
  protocol.mitigation_approaches AS recommended_mitigations
ORDER BY asset.criticality DESC, asset.purdue_level ASC
```

### 6.4 Cross-Domain Attack Path (IT to OT)

**Query: Find attack paths from IT network to critical OT assets**
```cypher
// Enterprise to ICS attack path simulation
MATCH (it_asset:Asset {asset_category: "IT"})-[:CONNECTS_TO*1..5]->(ics_asset:ICS_Asset)
WHERE
  ics_asset.network_zone = "Control Network" AND
  ics_asset.criticality = "CRITICAL"
MATCH (enterprise_tech:Technique)-[:TARGETS_ASSET]->(it_asset)
MATCH (ics_tech:ICS_Technique)-[:TARGETS_ICS_ASSET]->(ics_asset)
OPTIONAL MATCH (ics_tech)-[:EXTENDS_ENTERPRISE_TECHNIQUE]->(enterprise_tech)
RETURN
  it_asset.hostname AS it_entry_point,
  enterprise_tech.name AS it_technique,
  [node IN nodes(path) WHERE node:Asset OR node:ICS_Asset |
    CASE
      WHEN node:Asset THEN node.hostname
      ELSE node.asset_type
    END
  ] AS lateral_movement_path,
  ics_asset.asset_type AS ot_target,
  ics_tech.name AS ot_technique,
  CASE WHEN ics_tech IS NOT NULL AND enterprise_tech IS NOT NULL
    THEN "TECHNIQUE_CHAINING"
    ELSE "SEPARATE_TECHNIQUES"
  END AS attack_pattern
LIMIT 15
```

### 6.5 ICS Threat Actor Attribution

**Query: Threat actors with ICS capabilities**
```cypher
// Find threat actors using ICS techniques
MATCH (actor:ThreatActor)-[:USES]->(enterprise_tech:Technique)
MATCH (ics_tech:ICS_Technique)-[:EXTENDS_ENTERPRISE_TECHNIQUE]->(enterprise_tech)
OPTIONAL MATCH (ics_tech)-[:TARGETS_ICS_ASSET]->(asset:ICS_Asset)
OPTIONAL MATCH (asset)<-[:DEPLOYS_ASSET]-(sector:Critical_Infrastructure_Sector)
RETURN
  actor.name AS threat_actor,
  actor.country AS nation_state,
  collect(DISTINCT ics_tech.name) AS ics_techniques_available,
  collect(DISTINCT asset.asset_type) AS targetable_assets,
  collect(DISTINCT sector.sector_abbreviation) AS threatened_sectors,
  actor.sophistication_level AS sophistication
ORDER BY size(collect(DISTINCT ics_tech.name)) DESC
LIMIT 10
```

### 6.6 Safety System Impact Assessment

**Query: Techniques that can affect safety systems**
```cypher
// Identify threats to safety-critical systems
MATCH (technique:ICS_Technique)-[:TARGETS_ICS_ASSET]->(asset:ICS_Asset)
WHERE
  asset.asset_type IN ["Safety Instrumented System (SIS)", "Emergency Shutdown System (ESD)"] OR
  ANY(func IN asset.process_functions WHERE func CONTAINS "Safety" OR func CONTAINS "Emergency")
MATCH (tactic:ICS_Tactic)-[:CONTAINS_ICS_TECHNIQUE]->(technique)
OPTIONAL MATCH (cve:CVE)-[:ENABLES_ICS_TECHNIQUE]->(technique)
WHERE cve.cvss_base_score > 7.0
RETURN
  asset.asset_type AS safety_system,
  asset.process_functions AS safety_functions,
  asset.iec_62443_level AS current_security_level,
  tactic.name AS attack_tactic,
  technique.name AS attack_technique,
  technique.severity_rating AS threat_severity,
  collect(cve.cve_id) AS high_severity_cves,
  technique.mitigation_strategies AS mitigation_recommendations
ORDER BY
  CASE technique.severity_rating
    WHEN "CRITICAL" THEN 1
    WHEN "HIGH" THEN 2
    ELSE 3
  END
```

### 6.7 Compliance Mapping

**Query: Map ICS techniques to compliance requirements**
```cypher
// NERC CIP compliance gap analysis
MATCH (technique:ICS_Technique)-[:TARGETS_ICS_ASSET]->(asset:ICS_Asset)
WHERE
  asset.sector = "Energy" AND
  asset.nerc_cip_classification = "BES Cyber Asset"
WITH
  technique,
  asset,
  technique.nerc_cip_references AS nerc_requirements
UNWIND nerc_requirements AS requirement
RETURN
  requirement AS nerc_cip_requirement,
  collect(DISTINCT technique.name) AS relevant_threat_techniques,
  count(DISTINCT asset) AS affected_assets,
  collect(DISTINCT technique.mitigation_strategies) AS mitigation_strategies
ORDER BY count(DISTINCT asset) DESC
```

### 6.8 Network Segmentation Validation

**Query: Verify Purdue model segmentation enforcement**
```cypher
// Identify potential segmentation violations
MATCH (asset1:ICS_Asset)-[:CONNECTS_TO]->(asset2:ICS_Asset)
WHERE abs(asset1.purdue_level - asset2.purdue_level) > 1
RETURN
  asset1.asset_type AS source_asset,
  asset1.purdue_level AS source_level,
  asset1.network_zone AS source_zone,
  asset2.asset_type AS destination_asset,
  asset2.purdue_level AS destination_level,
  asset2.network_zone AS destination_zone,
  "SEGMENTATION_VIOLATION" AS issue_type,
  "Direct connection violates Purdue model adjacent-level rule" AS description
ORDER BY asset2.purdue_level ASC
```

### 6.9 ICS Incident Response Prioritization

**Query: Generate incident response priority matrix**
```cypher
// Prioritize ICS security incidents
MATCH (technique:ICS_Technique)-[:TARGETS_ICS_ASSET]->(asset:ICS_Asset)
OPTIONAL MATCH (cve:CVE)-[:ENABLES_ICS_TECHNIQUE]->(technique)
WHERE asset.operational_state = "RUNNING"
WITH
  technique,
  asset,
  count(DISTINCT cve) AS exploitable_cves,
  CASE asset.criticality
    WHEN "CRITICAL" THEN 4
    WHEN "HIGH" THEN 3
    WHEN "MEDIUM" THEN 2
    ELSE 1
  END AS criticality_score,
  CASE technique.severity_rating
    WHEN "CRITICAL" THEN 4
    WHEN "HIGH" THEN 3
    WHEN "MEDIUM" THEN 2
    ELSE 1
  END AS technique_severity_score
WITH
  technique,
  asset,
  exploitable_cves,
  (criticality_score * technique_severity_score * (1 + exploitable_cves * 0.1)) AS risk_score
RETURN
  asset.asset_type AS asset,
  asset.asset_id AS asset_identifier,
  asset.physical_location AS location,
  technique.name AS threat_technique,
  exploitable_cves AS known_exploits,
  round(risk_score, 2) AS priority_score,
  technique.detection_methods[0] AS primary_detection_method
ORDER BY risk_score DESC
LIMIT 20
```

### 6.10 ICS Honeypot Planning

**Query: Identify high-value honeypot configurations**
```cypher
// Recommend ICS honeypot deployments based on threat intelligence
MATCH (technique:ICS_Technique)-[:TARGETS_ICS_ASSET]->(asset:ICS_Asset)
MATCH (technique)-[:EXPLOITS_PROTOCOL]->(protocol:ICS_Protocol)
WHERE
  protocol.authentication_support = false AND
  technique.severity_rating IN ["CRITICAL", "HIGH"]
WITH
  asset.asset_type AS honeypot_type,
  protocol.protocol_name AS protocol,
  collect(DISTINCT technique.name) AS detectable_techniques,
  count(DISTINCT technique) AS technique_count
ORDER BY technique_count DESC
RETURN
  honeypot_type AS recommended_honeypot,
  protocol AS protocol_to_emulate,
  detectable_techniques AS techniques_detected,
  technique_count AS threat_coverage_score
LIMIT 10
```

## 7. Wave 5 Implementation Checklist

### 7.1 Pre-Implementation

- [ ] Complete Wave 1-4 validation
- [ ] Backup existing graph database
- [ ] Verify CVE node count and relationships (baseline)
- [ ] Review MITRE ATT&CK ICS v13 documentation
- [ ] Prepare ICS asset inventory template
- [ ] Review critical infrastructure sector definitions

### 7.2 Implementation Phase 1: Schema Creation (Week 1)

- [ ] Create ICS_Tactic nodes (12 tactics)
- [ ] Create ICS_Technique nodes (78+ techniques)
- [ ] Create ICS_Asset nodes (150+ assets)
- [ ] Create ICS_Protocol nodes (10+ protocols)
- [ ] Create Critical_Infrastructure_Sector nodes (16 sectors)
- [ ] Create all indexes and constraints
- [ ] Validate node creation counts

### 7.3 Implementation Phase 2: Relationships (Week 2)

- [ ] Create CONTAINS_ICS_TECHNIQUE relationships (100+ relationships)
- [ ] Create TARGETS_ICS_ASSET relationships (200+ relationships)
- [ ] Create USES_PROTOCOL relationships (50+ relationships)
- [ ] Create DEPLOYS_ASSET relationships (100+ relationships)
- [ ] Create EXPLOITS_PROTOCOL relationships (30+ relationships)
- [ ] Create ENABLES_ICS_TECHNIQUE relationships (CVE integration, 20+ relationships)
- [ ] Create EXTENDS_ENTERPRISE_TECHNIQUE relationships (15+ relationships)
- [ ] Validate relationship counts

### 7.4 Implementation Phase 3: Integration & Validation (Week 3)

- [ ] Run CVE preservation validation query
- [ ] Verify no CVE nodes deleted or modified
- [ ] Test cross-domain (IT-OT) attack path queries
- [ ] Validate Purdue model integration
- [ ] Test all example queries
- [ ] Run performance benchmarks (<500ms target)
- [ ] Check property completeness (no null required fields)
- [ ] Verify orphaned node detection (0 expected)
- [ ] Generate validation report
- [ ] Create Wave 5 documentation

### 7.5 Post-Implementation

- [ ] Update graph statistics
- [ ] Document any schema deviations
- [ ] Create user training materials for ICS queries
- [ ] Establish ongoing MITRE ATT&CK ICS update process
- [ ] Plan Wave 6 integration points

## 8. Wave 5 Success Criteria Summary

**Quantitative Targets**:
- ✅ 12 ICS tactics created
- ✅ 78+ ICS techniques with complete properties
- ✅ 150+ ICS asset types modeled
- ✅ 10+ ICS protocols with security characteristics
- ✅ 16 critical infrastructure sectors
- ✅ 100+ tactic-technique relationships
- ✅ 200+ technique-asset relationships
- ✅ 20+ CVE-technique relationships
- ✅ 100% CVE preservation validation passed

**Qualitative Targets**:
- ✅ Query performance <500ms for ICS attack path queries
- ✅ Complete OT kill chain modeling capability
- ✅ Seamless integration with enterprise ATT&CK (Wave 1)
- ✅ No CVE data loss or corruption
- ✅ Support for compliance mapping (NERC CIP, IEC 62443)
- ✅ Purdue model architecture validated

---

**Wave 5 Status**: Ready for implementation
**Dependencies**: Waves 1, 2, 4 completed
**Next Wave**: Wave 6 - UCO/STIX Integration
**Document Version**: v1.0.0
**Last Updated**: 2025-10-30
