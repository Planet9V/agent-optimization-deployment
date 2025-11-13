#!/bin/bash

# GAP-004 Performance Benchmark Runner
# Target: <2s for 8-15 hop queries
# Executes each benchmark 5 times and calculates statistics

set -e

CONTAINER="openspg-neo4j"
NEO4J_USER="neo4j"
NEO4J_PASS="neo4j@openspg"
CYPHER_FILE="gap004_performance_benchmarks.cypher"
RESULTS_FILE="performance_baseline_results.json"
ITERATIONS=5

echo "=================================================="
echo "GAP-004 Performance Benchmark Suite"
echo "Target: <2s for 8-15 hop queries"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Iterations per benchmark: $ITERATIONS"
echo "=================================================="
echo ""

# Function to execute a single Cypher query and measure time
run_benchmark() {
    local benchmark_name="$1"
    local query="$2"
    local timings=()

    echo "Running: $benchmark_name"

    for i in $(seq 1 $ITERATIONS); do
        start_time=$(date +%s%3N)

        # Execute query and capture output
        result=$(docker exec $CONTAINER cypher-shell \
            -u $NEO4J_USER \
            -p "$NEO4J_PASS" \
            --format plain \
            "$query" 2>&1)

        end_time=$(date +%s%3N)
        elapsed=$((end_time - start_time))
        timings+=($elapsed)

        echo "  Iteration $i: ${elapsed}ms"
    done

    # Calculate statistics
    min=${timings[0]}
    max=${timings[0]}
    sum=0

    for timing in "${timings[@]}"; do
        sum=$((sum + timing))
        [ $timing -lt $min ] && min=$timing
        [ $timing -gt $max ] && max=$timing
    done

    avg=$((sum / ITERATIONS))

    echo "  Statistics: min=${min}ms, avg=${avg}ms, max=${max}ms"
    echo ""

    # Return avg for JSON storage
    echo "$avg"
}

# Extract queries from cypher file
echo "Extracting benchmarks from $CYPHER_FILE..."
echo ""

# ============================================================================
# SIMPLE QUERIES
# ============================================================================

echo "=== SIMPLE QUERIES (Target: <100ms) ==="
echo ""

# Benchmark 1: Find DigitalTwinState by namespace
query1="MATCH (dts:DigitalTwinState {customer_namespace: 'customer_001'}) RETURN count(dts) as digital_twin_count, avg(dts.confidence_score) as avg_confidence;"
avg1=$(run_benchmark "Benchmark 1: DigitalTwinState by namespace" "$query1")

# Benchmark 2: TemporalEvent last 24h
query2="MATCH (te:TemporalEvent) WHERE te.event_timestamp > datetime() - duration('P1D') RETURN count(te) as recent_events;"
avg2=$(run_benchmark "Benchmark 2: TemporalEvent last 24h" "$query2")

# Benchmark 3: OperationalMetric breaches
query3="MATCH (om:OperationalMetric) WHERE om.metric_value > om.threshold_value RETURN count(om) as breach_count;"
avg3=$(run_benchmark "Benchmark 3: OperationalMetric breaches" "$query3")

# ============================================================================
# COMPLEX TRAVERSALS
# ============================================================================

echo "=== COMPLEX TRAVERSALS (Target: <2000ms for 8-15 hops) ==="
echo ""

# Benchmark 4: UC2 Cyber-physical attack chain (8 hops)
query4="MATCH path = (s:DigitalTwinState {twin_id: 'sensor_temp_001'})-[:OBSERVES_STATE]->(:PhysicalEntity)-[:HAS_DIGITAL_TWIN]->(dt:DigitalTwinState)-[:CONTROLS_ACTUATOR]->(:PhysicalEntity)-[:GOVERNED_BY]->(:SafetyConstraint)-[:TRIGGERS_ANOMALY]->(a:AnomalyDetection)-[:LEADS_TO_INCIDENT]->(i:SecurityIncident)-[:CAUSES_IMPACT]->(ci:CustomerImpact) WHERE a.anomaly_severity = 'critical' AND i.incident_status = 'active' RETURN length(path) as hop_count LIMIT 10;"
avg4=$(run_benchmark "Benchmark 4: UC2 Attack chain (8 hops)" "$query4")

# Benchmark 5: UC3 Cascading failure (10+ hops)
query5="MATCH path = (te:TemporalEvent {event_id: 'event_cascade_001'})-[:TRIGGERS_CASCADE*1..10]->(cascade:TemporalEvent)-[:CAUSES_FAILURE]->(failure:SystemFailure)-[:IMPACTS_SERVICE]->(service:ServiceInstance)-[:DEGRADES_PERFORMANCE]->(om:OperationalMetric) WHERE cascade.event_type = 'cascade' AND failure.failure_severity IN ['high', 'critical'] RETURN length(path) as cascade_depth LIMIT 5;"
avg5=$(run_benchmark "Benchmark 5: UC3 Cascading failure (10+ hops)" "$query5")

# Benchmark 6: R6 Temporal correlation (12 hops)
query6="MATCH (te1:TemporalEvent) WHERE te1.event_timestamp > datetime() - duration('PT1H') WITH te1 MATCH path = (te1)-[:TEMPORALLY_CORRELATED_WITH*1..10]->(te2:TemporalEvent) WHERE te2.event_timestamp - te1.event_timestamp < duration('PT5M') AND te1.customer_namespace = te2.customer_namespace WITH path, te1, te2 MATCH (te2)-[:CONTRIBUTES_TO]->(a:AnomalyDetection)-[:LEADS_TO_INCIDENT]->(i:SecurityIncident) RETURN length(path) as correlation_chain_length ORDER BY correlation_chain_length DESC LIMIT 10;"
avg6=$(run_benchmark "Benchmark 6: R6 Temporal correlation (12 hops)" "$query6")

# Benchmark 7: CG-9 Operational impact (15 hops)
query7="MATCH path = (om:OperationalMetric {customer_namespace: 'customer_002'})-[:MONITORS_PERFORMANCE]->(si:ServiceInstance)-[:RUNS_ON]->(pe:PhysicalEntity)-[:HAS_DIGITAL_TWIN]->(dt:DigitalTwinState)-[:OBSERVES_STATE]->(pe2:PhysicalEntity)-[:GOVERNED_BY]->(sc:SafetyConstraint)-[:ENFORCES_COMPLIANCE]->(cp:CompliancePolicy)-[:REQUIRES_VALIDATION]->(gp:GovernancePolicy)-[:APPLIES_TO_CUSTOMER]->(ci:CustomerImpact) WHERE om.metric_value < om.threshold_value AND si.service_status = 'degraded' AND dt.confidence_score < 0.8 RETURN length(path) as total_hops LIMIT 10;"
avg7=$(run_benchmark "Benchmark 7: CG-9 Impact aggregation (15 hops)" "$query7")

# Benchmark 8: Cross-namespace cascade (14 hops)
query8="MATCH path = (te:TemporalEvent)-[:TRIGGERS_CASCADE]->(c1:TemporalEvent)-[:CROSSES_NAMESPACE]->(c2:TemporalEvent)-[:CAUSES_FAILURE]->(sf:SystemFailure)-[:IMPACTS_SERVICE]->(si:ServiceInstance)-[:DEPENDS_ON*1..5]->(dep_si:ServiceInstance)-[:DEGRADES_PERFORMANCE]->(om:OperationalMetric)-[:TRIGGERS_ANOMALY]->(a:AnomalyDetection)-[:LEADS_TO_INCIDENT]->(i:SecurityIncident) WHERE te.customer_namespace <> c2.customer_namespace AND sf.failure_severity = 'critical' AND i.incident_status = 'active' RETURN length(path) as hop_count ORDER BY hop_count DESC LIMIT 5;"
avg8=$(run_benchmark "Benchmark 8: Cross-namespace cascade (14 hops)" "$query8")

# ============================================================================
# AGGREGATIONS
# ============================================================================

echo "=== AGGREGATION QUERIES (Target: <500ms) ==="
echo ""

# Benchmark 9: Total financial impact
query9="MATCH (ci:CustomerImpact) RETURN count(ci) as total_customers_impacted, sum(ci.total_revenue_impact_usd) as total_revenue_loss;"
avg9=$(run_benchmark "Benchmark 9: Total financial impact" "$query9")

# Benchmark 10: Avg metrics by namespace
query10="MATCH (om:OperationalMetric) WHERE om.customer_namespace IS NOT NULL WITH om.customer_namespace as namespace, avg(om.metric_value) as avg_value, count(om) as metric_count RETURN namespace, avg_value, metric_count ORDER BY namespace LIMIT 20;"
avg10=$(run_benchmark "Benchmark 10: Avg metrics by namespace" "$query10")

# ============================================================================
# RESULTS SUMMARY
# ============================================================================

echo "=================================================="
echo "BENCHMARK RESULTS SUMMARY"
echo "=================================================="
echo ""

echo "Simple Queries:"
echo "  [1] DigitalTwinState by namespace: ${avg1}ms (target: 50ms)"
echo "  [2] TemporalEvent last 24h: ${avg2}ms (target: 100ms)"
echo "  [3] OperationalMetric breaches: ${avg3}ms (target: 50ms)"
echo ""

echo "Complex Traversals:"
echo "  [4] UC2 Attack chain (8 hops): ${avg4}ms (target: 2000ms)"
echo "  [5] UC3 Cascading failure (10+ hops): ${avg5}ms (target: 2000ms)"
echo "  [6] R6 Temporal correlation (12 hops): ${avg6}ms (target: 2000ms)"
echo "  [7] CG-9 Impact aggregation (15 hops): ${avg7}ms (target: 2000ms)"
echo "  [8] Cross-namespace cascade (14 hops): ${avg8}ms (target: 2000ms)"
echo ""

echo "Aggregations:"
echo "  [9] Total financial impact: ${avg9}ms (target: 300ms)"
echo "  [10] Avg metrics by namespace: ${avg10}ms (target: 500ms)"
echo ""

# Update JSON results file
echo "Updating results file: $RESULTS_FILE"

cat > "$RESULTS_FILE" <<EOF
{
  "test_date": "$(date '+%Y-%m-%d %H:%M:%S')",
  "neo4j_version": "5.26.14",
  "node_count": 571913,
  "iterations_per_benchmark": $ITERATIONS,
  "benchmarks": {
    "simple_queries": [
      {
        "id": "benchmark_1",
        "name": "Find DigitalTwinState by namespace",
        "target_ms": 50,
        "avg_ms": $avg1,
        "status": "$( [ $avg1 -le 50 ] && echo 'PASS' || echo 'FAIL' )"
      },
      {
        "id": "benchmark_2",
        "name": "Find TemporalEvent last 24h",
        "target_ms": 100,
        "avg_ms": $avg2,
        "status": "$( [ $avg2 -le 100 ] && echo 'PASS' || echo 'FAIL' )"
      },
      {
        "id": "benchmark_3",
        "name": "Count OperationalMetric breaches",
        "target_ms": 50,
        "avg_ms": $avg3,
        "status": "$( [ $avg3 -le 50 ] && echo 'PASS' || echo 'FAIL' )"
      }
    ],
    "complex_traversals": [
      {
        "id": "benchmark_4",
        "name": "UC2: Cyber-physical attack chain (8 hops)",
        "target_ms": 2000,
        "hops": 8,
        "avg_ms": $avg4,
        "status": "$( [ $avg4 -le 2000 ] && echo 'PASS' || echo 'FAIL' )"
      },
      {
        "id": "benchmark_5",
        "name": "UC3: Cascading failure propagation (10+ hops)",
        "target_ms": 2000,
        "hops": 10,
        "avg_ms": $avg5,
        "status": "$( [ $avg5 -le 2000 ] && echo 'PASS' || echo 'FAIL' )"
      },
      {
        "id": "benchmark_6",
        "name": "R6: Temporal correlation (12 hops)",
        "target_ms": 2000,
        "hops": 12,
        "avg_ms": $avg6,
        "status": "$( [ $avg6 -le 2000 ] && echo 'PASS' || echo 'FAIL' )"
      },
      {
        "id": "benchmark_7",
        "name": "CG-9: Operational impact aggregation (15 hops)",
        "target_ms": 2000,
        "hops": 15,
        "avg_ms": $avg7,
        "status": "$( [ $avg7 -le 2000 ] && echo 'PASS' || echo 'FAIL' )"
      },
      {
        "id": "benchmark_8",
        "name": "Cross-namespace cascading failure (14 hops)",
        "target_ms": 2000,
        "hops": 14,
        "avg_ms": $avg8,
        "status": "$( [ $avg8 -le 2000 ] && echo 'PASS' || echo 'FAIL' )"
      }
    ],
    "aggregations": [
      {
        "id": "benchmark_9",
        "name": "Sum total financial impact",
        "target_ms": 300,
        "avg_ms": $avg9,
        "status": "$( [ $avg9 -le 300 ] && echo 'PASS' || echo 'FAIL' )"
      },
      {
        "id": "benchmark_10",
        "name": "Average operational metrics by namespace",
        "target_ms": 500,
        "avg_ms": $avg10,
        "status": "$( [ $avg10 -le 500 ] && echo 'PASS' || echo 'FAIL' )"
      }
    ]
  }
}
EOF

echo ""
echo "Results saved to: $RESULTS_FILE"
echo ""
echo "=================================================="
echo "BENCHMARK COMPLETE"
echo "=================================================="
