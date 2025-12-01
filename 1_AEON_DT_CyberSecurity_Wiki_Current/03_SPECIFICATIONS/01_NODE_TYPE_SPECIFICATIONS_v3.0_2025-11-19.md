# Node Type Specifications - AEON Cyber DT v3.0

**File**: 01_NODE_TYPE_SPECIFICATIONS_v3.0_2025-11-19.md
**Created**: 2025-11-19 11:47:00 UTC
**Modified**: 2025-11-19 11:47:00 UTC
**Version**: v3.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete technical specifications for all Neo4j node types
**Status**: ACTIVE

## Document Overview

This document provides comprehensive technical specifications for all 50+ node types in the AEON Cyber Digital Twin v3.0 knowledge graph.

## Node Type Categories

### 1. Core Threat Intelligence Nodes

#### CVE (Common Vulnerabilities and Exposures)
```cypher
(:CVE {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  cveId: String [REQUIRED, UNIQUE, INDEX],

  // Descriptive Properties
  description: String [REQUIRED],
  publishedDate: DateTime [REQUIRED, INDEX],
  lastModifiedDate: DateTime [REQUIRED, INDEX],

  // Severity & Impact
  cvssV2Score: Float [OPTIONAL],
  cvssV2Vector: String [OPTIONAL],
  cvssV3Score: Float [OPTIONAL, INDEX],
  cvssV3Vector: String [OPTIONAL],
  cvssV4Score: Float [OPTIONAL, INDEX],
  cvssV4Vector: String [OPTIONAL],

  baseSeverity: String [REQUIRED, INDEX], // LOW, MEDIUM, HIGH, CRITICAL
  exploitabilityScore: Float [OPTIONAL],
  impactScore: Float [OPTIONAL],

  // Attack Characteristics
  attackVector: String [OPTIONAL], // NETWORK, ADJACENT, LOCAL, PHYSICAL
  attackComplexity: String [OPTIONAL], // LOW, HIGH
  privilegesRequired: String [OPTIONAL], // NONE, LOW, HIGH
  userInteraction: String [OPTIONAL], // NONE, REQUIRED
  scope: String [OPTIONAL], // UNCHANGED, CHANGED

  // Impact Ratings
  confidentialityImpact: String [OPTIONAL], // NONE, LOW, HIGH
  integrityImpact: String [OPTIONAL], // NONE, LOW, HIGH
  availabilityImpact: String [OPTIONAL], // NONE, LOW, HIGH

  // Status & Classification
  status: String [REQUIRED], // PUBLISHED, MODIFIED, REJECTED, ANALYZED
  assigner: String [OPTIONAL],

  // References
  references: [String] [OPTIONAL],
  sourceUrls: [String] [OPTIONAL],

  // Metadata
  dataSource: String [REQUIRED], // NVD, MITRE, VENDOR
  lastSyncDate: DateTime [REQUIRED],
  version: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings for AI/ML
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT cve_id_unique FOR (c:CVE) REQUIRE c.id IS UNIQUE`
- `CREATE CONSTRAINT cve_cveid_unique FOR (c:CVE) REQUIRE c.cveId IS UNIQUE`

**Indexes**:
- `CREATE INDEX cve_published_date FOR (c:CVE) ON (c.publishedDate)`
- `CREATE INDEX cve_severity FOR (c:CVE) ON (c.baseSeverity)`
- `CREATE INDEX cve_cvss_score FOR (c:CVE) ON (c.cvssV3Score)`
- `CREATE FULLTEXT INDEX cve_description_fulltext FOR (c:CVE) ON EACH [c.description]`

---

#### CWE (Common Weakness Enumeration)
```cypher
(:CWE {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  cweId: String [REQUIRED, UNIQUE, INDEX],

  // Descriptive Properties
  name: String [REQUIRED, INDEX],
  description: String [REQUIRED],
  extendedDescription: String [OPTIONAL],

  // Classification
  abstraction: String [REQUIRED], // CLASS, BASE, VARIANT, COMPOUND
  structure: String [OPTIONAL], // SIMPLE, COMPOSITE, CHAIN
  status: String [REQUIRED], // STABLE, DRAFT, DEPRECATED

  // Hierarchy & Categorization
  category: String [OPTIONAL],
  view: [String] [OPTIONAL], // Research Concepts, Development Concepts

  // Impact & Likelihood
  likelihoodOfExploit: String [OPTIONAL], // HIGH, MEDIUM, LOW
  typicalSeverity: String [OPTIONAL],

  // Consequences
  consequenceScopes: [String] [OPTIONAL],
  consequenceTechnicalImpacts: [String] [OPTIONAL],

  // Detection & Mitigation
  detectionMethods: [String] [OPTIONAL],
  potentialMitigations: [String] [OPTIONAL],

  // Examples
  demonstrativeExamples: [String] [OPTIONAL],
  observedExamples: [String] [OPTIONAL],

  // Related Patterns
  modesOfIntroduction: [String] [OPTIONAL],
  applicablePlatforms: [String] [OPTIONAL],

  // Metadata
  dataSource: String [REQUIRED],
  lastSyncDate: DateTime [REQUIRED],
  version: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT cwe_id_unique FOR (w:CWE) REQUIRE w.id IS UNIQUE`
- `CREATE CONSTRAINT cwe_cweid_unique FOR (w:CWE) REQUIRE w.cweId IS UNIQUE`

**Indexes**:
- `CREATE INDEX cwe_name FOR (w:CWE) ON (w.name)`
- `CREATE INDEX cwe_abstraction FOR (w:CWE) ON (w.abstraction)`
- `CREATE FULLTEXT INDEX cwe_description_fulltext FOR (w:CWE) ON EACH [w.description, w.extendedDescription]`

---

#### CAPEC (Common Attack Pattern Enumeration and Classification)
```cypher
(:CAPEC {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  capecId: String [REQUIRED, UNIQUE, INDEX],

  // Descriptive Properties
  name: String [REQUIRED, INDEX],
  description: String [REQUIRED],
  extendedDescription: String [OPTIONAL],

  // Classification
  abstraction: String [REQUIRED], // META, STANDARD, DETAILED
  status: String [REQUIRED], // STABLE, DRAFT, DEPRECATED

  // Attack Characteristics
  typicalSeverity: String [OPTIONAL],
  likelihoodOfAttack: String [OPTIONAL], // HIGH, MEDIUM, LOW

  // Prerequisites
  prerequisites: [String] [OPTIONAL],
  skillsRequired: [String] [OPTIONAL],
  resourcesRequired: [String] [OPTIONAL],

  // Execution
  executionFlow: String [OPTIONAL],
  solutionsAndMitigations: [String] [OPTIONAL],

  // Impact
  consequenceScopes: [String] [OPTIONAL],
  consequenceTechnicalImpacts: [String] [OPTIONAL],

  // Examples
  exampleInstances: [String] [OPTIONAL],
  relatedAttackPatterns: [String] [OPTIONAL],

  // Taxonomy Mappings
  taxonomyMappings: [String] [OPTIONAL],

  // Metadata
  dataSource: String [REQUIRED],
  lastSyncDate: DateTime [REQUIRED],
  version: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT capec_id_unique FOR (a:CAPEC) REQUIRE a.id IS UNIQUE`
- `CREATE CONSTRAINT capec_capecid_unique FOR (a:CAPEC) REQUIRE a.capecId IS UNIQUE`

**Indexes**:
- `CREATE INDEX capec_name FOR (a:CAPEC) ON (a.name)`
- `CREATE INDEX capec_abstraction FOR (a:CAPEC) ON (a.abstraction)`
- `CREATE INDEX capec_severity FOR (a:CAPEC) ON (a.typicalSeverity)`
- `CREATE FULLTEXT INDEX capec_description_fulltext FOR (a:CAPEC) ON EACH [a.description, a.extendedDescription]`

---

### 2. Asset & Infrastructure Nodes

#### Asset
```cypher
(:Asset {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  assetId: String [REQUIRED, UNIQUE, INDEX],
  name: String [REQUIRED, INDEX],

  // Classification
  assetType: String [REQUIRED, INDEX], // SERVER, WORKSTATION, NETWORK_DEVICE, DATABASE, APPLICATION, MOBILE, IOT
  category: String [OPTIONAL], // HARDWARE, SOFTWARE, DATA, FACILITY
  criticality: String [REQUIRED, INDEX], // CRITICAL, HIGH, MEDIUM, LOW

  // Business Context
  businessOwner: String [OPTIONAL],
  technicalOwner: String [OPTIONAL],
  department: String [OPTIONAL, INDEX],
  businessFunction: String [OPTIONAL],

  // Technical Details
  ipAddress: String [OPTIONAL, INDEX],
  macAddress: String [OPTIONAL],
  hostname: String [OPTIONAL, INDEX],
  fqdn: String [OPTIONAL],
  location: String [OPTIONAL, INDEX],
  zone: String [OPTIONAL], // DMZ, INTERNAL, EXTERNAL, CLOUD

  // Configuration
  operatingSystem: String [OPTIONAL, INDEX],
  osVersion: String [OPTIONAL],
  manufacturer: String [OPTIONAL],
  model: String [OPTIONAL],
  serialNumber: String [OPTIONAL],

  // Status & State
  status: String [REQUIRED], // ACTIVE, INACTIVE, DECOMMISSIONED, MAINTENANCE
  operationalState: String [OPTIONAL], // RUNNING, STOPPED, DEGRADED
  lastSeenOnline: DateTime [OPTIONAL, INDEX],

  // Security Posture
  riskScore: Float [OPTIONAL, INDEX],
  exposureScore: Float [OPTIONAL],
  vulnerabilityCount: Integer [OPTIONAL],
  patchLevel: String [OPTIONAL],

  // Compliance
  complianceFrameworks: [String] [OPTIONAL], // HIPAA, PCI-DSS, SOC2, ISO27001
  dataClassification: String [OPTIONAL], // PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED

  // Network Context
  networkSegment: String [OPTIONAL],
  vlanId: String [OPTIONAL],
  subnetMask: String [OPTIONAL],

  // Metadata
  acquisitionDate: Date [OPTIONAL],
  warrantyExpiration: Date [OPTIONAL],
  supportContract: String [OPTIONAL],

  // Discovery
  discoverySource: String [OPTIONAL], // CMDB, SCANNER, MANUAL, API
  lastDiscoveryDate: DateTime [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT asset_id_unique FOR (a:Asset) REQUIRE a.id IS UNIQUE`
- `CREATE CONSTRAINT asset_assetid_unique FOR (a:Asset) REQUIRE a.assetId IS UNIQUE`

**Indexes**:
- `CREATE INDEX asset_type FOR (a:Asset) ON (a.assetType)`
- `CREATE INDEX asset_criticality FOR (a:Asset) ON (a.criticality)`
- `CREATE INDEX asset_ip FOR (a:Asset) ON (a.ipAddress)`
- `CREATE INDEX asset_hostname FOR (a:Asset) ON (a.hostname)`
- `CREATE INDEX asset_risk FOR (a:Asset) ON (a.riskScore)`
- `CREATE FULLTEXT INDEX asset_name_fulltext FOR (a:Asset) ON EACH [a.name, a.hostname]`

---

#### Software
```cypher
(:Software {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  softwareId: String [REQUIRED, UNIQUE, INDEX],
  name: String [REQUIRED, INDEX],

  // Product Information
  vendor: String [REQUIRED, INDEX],
  product: String [REQUIRED, INDEX],
  version: String [REQUIRED, INDEX],
  edition: String [OPTIONAL],

  // CPE (Common Platform Enumeration)
  cpe23Uri: String [OPTIONAL, UNIQUE, INDEX],
  cpe22Uri: String [OPTIONAL],

  // Classification
  softwareType: String [REQUIRED], // APPLICATION, OPERATING_SYSTEM, FIRMWARE, LIBRARY, DRIVER
  category: String [OPTIONAL], // DATABASE, WEB_SERVER, SECURITY, PRODUCTIVITY

  // Version Control
  versionType: String [OPTIONAL], // MAJOR, MINOR, PATCH, BUILD
  isLatestVersion: Boolean [OPTIONAL],
  isEndOfLife: Boolean [OPTIONAL, INDEX],
  endOfLifeDate: Date [OPTIONAL],
  endOfSupportDate: Date [OPTIONAL],

  // Release Information
  releaseDate: Date [OPTIONAL],
  buildNumber: String [OPTIONAL],
  releaseNotes: String [OPTIONAL],

  // Licensing
  licenseType: String [OPTIONAL], // COMMERCIAL, OPEN_SOURCE, FREEWARE, PROPRIETARY
  licenseName: String [OPTIONAL],

  // Security Properties
  vulnerabilityCount: Integer [OPTIONAL, INDEX],
  criticalVulnerabilityCount: Integer [OPTIONAL],
  knownExploitCount: Integer [OPTIONAL],

  // Metadata
  description: String [OPTIONAL],
  homepage: String [OPTIONAL],
  downloadUrl: String [OPTIONAL],
  documentationUrl: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT software_id_unique FOR (s:Software) REQUIRE s.id IS UNIQUE`
- `CREATE CONSTRAINT software_softwareid_unique FOR (s:Software) REQUIRE s.softwareId IS UNIQUE`

**Indexes**:
- `CREATE INDEX software_name FOR (s:Software) ON (s.name)`
- `CREATE INDEX software_vendor FOR (s:Software) ON (s.vendor)`
- `CREATE INDEX software_cpe FOR (s:Software) ON (s.cpe23Uri)`
- `CREATE INDEX software_eol FOR (s:Software) ON (s.isEndOfLife)`
- `CREATE FULLTEXT INDEX software_fulltext FOR (s:Software) ON EACH [s.name, s.vendor, s.product]`

---

### 3. Threat Actor & Campaign Nodes

#### ThreatActor
```cypher
(:ThreatActor {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  actorId: String [REQUIRED, UNIQUE, INDEX],
  name: String [REQUIRED, INDEX],
  aliases: [String] [OPTIONAL],

  // Classification
  actorType: String [REQUIRED, INDEX], // NATION_STATE, CYBERCRIMINAL, HACKTIVIST, INSIDER, TERRORIST
  sophisticationLevel: String [OPTIONAL], // ADVANCED, INTERMEDIATE, BASIC

  // Attribution
  primaryMotivation: String [OPTIONAL], // FINANCIAL, ESPIONAGE, DISRUPTION, IDEOLOGY, REVENGE
  secondaryMotivations: [String] [OPTIONAL],
  nationality: String [OPTIONAL, INDEX],
  sponsorship: String [OPTIONAL], // STATE_SPONSORED, INDEPENDENT, CORPORATE

  // Operational Characteristics
  firstSeen: DateTime [OPTIONAL, INDEX],
  lastSeen: DateTime [OPTIONAL, INDEX],
  status: String [REQUIRED], // ACTIVE, DORMANT, DISBANDED, UNKNOWN

  // Capabilities
  primaryTargets: [String] [OPTIONAL], // GOVERNMENT, FINANCE, HEALTHCARE, ENERGY
  targetIndustries: [String] [OPTIONAL],
  targetRegions: [String] [OPTIONAL],

  // Tactics & Techniques
  preferredTactics: [String] [OPTIONAL],
  knownTools: [String] [OPTIONAL],
  commonTTPs: [String] [OPTIONAL],

  // Impact
  campaigns: Integer [OPTIONAL],
  knownVictims: Integer [OPTIONAL],
  estimatedImpact: String [OPTIONAL],

  // Intelligence
  description: String [OPTIONAL],
  confidenceLevel: String [OPTIONAL], // HIGH, MEDIUM, LOW
  intelSources: [String] [OPTIONAL],

  // Metadata
  dataSource: String [OPTIONAL],
  lastIntelUpdate: DateTime [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT threat_actor_id_unique FOR (t:ThreatActor) REQUIRE t.id IS UNIQUE`
- `CREATE CONSTRAINT threat_actor_actorid_unique FOR (t:ThreatActor) REQUIRE t.actorId IS UNIQUE`

**Indexes**:
- `CREATE INDEX threat_actor_name FOR (t:ThreatActor) ON (t.name)`
- `CREATE INDEX threat_actor_type FOR (t:ThreatActor) ON (t.actorType)`
- `CREATE INDEX threat_actor_nationality FOR (t:ThreatActor) ON (t.nationality)`
- `CREATE FULLTEXT INDEX threat_actor_fulltext FOR (t:ThreatActor) ON EACH [t.name, t.description]`

---

#### Campaign
```cypher
(:Campaign {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  campaignId: String [REQUIRED, UNIQUE, INDEX],
  name: String [REQUIRED, INDEX],
  aliases: [String] [OPTIONAL],

  // Temporal Scope
  startDate: DateTime [OPTIONAL, INDEX],
  endDate: DateTime [OPTIONAL, INDEX],
  status: String [REQUIRED], // ACTIVE, COMPLETED, ONGOING, HISTORICAL

  // Classification
  campaignType: String [OPTIONAL], // APT, RANSOMWARE, PHISHING, DDoS, DATA_THEFT
  sophistication: String [OPTIONAL], // ADVANCED, MODERATE, BASIC

  // Objectives
  objectives: [String] [OPTIONAL], // ESPIONAGE, FINANCIAL_GAIN, DISRUPTION, DESTRUCTION
  targetedSectors: [String] [OPTIONAL],
  targetedCountries: [String] [OPTIONAL],

  // Impact
  victimCount: Integer [OPTIONAL],
  estimatedImpact: String [OPTIONAL],
  impactSeverity: String [OPTIONAL], // CRITICAL, HIGH, MEDIUM, LOW

  // Tactics & Techniques
  attackVectors: [String] [OPTIONAL],
  commonTTPs: [String] [OPTIONAL],
  toolsUsed: [String] [OPTIONAL],

  // Intelligence
  description: String [OPTIONAL],
  confidenceLevel: String [OPTIONAL], // HIGH, MEDIUM, LOW
  intelSources: [String] [OPTIONAL],

  // Attribution
  attributedTo: [String] [OPTIONAL], // Threat actor names/IDs
  attributionConfidence: String [OPTIONAL],

  // Metadata
  dataSource: String [OPTIONAL],
  lastIntelUpdate: DateTime [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT campaign_id_unique FOR (c:Campaign) REQUIRE c.id IS UNIQUE`
- `CREATE CONSTRAINT campaign_campaignid_unique FOR (c:Campaign) REQUIRE c.campaignId IS UNIQUE`

**Indexes**:
- `CREATE INDEX campaign_name FOR (c:Campaign) ON (c.name)`
- `CREATE INDEX campaign_status FOR (c:Campaign) ON (c.status)`
- `CREATE INDEX campaign_start FOR (c:Campaign) ON (c.startDate)`
- `CREATE FULLTEXT INDEX campaign_fulltext FOR (c:Campaign) ON EACH [c.name, c.description]`

---

### 4. Detection & Response Nodes

#### Indicator
```cypher
(:Indicator {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  indicatorId: String [REQUIRED, UNIQUE, INDEX],

  // Indicator Value
  value: String [REQUIRED, INDEX],
  type: String [REQUIRED, INDEX], // IP, DOMAIN, URL, FILE_HASH, EMAIL, REGISTRY_KEY

  // Classification
  category: String [OPTIONAL], // MALWARE, C2, PHISHING, EXPLOIT, SUSPICIOUS
  threatType: String [OPTIONAL],

  // Validity
  validFrom: DateTime [REQUIRED, INDEX],
  validUntil: DateTime [OPTIONAL, INDEX],
  isExpired: Boolean [OPTIONAL, INDEX],

  // Confidence & Severity
  confidenceScore: Float [OPTIONAL, INDEX], // 0.0 - 1.0
  severity: String [OPTIONAL], // CRITICAL, HIGH, MEDIUM, LOW, INFO
  falsePositiveRate: Float [OPTIONAL],

  // Detection
  pattern: String [OPTIONAL],
  detectionMethods: [String] [OPTIONAL],
  observableTypes: [String] [OPTIONAL],

  // Context
  description: String [OPTIONAL],
  context: String [OPTIONAL],
  tags: [String] [OPTIONAL],

  // Attribution
  relatedCampaigns: [String] [OPTIONAL],
  relatedActors: [String] [OPTIONAL],
  relatedMalware: [String] [OPTIONAL],

  // Intelligence
  intelSource: String [OPTIONAL],
  sourceReliability: String [OPTIONAL], // A, B, C, D, E, F
  intelConfidence: String [OPTIONAL], // CONFIRMED, PROBABLE, POSSIBLE, DOUBTFUL

  // Status
  status: String [REQUIRED], // ACTIVE, INACTIVE, REVOKED
  lastSeen: DateTime [OPTIONAL, INDEX],
  hitCount: Integer [OPTIONAL],

  // Sharing
  tlpMarking: String [OPTIONAL], // WHITE, GREEN, AMBER, RED
  shareableWith: [String] [OPTIONAL],

  // Metadata
  createdBy: String [OPTIONAL],
  dataSource: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
})
```

**Constraints**:
- `CREATE CONSTRAINT indicator_id_unique FOR (i:Indicator) REQUIRE i.id IS UNIQUE`
- `CREATE CONSTRAINT indicator_indicatorid_unique FOR (i:Indicator) REQUIRE i.indicatorId IS UNIQUE`

**Indexes**:
- `CREATE INDEX indicator_value FOR (i:Indicator) ON (i.value)`
- `CREATE INDEX indicator_type FOR (i:Indicator) ON (i.type)`
- `CREATE INDEX indicator_valid_from FOR (i:Indicator) ON (i.validFrom)`
- `CREATE INDEX indicator_confidence FOR (i:Indicator) ON (i.confidenceScore)`
- `CREATE FULLTEXT INDEX indicator_fulltext FOR (i:Indicator) ON EACH [i.value, i.description]`

---

#### Alert
```cypher
(:Alert {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  alertId: String [REQUIRED, UNIQUE, INDEX],

  // Classification
  alertType: String [REQUIRED, INDEX], // INTRUSION, MALWARE, POLICY_VIOLATION, ANOMALY
  category: String [OPTIONAL],
  severity: String [REQUIRED, INDEX], // CRITICAL, HIGH, MEDIUM, LOW, INFO

  // Detection
  detectionMethod: String [OPTIONAL], // SIGNATURE, BEHAVIORAL, ANOMALY, ML, CORRELATION
  detectionSource: String [OPTIONAL], // IDS, EDR, SIEM, FIREWALL, AV
  detectionTime: DateTime [REQUIRED, INDEX],

  // Description
  title: String [REQUIRED, INDEX],
  description: String [REQUIRED],
  details: String [OPTIONAL],

  // Status & Workflow
  status: String [REQUIRED, INDEX], // NEW, IN_PROGRESS, RESOLVED, CLOSED, FALSE_POSITIVE
  assignedTo: String [OPTIONAL, INDEX],
  priority: Integer [OPTIONAL, INDEX], // 1-5

  // Response
  responseActions: [String] [OPTIONAL],
  containmentStatus: String [OPTIONAL], // NONE, ISOLATED, CONTAINED, REMEDIATED
  resolutionTime: DateTime [OPTIONAL],
  resolutionNotes: String [OPTIONAL],

  // Analysis
  falsePositive: Boolean [OPTIONAL, INDEX],
  truePositive: Boolean [OPTIONAL, INDEX],
  investigationStatus: String [OPTIONAL],
  analystNotes: String [OPTIONAL],

  // Context
  affectedAssets: [String] [OPTIONAL],
  affectedUsers: [String] [OPTIONAL],
  sourceIp: String [OPTIONAL, INDEX],
  destinationIp: String [OPTIONAL, INDEX],

  // Risk
  riskScore: Float [OPTIONAL, INDEX],
  impactAssessment: String [OPTIONAL],

  // Correlation
  correlationId: String [OPTIONAL, INDEX],
  relatedAlertIds: [String] [OPTIONAL],

  // Compliance
  complianceViolation: Boolean [OPTIONAL],
  regulatoryRequirements: [String] [OPTIONAL],

  // Metadata
  rawData: String [OPTIONAL],
  dataSource: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],
  acknowledgedAt: DateTime [OPTIONAL],
  closedAt: DateTime [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT alert_id_unique FOR (a:Alert) REQUIRE a.id IS UNIQUE`
- `CREATE CONSTRAINT alert_alertid_unique FOR (a:Alert) REQUIRE a.alertId IS UNIQUE`

**Indexes**:
- `CREATE INDEX alert_type FOR (a:Alert) ON (a.alertType)`
- `CREATE INDEX alert_severity FOR (a:Alert) ON (a.severity)`
- `CREATE INDEX alert_status FOR (a:Alert) ON (a.status)`
- `CREATE INDEX alert_detection_time FOR (a:Alert) ON (a.detectionTime)`
- `CREATE FULLTEXT INDEX alert_fulltext FOR (a:Alert) ON EACH [a.title, a.description]`

---

### 5. MITRE ATT&CK Framework Nodes

#### MitreTactic
```cypher
(:MitreTactic {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  tacticId: String [REQUIRED, UNIQUE, INDEX],

  // Descriptive Properties
  name: String [REQUIRED, INDEX],
  description: String [REQUIRED],
  shortName: String [OPTIONAL],

  // Framework Context
  matrix: String [REQUIRED, INDEX], // ENTERPRISE, MOBILE, ICS
  platform: [String] [OPTIONAL],

  // Hierarchy
  ordinal: Integer [OPTIONAL], // Position in kill chain

  // Metadata
  externalId: String [OPTIONAL], // MITRE ATT&CK ID (e.g., TA0001)
  url: String [OPTIONAL],
  version: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT mitre_tactic_id_unique FOR (t:MitreTactic) REQUIRE t.id IS UNIQUE`
- `CREATE CONSTRAINT mitre_tactic_tacticid_unique FOR (t:MitreTactic) REQUIRE t.tacticId IS UNIQUE`

**Indexes**:
- `CREATE INDEX mitre_tactic_name FOR (t:MitreTactic) ON (t.name)`
- `CREATE INDEX mitre_tactic_matrix FOR (t:MitreTactic) ON (t.matrix)`

---

#### MitreTechnique
```cypher
(:MitreTechnique {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  techniqueId: String [REQUIRED, UNIQUE, INDEX],

  // Descriptive Properties
  name: String [REQUIRED, INDEX],
  description: String [REQUIRED],

  // Classification
  isSubTechnique: Boolean [REQUIRED, INDEX],
  parentTechniqueId: String [OPTIONAL, INDEX],

  // Framework Context
  matrix: String [REQUIRED, INDEX], // ENTERPRISE, MOBILE, ICS
  platforms: [String] [OPTIONAL],

  // Attack Characteristics
  dataSourcesRequired: [String] [OPTIONAL],
  defensesBypassed: [String] [OPTIONAL],
  permissionsRequired: [String] [OPTIONAL],

  // Detection & Mitigation
  detectionMethods: [String] [OPTIONAL],
  mitigationStrategies: [String] [OPTIONAL],

  // Metadata
  externalId: String [REQUIRED, UNIQUE, INDEX], // MITRE ATT&CK ID (e.g., T1566)
  url: String [OPTIONAL],
  version: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT mitre_technique_id_unique FOR (t:MitreTechnique) REQUIRE t.id IS UNIQUE`
- `CREATE CONSTRAINT mitre_technique_techniqueid_unique FOR (t:MitreTechnique) REQUIRE t.techniqueId IS UNIQUE`
- `CREATE CONSTRAINT mitre_technique_externalid_unique FOR (t:MitreTechnique) REQUIRE t.externalId IS UNIQUE`

**Indexes**:
- `CREATE INDEX mitre_technique_name FOR (t:MitreTechnique) ON (t.name)`
- `CREATE INDEX mitre_technique_matrix FOR (t:MitreTechnique) ON (t.matrix)`
- `CREATE INDEX mitre_technique_is_sub FOR (t:MitreTechnique) ON (t.isSubTechnique)`
- `CREATE FULLTEXT INDEX mitre_technique_fulltext FOR (t:MitreTechnique) ON EACH [t.name, t.description]`

---

### 6. Organizational Context Nodes

#### Organization
```cypher
(:Organization {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  organizationId: String [REQUIRED, UNIQUE, INDEX],
  name: String [REQUIRED, INDEX],

  // Classification
  type: String [REQUIRED], // ENTERPRISE, SMB, GOVERNMENT, EDUCATION, NONPROFIT
  industry: String [OPTIONAL, INDEX], // FINANCE, HEALTHCARE, ENERGY, TECHNOLOGY
  sector: String [OPTIONAL],

  // Geographic
  country: String [OPTIONAL, INDEX],
  region: String [OPTIONAL],
  headquarters: String [OPTIONAL],

  // Contact
  contactEmail: String [OPTIONAL],
  contactPhone: String [OPTIONAL],
  website: String [OPTIONAL],

  // Size & Scale
  employeeCount: Integer [OPTIONAL],
  revenueRange: String [OPTIONAL],

  // Security Profile
  securityMaturityLevel: String [OPTIONAL], // INITIAL, MANAGED, DEFINED, OPTIMIZED
  complianceFrameworks: [String] [OPTIONAL],
  riskTolerance: String [OPTIONAL], // LOW, MEDIUM, HIGH

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
})
```

**Constraints**:
- `CREATE CONSTRAINT organization_id_unique FOR (o:Organization) REQUIRE o.id IS UNIQUE`
- `CREATE CONSTRAINT organization_orgid_unique FOR (o:Organization) REQUIRE o.organizationId IS UNIQUE`

**Indexes**:
- `CREATE INDEX organization_name FOR (o:Organization) ON (o.name)`
- `CREATE INDEX organization_industry FOR (o:Organization) ON (o.industry)`

---

#### Department
```cypher
(:Department {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  departmentId: String [REQUIRED, UNIQUE, INDEX],
  name: String [REQUIRED, INDEX],

  // Hierarchy
  parentDepartmentId: String [OPTIONAL, INDEX],
  level: Integer [OPTIONAL],

  // Leadership
  headOfDepartment: String [OPTIONAL],
  managerId: String [OPTIONAL],

  // Classification
  function: String [OPTIONAL], // IT, FINANCE, HR, OPERATIONS, SALES
  costCenter: String [OPTIONAL],

  // Contact
  contactEmail: String [OPTIONAL],
  location: String [OPTIONAL],

  // Size
  employeeCount: Integer [OPTIONAL],

  // Security Context
  dataClassificationLevel: String [OPTIONAL],
  criticalAssetCount: Integer [OPTIONAL],

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
})
```

**Constraints**:
- `CREATE CONSTRAINT department_id_unique FOR (d:Department) REQUIRE d.id IS UNIQUE`
- `CREATE CONSTRAINT department_deptid_unique FOR (d:Department) REQUIRE d.departmentId IS UNIQUE`

**Indexes**:
- `CREATE INDEX department_name FOR (d:Department) ON (d.name)`
- `CREATE INDEX department_parent FOR (d:Department) ON (d.parentDepartmentId)`

---

### 7. Security Control & Mitigation Nodes

#### Control
```cypher
(:Control {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  controlId: String [REQUIRED, UNIQUE, INDEX],

  // Descriptive Properties
  name: String [REQUIRED, INDEX],
  description: String [REQUIRED],

  // Classification
  controlType: String [REQUIRED, INDEX], // PREVENTIVE, DETECTIVE, CORRECTIVE, DETERRENT, COMPENSATING
  category: String [OPTIONAL], // TECHNICAL, ADMINISTRATIVE, PHYSICAL

  // Framework Mapping
  frameworkMappings: [String] [OPTIONAL], // NIST_CSF, CIS, ISO27001
  complianceRequirements: [String] [OPTIONAL],

  // Implementation
  implementationStatus: String [OPTIONAL], // IMPLEMENTED, PARTIAL, NOT_IMPLEMENTED, PLANNED
  implementationDate: Date [OPTIONAL],
  automationLevel: String [OPTIONAL], // MANUAL, SEMI_AUTOMATED, FULLY_AUTOMATED

  // Effectiveness
  effectivenessScore: Float [OPTIONAL, INDEX], // 0.0 - 1.0
  lastAssessmentDate: DateTime [OPTIONAL],
  testingFrequency: String [OPTIONAL], // CONTINUOUS, DAILY, WEEKLY, MONTHLY, QUARTERLY, ANNUALLY

  // Ownership
  owner: String [OPTIONAL],
  responsibleParty: String [OPTIONAL],

  // Cost & Resources
  implementationCost: Float [OPTIONAL],
  operationalCost: Float [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
})
```

**Constraints**:
- `CREATE CONSTRAINT control_id_unique FOR (c:Control) REQUIRE c.id IS UNIQUE`
- `CREATE CONSTRAINT control_controlid_unique FOR (c:Control) REQUIRE c.controlId IS UNIQUE`

**Indexes**:
- `CREATE INDEX control_name FOR (c:Control) ON (c.name)`
- `CREATE INDEX control_type FOR (c:Control) ON (c.controlType)`
- `CREATE INDEX control_effectiveness FOR (c:Control) ON (c.effectivenessScore)`

---

#### Mitigation
```cypher
(:Mitigation {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  mitigationId: String [REQUIRED, UNIQUE, INDEX],

  // Descriptive Properties
  name: String [REQUIRED, INDEX],
  description: String [REQUIRED],

  // Classification
  mitigationType: String [REQUIRED], // PATCH, CONFIGURATION, POLICY, PROCEDURE, TECHNICAL, COMPENSATING
  urgency: String [OPTIONAL], // IMMEDIATE, HIGH, MEDIUM, LOW

  // Implementation
  implementationSteps: [String] [OPTIONAL],
  implementationComplexity: String [OPTIONAL], // LOW, MEDIUM, HIGH
  estimatedEffort: String [OPTIONAL],

  // Effectiveness
  effectivenessRating: Float [OPTIONAL], // 0.0 - 1.0
  riskReduction: Float [OPTIONAL], // Percentage

  // Status
  status: String [REQUIRED], // PLANNED, IN_PROGRESS, IMPLEMENTED, VERIFIED, FAILED
  implementationDate: DateTime [OPTIONAL],
  verificationDate: DateTime [OPTIONAL],

  // Ownership
  owner: String [OPTIONAL],
  implementer: String [OPTIONAL],

  // Cost & Impact
  cost: Float [OPTIONAL],
  businessImpact: String [OPTIONAL],
  downtime: String [OPTIONAL],

  // Dependencies
  prerequisites: [String] [OPTIONAL],
  dependencies: [String] [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
})
```

**Constraints**:
- `CREATE CONSTRAINT mitigation_id_unique FOR (m:Mitigation) REQUIRE m.id IS UNIQUE`
- `CREATE CONSTRAINT mitigation_mitigationid_unique FOR (m:Mitigation) REQUIRE m.mitigationId IS UNIQUE`

**Indexes**:
- `CREATE INDEX mitigation_name FOR (m:Mitigation) ON (m.name)`
- `CREATE INDEX mitigation_status FOR (m:Mitigation) ON (m.status)`
- `CREATE INDEX mitigation_urgency FOR (m:Mitigation) ON (m.urgency)`

---

### 8. Specialized Domain Nodes

#### Malware
```cypher
(:Malware {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  malwareId: String [REQUIRED, UNIQUE, INDEX],
  name: String [REQUIRED, INDEX],
  aliases: [String] [OPTIONAL],

  // Classification
  malwareType: String [REQUIRED, INDEX], // RANSOMWARE, TROJAN, WORM, ROOTKIT, SPYWARE, ADWARE
  family: String [OPTIONAL, INDEX],
  variant: String [OPTIONAL],

  // Characteristics
  capabilities: [String] [OPTIONAL],
  targetedPlatforms: [String] [OPTIONAL],
  propagationMethods: [String] [OPTIONAL],

  // Detection
  signatures: [String] [OPTIONAL],
  fileHashes: [String] [OPTIONAL],
  yara_rules: [String] [OPTIONAL],

  // Impact
  severity: String [OPTIONAL], // CRITICAL, HIGH, MEDIUM, LOW
  impactTypes: [String] [OPTIONAL],

  // Attribution
  firstSeen: DateTime [OPTIONAL, INDEX],
  lastSeen: DateTime [OPTIONAL, INDEX],
  associatedActors: [String] [OPTIONAL],

  // Metadata
  description: String [OPTIONAL],
  analysisReports: [String] [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT malware_id_unique FOR (m:Malware) REQUIRE m.id IS UNIQUE`
- `CREATE CONSTRAINT malware_malwareid_unique FOR (m:Malware) REQUIRE m.malwareId IS UNIQUE`

**Indexes**:
- `CREATE INDEX malware_name FOR (m:Malware) ON (m.name)`
- `CREATE INDEX malware_type FOR (m:Malware) ON (m.malwareType)`
- `CREATE INDEX malware_family FOR (m:Malware) ON (m.family)`
- `CREATE FULLTEXT INDEX malware_fulltext FOR (m:Malware) ON EACH [m.name, m.description]`

---

#### Exploit
```cypher
(:Exploit {
  // Identity Properties
  id: String [REQUIRED, UNIQUE, INDEX],
  exploitId: String [REQUIRED, UNIQUE, INDEX],
  name: String [REQUIRED, INDEX],

  // Classification
  exploitType: String [REQUIRED], // REMOTE, LOCAL, WEB, CLIENT_SIDE
  availabilityType: String [REQUIRED, INDEX], // PUBLIC, PRIVATE, METASPLOIT, COMMERCIAL

  // Technical Details
  targetedVulnerabilities: [String] [OPTIONAL],
  platforms: [String] [OPTIONAL],
  architectures: [String] [OPTIONAL],

  // Characteristics
  reliabilityScore: Float [OPTIONAL], // 0.0 - 1.0
  complexity: String [OPTIONAL], // LOW, MEDIUM, HIGH
  privilegesRequired: String [OPTIONAL],

  // Availability
  publicationDate: Date [OPTIONAL, INDEX],
  proofOfConcept: Boolean [OPTIONAL, INDEX],
  weaponized: Boolean [OPTIONAL, INDEX],

  // Impact
  impactSeverity: String [OPTIONAL],
  exploitEffects: [String] [OPTIONAL],

  // Metadata
  description: String [OPTIONAL],
  sourceUrl: String [OPTIONAL],
  author: String [OPTIONAL],

  // Temporal Properties
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO],

  // Embeddings
  descriptionEmbedding: [Float] [OPTIONAL],
  embeddingModel: String [OPTIONAL]
})
```

**Constraints**:
- `CREATE CONSTRAINT exploit_id_unique FOR (e:Exploit) REQUIRE e.id IS UNIQUE`
- `CREATE CONSTRAINT exploit_exploitid_unique FOR (e:Exploit) REQUIRE e.exploitId IS UNIQUE`

**Indexes**:
- `CREATE INDEX exploit_name FOR (e:Exploit) ON (e.name)`
- `CREATE INDEX exploit_availability FOR (e:Exploit) ON (e.availabilityType)`
- `CREATE INDEX exploit_weaponized FOR (e:Exploit) ON (e.weaponized)`
- `CREATE FULLTEXT INDEX exploit_fulltext FOR (e:Exploit) ON EACH [e.name, e.description]`

---

## Node Type Summary Table

| Node Type | Primary Purpose | Key Relationships | Index Count |
|-----------|----------------|-------------------|-------------|
| CVE | Vulnerability tracking | →CWE, →CAPEC, →Software | 5 |
| CWE | Weakness patterns | ←CVE, →CAPEC | 3 |
| CAPEC | Attack patterns | ←CVE, ←CWE, →MitreTechnique | 4 |
| Asset | Infrastructure inventory | →Software, →Vulnerability, →Alert | 7 |
| Software | Product tracking | ←Asset, →CVE | 5 |
| ThreatActor | Attribution | →Campaign, →TTP, →Malware | 4 |
| Campaign | Threat operations | ←ThreatActor, →Asset, →Indicator | 4 |
| Indicator | IOC management | →Alert, →ThreatActor, →Malware | 5 |
| Alert | Incident tracking | ←Indicator, →Asset, →Mitigation | 5 |
| MitreTactic | ATT&CK tactics | →MitreTechnique | 2 |
| MitreTechnique | ATT&CK techniques | ←MitreTactic, →CAPEC | 4 |
| Organization | Business context | →Department, →Asset | 2 |
| Department | Organizational structure | ←Organization, →Asset | 2 |
| Control | Security controls | →Mitigation, →Asset | 3 |
| Mitigation | Risk remediation | ←Control, →CVE, →Alert | 3 |
| Malware | Malware tracking | →ThreatActor, →Indicator, →Exploit | 4 |
| Exploit | Exploit tracking | →CVE, →Malware | 4 |

## Property Type Conventions

- **String**: Text values, max 64KB
- **Integer**: Whole numbers, -2^63 to 2^63-1
- **Float**: Decimal numbers, IEEE 754 double precision
- **Boolean**: true/false values
- **DateTime**: ISO 8601 format timestamps with timezone
- **Date**: ISO 8601 format dates (YYYY-MM-DD)
- **[Type]**: Array/list of specified type

## Naming Conventions

- **Node Labels**: PascalCase (e.g., ThreatActor, MitreTechnique)
- **Properties**: camelCase (e.g., publishedDate, cvssV3Score)
- **ID Fields**: All nodes have both `id` (internal UUID) and `[nodeType]Id` (business identifier)
- **Temporal Fields**: `createdAt`, `updatedAt` standardized across all nodes
- **Embedding Fields**: `[field]Embedding` for vector embeddings, `embeddingModel` for model tracking

## Version History

- v3.0.0 (2025-11-19): Complete node type specifications with embeddings, enhanced MITRE integration
- v2.5.0 (2025-11-11): Added malware and exploit nodes
- v2.0.0 (2025-11-01): Initial comprehensive specification

---

**Document Classification**: TECHNICAL SPECIFICATION
**Confidentiality**: INTERNAL USE
**Review Cycle**: Quarterly
**Next Review**: 2026-02-19
