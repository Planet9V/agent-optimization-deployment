# TASKMASTER: RAMS (Reliability/Availability/Maintainability/Safety) Data Ingestion
# 10-Agent Swarm Architecture

**File:** Enhancement_08_RAMS_Reliability/TASKMASTER_RAMS_v1.0.md
**Created:** 2025-11-25 14:35:00 UTC
**Version:** v1.0.0
**Status:** ACTIVE
**Purpose:** Orchestrate 10-agent swarm for RAMS discipline data ingestion into AEON Digital Twin Neo4j knowledge graph

---

## MISSION STATEMENT

**PRIMARY OBJECTIVE**: Ingest 8 RAMS (Reliability, Availability, Maintainability, Safety) discipline files into Neo4j knowledge graph, enabling equipment reliability modeling, predictive maintenance, failure analysis, and safety-critical system identification.

**TARGET DATA**: 8 verified RAMS files from AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTORS]

**DELIVERABLES**:
1. Neo4j nodes: Equipment (RAMS properties), FailureEvent, MaintenanceEvent, ReliabilityModel, SafetyAnalysis
2. Neo4j relationships: EXPERIENCED_FAILURE, RECEIVED_MAINTENANCE, HAS_RELIABILITY_MODEL, HAS_SAFETY_ANALYSIS
3. RAMS metrics: MTBF, MTTR, availability, failure rates, Weibull parameters, SIL levels
4. Predictive models: Remaining Useful Life (RUL), failure probability, maintenance prioritization
5. Safety analysis: FMEA, criticality assessment, protection layer validation

**SUCCESS CRITERIA**:
- 8 RAMS files fully processed
- 100% entity extraction accuracy for critical RAMS entities
- Neo4j graph populated with RAMS nodes and relationships
- Reliability models validated (R² > 0.90 for Weibull fits)
- Predictive maintenance queries operational
- Safety-critical equipment identified and SIL-classified

---

## SWARM ARCHITECTURE

### Topology: HIERARCHICAL with MESH coordination

```
                    SWARM COORDINATOR (Agent 1)
                            |
        +-------------------+-------------------+
        |                   |                   |
    PLANNING           EXECUTION           VALIDATION
   (Agents 2-3)       (Agents 4-8)        (Agents 9-10)
        |                   |                   |
   +---------+         +---------+         +---------+
   |         |         |    |    |         |         |
Schema    Data      Extract NER  Model   Verify  Audit
Design   Survey    (A4-5) (A6) (A7-8)   (A9)   (A10)
(A2)     (A3)
```

### Agent Roster (10 Total)

| Agent ID | Role | Primary Function | Deliverable |
|----------|------|------------------|-------------|
| AGENT-1 | Swarm Coordinator | Orchestrate swarm, coordinate phases, aggregate results | Swarm execution log, phase transitions |
| AGENT-2 | Schema Architect | Design RAMS Neo4j schema, define constraints | Neo4j schema DDL, constraint definitions |
| AGENT-3 | Data Survey Agent | Identify RAMS files, validate structure, extract metadata | File inventory, data quality report |
| AGENT-4 | Equipment Extractor | Extract equipment entities with RAMS properties | Equipment nodes with MTBF/MTTR/availability |
| AGENT-5 | Event Extractor | Extract failure events and maintenance events | FailureEvent and MaintenanceEvent nodes |
| AGENT-6 | NER Specialist | Named Entity Recognition for RAMS terms | RAMS entity dictionary, taxonomy |
| AGENT-7 | Reliability Modeler | Build reliability models, Weibull fitting | ReliabilityModel nodes with distribution params |
| AGENT-8 | Safety Analyst | Extract safety data, SIL classification, FMEA | SafetyAnalysis nodes, criticality scores |
| AGENT-9 | Validation Agent | Verify data quality, validate models | Quality assurance report, accuracy metrics |
| AGENT-10 | Audit Agent | Track provenance, document process | Audit trail, ingestion report |

---

## PHASE 1: PLANNING (Agents 1-3)

### AGENT-2: Schema Architect

**TASK**: Design comprehensive Neo4j schema for RAMS discipline data.

**INPUTS**:
- Enhancement_08_RAMS_Reliability/README.md (schema section)
- Existing AEON graph schema from Enhancement_01

**PROCESS**:
1. Define node labels: Equipment, FailureEvent, MaintenanceEvent, ReliabilityModel, SafetyAnalysis
2. Define RAMS-specific properties:
   - Equipment: mtbf_hours, mttr_hours, failure_rate, availability_target, current_availability
   - FailureEvent: failure_mode, failure_cause, downtime_hours, detection_time, repair_time
   - MaintenanceEvent: maintenance_type (PM/CM), duration, cost, effectiveness
   - ReliabilityModel: distribution_type, weibull_shape, weibull_scale, confidence_intervals
   - SafetyAnalysis: safety_integrity_level, consequence_category, risk_priority_number
3. Define relationship types:
   - (Equipment)-[:EXPERIENCED_FAILURE]->(FailureEvent)
   - (Equipment)-[:RECEIVED_MAINTENANCE]->(MaintenanceEvent)
   - (Equipment)-[:HAS_RELIABILITY_MODEL]->(ReliabilityModel)
   - (Equipment)-[:HAS_SAFETY_ANALYSIS]->(SafetyAnalysis)
   - (FailureEvent)-[:CAUSED_BY]->(FailureEvent)
   - (MaintenanceEvent)-[:PREVENTED_FAILURE]->(FailureEvent)
4. Create unique constraints and indexes:
   ```cypher
   CREATE CONSTRAINT equipment_id IF NOT EXISTS
   FOR (e:Equipment) REQUIRE e.equipment_id IS UNIQUE;

   CREATE CONSTRAINT failure_event_id IF NOT EXISTS
   FOR (f:FailureEvent) REQUIRE f.failure_id IS UNIQUE;

   CREATE INDEX equipment_mtbf IF NOT EXISTS
   FOR (e:Equipment) ON (e.mtbf_hours);

   CREATE INDEX failure_timestamp IF NOT EXISTS
   FOR (f:FailureEvent) ON (f.failure_timestamp);
   ```

**OUTPUTS**:
- `neo4j_rams_schema.cypher` - Complete schema DDL
- `rams_constraints.cypher` - Constraint definitions
- `rams_indexes.cypher` - Index definitions
- `schema_documentation.md` - Human-readable schema docs

**COORDINATION**:
- Send schema to AGENT-1 (Coordinator) for approval
- Share schema with AGENT-4, AGENT-5, AGENT-7, AGENT-8 (extraction agents)

---

### AGENT-3: Data Survey Agent

**TASK**: Identify and validate 8 RAMS files, extract metadata, assess data quality.

**INPUTS**:
- Directory: `AEON_Training_data_NER10/Training_Data_Check_to_see/`
- File patterns: `reliability_*.md`, `maintenance_*.md`, `safety_*.md`, `failure_analysis_*.md`, `availability_*.md`, `predictive_maintenance_*.md`, `spare_parts_*.md`, `equipment_*.md`

**PROCESS**:
1. **File Discovery**:
   ```bash
   # Search for RAMS files across sectors
   find AEON_Training_data_NER10/Training_Data_Check_to_see/ -type f \
     \( -name "*reliability*" -o -name "*maintenance*" -o -name "*safety*" \
        -o -name "*failure*" -o -name "*availability*" -o -name "*predictive*" \
        -o -name "*spare*parts*" -o -name "*equipment*" \) \
     -name "*.md" | head -8
   ```

2. **File Validation**:
   - Verify file exists and is readable
   - Check file size > 1KB (substantive content)
   - Validate markdown structure
   - Extract file metadata: sector, subsector, document type

3. **Content Analysis**:
   - Identify RAMS entity types present (equipment, failures, maintenance, safety)
   - Count entity mentions (estimated)
   - Detect RAMS metrics (MTBF, MTTR, availability, failure rates)
   - Identify reliability distributions (Weibull, exponential, lognormal)
   - Extract safety classifications (SIL levels, criticality)

4. **Data Quality Assessment**:
   ```yaml
   quality_metrics:
     completeness:
       - equipment_identifiers: "present/absent"
       - failure_timestamps: "present/absent"
       - maintenance_records: "present/absent"
       - safety_classifications: "present/absent"

     consistency:
       - date_format_standard: "ISO 8601 compliant"
       - equipment_naming: "consistent across documents"
       - unit_standardization: "hours/days consistent"

     accuracy:
       - mtbf_plausibility: "within industry norms"
       - availability_range: "0-100%"
       - failure_rate_positive: "> 0"
   ```

5. **Priority Ranking**:
   - Rank files by RAMS content richness
   - Identify critical vs supplementary files
   - Flag files requiring special handling

**OUTPUTS**:
- `rams_file_inventory.json` - List of 8 files with metadata
- `data_quality_report.md` - Quality assessment per file
- `entity_type_distribution.json` - Estimated entity counts per type
- `processing_priorities.json` - Recommended ingestion order

**COORDINATION**:
- Send file inventory to AGENT-1 (Coordinator)
- Share quality report with AGENT-4 through AGENT-8 (extraction agents)
- Alert AGENT-9 (Validation) of quality concerns

---

## PHASE 2: EXTRACTION (Agents 4-8)

### AGENT-4: Equipment Extractor

**TASK**: Extract equipment entities with RAMS properties from 8 files.

**INPUTS**:
- 8 RAMS files from AGENT-3's inventory
- Neo4j schema from AGENT-2

**EXTRACTION TARGETS**:
```yaml
equipment_entity:
  core_properties:
    - equipment_id: "Unique identifier (e.g., EQUIP-001, TURB-GEN-01)"
    - name: "Equipment name (e.g., Main Turbine Generator)"
    - equipment_type: "Category (Rotating Equipment, Static Equipment, Control System)"
    - location: "Physical location or system membership"

  reliability_properties:
    - mtbf_hours: "Mean Time Between Failures (numeric, hours)"
    - failure_rate: "Lambda (λ), failures per hour (numeric)"
    - reliability_at_time: "R(t) values at specific time points"
    - operating_hours_ytd: "Cumulative operating hours year-to-date"
    - cycles_ytd: "Operating cycles (for cyclic equipment)"
    - last_failure_date: "Most recent failure timestamp (ISO 8601)"

  availability_properties:
    - availability_target: "Target availability percentage (99.0, 99.9, etc.)"
    - current_availability: "Actual availability (calculated or stated)"
    - downtime_ytd_hours: "Total downtime hours year-to-date"

  maintainability_properties:
    - mttr_hours: "Mean Time To Repair (numeric, hours)"
    - maintenance_complexity: "LOW/MEDIUM/HIGH"
    - spare_parts_availability: "POOR/FAIR/GOOD/EXCELLENT"
    - technician_skill_level: "BASIC/INTERMEDIATE/EXPERT"
    - pm_interval_days: "Preventive maintenance interval"

  safety_properties:
    - safety_critical: "Boolean (true/false)"
    - safety_classification: "SIL-1/SIL-2/SIL-3/SIL-4"
    - failure_consequence: "NEGLIGIBLE/MARGINAL/CRITICAL/CATASTROPHIC"

  financial_properties:
    - replacement_cost: "Equipment replacement cost (numeric, USD)"
    - downtime_cost_per_hour: "Cost of downtime per hour (numeric, USD)"
    - maintenance_cost_per_year: "Annual maintenance budget (numeric, USD)"
```

**PROCESS**:
1. **Pattern Matching**:
   ```regex
   equipment_patterns:
     equipment_id: "(?:Equipment|EQUIP|ID)[-:]?\s*([A-Z0-9-]+)"
     mtbf: "MTBF[:=]\s*(\d+(?:\.\d+)?)\s*(?:hours|hrs|h)"
     mttr: "MTTR[:=]\s*(\d+(?:\.\d+)?)\s*(?:hours|hrs|h)"
     availability: "Availability[:=]\s*(\d+(?:\.\d+)?)\s*%"
     failure_rate: "Failure Rate[:=]\s*(\d+(?:\.\d+)?(?:e-\d+)?)"
   ```

2. **Entity Normalization**:
   - Standardize equipment IDs (uppercase, consistent format)
   - Convert time units to hours
   - Normalize percentages to decimals (99.9% → 0.999)
   - Handle missing values (NULL vs 0.0)

3. **Relationship Inference**:
   - Calculate availability from MTBF/MTTR if not stated: A = MTBF / (MTBF + MTTR)
   - Calculate failure rate from MTBF: λ = 1 / MTBF
   - Infer maintenance complexity from MTTR (>12h = HIGH, 4-12h = MEDIUM, <4h = LOW)

4. **Neo4j Cypher Generation**:
   ```cypher
   MERGE (e:Equipment {equipment_id: $equipment_id})
   SET e.name = $name,
       e.equipment_type = $type,
       e.mtbf_hours = $mtbf,
       e.mttr_hours = $mttr,
       e.failure_rate = $failure_rate,
       e.availability_target = $avail_target,
       e.current_availability = $current_avail,
       e.safety_critical = $safety_critical,
       e.safety_classification = $sil,
       e.replacement_cost = $cost,
       e.created_at = datetime(),
       e.updated_at = datetime()
   ```

**OUTPUTS**:
- `equipment_entities.json` - Extracted equipment with RAMS properties (JSON format)
- `equipment_cypher.cypher` - Neo4j MERGE statements for equipment nodes
- `equipment_extraction_log.txt` - Extraction statistics and issues
- `equipment_validation_report.md` - Quality checks and validation results

**COORDINATION**:
- Send extracted equipment to AGENT-1 (Coordinator) for aggregation
- Share equipment IDs with AGENT-5 (Event Extractor) for relationship building
- Provide equipment list to AGENT-7 (Reliability Modeler) for model association
- Notify AGENT-9 (Validation) when extraction complete

---

### AGENT-5: Event Extractor

**TASK**: Extract failure events and maintenance events from 8 files.

**INPUTS**:
- 8 RAMS files from AGENT-3's inventory
- Equipment entities from AGENT-4
- Neo4j schema from AGENT-2

**EXTRACTION TARGETS**:

**A. FailureEvent Entities**:
```yaml
failure_event:
  core_properties:
    - failure_id: "Unique failure identifier (e.g., FAIL-20251115-001)"
    - equipment_id: "Reference to Equipment node"
    - failure_timestamp: "Failure occurrence date/time (ISO 8601)"

  failure_characteristics:
    - failure_mode: "How it failed (Bearing Seizure, Shaft Fracture, etc.)"
    - failure_cause: "Why it failed (Lubrication Loss, Fatigue, Corrosion)"
    - failure_mechanism: "Physical mechanism (Friction Heat, Crack Propagation)"
    - failure_severity: "MINOR/MODERATE/SEVERE/CRITICAL"

  detection_diagnosis:
    - detection_method: "How failure detected (Sensor Alarm, Visual Inspection)"
    - detection_time_minutes: "Time from failure to detection"
    - diagnosis_time_minutes: "Time from detection to root cause identification"

  repair_information:
    - repair_action: "What was done (Bearing Replacement, Weld Repair)"
    - repair_time_hours: "Actual repair duration"
    - logistics_delay_hours: "Waiting for parts/resources"
    - verification_time_hours: "Post-repair testing and validation"
    - total_downtime_hours: "Sum of all downtime components"

  impact:
    - safety_incident: "Boolean - was there a safety event?"
    - personnel_exposed: "Number of people at risk"
    - environmental_release: "Boolean - environmental impact?"
    - repair_cost: "Direct repair cost (USD)"
    - lost_production_cost: "Indirect cost from downtime (USD)"

  root_cause:
    - root_cause: "Fundamental cause after RCA"
    - corrective_actions: "List of actions taken to prevent recurrence"
    - preventable: "Boolean - could this have been prevented?"
```

**B. MaintenanceEvent Entities**:
```yaml
maintenance_event:
  core_properties:
    - maintenance_id: "Unique maintenance identifier"
    - equipment_id: "Reference to Equipment node"
    - maintenance_timestamp: "Maintenance start date/time (ISO 8601)"

  maintenance_type:
    - maintenance_type: "PREVENTIVE/CORRECTIVE/PREDICTIVE/EMERGENCY"
    - maintenance_category: "Inspection/Lubrication/Calibration/Overhaul"
    - maintenance_priority: "ROUTINE/URGENT/EMERGENCY"

  execution:
    - scheduled_duration_hours: "Planned duration"
    - actual_duration_hours: "Actual duration"
    - technicians_assigned: "Number of technicians"
    - cost: "Total maintenance cost (USD)"

  work_performed:
    - tasks_completed: "List of maintenance tasks"
    - parts_replaced: "List of parts replaced"
    - findings: "Observations during maintenance"

  quality:
    - quality_check_passed: "Boolean"
    - supervisor_approved: "Boolean"
    - follow_up_required: "Boolean"
```

**PROCESS**:

1. **FailureEvent Extraction**:
   ```regex
   failure_patterns:
     failure_id: "(?:Failure|FAIL)[-:]?\s*([A-Z0-9-]+)"
     timestamp: "(\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2})?)"
     failure_mode: "(?:Failure Mode|Mode):\s*([A-Za-z\s]+)"
     downtime: "(?:Downtime|Down Time)[:=]\s*(\d+(?:\.\d+)?)\s*(?:hours|hrs|h)"
     cost: "(?:Cost|Repair Cost)[:=]\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
   ```

2. **MaintenanceEvent Extraction**:
   ```regex
   maintenance_patterns:
     maintenance_id: "(?:Maintenance|MAINT)[-:]?\s*([A-Z0-9-]+)"
     type: "(Preventive|Corrective|Predictive|Emergency)\s+Maintenance"
     duration: "(?:Duration|Time)[:=]\s*(\d+(?:\.\d+)?)\s*(?:hours|hrs|h)"
     tasks: "Tasks?:\s*\n?((?:\s*[-•*]\s*.+\n?)+)"
   ```

3. **Relationship Building**:
   ```cypher
   // Link FailureEvent to Equipment
   MATCH (e:Equipment {equipment_id: $equipment_id})
   CREATE (f:FailureEvent {
     failure_id: $failure_id,
     equipment_id: $equipment_id,
     failure_timestamp: datetime($timestamp),
     failure_mode: $mode,
     total_downtime_hours: $downtime
   })
   CREATE (e)-[:EXPERIENCED_FAILURE {
     failure_number: $failure_sequence,
     operating_hours_at_failure: $op_hours,
     time_since_last_failure_hours: $interval
   }]->(f);

   // Link MaintenanceEvent to Equipment
   MATCH (e:Equipment {equipment_id: $equipment_id})
   CREATE (m:MaintenanceEvent {
     maintenance_id: $maintenance_id,
     equipment_id: $equipment_id,
     maintenance_timestamp: datetime($timestamp),
     maintenance_type: $type,
     actual_duration_hours: $duration
   })
   CREATE (e)-[:RECEIVED_MAINTENANCE {
     maintenance_number: $maintenance_sequence,
     on_schedule: $on_schedule,
     effectiveness_rating: $effectiveness
   }]->(m);
   ```

4. **Temporal Ordering**:
   - Sort failure events by timestamp for each equipment
   - Calculate inter-failure times
   - Link consecutive failures if causal relationship suspected
   - Associate maintenance events with subsequent failure prevention

**OUTPUTS**:
- `failure_events.json` - Extracted failure events (JSON)
- `maintenance_events.json` - Extracted maintenance events (JSON)
- `events_cypher.cypher` - Neo4j CREATE statements for event nodes and relationships
- `event_extraction_log.txt` - Statistics and processing notes
- `temporal_analysis.json` - Inter-event time intervals and patterns

**COORDINATION**:
- Send events to AGENT-1 (Coordinator)
- Provide failure data to AGENT-7 (Reliability Modeler) for distribution fitting
- Share maintenance effectiveness data with AGENT-8 (Safety Analyst)
- Notify AGENT-9 (Validation) when extraction complete

---

### AGENT-6: NER Specialist (Named Entity Recognition)

**TASK**: Perform Named Entity Recognition for RAMS-specific terminology, build RAMS entity dictionary.

**INPUTS**:
- 8 RAMS files from AGENT-3's inventory
- RAMS terminology from Enhancement_08_RAMS_Reliability/README.md

**NER TARGETS**:

```yaml
rams_entity_types:
  equipment_types:
    - "Rotating Equipment": ["Turbine", "Generator", "Motor", "Pump", "Compressor", "Fan", "Blower"]
    - "Static Equipment": ["Vessel", "Tank", "Heat Exchanger", "Reactor", "Column", "Separator"]
    - "Control Systems": ["PLC", "DCS", "SCADA", "HMI", "Controller", "Sensor", "Actuator"]
    - "Protection Systems": ["SIS", "ESD", "Fire Suppression", "Relief Valve", "Alarm System"]

  failure_modes:
    mechanical: ["Fracture", "Fatigue", "Wear", "Corrosion", "Erosion", "Seizure", "Misalignment", "Imbalance"]
    electrical: ["Short Circuit", "Open Circuit", "Ground Fault", "Insulation Failure", "Overcurrent"]
    process: ["Overpressure", "Underpressure", "Overtemperature", "Undertemperature", "Flow Loss"]
    control: ["Sensor Drift", "Actuator Failure", "Logic Error", "Communication Loss"]

  failure_causes:
    design: ["Undersized", "Incorrect Material", "Design Flaw", "Inadequate Redundancy"]
    manufacturing: ["Defect", "Poor Welding", "Improper Assembly", "Out of Tolerance"]
    operational: ["Overload", "Overspeed", "Improper Operation", "Operating Outside Limits"]
    maintenance: ["Inadequate PM", "Incorrect Procedure", "Deferred Maintenance", "Poor Lubrication"]
    environmental: ["Corrosive Atmosphere", "Extreme Temperature", "Vibration", "Contamination"]

  maintenance_types:
    preventive: ["Scheduled Inspection", "Lubrication", "Calibration", "Cleaning", "Adjustment"]
    corrective: ["Repair", "Replacement", "Rebuild", "Restoration"]
    predictive: ["Condition Monitoring", "Vibration Analysis", "Oil Analysis", "Thermography"]
    emergency: ["Immediate Repair", "Temporary Fix", "Bypass"]

  safety_classifications:
    sil_levels: ["SIL-1", "SIL-2", "SIL-3", "SIL-4"]
    consequences: ["NEGLIGIBLE", "MARGINAL", "CRITICAL", "CATASTROPHIC"]
    likelihood: ["IMPROBABLE", "REMOTE", "OCCASIONAL", "PROBABLE", "FREQUENT"]

  reliability_distributions:
    - "Exponential Distribution"
    - "Weibull Distribution"
    - "Lognormal Distribution"
    - "Normal Distribution"
    - "Gamma Distribution"

  reliability_metrics:
    - "MTBF" (Mean Time Between Failures)
    - "MTTR" (Mean Time To Repair)
    - "MTTF" (Mean Time To Failure)
    - "MDT" (Mean Down Time)
    - "PFD" (Probability of Failure on Demand)
    - "Availability"
    - "Reliability"
    - "Failure Rate"
    - "Hazard Rate"
```

**PROCESS**:

1. **Dictionary-Based NER**:
   ```python
   import spacy
   from spacy.matcher import PhraseMatcher

   nlp = spacy.load("en_core_web_sm")
   matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

   # Load RAMS terminology
   failure_modes = ["bearing seizure", "shaft fracture", "corrosion", ...]
   patterns = [nlp.make_doc(term) for term in failure_modes]
   matcher.add("FAILURE_MODE", patterns)

   # Extract from text
   doc = nlp(text)
   matches = matcher(doc)
   entities = [(doc[start:end].text, "FAILURE_MODE") for _, start, end in matches]
   ```

2. **Pattern-Based NER**:
   ```regex
   ner_patterns:
     mtbf_value: "MTBF[:=]?\s*(\d+(?:,\d{3})*(?:\.\d+)?)\s*(hours?|hrs?|h)"
     availability_value: "Availability[:=]?\s*(\d{1,3}(?:\.\d{1,4})?)\s*%"
     sil_classification: "(SIL-[1-4])"
     failure_rate: "(?:Failure Rate|λ)[:=]?\s*(\d+(?:\.\d+)?(?:e-?\d+)?)"
     weibull_params: "β[:=]?\s*(\d+(?:\.\d+)?)[,\s]+η[:=]?\s*(\d+(?:\.\d+)?)"
   ```

3. **Context-Based Entity Linking**:
   - Link failure modes to equipment types (e.g., "Bearing Seizure" → "Rotating Equipment")
   - Associate maintenance types with failure causes
   - Connect safety classifications to equipment criticality

4. **Taxonomy Building**:
   ```json
   {
     "failure_mode": "Bearing Seizure",
     "parent_category": "Mechanical Failure",
     "applicable_to": ["Rotating Equipment"],
     "typical_causes": ["Lubrication Loss", "Contamination", "Overload"],
     "detection_methods": ["Vibration Monitoring", "Temperature Monitoring"],
     "prevention_strategies": ["Regular Lubrication", "Condition Monitoring"]
   }
   ```

5. **Entity Disambiguation**:
   - Resolve acronyms (MTBF vs MTF vs MTTF)
   - Standardize terminology across documents
   - Handle domain-specific vs generic terms

**OUTPUTS**:
- `rams_entity_dictionary.json` - Complete RAMS terminology with definitions
- `ner_annotations.json` - Annotated entities from 8 files with positions
- `rams_taxonomy.json` - Hierarchical taxonomy of RAMS concepts
- `entity_frequency_analysis.json` - Entity occurrence statistics
- `disambiguation_rules.json` - Rules for resolving ambiguous terms

**COORDINATION**:
- Send entity dictionary to AGENT-4, AGENT-5, AGENT-7, AGENT-8 for standardization
- Provide taxonomy to AGENT-1 (Coordinator) for knowledge graph enrichment
- Share frequency analysis with AGENT-9 (Validation) for coverage assessment
- Alert AGENT-10 (Audit) of terminology inconsistencies

---

### AGENT-7: Reliability Modeler

**TASK**: Build reliability models (Weibull distribution fitting) for equipment based on failure data.

**INPUTS**:
- Equipment entities from AGENT-4
- Failure events from AGENT-5
- RAMS files with reliability data

**MODELING TARGETS**:

```yaml
reliability_model:
  model_identification:
    - model_id: "RELMODEL-{equipment_id}"
    - equipment_id: "Reference to Equipment node"
    - model_version: "Version number"

  distribution_parameters:
    weibull:
      - shape_beta: "Shape parameter (β) - failure rate behavior"
      - scale_eta: "Scale parameter (η) - characteristic life"
      - location_gamma: "Location parameter (γ) - failure-free period"

    exponential:
      - lambda: "Failure rate (λ)"

    lognormal:
      - mu: "Mean of log(T)"
      - sigma: "Standard deviation of log(T)"

    normal:
      - mu: "Mean time to failure"
      - sigma: "Standard deviation"

  statistical_fit:
    - sample_size: "Number of failure observations"
    - data_start_date: "Beginning of data collection period"
    - data_end_date: "End of data collection period"
    - goodness_of_fit_r_squared: "R² statistic"
    - anderson_darling_statistic: "A² test statistic"
    - kolmogorov_smirnov_statistic: "K-S test statistic"

  confidence_intervals:
    - mtbf_lower_95: "Lower bound of 95% CI for MTBF"
    - mtbf_point_estimate: "Point estimate of MTBF"
    - mtbf_upper_95: "Upper bound of 95% CI for MTBF"

  predictions:
    - reliability_at_500h: "R(500 hours)"
    - reliability_at_1000h: "R(1000 hours)"
    - reliability_at_5000h: "R(5000 hours)"
    - reliability_at_8760h: "R(8760 hours) = 1 year"

  model_metadata:
    - model_created_date: "Model creation timestamp"
    - model_created_by: "Agent or user identifier"
    - validation_status: "DRAFT/VALIDATED/APPROVED"
    - next_review_date: "Scheduled model update date"
```

**PROCESS**:

1. **Data Preparation**:
   ```python
   import pandas as pd
   import numpy as np

   # Get failure events for equipment
   query = """
   MATCH (e:Equipment {equipment_id: $equipment_id})-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
   RETURN f.failure_timestamp AS timestamp
   ORDER BY timestamp
   """

   # Calculate inter-failure times
   timestamps = pd.to_datetime(failures['timestamp'])
   inter_failure_times = timestamps.diff().dt.total_seconds() / 3600  # hours
   inter_failure_times = inter_failure_times.dropna()
   ```

2. **Distribution Fitting**:
   ```python
   from scipy.stats import weibull_min, expon, lognorm, norm
   from scipy.stats import anderson, kstest

   def fit_weibull(data):
       """Fit Weibull distribution to failure data"""
       # Maximum Likelihood Estimation
       shape, loc, scale = weibull_min.fit(data, floc=0)

       # Goodness of fit
       ad_stat, critical_values, significance_level = anderson(data, dist='weibull_min')

       # Calculate MTBF
       from scipy.special import gamma
       mtbf = scale * gamma(1 + 1/shape)

       # Confidence intervals (bootstrap)
       bootstrap_samples = 1000
       bootstrap_mtbf = []
       for _ in range(bootstrap_samples):
           resample = np.random.choice(data, size=len(data), replace=True)
           s, l, sc = weibull_min.fit(resample, floc=0)
           bootstrap_mtbf.append(sc * gamma(1 + 1/s))

       mtbf_lower = np.percentile(bootstrap_mtbf, 2.5)
       mtbf_upper = np.percentile(bootstrap_mtbf, 97.5)

       return {
           'shape_beta': shape,
           'scale_eta': scale,
           'location_gamma': loc,
           'mtbf_point': mtbf,
           'mtbf_lower_95': mtbf_lower,
           'mtbf_upper_95': mtbf_upper,
           'anderson_darling': ad_stat,
           'sample_size': len(data)
       }

   def calculate_reliability_function(t, shape, scale):
       """Calculate R(t) for Weibull distribution"""
       return np.exp(-(t / scale)**shape)

   def calculate_hazard_rate(t, shape, scale):
       """Calculate instantaneous hazard rate h(t)"""
       return (shape / scale) * (t / scale)**(shape - 1)
   ```

3. **Model Validation**:
   ```python
   def validate_model(data, shape, scale):
       """Validate Weibull model against data"""
       # Probability plot
       theoretical_quantiles = weibull_min.ppf(np.linspace(0.01, 0.99, len(data)), shape, scale=scale)
       empirical_quantiles = np.sort(data)

       # R² calculation
       ss_res = np.sum((empirical_quantiles - theoretical_quantiles)**2)
       ss_tot = np.sum((empirical_quantiles - np.mean(empirical_quantiles))**2)
       r_squared = 1 - (ss_res / ss_tot)

       # Kolmogorov-Smirnov test
       ks_stat, ks_pvalue = kstest(data, lambda x: weibull_min.cdf(x, shape, scale=scale))

       return {
           'r_squared': r_squared,
           'ks_statistic': ks_stat,
           'ks_pvalue': ks_pvalue,
           'validation_status': 'VALIDATED' if r_squared > 0.90 and ks_pvalue > 0.05 else 'NEEDS_REVIEW'
       }
   ```

4. **Predictive Calculations**:
   ```python
   def calculate_rul(current_age, shape, scale, target_reliability=0.90):
       """Calculate Remaining Useful Life"""
       # Solve R(t) = target for t, then subtract current age
       t_target = scale * (-np.log(target_reliability))**(1/shape)
       rul = max(0, t_target - current_age)
       return rul

   def failure_probability_window(current_age, shape, scale, window_hours):
       """Probability of failure in next window_hours"""
       R_current = np.exp(-(current_age / scale)**shape)
       R_future = np.exp(-((current_age + window_hours) / scale)**shape)
       prob_failure = (R_current - R_future) / R_current
       return prob_failure
   ```

5. **Neo4j Integration**:
   ```cypher
   MATCH (e:Equipment {equipment_id: $equipment_id})
   MERGE (r:ReliabilityModel {model_id: "RELMODEL-" + $equipment_id})
   SET r.distribution_type = "WEIBULL",
       r.weibull_shape_beta = $shape,
       r.weibull_scale_eta = $scale,
       r.location_gamma = $location,
       r.mtbf_point_estimate = $mtbf,
       r.mtbf_lower_95 = $mtbf_lower,
       r.mtbf_upper_95 = $mtbf_upper,
       r.goodness_of_fit_r_squared = $r_squared,
       r.anderson_darling_statistic = $ad_stat,
       r.sample_size = $sample_size,
       r.reliability_at_500h = $R_500,
       r.reliability_at_1000h = $R_1000,
       r.reliability_at_5000h = $R_5000,
       r.reliability_at_8760h = $R_8760,
       r.model_created_date = datetime(),
       r.validation_status = $status,
       r.updated_at = datetime()
   MERGE (e)-[:HAS_RELIABILITY_MODEL {
     model_version: $version,
     confidence_level: $confidence,
     applicable_from: datetime()
   }]->(r);
   ```

**OUTPUTS**:
- `reliability_models.json` - Fitted models for all equipment (JSON)
- `weibull_parameters.csv` - Distribution parameters in tabular format
- `reliability_models_cypher.cypher` - Neo4j MERGE statements
- `model_validation_report.md` - Validation statistics and fit quality
- `reliability_plots.png` - Probability plots and hazard rate curves (if visualization enabled)

**COORDINATION**:
- Send models to AGENT-1 (Coordinator)
- Provide reliability predictions to AGENT-8 (Safety Analyst) for risk calculations
- Share model quality metrics with AGENT-9 (Validation)
- Notify AGENT-10 (Audit) of models requiring review

---

### AGENT-8: Safety Analyst

**TASK**: Extract safety data, perform SIL classification, conduct FMEA, assess protection layers.

**INPUTS**:
- Equipment entities from AGENT-4
- Failure events from AGENT-5
- Reliability models from AGENT-7
- RAMS files with safety content

**ANALYSIS TARGETS**:

```yaml
safety_analysis:
  identification:
    - analysis_id: "SAFETY-{equipment_id}"
    - equipment_id: "Reference to Equipment node"
    - analysis_date: "Date of safety assessment"

  safety_classification:
    - safety_integrity_level: "SIL-1/SIL-2/SIL-3/SIL-4"
    - consequence_category: "NEGLIGIBLE/MARGINAL/CRITICAL/CATASTROPHIC/HAZARDOUS"
    - likelihood_category: "IMPROBABLE/REMOTE/OCCASIONAL/PROBABLE/FREQUENT"
    - risk_priority_number: "Numeric RPN (1-1000)"

  fmea_analysis:
    - critical_failure_modes: "List of failure modes with high criticality"
    - failure_effects: "Consequences of each failure mode"
    - severity_rating: "1-10 scale for each failure mode"
    - occurrence_rating: "1-10 scale for each failure mode"
    - detection_rating: "1-10 scale for each failure mode"

  protection_layers:
    - protection_layer_1: "First line of defense (e.g., Automatic Shutdown)"
    - protection_layer_2: "Second line (e.g., Emergency Stop)"
    - protection_layer_3: "Third line (e.g., Manual Isolation)"
    - protection_layer_4: "Fourth line (e.g., Physical Barriers)"

  safety_system_architecture:
    - voting_architecture: "1oo1, 1oo2, 2oo3, 2oo4, etc."
    - redundancy_level: "SIMPLEX/DUPLEX/TRIPLE_MODULAR"
    - common_cause_beta: "Beta factor for common cause failures (0-1)"

  probability_calculations:
    - pfd_avg: "Average Probability of Failure on Demand"
    - sif_failure_rate: "Safety Instrumented Function failure rate"
    - dangerous_failure_probability: "Probability of dangerous undetected failure"

  human_factors:
    - human_error_probability: "Probability of operator error"
    - operator_response_time_seconds: "Expected response time"
    - alarm_management_burden: "LOW/MODERATE/HIGH/EXCESSIVE"

  compliance:
    - standards_compliance: "List of standards (IEC 61508, IEC 61511, etc.)"
    - last_safety_audit_date: "Most recent safety audit"
    - next_safety_audit_date: "Scheduled next audit"
    - audit_findings: "Number of open findings"
```

**PROCESS**:

1. **SIL Classification**:
   ```python
   def determine_sil(consequence_category, likelihood_category):
       """Determine Safety Integrity Level based on risk matrix"""
       consequence_scores = {
           'NEGLIGIBLE': 1,
           'MARGINAL': 2,
           'CRITICAL': 3,
           'CATASTROPHIC': 4,
           'HAZARDOUS': 4
       }

       likelihood_scores = {
           'IMPROBABLE': 1,
           'REMOTE': 2,
           'OCCASIONAL': 3,
           'PROBABLE': 4,
           'FREQUENT': 5
       }

       risk_score = consequence_scores[consequence_category] * likelihood_scores[likelihood_category]

       # Risk matrix to SIL mapping (IEC 61508)
       if risk_score >= 16:
           return 'SIL-4'
       elif risk_score >= 12:
           return 'SIL-3'
       elif risk_score >= 8:
           return 'SIL-2'
       else:
           return 'SIL-1'
   ```

2. **FMEA/FMECA**:
   ```python
   def calculate_rpn(severity, occurrence, detection):
       """Calculate Risk Priority Number"""
       rpn = severity * occurrence * detection
       return rpn

   def fmea_analysis(failure_mode_data):
       """Perform Failure Mode and Effects Analysis"""
       fmea_results = []

       for mode in failure_mode_data:
           severity = mode['severity_rating']  # 1-10
           occurrence = mode['occurrence_rating']  # 1-10
           detection = mode['detection_rating']  # 1-10

           rpn = calculate_rpn(severity, occurrence, detection)

           criticality = "CRITICAL" if rpn > 200 else "HIGH" if rpn > 100 else "MEDIUM"

           fmea_results.append({
               'failure_mode': mode['description'],
               'severity': severity,
               'occurrence': occurrence,
               'detection': detection,
               'rpn': rpn,
               'criticality': criticality,
               'recommended_actions': mode.get('actions', [])
           })

       return sorted(fmea_results, key=lambda x: x['rpn'], reverse=True)
   ```

3. **PFD Calculation** (Probability of Failure on Demand):
   ```python
   def calculate_pfd_avg(failure_rate, test_interval, beta_factor=0.1):
       """
       Calculate average PFD for safety instrumented system

       Args:
           failure_rate: Dangerous failure rate (λD) in failures/hour
           test_interval: Proof test interval (T) in hours
           beta_factor: Common cause failure factor (0-1)

       Returns:
           pfd_avg: Average probability of failure on demand
       """
       # For 1oo1 (simplex) architecture
       pfd_1oo1 = (failure_rate * test_interval) / 2

       # Account for common cause failures
       pfd_total = pfd_1oo1 * (1 + beta_factor)

       return pfd_total

   def calculate_pfd_redundant(failure_rate, test_interval, architecture="2oo3", beta_factor=0.05):
       """Calculate PFD for redundant architectures"""
       if architecture == "1oo2":
           # One out of two (high availability)
           pfd = ((failure_rate * test_interval) / 2) ** 2
       elif architecture == "2oo3":
           # Two out of three (balanced)
           pfd = 3 * ((failure_rate * test_interval) / 2) ** 2
       elif architecture == "2oo4":
           # Two out of four (high integrity)
           pfd = 6 * ((failure_rate * test_interval) / 2) ** 2
       else:
           pfd = (failure_rate * test_interval) / 2

       # Common cause adjustment
       pfd_total = pfd * (1 + beta_factor)

       return pfd_total
   ```

4. **Protection Layer Validation**:
   ```python
   def validate_protection_layers(equipment_data):
       """Validate independence of protection layers"""
       layers = equipment_data['protection_layers']

       independence_check = {
           'layer_count': len([l for l in layers if l is not None]),
           'independence_verified': True,  # Would check actual independence
           'common_mode_risk': 'LOW',  # Based on layer diversity
           'effectiveness': 'ADEQUATE' if len([l for l in layers if l]) >= 3 else 'INADEQUATE'
       }

       return independence_check
   ```

5. **Neo4j Integration**:
   ```cypher
   MATCH (e:Equipment {equipment_id: $equipment_id})
   MERGE (s:SafetyAnalysis {analysis_id: "SAFETY-" + $equipment_id})
   SET s.analysis_date = date(),
       s.safety_integrity_level = $sil,
       s.consequence_category = $consequence,
       s.likelihood_category = $likelihood,
       s.risk_priority_number = $rpn,
       s.critical_failure_modes = $failure_modes,
       s.failure_effects = $effects,
       s.protection_layer_1 = $layer1,
       s.protection_layer_2 = $layer2,
       s.protection_layer_3 = $layer3,
       s.protection_layer_4 = $layer4,
       s.voting_architecture = $voting,
       s.redundancy_level = $redundancy,
       s.common_cause_beta = $beta,
       s.pfd_avg = $pfd,
       s.standards_compliance = $standards,
       s.updated_at = datetime()
   MERGE (e)-[:HAS_SAFETY_ANALYSIS {
     analysis_version: $version,
     risk_level: $risk_level,
     mitigation_status: $mitigation
   }]->(s);
   ```

**OUTPUTS**:
- `safety_analysis.json` - Safety assessments for all safety-critical equipment
- `fmea_results.csv` - FMEA/FMECA results with RPN rankings
- `sil_classifications.json` - SIL classification for each equipment
- `safety_analysis_cypher.cypher` - Neo4j MERGE statements
- `protection_layer_report.md` - Protection layer effectiveness assessment
- `compliance_status.json` - Standards compliance and audit status

**COORDINATION**:
- Send safety analysis to AGENT-1 (Coordinator)
- Share SIL classifications with AGENT-4 (Equipment Extractor) for equipment updates
- Provide high-RPN failure modes to AGENT-5 (Event Extractor) for monitoring
- Report compliance gaps to AGENT-9 (Validation)
- Alert AGENT-10 (Audit) of safety-critical findings

---

## PHASE 3: VALIDATION (Agents 9-10)

### AGENT-9: Validation Agent

**TASK**: Verify data quality, validate models, ensure accuracy and completeness.

**INPUTS**:
- All extracted entities from AGENT-4 through AGENT-8
- Neo4j schema from AGENT-2
- Quality reports from AGENT-3

**VALIDATION CHECKS**:

```yaml
data_quality_validation:
  completeness:
    - equipment_coverage: "All equipment have required RAMS properties"
    - failure_event_coverage: "All equipment have failure history (or marked as new)"
    - maintenance_event_coverage: "All equipment have maintenance records"
    - reliability_model_coverage: "All equipment with >3 failures have models"
    - safety_analysis_coverage: "All safety-critical equipment have safety analysis"

  consistency:
    - equipment_id_uniqueness: "No duplicate equipment IDs"
    - timestamp_validity: "All timestamps are valid ISO 8601 format"
    - unit_consistency: "Time units consistent (hours), costs in USD"
    - relationship_integrity: "All relationships reference existing nodes"

  accuracy:
    - mtbf_plausibility: "MTBF within industry norms (100-50,000 hours)"
    - mttr_plausibility: "MTTR within reasonable range (0.1-100 hours)"
    - availability_range: "Availability between 0.50 and 0.9999"
    - failure_rate_positive: "Failure rates > 0"
    - weibull_shape_valid: "Shape parameter β > 0"
    - sil_classification_valid: "SIL levels are SIL-1 through SIL-4"

  model_validation:
    - weibull_fit_quality: "R² > 0.85 for all reliability models"
    - sample_size_adequate: "At least 5 failures for model fitting"
    - confidence_intervals_valid: "Lower bound < point estimate < upper bound"
    - prediction_plausibility: "Reliability decreases monotonically with time"

  safety_validation:
    - rpn_calculation_correct: "RPN = Severity * Occurrence * Detection"
    - sil_determination_correct: "SIL matches risk matrix for consequence + likelihood"
    - pfd_calculation_valid: "PFD within valid range (1e-5 to 1e-1)"
    - protection_layers_independent: "Protection layers are truly independent"
```

**VALIDATION PROCESS**:

1. **Completeness Checks**:
   ```cypher
   // Check equipment coverage
   MATCH (e:Equipment)
   WHERE e.mtbf_hours IS NULL
      OR e.mttr_hours IS NULL
      OR e.availability_target IS NULL
   RETURN count(e) AS equipment_missing_rams_properties,
          collect(e.equipment_id)[0..10] AS sample_equipment_ids;

   // Check reliability model coverage
   MATCH (e:Equipment)
   WHERE NOT (e)-[:HAS_RELIABILITY_MODEL]->()
   WITH e
   MATCH (e)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
   WITH e, count(f) AS failure_count
   WHERE failure_count >= 3
   RETURN count(e) AS equipment_missing_models,
          collect(e.equipment_id)[0..10] AS sample_equipment_ids;

   // Check safety analysis coverage
   MATCH (e:Equipment)
   WHERE e.safety_critical = true
     AND NOT (e)-[:HAS_SAFETY_ANALYSIS]->()
   RETURN count(e) AS safety_critical_missing_analysis,
          collect(e.equipment_id) AS equipment_ids;
   ```

2. **Consistency Checks**:
   ```cypher
   // Check for duplicate equipment IDs
   MATCH (e:Equipment)
   WITH e.equipment_id AS id, count(*) AS cnt
   WHERE cnt > 1
   RETURN id, cnt;

   // Check relationship integrity
   MATCH (f:FailureEvent)
   WHERE NOT EXISTS {
     MATCH (e:Equipment {equipment_id: f.equipment_id})
   }
   RETURN count(f) AS orphaned_failure_events,
          collect(f.failure_id)[0..10] AS sample_failure_ids;

   // Check timestamp validity
   MATCH (f:FailureEvent)
   WHERE f.failure_timestamp < datetime('2000-01-01')
      OR f.failure_timestamp > datetime()
   RETURN count(f) AS invalid_timestamps,
          collect(f.failure_id) AS failure_ids;
   ```

3. **Accuracy Checks**:
   ```cypher
   // Check MTBF plausibility
   MATCH (e:Equipment)
   WHERE e.mtbf_hours < 100 OR e.mtbf_hours > 50000
   RETURN count(e) AS mtbf_outliers,
          collect({id: e.equipment_id, mtbf: e.mtbf_hours}) AS outliers;

   // Check availability range
   MATCH (e:Equipment)
   WHERE e.current_availability < 0.50 OR e.current_availability > 0.9999
   RETURN count(e) AS availability_outliers,
          collect({id: e.equipment_id, avail: e.current_availability}) AS outliers;

   // Check Weibull parameters
   MATCH (r:ReliabilityModel)
   WHERE r.weibull_shape_beta <= 0
      OR r.weibull_scale_eta <= 0
   RETURN count(r) AS invalid_weibull_params,
          collect(r.model_id) AS model_ids;
   ```

4. **Model Validation**:
   ```python
   def validate_reliability_models(neo4j_session):
       """Validate all reliability models"""
       query = """
       MATCH (e:Equipment)-[:HAS_RELIABILITY_MODEL]->(r:ReliabilityModel)
       RETURN e.equipment_id AS equipment_id,
              r.model_id AS model_id,
              r.goodness_of_fit_r_squared AS r_squared,
              r.sample_size AS sample_size,
              r.mtbf_lower_95 AS mtbf_lower,
              r.mtbf_point_estimate AS mtbf_point,
              r.mtbf_upper_95 AS mtbf_upper
       """

       results = neo4j_session.run(query)

       validation_issues = []

       for record in results:
           # Check R² threshold
           if record['r_squared'] < 0.85:
               validation_issues.append({
                   'equipment_id': record['equipment_id'],
                   'issue': 'LOW_R_SQUARED',
                   'value': record['r_squared'],
                   'threshold': 0.85
               })

           # Check sample size
           if record['sample_size'] < 5:
               validation_issues.append({
                   'equipment_id': record['equipment_id'],
                   'issue': 'INSUFFICIENT_SAMPLE_SIZE',
                   'value': record['sample_size'],
                   'minimum': 5
               })

           # Check confidence interval ordering
           if not (record['mtbf_lower'] < record['mtbf_point'] < record['mtbf_upper']):
               validation_issues.append({
                   'equipment_id': record['equipment_id'],
                   'issue': 'INVALID_CONFIDENCE_INTERVALS',
                   'values': {
                       'lower': record['mtbf_lower'],
                       'point': record['mtbf_point'],
                       'upper': record['mtbf_upper']
                   }
               })

       return validation_issues
   ```

5. **Safety Validation**:
   ```python
   def validate_safety_analysis(neo4j_session):
       """Validate safety analysis calculations"""
       query = """
       MATCH (e:Equipment)-[:HAS_SAFETY_ANALYSIS]->(s:SafetyAnalysis)
       RETURN e.equipment_id AS equipment_id,
              s.safety_integrity_level AS sil,
              s.consequence_category AS consequence,
              s.likelihood_category AS likelihood,
              s.risk_priority_number AS rpn,
              s.pfd_avg AS pfd
       """

       results = neo4j_session.run(query)

       validation_issues = []

       for record in results:
           # Validate SIL determination
           expected_sil = determine_sil(record['consequence'], record['likelihood'])
           if record['sil'] != expected_sil:
               validation_issues.append({
                   'equipment_id': record['equipment_id'],
                   'issue': 'INCORRECT_SIL',
                   'actual': record['sil'],
                   'expected': expected_sil
               })

           # Validate PFD range
           if record['pfd'] is not None:
               if record['pfd'] < 1e-5 or record['pfd'] > 1e-1:
                   validation_issues.append({
                       'equipment_id': record['equipment_id'],
                       'issue': 'PFD_OUT_OF_RANGE',
                       'value': record['pfd'],
                       'valid_range': [1e-5, 1e-1]
                   })

       return validation_issues
   ```

**OUTPUTS**:
- `validation_report.md` - Comprehensive validation report with pass/fail status
- `data_quality_metrics.json` - Quality metrics for all data
- `validation_issues.json` - Detailed list of validation failures
- `model_validation_results.json` - Reliability model validation results
- `safety_validation_results.json` - Safety analysis validation results
- `corrective_actions.json` - Recommended fixes for validation failures

**COORDINATION**:
- Report validation results to AGENT-1 (Coordinator)
- Send issues back to AGENT-4 through AGENT-8 for correction
- Approve validated data for Neo4j ingestion
- Notify AGENT-10 (Audit) of validation completion

---

### AGENT-10: Audit Agent

**TASK**: Track data provenance, document process, create audit trail, generate ingestion report.

**INPUTS**:
- All agent outputs (AGENT-2 through AGENT-9)
- Swarm execution logs from AGENT-1
- Validation results from AGENT-9

**AUDIT TRACKING**:

```yaml
audit_trail:
  data_provenance:
    - source_file: "Original RAMS file path"
    - extraction_agent: "Agent that extracted entity"
    - extraction_timestamp: "When entity was extracted"
    - extraction_method: "Pattern matching, NER, manual, etc."
    - confidence_score: "0.0-1.0 confidence in extraction"

  processing_lineage:
    - raw_entity: "Original text snippet"
    - normalized_entity: "Standardized form"
    - transformations_applied: "List of transformations"
    - validation_status: "PASSED/FAILED/WARNING"

  quality_metrics:
    - total_entities_extracted: "Count by entity type"
    - extraction_accuracy: "% of entities correctly extracted"
    - validation_pass_rate: "% of entities passing validation"
    - model_quality: "Average R² for reliability models"
    - safety_coverage: "% of safety-critical equipment analyzed"

  performance_metrics:
    - total_processing_time: "End-to-end duration"
    - agent_performance: "Processing time per agent"
    - bottlenecks_identified: "Slowest processing stages"
    - error_rate: "% of entities requiring manual review"

  compliance_documentation:
    - standards_referenced: "IEC 61508, IEC 61511, ISO 14224, etc."
    - methodology_followed: "SPARC, RAMS best practices"
    - quality_gates_applied: "Validation checkpoints"
    - approval_workflow: "Who approved what, when"
```

**AUDIT PROCESS**:

1. **Provenance Tracking**:
   ```cypher
   // Store provenance in Neo4j
   MATCH (e:Equipment {equipment_id: $equipment_id})
   CREATE (p:Provenance {
     provenance_id: apoc.create.uuid(),
     entity_type: "Equipment",
     entity_id: $equipment_id,
     source_file: $source_file,
     source_file_line: $line_number,
     extraction_agent: "AGENT-4",
     extraction_timestamp: datetime(),
     extraction_method: $method,
     confidence_score: $confidence,
     raw_text: $original_text,
     normalized_value: e.mtbf_hours,
     validation_status: "PASSED"
   })
   CREATE (e)-[:HAS_PROVENANCE]->(p);
   ```

2. **Change Tracking**:
   ```json
   {
     "entity_id": "EQUIP-001",
     "property": "mtbf_hours",
     "changes": [
       {
         "timestamp": "2025-11-25T14:45:00Z",
         "agent": "AGENT-4",
         "operation": "CREATED",
         "old_value": null,
         "new_value": 8760.0,
         "reason": "Initial extraction from file"
       },
       {
         "timestamp": "2025-11-25T14:52:00Z",
         "agent": "AGENT-9",
         "operation": "VALIDATED",
         "old_value": 8760.0,
         "new_value": 8760.0,
         "reason": "Passed plausibility check"
       }
     ]
   }
   ```

3. **Performance Monitoring**:
   ```python
   def track_agent_performance():
       """Track execution time and throughput for each agent"""
       agent_metrics = {
           'AGENT-2': {
               'task': 'Schema Design',
               'start_time': '2025-11-25T14:30:00Z',
               'end_time': '2025-11-25T14:32:30Z',
               'duration_seconds': 150,
               'deliverables_count': 4,
               'status': 'COMPLETED'
           },
           'AGENT-3': {
               'task': 'Data Survey',
               'start_time': '2025-11-25T14:32:30Z',
               'end_time': '2025-11-25T14:38:00Z',
               'duration_seconds': 330,
               'files_surveyed': 8,
               'status': 'COMPLETED'
           },
           'AGENT-4': {
               'task': 'Equipment Extraction',
               'start_time': '2025-11-25T14:38:00Z',
               'end_time': '2025-11-25T14:55:00Z',
               'duration_seconds': 1020,
               'entities_extracted': 245,
               'throughput_entities_per_min': 14.4,
               'status': 'COMPLETED'
           },
           # ... similar for AGENT-5 through AGENT-9
       }

       total_duration = sum(m['duration_seconds'] for m in agent_metrics.values())
       avg_duration = total_duration / len(agent_metrics)

       return {
           'agent_metrics': agent_metrics,
           'total_duration_seconds': total_duration,
           'average_duration_seconds': avg_duration,
           'bottleneck_agent': max(agent_metrics.items(), key=lambda x: x[1]['duration_seconds'])[0]
       }
   ```

4. **Quality Reporting**:
   ```python
   def generate_quality_report(validation_results):
       """Generate comprehensive quality report"""
       report = {
           'ingestion_summary': {
               'total_files_processed': 8,
               'total_entities_extracted': {
                   'Equipment': 245,
                   'FailureEvent': 1823,
                   'MaintenanceEvent': 3456,
                   'ReliabilityModel': 198,
                   'SafetyAnalysis': 87
               },
               'total_relationships_created': 5609,
               'processing_duration_minutes': 67
           },
           'quality_metrics': {
               'extraction_accuracy': 0.978,  # 97.8%
               'validation_pass_rate': 0.945,  # 94.5%
               'reliability_model_quality': {
                   'average_r_squared': 0.923,
                   'models_above_threshold': 0.956  # 95.6% have R² > 0.85
               },
               'safety_coverage': {
                   'safety_critical_equipment': 87,
                   'with_safety_analysis': 87,
                   'coverage_percent': 1.00  # 100%
               }
           },
           'validation_issues': {
               'total_issues': 48,
               'critical': 2,
               'high': 8,
               'medium': 18,
               'low': 20,
               'resolved': 40,
               'remaining': 8
           },
           'recommendations': [
               "Review 2 critical validation issues before production deployment",
               "Obtain additional failure data for 47 equipment lacking reliability models",
               "Schedule safety audit for 15 equipment with expired audit dates"
           ]
       }

       return report
   ```

5. **Final Report Generation**:
   ```markdown
   # RAMS Data Ingestion Audit Report

   **Ingestion ID**: RAMS-INGEST-20251125-001
   **Date**: 2025-11-25
   **Swarm Coordinator**: AGENT-1
   **Agent Count**: 10
   **Status**: COMPLETED

   ## Executive Summary

   Successfully ingested 8 RAMS discipline files into AEON Digital Twin Neo4j knowledge graph.
   Extracted 5,809 entities and created 5,609 relationships with 94.5% validation pass rate.

   ## Data Provenance

   | Source File | Entities Extracted | Validation Status |
   |-------------|-------------------|-------------------|
   | reliability_energy_001.md | 723 | PASSED |
   | maintenance_chemical_002.md | 1,234 | PASSED |
   | safety_dams_003.md | 456 | PASSED |
   | ... | ... | ... |

   ## Quality Assurance

   - **Extraction Accuracy**: 97.8%
   - **Validation Pass Rate**: 94.5%
   - **Reliability Model Quality**: Average R² = 0.923
   - **Safety Coverage**: 100% of safety-critical equipment analyzed

   ## Performance Metrics

   - **Total Processing Time**: 67 minutes
   - **Throughput**: 86.7 entities/minute
   - **Bottleneck**: AGENT-5 (Event Extraction) - 28 minutes

   ## Recommendations

   1. Review 2 critical validation issues before production
   2. Obtain additional failure data for 47 equipment
   3. Schedule safety audits for 15 equipment with expired dates

   ## Sign-off

   - **Data Quality Approved**: AGENT-9 (Validation Agent)
   - **Audit Complete**: AGENT-10 (Audit Agent)
   - **Swarm Coordinator Approval**: AGENT-1
   ```

**OUTPUTS**:
- `audit_trail.json` - Complete provenance and change history
- `ingestion_report.md` - Human-readable final report
- `performance_metrics.json` - Agent performance and bottlenecks
- `quality_metrics.json` - Data quality statistics
- `provenance_cypher.cypher` - Neo4j statements for provenance nodes
- `compliance_documentation.pdf` - Standards compliance report

**COORDINATION**:
- Send final report to AGENT-1 (Coordinator) for sign-off
- Archive all agent outputs and logs
- Notify stakeholders of ingestion completion
- Trigger post-ingestion workflows (if configured)

---

## SWARM COORDINATION PROTOCOL

### Communication Pattern: HIERARCHICAL with MESH

```yaml
communication_flows:
  hierarchical:
    - AGENT-1 (Coordinator) broadcasts phase transitions to all agents
    - Agents report completion and issues back to AGENT-1
    - AGENT-1 aggregates results and makes go/no-go decisions

  mesh_coordination:
    planning_phase:
      - AGENT-2 ↔ AGENT-3: Schema validation against discovered data
      - AGENT-3 → AGENT-4,5,6,7,8: File assignments and priorities

    execution_phase:
      - AGENT-4 → AGENT-5: Equipment IDs for event linking
      - AGENT-4 → AGENT-7: Equipment list for model creation
      - AGENT-4 → AGENT-8: Equipment list for safety analysis
      - AGENT-5 → AGENT-7: Failure data for reliability modeling
      - AGENT-6 → AGENT-4,5,7,8: Standardized terminology
      - AGENT-7 → AGENT-8: Reliability predictions for risk calculations

    validation_phase:
      - AGENT-9 → AGENT-4,5,7,8: Validation issues for correction
      - AGENT-9 → AGENT-10: Validation results for audit
      - AGENT-10 → AGENT-1: Final audit report
```

### Synchronization Points

```yaml
phase_gates:
  planning_complete:
    condition: "AGENT-2 AND AGENT-3 both report completion"
    approval: "AGENT-1 reviews schema and file inventory"
    next_phase: "EXECUTION"

  extraction_complete:
    condition: "AGENT-4, AGENT-5, AGENT-6, AGENT-7, AGENT-8 all report completion"
    approval: "AGENT-1 verifies entity counts and Neo4j schema population"
    next_phase: "VALIDATION"

  validation_complete:
    condition: "AGENT-9 reports validation pass rate > 90%"
    approval: "AGENT-1 reviews validation report and decides on re-extraction or proceed"
    next_phase: "AUDIT OR RE-EXTRACTION"

  audit_complete:
    condition: "AGENT-10 produces final audit report"
    approval: "AGENT-1 signs off on ingestion"
    next_phase: "SWARM TERMINATION"
```

### Error Handling

```yaml
error_protocols:
  agent_failure:
    detection: "Agent does not report completion within expected time"
    action: "AGENT-1 reassigns task to backup agent or retries"
    escalation: "After 3 retries, mark task as FAILED and proceed with partial data"

  validation_failure:
    detection: "AGENT-9 reports validation pass rate < 90%"
    action: "AGENT-1 reviews issues, directs AGENT-4 through AGENT-8 to re-extract"
    threshold: "If pass rate < 70%, abort and flag for manual review"

  data_quality_issues:
    detection: "AGENT-3 reports files with quality score < 0.6"
    action: "Flag files for manual preprocessing or exclusion"
    escalation: "If >50% of files are low quality, abort and request better data"

  neo4j_constraint_violations:
    detection: "Duplicate equipment_id or invalid relationship reference"
    action: "AGENT-9 identifies offending entities, AGENT-4/5 corrects"
    prevention: "Pre-flight constraint check before bulk ingestion"
```

---

## SUCCESS CRITERIA AND DELIVERABLES

### Success Metrics

```yaml
quantitative_success:
  data_coverage:
    - all_8_files_processed: true
    - entities_extracted_per_file: "> 50"
    - total_equipment_nodes: "> 200"
    - total_failure_events: "> 1000"
    - total_maintenance_events: "> 2000"
    - reliability_models_created: "> 150"
    - safety_analyses_created: "> 50"

  data_quality:
    - extraction_accuracy: "> 95%"
    - validation_pass_rate: "> 90%"
    - reliability_model_r_squared: "> 0.85"
    - safety_coverage: "> 95% of safety-critical equipment"

  performance:
    - total_processing_time: "< 120 minutes"
    - agent_throughput: "> 50 entities/minute"
    - neo4j_ingestion_success: "> 99%"

qualitative_success:
  - RAMS schema integrated seamlessly with AEON graph
  - Predictive maintenance queries operational
  - Safety-critical equipment identified and SIL-classified
  - Reliability models validated and ready for predictions
  - Audit trail complete and compliance-ready
  - Stakeholder approval obtained
```

### Final Deliverables

```yaml
neo4j_deliverables:
  - neo4j_rams_schema.cypher: "Schema DDL with constraints and indexes"
  - equipment_cypher.cypher: "Equipment node MERGE statements"
  - events_cypher.cypher: "FailureEvent and MaintenanceEvent CREATE statements"
  - reliability_models_cypher.cypher: "ReliabilityModel MERGE statements"
  - safety_analysis_cypher.cypher: "SafetyAnalysis MERGE statements"
  - provenance_cypher.cypher: "Provenance tracking nodes"

json_deliverables:
  - equipment_entities.json: "All extracted equipment with RAMS properties"
  - failure_events.json: "All failure events"
  - maintenance_events.json: "All maintenance events"
  - reliability_models.json: "Fitted Weibull models"
  - safety_analysis.json: "Safety assessments and FMEA"
  - rams_entity_dictionary.json: "RAMS terminology and taxonomy"
  - validation_results.json: "Data quality and model validation results"
  - audit_trail.json: "Complete provenance and processing history"

documentation_deliverables:
  - ingestion_report.md: "Executive summary of ingestion process"
  - data_quality_report.md: "Quality assessment for each file"
  - validation_report.md: "Validation results and issues"
  - model_validation_report.md: "Reliability model fit quality"
  - safety_validation_report.md: "Safety analysis validation"
  - performance_report.md: "Agent performance and bottlenecks"
  - compliance_documentation.pdf: "Standards compliance report"

operational_deliverables:
  - rams_kpi_queries.cypher: "Dashboard queries for RAMS KPIs"
  - predictive_maintenance_queries.cypher: "RUL and failure prediction queries"
  - safety_monitoring_queries.cypher: "Safety-critical equipment monitoring"
  - rams_api_endpoints.yaml: "API specifications for RAMS analytics"
```

---

## EXECUTION TIMELINE

### Estimated Duration: 90 minutes (parallel execution)

```yaml
timeline:
  phase_1_planning:
    duration: "15 minutes"
    agents: [AGENT-2, AGENT-3]
    parallel: true
    activities:
      - "AGENT-2: Schema design (10 min)"
      - "AGENT-3: Data survey (15 min)"

  phase_2_extraction:
    duration: "50 minutes"
    agents: [AGENT-4, AGENT-5, AGENT-6, AGENT-7, AGENT-8]
    parallel: true
    activities:
      - "AGENT-4: Equipment extraction (25 min)"
      - "AGENT-5: Event extraction (35 min)"  # Bottleneck
      - "AGENT-6: NER (20 min)"
      - "AGENT-7: Reliability modeling (30 min)"
      - "AGENT-8: Safety analysis (28 min)"

  phase_3_validation:
    duration: "15 minutes"
    agents: [AGENT-9, AGENT-10]
    parallel: true
    activities:
      - "AGENT-9: Data validation (15 min)"
      - "AGENT-10: Audit trail generation (12 min)"

  phase_4_finalization:
    duration: "10 minutes"
    agents: [AGENT-1, AGENT-10]
    activities:
      - "AGENT-1: Result aggregation (5 min)"
      - "AGENT-10: Final report generation (10 min)"
      - "AGENT-1: Sign-off (2 min)"

  total_duration: "90 minutes"
  critical_path: "PLANNING → AGENT-5 (Event Extraction) → VALIDATION → FINALIZATION"
```

---

## POST-INGESTION VALIDATION

### Neo4j Graph Validation Queries

```cypher
// Validation Query 1: Verify schema constraints
SHOW CONSTRAINTS;

// Expected: equipment_id, failure_event_id, maintenance_event_id, reliability_model_id, safety_analysis_id

// Validation Query 2: Count nodes by type
MATCH (n)
RETURN labels(n) AS node_type, count(n) AS count
ORDER BY count DESC;

// Expected: Equipment (200+), FailureEvent (1000+), MaintenanceEvent (2000+), ReliabilityModel (150+), SafetyAnalysis (50+)

// Validation Query 3: Verify relationships
MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(r) AS count
ORDER BY count DESC;

// Expected: EXPERIENCED_FAILURE (1000+), RECEIVED_MAINTENANCE (2000+), HAS_RELIABILITY_MODEL (150+), HAS_SAFETY_ANALYSIS (50+)

// Validation Query 4: Check RAMS property completeness
MATCH (e:Equipment)
WHERE e.mtbf_hours IS NULL
   OR e.mttr_hours IS NULL
   OR e.availability_target IS NULL
RETURN count(e) AS equipment_missing_rams_properties;

// Expected: 0 (or close to 0)

// Validation Query 5: Verify reliability models
MATCH (e:Equipment)-[:HAS_RELIABILITY_MODEL]->(r:ReliabilityModel)
WHERE r.goodness_of_fit_r_squared < 0.85
RETURN count(r) AS low_quality_models, avg(r.goodness_of_fit_r_squared) AS avg_r_squared;

// Expected: low_quality_models < 10%, avg_r_squared > 0.90

// Validation Query 6: Check safety coverage
MATCH (e:Equipment)
WHERE e.safety_critical = true
WITH count(e) AS total_safety_critical
MATCH (e:Equipment)-[:HAS_SAFETY_ANALYSIS]->(s:SafetyAnalysis)
WHERE e.safety_critical = true
RETURN total_safety_critical, count(e) AS with_safety_analysis,
       round(count(e) * 100.0 / total_safety_critical, 1) AS coverage_percent;

// Expected: coverage_percent > 95%

// Validation Query 7: Test predictive maintenance query
MATCH (e:Equipment)-[:HAS_RELIABILITY_MODEL]->(r:ReliabilityModel)
WITH e, r,
     duration.inHours(datetime(), datetime(e.last_failure_date)) AS hours_since_failure,
     r.weibull_scale_eta * (-ln(0.90))^(1/r.weibull_shape_beta) -
       duration.inHours(datetime(), datetime(e.last_failure_date)) AS rul_hours
WHERE rul_hours > 0 AND rul_hours < 2000
RETURN e.equipment_id,
       round(hours_since_failure, 0) AS hours_since_failure,
       round(rul_hours, 0) AS rul_hours,
       CASE
         WHEN rul_hours < 168 THEN "URGENT"
         WHEN rul_hours < 720 THEN "HIGH"
         ELSE "MEDIUM"
       END AS priority
ORDER BY rul_hours ASC
LIMIT 10;

// Expected: 10 equipment with RUL predictions and priority rankings

// Validation Query 8: Verify FMEA data
MATCH (e:Equipment)-[:HAS_SAFETY_ANALYSIS]->(s:SafetyAnalysis)
WHERE s.risk_priority_number > 100
RETURN e.equipment_id,
       s.safety_integrity_level,
       s.risk_priority_number,
       s.consequence_category
ORDER BY s.risk_priority_number DESC
LIMIT 10;

// Expected: 10 high-RPN equipment with SIL classifications
```

---

## INTEGRATION WITH AEON DIGITAL TWIN

### Cross-Enhancement Integration Points

```yaml
integration_hooks:
  enhancement_01_graph_schema:
    integration: "RAMS extends Equipment nodes with reliability properties"
    action: "Add RAMS properties to existing Equipment nodes via MERGE"
    validation: "Ensure no equipment_id conflicts with existing nodes"

  enhancement_02_temporal_dynamics:
    integration: "FailureEvent and MaintenanceEvent provide temporal patterns"
    action: "Link events to temporal timeline for time-series analysis"
    query: "Failure rate trends over time, maintenance schedule adherence"

  enhancement_03_geospatial:
    integration: "Equipment location for technician dispatch optimization"
    action: "Spatial queries for nearest spare parts depot, technician proximity"
    benefit: "Reduce MTTR through optimized logistics"

  enhancement_04_threat_modeling:
    integration: "Cyber-physical attack impact on equipment reliability"
    action: "Model safety system compromise scenarios"
    query: "Equipment vulnerable to cascading failures from cyber attacks"

  enhancement_05_predictive_analytics:
    integration: "Reliability models feed into predictive platform"
    action: "RUL predictions, failure probability forecasting"
    benefit: "Proactive maintenance scheduling, downtime prevention"

  enhancement_06_cognitive_behavioral:
    integration: "Human factors in maintenance errors and operator behavior"
    action: "Link failure causes to cognitive biases, human error probability"
    query: "Failures attributed to human factors, training effectiveness"

  enhancement_07_psychometric_ner:
    integration: "Extract RAMS entities from unstructured text"
    action: "NER for failure descriptions, maintenance procedures"
    benefit: "Automated extraction of RAMS data from reports"

  enhancement_09_nlp_query:
    integration: "Natural language queries for RAMS analytics"
    action: "Convert questions like 'What will fail next?' to Cypher"
    example: "'Show me equipment with high failure risk' → RUL query"
```

### API Endpoint Integration

```yaml
rams_api_integration:
  predictive_maintenance_endpoint:
    method: POST
    path: "/api/rams/predictive/prioritization"
    description: "Get predictive maintenance priority queue"
    request:
      site_id: "SITE-001"
      priority_threshold: "HIGH"
      forecast_horizon_days: 90
    response:
      maintenance_queue: [...]
      total_cost_avoidance: 1250000
      urgent_count: 12

  reliability_prediction_endpoint:
    method: GET
    path: "/api/rams/reliability/predict"
    description: "Predict equipment failure probability"
    params:
      equipment_id: "EQUIP-001"
      prediction_horizon_days: 30
    response:
      failure_probability: 0.15
      confidence: 0.87
      rul_days: 52
      recommended_action: "SCHEDULE_PM"

  safety_dashboard_endpoint:
    method: GET
    path: "/api/rams/safety/critical"
    description: "Get safety-critical equipment status"
    params:
      sil_levels: ["SIL-3", "SIL-4"]
    response:
      critical_equipment: [...]
      compliance_status: "87/87 compliant"
      overdue_audits: 3
```

---

## APPENDICES

### Appendix A: RAMS Terminology Glossary

```yaml
rams_terms:
  mtbf: "Mean Time Between Failures - Average operating time between failures"
  mttr: "Mean Time To Repair - Average time to restore to operational status"
  mttf: "Mean Time To Failure - Average time to first failure (non-repairable)"
  mdt: "Mean Down Time - Total downtime including administrative delays"
  availability: "Proportion of time equipment is operational (MTBF / (MTBF + MTTR))"
  reliability: "Probability equipment performs intended function for specified time"
  failure_rate: "Lambda (λ) - Instantaneous rate of failure (failures per hour)"
  hazard_rate: "Instantaneous failure rate at time t (can vary with age)"
  weibull_distribution: "Probability distribution for equipment lifetime modeling"
  sil: "Safety Integrity Level - IEC 61508 classification (SIL-1 to SIL-4)"
  pfd: "Probability of Failure on Demand - For safety instrumented systems"
  fmea: "Failure Mode and Effects Analysis - Systematic failure identification"
  rpn: "Risk Priority Number - Severity × Occurrence × Detection in FMEA"
  rul: "Remaining Useful Life - Time until equipment reaches reliability threshold"
```

### Appendix B: Weibull Distribution Parameters

```yaml
weibull_interpretation:
  shape_parameter_beta:
    beta_less_than_1:
      meaning: "Decreasing failure rate (infant mortality)"
      example: "Manufacturing defects, burn-in period"
      action: "Extended commissioning, infant mortality testing"

    beta_equals_1:
      meaning: "Constant failure rate (random failures)"
      example: "Electronic components, exponential distribution"
      action: "Time-based replacement not effective, use condition monitoring"

    beta_greater_than_1:
      meaning: "Increasing failure rate (wear-out)"
      example: "Mechanical wear, fatigue, aging"
      action: "Preventive maintenance before characteristic life"

    typical_values:
      electronics: "0.5 - 1.0"
      mechanical: "1.5 - 2.5"
      bearings: "1.1 - 1.5"
      fatigue: "2.0 - 4.0"

  scale_parameter_eta:
    meaning: "Characteristic life - Time at which 63.2% have failed"
    relationship_to_mtbf: "MTBF = η * Γ(1 + 1/β)"
    usage: "Determines overall reliability level"
```

### Appendix C: Safety Integrity Level (SIL) Reference

```yaml
sil_reference_table:
  sil_1:
    pfd_range: "10^-1 to 10^-2"
    risk_reduction_factor: "10 to 100"
    consequence: "Minor injury"
    typical_application: "Non-critical process equipment"

  sil_2:
    pfd_range: "10^-2 to 10^-3"
    risk_reduction_factor: "100 to 1,000"
    consequence: "Serious injury"
    typical_application: "Industrial process control"

  sil_3:
    pfd_range: "10^-3 to 10^-4"
    risk_reduction_factor: "1,000 to 10,000"
    consequence: "Multiple fatalities"
    typical_application: "Critical infrastructure safety systems"

  sil_4:
    pfd_range: "< 10^-4"
    risk_reduction_factor: "> 10,000"
    consequence: "Catastrophic"
    typical_application: "Nuclear, aerospace, high-consequence systems"
```

---

## EXECUTION COMMAND

```bash
# Initialize RAMS ingestion swarm
npx claude-flow@alpha swarm init --topology hierarchical --max-agents 10

# Spawn AGENT-1 (Swarm Coordinator)
npx claude-flow@alpha agent spawn --type coordinator --agent-id AGENT-1 \
  --instructions "Orchestrate 10-agent RAMS ingestion swarm per TASKMASTER_RAMS_v1.0.md"

# AGENT-1 will spawn remaining agents (AGENT-2 through AGENT-10) and coordinate execution

# Monitor swarm progress
npx claude-flow@alpha swarm status --swarm-id RAMS-INGEST-20251125-001

# Retrieve final results
npx claude-flow@alpha swarm results --swarm-id RAMS-INGEST-20251125-001 \
  --output-dir /home/jim/2_OXOT_Projects_Dev/Enhancement_08_RAMS_Reliability/results
```

---

**TASKMASTER COMPLETE**

**Version:** v1.0.0
**Created:** 2025-11-25 14:35:00 UTC
**Status:** READY FOR EXECUTION
**Total Lines:** 1,750+
**Agent Count:** 10
**Estimated Duration:** 90 minutes
**Success Probability:** 95%

🎯 **MISSION**: Transform 8 RAMS files into predictive maintenance intelligence
🤖 **SWARM**: 10 specialized agents working in parallel
📊 **TARGET**: 200+ equipment with reliability models, safety analysis, and RUL predictions
✅ **DELIVERABLE**: Production-ready RAMS analytics in Neo4j knowledge graph
