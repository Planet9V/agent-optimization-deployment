#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
# NEO4J TEST EXECUTION SCRIPT
# ═══════════════════════════════════════════════════════════════════════

set -e

NEO4J_CONTAINER="openspg-neo4j"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="neo4j@openspg"
TEST_FILE="/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/tests/actual_comprehensive_test_suite.cypher"
RESULTS_FILE="/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/tests/test_results.json"

echo "Executing comprehensive test suite..."
echo "Results will be saved to: $RESULTS_FILE"

# Execute full test file
docker exec $NEO4J_CONTAINER cypher-shell -u $NEO4J_USER -p "$NEO4J_PASSWORD" --format plain < "$TEST_FILE" > "${RESULTS_FILE}.raw"

echo "Tests complete. Results in $RESULTS_FILE"
