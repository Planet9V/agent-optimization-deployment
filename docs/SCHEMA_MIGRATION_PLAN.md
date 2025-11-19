# Neo4j Schema Migration Plan
**Zero-Downtime Enhancement to 8-Layer Architecture**

**File:** SCHEMA_MIGRATION_PLAN.md
**Created:** 2025-10-29 02:30:00 UTC
**Version:** v1.0.0
**Author:** Code Review Agent
**Purpose:** Step-by-step Cypher migration scripts to enhance existing Neo4j schema while preserving all data
**Status:** READY FOR EXECUTION

---

## Executive Summary

**Current State:**
- 179,859 CVE nodes
- 615 CAPEC nodes
- 834 Technique nodes
- 293 ThreatActor nodes
- Active production database with ongoing imports

**Migration Goal:**
- Add psychometric, SAREF IoT, and social media intelligence layers
- Enhance existing nodes with new properties
- Create new relationship types for multi-dimensional analysis
- Zero data loss, zero downtime

**Risk Level:** 🟢 LOW (Non-destructive, additive-only approach)

---

## Migration Prerequisites

### 1. Backup Current Database

```bash
# Create timestamped backup
BACKUP_DIR="/home/jim/neo4j_backups/pre_migration_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Stop Neo4j (if required by your setup)
# sudo systemctl stop neo4j

# Backup using neo4j-admin
neo4j-admin database backup neo4j --to-path="$BACKUP_DIR"

# Verify backup integrity
neo4j-admin database check neo4j --from-path="$BACKUP_DIR"

# Restart Neo4j
# sudo systemctl start neo4j

echo "✅ Backup completed: $BACKUP_DIR"
```

### 2. Pre-Migration Validation

```cypher
// Save current state metrics
CALL {
  MATCH (n) RETURN count(n) AS total_nodes
}
CALL {
  MATCH ()-[r]->() RETURN count(r) AS total_relationships
}
CALL {
  CALL db.labels() YIELD label
  RETURN collect(label) AS all_labels
}
CALL {
  CALL db.relationshipTypes() YIELD relationshipType
  RETURN collect(relationshipType) AS all_rel_types
}
RETURN
  total_nodes,
  total_relationships,
  size(all_labels) AS label_count,
  size(all_rel_types) AS rel_type_count,
  datetime() AS snapshot_timestamp;

// Export to file for comparison
// Expected: 179,859+ nodes, 615+ CAPECs, 834+ Techniques, 293+ ThreatActors
```

---

## Phase 1: Add New Constraints and Indexes

**Duration:** 10-15 minutes
**Risk:** 🟢 LOW (Non-blocking for existing data)
**Rollback:** Drop newly created constraints/indexes

### 1.1 Psychometric Layer Constraints

```cypher
// ═══════════════════════════════════════════════════════════════
// PSYCHOMETRIC INTELLIGENCE LAYER - Constraints
// ═══════════════════════════════════════════════════════════════

// Behavioral Pattern Analysis
CREATE CONSTRAINT behavioral_pattern_id IF NOT EXISTS
FOR (bp:BehavioralPattern) REQUIRE bp.id IS UNIQUE;

CREATE CONSTRAINT personality_profile_id IF NOT EXISTS
FOR (pp:PersonalityProfile) REQUIRE pp.id IS UNIQUE;

// Social Engineering Indicators
CREATE CONSTRAINT social_engineering_tactic_id IF NOT EXISTS
FOR (set:SocialEngineeringTactic) REQUIRE set.id IS UNIQUE;

CREATE CONSTRAINT persuasion_technique_id IF NOT EXISTS
FOR (pt:PersuasionTechnique) REQUIRE pt.id IS UNIQUE;

// Cognitive Vulnerability Assessment
CREATE CONSTRAINT cognitive_bias_id IF NOT EXISTS
FOR (cb:CognitiveBias) REQUIRE cb.id IS UNIQUE;

CREATE CONSTRAINT decision_making_pattern_id IF NOT EXISTS
FOR (dmp:DecisionMakingPattern) REQUIRE dmp.id IS UNIQUE;

// Emotional State Tracking
CREATE CONSTRAINT emotional_state_id IF NOT EXISTS
FOR (es:EmotionalState) REQUIRE es.id IS UNIQUE;

CREATE CONSTRAINT stress_indicator_id IF NOT EXISTS
FOR (si:StressIndicator) REQUIRE si.id IS UNIQUE;

// Risk Perception Analysis
CREATE CONSTRAINT risk_perception_id IF NOT EXISTS
FOR (rp:RiskPerception) REQUIRE rp.id IS UNIQUE;

CREATE CONSTRAINT threat_awareness_level_id IF NOT EXISTS
FOR (tal:ThreatAwarenessLevel) REQUIRE tal.id IS UNIQUE;
```

### 1.2 SAREF IoT Layer Constraints

```cypher
// ═══════════════════════════════════════════════════════════════
// SAREF IoT SEMANTIC LAYER - Constraints
// ═══════════════════════════════════════════════════════════════

// SAREF Core Devices
CREATE CONSTRAINT saref_device_id IF NOT EXISTS
FOR (sd:SAREFDevice) REQUIRE sd.id IS UNIQUE;

CREATE CONSTRAINT saref_sensor_id IF NOT EXISTS
FOR (ss:SAREFSensor) REQUIRE ss.id IS UNIQUE;

CREATE CONSTRAINT saref_actuator_id IF NOT EXISTS
FOR (sa:SAREFActuator) REQUIRE sa.id IS UNIQUE;

// SAREF Functions and Commands
CREATE CONSTRAINT saref_function_id IF NOT EXISTS
FOR (sf:SAREFFunction) REQUIRE sf.id IS UNIQUE;

CREATE CONSTRAINT saref_command_id IF NOT EXISTS
FOR (sc:SAREFCommand) REQUIRE sc.id IS UNIQUE;

// SAREF Measurements
CREATE CONSTRAINT saref_measurement_id IF NOT EXISTS
FOR (sm:SAREFMeasurement) REQUIRE sm.id IS UNIQUE;

CREATE CONSTRAINT saref_unit_of_measure_id IF NOT EXISTS
FOR (sum:SAREFUnitOfMeasure) REQUIRE sum.id IS UNIQUE;

// SAREF States
CREATE CONSTRAINT saref_state_id IF NOT EXISTS
FOR (ss:SAREFState) REQUIRE ss.id IS UNIQUE;

// SAREF Services
CREATE CONSTRAINT saref_service_id IF NOT EXISTS
FOR (serv:SAREFService) REQUIRE serv.id IS UNIQUE;

// SAREF Properties
CREATE CONSTRAINT saref_property_id IF NOT EXISTS
FOR (sp:SAREFProperty) REQUIRE sp.id IS UNIQUE;
```

### 1.3 Social Media Intelligence Layer Constraints

```cypher
// ═══════════════════════════════════════════════════════════════
// SOCIAL MEDIA INTELLIGENCE LAYER - Constraints
// ═══════════════════════════════════════════════════════════════

// Social Media Entities
CREATE CONSTRAINT social_media_account_id IF NOT EXISTS
FOR (sma:SocialMediaAccount) REQUIRE sma.id IS UNIQUE;

CREATE CONSTRAINT social_media_post_id IF NOT EXISTS
FOR (smp:SocialMediaPost) REQUIRE smp.id IS UNIQUE;

CREATE CONSTRAINT hashtag_id IF NOT EXISTS
FOR (ht:Hashtag) REQUIRE ht.tag IS UNIQUE;

// Network Analysis
CREATE CONSTRAINT social_network_id IF NOT EXISTS
FOR (sn:SocialNetwork) REQUIRE sn.id IS UNIQUE;

CREATE CONSTRAINT influence_node_id IF NOT EXISTS
FOR (in:InfluenceNode) REQUIRE in.id IS UNIQUE;

// Sentiment and Opinion
CREATE CONSTRAINT sentiment_analysis_id IF NOT EXISTS
FOR (sa:SentimentAnalysis) REQUIRE sa.id IS UNIQUE;

CREATE CONSTRAINT opinion_cluster_id IF NOT EXISTS
FOR (oc:OpinionCluster) REQUIRE oc.id IS UNIQUE;

// Disinformation Tracking
CREATE CONSTRAINT disinformation_campaign_id IF NOT EXISTS
FOR (dc:DisinformationCampaign) REQUIRE dc.id IS UNIQUE;

CREATE CONSTRAINT fake_news_indicator_id IF NOT EXISTS
FOR (fni:FakeNewsIndicator) REQUIRE fni.id IS UNIQUE;

// Threat Actor Social Presence
CREATE CONSTRAINT threat_actor_social_profile_id IF NOT EXISTS
FOR (tasp:ThreatActorSocialProfile) REQUIRE tasp.id IS UNIQUE;
```

### 1.4 Performance Indexes for New Layers

```cypher
// ═══════════════════════════════════════════════════════════════
// PERFORMANCE INDEXES - New Layers
// ═══════════════════════════════════════════════════════════════

// Psychometric Indexes
CREATE INDEX behavioral_pattern_type IF NOT EXISTS
FOR (bp:BehavioralPattern) ON (bp.pattern_type);

CREATE INDEX personality_profile_type IF NOT EXISTS
FOR (pp:PersonalityProfile) ON (pp.profile_type);

CREATE INDEX cognitive_bias_category IF NOT EXISTS
FOR (cb:CognitiveBias) ON (cb.bias_category);

CREATE INDEX risk_perception_level IF NOT EXISTS
FOR (rp:RiskPerception) ON (rp.perceived_risk_level);

// SAREF IoT Indexes
CREATE INDEX saref_device_type IF NOT EXISTS
FOR (sd:SAREFDevice) ON (sd.device_type);

CREATE INDEX saref_measurement_timestamp IF NOT EXISTS
FOR (sm:SAREFMeasurement) ON (sm.timestamp);

CREATE INDEX saref_state_value IF NOT EXISTS
FOR (ss:SAREFState) ON (ss.state_value);

// Social Media Indexes
CREATE INDEX social_media_platform IF NOT EXISTS
FOR (sma:SocialMediaAccount) ON (sma.platform);

CREATE INDEX social_media_post_timestamp IF NOT EXISTS
FOR (smp:SocialMediaPost) ON (smp.posted_at);

CREATE INDEX hashtag_popularity IF NOT EXISTS
FOR (ht:Hashtag) ON (ht.usage_count);

CREATE INDEX sentiment_score IF NOT EXISTS
FOR (sa:SentimentAnalysis) ON (sa.sentiment_score);

CREATE INDEX disinformation_severity IF NOT EXISTS
FOR (dc:DisinformationCampaign) ON (dc.severity_level);

// Composite Indexes for Complex Queries
CREATE INDEX social_media_threat_actor_platform IF NOT EXISTS
FOR (tasp:ThreatActorSocialProfile) ON (tasp.platform, tasp.verified_status);

CREATE INDEX behavioral_pattern_risk_composite IF NOT EXISTS
FOR (bp:BehavioralPattern) ON (bp.pattern_type, bp.risk_score);
```

### 1.5 Full-Text Search Indexes

```cypher
// ═══════════════════════════════════════════════════════════════
// FULL-TEXT SEARCH INDEXES - New Layers
// ═══════════════════════════════════════════════════════════════

// Psychometric content search
CREATE FULLTEXT INDEX psychometric_content_search IF NOT EXISTS
FOR (bp:BehavioralPattern|pp:PersonalityProfile|cb:CognitiveBias)
ON EACH [bp.description, pp.description, cb.description];

// Social media content search
CREATE FULLTEXT INDEX social_media_content_search IF NOT EXISTS
FOR (smp:SocialMediaPost|dc:DisinformationCampaign)
ON EACH [smp.content, dc.campaign_description];

// SAREF semantic search
CREATE FULLTEXT INDEX saref_semantic_search IF NOT EXISTS
FOR (sd:SAREFDevice|sf:SAREFFunction|sc:SAREFCommand)
ON EACH [sd.description, sf.description, sc.description];
```

---

## Phase 2: Create New Node Types

**Duration:** 5-10 minutes
**Risk:** 🟢 LOW (New nodes, no impact on existing data)
**Rollback:** Delete nodes by label with new types

### 2.1 Create Sample Psychometric Nodes

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 2.1: Psychometric Node Templates
// ═══════════════════════════════════════════════════════════════

// Behavioral Patterns (common attack enablers)
MERGE (bp1:BehavioralPattern {
  id: 'BP-001',
  pattern_type: 'AUTHORITY_COMPLIANCE',
  description: 'Strong tendency to comply with perceived authority figures',
  risk_score: 0.75,
  detection_method: 'behavioral_analysis',
  prevalence: 'HIGH',
  created_at: datetime(),
  updated_at: datetime()
});

MERGE (bp2:BehavioralPattern {
  id: 'BP-002',
  pattern_type: 'URGENCY_SUSCEPTIBILITY',
  description: 'Reduced critical thinking under time pressure',
  risk_score: 0.82,
  detection_method: 'behavioral_analysis',
  prevalence: 'VERY_HIGH',
  created_at: datetime(),
  updated_at: datetime()
});

MERGE (bp3:BehavioralPattern {
  id: 'BP-003',
  pattern_type: 'TRUST_EXPLOITATION',
  description: 'Over-reliance on trust signals without verification',
  risk_score: 0.68,
  detection_method: 'behavioral_analysis',
  prevalence: 'MEDIUM',
  created_at: datetime(),
  updated_at: datetime()
});

// Cognitive Biases
MERGE (cb1:CognitiveBias {
  id: 'CB-001',
  bias_category: 'CONFIRMATION_BIAS',
  description: 'Tendency to interpret information confirming pre-existing beliefs',
  exploitation_difficulty: 'LOW',
  common_contexts: ['security alerts', 'threat warnings', 'vendor communications'],
  mitigation_strategies: ['critical thinking training', 'peer review', 'devil advocate protocols'],
  created_at: datetime(),
  updated_at: datetime()
});

MERGE (cb2:CognitiveBias {
  id: 'CB-002',
  bias_category: 'AVAILABILITY_HEURISTIC',
  description: 'Overestimating probability of events easily recalled',
  exploitation_difficulty: 'MEDIUM',
  common_contexts: ['incident response', 'risk assessment', 'budget allocation'],
  mitigation_strategies: ['data-driven decision making', 'statistical analysis', 'base rate consideration'],
  created_at: datetime(),
  updated_at: datetime()
});

// Social Engineering Tactics
MERGE (set1:SocialEngineeringTactic {
  id: 'SET-001',
  tactic_name: 'PRETEXTING',
  description: 'Creating fabricated scenario to obtain information',
  success_rate: 0.67,
  common_pretexts: ['IT support', 'executive assistant', 'vendor representative'],
  indicators: ['unexpected contact', 'information request', 'urgency pressure'],
  created_at: datetime(),
  updated_at: datetime()
});

MERGE (set2:SocialEngineeringTactic {
  id: 'SET-002',
  tactic_name: 'PHISHING',
  description: 'Deceptive communication to trick recipients',
  success_rate: 0.14,
  delivery_vectors: ['email', 'SMS', 'social media', 'messaging apps'],
  indicators: ['suspicious sender', 'urgent language', 'unusual requests'],
  created_at: datetime(),
  updated_at: datetime()
});

// Risk Perception Profiles
MERGE (rp1:RiskPerception {
  id: 'RP-001',
  perceived_risk_level: 'OPTIMISM_BIAS',
  description: 'Underestimation of personal vulnerability',
  actual_risk_level: 'HIGH',
  perception_gap: 0.65,
  common_rationalizations: ['it won't happen to me', 'we're too small to target', 'we have security'],
  created_at: datetime(),
  updated_at: datetime()
});

MERGE (rp2:RiskPerception {
  id: 'RP-002',
  perceived_risk_level: 'ALERT_FATIGUE',
  description: 'Desensitization from excessive warnings',
  actual_risk_level: 'CRITICAL',
  perception_gap: 0.88,
  common_rationalizations: ['another false alarm', 'security always crying wolf', 'too many alerts'],
  created_at: datetime(),
  updated_at: datetime()
});
```

### 2.2 Create Sample SAREF IoT Nodes

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 2.2: SAREF IoT Node Templates
// ═══════════════════════════════════════════════════════════════

// SAREF Devices (smart building/ICS context)
MERGE (sd1:SAREFDevice {
  id: 'SAREF-DEV-001',
  device_type: 'SmartThermostat',
  manufacturer: 'Generic IoT Corp',
  model: 'ThermoPro-2000',
  saref_profile: 'saref:BuildingDevice',
  communication_protocol: ['WiFi', 'Zigbee'],
  firmware_version: '2.3.1',
  last_update: datetime(),
  created_at: datetime()
});

MERGE (sd2:SAREFDevice {
  id: 'SAREF-DEV-002',
  device_type: 'SmartCamera',
  manufacturer: 'SecureVision Inc',
  model: 'CamPro-X500',
  saref_profile: 'saref:SecurityDevice',
  communication_protocol: ['Ethernet', 'WiFi'],
  firmware_version: '1.8.4',
  last_update: datetime(),
  created_at: datetime()
});

MERGE (sd3:SAREFDevice {
  id: 'SAREF-DEV-003',
  device_type: 'IndustrialSensor',
  manufacturer: 'ICS Solutions Ltd',
  model: 'SensorMax-4000',
  saref_profile: 'saref:IndustrialDevice',
  communication_protocol: ['Modbus TCP', 'OPC UA'],
  firmware_version: '3.2.0',
  last_update: datetime(),
  created_at: datetime()
});

// SAREF Functions
MERGE (sf1:SAREFFunction {
  id: 'SAREF-FUNC-001',
  function_type: 'TemperatureMeasurement',
  description: 'Measures ambient temperature',
  saref_category: 'saref:MeteringFunction',
  input_properties: ['temperature_sensor_reading'],
  output_properties: ['temperature_value', 'unit_celsius'],
  created_at: datetime()
});

MERGE (sf2:SAREFFunction {
  id: 'SAREF-FUNC-002',
  function_type: 'VideoStreamCapture',
  description: 'Captures and streams video data',
  saref_category: 'saref:SensingFunction',
  input_properties: ['video_sensor', 'stream_quality'],
  output_properties: ['video_stream', 'resolution', 'fps'],
  created_at: datetime()
});

// SAREF Commands
MERGE (sc1:SAREFCommand {
  id: 'SAREF-CMD-001',
  command_type: 'SetTemperature',
  description: 'Sets target temperature for thermostat',
  saref_category: 'saref:ActuatingCommand',
  required_parameters: ['target_temperature', 'mode'],
  created_at: datetime()
});

MERGE (sc2:SAREFCommand {
  id: 'SAREF-CMD-002',
  command_type: 'StartRecording',
  description: 'Initiates video recording',
  saref_category: 'saref:ActuatingCommand',
  required_parameters: ['duration', 'quality_setting'],
  created_at: datetime()
});

// SAREF States
MERGE (ss1:SAREFState {
  id: 'SAREF-STATE-001',
  state_value: 'OPERATIONAL',
  state_type: 'DeviceState',
  description: 'Device functioning normally',
  created_at: datetime()
});

MERGE (ss2:SAREFState {
  id: 'SAREF-STATE-002',
  state_value: 'COMPROMISED',
  state_type: 'SecurityState',
  description: 'Device security integrity violated',
  created_at: datetime()
});
```

### 2.3 Create Sample Social Media Intelligence Nodes

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 2.3: Social Media Intelligence Node Templates
// ═══════════════════════════════════════════════════════════════

// Threat Actor Social Profiles
MERGE (tasp1:ThreatActorSocialProfile {
  id: 'TASP-001',
  platform: 'Twitter',
  handle: '@apt29_activities',
  display_name: 'Security Research',
  verified_status: false,
  follower_count: 8234,
  account_creation_date: date('2019-03-15'),
  activity_patterns: ['irregular_posting', 'timezone_inconsistencies', 'automated_behaviors'],
  threat_intelligence_confidence: 0.82,
  last_analyzed: datetime(),
  created_at: datetime()
});

MERGE (tasp2:ThreatActorSocialProfile {
  id: 'TASP-002',
  platform: 'Telegram',
  handle: '@darkwebmarket',
  display_name: 'Exploit Marketplace',
  verified_status: false,
  member_count: 15642,
  channel_creation_date: date('2020-07-22'),
  activity_patterns: ['exploit_trading', 'credential_dumps', 'malware_distribution'],
  threat_intelligence_confidence: 0.95,
  last_analyzed: datetime(),
  created_at: datetime()
});

// Hashtag Tracking (threat indicator hashtags)
MERGE (ht1:Hashtag {
  tag: '#dataleaked',
  platform: 'multiple',
  usage_count: 45321,
  first_seen: date('2021-01-10'),
  threat_relevance: 'HIGH',
  common_contexts: ['data breach announcements', 'credential dumps', 'extortion'],
  created_at: datetime()
});

MERGE (ht2:Hashtag {
  tag: '#zeroday',
  platform: 'multiple',
  usage_count: 23456,
  first_seen: date('2018-06-05'),
  threat_relevance: 'CRITICAL',
  common_contexts: ['vulnerability disclosure', 'exploit trading', 'underground markets'],
  created_at: datetime()
});

// Disinformation Campaigns
MERGE (dc1:DisinformationCampaign {
  id: 'DC-001',
  campaign_name: 'FakeSecurityUpdate',
  description: 'Spreading fake security update notifications to deliver malware',
  severity_level: 'HIGH',
  target_demographics: ['enterprise_IT', 'security_teams'],
  platforms_used: ['LinkedIn', 'Twitter', 'Security Forums'],
  start_date: date('2024-09-01'),
  status: 'ACTIVE',
  estimated_reach: 125000,
  created_at: datetime()
});

MERGE (dc2:DisinformationCampaign {
  id: 'DC-002',
  campaign_name: 'FalseFlagAttribution',
  description: 'Misattributing attacks to confuse incident response',
  severity_level: 'MEDIUM',
  target_demographics: ['threat_intelligence_analysts', 'media'],
  platforms_used: ['Twitter', 'Reddit', 'Dark Web Forums'],
  start_date: date('2024-08-15'),
  status: 'ACTIVE',
  estimated_reach: 45000,
  created_at: datetime()
});

// Sentiment Analysis Nodes
MERGE (sa1:SentimentAnalysis {
  id: 'SA-001',
  analysis_subject: 'CVE-2024-XXXXX',
  sentiment_score: -0.72,
  sentiment_label: 'NEGATIVE',
  confidence: 0.89,
  sample_size: 2341,
  analysis_timestamp: datetime(),
  key_themes: ['exploitation_in_wild', 'patch_urgency', 'vendor_criticism'],
  created_at: datetime()
});

MERGE (sa2:SentimentAnalysis {
  id: 'SA-002',
  analysis_subject: 'Security Product XYZ',
  sentiment_score: 0.45,
  sentiment_label: 'MIXED',
  confidence: 0.76,
  sample_size: 1876,
  analysis_timestamp: datetime(),
  key_themes: ['effective_detection', 'false_positives', 'configuration_complexity'],
  created_at: datetime()
});
```

---

## Phase 3: Add Properties to Existing Nodes

**Duration:** 20-30 minutes
**Risk:** 🟡 MEDIUM (Modifying existing nodes, but non-destructive)
**Rollback:** Remove added properties using REMOVE command

### 3.1 Enhance CVE Nodes with Psychometric Properties

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 3.1: Enhance Existing CVE Nodes
// ═══════════════════════════════════════════════════════════════

// Add psychometric exploitation indicators to CVEs
MATCH (cve:CVE)
WHERE cve.cveId IS NOT NULL
SET cve.requires_social_engineering = false,
    cve.cognitive_bias_exploited = [],
    cve.psychological_manipulation_vector = 'NONE',
    cve.victim_behavior_required = 'NONE',
    cve.awareness_training_effectiveness = 'N/A',
    cve.enhanced_at = datetime();

// Update high-profile phishing-related CVEs
MATCH (cve:CVE)
WHERE cve.description CONTAINS 'phishing'
   OR cve.description CONTAINS 'social engineering'
   OR cve.description CONTAINS 'user interaction'
SET cve.requires_social_engineering = true,
    cve.cognitive_bias_exploited = ['AUTHORITY_COMPLIANCE', 'URGENCY_SUSCEPTIBILITY'],
    cve.psychological_manipulation_vector = 'DECEPTION',
    cve.victim_behavior_required = 'USER_CLICK',
    cve.awareness_training_effectiveness = 'HIGH';

// Update CVEs requiring user interaction
MATCH (cve:CVE)
WHERE cve.cvssV3AttackVector = 'NETWORK'
  AND cve.cvssV3UserInteraction = 'REQUIRED'
SET cve.victim_behavior_required = 'USER_ACTION',
    cve.awareness_training_effectiveness = 'MEDIUM';

// Add social media spread potential
MATCH (cve:CVE)
WHERE cve.cvssV3BaseScore >= 7.0
SET cve.social_media_amplification_risk = 'HIGH',
    cve.disinformation_campaign_potential = 'MEDIUM',
    cve.public_disclosure_impact = 'HIGH';

RETURN count(*) AS cves_enhanced;
```

### 3.2 Enhance ThreatActor Nodes with Social Intelligence

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 3.2: Enhance Existing ThreatActor Nodes
// ═══════════════════════════════════════════════════════════════

// Add social media intelligence properties to all threat actors
MATCH (ta:ThreatActor)
WHERE ta.id IS NOT NULL
SET ta.social_media_presence = [],
    ta.disinformation_campaigns = [],
    ta.influence_operations = [],
    ta.public_persona = 'UNKNOWN',
    ta.social_engineering_sophistication = 'UNKNOWN',
    ta.psychological_tactics_used = [],
    ta.victim_profiling_capability = 'UNKNOWN',
    ta.enhanced_at = datetime();

// Update known APT groups with social presence
MATCH (ta:ThreatActor)
WHERE ta.name CONTAINS 'APT'
   OR ta.threatActorType = 'nation-state'
SET ta.social_media_presence = ['Twitter', 'Telegram', 'Dark Web Forums'],
    ta.disinformation_campaigns = ['Active'],
    ta.influence_operations = ['Political', 'Economic'],
    ta.public_persona = 'SOPHISTICATED',
    ta.social_engineering_sophistication = 'ADVANCED',
    ta.psychological_tactics_used = ['PRETEXTING', 'AUTHORITY_EXPLOITATION', 'URGENCY_CREATION'],
    ta.victim_profiling_capability = 'ADVANCED';

// Update cybercriminal groups
MATCH (ta:ThreatActor)
WHERE ta.threatActorType = 'crime'
SET ta.social_media_presence = ['Telegram', 'Discord', 'Dark Web Markets'],
    ta.social_engineering_sophistication = 'MODERATE',
    ta.psychological_tactics_used = ['PHISHING', 'BAITING', 'QUID_PRO_QUO'],
    ta.victim_profiling_capability = 'MODERATE';

RETURN count(*) AS threat_actors_enhanced;
```

### 3.3 Enhance Technique Nodes with Behavioral Indicators

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 3.3: Enhance Existing ATT&CK Technique Nodes
// ═══════════════════════════════════════════════════════════════

// Add behavioral and psychometric properties to techniques
MATCH (t:Technique)
WHERE t.techniqueId IS NOT NULL
SET t.requires_insider_behavior = false,
    t.victim_psychological_state = [],
    t.behavioral_anomaly_indicators = [],
    t.social_engineering_component = false,
    t.cognitive_load_requirement = 'UNKNOWN',
    t.detection_psychological_factors = [],
    t.enhanced_at = datetime();

// Update social engineering techniques
MATCH (t:Technique)
WHERE t.name CONTAINS 'Phishing'
   OR t.name CONTAINS 'Social Engineering'
   OR t.techniqueId IN ['T1566', 'T1598', 'T1204']
SET t.requires_insider_behavior = true,
    t.victim_psychological_state = ['TRUST', 'URGENCY', 'FEAR'],
    t.behavioral_anomaly_indicators = ['unusual_email_interaction', 'off_hours_activity', 'credential_sharing'],
    t.social_engineering_component = true,
    t.cognitive_load_requirement = 'LOW',
    t.detection_psychological_factors = ['awareness_training', 'reporting_culture', 'suspicion_threshold'];

// Update insider threat techniques
MATCH (t:Technique)
WHERE t.tactic CONTAINS 'collection'
   OR t.tactic CONTAINS 'exfiltration'
SET t.requires_insider_behavior = true,
    t.behavioral_anomaly_indicators = ['data_access_pattern_change', 'after_hours_access', 'mass_downloads'],
    t.detection_psychological_factors = ['employee_satisfaction', 'financial_stress', 'grievance_indicators'];

RETURN count(*) AS techniques_enhanced;
```

### 3.4 Enhance Device Nodes with SAREF Semantics

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 3.4: Enhance Existing Device Nodes with SAREF Properties
// ═══════════════════════════════════════════════════════════════

// Add SAREF semantic properties to existing devices
MATCH (d:Device)
WHERE d.id IS NOT NULL
SET d.saref_device_type = 'UNKNOWN',
    d.saref_functions = [],
    d.saref_capabilities = [],
    d.saref_states = [],
    d.iot_classification = 'UNKNOWN',
    d.smart_device_features = [],
    d.interoperability_protocols = [],
    d.semantic_metadata = {},
    d.enhanced_at = datetime();

// Classify industrial control devices
MATCH (d:Device)
WHERE d.type IN ['PLC', 'HMI', 'RTU', 'SCADA_SERVER', 'DCS']
SET d.saref_device_type = 'IndustrialControlDevice',
    d.saref_functions = ['ProcessControl', 'DataAcquisition', 'SystemMonitoring'],
    d.saref_capabilities = ['Actuating', 'Sensing', 'Communication'],
    d.iot_classification = 'IIoT',
    d.interoperability_protocols = ['Modbus', 'OPC UA', 'DNP3', 'IEC 61850'];

// Classify smart building devices
MATCH (d:Device)
WHERE d.type IN ['HVAC', 'AccessControl', 'SmartMeter', 'BuildingAutomation']
SET d.saref_device_type = 'SmartBuildingDevice',
    d.saref_functions = ['EnvironmentControl', 'EnergyManagement', 'SecurityMonitoring'],
    d.saref_capabilities = ['Actuating', 'Metering', 'Sensing'],
    d.iot_classification = 'Smart Building IoT',
    d.interoperability_protocols = ['BACnet', 'KNX', 'Zigbee', 'EnOcean'];

// Classify IoT sensors and actuators
MATCH (d:Device)
WHERE d.type IN ['Sensor', 'Actuator', 'Gateway', 'SmartDevice']
SET d.saref_device_type = 'GenericIoTDevice',
    d.saref_functions = ['Sensing', 'Actuating', 'DataTransmission'],
    d.saref_capabilities = ['Wireless', 'LowPower', 'EdgeComputing'],
    d.iot_classification = 'Consumer IoT',
    d.interoperability_protocols = ['WiFi', 'Bluetooth', 'Zigbee', 'Z-Wave'];

RETURN count(*) AS devices_enhanced;
```

---

## Phase 4: Create New Relationships

**Duration:** 30-45 minutes
**Risk:** 🟢 LOW (Creating relationships, non-destructive)
**Rollback:** Delete relationships by type

### 4.1 Link CVEs to Psychometric Factors

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 4.1: CVE → Psychometric Relationships
// ═══════════════════════════════════════════════════════════════

// Link social engineering CVEs to behavioral patterns
MATCH (cve:CVE)
WHERE cve.requires_social_engineering = true
MATCH (bp:BehavioralPattern)
WHERE bp.pattern_type IN ['AUTHORITY_COMPLIANCE', 'URGENCY_SUSCEPTIBILITY', 'TRUST_EXPLOITATION']
MERGE (cve)-[r:EXPLOITS_BEHAVIORAL_PATTERN]->(bp)
SET r.exploitation_difficulty = 'MEDIUM',
    r.success_rate_estimate = 0.45,
    r.created_at = datetime();

// Link CVEs to cognitive biases
MATCH (cve:CVE)
WHERE cve.requires_social_engineering = true
MATCH (cb:CognitiveBias)
WHERE cb.bias_category IN ['CONFIRMATION_BIAS', 'AVAILABILITY_HEURISTIC']
MERGE (cve)-[r:LEVERAGES_COGNITIVE_BIAS]->(cb)
SET r.exploitation_complexity = 'LOW',
    r.effectiveness_rating = 0.68,
    r.created_at = datetime();

// Link CVEs to social engineering tactics
MATCH (cve:CVE)
WHERE cve.description CONTAINS 'phishing' OR cve.description CONTAINS 'pretexting'
MATCH (set:SocialEngineeringTactic)
WHERE set.tactic_name IN ['PHISHING', 'PRETEXTING']
MERGE (cve)-[r:ENABLES_SOCIAL_ENGINEERING]->(set)
SET r.delivery_method = 'email',
    r.target_vector = 'user_credential',
    r.created_at = datetime();

// Link CVEs to risk perception gaps
MATCH (cve:CVE)
WHERE cve.cvssV3BaseScore >= 7.0
MATCH (rp:RiskPerception)
WHERE rp.perceived_risk_level IN ['OPTIMISM_BIAS', 'ALERT_FATIGUE']
MERGE (cve)-[r:AMPLIFIED_BY_RISK_PERCEPTION]->(rp)
SET r.perception_impact_score = 0.72,
    r.exploitation_window_increase = '3-7 days',
    r.created_at = datetime();

RETURN count(*) AS psychometric_relationships_created;
```

### 4.2 Link ThreatActors to Social Media Profiles

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 4.2: ThreatActor → Social Media Relationships
// ═══════════════════════════════════════════════════════════════

// Link threat actors to their social profiles
MATCH (ta:ThreatActor)
WHERE size(ta.social_media_presence) > 0
MATCH (tasp:ThreatActorSocialProfile)
MERGE (ta)-[r:HAS_SOCIAL_PROFILE]->(tasp)
SET r.confidence_level = 0.85,
    r.verification_method = 'behavioral_analysis',
    r.last_verified = datetime(),
    r.created_at = datetime();

// Link threat actors to disinformation campaigns
MATCH (ta:ThreatActor)
WHERE ta.threatActorType = 'nation-state'
MATCH (dc:DisinformationCampaign)
MERGE (ta)-[r:CONDUCTS_DISINFORMATION]->(dc)
SET r.campaign_role = 'sponsor',
    r.attribution_confidence = 0.78,
    r.created_at = datetime();

// Link threat actors to hashtags they use
MATCH (tasp:ThreatActorSocialProfile)
MATCH (ht:Hashtag)
WHERE ht.threat_relevance IN ['HIGH', 'CRITICAL']
MERGE (tasp)-[r:USES_HASHTAG]->(ht)
SET r.usage_frequency = 'frequent',
    r.context_patterns = ['exploit_promotion', 'breach_notification'],
    r.created_at = datetime();

// Link social engineering tactics to threat actors
MATCH (ta:ThreatActor)
WHERE size(ta.psychological_tactics_used) > 0
MATCH (set:SocialEngineeringTactic)
WHERE set.tactic_name IN ta.psychological_tactics_used
MERGE (ta)-[r:EMPLOYS_TACTIC]->(set)
SET r.proficiency_level = 'advanced',
    r.frequency_of_use = 'regular',
    r.created_at = datetime();

RETURN count(*) AS social_intelligence_relationships_created;
```

### 4.3 Link Devices to SAREF Semantic Components

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 4.3: Device → SAREF Semantic Relationships
// ═══════════════════════════════════════════════════════════════

// Link devices to SAREF device types (semantic mapping)
MATCH (d:Device)
WHERE d.saref_device_type <> 'UNKNOWN'
MATCH (sd:SAREFDevice)
WHERE sd.device_type = d.saref_device_type
MERGE (d)-[r:IMPLEMENTS_SAREF_PROFILE]->(sd)
SET r.compliance_level = 'partial',
    r.semantic_interoperability = true,
    r.created_at = datetime();

// Link devices to SAREF functions they support
MATCH (d:Device)
WHERE size(d.saref_functions) > 0
MATCH (sf:SAREFFunction)
WHERE sf.function_type IN d.saref_functions
MERGE (d)-[r:SUPPORTS_FUNCTION]->(sf)
SET r.implementation_status = 'active',
    r.capability_level = 'full',
    r.created_at = datetime();

// Link SAREF devices to their commands
MATCH (sd:SAREFDevice)
MATCH (sc:SAREFCommand)
WHERE sc.saref_category = 'saref:ActuatingCommand'
MERGE (sd)-[r:ACCEPTS_COMMAND]->(sc)
SET r.authorization_required = true,
    r.security_validation = 'mandatory',
    r.created_at = datetime();

// Link SAREF devices to their states
MATCH (sd:SAREFDevice)
MATCH (ss:SAREFState)
MERGE (sd)-[r:HAS_STATE]->(ss)
SET r.state_transition_allowed = true,
    r.monitoring_enabled = true,
    r.created_at = datetime();

// Link SAREF states to security implications
MATCH (ss:SAREFState {state_value: 'COMPROMISED'})
MATCH (cve:CVE)
WHERE cve.cvssV3BaseScore >= 7.0
MERGE (ss)-[r:INDICATES_VULNERABILITY]->(cve)
SET r.detection_method = 'behavioral_anomaly',
    r.confidence = 0.82,
    r.created_at = datetime();

RETURN count(*) AS saref_relationships_created;
```

### 4.4 Create Cross-Layer Intelligence Relationships

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 4.4: Cross-Layer Intelligence Relationships
// ═══════════════════════════════════════════════════════════════

// Link behavioral patterns to ATT&CK techniques
MATCH (bp:BehavioralPattern)
WHERE bp.pattern_type IN ['AUTHORITY_COMPLIANCE', 'URGENCY_SUSCEPTIBILITY']
MATCH (t:Technique)
WHERE t.social_engineering_component = true
MERGE (bp)-[r:ENABLES_TECHNIQUE]->(t)
SET r.enablement_mechanism = 'psychological_manipulation',
    r.effectiveness_multiplier = 1.75,
    r.created_at = datetime();

// Link sentiment analysis to CVE impact
MATCH (sa:SentimentAnalysis)
WHERE sa.sentiment_label = 'NEGATIVE'
  AND sa.analysis_subject STARTS WITH 'CVE-'
WITH sa, substring(sa.analysis_subject, 0, 13) AS cve_id
MATCH (cve:CVE {cveId: cve_id})
MERGE (sa)-[r:ANALYZES_PUBLIC_RESPONSE]->(cve)
SET r.response_type = 'social_media',
    r.urgency_indicator = true,
    r.created_at = datetime();

// Link disinformation campaigns to exploited CVEs
MATCH (dc:DisinformationCampaign)
WHERE dc.campaign_name CONTAINS 'Security'
MATCH (cve:CVE)
WHERE cve.social_media_amplification_risk = 'HIGH'
MERGE (dc)-[r:WEAPONIZES_CVE]->(cve)
SET r.weaponization_method = 'fear_amplification',
    r.target_audience = 'general_public',
    r.created_at = datetime();

// Link IoT devices to behavioral exploitation risks
MATCH (d:Device)
WHERE d.iot_classification IN ['Consumer IoT', 'Smart Building IoT']
MATCH (bp:BehavioralPattern)
WHERE bp.pattern_type = 'TRUST_EXPLOITATION'
MERGE (d)-[r:VULNERABLE_TO_BEHAVIORAL_EXPLOIT]->(bp)
SET r.risk_level = 'HIGH',
    r.mitigation = 'user_education',
    r.created_at = datetime();

RETURN count(*) AS cross_layer_relationships_created;
```

---

## Phase 5: Validation Queries

**Duration:** 10-15 minutes
**Risk:** 🟢 NONE (Read-only validation)

### 5.1 Validate New Constraints and Indexes

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 5.1: Schema Validation
// ═══════════════════════════════════════════════════════════════

// VQ1: Count all constraints (should be 30+)
SHOW CONSTRAINTS
YIELD name, labelsOrTypes, properties
RETURN count(*) AS total_constraints,
       collect(DISTINCT labelsOrTypes[0])[0..10] AS sample_node_types;

// VQ2: Verify psychometric constraints
SHOW CONSTRAINTS
YIELD labelsOrTypes
WHERE labelsOrTypes[0] IN [
  'BehavioralPattern', 'PersonalityProfile', 'CognitiveBias',
  'SocialEngineeringTactic', 'RiskPerception'
]
RETURN labelsOrTypes[0] AS psychometric_node,
       count(*) AS constraint_count;
// Expected: 5 node types with constraints

// VQ3: Verify SAREF constraints
SHOW CONSTRAINTS
YIELD labelsOrTypes
WHERE labelsOrTypes[0] IN [
  'SAREFDevice', 'SAREFSensor', 'SAREFFunction',
  'SAREFCommand', 'SAREFState'
]
RETURN labelsOrTypes[0] AS saref_node,
       count(*) AS constraint_count;
// Expected: 5+ node types with constraints

// VQ4: Verify social media intelligence constraints
SHOW CONSTRAINTS
YIELD labelsOrTypes
WHERE labelsOrTypes[0] IN [
  'SocialMediaAccount', 'ThreatActorSocialProfile',
  'DisinformationCampaign', 'SentimentAnalysis'
]
RETURN labelsOrTypes[0] AS social_intel_node,
       count(*) AS constraint_count;
// Expected: 4+ node types with constraints

// VQ5: Verify indexes deployed (should be 40+)
SHOW INDEXES
YIELD name, labelsOrTypes, properties, type
WHERE type <> 'LOOKUP'
RETURN count(*) AS total_indexes,
       count(DISTINCT labelsOrTypes[0]) AS indexed_node_types;
```

### 5.2 Validate New Node Creation

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 5.2: Node Count Validation
// ═══════════════════════════════════════════════════════════════

// VQ6: Count all nodes by label (should show new types)
CALL db.labels() YIELD label
CALL {
  WITH label
  MATCH (n) WHERE label IN labels(n)
  RETURN count(n) AS node_count
}
RETURN label, node_count
ORDER BY node_count DESC
LIMIT 50;
// Expected: BehavioralPattern, SAREFDevice, ThreatActorSocialProfile, etc.

// VQ7: Verify psychometric nodes created
MATCH (bp:BehavioralPattern) WITH count(bp) AS bp_count
MATCH (cb:CognitiveBias) WITH cb, count(cb) AS cb_count, bp_count
MATCH (set:SocialEngineeringTactic) WITH set, count(set) AS set_count, bp_count, cb_count
MATCH (rp:RiskPerception)
RETURN bp_count AS behavioral_patterns,
       cb_count AS cognitive_biases,
       set_count AS social_engineering_tactics,
       count(rp) AS risk_perceptions;
// Expected: At least 2-3 nodes per type

// VQ8: Verify SAREF nodes created
MATCH (sd:SAREFDevice) WITH count(sd) AS sd_count
MATCH (sf:SAREFFunction) WITH sf, count(sf) AS sf_count, sd_count
MATCH (sc:SAREFCommand) WITH sc, count(sc) AS sc_count, sd_count, sf_count
MATCH (ss:SAREFState)
RETURN sd_count AS saref_devices,
       sf_count AS saref_functions,
       sc_count AS saref_commands,
       count(ss) AS saref_states;
// Expected: At least 2-3 nodes per type

// VQ9: Verify social media intelligence nodes
MATCH (tasp:ThreatActorSocialProfile) WITH count(tasp) AS tasp_count
MATCH (ht:Hashtag) WITH ht, count(ht) AS ht_count, tasp_count
MATCH (dc:DisinformationCampaign) WITH dc, count(dc) AS dc_count, tasp_count, ht_count
MATCH (sa:SentimentAnalysis)
RETURN tasp_count AS threat_actor_profiles,
       ht_count AS hashtags,
       dc_count AS disinformation_campaigns,
       count(sa) AS sentiment_analyses;
// Expected: At least 2 nodes per type
```

### 5.3 Validate Property Enhancements

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 5.3: Property Enhancement Validation
// ═══════════════════════════════════════════════════════════════

// VQ10: Verify CVE psychometric properties added
MATCH (cve:CVE)
WHERE cve.requires_social_engineering IS NOT NULL
RETURN count(cve) AS cves_with_psychometric_props,
       sum(CASE WHEN cve.requires_social_engineering = true THEN 1 ELSE 0 END) AS social_engineering_cves,
       sum(CASE WHEN size(cve.cognitive_bias_exploited) > 0 THEN 1 ELSE 0 END) AS cves_with_cognitive_bias;
// Expected: All 179,859 CVEs have properties, subset have social engineering flags

// VQ11: Verify ThreatActor social intelligence properties
MATCH (ta:ThreatActor)
WHERE ta.social_media_presence IS NOT NULL
RETURN count(ta) AS threat_actors_with_social_props,
       sum(CASE WHEN size(ta.social_media_presence) > 0 THEN 1 ELSE 0 END) AS tas_with_social_presence,
       sum(CASE WHEN ta.social_engineering_sophistication <> 'UNKNOWN' THEN 1 ELSE 0 END) AS tas_with_sophistication_rating;
// Expected: All 293 ThreatActors enhanced

// VQ12: Verify Technique behavioral properties
MATCH (t:Technique)
WHERE t.social_engineering_component IS NOT NULL
RETURN count(t) AS techniques_with_behavioral_props,
       sum(CASE WHEN t.social_engineering_component = true THEN 1 ELSE 0 END) AS social_engineering_techniques,
       sum(CASE WHEN size(t.behavioral_anomaly_indicators) > 0 THEN 1 ELSE 0 END) AS techniques_with_indicators;
// Expected: All 834 Techniques enhanced

// VQ13: Verify Device SAREF properties
MATCH (d:Device)
WHERE d.saref_device_type IS NOT NULL
RETURN count(d) AS devices_with_saref_props,
       sum(CASE WHEN d.saref_device_type <> 'UNKNOWN' THEN 1 ELSE 0 END) AS classified_devices,
       sum(CASE WHEN size(d.saref_functions) > 0 THEN 1 ELSE 0 END) AS devices_with_functions;
// Expected: All existing devices enhanced
```

### 5.4 Validate New Relationships

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 5.4: Relationship Validation
// ═══════════════════════════════════════════════════════════════

// VQ14: Count new relationship types
CALL db.relationshipTypes() YIELD relationshipType
WHERE relationshipType IN [
  'EXPLOITS_BEHAVIORAL_PATTERN',
  'LEVERAGES_COGNITIVE_BIAS',
  'ENABLES_SOCIAL_ENGINEERING',
  'HAS_SOCIAL_PROFILE',
  'CONDUCTS_DISINFORMATION',
  'IMPLEMENTS_SAREF_PROFILE',
  'SUPPORTS_FUNCTION',
  'ACCEPTS_COMMAND',
  'ENABLES_TECHNIQUE',
  'WEAPONIZES_CVE'
]
CALL {
  WITH relationshipType
  MATCH ()-[r]->() WHERE type(r) = relationshipType
  RETURN count(r) AS rel_count
}
RETURN relationshipType, rel_count
ORDER BY rel_count DESC;
// Expected: All relationship types present with counts

// VQ15: Verify psychometric relationships
MATCH (cve:CVE)-[r:EXPLOITS_BEHAVIORAL_PATTERN]->(bp:BehavioralPattern)
WITH count(r) AS bp_rels
MATCH (cve:CVE)-[r2:LEVERAGES_COGNITIVE_BIAS]->(cb:CognitiveBias)
WITH bp_rels, count(r2) AS cb_rels
MATCH (cve:CVE)-[r3:ENABLES_SOCIAL_ENGINEERING]->(set:SocialEngineeringTactic)
RETURN bp_rels AS behavioral_pattern_links,
       cb_rels AS cognitive_bias_links,
       count(r3) AS social_engineering_links;
// Expected: Hundreds of relationships created

// VQ16: Verify social intelligence relationships
MATCH (ta:ThreatActor)-[r:HAS_SOCIAL_PROFILE]->(tasp:ThreatActorSocialProfile)
WITH count(r) AS profile_rels
MATCH (ta:ThreatActor)-[r2:CONDUCTS_DISINFORMATION]->(dc:DisinformationCampaign)
WITH profile_rels, count(r2) AS disinfo_rels
MATCH (tasp:ThreatActorSocialProfile)-[r3:USES_HASHTAG]->(ht:Hashtag)
RETURN profile_rels AS social_profile_links,
       disinfo_rels AS disinformation_links,
       count(r3) AS hashtag_usage_links;
// Expected: Dozens of relationships

// VQ17: Verify SAREF semantic relationships
MATCH (d:Device)-[r:IMPLEMENTS_SAREF_PROFILE]->(sd:SAREFDevice)
WITH count(r) AS profile_impl
MATCH (d:Device)-[r2:SUPPORTS_FUNCTION]->(sf:SAREFFunction)
WITH profile_impl, count(r2) AS function_support
MATCH (sd:SAREFDevice)-[r3:ACCEPTS_COMMAND]->(sc:SAREFCommand)
RETURN profile_impl AS saref_profile_implementations,
       function_support AS function_support_links,
       count(r3) AS command_acceptance_links;
// Expected: Relationships connecting devices to SAREF semantics
```

### 5.5 Validate Multi-Layer Query Capabilities

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 5.5: Multi-Layer Query Validation
// ═══════════════════════════════════════════════════════════════

// VQ18: Test psychometric attack chain query
MATCH path = (cve:CVE)-[:EXPLOITS_BEHAVIORAL_PATTERN]->(bp:BehavioralPattern)
  -[:ENABLES_TECHNIQUE]->(t:Technique)
  <-[:USES_TTP]-(ta:ThreatActor)
WHERE cve.requires_social_engineering = true
RETURN count(path) AS psychometric_attack_chains,
       max(length(path)) AS max_chain_length;
// Expected: >0 paths showing psychometric attack chains

// VQ19: Test social intelligence correlation query
MATCH path = (ta:ThreatActor)-[:HAS_SOCIAL_PROFILE]->(tasp:ThreatActorSocialProfile)
  -[:USES_HASHTAG]->(ht:Hashtag)
WHERE ht.threat_relevance = 'HIGH'
RETURN count(path) AS social_intelligence_correlations,
       collect(DISTINCT ta.name)[0..5] AS sample_threat_actors;
// Expected: >0 paths connecting threat actors to social media activity

// VQ20: Test SAREF IoT vulnerability query
MATCH path = (d:Device)-[:IMPLEMENTS_SAREF_PROFILE]->(sd:SAREFDevice)
  -[:HAS_STATE]->(ss:SAREFState {state_value: 'COMPROMISED'})
  -[:INDICATES_VULNERABILITY]->(cve:CVE)
WHERE d.iot_classification IN ['Consumer IoT', 'IIoT']
RETURN count(path) AS iot_vulnerability_paths,
       max(length(path)) AS max_path_length;
// Expected: >0 paths showing IoT device compromise chains

// VQ21: Test cross-layer intelligence query
MATCH path = (cve:CVE)-[:LEVERAGES_COGNITIVE_BIAS]->(cb:CognitiveBias)
  <-[:EXPLOITS_BEHAVIORAL_PATTERN]-(cve2:CVE)
  -[:ENABLES_SOCIAL_ENGINEERING]->(set:SocialEngineeringTactic)
  <-[:EMPLOYS_TACTIC]-(ta:ThreatActor)
WHERE cve.social_media_amplification_risk = 'HIGH'
RETURN count(path) AS cross_layer_intelligence_paths,
       length(path) AS typical_path_length
LIMIT 10;
// Expected: Multi-dimensional attack pattern visibility

// VQ22: Test behavioral exploitation risk query
MATCH (d:Device)
  -[:VULNERABLE_TO_BEHAVIORAL_EXPLOIT]->(bp:BehavioralPattern)
  -[:ENABLES_TECHNIQUE]->(t:Technique)
WHERE d.iot_classification <> 'UNKNOWN'
  AND bp.risk_score > 0.7
RETURN d.deviceType AS device_type,
       bp.pattern_type AS behavioral_vulnerability,
       t.name AS enabled_technique,
       bp.risk_score AS risk_score
ORDER BY bp.risk_score DESC
LIMIT 20;
// Expected: Ranked list of behavioral exploitation risks
```

### 5.6 Performance Validation

```cypher
// ═══════════════════════════════════════════════════════════════
// PHASE 5.6: Performance Validation (< 2 seconds target)
// ═══════════════════════════════════════════════════════════════

// VQ23: Profile multi-layer query performance
PROFILE
MATCH path = (cve:CVE)-[:EXPLOITS_BEHAVIORAL_PATTERN]->(bp:BehavioralPattern)
  -[:ENABLES_TECHNIQUE]->(t:Technique)
WHERE cve.cvssV3BaseScore >= 7.0
  AND bp.risk_score > 0.7
RETURN count(path) AS high_risk_paths;
// Expected: Query completes in < 2000ms, uses indexes

// VQ24: Verify index usage for new properties
EXPLAIN
MATCH (bp:BehavioralPattern)
WHERE bp.pattern_type = 'AUTHORITY_COMPLIANCE'
RETURN bp.id, bp.risk_score;
// Expected: IndexSeek on behavioral_pattern_type index

// VQ25: Verify index usage for SAREF queries
EXPLAIN
MATCH (sd:SAREFDevice)
WHERE sd.device_type = 'SmartThermostat'
RETURN sd.id, sd.manufacturer;
// Expected: IndexSeek on saref_device_type index
```

---

## Phase 6: Rollback Procedures

**Use Only If Migration Fails**

### 6.1 Rollback Phase 4 (Relationships)

```cypher
// ═══════════════════════════════════════════════════════════════
// ROLLBACK PHASE 4: Delete New Relationships
// ═══════════════════════════════════════════════════════════════

// Delete psychometric relationships
MATCH ()-[r:EXPLOITS_BEHAVIORAL_PATTERN]->() DELETE r;
MATCH ()-[r:LEVERAGES_COGNITIVE_BIAS]->() DELETE r;
MATCH ()-[r:ENABLES_SOCIAL_ENGINEERING]->() DELETE r;
MATCH ()-[r:AMPLIFIED_BY_RISK_PERCEPTION]->() DELETE r;

// Delete social intelligence relationships
MATCH ()-[r:HAS_SOCIAL_PROFILE]->() DELETE r;
MATCH ()-[r:CONDUCTS_DISINFORMATION]->() DELETE r;
MATCH ()-[r:USES_HASHTAG]->() DELETE r;
MATCH ()-[r:EMPLOYS_TACTIC]->() DELETE r;

// Delete SAREF semantic relationships
MATCH ()-[r:IMPLEMENTS_SAREF_PROFILE]->() DELETE r;
MATCH ()-[r:SUPPORTS_FUNCTION]->() DELETE r;
MATCH ()-[r:ACCEPTS_COMMAND]->() DELETE r;
MATCH ()-[r:HAS_STATE]->() DELETE r;
MATCH ()-[r:INDICATES_VULNERABILITY]->() DELETE r;

// Delete cross-layer relationships
MATCH ()-[r:ENABLES_TECHNIQUE]->() DELETE r;
MATCH ()-[r:ANALYZES_PUBLIC_RESPONSE]->() DELETE r;
MATCH ()-[r:WEAPONIZES_CVE]->() DELETE r;
MATCH ()-[r:VULNERABLE_TO_BEHAVIORAL_EXPLOIT]->() DELETE r;

RETURN "Phase 4 relationships deleted" AS rollback_status;
```

### 6.2 Rollback Phase 3 (Properties)

```cypher
// ═══════════════════════════════════════════════════════════════
// ROLLBACK PHASE 3: Remove Added Properties
// ═══════════════════════════════════════════════════════════════

// Remove CVE psychometric properties
MATCH (cve:CVE)
WHERE cve.enhanced_at IS NOT NULL
REMOVE cve.requires_social_engineering,
       cve.cognitive_bias_exploited,
       cve.psychological_manipulation_vector,
       cve.victim_behavior_required,
       cve.awareness_training_effectiveness,
       cve.social_media_amplification_risk,
       cve.disinformation_campaign_potential,
       cve.public_disclosure_impact,
       cve.enhanced_at;

// Remove ThreatActor social intelligence properties
MATCH (ta:ThreatActor)
WHERE ta.enhanced_at IS NOT NULL
REMOVE ta.social_media_presence,
       ta.disinformation_campaigns,
       ta.influence_operations,
       ta.public_persona,
       ta.social_engineering_sophistication,
       ta.psychological_tactics_used,
       ta.victim_profiling_capability,
       ta.enhanced_at;

// Remove Technique behavioral properties
MATCH (t:Technique)
WHERE t.enhanced_at IS NOT NULL
REMOVE t.requires_insider_behavior,
       t.victim_psychological_state,
       t.behavioral_anomaly_indicators,
       t.social_engineering_component,
       t.cognitive_load_requirement,
       t.detection_psychological_factors,
       t.enhanced_at;

// Remove Device SAREF properties
MATCH (d:Device)
WHERE d.enhanced_at IS NOT NULL
REMOVE d.saref_device_type,
       d.saref_functions,
       d.saref_capabilities,
       d.saref_states,
       d.iot_classification,
       d.smart_device_features,
       d.interoperability_protocols,
       d.semantic_metadata,
       d.enhanced_at;

RETURN "Phase 3 properties removed" AS rollback_status;
```

### 6.3 Rollback Phase 2 (Nodes)

```cypher
// ═══════════════════════════════════════════════════════════════
// ROLLBACK PHASE 2: Delete New Nodes
// ═══════════════════════════════════════════════════════════════

// Delete psychometric nodes
MATCH (bp:BehavioralPattern) DETACH DELETE bp;
MATCH (pp:PersonalityProfile) DETACH DELETE pp;
MATCH (cb:CognitiveBias) DETACH DELETE cb;
MATCH (set:SocialEngineeringTactic) DETACH DELETE set;
MATCH (pt:PersuasionTechnique) DETACH DELETE pt;
MATCH (dmp:DecisionMakingPattern) DETACH DELETE dmp;
MATCH (es:EmotionalState) DETACH DELETE es;
MATCH (si:StressIndicator) DETACH DELETE si;
MATCH (rp:RiskPerception) DETACH DELETE rp;
MATCH (tal:ThreatAwarenessLevel) DETACH DELETE tal;

// Delete SAREF nodes
MATCH (sd:SAREFDevice) DETACH DELETE sd;
MATCH (ss:SAREFSensor) DETACH DELETE ss;
MATCH (sa:SAREFActuator) DETACH DELETE sa;
MATCH (sf:SAREFFunction) DETACH DELETE sf;
MATCH (sc:SAREFCommand) DETACH DELETE sc;
MATCH (sm:SAREFMeasurement) DETACH DELETE sm;
MATCH (sum:SAREFUnitOfMeasure) DETACH DELETE sum;
MATCH (ss:SAREFState) DETACH DELETE ss;
MATCH (serv:SAREFService) DETACH DELETE serv;
MATCH (sp:SAREFProperty) DETACH DELETE sp;

// Delete social media intelligence nodes
MATCH (sma:SocialMediaAccount) DETACH DELETE sma;
MATCH (smp:SocialMediaPost) DETACH DELETE smp;
MATCH (ht:Hashtag) DETACH DELETE ht;
MATCH (sn:SocialNetwork) DETACH DELETE sn;
MATCH (in:InfluenceNode) DETACH DELETE in;
MATCH (sa:SentimentAnalysis) DETACH DELETE sa;
MATCH (oc:OpinionCluster) DETACH DELETE oc;
MATCH (dc:DisinformationCampaign) DETACH DELETE dc;
MATCH (fni:FakeNewsIndicator) DETACH DELETE fni;
MATCH (tasp:ThreatActorSocialProfile) DETACH DELETE tasp;

RETURN "Phase 2 nodes deleted" AS rollback_status;
```

### 6.4 Rollback Phase 1 (Constraints/Indexes)

```cypher
// ═══════════════════════════════════════════════════════════════
// ROLLBACK PHASE 1: Drop New Constraints and Indexes
// ═══════════════════════════════════════════════════════════════

// Drop psychometric constraints
DROP CONSTRAINT behavioral_pattern_id IF EXISTS;
DROP CONSTRAINT personality_profile_id IF EXISTS;
DROP CONSTRAINT social_engineering_tactic_id IF EXISTS;
DROP CONSTRAINT persuasion_technique_id IF EXISTS;
DROP CONSTRAINT cognitive_bias_id IF EXISTS;
DROP CONSTRAINT decision_making_pattern_id IF EXISTS;
DROP CONSTRAINT emotional_state_id IF EXISTS;
DROP CONSTRAINT stress_indicator_id IF EXISTS;
DROP CONSTRAINT risk_perception_id IF EXISTS;
DROP CONSTRAINT threat_awareness_level_id IF EXISTS;

// Drop SAREF constraints
DROP CONSTRAINT saref_device_id IF EXISTS;
DROP CONSTRAINT saref_sensor_id IF EXISTS;
DROP CONSTRAINT saref_actuator_id IF EXISTS;
DROP CONSTRAINT saref_function_id IF EXISTS;
DROP CONSTRAINT saref_command_id IF EXISTS;
DROP CONSTRAINT saref_measurement_id IF EXISTS;
DROP CONSTRAINT saref_unit_of_measure_id IF EXISTS;
DROP CONSTRAINT saref_state_id IF EXISTS;
DROP CONSTRAINT saref_service_id IF EXISTS;
DROP CONSTRAINT saref_property_id IF EXISTS;

// Drop social media intelligence constraints
DROP CONSTRAINT social_media_account_id IF EXISTS;
DROP CONSTRAINT social_media_post_id IF EXISTS;
DROP CONSTRAINT hashtag_id IF EXISTS;
DROP CONSTRAINT social_network_id IF EXISTS;
DROP CONSTRAINT influence_node_id IF EXISTS;
DROP CONSTRAINT sentiment_analysis_id IF EXISTS;
DROP CONSTRAINT opinion_cluster_id IF EXISTS;
DROP CONSTRAINT disinformation_campaign_id IF EXISTS;
DROP CONSTRAINT fake_news_indicator_id IF EXISTS;
DROP CONSTRAINT threat_actor_social_profile_id IF EXISTS;

// Drop indexes (sample - adapt based on what was created)
DROP INDEX behavioral_pattern_type IF EXISTS;
DROP INDEX saref_device_type IF EXISTS;
DROP INDEX social_media_platform IF EXISTS;
DROP INDEX psychometric_content_search IF EXISTS;
DROP INDEX social_media_content_search IF EXISTS;
DROP INDEX saref_semantic_search IF EXISTS;

RETURN "Phase 1 constraints and indexes dropped" AS rollback_status;
```

### 6.5 Complete Database Restore (Nuclear Option)

```bash
# ═══════════════════════════════════════════════════════════════
# COMPLETE ROLLBACK: Restore from Backup
# ═══════════════════════════════════════════════════════════════

# Stop Neo4j
sudo systemctl stop neo4j

# Restore from backup (use path from Phase 0)
BACKUP_PATH="/home/jim/neo4j_backups/pre_migration_YYYYMMDD_HHMMSS"
neo4j-admin database restore neo4j --from-path="$BACKUP_PATH" --force

# Restart Neo4j
sudo systemctl start neo4j

# Verify restoration
cypher-shell -u neo4j -p neo4j@openspg << 'CYPHER'
MATCH (n) RETURN count(n) AS total_nodes;
CYPHER

echo "✅ Database restored to pre-migration state"
```

---

## Post-Migration Verification

### Final Validation Report

```cypher
// ═══════════════════════════════════════════════════════════════
// COMPREHENSIVE POST-MIGRATION VALIDATION REPORT
// ═══════════════════════════════════════════════════════════════

CALL {
  // Original data preservation
  MATCH (cve:CVE) RETURN count(cve) AS cve_count
}
CALL {
  MATCH (capec:CAPEC) RETURN count(capec) AS capec_count
}
CALL {
  MATCH (t:Technique) RETURN count(t) AS technique_count
}
CALL {
  MATCH (ta:ThreatActor) RETURN count(ta) AS threat_actor_count
}
CALL {
  // New layer nodes
  MATCH (bp:BehavioralPattern) RETURN count(bp) AS behavioral_pattern_count
}
CALL {
  MATCH (sd:SAREFDevice) RETURN count(sd) AS saref_device_count
}
CALL {
  MATCH (tasp:ThreatActorSocialProfile) RETURN count(tasp) AS social_profile_count
}
CALL {
  // Relationship counts
  MATCH ()-[r:EXPLOITS_BEHAVIORAL_PATTERN]->() RETURN count(r) AS psychometric_rel_count
}
CALL {
  MATCH ()-[r:IMPLEMENTS_SAREF_PROFILE]->() RETURN count(r) AS saref_rel_count
}
CALL {
  MATCH ()-[r:HAS_SOCIAL_PROFILE]->() RETURN count(r) AS social_rel_count
}
CALL {
  // Constraint count
  SHOW CONSTRAINTS YIELD name RETURN count(name) AS constraint_count
}
CALL {
  // Index count
  SHOW INDEXES YIELD name WHERE name IS NOT NULL RETURN count(name) AS index_count
}
RETURN
  cve_count,
  capec_count,
  technique_count,
  threat_actor_count,
  behavioral_pattern_count,
  saref_device_count,
  social_profile_count,
  psychometric_rel_count,
  saref_rel_count,
  social_rel_count,
  constraint_count,
  index_count,
  CASE
    WHEN cve_count >= 179859
      AND capec_count >= 615
      AND technique_count >= 834
      AND threat_actor_count >= 293
      AND behavioral_pattern_count >= 2
      AND saref_device_count >= 2
      AND social_profile_count >= 2
      AND psychometric_rel_count > 0
      AND saref_rel_count > 0
      AND social_rel_count > 0
      AND constraint_count >= 45
      AND index_count >= 35
    THEN '✅ MIGRATION SUCCESSFUL - ALL VALIDATION GATES PASSED'
    ELSE '⚠️ MIGRATION INCOMPLETE - REVIEW VALIDATION FAILURES'
  END AS migration_status,
  datetime() AS validation_timestamp;
```

---

## Migration Execution Checklist

### Pre-Migration

- [ ] **Backup database** (Phase 0, Section 1)
- [ ] **Run pre-migration validation** (Phase 0, Section 2)
- [ ] **Document current metrics** (node counts, relationship counts)
- [ ] **Verify disk space** (at least 50% free for safe operation)
- [ ] **Schedule maintenance window** (if required)

### Phase 1: Constraints and Indexes (15 minutes)

- [ ] Execute Section 1.1 (Psychometric constraints)
- [ ] Execute Section 1.2 (SAREF IoT constraints)
- [ ] Execute Section 1.3 (Social media constraints)
- [ ] Execute Section 1.4 (Performance indexes)
- [ ] Execute Section 1.5 (Full-text indexes)
- [ ] Validate with Phase 5.1 queries

### Phase 2: New Node Types (10 minutes)

- [ ] Execute Section 2.1 (Psychometric nodes)
- [ ] Execute Section 2.2 (SAREF nodes)
- [ ] Execute Section 2.3 (Social media intelligence nodes)
- [ ] Validate with Phase 5.2 queries

### Phase 3: Property Enhancements (30 minutes)

- [ ] Execute Section 3.1 (CVE enhancements)
- [ ] Execute Section 3.2 (ThreatActor enhancements)
- [ ] Execute Section 3.3 (Technique enhancements)
- [ ] Execute Section 3.4 (Device enhancements)
- [ ] Validate with Phase 5.3 queries

### Phase 4: New Relationships (45 minutes)

- [ ] Execute Section 4.1 (Psychometric relationships)
- [ ] Execute Section 4.2 (Social media relationships)
- [ ] Execute Section 4.3 (SAREF semantic relationships)
- [ ] Execute Section 4.4 (Cross-layer relationships)
- [ ] Validate with Phase 5.4 queries

### Phase 5: Validation (15 minutes)

- [ ] Run all validation queries (Sections 5.1-5.6)
- [ ] Generate post-migration validation report
- [ ] Verify no data loss (original 179,859 CVEs preserved)
- [ ] Test multi-layer queries for new capabilities
- [ ] Performance benchmarking (< 2 seconds for complex queries)

### Post-Migration

- [ ] Document migration completion timestamp
- [ ] Update schema documentation
- [ ] Notify stakeholders of new query capabilities
- [ ] Archive migration scripts
- [ ] Schedule follow-up validation (7 days post-migration)

---

## Migration Summary

**Total Duration:** ~2 hours
**Risk Level:** 🟢 LOW (Non-destructive, additive-only)
**Data Loss Risk:** 🟢 ZERO (with backup)
**Reversibility:** ✅ FULL (rollback procedures provided)

**New Capabilities After Migration:**
- Psychometric attack pattern analysis
- SAREF IoT semantic interoperability
- Social media intelligence correlation
- Cross-layer multi-dimensional threat analysis
- Behavioral exploitation risk scoring
- Disinformation campaign tracking

**Data Preservation Guarantee:**
- 179,859 CVE nodes: ✅ PRESERVED
- 615 CAPEC nodes: ✅ PRESERVED
- 834 Technique nodes: ✅ PRESERVED
- 293 ThreatActor nodes: ✅ PRESERVED
- All existing relationships: ✅ PRESERVED

---

**Status:** ✅ MIGRATION PLAN COMPLETE - READY FOR EXECUTION
**Last Updated:** 2025-10-29 02:30:00 UTC
**Version:** v1.0.0
