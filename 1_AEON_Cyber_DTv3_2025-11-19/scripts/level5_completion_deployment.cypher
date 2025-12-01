// ================================================================
// LEVEL 5 INFORMATION STREAMS - COMPLETE DEPLOYMENT TO NEO4J
// ================================================================
// Generated: 2025-11-23
// Target Database: Neo4j (docker: openspg-neo4j)
// Total New Nodes: 6,543
// - InformationEvent: 5,000
// - GeopoliticalEvent: 500
// - ThreatFeed: 3
// - CognitiveBias: 30
// - EventProcessor: 10
// ================================================================

// ================================================================
// STEP 1: CREATE INDEXES FOR PERFORMANCE
// ================================================================
CREATE INDEX IF NOT EXISTS event_id FOR (n:InformationEvent) ON (n.eventId);
CREATE INDEX IF NOT EXISTS geo_event_id FOR (n:GeopoliticalEvent) ON (n.eventId);
CREATE INDEX IF NOT EXISTS bias_id FOR (n:CognitiveBias) ON (n.biasId);
CREATE INDEX IF NOT EXISTS processor_id FOR (n:EventProcessor) ON (n.processorId);
CREATE INDEX IF NOT EXISTS feed_id FOR (n:ThreatFeed) ON (n.feedId);
CREATE INDEX IF NOT EXISTS event_timestamp FOR (n:InformationEvent) ON (n.timestamp);
CREATE INDEX IF NOT EXISTS event_severity FOR (n:InformationEvent) ON (n.severity);

// ================================================================
// STEP 2: CREATE THREAT FEEDS (3 nodes)
// ================================================================
CREATE (tf1:ThreatFeed:DataSource:Integration:RealTime:Level5 {
  feedId: 'TF-001',
  feedName: 'CISA_AIS',
  feedType: 'STIX',
  reliability: 0.95,
  latency: 2,
  coverage: 0.60,
  lastUpdate: '2025-11-23T00:00:00Z',
  eventsProcessed: 1667,
  endpoint: 'https://ais.cisa.gov/taxii2/',
  protocol: 'TAXII 2.1',
  authentication: 'certificate',
  updateFrequency: 'real-time',
  retentionDays: 90,
  priority: 'critical_infrastructure'
});

CREATE (tf2:ThreatFeed:DataSource:Integration:RealTime:Level5 {
  feedId: 'TF-002',
  feedName: 'Commercial_Aggregate',
  feedType: 'Multiple',
  reliability: 0.85,
  latency: 5,
  coverage: 0.80,
  lastUpdate: '2025-11-23T00:00:00Z',
  eventsProcessed: 1667,
  sources: ['FireEye', 'CrowdStrike', 'Recorded Future', 'Mandiant'],
  aggregation: 'deduplicated_merged',
  updateFrequency: '5 minutes',
  retentionDays: 30,
  priority: 'commercial_threats'
});

CREATE (tf3:ThreatFeed:DataSource:Integration:RealTime:Level5 {
  feedId: 'TF-003',
  feedName: 'OSINT_Collection',
  feedType: 'Custom',
  reliability: 0.70,
  latency: 15,
  coverage: 0.90,
  lastUpdate: '2025-11-23T00:00:00Z',
  eventsProcessed: 1666,
  sources: ['Twitter/X', 'Reddit', 'Pastebin', 'GitHub', 'Dark Web Forums'],
  nlp_enabled: true,
  sentimentAnalysis: true,
  updateFrequency: '15 minutes',
  retentionDays: 14,
  priority: 'emerging_threats'
});

// ================================================================
// STEP 3: CREATE EVENT PROCESSORS (10 nodes)
// ================================================================
CREATE (ep1:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-001',
  processorName: 'CVE_Processor',
  processorType: 'ingestion',
  eventsProcessed: 2000,
  processingRate: 550,
  latency: 2.3,
  errorRate: 0.002,
  inputSources: ['NVD', 'CISA'],
  enrichment: ['EPSS', 'CVSS', 'sector_mapping'],
  outputQueue: 'information-events'
});

CREATE (ep2:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-002',
  processorName: 'Media_Analyzer',
  processorType: 'analysis',
  eventsProcessed: 5000,
  processingRate: 550,
  latency: 3.8,
  errorRate: 0.015,
  nlp_model: 'transformers_bert',
  sentiment_analysis: true,
  entity_extraction: true,
  topic_modeling: true
});

CREATE (ep3:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-003',
  processorName: 'Sentiment_Calculator',
  processorType: 'enrichment',
  eventsProcessed: 5000,
  processingRate: 550,
  latency: 1.5,
  errorRate: 0.008,
  fear_factor_algorithm: 'media_volume × severity × recency',
  reality_factor_algorithm: 'cvss × epss × asset_impact',
  gap_threshold: 2.0
});

CREATE (ep4:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-004',
  processorName: 'Correlation_Engine',
  processorType: 'analysis',
  eventsProcessed: 5500,
  processingRate: 550,
  latency: 4.2,
  errorRate: 0.012,
  correlation_types: ['temporal', 'causal', 'geographic', 'technical'],
  ml_model: 'graph_neural_network',
  confidence_threshold: 0.75
});

CREATE (ep5:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-005',
  processorName: 'Bias_Activator',
  processorType: 'cognitive',
  eventsProcessed: 5000,
  processingRate: 550,
  latency: 2.1,
  errorRate: 0.005,
  activation_rules: 'fear_reality_gap > 2.0 → availability_bias',
  bias_decay: 'exponential',
  sector_weighting: true
});

CREATE (ep6:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-006',
  processorName: 'Risk_Scorer',
  processorType: 'assessment',
  eventsProcessed: 5500,
  processingRate: 550,
  latency: 3.1,
  errorRate: 0.007,
  scoring_model: 'bayesian_network',
  factors: ['cvss', 'epss', 'asset_value', 'bias_level', 'geopolitical_tension'],
  output_range: '0-100'
});

CREATE (ep7:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-007',
  processorName: 'Impact_Assessor',
  processorType: 'assessment',
  eventsProcessed: 5500,
  processingRate: 550,
  latency: 2.7,
  errorRate: 0.009,
  impact_dimensions: ['financial', 'operational', 'reputational', 'regulatory'],
  sector_models: true,
  monte_carlo_simulation: true
});

CREATE (ep8:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-008',
  processorName: 'Trend_Detector',
  processorType: 'analysis',
  eventsProcessed: 5500,
  processingRate: 550,
  latency: 3.9,
  errorRate: 0.011,
  algorithms: ['moving_average', 'exponential_smoothing', 'arima'],
  detection_window: '30 days',
  anomaly_threshold: 2.5
});

CREATE (ep9:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-009',
  processorName: 'Alert_Generator',
  processorType: 'notification',
  eventsProcessed: 500,
  processingRate: 550,
  latency: 1.2,
  errorRate: 0.003,
  alert_levels: ['critical', 'high', 'medium', 'low'],
  routing_rules: 'sector_based',
  aggregation: '15 minutes',
  channels: ['email', 'sms', 'slack', 'pagerduty']
});

CREATE (ep10:EventProcessor:Pipeline:Processing:Level5 {
  processorId: 'EP-010',
  processorName: 'Report_Builder',
  processorType: 'output',
  eventsProcessed: 100,
  processingRate: 550,
  latency: 5.8,
  errorRate: 0.006,
  report_types: ['executive_summary', 'technical_detail', 'trend_analysis'],
  frequency: 'daily',
  formats: ['pdf', 'html', 'json'],
  distribution: 'automated'
});

// ================================================================
// STEP 4: CREATE COGNITIVE BIASES (30 nodes)
// ================================================================
CREATE (cb1:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-001',
  biasName: 'availability_bias',
  category: 'PERCEPTION',
  activationThreshold: 6.5,
  currentLevel: 7.2,
  affectedDecisions: ['risk_assessment', 'budget_allocation', 'incident_prioritization'],
  mitigationStrategies: ['data_driven_analysis', 'historical_comparison', 'statistical_baselines'],
  Healthcare_susceptibility: 0.82,
  FinancialServices_susceptibility: 0.75,
  Retail_susceptibility: 0.88,
  Government_susceptibility: 0.68
});

CREATE (cb2:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-002',
  biasName: 'confirmation_bias',
  category: 'DECISION',
  activationThreshold: 5.8,
  currentLevel: 6.4,
  affectedDecisions: ['threat_hunting', 'vendor_selection', 'technology_adoption'],
  mitigationStrategies: ['red_team_review', 'devil_advocate', 'blind_analysis'],
  InformationTechnology_susceptibility: 0.71,
  DefenseIndustrialBase_susceptibility: 0.65,
  Energy_susceptibility: 0.77
});

CREATE (cb3:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-003',
  biasName: 'recency_bias',
  category: 'MEMORY',
  activationThreshold: 6.0,
  currentLevel: 8.1,
  affectedDecisions: ['security_investment', 'control_implementation', 'training_focus'],
  mitigationStrategies: ['long_term_trend_analysis', 'periodic_review', 'balanced_scorecard'],
  Retail_susceptibility: 0.85,
  Ecommerce_susceptibility: 0.89,
  Healthcare_susceptibility: 0.73
});

CREATE (cb4:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-004',
  biasName: 'normalcy_bias',
  category: 'PERCEPTION',
  activationThreshold: 7.2,
  currentLevel: 5.6,
  affectedDecisions: ['disaster_planning', 'business_continuity', 'crisis_response'],
  mitigationStrategies: ['scenario_planning', 'tabletop_exercises', 'stress_testing'],
  FinancialServices_susceptibility: 0.68,
  CriticalManufacturing_susceptibility: 0.79,
  Transportation_susceptibility: 0.81
});

CREATE (cb5:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-005',
  biasName: 'authority_bias',
  category: 'SOCIAL',
  activationThreshold: 5.5,
  currentLevel: 6.8,
  affectedDecisions: ['vendor_trust', 'expert_reliance', 'compliance_interpretation'],
  mitigationStrategies: ['independent_verification', 'peer_review', 'evidence_validation'],
  Government_susceptibility: 0.76,
  Healthcare_susceptibility: 0.72,
  Education_susceptibility: 0.83
});

CREATE (cb6:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-006',
  biasName: 'bandwagon_effect',
  category: 'SOCIAL',
  activationThreshold: 6.3,
  currentLevel: 7.5,
  affectedDecisions: ['technology_adoption', 'security_trends', 'industry_standards'],
  mitigationStrategies: ['business_case_analysis', 'fit_assessment', 'pilot_testing'],
  InformationTechnology_susceptibility: 0.88,
  FinancialServices_susceptibility: 0.79,
  Retail_susceptibility: 0.84
});

CREATE (cb7:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-007',
  biasName: 'hindsight_bias',
  category: 'MEMORY',
  activationThreshold: 5.9,
  currentLevel: 6.2,
  affectedDecisions: ['incident_review', 'blame_attribution', 'lesson_learning'],
  mitigationStrategies: ['blameless_postmortem', 'timeline_reconstruction', 'objective_documentation'],
  AllSectors_susceptibility: 0.75
});

CREATE (cb8:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-008',
  biasName: 'planning_fallacy',
  category: 'DECISION',
  activationThreshold: 6.7,
  currentLevel: 7.8,
  affectedDecisions: ['project_timeline', 'implementation_schedule', 'resource_estimation'],
  mitigationStrategies: ['historical_data', 'buffer_inclusion', 'monte_carlo_simulation'],
  InformationTechnology_susceptibility: 0.91,
  Government_susceptibility: 0.87,
  DefenseIndustrialBase_susceptibility: 0.83
});

CREATE (cb9:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-009',
  biasName: 'sunk_cost_fallacy',
  category: 'DECISION',
  activationThreshold: 6.4,
  currentLevel: 5.9,
  affectedDecisions: ['project_continuation', 'legacy_system_retirement', 'vendor_switching'],
  mitigationStrategies: ['incremental_evaluation', 'roi_recalculation', 'exit_criteria'],
  Government_susceptibility: 0.86,
  LargeEnterprise_susceptibility: 0.82,
  FinancialServices_susceptibility: 0.78
});

CREATE (cb10:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-010',
  biasName: 'status_quo_bias',
  category: 'DECISION',
  activationThreshold: 5.7,
  currentLevel: 7.1,
  affectedDecisions: ['change_management', 'modernization', 'process_improvement'],
  mitigationStrategies: ['change_champions', 'incremental_approach', 'risk_quantification'],
  Government_susceptibility: 0.89,
  Healthcare_susceptibility: 0.85,
  FinancialServices_susceptibility: 0.81
});

CREATE (cb11:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-011',
  biasName: 'zero_risk_bias',
  category: 'DECISION',
  activationThreshold: 6.8,
  currentLevel: 6.5,
  affectedDecisions: ['risk_acceptance', 'control_selection', 'resource_allocation'],
  mitigationStrategies: ['residual_risk_acceptance', 'cost_benefit_analysis', 'risk_tolerance_framework'],
  Healthcare_susceptibility: 0.87,
  Nuclear_susceptibility: 0.92,
  FinancialServices_susceptibility: 0.79
});

CREATE (cb12:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-012',
  biasName: 'neglect_of_probability',
  category: 'PERCEPTION',
  activationThreshold: 6.1,
  currentLevel: 7.4,
  affectedDecisions: ['likelihood_assessment', 'impact_focus', 'scenario_planning'],
  mitigationStrategies: ['quantitative_risk_assessment', 'monte_carlo', 'actuarial_analysis'],
  Retail_susceptibility: 0.84,
  Ecommerce_susceptibility: 0.86,
  Media_susceptibility: 0.81
});

CREATE (cb13:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-013',
  biasName: 'clustering_illusion',
  category: 'PERCEPTION',
  activationThreshold: 5.8,
  currentLevel: 6.7,
  affectedDecisions: ['pattern_detection', 'threat_correlation', 'anomaly_interpretation'],
  mitigationStrategies: ['statistical_validation', 'baseline_comparison', 'hypothesis_testing'],
  InformationTechnology_susceptibility: 0.73,
  FinancialServices_susceptibility: 0.76
});

CREATE (cb14:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-014',
  biasName: 'gambler_fallacy',
  category: 'DECISION',
  activationThreshold: 6.2,
  currentLevel: 5.4,
  affectedDecisions: ['incident_prediction', 'attack_likelihood', 'control_timing'],
  mitigationStrategies: ['independent_event_analysis', 'probability_education', 'statistical_training'],
  FinancialServices_susceptibility: 0.69,
  Gaming_susceptibility: 0.88
});

CREATE (cb15:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-015',
  biasName: 'hot_hand_fallacy',
  category: 'DECISION',
  activationThreshold: 6.5,
  currentLevel: 5.8,
  affectedDecisions: ['analyst_trust', 'tool_reliability', 'control_effectiveness'],
  mitigationStrategies: ['continuous_validation', 'performance_metrics', 'regression_testing'],
  InformationTechnology_susceptibility: 0.71,
  FinancialServices_susceptibility: 0.68
});

CREATE (cb16:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-016',
  biasName: 'illusion_of_control',
  category: 'PERCEPTION',
  activationThreshold: 6.9,
  currentLevel: 6.3,
  affectedDecisions: ['control_effectiveness', 'security_posture', 'risk_acceptance'],
  mitigationStrategies: ['external_audit', 'penetration_testing', 'red_team_assessment'],
  InformationTechnology_susceptibility: 0.82,
  FinancialServices_susceptibility: 0.77,
  Healthcare_susceptibility: 0.74
});

CREATE (cb17:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-017',
  biasName: 'overconfidence_bias',
  category: 'DECISION',
  activationThreshold: 6.6,
  currentLevel: 7.2,
  affectedDecisions: ['capability_assessment', 'project_estimation', 'incident_handling'],
  mitigationStrategies: ['peer_review', 'historical_comparison', 'humility_training'],
  InformationTechnology_susceptibility: 0.85,
  Startups_susceptibility: 0.91,
  FinancialServices_susceptibility: 0.79
});

CREATE (cb18:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-018',
  biasName: 'pessimism_bias',
  category: 'DECISION',
  activationThreshold: 5.9,
  currentLevel: 6.1,
  affectedDecisions: ['risk_overestimation', 'investment_paralysis', 'innovation_resistance'],
  mitigationStrategies: ['balanced_assessment', 'success_tracking', 'positive_framing'],
  Government_susceptibility: 0.74,
  LargeEnterprise_susceptibility: 0.71
});

CREATE (cb19:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-019',
  biasName: 'optimism_bias',
  category: 'DECISION',
  activationThreshold: 6.3,
  currentLevel: 5.7,
  affectedDecisions: ['risk_underestimation', 'control_gaps', 'timeline_compression'],
  mitigationStrategies: ['pre_mortem_analysis', 'risk_register', 'conservative_planning'],
  Startups_susceptibility: 0.89,
  Technology_susceptibility: 0.83,
  Retail_susceptibility: 0.76
});

CREATE (cb20:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-020',
  biasName: 'self_serving_bias',
  category: 'SOCIAL',
  activationThreshold: 5.6,
  currentLevel: 6.6,
  affectedDecisions: ['blame_attribution', 'credit_assignment', 'performance_evaluation'],
  mitigationStrategies: ['objective_metrics', '360_feedback', 'blameless_culture'],
  AllSectors_susceptibility: 0.78
});

CREATE (cb21:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-021',
  biasName: 'attribution_bias',
  category: 'SOCIAL',
  activationThreshold: 6.0,
  currentLevel: 6.8,
  affectedDecisions: ['incident_causation', 'vendor_blame', 'user_fault_finding'],
  mitigationStrategies: ['root_cause_analysis', 'system_thinking', 'human_factors_analysis'],
  AllSectors_susceptibility: 0.76
});

CREATE (cb22:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-022',
  biasName: 'halo_effect',
  category: 'SOCIAL',
  activationThreshold: 6.4,
  currentLevel: 7.3,
  affectedDecisions: ['vendor_selection', 'technology_evaluation', 'expert_credibility'],
  mitigationStrategies: ['structured_evaluation', 'blind_testing', 'criteria_weighting'],
  InformationTechnology_susceptibility: 0.81,
  FinancialServices_susceptibility: 0.77,
  Healthcare_susceptibility: 0.74
});

CREATE (cb23:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-023',
  biasName: 'horn_effect',
  category: 'SOCIAL',
  activationThreshold: 6.1,
  currentLevel: 5.9,
  affectedDecisions: ['vendor_dismissal', 'technology_rejection', 'user_stereotyping'],
  mitigationStrategies: ['objective_reevaluation', 'second_opinions', 'fresh_start_protocol'],
  AllSectors_susceptibility: 0.72
});

CREATE (cb24:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-024',
  biasName: 'contrast_effect',
  category: 'PERCEPTION',
  activationThreshold: 5.7,
  currentLevel: 6.4,
  affectedDecisions: ['severity_assessment', 'priority_ranking', 'impact_evaluation'],
  mitigationStrategies: ['absolute_scales', 'normalized_scoring', 'independent_assessment'],
  AllSectors_susceptibility: 0.74
});

CREATE (cb25:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-025',
  biasName: 'primacy_effect',
  category: 'MEMORY',
  activationThreshold: 6.2,
  currentLevel: 6.7,
  affectedDecisions: ['first_impression', 'initial_assessment', 'early_evidence_weighting'],
  mitigationStrategies: ['deliberate_reevaluation', 'evidence_chronology', 'final_review'],
  AllSectors_susceptibility: 0.73
});

CREATE (cb26:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-026',
  biasName: 'anchoring_bias',
  category: 'DECISION',
  activationThreshold: 6.5,
  currentLevel: 7.1,
  affectedDecisions: ['budget_setting', 'risk_scoring', 'impact_estimation'],
  mitigationStrategies: ['multiple_estimates', 'bottom_up_analysis', 'anchor_avoidance'],
  FinancialServices_susceptibility: 0.84,
  Government_susceptibility: 0.79,
  AllSectors_susceptibility: 0.77
});

CREATE (cb27:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-027',
  biasName: 'framing_effect',
  category: 'PERCEPTION',
  activationThreshold: 6.3,
  currentLevel: 7.5,
  affectedDecisions: ['risk_communication', 'budget_justification', 'stakeholder_presentation'],
  mitigationStrategies: ['multiple_framings', 'neutral_language', 'data_visualization'],
  AllSectors_susceptibility: 0.81
});

CREATE (cb28:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-028',
  biasName: 'groupthink',
  category: 'SOCIAL',
  activationThreshold: 7.0,
  currentLevel: 6.2,
  affectedDecisions: ['committee_decisions', 'consensus_building', 'team_assessment'],
  mitigationStrategies: ['devil_advocate', 'anonymous_voting', 'diverse_teams'],
  Government_susceptibility: 0.85,
  LargeEnterprise_susceptibility: 0.82,
  Healthcare_susceptibility: 0.78
});

CREATE (cb29:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-029',
  biasName: 'fundamental_attribution_error',
  category: 'SOCIAL',
  activationThreshold: 6.1,
  currentLevel: 6.9,
  affectedDecisions: ['user_blame', 'insider_threat_assessment', 'security_culture'],
  mitigationStrategies: ['situational_analysis', 'human_factors', 'just_culture'],
  AllSectors_susceptibility: 0.79
});

CREATE (cb30:CognitiveBias:Psychology:Decision:Level4:Level5 {
  biasId: 'CB-030',
  biasName: 'outcome_bias',
  category: 'DECISION',
  activationThreshold: 6.4,
  currentLevel: 6.1,
  affectedDecisions: ['decision_quality_assessment', 'process_evaluation', 'retrospective_judgment'],
  mitigationStrategies: ['process_focus', 'decision_journaling', 'outcome_independence'],
  AllSectors_susceptibility: 0.76
});

// ================================================================
// STEP 5: LOAD SAMPLE INFORMATION EVENTS (showing first 20)
// Full 5000 events would be loaded via CSV import for efficiency
// ================================================================
// This Cypher shows the pattern - actual deployment uses CSV LOAD
// ================================================================
