# AEON Cyber Digital Twin - Maintenance Guide

**Version**: 1.0.0
**Last Updated**: 2024-11-22
**Database**: Neo4j 5.x

[← Back to Main Index](00_MAIN_INDEX.md)

---

## 📝 Table of Contents

1. [Daily Maintenance](#daily-maintenance)
2. [Add New Equipment](#add-new-equipment)
3. [Update Equipment](#update-equipment)
4. [Delete Equipment](#delete-equipment)
5. [Add New Sector](#add-new-sector)
6. [CVE Integration](#cve-integration)
7. [Data Validation](#data-validation)
8. [Backup & Restore](#backup--restore)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting](#troubleshooting)
11. [Level 5: Event Stream Maintenance](#level-5-event-stream-maintenance)
12. [Level 6: Prediction System Maintenance](#level-6-prediction-system-maintenance)
13. [Cognitive Bias Relationship Maintenance](#cognitive-bias-relationship-maintenance)
14. [Pipeline Health Monitoring](#pipeline-health-monitoring)
15. [Advanced Backup & Recovery](#advanced-backup--recovery)

---

## 🔄 Daily Maintenance

### Check Database Health
```cypher
// Database status check
CALL dbms.queryJmx("org.neo4j:instance=kernel#0,name=Store file sizes")
YIELD attributes
RETURN attributes.TotalStoreSize as DatabaseSize;

// Active connections
CALL dbms.listConnections() YIELD connectionId, connectTime, connector, username
RETURN username, count(*) as connections;

// Transaction status
CALL dbms.listTransactions() YIELD transactionId, currentQuery, status, elapsedTime
WHERE status = 'Running'
RETURN transactionId, currentQuery, elapsedTime;
```

### Verify Sector Integrity
```cypher
// Check all sectors have expected nodes
WITH [
  {sector: 'WATER', expected: 27200},
  {sector: 'ENERGY', expected: 35475},
  {sector: 'COMMUNICATIONS', expected: 40759},
  {sector: 'NUCLEAR', expected: 10448}
] as expectations
UNWIND expectations as exp
MATCH (n)
WHERE n.sector = exp.sector
WITH exp.sector as sector,
     exp.expected as expected,
     count(n) as actual
RETURN sector,
       expected,
       actual,
       CASE WHEN abs(expected - actual) < expected * 0.05 THEN 'OK' ELSE 'CHECK' END as status
ORDER BY sector;
```

---

## ➕ Add New Equipment

### Step 1: Verify Facility Exists
```cypher
// Check if facility exists
MATCH (f:Facility)
WHERE f.facilityId = 'TARGET-FACILITY-ID'
RETURN f.facilityId, f.name, f.sector, f.facilityType;
```

### Step 2: Create Equipment with Proper Tags
```cypher
// Add new equipment template
CREATE (e:Equipment {
  // Required fields
  equipmentId: 'EQ-[SECTOR]-[TYPE]-[STATE]-[NUMBER]',
  equipmentType: 'Equipment Type',
  sector: 'SECTOR_NAME',

  // Recommended fields
  manufacturer: 'Vendor Name',
  model: 'Model Number',
  serialNumber: 'SN123456',
  installDate: date('2024-01-01'),

  // Tag system (MANDATORY)
  tags: [
    'SECTOR_[NAME]',                     // Primary sector
    'SECTOR_COMMON_[TYPE]',              // If cross-sector
    'EQUIP_TYPE_[TYPE]',                 // Equipment category
    'FUNCTION_[PRIMARY_FUNCTION]',       // Primary function
    'VENDOR_[NAME]',                     // Manufacturer
    'GEO_STATE_[XX]',                    // Geographic location
    'OPS_CRITICALITY_[LEVEL]',          // CRITICAL|HIGH|MEDIUM|LOW
    'OPS_STATUS_[STATUS]',               // OPERATIONAL|MAINTENANCE
    'TECH_PROTOCOL_[NAME]',             // Technical protocols
    'REG_[STANDARD]',                   // Regulatory compliance
    'SUBSECTOR_[NAME]'                  // Subsector classification
  ],

  // Metadata
  createdAt: datetime(),
  createdBy: 'username',
  updatedAt: datetime()
})

// Link to facility
WITH e
MATCH (f:Facility {facilityId: 'TARGET-FACILITY-ID'})
CREATE (e)-[:LOCATED_AT]->(f)
RETURN e;
```

### Step 3: Verify Creation
```cypher
// Verify equipment was created correctly
MATCH (e:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE e.equipmentId = 'NEW-EQUIPMENT-ID'
RETURN e, f;
```

---

## 🔧 Update Equipment

### Update Equipment Properties
```cypher
// Update single property
MATCH (e:Equipment {equipmentId: 'EQ-XXX'})
SET e.operationalStatus = 'MAINTENANCE',
    e.updatedAt = datetime()
RETURN e;

// Update multiple properties
MATCH (e:Equipment {equipmentId: 'EQ-XXX'})
SET e += {
  maintenanceSchedule: 'QUARTERLY',
  lastInspection: date('2024-11-01'),
  nextInspection: date('2025-02-01'),
  inspector: 'John Doe',
  updatedAt: datetime()
}
RETURN e;
```

### Add/Remove Tags
```cypher
// Add new tags
MATCH (e:Equipment {equipmentId: 'EQ-XXX'})
SET e.tags = e.tags + ['NEW_TAG_1', 'NEW_TAG_2'],
    e.updatedAt = datetime()
RETURN e.tags;

// Remove specific tags
MATCH (e:Equipment {equipmentId: 'EQ-XXX'})
SET e.tags = [tag IN e.tags WHERE NOT tag IN ['TAG_TO_REMOVE']],
    e.updatedAt = datetime()
RETURN e.tags;
```

### Move Equipment to Different Facility
```cypher
// Move equipment to new facility
MATCH (e:Equipment {equipmentId: 'EQ-XXX'})-[r:LOCATED_AT]->()
DELETE r
WITH e
MATCH (newF:Facility {facilityId: 'NEW-FACILITY-ID'})
CREATE (e)-[:LOCATED_AT]->(newF)
SET e.updatedAt = datetime()
RETURN e, newF;
```

---

## ❌ Delete Equipment

### Safe Deletion Process
```cypher
// Step 1: Check relationships
MATCH (e:Equipment {equipmentId: 'EQ-TO-DELETE'})
OPTIONAL MATCH (e)-[r]-()
RETURN e, type(r) as relationship, count(r) as count;

// Step 2: Archive before deletion (optional)
MATCH (e:Equipment {equipmentId: 'EQ-TO-DELETE'})
WITH e, properties(e) as props
CREATE (archive:ArchivedEquipment)
SET archive = props,
    archive.archivedAt = datetime(),
    archive.archivedBy = 'username'
RETURN archive;

// Step 3: Delete equipment and relationships
MATCH (e:Equipment {equipmentId: 'EQ-TO-DELETE'})
DETACH DELETE e;

// Step 4: Verify deletion
MATCH (e:Equipment {equipmentId: 'EQ-TO-DELETE'})
RETURN count(e) as shouldBeZero;
```

---

## 🏗️ Add New Sector

### Step 1: Define Sector Schema
```cypher
// Create sector configuration
CREATE (config:SectorConfig {
  sectorName: 'NEW_SECTOR',
  sectorCode: 'NS',
  description: 'New Critical Infrastructure Sector',
  nodeTypes: ['Equipment', 'Facility', 'Device', 'Property', 'Measurement'],
  subsectors: ['SUBSECTOR_1', 'SUBSECTOR_2'],
  targetNodes: 30000,
  criticalityLevels: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
  createdAt: datetime()
})
RETURN config;
```

### Step 2: Deploy Sector Infrastructure
```cypher
// Create facilities for new sector
UNWIND range(1, 10) as i
CREATE (f:Facility {
  facilityId: 'NS-FAC-' + toString(i),
  name: 'New Sector Facility ' + toString(i),
  facilityType: 'PRIMARY_FACILITY',
  sector: 'NEW_SECTOR',
  state: CASE i % 5
    WHEN 0 THEN 'CA'
    WHEN 1 THEN 'TX'
    WHEN 2 THEN 'NY'
    WHEN 3 THEN 'FL'
    ELSE 'IL'
  END,
  createdAt: datetime()
})

// Create equipment for facilities
WITH f
UNWIND range(1, 50) as j
CREATE (e:Equipment {
  equipmentId: 'EQ-NS-' + f.facilityId + '-' + toString(j),
  equipmentType: 'Generic Equipment',
  sector: 'NEW_SECTOR',
  tags: [
    'SECTOR_NEW_SECTOR',
    'EQUIP_TYPE_GENERIC',
    'OPS_STATUS_OPERATIONAL'
  ],
  createdAt: datetime()
})-[:LOCATED_AT]->(f);
```

### Step 3: Validate New Sector
```cypher
// Verify sector deployment
MATCH (n)
WHERE n.sector = 'NEW_SECTOR'
WITH count(n) as totalNodes
MATCH (f:Facility)
WHERE f.sector = 'NEW_SECTOR'
WITH totalNodes, count(f) as facilities
MATCH (e:Equipment)
WHERE e.sector = 'NEW_SECTOR'
RETURN 'NEW_SECTOR' as sector,
       totalNodes,
       facilities,
       count(e) as equipment;
```

---

## 🛡️ CVE Integration

### Link CVE to Equipment
```cypher
// Create CVE if doesn't exist
MERGE (cve:CVE {id: 'CVE-2024-12345'})
ON CREATE SET
  cve.description = 'Vulnerability description',
  cve.baseScore = 8.5,
  cve.severity = 'HIGH',
  cve.publishedDate = date('2024-11-01'),
  cve.createdAt = datetime()

// Link to affected equipment
WITH cve
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND e.equipmentType = 'SCADA System'
CREATE (cve)-[:AFFECTS]->(e)
RETURN cve.id, count(e) as affectedEquipment;
```

### Patch Management
```cypher
// Mark equipment as patched
MATCH (cve:CVE {id: 'CVE-2024-12345'})-[:AFFECTS]->(e:Equipment)
WHERE e.equipmentId IN ['EQ-1', 'EQ-2', 'EQ-3']
CREATE (e)-[:PATCHED_FOR {
  patchDate: date('2024-11-15'),
  patchVersion: '1.2.3',
  appliedBy: 'username'
}]->(cve)
SET e.lastPatched = date('2024-11-15')
RETURN e.equipmentId, e.lastPatched;
```

---

## ✅ Data Validation

### Check Data Integrity
```cypher
// Find orphan equipment (no facility)
MATCH (e:Equipment)
WHERE NOT exists((e)-[:LOCATED_AT]->(:Facility))
RETURN e.sector, count(e) as orphanEquipment;

// Find equipment without required fields
MATCH (e:Equipment)
WHERE e.equipmentId IS NULL
   OR e.sector IS NULL
   OR e.equipmentType IS NULL
   OR e.tags IS NULL
   OR size(e.tags) = 0
RETURN e.equipmentId, e.sector,
       CASE
         WHEN e.equipmentId IS NULL THEN 'Missing ID'
         WHEN e.sector IS NULL THEN 'Missing Sector'
         WHEN e.equipmentType IS NULL THEN 'Missing Type'
         WHEN e.tags IS NULL OR size(e.tags) = 0 THEN 'Missing Tags'
       END as issue;

// Check tag consistency
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND NOT ('SECTOR_WATER' IN e.tags)
RETURN e.equipmentId, e.sector, e.tags
LIMIT 50;
```

### Fix Common Issues
```cypher
// Fix missing sector tags
MATCH (e:Equipment)
WHERE e.sector IS NOT NULL
  AND NOT ('SECTOR_' + e.sector IN e.tags)
SET e.tags = e.tags + ['SECTOR_' + e.sector],
    e.updatedAt = datetime()
RETURN count(e) as fixed;

// Clean duplicate tags
MATCH (e:Equipment)
WHERE size(e.tags) <> size(apoc.coll.toSet(e.tags))
SET e.tags = apoc.coll.toSet(e.tags),
    e.updatedAt = datetime()
RETURN count(e) as cleaned;
```

---

## 💾 Backup & Restore

### Create Backup
```bash
# Stop database
neo4j stop

# Create backup
neo4j-admin database dump neo4j --to-path=/backup/aeon-$(date +%Y%m%d).dump

# Start database
neo4j start
```

### Restore from Backup
```bash
# Stop database
neo4j stop

# Restore backup
neo4j-admin database load neo4j --from-path=/backup/aeon-20241122.dump --overwrite-destination=true

# Start database
neo4j start
```

### Export Sector Data
```cypher
// Export sector to CSV
CALL apoc.export.csv.query(
  "MATCH (e:Equipment) WHERE e.sector = 'WATER' RETURN e",
  "/exports/water_sector_backup.csv",
  {}
);
```

---

## ⚡ Performance Optimization

### Create Indexes
```cypher
// Essential indexes for performance
CREATE INDEX sector_index IF NOT EXISTS FOR (n:Equipment) ON (n.sector);
CREATE INDEX equipment_id_index IF NOT EXISTS FOR (e:Equipment) ON (e.equipmentId);
CREATE INDEX facility_id_index IF NOT EXISTS FOR (f:Facility) ON (f.facilityId);
CREATE INDEX cve_id_index IF NOT EXISTS FOR (c:CVE) ON (c.id);
CREATE INDEX cve_score_index IF NOT EXISTS FOR (c:CVE) ON (c.baseScore);
```

### Analyze Query Performance
```cypher
// Profile slow queries
PROFILE
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND 'OPS_CRITICALITY_CRITICAL' IN e.tags
RETURN count(e);

// Get query plan
EXPLAIN
MATCH (cve:CVE)-[:AFFECTS]->(e:Equipment)
WHERE e.sector = 'ENERGY'
RETURN count(cve);
```

### Database Statistics
```cypher
// Update statistics
CALL db.stats.clear();
CALL db.stats.collect();

// Check memory usage
CALL dbms.queryJmx("org.neo4j:instance=kernel#0,name=Transactions")
YIELD attributes
RETURN attributes;
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: Slow Queries
```cypher
// Check for missing indexes
SHOW INDEXES;

// Add composite index for common queries
CREATE INDEX composite_sector_critical IF NOT EXISTS
FOR (e:Equipment) ON (e.sector, e.tags);
```

#### Issue: Duplicate Nodes
```cypher
// Find duplicates
MATCH (e1:Equipment), (e2:Equipment)
WHERE e1.equipmentId = e2.equipmentId
  AND id(e1) < id(e2)
RETURN e1.equipmentId, count(*) as duplicates;

// Merge duplicates
MATCH (e1:Equipment), (e2:Equipment)
WHERE e1.equipmentId = e2.equipmentId
  AND id(e1) < id(e2)
DETACH DELETE e2;
```

#### Issue: Memory Problems
```cypher
// Clear query cache
CALL db.clearQueryCaches();

// Check transaction logs
CALL dbms.listTransactions()
YIELD transactionId, elapsedTime, currentQuery
WHERE elapsedTime > duration('PT1M')
RETURN transactionId, elapsedTime;

// Kill long-running transaction
CALL dbms.killTransaction('transaction-id');
```

---

## 📋 Maintenance Schedule

### Daily Tasks
- Check database health
- Verify critical equipment status
- Review error logs
- Update CVE database

### Weekly Tasks
- Run data validation checks
- Clean duplicate entries
- Update equipment status
- Generate sector reports

### Monthly Tasks
- Full database backup
- Performance analysis
- Index optimization
- Schema validation

### Quarterly Tasks
- Capacity planning
- Security audit
- Compliance verification
- Documentation update

---

## 📡 Level 5: Event Stream Maintenance

### Overview
Level 5 implements real-time threat intelligence ingestion, geopolitical event correlation, and cognitive bias activation through event streams. This section provides detailed procedures for maintaining event pipelines, adding new event types, and monitoring stream health.

### 1. Add New Information Event

#### Step 1: Define Event Schema
```cypher
// Create InformationEvent with complete schema
CREATE (event:InformationEvent {
  // Core identifiers
  eventId: 'INFO-' + toString(timestamp()),
  eventType: 'THREAT_INTELLIGENCE',  // THREAT_INTELLIGENCE | INCIDENT_REPORT | VULNERABILITY_DISCLOSURE

  // Source metadata
  source: 'CISA Alert',
  sourceUrl: 'https://www.cisa.gov/alert/...',
  sourceCredibility: 0.95,  // 0.0-1.0 scale

  // Temporal data
  publishedDate: datetime('2024-11-23T10:30:00Z'),
  collectedDate: datetime(),
  eventDate: datetime('2024-11-23T08:00:00Z'),

  // Content
  title: 'Critical Infrastructure SCADA Vulnerability',
  description: 'Multiple SCADA systems vulnerable to remote code execution...',
  rawText: 'Full event text content...',

  // Classification
  severity: 'CRITICAL',  // CRITICAL | HIGH | MEDIUM | LOW
  impactScore: 9.2,
  confidenceScore: 0.88,

  // Affected sectors (array)
  affectedSectors: ['WATER', 'ENERGY', 'NUCLEAR'],

  // Keywords for correlation
  keywords: ['SCADA', 'RCE', 'water', 'energy', 'industrial control'],

  // Geopolitical context
  region: 'NORTH_AMERICA',
  countries: ['USA'],

  // Processing metadata
  processed: false,
  correlatedAt: null,

  // Timestamps
  createdAt: datetime(),
  updatedAt: datetime()
})
RETURN event;
```

#### Step 2: Correlate Event with Infrastructure
```cypher
// Correlate event with affected equipment based on sectors and keywords
MATCH (event:InformationEvent {eventId: 'INFO-1234567890'})
WHERE event.processed = false
WITH event

// Find affected equipment by sector
MATCH (e:Equipment)
WHERE e.sector IN event.affectedSectors
  AND any(keyword IN event.keywords WHERE
    toLower(e.equipmentType) CONTAINS toLower(keyword) OR
    any(tag IN e.tags WHERE toLower(tag) CONTAINS toLower(keyword))
  )

// Create CORRELATES_TO relationship with relevance score
WITH event, e,
  size([keyword IN event.keywords WHERE
    toLower(e.equipmentType) CONTAINS toLower(keyword)
  ]) as matches
CREATE (event)-[:CORRELATES_TO {
  correlationScore: toFloat(matches) / size(event.keywords),
  correlatedAt: datetime(),
  correlationMethod: 'KEYWORD_SECTOR_MATCH',
  autoGenerated: true
}]->(e)

// Mark event as processed
WITH event, count(e) as correlatedCount
SET event.processed = true,
    event.correlatedAt = datetime(),
    event.correlatedCount = correlatedCount,
    event.updatedAt = datetime()

RETURN event.eventId, correlatedCount;
```

#### Step 3: Activate Cognitive Biases
```cypher
// Activate cognitive biases based on event characteristics
MATCH (event:InformationEvent {eventId: 'INFO-1234567890'})
WHERE event.severity IN ['CRITICAL', 'HIGH']

WITH event

// Find relevant cognitive biases
MATCH (bias:CognitiveBias)
WHERE (
  // Availability bias for high-severity events
  (event.severity = 'CRITICAL' AND bias.biasType = 'AVAILABILITY') OR

  // Recency bias for recent events
  (duration.between(event.publishedDate, datetime()).days < 7
   AND bias.biasType = 'RECENCY') OR

  // Confirmation bias for specific threat patterns
  (any(keyword IN event.keywords WHERE keyword IN ['APT', 'nation-state'])
   AND bias.biasType = 'CONFIRMATION')
)

// Create activation relationship
CREATE (event)-[:ACTIVATES {
  activationStrength: CASE event.severity
    WHEN 'CRITICAL' THEN 0.9
    WHEN 'HIGH' THEN 0.75
    WHEN 'MEDIUM' THEN 0.5
    ELSE 0.25
  END,
  activatedAt: datetime(),
  reason: 'Event severity: ' + event.severity,
  duration: duration('P7D'),  // Active for 7 days
  expiresAt: datetime() + duration('P7D')
}]->(bias)

RETURN event.eventId, bias.biasType, bias.name;
```

#### Complete Event Ingestion Script
```cypher
// Complete script: Create event → Correlate → Activate biases
// Run as single transaction

// 1. Create event
CREATE (event:InformationEvent {
  eventId: 'INFO-' + toString(timestamp()),
  eventType: 'THREAT_INTELLIGENCE',
  source: 'CISA Alert AA24-123',
  sourceUrl: 'https://www.cisa.gov/alert/aa24-123',
  sourceCredibility: 0.95,
  publishedDate: datetime(),
  collectedDate: datetime(),
  eventDate: datetime(),
  title: 'Critical SCADA Vulnerability CVE-2024-99999',
  description: 'Remote code execution in water/energy SCADA systems',
  rawText: 'Full alert text...',
  severity: 'CRITICAL',
  impactScore: 9.2,
  confidenceScore: 0.88,
  affectedSectors: ['WATER', 'ENERGY'],
  keywords: ['SCADA', 'RCE', 'industrial control'],
  region: 'NORTH_AMERICA',
  countries: ['USA'],
  processed: false,
  createdAt: datetime()
})

// 2. Correlate with equipment
WITH event
MATCH (e:Equipment)
WHERE e.sector IN event.affectedSectors
  AND any(keyword IN event.keywords WHERE
    toLower(e.equipmentType) CONTAINS toLower(keyword))
CREATE (event)-[:CORRELATES_TO {
  correlationScore: 0.8,
  correlatedAt: datetime(),
  correlationMethod: 'AUTO'
}]->(e)

// 3. Activate biases
WITH event, count(e) as equipCount
MATCH (bias:CognitiveBias)
WHERE bias.biasType IN ['AVAILABILITY', 'RECENCY']
CREATE (event)-[:ACTIVATES {
  activationStrength: 0.9,
  activatedAt: datetime(),
  expiresAt: datetime() + duration('P7D')
}]->(bias)

// 4. Mark processed
SET event.processed = true,
    event.correlatedAt = datetime(),
    event.correlatedCount = equipCount

RETURN event.eventId, equipCount as equipmentCorrelated,
       count(bias) as biasesActivated;
```

### 2. Add Geopolitical Event

#### Step 1: Create Geopolitical Event with APT Correlation
```cypher
// Create GeopoliticalEvent with threat actor linkage
CREATE (geoEvent:GeopoliticalEvent {
  // Core identifiers
  eventId: 'GEO-' + toString(timestamp()),
  eventType: 'CYBER_ATTACK',  // CYBER_ATTACK | SANCTIONS | CONFLICT | DIPLOMATIC

  // Geopolitical context
  region: 'EASTERN_EUROPE',
  primaryCountry: 'Ukraine',
  affectedCountries: ['Ukraine', 'Poland', 'Germany'],

  // Temporal
  eventDate: datetime('2024-11-20T14:00:00Z'),
  publishedDate: datetime('2024-11-21T09:00:00Z'),
  collectedDate: datetime(),

  // Content
  title: 'Critical Infrastructure Cyber Attack',
  description: 'Nation-state actor targeting energy sector...',

  // Attribution
  attributedActors: ['APT28', 'SANDWORM'],
  attributionConfidence: 0.85,

  // Impact assessment
  severity: 'HIGH',
  impactScore: 8.5,
  escalationRisk: 0.72,

  // Sector implications
  targetSectors: ['ENERGY', 'COMMUNICATIONS'],

  // Intelligence sources
  sources: ['NATO CCDCOE', 'CISA', 'ENISA'],

  // Analysis
  geopoliticalTension: 0.88,
  cyberWarfareIndicator: 0.92,

  // Processing
  processed: false,

  createdAt: datetime(),
  updatedAt: datetime()
})
RETURN geoEvent;
```

#### Step 2: Link to Threat Actors (APT Groups)
```cypher
// Link GeopoliticalEvent to known APT groups
MATCH (geoEvent:GeopoliticalEvent {eventId: 'GEO-1234567890'})
WHERE NOT geoEvent.processed

WITH geoEvent

// Find or create APT groups
UNWIND geoEvent.attributedActors as aptName
MERGE (apt:ThreatActor {name: aptName})
ON CREATE SET
  apt.actorId = 'APT-' + toString(timestamp()),
  apt.actorType = 'NATION_STATE',
  apt.firstSeen: datetime(),
  apt.createdAt = datetime()
ON MATCH SET
  apt.lastSeen = datetime(),
  apt.updatedAt = datetime()

// Create attribution relationship
CREATE (geoEvent)-[:ATTRIBUTED_TO {
  confidence: geoEvent.attributionConfidence,
  attributedAt: datetime(),
  sources: geoEvent.sources,
  evidenceStrength: CASE geoEvent.attributionConfidence
    WHEN > 0.8 THEN 'HIGH'
    WHEN > 0.6 THEN 'MEDIUM'
    ELSE 'LOW'
  END
}]->(apt)

RETURN geoEvent.eventId, apt.name, geoEvent.attributionConfidence;
```

#### Step 3: Correlate with US Infrastructure
```cypher
// Correlate geopolitical event with domestic infrastructure
// Focus on similar attack patterns and vulnerable sectors

MATCH (geoEvent:GeopoliticalEvent {eventId: 'GEO-1234567890'})
WHERE NOT geoEvent.processed

// Find US equipment in target sectors
MATCH (e:Equipment)
WHERE e.sector IN geoEvent.targetSectors
  AND (e.country = 'USA' OR 'GEO_STATE_' + e.state IN [tag IN e.tags WHERE tag STARTS WITH 'GEO_STATE_'])

// Calculate risk score based on multiple factors
WITH geoEvent, e,
  // Sector match weight
  CASE WHEN e.sector IN geoEvent.targetSectors THEN 0.4 ELSE 0.0 END +
  // Equipment criticality weight
  CASE WHEN 'OPS_CRITICALITY_CRITICAL' IN e.tags THEN 0.3 ELSE 0.0 END +
  // Technology similarity weight (if equipment uses similar tech)
  CASE WHEN any(keyword IN ['SCADA', 'ICS', 'control system'] WHERE
    toLower(e.equipmentType) CONTAINS toLower(keyword)) THEN 0.3 ELSE 0.0 END
  as riskScore

WHERE riskScore > 0.5  // Only create relationships for significant risk

CREATE (geoEvent)-[:IMPLIES_RISK {
  riskScore: riskScore,
  threatLevel: CASE
    WHEN riskScore > 0.8 THEN 'CRITICAL'
    WHEN riskScore > 0.6 THEN 'HIGH'
    ELSE 'MEDIUM'
  END,
  correlation: 'GEOPOLITICAL_THREAT_PATTERN',
  assessedAt: datetime(),
  validUntil: datetime() + duration('P30D')  // Valid for 30 days
}]->(e)

// Mark as processed
WITH geoEvent, count(e) as affectedEquipment
SET geoEvent.processed = true,
    geoEvent.processedAt = datetime(),
    geoEvent.domesticImpactCount = affectedEquipment

RETURN geoEvent.eventId, affectedEquipment;
```

### 3. Update Threat Feed Configurations

#### Configure RSS/ATOM Feed Sources
```cypher
// Create ThreatFeed source configuration
CREATE (feed:ThreatFeed {
  feedId: 'FEED-CISA-' + toString(timestamp()),
  feedName: 'CISA Alerts',
  feedType: 'RSS',
  feedUrl: 'https://www.cisa.gov/cybersecurity-advisories/all.xml',

  // Collection schedule
  updateFrequency: duration('PT1H'),  // Every 1 hour
  lastCollected: null,
  nextCollection: datetime() + duration('PT1H'),

  // Processing configuration
  autoProcess: true,
  minSeverity: 'MEDIUM',
  targetEventType: 'THREAT_INTELLIGENCE',

  // Quality settings
  credibilityScore: 0.95,
  requireManualReview: false,

  // Sector filters
  sectors: ['WATER', 'ENERGY', 'NUCLEAR', 'COMMUNICATIONS'],

  // Status
  active: true,
  errorCount: 0,
  lastError: null,

  createdAt: datetime(),
  updatedAt: datetime()
})
RETURN feed;
```

#### Create Feed Collection Job
```cypher
// Create scheduled collection job
MATCH (feed:ThreatFeed {feedId: 'FEED-CISA-123'})
WHERE feed.active = true
  AND feed.nextCollection <= datetime()

CREATE (job:FeedCollectionJob {
  jobId: 'JOB-' + toString(timestamp()),
  feedId: feed.feedId,
  feedUrl: feed.feedUrl,

  // Job parameters
  scheduledAt: feed.nextCollection,
  startedAt: datetime(),
  status: 'RUNNING',

  // Processing config
  batchSize: 100,
  timeout: duration('PT10M'),

  createdAt: datetime()
})

// Update feed last collection
SET feed.lastCollected = datetime(),
    feed.nextCollection = datetime() + feed.updateFrequency

RETURN job, feed;
```

### 4. Monitor Event Processor Performance

#### Check Event Processing Latency
```cypher
// Monitor event processing performance (must be < 5 minutes)
MATCH (event:InformationEvent)
WHERE event.collectedDate > datetime() - duration('P1D')
WITH event,
  duration.between(event.collectedDate, event.correlatedAt) as processingTime,
  duration('PT5M') as threshold

RETURN
  date(event.collectedDate) as date,
  count(event) as totalEvents,
  sum(CASE WHEN processingTime < threshold THEN 1 ELSE 0 END) as withinSLA,
  sum(CASE WHEN processingTime >= threshold THEN 1 ELSE 0 END) as breachedSLA,
  avg(processingTime.seconds) as avgProcessingSeconds,
  max(processingTime.seconds) as maxProcessingSeconds,
  toFloat(sum(CASE WHEN processingTime < threshold THEN 1 ELSE 0 END)) / count(event) as slaCompliance
ORDER BY date DESC;
```

#### Monitor Correlation Quality
```cypher
// Check correlation accuracy (must be ≥ 0.75)
MATCH (event:InformationEvent)-[r:CORRELATES_TO]->(e:Equipment)
WHERE event.correlatedAt > datetime() - duration('P7D')

WITH event,
  avg(r.correlationScore) as avgScore,
  count(r) as correlationCount,
  collect(DISTINCT e.sector) as affectedSectors

RETURN
  event.eventId,
  event.severity,
  avgScore,
  correlationCount,
  affectedSectors,
  CASE WHEN avgScore >= 0.75 THEN 'PASS' ELSE 'REVIEW' END as qualityStatus
ORDER BY avgScore ASC;
```

#### Check Unprocessed Events
```cypher
// Find events stuck in processing
MATCH (event:InformationEvent)
WHERE event.processed = false
  AND event.collectedDate < datetime() - duration('PT15M')

RETURN
  event.eventId,
  event.eventType,
  event.severity,
  event.collectedDate,
  duration.between(event.collectedDate, datetime()) as stuckDuration,
  event.source
ORDER BY event.collectedDate ASC
LIMIT 50;
```

### 5. Update Cognitive Bias Activation Thresholds

#### Review and Adjust Activation Rules
```cypher
// Update bias activation thresholds based on historical performance
MATCH (event:InformationEvent)-[r:ACTIVATES]->(bias:CognitiveBias)
WHERE event.correlatedAt > datetime() - duration('P30D')

WITH bias,
  count(r) as activationCount,
  avg(r.activationStrength) as avgStrength,
  collect(event.severity) as severities

// Calculate optimal threshold
WITH bias, activationCount, avgStrength,
  size([s IN severities WHERE s IN ['CRITICAL', 'HIGH']]) as highSevCount,
  toFloat(size([s IN severities WHERE s IN ['CRITICAL', 'HIGH']])) / size(severities) as highSevRate

// Update bias configuration
SET bias.activationThreshold = CASE
  WHEN highSevRate > 0.7 THEN 0.8  // Raise threshold if too many activations
  WHEN highSevRate < 0.3 THEN 0.6  // Lower threshold if too few activations
  ELSE 0.7  // Default
END,
bias.lastCalibrated = datetime(),
bias.historicalActivations = activationCount

RETURN
  bias.biasType,
  bias.name,
  activationCount,
  avgStrength,
  highSevRate,
  bias.activationThreshold as newThreshold;
```

### 6. Complete Event Maintenance Scripts

#### Daily Event Stream Health Check
```cypher
// Daily comprehensive event stream health check
// Run every morning at 8:00 AM

// 1. Check feed collection status
MATCH (feed:ThreatFeed)
WHERE feed.active = true

WITH feed,
  duration.between(feed.lastCollected, datetime()) as timeSinceCollection

WITH
  count(feed) as totalFeeds,
  sum(CASE WHEN timeSinceCollection > feed.updateFrequency * 2 THEN 1 ELSE 0 END) as staleFeeds,
  sum(feed.errorCount) as totalErrors

// 2. Check event processing
MATCH (event:InformationEvent)
WHERE event.collectedDate > datetime() - duration('P1D')

WITH totalFeeds, staleFeeds, totalErrors,
  count(event) as eventsLast24h,
  sum(CASE WHEN event.processed = false THEN 1 ELSE 0 END) as unprocessed,
  avg(duration.between(event.collectedDate, event.correlatedAt).seconds) as avgProcessing

// 3. Check correlation quality
MATCH (event:InformationEvent)-[r:CORRELATES_TO]->()
WHERE event.correlatedAt > datetime() - duration('P1D')

WITH totalFeeds, staleFeeds, totalErrors, eventsLast24h, unprocessed, avgProcessing,
  avg(r.correlationScore) as avgCorrelationScore

// 4. Check bias activations
MATCH ()-[a:ACTIVATES]->(bias:CognitiveBias)
WHERE a.activatedAt > datetime() - duration('P1D')
  AND a.expiresAt > datetime()

RETURN
  // Feed health
  totalFeeds,
  staleFeeds,
  totalErrors,
  CASE WHEN staleFeeds = 0 AND totalErrors < 5 THEN '✓ HEALTHY' ELSE '⚠ CHECK REQUIRED' END as feedStatus,

  // Event processing
  eventsLast24h,
  unprocessed,
  round(avgProcessing, 2) as avgProcessingSeconds,
  CASE WHEN avgProcessing < 300 AND unprocessed < 10 THEN '✓ HEALTHY' ELSE '⚠ CHECK REQUIRED' END as processingStatus,

  // Correlation quality
  round(avgCorrelationScore, 3) as avgCorrelationScore,
  CASE WHEN avgCorrelationScore >= 0.75 THEN '✓ HEALTHY' ELSE '⚠ CHECK REQUIRED' END as correlationStatus,

  // Bias activations
  count(DISTINCT bias) as activeBiases,
  CASE WHEN count(DISTINCT bias) > 0 THEN '✓ ACTIVE' ELSE '⚠ NO ACTIVATIONS' END as biasStatus;
```

---

## 🔮 Level 6: Prediction System Maintenance

### Overview
Level 6 implements time-series forecasting using NHITS models, historical pattern analysis, and what-if scenario planning. This section provides detailed procedures for maintaining prediction models, updating historical patterns, and managing future threat scenarios.

### 1. Add Historical Pattern from New Incident

#### Step 1: Extract Pattern from Incident
```cypher
// Create HistoricalPattern from actual security incident
CREATE (pattern:HistoricalPattern {
  // Identifiers
  patternId: 'PATTERN-' + toString(timestamp()),
  patternName: 'Colonial Pipeline Ransomware Attack Pattern',
  patternType: 'RANSOMWARE_ATTACK',  // RANSOMWARE_ATTACK | APT_CAMPAIGN | SUPPLY_CHAIN | DDoS

  // Incident reference
  incidentId: 'INC-2021-05-07-COLONIAL',
  incidentDate: datetime('2021-05-07T00:00:00Z'),

  // Attack characteristics
  attackVector: 'VPN_COMPROMISE',
  attackPhase: ['INITIAL_ACCESS', 'LATERAL_MOVEMENT', 'ENCRYPTION', 'EXTORTION'],
  ttps: ['T1133', 'T1486', 'T1490'],  // MITRE ATT&CK techniques

  // Target profile
  targetSector: 'ENERGY',
  targetSubsector: 'PIPELINE',
  targetAssetType: ['SCADA', 'OT_NETWORK', 'BILLING_SYSTEM'],

  // Impact data
  impactScore: 9.5,
  downtime: duration('P6D'),  // 6 days
  financialImpact: 4400000,  // USD
  affectedPopulation: 45000000,

  // Attack timeline (hours from initial breach)
  dwellTime: duration('PT72H'),  // 3 days before detection
  detectionTime: duration('PT2H'),  // 2 hours to detect after activation
  containmentTime: duration('PT24H'),  // 24 hours to contain
  recoveryTime: duration('P6D'),  // 6 days to full recovery

  // Threat actor
  threatActor: 'DARKSIDE',
  actorType: 'CYBERCRIMINAL',
  actorMotivation: 'FINANCIAL',

  // Defensive gaps exploited
  vulnerabilities: ['WEAK_VPN_MFA', 'SEGMENTATION_FAILURE', 'BACKUP_INADEQUATE'],
  missingControls: ['MFA_ON_VPN', 'OT_IT_SEGMENTATION', 'OFFLINE_BACKUPS'],

  // Environmental factors
  geopoliticalContext: 'POST_SOLARWINDS_ERA',
  regulatoryPressure: 'MEDIUM',
  publicAttention: 'EXTREME',

  // Pattern metadata
  confidenceScore: 0.92,
  validatedBy: ['CISA', 'FBI', 'Company IR Report'],
  lessonLearned: 'Critical infrastructure OT/IT segmentation essential',

  // Analysis tags
  tags: ['CRITICAL_INFRASTRUCTURE', 'RANSOMWARE', 'NATION_STATE_LEVEL', 'SUPPLY_CHAIN_IMPACT'],

  createdAt: datetime(),
  updatedAt: datetime()
})
RETURN pattern;
```

#### Step 2: Link Pattern to Similar Current Equipment
```cypher
// Find equipment matching historical pattern characteristics
MATCH (pattern:HistoricalPattern {patternId: 'PATTERN-1234567890'})

// Find current equipment with similar profile
MATCH (e:Equipment)
WHERE e.sector = pattern.targetSector
  AND (
    // Equipment type matches target asset types
    any(assetType IN pattern.targetAssetType WHERE
      toLower(e.equipmentType) CONTAINS toLower(assetType)) OR
    // Tags indicate similar functionality
    any(tag IN e.tags WHERE tag IN pattern.tags)
  )

// Calculate similarity score
WITH pattern, e,
  // Sector match
  CASE WHEN e.sector = pattern.targetSector THEN 0.3 ELSE 0.0 END +
  // Asset type similarity
  toFloat(size([assetType IN pattern.targetAssetType WHERE
    toLower(e.equipmentType) CONTAINS toLower(assetType)])) / size(pattern.targetAssetType) * 0.4 +
  // Tag overlap
  toFloat(size([tag IN e.tags WHERE tag IN pattern.tags])) / size(pattern.tags) * 0.3
  as similarityScore

WHERE similarityScore > 0.5

// Create relationship with risk assessment
CREATE (pattern)-[:SIMILAR_TO {
  similarityScore: round(similarityScore, 3),
  riskLevel: CASE
    WHEN similarityScore > 0.8 THEN 'CRITICAL'
    WHEN similarityScore > 0.6 THEN 'HIGH'
    ELSE 'MEDIUM'
  END,
  recommendedControls: pattern.missingControls,
  assessedAt: datetime(),
  validUntil: datetime() + duration('P90D')  // Reassess quarterly
}]->(e)

RETURN pattern.patternName, count(e) as similarEquipment, avg(similarityScore) as avgSimilarity;
```

#### Step 3: Create Prediction from Pattern
```cypher
// Generate FutureThreat prediction from historical pattern
MATCH (pattern:HistoricalPattern {patternId: 'PATTERN-1234567890'})

CREATE (prediction:FutureThreat {
  // Identifiers
  predictionId: 'PRED-' + toString(timestamp()),
  threatName: 'Projected ' + pattern.patternName + ' Repeat',

  // Prediction basis
  basedOnPattern: pattern.patternId,
  predictionMethod: 'HISTORICAL_PATTERN_PROJECTION',

  // Temporal
  predictionDate: datetime(),
  forecastHorizon: duration('P12M'),  // Predicting 12 months out
  predictionWindow: {
    earliest: datetime() + duration('P3M'),
    mostLikely: datetime() + duration('P6M'),
    latest: datetime() + duration('P12M')
  },

  // Threat characteristics (inherited from pattern)
  threatType: pattern.patternType,
  attackVectors: pattern.attackVector,
  targetSectors: [pattern.targetSector],

  // Likelihood assessment
  probability: CASE pattern.confidenceScore
    WHEN > 0.9 THEN 0.75
    WHEN > 0.8 THEN 0.65
    WHEN > 0.7 THEN 0.55
    ELSE 0.45
  END,

  // Impact projection (scaled from historical)
  projectedImpact: pattern.impactScore,
  projectedDowntime: pattern.downtime,
  projectedFinancialLoss: pattern.financialImpact * 1.2,  // 20% increase adjustment

  // Confidence metrics
  confidenceLevel: pattern.confidenceScore * 0.85,  // Slightly lower for prediction
  uncertaintyFactors: ['THREAT_ACTOR_EVOLUTION', 'DEFENSIVE_IMPROVEMENTS', 'GEOPOLITICAL_CHANGES'],

  // Recommendations
  mitigationPriority: pattern.missingControls,
  earlyWarningIndicators: ['RECONNAISSANCE_ACTIVITY', 'VPN_BRUTEFORCE', 'DARKWEB_CHATTER'],

  createdAt: datetime(),
  updatedAt: datetime(),
  validUntil: datetime() + duration('P12M')
})

// Link prediction to pattern
CREATE (prediction)-[:DERIVED_FROM {
  confidence: pattern.confidenceScore,
  derivedAt: datetime()
}]->(pattern)

RETURN prediction, pattern;
```

### 2. Update Future Threat Predictions (Weekly)

#### Weekly Prediction Refresh Script
```cypher
// Weekly prediction update script
// Run every Monday at 6:00 AM

// 1. Update existing predictions with new data
MATCH (pred:FutureThreat)
WHERE pred.validUntil > datetime()
  AND pred.updatedAt < datetime() - duration('P7D')

// Recalculate probability based on recent events
WITH pred
OPTIONAL MATCH (pred)-[:DERIVED_FROM]->(pattern:HistoricalPattern)
OPTIONAL MATCH (event:InformationEvent)
WHERE event.publishedDate > datetime() - duration('P7D')
  AND event.eventType = pattern.patternType

WITH pred, pattern, count(event) as recentSimilarEvents

// Adjust probability based on recent activity
SET pred.probability = CASE
  WHEN recentSimilarEvents > 5 THEN least(pred.probability * 1.15, 0.95)
  WHEN recentSimilarEvents > 2 THEN least(pred.probability * 1.05, 0.90)
  WHEN recentSimilarEvents = 0 THEN pred.probability * 0.95
  ELSE pred.probability
END,
pred.recentActivityCount = recentSimilarEvents,
pred.updatedAt = datetime(),
pred.lastReviewDate = datetime()

// 2. Archive expired predictions
WITH count(pred) as updatedCount
MATCH (expired:FutureThreat)
WHERE expired.validUntil <= datetime()

SET expired:ArchivedPrediction,
    expired.archivedAt = datetime(),
    expired.archivedReason = 'EXPIRED'
REMOVE expired:FutureThreat

// 3. Generate new predictions from recent patterns
WITH updatedCount, count(expired) as archivedCount
MATCH (pattern:HistoricalPattern)
WHERE pattern.createdAt > datetime() - duration('P7D')
  AND NOT exists((:FutureThreat)-[:DERIVED_FROM]->(pattern))

CREATE (newPred:FutureThreat {
  predictionId: 'PRED-' + toString(timestamp()),
  threatName: 'Emerging: ' + pattern.patternName,
  basedOnPattern: pattern.patternId,
  predictionMethod: 'AUTO_GENERATED_FROM_PATTERN',
  predictionDate: datetime(),
  forecastHorizon: duration('P6M'),
  probability: pattern.confidenceScore * 0.7,
  projectedImpact: pattern.impactScore,
  targetSectors: [pattern.targetSector],
  confidenceLevel: pattern.confidenceScore * 0.75,
  createdAt: datetime(),
  validUntil: datetime() + duration('P6M')
})
CREATE (newPred)-[:DERIVED_FROM]->(pattern)

WITH updatedCount, archivedCount, count(newPred) as newPredictions

RETURN
  updatedCount as predictionsUpdated,
  archivedCount as predictionsArchived,
  newPredictions as newPredictionsCreated,
  datetime() as completedAt;
```

### 3. Create What-If Scenario (Quarterly)

#### Step 1: Define Scenario Parameters
```cypher
// Create comprehensive what-if scenario
CREATE (scenario:WhatIfScenario {
  // Identifiers
  scenarioId: 'SCENARIO-' + toString(timestamp()),
  scenarioName: 'Multi-Sector Coordinated APT Campaign',
  scenarioType: 'WORST_CASE_ANALYSIS',  // WORST_CASE | LIKELY_CASE | BEST_CASE

  // Scenario description
  description: 'Nation-state APT conducts coordinated attack on water and energy sectors during winter peak demand',

  // Threat parameters
  threatActor: 'NATION_STATE_APT',
  attackComplexity: 'HIGH',
  attackCoordination: 'MULTI_SECTOR_SIMULTANEOUS',

  // Initial conditions
  assumptions: [
    'APT has 6-month dwell time in networks',
    'Zero-day exploits in SCADA systems',
    'Attacks triggered during winter storm',
    'Coordinated across 5 states',
    'Backup systems also compromised'
  ],

  // Scope
  targetSectors: ['WATER', 'ENERGY'],
  geographicScope: ['CA', 'OR', 'WA', 'NV', 'AZ'],
  populationAffected: 35000000,

  // Timeline
  attackDuration: duration('P14D'),
  detectionDelay: duration('PT48H'),
  responseTime: duration('PT6H'),
  recoveryTime: duration('P21D'),

  // Impact parameters
  infrastructureImpactPercent: 0.35,  // 35% of infrastructure affected
  projectedDowntime: duration('P7D'),
  estimatedFinancialLoss: 50000000000,  // $50 billion
  cascadingFailures: true,

  // Severity assessments
  overallSeverity: 'CATASTROPHIC',
  humanImpact: 'CRITICAL',
  economicImpact: 'SEVERE',
  nationalSecurityImpact: 'CRITICAL',

  // Mitigation factors
  existingDefenses: ['IDS', 'SEGMENTATION', 'MONITORING'],
  mitigationEffectiveness: 0.45,  // Current defenses 45% effective

  // Required improvements
  requiredInvestment: 5000000000,  // $5 billion
  requiredTime: duration('P18M'),  // 18 months to implement
  recommendedControls: [
    'COMPLETE_OT_IT_SEGMENTATION',
    'AI_THREAT_DETECTION',
    'ZERO_TRUST_ARCHITECTURE',
    'QUANTUM_RESISTANT_CRYPTO',
    'SECTOR_COORDINATION_CENTER'
  ],

  // Confidence and validity
  confidenceLevel: 0.70,
  validatedBy: ['DHS', 'CISA', 'Industry SMEs'],
  reviewDate: datetime() + duration('P3M'),

  // Metadata
  createdAt: datetime(),
  createdBy: 'Quarterly Risk Assessment Team',
  updatedAt: datetime()
})
RETURN scenario;
```

#### Step 2: Simulate Scenario Impact
```cypher
// Simulate scenario impact on actual infrastructure
MATCH (scenario:WhatIfScenario {scenarioId: 'SCENARIO-1234567890'})

// Find equipment in scenario scope
MATCH (e:Equipment)
WHERE e.sector IN scenario.targetSectors
  AND any(state IN scenario.geographicScope WHERE
    'GEO_STATE_' + state IN e.tags)

// Calculate individual equipment risk
WITH scenario, e,
  // Base probability from scenario
  scenario.infrastructureImpactPercent as baseProb,
  // Criticality multiplier
  CASE WHEN 'OPS_CRITICALITY_CRITICAL' IN e.tags THEN 1.5
       WHEN 'OPS_CRITICALITY_HIGH' IN e.tags THEN 1.2
       ELSE 1.0 END as criticalityMult,
  // Defense effectiveness reduction
  (1.0 - scenario.mitigationEffectiveness) as defenselessFactor

// Calculate impact probability for each equipment
WITH scenario, e,
  least(baseProb * criticalityMult * defenselessFactor, 0.95) as impactProbability,
  round(scenario.estimatedFinancialLoss * (toFloat(1) / 100000), 2) as equipmentLoss  // Distributed loss

// Create scenario impact relationships
CREATE (scenario)-[:WOULD_AFFECT {
  probability: round(impactProbability, 3),
  estimatedDowntime: scenario.projectedDowntime,
  estimatedLoss: equipmentLoss,
  cascadeRisk: scenario.cascadingFailures,
  detectionLikelihood: 1.0 - (scenario.detectionDelay.seconds / 86400.0),  // Convert to 0-1 scale
  recoveryComplexity: CASE
    WHEN impactProbability > 0.8 THEN 'VERY_HIGH'
    WHEN impactProbability > 0.6 THEN 'HIGH'
    WHEN impactProbability > 0.4 THEN 'MEDIUM'
    ELSE 'LOW'
  END,
  simulatedAt: datetime()
}]->(e)

WITH scenario, count(e) as affectedCount,
     sum(equipmentLoss) as totalLoss,
     avg(impactProbability) as avgProbability

// Update scenario with simulation results
SET scenario.simulatedAffectedCount = affectedCount,
    scenario.simulatedTotalLoss = totalLoss,
    scenario.simulatedAvgProbability = round(avgProbability, 3),
    scenario.lastSimulated = datetime()

RETURN scenario.scenarioName, affectedCount, totalLoss, avgProbability;
```

#### Step 3: Generate Mitigation Recommendations
```cypher
// Generate prioritized mitigation recommendations from scenario
MATCH (scenario:WhatIfScenario {scenarioId: 'SCENARIO-1234567890'})-[r:WOULD_AFFECT]->(e:Equipment)
WHERE r.probability > 0.6

// Group by equipment type and location
WITH scenario, e, r
WITH scenario,
  e.equipmentType as equipType,
  e.sector as sector,
  collect(DISTINCT substring(e.tags[0], 10)) as states,  // Extract state from tag
  count(e) as equipmentCount,
  avg(r.probability) as avgRisk,
  sum(r.estimatedLoss) as totalLoss,
  collect(r.recoveryComplexity) as complexities
ORDER BY totalLoss DESC

// Create mitigation recommendation nodes
CREATE (rec:MitigationRecommendation {
  recommendationId: 'REC-' + toString(timestamp()),
  scenarioId: scenario.scenarioId,

  // Target
  targetEquipmentType: equipType,
  targetSector: sector,
  targetStates: states,
  affectedCount: equipmentCount,

  // Risk metrics
  averageRiskScore: round(avgRisk, 3),
  totalFinancialExposure: totalLoss,

  // Recommended actions (from scenario)
  recommendations: scenario.recommendedControls,

  // Implementation
  priority: CASE
    WHEN totalLoss > scenario.estimatedFinancialLoss * 0.1 THEN 'CRITICAL'
    WHEN totalLoss > scenario.estimatedFinancialLoss * 0.05 THEN 'HIGH'
    ELSE 'MEDIUM'
  END,
  estimatedCost: round(scenario.requiredInvestment * (totalLoss / scenario.estimatedFinancialLoss), 0),
  estimatedTime: scenario.requiredTime,

  // ROI calculation
  riskReduction: scenario.mitigationEffectiveness,
  costBenefitRatio: round(totalLoss / (scenario.requiredInvestment * (totalLoss / scenario.estimatedFinancialLoss)), 2),

  createdAt: datetime(),
  validUntil: scenario.reviewDate
})

RETURN
  rec.targetEquipmentType,
  rec.targetSector,
  rec.affectedCount,
  rec.totalFinancialExposure,
  rec.priority,
  rec.costBenefitRatio
ORDER BY rec.totalFinancialExposure DESC;
```

### 4. Retrain NHITS Model (Monthly)

#### Model Retraining Procedure
```cypher
// Monthly NHITS model retraining data extraction
// Run on the 1st of each month

// 1. Extract training data from last 12 months
MATCH (event:InformationEvent)
WHERE event.publishedDate > datetime() - duration('P12M')
  AND event.processed = true

WITH event
ORDER BY event.publishedDate

// Aggregate by week for time-series
WITH
  date.truncate('week', event.publishedDate) as week,
  event.severity as severity,
  event.affectedSectors as sectors,
  event.impactScore as impact

WITH week, severity,
  count(*) as eventCount,
  avg(impact) as avgImpact,
  collect(DISTINCT sectors) as allSectors

// Format for NHITS training
RETURN
  toString(week) as timestamp,
  eventCount as target_variable,
  avgImpact as covariate_impact,
  size(allSectors) as covariate_sector_diversity,
  CASE severity
    WHEN 'CRITICAL' THEN 4
    WHEN 'HIGH' THEN 3
    WHEN 'MEDIUM' THEN 2
    ELSE 1
  END as covariate_severity_numeric
ORDER BY week;

// Export to CSV for Python NHITS training:
// CALL apoc.export.csv.query("...", "nhits_training_data.csv", {})
```

#### Model Performance Validation
```cypher
// Validate NHITS prediction accuracy
// Compare predictions from previous month with actual events

// Load previous month's predictions (assume stored in PredictionRun nodes)
MATCH (run:PredictionRun)
WHERE run.predictionDate = datetime() - duration('P1M')

WITH run
UNWIND run.predictions as pred

// Compare with actual events that occurred
MATCH (actual:InformationEvent)
WHERE date.truncate('week', actual.publishedDate) = date(pred.predicted_week)

WITH pred,
  count(actual) as actualCount,
  pred.predicted_count as predictedCount,
  abs(count(actual) - pred.predicted_count) as error

WITH
  avg(error) as meanAbsoluteError,
  sqrt(avg(error * error)) as rootMeanSquareError,
  collect({week: pred.predicted_week, predicted: predictedCount, actual: actualCount}) as comparisons

RETURN
  meanAbsoluteError,
  rootMeanSquareError,
  CASE WHEN meanAbsoluteError < 2.0 THEN 'ACCEPTABLE' ELSE 'RETRAIN_REQUIRED' END as modelStatus,
  comparisons
LIMIT 10;
```

### 5. Validate Prediction Accuracy (Quarterly)

#### Quarterly Prediction Audit
```cypher
// Comprehensive quarterly prediction accuracy audit
// Run at end of each quarter

// 1. Evaluate FutureThreat predictions
MATCH (pred:FutureThreat)
WHERE pred.predictionDate > datetime() - duration('P3M')
  AND pred.predictionDate < datetime()

WITH pred

// Check if predicted threat materialized
OPTIONAL MATCH (actual:InformationEvent)
WHERE actual.publishedDate >= pred.predictionDate
  AND actual.publishedDate <= pred.predictionDate + pred.forecastHorizon
  AND actual.eventType = pred.threatType
  AND any(sector IN actual.affectedSectors WHERE sector IN pred.targetSectors)

WITH pred, count(actual) as matchingEvents,
  CASE WHEN count(actual) > 0 THEN true ELSE false END as threatMaterialized

// Calculate prediction accuracy metrics
SET pred.validated = true,
    pred.validationDate = datetime(),
    pred.actualOccurrence = threatMaterialized,
    pred.accuracyScore = CASE
      WHEN threatMaterialized AND pred.probability > 0.7 THEN 1.0  // Correct high-probability prediction
      WHEN threatMaterialized AND pred.probability > 0.5 THEN 0.8  // Correct medium-probability
      WHEN threatMaterialized THEN 0.6  // Occurred but low probability
      WHEN NOT threatMaterialized AND pred.probability < 0.3 THEN 0.9  // Correctly predicted unlikely
      WHEN NOT threatMaterialized AND pred.probability < 0.5 THEN 0.7  // Acceptable false alarm
      ELSE 0.3  // High probability but didn't occur (poor prediction)
    END

WITH
  count(pred) as totalPredictions,
  sum(CASE WHEN pred.actualOccurrence THEN 1 ELSE 0 END) as correctPredictions,
  avg(pred.accuracyScore) as avgAccuracy,
  collect({
    prediction: pred.threatName,
    probability: pred.probability,
    occurred: pred.actualOccurrence,
    accuracy: pred.accuracyScore
  }) as details

RETURN
  totalPredictions,
  correctPredictions,
  round(toFloat(correctPredictions) / totalPredictions, 3) as hitRate,
  round(avgAccuracy, 3) as avgAccuracyScore,
  CASE WHEN avgAccuracy > 0.7 THEN '✓ ACCEPTABLE' ELSE '⚠ NEEDS IMPROVEMENT' END as overallStatus,
  details[0..5] as samplePredictions;
```

### 6. Archive Old Predictions (Annual)

#### Annual Cleanup Script
```cypher
// Annual prediction archive and cleanup
// Run on January 1st each year

// 1. Archive validated predictions older than 1 year
MATCH (pred:FutureThreat)
WHERE pred.validated = true
  AND pred.validationDate < datetime() - duration('P12M')

// Move to archive with summary
CREATE (archive:PredictionArchive {
  archiveId: 'ARCHIVE-' + toString(date.truncate('year', datetime())),
  originalPredictionId: pred.predictionId,
  threatName: pred.threatName,
  predictionDate: pred.predictionDate,
  probability: pred.probability,
  actualOccurrence: pred.actualOccurrence,
  accuracyScore: pred.accuracyScore,
  archivedAt: datetime(),
  archiveReason: 'ANNUAL_CLEANUP'
})

WITH archive, pred, count(pred) as archivedCount
DETACH DELETE pred

// 2. Archive expired scenarios
WITH archivedCount
MATCH (scenario:WhatIfScenario)
WHERE scenario.reviewDate < datetime() - duration('P6M')

SET scenario:ArchivedScenario,
    scenario.archivedAt = datetime()
REMOVE scenario:WhatIfScenario

// 3. Clean up orphaned relationships
WITH archivedCount, count(scenario) as archivedScenarios
MATCH ()-[r:WOULD_AFFECT]->()
WHERE NOT exists((:WhatIfScenario)--())
DELETE r

// 4. Generate archive summary
WITH archivedCount, archivedScenarios, count(r) as cleanedRelationships
MATCH (archive:PredictionArchive)
WHERE date.truncate('year', archive.archivedAt) = date.truncate('year', datetime())

WITH archivedCount, archivedScenarios, cleanedRelationships,
  count(archive) as totalArchived,
  avg(archive.accuracyScore) as avgHistoricalAccuracy,
  sum(CASE WHEN archive.actualOccurrence THEN 1 ELSE 0 END) as historicalHits

RETURN
  totalArchived as predictionsArchived,
  archivedScenarios as scenariosArchived,
  cleanedRelationships as orphanRelationshipsRemoved,
  round(avgHistoricalAccuracy, 3) as historicalAccuracy,
  round(toFloat(historicalHits) / totalArchived, 3) as historicalHitRate,
  datetime() as completedAt;
```

---

## 🧠 Cognitive Bias Relationship Maintenance

### Overview
Cognitive biases influence threat perception and decision-making. This section provides procedures for maintaining bias relationships, updating strength scores, and recalculating sector susceptibility.

### 1. Update HAS_BIAS Strengths (Weekly)

#### Weekly Bias Strength Calibration
```cypher
// Weekly cognitive bias strength recalibration
// Run every Sunday at midnight

// 1. Analyze recent event activations
MATCH (event:InformationEvent)-[a:ACTIVATES]->(bias:CognitiveBias)
WHERE a.activatedAt > datetime() - duration('P7D')
  AND a.expiresAt > datetime()

WITH bias,
  count(a) as weeklyActivations,
  avg(a.activationStrength) as avgActivationStrength

// 2. Update bias strength based on activity
MATCH (bias)-[hb:HAS_BIAS]->(sector)

WITH bias, hb, sector, weeklyActivations, avgActivationStrength,
  // Calculate adjustment factor
  CASE
    WHEN weeklyActivations > 10 THEN 1.1  // High activity increases bias strength
    WHEN weeklyActivations > 5 THEN 1.05
    WHEN weeklyActivations < 2 THEN 0.95  // Low activity decreases strength
    ELSE 1.0
  END as adjustmentFactor

// Apply bounded adjustment (keep between 0.1 and 1.0)
SET hb.strength = round(
  least(greatest(hb.strength * adjustmentFactor, 0.1), 1.0),
  3
),
hb.lastUpdated = datetime(),
hb.weeklyActivations = weeklyActivations,
hb.calibrationReason = 'WEEKLY_ACTIVITY_ADJUSTMENT'

RETURN
  bias.biasType,
  sector.name as sector,
  hb.strength as newStrength,
  weeklyActivations,
  adjustmentFactor
ORDER BY weeklyActivations DESC;
```

### 2. Recalculate TARGETS_SECTOR Susceptibility (Monthly)

#### Monthly Sector Susceptibility Analysis
```cypher
// Monthly sector susceptibility recalculation
// Run on the 1st of each month

// 1. Analyze historical attack patterns by sector
MATCH (pattern:HistoricalPattern)
WHERE pattern.incidentDate > datetime() - duration('P24M')

WITH pattern.targetSector as sector,
  count(pattern) as historicalAttacks,
  avg(pattern.impactScore) as avgImpact,
  collect(pattern.threatActor) as threatActors

// 2. Analyze recent events by sector
MATCH (event:InformationEvent)
WHERE event.publishedDate > datetime() - duration('P6M')
  AND event.processed = true

UNWIND event.affectedSectors as eventSector
WITH sector, historicalAttacks, avgImpact, threatActors,
  eventSector,
  count(event) as recentEvents,
  avg(event.impactScore) as recentAvgImpact

WHERE sector = eventSector

// 3. Calculate composite susceptibility score
WITH sector,
  // Historical attack frequency (normalized)
  toFloat(historicalAttacks) / 50.0 as historicalFactor,
  // Recent event frequency (normalized)
  toFloat(recentEvents) / 20.0 as recentFactor,
  // Impact severity
  (avgImpact + recentAvgImpact) / 20.0 as impactFactor,
  // Threat actor diversity
  toFloat(size(apoc.coll.toSet(threatActors))) / 10.0 as actorDiversityFactor

WITH sector,
  least((historicalFactor * 0.3 + recentFactor * 0.4 + impactFactor * 0.2 + actorDiversityFactor * 0.1), 1.0) as susceptibilityScore

// 4. Update TARGETS_SECTOR relationships
MATCH (bias:CognitiveBias)-[ts:TARGETS_SECTOR]->(s:Sector)
WHERE s.name = sector

SET ts.susceptibility = round(susceptibilityScore, 3),
    ts.lastCalculated = datetime(),
    ts.calculationMethod = 'MONTHLY_COMPOSITE',
    ts.factors = {
      historical: round(historicalFactor, 3),
      recent: round(recentFactor, 3),
      impact: round(impactFactor, 3),
      actorDiversity: round(actorDiversityFactor, 3)
    }

RETURN
  sector,
  round(susceptibilityScore, 3) as newSusceptibility,
  count(bias) as biasesUpdated
ORDER BY susceptibilityScore DESC;
```

### 3. Add New Bias Type

#### Create New Cognitive Bias
```cypher
// Add new cognitive bias type to system
CREATE (bias:CognitiveBias {
  // Identifiers
  biasId: 'BIAS-' + toString(timestamp()),
  biasType: 'NORMALCY',  // New bias type
  name: 'Normalcy Bias',

  // Description
  description: 'Tendency to underestimate threat likelihood by assuming conditions will remain normal',
  psychologicalBasis: 'Cognitive dissonance reduction and status quo preference',

  // Activation parameters
  activationThreshold: 0.65,
  decayRate: duration('P14D'),  // Decays over 14 days

  // Impact on decision-making
  decisionImpact: 'UNDERESTIMATION',  // UNDERESTIMATION | OVERESTIMATION | DISTORTION
  riskPerceptionEffect: -0.3,  // Reduces perceived risk by 30%

  // Mitigation strategies
  mitigationStrategies: [
    'RED_TEAM_EXERCISES',
    'HISTORICAL_INCIDENT_REVIEW',
    'REGULAR_THREAT_BRIEFINGS',
    'TABLETOP_EXERCISES'
  ],

  // Metadata
  evidenceBase: ['Psychology literature', 'Disaster response studies'],
  addedBy: 'Behavioral Security Team',

  createdAt: datetime(),
  updatedAt: datetime()
})

// Link to all sectors with initial strength
WITH bias
MATCH (sector:Sector)
CREATE (bias)-[:HAS_BIAS {
  strength: 0.5,  // Initial moderate strength
  confidence: 0.6,
  createdAt: datetime(),
  lastUpdated: datetime()
}]->(sector)

CREATE (bias)-[:TARGETS_SECTOR {
  susceptibility: 0.5,  // Initial moderate susceptibility
  lastCalculated: datetime()
}]->(sector)

RETURN bias, count(sector) as sectorsLinked;
```

### 4. Complete Bias Update Scripts

#### Comprehensive Bias Maintenance Script
```cypher
// Daily comprehensive bias relationship maintenance
// Run every day at 2:00 AM

// 1. Expire old activations
MATCH (event:InformationEvent)-[a:ACTIVATES]->(bias:CognitiveBias)
WHERE a.expiresAt <= datetime()

DELETE a

WITH count(a) as expiredActivations

// 2. Update active bias strengths based on current activations
MATCH (event:InformationEvent)-[a:ACTIVATES]->(bias:CognitiveBias)
WHERE a.expiresAt > datetime()

WITH bias,
  count(a) as activeActivations,
  avg(a.activationStrength) as avgStrength,
  max(a.expiresAt) as latestExpiration

MATCH (bias)-[hb:HAS_BIAS]->(sector:Sector)

// Boost strength for actively activated biases
SET hb.strength = least(
  hb.strength + (activeActivations * 0.05),
  1.0
),
hb.lastUpdated = datetime(),
hb.activeActivations = activeActivations

// 3. Decay biases without recent activations
WITH count(hb) as boostedBiases, expiredActivations
MATCH (bias:CognitiveBias)-[hb:HAS_BIAS]->(sector:Sector)
WHERE hb.lastUpdated < datetime() - duration('P7D')
  AND NOT exists((bias)<-[:ACTIVATES]-(:InformationEvent))

SET hb.strength = greatest(hb.strength * 0.95, 0.1),  // 5% weekly decay, minimum 0.1
    hb.lastUpdated = datetime(),
    hb.decayApplied = true

WITH boostedBiases, expiredActivations, count(hb) as decayedBiases

RETURN
  expiredActivations,
  boostedBiases,
  decayedBiases,
  datetime() as completedAt;
```

---

## 📊 Pipeline Health Monitoring

### Overview
Continuous monitoring of Level 5/6 pipeline performance, latency metrics, correlation accuracy, and data quality.

### 1. Check Latency Metrics (<5 min requirement)

#### Real-Time Latency Monitor
```cypher
// Real-time event processing latency check
// Run continuously or every 5 minutes

// Check current hour's processing performance
MATCH (event:InformationEvent)
WHERE event.collectedDate > datetime() - duration('PT1H')
  AND event.correlatedAt IS NOT NULL

WITH event,
  duration.between(event.collectedDate, event.correlatedAt) as latency,
  duration('PT5M') as slaThreshold

WITH
  count(event) as totalEvents,
  avg(latency.seconds) as avgLatencySeconds,
  max(latency.seconds) as maxLatencySeconds,
  percentileCont(latency.seconds, 0.95) as p95LatencySeconds,
  sum(CASE WHEN latency <= slaThreshold THEN 1 ELSE 0 END) as withinSLA,
  collect(CASE WHEN latency > slaThreshold THEN event.eventId ELSE null END) as breachedEvents

RETURN
  totalEvents,
  round(avgLatencySeconds, 2) as avgLatency,
  round(maxLatencySeconds, 2) as maxLatency,
  round(p95LatencySeconds, 2) as p95Latency,
  withinSLA,
  round(toFloat(withinSLA) / totalEvents * 100, 2) as slaCompliancePercent,
  CASE
    WHEN toFloat(withinSLA) / totalEvents >= 0.95 THEN '✓ HEALTHY'
    WHEN toFloat(withinSLA) / totalEvents >= 0.85 THEN '⚠ DEGRADED'
    ELSE '❌ CRITICAL'
  END as status,
  [e IN breachedEvents WHERE e IS NOT NULL] as breachedEventIds;
```

### 2. Monitor Correlation Accuracy (≥0.75 requirement)

#### Correlation Quality Dashboard
```cypher
// Correlation accuracy monitoring dashboard
// Run every 15 minutes

// Analyze correlation quality by event type
MATCH (event:InformationEvent)-[r:CORRELATES_TO]->(e:Equipment)
WHERE event.correlatedAt > datetime() - duration('PT4H')

WITH event.eventType as eventType,
  event.severity as severity,
  avg(r.correlationScore) as avgScore,
  count(r) as correlationCount,
  percentileCont(r.correlationScore, 0.5) as medianScore,
  percentileCont(r.correlationScore, 0.25) as q1Score,
  collect(CASE WHEN r.correlationScore < 0.75 THEN event.eventId ELSE null END) as lowQualityEvents

RETURN
  eventType,
  severity,
  correlationCount,
  round(avgScore, 3) as avgCorrelationScore,
  round(medianScore, 3) as medianScore,
  round(q1Score, 3) as q1Score,
  CASE
    WHEN avgScore >= 0.85 THEN '✓ EXCELLENT'
    WHEN avgScore >= 0.75 THEN '✓ GOOD'
    WHEN avgScore >= 0.65 THEN '⚠ ACCEPTABLE'
    ELSE '❌ REVIEW REQUIRED'
  END as qualityStatus,
  size([e IN lowQualityEvents WHERE e IS NOT NULL]) as lowQualityCount
ORDER BY avgScore DESC;
```

### 3. Event Processor Status Checks

#### Event Processor Health Monitor
```cypher
// Comprehensive event processor health check
// Run every 10 minutes

// 1. Check processing queue depth
MATCH (event:InformationEvent)
WHERE event.processed = false

WITH count(event) as queueDepth,
  min(event.collectedDate) as oldestEvent

// 2. Check processor throughput
MATCH (processed:InformationEvent)
WHERE processed.correlatedAt > datetime() - duration('PT1H')

WITH queueDepth, oldestEvent,
  count(processed) as lastHourThroughput,
  avg(duration.between(processed.collectedDate, processed.correlatedAt).seconds) as avgProcessingTime

// 3. Check error rates
MATCH (failed:InformationEvent)
WHERE failed.processed = false
  AND failed.collectedDate < datetime() - duration('PT30M')

WITH queueDepth, oldestEvent, lastHourThroughput, avgProcessingTime,
  count(failed) as stuckEvents

// 4. Overall processor health assessment
RETURN
  // Queue metrics
  queueDepth,
  oldestEvent,
  duration.between(oldestEvent, datetime()) as oldestEventAge,

  // Throughput metrics
  lastHourThroughput,
  round(lastHourThroughput / 60.0, 2) as eventsPerMinute,
  round(avgProcessingTime, 2) as avgProcessingSeconds,

  // Error metrics
  stuckEvents,

  // Overall status
  CASE
    WHEN queueDepth < 50 AND stuckEvents = 0 AND avgProcessingTime < 120 THEN '✓ HEALTHY'
    WHEN queueDepth < 100 AND stuckEvents < 10 THEN '⚠ DEGRADED'
    ELSE '❌ CRITICAL - INTERVENTION REQUIRED'
  END as processorStatus,

  datetime() as checkTime;
```

### 4. Threat Feed Reliability Monitoring

#### Feed Reliability Dashboard
```cypher
// Threat feed health and reliability monitoring
// Run every 30 minutes

MATCH (feed:ThreatFeed)
WHERE feed.active = true

WITH feed,
  duration.between(feed.lastCollected, datetime()) as timeSinceCollection,
  feed.updateFrequency as expectedFrequency

// Calculate reliability metrics
OPTIONAL MATCH (job:FeedCollectionJob)
WHERE job.feedId = feed.feedId
  AND job.startedAt > datetime() - duration('P7D')

WITH feed, timeSinceCollection, expectedFrequency,
  count(job) as collectionsLast7Days,
  sum(CASE WHEN job.status = 'SUCCESS' THEN 1 ELSE 0 END) as successfulCollections,
  sum(CASE WHEN job.status = 'FAILED' THEN 1 ELSE 0 END) as failedCollections

// Calculate uptime and reliability
WITH feed, timeSinceCollection, expectedFrequency,
  collectionsLast7Days,
  successfulCollections,
  failedCollections,
  toFloat(successfulCollections) / nullif(collectionsLast7Days, 0) as uptimePercent

RETURN
  feed.feedName,
  feed.feedType,
  round(timeSinceCollection.minutes, 2) as minutesSinceCollection,
  round(expectedFrequency.minutes, 2) as expectedFrequencyMinutes,
  collectionsLast7Days,
  successfulCollections,
  failedCollections,
  round(uptimePercent * 100, 2) as uptimePercent,
  feed.errorCount as currentErrors,
  CASE
    WHEN timeSinceCollection > (expectedFrequency * 2) THEN '❌ STALE'
    WHEN uptimePercent < 0.95 THEN '⚠ UNRELIABLE'
    WHEN uptimePercent >= 0.99 THEN '✓ EXCELLENT'
    ELSE '✓ GOOD'
  END as status
ORDER BY uptimePercent ASC;
```

### 5. Complete Monitoring Queries

#### Comprehensive System Health Check
```cypher
// Complete Level 5/6 system health check
// Run every hour for full system assessment

// 1. Event pipeline metrics
MATCH (event:InformationEvent)
WHERE event.collectedDate > datetime() - duration('P1D')

WITH
  count(event) as totalEvents24h,
  sum(CASE WHEN event.processed THEN 1 ELSE 0 END) as processedEvents,
  sum(CASE WHEN NOT event.processed THEN 1 ELSE 0 END) as pendingEvents,
  avg(duration.between(event.collectedDate, event.correlatedAt).seconds) as avgLatency

// 2. Correlation quality metrics
MATCH (event:InformationEvent)-[r:CORRELATES_TO]->()
WHERE event.correlatedAt > datetime() - duration('P1D')

WITH totalEvents24h, processedEvents, pendingEvents, avgLatency,
  avg(r.correlationScore) as avgCorrelation,
  sum(CASE WHEN r.correlationScore >= 0.75 THEN 1 ELSE 0 END) as highQualityCorrelations,
  count(r) as totalCorrelations

// 3. Prediction system metrics
MATCH (pred:FutureThreat)
WHERE pred.updatedAt > datetime() - duration('P7D')

WITH totalEvents24h, processedEvents, pendingEvents, avgLatency,
  avgCorrelation, highQualityCorrelations, totalCorrelations,
  count(pred) as activePredictions,
  avg(pred.probability) as avgPredictionProbability

// 4. Bias activation metrics
MATCH ()-[a:ACTIVATES]->(bias:CognitiveBias)
WHERE a.activatedAt > datetime() - duration('P1D')
  AND a.expiresAt > datetime()

WITH totalEvents24h, processedEvents, pendingEvents, avgLatency,
  avgCorrelation, highQualityCorrelations, totalCorrelations,
  activePredictions, avgPredictionProbability,
  count(DISTINCT bias) as activeBiases

RETURN
  // Event Pipeline
  totalEvents24h,
  processedEvents,
  pendingEvents,
  round(toFloat(processedEvents) / totalEvents24h * 100, 2) as processingRate,
  round(avgLatency, 2) as avgLatencySeconds,
  CASE WHEN avgLatency < 300 THEN '✓' ELSE '❌' END as latencySLA,

  // Correlation Quality
  totalCorrelations,
  round(avgCorrelation, 3) as avgCorrelationScore,
  round(toFloat(highQualityCorrelations) / totalCorrelations * 100, 2) as highQualityPercent,
  CASE WHEN avgCorrelation >= 0.75 THEN '✓' ELSE '❌' END as correlationSLA,

  // Prediction System
  activePredictions,
  round(avgPredictionProbability, 3) as avgProbability,

  // Bias System
  activeBiases,

  // Overall Status
  CASE
    WHEN avgLatency < 300 AND avgCorrelation >= 0.75 AND pendingEvents < 20 THEN '✓ ALL SYSTEMS HEALTHY'
    WHEN avgLatency < 600 AND avgCorrelation >= 0.70 THEN '⚠ DEGRADED PERFORMANCE'
    ELSE '❌ CRITICAL - IMMEDIATE ATTENTION REQUIRED'
  END as overallStatus,

  datetime() as reportTime;
```

---

## 💾 Advanced Backup & Recovery

### Overview
Comprehensive backup and recovery procedures specific to Level 5/6 components, including event streams, predictions, and trained models.

### 1. Level 5/6 Backup Procedures

#### Daily Event Stream Backup
```bash
#!/bin/bash
# daily_level56_backup.sh
# Run daily at 3:00 AM

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backup/level56"
mkdir -p "${BACKUP_DIR}"

# 1. Export InformationEvents from last 7 days
neo4j-admin database dump neo4j --to-path="${BACKUP_DIR}/events_${DATE}.dump" \
  --include-query="MATCH (e:InformationEvent) WHERE e.collectedDate > datetime() - duration('P7D') RETURN e"

# 2. Export GeopoliticalEvents
neo4j-admin database dump neo4j --to-path="${BACKUP_DIR}/geo_events_${DATE}.dump" \
  --include-query="MATCH (g:GeopoliticalEvent) RETURN g"

# 3. Export FutureThreat predictions
neo4j-admin database dump neo4j --to-path="${BACKUP_DIR}/predictions_${DATE}.dump" \
  --include-query="MATCH (p:FutureThreat) WHERE p.validUntil > datetime() RETURN p"

# 4. Export HistoricalPatterns
neo4j-admin database dump neo4j --to-path="${BACKUP_DIR}/patterns_${DATE}.dump" \
  --include-query="MATCH (h:HistoricalPattern) RETURN h"

# 5. Export ThreatFeed configurations
neo4j-admin database dump neo4j --to-path="${BACKUP_DIR}/feeds_${DATE}.dump" \
  --include-query="MATCH (f:ThreatFeed) RETURN f"

# 6. Compress backups
tar -czf "${BACKUP_DIR}/level56_complete_${DATE}.tar.gz" \
  "${BACKUP_DIR}"/events_${DATE}.dump \
  "${BACKUP_DIR}"/geo_events_${DATE}.dump \
  "${BACKUP_DIR}"/predictions_${DATE}.dump \
  "${BACKUP_DIR}"/patterns_${DATE}.dump \
  "${BACKUP_DIR}"/feeds_${DATE}.dump

# 7. Remove individual dumps, keep compressed archive
rm "${BACKUP_DIR}"/*.dump

# 8. Clean old backups (keep 30 days)
find "${BACKUP_DIR}" -name "level56_complete_*.tar.gz" -mtime +30 -delete

echo "Level 5/6 backup completed: ${DATE}"
```

#### Weekly Full System Backup
```bash
#!/bin/bash
# weekly_full_backup.sh
# Run every Sunday at 2:00 AM

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backup/full"
mkdir -p "${BACKUP_DIR}"

# Stop Neo4j for consistent backup
sudo systemctl stop neo4j

# Full database dump
neo4j-admin database dump neo4j --to-path="${BACKUP_DIR}/aeon_complete_${DATE}.dump"

# Start Neo4j
sudo systemctl start neo4j

# Compress and encrypt
tar -czf - "${BACKUP_DIR}/aeon_complete_${DATE}.dump" | \
  openssl enc -aes-256-cbc -salt -out "${BACKUP_DIR}/aeon_complete_${DATE}.dump.tar.gz.enc" \
  -pass file:/secure/backup_key.txt

# Remove unencrypted dump
rm "${BACKUP_DIR}/aeon_complete_${DATE}.dump"

# Clean old backups (keep 12 weeks)
find "${BACKUP_DIR}" -name "aeon_complete_*.dump.tar.gz.enc" -mtime +84 -delete

echo "Full system backup completed: ${DATE}"
```

### 2. Rollback Scripts for Failed Deployments

#### Event Stream Rollback
```cypher
// Rollback failed event processing deployment
// Use when event processor updates cause issues

// 1. Identify events processed by failed deployment
MATCH (event:InformationEvent)
WHERE event.correlatedAt > datetime('2024-11-23T10:00:00Z')  // Deployment time
  AND event.processed = true

// 2. Mark events for reprocessing
SET event.processed = false,
    event.correlatedAt = null,
    event.correlatedCount = null,
    event.rollbackAt = datetime(),
    event.rollbackReason = 'FAILED_DEPLOYMENT_ROLLBACK'

// 3. Delete correlations created by failed deployment
WITH event
MATCH (event)-[r:CORRELATES_TO]->()
WHERE r.correlatedAt > datetime('2024-11-23T10:00:00Z')
DELETE r

// 4. Delete bias activations from failed deployment
WITH event
MATCH (event)-[a:ACTIVATES]->()
WHERE a.activatedAt > datetime('2024-11-23T10:00:00Z')
DELETE a

WITH count(event) as rolledBackEvents

RETURN
  rolledBackEvents,
  'Events will be reprocessed by stable version' as status,
  datetime() as rollbackCompletedAt;
```

#### Prediction Model Rollback
```cypher
// Rollback failed prediction model deployment
// Restore previous model predictions

// 1. Archive predictions from failed model
MATCH (pred:FutureThreat)
WHERE pred.createdAt > datetime('2024-11-23T10:00:00Z')  // Failed deployment time
  AND pred.predictionMethod = 'NHITS_V2_FAILED'

SET pred:FailedPrediction,
    pred.archivedAt = datetime(),
    pred.archivedReason = 'MODEL_ROLLBACK'
REMOVE pred:FutureThreat

// 2. Restore predictions from previous model (from backup)
WITH count(pred) as archivedCount

// Load backup predictions (assumes backup was restored to temp label)
MATCH (backup:BackupPrediction)
WHERE backup.backupDate = date('2024-11-22')

// Restore as active predictions
CREATE (restored:FutureThreat)
SET restored = properties(backup),
    restored.restoredAt = datetime(),
    restored.restoredFrom = 'BACKUP_2024-11-22'
REMOVE restored:BackupPrediction

WITH archivedCount, count(restored) as restoredCount

RETURN
  archivedCount as failedPredictionsArchived,
  restoredCount as previousPredictionsRestored,
  'Prediction system rolled back to stable version' as status;
```

### 3. Data Validation After Recovery

#### Post-Recovery Validation Script
```cypher
// Comprehensive post-recovery validation
// Run after any backup restoration

// 1. Validate InformationEvents integrity
MATCH (event:InformationEvent)
WITH
  count(event) as totalEvents,
  sum(CASE WHEN event.eventId IS NULL THEN 1 ELSE 0 END) as missingIds,
  sum(CASE WHEN event.collectedDate IS NULL THEN 1 ELSE 0 END) as missingDates,
  sum(CASE WHEN event.affectedSectors IS NULL OR size(event.affectedSectors) = 0 THEN 1 ELSE 0 END) as missingSectors

WITH totalEvents, missingIds, missingDates, missingSectors,
  CASE WHEN missingIds + missingDates + missingSectors = 0 THEN '✓ VALID' ELSE '❌ DATA ISSUES' END as eventStatus

// 2. Validate relationship integrity
MATCH (event:InformationEvent)-[r:CORRELATES_TO]->(e:Equipment)
WITH eventStatus, totalEvents, missingIds, missingDates, missingSectors,
  count(r) as correlations,
  sum(CASE WHEN r.correlationScore IS NULL THEN 1 ELSE 0 END) as invalidCorrelations

WITH eventStatus, totalEvents, missingIds, missingDates, missingSectors, correlations, invalidCorrelations,
  CASE WHEN invalidCorrelations = 0 THEN '✓ VALID' ELSE '❌ INVALID CORRELATIONS' END as correlationStatus

// 3. Validate FutureThreat predictions
MATCH (pred:FutureThreat)
WITH eventStatus, totalEvents, missingIds, missingDates, missingSectors,
  correlations, invalidCorrelations, correlationStatus,
  count(pred) as predictions,
  sum(CASE WHEN pred.predictionId IS NULL OR pred.probability IS NULL THEN 1 ELSE 0 END) as invalidPredictions

WITH eventStatus, totalEvents, missingIds, missingDates, missingSectors,
  correlations, invalidCorrelations, correlationStatus,
  predictions, invalidPredictions,
  CASE WHEN invalidPredictions = 0 THEN '✓ VALID' ELSE '❌ INVALID PREDICTIONS' END as predictionStatus

// 4. Validate CognitiveBias relationships
MATCH ()-[hb:HAS_BIAS]->()
WITH eventStatus, totalEvents, missingIds, missingDates, missingSectors,
  correlations, invalidCorrelations, correlationStatus,
  predictions, invalidPredictions, predictionStatus,
  count(hb) as biasRelationships,
  sum(CASE WHEN hb.strength IS NULL OR hb.strength < 0 OR hb.strength > 1 THEN 1 ELSE 0 END) as invalidBiases

RETURN
  // Events validation
  eventStatus,
  totalEvents,
  missingIds,
  missingDates,
  missingSectors,

  // Correlations validation
  correlationStatus,
  correlations,
  invalidCorrelations,

  // Predictions validation
  predictionStatus,
  predictions,
  invalidPredictions,

  // Bias validation
  CASE WHEN invalidBiases = 0 THEN '✓ VALID' ELSE '❌ INVALID BIASES' END as biasStatus,
  biasRelationships,
  invalidBiases,

  // Overall status
  CASE
    WHEN eventStatus = '✓ VALID'
      AND correlationStatus = '✓ VALID'
      AND predictionStatus = '✓ VALID'
      AND invalidBiases = 0
    THEN '✓✓✓ RECOVERY SUCCESSFUL - ALL DATA VALID'
    ELSE '❌ RECOVERY ISSUES DETECTED - MANUAL REVIEW REQUIRED'
  END as overallStatus,

  datetime() as validationTime;
```

---

**Wiki Navigation**: [Main](00_MAIN_INDEX.md) | [API](API_REFERENCE.md) | [Queries](QUERIES_LIBRARY.md) | [Reproducibility](REPRODUCIBILITY_GUIDE.md)