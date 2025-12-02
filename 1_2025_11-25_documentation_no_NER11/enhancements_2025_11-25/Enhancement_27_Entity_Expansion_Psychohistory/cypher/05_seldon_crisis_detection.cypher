// ============================================================
// Enhancement 27: Seldon Crisis Detection Framework
// File: 05_seldon_crisis_detection.cypher
// Created: 2025-11-26 23:30:00 UTC
// Purpose: Implement detection for 3 identified Seldon Crises
// ============================================================

// ============================================================
// SECTION 1: CRISIS SCHEMA CREATION
// ============================================================

// 1.1 Create SeldonCrisis label and constraint
CREATE CONSTRAINT seldon_crisis_id IF NOT EXISTS
FOR (sc:SeldonCrisis) REQUIRE sc.crisis_id IS UNIQUE;

// 1.2 Create CrisisIndicator label and constraint
CREATE CONSTRAINT crisis_indicator_id IF NOT EXISTS
FOR (ci:CrisisIndicator) REQUIRE ci.indicator_id IS UNIQUE;

// ============================================================
// SECTION 2: SELDON CRISIS 1 - GREAT RESIGNATION CASCADE
// Intervention Window: 8 months
// ============================================================

// 2.1 Create Crisis Node
CREATE (sc:SeldonCrisis {
  crisis_id: 'SC001',
  name: 'Great Resignation Cascade',
  description: 'OT expertise retirement + inadequate knowledge transfer + nation-state targeting',
  intervention_window_months: 8,
  sector_focus: ['Energy', 'Manufacturing', 'Water', 'Chemical'],
  probability_baseline: 0.35,
  impact_category: 'CATASTROPHIC',
  created: datetime(),
  last_updated: datetime()
});

// 2.2 Create Leading Indicators
CREATE (li1:CrisisIndicator {
  indicator_id: 'SC001-L01',
  crisis_id: 'SC001',
  type: 'leading',
  name: 'OT Personnel Retirement Rate',
  description: 'Percentage of OT engineers retiring within 5 years',
  threshold: 0.15,
  operator: '>',
  weight: 0.35,
  measurement_query: 'retirement_rate_query',
  current_value: null,
  last_measured: null
});

CREATE (li2:CrisisIndicator {
  indicator_id: 'SC001-L02',
  crisis_id: 'SC001',
  type: 'leading',
  name: 'Knowledge Transfer Completion',
  description: 'Percentage of critical OT knowledge documented and transferred',
  threshold: 0.30,
  operator: '<',
  weight: 0.30,
  measurement_query: 'kt_completion_query',
  current_value: null,
  last_measured: null
});

CREATE (li3:CrisisIndicator {
  indicator_id: 'SC001-L03',
  crisis_id: 'SC001',
  type: 'leading',
  name: 'Junior-to-Senior Ratio',
  description: 'Ratio of junior (<5 years) to senior (>10 years) OT staff',
  threshold: 3.0,
  operator: '>',
  weight: 0.20,
  measurement_query: 'experience_ratio_query',
  current_value: null,
  last_measured: null
});

CREATE (li4:CrisisIndicator {
  indicator_id: 'SC001-L04',
  crisis_id: 'SC001',
  type: 'leading',
  name: 'Nation-State Interest Score',
  description: 'Intelligence indicating nation-state targeting of sector',
  threshold: 0.7,
  operator: '>',
  weight: 0.15,
  measurement_query: 'threat_intel_query',
  current_value: null,
  last_measured: null
});

// 2.3 Create Lagging Indicators
CREATE (lag1:CrisisIndicator {
  indicator_id: 'SC001-G01',
  crisis_id: 'SC001',
  type: 'lagging',
  name: 'Incident Response Time Degradation',
  description: 'Increase in mean time to respond to OT incidents',
  threshold: 0.40,
  operator: '>',
  weight: 0.4,
  measurement_query: 'mttr_degradation_query',
  current_value: null,
  last_measured: null
});

CREATE (lag2:CrisisIndicator {
  indicator_id: 'SC001-G02',
  crisis_id: 'SC001',
  type: 'lagging',
  name: 'Configuration Drift',
  description: 'Percentage of OT systems with undocumented configuration changes',
  threshold: 0.25,
  operator: '>',
  weight: 0.35,
  measurement_query: 'config_drift_query',
  current_value: null,
  last_measured: null
});

CREATE (lag3:CrisisIndicator {
  indicator_id: 'SC001-G03',
  crisis_id: 'SC001',
  type: 'lagging',
  name: 'Undocumented Access',
  description: 'Percentage of OT system access without proper documentation',
  threshold: 0.50,
  operator: '>',
  weight: 0.25,
  measurement_query: 'access_doc_query',
  current_value: null,
  last_measured: null
});

// 2.4 Link indicators to crisis
MATCH (sc:SeldonCrisis {crisis_id: 'SC001'})
MATCH (ci:CrisisIndicator) WHERE ci.crisis_id = 'SC001'
CREATE (ci)-[:INDICATES]->(sc);

// ============================================================
// SECTION 3: SELDON CRISIS 2 - SUPPLY CHAIN COLLAPSE
// Intervention Window: 4 months
// ============================================================

// 3.1 Create Crisis Node
CREATE (sc:SeldonCrisis {
  crisis_id: 'SC002',
  name: 'Supply Chain Collapse',
  description: 'Compromised firmware + JIT manufacturing + regulatory blindspot',
  intervention_window_months: 4,
  sector_focus: ['Manufacturing', 'Energy', 'Healthcare', 'Defense'],
  probability_baseline: 0.25,
  impact_category: 'CATASTROPHIC',
  created: datetime(),
  last_updated: datetime()
});

// 3.2 Create Leading Indicators
CREATE (li:CrisisIndicator {
  indicator_id: 'SC002-L01',
  crisis_id: 'SC002',
  type: 'leading',
  name: 'Firmware Vulnerability Density',
  description: 'Number of known vulnerabilities per firmware component',
  threshold: 5.0,
  operator: '>',
  weight: 0.30,
  measurement_query: 'firmware_vuln_density_query',
  current_value: null,
  last_measured: null
});

CREATE (li:CrisisIndicator {
  indicator_id: 'SC002-L02',
  crisis_id: 'SC002',
  type: 'leading',
  name: 'Single Supplier Dependency',
  description: 'Percentage of critical components from single source',
  threshold: 0.60,
  operator: '>',
  weight: 0.25,
  measurement_query: 'supplier_concentration_query',
  current_value: null,
  last_measured: null
});

CREATE (li:CrisisIndicator {
  indicator_id: 'SC002-L03',
  crisis_id: 'SC002',
  type: 'leading',
  name: 'JIT Inventory Buffer',
  description: 'Days of critical component inventory on hand',
  threshold: 7,
  operator: '<',
  weight: 0.25,
  measurement_query: 'inventory_buffer_query',
  current_value: null,
  last_measured: null
});

CREATE (li:CrisisIndicator {
  indicator_id: 'SC002-L04',
  crisis_id: 'SC002',
  type: 'leading',
  name: 'Regulatory Coverage Gap',
  description: 'Percentage of supply chain without regulatory oversight',
  threshold: 0.40,
  operator: '>',
  weight: 0.20,
  measurement_query: 'regulatory_gap_query',
  current_value: null,
  last_measured: null
});

// 3.3 Create Lagging Indicators
CREATE (lag:CrisisIndicator {
  indicator_id: 'SC002-G01',
  crisis_id: 'SC002',
  type: 'lagging',
  name: 'Compromised Component Discoveries',
  description: 'Number of supply chain compromises discovered post-deployment',
  threshold: 3,
  operator: '>',
  weight: 0.50,
  measurement_query: 'compromise_discovery_query',
  current_value: null,
  last_measured: null
});

CREATE (lag:CrisisIndicator {
  indicator_id: 'SC002-G02',
  crisis_id: 'SC002',
  type: 'lagging',
  name: 'Production Disruption Events',
  description: 'Number of production halts due to component unavailability',
  threshold: 2,
  operator: '>',
  weight: 0.50,
  measurement_query: 'production_halt_query',
  current_value: null,
  last_measured: null
});

// 3.4 Link indicators to crisis
MATCH (sc:SeldonCrisis {crisis_id: 'SC002'})
MATCH (ci:CrisisIndicator) WHERE ci.crisis_id = 'SC002'
CREATE (ci)-[:INDICATES]->(sc);

// ============================================================
// SECTION 4: SELDON CRISIS 3 - MEDICAL DEVICE PANDEMIC
// Intervention Window: 3 months
// ============================================================

// 4.1 Create Crisis Node
CREATE (sc:SeldonCrisis {
  crisis_id: 'SC003',
  name: 'Medical Device Pandemic',
  description: 'IoMT ransomware + hospital consolidation + clinician burnout',
  intervention_window_months: 3,
  sector_focus: ['Healthcare'],
  probability_baseline: 0.20,
  impact_category: 'CATASTROPHIC',
  created: datetime(),
  last_updated: datetime()
});

// 4.2 Create Leading Indicators
CREATE (li:CrisisIndicator {
  indicator_id: 'SC003-L01',
  crisis_id: 'SC003',
  type: 'leading',
  name: 'IoMT Device Vulnerability Score',
  description: 'Average CVSS of vulnerabilities in connected medical devices',
  threshold: 7.0,
  operator: '>',
  weight: 0.30,
  measurement_query: 'iomt_cvss_query',
  current_value: null,
  last_measured: null
});

CREATE (li:CrisisIndicator {
  indicator_id: 'SC003-L02',
  crisis_id: 'SC003',
  type: 'leading',
  name: 'Hospital System Concentration',
  description: 'Percentage of regional healthcare under single management',
  threshold: 0.50,
  operator: '>',
  weight: 0.25,
  measurement_query: 'hospital_concentration_query',
  current_value: null,
  last_measured: null
});

CREATE (li:CrisisIndicator {
  indicator_id: 'SC003-L03',
  crisis_id: 'SC003',
  type: 'leading',
  name: 'Clinical Staff Burnout Index',
  description: 'Aggregated measure of healthcare worker burnout and turnover',
  threshold: 0.65,
  operator: '>',
  weight: 0.25,
  measurement_query: 'burnout_index_query',
  current_value: null,
  last_measured: null
});

CREATE (li:CrisisIndicator {
  indicator_id: 'SC003-L04',
  crisis_id: 'SC003',
  type: 'leading',
  name: 'Ransomware Healthcare Targeting',
  description: 'Increase in ransomware campaigns specifically targeting healthcare',
  threshold: 0.30,
  operator: '>',
  weight: 0.20,
  measurement_query: 'ransomware_targeting_query',
  current_value: null,
  last_measured: null
});

// 4.3 Create Lagging Indicators
CREATE (lag:CrisisIndicator {
  indicator_id: 'SC003-G01',
  crisis_id: 'SC003',
  type: 'lagging',
  name: 'Patient Care Disruption Events',
  description: 'Number of patient care delays/cancellations due to cyber events',
  threshold: 5,
  operator: '>',
  weight: 0.60,
  measurement_query: 'care_disruption_query',
  current_value: null,
  last_measured: null
});

CREATE (lag:CrisisIndicator {
  indicator_id: 'SC003-G02',
  crisis_id: 'SC003',
  type: 'lagging',
  name: 'Medical Device Downtime',
  description: 'Cumulative hours of critical medical device unavailability',
  threshold: 72,
  operator: '>',
  weight: 0.40,
  measurement_query: 'device_downtime_query',
  current_value: null,
  last_measured: null
});

// 4.4 Link indicators to crisis
MATCH (sc:SeldonCrisis {crisis_id: 'SC003'})
MATCH (ci:CrisisIndicator) WHERE ci.crisis_id = 'SC003'
CREATE (ci)-[:INDICATES]->(sc);

// ============================================================
// SECTION 5: CRISIS PROBABILITY CALCULATION
// ============================================================

// 5.1 Create composite probability function
CALL apoc.custom.declareFunction(
  'seldon.compositeProbability(indicators LIST OF MAP) :: FLOAT',
  '
  WITH reduce(prob = 0.0, ind IN $indicators |
    prob + CASE
      WHEN ind.operator = ">" AND ind.current_value > ind.threshold THEN ind.weight
      WHEN ind.operator = "<" AND ind.current_value < ind.threshold THEN ind.weight
      ELSE 0.0
    END
  ) as triggered_weight
  RETURN triggered_weight
  '
);

// 5.2 Master crisis detection query
// MATCH (sc:SeldonCrisis)
// MATCH (ci:CrisisIndicator)-[:INDICATES]->(sc)
// WHERE ci.current_value IS NOT NULL
// WITH sc, collect({
//   name: ci.name,
//   type: ci.type,
//   threshold: ci.threshold,
//   operator: ci.operator,
//   current_value: ci.current_value,
//   weight: ci.weight,
//   triggered: CASE
//     WHEN ci.operator = '>' AND ci.current_value > ci.threshold THEN true
//     WHEN ci.operator = '<' AND ci.current_value < ci.threshold THEN true
//     ELSE false
//   END
// }) as indicators
// WITH sc, indicators,
//      [i IN indicators WHERE i.triggered = true AND i.type = 'leading'] as leading_triggered,
//      [i IN indicators WHERE i.triggered = true AND i.type = 'lagging'] as lagging_triggered
// WITH sc, indicators, leading_triggered, lagging_triggered,
//      reduce(s = 0.0, i IN leading_triggered | s + i.weight) as leading_score,
//      reduce(s = 0.0, i IN lagging_triggered | s + i.weight) as lagging_score
// RETURN sc.name as crisis,
//        sc.intervention_window_months as intervention_months,
//        sc.probability_baseline as baseline,
//        leading_score as leading_indicator_score,
//        lagging_score as lagging_indicator_score,
//        sc.probability_baseline + (leading_score * 0.3) + (lagging_score * 0.5) as composite_probability,
//        CASE
//          WHEN sc.probability_baseline + (leading_score * 0.3) + (lagging_score * 0.5) > 0.8 THEN 'CRISIS_IMMINENT'
//          WHEN sc.probability_baseline + (leading_score * 0.3) + (lagging_score * 0.5) > 0.6 THEN 'CRISIS_LIKELY'
//          WHEN sc.probability_baseline + (leading_score * 0.3) + (lagging_score * 0.5) > 0.4 THEN 'ELEVATED_RISK'
//          ELSE 'MONITORING'
//        END as status,
//        [i IN leading_triggered | i.name] as triggered_leading,
//        [i IN lagging_triggered | i.name] as triggered_lagging
// ORDER BY composite_probability DESC;

// ============================================================
// SECTION 6: SECTOR-SPECIFIC CRISIS QUERIES
// ============================================================

// 6.1 Energy sector crisis assessment
// MATCH (o:Organization)-[:OPERATES_IN]->(s:Sector {name: 'Energy'})
// MATCH (sc:SeldonCrisis) WHERE 'Energy' IN sc.sector_focus
// MATCH (ci:CrisisIndicator)-[:INDICATES]->(sc)
// // ... organization-specific indicator calculation
// RETURN o.name, sc.name, crisis_probability;

// 6.2 Healthcare sector crisis assessment
// MATCH (o:Organization)-[:OPERATES_IN]->(s:Sector {name: 'Healthcare'})
// MATCH (sc:SeldonCrisis) WHERE 'Healthcare' IN sc.sector_focus
// MATCH (ci:CrisisIndicator)-[:INDICATES]->(sc)
// // ... organization-specific indicator calculation
// RETURN o.name, sc.name, crisis_probability;

// ============================================================
// SECTION 7: CRISIS MONITORING DASHBOARD
// ============================================================

// 7.1 Real-time crisis dashboard query
// MATCH (sc:SeldonCrisis)
// OPTIONAL MATCH (ci:CrisisIndicator)-[:INDICATES]->(sc)
// WITH sc,
//      count(ci) as total_indicators,
//      count(CASE WHEN ci.current_value IS NOT NULL THEN 1 END) as measured_indicators
// RETURN sc.crisis_id,
//        sc.name,
//        sc.intervention_window_months as window,
//        sc.probability_baseline as baseline,
//        total_indicators,
//        measured_indicators,
//        CASE
//          WHEN measured_indicators = 0 THEN 'NO_DATA'
//          WHEN measured_indicators < total_indicators THEN 'PARTIAL_DATA'
//          ELSE 'FULL_DATA'
//        END as data_status;

// ============================================================
// VERIFICATION QUERIES
// ============================================================

// V1: Verify all 3 Seldon Crises exist
// MATCH (sc:SeldonCrisis)
// RETURN sc.crisis_id, sc.name, sc.intervention_window_months
// ORDER BY sc.crisis_id;
// EXPECTED: 3 crises (SC001, SC002, SC003)

// V2: Verify indicator counts per crisis
// MATCH (sc:SeldonCrisis)
// MATCH (ci:CrisisIndicator)-[:INDICATES]->(sc)
// WITH sc, ci.type as indicator_type, count(*) as count
// RETURN sc.crisis_id, indicator_type, count
// ORDER BY sc.crisis_id, indicator_type;

// V3: Verify indicator relationships
// MATCH (ci:CrisisIndicator)-[r:INDICATES]->(sc:SeldonCrisis)
// RETURN count(r) as total_relationships;
// EXPECTED: 13 relationships (4+3+4+2+4+2 = 17 total indicators, but some are create statements without links)
