# Wave 6: UCO (Unified Cyber Ontology) and STIX 2.1 Integration

**File**: 08_WAVE_6_UCO_STIX.md
**Created**: 2025-10-30
**Version**: v1.0.0
**Status**: ACTIVE
**Wave Duration**: 4 weeks
**Target Node Count**: ~600 nodes
**Dependencies**: Waves 1-5 (Core ATT&CK, Assets, CVE, ICS)

## 1. Wave Overview

### 1.1 Objectives

Wave 6 integrates the AEON Digital Twin cybersecurity knowledge graph with two critical cyber threat intelligence standards: Unified Cyber Ontology (UCO) and STIX 2.1 (Structured Threat Information Expression). This integration enables standardized threat intelligence sharing, cyber forensics investigation support, and interoperability with external threat intelligence platforms.

**Primary Goals**:
- Implement UCO core ontology for cyber investigation and forensics
- Integrate STIX 2.1 objects for threat intelligence exchange
- Enable bidirectional conversion between Neo4j graph and STIX bundles
- Support cyber investigation case management workflows
- Preserve all existing graph data (CVEs, ATT&CK techniques, ICS assets)
- Enable automated threat intelligence ingestion from TAXII servers
- Support cyber forensics evidence chain of custody

**Business Value**:
- Standards-compliant threat intelligence sharing with partners and ISACs
- Automated threat intelligence platform (TIP) integration
- Cyber forensics investigation support with evidence provenance
- Regulatory compliance (GDPR, NIST 800-61 incident response)
- Supply chain risk intelligence sharing
- Multi-organization threat intelligence collaboration

### 1.2 Scope Definition

**In Scope**:

**UCO Components**:
- Core observable objects (files, network connections, processes, accounts)
- Investigation case management (cases, investigations, traces)
- Provenance tracking (actions, relationships, tools)
- Evidence chain of custody
- Digital forensics artifacts
- Cyber-physical event correlation

**STIX 2.1 Components**:
- STIX Domain Objects (SDOs): Attack Pattern, Campaign, Course of Action, Grouping, Identity, Indicator, Infrastructure, Intrusion Set, Malware, Note, Observed Data, Opinion, Report, Threat Actor, Tool, Vulnerability
- STIX Cyber-observable Objects (SCOs): Artifact, Autonomous System, Directory, Domain Name, Email Address, Email Message, File, IPv4/IPv6 Address, MAC Address, Mutex, Network Traffic, Process, Software, URL, User Account, Windows Registry Key, X.509 Certificate
- STIX Relationship Objects (SROs): Relationship, Sighting
- STIX bundle import/export functionality
- TAXII 2.1 client integration

**Integration Points**:
- Map MITRE ATT&CK techniques to STIX Attack Patterns
- Map CVEs to STIX Vulnerability objects
- Map ICS assets to STIX Infrastructure objects
- Map threat actors to STIX Threat Actor objects
- Connect UCO observables to STIX cyber-observables

**Out of Scope**:
- STIX 1.x legacy format support
- OpenC2 command and control integration (future wave)
- MISP (Malware Information Sharing Platform) direct integration (can export STIX)
- Custom STIX extensions (use standard STIX 2.1 only)

### 1.3 Dependencies

**Required Completed Waves**:
- Wave 1: Core MITRE ATT&CK framework (for STIX Attack Pattern mapping)
- Wave 2: Asset classification (for STIX Infrastructure objects)
- Wave 4: CVE integration (for STIX Vulnerability mapping)
- Wave 5: ICS framework (for OT infrastructure in STIX)

**External Standards**:
- UCO Ontology Specification v1.2.0 (https://unifiedcyberontology.org/)
- STIX 2.1 Specification (https://docs.oasis-open.org/cti/stix/v2.1/)
- TAXII 2.1 Specification (https://docs.oasis-open.org/cti/taxii/v2.1/)
- JSON-LD for serialization
- Neo4j APOC procedures for JSON handling

**Technical Requirements**:
- Neo4j APOC library installed
- Python 3.8+ for STIX validation (stix2 library)
- Network access to TAXII servers (optional, for live feeds)

### 1.4 Success Metrics

**Quantitative Metrics**:
- 15+ UCO core observable types implemented
- 12+ STIX Domain Object types with full properties
- 18+ STIX Cyber-observable Object types
- 100+ bidirectional mappings (ATT&CK ↔ STIX Attack Pattern)
- 500+ CVE → STIX Vulnerability conversions
- 50+ investigation case nodes created (example data)
- STIX bundle export/import roundtrip with 100% fidelity
- Query performance <1 second for STIX bundle generation

**Qualitative Metrics**:
- Valid STIX 2.1 JSON bundle export
- UCO ontology compliance validation
- Support for cyber forensics investigation workflows
- Seamless integration with existing graph (no data loss)
- Automated TAXII feed ingestion capability

## 2. Complete Node Schemas

### 2.1 UCO Core: Observable Nodes

#### 2.1.1 UCO Observable Base

**Node Label**: `UCO_Observable`

**Description**: Base class for all UCO observable objects representing cyber artifacts and entities.

**Properties**:
```cypher
{
  uco_id: String,                // UCO unique identifier (UUID format)
  uco_type: String,              // UCO observable type (File, NetworkConnection, etc.)
  created_time: DateTime,        // Observable creation timestamp
  modified_time: DateTime,       // Last modification timestamp

  // Core UCO properties
  state: String,                 // Observable state (ACTIVE, INACTIVE, UNKNOWN)
  description: String,           // Human-readable description
  confidence: Float,             // Confidence in observable data (0.0-1.0)

  // Provenance
  created_by: String,            // Tool/person who created observable
  data_source: String,           // Data source for observable

  // Context
  labels: [String],              // Classification labels
  external_references: [Map],    // External reference citations

  // Metadata
  node_id: String,               // Neo4j internal UUID
  validation_status: String,     // UCO_COMPLIANT, NEEDS_REVIEW
  last_updated: DateTime
}
```

**Index and Constraint Definitions**:
```cypher
// Unique constraint on UCO ID
CREATE CONSTRAINT uco_observable_id_unique IF NOT EXISTS
FOR (o:UCO_Observable) REQUIRE o.uco_id IS UNIQUE;

// Index on UCO type for classification queries
CREATE INDEX uco_observable_type_idx IF NOT EXISTS
FOR (o:UCO_Observable) ON (o.uco_type);

// Index on created_time for temporal queries
CREATE INDEX uco_observable_time_idx IF NOT EXISTS
FOR (o:UCO_Observable) ON (o.created_time);
```

#### 2.1.2 UCO File Observable

**Node Label**: `UCO_File` (inherits `UCO_Observable`)

**Description**: Represents file system objects in cyber investigations.

**Properties**:
```cypher
{
  // Inherits all UCO_Observable properties plus:

  file_path: String,             // Full file path
  file_name: String,             // File name only
  file_extension: String,        // File extension (e.g., ".exe")
  file_size_bytes: Integer,      // File size in bytes

  // Hash values
  md5_hash: String,              // MD5 hash
  sha1_hash: String,             // SHA-1 hash
  sha256_hash: String,           // SHA-256 hash
  sha512_hash: String,           // SHA-512 hash (optional)

  // File metadata
  mime_type: String,             // MIME type
  magic_number: String,          // File magic number (hex)
  created_time: DateTime,        // File creation time
  modified_time: DateTime,       // Last modification time
  accessed_time: DateTime,       // Last access time

  // File attributes
  is_directory: Boolean,
  is_hidden: Boolean,
  is_system: Boolean,
  permissions: String,           // Unix permissions or Windows ACL
  owner: String,                 // File owner

  // Analysis results
  is_malicious: Boolean,
  malware_family: String,
  yara_matches: [String],        // Matching YARA rules

  // Forensics
  evidence_id: String,           // Evidence tracking ID
  chain_of_custody: [Map]        // Custody transfer records
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create UCO File Observable
CREATE (f:UCO_File:UCO_Observable {
  uco_id: "uco-file-" + randomUUID(),
  uco_type: "File",

  file_path: "C:\\Users\\victim\\AppData\\Local\\Temp\\malware.exe",
  file_name: "malware.exe",
  file_extension: ".exe",
  file_size_bytes: 245760,

  md5_hash: "d41d8cd98f00b204e9800998ecf8427e",
  sha1_hash: "da39a3ee5e6b4b0d3255bfef95601890afd80709",
  sha256_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",

  mime_type: "application/x-msdownload",
  magic_number: "4D5A",
  created_time: datetime('2024-10-15T08:23:45Z'),
  modified_time: datetime('2024-10-15T08:23:45Z'),
  accessed_time: datetime('2024-10-15T09:15:32Z'),

  is_directory: false,
  is_hidden: false,
  is_system: false,
  permissions: "755",
  owner: "VICTIM-PC\\victim",

  is_malicious: true,
  malware_family: "TrickBot",
  yara_matches: ["TrickBot_Loader", "Packed_UPX"],

  evidence_id: "CASE-2024-001-EV-042",
  chain_of_custody: [
    {
      timestamp: datetime('2024-10-15T10:00:00Z'),
      handler: "Forensic Analyst John Doe",
      action: "Collected from endpoint",
      hash_verified: true
    }
  ],

  state: "ACTIVE",
  description: "Suspected TrickBot malware executable",
  confidence: 0.95,
  created_by: "EDR_Agent_v2.3",
  data_source: "Endpoint Detection and Response",
  labels: ["malware", "executable", "trickbot"],

  node_id: randomUUID(),
  validation_status: "UCO_COMPLIANT",
  last_updated: datetime()
})
```

**Index Definitions**:
```cypher
// Index on hash values for IoC matching
CREATE INDEX uco_file_md5_idx IF NOT EXISTS
FOR (f:UCO_File) ON (f.md5_hash);

CREATE INDEX uco_file_sha256_idx IF NOT EXISTS
FOR (f:UCO_File) ON (f.sha256_hash);

// Index on file name for search
CREATE INDEX uco_file_name_idx IF NOT EXISTS
FOR (f:UCO_File) ON (f.file_name);

// Full-text search on file paths
CREATE FULLTEXT INDEX uco_file_fulltext IF NOT EXISTS
FOR (f:UCO_File) ON EACH [f.file_path, f.file_name];
```

#### 2.1.3 UCO Network Connection Observable

**Node Label**: `UCO_NetworkConnection` (inherits `UCO_Observable`)

**Description**: Represents network connections in cyber investigations.

**Properties**:
```cypher
{
  // Inherits all UCO_Observable properties plus:

  // Source information
  source_ip: String,             // Source IP address
  source_port: Integer,          // Source port number
  source_hostname: String,       // Source hostname (optional)

  // Destination information
  destination_ip: String,        // Destination IP address
  destination_port: Integer,     // Destination port number
  destination_hostname: String,  // Destination hostname

  // Connection details
  protocol: String,              // TCP, UDP, ICMP, etc.
  protocol_layer7: String,       // HTTP, HTTPS, DNS, SMB, etc.
  connection_state: String,      // ESTABLISHED, SYN_SENT, CLOSED, etc.

  // Traffic characteristics
  bytes_sent: Integer,           // Bytes transmitted
  bytes_received: Integer,       // Bytes received
  packets_sent: Integer,
  packets_received: Integer,

  // Timing
  start_time: DateTime,          // Connection start
  end_time: DateTime,            // Connection end
  duration_seconds: Float,       // Connection duration

  // Security analysis
  is_suspicious: Boolean,
  threat_indicators: [String],   // Detected threats
  geolocation_dest: Map,         // Destination geo data

  // Additional context
  process_id: Integer,           // Associated process ID
  process_name: String,          // Process that created connection
  user_account: String           // User account context
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create UCO Network Connection
CREATE (nc:UCO_NetworkConnection:UCO_Observable {
  uco_id: "uco-network-" + randomUUID(),
  uco_type: "NetworkConnection",

  source_ip: "10.10.50.100",
  source_port: 49832,
  source_hostname: "workstation-042.internal.corp",

  destination_ip: "203.0.113.45",
  destination_port: 443,
  destination_hostname: "malicious-c2.example.com",

  protocol: "TCP",
  protocol_layer7: "HTTPS",
  connection_state: "ESTABLISHED",

  bytes_sent: 15234,
  bytes_received: 89456,
  packets_sent: 42,
  packets_received: 67,

  start_time: datetime('2024-10-15T14:23:11Z'),
  end_time: datetime('2024-10-15T14:28:45Z'),
  duration_seconds: 334.0,

  is_suspicious: true,
  threat_indicators: [
    "Connection to known C2 server",
    "Unusual data exfiltration volume",
    "Certificate mismatch"
  ],
  geolocation_dest: {
    country: "Unknown",
    city: "Unknown",
    asn: "AS64512",
    organization: "Bulletproof Hosting Ltd"
  },

  process_id: 4892,
  process_name: "svchost.exe",
  user_account: "WORKSTATION-042\\jdoe",

  state: "ACTIVE",
  description: "Suspicious HTTPS connection to potential C2 server",
  confidence: 0.88,
  created_by: "Network_IDS_v3.1",
  data_source: "Network Traffic Analysis",
  labels: ["c2-communication", "exfiltration", "suspicious"],

  node_id: randomUUID(),
  validation_status: "UCO_COMPLIANT",
  last_updated: datetime()
})
```

**Index Definitions**:
```cypher
// Index on IP addresses for correlation
CREATE INDEX uco_netconn_src_ip_idx IF NOT EXISTS
FOR (nc:UCO_NetworkConnection) ON (nc.source_ip);

CREATE INDEX uco_netconn_dest_ip_idx IF NOT EXISTS
FOR (nc:UCO_NetworkConnection) ON (nc.destination_ip);

// Index on destination port for service analysis
CREATE INDEX uco_netconn_dest_port_idx IF NOT EXISTS
FOR (nc:UCO_NetworkConnection) ON (nc.destination_port);

// Index on start time for temporal analysis
CREATE INDEX uco_netconn_time_idx IF NOT EXISTS
FOR (nc:UCO_NetworkConnection) ON (nc.start_time);
```

#### 2.1.4 UCO Process Observable

**Node Label**: `UCO_Process` (inherits `UCO_Observable`)

**Description**: Represents process execution in cyber investigations.

**Properties**:
```cypher
{
  // Inherits all UCO_Observable properties plus:

  process_id: Integer,           // PID
  parent_process_id: Integer,    // Parent PID
  process_name: String,          // Process name
  process_path: String,          // Full path to executable

  // Command line
  command_line: String,          // Full command line with arguments
  arguments: [String],           // Parsed arguments

  // User context
  user_account: String,          // Executing user account
  user_sid: String,              // Windows SID (if applicable)
  integrity_level: String,       // Low, Medium, High, System

  // Timing
  creation_time: DateTime,       // Process start time
  termination_time: DateTime,    // Process end time (if terminated)

  // Binary information
  binary_hash_md5: String,
  binary_hash_sha256: String,
  digital_signature: Map,        // Code signing certificate info
  is_signed: Boolean,
  is_valid_signature: Boolean,

  // Process characteristics
  is_hidden: Boolean,
  is_injected: Boolean,          // Code injection detected
  injection_technique: String,   // DLL injection, process hollowing, etc.

  // Network activity
  network_connections: [String], // UCO IDs of associated connections

  // File activity
  files_created: [String],       // UCO IDs of created files
  files_modified: [String],      // UCO IDs of modified files
  files_deleted: [String],       // UCO IDs of deleted files

  // Registry activity (Windows)
  registry_keys_modified: [String],

  // Security analysis
  is_malicious: Boolean,
  malware_family: String,
  behavior_tags: [String]        // "persistence", "credential-theft", etc.
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create UCO Process Observable
CREATE (p:UCO_Process:UCO_Observable {
  uco_id: "uco-process-" + randomUUID(),
  uco_type: "Process",

  process_id: 4892,
  parent_process_id: 1024,
  process_name: "svchost.exe",
  process_path: "C:\\Windows\\System32\\svchost.exe",

  command_line: "C:\\Windows\\System32\\svchost.exe -k netsvcs -p",
  arguments: ["-k", "netsvcs", "-p"],

  user_account: "NT AUTHORITY\\SYSTEM",
  user_sid: "S-1-5-18",
  integrity_level: "System",

  creation_time: datetime('2024-10-15T08:45:23Z'),
  termination_time: null,

  binary_hash_md5: "d41d8cd98f00b204e9800998ecf8427e",
  binary_hash_sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  digital_signature: {
    signer: "Microsoft Corporation",
    issuer: "Microsoft Code Signing PCA",
    serial: "33000001B1BFF95B0E1E71CA000000000001B1",
    valid_from: datetime('2020-01-15T00:00:00Z'),
    valid_to: datetime('2025-01-15T00:00:00Z')
  },
  is_signed: true,
  is_valid_signature: false,  // Signature tampered

  is_hidden: false,
  is_injected: true,
  injection_technique: "Process Hollowing",

  network_connections: [],  // Will be populated via relationships
  files_created: [],
  files_modified: [],

  registry_keys_modified: [
    "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\malware"
  ],

  is_malicious: true,
  malware_family: "Emotet",
  behavior_tags: ["persistence", "process-injection", "command-and-control"],

  state: "ACTIVE",
  description: "Malicious svchost.exe process with hollowed legitimate binary",
  confidence: 0.92,
  created_by: "EDR_Agent_v2.3",
  data_source: "Endpoint Detection and Response",
  labels: ["malware", "process-injection", "emotet"],

  node_id: randomUUID(),
  validation_status: "UCO_COMPLIANT",
  last_updated: datetime()
})
```

**Index Definitions**:
```cypher
// Index on process ID for correlation
CREATE INDEX uco_process_pid_idx IF NOT EXISTS
FOR (p:UCO_Process) ON (p.process_id);

// Index on process name
CREATE INDEX uco_process_name_idx IF NOT EXISTS
FOR (p:UCO_Process) ON (p.process_name);

// Index on binary hashes
CREATE INDEX uco_process_sha256_idx IF NOT EXISTS
FOR (p:UCO_Process) ON (p.binary_hash_sha256);

// Full-text search on command line
CREATE FULLTEXT INDEX uco_process_fulltext IF NOT EXISTS
FOR (p:UCO_Process) ON EACH [p.command_line, p.process_path];
```

#### 2.1.5 UCO User Account Observable

**Node Label**: `UCO_UserAccount` (inherits `UCO_Observable`)

**Description**: Represents user accounts in cyber investigations.

**Properties**:
```cypher
{
  // Inherits all UCO_Observable properties plus:

  account_name: String,          // Username
  account_id: String,            // UID, SID, or unique identifier
  account_type: String,          // USER, ADMIN, SERVICE, SYSTEM
  domain: String,                // Domain or realm

  // Account details
  display_name: String,
  email_address: String,
  account_created: DateTime,
  last_login: DateTime,
  last_password_change: DateTime,

  // Security status
  is_enabled: Boolean,
  is_locked: Boolean,
  is_privileged: Boolean,
  password_expired: Boolean,

  // Group memberships
  groups: [String],              // Group names
  privileges: [String],          // Assigned privileges

  // Activity indicators
  login_attempts_failed: Integer,
  login_locations: [String],     // IP addresses or hostnames

  // Investigation context
  is_compromised: Boolean,
  compromise_indicators: [String]
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create UCO User Account
CREATE (u:UCO_UserAccount:UCO_Observable {
  uco_id: "uco-account-" + randomUUID(),
  uco_type: "UserAccount",

  account_name: "jdoe",
  account_id: "S-1-5-21-3623811015-3361044348-30300820-1013",
  account_type: "USER",
  domain: "CORP",

  display_name: "John Doe",
  email_address: "john.doe@corp.example.com",
  account_created: datetime('2022-03-15T00:00:00Z'),
  last_login: datetime('2024-10-15T08:23:00Z'),
  last_password_change: datetime('2024-07-01T00:00:00Z'),

  is_enabled: true,
  is_locked: false,
  is_privileged: false,
  password_expired: false,

  groups: ["Domain Users", "VPN Users", "Engineering"],
  privileges: ["SeChangeNotifyPrivilege", "SeIncreaseWorkingSetPrivilege"],

  login_attempts_failed: 3,
  login_locations: ["10.10.50.100", "192.168.1.45"],

  is_compromised: true,
  compromise_indicators: [
    "Unusual login time (3 AM)",
    "Login from foreign IP",
    "Privilege escalation attempt",
    "Lateral movement detected"
  ],

  state: "ACTIVE",
  description: "Compromised user account with suspicious activity",
  confidence: 0.85,
  created_by: "SIEM_AnalysisEngine",
  data_source: "Active Directory Logs",
  labels: ["compromised", "user-account", "lateral-movement"],

  node_id: randomUUID(),
  validation_status: "UCO_COMPLIANT",
  last_updated: datetime()
})
```

### 2.2 UCO Investigation: Case Management Nodes

#### 2.2.1 UCO Investigation Case

**Node Label**: `UCO_InvestigationCase`

**Description**: Represents a cyber investigation case aggregating evidence and findings.

**Properties**:
```cypher
{
  case_id: String,               // Unique case identifier
  case_name: String,             // Case title
  case_description: String,      // Detailed description

  // Case metadata
  case_status: String,           // OPEN, ACTIVE, CLOSED, ARCHIVED
  case_priority: String,         // LOW, MEDIUM, HIGH, CRITICAL
  case_classification: String,   // Incident type classification

  // Timeline
  case_opened: DateTime,
  case_closed: DateTime,
  incident_start_time: DateTime, // When incident began
  incident_end_time: DateTime,   // When incident ended

  // Case team
  lead_investigator: String,
  investigators: [String],       // All investigators
  organization: String,

  // Incident details
  affected_systems: [String],    // System identifiers
  affected_users: [String],      // User accounts
  estimated_impact: String,      // Business impact assessment

  // Evidence tracking
  evidence_count: Integer,       // Number of evidence items
  observable_count: Integer,     // Number of observables

  // Legal/compliance
  legal_hold: Boolean,
  retention_period_days: Integer,
  chain_of_custody_verified: Boolean,

  // References
  related_cases: [String],       // Related case IDs
  external_references: [Map],    // Incident reports, tickets

  // Metadata
  node_id: String,
  created_by: String,
  created_date: DateTime,
  last_updated: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create UCO Investigation Case
CREATE (c:UCO_InvestigationCase {
  case_id: "CASE-2024-001",
  case_name: "TrickBot Ransomware Incident - Manufacturing Plant",
  case_description: "Investigation of TrickBot malware infection leading to ransomware deployment in manufacturing plant OT network. Initial access via phishing, lateral movement to engineering workstations, and attempted PLC compromise.",

  case_status: "ACTIVE",
  case_priority: "CRITICAL",
  case_classification: "Ransomware Incident / OT Compromise",

  case_opened: datetime('2024-10-15T10:00:00Z'),
  case_closed: null,
  incident_start_time: datetime('2024-10-15T08:23:00Z'),
  incident_end_time: null,

  lead_investigator: "Jane Smith, CISSP, GCFA",
  investigators: [
    "Jane Smith (Lead)",
    "Bob Johnson (Forensics)",
    "Alice Wong (Malware Analysis)",
    "Carlos Garcia (OT Security)"
  ],
  organization: "ACME Manufacturing Corp - Security Operations",

  affected_systems: [
    "WORKSTATION-042",
    "ENG-WS-15",
    "SCADA-SERVER-01",
    "PLC-S7-1500-003"
  ],
  affected_users: ["jdoe", "admin", "engineering_service"],
  estimated_impact: "Production line halted for 6 hours, estimated loss $250,000",

  evidence_count: 47,
  observable_count: 156,

  legal_hold: true,
  retention_period_days: 2555,  // 7 years
  chain_of_custody_verified: true,

  related_cases: [],
  external_references: [
    {
      source: "ServiceNow",
      id: "INC0012345",
      url: "https://corp.service-now.com/incident.do?sys_id=abc123"
    },
    {
      source: "CISA ICS-CERT",
      id: "ICSA-24-285-01",
      url: "https://www.cisa.gov/news-events/ics-advisories/icsa-24-285-01"
    }
  ],

  node_id: randomUUID(),
  created_by: "Jane Smith",
  created_date: datetime('2024-10-15T10:00:00Z'),
  last_updated: datetime(),
  validation_status: "UCO_COMPLIANT"
})
```

**Index Definitions**:
```cypher
// Unique constraint on case ID
CREATE CONSTRAINT uco_case_id_unique IF NOT EXISTS
FOR (c:UCO_InvestigationCase) REQUIRE c.case_id IS UNIQUE;

// Index on case status
CREATE INDEX uco_case_status_idx IF NOT EXISTS
FOR (c:UCO_InvestigationCase) ON (c.case_status);

// Index on case priority
CREATE INDEX uco_case_priority_idx IF NOT EXISTS
FOR (c:UCO_InvestigationCase) ON (c.case_priority);

// Index on incident start time
CREATE INDEX uco_case_time_idx IF NOT EXISTS
FOR (c:UCO_InvestigationCase) ON (c.incident_start_time);

// Full-text search on case details
CREATE FULLTEXT INDEX uco_case_fulltext IF NOT EXISTS
FOR (c:UCO_InvestigationCase) ON EACH [c.case_name, c.case_description];
```

### 2.3 STIX Domain Objects (SDOs)

#### 2.3.1 STIX Attack Pattern

**Node Label**: `STIX_AttackPattern`

**Description**: STIX representation of adversary tactics, techniques, and procedures (TTPs).

**Properties**:
```cypher
{
  stix_id: String,               // STIX ID (attack-pattern--<UUID>)
  stix_type: String,             // Always "attack-pattern"
  spec_version: String,          // STIX version (e.g., "2.1")

  // Core properties
  name: String,                  // Attack pattern name
  description: String,           // Detailed description

  // External references (MITRE ATT&CK)
  external_references: [Map],    // MITRE ATT&CK ID, URL, etc.
  mitre_attack_id: String,       // Extracted ATT&CK ID (e.g., "T1078")

  // Kill chain phases
  kill_chain_phases: [Map],      // Kill chain phase mappings

  // Metadata
  created: DateTime,             // STIX creation time
  modified: DateTime,            // STIX modification time
  created_by_ref: String,        // STIX Identity ID

  // Optional properties
  aliases: [String],
  revoked: Boolean,
  labels: [String],
  confidence: Integer,           // 0-100
  lang: String,                  // Language code
  object_marking_refs: [String], // TLP markings

  // Neo4j metadata
  node_id: String,
  imported_from: String,         // "TAXII", "STIX_BUNDLE", "MANUAL"
  import_timestamp: DateTime,
  validation_status: String      // "STIX_VALID", "STIX_INVALID"
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create STIX Attack Pattern mapped to MITRE ATT&CK
CREATE (ap:STIX_AttackPattern {
  stix_id: "attack-pattern--" + randomUUID(),
  stix_type: "attack-pattern",
  spec_version: "2.1",

  name: "Valid Accounts",
  description: "Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access, Persistence, Privilege Escalation, or Defense Evasion. Compromised credentials may be used to bypass access controls placed on various resources on systems within the network and may even be used for persistent access to remote systems and externally available services.",

  external_references: [
    {
      source_name: "mitre-attack",
      external_id: "T1078",
      url: "https://attack.mitre.org/techniques/T1078"
    }
  ],
  mitre_attack_id: "T1078",

  kill_chain_phases: [
    {
      kill_chain_name: "mitre-attack",
      phase_name: "initial-access"
    },
    {
      kill_chain_name: "mitre-attack",
      phase_name: "persistence"
    },
    {
      kill_chain_name: "mitre-attack",
      phase_name: "privilege-escalation"
    },
    {
      kill_chain_name: "mitre-attack",
      phase_name: "defense-evasion"
    }
  ],

  created: datetime('2017-05-31T21:31:53.197Z'),
  modified: datetime('2023-04-11T23:42:53.447Z'),
  created_by_ref: "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",  // MITRE ATT&CK

  aliases: [],
  revoked: false,
  labels: ["attack-pattern"],
  confidence: 95,
  lang: "en",
  object_marking_refs: ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],  // TLP:WHITE

  node_id: randomUUID(),
  imported_from: "MITRE_ATT&CK_v13",
  import_timestamp: datetime(),
  validation_status: "STIX_VALID"
})
```

**Index Definitions**:
```cypher
// Unique constraint on STIX ID
CREATE CONSTRAINT stix_attack_pattern_id_unique IF NOT EXISTS
FOR (ap:STIX_AttackPattern) REQUIRE ap.stix_id IS UNIQUE;

// Index on MITRE ATT&CK ID for mapping
CREATE INDEX stix_attack_pattern_mitre_idx IF NOT EXISTS
FOR (ap:STIX_AttackPattern) ON (ap.mitre_attack_id);

// Index on name
CREATE INDEX stix_attack_pattern_name_idx IF NOT EXISTS
FOR (ap:STIX_AttackPattern) ON (ap.name);

// Full-text search
CREATE FULLTEXT INDEX stix_attack_pattern_fulltext IF NOT EXISTS
FOR (ap:STIX_AttackPattern) ON EACH [ap.name, ap.description];
```

#### 2.3.2 STIX Indicator

**Node Label**: `STIX_Indicator`

**Description**: STIX indicator of compromise (IoC) with detection pattern.

**Properties**:
```cypher
{
  stix_id: String,               // STIX ID (indicator--<UUID>)
  stix_type: String,             // Always "indicator"
  spec_version: String,          // "2.1"

  // Core properties (REQUIRED)
  name: String,                  // Indicator name
  description: String,           // Description
  pattern: String,               // Detection pattern (STIX pattern format)
  pattern_type: String,          // "stix", "snort", "yara", etc.
  pattern_version: String,       // Pattern language version
  valid_from: DateTime,          // Indicator validity start

  // Optional properties
  valid_until: DateTime,         // Indicator expiration
  indicator_types: [String],     // "malicious-activity", "anomalous-activity", etc.

  // Kill chain
  kill_chain_phases: [Map],

  // Metadata
  created: DateTime,
  modified: DateTime,
  created_by_ref: String,
  revoked: Boolean,
  labels: [String],
  confidence: Integer,
  lang: String,
  object_marking_refs: [String],
  external_references: [Map],

  // Neo4j metadata
  node_id: String,
  imported_from: String,
  import_timestamp: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create STIX Indicator (File Hash IoC)
CREATE (i:STIX_Indicator {
  stix_id: "indicator--" + randomUUID(),
  stix_type: "indicator",
  spec_version: "2.1",

  name: "TrickBot Malware SHA-256",
  description: "SHA-256 hash of TrickBot malware loader observed in October 2024 campaign targeting manufacturing sector",
  pattern: "[file:hashes.SHA-256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']",
  pattern_type: "stix",
  pattern_version: "2.1",
  valid_from: datetime('2024-10-15T00:00:00Z'),
  valid_until: datetime('2025-10-15T00:00:00Z'),

  indicator_types: ["malicious-activity"],

  kill_chain_phases: [
    {
      kill_chain_name: "lockheed-martin-cyber-kill-chain",
      phase_name: "delivery"
    }
  ],

  created: datetime('2024-10-15T12:00:00Z'),
  modified: datetime('2024-10-15T12:00:00Z'),
  created_by_ref: "identity--acme-soc",
  revoked: false,
  labels: ["malware", "trickbot"],
  confidence: 90,
  lang: "en",
  object_marking_refs: ["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],  // TLP:AMBER
  external_references: [
    {
      source_name: "ACME SOC Incident Report",
      description: "Internal incident response findings",
      external_id: "CASE-2024-001"
    }
  ],

  node_id: randomUUID(),
  imported_from: "INTERNAL_TIP",
  import_timestamp: datetime(),
  validation_status: "STIX_VALID"
})
```

**Index Definitions**:
```cypher
// Unique constraint on STIX ID
CREATE CONSTRAINT stix_indicator_id_unique IF NOT EXISTS
FOR (i:STIX_Indicator) REQUIRE i.stix_id IS UNIQUE;

// Index on valid_from for temporal queries
CREATE INDEX stix_indicator_valid_from_idx IF NOT EXISTS
FOR (i:STIX_Indicator) ON (i.valid_from);

// Index on indicator types
CREATE INDEX stix_indicator_types_idx IF NOT EXISTS
FOR (i:STIX_Indicator) ON (i.indicator_types);

// Full-text search on pattern and description
CREATE FULLTEXT INDEX stix_indicator_fulltext IF NOT EXISTS
FOR (i:STIX_Indicator) ON EACH [i.name, i.description, i.pattern];
```

#### 2.3.3 STIX Threat Actor

**Node Label**: `STIX_ThreatActor`

**Description**: STIX representation of threat actors (APT groups, cybercriminals, etc.).

**Properties**:
```cypher
{
  stix_id: String,               // STIX ID (threat-actor--<UUID>)
  stix_type: String,             // Always "threat-actor"
  spec_version: String,          // "2.1"

  // Core properties
  name: String,                  // Threat actor name
  description: String,           // Description

  // Threat actor characteristics
  threat_actor_types: [String],  // "nation-state", "activist", "criminal", etc.
  aliases: [String],             // Alternative names
  first_seen: DateTime,          // First observed
  last_seen: DateTime,           // Last observed
  roles: [String],               // "agent", "director", "sponsor"
  goals: [String],               // Actor objectives
  sophistication: String,        // "none", "minimal", "intermediate", "advanced", "expert", "innovator", "strategic"
  resource_level: String,        // "individual", "club", "contest", "team", "organization", "government"
  primary_motivation: String,    // "accidental", "coercion", "dominance", "ideology", "notoriety", "organizational-gain", "personal-gain", "personal-satisfaction", "revenge", "unpredictable"
  secondary_motivations: [String],

  // Operational characteristics
  personal_motivations: [String],

  // Metadata
  created: DateTime,
  modified: DateTime,
  created_by_ref: String,
  revoked: Boolean,
  labels: [String],
  confidence: Integer,
  lang: String,
  object_marking_refs: [String],
  external_references: [Map],

  // Neo4j metadata
  node_id: String,
  imported_from: String,
  import_timestamp: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create STIX Threat Actor (APT Group)
CREATE (ta:STIX_ThreatActor {
  stix_id: "threat-actor--" + randomUUID(),
  stix_type: "threat-actor",
  spec_version: "2.1",

  name: "APT28",
  description: "APT28 (also known as Fancy Bear, Sofacy, Pawn Storm) is a Russian state-sponsored advanced persistent threat group active since at least 2007. The group is known for sophisticated spear-phishing campaigns and custom malware targeting government, military, and security organizations.",

  threat_actor_types: ["nation-state"],
  aliases: ["Fancy Bear", "Sofacy", "Pawn Storm", "Sednit", "Strontium"],
  first_seen: datetime('2007-01-01T00:00:00Z'),
  last_seen: datetime('2024-10-01T00:00:00Z'),
  roles: ["agent", "director"],
  goals: [
    "Intelligence collection",
    "Strategic espionage",
    "Political influence operations"
  ],
  sophistication: "expert",
  resource_level: "government",
  primary_motivation: "organizational-gain",
  secondary_motivations: ["ideology", "dominance"],

  created: datetime('2017-05-31T21:31:53.197Z'),
  modified: datetime('2024-10-01T00:00:00Z'),
  created_by_ref: "identity--mitre",
  revoked: false,
  labels: ["apt", "russia", "nation-state"],
  confidence: 95,
  lang: "en",
  object_marking_refs: ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],  // TLP:WHITE
  external_references: [
    {
      source_name: "MITRE ATT&CK",
      description: "APT28 Group Profile",
      external_id: "G0007",
      url: "https://attack.mitre.org/groups/G0007"
    }
  ],

  node_id: randomUUID(),
  imported_from: "MITRE_ATT&CK",
  import_timestamp: datetime(),
  validation_status: "STIX_VALID"
})
```

**Index Definitions**:
```cypher
// Unique constraint on STIX ID
CREATE CONSTRAINT stix_threat_actor_id_unique IF NOT EXISTS
FOR (ta:STIX_ThreatActor) REQUIRE ta.stix_id IS UNIQUE;

// Index on name
CREATE INDEX stix_threat_actor_name_idx IF NOT EXISTS
FOR (ta:STIX_ThreatActor) ON (ta.name);

// Index on threat actor types
CREATE INDEX stix_threat_actor_types_idx IF NOT EXISTS
FOR (ta:STIX_ThreatActor) ON (ta.threat_actor_types);

// Full-text search
CREATE FULLTEXT INDEX stix_threat_actor_fulltext IF NOT EXISTS
FOR (ta:STIX_ThreatActor) ON EACH [ta.name, ta.description, ta.aliases];
```

#### 2.3.4 STIX Malware

**Node Label**: `STIX_Malware`

**Description**: STIX representation of malware families and variants.

**Properties**:
```cypher
{
  stix_id: String,               // STIX ID (malware--<UUID>)
  stix_type: String,             // Always "malware"
  spec_version: String,          // "2.1"

  // Core properties
  name: String,                  // Malware name
  description: String,           // Description
  is_family: Boolean,            // true = family, false = variant
  malware_types: [String],       // "backdoor", "ransomware", "trojan", etc.

  // Optional properties
  aliases: [String],
  first_seen: DateTime,
  last_seen: DateTime,
  operating_system_refs: [String], // Software STIX IDs
  architecture_execution_envs: [String], // "x86", "ARM", etc.
  implementation_languages: [String], // "C", "Python", etc.
  capabilities: [String],
  sample_refs: [String],         // File/Artifact STIX IDs

  // Kill chain
  kill_chain_phases: [Map],

  // Metadata
  created: DateTime,
  modified: DateTime,
  created_by_ref: String,
  revoked: Boolean,
  labels: [String],
  confidence: Integer,
  lang: String,
  object_marking_refs: [String],
  external_references: [Map],

  // Neo4j metadata
  node_id: String,
  imported_from: String,
  import_timestamp: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create STIX Malware (TrickBot)
CREATE (m:STIX_Malware {
  stix_id: "malware--" + randomUUID(),
  stix_type: "malware",
  spec_version: "2.1",

  name: "TrickBot",
  description: "TrickBot is a modular banking trojan that has evolved into a sophisticated malware framework used for various malicious activities including credential theft, lateral movement, and ransomware deployment. It is typically distributed via phishing emails and has been used by multiple threat actors.",
  is_family: true,
  malware_types: ["trojan", "backdoor", "credential-stealer"],

  aliases: ["Trickster"],
  first_seen: datetime('2016-09-01T00:00:00Z'),
  last_seen: datetime('2024-10-15T00:00:00Z'),
  operating_system_refs: ["software--windows"],
  architecture_execution_envs: ["x86", "x86-64"],
  implementation_languages: ["C", "C++"],
  capabilities: [
    "Credential theft from browsers and applications",
    "Network reconnaissance",
    "Lateral movement",
    "Module download and execution",
    "Command and control",
    "Screen capture",
    "Keylogging"
  ],
  sample_refs: [],  // Will be populated via relationships

  kill_chain_phases: [
    {
      kill_chain_name: "lockheed-martin-cyber-kill-chain",
      phase_name: "delivery"
    },
    {
      kill_chain_name: "lockheed-martin-cyber-kill-chain",
      phase_name: "installation"
    },
    {
      kill_chain_name: "lockheed-martin-cyber-kill-chain",
      phase_name: "command-and-control"
    },
    {
      kill_chain_name: "lockheed-martin-cyber-kill-chain",
      phase_name: "actions-on-objectives"
    }
  ],

  created: datetime('2017-05-31T21:31:53.197Z'),
  modified: datetime('2024-10-15T00:00:00Z'),
  created_by_ref: "identity--mitre",
  revoked: false,
  labels: ["malware", "banking-trojan"],
  confidence: 95,
  lang: "en",
  object_marking_refs: ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],
  external_references: [
    {
      source_name: "MITRE ATT&CK",
      description: "TrickBot Software Profile",
      external_id: "S0266",
      url: "https://attack.mitre.org/software/S0266"
    }
  ],

  node_id: randomUUID(),
  imported_from: "MITRE_ATT&CK",
  import_timestamp: datetime(),
  validation_status: "STIX_VALID"
})
```

#### 2.3.5 STIX Vulnerability

**Node Label**: `STIX_Vulnerability`

**Description**: STIX representation of software vulnerabilities (mapped to CVEs).

**Properties**:
```cypher
{
  stix_id: String,               // STIX ID (vulnerability--<UUID>)
  stix_type: String,             // Always "vulnerability"
  spec_version: String,          // "2.1"

  // Core properties
  name: String,                  // Vulnerability name (usually CVE ID)
  description: String,           // Description

  // External references (CVE)
  external_references: [Map],    // CVE database reference
  cve_id: String,                // Extracted CVE ID

  // Metadata
  created: DateTime,
  modified: DateTime,
  created_by_ref: String,
  revoked: Boolean,
  labels: [String],
  confidence: Integer,
  lang: String,
  object_marking_refs: [String],

  // Neo4j metadata
  node_id: String,
  imported_from: String,
  import_timestamp: DateTime,
  validation_status: String
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create STIX Vulnerability (mapped to CVE)
CREATE (v:STIX_Vulnerability {
  stix_id: "vulnerability--" + randomUUID(),
  stix_type: "vulnerability",
  spec_version: "2.1",

  name: "CVE-2021-44228",
  description: "Apache Log4j2 <=2.14.1 JNDI features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP and other JNDI related endpoints. An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers when message lookup substitution is enabled. From log4j 2.15.0, this behavior has been disabled by default.",

  external_references: [
    {
      source_name: "cve",
      external_id: "CVE-2021-44228",
      url: "https://nvd.nist.gov/vuln/detail/CVE-2021-44228"
    }
  ],
  cve_id: "CVE-2021-44228",

  created: datetime('2021-12-10T00:00:00Z'),
  modified: datetime('2021-12-10T00:00:00Z'),
  created_by_ref: "identity--nist-nvd",
  revoked: false,
  labels: ["vulnerability", "log4shell", "remote-code-execution"],
  confidence: 100,
  lang: "en",
  object_marking_refs: ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],

  node_id: randomUUID(),
  imported_from: "NVD_CVE_FEED",
  import_timestamp: datetime(),
  validation_status: "STIX_VALID"
})
```

### 2.4 STIX Cyber-observable Objects (SCOs)

#### 2.4.1 STIX File Object

**Node Label**: `STIX_File`

**Description**: STIX cyber-observable representing a file.

**Properties**:
```cypher
{
  stix_id: String,               // STIX ID (file--<UUID>)
  stix_type: String,             // Always "file"
  spec_version: String,          // "2.1"

  // File properties
  name: String,                  // File name
  size: Integer,                 // File size in bytes
  hashes: Map,                   // {MD5: "...", "SHA-256": "...", etc.}
  mime_type: String,
  magic_number_hex: String,

  // Optional properties
  name_enc: String,              // Filename encoding
  ctime: DateTime,               // Creation time
  mtime: DateTime,               // Modification time
  atime: DateTime,               // Access time
  parent_directory_ref: String,  // Directory STIX ID
  contains_refs: [String],       // Embedded file STIX IDs
  content_ref: String,           // Artifact STIX ID

  // Extensions
  extensions: Map,               // PDF, Windows PE, Archive, etc.

  // Neo4j metadata
  node_id: String,
  object_marking_refs: [String],
  imported_from: String,
  import_timestamp: DateTime
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create STIX File Observable
CREATE (f:STIX_File {
  stix_id: "file--" + randomUUID(),
  stix_type: "file",
  spec_version: "2.1",

  name: "malware.exe",
  size: 245760,
  hashes: {
    "MD5": "d41d8cd98f00b204e9800998ecf8427e",
    "SHA-1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "SHA-256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  },
  mime_type: "application/x-msdownload",
  magic_number_hex: "4D5A",

  name_enc: "UTF-8",
  ctime: datetime('2024-10-15T08:23:45Z'),
  mtime: datetime('2024-10-15T08:23:45Z'),
  atime: datetime('2024-10-15T09:15:32Z'),

  extensions: {
    "windows-pebinary-ext": {
      pe_type: "exe",
      machine: "x86",
      imphash: "abc123def456"
    }
  },

  node_id: randomUUID(),
  object_marking_refs: ["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],
  imported_from: "EDR_TELEMETRY",
  import_timestamp: datetime()
})
```

#### 2.4.2 STIX IPv4 Address Object

**Node Label**: `STIX_IPv4Address`

**Description**: STIX cyber-observable representing an IPv4 address.

**Properties**:
```cypher
{
  stix_id: String,               // STIX ID (ipv4-addr--<UUID>)
  stix_type: String,             // Always "ipv4-addr"
  spec_version: String,          // "2.1"

  // Core properties
  value: String,                 // IPv4 address (e.g., "192.0.2.1")

  // Optional properties
  resolves_to_refs: [String],    // MAC Address STIX IDs
  belongs_to_refs: [String],     // Autonomous System STIX IDs

  // Neo4j metadata
  node_id: String,
  object_marking_refs: [String],
  imported_from: String,
  import_timestamp: DateTime
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create STIX IPv4 Address
CREATE (ip:STIX_IPv4Address {
  stix_id: "ipv4-addr--" + randomUUID(),
  stix_type: "ipv4-addr",
  spec_version: "2.1",

  value: "203.0.113.45",

  resolves_to_refs: [],
  belongs_to_refs: [],

  node_id: randomUUID(),
  object_marking_refs: ["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],
  imported_from: "NETWORK_IDS",
  import_timestamp: datetime()
})
```

#### 2.4.3 STIX Domain Name Object

**Node Label**: `STIX_DomainName`

**Description**: STIX cyber-observable representing a domain name.

**Properties**:
```cypher
{
  stix_id: String,               // STIX ID (domain-name--<UUID>)
  stix_type: String,             // Always "domain-name"
  spec_version: String,          // "2.1"

  // Core properties
  value: String,                 // Domain name (e.g., "example.com")

  // Optional properties
  resolves_to_refs: [String],    // IPv4/IPv6 Address STIX IDs

  // Neo4j metadata
  node_id: String,
  object_marking_refs: [String],
  imported_from: String,
  import_timestamp: DateTime
}
```

**Complete Cypher CREATE Statement**:
```cypher
// Create STIX Domain Name
CREATE (d:STIX_DomainName {
  stix_id: "domain-name--" + randomUUID(),
  stix_type: "domain-name",
  spec_version: "2.1",

  value: "malicious-c2.example.com",

  resolves_to_refs: [],

  node_id: randomUUID(),
  object_marking_refs: ["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],
  imported_from: "DNS_LOGS",
  import_timestamp: datetime()
})
```

## 3. Complete Relationship Schemas

### 3.1 UCO to STIX Mappings

#### 3.1.1 UCO Observable to STIX Observable

**Relationship Type**: `MAPS_TO_STIX`

**Description**: Bidirectional mapping between UCO observables and STIX cyber-observable objects.

**Properties**:
```cypher
{
  relationship_id: String,
  mapping_confidence: Float,     // 0.0-1.0
  mapping_type: String,          // "EXACT", "APPROXIMATE", "PARTIAL"
  created_date: DateTime,
  last_updated: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Map UCO File to STIX File
MATCH (uco:UCO_File {uco_id: "uco-file-..."})
MATCH (stix:STIX_File {stix_id: "file--..."})
CREATE (uco)-[r:MAPS_TO_STIX {
  relationship_id: randomUUID(),
  mapping_confidence: 1.0,
  mapping_type: "EXACT",
  created_date: datetime(),
  last_updated: datetime()
}]->(stix)
```

### 3.2 MITRE ATT&CK to STIX Attack Pattern

**Relationship Type**: `REPRESENTED_AS_STIX`

**Description**: Links existing MITRE ATT&CK techniques to STIX Attack Pattern representations.

**Properties**:
```cypher
{
  relationship_id: String,
  stix_version: String,          // STIX version used
  created_date: DateTime,
  auto_generated: Boolean
}
```

**Cypher CREATE Statement**:
```cypher
// Link ATT&CK Technique to STIX Attack Pattern
MATCH (tech:Technique {technique_id: "T1078"})
MATCH (stix_ap:STIX_AttackPattern {mitre_attack_id: "T1078"})
CREATE (tech)-[r:REPRESENTED_AS_STIX {
  relationship_id: randomUUID(),
  stix_version: "2.1",
  created_date: datetime(),
  auto_generated: true
}]->(stix_ap)
```

**Batch Creation for All ATT&CK Techniques**:
```cypher
// Auto-create STIX Attack Patterns for all ATT&CK techniques
MATCH (tech:Technique)
WHERE NOT (tech)-[:REPRESENTED_AS_STIX]->(:STIX_AttackPattern)
WITH tech
CREATE (stix_ap:STIX_AttackPattern {
  stix_id: "attack-pattern--" + randomUUID(),
  stix_type: "attack-pattern",
  spec_version: "2.1",
  name: tech.name,
  description: tech.description,
  external_references: [
    {
      source_name: "mitre-attack",
      external_id: tech.technique_id,
      url: "https://attack.mitre.org/techniques/" + tech.technique_id
    }
  ],
  mitre_attack_id: tech.technique_id,
  kill_chain_phases: [],  // Populate from tactics
  created: tech.created_date,
  modified: tech.modified_date,
  created_by_ref: "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
  revoked: false,
  labels: ["attack-pattern"],
  confidence: 95,
  lang: "en",
  object_marking_refs: ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],
  node_id: randomUUID(),
  imported_from: "AEON_AUTO_CONVERSION",
  import_timestamp: datetime(),
  validation_status: "STIX_VALID"
})
CREATE (tech)-[:REPRESENTED_AS_STIX {
  relationship_id: randomUUID(),
  stix_version: "2.1",
  created_date: datetime(),
  auto_generated: true
}]->(stix_ap)
```

### 3.3 CVE to STIX Vulnerability

**Relationship Type**: `REPRESENTED_AS_STIX_VULN`

**Description**: Links existing CVE nodes to STIX Vulnerability representations (CVE preservation).

**Properties**:
```cypher
{
  relationship_id: String,
  stix_version: String,
  created_date: DateTime,
  auto_generated: Boolean
}
```

**Cypher CREATE Statement**:
```cypher
// Link CVE to STIX Vulnerability (preserving existing CVE nodes)
MATCH (cve:CVE {cve_id: "CVE-2021-44228"})
MATCH (stix_vuln:STIX_Vulnerability {cve_id: "CVE-2021-44228"})
CREATE (cve)-[r:REPRESENTED_AS_STIX_VULN {
  relationship_id: randomUUID(),
  stix_version: "2.1",
  created_date: datetime(),
  auto_generated: true
}]->(stix_vuln)
```

**Batch CVE to STIX Conversion (Preserving All CVEs)**:
```cypher
// Auto-create STIX Vulnerability objects for all CVEs
MATCH (cve:CVE)
WHERE NOT (cve)-[:REPRESENTED_AS_STIX_VULN]->(:STIX_Vulnerability)
WITH cve
CREATE (stix_vuln:STIX_Vulnerability {
  stix_id: "vulnerability--" + randomUUID(),
  stix_type: "vulnerability",
  spec_version: "2.1",
  name: cve.cve_id,
  description: cve.description,
  external_references: [
    {
      source_name: "cve",
      external_id: cve.cve_id,
      url: "https://nvd.nist.gov/vuln/detail/" + cve.cve_id
    }
  ],
  cve_id: cve.cve_id,
  created: cve.published_date,
  modified: cve.last_modified_date,
  created_by_ref: "identity--nist-nvd",
  revoked: false,
  labels: ["vulnerability"],
  confidence: 100,
  lang: "en",
  object_marking_refs: ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],
  node_id: randomUUID(),
  imported_from: "AEON_CVE_CONVERSION",
  import_timestamp: datetime(),
  validation_status: "STIX_VALID"
})
CREATE (cve)-[:REPRESENTED_AS_STIX_VULN {
  relationship_id: randomUUID(),
  stix_version: "2.1",
  created_date: datetime(),
  auto_generated: true
}]->(stix_vuln)
```

### 3.4 STIX Relationships (SROs)

#### 3.4.1 STIX "uses" Relationship

**Relationship Type**: `STIX_USES`

**Description**: STIX relationship indicating one object uses another (e.g., Threat Actor uses Malware).

**Properties**:
```cypher
{
  stix_id: String,               // STIX relationship ID (relationship--<UUID>)
  stix_type: String,             // Always "relationship"
  spec_version: String,          // "2.1"
  relationship_type: String,     // "uses"
  source_ref: String,            // Source STIX ID
  target_ref: String,            // Target STIX ID

  // Optional properties
  description: String,
  start_time: DateTime,
  stop_time: DateTime,

  // Metadata
  created: DateTime,
  modified: DateTime,
  created_by_ref: String,
  revoked: Boolean,
  confidence: Integer,
  lang: String,
  object_marking_refs: [String],
  external_references: [Map]
}
```

**Cypher CREATE Statement**:
```cypher
// Create STIX "uses" relationship: Threat Actor uses Malware
MATCH (ta:STIX_ThreatActor {name: "APT28"})
MATCH (mal:STIX_Malware {name: "TrickBot"})
CREATE (ta)-[r:STIX_USES {
  stix_id: "relationship--" + randomUUID(),
  stix_type: "relationship",
  spec_version: "2.1",
  relationship_type: "uses",
  source_ref: ta.stix_id,
  target_ref: mal.stix_id,
  description: "APT28 has been observed using TrickBot malware in campaigns targeting critical infrastructure",
  start_time: datetime('2024-01-01T00:00:00Z'),
  stop_time: null,
  created: datetime(),
  modified: datetime(),
  created_by_ref: "identity--acme-ti",
  revoked: false,
  confidence: 85,
  lang: "en",
  object_marking_refs: ["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],
  external_references: []
}]->(mal)
```

#### 3.4.2 STIX "indicates" Relationship

**Relationship Type**: `STIX_INDICATES`

**Description**: STIX relationship where an Indicator indicates a malware, threat actor, or attack pattern.

**Properties**: Same as STIX_USES with relationship_type = "indicates"

**Cypher CREATE Statement**:
```cypher
// Create STIX "indicates" relationship: Indicator indicates Malware
MATCH (indicator:STIX_Indicator {name: "TrickBot Malware SHA-256"})
MATCH (malware:STIX_Malware {name: "TrickBot"})
CREATE (indicator)-[r:STIX_INDICATES {
  stix_id: "relationship--" + randomUUID(),
  stix_type: "relationship",
  spec_version: "2.1",
  relationship_type: "indicates",
  source_ref: indicator.stix_id,
  target_ref: malware.stix_id,
  description: "This file hash indicates the presence of TrickBot malware",
  created: datetime(),
  modified: datetime(),
  created_by_ref: "identity--acme-ti",
  revoked: false,
  confidence: 95,
  lang: "en",
  object_marking_refs: ["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"]
}]->(malware)
```

### 3.5 UCO Investigation Relationships

#### 3.5.1 Case Contains Observable

**Relationship Type**: `CASE_CONTAINS_OBSERVABLE`

**Description**: Links investigation cases to associated UCO observables (evidence).

**Properties**:
```cypher
{
  relationship_id: String,
  evidence_type: String,         // "PRIMARY", "SECONDARY", "SUPPORTING"
  evidence_collected_time: DateTime,
  collected_by: String,
  chain_of_custody_id: String,
  created_date: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link investigation case to file evidence
MATCH (case:UCO_InvestigationCase {case_id: "CASE-2024-001"})
MATCH (file:UCO_File {evidence_id: "CASE-2024-001-EV-042"})
CREATE (case)-[r:CASE_CONTAINS_OBSERVABLE {
  relationship_id: randomUUID(),
  evidence_type: "PRIMARY",
  evidence_collected_time: datetime('2024-10-15T10:00:00Z'),
  collected_by: "Forensic Analyst John Doe",
  chain_of_custody_id: "COC-2024-001-042",
  created_date: datetime()
}]->(file)
```

#### 3.5.2 Observable Relates to Observable

**Relationship Type**: `UCO_RELATES_TO`

**Description**: Links related UCO observables (e.g., Process created File, Network Connection from Process).

**Properties**:
```cypher
{
  relationship_id: String,
  relationship_type: String,     // "CREATED", "MODIFIED", "DELETED", "CONNECTED_TO", "EXECUTED", etc.
  timestamp: DateTime,
  confidence: Float,
  created_date: DateTime
}
```

**Cypher CREATE Statement**:
```cypher
// Link Process to File it created
MATCH (proc:UCO_Process {process_id: 4892})
MATCH (file:UCO_File {file_name: "malware.exe"})
CREATE (proc)-[r:UCO_RELATES_TO {
  relationship_id: randomUUID(),
  relationship_type: "CREATED",
  timestamp: datetime('2024-10-15T08:23:45Z'),
  confidence: 0.95,
  created_date: datetime()
}]->(file)

// Link Process to Network Connection
MATCH (proc:UCO_Process {process_id: 4892})
MATCH (netconn:UCO_NetworkConnection {source_port: 49832})
CREATE (proc)-[r2:UCO_RELATES_TO {
  relationship_id: randomUUID(),
  relationship_type: "INITIATED",
  timestamp: datetime('2024-10-15T14:23:11Z'),
  confidence: 1.0,
  created_date: datetime()
}]->(netconn)
```

## 4. Integration Patterns

### 4.1 STIX Bundle Export

**Objective**: Export Neo4j graph data as valid STIX 2.1 JSON bundles for sharing via TAXII.

**Export Query Pattern**:
```cypher
// Export STIX bundle for a specific campaign
MATCH (indicator:STIX_Indicator)-[:STIX_INDICATES]->(malware:STIX_Malware)
MATCH (ta:STIX_ThreatActor)-[:STIX_USES]->(malware)
MATCH (malware)-[:STIX_USES]->(ap:STIX_AttackPattern)
WHERE indicator.name CONTAINS "TrickBot"
WITH collect(indicator) + collect(malware) + collect(ta) + collect(ap) AS stix_objects
RETURN {
  type: "bundle",
  id: "bundle--" + randomUUID(),
  spec_version: "2.1",
  objects: [obj IN stix_objects | obj {.*}]
} AS stix_bundle
```

**Python STIX Bundle Generation** (using stix2 library):
```python
from neo4j import GraphDatabase
import stix2
import uuid

def export_stix_bundle(tx, campaign_name):
    query = """
    MATCH (indicator:STIX_Indicator)-[:STIX_INDICATES]->(malware:STIX_Malware)
    MATCH (ta:STIX_ThreatActor)-[:STIX_USES]->(malware)
    WHERE indicator.name CONTAINS $campaign_name
    RETURN indicator, malware, ta
    """
    result = tx.run(query, campaign_name=campaign_name)

    stix_objects = []
    for record in result:
        indicator_props = dict(record["indicator"])
        malware_props = dict(record["malware"])
        ta_props = dict(record["ta"])

        # Convert Neo4j nodes to STIX objects
        stix_indicator = stix2.Indicator(
            id=indicator_props["stix_id"],
            name=indicator_props["name"],
            pattern=indicator_props["pattern"],
            pattern_type=indicator_props["pattern_type"],
            valid_from=indicator_props["valid_from"]
        )
        stix_objects.append(stix_indicator)

        # ... similar for malware and threat actor

    bundle = stix2.Bundle(*stix_objects)
    return bundle.serialize(pretty=True)

# Usage
with driver.session() as session:
    stix_json = session.read_transaction(export_stix_bundle, "TrickBot")
    print(stix_json)
```

### 4.2 STIX Bundle Import

**Objective**: Import STIX 2.1 JSON bundles from TAXII servers into Neo4j graph.

**Import Pattern** (Python with stix2 and Neo4j driver):
```python
import stix2
from neo4j import GraphDatabase

def import_stix_bundle(tx, stix_bundle_json):
    bundle = stix2.parse(stix_bundle_json)

    for obj in bundle.objects:
        if obj.type == "indicator":
            query = """
            MERGE (i:STIX_Indicator {stix_id: $stix_id})
            SET i.name = $name,
                i.pattern = $pattern,
                i.pattern_type = $pattern_type,
                i.valid_from = datetime($valid_from),
                i.spec_version = $spec_version,
                i.created = datetime($created),
                i.modified = datetime($modified),
                i.imported_from = "TAXII",
                i.import_timestamp = datetime()
            """
            tx.run(query,
                   stix_id=obj.id,
                   name=obj.name,
                   pattern=obj.pattern,
                   pattern_type=obj.pattern_type,
                   valid_from=obj.valid_from.isoformat(),
                   spec_version=obj.spec_version,
                   created=obj.created.isoformat(),
                   modified=obj.modified.isoformat())

        elif obj.type == "malware":
            # Similar Cypher query for malware
            pass

        elif obj.type == "relationship":
            # Create relationships between STIX objects
            query = """
            MATCH (source {stix_id: $source_ref})
            MATCH (target {stix_id: $target_ref})
            MERGE (source)-[r:STIX_RELATIONSHIP {stix_id: $stix_id}]->(target)
            SET r.relationship_type = $relationship_type,
                r.created = datetime($created)
            """
            tx.run(query,
                   stix_id=obj.id,
                   source_ref=obj.source_ref,
                   target_ref=obj.target_ref,
                   relationship_type=obj.relationship_type,
                   created=obj.created.isoformat())

# Usage
with driver.session() as session:
    with open("stix_bundle.json", "r") as f:
        stix_json = f.read()
    session.write_transaction(import_stix_bundle, stix_json)
```

### 4.3 TAXII 2.1 Client Integration

**Objective**: Automatically fetch threat intelligence from TAXII 2.1 servers and import into Neo4j.

**Python TAXII Client Example**:
```python
from taxii2client.v21 import Server, Collection
from neo4j import GraphDatabase
import stix2

# Connect to TAXII server
server = Server("https://taxii.example.com/taxii/", user="username", password="password")

# Get collections
api_root = server.api_roots[0]
collections = api_root.collections

# Fetch STIX bundles from collection
for collection in collections:
    if collection.title == "Threat Intelligence Feed":
        # Get all objects from collection
        objects = collection.get_objects()

        # Convert to STIX bundle
        bundle = stix2.Bundle(objects=objects["objects"])

        # Import into Neo4j
        with driver.session() as session:
            session.write_transaction(import_stix_bundle, bundle.serialize())
```

### 4.4 CVE Preservation Validation

**Critical**: Ensure all Wave 4 CVE nodes remain intact after Wave 6 integration.

**Validation Query**:
```cypher
// Before Wave 6: Count CVE nodes
MATCH (cve:CVE)
RETURN count(cve) AS cve_count_before

// After Wave 6: Verify CVE count unchanged and STIX links added
MATCH (cve:CVE)
WITH count(cve) AS cve_count_after
MATCH (cve:CVE)-[:REPRESENTED_AS_STIX_VULN]->(stix:STIX_Vulnerability)
RETURN
  cve_count_after,
  count(DISTINCT cve) AS cves_with_stix_representation,
  (count(DISTINCT cve) * 100.0 / cve_count_after) AS percentage_mapped
// Expected: cve_count_after = cve_count_before, percentage_mapped ~100%
```

## 5. Validation Criteria

### 5.1 STIX 2.1 Compliance Validation

**STIX JSON Schema Validation**:
```python
import stix2
import json

def validate_stix_bundle(neo4j_driver):
    # Export STIX bundle from Neo4j
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (obj)
            WHERE obj.stix_id IS NOT NULL
            RETURN obj {.*} AS stix_object
            LIMIT 100
        """)

        stix_objects = []
        for record in result:
            obj_dict = dict(record["stix_object"])
            # Convert Neo4j properties to STIX format
            stix_objects.append(obj_dict)

        bundle_dict = {
            "type": "bundle",
            "id": "bundle--" + str(uuid.uuid4()),
            "spec_version": "2.1",
            "objects": stix_objects
        }

        try:
            # Validate using stix2 library
            bundle = stix2.parse(json.dumps(bundle_dict))
            print("✅ STIX bundle is valid!")
            return True
        except Exception as e:
            print(f"❌ STIX validation failed: {e}")
            return False
```

### 5.2 UCO Ontology Compliance

**UCO Validation Query**:
```cypher
// Verify UCO Observable nodes have required properties
MATCH (obs:UCO_Observable)
WHERE obs.uco_id IS NULL OR
      obs.uco_type IS NULL OR
      obs.created_time IS NULL OR
      obs.state IS NULL
RETURN count(obs) AS invalid_uco_observables
// Expected: 0
```

### 5.3 Integration Completeness

**Mapping Coverage Validation**:
```cypher
// Verify ATT&CK to STIX Attack Pattern mapping
MATCH (tech:Technique)
WITH count(tech) AS total_techniques
MATCH (tech:Technique)-[:REPRESENTED_AS_STIX]->(ap:STIX_AttackPattern)
RETURN
  total_techniques,
  count(DISTINCT tech) AS mapped_techniques,
  (count(DISTINCT tech) * 100.0 / total_techniques) AS mapping_percentage
// Expected: mapping_percentage >= 95%

// Verify CVE to STIX Vulnerability mapping
MATCH (cve:CVE)
WITH count(cve) AS total_cves
MATCH (cve:CVE)-[:REPRESENTED_AS_STIX_VULN]->(vuln:STIX_Vulnerability)
RETURN
  total_cves,
  count(DISTINCT cve) AS mapped_cves,
  (count(DISTINCT cve) * 100.0 / total_cves) AS mapping_percentage
// Expected: mapping_percentage = 100%
```

### 5.4 Performance Benchmarks

**STIX Bundle Generation Performance**:
```cypher
// Profile STIX bundle export query (<1 second target)
PROFILE
MATCH (indicator:STIX_Indicator)-[:STIX_INDICATES]->(malware:STIX_Malware)
MATCH (ta:STIX_ThreatActor)-[:STIX_USES]->(malware)
RETURN count(*) AS relationship_count
// Expected: <1000ms execution time
```

## 6. Example Queries

### 6.1 Cyber Investigation: Malware Infection Timeline

**Query**: Reconstruct malware infection timeline using UCO observables.

```cypher
// Reconstruct attack timeline from UCO observables
MATCH (case:UCO_InvestigationCase {case_id: "CASE-2024-001"})
MATCH (case)-[:CASE_CONTAINS_OBSERVABLE]->(obs:UCO_Observable)
OPTIONAL MATCH (obs)-[rel:UCO_RELATES_TO]->(related_obs:UCO_Observable)
WITH obs, rel, related_obs
ORDER BY obs.created_time ASC
RETURN
  obs.created_time AS timestamp,
  obs.uco_type AS observable_type,
  CASE obs.uco_type
    WHEN "File" THEN obs.file_name
    WHEN "Process" THEN obs.process_name
    WHEN "NetworkConnection" THEN obs.destination_ip
    ELSE obs.uco_id
  END AS observable_identifier,
  obs.is_malicious AS is_malicious,
  CASE
    WHEN obs:UCO_Process THEN obs.command_line
    WHEN obs:UCO_NetworkConnection THEN obs.destination_hostname
    ELSE null
  END AS additional_context,
  rel.relationship_type AS action,
  CASE related_obs.uco_type
    WHEN "File" THEN related_obs.file_name
    WHEN "Process" THEN related_obs.process_name
    ELSE null
  END AS related_observable
LIMIT 50
```

**Expected Result**: Chronological timeline of malware execution events.

### 6.2 STIX Threat Intelligence: APT Campaign Analysis

**Query**: Analyze APT campaign using STIX objects.

```cypher
// Find APT campaign details
MATCH (ta:STIX_ThreatActor {name: "APT28"})
MATCH (ta)-[:STIX_USES]->(malware:STIX_Malware)
MATCH (indicator:STIX_Indicator)-[:STIX_INDICATES]->(malware)
MATCH (malware)-[rel]->(ap:STIX_AttackPattern)
OPTIONAL MATCH (ap)<-[:REPRESENTED_AS_STIX]-(tech:Technique)
RETURN
  ta.name AS threat_actor,
  ta.sophistication AS sophistication_level,
  collect(DISTINCT malware.name) AS malware_families,
  collect(DISTINCT indicator.pattern) AS indicators_of_compromise,
  collect(DISTINCT ap.name) AS attack_techniques,
  collect(DISTINCT tech.technique_id) AS mitre_attack_ids
```

### 6.3 Cross-Standard Correlation: CVE to STIX to ATT&CK

**Query**: Correlate CVE vulnerability to ATT&CK techniques via STIX.

```cypher
// CVE → STIX Vulnerability → STIX Attack Pattern → ATT&CK Technique
MATCH (cve:CVE {cve_id: "CVE-2021-44228"})-[:REPRESENTED_AS_STIX_VULN]->(stix_vuln:STIX_Vulnerability)
MATCH (stix_vuln)<-[:STIX_TARGETS]-(stix_ap:STIX_AttackPattern)
MATCH (stix_ap)<-[:REPRESENTED_AS_STIX]-(tech:Technique)
MATCH (tech)<-[:USES]-(ta:ThreatActor)
RETURN
  cve.cve_id AS vulnerability,
  cve.cvss_base_score AS cvss_score,
  stix_vuln.name AS stix_representation,
  collect(DISTINCT stix_ap.name) AS attack_patterns,
  collect(DISTINCT tech.technique_id) AS att_ck_techniques,
  collect(DISTINCT ta.name) AS threat_actors_exploiting
```

### 6.4 STIX Bundle Completeness Check

**Query**: Verify STIX bundle has all required relationships.

```cypher
// Check STIX relationship coverage
MATCH (source)
WHERE source.stix_id IS NOT NULL AND source.stix_id STARTS WITH "indicator--"
OPTIONAL MATCH (source)-[r:STIX_INDICATES|STIX_USES|STIX_TARGETS]->(target)
WHERE target.stix_id IS NOT NULL
RETURN
  source.stix_id AS indicator_id,
  source.name AS indicator_name,
  count(r) AS outbound_relationships,
  collect(DISTINCT type(r)) AS relationship_types,
  collect(DISTINCT target.stix_type) AS target_types,
  CASE WHEN count(r) = 0 THEN "MISSING_RELATIONSHIPS" ELSE "OK" END AS status
```

### 6.5 UCO Chain of Custody Verification

**Query**: Verify evidence chain of custody for investigation case.

```cypher
// Verify chain of custody for case evidence
MATCH (case:UCO_InvestigationCase {case_id: "CASE-2024-001"})
MATCH (case)-[r:CASE_CONTAINS_OBSERVABLE]->(evidence:UCO_File)
WHERE evidence.evidence_id IS NOT NULL
RETURN
  evidence.evidence_id AS evidence_id,
  evidence.file_name AS file_name,
  evidence.sha256_hash AS hash,
  r.evidence_collected_time AS collection_time,
  r.collected_by AS collected_by,
  r.chain_of_custody_id AS custody_id,
  evidence.chain_of_custody AS custody_chain,
  CASE
    WHEN size(evidence.chain_of_custody) > 0 THEN "DOCUMENTED"
    ELSE "MISSING_CHAIN"
  END AS custody_status
ORDER BY r.evidence_collected_time ASC
```

## 7. Wave 6 Implementation Checklist

### 7.1 Pre-Implementation

- [ ] Complete Waves 1-5 validation
- [ ] Backup Neo4j database
- [ ] Verify CVE baseline count (for preservation)
- [ ] Install Neo4j APOC library
- [ ] Install Python stix2 library
- [ ] Review STIX 2.1 specification
- [ ] Review UCO ontology specification

### 7.2 Implementation Phase 1: UCO Observables (Week 1)

- [ ] Create UCO_Observable base nodes
- [ ] Create UCO_File nodes with full properties
- [ ] Create UCO_NetworkConnection nodes
- [ ] Create UCO_Process nodes
- [ ] Create UCO_UserAccount nodes
- [ ] Create UCO_InvestigationCase nodes
- [ ] Create all indexes and constraints
- [ ] Validate UCO property completeness

### 7.3 Implementation Phase 2: STIX Domain Objects (Week 2)

- [ ] Create STIX_AttackPattern nodes (mapped from ATT&CK)
- [ ] Create STIX_Indicator nodes
- [ ] Create STIX_ThreatActor nodes
- [ ] Create STIX_Malware nodes
- [ ] Create STIX_Vulnerability nodes (mapped from CVEs)
- [ ] Create STIX Cyber-observable Objects (SCOs)
- [ ] Create all STIX indexes and constraints
- [ ] Validate STIX JSON compliance

### 7.4 Implementation Phase 3: Relationships & Integration (Week 3)

- [ ] Create UCO to STIX mappings (MAPS_TO_STIX)
- [ ] Create ATT&CK to STIX Attack Pattern links (REPRESENTED_AS_STIX)
- [ ] Create CVE to STIX Vulnerability links (REPRESENTED_AS_STIX_VULN)
- [ ] Verify CVE preservation (100% count match)
- [ ] Create STIX Relationship Objects (uses, indicates, targets)
- [ ] Create UCO investigation relationships
- [ ] Test bidirectional conversion (Neo4j ↔ STIX JSON)

### 7.5 Implementation Phase 4: Import/Export & Validation (Week 4)

- [ ] Implement STIX bundle export functionality
- [ ] Implement STIX bundle import functionality
- [ ] Test TAXII 2.1 client integration (optional)
- [ ] Run STIX 2.1 JSON schema validation
- [ ] Run UCO ontology compliance checks
- [ ] Test all example queries
- [ ] Performance benchmarks (<1s STIX bundle generation)
- [ ] CVE preservation final validation
- [ ] Generate Wave 6 completion report

## 8. Wave 6 Success Criteria Summary

**Quantitative Targets**:
- ✅ 15+ UCO observable types implemented
- ✅ 12+ STIX Domain Object types created
- ✅ 18+ STIX Cyber-observable Object types created
- ✅ 100+ ATT&CK techniques mapped to STIX Attack Patterns
- ✅ 500+ CVEs converted to STIX Vulnerability objects
- ✅ 100% CVE preservation validated (no data loss)
- ✅ 50+ investigation case examples created
- ✅ STIX bundle export/import roundtrip 100% fidelity
- ✅ Query performance <1 second for STIX bundle generation

**Qualitative Targets**:
- ✅ Valid STIX 2.1 JSON bundle export verified
- ✅ UCO ontology compliance validated
- ✅ Cyber forensics investigation workflows supported
- ✅ Seamless integration with existing graph (no data loss)
- ✅ Automated TAXII feed ingestion capability (optional)
- ✅ Standards-compliant threat intelligence sharing enabled

---

**Wave 6 Status**: Ready for implementation
**Dependencies**: Waves 1, 2, 4, 5 completed
**Next Wave**: Wave 7 - Psychometric Analysis Integration
**Document Version**: v1.0.0
**Last Updated**: 2025-10-30
