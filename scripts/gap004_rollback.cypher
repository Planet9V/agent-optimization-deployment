// ═══════════════════════════════════════════════════════════════════════
// GAP-004 PHASE 1 SCHEMA ROLLBACK SCRIPT
// ═══════════════════════════════════════════════════════════════════════
// File: gap004_rollback.cypher
// Created: 2025-11-13
// Purpose: Safe rollback of GAP-004 Phase 1 schema changes
// WARNING: This will DROP all constraints and indexes created in Phase 1
// Usage: Execute only if deployment needs to be reverted
// ═══════════════════════════════════════════════════════════════════════

// -----------------------------------------------------------------------
// ROLLBACK SEQUENCE:
// 1. Drop indexes first (indexes depend on constraints)
// 2. Drop constraints second
// 3. Optionally delete nodes (commented out for safety)
// -----------------------------------------------------------------------

// ═══════════════════════════════════════════════════════════════════════
// SECTION 1: DROP INDEXES (70+ indexes)
// ═══════════════════════════════════════════════════════════════════════

// Multi-tenant isolation indexes (35 indexes)
DROP INDEX digital_twin_namespace IF EXISTS;
DROP INDEX sensor_namespace IF EXISTS;
DROP INDEX actuator_namespace IF EXISTS;
DROP INDEX constraint_namespace IF EXISTS;
DROP INDEX deviation_namespace IF EXISTS;
DROP INDEX loop_namespace IF EXISTS;
DROP INDEX safety_namespace IF EXISTS;
DROP INDEX interlock_namespace IF EXISTS;
DROP INDEX cascade_event_namespace IF EXISTS;
DROP INDEX dep_link_namespace IF EXISTS;
DROP INDEX prop_rule_namespace IF EXISTS;
DROP INDEX impact_namespace IF EXISTS;
DROP INDEX resilience_namespace IF EXISTS;
DROP INDEX cross_dep_namespace IF EXISTS;
DROP INDEX temporal_event_namespace IF EXISTS;
DROP INDEX event_store_namespace IF EXISTS;
DROP INDEX temp_pattern_namespace IF EXISTS;
DROP INDEX timeseries_namespace IF EXISTS;
DROP INDEX snapshot_namespace IF EXISTS;
DROP INDEX versioned_namespace IF EXISTS;
DROP INDEX metric_namespace IF EXISTS;
DROP INDEX sla_namespace IF EXISTS;
DROP INDEX customer_impact_namespace IF EXISTS;
DROP INDEX revenue_namespace IF EXISTS;
DROP INDEX disruption_namespace IF EXISTS;
DROP INDEX scada_event_namespace IF EXISTS;
DROP INDEX hmi_namespace IF EXISTS;
DROP INDEX plc_namespace IF EXISTS;
DROP INDEX rtu_namespace IF EXISTS;
DROP INDEX correlation_namespace IF EXISTS;
DROP INDEX timeline_namespace IF EXISTS;
DROP INDEX dataflow_namespace IF EXISTS;
DROP INDEX alert_rule_namespace IF EXISTS;
DROP INDEX remediation_namespace IF EXISTS;

// Temporal query indexes (15 indexes)
DROP INDEX digital_twin_timestamp IF EXISTS;
DROP INDEX sensor_timestamp IF EXISTS;
DROP INDEX actuator_timestamp IF EXISTS;
DROP INDEX deviation_timestamp IF EXISTS;
DROP INDEX cascade_timestamp IF EXISTS;
DROP INDEX temporal_timestamp IF EXISTS;
DROP INDEX metric_timestamp IF EXISTS;
DROP INDEX timeseries_timestamp IF EXISTS;
DROP INDEX snapshot_timestamp IF EXISTS;
DROP INDEX disruption_start IF EXISTS;
DROP INDEX disruption_end IF EXISTS;
DROP INDEX temporal_retention IF EXISTS;
DROP INDEX versioned_valid_from IF EXISTS;
DROP INDEX versioned_valid_to IF EXISTS;
DROP INDEX versioned_type IF EXISTS;

// Asset relationship indexes (15 indexes)
DROP INDEX digital_twin_asset_id IF EXISTS;
DROP INDEX sensor_asset IF EXISTS;
DROP INDEX actuator_asset IF EXISTS;
DROP INDEX constraint_asset IF EXISTS;
DROP INDEX deviation_asset IF EXISTS;
DROP INDEX loop_asset IF EXISTS;
DROP INDEX safety_asset IF EXISTS;
DROP INDEX cascade_asset IF EXISTS;
DROP INDEX resilience_asset IF EXISTS;
DROP INDEX timeseries_asset IF EXISTS;
DROP INDEX metric_asset IF EXISTS;
DROP INDEX scada_source IF EXISTS;
DROP INDEX plc_asset IF EXISTS;
DROP INDEX rtu_asset IF EXISTS;
DROP INDEX versioned_node IF EXISTS;

// Severity/priority indexes (10 indexes)
DROP INDEX deviation_severity IF EXISTS;
DROP INDEX cascade_severity IF EXISTS;
DROP INDEX temporal_severity IF EXISTS;
DROP INDEX disruption_severity IF EXISTS;
DROP INDEX safety_sil_level IF EXISTS;
DROP INDEX temp_pattern_severity IF EXISTS;
DROP INDEX impact_severity IF EXISTS;
DROP INDEX dep_link_criticality IF EXISTS;
DROP INDEX cross_dep_criticality IF EXISTS;
DROP INDEX scada_severity IF EXISTS;

// Categorical indexes (15 indexes)
DROP INDEX sensor_type IF EXISTS;
DROP INDEX actuator_type IF EXISTS;
DROP INDEX temporal_event_type IF EXISTS;
DROP INDEX temporal_source IF EXISTS;
DROP INDEX scada_event_type IF EXISTS;
DROP INDEX dep_type IF EXISTS;
DROP INDEX dep_source IF EXISTS;
DROP INDEX dep_target IF EXISTS;
DROP INDEX cross_dep_primary IF EXISTS;
DROP INDEX cross_dep_dependent IF EXISTS;
DROP INDEX metric_type IF EXISTS;
DROP INDEX sla_service IF EXISTS;
DROP INDEX sla_customer IF EXISTS;
DROP INDEX revenue_asset_type IF EXISTS;
DROP INDEX timeseries_metric IF EXISTS;

// Composite indexes (8 indexes)
DROP INDEX sensor_asset_timestamp IF EXISTS;
DROP INDEX temporal_type_timestamp IF EXISTS;
DROP INDEX cascade_simulation_sequence IF EXISTS;
DROP INDEX interlock_source IF EXISTS;
DROP INDEX interlock_dependent IF EXISTS;
DROP INDEX impact_event IF EXISTS;
DROP INDEX customer_impact_event IF EXISTS;
DROP INDEX cascade_simulation IF EXISTS;

// Full-text search indexes (5 indexes)
DROP INDEX cascade_event_search IF EXISTS;
DROP INDEX disruption_search IF EXISTS;
DROP INDEX temporal_event_search IF EXISTS;
DROP INDEX sla_service_search IF EXISTS;
DROP INDEX safety_function_search IF EXISTS;

// ═══════════════════════════════════════════════════════════════════════
// SECTION 2: DROP CONSTRAINTS (35 constraints)
// ═══════════════════════════════════════════════════════════════════════

// UC2: Cyber-Physical Constraints
DROP CONSTRAINT digital_twin_state_id IF EXISTS;
DROP CONSTRAINT physical_sensor_id IF EXISTS;
DROP CONSTRAINT physical_actuator_id IF EXISTS;
DROP CONSTRAINT physics_constraint_id IF EXISTS;
DROP CONSTRAINT state_deviation_id IF EXISTS;
DROP CONSTRAINT process_loop_id IF EXISTS;
DROP CONSTRAINT safety_function_id IF EXISTS;
DROP CONSTRAINT safety_interlock_id IF EXISTS;

// UC3: Cascading Failure Constraints
DROP CONSTRAINT cascade_event_id IF EXISTS;
DROP CONSTRAINT dependency_link_id IF EXISTS;
DROP CONSTRAINT propagation_rule_id IF EXISTS;
DROP CONSTRAINT impact_assessment_id IF EXISTS;
DROP CONSTRAINT system_resilience_id IF EXISTS;
DROP CONSTRAINT cross_infra_dep_id IF EXISTS;

// R6: Temporal Reasoning Constraints
DROP CONSTRAINT temporal_event_id IF EXISTS;
DROP CONSTRAINT event_store_id IF EXISTS;
DROP CONSTRAINT temporal_pattern_id IF EXISTS;
DROP CONSTRAINT timeseries_analysis_id IF EXISTS;
DROP CONSTRAINT historical_snapshot_id IF EXISTS;
DROP CONSTRAINT versioned_node_id IF EXISTS;

// CG-9: Operational Impact Constraints
DROP CONSTRAINT operational_metric_id IF EXISTS;
DROP CONSTRAINT service_level_id IF EXISTS;
DROP CONSTRAINT customer_impact_id IF EXISTS;
DROP CONSTRAINT revenue_model_id IF EXISTS;
DROP CONSTRAINT disruption_event_id IF EXISTS;

// UC1: SCADA Attack Reconstruction Constraints
DROP CONSTRAINT scada_event_id IF EXISTS;
DROP CONSTRAINT hmi_session_id IF EXISTS;
DROP CONSTRAINT plc_state_change_id IF EXISTS;
DROP CONSTRAINT rtu_communication_id IF EXISTS;
DROP CONSTRAINT event_correlation_id IF EXISTS;
DROP CONSTRAINT attack_timeline_id IF EXISTS;

// Supporting Integration Constraints
DROP CONSTRAINT data_flow_id IF EXISTS;
DROP CONSTRAINT alert_rule_id IF EXISTS;
DROP CONSTRAINT remediation_plan_id IF EXISTS;

// ═══════════════════════════════════════════════════════════════════════
// SECTION 3: DELETE NODES (COMMENTED OUT FOR SAFETY)
// ═══════════════════════════════════════════════════════════════════════
// WARNING: Uncomment only if you want to DELETE ALL DATA for these node types
// This is IRREVERSIBLE and will remove all nodes and relationships
// ═══════════════════════════════════════════════════════════════════════

/*
// UC2: Cyber-Physical Nodes
MATCH (n:DigitalTwinState) DETACH DELETE n;
MATCH (n:PhysicalSensor) DETACH DELETE n;
MATCH (n:PhysicalActuator) DETACH DELETE n;
MATCH (n:PhysicsConstraint) DETACH DELETE n;
MATCH (n:StateDeviation) DETACH DELETE n;
MATCH (n:ProcessLoop) DETACH DELETE n;
MATCH (n:SafetyFunction) DETACH DELETE n;
MATCH (n:SafetyInterlock) DETACH DELETE n;

// UC3: Cascading Failure Nodes
MATCH (n:CascadeEvent) DETACH DELETE n;
MATCH (n:DependencyLink) DETACH DELETE n;
MATCH (n:PropagationRule) DETACH DELETE n;
MATCH (n:ImpactAssessment) DETACH DELETE n;
MATCH (n:SystemResilience) DETACH DELETE n;
MATCH (n:CrossInfrastructureDependency) DETACH DELETE n;

// R6: Temporal Reasoning Nodes
MATCH (n:TemporalEvent) DETACH DELETE n;
MATCH (n:EventStore) DETACH DELETE n;
MATCH (n:TemporalPattern) DETACH DELETE n;
MATCH (n:TimeSeriesAnalysis) DETACH DELETE n;
MATCH (n:HistoricalSnapshot) DETACH DELETE n;
MATCH (n:VersionedNode) DETACH DELETE n;

// CG-9: Operational Impact Nodes
MATCH (n:OperationalMetric) DETACH DELETE n;
MATCH (n:ServiceLevel) DETACH DELETE n;
MATCH (n:CustomerImpact) DETACH DELETE n;
MATCH (n:RevenueModel) DETACH DELETE n;
MATCH (n:DisruptionEvent) DETACH DELETE n;

// UC1: SCADA Attack Reconstruction Nodes
MATCH (n:SCADAEvent) DETACH DELETE n;
MATCH (n:HMISession) DETACH DELETE n;
MATCH (n:PLCStateChange) DETACH DELETE n;
MATCH (n:RTUCommunication) DETACH DELETE n;
MATCH (n:EventCorrelation) DETACH DELETE n;
MATCH (n:AttackTimeline) DETACH DELETE n;

// Supporting Integration Nodes
MATCH (n:DataFlow) DETACH DELETE n;
MATCH (n:AlertRule) DETACH DELETE n;
MATCH (n:RemediationPlan) DETACH DELETE n;
*/

// ═══════════════════════════════════════════════════════════════════════
// ROLLBACK VERIFICATION
// ═══════════════════════════════════════════════════════════════════════

// Verify all constraints removed
SHOW CONSTRAINTS
YIELD name
WHERE name STARTS WITH 'digital_twin'
   OR name STARTS WITH 'physical'
   OR name STARTS WITH 'physics'
   OR name STARTS WITH 'state_deviation'
   OR name STARTS WITH 'process_loop'
   OR name STARTS WITH 'safety'
   OR name STARTS WITH 'cascade'
   OR name STARTS WITH 'dependency'
   OR name STARTS WITH 'propagation'
   OR name STARTS WITH 'impact'
   OR name STARTS WITH 'system_resilience'
   OR name STARTS WITH 'cross_infra'
   OR name STARTS WITH 'temporal'
   OR name STARTS WITH 'event_store'
   OR name STARTS WITH 'timeseries'
   OR name STARTS WITH 'historical'
   OR name STARTS WITH 'versioned'
   OR name STARTS WITH 'operational'
   OR name STARTS WITH 'service_level'
   OR name STARTS WITH 'customer_impact'
   OR name STARTS WITH 'revenue'
   OR name STARTS WITH 'disruption'
   OR name STARTS WITH 'scada'
   OR name STARTS WITH 'hmi'
   OR name STARTS WITH 'plc'
   OR name STARTS WITH 'rtu'
   OR name STARTS WITH 'event_correlation'
   OR name STARTS WITH 'attack_timeline'
   OR name STARTS WITH 'data_flow'
   OR name STARTS WITH 'alert_rule'
   OR name STARTS WITH 'remediation'
RETURN count(*) AS remaining_constraints;

// Verify all indexes removed
SHOW INDEXES
YIELD name
WHERE name STARTS WITH 'digital_twin'
   OR name STARTS WITH 'sensor'
   OR name STARTS WITH 'actuator'
   OR name STARTS WITH 'constraint'
   OR name STARTS WITH 'deviation'
   OR name STARTS WITH 'loop'
   OR name STARTS WITH 'safety'
   OR name STARTS WITH 'interlock'
   OR name STARTS WITH 'cascade'
   OR name STARTS WITH 'dep'
   OR name STARTS WITH 'prop'
   OR name STARTS WITH 'impact'
   OR name STARTS WITH 'resilience'
   OR name STARTS WITH 'cross'
   OR name STARTS WITH 'temporal'
   OR name STARTS WITH 'event_store'
   OR name STARTS WITH 'temp_pattern'
   OR name STARTS WITH 'timeseries'
   OR name STARTS WITH 'snapshot'
   OR name STARTS WITH 'versioned'
   OR name STARTS WITH 'metric'
   OR name STARTS WITH 'sla'
   OR name STARTS WITH 'customer_impact'
   OR name STARTS WITH 'revenue'
   OR name STARTS WITH 'disruption'
   OR name STARTS WITH 'scada'
   OR name STARTS WITH 'hmi'
   OR name STARTS WITH 'plc'
   OR name STARTS WITH 'rtu'
   OR name STARTS WITH 'correlation'
   OR name STARTS WITH 'timeline'
   OR name STARTS WITH 'dataflow'
   OR name STARTS WITH 'alert'
   OR name STARTS WITH 'remediation'
RETURN count(*) AS remaining_indexes;

// ═══════════════════════════════════════════════════════════════════════
// ROLLBACK COMPLETE
// Expected Results: remaining_constraints = 0, remaining_indexes = 0
// If counts > 0, some constraints/indexes were not removed
// ═══════════════════════════════════════════════════════════════════════
