// GAP-004 Performance Benchmark Suite
// Target: <2s for 8-15 hop queries
// Date: 2025-11-13

// ============================================================================
// SIMPLE QUERIES (<100ms target)
// ============================================================================

// BENCHMARK 1: Find all DigitalTwinState nodes for a customer namespace
// Expected: <50ms
:param namespace => 'customer_001';
MATCH (dts:DigitalTwinState {customer_namespace: $namespace})
RETURN count(dts) as digital_twin_count,
       avg(dts.confidence_score) as avg_confidence;

// BENCHMARK 2: Find all TemporalEvent nodes in last 24 hours
// Expected: <100ms
:param cutoff_time => datetime() - duration('P1D');
MATCH (te:TemporalEvent)
WHERE te.event_timestamp > $cutoff_time
RETURN count(te) as recent_events,
       collect(DISTINCT te.event_type)[0..5] as event_types;

// BENCHMARK 3: Count OperationalMetric threshold breaches
// Expected: <50ms
MATCH (om:OperationalMetric)
WHERE om.metric_value > om.threshold_value
RETURN count(om) as breach_count,
       avg(om.metric_value - om.threshold_value) as avg_breach_magnitude;

// ============================================================================
// COMPLEX TRAVERSALS (<2s target for 8-15 hops)
// ============================================================================

// BENCHMARK 4: UC2 - Cyber-physical attack chain (8 hops)
// Path: sensor → dt → actuator → constraint → safety
// Expected: <2s
:param sensor_id => 'sensor_temp_001';
MATCH path = (s:DigitalTwinState {twin_id: $sensor_id})
  -[:OBSERVES_STATE]->(:PhysicalEntity)
  -[:HAS_DIGITAL_TWIN]->(dt:DigitalTwinState)
  -[:CONTROLS_ACTUATOR]->(:PhysicalEntity)
  -[:GOVERNED_BY]->(:SafetyConstraint)
  -[:TRIGGERS_ANOMALY]->(a:AnomalyDetection)
  -[:LEADS_TO_INCIDENT]->(i:SecurityIncident)
  -[:CAUSES_IMPACT]->(ci:CustomerImpact)
WHERE a.anomaly_severity = 'critical'
  AND i.incident_status = 'active'
RETURN length(path) as hop_count,
       collect(labels(nodes(path)[-1])) as final_node_labels,
       ci.total_revenue_impact_usd as financial_impact
LIMIT 10;

// BENCHMARK 5: UC3 - Cascading failure propagation (10+ hops)
// Path: event → cascade → cascade → cascade...
// Expected: <2s
:param initial_event_id => 'event_cascade_001';
MATCH path = (te:TemporalEvent {event_id: $initial_event_id})
  -[:TRIGGERS_CASCADE*1..10]->(cascade:TemporalEvent)
  -[:CAUSES_FAILURE]->(failure:SystemFailure)
  -[:IMPACTS_SERVICE]->(service:ServiceInstance)
  -[:DEGRADES_PERFORMANCE]->(om:OperationalMetric)
WHERE cascade.event_type = 'cascade'
  AND failure.failure_severity IN ['high', 'critical']
RETURN length(path) as cascade_depth,
       count(DISTINCT cascade) as cascade_events,
       collect(DISTINCT service.service_id)[0..5] as affected_services,
       avg(om.metric_value) as avg_degradation
LIMIT 5;

// BENCHMARK 6: R6 - Temporal correlation across 10 events (12 hops)
// Path: event → correlation → correlation → correlation...
// Expected: <2s
:param correlation_window => duration('PT5M');
MATCH (te1:TemporalEvent)
WHERE te1.event_timestamp > datetime() - duration('PT1H')
WITH te1
MATCH path = (te1)
  -[:TEMPORALLY_CORRELATED_WITH*1..10]->(te2:TemporalEvent)
WHERE te2.event_timestamp - te1.event_timestamp < $correlation_window
  AND te1.customer_namespace = te2.customer_namespace
WITH path, te1, te2
MATCH (te2)-[:CONTRIBUTES_TO]->(a:AnomalyDetection)
  -[:LEADS_TO_INCIDENT]->(i:SecurityIncident)
RETURN length(path) as correlation_chain_length,
       te1.event_id as root_event,
       count(DISTINCT te2) as correlated_events,
       i.incident_severity as incident_severity
ORDER BY correlation_chain_length DESC
LIMIT 10;

// BENCHMARK 7: CG-9 - Operational impact aggregation (15 hops)
// Path: metric → service → revenue → customer
// Expected: <2s
:param customer_ns => 'customer_002';
MATCH path = (om:OperationalMetric {customer_namespace: $customer_ns})
  -[:MONITORS_PERFORMANCE]->(si:ServiceInstance)
  -[:RUNS_ON]->(pe:PhysicalEntity)
  -[:HAS_DIGITAL_TWIN]->(dt:DigitalTwinState)
  -[:OBSERVES_STATE]->(pe2:PhysicalEntity)
  -[:GOVERNED_BY]->(sc:SafetyConstraint)
  -[:ENFORCES_COMPLIANCE]->(cp:CompliancePolicy)
  -[:REQUIRES_VALIDATION]->(gp:GovernancePolicy)
  -[:APPLIES_TO_CUSTOMER]->(ci:CustomerImpact)
WHERE om.metric_value < om.threshold_value
  AND si.service_status = 'degraded'
  AND dt.confidence_score < 0.8
RETURN length(path) as total_hops,
       count(DISTINCT si) as degraded_services,
       sum(ci.total_revenue_impact_usd) as total_revenue_impact,
       avg(om.metric_value / om.threshold_value) as avg_performance_ratio,
       collect(DISTINCT sc.constraint_type)[0..3] as violated_constraints
LIMIT 10;

// BENCHMARK 8: Cross-namespace cascading failure detection (14 hops)
// Path: multi-tenant cascade across namespaces
// Expected: <2s
MATCH path = (te:TemporalEvent)
  -[:TRIGGERS_CASCADE]->(c1:TemporalEvent)
  -[:CROSSES_NAMESPACE]->(c2:TemporalEvent)
  -[:CAUSES_FAILURE]->(sf:SystemFailure)
  -[:IMPACTS_SERVICE]->(si:ServiceInstance)
  -[:DEPENDS_ON*1..5]->(dep_si:ServiceInstance)
  -[:DEGRADES_PERFORMANCE]->(om:OperationalMetric)
  -[:TRIGGERS_ANOMALY]->(a:AnomalyDetection)
  -[:LEADS_TO_INCIDENT]->(i:SecurityIncident)
WHERE te.customer_namespace <> c2.customer_namespace
  AND sf.failure_severity = 'critical'
  AND i.incident_status = 'active'
RETURN length(path) as hop_count,
       te.customer_namespace as origin_namespace,
       c2.customer_namespace as impacted_namespace,
       count(DISTINCT dep_si) as cascade_service_count,
       i.incident_id as security_incident
ORDER BY hop_count DESC
LIMIT 5;

// ============================================================================
// AGGREGATION QUERIES (<500ms target)
// ============================================================================

// BENCHMARK 9: Sum total financial impact across all CustomerImpact nodes
// Expected: <300ms
MATCH (ci:CustomerImpact)
RETURN count(ci) as total_customers_impacted,
       sum(ci.total_revenue_impact_usd) as total_revenue_loss,
       avg(ci.total_revenue_impact_usd) as avg_impact_per_customer,
       max(ci.total_revenue_impact_usd) as max_single_customer_impact;

// BENCHMARK 10: Average operational metrics by customer namespace
// Expected: <500ms
MATCH (om:OperationalMetric)
WHERE om.customer_namespace IS NOT NULL
WITH om.customer_namespace as namespace,
     avg(om.metric_value) as avg_value,
     avg(om.threshold_value) as avg_threshold,
     count(om) as metric_count
RETURN namespace,
       avg_value,
       avg_threshold,
       metric_count,
       CASE WHEN avg_value < avg_threshold THEN 'HEALTHY' ELSE 'DEGRADED' END as health_status
ORDER BY namespace
LIMIT 20;
