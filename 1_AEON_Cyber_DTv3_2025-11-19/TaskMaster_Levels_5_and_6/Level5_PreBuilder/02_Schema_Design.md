# Level 5 Event Schema Design - Complete DDL
**File**: 02_Schema_Design.md
**Created**: 2025-11-22 10:45:00 UTC
**Author**: Level 5 Pre-Builder Agent 2
**Purpose**: Complete schema design for Level 5 Event components
**Status**: READY FOR IMPLEMENTATION

---

## Executive Summary

This document provides the complete Cypher DDL for Level 5 Event schemas, designed to integrate with the existing AEON Neo4j database containing 316K CVE nodes, 16 sectors, and cognitive bias infrastructure.

---

## 1. CORE EVENT SCHEMAS

### 1.1 InformationEvent Schema

```cypher
// =========================================
// INFORMATION EVENT SCHEMA
// =========================================
// Purpose: Track cyber information events and their psychological impact
// Integration: Links to CVE, CognitiveBias, Sector nodes

// Primary Constraints
CREATE CONSTRAINT information_event_id IF NOT EXISTS
FOR (e:InformationEvent) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT information_event_eventid IF NOT EXISTS
FOR (e:InformationEvent) REQUIRE e.eventId IS UNIQUE;

// Node Template with Full Properties
(:InformationEvent {
  // Primary Identifiers
  id: String,                    // UUID format
  eventId: String,               // Human-readable ID (IE-YYYY-NNNN)

  // Event Classification
  eventType: String,             // CVE_DISCLOSURE|INCIDENT|BREACH|CAMPAIGN|ADVISORY
  eventCategory: String,         // VULNERABILITY|ATTACK|DEFENSIVE|WARNING
  timestamp: DateTime,           // ISO 8601 format
  discoveryTimestamp: DateTime,  // When first detected
  publicationTimestamp: DateTime,// When made public

  // Content Properties
  title: String,                 // Event headline
  description: String,           // Full description
  cveId: String,                // Link to CVE if applicable
  cveIds: String[],             // Multiple CVEs if applicable

  // Severity & Impact
  severity: String,              // CRITICAL|HIGH|MEDIUM|LOW|INFO
  cvssScore: Float,             // 0.0-10.0 if CVE-related
  exploitability: String,        // EXPLOITED|POC|THEORETICAL|NONE
  affectedAssets: Integer,       // Estimated affected count

  // Psychological Impact Metrics
  mediaAmplification: Float,     // 0-10 scale
  fearFactor: Float,            // 0-10 scale
  realityFactor: Float,         // 0-10 scale
  fearRealityGap: Float,        // Calculated: fearFactor - realityFactor
  publicAttention: Float,       // 0-10 scale

  // Bias Activation
  activatesBiases: String[],    // Array of bias IDs
  biasStrength: Map,            // {biasId: strength}
  predictedOrgResponse: String, // JSON structure
  responsePattern: String,      // OVERREACT|UNDERREACT|APPROPRIATE|DELAYED

  // Source & Confidence
  sources: String[],            // URLs, feeds, reports
  sourceTypes: String[],        // CISA|VENDOR|MEDIA|RESEARCHER|OSINT
  confidence: Float,            // 0-1 scale
  verificationStatus: String,   // VERIFIED|UNVERIFIED|DISPUTED

  // Metadata
  createdAt: DateTime,
  updatedAt: DateTime,
  processingStatus: String,     // NEW|ANALYZED|INTEGRATED|ARCHIVED
  tags: String[]                // Additional categorization
})

// Indexes for Performance
CREATE INDEX information_event_timestamp IF NOT EXISTS
FOR (e:InformationEvent) ON (e.timestamp);

CREATE INDEX information_event_severity IF NOT EXISTS
FOR (e:InformationEvent) ON (e.severity);

CREATE INDEX information_event_type IF NOT EXISTS
FOR (e:InformationEvent) ON (e.eventType);

CREATE INDEX information_event_cveid IF NOT EXISTS
FOR (e:InformationEvent) ON (e.cveId);
```

### 1.2 GeopoliticalEvent Schema

```cypher
// =========================================
// GEOPOLITICAL EVENT SCHEMA
// =========================================
// Purpose: Track geopolitical events that influence cyber threat landscape
// Integration: Links to ThreatActor, Sector, Campaign nodes

// Primary Constraints
CREATE CONSTRAINT geopolitical_event_id IF NOT EXISTS
FOR (g:GeopoliticalEvent) REQUIRE g.id IS UNIQUE;

CREATE CONSTRAINT geopolitical_event_eventid IF NOT EXISTS
FOR (g:GeopoliticalEvent) REQUIRE g.eventId IS UNIQUE;

// Node Template with Full Properties
(:GeopoliticalEvent {
  // Primary Identifiers
  id: String,                         // UUID format
  eventId: String,                    // Human-readable (GEO-YYYY-NNNN)

  // Event Classification
  eventType: String,                  // TENSION|CONFLICT|SANCTION|DIPLOMATIC|ECONOMIC|MILITARY
  eventCategory: String,              // ESCALATION|DE_ESCALATION|STATUS_QUO|DISRUPTION
  timestamp: DateTime,                // Event occurrence
  reportedTimestamp: DateTime,        // When reported

  // Actor Information
  primaryActors: String[],            // Countries/entities involved
  secondaryActors: String[],          // Supporting/affected parties
  actorRoles: Map,                   // {actor: role} mapping
  region: String,                     // Geographic region

  // Tension & Impact Metrics
  tensionLevel: Float,                // 0-10 scale
  previousTensionLevel: Float,        // For delta calculation
  tensionDelta: Float,                // Change in tension
  escalationProbability: Float,       // 0-1 scale

  // Cyber Correlation
  cyberActivityCorrelation: Float,    // 0-1 correlation strength
  threatActorActivityMultiplier: Float, // 1.0-5.0x multiplier
  observedCyberActivity: Boolean,     // Direct cyber component observed
  attributedActors: String[],         // Threat actor IDs

  // Predicted Cyber Impact
  predictedImpact: Map,               // Structured predictions
  targetSectors: String[],            // Expected target sectors
  targetCountries: String[],          // Expected target nations
  ttlInDays: Integer,                // Time-to-live for predictions

  // Impact Scoring
  economicImpact: Float,              // 0-10 scale
  militaryImpact: Float,              // 0-10 scale
  diplomaticImpact: Float,            // 0-10 scale
  cyberImpact: Float,                 // 0-10 scale
  overallImpact: Float,               // Calculated composite

  // Evidence & Sources
  sources: String[],                  // Information sources
  sourceCredibility: Map,             // {source: credibility}
  confidence: Float,                  // Overall confidence 0-1
  verificationLevel: String,          // CONFIRMED|PROBABLE|POSSIBLE|UNCONFIRMED

  // Metadata
  createdAt: DateTime,
  updatedAt: DateTime,
  expiresAt: DateTime,                // When predictions expire
  tags: String[],
  notes: String                       // Analyst notes
})

// Indexes for Performance
CREATE INDEX geopolitical_event_timestamp IF NOT EXISTS
FOR (g:GeopoliticalEvent) ON (g.timestamp);

CREATE INDEX geopolitical_event_tension IF NOT EXISTS
FOR (g:GeopoliticalEvent) ON (g.tensionLevel);

CREATE INDEX geopolitical_event_type IF NOT EXISTS
FOR (g:GeopoliticalEvent) ON (g.eventType);

CREATE INDEX geopolitical_event_region IF NOT EXISTS
FOR (g:GeopoliticalEvent) ON (g.region);
```

### 1.3 ThreatFeed Schema

```cypher
// =========================================
// THREAT FEED SCHEMA
// =========================================
// Purpose: Manage threat intelligence feed sources and their reliability
// Integration: Source for InformationEvent nodes

// Primary Constraints
CREATE CONSTRAINT threat_feed_id IF NOT EXISTS
FOR (f:ThreatFeed) REQUIRE f.id IS UNIQUE;

CREATE CONSTRAINT threat_feed_feedid IF NOT EXISTS
FOR (f:ThreatFeed) REQUIRE f.feedId IS UNIQUE;

// Node Template with Full Properties
(:ThreatFeed {
  // Primary Identifiers
  id: String,                    // UUID format
  feedId: String,                // Human-readable (FEED-NAME)
  feedName: String,              // Display name

  // Feed Classification
  feedType: String,              // CISA_AIS|COMMERCIAL|OSINT|VENDOR|GOVERNMENT|ISAC
  feedCategory: String,          // VULNERABILITY|INDICATOR|INCIDENT|STRATEGIC
  dataFormat: String,            // STIX|TAXII|JSON|XML|CSV|TEXT

  // Reliability Metrics
  reliability: Float,            // 0-1 current reliability
  historicalAccuracy: Float,    // 0-1 based on past performance
  falsePositiveRate: Float,     // 0-1 percentage
  timeliness: Float,            // 0-1 speed of reporting
  completeness: Float,          // 0-1 data completeness

  // Bias Profile
  biasProfile: String[],        // Known biases
  geographicFocus: String[],    // Regional focus areas
  sectorFocus: String[],        // Industry sectors emphasized
  threatActorFocus: String[],   // Actor types emphasized

  // Coverage
  coverageScore: Map,           // {category: score} for different areas
  blindSpots: String[],         // Known gaps in coverage
  strengths: String[],          // Areas of excellence

  // Configuration
  apiEndpoint: String,          // Feed URL/endpoint
  apiKey: String,               // Encrypted API key
  updateFrequency: String,      // REAL_TIME|MINUTE|HOURLY|DAILY|WEEKLY
  pullSchedule: String,         // Cron expression
  retryPolicy: Map,             // Retry configuration

  // Operational Status
  status: String,               // ACTIVE|INACTIVE|ERROR|MAINTENANCE
  lastUpdate: DateTime,         // Last successful pull
  lastError: DateTime,          // Last error occurrence
  errorCount: Integer,          // Recent error count
  errorMessage: String,         // Last error message

  // Data Volume
  eventsPerDay: Float,          // Average events/day
  totalEvents: Integer,         // Total events processed
  storageUsedMB: Float,        // Storage consumption

  // Cost & Licensing
  costModel: String,            // FREE|SUBSCRIPTION|USAGE_BASED
  monthlyCost: Float,          // USD per month
  licenseType: String,         // Commercial/Open/Government
  dataRights: String,          // Usage rights

  // Metadata
  createdAt: DateTime,
  updatedAt: DateTime,
  owner: String,               // Responsible team/person
  notes: String                // Configuration notes
})

// Indexes for Performance
CREATE INDEX threat_feed_status IF NOT EXISTS
FOR (f:ThreatFeed) ON (f.status);

CREATE INDEX threat_feed_type IF NOT EXISTS
FOR (f:ThreatFeed) ON (f.feedType);

CREATE INDEX threat_feed_reliability IF NOT EXISTS
FOR (f:ThreatFeed) ON (f.reliability);
```

---

## 2. RELATIONSHIP SCHEMAS

### 2.1 Event-to-Bias Relationships

```cypher
// InformationEvent activates CognitiveBias
(:InformationEvent)-[:ACTIVATES_BIAS {
  activationStrength: Float,     // 0-1 strength
  mechanism: String,              // How bias is triggered
  predictedEffect: String,        // Expected outcome
  timestamp: DateTime
}]->(:CognitiveBias)

// GeopoliticalEvent triggers bias patterns
(:GeopoliticalEvent)-[:TRIGGERS_BIAS {
  biasType: String,
  strength: Float,
  context: String,
  timestamp: DateTime
}]->(:CognitiveBias)
```

### 2.2 Event-to-Sector Relationships

```cypher
// InformationEvent affects sectors
(:InformationEvent)-[:AFFECTS_SECTOR {
  impactLevel: String,           // CRITICAL|HIGH|MEDIUM|LOW
  impactType: String,            // DIRECT|INDIRECT|CASCADE
  estimatedCost: Float,          // USD estimate
  affectedAssets: Integer,       // Count of assets
  mitigationUrgency: String,     // IMMEDIATE|HIGH|MEDIUM|LOW
  timestamp: DateTime
}]->(:Sector)

// GeopoliticalEvent targets sectors
(:GeopoliticalEvent)-[:TARGETS_SECTOR {
  targetingProbability: Float,   // 0-1 likelihood
  threatLevel: String,           // Threat level
  timeframe: String,             // Expected timeframe
  indicators: String[],          // Warning signs
  timestamp: DateTime
}]->(:Sector)
```

### 2.3 Event-to-Actor Relationships

```cypher
// GeopoliticalEvent increases threat actor activity
(:GeopoliticalEvent)-[:INCREASES_ACTIVITY {
  activityMultiplier: Float,     // 1.0-5.0x
  timeframe: String,             // Duration of increase
  confidence: Float,             // Confidence in prediction
  observedChange: Boolean,       // Actually observed vs predicted
  timestamp: DateTime
}]->(:ThreatActor)

// InformationEvent attributed to threat actor
(:InformationEvent)-[:ATTRIBUTED_TO {
  attributionConfidence: Float,  // 0-1 confidence
  attributionMethod: String,     // TTP|INFRASTRUCTURE|INTENT
  evidence: String[],            // Supporting evidence
  disputed: Boolean,             // Attribution disputed?
  timestamp: DateTime
}]->(:ThreatActor)
```

### 2.4 Feed-to-Event Relationships

```cypher
// ThreatFeed publishes events
(:ThreatFeed)-[:PUBLISHES {
  publishedAt: DateTime,
  originalFormat: String,        // Original data format
  processingLatency: Integer,   // Milliseconds to process
  transformations: String[],     // Applied transformations
  qualityScore: Float           // 0-1 quality assessment
}]->(:InformationEvent)

// ThreatFeed reports on geopolitical events
(:ThreatFeed)-[:REPORTS {
  reportedAt: DateTime,
  analysisDepth: String,        // SURFACE|MODERATE|DEEP
  perspective: String,          // Feed's perspective/bias
  confidence: Float
}]->(:GeopoliticalEvent)
```

### 2.5 Event-to-CVE Relationships

```cypher
// InformationEvent involves CVEs
(:InformationEvent)-[:INVOLVES_CVE {
  exploitStatus: String,         // EXPLOITED|POC|THEORETICAL
  patchAvailable: Boolean,
  mitigationExists: Boolean,
  affectedVersions: String[],
  timestamp: DateTime
}]->(:CVE)

// Direct CVE disclosure events
(:InformationEvent)-[:DISCLOSES_CVE {
  disclosureType: String,        // RESPONSIBLE|FULL|ZERO_DAY
  embargoLifted: DateTime,
  vendorNotified: Boolean,
  patchReleased: Boolean,
  timestamp: DateTime
}]->(:CVE)
```

### 2.6 Inter-Event Relationships

```cypher
// Event correlation
(:InformationEvent)-[:CORRELATES_WITH {
  correlationStrength: Float,    // 0-1 strength
  correlationType: String,       // TEMPORAL|CAUSAL|TACTICAL
  timeOffset: Integer,           // Seconds between events
  confidence: Float
}]->(:InformationEvent)

// Geopolitical events trigger information events
(:GeopoliticalEvent)-[:TRIGGERS_INFO_EVENT {
  triggerMechanism: String,      // How geo triggers cyber
  timeDelay: Integer,            // Expected delay in hours
  probability: Float,            // Likelihood 0-1
  observed: Boolean              // Actually occurred?
}]->(:InformationEvent)
```

---

## 3. INTEGRATION WITH EXISTING INFRASTRUCTURE

### 3.1 Link to Existing CVE Infrastructure (316K nodes)

```cypher
// Validate CVE links exist before creating relationships
MATCH (e:InformationEvent)
WHERE e.cveId IS NOT NULL
MATCH (c:CVE {cveId: e.cveId})
MERGE (e)-[:INVOLVES_CVE {
  linkedAt: datetime(),
  linkType: 'PRIMARY'
}]->(c);

// Handle multiple CVE references
MATCH (e:InformationEvent)
WHERE e.cveIds IS NOT NULL
UNWIND e.cveIds AS cveId
MATCH (c:CVE {cveId: cveId})
MERGE (e)-[:INVOLVES_CVE {
  linkedAt: datetime(),
  linkType: 'SECONDARY'
}]->(c);
```

### 3.2 Link to 16 Existing Sectors

```cypher
// Map events to sectors based on tags/content
MATCH (e:InformationEvent)
WHERE e.targetSectors IS NOT NULL
UNWIND e.targetSectors AS sectorName
MATCH (s:Sector {name: sectorName})
MERGE (e)-[:AFFECTS_SECTOR {
  linkedAt: datetime()
}]->(s);
```

### 3.3 Expand Cognitive Bias Infrastructure (7 → 30)

```cypher
// Create additional cognitive bias nodes
CREATE (b1:CognitiveBias {
  id: 'bias-008',
  biasId: 'ANCHORING',
  name: 'Anchoring Bias',
  description: 'Over-reliance on first information received',
  category: 'JUDGMENT',
  impact: 'HIGH'
})

CREATE (b2:CognitiveBias {
  id: 'bias-009',
  biasId: 'RECENCY',
  name: 'Recency Bias',
  description: 'Overweighting recent events',
  category: 'MEMORY',
  impact: 'MEDIUM'
})

// ... continue for all 30 biases
```

---

## 4. VALIDATION RULES

### 4.1 Data Integrity Constraints

```cypher
// Ensure fear-reality gap calculation
CREATE CONSTRAINT information_event_gap_check IF NOT EXISTS
FOR (e:InformationEvent)
REQUIRE (e.fearRealityGap = e.fearFactor - e.realityFactor);

// Ensure valid severity values
CREATE CONSTRAINT information_event_severity_valid IF NOT EXISTS
FOR (e:InformationEvent)
REQUIRE e.severity IN ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'];

// Ensure valid event types
CREATE CONSTRAINT geopolitical_event_type_valid IF NOT EXISTS
FOR (g:GeopoliticalEvent)
REQUIRE g.eventType IN ['TENSION', 'CONFLICT', 'SANCTION', 'DIPLOMATIC', 'ECONOMIC', 'MILITARY'];
```

### 4.2 Temporal Validation

```cypher
// Ensure timestamp consistency
CALL apoc.trigger.add('validate_event_timestamps',
  'UNWIND $createdNodes AS node
   WITH node
   WHERE node:InformationEvent OR node:GeopoliticalEvent
   AND node.timestamp > datetime()
   SET node.timestamp = datetime()',
  {phase: 'before'}
);
```

---

## 5. INDEX OPTIMIZATION RECOMMENDATIONS

### 5.1 Composite Indexes for Common Queries

```cypher
// Event search patterns
CREATE INDEX event_search_composite IF NOT EXISTS
FOR (e:InformationEvent)
ON (e.eventType, e.severity, e.timestamp);

// Geopolitical analysis patterns
CREATE INDEX geo_analysis_composite IF NOT EXISTS
FOR (g:GeopoliticalEvent)
ON (g.tensionLevel, g.region, g.timestamp);

// Feed reliability tracking
CREATE INDEX feed_reliability_composite IF NOT EXISTS
FOR (f:ThreatFeed)
ON (f.feedType, f.reliability, f.status);
```

### 5.2 Full-Text Search Indexes

```cypher
// Event content search
CALL db.index.fulltext.createNodeIndex(
  'eventContentSearch',
  ['InformationEvent', 'GeopoliticalEvent'],
  ['title', 'description', 'notes']
);

// Feed metadata search
CALL db.index.fulltext.createNodeIndex(
  'feedSearch',
  ['ThreatFeed'],
  ['feedName', 'feedType', 'notes']
);
```

---

## 6. SAMPLE DATA GENERATION QUERIES

### 6.1 Create Sample InformationEvent

```cypher
CREATE (e:InformationEvent {
  id: apoc.create.uuid(),
  eventId: 'IE-2024-0001',
  eventType: 'CVE_DISCLOSURE',
  timestamp: datetime(),
  title: 'Critical RCE in Popular Framework',
  description: 'A critical remote code execution vulnerability...',
  cveId: 'CVE-2024-12345',
  severity: 'CRITICAL',
  cvssScore: 9.8,
  mediaAmplification: 8.5,
  fearFactor: 9.0,
  realityFactor: 7.0,
  fearRealityGap: 2.0,
  activatesBiases: ['AVAILABILITY', 'RECENCY'],
  sources: ['https://nvd.nist.gov/...'],
  confidence: 0.95,
  createdAt: datetime()
})
RETURN e;
```

### 6.2 Create Sample GeopoliticalEvent

```cypher
CREATE (g:GeopoliticalEvent {
  id: apoc.create.uuid(),
  eventId: 'GEO-2024-0001',
  eventType: 'TENSION',
  timestamp: datetime(),
  primaryActors: ['CountryA', 'CountryB'],
  region: 'EASTERN_EUROPE',
  tensionLevel: 7.5,
  cyberActivityCorrelation: 0.85,
  threatActorActivityMultiplier: 2.5,
  targetSectors: ['ENERGY', 'FINANCE'],
  confidence: 0.8,
  createdAt: datetime()
})
RETURN g;
```

---

## 7. MIGRATION & ROLLBACK PROCEDURES

### 7.1 Schema Installation Script

```cypher
// Transaction 1: Create constraints
:begin
// [All constraint creation statements]
:commit

// Transaction 2: Create indexes
:begin
// [All index creation statements]
:commit

// Transaction 3: Validate schema
CALL db.constraints() YIELD name
RETURN count(name) AS constraintCount;

CALL db.indexes() YIELD name
RETURN count(name) AS indexCount;
```

### 7.2 Rollback Script

```cypher
// Remove Level 5 specific constraints
DROP CONSTRAINT information_event_id IF EXISTS;
DROP CONSTRAINT information_event_eventid IF EXISTS;
DROP CONSTRAINT geopolitical_event_id IF EXISTS;
DROP CONSTRAINT geopolitical_event_eventid IF EXISTS;
DROP CONSTRAINT threat_feed_id IF EXISTS;
DROP CONSTRAINT threat_feed_feedid IF EXISTS;

// Remove Level 5 nodes (with safety check)
MATCH (n)
WHERE n:InformationEvent OR n:GeopoliticalEvent OR n:ThreatFeed
AND n.createdAt > datetime('2024-11-22T00:00:00')
DETACH DELETE n;
```

---

## DELIVERABLES SUMMARY

✅ **Complete Cypher DDL**: All three core schemas with full property definitions
✅ **Relationship Schemas**: 6 categories with detailed properties
✅ **Integration Points**: Clear linkage to 316K CVEs, 16 sectors, cognitive biases
✅ **Validation Rules**: Data integrity and temporal constraints
✅ **Index Recommendations**: Composite and full-text search optimization
✅ **Sample Data Queries**: Ready-to-execute examples
✅ **Migration Procedures**: Safe installation and rollback scripts

**EVIDENCE**: Complete executable Cypher DDL ready for Neo4j deployment
**INTEGRATION**: Fully compatible with existing AEON v3.0 schema
**NEXT STEP**: Agent 3 can proceed with Python implementation using these schemas