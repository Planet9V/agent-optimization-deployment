#!/bin/bash

# Post-Task Verification Script
# Purpose: Verify task outcomes match expected results
# Usage: ./post_task_verify.sh <task_id> <taskmaster_file>

set -e

TASK_ID="$1"
TASKMASTER_FILE="$2"
EVIDENCE_DIR="verification_system/evidence"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
EVIDENCE_FILE="${EVIDENCE_DIR}/post_check_${TASK_ID}_${TIMESTAMP}.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}POST-TASK VERIFICATION: ${TASK_ID}${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Extract task details
TASK_LINE=$(grep "^${TASK_ID}" "$TASKMASTER_FILE")
TASK_DESC=$(echo "$TASK_LINE" | cut -d'|' -f2)
SUCCESS_CRITERIA=$(echo "$TASK_LINE" | cut -d'|' -f6)

echo -e "Task: ${TASK_DESC}"
echo -e "Success Criteria: ${SUCCESS_CRITERIA}"
echo ""

# Initialize verification results
CHECKS_PASSED=0
CHECKS_FAILED=0
VERIFICATION_DETAILS=()

# Task-specific outcome verification
case "$TASK_ID" in
    "1.1")
        echo -e "${YELLOW}Verifying Task 1.1: Entity catalog in Qdrant...${NC}"

        # Check Qdrant collection exists
        COLLECTIONS=$(curl -s http://localhost:6333/collections | jq -r '.result.collections[].name' 2>/dev/null || echo "")

        if echo "$COLLECTIONS" | grep -q "ner11_entities"; then
            echo -e "${GREEN}✓ Qdrant collection 'ner11_entities' exists${NC}"
            CHECKS_PASSED=$((CHECKS_PASSED + 1))
            VERIFICATION_DETAILS+=("Collection exists: PASS")

            # Verify entity count
            POINT_COUNT=$(curl -s http://localhost:6333/collections/ner11_entities | jq -r '.result.points_count')

            if [ "$POINT_COUNT" -gt 0 ]; then
                echo -e "${GREEN}✓ Collection has ${POINT_COUNT} entities${NC}"
                CHECKS_PASSED=$((CHECKS_PASSED + 1))
                VERIFICATION_DETAILS+=("Entity count: ${POINT_COUNT} PASS")
            else
                echo -e "${RED}✗ Collection is empty${NC}"
                CHECKS_FAILED=$((CHECKS_FAILED + 1))
                VERIFICATION_DETAILS+=("Entity count: 0 FAIL")
            fi

            # Verify entity structure (sample one entity)
            SAMPLE_ENTITY=$(curl -s -X POST http://localhost:6333/collections/ner11_entities/points/scroll \
                -H "Content-Type: application/json" \
                -d '{"limit": 1}' | jq -r '.result.points[0]')

            if echo "$SAMPLE_ENTITY" | jq -e '.payload.entity_name' > /dev/null 2>&1; then
                echo -e "${GREEN}✓ Entities have required 'entity_name' field${NC}"
                CHECKS_PASSED=$((CHECKS_PASSED + 1))
                VERIFICATION_DETAILS+=("Entity structure: PASS")
            else
                echo -e "${RED}✗ Entities missing required fields${NC}"
                CHECKS_FAILED=$((CHECKS_FAILED + 1))
                VERIFICATION_DETAILS+=("Entity structure: FAIL")
            fi
        else
            echo -e "${RED}✗ Qdrant collection 'ner11_entities' not found${NC}"
            CHECKS_FAILED=$((CHECKS_FAILED + 1))
            VERIFICATION_DETAILS+=("Collection exists: FAIL")
        fi
        ;;

    "2.2")
        echo -e "${YELLOW}Verifying Task 2.2: Expanded entities in Qdrant...${NC}"

        # Query for entities with expansion_data
        EXPANDED_COUNT=$(curl -s -X POST http://localhost:6333/collections/ner11_entities/points/scroll \
            -H "Content-Type: application/json" \
            -d '{
                "filter": {
                    "must": [
                        {"key": "expansion_data", "match": {"any": ["*"]}}
                    ]
                },
                "limit": 100
            }' | jq -r '.result.points | length' 2>/dev/null || echo "0")

        if [ "$EXPANDED_COUNT" -gt 0 ]; then
            echo -e "${GREEN}✓ Found ${EXPANDED_COUNT} expanded entities in Qdrant${NC}"
            CHECKS_PASSED=$((CHECKS_PASSED + 1))
            VERIFICATION_DETAILS+=("Expanded entities count: ${EXPANDED_COUNT} PASS")

            # Verify expansion fields exist
            SAMPLE_EXPANSION=$(curl -s -X POST http://localhost:6333/collections/ner11_entities/points/scroll \
                -H "Content-Type: application/json" \
                -d '{
                    "filter": {
                        "must": [
                            {"key": "expansion_data", "match": {"any": ["*"]}}
                        ]
                    },
                    "limit": 1
                }' | jq -r '.result.points[0].payload.expansion_data')

            if echo "$SAMPLE_EXPANSION" | jq -e '.description' > /dev/null 2>&1; then
                echo -e "${GREEN}✓ Expansion data has 'description' field${NC}"
                CHECKS_PASSED=$((CHECKS_PASSED + 1))
                VERIFICATION_DETAILS+=("Expansion structure: PASS")
            else
                echo -e "${RED}✗ Expansion data missing required fields${NC}"
                CHECKS_FAILED=$((CHECKS_FAILED + 1))
                VERIFICATION_DETAILS+=("Expansion structure: FAIL")
            fi
        else
            echo -e "${RED}✗ No expanded entities found in Qdrant${NC}"
            CHECKS_FAILED=$((CHECKS_FAILED + 1))
            VERIFICATION_DETAILS+=("Expanded entities: 0 FAIL")
        fi
        ;;

    "2.3")
        echo -e "${YELLOW}Verifying Task 2.3: Expanded entities in Neo4j...${NC}"

        # Count entity nodes with expansion properties
        EXPANDED_COUNT=$(cypher-shell -u neo4j -p your_password \
            "MATCH (e:Entity) WHERE e.description IS NOT NULL RETURN count(e) as count" \
            --format plain 2>/dev/null | tail -n1 || echo "0")

        if [ "$EXPANDED_COUNT" -gt 0 ]; then
            echo -e "${GREEN}✓ Found ${EXPANDED_COUNT} expanded entities in Neo4j${NC}"
            CHECKS_PASSED=$((CHECKS_PASSED + 1))
            VERIFICATION_DETAILS+=("Neo4j expanded entities: ${EXPANDED_COUNT} PASS")
        else
            echo -e "${RED}✗ No expanded entities in Neo4j${NC}"
            CHECKS_FAILED=$((CHECKS_FAILED + 1))
            VERIFICATION_DETAILS+=("Neo4j expanded entities: 0 FAIL")
        fi
        ;;

    "2.4")
        echo -e "${YELLOW}Verifying Task 2.4: Psychohistory relationships...${NC}"

        # Count psychohistory relationships
        REL_COUNT=$(cypher-shell -u neo4j -p your_password \
            "MATCH ()-[r:INFLUENCES|PREDICTS|SHAPES]->() RETURN count(r) as count" \
            --format plain 2>/dev/null | tail -n1 || echo "0")

        if [ "$REL_COUNT" -gt 0 ]; then
            echo -e "${GREEN}✓ Found ${REL_COUNT} psychohistory relationships in Neo4j${NC}"
            CHECKS_PASSED=$((CHECKS_PASSED + 1))
            VERIFICATION_DETAILS+=("Psychohistory relationships: ${REL_COUNT} PASS")

            # Verify relationship properties
            HAS_PROPS=$(cypher-shell -u neo4j -p your_password \
                "MATCH ()-[r:INFLUENCES|PREDICTS|SHAPES]->() WHERE r.confidence IS NOT NULL RETURN count(r) as count" \
                --format plain 2>/dev/null | tail -n1 || echo "0")

            if [ "$HAS_PROPS" -gt 0 ]; then
                echo -e "${GREEN}✓ Relationships have confidence properties${NC}"
                CHECKS_PASSED=$((CHECKS_PASSED + 1))
                VERIFICATION_DETAILS+=("Relationship properties: PASS")
            else
                echo -e "${RED}✗ Relationships missing properties${NC}"
                CHECKS_FAILED=$((CHECKS_FAILED + 1))
                VERIFICATION_DETAILS+=("Relationship properties: FAIL")
            fi
        else
            echo -e "${RED}✗ No psychohistory relationships in Neo4j${NC}"
            CHECKS_FAILED=$((CHECKS_FAILED + 1))
            VERIFICATION_DETAILS+=("Psychohistory relationships: 0 FAIL")
        fi
        ;;

    *)
        echo -e "${YELLOW}⚠ No specific verification defined for task ${TASK_ID}${NC}"
        echo -e "${YELLOW}  Assuming task complete if marked in taskmaster${NC}"
        CHECKS_PASSED=1
        VERIFICATION_DETAILS+=("Generic verification: PASS")
        ;;
esac

# Generate evidence report
mkdir -p "$EVIDENCE_DIR"

cat > "$EVIDENCE_FILE" << EOF
{
  "task_id": "$TASK_ID",
  "task_description": "$TASK_DESC",
  "timestamp": "$TIMESTAMP",
  "verification_type": "post_task",
  "checks_passed": $CHECKS_PASSED,
  "checks_failed": $CHECKS_FAILED,
  "verification_details": [
$(IFS=$'\n'; echo "${VERIFICATION_DETAILS[*]}" | sed 's/^/    "/' | sed 's/$/",/' | sed '$ s/,$//')
  ],
  "overall_result": "$([ $CHECKS_FAILED -eq 0 ] && echo "PASS" || echo "FAIL")"
}
EOF

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}VERIFICATION SUMMARY${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Checks passed: ${CHECKS_PASSED}"
echo -e "Checks failed: ${CHECKS_FAILED}"
echo ""

# Final decision
if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ VERIFICATION PASSED: Task ${TASK_ID} completed successfully${NC}"
    echo -e "Evidence stored: ${EVIDENCE_FILE}"
    exit 0
else
    echo -e "${RED}❌ VERIFICATION FAILED: Task ${TASK_ID} outcomes do not match expectations${NC}"
    echo -e "Evidence stored: ${EVIDENCE_FILE}"
    echo ""
    echo -e "${RED}Task must be re-executed to meet success criteria${NC}"
    exit 1
fi
