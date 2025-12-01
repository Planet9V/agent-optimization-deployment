// ============================================================================
// LEVEL 6 DEPLOYMENT SCRIPT - Predictive Analytics & ML Predictions
// ============================================================================
// Created: 2025-11-23
// Purpose: Deploy 111,000 Level 6 nodes with 636,000+ relationships
// Integration: Links to 541K existing nodes (Equipment, CVE, MITRE, Events)
// Data Source: level6_generated_data.json (TO BE CREATED BY AGENT 6)
//
// DEPLOYMENT PHASES:
//   Phase 1: Constraints & Indexes (20 constraints, 25+ indexes)
//   Phase 2: HistoricalPattern (100,000 nodes)
//   Phase 3: FutureThreat (10,000 nodes)
//   Phase 4: WhatIfScenario (1,000 nodes)
//   Phase 5: SecurityControl (200 nodes - if not exists)
//   Phase 6: Cross-level relationships (636,000+ edges)
//   Phase 7: Integration with Levels 0-5 (541K nodes)
//   Phase 8: Verification queries
//
// MCKNENNEY QUESTIONS ENABLED:
//   Question 7: "What will happen?" → FutureThreat predictions
//   Question 8: "What should we do?" → WhatIfScenario + SecurityControl
// ============================================================================

// ============================================================================
// PHASE 1: CONSTRAINTS AND INDEXES
// ============================================================================

// 1.1: HistoricalPattern Constraints
CREATE CONSTRAINT historical_pattern_id IF NOT EXISTS
FOR (hp:HistoricalPattern) REQUIRE hp.id IS UNIQUE;

CREATE CONSTRAINT historical_pattern_patternid IF NOT EXISTS
FOR (hp:HistoricalPattern) REQUIRE hp.patternId IS UNIQUE;

CREATE CONSTRAINT historical_pattern_id_not_null IF NOT EXISTS
FOR (hp:HistoricalPattern) REQUIRE hp.id IS NOT NULL;

// 1.2: FutureThreat Constraints
CREATE CONSTRAINT future_threat_id IF NOT EXISTS
FOR (ft:FutureThreat) REQUIRE ft.id IS UNIQUE;

CREATE CONSTRAINT future_threat_predictionid IF NOT EXISTS
FOR (ft:FutureThreat) REQUIRE ft.predictionId IS UNIQUE;

CREATE CONSTRAINT future_threat_id_not_null IF NOT EXISTS
FOR (ft:FutureThreat) REQUIRE ft.id IS NOT NULL;

// 1.3: WhatIfScenario Constraints
CREATE CONSTRAINT whatif_scenario_id IF NOT EXISTS
FOR (ws:WhatIfScenario) REQUIRE ws.id IS UNIQUE;

CREATE CONSTRAINT whatif_scenario_scenarioid IF NOT EXISTS
FOR (ws:WhatIfScenario) REQUIRE ws.scenarioId IS UNIQUE;

CREATE CONSTRAINT whatif_scenario_id_not_null IF NOT EXISTS
FOR (ws:WhatIfScenario) REQUIRE ws.id IS NOT NULL;

// 1.4: SecurityControl Constraints
CREATE CONSTRAINT security_control_id IF NOT EXISTS
FOR (sc:SecurityControl) REQUIRE sc.id IS UNIQUE;

CREATE CONSTRAINT security_control_controlid IF NOT EXISTS
FOR (sc:SecurityControl) REQUIRE sc.controlId IS UNIQUE;

CREATE CONSTRAINT security_control_id_not_null IF NOT EXISTS
FOR (sc:SecurityControl) REQUIRE sc.id IS NOT NULL;

// 1.5: Data Integrity Constraints
CREATE CONSTRAINT future_threat_probability_bounds IF NOT EXISTS
FOR (ft:FutureThreat) REQUIRE ft.probability >= 0.0 AND ft.probability <= 1.0;

CREATE CONSTRAINT historical_pattern_confidence_bounds IF NOT EXISTS
FOR (hp:HistoricalPattern) REQUIRE hp.confidence >= 0.0 AND hp.confidence <= 1.0;

CREATE CONSTRAINT security_control_effectiveness_bounds IF NOT EXISTS
FOR (sc:SecurityControl) REQUIRE sc.effectiveness >= 0.0 AND sc.effectiveness <= 1.0;

// 1.6: Performance Indexes - HistoricalPattern
CREATE INDEX historical_pattern_sector IF NOT EXISTS
FOR (hp:HistoricalPattern) ON (hp.sector);

CREATE INDEX historical_pattern_type IF NOT EXISTS
FOR (hp:HistoricalPattern) ON (hp.patternType);

CREATE INDEX historical_pattern_confidence IF NOT EXISTS
FOR (hp:HistoricalPattern) ON (hp.confidence);

CREATE INDEX historical_pattern_extracted IF NOT EXISTS
FOR (hp:HistoricalPattern) ON (hp.extractedAt);

CREATE INDEX historical_pattern_status IF NOT EXISTS
FOR (hp:HistoricalPattern) ON (hp.status);

// 1.7: Performance Indexes - FutureThreat
CREATE INDEX future_threat_probability IF NOT EXISTS
FOR (ft:FutureThreat) ON (ft.probability);

CREATE INDEX future_threat_timeframe IF NOT EXISTS
FOR (ft:FutureThreat) ON (ft.timeframe);

CREATE INDEX future_threat_impact IF NOT EXISTS
FOR (ft:FutureThreat) ON (ft.estimatedImpact);

CREATE INDEX future_threat_status IF NOT EXISTS
FOR (ft:FutureThreat) ON (ft.predictionStatus);

CREATE INDEX future_threat_generated IF NOT EXISTS
FOR (ft:FutureThreat) ON (ft.generatedAt);

CREATE INDEX future_threat_priority IF NOT EXISTS
FOR (ft:FutureThreat) ON (ft.priority);

// 1.8: Performance Indexes - WhatIfScenario
CREATE INDEX whatif_scenario_threatid IF NOT EXISTS
FOR (ws:WhatIfScenario) ON (ws.threatId);

CREATE INDEX whatif_scenario_roi IF NOT EXISTS
FOR (ws:WhatIfScenario) ON (ws.roi);

CREATE INDEX whatif_scenario_action IF NOT EXISTS
FOR (ws:WhatIfScenario) ON (ws.action);

CREATE INDEX whatif_scenario_recommended IF NOT EXISTS
FOR (ws:WhatIfScenario) ON (ws.recommended);

CREATE INDEX whatif_scenario_status IF NOT EXISTS
FOR (ws:WhatIfScenario) ON (ws.implementationStatus);

// 1.9: Performance Indexes - SecurityControl
CREATE INDEX security_control_framework IF NOT EXISTS
FOR (sc:SecurityControl) ON (sc.framework);

CREATE INDEX security_control_effectiveness IF NOT EXISTS
FOR (sc:SecurityControl) ON (sc.effectiveness);

CREATE INDEX security_control_cost IF NOT EXISTS
FOR (sc:SecurityControl) ON (sc.totalCost);

CREATE INDEX security_control_status IF NOT EXISTS
FOR (sc:SecurityControl) ON (sc.deploymentStatus);

CREATE INDEX security_control_type IF NOT EXISTS
FOR (sc:SecurityControl) ON (sc.controlType);

// 1.10: Composite Indexes for Common Cross-Level Queries
CREATE INDEX historical_pattern_query_composite IF NOT EXISTS
FOR (hp:HistoricalPattern) ON (hp.sector, hp.patternType, hp.confidence);

CREATE INDEX future_threat_priority_composite IF NOT EXISTS
FOR (ft:FutureThreat) ON (ft.probability, ft.estimatedImpact, ft.predictionStatus);

CREATE INDEX whatif_scenario_decision_composite IF NOT EXISTS
FOR (ws:WhatIfScenario) ON (ws.recommended, ws.roi, ws.priority);

CREATE INDEX security_control_selection_composite IF NOT EXISTS
FOR (sc:SecurityControl) ON (sc.effectiveness, sc.totalCost, sc.deploymentStatus);

// 1.11: Full-Text Search Indexes
CALL db.index.fulltext.createNodeIndex(
  'threatContentSearch',
  ['FutureThreat'],
  ['predictedEvent', 'threatType', 'notes']
);

CALL db.index.fulltext.createNodeIndex(
  'controlSearch',
  ['SecurityControl'],
  ['controlName', 'description', 'implementation', 'framework']
);

CALL db.index.fulltext.createNodeIndex(
  'patternSearch',
  ['HistoricalPattern'],
  ['behavior', 'sector', 'notes']
);

// ============================================================================
// PHASE 2: LOAD HISTORICAL PATTERNS (100,000 nodes)
// ============================================================================
// Pattern Categories:
//   - Patch Velocity: 16,000 nodes
//   - Incident Response: 8,000 nodes
//   - Budget Cycles: 4,800 nodes
//   - Technology Adoption: 6,400 nodes
//   - Breach Sequences: 12,000 nodes
//   - Cognitive Bias Patterns: 9,600 nodes
//   - Geopolitical Cyber Correlation: 8,000 nodes
//   - Vulnerability Exploitation: 32,000 nodes
//   - Sector Interdependency: 3,200 nodes
// ============================================================================

// 2.1: HistoricalPattern - Patch Velocity (16,000 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.patchVelocity AS pattern
CREATE (hp:HistoricalPattern:PatchVelocity:Level6 {
  // Primary Identifiers
  id: pattern.id,
  patternId: pattern.patternId,

  // Pattern Classification
  patternType: 'PATCH_VELOCITY',
  patternCategory: 'BEHAVIORAL',
  behavior: pattern.behavior,

  // Scope & Context
  sector: pattern.sector,
  organizationType: pattern.organizationType,
  assetSize: pattern.assetSize,
  geographicRegion: pattern.geographicRegion,

  // Statistical Metrics
  avgDelay: pattern.avgDelay,
  medianDelay: pattern.medianDelay,
  stdDev: pattern.stdDev,
  minObserved: pattern.minObserved,
  maxObserved: pattern.maxObserved,
  percentile25: pattern.percentile25,
  percentile75: pattern.percentile75,

  // Confidence & Validation
  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  significanceLevel: pattern.significanceLevel,
  validationMethod: pattern.validationMethod,

  // Temporal Patterns
  seasonalPattern: pattern.seasonalPattern,
  seasonality: pattern.seasonality,
  peakMonths: pattern.peakMonths,
  trendDirection: pattern.trendDirection,
  trendSlope: pattern.trendSlope,

  // Predictive Power
  predictiveAccuracy: pattern.predictiveAccuracy,
  falsePositiveRate: pattern.falsePositiveRate,
  falseNegativeRate: pattern.falseNegativeRate,
  applicabilityScore: pattern.applicabilityScore,

  // Evidence & Sources
  sources: pattern.sources,
  incidents: pattern.incidents,
  cveIds: pattern.cveIds,
  evidenceQuality: pattern.evidenceQuality,

  // Metadata
  extractedAt: datetime(pattern.extractedAt),
  lastValidated: datetime(pattern.lastValidated),
  validUntil: datetime(pattern.validUntil),
  extractionMethod: pattern.extractionMethod,
  status: pattern.status,
  tags: pattern.tags,
  notes: pattern.notes,
  createdAt: datetime()
});

// 2.2: HistoricalPattern - Incident Response (8,000 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.incidentResponse AS pattern
CREATE (hp:HistoricalPattern:IncidentResponse:Level6 {
  id: pattern.id,
  patternId: pattern.patternId,
  patternType: 'INCIDENT_RESPONSE',
  patternCategory: 'OPERATIONAL',
  behavior: pattern.behavior,
  sector: pattern.sector,

  // Response Time Metrics
  avgDetectionTime: pattern.avgDetectionTime,
  avgContainmentTime: pattern.avgContainmentTime,
  avgRecoveryTime: pattern.avgRecoveryTime,
  totalResponseTime: pattern.totalResponseTime,

  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  predictiveAccuracy: pattern.predictiveAccuracy,

  extractedAt: datetime(pattern.extractedAt),
  validUntil: datetime(pattern.validUntil),
  status: pattern.status,
  createdAt: datetime()
});

// 2.3: HistoricalPattern - Budget Cycles (4,800 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.budgetCycles AS pattern
CREATE (hp:HistoricalPattern:BudgetCycle:Level6 {
  id: pattern.id,
  patternId: pattern.patternId,
  patternType: 'BUDGET_CYCLE',
  patternCategory: 'ECONOMIC',
  behavior: pattern.behavior,
  sector: pattern.sector,

  // Budget Metrics
  avgQ1Spending: pattern.avgQ1Spending,
  avgQ2Spending: pattern.avgQ2Spending,
  avgQ3Spending: pattern.avgQ3Spending,
  avgQ4Spending: pattern.avgQ4Spending,
  emergencyBudgetAvg: pattern.emergencyBudgetAvg,
  roiCycle: pattern.roiCycle,

  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  seasonalPattern: true,
  seasonality: 'QUARTERLY',

  extractedAt: datetime(pattern.extractedAt),
  validUntil: datetime(pattern.validUntil),
  status: pattern.status,
  createdAt: datetime()
});

// 2.4: HistoricalPattern - Technology Adoption (6,400 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.technologyAdoption AS pattern
CREATE (hp:HistoricalPattern:TechnologyAdoption:Level6 {
  id: pattern.id,
  patternId: pattern.patternId,
  patternType: 'TECHNOLOGY_ADOPTION',
  patternCategory: 'BEHAVIORAL',
  behavior: pattern.behavior,
  sector: pattern.sector,

  // Adoption Metrics
  avgAdoptionRate: pattern.avgAdoptionRate,
  avgRetirementAge: pattern.avgRetirementAge,
  avgUpgradeFrequency: pattern.avgUpgradeFrequency,
  laggardPercentage: pattern.laggardPercentage,

  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  predictiveAccuracy: pattern.predictiveAccuracy,

  extractedAt: datetime(pattern.extractedAt),
  validUntil: datetime(pattern.validUntil),
  status: pattern.status,
  createdAt: datetime()
});

// 2.5: HistoricalPattern - Breach Sequences (12,000 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.breachSequences AS pattern
CREATE (hp:HistoricalPattern:BreachSequence:Level6 {
  id: pattern.id,
  patternId: pattern.patternId,
  patternType: 'BREACH_SEQUENCE',
  patternCategory: 'TECHNICAL',
  behavior: pattern.behavior,
  sector: pattern.sector,

  // Attack Timeline Metrics
  avgInitialAccessTime: pattern.avgInitialAccessTime,
  avgLateralMovementTime: pattern.avgLateralMovementTime,
  avgExfiltrationTime: pattern.avgExfiltrationTime,
  totalDwellTime: pattern.totalDwellTime,

  // Attack Vector Details
  commonInitialVectors: pattern.commonInitialVectors,
  commonTechniques: pattern.commonTechniques,
  commonTargets: pattern.commonTargets,

  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  predictiveAccuracy: pattern.predictiveAccuracy,

  extractedAt: datetime(pattern.extractedAt),
  validUntil: datetime(pattern.validUntil),
  status: pattern.status,
  createdAt: datetime()
});

// 2.6: HistoricalPattern - Cognitive Bias Patterns (9,600 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.cognitiveBias AS pattern
CREATE (hp:HistoricalPattern:CognitiveBias:Level6 {
  id: pattern.id,
  patternId: pattern.patternId,
  patternType: 'COGNITIVE_BIAS',
  patternCategory: 'PSYCHOLOGICAL',
  behavior: pattern.behavior,
  sector: pattern.sector,

  // Bias Activation Metrics
  biasType: pattern.biasType,
  activationThreshold: pattern.activationThreshold,
  avgDecisionDelay: pattern.avgDecisionDelay,
  mitigationSuccessRate: pattern.mitigationSuccessRate,

  // Impact on Security Decisions
  affectedDecisions: pattern.affectedDecisions,
  costOfDelay: pattern.costOfDelay,

  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  predictiveAccuracy: pattern.predictiveAccuracy,

  extractedAt: datetime(pattern.extractedAt),
  validUntil: datetime(pattern.validUntil),
  status: pattern.status,
  createdAt: datetime()
});

// 2.7: HistoricalPattern - Geopolitical Cyber Correlation (8,000 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.geopoliticalCyber AS pattern
CREATE (hp:HistoricalPattern:GeopoliticalCyber:Level6 {
  id: pattern.id,
  patternId: pattern.patternId,
  patternType: 'GEOPOLITICAL_CYBER_CORRELATION',
  patternCategory: 'GEOPOLITICAL',
  behavior: pattern.behavior,

  // Correlation Metrics
  geopoliticalEventType: pattern.geopoliticalEventType,
  avgLagTime: pattern.avgLagTime,
  avgActivityIncrease: pattern.avgActivityIncrease,
  targetShiftPattern: pattern.targetShiftPattern,

  // Affected Regions/Sectors
  affectedRegions: pattern.affectedRegions,
  affectedSectors: pattern.affectedSectors,

  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  predictiveAccuracy: pattern.predictiveAccuracy,

  extractedAt: datetime(pattern.extractedAt),
  validUntil: datetime(pattern.validUntil),
  status: pattern.status,
  createdAt: datetime()
});

// 2.8: HistoricalPattern - Vulnerability Exploitation (32,000 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.vulnerabilityExploitation AS pattern
CREATE (hp:HistoricalPattern:VulnerabilityExploitation:Level6 {
  id: pattern.id,
  patternId: pattern.patternId,
  patternType: 'VULNERABILITY_EXPLOITATION',
  patternCategory: 'TECHNICAL',
  behavior: pattern.behavior,

  // Exploitation Timeline Metrics
  avgDisclosureToExploit: pattern.avgDisclosureToExploit,
  avgExploitToWeaponization: pattern.avgExploitToWeaponization,
  avgWeaponizationToWide: pattern.avgWeaponizationToWide,

  // CVE Characteristics
  cvssScoreRange: pattern.cvssScoreRange,
  epssAccuracyScore: pattern.epssAccuracyScore,
  patchEffectiveness: pattern.patchEffectiveness,

  // Exploitation Context
  commonVulnTypes: pattern.commonVulnTypes,
  targetedProducts: pattern.targetedProducts,

  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  predictiveAccuracy: pattern.predictiveAccuracy,

  extractedAt: datetime(pattern.extractedAt),
  validUntil: datetime(pattern.validUntil),
  status: pattern.status,
  createdAt: datetime()
});

// 2.9: HistoricalPattern - Sector Interdependency (3,200 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.historicalPatterns.sectorInterdependency AS pattern
CREATE (hp:HistoricalPattern:SectorInterdependency:Level6 {
  id: pattern.id,
  patternId: pattern.patternId,
  patternType: 'SECTOR_INTERDEPENDENCY',
  patternCategory: 'SYSTEMIC',
  behavior: pattern.behavior,

  // Cascade Metrics
  primarySector: pattern.primarySector,
  dependentSectors: pattern.dependentSectors,
  avgCascadeDelay: pattern.avgCascadeDelay,
  impactMultiplier: pattern.impactMultiplier,
  recoverySequence: pattern.recoverySequence,

  // Interdependency Strength
  dependencyStrength: pattern.dependencyStrength,
  bidirectionalDependency: pattern.bidirectionalDependency,

  confidence: pattern.confidence,
  sampleSize: pattern.sampleSize,
  predictiveAccuracy: pattern.predictiveAccuracy,

  extractedAt: datetime(pattern.extractedAt),
  validUntil: datetime(pattern.validUntil),
  status: pattern.status,
  createdAt: datetime()
});

// ============================================================================
// PHASE 3: LOAD FUTURE THREATS (10,000 nodes)
// ============================================================================
// Threat Categories:
//   - Critical CVE Predictions: 4,000 nodes
//   - Targeted Attack Campaigns: 2,500 nodes
//   - Supply Chain Risks: 1,500 nodes
//   - Zero-Day Predictions: 1,000 nodes
//   - Ransomware Evolution: 1,000 nodes
// ============================================================================

// 3.1: FutureThreat - Critical CVE Predictions (4,000 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.futureThreats.criticalCve AS threat
CREATE (ft:FutureThreat:CriticalCVE:Level6 {
  // Primary Identifiers
  id: threat.id,
  predictionId: threat.predictionId,

  // Threat Classification
  predictedEvent: 'CRITICAL_CVE',
  threatType: threat.threatType,
  threatCategory: 'TECHNICAL',
  attackVector: threat.attackVector,

  // Probability & Confidence
  probability: threat.probability,
  confidence: threat.confidence,
  uncertaintyBounds: threat.uncertaintyBounds,

  // Timeframe
  timeframe: threat.timeframe,
  predictionHorizon: threat.predictionHorizon,
  earliestDate: datetime(threat.earliestDate),
  likelyDate: datetime(threat.likelyDate),
  latestDate: datetime(threat.latestDate),

  // Impact Assessment
  estimatedImpact: threat.estimatedImpact,
  impactDistribution: threat.impactDistribution,
  affectedEquipment: threat.affectedEquipment,
  affectedOrganizations: threat.affectedOrganizations,
  affectedSectors: threat.affectedSectors,

  // Impact Breakdown
  downtimeCost: threat.downtimeCost,
  recoveryCost: threat.recoveryCost,
  reputationCost: threat.reputationCost,
  regulatoryFines: threat.regulatoryFines,
  investigationCost: threat.investigationCost,
  legalCost: threat.legalCost,

  // Vulnerability Details
  cveId: threat.cveId,
  relatedCveIds: threat.relatedCveIds,
  cvssScore: threat.cvssScore,
  epssScore: threat.epssScore,
  exploitAvailable: threat.exploitAvailable,
  weaponizationTimeline: threat.weaponizationTimeline,

  // Attacker Profile
  likelyActors: threat.likelyActors,
  actorMotivation: threat.actorMotivation,
  actorCapability: threat.actorCapability,
  targetingConfidence: threat.targetingConfidence,

  // Evidence Chain (5-dimensional)
  technicalEvidence: threat.technicalEvidence,
  behavioralEvidence: threat.behavioralEvidence,
  geopoliticalEvidence: threat.geopoliticalEvidence,
  attackerEvidence: threat.attackerEvidence,
  sectorEvidence: threat.sectorEvidence,
  evidenceStrength: threat.evidenceStrength,

  // Model Metadata
  modelName: threat.modelName,
  modelVersion: threat.modelVersion,
  trainingAccuracy: threat.trainingAccuracy,
  validationAccuracy: threat.validationAccuracy,
  featureImportance: threat.featureImportance,

  // Prediction Provenance
  basedOnPatterns: threat.basedOnPatterns,
  basedOnEvents: threat.basedOnEvents,
  basedOnIntelligence: threat.basedOnIntelligence,
  generatedAt: datetime(threat.generatedAt),
  expiresAt: datetime(threat.expiresAt),

  // Validation & Updates
  predictionStatus: threat.predictionStatus,
  priority: threat.priority,
  tags: threat.tags,
  notes: threat.notes,
  createdAt: datetime()
});

// 3.2: FutureThreat - Targeted Attack Campaigns (2,500 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.futureThreats.targetedCampaigns AS threat
CREATE (ft:FutureThreat:TargetedCampaign:Level6 {
  id: threat.id,
  predictionId: threat.predictionId,
  predictedEvent: 'TARGETED_ATTACK',
  threatType: 'APT_CAMPAIGN',

  probability: threat.probability,
  confidence: threat.confidence,
  timeframe: threat.timeframe,
  likelyDate: datetime(threat.likelyDate),

  estimatedImpact: threat.estimatedImpact,
  affectedSectors: threat.affectedSectors,

  likelyActors: threat.likelyActors,
  actorMotivation: threat.actorMotivation,
  actorCapability: threat.actorCapability,

  campaignName: threat.campaignName,
  targetedOrganizations: threat.targetedOrganizations,
  techniques: threat.techniques,

  modelName: threat.modelName,
  generatedAt: datetime(threat.generatedAt),
  predictionStatus: threat.predictionStatus,
  priority: threat.priority,
  createdAt: datetime()
});

// 3.3: FutureThreat - Supply Chain Risks (1,500 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.futureThreats.supplyChain AS threat
CREATE (ft:FutureThreat:SupplyChain:Level6 {
  id: threat.id,
  predictionId: threat.predictionId,
  predictedEvent: 'SUPPLY_CHAIN',
  threatType: 'SUPPLY_CHAIN_COMPROMISE',

  probability: threat.probability,
  confidence: threat.confidence,
  timeframe: threat.timeframe,
  likelyDate: datetime(threat.likelyDate),

  estimatedImpact: threat.estimatedImpact,
  affectedSectors: threat.affectedSectors,

  targetedVendor: threat.targetedVendor,
  affectedProducts: threat.affectedProducts,
  cascadeRisk: threat.cascadeRisk,

  modelName: threat.modelName,
  generatedAt: datetime(threat.generatedAt),
  predictionStatus: threat.predictionStatus,
  priority: threat.priority,
  createdAt: datetime()
});

// 3.4: FutureThreat - Zero-Day Predictions (1,000 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.futureThreats.zeroDay AS threat
CREATE (ft:FutureThreat:ZeroDay:Level6 {
  id: threat.id,
  predictionId: threat.predictionId,
  predictedEvent: 'ZERO_DAY',
  threatType: 'ZERO_DAY_EXPLOIT',

  probability: threat.probability,
  confidence: threat.confidence,
  timeframe: threat.timeframe,
  likelyDate: datetime(threat.likelyDate),

  estimatedImpact: threat.estimatedImpact,
  affectedSectors: threat.affectedSectors,

  targetedProduct: threat.targetedProduct,
  vulnerabilityClass: threat.vulnerabilityClass,
  exploitComplexity: threat.exploitComplexity,

  modelName: threat.modelName,
  generatedAt: datetime(threat.generatedAt),
  predictionStatus: threat.predictionStatus,
  priority: threat.priority,
  createdAt: datetime()
});

// 3.5: FutureThreat - Ransomware Evolution (1,000 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.futureThreats.ransomware AS threat
CREATE (ft:FutureThreat:Ransomware:Level6 {
  id: threat.id,
  predictionId: threat.predictionId,
  predictedEvent: 'RANSOMWARE',
  threatType: 'RANSOMWARE_CAMPAIGN',

  probability: threat.probability,
  confidence: threat.confidence,
  timeframe: threat.timeframe,
  likelyDate: datetime(threat.likelyDate),

  estimatedImpact: threat.estimatedImpact,
  affectedSectors: threat.affectedSectors,

  ransomwareFamily: threat.ransomwareFamily,
  ransomDemandAvg: threat.ransomDemandAvg,
  paymentProbability: threat.paymentProbability,

  modelName: threat.modelName,
  generatedAt: datetime(threat.generatedAt),
  predictionStatus: threat.predictionStatus,
  priority: threat.priority,
  createdAt: datetime()
});

// ============================================================================
// PHASE 4: LOAD WHAT-IF SCENARIOS (1,000 nodes)
// ============================================================================
// Scenario Types:
//   - Proactive Patching: 400 nodes
//   - Defense in Depth: 300 nodes
//   - Risk Acceptance: 150 nodes
//   - Insurance Transfer: 100 nodes
//   - Reactive Response: 50 nodes
// ============================================================================

// 4.1: WhatIfScenario - Proactive Patching (400 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.whatIfScenarios.proactivePatching AS scenario
CREATE (ws:WhatIfScenario:ProactivePatch:Level6 {
  // Primary Identifiers
  id: scenario.id,
  scenarioId: scenario.scenarioId,
  threatId: scenario.threatId,

  // Scenario Classification
  action: 'PROACTIVE_PATCH',
  actionType: 'PREVENTIVE',
  actionCategory: 'TECHNICAL',
  interventionTiming: 'IMMEDIATE',

  // Cost Analysis
  interventionCost: scenario.interventionCost,
  costBreakdown: scenario.costBreakdown,
  laborCost: scenario.laborCost,
  toolCost: scenario.toolCost,
  maintenanceCost: scenario.maintenanceCost,

  // Risk Reduction
  baselineBreachProb: scenario.baselineBreachProb,
  reducedBreachProb: scenario.reducedBreachProb,
  riskReduction: scenario.riskReduction,
  breachProbMultiplier: scenario.breachProbMultiplier,

  // Impact Assessment
  baselineImpact: scenario.baselineImpact,
  residualImpact: scenario.residualImpact,
  expectedLoss: scenario.expectedLoss,
  preventedLoss: scenario.preventedLoss,
  netBenefit: scenario.netBenefit,

  // ROI Calculation
  roi: scenario.roi,
  roiPercentage: scenario.roiPercentage,
  paybackPeriod: scenario.paybackPeriod,
  npv: scenario.npv,
  irr: scenario.irr,

  // Effectiveness Metrics
  effectiveness: scenario.effectiveness,
  implementationDifficulty: scenario.implementationDifficulty,
  timeToImplement: scenario.timeToImplement,
  organizationalImpact: scenario.organizationalImpact,

  // Security Controls Applied
  controls: scenario.controls,
  controlCount: scenario.controlCount,
  controlCategories: scenario.controlCategories,
  frameworks: scenario.frameworks,

  // Risk Assessment
  residualRisk: scenario.residualRisk,
  riskAcceptable: scenario.riskAcceptable,

  // Comparison Metrics
  betterThanBaseline: scenario.betterThanBaseline,
  betterThanReactive: scenario.betterThanReactive,
  optimalForRoi: scenario.optimalForRoi,
  optimalForRisk: scenario.optimalForRisk,

  // Recommendation
  recommended: scenario.recommended,
  recommendationReason: scenario.recommendationReason,
  priority: scenario.priority,
  urgency: scenario.urgency,

  // Validation & Tracking
  simulationRuns: scenario.simulationRuns,
  validationMethod: scenario.validationMethod,
  implementationStatus: scenario.implementationStatus,

  createdAt: datetime(),
  expiresAt: datetime(scenario.expiresAt),
  notes: scenario.notes
});

// 4.2: WhatIfScenario - Defense in Depth (300 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.whatIfScenarios.defenseInDepth AS scenario
CREATE (ws:WhatIfScenario:DefenseInDepth:Level6 {
  id: scenario.id,
  scenarioId: scenario.scenarioId,
  threatId: scenario.threatId,
  action: 'DEFENSE_IN_DEPTH',
  actionType: 'PREVENTIVE',

  interventionCost: scenario.interventionCost,
  baselineBreachProb: scenario.baselineBreachProb,
  reducedBreachProb: scenario.reducedBreachProb,
  riskReduction: scenario.riskReduction,

  baselineImpact: scenario.baselineImpact,
  preventedLoss: scenario.preventedLoss,
  netBenefit: scenario.netBenefit,
  roi: scenario.roi,

  controls: scenario.controls,
  controlCount: scenario.controlCount,

  recommended: scenario.recommended,
  priority: scenario.priority,
  implementationStatus: scenario.implementationStatus,
  createdAt: datetime()
});

// 4.3: WhatIfScenario - Risk Acceptance (150 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.whatIfScenarios.riskAcceptance AS scenario
CREATE (ws:WhatIfScenario:RiskAcceptance:Level6 {
  id: scenario.id,
  scenarioId: scenario.scenarioId,
  threatId: scenario.threatId,
  action: 'ACCEPT_RISK',
  actionType: 'RISK_TRANSFER',

  interventionCost: 0.0,
  baselineBreachProb: scenario.baselineBreachProb,
  reducedBreachProb: scenario.baselineBreachProb,
  riskReduction: 0.0,

  baselineImpact: scenario.baselineImpact,
  expectedLoss: scenario.expectedLoss,

  residualRisk: scenario.residualRisk,
  riskAcceptable: scenario.riskAcceptable,

  recommended: scenario.recommended,
  recommendationReason: scenario.recommendationReason,
  priority: scenario.priority,
  implementationStatus: scenario.implementationStatus,
  createdAt: datetime()
});

// 4.4: WhatIfScenario - Insurance Transfer (100 nodes)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.whatIfScenarios.insuranceTransfer AS scenario
CREATE (ws:WhatIfScenario:InsuranceTransfer:Level6 {
  id: scenario.id,
  scenarioId: scenario.scenarioId,
  threatId: scenario.threatId,
  action: 'INSURANCE_TRANSFER',
  actionType: 'RISK_TRANSFER',

  interventionCost: scenario.annualPremium,
  insuranceCoverage: scenario.insuranceCoverage,
  deductible: scenario.deductible,

  baselineImpact: scenario.baselineImpact,
  coveredLoss: scenario.coveredLoss,
  residualLoss: scenario.residualLoss,

  roi: scenario.roi,
  recommended: scenario.recommended,
  priority: scenario.priority,
  implementationStatus: scenario.implementationStatus,
  createdAt: datetime()
});

// 4.5: WhatIfScenario - Reactive Response (50 nodes - baseline comparison)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.whatIfScenarios.reactiveResponse AS scenario
CREATE (ws:WhatIfScenario:ReactiveResponse:Level6 {
  id: scenario.id,
  scenarioId: scenario.scenarioId,
  threatId: scenario.threatId,
  action: 'REACTIVE_PATCH',
  actionType: 'CORRECTIVE',

  interventionCost: scenario.interventionCost,
  baselineBreachProb: scenario.baselineBreachProb,
  reducedBreachProb: scenario.reducedBreachProb,

  baselineImpact: scenario.baselineImpact,
  preventedLoss: scenario.preventedLoss,
  netBenefit: scenario.netBenefit,
  roi: scenario.roi,

  timeToImplement: scenario.timeToImplement,
  recommended: false,  // Baseline comparison - not recommended
  priority: 'LOW',
  implementationStatus: 'NOT_STARTED',
  createdAt: datetime()
});

// ============================================================================
// PHASE 5: LOAD SECURITY CONTROLS (200 nodes - if not exists)
// ============================================================================
// Note: Only create if SecurityControl nodes don't already exist
// Control Frameworks:
//   - NIST 800-53: 80 controls
//   - IEC 62443: 60 controls
//   - NERC-CIP: 40 controls
//   - CIS CSC: 20 controls
// ============================================================================

// 5.1: SecurityControl - NIST 800-53 (80 controls)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.securityControls.nist80053 AS control
MERGE (sc:SecurityControl {controlId: control.controlId})
ON CREATE SET
  sc.id = control.id,
  sc.controlName = control.controlName,
  sc.framework = 'NIST_800_53',
  sc.frameworkVersion = 'Rev 5',
  sc.controlFamily = control.controlFamily,
  sc.nistFunction = control.nistFunction,

  sc.controlType = control.controlType,
  sc.controlClass = control.controlClass,
  sc.controlCategory = control.controlCategory,

  sc.description = control.description,
  sc.objective = control.objective,
  sc.requirements = control.requirements,

  sc.implementationType = control.implementationType,
  sc.implementation = control.implementation,
  sc.vendor = control.vendor,

  sc.effectiveness = control.effectiveness,
  sc.mitigationStrength = control.mitigationStrength,
  sc.reliability = control.reliability,

  sc.initialCost = control.initialCost,
  sc.annualCost = control.annualCost,
  sc.totalCost = control.totalCost,

  sc.applicableSectors = control.applicableSectors,
  sc.mitigatedTechniques = control.mitigatedTechniques,

  sc.deploymentStatus = control.deploymentStatus,
  sc.operationalStatus = control.operationalStatus,
  sc.status = 'ACTIVE',
  sc.createdAt = datetime();

// 5.2: SecurityControl - IEC 62443 (60 controls)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.securityControls.iec62443 AS control
MERGE (sc:SecurityControl {controlId: control.controlId})
ON CREATE SET
  sc.id = control.id,
  sc.controlName = control.controlName,
  sc.framework = 'IEC_62443',
  sc.frameworkVersion = '4-2',
  sc.controlFamily = control.controlFamily,

  sc.controlType = control.controlType,
  sc.controlClass = control.controlClass,
  sc.description = control.description,

  sc.effectiveness = control.effectiveness,
  sc.totalCost = control.totalCost,
  sc.applicableSectors = control.applicableSectors,

  sc.deploymentStatus = control.deploymentStatus,
  sc.status = 'ACTIVE',
  sc.createdAt = datetime();

// 5.3: SecurityControl - NERC-CIP (40 controls)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.securityControls.nercCip AS control
MERGE (sc:SecurityControl {controlId: control.controlId})
ON CREATE SET
  sc.id = control.id,
  sc.controlName = control.controlName,
  sc.framework = 'NERC_CIP',
  sc.frameworkVersion = 'v6',
  sc.controlFamily = control.controlFamily,

  sc.controlType = control.controlType,
  sc.description = control.description,
  sc.effectiveness = control.effectiveness,
  sc.totalCost = control.totalCost,

  sc.applicableSectors = ['Energy'],
  sc.deploymentStatus = control.deploymentStatus,
  sc.status = 'ACTIVE',
  sc.createdAt = datetime();

// 5.4: SecurityControl - CIS CSC (20 controls)
CALL apoc.load.json('file:///data/level6_generated_data.json') YIELD value
UNWIND value.securityControls.cisCsc AS control
MERGE (sc:SecurityControl {controlId: control.controlId})
ON CREATE SET
  sc.id = control.id,
  sc.controlName = control.controlName,
  sc.framework = 'CIS_CSC',
  sc.frameworkVersion = 'v8',
  sc.controlFamily = control.controlFamily,

  sc.controlType = control.controlType,
  sc.description = control.description,
  sc.effectiveness = control.effectiveness,
  sc.totalCost = control.totalCost,

  sc.applicableSectors = control.applicableSectors,
  sc.deploymentStatus = control.deploymentStatus,
  sc.status = 'ACTIVE',
  sc.createdAt = datetime();

// ============================================================================
// PHASE 6: CREATE LEVEL 6 INTERNAL RELATIONSHIPS (50,000+ edges)
// ============================================================================

// 6.1: FutureThreat → HistoricalPattern (BASED_ON_PATTERN) - ~30,000 relationships
MATCH (ft:FutureThreat)
WHERE ft.basedOnPatterns IS NOT NULL
UNWIND ft.basedOnPatterns AS patternId
MATCH (hp:HistoricalPattern {patternId: patternId})
CREATE (ft)-[:BASED_ON_PATTERN {
  patternWeight: 0.8,
  contributionScore: 0.75,
  confidence: hp.confidence,
  extractedAt: datetime()
}]->(hp);

// 6.2: WhatIfScenario → FutureThreat (ADDRESSES_THREAT) - ~1,000 relationships
MATCH (ws:WhatIfScenario)
WHERE ws.threatId IS NOT NULL
MATCH (ft:FutureThreat {predictionId: ws.threatId})
CREATE (ws)-[:ADDRESSES_THREAT {
  mitigationLevel: ws.riskReduction,
  riskReduction: ws.riskReduction,
  costEffectiveness: ws.roi,
  timestamp: datetime()
}]->(ft);

// 6.3: WhatIfScenario → SecurityControl (APPLIES_CONTROL) - ~5,000 relationships
MATCH (ws:WhatIfScenario)
WHERE ws.controls IS NOT NULL
UNWIND ws.controls AS controlId
MATCH (sc:SecurityControl {controlId: controlId})
CREATE (ws)-[:APPLIES_CONTROL {
  controlRelevance: 0.9,
  effectiveness: sc.effectiveness,
  cost: sc.totalCost,
  priority: ws.priority,
  timestamp: datetime()
}]->(sc);

// 6.4: WhatIfScenario → WhatIfScenario (ALTERNATIVE_TO) - ~2,000 relationships
MATCH (ws1:WhatIfScenario)
MATCH (ws2:WhatIfScenario)
WHERE ws1.threatId = ws2.threatId AND ws1.scenarioId < ws2.scenarioId
CREATE (ws1)-[:ALTERNATIVE_TO {
  roiDifference: ws1.roi - ws2.roi,
  costDifference: ws1.interventionCost - ws2.interventionCost,
  recommendation: CASE WHEN ws1.roi > ws2.roi THEN ws1.action ELSE ws2.action END,
  timestamp: datetime()
}]->(ws2);

// 6.5: HistoricalPattern → HistoricalPattern (EVOLVES_FROM) - ~10,000 relationships
MATCH (hp1:HistoricalPattern)
MATCH (hp2:HistoricalPattern)
WHERE hp1.sector = hp2.sector
  AND hp1.patternType = hp2.patternType
  AND hp1.extractedAt > hp2.extractedAt
  AND duration.between(hp2.extractedAt, hp1.extractedAt).days < 365
CREATE (hp1)-[:EVOLVES_FROM {
  evolutionMechanism: 'TEMPORAL_PROGRESSION',
  timespan: duration.between(hp2.extractedAt, hp1.extractedAt).days,
  confidence: 0.8,
  timestamp: datetime()
}]->(hp2);

// 6.6: HistoricalPattern → FutureThreat (PREDICTS) - ~15,000 relationships
MATCH (hp:HistoricalPattern)
WHERE hp.predictiveAccuracy > 0.70
MATCH (ft:FutureThreat)
WHERE hp.sector IN ft.affectedSectors
  AND hp.patternType IN ['PATCH_VELOCITY', 'VULNERABILITY_EXPLOITATION', 'BREACH_SEQUENCE']
CREATE (hp)-[:PREDICTS {
  predictionStrength: hp.predictiveAccuracy,
  accuracy: hp.predictiveAccuracy,
  timeframe: ft.timeframe,
  confidence: hp.confidence,
  timestamp: datetime()
}]->(ft);

// ============================================================================
// PHASE 7: CROSS-LEVEL INTEGRATION RELATIONSHIPS (586,000+ edges)
// ============================================================================

// 7.1: FutureThreat → CVE (EXPLOITS_CVE) - ~50,000 relationships
MATCH (ft:FutureThreat)
WHERE ft.cveId IS NOT NULL
MATCH (cve:CVE {id: ft.cveId})
CREATE (ft)-[:EXPLOITS_CVE {
  exploitLikelihood: ft.probability,
  weaponizationStatus: CASE
    WHEN ft.exploitAvailable THEN 'WEAPONIZED'
    WHEN ft.weaponizationTimeline < 30 THEN 'IN_PROGRESS'
    ELSE 'THEORETICAL'
  END,
  patchAvailable: true,
  timestamp: datetime()
}]->(cve);

// 7.2: FutureThreat → CVE (MENTIONS - from arrays) - ~30,000 relationships
MATCH (ft:FutureThreat)
WHERE ft.relatedCveIds IS NOT NULL
UNWIND ft.relatedCveIds AS cveId
MATCH (cve:CVE {id: cveId})
CREATE (ft)-[:MENTIONS {
  context: 'related_vulnerability',
  timestamp: datetime()
}]->(cve);

// 7.3: FutureThreat → Equipment (THREATENS_EQUIPMENT) - ~200,000 relationships
MATCH (ft:FutureThreat)-[:EXPLOITS_CVE]->(cve:CVE)
MATCH (eq:Equipment)-[:VULNERABLE_TO]->(cve)
CREATE (ft)-[:THREATENS_EQUIPMENT {
  threatLevel: ft.priority,
  exploitProbability: ft.probability,
  impactSeverity: CASE
    WHEN ft.estimatedImpact > 50000000 THEN 'CATASTROPHIC'
    WHEN ft.estimatedImpact > 10000000 THEN 'CRITICAL'
    WHEN ft.estimatedImpact > 1000000 THEN 'MODERATE'
    ELSE 'MINOR'
  END,
  estimatedCost: ft.estimatedImpact / ft.affectedEquipment,
  timestamp: datetime()
}]->(eq);

// 7.4: FutureThreat → Technique (USES_TECHNIQUE) - ~80,000 relationships
MATCH (ft:FutureThreat)
WHERE ft.techniques IS NOT NULL
UNWIND ft.techniques AS techId
MATCH (t:Technique {techniqueId: techId})
CREATE (ft)-[:USES_TECHNIQUE {
  techniqueRelevance: 0.85,
  executionProbability: ft.probability,
  detectionDifficulty: 'MODERATE',
  timestamp: datetime()
}]->(t);

// 7.5: FutureThreat → Sector (TARGETS_SECTOR) - ~40,000 relationships
MATCH (ft:FutureThreat)
WHERE ft.affectedSectors IS NOT NULL
UNWIND ft.affectedSectors AS sectorName
MATCH (s:Sector {name: sectorName})
CREATE (ft)-[:TARGETS_SECTOR {
  targetingConfidence: ft.confidence,
  vulnerability: 0.75,
  estimatedImpact: ft.estimatedImpact,
  timestamp: datetime()
}]->(s);

// 7.6: SecurityControl → Technique (MITIGATES_TECHNIQUE) - ~60,000 relationships
MATCH (sc:SecurityControl)
WHERE sc.mitigatedTechniques IS NOT NULL
UNWIND sc.mitigatedTechniques AS techId
MATCH (t:Technique {techniqueId: techId})
CREATE (sc)-[:MITIGATES_TECHNIQUE {
  effectiveness: sc.effectiveness,
  coverageType: 'PREVENT',
  mechanism: sc.controlClass,
  confidence: 0.9,
  timestamp: datetime()
}]->(t);

// 7.7: SecurityControl → Equipment (PROTECTS_EQUIPMENT) - ~100,000 relationships
MATCH (sc:SecurityControl)
WHERE sc.applicableSectors IS NOT NULL
UNWIND sc.applicableSectors AS sectorName
MATCH (eq:Equipment)-[:PART_OF_SECTOR]->(s:Sector {name: sectorName})
CREATE (sc)-[:PROTECTS_EQUIPMENT {
  protectionLevel: sc.mitigationStrength,
  applicability: sc.effectiveness,
  deployedOn: CASE WHEN sc.deploymentStatus = 'FULL' THEN true ELSE false END,
  effectiveness: sc.effectiveness,
  timestamp: datetime()
}]->(eq);

// 7.8: SecurityControl → CVE (PREVENTS_EXPLOITATION) - ~50,000 relationships
MATCH (sc:SecurityControl)-[:MITIGATES_TECHNIQUE]->(t:Technique)
MATCH (cve:CVE)-[:USES_TECHNIQUE]->(t)
CREATE (sc)-[:PREVENTS_EXPLOITATION {
  preventionStrength: sc.mitigationStrength,
  bypassDifficulty: CASE
    WHEN sc.effectiveness > 0.9 THEN 'VERY_HARD'
    WHEN sc.effectiveness > 0.7 THEN 'HARD'
    ELSE 'MODERATE'
  END,
  timestamp: datetime()
}]->(cve);

// 7.9: FutureThreat → InformationEvent (TRIGGERED_BY_EVENT) - ~20,000 relationships
MATCH (ft:FutureThreat)
WHERE ft.basedOnEvents IS NOT NULL
UNWIND ft.basedOnEvents AS eventId
MATCH (ie:InformationEvent {eventId: eventId})
CREATE (ft)-[:TRIGGERED_BY_EVENT {
  eventRelevance: 0.8,
  timeOffset: duration.between(ie.timestamp, ft.likelyDate).hours,
  correlationStrength: 0.75,
  timestamp: datetime()
}]->(ie);

// 7.10: FutureThreat → GeopoliticalEvent (INFLUENCED_BY_GEOPOLITICS) - ~15,000 relationships
MATCH (ft:FutureThreat)
MATCH (ge:GeopoliticalEvent)
WHERE ge.tensionLevel > 7.0
  AND ft.likelyDate > ge.timestamp
  AND duration.between(ge.timestamp, ft.likelyDate).days < 180
  AND EXISTS {
    MATCH (ge)-[:TARGETS_SECTOR]->(s:Sector)
    WHERE s.name IN ft.affectedSectors
  }
CREATE (ft)-[:INFLUENCED_BY_GEOPOLITICS {
  influenceMultiplier: ge.cyberActivityCorrelation,
  mechanism: 'GEOPOLITICAL_TENSION',
  confidence: 0.7,
  timestamp: datetime()
}]->(ge);

// 7.11: HistoricalPattern → Sector (CHARACTERISTIC_OF) - ~100,000 relationships
MATCH (hp:HistoricalPattern)
WHERE hp.sector IS NOT NULL
MATCH (s:Sector {name: hp.sector})
CREATE (hp)-[:CHARACTERISTIC_OF {
  prevalence: hp.confidence,
  representativeness: hp.applicabilityScore,
  stability: hp.predictiveAccuracy,
  timestamp: datetime()
}]->(s);

// 7.12: HistoricalPattern → CognitiveBias (EXHIBITS_BIAS) - ~30,000 relationships
MATCH (hp:HistoricalPattern)
WHERE hp.patternType IN ['PATCH_VELOCITY', 'INCIDENT_RESPONSE', 'BUDGET_CYCLE']
MATCH (cb:CognitiveBias)
WHERE cb.name IN ['normalcy_bias', 'optimism_bias', 'status_quo_bias', 'availability_bias']
CREATE (hp)-[:EXHIBITS_BIAS {
  strength: hp.confidence,
  mechanism: 'BEHAVIORAL_PATTERN',
  timestamp: datetime()
}]->(cb);

// 7.13: WhatIfScenario → Organization (IMPACTS_BUDGET) - ~10,000 relationships
MATCH (ws:WhatIfScenario)
WHERE ws.recommended = true AND ws.interventionCost > 100000
MATCH (ft:FutureThreat {predictionId: ws.threatId})
MATCH (ft)-[:THREATENS_EQUIPMENT]->(eq:Equipment)-[:OWNED_BY]->(org:Organization)
WITH ws, org, count(DISTINCT eq) AS affectedAssets
WHERE affectedAssets > 10
CREATE (ws)-[:IMPACTS_BUDGET {
  budgetCategory: 'CAPEX',
  amount: ws.interventionCost,
  fiscalYear: 'FY2026',
  approval: 'PENDING',
  timestamp: datetime()
}]->(org);

// 7.14: SecurityControl → FutureThreat (RECOMMENDED_FOR) - ~20,000 relationships
MATCH (sc:SecurityControl)-[:PREVENTS_EXPLOITATION]->(cve:CVE)<-[:EXPLOITS_CVE]-(ft:FutureThreat)
WHERE ft.probability > 0.70 AND sc.effectiveness > 0.80
CREATE (sc)-[:RECOMMENDED_FOR {
  recommendationPriority: ft.priority,
  roi: 100.0,  // Simplified calculation
  effectiveness: sc.effectiveness,
  urgency: CASE WHEN ft.predictionHorizon < 30 THEN 'CRITICAL' ELSE 'HIGH' END,
  timestamp: datetime()
}]->(ft);

// ============================================================================
// PHASE 8: VERIFICATION & STATISTICS
// ============================================================================

// 8.1: Count all Level 6 nodes by type
MATCH (n)
WHERE any(label IN labels(n) WHERE
  label IN ['HistoricalPattern', 'FutureThreat', 'WhatIfScenario', 'SecurityControl'])
RETURN
  labels(n)[0] AS node_type,
  count(n) AS node_count,
  collect(DISTINCT labels(n)) AS label_combinations
ORDER BY node_count DESC;

// 8.2: Count all Level 6 relationships by type
MATCH ()-[r]->()
WHERE type(r) IN [
  'BASED_ON_PATTERN', 'ADDRESSES_THREAT', 'APPLIES_CONTROL', 'ALTERNATIVE_TO',
  'EVOLVES_FROM', 'PREDICTS', 'EXPLOITS_CVE', 'MENTIONS', 'THREATENS_EQUIPMENT',
  'USES_TECHNIQUE', 'TARGETS_SECTOR', 'MITIGATES_TECHNIQUE', 'PROTECTS_EQUIPMENT',
  'PREVENTS_EXPLOITATION', 'TRIGGERED_BY_EVENT', 'INFLUENCED_BY_GEOPOLITICS',
  'CHARACTERISTIC_OF', 'EXHIBITS_BIAS', 'IMPACTS_BUDGET', 'RECOMMENDED_FOR'
]
RETURN
  type(r) AS relationship_type,
  count(r) AS relationship_count
ORDER BY relationship_count DESC;

// 8.3: Cross-level integration verification
MATCH (ft:FutureThreat)-[r]->(cve:CVE)
RETURN
  'FutureThreat_to_CVE' AS connection_type,
  count(DISTINCT ft) AS future_threats,
  count(DISTINCT cve) AS cves_referenced,
  count(r) AS total_links;

MATCH (ft:FutureThreat)-[r]->(eq:Equipment)
RETURN
  'FutureThreat_to_Equipment' AS connection_type,
  count(DISTINCT ft) AS future_threats,
  count(DISTINCT eq) AS equipment_threatened,
  count(r) AS total_links;

MATCH (sc:SecurityControl)-[r]->(t:Technique)
RETURN
  'SecurityControl_to_Technique' AS connection_type,
  count(DISTINCT sc) AS controls,
  count(DISTINCT t) AS techniques_mitigated,
  count(r) AS total_links;

// 8.4: High-Value Threat Query (McKenney Q7)
MATCH (ft:FutureThreat)
WHERE ft.predictionStatus = 'ACTIVE'
  AND ft.probability > 0.70
WITH ft
ORDER BY ft.probability * ft.estimatedImpact DESC
LIMIT 50
RETURN
  ft.predictionId,
  ft.predictedEvent,
  ft.probability,
  ft.estimatedImpact,
  ft.likelyDate,
  ft.affectedEquipment,
  ft.affectedSectors;

// 8.5: Recommended Actions Query (McKenney Q8)
MATCH (ft:FutureThreat)
WHERE ft.probability > 0.70
MATCH (ws:WhatIfScenario)-[:ADDRESSES_THREAT]->(ft)
WHERE ws.recommended = true
WITH ft, ws
ORDER BY ws.roi DESC
LIMIT 100
RETURN
  ft.predictionId,
  ft.predictedEvent,
  ft.probability,
  ft.estimatedImpact,
  ws.action,
  ws.roi,
  ws.roiPercentage,
  ws.interventionCost,
  ws.preventedLoss,
  ws.priority;

// 8.6: Final deployment summary
MATCH (hp:HistoricalPattern)
WITH count(hp) AS hp_count
MATCH (ft:FutureThreat)
WITH hp_count, count(ft) AS ft_count
MATCH (ws:WhatIfScenario)
WITH hp_count, ft_count, count(ws) AS ws_count
MATCH (sc:SecurityControl)
WITH hp_count, ft_count, ws_count, count(sc) AS sc_count
MATCH ()-[r]->()
WHERE type(r) IN [
  'BASED_ON_PATTERN', 'ADDRESSES_THREAT', 'APPLIES_CONTROL', 'EXPLOITS_CVE',
  'THREATENS_EQUIPMENT', 'USES_TECHNIQUE', 'TARGETS_SECTOR', 'MITIGATES_TECHNIQUE',
  'PROTECTS_EQUIPMENT', 'PREVENTS_EXPLOITATION', 'TRIGGERED_BY_EVENT',
  'INFLUENCED_BY_GEOPOLITICS', 'CHARACTERISTIC_OF', 'RECOMMENDED_FOR'
]
RETURN
  'LEVEL 6 DEPLOYMENT SUMMARY' AS status,
  hp_count AS HistoricalPatterns,
  ft_count AS FutureThreats,
  ws_count AS WhatIfScenarios,
  sc_count AS SecurityControls,
  (hp_count + ft_count + ws_count + sc_count) AS total_nodes,
  count(r) AS total_relationships,
  datetime() AS deployment_completed;

// 8.7: McKenney Questions Validation
MATCH (ft:FutureThreat)
WHERE ft.predictionStatus = 'ACTIVE'
WITH count(ft) AS active_predictions
MATCH (ft:FutureThreat)
WHERE ft.predictionStatus = 'ACTIVE' AND ft.probability > 0.70
WITH active_predictions, count(ft) AS high_confidence_predictions
MATCH (ws:WhatIfScenario)
WHERE ws.recommended = true AND ws.roi > 100
WITH active_predictions, high_confidence_predictions, count(ws) AS high_roi_scenarios
RETURN
  'MCKENNEY QUESTIONS VALIDATION' AS status,
  active_predictions AS Q7_predictions_total,
  high_confidence_predictions AS Q7_high_confidence,
  CASE WHEN high_confidence_predictions >= 50 THEN 'PASS' ELSE 'FAIL' END AS Q7_target_met,
  high_roi_scenarios AS Q8_scenarios_high_roi,
  CASE WHEN high_roi_scenarios >= 10 THEN 'PASS' ELSE 'FAIL' END AS Q8_target_met;

// ============================================================================
// END OF DEPLOYMENT SCRIPT
// ============================================================================
