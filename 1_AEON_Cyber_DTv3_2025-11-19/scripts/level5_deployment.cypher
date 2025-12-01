// ============================================================================
// LEVEL 5 DEPLOYMENT SCRIPT - Information Streams & Events
// ============================================================================
// Created: 2025-11-23
// Purpose: Deploy 6,000 Level 5 nodes with 50,000+ relationships
// Integration: Links to 537K existing nodes (CVEs, Sectors, Organizations)
// Data Source: level5_generated_data.json
//
// DEPLOYMENT PHASES:
//   Phase 1: Constraints & Indexes (15 constraints, 20+ indexes)
//   Phase 2: InformationEvents (2,000 nodes)
//   Phase 3: GeopoliticalEvents (800 nodes)
//   Phase 4: ThreatFeeds (200 nodes)
//   Phase 5: MediaEvents (2,000 nodes)
//   Phase 6: TechnologyShifts (1,000 nodes)
//   Phase 7: Cross-level relationships (50,000+ edges)
//   Phase 8: Verification queries
// ============================================================================

// ============================================================================
// PHASE 1: CONSTRAINTS AND INDEXES
// ============================================================================

// 1.1: InformationEvent Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (ie:InformationEvent) REQUIRE ie.eventId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ie:InformationEvent) REQUIRE ie.eventId IS NOT NULL;

// 1.2: GeopoliticalEvent Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (ge:GeopoliticalEvent) REQUIRE ge.eventId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ge:GeopoliticalEvent) REQUIRE ge.eventId IS NOT NULL;

// 1.3: ThreatFeed Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (tf:ThreatFeed) REQUIRE tf.feedId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (tf:ThreatFeed) REQUIRE tf.feedId IS NOT NULL;

// 1.4: MediaEvent Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (me:MediaEvent) REQUIRE me.eventId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (me:MediaEvent) REQUIRE me.eventId IS NOT NULL;

// 1.5: TechnologyShift Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (ts:TechnologyShift) REQUIRE ts.shiftId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ts:TechnologyShift) REQUIRE ts.shiftId IS NOT NULL;

// 1.6: Performance Indexes - InformationEvent
CREATE INDEX IF NOT EXISTS FOR (ie:InformationEvent) ON (ie.eventType);
CREATE INDEX IF NOT EXISTS FOR (ie:InformationEvent) ON (ie.timestamp);
CREATE INDEX IF NOT EXISTS FOR (ie:InformationEvent) ON (ie.severity);
CREATE INDEX IF NOT EXISTS FOR (ie:InformationEvent) ON (ie.cveId);
CREATE INDEX IF NOT EXISTS FOR (ie:InformationEvent) ON (ie.sector);

// 1.7: Performance Indexes - GeopoliticalEvent
CREATE INDEX IF NOT EXISTS FOR (ge:GeopoliticalEvent) ON (ge.eventType);
CREATE INDEX IF NOT EXISTS FOR (ge:GeopoliticalEvent) ON (ge.timestamp);
CREATE INDEX IF NOT EXISTS FOR (ge:GeopoliticalEvent) ON (ge.tensionLevel);

// 1.8: Performance Indexes - ThreatFeed
CREATE INDEX IF NOT EXISTS FOR (tf:ThreatFeed) ON (tf.updateFrequency);
CREATE INDEX IF NOT EXISTS FOR (tf:ThreatFeed) ON (tf.reliability);
CREATE INDEX IF NOT EXISTS FOR (tf:ThreatFeed) ON (tf.feedType);

// 1.9: Performance Indexes - MediaEvent
CREATE INDEX IF NOT EXISTS FOR (me:MediaEvent) ON (me.eventType);
CREATE INDEX IF NOT EXISTS FOR (me:MediaEvent) ON (me.amplification);
CREATE INDEX IF NOT EXISTS FOR (me:MediaEvent) ON (me.sentiment);
CREATE INDEX IF NOT EXISTS FOR (me:MediaEvent) ON (me.timestamp);

// 1.10: Performance Indexes - TechnologyShift
CREATE INDEX IF NOT EXISTS FOR (ts:TechnologyShift) ON (ts.shiftType);
CREATE INDEX IF NOT EXISTS FOR (ts:TechnologyShift) ON (ts.paradigm);
CREATE INDEX IF NOT EXISTS FOR (ts:TechnologyShift) ON (ts.impactLevel);
CREATE INDEX IF NOT EXISTS FOR (ts:TechnologyShift) ON (ts.maturityLevel);

// 1.11: Composite Indexes for Common Cross-Level Queries
CREATE INDEX IF NOT EXISTS FOR (ie:InformationEvent) ON (ie.eventType, ie.severity);
CREATE INDEX IF NOT EXISTS FOR (ie:InformationEvent) ON (ie.sector, ie.timestamp);
CREATE INDEX IF NOT EXISTS FOR (me:MediaEvent) ON (me.eventType, me.amplification);

// ============================================================================
// PHASE 2: LOAD INFORMATION EVENTS (2,000 nodes)
// ============================================================================

// 2.1: InformationEvent - CVE Disclosures (1,000 events)
// Links to 316,000 existing CVE nodes
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.informationEvents.cveDisclosures AS event
CREATE (ie:InformationEvent {
  eventId: event.eventId,
  eventType: 'CVE_DISCLOSURE',
  timestamp: datetime(event.timestamp),
  
  // CVE Reference
  cveId: event.cveId,
  severity: event.severity,
  cvssScore: event.cvssScore,
  
  // Media & Psychology
  mediaAmplification: event.mediaAmplification,
  fearFactor: event.fearFactor,
  realityFactor: event.realityFactor,
  
  // Organizational Impact
  sector: event.sector,
  affectedOrganizations: event.affectedOrganizations,
  activatesBiases: event.activatesBiases,
  
  // Predicted Response
  predictedResponseTime: event.predictedResponseTime,
  predictedPatchVelocity: event.predictedPatchVelocity,
  
  // Metadata
  source: event.source,
  confidence: event.confidence,
  createdAt: datetime()
});

// 2.2: InformationEvent - Security Incidents (500 events)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.informationEvents.incidents AS event
CREATE (ie:InformationEvent {
  eventId: event.eventId,
  eventType: 'INCIDENT',
  timestamp: datetime(event.timestamp),
  
  // Incident Details
  incidentType: event.incidentType,
  severity: event.severity,
  impactScore: event.impactScore,
  
  // Affected Entities
  sector: event.sector,
  organization: event.organization,
  affectedAssets: event.affectedAssets,
  
  // Media & Psychology
  mediaAmplification: event.mediaAmplification,
  fearFactor: event.fearFactor,
  realityFactor: event.realityFactor,
  publicDisclosure: event.publicDisclosure,
  
  // Organizational Response
  activatesBiases: event.activatesBiases,
  responsePattern: event.responsePattern,
  
  // Attack Details
  attackVectors: event.attackVectors,
  threatActorType: event.threatActorType,
  
  // Metadata
  source: event.source,
  confidence: event.confidence,
  createdAt: datetime()
});

// 2.3: InformationEvent - Data Breaches (300 events)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.informationEvents.breaches AS event
CREATE (ie:InformationEvent {
  eventId: event.eventId,
  eventType: 'BREACH',
  timestamp: datetime(event.timestamp),
  
  // Breach Details
  breachType: event.breachType,
  recordsExposed: event.recordsExposed,
  dataTypes: event.dataTypes,
  severity: event.severity,
  
  // Affected Entities
  sector: event.sector,
  organization: event.organization,
  
  // Media & Psychology
  mediaAmplification: event.mediaAmplification,
  fearFactor: event.fearFactor,
  realityFactor: event.realityFactor,
  regulatoryImpact: event.regulatoryImpact,
  
  // Organizational Impact
  activatesBiases: event.activatesBiases,
  estimatedCost: event.estimatedCost,
  reputationDamage: event.reputationDamage,
  
  // Attack Chain
  attackVectors: event.attackVectors,
  exploitedCVEs: event.exploitedCVEs,
  
  // Metadata
  source: event.source,
  confidence: event.confidence,
  createdAt: datetime()
});

// 2.4: InformationEvent - Campaigns (200 events)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.informationEvents.campaigns AS event
CREATE (ie:InformationEvent {
  eventId: event.eventId,
  eventType: 'CAMPAIGN',
  timestamp: datetime(event.timestamp),
  
  // Campaign Details
  campaignName: event.campaignName,
  threatActor: event.threatActor,
  motivation: event.motivation,
  sophistication: event.sophistication,
  
  // Targets
  targetSectors: event.targetSectors,
  targetRegions: event.targetRegions,
  targetedOrganizations: event.targetedOrganizations,
  
  // Tactics & Techniques
  techniques: event.techniques,
  exploitedCVEs: event.exploitedCVEs,
  toolsUsed: event.toolsUsed,
  
  // Media & Psychology
  mediaAmplification: event.mediaAmplification,
  fearFactor: event.fearFactor,
  realityFactor: event.realityFactor,
  
  // Impact
  severity: event.severity,
  affectedOrganizations: event.affectedOrganizations,
  estimatedLosses: event.estimatedLosses,
  
  // Metadata
  source: event.source,
  confidence: event.confidence,
  duration: event.duration,
  status: event.status,
  createdAt: datetime()
});

// ============================================================================
// PHASE 3: LOAD GEOPOLITICAL EVENTS (800 nodes)
// ============================================================================

// 3.1: GeopoliticalEvent - International Tensions (400 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.geopoliticalEvents.tensions AS event
CREATE (ge:GeopoliticalEvent {
  eventId: event.eventId,
  eventType: 'INTERNATIONAL_TENSION',
  timestamp: datetime(event.timestamp),
  
  // Event Details
  actors: event.actors,
  tensionLevel: event.tensionLevel,
  conflictType: event.conflictType,
  
  // Cyber Correlation
  cyberActivityCorrelation: event.cyberActivityCorrelation,
  observedActivityIncrease: event.observedActivityIncrease,
  
  // Predicted Impact
  predictedThreatActorActivity: event.predictedThreatActorActivity,
  targetSectors: event.targetSectors,
  targetRegions: event.targetRegions,
  
  // Timeline
  startDate: datetime(event.startDate),
  expectedDuration: event.expectedDuration,
  escalationRisk: event.escalationRisk,
  
  // Metadata
  source: event.source,
  confidence: event.confidence,
  createdAt: datetime()
});

// 3.2: GeopoliticalEvent - Sanctions (200 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.geopoliticalEvents.sanctions AS event
CREATE (ge:GeopoliticalEvent {
  eventId: event.eventId,
  eventType: 'SANCTION',
  timestamp: datetime(event.timestamp),
  
  imposingCountry: event.imposingCountry,
  targetCountry: event.targetCountry,
  sanctionType: event.sanctionType,
  
  affectedTechnologies: event.affectedTechnologies,
  affectedSectors: event.affectedSectors,
  supplyChainImpact: event.supplyChainImpact,
  
  retaliationRisk: event.retaliationRisk,
  predictedCyberResponse: event.predictedCyberResponse,
  
  source: event.source,
  confidence: event.confidence,
  createdAt: datetime()
});

// 3.3: GeopoliticalEvent - Conflicts (200 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.geopoliticalEvents.conflicts AS event
CREATE (ge:GeopoliticalEvent {
  eventId: event.eventId,
  eventType: 'CONFLICT',
  timestamp: datetime(event.timestamp),
  
  conflictName: event.conflictName,
  parties: event.parties,
  conflictType: event.conflictType,
  intensity: event.intensity,
  
  cyberWarfareActive: event.cyberWarfareActive,
  cyberOperations: event.cyberOperations,
  targetedInfrastructure: event.targetedInfrastructure,
  
  affectedRegions: event.affectedRegions,
  spilloverRisk: event.spilloverRisk,
  globalCyberActivityIncrease: event.globalCyberActivityIncrease,
  
  source: event.source,
  confidence: event.confidence,
  createdAt: datetime()
});

// ============================================================================
// PHASE 4: LOAD THREAT FEEDS (200 nodes)
// ============================================================================

// 4.1: ThreatFeed - Government Feeds (80 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.threatFeeds.government AS feed
CREATE (tf:ThreatFeed {
  feedId: feed.feedId,
  feedName: feed.feedName,
  feedType: 'GOVERNMENT',
  
  source: feed.source,
  updateFrequency: feed.updateFrequency,
  reliability: feed.reliability,
  coverage: feed.coverage,
  
  biasProfile: feed.biasProfile,
  geographicFocus: feed.geographicFocus,
  sectorFocus: feed.sectorFocus,
  
  format: feed.format,
  apiEndpoint: feed.apiEndpoint,
  authRequired: feed.authRequired,
  
  falsePositiveRate: feed.falsePositiveRate,
  timeliness: feed.timeliness,
  
  active: feed.active,
  createdAt: datetime()
});

// 4.2: ThreatFeed - Commercial Feeds (80 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.threatFeeds.commercial AS feed
CREATE (tf:ThreatFeed {
  feedId: feed.feedId,
  feedName: feed.feedName,
  feedType: 'COMMERCIAL',
  
  vendor: feed.vendor,
  updateFrequency: feed.updateFrequency,
  reliability: feed.reliability,
  coverage: feed.coverage,
  
  biasProfile: feed.biasProfile,
  specialization: feed.specialization,
  
  tier: feed.tier,
  costModel: feed.costModel,
  
  falsePositiveRate: feed.falsePositiveRate,
  timeliness: feed.timeliness,
  analysisDepth: feed.analysisDepth,
  
  active: feed.active,
  createdAt: datetime()
});

// 4.3: ThreatFeed - Open Source Intelligence (40 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.threatFeeds.osint AS feed
CREATE (tf:ThreatFeed {
  feedId: feed.feedId,
  feedName: feed.feedName,
  feedType: 'OSINT',
  
  sources: feed.sources,
  updateFrequency: feed.updateFrequency,
  reliability: feed.reliability,
  coverage: feed.coverage,
  
  communitySize: feed.communitySize,
  contributorQuality: feed.contributorQuality,
  
  falsePositiveRate: feed.falsePositiveRate,
  verificationLevel: feed.verificationLevel,
  
  active: feed.active,
  createdAt: datetime()
});

// ============================================================================
// PHASE 5: LOAD MEDIA EVENTS (2,000 nodes)
// ============================================================================

// 5.1: MediaEvent - Major Coverage (1,200 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.mediaEvents.majorCoverage AS event
CREATE (me:MediaEvent {
  eventId: event.eventId,
  eventType: 'MAJOR_COVERAGE',
  timestamp: datetime(event.timestamp),
  
  headline: event.headline,
  outlets: event.outlets,
  amplification: event.amplification,
  reach: event.reach,
  
  sentiment: event.sentiment,
  emotionalTone: event.emotionalTone,
  fearMongering: event.fearMongering,
  
  referencesEventId: event.referencesEventId,
  referencesCVE: event.referencesCVE,
  
  publicAwareness: event.publicAwareness,
  organizationalPressure: event.organizationalPressure,
  regulatoryPressure: event.regulatoryPressure,
  
  activatesBiases: event.activatesBiases,
  
  source: event.source,
  createdAt: datetime()
});

// 5.2: MediaEvent - Social Media Trends (800 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.mediaEvents.socialTrends AS event
CREATE (me:MediaEvent {
  eventId: event.eventId,
  eventType: 'SOCIAL_TREND',
  timestamp: datetime(event.timestamp),
  
  hashtag: event.hashtag,
  platform: event.platform,
  trendingScore: event.trendingScore,
  viralityIndex: event.viralityIndex,
  
  sentiment: event.sentiment,
  emotionalTone: event.emotionalTone,
  
  referencesEventId: event.referencesEventId,
  referencesCVE: event.referencesCVE,
  
  botPercentage: event.botPercentage,
  manipulationIndicators: event.manipulationIndicators,
  
  publicPerception: event.publicPerception,
  activatesBiases: event.activatesBiases,
  
  source: event.source,
  createdAt: datetime()
});

// ============================================================================
// PHASE 6: LOAD TECHNOLOGY SHIFTS (1,000 nodes)
// ============================================================================

// 6.1: TechnologyShift - Paradigm Changes (500 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.technologyShifts.paradigms AS shift
CREATE (ts:TechnologyShift {
  shiftId: shift.shiftId,
  shiftType: 'PARADIGM_CHANGE',
  timestamp: datetime(shift.timestamp),
  
  shiftName: shift.shiftName,
  paradigm: shift.paradigm,
  maturityLevel: shift.maturityLevel,
  
  impactLevel: shift.impactLevel,
  affectedSectors: shift.affectedSectors,
  adoptionRate: shift.adoptionRate,
  
  newVulnerabilityClasses: shift.newVulnerabilityClasses,
  securityChallenges: shift.securityChallenges,
  attackSurfaceChange: shift.attackSurfaceChange,
  
  requiredSkills: shift.requiredSkills,
  investmentRequired: shift.investmentRequired,
  organizationalResistance: shift.organizationalResistance,
  activatesBiases: shift.activatesBiases,
  
  source: shift.source,
  confidence: shift.confidence,
  createdAt: datetime()
});

// 6.2: TechnologyShift - Emerging Technologies (500 nodes)
CALL apoc.load.json('file:///data/level5_generated_data.json') YIELD value
UNWIND value.technologyShifts.emerging AS shift
CREATE (ts:TechnologyShift {
  shiftId: shift.shiftId,
  shiftType: 'EMERGING_TECHNOLOGY',
  timestamp: datetime(shift.timestamp),
  
  technologyName: shift.technologyName,
  category: shift.category,
  maturityLevel: shift.maturityLevel,
  
  adoptionStage: shift.adoptionStage,
  marketPenetration: shift.marketPenetration,
  growthRate: shift.growthRate,
  
  vulnerabilityResearch: shift.vulnerabilityResearch,
  knownWeaknesses: shift.knownWeaknesses,
  securityMaturity: shift.securityMaturity,
  
  affectedSectors: shift.affectedSectors,
  businessValueProposition: shift.businessValueProposition,
  competitiveAdvantage: shift.competitiveAdvantage,
  
  source: shift.source,
  confidence: shift.confidence,
  createdAt: datetime()
});

// ============================================================================
// PHASE 7: CREATE RELATIONSHIPS TO EXISTING NODES (50,000+ edges)
// ============================================================================

// 7.1: InformationEvent → CVE (REFERENCES) - ~10,000 relationships
MATCH (ie:InformationEvent)
WHERE ie.cveId IS NOT NULL
MATCH (cve:CVE {id: ie.cveId})
CREATE (ie)-[:REFERENCES {
  confidence: ie.confidence,
  severity: ie.severity,
  createdAt: datetime()
}]->(cve);

// 7.2: InformationEvent → CVE (MENTIONS from arrays) - ~5,000 relationships
MATCH (ie:InformationEvent)
WHERE ie.exploitedCVEs IS NOT NULL
UNWIND ie.exploitedCVEs AS cveId
MATCH (cve:CVE {id: cveId})
CREATE (ie)-[:MENTIONS {
  context: 'exploited',
  createdAt: datetime()
}]->(cve);

// 7.3: InformationEvent → Sector (AFFECTS_SECTOR) - ~2,000 relationships
MATCH (ie:InformationEvent)
WHERE ie.sector IS NOT NULL
MERGE (s:Sector {name: ie.sector})
CREATE (ie)-[:AFFECTS_SECTOR {
  impactLevel: ie.severity,
  predictedResponse: ie.predictedPatchVelocity,
  createdAt: datetime()
}]->(s);

// 7.4: InformationEvent → CognitiveBias (ACTIVATES_BIAS) - ~8,000 relationships
MATCH (ie:InformationEvent)
WHERE ie.activatesBiases IS NOT NULL
UNWIND ie.activatesBiases AS biasName
MATCH (cb:CognitiveBias {name: biasName})
CREATE (ie)-[:ACTIVATES_BIAS {
  mechanism: 'media_amplification',
  strength: ie.mediaAmplification,
  createdAt: datetime()
}]->(cb);

// 7.5: GeopoliticalEvent → Sector (TARGETS_SECTOR) - ~3,000 relationships
MATCH (ge:GeopoliticalEvent)
WHERE ge.targetSectors IS NOT NULL
UNWIND ge.targetSectors AS sectorName
MERGE (s:Sector {name: sectorName})
CREATE (ge)-[:TARGETS_SECTOR {
  targetingIntensity: ge.tensionLevel,
  createdAt: datetime()
}]->(s);

// 7.6: ThreatFeed → InformationEvent (PUBLISHES) - ~2,000 relationships
MATCH (tf:ThreatFeed)
MATCH (ie:InformationEvent)
WHERE ie.source = tf.feedId OR ie.source = tf.feedName
CREATE (tf)-[:PUBLISHES {
  publishedAt: ie.timestamp,
  reliability: tf.reliability,
  createdAt: datetime()
}]->(ie);

// 7.7: MediaEvent → InformationEvent (AMPLIFIES) - ~2,000 relationships
MATCH (me:MediaEvent)
WHERE me.referencesEventId IS NOT NULL
MATCH (ie:InformationEvent {eventId: me.referencesEventId})
CREATE (me)-[:AMPLIFIES {
  amplification: me.amplification,
  sentiment: me.sentiment,
  createdAt: datetime()
}]->(ie);

// 7.8: MediaEvent → CVE (DISCUSSES) - ~1,500 relationships
MATCH (me:MediaEvent)
WHERE me.referencesCVE IS NOT NULL
MATCH (cve:CVE {id: me.referencesCVE})
CREATE (me)-[:DISCUSSES {
  sentiment: me.sentiment,
  fearMongering: me.fearMongering,
  createdAt: datetime()
}]->(cve);

// 7.9: MediaEvent → CognitiveBias (ACTIVATES_BIAS) - ~5,000 relationships
MATCH (me:MediaEvent)
WHERE me.activatesBiases IS NOT NULL
UNWIND me.activatesBiases AS biasName
MATCH (cb:CognitiveBias {name: biasName})
CREATE (me)-[:ACTIVATES_BIAS {
  mechanism: 'media_framing',
  strength: me.amplification,
  createdAt: datetime()
}]->(cb);

// 7.10: TechnologyShift → Sector (AFFECTS_SECTOR) - ~4,000 relationships
MATCH (ts:TechnologyShift)
WHERE ts.affectedSectors IS NOT NULL
UNWIND ts.affectedSectors AS sectorName
MERGE (s:Sector {name: sectorName})
CREATE (ts)-[:AFFECTS_SECTOR {
  impactLevel: ts.impactLevel,
  adoptionRate: ts.adoptionRate,
  createdAt: datetime()
}]->(s);

// 7.11: TechnologyShift → CognitiveBias (TRIGGERS_BIAS) - ~2,500 relationships
MATCH (ts:TechnologyShift)
WHERE ts.activatesBiases IS NOT NULL
UNWIND ts.activatesBiases AS biasName
MATCH (cb:CognitiveBias {name: biasName})
CREATE (ts)-[:TRIGGERS_BIAS {
  mechanism: 'change_resistance',
  strength: ts.organizationalResistance,
  createdAt: datetime()
}]->(cb);

// 7.12: Cross-Level Integration - Event → Decision Chain (~5,000 relationships)
MATCH (ie:InformationEvent)-[:ACTIVATES_BIAS]->(cb:CognitiveBias)
MATCH (cb)-[:INFLUENCES]->(d:Decision)
CREATE (ie)-[:INFLUENCES_DECISION {
  mechanism: 'bias_activation',
  mediaAmplification: ie.mediaAmplification,
  createdAt: datetime()
}]->(d);

// ============================================================================
// PHASE 8: VERIFICATION & STATISTICS
// ============================================================================

// 8.1: Count all Level 5 nodes
MATCH (n)
WHERE any(label IN labels(n) WHERE
  label IN ['InformationEvent', 'GeopoliticalEvent', 'ThreatFeed',
            'MediaEvent', 'TechnologyShift'])
RETURN
  labels(n)[0] AS node_type,
  count(n) AS node_count
ORDER BY node_count DESC;

// 8.2: Count all Level 5 relationships
MATCH ()-[r]->()
WHERE type(r) IN [
  'REFERENCES', 'MENTIONS', 'DESCRIBES', 'AFFECTS_SECTOR',
  'AFFECTS_ORGANIZATION', 'ATTRIBUTED_TO', 'USES_TECHNIQUE',
  'TARGETS_EQUIPMENT', 'ACTIVATES_BIAS', 'INCREASES_ACTIVITY',
  'TARGETS_SECTOR', 'PUBLISHES', 'AMPLIFIES', 'DISCUSSES',
  'TRIGGERS_BIAS', 'INFLUENCES_DECISION', 'AFFECTS_PSYCHOLOGY',
  'CREATES_PRESSURE', 'INTRODUCES_VULNERABILITY_CLASS',
  'CASCADES_TO', 'BIASES_INTERPRETATION'
]
RETURN
  type(r) AS relationship_type,
  count(r) AS relationship_count
ORDER BY relationship_count DESC;

// 8.3: Cross-level integration verification
MATCH (ie:InformationEvent)-[r]->(cve:CVE)
RETURN
  'InformationEvent_to_CVE' AS connection_type,
  count(DISTINCT ie) AS information_events,
  count(DISTINCT cve) AS cves_referenced,
  count(r) AS total_links;

// 8.4: Final deployment summary
MATCH (ie:InformationEvent)
WITH count(ie) AS ie_count
MATCH (ge:GeopoliticalEvent)
WITH ie_count, count(ge) AS ge_count
MATCH (tf:ThreatFeed)
WITH ie_count, ge_count, count(tf) AS tf_count
MATCH (me:MediaEvent)
WITH ie_count, ge_count, tf_count, count(me) AS me_count
MATCH (ts:TechnologyShift)
WITH ie_count, ge_count, tf_count, me_count, count(ts) AS ts_count
MATCH ()-[r]->()
WHERE type(r) IN [
  'REFERENCES', 'MENTIONS', 'AFFECTS_SECTOR', 'ACTIVATES_BIAS',
  'TARGETS_SECTOR', 'PUBLISHES', 'AMPLIFIES', 'DISCUSSES',
  'TRIGGERS_BIAS', 'INFLUENCES_DECISION'
]
RETURN
  'LEVEL 5 DEPLOYMENT SUMMARY' AS status,
  ie_count AS InformationEvents,
  ge_count AS GeopoliticalEvents,
  tf_count AS ThreatFeeds,
  me_count AS MediaEvents,
  ts_count AS TechnologyShifts,
  (ie_count + ge_count + tf_count + me_count + ts_count) AS total_nodes,
  count(r) AS total_relationships,
  datetime() AS deployment_completed;

// ============================================================================
// END OF DEPLOYMENT SCRIPT
// ============================================================================
