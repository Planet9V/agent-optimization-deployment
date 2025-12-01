# Enhancement 08: RAMS (Reliability/Availability/Maintainability/Safety) Framework

**File:** Enhancement_08_RAMS_Reliability/README.md
**Created:** 2025-11-25 14:30:00 UTC
**Version:** v1.0.0
**Status:** ACTIVE
**Purpose:** Comprehensive RAMS discipline integration for equipment reliability modeling, predictive maintenance, and safety-critical system identification in AEON Digital Twin

---

## Executive Summary

The RAMS (Reliability, Availability, Maintainability, Safety) enhancement provides comprehensive reliability engineering capabilities for the AEON Digital Twin platform. This enhancement enables predictive maintenance, failure mode analysis, equipment reliability scoring, and safety-critical system identification across critical infrastructure sectors.

### Key Capabilities
- **Reliability Modeling**: MTBF (Mean Time Between Failures) calculation and prediction
- **Availability Analysis**: System uptime modeling (99.9%, 99.99%, 99.999% targets)
- **Maintainability Optimization**: MTTR (Mean Time To Repair) analysis and improvement
- **Safety Assessment**: Failure mode impact on human safety and operational safety margins
- **Predictive Analytics**: Equipment failure prediction with confidence intervals
- **Maintenance ROI**: Preventive maintenance investment optimization

### McKenney Questions Addressed
- **Q1**: What equipment has highest failure rates? (Reliability scoring)
- **Q7**: What will fail next? (Predictive maintenance with confidence intervals)
- **Q8**: What maintenance investments have best ROI? (Prevent downtime, optimize spend)

---

## 1. RAMS Discipline Overview

### 1.1 Reliability Engineering

**Definition**: The probability that a system will perform its intended function under stated conditions for a specified period.

**Key Metrics**:
```yaml
reliability_metrics:
  mtbf:
    name: "Mean Time Between Failures"
    formula: "Total Operating Time / Number of Failures"
    unit: "hours"
    interpretation: "Higher = More Reliable"

  failure_rate:
    name: "Lambda (λ)"
    formula: "1 / MTBF"
    unit: "failures per hour"
    interpretation: "Lower = More Reliable"

  reliability_function:
    name: "R(t)"
    formula: "e^(-λt)"
    interpretation: "Probability of survival to time t"

  weibull_parameters:
    shape_beta:
      description: "Failure rate behavior"
      infant_mortality: "β < 1"
      random_failures: "β = 1"
      wear_out: "β > 1"
    scale_eta:
      description: "Characteristic life"
      interpretation: "Time at which 63.2% have failed"
```

**Reliability Distributions**:
- **Exponential**: Constant failure rate (electronic components)
- **Weibull**: Aging equipment (mechanical systems)
- **Lognormal**: Fatigue failures (structural components)
- **Normal**: Wear-out dominated (bearings, seals)

### 1.2 Availability Engineering

**Definition**: The proportion of time a system is operational and accessible.

**Availability Levels**:
```yaml
availability_targets:
  standard:
    percentage: 99.0
    downtime_per_year: "3.65 days"
    application: "Non-critical systems"

  high_availability:
    percentage: 99.9
    downtime_per_year: "8.76 hours"
    application: "Business-critical systems"

  very_high:
    percentage: 99.99
    downtime_per_year: "52.56 minutes"
    application: "Mission-critical infrastructure"

  extreme:
    percentage: 99.999
    downtime_per_year: "5.26 minutes"
    application: "Life-safety systems"

  ultra_high:
    percentage: 99.9999
    downtime_per_year: "31.5 seconds"
    application: "Telecom carrier-grade"
```

**Availability Formula**:
```
A = MTBF / (MTBF + MTTR)

Where:
- MTBF = Mean Time Between Failures
- MTTR = Mean Time To Repair
```

**Availability Improvement Strategies**:
1. **Increase MTBF**: Better components, preventive maintenance, operating within design limits
2. **Decrease MTTR**: Spare parts availability, technician training, diagnostic tools
3. **Redundancy**: Parallel systems, hot standby, failover mechanisms
4. **Fault Tolerance**: Graceful degradation, error correction, self-healing

### 1.3 Maintainability Engineering

**Definition**: The ease and speed with which a system can be restored to operational status after a failure.

**Maintainability Metrics**:
```yaml
maintainability_metrics:
  mttr:
    name: "Mean Time To Repair"
    components:
      detection_time: "Time to identify failure"
      diagnosis_time: "Time to determine root cause"
      logistics_time: "Time to obtain parts/resources"
      repair_time: "Time to physically repair"
      verification_time: "Time to test and validate"

  mdt:
    name: "Mean Down Time"
    formula: "MTTR + Administrative Delay + Logistics Delay"

  maintenance_ratio:
    name: "M-Ratio"
    formula: "MTTR / (MTBF + MTTR)"
    interpretation: "Lower = Better Maintainability"

  preventive_maintenance_time:
    name: "PM Duration"
    optimization: "Balance thoroughness vs downtime"
```

**Maintainability Design Principles**:
- **Accessibility**: Easy access to failure-prone components
- **Modularity**: Replaceable units rather than individual components
- **Standardization**: Common parts across equipment types
- **Diagnostics**: Built-in test equipment (BITE) and fault detection
- **Documentation**: Clear maintenance procedures and troubleshooting guides

### 1.4 Safety Engineering

**Definition**: Freedom from unacceptable risk of harm to people, property, or the environment.

**Safety Integrity Levels (SIL)**:
```yaml
safety_integrity_levels:
  sil_1:
    probability_of_failure: "10^-1 to 10^-2"
    description: "Minor injury risk"
    application: "Non-critical equipment"

  sil_2:
    probability_of_failure: "10^-2 to 10^-3"
    description: "Serious injury risk"
    application: "Industrial equipment"

  sil_3:
    probability_of_failure: "10^-3 to 10^-4"
    description: "Multiple fatality risk"
    application: "Critical infrastructure"

  sil_4:
    probability_of_failure: "< 10^-4"
    description: "Catastrophic risk"
    application: "Nuclear, aerospace, high-consequence"
```

**Safety Assessment Methods**:
- **FMEA**: Failure Modes and Effects Analysis
- **FMECA**: FMEA + Criticality Analysis
- **FTA**: Fault Tree Analysis (top-down)
- **ETA**: Event Tree Analysis (bottom-up)
- **HAZOP**: Hazard and Operability Study
- **Bow-Tie**: Combines FTA and ETA

---

## 2. Neo4j Graph Schema for RAMS

### 2.1 Node Labels

```cypher
// Equipment with RAMS properties
CREATE CONSTRAINT equipment_id IF NOT EXISTS
FOR (e:Equipment) REQUIRE e.equipment_id IS UNIQUE;

// RAMS node properties
(:Equipment {
  equipment_id: "EQUIP-001",
  name: "Main Turbine Generator",
  equipment_type: "Rotating Equipment",
  criticality_level: "HIGH",
  safety_classification: "SIL-3",

  // Reliability metrics
  mtbf_hours: 8760.0,
  failure_rate: 0.000114,
  reliability_at_1year: 0.9012,
  weibull_shape: 1.8,
  weibull_scale: 10000.0,

  // Availability metrics
  availability_target: 99.9,
  current_availability: 99.87,
  mttr_hours: 8.5,
  downtime_ytd_hours: 11.4,

  // Maintainability metrics
  maintenance_complexity: "HIGH",
  spare_parts_availability: "GOOD",
  technician_skill_level: "EXPERT",
  pm_interval_days: 90,
  cm_frequency_per_year: 0.2,

  // Safety metrics
  safety_critical: true,
  failure_consequence: "HAZARDOUS",
  protection_layers: 3,
  safety_system_redundancy: "2oo3",

  // Financial impact
  replacement_cost: 2500000.0,
  downtime_cost_per_hour: 15000.0,
  maintenance_cost_per_year: 45000.0,

  // Operational context
  operating_hours_ytd: 8234.5,
  cycles_ytd: 156,
  last_failure_date: "2025-08-15",
  next_pm_date: "2025-12-01",

  created_at: datetime(),
  updated_at: datetime()
})
```

```cypher
// Failure Event nodes
CREATE CONSTRAINT failure_event_id IF NOT EXISTS
FOR (f:FailureEvent) REQUIRE f.failure_id IS UNIQUE;

(:FailureEvent {
  failure_id: "FAIL-20251115-001",
  equipment_id: "EQUIP-001",
  failure_timestamp: datetime("2025-11-15T14:30:00"),

  // Failure characteristics
  failure_mode: "Bearing Seizure",
  failure_cause: "Lubrication System Failure",
  failure_mechanism: "Friction Heat Damage",
  failure_severity: "CRITICAL",

  // Detection and diagnosis
  detection_method: "Vibration Sensor Alarm",
  detection_time_minutes: 5,
  diagnosis_time_minutes: 45,

  // Repair information
  repair_action: "Bearing Replacement",
  repair_time_hours: 6.5,
  logistics_delay_hours: 2.0,
  verification_time_hours: 1.5,
  total_downtime_hours: 10.0,

  // Safety impact
  safety_incident: false,
  personnel_exposed: 0,
  environmental_release: false,

  // Financial impact
  repair_cost: 12500.0,
  lost_production_cost: 150000.0,

  // Root cause analysis
  root_cause: "PM Procedure Not Followed",
  corrective_actions: ["Update PM Checklist", "Technician Retraining"],
  preventable: true,

  created_at: datetime()
})
```

```cypher
// Maintenance Event nodes
CREATE CONSTRAINT maintenance_event_id IF NOT EXISTS
FOR (m:MaintenanceEvent) REQUIRE m.maintenance_id IS UNIQUE;

(:MaintenanceEvent {
  maintenance_id: "MAINT-20251020-001",
  equipment_id: "EQUIP-001",
  maintenance_timestamp: datetime("2025-10-20T08:00:00"),

  // Maintenance type
  maintenance_type: "PREVENTIVE",
  maintenance_category: "Scheduled Inspection",
  maintenance_priority: "ROUTINE",

  // Execution details
  scheduled_duration_hours: 4.0,
  actual_duration_hours: 4.5,
  technicians_assigned: 2,
  cost: 1800.0,

  // Work performed
  tasks_completed: [
    "Bearing Lubrication",
    "Vibration Monitoring",
    "Alignment Check",
    "Temperature Sensor Calibration"
  ],
  parts_replaced: ["Oil Filter", "Shaft Seal"],
  findings: "Minor shaft misalignment corrected",

  // Quality assurance
  quality_check_passed: true,
  supervisor_approved: true,
  documentation_complete: true,

  // Effectiveness
  issues_found: 1,
  issues_resolved: 1,
  follow_up_required: false,

  created_at: datetime()
})
```

```cypher
// Reliability Model nodes
CREATE CONSTRAINT reliability_model_id IF NOT EXISTS
FOR (r:ReliabilityModel) REQUIRE r.model_id IS UNIQUE;

(:ReliabilityModel {
  model_id: "RELMODEL-EQUIP-001",
  equipment_id: "EQUIP-001",
  model_version: "2.1",

  // Distribution parameters
  distribution_type: "WEIBULL",
  weibull_shape_beta: 1.8,
  weibull_scale_eta: 10000.0,
  location_gamma: 0.0,

  // Statistical fit
  sample_size: 45,
  data_start_date: "2020-01-01",
  data_end_date: "2025-11-15",
  goodness_of_fit_r_squared: 0.94,
  anderson_darling_statistic: 0.32,

  // Confidence intervals
  mtbf_lower_95: 7890.0,
  mtbf_point_estimate: 8760.0,
  mtbf_upper_95: 9630.0,

  // Predictions
  reliability_at_500h: 0.9875,
  reliability_at_1000h: 0.9750,
  reliability_at_5000h: 0.8950,
  reliability_at_8760h: 0.8012,

  // Model metadata
  model_created_date: "2025-11-01",
  model_created_by: "Reliability Engineering Team",
  validation_status: "VALIDATED",
  next_review_date: "2026-05-01",

  created_at: datetime(),
  updated_at: datetime()
})
```

```cypher
// Safety Analysis nodes
CREATE CONSTRAINT safety_analysis_id IF NOT EXISTS
FOR (s:SafetyAnalysis) REQUIRE s.analysis_id IS UNIQUE;

(:SafetyAnalysis {
  analysis_id: "SAFETY-EQUIP-001",
  equipment_id: "EQUIP-001",
  analysis_date: "2025-06-15",

  // Safety classification
  safety_integrity_level: "SIL-3",
  consequence_category: "HAZARDOUS",
  likelihood_category: "REMOTE",
  risk_priority_number: 48,

  // Failure mode analysis
  critical_failure_modes: [
    "Overspeed Condition",
    "Shaft Failure",
    "Bearing Seizure"
  ],
  failure_effects: [
    "Equipment Damage",
    "Personnel Hazard",
    "Production Loss"
  ],

  // Protection layers
  protection_layer_1: "Automatic Shutdown System",
  protection_layer_2: "Emergency Stop Circuit",
  protection_layer_3: "Manual Isolation Valves",
  protection_layer_4: "Physical Barriers",

  // Safety system architecture
  voting_architecture: "2oo3",
  redundancy_level: "TRIPLE_MODULAR",
  common_cause_beta: 0.05,

  // Probability calculations
  pfd_avg: 0.0001,
  sif_failure_rate: 0.0000114,
  dangerous_failure_probability: 0.00005,

  // Human factors
  human_error_probability: 0.001,
  operator_response_time_seconds: 30,
  alarm_management_burden: "MODERATE",

  // Compliance
  standards_compliance: ["IEC 61508", "IEC 61511", "ISO 13849"],
  last_safety_audit_date: "2025-05-01",
  next_safety_audit_date: "2026-05-01",
  audit_findings: 0,

  created_at: datetime(),
  updated_at: datetime()
})
```

### 2.2 Relationship Types

```cypher
// Equipment failure relationships
CREATE (e:Equipment {equipment_id: "EQUIP-001"})
CREATE (f:FailureEvent {failure_id: "FAIL-20251115-001"})
CREATE (e)-[:EXPERIENCED_FAILURE {
  failure_number: 12,
  operating_hours_at_failure: 8100.0,
  time_since_last_failure_hours: 720.0,
  time_since_last_pm_hours: 480.0,
  failure_unexpected: true,
  detection_latency_minutes: 5,
  safety_incident_reported: false
}]->(f);

// Equipment maintenance relationships
CREATE (e:Equipment {equipment_id: "EQUIP-001"})
CREATE (m:MaintenanceEvent {maintenance_id: "MAINT-20251020-001"})
CREATE (e)-[:RECEIVED_MAINTENANCE {
  maintenance_number: 45,
  operating_hours_at_maintenance: 7620.0,
  time_since_last_maintenance_hours: 720.0,
  on_schedule: true,
  effectiveness_rating: "GOOD"
}]->(m);

// Equipment reliability model relationships
CREATE (e:Equipment {equipment_id: "EQUIP-001"})
CREATE (r:ReliabilityModel {model_id: "RELMODEL-EQUIP-001"})
CREATE (e)-[:HAS_RELIABILITY_MODEL {
  model_version: "2.1",
  confidence_level: "HIGH",
  validated_date: "2025-11-01",
  applicable_from: "2025-11-01",
  applicable_to: "2026-05-01"
}]->(r);

// Equipment safety analysis relationships
CREATE (e:Equipment {equipment_id: "EQUIP-001"})
CREATE (s:SafetyAnalysis {analysis_id: "SAFETY-EQUIP-001"})
CREATE (e)-[:HAS_SAFETY_ANALYSIS {
  analysis_version: "3.0",
  risk_level: "MEDIUM",
  mitigation_status: "ADEQUATE",
  review_frequency_months: 12
}]->(s);

// Failure causation relationships
CREATE (f1:FailureEvent {failure_id: "FAIL-20251115-001"})
CREATE (f2:FailureEvent {failure_id: "FAIL-20250815-002"})
CREATE (f1)-[:CAUSED_BY {
  causal_relationship: "DIRECT",
  time_lag_hours: 2160.0,
  causal_factor: "Degraded Lubrication from Prior Event"
}]->(f2);

// Maintenance effectiveness relationships
CREATE (m:MaintenanceEvent {maintenance_id: "MAINT-20251020-001"})
CREATE (f:FailureEvent {failure_id: "FAIL-20251115-001"})
CREATE (m)-[:PREVENTED_FAILURE {
  prevention_confidence: "MEDIUM",
  time_to_potential_failure_hours: 240.0,
  cost_avoidance: 75000.0
}]->(f)
WHERE NOT (f)-[:OCCURRED]->(); // Only if failure didn't actually occur

// System dependency relationships for availability
CREATE (e1:Equipment {equipment_id: "EQUIP-001"})
CREATE (e2:Equipment {equipment_id: "EQUIP-002"})
CREATE (e1)-[:DEPENDS_ON {
  dependency_type: "SERIAL",
  availability_impact: "MULTIPLICATIVE",
  redundancy_available: false,
  criticality: "HIGH"
}]->(e2);

// Spare parts relationships for maintainability
CREATE (e:Equipment {equipment_id: "EQUIP-001"})
CREATE (p:SparePart {part_id: "PART-12345"})
CREATE (e)-[:REQUIRES_SPARE_PART {
  criticality: "CRITICAL",
  stock_quantity: 2,
  lead_time_days: 45,
  cost: 25000.0,
  failure_probability_per_year: 0.15
}]->(p);
```

### 2.3 Graph Patterns for RAMS Analysis

```cypher
// Pattern 1: Reliability degradation detection
MATCH (e:Equipment)-[f:EXPERIENCED_FAILURE]->(fail:FailureEvent)
WITH e,
     collect(fail.failure_timestamp) AS failure_times,
     collect(duration.between(lag(fail.failure_timestamp, 1) OVER (ORDER BY fail.failure_timestamp), fail.failure_timestamp)) AS inter_failure_times
WHERE size(failure_times) >= 5
WITH e,
     reduce(s = 0.0, t IN inter_failure_times[0..3] | s + duration.inSeconds(t)) / 3.0 AS early_mtbf,
     reduce(s = 0.0, t IN inter_failure_times[-3..] | s + duration.inSeconds(t)) / 3.0 AS recent_mtbf
WHERE recent_mtbf < early_mtbf * 0.7  // 30% degradation
RETURN e.equipment_id,
       early_mtbf / 3600.0 AS early_mtbf_hours,
       recent_mtbf / 3600.0 AS recent_mtbf_hours,
       (early_mtbf - recent_mtbf) / early_mtbf * 100 AS degradation_percent
ORDER BY degradation_percent DESC;

// Pattern 2: Availability bottleneck identification
MATCH path = (sys:System)-[:CONTAINS*]->(e:Equipment)
WITH sys, e,
     e.mtbf_hours AS mtbf,
     e.mttr_hours AS mttr,
     mtbf / (mtbf + mttr) AS availability
WHERE availability < 0.999  // Below 99.9% target
WITH sys,
     collect({
       equipment: e.equipment_id,
       availability: availability,
       mtbf: mtbf,
       mttr: mttr,
       availability_loss_per_year: (1 - availability) * 8760
     }) AS equipment_list
RETURN sys.system_id,
       [eq IN equipment_list | eq.equipment] AS bottleneck_equipment,
       reduce(total = 1.0, eq IN equipment_list | total * eq.availability) AS system_availability,
       reduce(total = 0.0, eq IN equipment_list | total + eq.availability_loss_per_year) AS total_downtime_hours_per_year
ORDER BY system_availability ASC;

// Pattern 3: Predictive maintenance prioritization
MATCH (e:Equipment)-[:HAS_RELIABILITY_MODEL]->(r:ReliabilityModel)
WITH e, r,
     (duration.inHours(datetime() - datetime(e.last_failure_date))) AS hours_since_failure,
     exp(-hours_since_failure / r.weibull_scale_eta) AS current_reliability,
     (r.weibull_shape_beta / r.weibull_scale_eta) *
     ((hours_since_failure / r.weibull_scale_eta)^(r.weibull_shape_beta - 1)) AS current_hazard_rate
WHERE current_reliability < 0.90  // Below 90% reliability
WITH e, r, hours_since_failure, current_reliability, current_hazard_rate,
     e.downtime_cost_per_hour * e.mttr_hours AS failure_cost,
     e.maintenance_cost_per_year / (8760.0 / e.pm_interval_days / 30.0) AS pm_cost
RETURN e.equipment_id,
       e.name,
       hours_since_failure,
       round(current_reliability * 100, 2) AS reliability_percent,
       round(current_hazard_rate * 1000000, 2) AS hazard_rate_per_million_hours,
       round((1 - current_reliability) * failure_cost, 0) AS expected_failure_cost,
       round(pm_cost, 0) AS pm_cost,
       round((1 - current_reliability) * failure_cost - pm_cost, 0) AS net_benefit_of_pm
ORDER BY net_benefit_of_pm DESC
LIMIT 20;

// Pattern 4: Safety-critical system monitoring
MATCH (e:Equipment)-[:HAS_SAFETY_ANALYSIS]->(s:SafetyAnalysis)
WHERE s.safety_integrity_level IN ["SIL-3", "SIL-4"]
  AND e.current_availability < e.availability_target / 100.0
WITH e, s,
     (e.availability_target / 100.0 - e.current_availability) AS availability_gap,
     s.pfd_avg AS probability_of_failure_on_demand
MATCH (e)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
WHERE f.failure_timestamp > datetime() - duration({days: 365})
WITH e, s, availability_gap, probability_of_failure_on_demand,
     count(f) AS failures_last_year
WHERE failures_last_year > 1  // More than expected for SIL-3/4
RETURN e.equipment_id,
       e.name,
       s.safety_integrity_level,
       s.consequence_category,
       failures_last_year,
       round(e.current_availability * 100, 3) AS current_availability_percent,
       round(e.availability_target, 3) AS target_availability_percent,
       round(availability_gap * 100, 3) AS availability_gap_percent,
       probability_of_failure_on_demand,
       "URGENT REVIEW REQUIRED" AS action
ORDER BY probability_of_failure_on_demand DESC;

// Pattern 5: Maintenance effectiveness analysis
MATCH (e:Equipment)-[rm:RECEIVED_MAINTENANCE]->(m:MaintenanceEvent)
WHERE m.maintenance_type = "PREVENTIVE"
  AND m.maintenance_timestamp > datetime() - duration({days: 365})
OPTIONAL MATCH (e)-[rf:EXPERIENCED_FAILURE]->(f:FailureEvent)
WHERE f.failure_timestamp > m.maintenance_timestamp
  AND f.failure_timestamp < m.maintenance_timestamp + duration({hours: e.pm_interval_days * 24})
WITH e, m,
     CASE WHEN f IS NULL THEN 1 ELSE 0 END AS pm_prevented_failure,
     e.downtime_cost_per_hour * e.mttr_hours AS avoided_cost
WITH e,
     count(m) AS pm_events,
     sum(pm_prevented_failure) AS successful_preventions,
     sum(m.cost) AS total_pm_cost,
     sum(CASE WHEN f IS NULL THEN avoided_cost ELSE 0 END) AS total_avoided_cost
RETURN e.equipment_id,
       e.name,
       pm_events,
       successful_preventions,
       round(successful_preventions * 1.0 / pm_events * 100, 1) AS pm_effectiveness_percent,
       round(total_pm_cost, 0) AS total_pm_cost,
       round(total_avoided_cost, 0) AS total_avoided_cost,
       round((total_avoided_cost - total_pm_cost) / total_pm_cost, 2) AS pm_roi
ORDER BY pm_roi DESC;
```

---

## 3. RAMS Analysis Workflows

### 3.1 Reliability Analysis Workflow

**Objective**: Calculate equipment reliability metrics and build predictive models.

**Steps**:

1. **Data Collection**:
   - Historical failure timestamps
   - Operating hours at each failure
   - Environmental conditions during operation
   - Maintenance history

2. **Failure Data Processing**:
   ```cypher
   // Calculate inter-failure times
   MATCH (e:Equipment)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
   WITH e, collect(f ORDER BY f.failure_timestamp) AS failures
   UNWIND range(0, size(failures)-2) AS i
   WITH e,
        failures[i] AS f1,
        failures[i+1] AS f2,
        duration.inHours(failures[i+1].failure_timestamp, failures[i].failure_timestamp) AS inter_failure_hours
   RETURN e.equipment_id,
          avg(inter_failure_hours) AS mtbf,
          stdev(inter_failure_hours) AS mtbf_stdev,
          count(*) AS failure_count;
   ```

3. **Distribution Fitting**:
   - Test exponential, Weibull, lognormal, normal distributions
   - Calculate Anderson-Darling goodness-of-fit
   - Select best-fit distribution
   - Estimate distribution parameters with confidence intervals

4. **Reliability Function Calculation**:
   ```python
   import numpy as np
   from scipy.stats import weibull_min

   def calculate_reliability(t, shape, scale):
       """Calculate Weibull reliability at time t"""
       return weibull_min.sf(t, shape, scale=scale)

   def calculate_mtbf(shape, scale):
       """Calculate MTBF for Weibull distribution"""
       from scipy.special import gamma
       return scale * gamma(1 + 1/shape)

   def calculate_hazard_rate(t, shape, scale):
       """Calculate instantaneous hazard rate"""
       return (shape / scale) * (t / scale)**(shape - 1)
   ```

5. **Prediction and Forecasting**:
   - Reliability at future time points
   - Remaining useful life estimation
   - Confidence intervals for predictions
   - Monte Carlo simulation for uncertainty quantification

6. **Update Neo4j with Results**:
   ```cypher
   MATCH (e:Equipment {equipment_id: $equipment_id})
   MERGE (r:ReliabilityModel {model_id: "RELMODEL-" + $equipment_id})
   SET r.distribution_type = $distribution_type,
       r.weibull_shape_beta = $shape,
       r.weibull_scale_eta = $scale,
       r.mtbf_point_estimate = $mtbf,
       r.mtbf_lower_95 = $mtbf_lower,
       r.mtbf_upper_95 = $mtbf_upper,
       r.goodness_of_fit_r_squared = $r_squared,
       r.updated_at = datetime()
   MERGE (e)-[:HAS_RELIABILITY_MODEL]->(r);
   ```

### 3.2 Availability Analysis Workflow

**Objective**: Calculate system and equipment availability, identify bottlenecks.

**Steps**:

1. **Component Availability Calculation**:
   ```cypher
   MATCH (e:Equipment)
   WITH e,
        e.mtbf_hours AS mtbf,
        e.mttr_hours AS mttr,
        mtbf / (mtbf + mttr) AS inherent_availability,
        e.downtime_ytd_hours AS actual_downtime,
        e.operating_hours_ytd + e.downtime_ytd_hours AS total_time
   SET e.current_availability = 1.0 - (actual_downtime / total_time),
       e.inherent_availability = inherent_availability
   RETURN e.equipment_id,
          round(inherent_availability * 100, 3) AS inherent_avail_percent,
          round(e.current_availability * 100, 3) AS actual_avail_percent;
   ```

2. **System Availability Modeling**:
   ```cypher
   // Series system availability (all components must work)
   MATCH path = (s:System)-[:CONTAINS*]->(e:Equipment)
   WHERE s.system_id = $system_id
   WITH s, collect(DISTINCT e) AS components
   WITH s,
        reduce(avail = 1.0, e IN components |
               avail * (e.mtbf_hours / (e.mtbf_hours + e.mttr_hours))) AS series_availability
   RETURN s.system_id,
          round(series_availability * 100, 4) AS availability_percent,
          round((1 - series_availability) * 8760, 1) AS expected_downtime_hours_per_year;

   // Parallel system availability (redundancy)
   MATCH (s:System)-[:HAS_REDUNDANCY]->(rg:RedundancyGroup)-[:CONTAINS]->(e:Equipment)
   WHERE s.system_id = $system_id
   WITH s, rg, collect(e) AS redundant_components
   WITH s, rg,
        1.0 - reduce(unavail = 1.0, e IN redundant_components |
                     unavail * (e.mttr_hours / (e.mtbf_hours + e.mttr_hours))) AS parallel_availability
   RETURN s.system_id,
          rg.redundancy_group_id,
          round(parallel_availability * 100, 4) AS availability_percent;
   ```

3. **Downtime Attribution**:
   ```cypher
   MATCH (e:Equipment)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
   WHERE f.failure_timestamp > datetime() - duration({days: 365})
   WITH e,
        sum(f.total_downtime_hours) AS failure_downtime
   MATCH (e)-[:RECEIVED_MAINTENANCE]->(m:MaintenanceEvent)
   WHERE m.maintenance_timestamp > datetime() - duration({days: 365})
     AND m.maintenance_type = "PREVENTIVE"
   WITH e, failure_downtime,
        sum(m.actual_duration_hours) AS pm_downtime
   RETURN e.equipment_id,
          round(failure_downtime, 1) AS failure_downtime_hours,
          round(pm_downtime, 1) AS pm_downtime_hours,
          round(failure_downtime + pm_downtime, 1) AS total_downtime_hours,
          round(failure_downtime / (failure_downtime + pm_downtime) * 100, 1) AS failure_percent,
          round(pm_downtime / (failure_downtime + pm_downtime) * 100, 1) AS pm_percent;
   ```

4. **Bottleneck Identification**:
   - Calculate availability sensitivity: ∂A_system/∂A_component
   - Rank components by impact on system availability
   - Identify critical single points of failure
   - Recommend redundancy or reliability improvements

### 3.3 Maintainability Analysis Workflow

**Objective**: Optimize maintenance processes to minimize MTTR and maximize availability.

**Steps**:

1. **MTTR Component Breakdown**:
   ```cypher
   MATCH (e:Equipment)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
   WHERE f.failure_timestamp > datetime() - duration({days: 365})
   WITH e,
        avg(f.detection_time_minutes) AS avg_detection_min,
        avg(f.diagnosis_time_minutes) AS avg_diagnosis_min,
        avg(f.logistics_delay_hours) AS avg_logistics_hours,
        avg(f.repair_time_hours) AS avg_repair_hours,
        avg(f.verification_time_hours) AS avg_verification_hours,
        avg(f.total_downtime_hours) AS avg_total_downtime_hours
   RETURN e.equipment_id,
          round(avg_detection_min, 1) AS avg_detection_minutes,
          round(avg_diagnosis_min, 1) AS avg_diagnosis_minutes,
          round(avg_logistics_hours, 1) AS avg_logistics_hours,
          round(avg_repair_hours, 1) AS avg_repair_hours,
          round(avg_verification_hours, 1) AS avg_verification_hours,
          round(avg_total_downtime_hours, 1) AS avg_mttr_hours;
   ```

2. **Maintenance Complexity Assessment**:
   - Number of technicians required
   - Specialized tools/equipment needed
   - Skill level requirements
   - Documentation quality
   - Spare parts availability

3. **Improvement Opportunity Identification**:
   ```cypher
   // Identify equipment with high MTTR relative to peers
   MATCH (e1:Equipment)
   WHERE e1.equipment_type = $equipment_type
   WITH avg(e1.mttr_hours) AS type_avg_mttr,
        stdev(e1.mttr_hours) AS type_stdev_mttr
   MATCH (e2:Equipment)
   WHERE e2.equipment_type = $equipment_type
     AND e2.mttr_hours > type_avg_mttr + type_stdev_mttr
   WITH e2, type_avg_mttr, type_stdev_mttr,
        (e2.mttr_hours - type_avg_mttr) AS mttr_excess,
        e2.downtime_cost_per_hour * (e2.mttr_hours - type_avg_mttr) AS cost_per_failure
   MATCH (e2)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
   WHERE f.failure_timestamp > datetime() - duration({days: 365})
   WITH e2, type_avg_mttr, mttr_excess, cost_per_failure,
        count(f) AS failures_per_year
   RETURN e2.equipment_id,
          e2.name,
          round(e2.mttr_hours, 1) AS current_mttr,
          round(type_avg_mttr, 1) AS typical_mttr,
          round(mttr_excess, 1) AS excess_mttr,
          failures_per_year,
          round(cost_per_failure * failures_per_year, 0) AS annual_cost_of_excess_mttr,
          ["Spare Parts Pre-positioning", "Enhanced Diagnostics", "Technician Training"] AS improvement_options
   ORDER BY annual_cost_of_excess_mttr DESC;
   ```

4. **Maintenance Strategy Optimization**:
   - Compare preventive vs corrective maintenance costs
   - Optimize PM intervals
   - Evaluate condition-based maintenance benefits
   - Assess predictive maintenance ROI

### 3.4 Safety Analysis Workflow

**Objective**: Identify safety-critical equipment, assess risk levels, ensure adequate protection.

**Steps**:

1. **Failure Mode and Effects Analysis (FMEA)**:
   ```cypher
   MATCH (e:Equipment)-[:HAS_FAILURE_MODE]->(fm:FailureMode)
   WITH e, fm,
        fm.severity_rating AS S,  // 1-10 scale
        fm.occurrence_rating AS O,  // 1-10 scale
        fm.detection_rating AS D,  // 1-10 scale
        S * O * D AS RPN  // Risk Priority Number
   WHERE RPN > 100  // High risk threshold
   WITH e, fm, S, O, D, RPN
   ORDER BY RPN DESC
   RETURN e.equipment_id,
          e.name,
          fm.failure_mode_description,
          fm.potential_effects,
          S AS severity,
          O AS occurrence,
          D AS detection_difficulty,
          RPN,
          CASE
            WHEN RPN > 200 THEN "CRITICAL"
            WHEN RPN > 100 THEN "HIGH"
            ELSE "MEDIUM"
          END AS risk_level,
          fm.recommended_actions;
   ```

2. **Safety Integrity Level Assessment**:
   ```cypher
   MATCH (e:Equipment)-[:HAS_SAFETY_ANALYSIS]->(s:SafetyAnalysis)
   WITH e, s,
        CASE s.consequence_category
          WHEN "CATASTROPHIC" THEN 4
          WHEN "CRITICAL" THEN 3
          WHEN "MARGINAL" THEN 2
          WHEN "NEGLIGIBLE" THEN 1
        END AS severity_score,
        CASE s.likelihood_category
          WHEN "FREQUENT" THEN 5
          WHEN "PROBABLE" THEN 4
          WHEN "OCCASIONAL" THEN 3
          WHEN "REMOTE" THEN 2
          WHEN "IMPROBABLE" THEN 1
        END AS likelihood_score
   WITH e, s, severity_score, likelihood_score,
        severity_score * likelihood_score AS risk_score,
        CASE
          WHEN severity_score >= 4 AND likelihood_score >= 3 THEN "SIL-4"
          WHEN severity_score >= 3 AND likelihood_score >= 3 THEN "SIL-3"
          WHEN severity_score >= 2 THEN "SIL-2"
          ELSE "SIL-1"
        END AS required_sil
   WHERE s.safety_integrity_level < required_sil  // Current SIL insufficient
   RETURN e.equipment_id,
          e.name,
          s.safety_integrity_level AS current_sil,
          required_sil,
          s.consequence_category,
          s.likelihood_category,
          risk_score,
          "UPGRADE SAFETY SYSTEM" AS recommendation;
   ```

3. **Protection Layer Analysis**:
   - Verify independence of protection layers
   - Calculate probability of failure on demand (PFD)
   - Assess common cause failures (beta factor)
   - Validate voting logic (1oo1, 1oo2, 2oo3, etc.)

4. **Fault Tree Analysis**:
   ```cypher
   // Top event: Catastrophic system failure
   MATCH path = (top:TopEvent {event: "Catastrophic Failure"})-[:CAUSED_BY*]->(basic:BasicEvent)
   WHERE basic.failure_probability IS NOT NULL
   WITH top, path, collect(basic.failure_probability) AS probabilities
   WITH top,
        reduce(p = 1.0, prob IN probabilities | p * (1 - prob)) AS success_probability,
        reduce(p = 1.0, prob IN probabilities | p * (1 - prob)) AS system_reliability
   RETURN top.event,
          round((1 - success_probability) * 100, 6) AS top_event_probability_percent,
          round(system_reliability * 100, 4) AS system_reliability_percent;
   ```

5. **Safety Audit and Compliance**:
   ```cypher
   MATCH (e:Equipment)-[:HAS_SAFETY_ANALYSIS]->(s:SafetyAnalysis)
   WHERE s.next_safety_audit_date < datetime() + duration({days: 90})
     OR s.audit_findings > 0
   RETURN e.equipment_id,
          e.name,
          s.safety_integrity_level,
          s.last_safety_audit_date,
          s.next_safety_audit_date,
          s.audit_findings,
          CASE
            WHEN s.next_safety_audit_date < datetime() THEN "OVERDUE"
            WHEN s.next_safety_audit_date < datetime() + duration({days: 30}) THEN "DUE SOON"
            ELSE "SCHEDULED"
          END AS audit_status,
          CASE
            WHEN s.audit_findings > 0 THEN "RESOLVE FINDINGS"
            ELSE "COMPLETE AUDIT"
          END AS action_required;
   ```

### 3.5 Predictive Maintenance Workflow

**Objective**: Predict equipment failures before they occur and optimize maintenance timing.

**Steps**:

1. **Remaining Useful Life (RUL) Calculation**:
   ```python
   import numpy as np
   from scipy.stats import weibull_min

   def calculate_rul(current_age, shape, scale, target_reliability=0.90):
       """
       Calculate remaining useful life until target reliability threshold

       Args:
           current_age: Current operating hours since last maintenance
           shape: Weibull shape parameter (beta)
           scale: Weibull scale parameter (eta)
           target_reliability: Target reliability threshold (default 90%)

       Returns:
           rul: Remaining useful life in hours
       """
       # Current reliability
       R_current = weibull_min.sf(current_age, shape, scale=scale)

       # If already below target, RUL = 0
       if R_current < target_reliability:
           return 0.0

       # Solve for time when R(t) = target_reliability
       # R(t) = exp(-(t/eta)^beta) = target
       # t = eta * (-ln(target))^(1/beta)
       t_target = scale * (-np.log(target_reliability))**(1/shape)

       rul = max(0, t_target - current_age)
       return rul

   def calculate_failure_probability_window(current_age, shape, scale, window_hours):
       """Calculate probability of failure in next window_hours"""
       R_current = weibull_min.sf(current_age, shape, scale=scale)
       R_future = weibull_min.sf(current_age + window_hours, shape, scale=scale)

       prob_failure = (R_current - R_future) / R_current
       return prob_failure
   ```

2. **Predictive Maintenance Prioritization**:
   ```cypher
   MATCH (e:Equipment)-[:HAS_RELIABILITY_MODEL]->(r:ReliabilityModel)
   WITH e, r,
        duration.inHours(datetime(), datetime(e.last_failure_date)) AS hours_since_failure,
        e.downtime_cost_per_hour * e.mttr_hours AS expected_failure_cost,
        e.maintenance_cost_per_year / (8760.0 / e.pm_interval_days / 30.0) AS pm_cost
   WITH e, r, hours_since_failure, expected_failure_cost, pm_cost,
        exp(-(hours_since_failure / r.weibull_scale_eta)^r.weibull_shape_beta) AS current_reliability,
        // Calculate RUL to 90% reliability
        r.weibull_scale_eta * (-ln(0.90))^(1/r.weibull_shape_beta) - hours_since_failure AS rul_hours
   WHERE rul_hours > 0 AND rul_hours < 2000  // Within 2000 hours of threshold
   WITH e, hours_since_failure, current_reliability, rul_hours, expected_failure_cost, pm_cost,
        (1 - current_reliability) * expected_failure_cost AS expected_cost_if_wait,
        CASE
          WHEN rul_hours < 168 THEN "URGENT"
          WHEN rul_hours < 720 THEN "HIGH"
          WHEN rul_hours < 1440 THEN "MEDIUM"
          ELSE "LOW"
        END AS priority
   RETURN e.equipment_id,
          e.name,
          round(hours_since_failure, 0) AS hours_since_last_event,
          round(current_reliability * 100, 1) AS current_reliability_percent,
          round(rul_hours, 0) AS rul_hours,
          round(rul_hours / 24, 0) AS rul_days,
          priority,
          round(expected_cost_if_wait, 0) AS expected_failure_cost,
          round(pm_cost, 0) AS pm_cost,
          round(expected_cost_if_wait - pm_cost, 0) AS net_benefit
   ORDER BY
     CASE priority
       WHEN "URGENT" THEN 1
       WHEN "HIGH" THEN 2
       WHEN "MEDIUM" THEN 3
       ELSE 4
     END,
     net_benefit DESC;
   ```

3. **Condition Monitoring Integration**:
   ```cypher
   // Integrate sensor data with reliability models
   MATCH (e:Equipment)-[:HAS_SENSOR]->(s:Sensor)
   WHERE s.sensor_type IN ["VIBRATION", "TEMPERATURE", "OIL_ANALYSIS"]
   WITH e, s
   MATCH (s)-[:RECORDED_READING]->(r:SensorReading)
   WHERE r.timestamp > datetime() - duration({days: 30})
   WITH e, s,
        avg(r.value) AS avg_value,
        stdev(r.value) AS stdev_value,
        s.alert_threshold_high AS threshold
   WHERE avg_value > threshold * 0.85  // Approaching threshold
   MATCH (e)-[:HAS_RELIABILITY_MODEL]->(rm:ReliabilityModel)
   WITH e, s, avg_value, threshold,
        duration.inHours(datetime(), datetime(e.last_failure_date)) AS hours_since_failure,
        rm.weibull_shape_beta AS shape,
        rm.weibull_scale_eta AS scale
   WITH e, s, avg_value, threshold, hours_since_failure,
        exp(-(hours_since_failure / scale)^shape) AS reliability_model_estimate,
        (avg_value / threshold) AS condition_degradation_factor
   WITH e, s, avg_value, threshold,
        reliability_model_estimate * (1 - condition_degradation_factor * 0.5) AS adjusted_reliability
   WHERE adjusted_reliability < 0.90
   RETURN e.equipment_id,
          s.sensor_type,
          round(avg_value, 2) AS current_reading,
          round(threshold, 2) AS alert_threshold,
          round(reliability_model_estimate * 100, 1) AS model_reliability_percent,
          round(adjusted_reliability * 100, 1) AS condition_adjusted_reliability_percent,
          "SCHEDULE INSPECTION" AS recommendation;
   ```

4. **Maintenance Window Optimization**:
   ```cypher
   // Find optimal maintenance windows considering production schedule
   MATCH (e:Equipment)
   WHERE e.next_pm_date IS NOT NULL
   WITH e,
        duration.inDays(datetime(e.next_pm_date), datetime()) AS days_to_pm
   MATCH (ps:ProductionSchedule)
   WHERE ps.equipment_id = e.equipment_id
     AND ps.start_date >= datetime()
     AND ps.start_date <= datetime() + duration({days: 90})
   WITH e, days_to_pm, collect(ps) AS production_schedule
   WITH e, days_to_pm, production_schedule,
        [ps IN production_schedule WHERE ps.production_priority = "LOW" | ps] AS low_priority_windows
   WHERE size(low_priority_windows) > 0
   WITH e, days_to_pm,
        head([w IN low_priority_windows ORDER BY w.start_date | w]) AS optimal_window
   RETURN e.equipment_id,
          e.name,
          e.next_pm_date AS scheduled_pm_date,
          optimal_window.start_date AS recommended_pm_date,
          optimal_window.production_priority,
          duration.inDays(datetime(e.next_pm_date), optimal_window.start_date) AS schedule_adjustment_days,
          CASE
            WHEN duration.inDays(datetime(e.next_pm_date), optimal_window.start_date) > 7 THEN "REVIEW RELIABILITY IMPACT"
            ELSE "ACCEPTABLE ADJUSTMENT"
          END AS adjustment_assessment;
   ```

5. **Maintenance Decision Support**:
   ```python
   import pandas as pd
   import numpy as np

   def maintenance_decision_model(equipment_data):
       """
       Decision model for maintenance action selection

       Returns:
           action: "URGENT_PM", "SCHEDULE_PM", "MONITOR", "NO_ACTION"
           justification: Reasoning for decision
           estimated_benefit: Expected cost savings
       """
       reliability = equipment_data['current_reliability']
       rul_hours = equipment_data['rul_hours']
       condition_score = equipment_data['condition_monitoring_score']
       failure_cost = equipment_data['expected_failure_cost']
       pm_cost = equipment_data['pm_cost']

       # Decision logic
       if reliability < 0.80 or rul_hours < 168:
           action = "URGENT_PM"
           justification = f"Reliability {reliability:.1%} below 80% or RUL {rul_hours:.0f}h < 1 week"
           benefit = failure_cost * (1 - reliability) - pm_cost

       elif reliability < 0.90 or rul_hours < 720:
           action = "SCHEDULE_PM"
           justification = f"Reliability {reliability:.1%} below 90% or RUL {rul_hours:.0f}h < 30 days"
           benefit = failure_cost * (1 - reliability) * 0.7 - pm_cost

       elif condition_score < 0.85:
           action = "MONITOR"
           justification = f"Condition monitoring score {condition_score:.1%} shows degradation"
           benefit = 0  # Monitoring cost assumed negligible

       else:
           action = "NO_ACTION"
           justification = f"Equipment within normal operating parameters"
           benefit = failure_cost * (1 - reliability) * -1  # Cost of unnecessary PM

       return {
           'action': action,
           'justification': justification,
           'estimated_benefit': max(0, benefit),
           'confidence': reliability * condition_score
       }
   ```

---

## 4. RAMS KPIs and Dashboards

### 4.1 Executive Dashboard KPIs

```yaml
reliability_kpis:
  fleet_mtbf:
    calculation: "Weighted average MTBF across all equipment"
    target: "> 8000 hours"
    red_threshold: "< 6000 hours"

  failure_rate_trend:
    calculation: "Slope of failures per month over 12 months"
    target: "< 0 (decreasing)"
    red_threshold: "> 0.1 (increasing > 10%/year)"

  reliability_improvement:
    calculation: "(Current MTBF - Last Year MTBF) / Last Year MTBF"
    target: "> 5%"
    red_threshold: "< 0%"

availability_kpis:
  system_availability:
    calculation: "Weighted system availability across all systems"
    target: "> 99.5%"
    red_threshold: "< 99.0%"

  unplanned_downtime:
    calculation: "Sum of failure downtime hours"
    target: "< 100 hours/year"
    red_threshold: "> 200 hours/year"

  availability_gap:
    calculation: "Target availability - Actual availability"
    target: "< 0.5%"
    red_threshold: "> 1.0%"

maintainability_kpis:
  fleet_mttr:
    calculation: "Weighted average MTTR across all equipment"
    target: "< 8 hours"
    red_threshold: "> 12 hours"

  maintenance_efficiency:
    calculation: "Actual PM duration / Scheduled PM duration"
    target: "< 1.1 (within 10% of plan)"
    red_threshold: "> 1.3 (>30% overrun)"

  first_time_fix_rate:
    calculation: "Repairs resolved without repeat within 30 days / Total repairs"
    target: "> 95%"
    red_threshold: "< 85%"

safety_kpis:
  sil_compliance:
    calculation: "Equipment meeting SIL requirements / Total safety-critical equipment"
    target: "100%"
    red_threshold: "< 98%"

  safety_incidents:
    calculation: "Count of safety incidents related to equipment failure"
    target: "0"
    red_threshold: "> 0"

  protection_layer_effectiveness:
    calculation: "Protection layers that functioned correctly / Total demands"
    target: "> 99%"
    red_threshold: "< 95%"

financial_kpis:
  maintenance_roi:
    calculation: "(Avoided failure costs - Maintenance costs) / Maintenance costs"
    target: "> 3.0 (300% return)"
    red_threshold: "< 1.0 (negative return)"

  downtime_cost:
    calculation: "Sum of (Downtime hours * Cost per hour)"
    target: "< $500,000/year"
    red_threshold: "> $1,000,000/year"

  predictive_maintenance_benefit:
    calculation: "Failures prevented by PdM * Avg failure cost"
    target: "> $1,000,000/year"
    red_threshold: "< $250,000/year"
```

### 4.2 Operational Dashboard Queries

```cypher
// Dashboard 1: Reliability Overview
MATCH (e:Equipment)
WITH count(e) AS total_equipment,
     avg(e.mtbf_hours) AS avg_mtbf,
     stdev(e.mtbf_hours) AS stdev_mtbf
MATCH (e:Equipment)
WHERE e.mtbf_hours < avg_mtbf - stdev_mtbf
WITH total_equipment, avg_mtbf, count(e) AS below_avg_equipment
MATCH (f:FailureEvent)
WHERE f.failure_timestamp > datetime() - duration({days: 30})
WITH total_equipment, avg_mtbf, below_avg_equipment,
     count(f) AS failures_last_30_days
MATCH (f:FailureEvent)
WHERE f.failure_timestamp > datetime() - duration({days: 60})
  AND f.failure_timestamp <= datetime() - duration({days: 30})
RETURN total_equipment,
       round(avg_mtbf, 0) AS fleet_mtbf_hours,
       below_avg_equipment,
       round(below_avg_equipment * 100.0 / total_equipment, 1) AS below_avg_percent,
       failures_last_30_days,
       count(f) AS failures_prior_30_days,
       round((failures_last_30_days - count(f)) * 100.0 / count(f), 1) AS failure_trend_percent;

// Dashboard 2: Availability Heatmap
MATCH (s:System)-[:CONTAINS]->(e:Equipment)
WITH s, e,
     e.mtbf_hours / (e.mtbf_hours + e.mttr_hours) AS inherent_availability,
     e.current_availability AS actual_availability
WITH s,
     collect({
       equipment: e.equipment_id,
       name: e.name,
       inherent: inherent_availability,
       actual: actual_availability,
       gap: inherent_availability - actual_availability
     }) AS equipment_list
RETURN s.system_id,
       s.system_name,
       [eq IN equipment_list | {equipment: eq.equipment, availability: eq.actual}] AS equipment_availability,
       round(reduce(total = 1.0, eq IN equipment_list | total * eq.actual) * 100, 2) AS system_availability_percent,
       [eq IN equipment_list WHERE eq.gap > 0.01 | eq.equipment] AS underperforming_equipment
ORDER BY system_availability_percent ASC
LIMIT 10;

// Dashboard 3: Maintenance Backlog
MATCH (e:Equipment)-[:HAS_RELIABILITY_MODEL]->(r:ReliabilityModel)
WITH e, r,
     duration.inHours(datetime(), datetime(e.last_failure_date)) AS hours_since_failure,
     r.weibull_scale_eta * (-ln(0.90))^(1/r.weibull_shape_beta) -
       duration.inHours(datetime(), datetime(e.last_failure_date)) AS rul_hours
WHERE rul_hours < 2000 AND rul_hours > 0
WITH e, hours_since_failure, rul_hours,
     CASE
       WHEN rul_hours < 168 THEN "URGENT"
       WHEN rul_hours < 720 THEN "HIGH"
       WHEN rul_hours < 1440 THEN "MEDIUM"
       ELSE "LOW"
     END AS priority,
     e.downtime_cost_per_hour * e.mttr_hours * (1 - exp(-(hours_since_failure / r.weibull_scale_eta)^r.weibull_shape_beta)) AS expected_cost
WITH priority,
     count(e) AS equipment_count,
     sum(expected_cost) AS total_expected_cost,
     collect(e.equipment_id)[0..5] AS sample_equipment
RETURN priority,
       equipment_count,
       round(total_expected_cost, 0) AS total_expected_cost,
       sample_equipment
ORDER BY
  CASE priority
    WHEN "URGENT" THEN 1
    WHEN "HIGH" THEN 2
    WHEN "MEDIUM" THEN 3
    ELSE 4
  END;

// Dashboard 4: Safety Critical Equipment Status
MATCH (e:Equipment)-[:HAS_SAFETY_ANALYSIS]->(s:SafetyAnalysis)
WHERE s.safety_integrity_level IN ["SIL-3", "SIL-4"]
WITH e, s
MATCH (e)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
WHERE f.failure_timestamp > datetime() - duration({days: 365})
WITH e, s, count(f) AS failures_last_year,
     e.current_availability AS availability
WHERE failures_last_year > 1 OR availability < e.availability_target / 100.0
RETURN e.equipment_id,
       e.name,
       s.safety_integrity_level,
       s.consequence_category,
       failures_last_year,
       round(availability * 100, 3) AS availability_percent,
       round(e.availability_target, 3) AS target_availability_percent,
       s.next_safety_audit_date,
       CASE
         WHEN failures_last_year > 2 THEN "CRITICAL REVIEW"
         WHEN availability < e.availability_target / 100.0 * 0.95 THEN "AVAILABILITY CONCERN"
         ELSE "MONITOR"
       END AS status
ORDER BY failures_last_year DESC, availability ASC;

// Dashboard 5: Maintenance ROI Analysis
MATCH (e:Equipment)-[:RECEIVED_MAINTENANCE]->(m:MaintenanceEvent)
WHERE m.maintenance_type = "PREVENTIVE"
  AND m.maintenance_timestamp > datetime() - duration({days: 365})
WITH e,
     count(m) AS pm_count,
     sum(m.cost) AS total_pm_cost
MATCH (e)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
WHERE f.failure_timestamp > datetime() - duration({days: 365})
WITH e, pm_count, total_pm_cost,
     count(f) AS failure_count,
     sum(f.repair_cost + f.lost_production_cost) AS total_failure_cost
WITH e, pm_count, total_pm_cost, failure_count, total_failure_cost,
     // Estimate failures prevented (assume PM prevents 50% of potential failures)
     failure_count * 2 AS estimated_failures_without_pm,
     total_failure_cost * 2 AS estimated_cost_without_pm
WITH e, pm_count, total_pm_cost, failure_count, total_failure_cost,
     estimated_failures_without_pm,
     estimated_cost_without_pm,
     (estimated_cost_without_pm - total_pm_cost - total_failure_cost) AS estimated_savings,
     (estimated_cost_without_pm - total_pm_cost - total_failure_cost) / total_pm_cost AS roi
WHERE total_pm_cost > 0
RETURN e.equipment_id,
       e.name,
       pm_count,
       failure_count,
       round(total_pm_cost, 0) AS total_pm_cost,
       round(total_failure_cost, 0) AS total_failure_cost,
       round(estimated_cost_without_pm, 0) AS estimated_cost_without_pm,
       round(estimated_savings, 0) AS estimated_savings,
       round(roi, 2) AS roi_ratio,
       CASE
         WHEN roi > 3.0 THEN "EXCELLENT"
         WHEN roi > 1.5 THEN "GOOD"
         WHEN roi > 0.5 THEN "ADEQUATE"
         ELSE "REVIEW STRATEGY"
       END AS roi_assessment
ORDER BY roi DESC
LIMIT 20;
```

---

## 5. Integration with AEON Digital Twin

### 5.1 Cross-Enhancement Integration

```yaml
integration_points:
  enhancement_01_graph_schema:
    rams_extends:
      - Equipment nodes with RAMS properties
      - Failure event tracking
      - Maintenance event modeling

  enhancement_02_temporal_dynamics:
    rams_uses:
      - Time-series failure data
      - Operating hours tracking
      - Maintenance schedule temporal patterns
      - Degradation trends over time

  enhancement_03_geospatial:
    rams_integrates:
      - Equipment location for technician dispatch optimization
      - Regional failure pattern analysis
      - Spare parts depot proximity for MTTR reduction

  enhancement_04_threat_modeling:
    rams_informs:
      - Cyber-physical attack impact on equipment reliability
      - Safety system compromise scenarios
      - Cascading failure vulnerability assessment

  enhancement_05_predictive_analytics:
    rams_enables:
      - Failure prediction models (core capability)
      - Remaining useful life estimation
      - Maintenance optimization algorithms
      - Condition-based monitoring integration

  enhancement_06_cognitive_behavioral:
    rams_analyzes:
      - Human factors in maintenance errors
      - Operator behavior impact on equipment reliability
      - Cognitive biases in failure diagnosis
      - Safety culture assessment

  enhancement_07_psychometric_ner:
    rams_extracts:
      - Failure mode descriptions from text
      - Maintenance procedure entities
      - Safety incident narratives
      - Root cause analysis reports
```

### 5.2 API Endpoints for RAMS

```yaml
rams_api_endpoints:
  reliability_analysis:
    POST /api/rams/reliability/calculate:
      description: "Calculate reliability metrics for equipment"
      input:
        equipment_id: "EQUIP-001"
        analysis_period_days: 365
      output:
        mtbf_hours: 8760.0
        failure_rate: 0.000114
        reliability_function: "weibull"
        confidence_interval: [7890, 9630]

    GET /api/rams/reliability/predict:
      description: "Predict equipment failures"
      params:
        equipment_id: "EQUIP-001"
        prediction_horizon_days: 90
      output:
        failure_probability: 0.15
        confidence: 0.87
        rul_hours: 1240
        recommended_action: "SCHEDULE_PM"

  availability_analysis:
    GET /api/rams/availability/system:
      description: "Calculate system availability"
      params:
        system_id: "SYS-001"
      output:
        system_availability: 0.9987
        downtime_hours_per_year: 11.4
        bottleneck_equipment: ["EQUIP-023", "EQUIP-056"]

    POST /api/rams/availability/optimize:
      description: "Recommend availability improvements"
      input:
        system_id: "SYS-001"
        target_availability: 0.9999
      output:
        current_availability: 0.9987
        gap: 0.0012
        recommendations:
          - action: "Add redundancy to EQUIP-023"
            cost: 125000
            availability_improvement: 0.0008
          - action: "Reduce MTTR for EQUIP-056"
            cost: 35000
            availability_improvement: 0.0005

  maintainability_analysis:
    GET /api/rams/maintainability/mttr:
      description: "Analyze MTTR components"
      params:
        equipment_id: "EQUIP-001"
      output:
        mttr_hours: 8.5
        detection_time_min: 5
        diagnosis_time_min: 45
        logistics_delay_hours: 2.0
        repair_time_hours: 6.5
        improvement_opportunities:
          - "Pre-position spare parts (save 1.5h)"
          - "Enhanced diagnostics (save 0.5h)"

    POST /api/rams/maintainability/optimize:
      description: "Optimize maintenance schedules"
      input:
        system_id: "SYS-001"
        optimization_objective: "minimize_downtime_cost"
      output:
        current_schedule: {...}
        optimized_schedule: {...}
        annual_savings: 285000

  safety_analysis:
    GET /api/rams/safety/assessment:
      description: "Safety integrity level assessment"
      params:
        equipment_id: "EQUIP-001"
      output:
        current_sil: "SIL-3"
        required_sil: "SIL-3"
        pfd_avg: 0.0001
        compliance_status: "COMPLIANT"

    POST /api/rams/safety/fmea:
      description: "Conduct FMEA analysis"
      input:
        equipment_id: "EQUIP-001"
        analysis_type: "FMECA"
      output:
        failure_modes:
          - mode: "Bearing Seizure"
            severity: 8
            occurrence: 3
            detection: 2
            rpn: 48
            recommended_actions: [...]

  predictive_maintenance:
    GET /api/rams/predictive/prioritization:
      description: "Prioritize predictive maintenance"
      params:
        site_id: "SITE-001"
        priority_threshold: "HIGH"
      output:
        maintenance_queue:
          - equipment_id: "EQUIP-012"
            priority: "URGENT"
            rul_days: 5
            expected_benefit: 125000
          - equipment_id: "EQUIP-045"
            priority: "HIGH"
            rul_days: 18
            expected_benefit: 87000

    POST /api/rams/predictive/decision:
      description: "Maintenance decision support"
      input:
        equipment_id: "EQUIP-001"
        decision_factors:
          current_reliability: 0.87
          condition_score: 0.82
          production_schedule: "CRITICAL"
      output:
        recommended_action: "SCHEDULE_PM"
        timing: "within_7_days"
        justification: "..."
        estimated_benefit: 95000
```

---

## 6. Training Data Sources

### 6.1 Verified RAMS Files (8 total)

```yaml
rams_training_files:
  file_1:
    path: "AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTOR]/reliability_*.md"
    content: "Equipment reliability models, MTBF data, Weibull parameters"

  file_2:
    path: "AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTOR]/maintenance_*.md"
    content: "Maintenance procedures, PM schedules, MTTR breakdowns"

  file_3:
    path: "AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTOR]/safety_*.md"
    content: "Safety integrity levels, FMEA, protection layers"

  file_4:
    path: "AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTOR]/failure_analysis_*.md"
    content: "Failure modes, root causes, corrective actions"

  file_5:
    path: "AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTOR]/availability_*.md"
    content: "System availability targets, downtime analysis"

  file_6:
    path: "AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTOR]/predictive_maintenance_*.md"
    content: "Condition monitoring, RUL estimation, PdM strategies"

  file_7:
    path: "AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTOR]/spare_parts_*.md"
    content: "Spare parts inventory, logistics delays, criticality"

  file_8:
    path: "AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTOR]/equipment_*.md"
    content: "Equipment specifications, operating conditions, criticality"
```

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- Extend Neo4j schema with RAMS node labels and relationships
- Implement reliability calculation algorithms (MTBF, Weibull fitting)
- Develop availability analysis queries
- Create MTTR component tracking

### Phase 2: Advanced Analytics (Weeks 3-4)
- Build predictive maintenance algorithms (RUL estimation)
- Implement safety analysis workflows (FMEA, SIL assessment)
- Develop maintenance optimization models
- Create RAMS KPI dashboard queries

### Phase 3: Integration (Weeks 5-6)
- Connect RAMS to temporal dynamics (Enhancement 02)
- Integrate with predictive analytics platform (Enhancement 05)
- Link to cognitive bias analysis (Enhancement 06)
- Develop cross-enhancement API endpoints

### Phase 4: Validation (Weeks 7-8)
- Validate reliability models against historical data
- Test predictive maintenance accuracy
- Verify safety analysis compliance
- Performance optimization and tuning

---

## 8. Success Metrics

```yaml
success_criteria:
  reliability:
    mtbf_calculation_accuracy: "> 95%"
    weibull_fit_quality: "R² > 0.90"
    failure_prediction_accuracy: "> 80%"

  availability:
    availability_calculation_accuracy: "±0.1%"
    bottleneck_identification_precision: "> 90%"
    system_availability_model_accuracy: "> 95%"

  maintainability:
    mttr_prediction_accuracy: "±10%"
    pm_optimization_cost_savings: "> 15%"
    first_time_fix_rate_improvement: "> 5%"

  safety:
    sil_assessment_accuracy: "100%"
    fmea_completeness: "> 95% of critical modes"
    protection_layer_validation: "100%"

  predictive_maintenance:
    rul_prediction_accuracy: "±20%"
    maintenance_cost_reduction: "> 20%"
    unplanned_downtime_reduction: "> 30%"
```

---

## References

1. **IEC 61508** - Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems
2. **IEC 61511** - Functional Safety - Safety Instrumented Systems for the Process Industry Sector
3. **ISO 13849** - Safety of Machinery - Safety-related Parts of Control Systems
4. **MIL-HDBK-217** - Reliability Prediction of Electronic Equipment
5. **ReliaSoft** - Weibull Analysis and Life Data Analysis
6. **NASA Reliability Handbook** - NASA Technical Standards
7. **DoD Reliability Analysis Center** - RAC Failure Mode Database
8. **SAE JA1011** - Evaluation Criteria for Reliability-Centered Maintenance Processes
9. **ISO 14224** - Collection and Exchange of Reliability and Maintenance Data for Equipment
10. **API 580/581** - Risk-Based Inspection Methodology

---

**Document Version:** v1.0.0
**Last Updated:** 2025-11-25
**Total Lines:** 1,450+
**Status:** ACTIVE - Ready for TASKMASTER creation
