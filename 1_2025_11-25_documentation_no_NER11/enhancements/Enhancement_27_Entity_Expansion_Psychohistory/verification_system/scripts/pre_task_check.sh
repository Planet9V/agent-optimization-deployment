#!/bin/bash

# Pre-Task Verification Script
# Purpose: Verify all prerequisites before task execution
# Usage: ./pre_task_check.sh <task_id> <taskmaster_file>

set -e

TASK_ID="$1"
TASKMASTER_FILE="$2"
EVIDENCE_DIR="verification_system/evidence"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
EVIDENCE_FILE="${EVIDENCE_DIR}/pre_check_${TASK_ID}_${TIMESTAMP}.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}PRE-TASK VERIFICATION: ${TASK_ID}${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Verify task exists in taskmaster
if ! grep -q "^${TASK_ID}" "$TASKMASTER_FILE"; then
    echo -e "${RED}❌ FATAL: Task ${TASK_ID} not found in taskmaster${NC}"
    exit 1
fi

# Extract task details
TASK_LINE=$(grep "^${TASK_ID}" "$TASKMASTER_FILE")
TASK_DESC=$(echo "$TASK_LINE" | cut -d'|' -f2)
DEPENDENCIES=$(echo "$TASK_LINE" | cut -d'|' -f4)

echo -e "Task: ${TASK_DESC}"
echo -e "Dependencies: ${DEPENDENCIES}"
echo ""

# Parse and verify dependencies
FAILED_DEPS=()
PASSED_DEPS=()

if [ "$DEPENDENCIES" != "none" ] && [ -n "$DEPENDENCIES" ]; then
    IFS=',' read -ra DEP_ARRAY <<< "$DEPENDENCIES"

    for dep in "${DEP_ARRAY[@]}"; do
        dep=$(echo "$dep" | xargs) # trim whitespace

        echo -e "Checking dependency: ${dep}"

        # Check if dependency task is marked complete in taskmaster
        DEP_STATUS=$(grep "^${dep}" "$TASKMASTER_FILE" | cut -d'|' -f5)

        if [ "$DEP_STATUS" != "✅" ]; then
            echo -e "${RED}  ❌ FAIL: Dependency ${dep} not completed (status: ${DEP_STATUS})${NC}"
            FAILED_DEPS+=("$dep")
        else
            echo -e "${GREEN}  ✓ PASS: Dependency ${dep} completed${NC}"
            PASSED_DEPS+=("$dep")

            # Verify evidence exists for dependency
            EVIDENCE_EXISTS=$(find "$EVIDENCE_DIR" -name "post_check_${dep}_*.json" | wc -l)
            if [ "$EVIDENCE_EXISTS" -eq 0 ]; then
                echo -e "${YELLOW}  ⚠ WARNING: No verification evidence found for ${dep}${NC}"
            fi
        fi
    done
fi

# Check database prerequisites for specific tasks
echo ""
echo -e "${YELLOW}Checking database prerequisites...${NC}"

DB_CHECKS_PASSED=true

case "$TASK_ID" in
    "2.2")
        # Task 2.2 requires Qdrant collection with entities
        echo "Verifying Qdrant collection 'ner11_entities' exists..."

        COLLECTIONS=$(curl -s http://localhost:6333/collections | jq -r '.result.collections[].name' 2>/dev/null || echo "")

        if echo "$COLLECTIONS" | grep -q "ner11_entities"; then
            POINT_COUNT=$(curl -s http://localhost:6333/collections/ner11_entities | jq -r '.result.points_count' 2>/dev/null || echo "0")

            if [ "$POINT_COUNT" -gt 0 ]; then
                echo -e "${GREEN}  ✓ PASS: Qdrant collection exists with ${POINT_COUNT} entities${NC}"
            else
                echo -e "${RED}  ❌ FAIL: Qdrant collection exists but is empty${NC}"
                DB_CHECKS_PASSED=false
            fi
        else
            echo -e "${RED}  ❌ FAIL: Qdrant collection 'ner11_entities' not found${NC}"
            DB_CHECKS_PASSED=false
        fi
        ;;

    "2.3"|"2.4")
        # Tasks 2.3 and 2.4 require Neo4j with entity nodes
        echo "Verifying Neo4j has entity nodes..."

        ENTITY_COUNT=$(cypher-shell -u neo4j -p your_password \
            "MATCH (e:Entity) RETURN count(e) as count" \
            --format plain 2>/dev/null | tail -n1 || echo "0")

        if [ "$ENTITY_COUNT" -gt 0 ]; then
            echo -e "${GREEN}  ✓ PASS: Neo4j has ${ENTITY_COUNT} entity nodes${NC}"
        else
            echo -e "${RED}  ❌ FAIL: Neo4j has no entity nodes${NC}"
            DB_CHECKS_PASSED=false
        fi
        ;;
esac

# Generate evidence report
mkdir -p "$EVIDENCE_DIR"

cat > "$EVIDENCE_FILE" << EOF
{
  "task_id": "$TASK_ID",
  "task_description": "$TASK_DESC",
  "timestamp": "$TIMESTAMP",
  "verification_type": "pre_task",
  "dependencies": {
    "required": "$DEPENDENCIES",
    "passed": [$(IFS=','; echo "\"${PASSED_DEPS[*]}\"")],
    "failed": [$(IFS=','; echo "\"${FAILED_DEPS[*]}\"")]
  },
  "database_checks_passed": $DB_CHECKS_PASSED,
  "overall_result": "$([ ${#FAILED_DEPS[@]} -eq 0 ] && [ "$DB_CHECKS_PASSED" = true ] && echo "PASS" || echo "FAIL")"
}
EOF

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}VERIFICATION SUMMARY${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Dependencies passed: ${#PASSED_DEPS[@]}"
echo -e "Dependencies failed: ${#FAILED_DEPS[@]}"
echo -e "Database checks: $([ "$DB_CHECKS_PASSED" = true ] && echo "PASS" || echo "FAIL")"
echo ""

# Final decision
if [ ${#FAILED_DEPS[@]} -eq 0 ] && [ "$DB_CHECKS_PASSED" = true ]; then
    echo -e "${GREEN}✅ VERIFICATION PASSED: Task ${TASK_ID} may proceed${NC}"
    echo -e "Evidence stored: ${EVIDENCE_FILE}"
    exit 0
else
    echo -e "${RED}❌ VERIFICATION FAILED: Task ${TASK_ID} BLOCKED${NC}"
    echo -e "Evidence stored: ${EVIDENCE_FILE}"
    echo ""
    echo -e "${RED}BLOCKING REASONS:${NC}"

    if [ ${#FAILED_DEPS[@]} -gt 0 ]; then
        echo -e "${RED}  • Incomplete dependencies: ${FAILED_DEPS[*]}${NC}"
    fi

    if [ "$DB_CHECKS_PASSED" = false ]; then
        echo -e "${RED}  • Database prerequisites not met${NC}"
    fi

    exit 1
fi
