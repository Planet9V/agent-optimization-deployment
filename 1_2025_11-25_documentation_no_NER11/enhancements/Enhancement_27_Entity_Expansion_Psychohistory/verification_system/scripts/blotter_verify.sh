#!/bin/bash

# BLOTTER Verification Script
# Purpose: Cross-check BLOTTER claims against database reality
# Usage: ./blotter_verify.sh <blotter_file> <taskmaster_file>

set -e

BLOTTER_FILE="$1"
TASKMASTER_FILE="$2"
EVIDENCE_DIR="verification_system/evidence"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
REPORT_FILE="${EVIDENCE_DIR}/blotter_verification_${TIMESTAMP}.txt"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        BLOTTER VERIFICATION - CLAIMS vs REALITY           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create report file
exec > >(tee -a "$REPORT_FILE")
exec 2>&1

echo "BLOTTER Verification Report"
echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
echo "BLOTTER File: $BLOTTER_FILE"
echo "Taskmaster File: $TASKMASTER_FILE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Extract task completions claimed in BLOTTER
echo -e "${YELLOW}Extracting completion claims from BLOTTER...${NC}"
echo ""

COMPLETED_CLAIMS=$(grep -E "✅|COMPLETE|DONE|FINISHED" "$BLOTTER_FILE" | grep -E "[0-9]+\.[0-9]+" || true)

if [ -z "$COMPLETED_CLAIMS" ]; then
    echo -e "${RED}❌ No completion claims found in BLOTTER${NC}"
    exit 1
fi

echo "Found completion claims:"
echo "$COMPLETED_CLAIMS"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Initialize counters
TOTAL_CLAIMS=0
VERIFIED_CLAIMS=0
DISCREPANCIES=0

echo -e "${YELLOW}Cross-checking claims against database state...${NC}"
echo ""

# Extract task IDs from claims
TASK_IDS=$(echo "$COMPLETED_CLAIMS" | grep -oE "[0-9]+\.[0-9]+" | sort -u)

for TASK_ID in $TASK_IDS; do
    TOTAL_CLAIMS=$((TOTAL_CLAIMS + 1))

    echo -e "${BLUE}━━━ Task ${TASK_ID} ━━━${NC}"

    # Get claim from BLOTTER
    CLAIM_LINE=$(echo "$COMPLETED_CLAIMS" | grep "$TASK_ID" | head -n1)
    echo "BLOTTER Claim: $CLAIM_LINE"

    # Check taskmaster status
    TASKMASTER_STATUS=$(grep "^${TASK_ID}" "$TASKMASTER_FILE" | cut -d'|' -f5 | xargs)
    echo "Taskmaster Status: $TASKMASTER_STATUS"

    # Check verification evidence
    EVIDENCE_FILES=$(find "$EVIDENCE_DIR" -name "post_check_${TASK_ID}_*.json" 2>/dev/null | wc -l)
    echo "Verification Evidence: $EVIDENCE_FILES file(s)"

    # Database verification based on task
    DB_VERIFIED=false
    DB_DETAILS=""

    case "$TASK_ID" in
        "1.1")
            echo "Checking Qdrant for initial catalog..."
            POINT_COUNT=$(curl -s http://localhost:6333/collections/ner11_entities 2>/dev/null | jq -r '.result.points_count' || echo "0")
            if [ "$POINT_COUNT" -gt 0 ]; then
                DB_VERIFIED=true
                DB_DETAILS="Qdrant has ${POINT_COUNT} entities"
            else
                DB_DETAILS="Qdrant collection empty or not found"
            fi
            ;;

        "2.2")
            echo "Checking Qdrant for expanded entities..."
            EXPANDED_COUNT=$(curl -s -X POST http://localhost:6333/collections/ner11_entities/points/scroll \
                -H "Content-Type: application/json" \
                -d '{
                    "filter": {
                        "must": [
                            {"key": "expansion_data", "match": {"any": ["*"]}}
                        ]
                    },
                    "limit": 100
                }' 2>/dev/null | jq -r '.result.points | length' || echo "0")

            if [ "$EXPANDED_COUNT" -gt 0 ]; then
                DB_VERIFIED=true
                DB_DETAILS="Qdrant has ${EXPANDED_COUNT} expanded entities"
            else
                DB_DETAILS="No expanded entities in Qdrant"
            fi
            ;;

        "2.3")
            echo "Checking Neo4j for expanded entities..."
            ENTITY_COUNT=$(cypher-shell -u neo4j -p your_password \
                "MATCH (e:Entity) WHERE e.description IS NOT NULL RETURN count(e) as count" \
                --format plain 2>/dev/null | tail -n1 || echo "0")

            if [ "$ENTITY_COUNT" -gt 0 ]; then
                DB_VERIFIED=true
                DB_DETAILS="Neo4j has ${ENTITY_COUNT} expanded entities"
            else
                DB_DETAILS="No expanded entities in Neo4j"
            fi
            ;;

        "2.4")
            echo "Checking Neo4j for psychohistory relationships..."
            REL_COUNT=$(cypher-shell -u neo4j -p your_password \
                "MATCH ()-[r:INFLUENCES|PREDICTS|SHAPES]->() RETURN count(r) as count" \
                --format plain 2>/dev/null | tail -n1 || echo "0")

            if [ "$REL_COUNT" -gt 0 ]; then
                DB_VERIFIED=true
                DB_DETAILS="Neo4j has ${REL_COUNT} psychohistory relationships"
            else
                DB_DETAILS="No psychohistory relationships in Neo4j"
            fi
            ;;

        *)
            DB_VERIFIED=true  # Assume verified for tasks without specific checks
            DB_DETAILS="No specific database check defined"
            ;;
    esac

    echo "Database Status: $DB_DETAILS"

    # Final verification decision
    if [ "$TASKMASTER_STATUS" = "✅" ] && [ "$EVIDENCE_FILES" -gt 0 ] && [ "$DB_VERIFIED" = true ]; then
        echo -e "${GREEN}✅ VERIFIED: Claim matches reality${NC}"
        VERIFIED_CLAIMS=$((VERIFIED_CLAIMS + 1))
    else
        echo -e "${RED}❌ DISCREPANCY: Claim does not match reality${NC}"
        DISCREPANCIES=$((DISCREPANCIES + 1))

        echo -e "${RED}Discrepancy Details:${NC}"
        [ "$TASKMASTER_STATUS" != "✅" ] && echo -e "${RED}  • Taskmaster not marked complete${NC}"
        [ "$EVIDENCE_FILES" -eq 0 ] && echo -e "${RED}  • No verification evidence${NC}"
        [ "$DB_VERIFIED" = false ] && echo -e "${RED}  • Database verification failed: $DB_DETAILS${NC}"
    fi

    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    VERIFICATION SUMMARY                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo "Total claims checked:     $TOTAL_CLAIMS"
echo -e "Claims verified:          ${GREEN}${VERIFIED_CLAIMS}${NC}"
echo -e "Discrepancies found:      ${RED}${DISCREPANCIES}${NC}"
echo "Verification rate:        $(awk "BEGIN {printf \"%.1f%%\", ($VERIFIED_CLAIMS/$TOTAL_CLAIMS)*100}")"
echo ""

# Additional checks
echo -e "${YELLOW}Additional Integrity Checks:${NC}"
echo ""

# Check for tasks marked in taskmaster but not in BLOTTER
TASKMASTER_COMPLETE=$(grep "✅" "$TASKMASTER_FILE" | grep -oE "^[0-9]+\.[0-9]+" || true)
MISSING_FROM_BLOTTER=()

for TASK_ID in $TASKMASTER_COMPLETE; do
    if ! echo "$TASK_IDS" | grep -q "^${TASK_ID}$"; then
        MISSING_FROM_BLOTTER+=("$TASK_ID")
    fi
done

if [ ${#MISSING_FROM_BLOTTER[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Tasks marked complete in taskmaster but not claimed in BLOTTER:${NC}"
    for task in "${MISSING_FROM_BLOTTER[@]}"; do
        echo "  • $task"
    done
    echo ""
fi

# Check for database state without task completion
echo "Checking for database state inconsistencies..."

# Qdrant check
QDRANT_POINTS=$(curl -s http://localhost:6333/collections/ner11_entities 2>/dev/null | jq -r '.result.points_count' || echo "0")
TASK_11_STATUS=$(grep "^1\.1" "$TASKMASTER_FILE" | cut -d'|' -f5 | xargs)

if [ "$QDRANT_POINTS" -gt 0 ] && [ "$TASK_11_STATUS" != "✅" ]; then
    echo -e "${YELLOW}⚠️  Qdrant has data but Task 1.1 not marked complete${NC}"
fi

# Neo4j check
NEO4J_ENTITIES=$(cypher-shell -u neo4j -p your_password \
    "MATCH (e:Entity) RETURN count(e) as count" \
    --format plain 2>/dev/null | tail -n1 || echo "0")
TASK_23_STATUS=$(grep "^2\.3" "$TASKMASTER_FILE" | cut -d'|' -f5 | xargs)

if [ "$NEO4J_ENTITIES" -gt 0 ] && [ "$TASK_23_STATUS" != "✅" ]; then
    echo -e "${YELLOW}⚠️  Neo4j has entities but Task 2.3 not marked complete${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Final verdict
if [ $DISCREPANCIES -eq 0 ] && [ ${#MISSING_FROM_BLOTTER[@]} -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ BLOTTER VERIFIED - ALL CLAIMS MATCH REALITY           ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Report saved to: $REPORT_FILE"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ BLOTTER DISCREPANCIES FOUND                            ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${RED}ACTION REQUIRED:${NC}"
    echo "1. Review discrepancies listed above"
    echo "2. Update BLOTTER to reflect actual completion state"
    echo "3. Re-execute tasks that show discrepancies"
    echo "4. Run verification scripts to generate proper evidence"
    echo "5. Re-run this BLOTTER verification"
    echo ""
    echo "Report saved to: $REPORT_FILE"
    exit 1
fi
