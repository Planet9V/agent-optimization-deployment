// ═══════════════════════════════════════════════════════════════════════
// GAP-004 PHASE 1 RELATIONSHIP PATTERNS
// ═══════════════════════════════════════════════════════════════════════
// File: gap004_relationships.cypher
// Created: 2025-11-13
// Purpose: Define relationship patterns for 35 new node types
// Target: 50+ relationship types connecting new and existing nodes
// Deployment Order: Execute AFTER indexes (for reference only - actual
//                   relationships created during data ingestion)
// ═══════════════════════════════════════════════════════════════════════

// -----------------------------------------------------------------------
// SECTION 1: UC2 - CYBER-PHYSICAL ATTACK DETECTION RELATIONSHIPS
// -----------------------------------------------------------------------

// Digital Twin to Asset Modeling
// DigitalTwinState represents expected behavior of physical assets
// (dt:DigitalTwinState)-[:MODELS_ASSET]->(device:Device|Component)

// Sensor to Asset Monitoring
// PhysicalSensor captures actual readings from devices
// (sensor:PhysicalSensor)-[:MONITORS_ASSET]->(device:Device|Component)

// Sensor to Digital Twin Comparison
// Compare actual vs expected states for anomaly detection
// (sensor:PhysicalSensor)-[:ACTUAL_STATE]->(dt:DigitalTwinState)
// (dt:DigitalTwinState)<-[:EXPECTED_STATE]-(sensor:PhysicalSensor)

// Actuator Control Relationships
// (actuator:PhysicalActuator)-[:CONTROLS_ASSET]->(device:Device|Component)
// (actuator:PhysicalActuator)-[:COMMAND_MATCHES]->(dt:DigitalTwinState)
// (actuator:PhysicalActuator)-[:PART_OF_LOOP]->(loop:ProcessLoop)

// Physics Constraint Enforcement
// (constraint:PhysicsConstraint)-[:CONSTRAINS_ASSET]->(device:Device|Component)
// (constraint:PhysicsConstraint)-[:VIOLATED_BY]->(deviation:StateDeviation)
// (constraint:PhysicsConstraint)-[:ENFORCED_BY]->(safety:SafetyFunction)

// State Deviation Detection
// (deviation:StateDeviation)-[:DETECTED_ON]->(device:Device|Component)
// (deviation:StateDeviation)-[:EXPECTED_FROM]->(dt:DigitalTwinState)
// (deviation:StateDeviation)-[:ACTUAL_FROM]->(sensor:PhysicalSensor)
// (deviation:StateDeviation)-[:VIOLATES]->(constraint:PhysicsConstraint)
// (deviation:StateDeviation)-[:CORRELATES_WITH]->(cve:CVE|Technique)

// Process Loop Control
// (loop:ProcessLoop)-[:CONTROLS]->(device:Device|Component)
// (loop:ProcessLoop)-[:READS_FROM]->(sensor:PhysicalSensor)
// (loop:ProcessLoop)-[:COMMANDS]->(actuator:PhysicalActuator)

// Safety Function Protection
// (safety:SafetyFunction)-[:PROTECTS_ASSET]->(device:Device|Component)
// (safety:SafetyFunction)-[:SAFETY_INTERLOCK]->(dependency:SafetyFunction)
// (safety:SafetyFunction)-[:MONITORS_INPUT]->(sensor:PhysicalSensor)
// (safety:SafetyFunction)-[:TRIGGERS_OUTPUT]->(actuator:PhysicalActuator)

// Safety Interlock Dependencies
// (source:SafetyFunction)-[:HAS_INTERLOCK]->(interlock:SafetyInterlock)-[:REQUIRES]->(dependent:SafetyFunction)
// (interlock:SafetyInterlock)-[:BYPASSED_BY]->(user:User)

// Integration with Existing Nodes
// (cve:CVE)-[:AFFECTS_SENSOR]->(sensor:PhysicalSensor)
// (cve:CVE)-[:AFFECTS_ACTUATOR]->(actuator:PhysicalActuator)
// (technique:Technique)-[:CAUSES]->(deviation:StateDeviation)
// (threatActor:ThreatActor)-[:RESPONSIBLE_FOR]->(deviation:StateDeviation)

// -----------------------------------------------------------------------
// SECTION 2: UC3 - CASCADING FAILURE SIMULATION RELATIONSHIPS
// -----------------------------------------------------------------------

// Cascade Event Propagation
// (cascade:CascadeSimulation)-[:INCLUDES]->(event:CascadeEvent)
// (event:CascadeEvent)-[:AFFECTS]->(asset:Device|Component)
// (event:CascadeEvent)-[:CAUSED_BY]->(priorEvent:CascadeEvent)
// (event:CascadeEvent)-[:HAS_IMPACT]->(impact:ImpactAssessment)
// (event:CascadeEvent)-[:PROPAGATES_VIA]->(link:DependencyLink)

// Dependency Link Modeling
// (source:Device|Component)-[:PROVIDES_TO]->(link:DependencyLink)-[:REQUIRED_BY]->(target:Device|Component)
// (link:DependencyLink)-[:USES_RULE]->(rule:PropagationRule)

// Propagation Rule Application
// (rule:PropagationRule)-[:APPLIES_TO]->(link:DependencyLink)
// (rule:PropagationRule)-[:TRIGGERS]->(event:CascadeEvent)

// Impact Assessment
// (event:CascadeEvent)-[:HAS_IMPACT]->(impact:ImpactAssessment)
// (impact:ImpactAssessment)-[:AFFECTS_SECTOR]->(sector:IndustrialSector)
// (impact:ImpactAssessment)-[:AFFECTS_SERVICE]->(service:ServiceLevel)

// System Resilience Metrics
// (asset:Device|Component)-[:HAS_RESILIENCE]->(resilience:SystemResilience)
// (resilience:SystemResilience)-[:MEASURED_BY]->(metric:OperationalMetric)

// Cross-Infrastructure Dependencies
// (primary:Device|Component {sector: primaryInfra})-[:CROSS_SECTOR_DEP]->(dep:CrossInfrastructureDependency)-[:IMPACTS]->(dependent:Device|Component {sector: dependentInfra})

// Integration with Existing Nodes
// (cve:CVE)-[:ENABLES_CASCADE]->(cascade:CascadeEvent)
// (threatActor:ThreatActor)-[:EXPLOITS]->(dep:DependencyLink)

// -----------------------------------------------------------------------
// SECTION 3: R6 - TEMPORAL REASONING RELATIONSHIPS
// -----------------------------------------------------------------------

// Temporal Event Storage
// (event:TemporalEvent)-[:TARGETS]->(asset:Device|Component)
// (event:TemporalEvent)-[:USES_TECHNIQUE]->(technique:Technique)
// (event:TemporalEvent)-[:PART_OF_PATTERN]->(pattern:TemporalPattern)
// (event:TemporalEvent)-[:STORED_IN]->(store:EventStore)

// Event Store Management
// (event:TemporalEvent)-[:STORED_IN]->(store:EventStore)
// (store:EventStore)-[:ARCHIVES_TO]->(archiveStore:EventStore)

// Temporal Pattern Recognition
// (pattern:TemporalPattern)-[:MATCHES_EVENTS]->(event:TemporalEvent)
// (pattern:TemporalPattern)-[:INDICATES_ATTACK]->(attack:ThreatActor|Campaign)

// Time Series Analysis
// (analysis:TimeSeriesAnalysis)-[:ANALYZES_METRIC]->(asset:Device|Component)
// (analysis:TimeSeriesAnalysis)-[:DETECTS_ANOMALY]->(event:TemporalEvent)

// Historical Snapshots
// (snapshot:HistoricalSnapshot)-[:CAPTURES_STATE]->(asset:Device|Component|Network|Organization)
// (snapshot:HistoricalSnapshot)-[:TRIGGERED_BY]->(event:TemporalEvent|CascadeEvent)

// Bitemporal Versioning
// (current:Software)-[:HAS_VERSION]->(version:VersionedNode)
// (version:VersionedNode)-[:PREVIOUS_VERSION]->(priorVersion:VersionedNode)
// (version:VersionedNode)-[:HAD_VULNERABILITY]->(cve:CVE)

// Integration with Existing Nodes
// (device:Device)-[:GENERATES]->(event:TemporalEvent)
// (technique:Technique)-[:GENERATES_EVENT]->(event:TemporalEvent)

// -----------------------------------------------------------------------
// SECTION 4: CG-9 - OPERATIONAL IMPACT MODELING RELATIONSHIPS
// -----------------------------------------------------------------------

// Operational Metrics
// (metric:OperationalMetric)-[:MEASURES]->(asset:Device|Component|Train|Network)
// (metric:OperationalMetric)-[:IMPACTS]->(sla:ServiceLevel)
// (metric:OperationalMetric)-[:TRIGGERS_ALERT]->(alert:AlertRule)

// Service Level Agreement
// (service:ServiceLevel)-[:APPLIES_TO]->(asset:Device|Component|Train)
// (service:ServiceLevel)-[:BREACHED_BY]->(event:DisruptionEvent)
// (service:ServiceLevel)-[:MEASURED_BY]->(metric:OperationalMetric)

// Customer Impact Tracking
// (impact:CustomerImpact)-[:CAUSED_BY]->(event:DisruptionEvent)
// (impact:CustomerImpact)-[:AFFECTS_CUSTOMER]->(customer:Organization)
// (impact:CustomerImpact)-[:REQUIRES_COMPENSATION]->(amount:float)

// Revenue Model Application
// (model:RevenueModel)-[:APPLIES_TO]->(asset:Device|Component|Train)
// (model:RevenueModel)-[:CALCULATES_LOSS]->(impact:ImpactAssessment)

// Disruption Event Analysis
// (event:DisruptionEvent)-[:CAUSED_BY]->(cause:CVE|ThreatActor|Component)
// (event:DisruptionEvent)-[:IMPACTS]->(asset:Device|Component|Train)
// (event:DisruptionEvent)-[:BREACHES]->(sla:ServiceLevel)
// (event:DisruptionEvent)-[:AFFECTS_CUSTOMERS]->(impact:CustomerImpact)
// (event:DisruptionEvent)-[:FINANCIAL_IMPACT]->(assessment:ImpactAssessment)

// Integration with Existing Nodes
// (cve:CVE)-[:CAUSES_DISRUPTION]->(event:DisruptionEvent)
// (threatActor:ThreatActor)-[:CAUSES]->(event:DisruptionEvent)

// -----------------------------------------------------------------------
// SECTION 5: UC1 - SCADA ATTACK RECONSTRUCTION RELATIONSHIPS
// -----------------------------------------------------------------------

// SCADA Event Tracking
// (event:SCADAEvent)-[:TARGETS]->(device:Device)
// (event:SCADAEvent)-[:USES_PROTOCOL]->(protocol:Protocol)
// (event:SCADAEvent)-[:PART_OF]->(timeline:AttackTimeline)

// HMI Session Interaction
// (session:HMISession)-[:INITIATED_ON]->(hmi:HMI)
// (session:HMISession)-[:PERFORMED_BY]->(user:User)
// (session:HMISession)-[:CONTAINS]->(event:SCADAEvent)

// PLC State Changes
// (change:PLCStateChange)-[:STATE_OF]->(plc:PLC)
// (change:PLCStateChange)-[:TRIGGERED_BY]->(event:SCADAEvent)
// (change:PLCStateChange)-[:CORRELATES_WITH]->(correlation:EventCorrelation)

// RTU Communications
// (comm:RTUCommunication)-[:FROM]->(rtu:RTU)
// (comm:RTUCommunication)-[:TO]->(masterStation:MasterStation)
// (comm:RTUCommunication)-[:CONTAINS_DATA]->(dataPoint:DataPoint)

// Event Correlation
// (correlation:EventCorrelation)-[:CORRELATES]->(event:SCADAEvent)
// (correlation:EventCorrelation)-[:IDENTIFIES]->(attackPhase:AttackPhase)
// (correlation:EventCorrelation)-[:PART_OF]->(timeline:AttackTimeline)

// Attack Timeline Reconstruction
// (timeline:AttackTimeline)-[:RECONSTRUCTS]->(attack:Attack)
// (timeline:AttackTimeline)-[:INCLUDES]->(event:SCADAEvent)
// (timeline:AttackTimeline)-[:INCLUDES]->(correlation:EventCorrelation)

// Integration with Existing Nodes
// (technique:Technique)-[:GENERATES]->(event:SCADAEvent)
// (threatActor:ThreatActor)-[:EXECUTES]->(timeline:AttackTimeline)

// -----------------------------------------------------------------------
// SECTION 6: SUPPORTING INTEGRATION RELATIONSHIPS
// -----------------------------------------------------------------------

// Data Flow Modeling
// (flow:DataFlow)-[:FROM]->(source:Device|Component)
// (flow:DataFlow)-[:TO]->(destination:Device|Component)
// (flow:DataFlow)-[:CARRIES]->(dataType:DataType)

// Alert Rules
// (rule:AlertRule)-[:MONITORS]->(metric:OperationalMetric)
// (rule:AlertRule)-[:TRIGGERS]->(remediation:RemediationPlan)
// (rule:AlertRule)-[:NOTIFIES]->(contact:Contact)

// Remediation Plans
// (plan:RemediationPlan)-[:RESPONDS_TO]->(event:DisruptionEvent|StateDeviation)
// (plan:RemediationPlan)-[:INCLUDES_STEP]->(step:RemediationStep)
// (plan:RemediationPlan)-[:EXECUTED_BY]->(system:AutomationSystem)

// ═══════════════════════════════════════════════════════════════════════
// RELATIONSHIP PATTERN DEFINITION COMPLETE
// Total Relationship Types: 50+ defined patterns
// Purpose: Reference for data ingestion and graph modeling
// Note: Actual relationship instances created during data import
// Next Step: Execute gap004_deploy.sh for deployment
// ═══════════════════════════════════════════════════════════════════════

// -----------------------------------------------------------------------
// EXAMPLE RELATIONSHIP CREATION (for testing/validation)
// -----------------------------------------------------------------------

// Uncomment to create sample relationships after nodes exist:

/*
// Example 1: Link Digital Twin to Physical Device
MATCH (dt:DigitalTwinState {stateId: "dt-state-plc-001-20251113150000"})
MATCH (device:Device {id: "device-plc-001"})
CREATE (dt)-[:MODELS_ASSET]->(device);

// Example 2: Link Sensor to Asset
MATCH (sensor:PhysicalSensor {sensorId: "sensor-temp-plc001-01"})
MATCH (device:Device {id: "device-plc-001"})
CREATE (sensor)-[:MONITORS_ASSET]->(device);

// Example 3: Link State Deviation to CVE
MATCH (deviation:StateDeviation {deviationId: "deviation-plc001-20251113153007"})
MATCH (cve:CVE {cveId: "CVE-2010-2568"})
CREATE (cve)-[:CAUSES_DEVIATION]->(deviation);

// Example 4: Link Cascade Event to Impact Assessment
MATCH (event:CascadeEvent {eventId: "cascade-sim001-003"})
MATCH (impact:ImpactAssessment {impactId: "impact-cascade-sim001-003"})
CREATE (event)-[:HAS_IMPACT]->(impact);

// Example 5: Link Temporal Event to Attack Pattern
MATCH (event:TemporalEvent {eventId: "temporal-event-001"})
MATCH (pattern:TemporalPattern {patternId: "pattern-apt-reconnaissance"})
CREATE (event)-[:PART_OF_PATTERN]->(pattern);
*/
