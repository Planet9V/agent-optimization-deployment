// ============================================================================
// AEON DIGITAL TWIN CYBER SECURITY THREAT INTELLIGENCE
// Neo4j Node Type Definitions with Properties
// Version: 1.0.0
// Created: 2025-10-29
// ============================================================================

// ============================================================================
// NODE TYPE 1: ORGANIZATION
// Represents organizations that operate railway systems
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Organization name
// - type: STRING - Organization type (operator, manufacturer, regulator)
// - country: STRING - Country of operation
// - sector: STRING - Industry sector
// - employees: INTEGER - Number of employees
// - website: STRING - Official website URL
// - contactEmail: STRING - Primary contact email
// - foundedDate: DATE - Date organization was founded
// - description: STRING - Organization description
// - riskScore: FLOAT - Overall risk score (0-100)
// - lastAssessmentDate: DATETIME - Last security assessment
// - certifications: LIST<STRING> - Security certifications
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (org:Organization {
  id: 'ORG-001',
  name: 'Northern Railway Corporation',
  type: 'operator',
  country: 'United Kingdom',
  sector: 'Rail Transport',
  employees: 5000,
  website: 'https://northernrail.example.com',
  contactEmail: 'security@northernrail.example.com',
  foundedDate: date('1990-01-01'),
  description: 'Major railway operator in northern England',
  riskScore: 65.5,
  lastAssessmentDate: datetime('2025-10-15T10:30:00'),
  certifications: ['ISO 27001', 'IEC 62443'],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 2: SITE
// Represents physical railway sites (stations, depots, control centers)
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Site name
// - type: STRING - Site type (station, depot, control_center, maintenance)
// - location: STRING - Physical address
// - coordinates: POINT - GPS coordinates
// - operationalStatus: STRING - Current operational status
// - capacity: INTEGER - Maximum capacity
// - securityLevel: STRING - Physical security classification
// - hasPublicAccess: BOOLEAN - Public accessibility
// - criticalityLevel: STRING - Infrastructure criticality (critical, high, medium, low)
// - riskScore: FLOAT - Site-specific risk score
// - lastInspection: DATE - Last security inspection
// - emergencyContacts: LIST<STRING> - Emergency contact information
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (site:Site {
  id: 'SITE-001',
  name: 'Central Station',
  type: 'station',
  location: '123 Railway Street, London, UK',
  coordinates: point({latitude: 51.5074, longitude: -0.1278}),
  operationalStatus: 'active',
  capacity: 50000,
  securityLevel: 'high',
  hasPublicAccess: true,
  criticalityLevel: 'critical',
  riskScore: 72.3,
  lastInspection: date('2025-10-20'),
  emergencyContacts: ['+44-20-1234-5678', '+44-20-8765-4321'],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 3: TRAIN
// Represents individual trains or train sets
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Train name or designation
// - type: STRING - Train type (passenger, freight, high_speed, metro)
// - model: STRING - Manufacturer model number
// - manufacturer: STRING - Train manufacturer
// - yearBuilt: INTEGER - Year of manufacture
// - serialNumber: STRING - Manufacturer serial number
// - capacity: INTEGER - Passenger/cargo capacity
// - maxSpeed: INTEGER - Maximum operational speed (km/h)
// - powerType: STRING - Power system type (electric, diesel, hybrid)
// - status: STRING - Operational status (active, maintenance, retired)
// - lastMaintenance: DATE - Last maintenance date
// - nextMaintenance: DATE - Scheduled next maintenance
// - operatingRoute: STRING - Primary operating route
// - criticalityLevel: STRING - System criticality
// - riskScore: FLOAT - Train-specific risk score
// - mileage: INTEGER - Total distance traveled (km)
// - certifications: LIST<STRING> - Safety certifications
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (train:Train {
  id: 'TRAIN-001',
  name: 'Express-Alpha-1',
  type: 'high_speed',
  model: 'HST-500',
  manufacturer: 'Siemens Mobility',
  yearBuilt: 2020,
  serialNumber: 'SIE-HST-500-2020-001',
  capacity: 400,
  maxSpeed: 300,
  powerType: 'electric',
  status: 'active',
  lastMaintenance: date('2025-10-01'),
  nextMaintenance: date('2025-11-01'),
  operatingRoute: 'London-Edinburgh',
  criticalityLevel: 'critical',
  riskScore: 68.7,
  mileage: 500000,
  certifications: ['EN 15227', 'TSI'],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 4: COMPONENT
// Represents hardware/software components in trains and infrastructure
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Component name
// - type: STRING - Component type (PLC, SCADA, sensor, controller, actuator, display)
// - manufacturer: STRING - Manufacturer name
// - model: STRING - Model number
// - version: STRING - Hardware/firmware version
// - serialNumber: STRING - Serial number
// - installDate: DATE - Installation date
// - warrantyExpires: DATE - Warranty expiration
// - criticalityLevel: STRING - Component criticality (critical, high, medium, low)
// - functionDescription: STRING - Component function
// - networkConnected: BOOLEAN - Network connectivity
// - hasRemoteAccess: BOOLEAN - Remote access capability
// - encryptionEnabled: BOOLEAN - Encryption status
// - lastUpdate: DATETIME - Last update/patch date
// - vendorSupport: STRING - Vendor support status (active, limited, eol)
// - riskScore: FLOAT - Component risk score
// - mtbf: INTEGER - Mean time between failures (hours)
// - maintenanceSchedule: STRING - Maintenance schedule
// - certifications: LIST<STRING> - Component certifications
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (comp:Component {
  id: 'COMP-001',
  name: 'Train Control System',
  type: 'PLC',
  manufacturer: 'Rockwell Automation',
  model: 'ControlLogix 5580',
  version: '32.011',
  serialNumber: 'RA-CL5580-001',
  installDate: date('2020-01-15'),
  warrantyExpires: date('2025-01-15'),
  criticalityLevel: 'critical',
  functionDescription: 'Primary train control and safety system',
  networkConnected: true,
  hasRemoteAccess: true,
  encryptionEnabled: true,
  lastUpdate: datetime('2025-09-15T08:00:00'),
  vendorSupport: 'active',
  riskScore: 78.9,
  mtbf: 50000,
  maintenanceSchedule: 'quarterly',
  certifications: ['IEC 61508', 'EN 50128'],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 5: SOFTWARE
// Represents software packages and applications
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Software name
// - version: STRING - Software version
// - vendor: STRING - Software vendor
// - type: STRING - Software type (os, application, firmware, driver, middleware)
// - installDate: DATE - Installation date
// - licenseType: STRING - License type
// - licenseExpires: DATE - License expiration
// - purpose: STRING - Software purpose/function
// - criticalityLevel: STRING - Software criticality
// - hasKnownVulnerabilities: BOOLEAN - Known vulnerability flag
// - lastPatched: DATETIME - Last patch date
// - patchLevel: STRING - Current patch level
// - supportStatus: STRING - Vendor support status
// - endOfLife: DATE - End of life date
// - configFiles: LIST<STRING> - Configuration file paths
// - isOpenSource: BOOLEAN - Open source flag
// - sourceRepository: STRING - Source code repository URL
// - riskScore: FLOAT - Software risk score
// - cpe: STRING - Common Platform Enumeration identifier
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (sw:Software {
  id: 'SW-001',
  name: 'Windows Server',
  version: '2022',
  vendor: 'Microsoft',
  type: 'os',
  installDate: date('2022-03-01'),
  licenseType: 'enterprise',
  licenseExpires: date('2027-03-01'),
  purpose: 'Server operating system for train control network',
  criticalityLevel: 'critical',
  hasKnownVulnerabilities: true,
  lastPatched: datetime('2025-10-10T03:00:00'),
  patchLevel: 'KB5044284',
  supportStatus: 'active',
  endOfLife: date('2031-10-13'),
  configFiles: ['C:\\Windows\\System32\\config', 'C:\\ProgramData\\config.ini'],
  isOpenSource: false,
  sourceRepository: null,
  riskScore: 72.4,
  cpe: 'cpe:2.3:o:microsoft:windows_server_2022:-:*:*:*:*:*:*:*',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 6: LIBRARY
// Represents software libraries and dependencies
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Library name
// - version: STRING - Library version
// - language: STRING - Programming language
// - packageManager: STRING - Package manager (npm, pip, maven, nuget)
// - license: STRING - Software license
// - purpose: STRING - Library purpose
// - isOpenSource: BOOLEAN - Open source flag
// - repository: STRING - Source repository URL
// - lastUpdate: DATE - Last update date
// - hasKnownVulnerabilities: BOOLEAN - Known vulnerability flag
// - riskScore: FLOAT - Library risk score
// - popularity: INTEGER - Download/usage count
// - maintainerStatus: STRING - Maintenance status (active, maintained, abandoned)
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (lib:Library {
  id: 'LIB-001',
  name: 'log4j',
  version: '2.17.1',
  language: 'Java',
  packageManager: 'maven',
  license: 'Apache-2.0',
  purpose: 'Logging framework',
  isOpenSource: true,
  repository: 'https://github.com/apache/logging-log4j2',
  lastUpdate: date('2021-12-28'),
  hasKnownVulnerabilities: false,
  riskScore: 35.2,
  popularity: 10000000,
  maintainerStatus: 'active',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 7: NETWORKINTERFACE
// Represents network interfaces on components
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Interface name
// - type: STRING - Interface type (ethernet, wifi, serial, canbus)
// - ipAddress: STRING - IP address
// - macAddress: STRING - MAC address
// - subnetMask: STRING - Subnet mask
// - gateway: STRING - Default gateway
// - dnsServers: LIST<STRING> - DNS server addresses
// - vlanId: INTEGER - VLAN identifier
// - speed: INTEGER - Interface speed (Mbps)
// - status: STRING - Interface status (active, inactive, disabled)
// - isManagement: BOOLEAN - Management interface flag
// - securityLevel: STRING - Security classification
// - firewallEnabled: BOOLEAN - Firewall status
// - encryptionProtocol: STRING - Encryption protocol
// - lastActivity: DATETIME - Last activity timestamp
// - trafficVolume: INTEGER - Traffic volume (MB)
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (ni:NetworkInterface {
  id: 'NI-001',
  name: 'eth0',
  type: 'ethernet',
  ipAddress: '10.100.1.50',
  macAddress: '00:1A:2B:3C:4D:5E',
  subnetMask: '255.255.255.0',
  gateway: '10.100.1.1',
  dnsServers: ['10.100.1.10', '10.100.1.11'],
  vlanId: 100,
  speed: 1000,
  status: 'active',
  isManagement: false,
  securityLevel: 'high',
  firewallEnabled: true,
  encryptionProtocol: 'TLS 1.3',
  lastActivity: datetime('2025-10-29T10:00:00'),
  trafficVolume: 50000,
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 8: NETWORKSEGMENT
// Represents network segments/zones
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Segment name
// - type: STRING - Segment type (operational, management, dmz, public)
// - vlanId: INTEGER - VLAN identifier
// - ipRange: STRING - IP address range (CIDR notation)
// - securityZone: STRING - Security zone classification
// - purpose: STRING - Segment purpose
// - isolationLevel: STRING - Network isolation level
// - monitoringEnabled: BOOLEAN - Network monitoring status
// - idsEnabled: BOOLEAN - Intrusion detection status
// - ipsEnabled: BOOLEAN - Intrusion prevention status
// - accessControl: STRING - Access control policy
// - allowedProtocols: LIST<STRING> - Permitted protocols
// - riskScore: FLOAT - Segment risk score
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (ns:NetworkSegment {
  id: 'NS-001',
  name: 'Train Control Network',
  type: 'operational',
  vlanId: 100,
  ipRange: '10.100.0.0/16',
  securityZone: 'critical',
  purpose: 'Real-time train control and safety systems',
  isolationLevel: 'high',
  monitoringEnabled: true,
  idsEnabled: true,
  ipsEnabled: true,
  accessControl: 'whitelist',
  allowedProtocols: ['MODBUS', 'DNP3', 'IEC-104'],
  riskScore: 82.1,
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 9: FIREWALLRULE
// Represents firewall rules protecting network segments
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Rule name
// - priority: INTEGER - Rule priority/order
// - action: STRING - Rule action (allow, deny, log)
// - direction: STRING - Traffic direction (inbound, outbound, bidirectional)
// - sourceIp: STRING - Source IP address/range
// - destinationIp: STRING - Destination IP address/range
// - sourcePort: STRING - Source port/range
// - destinationPort: STRING - Destination port/range
// - protocol: STRING - Network protocol
// - enabled: BOOLEAN - Rule enabled status
// - logTraffic: BOOLEAN - Traffic logging status
// - description: STRING - Rule description
// - created: DATETIME - Rule creation timestamp
// - lastModified: DATETIME - Last modification timestamp
// - createdBy: STRING - Rule creator
// - reviewDate: DATE - Next review date

// Example:
CREATE (fr:FirewallRule {
  id: 'FR-001',
  name: 'Allow SCADA Traffic',
  priority: 100,
  action: 'allow',
  direction: 'bidirectional',
  sourceIp: '10.100.0.0/16',
  destinationIp: '10.200.0.0/16',
  sourcePort: 'any',
  destinationPort: '502',
  protocol: 'TCP',
  enabled: true,
  logTraffic: true,
  description: 'Allow MODBUS traffic between control and field networks',
  created: datetime('2025-01-15T10:00:00'),
  lastModified: datetime('2025-10-20T14:30:00'),
  createdBy: 'security-admin',
  reviewDate: date('2026-01-15')
});

// ============================================================================
// NODE TYPE 10: PROTOCOL
// Represents network protocols used in railway systems
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Protocol name
// - version: STRING - Protocol version
// - type: STRING - Protocol type (industrial, network, application)
// - port: INTEGER - Default port number
// - transportProtocol: STRING - Transport protocol (TCP, UDP)
// - isEncrypted: BOOLEAN - Encryption support
// - authenticationRequired: BOOLEAN - Authentication requirement
// - standard: STRING - Governing standard
// - commonUse: STRING - Common use case
// - knownVulnerabilities: INTEGER - Count of known vulnerabilities
// - riskLevel: STRING - Protocol risk level
// - description: STRING - Protocol description
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (p:Protocol {
  id: 'PROTO-001',
  name: 'MODBUS',
  version: 'TCP',
  type: 'industrial',
  port: 502,
  transportProtocol: 'TCP',
  isEncrypted: false,
  authenticationRequired: false,
  standard: 'MODBUS-IDA',
  commonUse: 'PLC communication and industrial control',
  knownVulnerabilities: 15,
  riskLevel: 'high',
  description: 'Industrial protocol for PLC and SCADA communication',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 11: CVE
// Represents Common Vulnerabilities and Exposures
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - CVE identifier (e.g., CVE-2021-44228)
// - description: STRING - Vulnerability description
// - severity: STRING - Severity level (critical, high, medium, low)
// - cvssScore: FLOAT - CVSS base score (0-10)
// - cvssVector: STRING - CVSS vector string
// - publishedDate: DATE - Publication date
// - lastModifiedDate: DATE - Last modification date
// - cweId: STRING - CWE identifier
// - attackVector: STRING - Attack vector (network, adjacent, local, physical)
// - attackComplexity: STRING - Attack complexity (low, high)
// - privilegesRequired: STRING - Privileges required (none, low, high)
// - userInteraction: STRING - User interaction (none, required)
// - scope: STRING - Scope (unchanged, changed)
// - confidentialityImpact: STRING - Confidentiality impact (none, low, high)
// - integrityImpact: STRING - Integrity impact (none, low, high)
// - availabilityImpact: STRING - Availability impact (none, low, high)
// - exploitAvailable: BOOLEAN - Public exploit availability
// - patchAvailable: BOOLEAN - Patch availability
// - workaroundAvailable: BOOLEAN - Workaround availability
// - status: STRING - Vulnerability status (active, patched, mitigated)
// - impact: STRING - Business impact description
// - mitigation: STRING - Mitigation guidance
// - references: LIST<STRING> - Reference URLs
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (cve:CVE {
  id: 'CVE-2021-44228',
  description: 'Apache Log4j2 JNDI features do not protect against attacker controlled LDAP and other JNDI related endpoints',
  severity: 'critical',
  cvssScore: 10.0,
  cvssVector: 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H',
  publishedDate: date('2021-12-10'),
  lastModifiedDate: date('2023-11-07'),
  cweId: 'CWE-502',
  attackVector: 'network',
  attackComplexity: 'low',
  privilegesRequired: 'none',
  userInteraction: 'none',
  scope: 'changed',
  confidentialityImpact: 'high',
  integrityImpact: 'high',
  availabilityImpact: 'high',
  exploitAvailable: true,
  patchAvailable: true,
  workaroundAvailable: true,
  status: 'patched',
  impact: 'Remote code execution, complete system compromise',
  mitigation: 'Upgrade to Log4j 2.17.1 or later, disable JNDI lookups',
  references: ['https://nvd.nist.gov/vuln/detail/CVE-2021-44228', 'https://logging.apache.org/log4j/2.x/security.html'],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 12: THREATACTOR
// Represents threat actors and adversary groups
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Threat actor name
// - aliases: LIST<STRING> - Known aliases
// - type: STRING - Actor type (nation_state, cybercrime, hacktivist, insider, terrorist)
// - sophisticationLevel: STRING - Sophistication (advanced, intermediate, basic)
// - primaryMotivation: STRING - Primary motivation (financial, espionage, ideology, revenge)
// - targetedSectors: LIST<STRING> - Targeted industry sectors
// - targetedCountries: LIST<STRING> - Targeted countries
// - firstSeen: DATE - First observation date
// - lastSeen: DATE - Most recent activity
// - isActive: BOOLEAN - Current activity status
// - attribution: STRING - Attribution confidence (confirmed, suspected, unknown)
// - capabilities: LIST<STRING> - Known capabilities
// - ttps: LIST<STRING> - Tactics, techniques, and procedures
// - infrastructure: STRING - Known infrastructure patterns
// - toolsUsed: LIST<STRING> - Known tools and malware
// - description: STRING - Threat actor description
// - riskLevel: STRING - Risk level to organization
// - intelligence: STRING - Additional intelligence notes
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (ta:ThreatActor {
  id: 'TA-001',
  name: 'APT28',
  aliases: ['Fancy Bear', 'Sofacy', 'STRONTIUM'],
  type: 'nation_state',
  sophisticationLevel: 'advanced',
  primaryMotivation: 'espionage',
  targetedSectors: ['Transportation', 'Critical Infrastructure', 'Government', 'Defense'],
  targetedCountries: ['United States', 'United Kingdom', 'Germany', 'France'],
  firstSeen: date('2007-01-01'),
  lastSeen: date('2025-10-15'),
  isActive: true,
  attribution: 'confirmed',
  capabilities: ['Zero-day exploitation', 'Social engineering', 'Supply chain attacks'],
  ttps: ['Spear phishing', 'Credential harvesting', 'Lateral movement', 'Data exfiltration'],
  infrastructure: 'Dynamic DNS, bulletproof hosting, compromised servers',
  toolsUsed: ['X-Agent', 'X-Tunnel', 'CHOPSTICK', 'Sofacy'],
  description: 'Russian state-sponsored APT group targeting critical infrastructure',
  riskLevel: 'critical',
  intelligence: 'Known to target railway control systems and operational technology',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 13: CAMPAIGN
// Represents coordinated threat campaigns
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - name: STRING - Campaign name
// - description: STRING - Campaign description
// - objectives: LIST<STRING> - Campaign objectives
// - startDate: DATE - Campaign start date
// - endDate: DATE - Campaign end date (if concluded)
// - status: STRING - Campaign status (active, concluded, suspected)
// - targetedIndustries: LIST<STRING> - Targeted industries
// - targetedRegions: LIST<STRING> - Targeted geographic regions
// - attackVectors: LIST<STRING> - Attack vectors used
// - indicators: LIST<STRING> - Indicators of compromise
// - victimCount: INTEGER - Number of known victims
// - impactLevel: STRING - Impact level (critical, high, medium, low)
// - detectionRate: FLOAT - Detection rate percentage
// - preventionGuidance: STRING - Prevention recommendations
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (camp:Campaign {
  id: 'CAMP-001',
  name: 'Operation Railway Disruption',
  description: 'Coordinated campaign targeting European railway infrastructure',
  objectives: ['Data exfiltration', 'System disruption', 'Intelligence gathering'],
  startDate: date('2025-06-01'),
  endDate: null,
  status: 'active',
  targetedIndustries: ['Rail Transport', 'Critical Infrastructure'],
  targetedRegions: ['Western Europe', 'United Kingdom'],
  attackVectors: ['Spear phishing', 'Supply chain compromise', 'Zero-day exploits'],
  indicators: ['185.220.101.X', 'malicious-domain.example', 'SHA256:abc123...'],
  victimCount: 12,
  impactLevel: 'high',
  detectionRate: 45.5,
  preventionGuidance: 'Enhanced monitoring, network segmentation, multi-factor authentication',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 14: ATTACKTECHNIQUE
// Represents MITRE ATT&CK techniques
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - mitreId: STRING - MITRE ATT&CK ID (e.g., T1059)
// - name: STRING - Technique name
// - tactic: STRING - ATT&CK tactic
// - description: STRING - Technique description
// - platforms: LIST<STRING> - Applicable platforms
// - dataSourcesRequired: LIST<STRING> - Data sources for detection
// - detection: STRING - Detection guidance
// - mitigation: STRING - Mitigation strategies
// - examples: LIST<STRING> - Real-world examples
// - subtechniques: LIST<STRING> - Related sub-techniques
// - difficulty: STRING - Exploitation difficulty (low, medium, high)
// - commonInRailway: BOOLEAN - Common in railway sector
// - riskLevel: STRING - Risk level
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (at:AttackTechnique {
  id: 'ATK-001',
  mitreId: 'T1059.001',
  name: 'PowerShell',
  tactic: 'Execution',
  description: 'Adversaries abuse PowerShell commands and scripts for execution',
  platforms: ['Windows'],
  dataSourcesRequired: ['Process monitoring', 'PowerShell logs', 'Script block logging'],
  detection: 'Monitor PowerShell execution and command-line arguments for suspicious activity',
  mitigation: 'Execution prevention, code signing, application control',
  examples: ['APT28', 'APT29', 'FIN7'],
  subtechniques: ['T1059.001'],
  difficulty: 'low',
  commonInRailway: true,
  riskLevel: 'high',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// NODE TYPE 15: DOCUMENT
// Represents security documents, reports, and policies
// ============================================================================

// Properties:
// - id: STRING (UNIQUE) - Unique identifier
// - title: STRING - Document title
// - type: STRING - Document type (policy, report, assessment, procedure, standard)
// - content: STRING - Document content/summary
// - summary: STRING - Executive summary
// - author: STRING - Document author
// - version: STRING - Document version
// - status: STRING - Document status (draft, published, archived)
// - classification: STRING - Security classification
// - createdDate: DATE - Creation date
// - publishedDate: DATE - Publication date
// - reviewDate: DATE - Next review date
// - expiryDate: DATE - Expiry date
// - approvedBy: STRING - Approval authority
// - tags: LIST<STRING> - Document tags
// - relatedStandards: LIST<STRING> - Related standards
// - filePath: STRING - File storage path
// - fileHash: STRING - Document hash for integrity
// - created: DATETIME - Record creation timestamp
// - modified: DATETIME - Record modification timestamp

// Example:
CREATE (doc:Document {
  id: 'DOC-001',
  title: 'Railway Cybersecurity Assessment Report 2025',
  type: 'assessment',
  content: 'Comprehensive security assessment of railway control systems...',
  summary: 'Annual security assessment identifying 45 vulnerabilities across operational technology systems',
  author: 'Security Team',
  version: '1.0',
  status: 'published',
  classification: 'confidential',
  createdDate: date('2025-09-01'),
  publishedDate: date('2025-10-01'),
  reviewDate: date('2026-10-01'),
  expiryDate: date('2028-10-01'),
  approvedBy: 'Chief Security Officer',
  tags: ['cybersecurity', 'assessment', 'railway', 'OT'],
  relatedStandards: ['IEC 62443', 'NIST CSF', 'ISO 27001'],
  filePath: '/secure/documents/assessments/2025/railway-assessment.pdf',
  fileHash: 'SHA256:def456...',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// END OF NODE DEFINITIONS
// ============================================================================
