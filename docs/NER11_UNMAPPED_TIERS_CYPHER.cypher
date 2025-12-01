// =============================================================================
// NER11 COMPLETE CYPHER MAPPING - UNMAPPED TIERS (5, 7, 8, 9)
// =============================================================================
// Date: 2025-11-27
// Total Entities: 186
// Tiers: TIER 5 (Behavioral), TIER 7 (Safety/Reliability),
//        TIER 8 (Ontology Frameworks), TIER 9 (Contextual/Meta)
// Super Labels: 16
// =============================================================================

// =============================================================================
// TIER 5: BEHAVIORAL (47 entities)
// =============================================================================

// -----------------------------------------------------------------------------
// Patterns (24 entities) - AttackPattern & Indicator
// -----------------------------------------------------------------------------

// Behavioral Indicators
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Indicator) REQUIRE n.name IS UNIQUE;

MERGE (n:Indicator {name: 'HISTORICAL_PATTERN', indicatorType: 'behavioral_pattern', tier: 5, category: 'behavioral_analysis'});
MERGE (n:Indicator {name: 'PAST_BEHAVIOR', indicatorType: 'historical_behavior', tier: 5, category: 'behavioral_analysis'});
MERGE (n:Indicator {name: 'ORG_BEHAVIOR', indicatorType: 'organizational_behavior', tier: 5, category: 'behavioral_analysis'});
MERGE (n:Indicator {name: 'SECTOR_BEHAVIOR', indicatorType: 'sector_behavior', tier: 5, category: 'behavioral_analysis'});
MERGE (n:Indicator {name: 'SEASONAL_PATTERN', indicatorType: 'temporal_pattern', tier: 5, category: 'temporal_analysis'});
MERGE (n:Indicator {name: 'TIME_BASED_TREND', indicatorType: 'temporal_trend', tier: 5, category: 'temporal_analysis'});
MERGE (n:Indicator {name: 'GEOGRAPHIC_PATTERN', indicatorType: 'geographic_pattern', tier: 5, category: 'geographic_analysis'});

// Attack Patterns
CREATE CONSTRAINT IF NOT EXISTS FOR (n:AttackPattern) REQUIRE n.name IS UNIQUE;

MERGE (n:AttackPattern {name: 'ATTACKER_BEHAVIOR', patternType: 'attacker_behavior', tier: 5, category: 'behavioral_pattern'});
MERGE (n:AttackPattern {name: 'ATTACK_PATTERN', patternType: 'generic_attack_pattern', tier: 5, category: 'behavioral_pattern'});
MERGE (n:AttackPattern {name: 'ATTACK_PATTERNS', patternType: 'generic_attack_pattern', tier: 5, category: 'behavioral_pattern'});
MERGE (n:AttackPattern {name: 'OBSERVABLE_TTP', patternType: 'observable_ttp', tier: 5, category: 'ttp_analysis'});
MERGE (n:AttackPattern {name: 'REGION_SPECIFIC_ATTACK', patternType: 'geographic_specific', tier: 5, category: 'geographic_attack'});
MERGE (n:AttackPattern {name: 'TARGET_SELECTION', patternType: 'targeting_method', tier: 5, category: 'targeting'});
MERGE (n:AttackPattern {name: 'VICTIM_CRITERIA', patternType: 'victim_selection', tier: 5, category: 'targeting'});
MERGE (n:AttackPattern {name: 'PERSISTENCE_METHOD', patternType: 'persistence', tier: 5, category: 'persistence'});
MERGE (n:AttackPattern {name: 'EXFILTRATION_METHOD', patternType: 'exfiltration', tier: 5, category: 'data_exfiltration'});
MERGE (n:AttackPattern {name: 'DATA_THEFT_TECHNIQUE', patternType: 'data_theft', tier: 5, category: 'data_exfiltration'});
MERGE (n:AttackPattern {name: 'DESTRUCTION_METHOD', patternType: 'destruction', tier: 5, category: 'destructive_attack'});
MERGE (n:AttackPattern {name: 'RANSOMWARE_TACTIC', patternType: 'ransomware_behavior', tier: 5, category: 'ransomware'});
MERGE (n:AttackPattern {name: 'SOCIAL_MEDIA_TACTIC', patternType: 'social_media', tier: 5, category: 'social_engineering'});

// Campaigns
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Campaign) REQUIRE n.name IS UNIQUE;

MERGE (n:Campaign {name: 'CAMPAIGN_PATTERN', campaignType: 'pattern_based', tier: 5, category: 'campaign_analysis'});
MERGE (n:Campaign {name: 'MULTI_STAGE_OPERATION', campaignType: 'multi_stage', tier: 5, category: 'complex_campaign'});

// Malware
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Malware) REQUIRE n.name IS UNIQUE;

MERGE (n:Malware {name: 'WIPER', malwareType: 'wiper', tier: 5, category: 'destructive_malware'});

// PsychTrait
CREATE CONSTRAINT IF NOT EXISTS FOR (n:PsychTrait) REQUIRE n.name IS UNIQUE;

MERGE (n:PsychTrait {name: 'SOCIAL_BEHAVIOR', traitType: 'social_behavior', tier: 5, category: 'social_psychology'});

// -----------------------------------------------------------------------------
// Threat Perception (23 entities) - Indicator, Event, EconomicMetric
// -----------------------------------------------------------------------------

// Threat Indicators
MERGE (n:Indicator {name: 'REAL_THREAT', indicatorType: 'real_threat', tier: 5, category: 'threat_perception'});
MERGE (n:Indicator {name: 'ACTUAL_THREAT', indicatorType: 'actual_threat', tier: 5, category: 'threat_perception'});
MERGE (n:Indicator {name: 'IMAGINARY_THREAT', indicatorType: 'imaginary_threat', tier: 5, category: 'threat_perception'});
MERGE (n:Indicator {name: 'PERCEIVED_THREAT', indicatorType: 'perceived_threat', tier: 5, category: 'threat_perception'});
MERGE (n:Indicator {name: 'SYMBOLIC_THREAT', indicatorType: 'symbolic_threat', tier: 5, category: 'threat_perception'});
MERGE (n:Indicator {name: 'CULTURAL_THREAT', indicatorType: 'cultural_threat', tier: 5, category: 'threat_perception'});
MERGE (n:Indicator {name: 'EXISTENTIAL_THREAT', indicatorType: 'existential_threat', tier: 5, category: 'threat_perception'});
MERGE (n:Indicator {name: 'SURVIVAL_THREAT', indicatorType: 'survival_threat', tier: 5, category: 'threat_perception'});
MERGE (n:Indicator {name: 'OPERATIONAL_THREAT', indicatorType: 'operational_threat', tier: 5, category: 'threat_type'});
MERGE (n:Indicator {name: 'OPERATIONS_THREAT', indicatorType: 'operations_threat', tier: 5, category: 'threat_type'});
MERGE (n:Indicator {name: 'REPUTATIONAL_THREAT', indicatorType: 'reputational_threat', tier: 5, category: 'threat_type'});
MERGE (n:Indicator {name: 'FINANCIAL_THREAT', indicatorType: 'financial_threat', tier: 5, category: 'threat_type'});
MERGE (n:Indicator {name: 'COMPLIANCE_THREAT', indicatorType: 'compliance_threat', tier: 5, category: 'threat_type'});
MERGE (n:Indicator {name: 'REGULATORY_RISK', indicatorType: 'regulatory_risk', tier: 5, category: 'threat_type'});
MERGE (n:Indicator {name: 'STRATEGIC_THREAT', indicatorType: 'strategic_threat', tier: 5, category: 'threat_scope'});
MERGE (n:Indicator {name: 'LONG_TERM_THREAT', indicatorType: 'long_term_threat', tier: 5, category: 'threat_scope'});
MERGE (n:Indicator {name: 'TACTICAL_THREAT', indicatorType: 'tactical_threat', tier: 5, category: 'threat_scope'});
MERGE (n:Indicator {name: 'IMMEDIATE_THREAT', indicatorType: 'immediate_threat', tier: 5, category: 'threat_scope'});
MERGE (n:Indicator {name: 'THREAT', indicatorType: 'generic_threat', tier: 5, category: 'threat_generic'});
MERGE (n:Indicator {name: 'RISK', indicatorType: 'risk', tier: 5, category: 'threat_generic'});
MERGE (n:Indicator {name: 'CHALLENGE', indicatorType: 'challenge', tier: 5, category: 'threat_generic'});

// Events
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Event) REQUIRE n.name IS UNIQUE;

MERGE (n:Event {name: 'BRAND_DAMAGE', eventType: 'brand_damage', tier: 5, category: 'reputation_impact'});

// Economic Metrics
CREATE CONSTRAINT IF NOT EXISTS FOR (n:EconomicMetric) REQUIRE n.name IS UNIQUE;

MERGE (n:EconomicMetric {name: 'ECONOMIC_LOSS', metricType: 'economic_loss', tier: 5, category: 'financial_impact'});

// =============================================================================
// TIER 7: SAFETY/RELIABILITY (52 entities)
// =============================================================================

// -----------------------------------------------------------------------------
// RAMS & Hazards (39 entities) - EconomicMetric, Control, Event, Asset, Vulnerability
// -----------------------------------------------------------------------------

// Reliability & Availability Metrics
MERGE (n:EconomicMetric {name: 'RELIABILITY', metricType: 'reliability', tier: 7, category: 'rams_metric'});
MERGE (n:EconomicMetric {name: 'MTBF', metricType: 'mean_time_between_failures', tier: 7, category: 'rams_metric'});
MERGE (n:EconomicMetric {name: 'MTTR', metricType: 'mean_time_to_repair', tier: 7, category: 'rams_metric'});
MERGE (n:EconomicMetric {name: 'FAILURE_RATE', metricType: 'failure_rate', tier: 7, category: 'rams_metric'});
MERGE (n:EconomicMetric {name: 'AVAILABILITY', metricType: 'availability', tier: 7, category: 'rams_metric'});
MERGE (n:EconomicMetric {name: 'UPTIME', metricType: 'uptime', tier: 7, category: 'rams_metric'});
MERGE (n:EconomicMetric {name: 'DOWNTIME', metricType: 'downtime', tier: 7, category: 'rams_metric'});
MERGE (n:EconomicMetric {name: 'MAINTAINABILITY', metricType: 'maintainability', tier: 7, category: 'rams_metric'});
MERGE (n:EconomicMetric {name: 'SAFETY_INTEGRITY_LEVEL', metricType: 'safety_integrity_level', tier: 7, category: 'safety_metric'});
MERGE (n:EconomicMetric {name: 'SIL', metricType: 'sil', tier: 7, category: 'safety_metric'});
MERGE (n:EconomicMetric {name: 'RPN', metricType: 'risk_priority_number', tier: 7, category: 'risk_metric'});
MERGE (n:EconomicMetric {name: 'RISK_SCORE', metricType: 'risk_score', tier: 7, category: 'risk_metric'});

// Safety Controls
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Control) REQUIRE n.name IS UNIQUE;

MERGE (n:Control {name: 'PREVENTIVE_MAINTENANCE', controlType: 'preventive_maintenance', tier: 7, category: 'maintenance'});
MERGE (n:Control {name: 'CORRECTIVE_MAINTENANCE', controlType: 'corrective_maintenance', tier: 7, category: 'maintenance'});
MERGE (n:Control {name: 'SAFETY', controlType: 'safety', tier: 7, category: 'safety_control'});
MERGE (n:Control {name: 'FUNCTIONAL_SAFETY', controlType: 'functional_safety', tier: 7, category: 'safety_control'});
MERGE (n:Control {name: 'REDUNDANCY', controlType: 'redundancy', tier: 7, category: 'reliability_control'});
MERGE (n:Control {name: 'N_PLUS_1', controlType: 'n_plus_1', tier: 7, category: 'reliability_control'});
MERGE (n:Control {name: 'FAIL_SAFE', controlType: 'fail_safe', tier: 7, category: 'safety_control'});
MERGE (n:Control {name: 'SAFETY_CONSIDERATIONS', controlType: 'safety_considerations', tier: 7, category: 'safety_control'});
MERGE (n:Control {name: 'HAZOP', controlType: 'hazop', tier: 7, category: 'hazard_analysis'});
MERGE (n:Control {name: 'GUIDE_WORD', controlType: 'guide_word', tier: 7, category: 'hazard_analysis'});
MERGE (n:Control {name: 'FMEA', controlType: 'fmea', tier: 7, category: 'hazard_analysis'});
MERGE (n:Control {name: 'EFFECT_ANALYSIS', controlType: 'effect_analysis', tier: 7, category: 'hazard_analysis'});
MERGE (n:Control {name: 'LOPA', controlType: 'lopa', tier: 7, category: 'protection_layers'});
MERGE (n:Control {name: 'IPL', controlType: 'independent_protection_layer', tier: 7, category: 'protection_layers'});
MERGE (n:Control {name: 'PROTECTION_LAYER', controlType: 'protection_layer', tier: 7, category: 'protection_layers'});
MERGE (n:Control {name: 'BOW_TIE', controlType: 'bow_tie', tier: 7, category: 'hazard_analysis'});
MERGE (n:Control {name: 'FAULT_TREE', controlType: 'fault_tree_analysis', tier: 7, category: 'hazard_analysis'});
MERGE (n:Control {name: 'MITIGATION', controlType: 'mitigation', tier: 7, category: 'risk_control'});
MERGE (n:Control {name: 'COUNTERMEASURE', controlType: 'countermeasure', tier: 7, category: 'risk_control'});
MERGE (n:Control {name: 'EXISTING_SAFEGUARDS', controlType: 'existing_safeguards', tier: 7, category: 'risk_control'});
MERGE (n:Control {name: 'WHAT_IF', controlType: 'what_if_analysis', tier: 7, category: 'hazard_analysis'});
MERGE (n:Control {name: 'FORMAL_VERIFICATION', controlType: 'formal_verification', tier: 7, category: 'verification'});
MERGE (n:Control {name: 'MODEL_CHECKING', controlType: 'model_checking', tier: 7, category: 'verification'});
MERGE (n:Control {name: 'THEOREM_PROVING', controlType: 'theorem_proving', tier: 7, category: 'verification'});

// Safety Events
MERGE (n:Event {name: 'HAZARD', eventType: 'hazard', tier: 7, category: 'safety_event'});
MERGE (n:Event {name: 'RISK_SCENARIO', eventType: 'risk_scenario', tier: 7, category: 'safety_event'});
MERGE (n:Event {name: 'ACCIDENT', eventType: 'accident', tier: 7, category: 'safety_event'});
MERGE (n:Event {name: 'INCIDENT', eventType: 'incident', tier: 7, category: 'safety_event'});
MERGE (n:Event {name: 'INCIDENT_DETAIL', eventType: 'incident_detail', tier: 7, category: 'safety_event'});
MERGE (n:Event {name: 'INCIDENT_IMPACT', eventType: 'incident_impact', tier: 7, category: 'safety_event'});
MERGE (n:Event {name: 'CONSEQUENCE_LINE', eventType: 'consequence_line', tier: 7, category: 'consequence_analysis'});
MERGE (n:Event {name: 'BASIC_EVENT', eventType: 'basic_event', tier: 7, category: 'fault_tree'});
MERGE (n:Event {name: 'TOP_EVENT', eventType: 'top_event', tier: 7, category: 'fault_tree'});
MERGE (n:Event {name: 'SCENARIO', eventType: 'scenario', tier: 7, category: 'risk_scenario'});
MERGE (n:Event {name: 'IMPACT', eventType: 'impact', tier: 7, category: 'consequence'});
MERGE (n:Event {name: 'CONSEQUENCE', eventType: 'consequence', tier: 7, category: 'consequence'});
MERGE (n:Event {name: 'CONSEQUENCES', eventType: 'consequences', tier: 7, category: 'consequence'});

// Safety Assets
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Asset) REQUIRE n.name IS UNIQUE;

MERGE (n:Asset {name: 'SAFETY_CRITICAL', assetType: 'safety_critical', tier: 7, category: 'critical_system'});
MERGE (n:Asset {name: 'DETERMINISTIC', assetType: 'deterministic_system', tier: 7, category: 'control_system'});
MERGE (n:Asset {name: 'REAL_TIME', assetType: 'real_time_system', tier: 7, category: 'control_system'});
MERGE (n:Asset {name: 'SAFETY_PLC', assetType: 'safety_plc', tier: 7, category: 'control_device'});
MERGE (n:Asset {name: 'SIS', assetType: 'safety_instrumented_system', tier: 7, category: 'safety_system'});
MERGE (n:Asset {name: 'ESD', assetType: 'emergency_shutdown_system', tier: 7, category: 'safety_system'});
MERGE (n:Asset {name: 'TRIP_SYSTEM', assetType: 'trip_system', tier: 7, category: 'safety_system'});

// Vulnerabilities
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Vulnerability) REQUIRE n.name IS UNIQUE;

MERGE (n:Vulnerability {name: 'CYBER_FAILURE_MODE', vulnerabilityType: 'cyber_failure_mode', tier: 7, category: 'cyber_safety'});
MERGE (n:Vulnerability {name: 'FAILURE_MODE', vulnerabilityType: 'failure_mode', tier: 7, category: 'fmea'});

// Indicators
MERGE (n:Indicator {name: 'DEVIATION', indicatorType: 'deviation', tier: 7, category: 'hazop_indicator'});
MERGE (n:Indicator {name: 'RESIDUAL_RISK', indicatorType: 'residual_risk', tier: 7, category: 'risk_indicator'});

// Attack Patterns
MERGE (n:AttackPattern {name: 'THREAT_LINE', patternType: 'threat_line', tier: 7, category: 'bow_tie_analysis'});

// -----------------------------------------------------------------------------
// Deterministic Control (11 entities) - covered above in Asset, Control, EconomicMetric
// -----------------------------------------------------------------------------

MERGE (n:EconomicMetric {name: 'WCET', metricType: 'worst_case_execution_time', tier: 7, category: 'real_time_metric'});
MERGE (n:EconomicMetric {name: 'DEADLINE', metricType: 'deadline', tier: 7, category: 'real_time_metric'});

// =============================================================================
// TIER 8: ONTOLOGY FRAMEWORKS (42 entities)
// =============================================================================

// -----------------------------------------------------------------------------
// IEC 62443 & Security Levels (11 entities) - EconomicMetric, Control
// -----------------------------------------------------------------------------

MERGE (n:EconomicMetric {name: 'SECURITY_LEVEL', metricType: 'security_level', tier: 8, category: 'iec_62443'});
MERGE (n:EconomicMetric {name: 'SL_TARGET', metricType: 'sl_target', tier: 8, category: 'iec_62443'});
MERGE (n:EconomicMetric {name: 'SL_ACHIEVED', metricType: 'sl_achieved', tier: 8, category: 'iec_62443'});
MERGE (n:EconomicMetric {name: 'SL_CAPABILITY', metricType: 'sl_capability', tier: 8, category: 'iec_62443'});

MERGE (n:Control {name: 'FOUNDATIONAL_REQUIREMENT', controlType: 'foundational_requirement', tier: 8, category: 'iec_62443'});
MERGE (n:Control {name: 'FR', controlType: 'fr', tier: 8, category: 'iec_62443'});
MERGE (n:Control {name: 'SYSTEM_REQUIREMENT', controlType: 'system_requirement', tier: 8, category: 'iec_62443'});
MERGE (n:Control {name: 'SR', controlType: 'sr', tier: 8, category: 'iec_62443'});
MERGE (n:Control {name: 'COMPONENT_REQUIREMENT', controlType: 'component_requirement', tier: 8, category: 'iec_62443'});
MERGE (n:Control {name: 'CR', controlType: 'cr', tier: 8, category: 'iec_62443'});
MERGE (n:Control {name: 'IEC_62443', controlType: 'iec_62443', tier: 8, category: 'standard'});

// -----------------------------------------------------------------------------
// Zone & Conduit (2 entities) - Asset
// -----------------------------------------------------------------------------

MERGE (n:Asset {name: 'ZONE_CONDUIT', assetType: 'zone_conduit', tier: 8, category: 'network_segmentation'});
MERGE (n:Asset {name: 'CONDUIT', assetType: 'conduit', tier: 8, category: 'network_segmentation'});

// -----------------------------------------------------------------------------
// Adversary Emulation (10 entities) - Control, ThreatActor, AttackPattern, Event, Indicator
// -----------------------------------------------------------------------------

MERGE (n:Control {name: 'EMULATION_PLAN', controlType: 'emulation_plan', tier: 8, category: 'adversary_emulation'});
MERGE (n:Control {name: 'MICRO_EMULATION_PLAN', controlType: 'micro_emulation_plan', tier: 8, category: 'adversary_emulation'});
MERGE (n:Control {name: 'Adversary Emulation Plan', controlType: 'adversary_emulation_plan', tier: 8, category: 'adversary_emulation'});
MERGE (n:Control {name: 'Micro Emulation Plan', controlType: 'micro_emulation_plan', tier: 8, category: 'adversary_emulation'});

CREATE CONSTRAINT IF NOT EXISTS FOR (n:ThreatActor) REQUIRE n.name IS UNIQUE;

MERGE (n:ThreatActor {name: 'ADVERSARY_PROFILE', actorType: 'adversary_profile', tier: 8, category: 'adversary_emulation'});
MERGE (n:ThreatActor {name: 'Adversary Overview', actorType: 'adversary_overview', tier: 8, category: 'adversary_emulation'});
MERGE (n:ThreatActor {name: 'Adversary Profile', actorType: 'adversary_profile', tier: 8, category: 'adversary_emulation'});

MERGE (n:AttackPattern {name: 'EM3D_TACTIC', patternType: 'em3d_tactic', tier: 8, category: 'em3d'});
MERGE (n:AttackPattern {name: 'EM3D_TECHNIQUE', patternType: 'em3d_technique', tier: 8, category: 'em3d'});
MERGE (n:AttackPattern {name: 'Operational Flow', patternType: 'operational_flow', tier: 8, category: 'adversary_emulation'});

MERGE (n:Event {name: 'ADVERSARY_EMULATION', eventType: 'adversary_emulation', tier: 8, category: 'testing'});
MERGE (n:Event {name: 'Emulation Phases', eventType: 'emulation_phases', tier: 8, category: 'adversary_emulation'});

MERGE (n:Indicator {name: 'Intelligence Summary', indicatorType: 'intelligence_summary', tier: 8, category: 'threat_intelligence'});

// -----------------------------------------------------------------------------
// Ontology Structures (9 entities) - Indicator
// -----------------------------------------------------------------------------

MERGE (n:Indicator {name: 'RELATIONSHIP', indicatorType: 'relationship', tier: 8, category: 'ontology'});
MERGE (n:Indicator {name: 'PROPERTY', indicatorType: 'property', tier: 8, category: 'ontology'});
MERGE (n:Indicator {name: 'CLASS', indicatorType: 'class', tier: 8, category: 'ontology'});
MERGE (n:Indicator {name: 'INSTANCE', indicatorType: 'instance', tier: 8, category: 'ontology'});
MERGE (n:Indicator {name: 'ONTOLOGY_CLASS', indicatorType: 'ontology_class', tier: 8, category: 'ontology'});
MERGE (n:Indicator {name: 'KNOWLEDGE_GRAPH_NODE', indicatorType: 'knowledge_graph_node', tier: 8, category: 'knowledge_graph'});
MERGE (n:Indicator {name: 'KNOWLEDGE_GRAPH_EDGE', indicatorType: 'knowledge_graph_edge', tier: 8, category: 'knowledge_graph'});
MERGE (n:Indicator {name: 'ENTITY_TYPE', indicatorType: 'entity_type', tier: 8, category: 'ontology'});
MERGE (n:Indicator {name: 'RELATED_ENTITIES', indicatorType: 'related_entities', tier: 8, category: 'ontology'});

// -----------------------------------------------------------------------------
// STRIDE & DFD (3 entities) - AttackPattern, Asset
// -----------------------------------------------------------------------------

MERGE (n:AttackPattern {name: 'STRIDE_CATEGORY', patternType: 'stride_category', tier: 8, category: 'stride'});
MERGE (n:AttackPattern {name: 'STRIDE_MAPPING', patternType: 'stride_mapping', tier: 8, category: 'stride'});

MERGE (n:Asset {name: 'DFD_ELEMENT', assetType: 'dfd_element', tier: 8, category: 'data_flow_diagram'});

// -----------------------------------------------------------------------------
// Risk Assessment & Standards (5 entities) - Control, ThreatActor, Asset
// -----------------------------------------------------------------------------

MERGE (n:Control {name: 'RISK_ASSESSMENT', controlType: 'risk_assessment', tier: 8, category: 'risk_management'});
MERGE (n:Control {name: 'NIST_800_53', controlType: 'nist_800_53', tier: 8, category: 'standard'});
MERGE (n:Control {name: 'MIL_STD', controlType: 'mil_std', tier: 8, category: 'standard'});

MERGE (n:Asset {name: 'ASSET', assetType: 'generic_asset', tier: 8, category: 'generic'});

// =============================================================================
// TIER 9: CONTEXTUAL & META (45 entities)
// =============================================================================

// -----------------------------------------------------------------------------
// Contextual Descriptors (9 entities) - Indicator, Event, EconomicMetric
// -----------------------------------------------------------------------------

MERGE (n:Indicator {name: 'CONTEXT', indicatorType: 'context', tier: 9, category: 'metadata'});
MERGE (n:Indicator {name: 'TECHNICAL_CONTEXT', indicatorType: 'technical_context', tier: 9, category: 'metadata'});
MERGE (n:Indicator {name: 'DESCRIPTION', indicatorType: 'description', tier: 9, category: 'metadata'});
MERGE (n:Indicator {name: 'PURPOSE', indicatorType: 'purpose', tier: 9, category: 'metadata'});
MERGE (n:Indicator {name: 'EXAMPLE', indicatorType: 'example', tier: 9, category: 'metadata'});
MERGE (n:Indicator {name: 'REALITY', indicatorType: 'reality', tier: 9, category: 'metadata'});
MERGE (n:Indicator {name: 'DEFINITION', indicatorType: 'definition', tier: 9, category: 'metadata'});
MERGE (n:Indicator {name: 'GOAL', indicatorType: 'goal', tier: 9, category: 'metadata'});

MERGE (n:Event {name: 'OUTCOME', eventType: 'outcome', tier: 9, category: 'result'});

MERGE (n:EconomicMetric {name: 'CALCULATION', metricType: 'calculation', tier: 9, category: 'measurement'});

// -----------------------------------------------------------------------------
// Methodological (3 entities) - Control, Indicator
// -----------------------------------------------------------------------------

MERGE (n:Control {name: 'METHODOLOGY', controlType: 'methodology', tier: 9, category: 'process'});
MERGE (n:Control {name: 'PRINCIPLE', controlType: 'principle', tier: 9, category: 'process'});

// -----------------------------------------------------------------------------
// Techniques & Controls (9 entities) - AttackPattern, Control
// -----------------------------------------------------------------------------

MERGE (n:AttackPattern {name: 'TECHNIQUES', patternType: 'techniques', tier: 9, category: 'generic_technique'});

MERGE (n:Control {name: 'CONTROL', controlType: 'generic_control', tier: 9, category: 'control'});
MERGE (n:Control {name: 'EXISTING_CONTROLS', controlType: 'existing_controls', tier: 9, category: 'control'});
MERGE (n:Control {name: 'NIST_CONTROLS', controlType: 'nist_controls', tier: 9, category: 'control'});
MERGE (n:Control {name: 'ENFORCEMENT', controlType: 'enforcement', tier: 9, category: 'control'});
MERGE (n:Control {name: 'VERIFICATION', controlType: 'verification', tier: 9, category: 'control'});
MERGE (n:Control {name: 'TECHNICAL_CONTROLS', controlType: 'technical_controls', tier: 9, category: 'control'});
MERGE (n:Control {name: 'MITIGATION_STRATEGIES', controlType: 'mitigation_strategies', tier: 9, category: 'mitigation'});
MERGE (n:Control {name: 'MITIGATION_TECHNOLOGY', controlType: 'mitigation_technology', tier: 9, category: 'mitigation'});

// -----------------------------------------------------------------------------
// Implementation & Operations (9 entities) - Event, Control, EconomicMetric
// -----------------------------------------------------------------------------

MERGE (n:Event {name: 'IMPLEMENTATION', eventType: 'implementation', tier: 9, category: 'activity'});
MERGE (n:Event {name: 'OPERATION', eventType: 'operation', tier: 9, category: 'activity'});
MERGE (n:Event {name: 'ACTIVITY', eventType: 'activity', tier: 9, category: 'activity'});
MERGE (n:Event {name: 'ACTION', eventType: 'action', tier: 9, category: 'activity'});
MERGE (n:Event {name: 'TASK', eventType: 'task', tier: 9, category: 'activity'});

MERGE (n:Control {name: 'PROCEDURE', controlType: 'procedure', tier: 9, category: 'process'});
MERGE (n:Control {name: 'PRACTICE', controlType: 'practice', tier: 9, category: 'process'});
MERGE (n:Control {name: 'MITIGATION_IMPLEMENTATION', controlType: 'mitigation_implementation', tier: 9, category: 'mitigation'});

MERGE (n:EconomicMetric {name: 'MITIGATION_EFFECTIVENESS', metricType: 'mitigation_effectiveness', tier: 9, category: 'effectiveness'});

// -----------------------------------------------------------------------------
// Benefits & Effectiveness (5 entities) - EconomicMetric, Event
// -----------------------------------------------------------------------------

MERGE (n:EconomicMetric {name: 'BENEFIT', metricType: 'benefit', tier: 9, category: 'effectiveness'});
MERGE (n:EconomicMetric {name: 'BENEFITS', metricType: 'benefits', tier: 9, category: 'effectiveness'});
MERGE (n:EconomicMetric {name: 'EFFECTIVENESS', metricType: 'effectiveness', tier: 9, category: 'effectiveness'});

MERGE (n:Event {name: 'CYBERSECURITY_IMPACT', eventType: 'cybersecurity_impact', tier: 9, category: 'impact'});
MERGE (n:Event {name: 'CYBERSECURITY_MANIFESTATION', eventType: 'cybersecurity_manifestation', tier: 9, category: 'impact'});

// -----------------------------------------------------------------------------
// Protocol Deployment (10 entities) - Event, Software, Protocol, Indicator, EconomicMetric
// -----------------------------------------------------------------------------

MERGE (n:Event {name: 'PROTOCOL_DEPLOYMENT', eventType: 'protocol_deployment', tier: 9, category: 'deployment'});
MERGE (n:Event {name: 'VENDOR_DEPLOYMENT', eventType: 'vendor_deployment', tier: 9, category: 'deployment'});
MERGE (n:Event {name: 'PROTOCOL_EVOLUTION', eventType: 'protocol_evolution', tier: 9, category: 'evolution'});

CREATE CONSTRAINT IF NOT EXISTS FOR (n:Software) REQUIRE n.name IS UNIQUE;

MERGE (n:Software {name: 'VENDOR_PRODUCT', softwareType: 'vendor_product', tier: 9, category: 'product'});
MERGE (n:Software {name: 'PRODUCT_LINE', softwareType: 'product_line', tier: 9, category: 'product'});

CREATE CONSTRAINT IF NOT EXISTS FOR (n:Protocol) REQUIRE n.name IS UNIQUE;

MERGE (n:Protocol {name: 'PROTOCOL_STANDARD', protocolType: 'protocol_standard', tier: 9, category: 'standard'});
MERGE (n:Protocol {name: 'PROTOCOL_SECTOR', protocolType: 'protocol_sector', tier: 9, category: 'sector'});
MERGE (n:Protocol {name: 'PROTOCOL_MESSAGE', protocolType: 'protocol_message', tier: 9, category: 'message'});

MERGE (n:Indicator {name: 'PROTOCOL_TREND', indicatorType: 'protocol_trend', tier: 9, category: 'trend'});

MERGE (n:EconomicMetric {name: 'PROTOCOL_LATENCY', metricType: 'protocol_latency', tier: 9, category: 'performance'});

// =============================================================================
// VERIFICATION QUERIES
// =============================================================================

// Count by Tier
MATCH (n) WHERE n.tier IN [5, 7, 8, 9]
RETURN n.tier AS tier, labels(n)[0] AS superLabel, COUNT(*) AS count
ORDER BY tier, superLabel;

// Count by Super Label
MATCH (n) WHERE n.tier IN [5, 7, 8, 9]
RETURN labels(n)[0] AS superLabel, COUNT(*) AS total
ORDER BY total DESC;

// Verify all 186 entities
MATCH (n) WHERE n.tier IN [5, 7, 8, 9]
RETURN COUNT(*) AS totalMapped;

// Show sample from each tier
MATCH (n) WHERE n.tier = 5
RETURN n.name, labels(n)[0] AS superLabel, n.tier
LIMIT 5;

MATCH (n) WHERE n.tier = 7
RETURN n.name, labels(n)[0] AS superLabel, n.tier
LIMIT 5;

MATCH (n) WHERE n.tier = 8
RETURN n.name, labels(n)[0] AS superLabel, n.tier
LIMIT 5;

MATCH (n) WHERE n.tier = 9
RETURN n.name, labels(n)[0] AS superLabel, n.tier
LIMIT 5;

// =============================================================================
// END OF CYPHER MAPPING
// =============================================================================
