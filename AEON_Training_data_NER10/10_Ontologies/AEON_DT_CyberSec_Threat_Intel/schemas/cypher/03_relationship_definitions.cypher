// ============================================================================
// AEON DIGITAL TWIN CYBER SECURITY THREAT INTELLIGENCE
// Neo4j Relationship Type Definitions
// Version: 1.0.0
// Created: 2025-10-29
// ============================================================================

// ============================================================================
// RELATIONSHIP TYPE 1: OPERATES
// Organization operates Sites
// ============================================================================

// Properties:
// - since: DATE - Operating since date
// - contractExpiry: DATE - Contract expiration
// - operationalRole: STRING - Role in operations
// - responsibilityLevel: STRING - Responsibility level

// Example:
MATCH (org:Organization {id: 'ORG-001'}), (site:Site {id: 'SITE-001'})
CREATE (org)-[:OPERATES {
  since: date('2015-01-01'),
  contractExpiry: date('2030-12-31'),
  operationalRole: 'primary_operator',
  responsibilityLevel: 'full'
}]->(site);

// ============================================================================
// RELATIONSHIP TYPE 2: HOSTS
// Site hosts Trains (stations, depots)
// ============================================================================

// Properties:
// - frequency: STRING - Hosting frequency
// - capacity: INTEGER - Hosting capacity
// - serviceType: STRING - Type of service

// Example:
MATCH (site:Site {id: 'SITE-001'}), (train:Train {id: 'TRAIN-001'})
CREATE (site)-[:HOSTS {
  frequency: 'daily',
  capacity: 10,
  serviceType: 'passenger'
}]->(train);

// ============================================================================
// RELATIONSHIP TYPE 3: HAS_COMPONENT
// Train/Site has Components
// ============================================================================

// Properties:
// - installDate: DATE - Installation date
// - location: STRING - Physical location
// - isRedundant: BOOLEAN - Redundancy status
// - maintenanceResponsibility: STRING - Maintenance owner

// Example:
MATCH (train:Train {id: 'TRAIN-001'}), (comp:Component {id: 'COMP-001'})
CREATE (train)-[:HAS_COMPONENT {
  installDate: date('2020-01-15'),
  location: 'control_cabin',
  isRedundant: true,
  maintenanceResponsibility: 'manufacturer'
}]->(comp);

// ============================================================================
// RELATIONSHIP TYPE 4: RUNS_SOFTWARE
// Component runs Software
// ============================================================================

// Properties:
// - installDate: DATETIME - Installation timestamp
// - configurationId: STRING - Configuration identifier
// - isActive: BOOLEAN - Active status
// - startupOrder: INTEGER - Boot sequence order

// Example:
MATCH (comp:Component {id: 'COMP-001'}), (sw:Software {id: 'SW-001'})
CREATE (comp)-[:RUNS_SOFTWARE {
  installDate: datetime('2020-01-15T10:00:00'),
  configurationId: 'CFG-001',
  isActive: true,
  startupOrder: 1
}]->(sw);

// ============================================================================
// RELATIONSHIP TYPE 5: DEPENDS_ON
// Software depends on Library
// ============================================================================

// Properties:
// - versionConstraint: STRING - Version requirement
// - dependencyType: STRING - Dependency type (runtime, compile, optional)
// - isTransitive: BOOLEAN - Transitive dependency flag
// - declaredIn: STRING - Declaration source file

// Example:
MATCH (sw:Software {id: 'SW-001'}), (lib:Library {id: 'LIB-001'})
CREATE (sw)-[:DEPENDS_ON {
  versionConstraint: '>=2.17.0',
  dependencyType: 'runtime',
  isTransitive: false,
  declaredIn: 'pom.xml'
}]->(lib);

// ============================================================================
// RELATIONSHIP TYPE 6: HAS_VULNERABILITY
// Software/Component/Library has CVE
// ============================================================================

// Properties:
// - discoveredDate: DATE - Discovery date
// - affectedVersions: LIST<STRING> - Affected versions
// - exploited: BOOLEAN - Exploitation status
// - patchedInVersion: STRING - Patch version
// - mitigationStatus: STRING - Mitigation status
// - riskScore: FLOAT - Specific risk score

// Example:
MATCH (sw:Software {id: 'SW-001'}), (cve:CVE {id: 'CVE-2021-44228'})
CREATE (sw)-[:HAS_VULNERABILITY {
  discoveredDate: date('2021-12-10'),
  affectedVersions: ['2.0', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '2.10', '2.11', '2.12', '2.13', '2.14', '2.15', '2.16'],
  exploited: false,
  patchedInVersion: '2.17.1',
  mitigationStatus: 'patched',
  riskScore: 95.5
}]->(cve);

// ============================================================================
// RELATIONSHIP TYPE 7: HAS_INTERFACE
// Component has NetworkInterface
// ============================================================================

// Properties:
// - purpose: STRING - Interface purpose
// - isManagement: BOOLEAN - Management interface flag
// - isPrimary: BOOLEAN - Primary interface flag

// Example:
MATCH (comp:Component {id: 'COMP-001'}), (ni:NetworkInterface {id: 'NI-001'})
CREATE (comp)-[:HAS_INTERFACE {
  purpose: 'operational',
  isManagement: false,
  isPrimary: true
}]->(ni);

// ============================================================================
// RELATIONSHIP TYPE 8: BELONGS_TO
// NetworkInterface belongs to NetworkSegment
// ============================================================================

// Properties:
// - assignedDate: DATE - Assignment date
// - isStatic: BOOLEAN - Static assignment flag
// - priority: INTEGER - Interface priority

// Example:
MATCH (ni:NetworkInterface {id: 'NI-001'}), (ns:NetworkSegment {id: 'NS-001'})
CREATE (ni)-[:BELONGS_TO {
  assignedDate: date('2020-01-15'),
  isStatic: true,
  priority: 1
}]->(ns);

// ============================================================================
// RELATIONSHIP TYPE 9: CONNECTS_TO
// NetworkSegment connects to NetworkSegment
// ============================================================================

// Properties:
// - connectionType: STRING - Connection type (routed, bridged, vpn)
// - bandwidth: INTEGER - Connection bandwidth (Mbps)
// - latency: INTEGER - Average latency (ms)
// - isEncrypted: BOOLEAN - Encryption status
// - routingProtocol: STRING - Routing protocol

// Example:
MATCH (ns1:NetworkSegment {id: 'NS-001'}), (ns2:NetworkSegment {id: 'NS-002'})
CREATE (ns1)-[:CONNECTS_TO {
  connectionType: 'routed',
  bandwidth: 1000,
  latency: 5,
  isEncrypted: true,
  routingProtocol: 'OSPF'
}]->(ns2);

// ============================================================================
// RELATIONSHIP TYPE 10: PROTECTED_BY
// NetworkSegment protected by FirewallRule
// ============================================================================

// Properties:
// - appliedDate: DATETIME - Rule application date
// - enforced: BOOLEAN - Enforcement status
// - effectiveFrom: DATETIME - Effective start time
// - effectiveUntil: DATETIME - Effective end time

// Example:
MATCH (ns:NetworkSegment {id: 'NS-001'}), (fr:FirewallRule {id: 'FR-001'})
CREATE (ns)-[:PROTECTED_BY {
  appliedDate: datetime('2025-01-15T10:00:00'),
  enforced: true,
  effectiveFrom: datetime('2025-01-15T10:00:00'),
  effectiveUntil: null
}]->(fr);

// ============================================================================
// RELATIONSHIP TYPE 11: USES_PROTOCOL
// Component/Software uses Protocol
// ============================================================================

// Properties:
// - purpose: STRING - Protocol usage purpose
// - isRequired: BOOLEAN - Required for operation
// - configuredSecurely: BOOLEAN - Security configuration status
// - alternativeAvailable: BOOLEAN - Alternative protocol available

// Example:
MATCH (comp:Component {id: 'COMP-001'}), (p:Protocol {id: 'PROTO-001'})
CREATE (comp)-[:USES_PROTOCOL {
  purpose: 'control_communication',
  isRequired: true,
  configuredSecurely: false,
  alternativeAvailable: true
}]->(p);

// ============================================================================
// RELATIONSHIP TYPE 12: EXPLOITS
// ThreatActor exploits CVE
// ============================================================================

// Properties:
// - firstObserved: DATE - First exploitation observed
// - lastObserved: DATE - Last exploitation observed
// - frequency: STRING - Exploitation frequency
// - successRate: FLOAT - Success rate percentage
// - technique: STRING - Exploitation technique

// Example:
MATCH (ta:ThreatActor {id: 'TA-001'}), (cve:CVE {id: 'CVE-2021-44228'})
CREATE (ta)-[:EXPLOITS {
  firstObserved: date('2021-12-12'),
  lastObserved: date('2025-10-15'),
  frequency: 'high',
  successRate: 85.5,
  technique: 'JNDI injection via malicious LDAP server'
}]->(cve);

// ============================================================================
// RELATIONSHIP TYPE 13: TARGETS
// ThreatActor targets Organization
// ============================================================================

// Properties:
// - firstTargeted: DATE - First targeting date
// - lastActivity: DATE - Last observed activity
// - isActive: BOOLEAN - Current targeting status
// - motivation: STRING - Targeting motivation
// - objective: STRING - Targeting objective
// - successfulBreaches: INTEGER - Number of successful breaches

// Example:
MATCH (ta:ThreatActor {id: 'TA-001'}), (org:Organization {id: 'ORG-001'})
CREATE (ta)-[:TARGETS {
  firstTargeted: date('2024-06-01'),
  lastActivity: date('2025-10-15'),
  isActive: true,
  motivation: 'espionage',
  objective: 'steal_operational_data',
  successfulBreaches: 0
}]->(org);

// ============================================================================
// RELATIONSHIP TYPE 14: CONDUCTS
// ThreatActor conducts Campaign
// ============================================================================

// Properties:
// - role: STRING - Actor role in campaign
// - attribution: STRING - Attribution confidence
// - evidenceType: LIST<STRING> - Evidence types

// Example:
MATCH (ta:ThreatActor {id: 'TA-001'}), (camp:Campaign {id: 'CAMP-001'})
CREATE (ta)-[:CONDUCTS {
  role: 'primary',
  attribution: 'high_confidence',
  evidenceType: ['infrastructure_overlap', 'ttp_similarity', 'malware_code_reuse']
}]->(camp);

// ============================================================================
// RELATIONSHIP TYPE 15: USES (ThreatActor/Campaign uses AttackTechnique)
// ============================================================================

// Properties:
// - frequency: STRING - Usage frequency
// - firstObserved: DATE - First observation
// - lastObserved: DATE - Last observation
// - effectiveness: STRING - Technique effectiveness

// Example:
MATCH (ta:ThreatActor {id: 'TA-001'}), (at:AttackTechnique {id: 'ATK-001'})
CREATE (ta)-[:USES {
  frequency: 'high',
  firstObserved: date('2020-01-01'),
  lastObserved: date('2025-10-15'),
  effectiveness: 'high'
}]->(at);

// ============================================================================
// RELATIONSHIP TYPE 16: TARGETS_SECTOR
// Campaign targets specific sectors
// ============================================================================

// Properties:
// - sector: STRING - Industry sector
// - targetCount: INTEGER - Number of targets
// - successRate: FLOAT - Success rate percentage

// Example:
MATCH (camp:Campaign {id: 'CAMP-001'}), (org:Organization {id: 'ORG-001'})
CREATE (camp)-[:TARGETS_SECTOR {
  sector: 'Rail Transport',
  targetCount: 12,
  successRate: 25.0
}]->(org);

// ============================================================================
// RELATIONSHIP TYPE 17: MENTIONS
// Document mentions CVE/ThreatActor/Campaign
// ============================================================================

// Properties:
// - context: STRING - Mention context
// - relevance: STRING - Relevance level (high, medium, low)
// - pageNumber: INTEGER - Page number (if applicable)
// - section: STRING - Document section

// Example:
MATCH (doc:Document {id: 'DOC-001'}), (cve:CVE {id: 'CVE-2021-44228'})
CREATE (doc)-[:MENTIONS {
  context: 'Critical vulnerability requiring immediate patching',
  relevance: 'high',
  pageNumber: 5,
  section: 'Executive Summary'
}]->(cve);

// ============================================================================
// RELATIONSHIP TYPE 18: DESCRIBES
// Document describes AttackTechnique/Mitigation
// ============================================================================

// Properties:
// - description: STRING - Description content
// - detailLevel: STRING - Level of detail
// - actionable: BOOLEAN - Contains actionable guidance

// Example:
MATCH (doc:Document {id: 'DOC-001'}), (at:AttackTechnique {id: 'ATK-001'})
CREATE (doc)-[:DESCRIBES {
  description: 'Detailed analysis of PowerShell attack vectors in railway control systems',
  detailLevel: 'comprehensive',
  actionable: true
}]->(at);

// ============================================================================
// RELATIONSHIP TYPE 19: ATTACK_PATH_STEP
// Represents steps in an attack path graph
// ============================================================================

// Properties:
// - stepNumber: INTEGER - Step sequence number
// - attackTechnique: STRING - MITRE ATT&CK technique
// - likelihood: FLOAT - Step likelihood (0-1)
// - impact: FLOAT - Step impact (0-1)
// - detectionDifficulty: STRING - Detection difficulty
// - requiredCapabilities: LIST<STRING> - Required attacker capabilities

// Example: Attack path from external network to train control system
MATCH (source:NetworkSegment {id: 'NS-003'}), // External network
      (target:Component {id: 'COMP-001'}) // Train control PLC
CREATE (source)-[:ATTACK_PATH_STEP {
  stepNumber: 1,
  attackTechnique: 'T1190',
  likelihood: 0.65,
  impact: 0.85,
  detectionDifficulty: 'medium',
  requiredCapabilities: ['exploit_development', 'network_reconnaissance']
}]->(target);

// ============================================================================
// RELATIONSHIP TYPE 20: MITIGATES
// Control/Measure mitigates Vulnerability/Threat
// ============================================================================

// Properties:
// - effectiveness: STRING - Mitigation effectiveness
// - implementationDate: DATE - Implementation date
// - cost: STRING - Implementation cost
// - verified: BOOLEAN - Verification status

// Example:
MATCH (fr:FirewallRule {id: 'FR-001'}), (cve:CVE {id: 'CVE-2021-44228'})
CREATE (fr)-[:MITIGATES {
  effectiveness: 'high',
  implementationDate: date('2021-12-15'),
  cost: 'low',
  verified: true
}]->(cve);

// ============================================================================
// RELATIONSHIP TYPE 21: MONITORS
// Monitoring system monitors Component/Network
// ============================================================================

// Properties:
// - monitoringType: STRING - Type of monitoring
// - frequency: STRING - Monitoring frequency
// - alertThreshold: FLOAT - Alert threshold
// - lastCheck: DATETIME - Last monitoring check

// Example:
MATCH (comp1:Component {id: 'COMP-002'}), // IDS/IPS system
      (comp2:Component {id: 'COMP-001'}) // Monitored PLC
CREATE (comp1)-[:MONITORS {
  monitoringType: 'network_traffic',
  frequency: 'realtime',
  alertThreshold: 0.7,
  lastCheck: datetime('2025-10-29T10:00:00')
}]->(comp2);

// ============================================================================
// RELATIONSHIP TYPE 22: AUTHENTICATES
// Authentication relationship between systems
// ============================================================================

// Properties:
// - authMethod: STRING - Authentication method
// - protocol: STRING - Authentication protocol
// - mfaEnabled: BOOLEAN - Multi-factor authentication
// - lastAuth: DATETIME - Last authentication

// Example:
MATCH (comp1:Component {id: 'COMP-003'}), // Authentication server
      (comp2:Component {id: 'COMP-001'}) // Client system
CREATE (comp2)-[:AUTHENTICATES {
  authMethod: 'certificate',
  protocol: 'TLS 1.3',
  mfaEnabled: true,
  lastAuth: datetime('2025-10-29T09:45:00')
}]->(comp1);

// ============================================================================
// RELATIONSHIP TYPE 23: SUPPLIES
// Manufacturer/Vendor supplies Component/Software
// ============================================================================

// Properties:
// - supplyDate: DATE - Supply/delivery date
// - contractNumber: STRING - Contract identifier
// - warrantyPeriod: INTEGER - Warranty period (months)
// - supportLevel: STRING - Support level

// Example:
MATCH (org:Organization {type: 'manufacturer'}),
      (comp:Component {id: 'COMP-001'})
CREATE (org)-[:SUPPLIES {
  supplyDate: date('2020-01-01'),
  contractNumber: 'CNT-2020-001',
  warrantyPeriod: 60,
  supportLevel: 'premium'
}]->(comp);

// ============================================================================
// RELATIONSHIP TYPE 24: REQUIRES_UPDATE
// Component/Software requires update/patch
// ============================================================================

// Properties:
// - updateType: STRING - Update type (security, feature, bugfix)
// - urgency: STRING - Update urgency
// - availableVersion: STRING - Available update version
// - scheduledDate: DATE - Scheduled update date
// - requiresDowntime: BOOLEAN - Downtime requirement

// Example:
MATCH (sw:Software {id: 'SW-001'}), (cve:CVE {id: 'CVE-2021-44228'})
CREATE (sw)-[:REQUIRES_UPDATE {
  updateType: 'security',
  urgency: 'critical',
  availableVersion: '2.17.1',
  scheduledDate: date('2025-11-01'),
  requiresDowntime: true
}]->(cve);

// ============================================================================
// RELATIONSHIP TYPE 25: COMMUNICATES_WITH
// Component/System communicates with another
// ============================================================================

// Properties:
// - protocol: STRING - Communication protocol
// - frequency: STRING - Communication frequency
// - dataType: STRING - Type of data exchanged
// - isEncrypted: BOOLEAN - Encryption status
// - bandwidth: INTEGER - Average bandwidth usage (Kbps)
// - lastCommunication: DATETIME - Last communication timestamp

// Example:
MATCH (comp1:Component {id: 'COMP-001'}), // PLC
      (comp2:Component {id: 'COMP-004'}) // SCADA server
CREATE (comp1)-[:COMMUNICATES_WITH {
  protocol: 'MODBUS/TCP',
  frequency: 'continuous',
  dataType: 'control_signals',
  isEncrypted: false,
  bandwidth: 100,
  lastCommunication: datetime('2025-10-29T10:00:00')
}]->(comp2);

// ============================================================================
// COMPREHENSIVE RELATIONSHIP PATTERN EXAMPLES
// ============================================================================

// Example 1: Complete Organization-to-Train chain
MATCH (org:Organization {id: 'ORG-001'}),
      (site:Site {id: 'SITE-001'}),
      (train:Train {id: 'TRAIN-001'}),
      (comp:Component {id: 'COMP-001'}),
      (sw:Software {id: 'SW-001'}),
      (lib:Library {id: 'LIB-001'}),
      (cve:CVE {id: 'CVE-2021-44228'})
CREATE (org)-[:OPERATES]->(site)-[:HOSTS]->(train)-[:HAS_COMPONENT]->(comp)
       -[:RUNS_SOFTWARE]->(sw)-[:DEPENDS_ON]->(lib)-[:HAS_VULNERABILITY]->(cve);

// Example 2: Network topology with security
MATCH (comp:Component {id: 'COMP-001'}),
      (ni:NetworkInterface {id: 'NI-001'}),
      (ns:NetworkSegment {id: 'NS-001'}),
      (fr:FirewallRule {id: 'FR-001'}),
      (proto:Protocol {id: 'PROTO-001'})
CREATE (comp)-[:HAS_INTERFACE]->(ni)-[:BELONGS_TO]->(ns)-[:PROTECTED_BY]->(fr),
       (comp)-[:USES_PROTOCOL]->(proto);

// Example 3: Threat intelligence chain
MATCH (ta:ThreatActor {id: 'TA-001'}),
      (camp:Campaign {id: 'CAMP-001'}),
      (at:AttackTechnique {id: 'ATK-001'}),
      (cve:CVE {id: 'CVE-2021-44228'}),
      (org:Organization {id: 'ORG-001'})
CREATE (ta)-[:CONDUCTS]->(camp)-[:TARGETS_SECTOR]->(org),
       (ta)-[:USES]->(at),
       (ta)-[:EXPLOITS]->(cve);

// Example 4: Documentation and intelligence
MATCH (doc:Document {id: 'DOC-001'}),
      (cve:CVE {id: 'CVE-2021-44228'}),
      (ta:ThreatActor {id: 'TA-001'}),
      (at:AttackTechnique {id: 'ATK-001'})
CREATE (doc)-[:MENTIONS]->(cve),
       (doc)-[:MENTIONS]->(ta),
       (doc)-[:DESCRIBES]->(at);

// ============================================================================
// END OF RELATIONSHIP DEFINITIONS
// ============================================================================
