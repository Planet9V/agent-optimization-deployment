# Relationship Specifications - AEON Cyber DT v3.0

**File**: 02_RELATIONSHIP_SPECIFICATIONS_v3.0_2025-11-19.md
**Created**: 2025-11-19 11:47:00 UTC
**Modified**: 2025-11-19 11:47:00 UTC
**Version**: v3.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete technical specifications for all Neo4j relationship types
**Status**: ACTIVE

## Document Overview

This document provides comprehensive technical specifications for all 50+ relationship types in the AEON Cyber Digital Twin v3.0 knowledge graph.

## Relationship Categories

### 1. Vulnerability Relationships

#### EXPLOITS
**Direction**: (CVE)-[EXPLOITS]->(CWE)
**Cardinality**: Many-to-Many
**Description**: Links CVE to the underlying weakness(es) it exploits

```cypher
-[EXPLOITS {
  // Core Properties
  exploitabilityScore: Float [OPTIONAL],
  confidenceLevel: String [OPTIONAL], // HIGH, MEDIUM, LOW

  // Context
  exploitationContext: String [OPTIONAL],
  notes: String [OPTIONAL],

  // Temporal Properties
  identifiedDate: DateTime [OPTIONAL],
  verifiedDate: DateTime [OPTIONAL],

  // Metadata
  source: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX exploits_score FOR ()-[r:EXPLOITS]-() ON (r.exploitabilityScore)`

---

#### DEMONSTRATES
**Direction**: (CVE)-[DEMONSTRATES]->(CAPEC)
**Cardinality**: Many-to-Many
**Description**: Links CVE to attack patterns that can exploit it

```cypher
-[DEMONSTRATES {
  // Applicability
  applicabilityScore: Float [OPTIONAL], // 0.0 - 1.0
  likelihood: String [OPTIONAL], // HIGH, MEDIUM, LOW

  // Context
  prerequisites: [String] [OPTIONAL],
  attackComplexity: String [OPTIONAL],

  // Evidence
  knownExploits: Boolean [OPTIONAL],
  publicExamples: [String] [OPTIONAL],

  // Metadata
  source: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX demonstrates_applicability FOR ()-[r:DEMONSTRATES]-() ON (r.applicabilityScore)`

---

#### AFFECTS
**Direction**: (CVE)-[AFFECTS]->(Software)
**Cardinality**: Many-to-Many
**Description**: Links CVE to affected software versions

```cypher
-[AFFECTS {
  // Version Scope
  versionStartIncluding: String [OPTIONAL],
  versionStartExcluding: String [OPTIONAL],
  versionEndIncluding: String [OPTIONAL],
  versionEndExcluding: String [OPTIONAL],

  // Platform Details
  cpe23Uri: String [OPTIONAL],
  configuration: String [OPTIONAL],
  vulnerable: Boolean [REQUIRED],

  // Impact
  impactScore: Float [OPTIONAL],
  exploitability: String [OPTIONAL],

  // Status
  status: String [OPTIONAL], // CONFIRMED, UNCONFIRMED, DISPUTED

  // Metadata
  source: String [OPTIONAL],
  lastVerified: DateTime [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX affects_vulnerable FOR ()-[r:AFFECTS]-() ON (r.vulnerable)`

---

#### RELATED_TO
**Direction**: (CWE)-[RELATED_TO]->(CWE)
**Cardinality**: Many-to-Many
**Description**: Links related weaknesses in the CWE taxonomy

```cypher
-[RELATED_TO {
  // Relationship Nature
  relationshipType: String [REQUIRED], // PARENT_OF, CHILD_OF, PEER_OF, STARTS_CHAIN, CAN_FOLLOW, CAN_PRECEDE

  // Hierarchy
  hierarchyLevel: Integer [OPTIONAL],
  abstraction: String [OPTIONAL],

  // Context
  relationshipNotes: String [OPTIONAL],

  // Metadata
  source: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX related_to_type FOR ()-[r:RELATED_TO]-() ON (r.relationshipType)`

---

### 2. Asset Relationships

#### RUNS
**Direction**: (Asset)-[RUNS]->(Software)
**Cardinality**: Many-to-Many
**Description**: Links assets to software/applications they run

```cypher
-[RUNS {
  // Installation Details
  installDate: Date [OPTIONAL],
  installPath: String [OPTIONAL],
  instanceId: String [OPTIONAL],

  // Configuration
  configuration: String [OPTIONAL],
  serviceAccount: String [OPTIONAL],
  port: Integer [OPTIONAL],

  // Status
  status: String [REQUIRED], // ACTIVE, INACTIVE, DISABLED
  lastSeenRunning: DateTime [OPTIONAL],

  // Usage
  usageType: String [OPTIONAL], // PRODUCTION, DEVELOPMENT, TEST, STAGING
  criticality: String [OPTIONAL],

  // Licensing
  licenseKey: String [OPTIONAL],
  licenseExpiry: Date [OPTIONAL],

  // Discovery
  discoveryMethod: String [OPTIONAL],
  lastScanned: DateTime [OPTIONAL],

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX runs_status FOR ()-[r:RUNS]-() ON (r.status)`
- `CREATE INDEX runs_usage FOR ()-[r:RUNS]-() ON (r.usageType)`

---

#### HAS_VULNERABILITY
**Direction**: (Asset)-[HAS_VULNERABILITY]->(CVE)
**Cardinality**: Many-to-Many
**Description**: Links assets to vulnerabilities affecting them

```cypher
-[HAS_VULNERABILITY {
  // Detection
  detectedDate: DateTime [REQUIRED],
  detectionMethod: String [OPTIONAL], // SCAN, MANUAL, AUTOMATED

  // Status
  status: String [REQUIRED], // OPEN, MITIGATED, REMEDIATED, ACCEPTED, FALSE_POSITIVE
  verificationStatus: String [OPTIONAL], // VERIFIED, UNVERIFIED, IN_PROGRESS

  // Risk Assessment
  assetRiskScore: Float [OPTIONAL, INDEX],
  exploitability: String [OPTIONAL],
  businessImpact: String [OPTIONAL],

  // Context
  affectedComponent: String [OPTIONAL],
  attackSurface: String [OPTIONAL], // EXTERNAL, INTERNAL, DMZ
  networkExposure: Boolean [OPTIONAL],

  // Remediation
  remediationPlan: String [OPTIONAL],
  targetRemediationDate: Date [OPTIONAL],
  remediatedDate: DateTime [OPTIONAL],

  // Assignment
  assignedTo: String [OPTIONAL],
  priorityScore: Integer [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX has_vuln_status FOR ()-[r:HAS_VULNERABILITY]-() ON (r.status)`
- `CREATE INDEX has_vuln_risk FOR ()-[r:HAS_VULNERABILITY]-() ON (r.assetRiskScore)`
- `CREATE INDEX has_vuln_detected FOR ()-[r:HAS_VULNERABILITY]-() ON (r.detectedDate)`

---

#### CONNECTS_TO
**Direction**: (Asset)-[CONNECTS_TO]->(Asset)
**Cardinality**: Many-to-Many
**Description**: Network connectivity between assets

```cypher
-[CONNECTS_TO {
  // Connection Details
  connectionType: String [REQUIRED], // NETWORK, APPLICATION, DATABASE, API
  protocol: String [OPTIONAL], // TCP, UDP, HTTP, HTTPS, SSH, RDP

  // Ports & Services
  sourcePort: Integer [OPTIONAL],
  destinationPort: Integer [OPTIONAL],
  service: String [OPTIONAL],

  // Direction
  bidirectional: Boolean [OPTIONAL],

  // Security
  encrypted: Boolean [OPTIONAL],
  authenticated: Boolean [OPTIONAL],
  authenticationMethod: String [OPTIONAL],

  // Traffic
  averageTrafficMbps: Float [OPTIONAL],
  lastSeenActive: DateTime [OPTIONAL],

  // Access Control
  firewallRuleId: String [OPTIONAL],
  aclRuleId: String [OPTIONAL],

  // Status
  status: String [REQUIRED], // ACTIVE, INACTIVE, BLOCKED

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX connects_to_type FOR ()-[r:CONNECTS_TO]-() ON (r.connectionType)`
- `CREATE INDEX connects_to_port FOR ()-[r:CONNECTS_TO]-() ON (r.destinationPort)`

---

#### BELONGS_TO
**Direction**: (Asset)-[BELONGS_TO]->(Department)
**Cardinality**: Many-to-One
**Description**: Organizational ownership of assets

```cypher
-[BELONGS_TO {
  // Ownership
  ownedSince: Date [OPTIONAL],
  ownershipType: String [OPTIONAL], // OWNED, LEASED, SHARED, MANAGED

  // Responsibility
  primaryContact: String [OPTIONAL],
  technicalContact: String [OPTIONAL],

  // Business Context
  businessJustification: String [OPTIONAL],
  costCenter: String [OPTIONAL],

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

---

### 3. Threat Actor Relationships

#### ATTRIBUTED_TO
**Direction**: (Campaign)-[ATTRIBUTED_TO]->(ThreatActor)
**Cardinality**: Many-to-One
**Description**: Attribution of campaigns to threat actors

```cypher
-[ATTRIBUTED_TO {
  // Attribution Confidence
  confidenceLevel: String [REQUIRED], // HIGH, MEDIUM, LOW, SUSPECTED
  confidenceScore: Float [OPTIONAL], // 0.0 - 1.0

  // Evidence
  attributionEvidence: [String] [OPTIONAL],
  attributionMethod: String [OPTIONAL], // TECHNICAL, BEHAVIORAL, STRATEGIC, COMBINED

  // Sources
  intelSources: [String] [OPTIONAL],
  analystNotes: String [OPTIONAL],

  // Temporal
  attributionDate: DateTime [OPTIONAL],

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX attributed_confidence FOR ()-[r:ATTRIBUTED_TO]-() ON (r.confidenceLevel)`

---

#### USES
**Direction**: (ThreatActor)-[USES]->(Malware)
**Cardinality**: Many-to-Many
**Description**: Threat actors using specific malware

```cypher
-[USES {
  // Usage Context
  firstSeen: DateTime [OPTIONAL, INDEX],
  lastSeen: DateTime [OPTIONAL, INDEX],
  frequency: String [OPTIONAL], // FREQUENT, OCCASIONAL, RARE

  // Campaign Context
  campaignIds: [String] [OPTIONAL],
  targetTypes: [String] [OPTIONAL],

  // Customization
  customized: Boolean [OPTIONAL],
  customizationDetails: String [OPTIONAL],

  // Effectiveness
  successRate: Float [OPTIONAL],

  // Intelligence
  confidenceLevel: String [OPTIONAL],
  intelSources: [String] [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX uses_first_seen FOR ()-[r:USES]-() ON (r.firstSeen)`
- `CREATE INDEX uses_last_seen FOR ()-[r:USES]-() ON (r.lastSeen)`

---

#### TARGETS
**Direction**: (Campaign)-[TARGETS]->(Asset)
**Cardinality**: Many-to-Many
**Description**: Campaign targeting specific assets

```cypher
-[TARGETS {
  // Targeting
  targetingDate: DateTime [OPTIONAL],
  targetingPhase: String [OPTIONAL], // RECONNAISSANCE, WEAPONIZATION, DELIVERY, EXPLOITATION

  // Success
  compromised: Boolean [OPTIONAL],
  compromiseDate: DateTime [OPTIONAL],

  // Attack Details
  attackVectors: [String] [OPTIONAL],
  techniquesUsed: [String] [OPTIONAL],

  // Impact
  impactLevel: String [OPTIONAL], // CRITICAL, HIGH, MEDIUM, LOW, NONE
  dataExfiltrated: Boolean [OPTIONAL],
  systemsAffected: [String] [OPTIONAL],

  // Detection
  detected: Boolean [OPTIONAL],
  detectionDate: DateTime [OPTIONAL],
  detectionMethod: String [OPTIONAL],

  // Intelligence
  confidenceLevel: String [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX targets_compromised FOR ()-[r:TARGETS]-() ON (r.compromised)`
- `CREATE INDEX targets_impact FOR ()-[r:TARGETS]-() ON (r.impactLevel)`

---

### 4. Detection & Response Relationships

#### INDICATES
**Direction**: (Indicator)-[INDICATES]->(ThreatActor|Malware|Campaign)
**Cardinality**: Many-to-Many
**Description**: IOC indicating threat actor, malware, or campaign activity

```cypher
-[INDICATES {
  // Confidence
  confidenceScore: Float [REQUIRED, INDEX], // 0.0 - 1.0
  confidenceReasoning: String [OPTIONAL],

  // Context
  indicatorContext: String [OPTIONAL],
  observationCount: Integer [OPTIONAL],

  // Validity
  validFrom: DateTime [OPTIONAL],
  validUntil: DateTime [OPTIONAL],

  // Intelligence
  intelSource: String [OPTIONAL],
  sourceReliability: String [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX indicates_confidence FOR ()-[r:INDICATES]-() ON (r.confidenceScore)`

---

#### TRIGGERED_BY
**Direction**: (Alert)-[TRIGGERED_BY]->(Indicator)
**Cardinality**: Many-to-Many
**Description**: Alert triggered by specific indicators

```cypher
-[TRIGGERED_BY {
  // Trigger Details
  triggerTime: DateTime [REQUIRED, INDEX],
  triggerRule: String [OPTIONAL],
  triggerCondition: String [OPTIONAL],

  // Match Details
  matchType: String [OPTIONAL], // EXACT, FUZZY, PATTERN, BEHAVIORAL
  matchConfidence: Float [OPTIONAL],

  // Context
  observedValue: String [OPTIONAL],
  observationCount: Integer [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX triggered_time FOR ()-[r:TRIGGERED_BY]-() ON (r.triggerTime)`

---

#### RELATED_ALERT
**Direction**: (Alert)-[RELATED_ALERT]->(Alert)
**Cardinality**: Many-to-Many
**Description**: Correlation between related alerts

```cypher
-[RELATED_ALERT {
  // Correlation
  correlationType: String [REQUIRED], // SAME_INCIDENT, SAME_ACTOR, SAME_CAMPAIGN, SAME_ASSET, TEMPORAL
  correlationScore: Float [OPTIONAL, INDEX], // 0.0 - 1.0

  // Temporal
  temporalProximity: Integer [OPTIONAL], // Seconds between alerts

  // Analysis
  correlationMethod: String [OPTIONAL], // AUTOMATED, MANUAL, ML
  correlationReasoning: String [OPTIONAL],

  // Metadata
  correlatedBy: String [OPTIONAL],
  correlationDate: DateTime [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX related_alert_type FOR ()-[r:RELATED_ALERT]-() ON (r.correlationType)`
- `CREATE INDEX related_alert_score FOR ()-[r:RELATED_ALERT]-() ON (r.correlationScore)`

---

### 5. MITRE ATT&CK Relationships

#### PART_OF
**Direction**: (MitreTechnique)-[PART_OF]->(MitreTactic)
**Cardinality**: Many-to-Many
**Description**: Techniques belonging to tactics in ATT&CK framework

```cypher
-[PART_OF {
  // Framework Context
  matrix: String [REQUIRED], // ENTERPRISE, MOBILE, ICS
  version: String [OPTIONAL],

  // Ordering
  ordinal: Integer [OPTIONAL],

  // Metadata
  source: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX part_of_matrix FOR ()-[r:PART_OF]-() ON (r.matrix)`

---

#### SUBTECHNIQUE_OF
**Direction**: (MitreTechnique)-[SUBTECHNIQUE_OF]->(MitreTechnique)
**Cardinality**: Many-to-One
**Description**: Sub-technique relationship in ATT&CK hierarchy

```cypher
-[SUBTECHNIQUE_OF {
  // Hierarchy
  hierarchyLevel: Integer [OPTIONAL],

  // Metadata
  source: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

---

#### IMPLEMENTS
**Direction**: (CAPEC)-[IMPLEMENTS]->(MitreTechnique)
**Cardinality**: Many-to-Many
**Description**: Attack patterns implementing ATT&CK techniques

```cypher
-[IMPLEMENTS {
  // Mapping Details
  mappingType: String [OPTIONAL], // DIRECT, RELATED, SIMILAR
  mappingConfidence: Float [OPTIONAL],

  // Context
  implementationNotes: String [OPTIONAL],

  // Metadata
  source: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

---

#### USES_TECHNIQUE
**Direction**: (ThreatActor|Campaign)-[USES_TECHNIQUE]->(MitreTechnique)
**Cardinality**: Many-to-Many
**Description**: Threat actors/campaigns using specific ATT&CK techniques

```cypher
-[USES_TECHNIQUE {
  // Observation
  firstObserved: DateTime [OPTIONAL, INDEX],
  lastObserved: DateTime [OPTIONAL, INDEX],
  observationCount: Integer [OPTIONAL],

  // Frequency
  frequency: String [OPTIONAL], // FREQUENT, COMMON, OCCASIONAL, RARE

  // Context
  usageContext: String [OPTIONAL],
  targetTypes: [String] [OPTIONAL],

  // Effectiveness
  successRate: Float [OPTIONAL],

  // Intelligence
  confidenceLevel: String [OPTIONAL], // HIGH, MEDIUM, LOW
  intelSources: [String] [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX uses_technique_first FOR ()-[r:USES_TECHNIQUE]-() ON (r.firstObserved)`
- `CREATE INDEX uses_technique_last FOR ()-[r:USES_TECHNIQUE]-() ON (r.lastObserved)`

---

### 6. Control & Mitigation Relationships

#### MITIGATES
**Direction**: (Control|Mitigation)-[MITIGATES]->(CVE|CWE|CAPEC|MitreTechnique)
**Cardinality**: Many-to-Many
**Description**: Controls/mitigations addressing vulnerabilities or techniques

```cypher
-[MITIGATES {
  // Effectiveness
  effectivenessScore: Float [OPTIONAL, INDEX], // 0.0 - 1.0
  effectivenessLevel: String [OPTIONAL], // FULL, PARTIAL, MINIMAL

  // Risk Reduction
  riskReductionPercentage: Float [OPTIONAL],
  residualRisk: String [OPTIONAL],

  // Implementation
  implementationStatus: String [OPTIONAL], // IMPLEMENTED, PLANNED, IN_PROGRESS
  implementationDate: DateTime [OPTIONAL],

  // Verification
  lastVerified: DateTime [OPTIONAL],
  verificationMethod: String [OPTIONAL],
  testResults: String [OPTIONAL],

  // Context
  mitigationNotes: String [OPTIONAL],
  limitations: [String] [OPTIONAL],

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX mitigates_effectiveness FOR ()-[r:MITIGATES]-() ON (r.effectivenessScore)`
- `CREATE INDEX mitigates_status FOR ()-[r:MITIGATES]-() ON (r.implementationStatus)`

---

#### PROTECTS
**Direction**: (Control)-[PROTECTS]->(Asset)
**Cardinality**: Many-to-Many
**Description**: Security controls protecting assets

```cypher
-[PROTECTS {
  // Coverage
  coverageScope: String [OPTIONAL], // FULL, PARTIAL, SPECIFIC
  protectionType: String [OPTIONAL], // PREVENTIVE, DETECTIVE, CORRECTIVE

  // Effectiveness
  effectivenessScore: Float [OPTIONAL, INDEX],
  lastAssessment: DateTime [OPTIONAL],

  // Configuration
  configurationStatus: String [OPTIONAL], // OPTIMAL, ACCEPTABLE, NEEDS_IMPROVEMENT
  configurationNotes: String [OPTIONAL],

  // Monitoring
  monitoringEnabled: Boolean [OPTIONAL],
  alertsEnabled: Boolean [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX protects_effectiveness FOR ()-[r:PROTECTS]-() ON (r.effectivenessScore)`

---

#### REQUIRES
**Direction**: (Mitigation)-[REQUIRES]->(Mitigation|Control)
**Cardinality**: Many-to-Many
**Description**: Dependencies between mitigations or controls

```cypher
-[REQUIRES {
  // Dependency Type
  dependencyType: String [REQUIRED], // PREREQUISITE, COMPLEMENTARY, ALTERNATIVE

  // Criticality
  critical: Boolean [OPTIONAL],
  priority: Integer [OPTIONAL],

  // Context
  dependencyReason: String [OPTIONAL],

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

---

### 7. Organizational Relationships

#### EMPLOYED_BY
**Direction**: (User)-[EMPLOYED_BY]->(Department)
**Cardinality**: Many-to-One
**Description**: User employment relationships (for NER10 integration)

```cypher
-[EMPLOYED_BY {
  // Employment Details
  startDate: Date [OPTIONAL],
  endDate: Date [OPTIONAL],
  employmentType: String [OPTIONAL], // FULL_TIME, PART_TIME, CONTRACTOR, VENDOR

  // Role
  jobTitle: String [OPTIONAL],
  roleType: String [OPTIONAL],
  clearanceLevel: String [OPTIONAL],

  // Status
  status: String [REQUIRED], // ACTIVE, INACTIVE, TERMINATED, ON_LEAVE

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

---

#### PART_OF_ORG
**Direction**: (Department)-[PART_OF_ORG]->(Organization)
**Cardinality**: Many-to-One
**Description**: Department belonging to organization

```cypher
-[PART_OF_ORG {
  // Hierarchy
  hierarchyLevel: Integer [OPTIONAL],

  // Effective Date
  effectiveFrom: Date [OPTIONAL],
  effectiveTo: Date [OPTIONAL],

  // Metadata
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

---

### 8. Specialized Domain Relationships

#### EXPLOITED_BY
**Direction**: (CVE)-[EXPLOITED_BY]->(Exploit)
**Cardinality**: Many-to-Many
**Description**: CVE exploited by specific exploit code

```cypher
-[EXPLOITED_BY {
  // Exploit Details
  exploitReliability: Float [OPTIONAL], // 0.0 - 1.0
  exploitComplexity: String [OPTIONAL], // LOW, MEDIUM, HIGH

  // Availability
  publiclyAvailable: Boolean [OPTIONAL, INDEX],
  weaponized: Boolean [OPTIONAL, INDEX],
  availabilityDate: Date [OPTIONAL],

  // Context
  exploitPlatforms: [String] [OPTIONAL],
  exploitRequirements: [String] [OPTIONAL],

  // Intelligence
  observedInWild: Boolean [OPTIONAL, INDEX],
  firstObserved: DateTime [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

**Indexes**:
- `CREATE INDEX exploited_public FOR ()-[r:EXPLOITED_BY]-() ON (r.publiclyAvailable)`
- `CREATE INDEX exploited_weaponized FOR ()-[r:EXPLOITED_BY]-() ON (r.weaponized)`
- `CREATE INDEX exploited_wild FOR ()-[r:EXPLOITED_BY]-() ON (r.observedInWild)`

---

#### DELIVERS
**Direction**: (Malware)-[DELIVERS]->(Malware)
**Cardinality**: Many-to-Many
**Description**: Malware delivering other malware (droppers, loaders)

```cypher
-[DELIVERS {
  // Delivery Mechanism
  deliveryMethod: String [OPTIONAL], // DROPPER, LOADER, DOWNLOADER, INJECTOR
  deliveryStage: String [OPTIONAL], // INITIAL, SECONDARY, TERTIARY

  // Timing
  deliveryDelay: Integer [OPTIONAL], // Seconds
  deliveryCondition: String [OPTIONAL],

  // Persistence
  persistenceMethod: [String] [OPTIONAL],

  // Detection
  detectionDifficulty: String [OPTIONAL], // LOW, MEDIUM, HIGH

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

---

#### VARIANT_OF
**Direction**: (Malware)-[VARIANT_OF]->(Malware)
**Cardinality**: Many-to-One
**Description**: Malware variants and their base families

```cypher
-[VARIANT_OF {
  // Variant Details
  variantName: String [OPTIONAL],
  variantType: String [OPTIONAL], // MINOR, MAJOR, REWRITE

  // Differences
  differenceDescription: String [OPTIONAL],
  newCapabilities: [String] [OPTIONAL],
  removedCapabilities: [String] [OPTIONAL],

  // Detection
  signatureSimilarity: Float [OPTIONAL], // 0.0 - 1.0
  behaviorSimilarity: Float [OPTIONAL],

  // Temporal
  variantFirstSeen: DateTime [OPTIONAL],

  // Metadata
  notes: String [OPTIONAL],
  createdAt: DateTime [REQUIRED, AUTO],
  updatedAt: DateTime [REQUIRED, AUTO]
}]->
```

---

## Relationship Summary Table

| Relationship | From Node | To Node | Cardinality | Key Properties |
|--------------|-----------|---------|-------------|----------------|
| EXPLOITS | CVE | CWE | M:M | exploitabilityScore |
| DEMONSTRATES | CVE | CAPEC | M:M | applicabilityScore, likelihood |
| AFFECTS | CVE | Software | M:M | versionRange, vulnerable |
| RELATED_TO | CWE | CWE | M:M | relationshipType, hierarchyLevel |
| RUNS | Asset | Software | M:M | status, usageType, installDate |
| HAS_VULNERABILITY | Asset | CVE | M:M | status, assetRiskScore, detectedDate |
| CONNECTS_TO | Asset | Asset | M:M | connectionType, protocol, ports |
| BELONGS_TO | Asset | Department | M:1 | ownershipType, primaryContact |
| ATTRIBUTED_TO | Campaign | ThreatActor | M:1 | confidenceLevel, evidence |
| USES | ThreatActor | Malware | M:M | frequency, firstSeen, lastSeen |
| TARGETS | Campaign | Asset | M:M | compromised, impactLevel |
| INDICATES | Indicator | ThreatActor/Malware/Campaign | M:M | confidenceScore, context |
| TRIGGERED_BY | Alert | Indicator | M:M | triggerTime, matchType |
| RELATED_ALERT | Alert | Alert | M:M | correlationType, correlationScore |
| PART_OF | MitreTechnique | MitreTactic | M:M | matrix, ordinal |
| SUBTECHNIQUE_OF | MitreTechnique | MitreTechnique | M:1 | hierarchyLevel |
| IMPLEMENTS | CAPEC | MitreTechnique | M:M | mappingType, confidence |
| USES_TECHNIQUE | ThreatActor/Campaign | MitreTechnique | M:M | frequency, observationCount |
| MITIGATES | Control/Mitigation | CVE/CWE/CAPEC/MitreTechnique | M:M | effectivenessScore, riskReduction |
| PROTECTS | Control | Asset | M:M | coverageScope, effectivenessScore |
| REQUIRES | Mitigation | Mitigation/Control | M:M | dependencyType, critical |
| EMPLOYED_BY | User | Department | M:1 | employmentType, status |
| PART_OF_ORG | Department | Organization | M:1 | hierarchyLevel |
| EXPLOITED_BY | CVE | Exploit | M:M | publiclyAvailable, weaponized |
| DELIVERS | Malware | Malware | M:M | deliveryMethod, deliveryStage |
| VARIANT_OF | Malware | Malware | M:1 | variantType, similarity |

## Relationship Property Patterns

### Temporal Properties (All Relationships)
- `createdAt`: DateTime [REQUIRED, AUTO]
- `updatedAt`: DateTime [REQUIRED, AUTO]

### Common Property Types
- **Confidence Scores**: Float 0.0 - 1.0, indexed for filtering
- **Status Fields**: Enumerated strings, indexed for workflow
- **Temporal Ranges**: validFrom/validUntil, firstSeen/lastSeen
- **Evidence Arrays**: Lists of supporting information
- **Source Attribution**: Data source and reliability indicators

### Performance Optimization
- **Selective Indexing**: Only frequently queried properties
- **Composite Keys**: Combine node IDs for unique relationship identification
- **Temporal Queries**: Index all date/time fields used in range queries
- **Score Filtering**: Index all float fields used for threshold filtering

## Relationship Naming Conventions

- **Active Voice**: Use action verbs (RUNS, TARGETS, MITIGATES)
- **Direction Clarity**: From source → to target logically
- **All Caps**: Relationship types in uppercase
- **Underscore Separation**: Multi-word relationships use underscores (HAS_VULNERABILITY)

## Query Patterns

### Most Common Relationship Traversals

```cypher
// Asset vulnerability exposure
MATCH (a:Asset)-[r:HAS_VULNERABILITY]->(c:CVE)
WHERE r.status = 'OPEN'
RETURN a, r, c

// Threat actor TTPs
MATCH (ta:ThreatActor)-[u:USES_TECHNIQUE]->(t:MitreTechnique)-[p:PART_OF]->(tac:MitreTactic)
RETURN ta, u, t, p, tac

// Attack path analysis
MATCH (a1:Asset)-[c:CONNECTS_TO*1..3]->(a2:Asset)-[h:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.baseSeverity IN ['HIGH', 'CRITICAL']
RETURN a1, c, a2, h, cve

// Mitigation coverage
MATCH (asset:Asset)-[hv:HAS_VULNERABILITY]->(cve:CVE)
OPTIONAL MATCH (m:Mitigation)-[mit:MITIGATES]->(cve)
RETURN asset, cve, collect(m) as mitigations

// Campaign attribution chain
MATCH (c:Campaign)-[a:ATTRIBUTED_TO]->(ta:ThreatActor)-[u:USES]->(m:Malware)
WHERE a.confidenceLevel IN ['HIGH', 'MEDIUM']
RETURN c, a, ta, u, m
```

## Version History

- v3.0.0 (2025-11-19): Complete relationship specifications with advanced properties
- v2.5.0 (2025-11-11): Added malware and exploit relationships
- v2.0.0 (2025-11-01): Initial comprehensive specification

---

**Document Classification**: TECHNICAL SPECIFICATION
**Confidentiality**: INTERNAL USE
**Review Cycle**: Quarterly
**Next Review**: 2026-02-19
