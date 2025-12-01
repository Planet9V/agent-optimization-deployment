// ============================================================================
// AEON DIGITAL TWIN CYBER SECURITY THREAT INTELLIGENCE
// Sample Data for Testing and Development
// Version: 1.0.0
// Created: 2025-10-29
// ============================================================================

// ============================================================================
// SAMPLE ORGANIZATIONS (3)
// ============================================================================

CREATE (org1:Organization {
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

CREATE (org2:Organization {
  id: 'ORG-002',
  name: 'Siemens Mobility',
  type: 'manufacturer',
  country: 'Germany',
  sector: 'Rail Equipment Manufacturing',
  employees: 38000,
  website: 'https://mobility.siemens.com',
  contactEmail: 'contact@siemens.com',
  foundedDate: date('1847-01-01'),
  description: 'Leading railway equipment and systems manufacturer',
  riskScore: 45.2,
  lastAssessmentDate: datetime('2025-10-01T09:00:00'),
  certifications: ['ISO 27001', 'IEC 62443', 'ISO 9001'],
  created: datetime(),
  modified: datetime()
});

CREATE (org3:Organization {
  id: 'ORG-003',
  name: 'European Rail Agency',
  type: 'regulator',
  country: 'European Union',
  sector: 'Railway Regulation',
  employees: 200,
  website: 'https://era.europa.eu',
  contactEmail: 'info@era.europa.eu',
  foundedDate: date('2004-04-29'),
  description: 'European Union railway safety and interoperability authority',
  riskScore: 35.8,
  lastAssessmentDate: datetime('2025-09-20T11:00:00'),
  certifications: ['ISO 27001'],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE SITES (10)
// ============================================================================

CREATE (site1:Site {
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
  emergencyContacts: ['+44-20-1234-5678'],
  created: datetime(),
  modified: datetime()
});

CREATE (site2:Site {
  id: 'SITE-002',
  name: 'North Depot',
  type: 'depot',
  location: '45 Maintenance Road, Manchester, UK',
  coordinates: point({latitude: 53.4808, longitude: -2.2426}),
  operationalStatus: 'active',
  capacity: 100,
  securityLevel: 'high',
  hasPublicAccess: false,
  criticalityLevel: 'high',
  riskScore: 68.5,
  lastInspection: date('2025-10-18'),
  emergencyContacts: ['+44-161-1234-5678'],
  created: datetime(),
  modified: datetime()
});

CREATE (site3:Site {
  id: 'SITE-003',
  name: 'Network Control Center',
  type: 'control_center',
  location: '10 Control Drive, Birmingham, UK',
  coordinates: point({latitude: 52.4862, longitude: -1.8904}),
  operationalStatus: 'active',
  capacity: 50,
  securityLevel: 'critical',
  hasPublicAccess: false,
  criticalityLevel: 'critical',
  riskScore: 85.2,
  lastInspection: date('2025-10-25'),
  emergencyContacts: ['+44-121-1234-5678'],
  created: datetime(),
  modified: datetime()
});

// Add 7 more sites (SITE-004 to SITE-010)
CREATE (site4:Site {id: 'SITE-004', name: 'East Station', type: 'station', location: 'Edinburgh, UK', coordinates: point({latitude: 55.9533, longitude: -3.1883}), operationalStatus: 'active', capacity: 30000, securityLevel: 'medium', hasPublicAccess: true, criticalityLevel: 'high', riskScore: 65.0, lastInspection: date('2025-10-15'), emergencyContacts: ['+44-131-1234-5678'], created: datetime(), modified: datetime()});
CREATE (site5:Site {id: 'SITE-005', name: 'South Maintenance', type: 'maintenance', location: 'Bristol, UK', coordinates: point({latitude: 51.4545, longitude: -2.5879}), operationalStatus: 'active', capacity: 25, securityLevel: 'medium', hasPublicAccess: false, criticalityLevel: 'medium', riskScore: 55.3, lastInspection: date('2025-10-10'), emergencyContacts: ['+44-117-1234-5678'], created: datetime(), modified: datetime()});
CREATE (site6:Site {id: 'SITE-006', name: 'West Junction', type: 'station', location: 'Liverpool, UK', coordinates: point({latitude: 53.4084, longitude: -2.9916}), operationalStatus: 'active', capacity: 20000, securityLevel: 'medium', hasPublicAccess: true, criticalityLevel: 'medium', riskScore: 62.1, lastInspection: date('2025-10-12'), emergencyContacts: ['+44-151-1234-5678'], created: datetime(), modified: datetime()});
CREATE (site7:Site {id: 'SITE-007', name: 'Training Center', type: 'maintenance', location: 'Leeds, UK', coordinates: point({latitude: 53.8008, longitude: -1.5491}), operationalStatus: 'active', capacity: 30, securityLevel: 'low', hasPublicAccess: false, criticalityLevel: 'low', riskScore: 42.7, lastInspection: date('2025-09-30'), emergencyContacts: ['+44-113-1234-5678'], created: datetime(), modified: datetime()});
CREATE (site8:Site {id: 'SITE-008', name: 'Emergency Depot', type: 'depot', location: 'Glasgow, UK', coordinates: point({latitude: 55.8642, longitude: -4.2518}), operationalStatus: 'active', capacity: 50, securityLevel: 'high', hasPublicAccess: false, criticalityLevel: 'high', riskScore: 70.5, lastInspection: date('2025-10-22'), emergencyContacts: ['+44-141-1234-5678'], created: datetime(), modified: datetime()});
CREATE (site9:Site {id: 'SITE-009', name: 'Regional Hub', type: 'station', location: 'Newcastle, UK', coordinates: point({latitude: 54.9783, longitude: -1.6178}), operationalStatus: 'active', capacity: 25000, securityLevel: 'medium', hasPublicAccess: true, criticalityLevel: 'medium', riskScore: 58.9, lastInspection: date('2025-10-08'), emergencyContacts: ['+44-191-1234-5678'], created: datetime(), modified: datetime()});
CREATE (site10:Site {id: 'SITE-010', name: 'Backup Control', type: 'control_center', location: 'Sheffield, UK', coordinates: point({latitude: 53.3811, longitude: -1.4701}), operationalStatus: 'standby', capacity: 30, securityLevel: 'critical', hasPublicAccess: false, criticalityLevel: 'critical', riskScore: 78.3, lastInspection: date('2025-10-20'), emergencyContacts: ['+44-114-1234-5678'], created: datetime(), modified: datetime()});

// ============================================================================
// SAMPLE TRAINS (20)
// ============================================================================

CREATE (train1:Train {
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

// Generate remaining 19 trains (TRAIN-002 to TRAIN-020)
UNWIND range(2, 20) AS i
CREATE (train:Train {
  id: 'TRAIN-' + toString(i),
  name: 'Express-' + ['Alpha', 'Beta', 'Gamma', 'Delta'][i % 4] + '-' + toString(i),
  type: ['high_speed', 'passenger', 'freight', 'metro'][i % 4],
  model: 'Model-' + toString(i),
  manufacturer: ['Siemens Mobility', 'Alstom', 'Bombardier', 'Hitachi'][i % 4],
  yearBuilt: 2015 + (i % 8),
  serialNumber: 'SER-' + toString(i) + '-2020',
  capacity: 200 + (i * 10),
  maxSpeed: 150 + (i * 5),
  powerType: ['electric', 'diesel', 'hybrid'][i % 3],
  status: ['active', 'maintenance'][i % 2],
  lastMaintenance: date('2025-' + toString((i % 12) + 1) + '-01'),
  nextMaintenance: date('2025-' + toString(((i % 12) + 2) % 12 + 1) + '-01'),
  operatingRoute: 'Route-' + toString(i),
  criticalityLevel: ['critical', 'high', 'medium'][i % 3],
  riskScore: 50.0 + (i * 1.5),
  mileage: 100000 + (i * 50000),
  certifications: ['EN 15227', 'TSI'],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE COMPONENTS (100) - Critical OT/ICS Components
// ============================================================================

// Create 100 diverse components
UNWIND range(1, 100) AS i
CREATE (comp:Component {
  id: 'COMP-' + toString(i),
  name: ['Train Control System', 'SCADA Server', 'PLC Controller', 'HMI Panel', 'Safety Relay', 'Door Controller', 'HVAC System', 'Brake Controller', 'Signal Processor', 'Communication Gateway'][i % 10],
  type: ['PLC', 'SCADA', 'sensor', 'controller', 'actuator', 'display', 'gateway', 'relay'][i % 8],
  manufacturer: ['Rockwell Automation', 'Siemens', 'Schneider Electric', 'ABB', 'Honeywell'][i % 5],
  model: 'Model-' + toString(i),
  version: toString((i % 5) + 1) + '.' + toString(i % 10),
  serialNumber: 'SN-' + toString(i) + '-2020',
  installDate: date('2020-' + toString((i % 12) + 1) + '-' + toString((i % 28) + 1)),
  warrantyExpires: date('2025-' + toString((i % 12) + 1) + '-' + toString((i % 28) + 1)),
  criticalityLevel: ['critical', 'high', 'medium', 'low'][i % 4],
  functionDescription: 'Critical railway control component',
  networkConnected: true,
  hasRemoteAccess: (i % 3 = 0),
  encryptionEnabled: (i % 2 = 0),
  lastUpdate: datetime('2025-' + toString((i % 12) + 1) + '-01T08:00:00'),
  vendorSupport: ['active', 'limited', 'eol'][i % 3],
  riskScore: 40.0 + (i * 0.4),
  mtbf: 20000 + (i * 500),
  maintenanceSchedule: ['monthly', 'quarterly', 'annually'][i % 3],
  certifications: ['IEC 61508', 'EN 50128'],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE SOFTWARE (200) - OS, Applications, Firmware
// ============================================================================

UNWIND range(1, 200) AS i
CREATE (sw:Software {
  id: 'SW-' + toString(i),
  name: ['Windows Server', 'Linux RHEL', 'VxWorks', 'QNX', 'SCADA Software', 'Control Logic', 'HMI Application', 'Firewall Software'][i % 8],
  version: toString((i % 10) + 1) + '.' + toString(i % 10) + '.' + toString(i % 5),
  vendor: ['Microsoft', 'Red Hat', 'Wind River', 'BlackBerry', 'Schneider Electric', 'Rockwell', 'Siemens'][i % 7],
  type: ['os', 'application', 'firmware', 'driver', 'middleware'][i % 5],
  installDate: date('2020-' + toString((i % 12) + 1) + '-' + toString((i % 28) + 1)),
  licenseType: ['enterprise', 'standard', 'oem'][i % 3],
  licenseExpires: date('2027-' + toString((i % 12) + 1) + '-' + toString((i % 28) + 1)),
  purpose: 'Railway control system software',
  criticalityLevel: ['critical', 'high', 'medium', 'low'][i % 4],
  hasKnownVulnerabilities: (i % 5 = 0),
  lastPatched: datetime('2025-' + toString((i % 12) + 1) + '-01T03:00:00'),
  patchLevel: 'v' + toString(i),
  supportStatus: ['active', 'limited', 'eol'][i % 3],
  endOfLife: date('2030-' + toString((i % 12) + 1) + '-01'),
  configFiles: ['/etc/config/app.conf'],
  isOpenSource: (i % 4 = 0),
  sourceRepository: CASE WHEN i % 4 = 0 THEN 'https://github.com/example/repo' ELSE null END,
  riskScore: 30.0 + (i * 0.3),
  cpe: 'cpe:2.3:a:vendor:product:' + toString(i),
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE LIBRARIES (50) - Software Dependencies
// ============================================================================

UNWIND range(1, 50) AS i
CREATE (lib:Library {
  id: 'LIB-' + toString(i),
  name: ['log4j', 'openssl', 'jackson', 'spring', 'commons-io', 'gson', 'netty', 'apache-http'][i % 8],
  version: toString((i % 5) + 1) + '.' + toString(i % 20) + '.' + toString(i % 10),
  language: ['Java', 'C', 'C++', 'Python', 'JavaScript'][i % 5],
  packageManager: ['maven', 'npm', 'pip', 'nuget'][i % 4],
  license: ['Apache-2.0', 'MIT', 'GPL-3.0', 'BSD-3-Clause'][i % 4],
  purpose: 'Software library dependency',
  isOpenSource: true,
  repository: 'https://github.com/apache/library-' + toString(i),
  lastUpdate: date('2025-' + toString((i % 12) + 1) + '-01'),
  hasKnownVulnerabilities: (i % 10 = 0),
  riskScore: 20.0 + (i * 0.5),
  popularity: 1000000 + (i * 100000),
  maintainerStatus: ['active', 'maintained', 'abandoned'][i % 3],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE CVES (500) - Vulnerabilities
// ============================================================================

// Create Log4Shell as specific example
CREATE (cve_log4j:CVE {
  id: 'CVE-2021-44228',
  description: 'Apache Log4j2 JNDI features do not protect against attacker controlled LDAP endpoints',
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
  mitigation: 'Upgrade to Log4j 2.17.1 or later',
  references: ['https://nvd.nist.gov/vuln/detail/CVE-2021-44228'],
  created: datetime(),
  modified: datetime()
});

// Generate remaining 499 CVEs
UNWIND range(1, 499) AS i
CREATE (cve:CVE {
  id: 'CVE-2024-' + toString(10000 + i),
  description: 'Security vulnerability in railway control system component',
  severity: ['critical', 'high', 'medium', 'low'][i % 4],
  cvssScore: 4.0 + ((i % 7) * 1.0),
  cvssVector: 'CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L',
  publishedDate: date('2024-' + toString((i % 12) + 1) + '-' + toString((i % 28) + 1)),
  lastModifiedDate: date('2025-' + toString((i % 12) + 1) + '-01'),
  cweId: 'CWE-' + toString(20 + (i % 100)),
  attackVector: ['network', 'adjacent', 'local', 'physical'][i % 4],
  attackComplexity: ['low', 'high'][i % 2],
  privilegesRequired: ['none', 'low', 'high'][i % 3],
  userInteraction: ['none', 'required'][i % 2],
  scope: ['unchanged', 'changed'][i % 2],
  confidentialityImpact: ['none', 'low', 'high'][i % 3],
  integrityImpact: ['none', 'low', 'high'][i % 3],
  availabilityImpact: ['none', 'low', 'high'][i % 3],
  exploitAvailable: (i % 5 = 0),
  patchAvailable: (i % 3 = 0),
  workaroundAvailable: (i % 4 = 0),
  status: ['active', 'patched', 'mitigated'][i % 3],
  impact: 'Potential security compromise',
  mitigation: 'Apply vendor patches and security updates',
  references: ['https://nvd.nist.gov/vuln/detail/CVE-2024-' + toString(10000 + i)],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE NETWORK INTERFACES (150)
// ============================================================================

UNWIND range(1, 150) AS i
CREATE (ni:NetworkInterface {
  id: 'NI-' + toString(i),
  name: 'eth' + toString(i % 10),
  type: ['ethernet', 'wifi', 'serial', 'canbus'][i % 4],
  ipAddress: '10.' + toString((i % 254) + 1) + '.' + toString((i % 254) + 1) + '.' + toString((i % 254) + 1),
  macAddress: '00:1A:2B:3C:' + toString(i % 256) + ':' + toString((i * 2) % 256),
  subnetMask: '255.255.255.0',
  gateway: '10.' + toString((i % 254) + 1) + '.' + toString((i % 254) + 1) + '.1',
  dnsServers: ['10.0.0.10', '10.0.0.11'],
  vlanId: 100 + (i % 50),
  speed: [100, 1000, 10000][i % 3],
  status: ['active', 'inactive', 'disabled'][i % 3],
  isManagement: (i % 10 = 0),
  securityLevel: ['high', 'medium', 'low'][i % 3],
  firewallEnabled: (i % 2 = 0),
  encryptionProtocol: ['TLS 1.3', 'TLS 1.2', 'None'][i % 3],
  lastActivity: datetime('2025-10-29T10:00:00'),
  trafficVolume: 1000 + (i * 100),
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE NETWORK SEGMENTS (20)
// ============================================================================

UNWIND range(1, 20) AS i
CREATE (ns:NetworkSegment {
  id: 'NS-' + toString(i),
  name: ['Control Network', 'Management Network', 'DMZ', 'Public Network', 'Sensor Network'][i % 5],
  type: ['operational', 'management', 'dmz', 'public'][i % 4],
  vlanId: 100 + i,
  ipRange: '10.' + toString(i) + '.0.0/16',
  securityZone: ['critical', 'high', 'medium', 'low'][i % 4],
  purpose: 'Network segment for railway operations',
  isolationLevel: ['high', 'medium', 'low'][i % 3],
  monitoringEnabled: true,
  idsEnabled: (i % 2 = 0),
  ipsEnabled: (i % 3 = 0),
  accessControl: ['whitelist', 'blacklist'][i % 2],
  allowedProtocols: ['MODBUS', 'DNP3', 'IEC-104'],
  riskScore: 50.0 + (i * 2.0),
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE FIREWALL RULES (50)
// ============================================================================

UNWIND range(1, 50) AS i
CREATE (fr:FirewallRule {
  id: 'FR-' + toString(i),
  name: 'Rule-' + toString(i),
  priority: i * 10,
  action: ['allow', 'deny', 'log'][i % 3],
  direction: ['inbound', 'outbound', 'bidirectional'][i % 3],
  sourceIp: '10.' + toString((i % 254) + 1) + '.0.0/16',
  destinationIp: '10.' + toString(((i + 1) % 254) + 1) + '.0.0/16',
  sourcePort: 'any',
  destinationPort: toString(80 + (i * 10)),
  protocol: ['TCP', 'UDP', 'ICMP'][i % 3],
  enabled: true,
  logTraffic: (i % 2 = 0),
  description: 'Firewall rule for network traffic control',
  created: datetime('2025-01-15T10:00:00'),
  lastModified: datetime('2025-10-20T14:30:00'),
  createdBy: 'security-admin',
  reviewDate: date('2026-01-15')
});

// ============================================================================
// SAMPLE PROTOCOLS (10)
// ============================================================================

CREATE (p1:Protocol {id: 'PROTO-001', name: 'MODBUS', version: 'TCP', type: 'industrial', port: 502, transportProtocol: 'TCP', isEncrypted: false, authenticationRequired: false, standard: 'MODBUS-IDA', commonUse: 'PLC communication', knownVulnerabilities: 15, riskLevel: 'high', description: 'Industrial protocol for PLC/SCADA', created: datetime(), modified: datetime()});
CREATE (p2:Protocol {id: 'PROTO-002', name: 'DNP3', version: '3.0', type: 'industrial', port: 20000, transportProtocol: 'TCP', isEncrypted: false, authenticationRequired: false, standard: 'IEEE 1815', commonUse: 'SCADA communication', knownVulnerabilities: 8, riskLevel: 'high', description: 'SCADA protocol', created: datetime(), modified: datetime()});
CREATE (p3:Protocol {id: 'PROTO-003', name: 'IEC-104', version: '2.0', type: 'industrial', port: 2404, transportProtocol: 'TCP', isEncrypted: false, authenticationRequired: false, standard: 'IEC 60870-5-104', commonUse: 'Power system monitoring', knownVulnerabilities: 12, riskLevel: 'high', description: 'Power automation protocol', created: datetime(), modified: datetime()});
CREATE (p4:Protocol {id: 'PROTO-004', name: 'OPC-UA', version: '1.04', type: 'industrial', port: 4840, transportProtocol: 'TCP', isEncrypted: true, authenticationRequired: true, standard: 'IEC 62541', commonUse: 'Industrial data exchange', knownVulnerabilities: 3, riskLevel: 'medium', description: 'Secure industrial communication', created: datetime(), modified: datetime()});
CREATE (p5:Protocol {id: 'PROTO-005', name: 'PROFINET', version: '2.4', type: 'industrial', port: 34964, transportProtocol: 'UDP', isEncrypted: false, authenticationRequired: false, standard: 'IEC 61158', commonUse: 'Factory automation', knownVulnerabilities: 5, riskLevel: 'medium', description: 'Industrial Ethernet', created: datetime(), modified: datetime()});
CREATE (p6:Protocol {id: 'PROTO-006', name: 'EtherCAT', version: '1.0', type: 'industrial', port: null, transportProtocol: 'Ethernet', isEncrypted: false, authenticationRequired: false, standard: 'IEC 61158', commonUse: 'Real-time control', knownVulnerabilities: 2, riskLevel: 'low', description: 'High-performance fieldbus', created: datetime(), modified: datetime()});
CREATE (p7:Protocol {id: 'PROTO-007', name: 'CAN-bus', version: '2.0', type: 'industrial', port: null, transportProtocol: 'CAN', isEncrypted: false, authenticationRequired: false, standard: 'ISO 11898', commonUse: 'Vehicle networks', knownVulnerabilities: 10, riskLevel: 'high', description: 'Vehicle communication bus', created: datetime(), modified: datetime()});
CREATE (p8:Protocol {id: 'PROTO-008', name: 'MQTT', version: '5.0', type: 'application', port: 1883, transportProtocol: 'TCP', isEncrypted: false, authenticationRequired: true, standard: 'OASIS', commonUse: 'IoT messaging', knownVulnerabilities: 4, riskLevel: 'medium', description: 'IoT publish/subscribe', created: datetime(), modified: datetime()});
CREATE (p9:Protocol {id: 'PROTO-009', name: 'AMQP', version: '1.0', type: 'application', port: 5672, transportProtocol: 'TCP', isEncrypted: true, authenticationRequired: true, standard: 'OASIS', commonUse: 'Message queuing', knownVulnerabilities: 2, riskLevel: 'low', description: 'Enterprise messaging', created: datetime(), modified: datetime()});
CREATE (p10:Protocol {id: 'PROTO-010', name: 'HTTPS', version: '1.1', type: 'network', port: 443, transportProtocol: 'TCP', isEncrypted: true, authenticationRequired: false, standard: 'RFC 2616', commonUse: 'Web traffic', knownVulnerabilities: 20, riskLevel: 'medium', description: 'Secure web protocol', created: datetime(), modified: datetime()});

// ============================================================================
// SAMPLE THREAT ACTORS (10)
// ============================================================================

CREATE (ta1:ThreatActor {id: 'TA-001', name: 'APT28', aliases: ['Fancy Bear', 'Sofacy'], type: 'nation_state', sophisticationLevel: 'advanced', primaryMotivation: 'espionage', targetedSectors: ['Transportation', 'Critical Infrastructure'], targetedCountries: ['United Kingdom', 'Germany'], firstSeen: date('2007-01-01'), lastSeen: date('2025-10-15'), isActive: true, attribution: 'confirmed', capabilities: ['Zero-day exploitation', 'Social engineering'], ttps: ['Spear phishing', 'Lateral movement'], infrastructure: 'Dynamic DNS', toolsUsed: ['X-Agent', 'X-Tunnel'], description: 'Russian APT group', riskLevel: 'critical', intelligence: 'Targets railway systems', created: datetime(), modified: datetime()});

UNWIND range(2, 10) AS i
CREATE (ta:ThreatActor {
  id: 'TA-' + toString(i),
  name: 'ThreatGroup-' + toString(i),
  aliases: ['Alias-' + toString(i)],
  type: ['nation_state', 'cybercrime', 'hacktivist', 'insider'][i % 4],
  sophisticationLevel: ['advanced', 'intermediate', 'basic'][i % 3],
  primaryMotivation: ['financial', 'espionage', 'ideology', 'revenge'][i % 4],
  targetedSectors: ['Transportation', 'Energy', 'Finance'],
  targetedCountries: ['United Kingdom', 'United States', 'Germany'],
  firstSeen: date('201' + toString(i % 10) + '-01-01'),
  lastSeen: date('2025-10-01'),
  isActive: (i % 2 = 0),
  attribution: ['confirmed', 'suspected', 'unknown'][i % 3],
  capabilities: ['Malware development', 'Network exploitation'],
  ttps: ['Phishing', 'Ransomware'],
  infrastructure: 'Cloud hosting',
  toolsUsed: ['Custom malware'],
  description: 'Threat actor targeting critical infrastructure',
  riskLevel: ['critical', 'high', 'medium'][i % 3],
  intelligence: 'Active threat',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE CAMPAIGNS (5)
// ============================================================================

UNWIND range(1, 5) AS i
CREATE (camp:Campaign {
  id: 'CAMP-' + toString(i),
  name: 'Campaign-' + toString(i),
  description: 'Coordinated attack campaign targeting railway infrastructure',
  objectives: ['Data exfiltration', 'System disruption'],
  startDate: date('2025-0' + toString(i) + '-01'),
  endDate: null,
  status: ['active', 'concluded'][i % 2],
  targetedIndustries: ['Rail Transport', 'Critical Infrastructure'],
  targetedRegions: ['Western Europe', 'United Kingdom'],
  attackVectors: ['Spear phishing', 'Supply chain'],
  indicators: ['malicious-domain-' + toString(i) + '.example'],
  victimCount: i * 5,
  impactLevel: ['critical', 'high', 'medium'][i % 3],
  detectionRate: 40.0 + (i * 5.0),
  preventionGuidance: 'Enhanced monitoring and segmentation',
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE ATTACK TECHNIQUES (20 - MITRE ATT&CK)
// ============================================================================

CREATE (at1:AttackTechnique {id: 'ATK-001', mitreId: 'T1059.001', name: 'PowerShell', tactic: 'Execution', description: 'Adversaries abuse PowerShell for execution', platforms: ['Windows'], dataSourcesRequired: ['Process monitoring', 'PowerShell logs'], detection: 'Monitor PowerShell execution', mitigation: 'Execution prevention', examples: ['APT28', 'APT29'], subtechniques: [], difficulty: 'low', commonInRailway: true, riskLevel: 'high', created: datetime(), modified: datetime()});
CREATE (at2:AttackTechnique {id: 'ATK-002', mitreId: 'T1190', name: 'Exploit Public-Facing Application', tactic: 'Initial Access', description: 'Exploit software vulnerabilities in Internet-facing systems', platforms: ['Windows', 'Linux'], dataSourcesRequired: ['Network traffic', 'Application logs'], detection: 'Monitor for exploitation attempts', mitigation: 'Patch management', examples: ['Multiple threat actors'], subtechniques: [], difficulty: 'medium', commonInRailway: true, riskLevel: 'critical', created: datetime(), modified: datetime()});
CREATE (at3:AttackTechnique {id: 'ATK-003', mitreId: 'T1566.001', name: 'Spearphishing Attachment', tactic: 'Initial Access', description: 'Send malicious attachments to gain access', platforms: ['Windows', 'macOS', 'Linux'], dataSourcesRequired: ['Email gateway', 'Endpoint detection'], detection: 'Email attachment scanning', mitigation: 'User training', examples: ['APT28', 'FIN7'], subtechniques: [], difficulty: 'low', commonInRailway: true, riskLevel: 'high', created: datetime(), modified: datetime()});

UNWIND range(4, 20) AS i
CREATE (at:AttackTechnique {
  id: 'ATK-' + toString(i),
  mitreId: 'T' + toString(1000 + i),
  name: 'Technique-' + toString(i),
  tactic: ['Initial Access', 'Execution', 'Persistence', 'Privilege Escalation', 'Defense Evasion'][i % 5],
  description: 'Attack technique description',
  platforms: ['Windows', 'Linux'],
  dataSourcesRequired: ['Process monitoring', 'Network traffic'],
  detection: 'Detection guidance',
  mitigation: 'Mitigation strategies',
  examples: ['ThreatActor-' + toString(i)],
  subtechniques: [],
  difficulty: ['low', 'medium', 'high'][i % 3],
  commonInRailway: (i % 2 = 0),
  riskLevel: ['critical', 'high', 'medium'][i % 3],
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// SAMPLE DOCUMENTS (10)
// ============================================================================

UNWIND range(1, 10) AS i
CREATE (doc:Document {
  id: 'DOC-' + toString(i),
  title: 'Security Document ' + toString(i),
  type: ['policy', 'report', 'assessment', 'procedure', 'standard'][i % 5],
  content: 'Document content and analysis',
  summary: 'Executive summary of document',
  author: 'Security Team',
  version: '1.' + toString(i % 10),
  status: ['draft', 'published', 'archived'][i % 3],
  classification: ['confidential', 'internal', 'public'][i % 3],
  createdDate: date('2025-0' + toString((i % 9) + 1) + '-01'),
  publishedDate: date('2025-' + toString((i % 12) + 1) + '-01'),
  reviewDate: date('2026-' + toString((i % 12) + 1) + '-01'),
  expiryDate: date('2028-01-01'),
  approvedBy: 'Chief Security Officer',
  tags: ['cybersecurity', 'railway', 'assessment'],
  relatedStandards: ['IEC 62443', 'ISO 27001'],
  filePath: '/secure/documents/doc-' + toString(i) + '.pdf',
  fileHash: 'SHA256:hash' + toString(i),
  created: datetime(),
  modified: datetime()
});

// ============================================================================
// CREATE RELATIONSHIPS - Complete Graph
// ============================================================================

// Organizations operate Sites
MATCH (org:Organization {id: 'ORG-001'}), (site:Site)
WHERE site.id IN ['SITE-001', 'SITE-002', 'SITE-003', 'SITE-004', 'SITE-005']
CREATE (org)-[:OPERATES {since: date('2015-01-01'), contractExpiry: date('2030-12-31'), operationalRole: 'primary_operator', responsibilityLevel: 'full'}]->(site);

// Sites host Trains
MATCH (site:Site), (train:Train)
WHERE site.id IN ['SITE-001', 'SITE-002'] AND train.id STARTS WITH 'TRAIN-'
CREATE (site)-[:HOSTS {frequency: 'daily', capacity: 10, serviceType: 'passenger'}]->(train);

// Trains have Components
MATCH (train:Train), (comp:Component)
WHERE train.id STARTS WITH 'TRAIN-' AND comp.id STARTS WITH 'COMP-'
WITH train, comp LIMIT 200
CREATE (train)-[:HAS_COMPONENT {installDate: date('2020-01-15'), location: 'control_cabin', isRedundant: false, maintenanceResponsibility: 'operator'}]->(comp);

// Components run Software
MATCH (comp:Component), (sw:Software)
WHERE comp.id STARTS WITH 'COMP-' AND sw.id STARTS WITH 'SW-'
WITH comp, sw LIMIT 300
CREATE (comp)-[:RUNS_SOFTWARE {installDate: datetime('2020-01-15T10:00:00'), configurationId: 'CFG-001', isActive: true, startupOrder: 1}]->(sw);

// Software depends on Libraries
MATCH (sw:Software), (lib:Library)
WHERE sw.id STARTS WITH 'SW-' AND lib.id STARTS WITH 'LIB-'
WITH sw, lib LIMIT 150
CREATE (sw)-[:DEPENDS_ON {versionConstraint: '>=1.0.0', dependencyType: 'runtime', isTransitive: false, declaredIn: 'pom.xml'}]->(lib);

// Software/Libraries have Vulnerabilities
MATCH (sw:Software {id: 'SW-001'}), (cve:CVE {id: 'CVE-2021-44228'})
CREATE (sw)-[:HAS_VULNERABILITY {discoveredDate: date('2021-12-10'), affectedVersions: ['2.x'], exploited: false, patchedInVersion: '2.17.1', mitigationStatus: 'patched', riskScore: 95.5}]->(cve);

MATCH (lib:Library {id: 'LIB-001'}), (cve:CVE {id: 'CVE-2021-44228'})
CREATE (lib)-[:HAS_VULNERABILITY {discoveredDate: date('2021-12-10'), affectedVersions: ['2.0-2.16'], exploited: false, patchedInVersion: '2.17.1', mitigationStatus: 'patched', riskScore: 98.0}]->(cve);

// Components have Network Interfaces
MATCH (comp:Component), (ni:NetworkInterface)
WHERE comp.id STARTS WITH 'COMP-' AND ni.id STARTS WITH 'NI-'
WITH comp, ni LIMIT 150
CREATE (comp)-[:HAS_INTERFACE {purpose: 'operational', isManagement: false, isPrimary: true}]->(ni);

// Network Interfaces belong to Segments
MATCH (ni:NetworkInterface), (ns:NetworkSegment)
WHERE ni.id STARTS WITH 'NI-' AND ns.id STARTS WITH 'NS-'
WITH ni, ns LIMIT 150
CREATE (ni)-[:BELONGS_TO {assignedDate: date('2020-01-15'), isStatic: true, priority: 1}]->(ns);

// Network Segments connect to each other
MATCH (ns1:NetworkSegment), (ns2:NetworkSegment)
WHERE ns1.id < ns2.id
WITH ns1, ns2 LIMIT 30
CREATE (ns1)-[:CONNECTS_TO {connectionType: 'routed', bandwidth: 1000, latency: 5, isEncrypted: true, routingProtocol: 'OSPF'}]->(ns2);

// Network Segments protected by Firewall Rules
MATCH (ns:NetworkSegment), (fr:FirewallRule)
WHERE ns.id STARTS WITH 'NS-' AND fr.id STARTS WITH 'FR-'
WITH ns, fr LIMIT 100
CREATE (ns)-[:PROTECTED_BY {appliedDate: datetime(), enforced: true, effectiveFrom: datetime(), effectiveUntil: null}]->(fr);

// Components use Protocols
MATCH (comp:Component), (p:Protocol)
WHERE comp.id STARTS WITH 'COMP-' AND p.id STARTS WITH 'PROTO-'
WITH comp, p LIMIT 200
CREATE (comp)-[:USES_PROTOCOL {purpose: 'control_communication', isRequired: true, configuredSecurely: false, alternativeAvailable: true}]->(p);

// Threat Actors exploit CVEs
MATCH (ta:ThreatActor {id: 'TA-001'}), (cve:CVE {id: 'CVE-2021-44228'})
CREATE (ta)-[:EXPLOITS {firstObserved: date('2021-12-12'), lastObserved: date('2025-10-15'), frequency: 'high', successRate: 85.5, technique: 'JNDI injection'}]->(cve);

// Threat Actors target Organizations
MATCH (ta:ThreatActor), (org:Organization)
WHERE ta.id STARTS WITH 'TA-' AND org.id = 'ORG-001'
CREATE (ta)-[:TARGETS {firstTargeted: date('2024-06-01'), lastActivity: date('2025-10-15'), isActive: true, motivation: 'espionage', objective: 'steal_data', successfulBreaches: 0}]->(org);

// Threat Actors conduct Campaigns
MATCH (ta:ThreatActor), (camp:Campaign)
WHERE ta.id STARTS WITH 'TA-' AND camp.id STARTS WITH 'CAMP-'
WITH ta, camp LIMIT 10
CREATE (ta)-[:CONDUCTS {role: 'primary', attribution: 'high_confidence', evidenceType: ['infrastructure_overlap', 'ttp_similarity']}]->(camp);

// Threat Actors use Attack Techniques
MATCH (ta:ThreatActor), (at:AttackTechnique)
WHERE ta.id STARTS WITH 'TA-' AND at.id STARTS WITH 'ATK-'
WITH ta, at LIMIT 50
CREATE (ta)-[:USES {frequency: 'high', firstObserved: date('2020-01-01'), lastObserved: date('2025-10-15'), effectiveness: 'high'}]->(at);

// Campaigns use Attack Techniques
MATCH (camp:Campaign), (at:AttackTechnique)
WHERE camp.id STARTS WITH 'CAMP-' AND at.id STARTS WITH 'ATK-'
WITH camp, at LIMIT 30
CREATE (camp)-[:USES {frequency: 'high', firstObserved: date('2025-01-01'), lastObserved: date('2025-10-15'), effectiveness: 'medium'}]->(at);

// Documents mention CVEs
MATCH (doc:Document), (cve:CVE)
WHERE doc.id STARTS WITH 'DOC-' AND cve.id = 'CVE-2021-44228'
CREATE (doc)-[:MENTIONS {context: 'Critical vulnerability analysis', relevance: 'high', pageNumber: 5, section: 'Executive Summary'}]->(cve);

// Documents mention Threat Actors
MATCH (doc:Document), (ta:ThreatActor)
WHERE doc.id STARTS WITH 'DOC-' AND ta.id STARTS WITH 'TA-'
WITH doc, ta LIMIT 20
CREATE (doc)-[:MENTIONS {context: 'Threat intelligence', relevance: 'high', pageNumber: 10, section: 'Threat Analysis'}]->(ta);

// Documents describe Attack Techniques
MATCH (doc:Document), (at:AttackTechnique)
WHERE doc.id STARTS WITH 'DOC-' AND at.id STARTS WITH 'ATK-'
WITH doc, at LIMIT 30
CREATE (doc)-[:DESCRIBES {description: 'Detailed technique analysis', detailLevel: 'comprehensive', actionable: true}]->(at);

// Attack Path Examples (from external network to critical PLC)
MATCH (ns_ext:NetworkSegment {id: 'NS-004'}), // External/Public network
      (ns_dmz:NetworkSegment {id: 'NS-003'}), // DMZ
      (ns_mgmt:NetworkSegment {id: 'NS-002'}), // Management network
      (ns_ctrl:NetworkSegment {id: 'NS-001'}), // Control network
      (comp_plc:Component {id: 'COMP-001'}) // Critical PLC
CREATE (ns_ext)-[:ATTACK_PATH_STEP {stepNumber: 1, attackTechnique: 'T1190', likelihood: 0.65, impact: 0.40, detectionDifficulty: 'medium', requiredCapabilities: ['exploit_development']}]->(ns_dmz),
       (ns_dmz)-[:ATTACK_PATH_STEP {stepNumber: 2, attackTechnique: 'T1078', likelihood: 0.50, impact: 0.60, detectionDifficulty: 'high', requiredCapabilities: ['credential_theft']}]->(ns_mgmt),
       (ns_mgmt)-[:ATTACK_PATH_STEP {stepNumber: 3, attackTechnique: 'T1021', likelihood: 0.45, impact: 0.80, detectionDifficulty: 'high', requiredCapabilities: ['lateral_movement']}]->(ns_ctrl),
       (ns_ctrl)-[:ATTACK_PATH_STEP {stepNumber: 4, attackTechnique: 'T1059', likelihood: 0.40, impact: 0.95, detectionDifficulty: 'critical', requiredCapabilities: ['ot_expertise']}]->(comp_plc);

// ============================================================================
// VERIFICATION QUERIES
// ============================================================================

// Count all nodes
// MATCH (n) RETURN labels(n)[0] AS NodeType, count(*) AS Count ORDER BY Count DESC;

// Count all relationships
// MATCH ()-[r]->() RETURN type(r) AS RelType, count(*) AS Count ORDER BY Count DESC;

// ============================================================================
// END OF SAMPLE DATA
// ============================================================================
