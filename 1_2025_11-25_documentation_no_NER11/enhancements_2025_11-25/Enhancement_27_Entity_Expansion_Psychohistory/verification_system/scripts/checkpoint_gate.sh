#!/bin/bash

# Checkpoint Gate Script
# Purpose: Block forward progress if any tasks are incomplete
# Usage: ./checkpoint_gate.sh <taskmaster_file> <phase_number>

set -e

TASKMASTER_FILE="$1"
PHASE="${2:-all}"  # Default to checking all phases
EVIDENCE_DIR="verification_system/evidence"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          CHECKPOINT GATE - TASK VERIFICATION              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Determine which tasks to check
if [ "$PHASE" = "all" ]; then
    echo -e "${YELLOW}Checking ALL tasks in taskmaster${NC}"
    TASKS=$(grep -E "^[0-9]+\.[0-9]+" "$TASKMASTER_FILE" || true)
else
    echo -e "${YELLOW}Checking Phase ${PHASE} tasks only${NC}"
    TASKS=$(grep -E "^${PHASE}\.[0-9]+" "$TASKMASTER_FILE" || true)
fi

if [ -z "$TASKS" ]; then
    echo -e "${RED}❌ No tasks found to verify${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
printf "${BLUE}%-8s %-35s %-15s %-15s %-10s${NC}\n" "TASK" "DESCRIPTION" "REQUIRED" "ACTUAL" "STATUS"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

TOTAL_TASKS=0
PASSED_TASKS=0
FAILED_TASKS=0
FAILED_LIST=()

# Process each task
while IFS= read -r task_line; do
    TOTAL_TASKS=$((TOTAL_TASKS + 1))

    TASK_ID=$(echo "$task_line" | cut -d'|' -f1 | xargs)
    TASK_DESC=$(echo "$task_line" | cut -d'|' -f2 | xargs)
    TASK_STATUS=$(echo "$task_line" | cut -d'|' -f5 | xargs)
    SUCCESS_CRITERIA=$(echo "$task_line" | cut -d'|' -f6 | xargs)

    # Truncate description for display
    DISPLAY_DESC=$(echo "$TASK_DESC" | cut -c1-35)

    # Determine what's required vs actual
    REQUIRED="Complete"
    ACTUAL="Unknown"
    STATUS_SYMBOL=""

    # Check taskmaster status
    if [ "$TASK_STATUS" = "✅" ]; then
        ACTUAL="Marked Complete"

        # Check for verification evidence
        EVIDENCE_FILES=$(find "$EVIDENCE_DIR" -name "post_check_${TASK_ID}_*.json" 2>/dev/null | wc -l)

        if [ "$EVIDENCE_FILES" -gt 0 ]; then
            # Get most recent evidence file
            LATEST_EVIDENCE=$(find "$EVIDENCE_DIR" -name "post_check_${TASK_ID}_*.json" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")

            # Check if verification passed
            VERIFICATION_RESULT=$(jq -r '.overall_result' "$LATEST_EVIDENCE" 2>/dev/null || echo "UNKNOWN")

            if [ "$VERIFICATION_RESULT" = "PASS" ]; then
                STATUS_SYMBOL="${GREEN}✅ PASS${NC}"
                PASSED_TASKS=$((PASSED_TASKS + 1))
            else
                STATUS_SYMBOL="${RED}❌ FAIL${NC}"
                ACTUAL="Verified FAILED"
                FAILED_TASKS=$((FAILED_TASKS + 1))
                FAILED_LIST+=("$TASK_ID: Verification failed")
            fi
        else
            STATUS_SYMBOL="${YELLOW}⚠️  WARN${NC}"
            ACTUAL="No Verification"
            FAILED_TASKS=$((FAILED_TASKS + 1))
            FAILED_LIST+=("$TASK_ID: Missing verification evidence")
        fi
    else
        STATUS_SYMBOL="${RED}❌ FAIL${NC}"
        ACTUAL="Incomplete"
        FAILED_TASKS=$((FAILED_TASKS + 1))
        FAILED_LIST+=("$TASK_ID: Not marked complete")
    fi

    # Task-specific database checks
    DB_STATUS=""
    case "$TASK_ID" in
        "1.1"|"2.2")
            # Check Qdrant
            POINT_COUNT=$(curl -s http://localhost:6333/collections/ner11_entities 2>/dev/null | jq -r '.result.points_count' || echo "0")
            if [ "$POINT_COUNT" -gt 0 ]; then
                DB_STATUS=" (Qdrant: ${POINT_COUNT} entities)"
            else
                DB_STATUS=" ${RED}(Qdrant: EMPTY)${NC}"
                if [ "$TASK_STATUS" = "✅" ]; then
                    STATUS_SYMBOL="${RED}❌ FAIL${NC}"
                    FAILED_TASKS=$((FAILED_TASKS + 1))
                    PASSED_TASKS=$((PASSED_TASKS - 1))
                    FAILED_LIST+=("$TASK_ID: Database verification failed (Qdrant empty)")
                fi
            fi
            ;;
        "2.3"|"2.4")
            # Check Neo4j
            ENTITY_COUNT=$(cypher-shell -u neo4j -p your_password \
                "MATCH (e:Entity) RETURN count(e) as count" \
                --format plain 2>/dev/null | tail -n1 || echo "0")
            if [ "$ENTITY_COUNT" -gt 0 ]; then
                DB_STATUS=" (Neo4j: ${ENTITY_COUNT} entities)"
            else
                DB_STATUS=" ${RED}(Neo4j: NO ENTITIES)${NC}"
                if [ "$TASK_STATUS" = "✅" ]; then
                    STATUS_SYMBOL="${RED}❌ FAIL${NC}"
                    FAILED_TASKS=$((FAILED_TASKS + 1))
                    PASSED_TASKS=$((PASSED_TASKS - 1))
                    FAILED_LIST+=("$TASK_ID: Database verification failed (Neo4j empty)")
                fi
            fi
            ;;
    esac

    printf "%-8s %-35s %-15s %-15s %b%s\n" \
        "$TASK_ID" \
        "$DISPLAY_DESC" \
        "$REQUIRED" \
        "$ACTUAL" \
        "$STATUS_SYMBOL" \
        "$DB_STATUS"

done <<< "$TASKS"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Summary statistics
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                      SUMMARY                               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo -e "Total tasks checked:    ${TOTAL_TASKS}"
echo -e "Tasks passed:           ${GREEN}${PASSED_TASKS}${NC}"
echo -e "Tasks failed:           ${RED}${FAILED_TASKS}${NC}"
echo -e "Pass rate:              $(awk "BEGIN {printf \"%.1f%%\", ($PASSED_TASKS/$TOTAL_TASKS)*100}")"
echo ""

# Final decision
if [ $FAILED_TASKS -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ CHECKPOINT PASSED - ALL TASKS VERIFIED                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ CHECKPOINT FAILED - BLOCKING FORWARD PROGRESS          ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${RED}FAILED TASKS:${NC}"
    for failure in "${FAILED_LIST[@]}"; do
        echo -e "${RED}  • $failure${NC}"
    done
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}ACTION REQUIRED:${NC}"
    echo -e "1. Review failed tasks listed above"
    echo -e "2. Re-execute failed tasks with proper verification"
    echo -e "3. Ensure database state matches task requirements"
    echo -e "4. Run verification scripts (pre_task_check.sh, post_task_verify.sh)"
    echo -e "5. Re-run this checkpoint gate to verify completion"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
fi
