#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
# NEO4J COMPREHENSIVE TEST EXECUTION SCRIPT
# ═══════════════════════════════════════════════════════════════════════
# File: execute_tests.sh
# Created: 2025-11-28 15:30:00 UTC
# Version: v1.0.0
# Purpose: Execute comprehensive test suite against Neo4j database
# Target: 95%+ pass rate
# ═══════════════════════════════════════════════════════════════════════

set -e

# Configuration
NEO4J_CONTAINER="openspg-neo4j"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="neo4j@openspg"
TEST_FILE="/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/tests/comprehensive_test_suite.cypher"
RESULTS_FILE="/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/tests/test_results_$(date +%Y%m%d_%H%M%S).json"

echo "═══════════════════════════════════════════════════════════════════════"
echo "EXECUTING COMPREHENSIVE NEO4J TEST SUITE"
echo "═══════════════════════════════════════════════════════════════════════"
echo "Container: $NEO4J_CONTAINER"
echo "Test File: $TEST_FILE"
echo "Results File: $RESULTS_FILE"
echo "═══════════════════════════════════════════════════════════════════════"

# Check if container is running
if ! docker ps | grep -q "$NEO4J_CONTAINER"; then
    echo "ERROR: Neo4j container '$NEO4J_CONTAINER' is not running"
    exit 1
fi

# Execute each test query and capture results
echo "Executing test queries..."
echo "{" > "$RESULTS_FILE"
echo '  "test_suite": "NER11 Gold Standard Comprehensive Validation",' >> "$RESULTS_FILE"
echo '  "timestamp": "'$(date -u +"%Y-%m-%d %H:%M:%S UTC")'",' >> "$RESULTS_FILE"
echo '  "tests": [' >> "$RESULTS_FILE"

# Extract and execute each test query
test_count=0
while IFS= read -r line; do
    if [[ "$line" =~ ^//[[:space:]]TEST[[:space:]][0-9]+ ]]; then
        # New test found
        test_name=$(echo "$line" | sed 's/^\/\/ TEST \([0-9]*\): \(.*\)/\2/')
        query=""
    elif [[ "$line" =~ ^MATCH.*TEST_[0-9]+ ]]; then
        # Start of query
        query="$line"
    elif [[ -n "$query" && ! "$line" =~ ^// && ! "$line" =~ ^[[:space:]]*$ ]]; then
        # Continue building query
        query="$query $line"

        # Check if query is complete (ends with semicolon)
        if [[ "$line" =~ \;[[:space:]]*$ ]]; then
            # Execute query
            test_count=$((test_count + 1))
            echo "  Executing Test $test_count: $test_name"

            # Run query and capture result
            result=$(docker exec "$NEO4J_CONTAINER" cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" --format plain "$query" 2>&1 || echo "ERROR")

            # Parse result
            if [[ "$result" == "ERROR" || "$result" =~ "error" ]]; then
                status="FAIL"
                actual_count="ERROR"
                expected_count="N/A"
            else
                status=$(echo "$result" | grep -oP '(?<=\|)[[:space:]]*PASS[[:space:]]*(?=\|)' || echo "FAIL")
                actual_count=$(echo "$result" | grep -oP '(?<=\|)[[:space:]]*[0-9.]+[[:space:]]*(?=\|)' | head -1 || echo "0")
                expected_count=$(echo "$result" | grep -oP '(?<=\|)[[:space:]]*[0-9.]+[[:space:]]*(?=\|)' | head -2 | tail -1 || echo "0")
            fi

            # Write to results file
            if [ $test_count -gt 1 ]; then
                echo "," >> "$RESULTS_FILE"
            fi
            cat >> "$RESULTS_FILE" << EOF
    {
      "test_id": "TEST_$(printf '%03d' $test_count)",
      "test_name": "$test_name",
      "status": "$status",
      "expected": "$expected_count",
      "actual": "$actual_count",
      "query": "$(echo $query | sed 's/"/\\"/g')"
    }
EOF

            # Reset query
            query=""
        fi
    fi
done < "$TEST_FILE"

echo "" >> "$RESULTS_FILE"
echo "  ]" >> "$RESULTS_FILE"
echo "}" >> "$RESULTS_FILE"

echo "═══════════════════════════════════════════════════════════════════════"
echo "TEST EXECUTION COMPLETE"
echo "Results saved to: $RESULTS_FILE"
echo "═══════════════════════════════════════════════════════════════════════"
