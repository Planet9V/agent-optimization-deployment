// GAP-004 Performance Optimization Indexes
// Generated: 2025-11-13
// Purpose: Improve query performance from benchmark analysis
// Expected improvement: 10-30x for simple queries and aggregations

// ============================================================================
// CRITICAL INDEXES (from benchmark analysis)
// ============================================================================

// Index 1: DigitalTwinState by customer namespace
// Benefit: 30x speedup for benchmark_1 (1508ms → ~50ms)
CREATE INDEX digital_twin_state_namespace IF NOT EXISTS
FOR (dts:DigitalTwinState)
ON (dts.customer_namespace);

// Index 2: TemporalEvent by timestamp
// Benefit: 15x speedup for benchmark_2 (1580ms → ~100ms)
CREATE INDEX temporal_event_timestamp IF NOT EXISTS
FOR (te:TemporalEvent)
ON (te.event_timestamp);

// Index 3: OperationalMetric composite for breach detection
// Benefit: 30x speedup for benchmark_3 (1527ms → ~50ms)
CREATE INDEX operational_metric_breach IF NOT EXISTS
FOR (om:OperationalMetric)
ON (om.metric_value, om.threshold_value);

// Index 4: OperationalMetric by customer namespace
// Benefit: 3x speedup for benchmark_10 (1622ms → ~500ms)
CREATE INDEX operational_metric_namespace IF NOT EXISTS
FOR (om:OperationalMetric)
ON (om.customer_namespace);

// Index 5: CustomerImpact for financial aggregations
// Benefit: 5x speedup for benchmark_9 (1582ms → ~300ms)
CREATE INDEX customer_impact_revenue IF NOT EXISTS
FOR (ci:CustomerImpact)
ON (ci.total_revenue_impact_usd);

// ============================================================================
// ADDITIONAL PERFORMANCE INDEXES (recommended)
// ============================================================================

// Index 6: AnomalyDetection by severity (for UC2 queries)
CREATE INDEX anomaly_detection_severity IF NOT EXISTS
FOR (a:AnomalyDetection)
ON (a.anomaly_severity);

// Index 7: SecurityIncident by status (for UC2 queries)
CREATE INDEX security_incident_status IF NOT EXISTS
FOR (si:SecurityIncident)
ON (si.incident_status);

// Index 8: SystemFailure by severity (for cascade queries)
CREATE INDEX system_failure_severity IF NOT EXISTS
FOR (sf:SystemFailure)
ON (sf.failure_severity);

// Index 9: TemporalEvent by type (for cascade detection)
CREATE INDEX temporal_event_type IF NOT EXISTS
FOR (te:TemporalEvent)
ON (te.event_type);

// Index 10: ServiceInstance by status (for impact queries)
CREATE INDEX service_instance_status IF NOT EXISTS
FOR (si:ServiceInstance)
ON (si.service_status);

// Index 11: DigitalTwinState composite for confidence filtering
CREATE INDEX digital_twin_state_confidence IF NOT EXISTS
FOR (dt:DigitalTwinState)
ON (dt.customer_namespace, dt.confidence_score);

// ============================================================================
// VERIFICATION QUERIES
// ============================================================================

// After creating indexes, verify they exist:
// SHOW INDEXES;

// Analyze index usage in query plans:
// EXPLAIN <your_query_here>;

// Monitor index performance:
// CALL db.indexes();

// ============================================================================
// EXECUTION INSTRUCTIONS
// ============================================================================

// Run this script with:
// docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" < CREATE_PERFORMANCE_INDEXES.cypher

// Or execute interactively:
// docker exec -it openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg"
// Then paste the CREATE INDEX commands one by one

// Wait for index creation to complete (can take several minutes for large datasets)
// Check status with: CALL db.indexes() YIELD name, state, populationPercent;

// ============================================================================
// EXPECTED RESULTS AFTER INDEXING
// ============================================================================

// Simple Queries:
//   Benchmark 1: 1508ms → ~50ms (30x improvement)
//   Benchmark 2: 1580ms → ~100ms (15x improvement)
//   Benchmark 3: 1527ms → ~50ms (30x improvement)

// Complex Traversals:
//   Already optimal (all under 2000ms target)
//   Minor improvements expected (5-10%)

// Aggregations:
//   Benchmark 9: 1582ms → ~300ms (5x improvement)
//   Benchmark 10: 1622ms → ~500ms (3x improvement)

// Overall Impact:
//   Total performance improvement: 10-30x for most queries
//   Complex traversals remain excellent (<2s for 8-15 hops)
//   Production-ready performance across all query types
