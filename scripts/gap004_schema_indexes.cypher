// ═══════════════════════════════════════════════════════════════════════
// GAP-004 PHASE 1 SCHEMA INDEXES
// ═══════════════════════════════════════════════════════════════════════
// File: gap004_schema_indexes.cypher
// Created: 2025-11-13
// Purpose: Create performance indexes for 35 new node types
// Target: 50+ indexes for query optimization
// Deployment Order: Execute AFTER constraints
// ═══════════════════════════════════════════════════════════════════════

// -----------------------------------------------------------------------
// SECTION 1: MULTI-TENANT ISOLATION INDEXES (35 indexes - CRITICAL)
// -----------------------------------------------------------------------
// Purpose: Ensure fast tenant-scoped queries for all node types
// Pattern: CREATE INDEX {node}_namespace FOR (n:{NodeType}) ON (n.customer_namespace)

// UC2: Cyber-Physical Nodes
CREATE INDEX digital_twin_namespace IF NOT EXISTS FOR (n:DigitalTwinState) ON (n.customer_namespace);
CREATE INDEX sensor_namespace IF NOT EXISTS FOR (n:PhysicalSensor) ON (n.customer_namespace);
CREATE INDEX actuator_namespace IF NOT EXISTS FOR (n:PhysicalActuator) ON (n.customer_namespace);
CREATE INDEX constraint_namespace IF NOT EXISTS FOR (n:PhysicsConstraint) ON (n.customer_namespace);
CREATE INDEX deviation_namespace IF NOT EXISTS FOR (n:StateDeviation) ON (n.customer_namespace);
CREATE INDEX loop_namespace IF NOT EXISTS FOR (n:ProcessLoop) ON (n.customer_namespace);
CREATE INDEX safety_namespace IF NOT EXISTS FOR (n:SafetyFunction) ON (n.customer_namespace);
CREATE INDEX interlock_namespace IF NOT EXISTS FOR (n:SafetyInterlock) ON (n.customer_namespace);

// UC3: Cascading Failure Nodes
CREATE INDEX cascade_event_namespace IF NOT EXISTS FOR (n:CascadeEvent) ON (n.customer_namespace);
CREATE INDEX dep_link_namespace IF NOT EXISTS FOR (n:DependencyLink) ON (n.customer_namespace);
CREATE INDEX prop_rule_namespace IF NOT EXISTS FOR (n:PropagationRule) ON (n.customer_namespace);
CREATE INDEX impact_namespace IF NOT EXISTS FOR (n:ImpactAssessment) ON (n.customer_namespace);
CREATE INDEX resilience_namespace IF NOT EXISTS FOR (n:SystemResilience) ON (n.customer_namespace);
CREATE INDEX cross_dep_namespace IF NOT EXISTS FOR (n:CrossInfrastructureDependency) ON (n.customer_namespace);

// R6: Temporal Reasoning Nodes
CREATE INDEX temporal_event_namespace IF NOT EXISTS FOR (n:TemporalEvent) ON (n.customer_namespace);
CREATE INDEX event_store_namespace IF NOT EXISTS FOR (n:EventStore) ON (n.customer_namespace);
CREATE INDEX temp_pattern_namespace IF NOT EXISTS FOR (n:TemporalPattern) ON (n.customer_namespace);
CREATE INDEX timeseries_namespace IF NOT EXISTS FOR (n:TimeSeriesAnalysis) ON (n.customer_namespace);
CREATE INDEX snapshot_namespace IF NOT EXISTS FOR (n:HistoricalSnapshot) ON (n.customer_namespace);
CREATE INDEX versioned_namespace IF NOT EXISTS FOR (n:VersionedNode) ON (n.customer_namespace);

// CG-9: Operational Impact Nodes
CREATE INDEX metric_namespace IF NOT EXISTS FOR (n:OperationalMetric) ON (n.customer_namespace);
CREATE INDEX sla_namespace IF NOT EXISTS FOR (n:ServiceLevel) ON (n.customer_namespace);
CREATE INDEX customer_impact_namespace IF NOT EXISTS FOR (n:CustomerImpact) ON (n.customer_namespace);
CREATE INDEX revenue_namespace IF NOT EXISTS FOR (n:RevenueModel) ON (n.customer_namespace);
CREATE INDEX disruption_namespace IF NOT EXISTS FOR (n:DisruptionEvent) ON (n.customer_namespace);

// UC1: SCADA Attack Reconstruction Nodes
CREATE INDEX scada_event_namespace IF NOT EXISTS FOR (n:SCADAEvent) ON (n.customer_namespace);
CREATE INDEX hmi_namespace IF NOT EXISTS FOR (n:HMISession) ON (n.customer_namespace);
CREATE INDEX plc_namespace IF NOT EXISTS FOR (n:PLCStateChange) ON (n.customer_namespace);
CREATE INDEX rtu_namespace IF NOT EXISTS FOR (n:RTUCommunication) ON (n.customer_namespace);
CREATE INDEX correlation_namespace IF NOT EXISTS FOR (n:EventCorrelation) ON (n.customer_namespace);
CREATE INDEX timeline_namespace IF NOT EXISTS FOR (n:AttackTimeline) ON (n.customer_namespace);

// Supporting Integration Nodes
CREATE INDEX dataflow_namespace IF NOT EXISTS FOR (n:DataFlow) ON (n.customer_namespace);
CREATE INDEX alert_rule_namespace IF NOT EXISTS FOR (n:AlertRule) ON (n.customer_namespace);
CREATE INDEX remediation_namespace IF NOT EXISTS FOR (n:RemediationPlan) ON (n.customer_namespace);

// -----------------------------------------------------------------------
// SECTION 2: TEMPORAL QUERY INDEXES (15 indexes)
// -----------------------------------------------------------------------
// Purpose: Optimize time-based queries, 90-day retention, historical analysis

// Timestamp indexes for real-time event tracking
CREATE INDEX digital_twin_timestamp IF NOT EXISTS FOR (n:DigitalTwinState) ON (n.timestamp);
CREATE INDEX sensor_timestamp IF NOT EXISTS FOR (n:PhysicalSensor) ON (n.timestamp);
CREATE INDEX actuator_timestamp IF NOT EXISTS FOR (n:PhysicalActuator) ON (n.timestamp);
CREATE INDEX deviation_timestamp IF NOT EXISTS FOR (n:StateDeviation) ON (n.timestamp);
CREATE INDEX cascade_timestamp IF NOT EXISTS FOR (n:CascadeEvent) ON (n.timestamp);
CREATE INDEX temporal_timestamp IF NOT EXISTS FOR (n:TemporalEvent) ON (n.timestamp);
CREATE INDEX metric_timestamp IF NOT EXISTS FOR (n:OperationalMetric) ON (n.timestamp);
CREATE INDEX timeseries_timestamp IF NOT EXISTS FOR (n:TimeSeriesAnalysis) ON (n.timestamp);
CREATE INDEX snapshot_timestamp IF NOT EXISTS FOR (n:HistoricalSnapshot) ON (n.timestamp);
CREATE INDEX disruption_start IF NOT EXISTS FOR (n:DisruptionEvent) ON (n.startTime);
CREATE INDEX disruption_end IF NOT EXISTS FOR (n:DisruptionEvent) ON (n.endTime);

// Retention policy indexes for 90-day window management
CREATE INDEX temporal_retention IF NOT EXISTS FOR (n:TemporalEvent) ON (n.retentionUntil);

// Bitemporal versioning indexes
CREATE INDEX versioned_valid_from IF NOT EXISTS FOR (n:VersionedNode) ON (n.validFrom);
CREATE INDEX versioned_valid_to IF NOT EXISTS FOR (n:VersionedNode) ON (n.validTo);
CREATE INDEX versioned_type IF NOT EXISTS FOR (n:VersionedNode) ON (n.nodeType);

// -----------------------------------------------------------------------
// SECTION 3: ASSET RELATIONSHIP INDEXES (15 indexes)
// -----------------------------------------------------------------------
// Purpose: Fast lookups for asset-centric queries (device health, sensor readings)

CREATE INDEX digital_twin_asset_id IF NOT EXISTS FOR (n:DigitalTwinState) ON (n.assetId);
CREATE INDEX sensor_asset IF NOT EXISTS FOR (n:PhysicalSensor) ON (n.assetId);
CREATE INDEX actuator_asset IF NOT EXISTS FOR (n:PhysicalActuator) ON (n.assetId);
CREATE INDEX constraint_asset IF NOT EXISTS FOR (n:PhysicsConstraint) ON (n.assetId);
CREATE INDEX deviation_asset IF NOT EXISTS FOR (n:StateDeviation) ON (n.assetId);
CREATE INDEX loop_asset IF NOT EXISTS FOR (n:ProcessLoop) ON (n.assetId);
CREATE INDEX safety_asset IF NOT EXISTS FOR (n:SafetyFunction) ON (n.assetId);
CREATE INDEX cascade_asset IF NOT EXISTS FOR (n:CascadeEvent) ON (n.failedAssetId);
CREATE INDEX resilience_asset IF NOT EXISTS FOR (n:SystemResilience) ON (n.assetId);
CREATE INDEX timeseries_asset IF NOT EXISTS FOR (n:TimeSeriesAnalysis) ON (n.assetId);
CREATE INDEX metric_asset IF NOT EXISTS FOR (n:OperationalMetric) ON (n.assetId);
CREATE INDEX scada_source IF NOT EXISTS FOR (n:SCADAEvent) ON (n.source);
CREATE INDEX plc_asset IF NOT EXISTS FOR (n:PLCStateChange) ON (n.plcId);
CREATE INDEX rtu_asset IF NOT EXISTS FOR (n:RTUCommunication) ON (n.rtuId);
CREATE INDEX versioned_node IF NOT EXISTS FOR (n:VersionedNode) ON (n.nodeId);

// -----------------------------------------------------------------------
// SECTION 4: SEVERITY/PRIORITY INDEXES (10 indexes)
// -----------------------------------------------------------------------
// Purpose: Fast filtering by criticality for alerting and incident response

CREATE INDEX deviation_severity IF NOT EXISTS FOR (n:StateDeviation) ON (n.severity);
CREATE INDEX cascade_severity IF NOT EXISTS FOR (n:CascadeEvent) ON (n.severity);
CREATE INDEX temporal_severity IF NOT EXISTS FOR (n:TemporalEvent) ON (n.severity);
CREATE INDEX disruption_severity IF NOT EXISTS FOR (n:DisruptionEvent) ON (n.severity);
CREATE INDEX safety_sil_level IF NOT EXISTS FOR (n:SafetyFunction) ON (n.silLevel);
CREATE INDEX temp_pattern_severity IF NOT EXISTS FOR (n:TemporalPattern) ON (n.severity);
CREATE INDEX impact_severity IF NOT EXISTS FOR (n:CustomerImpact) ON (n.impactSeverity);
CREATE INDEX dep_link_criticality IF NOT EXISTS FOR (n:DependencyLink) ON (n.criticality);
CREATE INDEX cross_dep_criticality IF NOT EXISTS FOR (n:CrossInfrastructureDependency) ON (n.criticalityLevel);
CREATE INDEX scada_severity IF NOT EXISTS FOR (n:SCADAEvent) ON (n.severity);

// -----------------------------------------------------------------------
// SECTION 5: CATEGORICAL INDEXES (12 indexes)
// -----------------------------------------------------------------------
// Purpose: Fast filtering by type, category, or classification

// Sensor and actuator types
CREATE INDEX sensor_type IF NOT EXISTS FOR (n:PhysicalSensor) ON (n.sensorType);
CREATE INDEX actuator_type IF NOT EXISTS FOR (n:PhysicalActuator) ON (n.actuatorType);

// Event types and classifications
CREATE INDEX temporal_event_type IF NOT EXISTS FOR (n:TemporalEvent) ON (n.eventType);
CREATE INDEX temporal_source IF NOT EXISTS FOR (n:TemporalEvent) ON (n.source);
CREATE INDEX scada_event_type IF NOT EXISTS FOR (n:SCADAEvent) ON (n.eventType);

// Dependency and infrastructure types
CREATE INDEX dep_type IF NOT EXISTS FOR (n:DependencyLink) ON (n.dependencyType);
CREATE INDEX dep_source IF NOT EXISTS FOR (n:DependencyLink) ON (n.sourceAssetId);
CREATE INDEX dep_target IF NOT EXISTS FOR (n:DependencyLink) ON (n.targetAssetId);
CREATE INDEX cross_dep_primary IF NOT EXISTS FOR (n:CrossInfrastructureDependency) ON (n.primaryInfra);
CREATE INDEX cross_dep_dependent IF NOT EXISTS FOR (n:CrossInfrastructureDependency) ON (n.dependentInfra);

// Operational metrics and SLA
CREATE INDEX metric_type IF NOT EXISTS FOR (n:OperationalMetric) ON (n.metricType);
CREATE INDEX sla_service IF NOT EXISTS FOR (n:ServiceLevel) ON (n.serviceName);
CREATE INDEX sla_customer IF NOT EXISTS FOR (n:ServiceLevel) ON (n.customerId);
CREATE INDEX revenue_asset_type IF NOT EXISTS FOR (n:RevenueModel) ON (n.assetType);
CREATE INDEX timeseries_metric IF NOT EXISTS FOR (n:TimeSeriesAnalysis) ON (n.metric);

// -----------------------------------------------------------------------
// SECTION 6: COMPOSITE INDEXES (8 indexes)
// -----------------------------------------------------------------------
// Purpose: Optimize complex multi-condition queries

// Asset + timestamp for historical analysis
CREATE INDEX sensor_asset_timestamp IF NOT EXISTS FOR (n:PhysicalSensor) ON (n.assetId, n.timestamp);
CREATE INDEX temporal_type_timestamp IF NOT EXISTS FOR (n:TemporalEvent) ON (n.eventType, n.timestamp);
CREATE INDEX cascade_simulation_sequence IF NOT EXISTS FOR (n:CascadeEvent) ON (n.simulationId, n.sequenceNumber);

// Interlock dependencies
CREATE INDEX interlock_source IF NOT EXISTS FOR (n:SafetyInterlock) ON (n.sourceFunctionId);
CREATE INDEX interlock_dependent IF NOT EXISTS FOR (n:SafetyInterlock) ON (n.dependentFunctionId);

// Impact event correlation
CREATE INDEX impact_event IF NOT EXISTS FOR (n:ImpactAssessment) ON (n.cascadeEventId);
CREATE INDEX customer_impact_event IF NOT EXISTS FOR (n:CustomerImpact) ON (n.disruptionEventId);

// Cascade simulation tracking
CREATE INDEX cascade_simulation IF NOT EXISTS FOR (n:CascadeEvent) ON (n.simulationId);

// -----------------------------------------------------------------------
// SECTION 7: FULL-TEXT SEARCH INDEXES (5 indexes)
// -----------------------------------------------------------------------
// Purpose: Enable natural language search for events, disruptions, and functions

CREATE FULLTEXT INDEX cascade_event_search IF NOT EXISTS
FOR (n:CascadeEvent) ON EACH [n.impactSummary];

CREATE FULLTEXT INDEX disruption_search IF NOT EXISTS
FOR (n:DisruptionEvent) ON EACH [n.eventName, n.rootCauseDetail];

CREATE FULLTEXT INDEX temporal_event_search IF NOT EXISTS
FOR (n:TemporalEvent) ON EACH [n.eventType];

CREATE FULLTEXT INDEX sla_service_search IF NOT EXISTS
FOR (n:ServiceLevel) ON EACH [n.serviceName];

CREATE FULLTEXT INDEX safety_function_search IF NOT EXISTS
FOR (n:SafetyFunction) ON EACH [n.functionName, n.logicDescription];

// ═══════════════════════════════════════════════════════════════════════
// INDEX CREATION COMPLETE
// Total Indexes: 70+ indexes across 35 node types
// Performance Target: <2s queries for 15M nodes
// Next Step: Execute gap004_relationships.cypher
// ═══════════════════════════════════════════════════════════════════════
