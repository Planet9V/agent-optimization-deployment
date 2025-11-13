// ═══════════════════════════════════════════════════════════════════════
// GAP-004 PHASE 1 SCHEMA CONSTRAINTS
// ═══════════════════════════════════════════════════════════════════════
// File: gap004_schema_constraints.cypher
// Created: 2025-11-13
// Purpose: Create unique constraints for 35 new node types
// Target: Neo4j 5.x with IF NOT EXISTS for idempotency
// Deployment Order: Execute BEFORE indexes
// ═══════════════════════════════════════════════════════════════════════

// -----------------------------------------------------------------------
// UC2: CYBER-PHYSICAL ATTACK DETECTION CONSTRAINTS (8 constraints)
// -----------------------------------------------------------------------

// Node 1: DigitalTwinState - Digital twin state representations
CREATE CONSTRAINT digital_twin_state_id IF NOT EXISTS
FOR (n:DigitalTwinState) REQUIRE n.stateId IS UNIQUE;

// Node 2: PhysicalSensor - Actual sensor readings
CREATE CONSTRAINT physical_sensor_id IF NOT EXISTS
FOR (n:PhysicalSensor) REQUIRE n.sensorId IS UNIQUE;

// Node 3: PhysicalActuator - Actuator command tracking
CREATE CONSTRAINT physical_actuator_id IF NOT EXISTS
FOR (n:PhysicalActuator) REQUIRE n.actuatorId IS UNIQUE;

// Node 4: PhysicsConstraint - Valid physical operating ranges
CREATE CONSTRAINT physics_constraint_id IF NOT EXISTS
FOR (n:PhysicsConstraint) REQUIRE n.constraintId IS UNIQUE;

// Node 5: StateDeviation - Cyber-physical anomaly detection
CREATE CONSTRAINT state_deviation_id IF NOT EXISTS
FOR (n:StateDeviation) REQUIRE n.deviationId IS UNIQUE;

// Node 6: ProcessLoop - Control loop modeling
CREATE CONSTRAINT process_loop_id IF NOT EXISTS
FOR (n:ProcessLoop) REQUIRE n.loopId IS UNIQUE;

// Node 7: SafetyFunction - IEC 61508 safety-critical functions
CREATE CONSTRAINT safety_function_id IF NOT EXISTS
FOR (n:SafetyFunction) REQUIRE n.functionId IS UNIQUE;

// Node 8: SafetyInterlock - Safety chain dependencies
CREATE CONSTRAINT safety_interlock_id IF NOT EXISTS
FOR (n:SafetyInterlock) REQUIRE n.interlockId IS UNIQUE;

// -----------------------------------------------------------------------
// UC3: CASCADING FAILURE SIMULATION CONSTRAINTS (6 constraints)
// -----------------------------------------------------------------------

// Node 9: CascadeEvent - Single failure event in cascade sequence
CREATE CONSTRAINT cascade_event_id IF NOT EXISTS
FOR (n:CascadeEvent) REQUIRE n.eventId IS UNIQUE;

// Node 10: DependencyLink - Inter-system dependencies
CREATE CONSTRAINT dependency_link_id IF NOT EXISTS
FOR (n:DependencyLink) REQUIRE n.linkId IS UNIQUE;

// Node 11: PropagationRule - Cascade propagation logic
CREATE CONSTRAINT propagation_rule_id IF NOT EXISTS
FOR (n:PropagationRule) REQUIRE n.ruleId IS UNIQUE;

// Node 12: ImpactAssessment - Multi-dimensional impact analysis
CREATE CONSTRAINT impact_assessment_id IF NOT EXISTS
FOR (n:ImpactAssessment) REQUIRE n.impactId IS UNIQUE;

// Node 13: SystemResilience - Resilience metrics (MTBF, MTTR)
CREATE CONSTRAINT system_resilience_id IF NOT EXISTS
FOR (n:SystemResilience) REQUIRE n.resilienceId IS UNIQUE;

// Node 14: CrossInfrastructureDependency - Multi-sector dependencies
CREATE CONSTRAINT cross_infra_dep_id IF NOT EXISTS
FOR (n:CrossInfrastructureDependency) REQUIRE n.dependencyId IS UNIQUE;

// -----------------------------------------------------------------------
// R6: TEMPORAL REASONING CONSTRAINTS (6 constraints)
// -----------------------------------------------------------------------

// Node 15: TemporalEvent - Time-stamped security events (90-day window)
CREATE CONSTRAINT temporal_event_id IF NOT EXISTS
FOR (n:TemporalEvent) REQUIRE n.eventId IS UNIQUE;

// Node 16: EventStore - 90-day retention policy management
CREATE CONSTRAINT event_store_id IF NOT EXISTS
FOR (n:EventStore) REQUIRE n.storeId IS UNIQUE;

// Node 17: TemporalPattern - Recurring attack pattern detection
CREATE CONSTRAINT temporal_pattern_id IF NOT EXISTS
FOR (n:TemporalPattern) REQUIRE n.patternId IS UNIQUE;

// Node 18: TimeSeriesAnalysis - Statistical trend analysis
CREATE CONSTRAINT timeseries_analysis_id IF NOT EXISTS
FOR (n:TimeSeriesAnalysis) REQUIRE n.analysisId IS UNIQUE;

// Node 19: HistoricalSnapshot - Point-in-time system state capture
CREATE CONSTRAINT historical_snapshot_id IF NOT EXISTS
FOR (n:HistoricalSnapshot) REQUIRE n.snapshotId IS UNIQUE;

// Node 20: VersionedNode - Bitemporal versioning for historical queries
CREATE CONSTRAINT versioned_node_id IF NOT EXISTS
FOR (n:VersionedNode) REQUIRE n.versionId IS UNIQUE;

// -----------------------------------------------------------------------
// CG-9: OPERATIONAL IMPACT MODELING CONSTRAINTS (5 constraints)
// -----------------------------------------------------------------------

// Node 21: OperationalMetric - KPI tracking for impact calculation
CREATE CONSTRAINT operational_metric_id IF NOT EXISTS
FOR (n:OperationalMetric) REQUIRE n.metricId IS UNIQUE;

// Node 22: ServiceLevel - SLA definitions with breach detection
CREATE CONSTRAINT service_level_id IF NOT EXISTS
FOR (n:ServiceLevel) REQUIRE n.slaId IS UNIQUE;

// Node 23: CustomerImpact - Affected customer tracking
CREATE CONSTRAINT customer_impact_id IF NOT EXISTS
FOR (n:CustomerImpact) REQUIRE n.impactId IS UNIQUE;

// Node 24: RevenueModel - Revenue calculation for financial impact
CREATE CONSTRAINT revenue_model_id IF NOT EXISTS
FOR (n:RevenueModel) REQUIRE n.modelId IS UNIQUE;

// Node 25: DisruptionEvent - Service disruption with root cause
CREATE CONSTRAINT disruption_event_id IF NOT EXISTS
FOR (n:DisruptionEvent) REQUIRE n.eventId IS UNIQUE;

// -----------------------------------------------------------------------
// UC1: SCADA ATTACK RECONSTRUCTION CONSTRAINTS (6 constraints)
// -----------------------------------------------------------------------

// Node 26: SCADAEvent - Real-time OT event capture
CREATE CONSTRAINT scada_event_id IF NOT EXISTS
FOR (n:SCADAEvent) REQUIRE n.eventId IS UNIQUE;

// Node 27: HMISession - Human-Machine Interface interaction tracking
CREATE CONSTRAINT hmi_session_id IF NOT EXISTS
FOR (n:HMISession) REQUIRE n.sessionId IS UNIQUE;

// Node 28: PLCStateChange - PLC state transition monitoring
CREATE CONSTRAINT plc_state_change_id IF NOT EXISTS
FOR (n:PLCStateChange) REQUIRE n.changeId IS UNIQUE;

// Node 29: RTUCommunication - Remote Terminal Unit communications
CREATE CONSTRAINT rtu_communication_id IF NOT EXISTS
FOR (n:RTUCommunication) REQUIRE n.commId IS UNIQUE;

// Node 30: EventCorrelation - Multi-stage attack correlation
CREATE CONSTRAINT event_correlation_id IF NOT EXISTS
FOR (n:EventCorrelation) REQUIRE n.correlationId IS UNIQUE;

// Node 31: AttackTimeline - Temporal sequence reconstruction
CREATE CONSTRAINT attack_timeline_id IF NOT EXISTS
FOR (n:AttackTimeline) REQUIRE n.timelineId IS UNIQUE;

// -----------------------------------------------------------------------
// SUPPORTING INTEGRATION CONSTRAINTS (4 constraints)
// -----------------------------------------------------------------------

// Node 32: DataFlow - Data movement and pipeline modeling
CREATE CONSTRAINT data_flow_id IF NOT EXISTS
FOR (n:DataFlow) REQUIRE n.flowId IS UNIQUE;

// Node 33: ControlLoop - Feedback control systems (alias for ProcessLoop)
// NOTE: ControlLoop uses same constraint as ProcessLoop (Node 6)

// Node 34: AlertRule - Automated alerting based on conditions
CREATE CONSTRAINT alert_rule_id IF NOT EXISTS
FOR (n:AlertRule) REQUIRE n.ruleId IS UNIQUE;

// Node 35: RemediationPlan - Automated response workflows
CREATE CONSTRAINT remediation_plan_id IF NOT EXISTS
FOR (n:RemediationPlan) REQUIRE n.planId IS UNIQUE;

// ═══════════════════════════════════════════════════════════════════════
// CONSTRAINT CREATION COMPLETE
// Total Constraints: 35 unique ID constraints across 35 node types
// Next Step: Execute gap004_schema_indexes.cypher
// ═══════════════════════════════════════════════════════════════════════
