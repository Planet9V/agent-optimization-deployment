#!/bin/bash
RESULTS="test_results_$(date +%Y%m%d_%H%M%S).md"
echo "# NEO4J TEST RESULTS" > "$RESULTS"
echo "" >> "$RESULTS"
echo "Timestamp: $(date)" >> "$RESULTS"
echo "" >> "$RESULTS"
echo "| Test | Description | Result | Status |" >> "$RESULTS"
echo "|------|-------------|--------|--------|" >> "$RESULTS"

# Test 1
RESULT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" --format plain "MATCH (n) RETURN count(n);" 2>&1 | tail -1)
if [[ $RESULT =~ ^[0-9]+$ ]] && [[ $RESULT -gt 0 ]]; then
  echo "| T001 | Database populated | $RESULT nodes | PASS |" >> "$RESULTS"
  ((PASSED++))
else
  echo "| T001 | Database populated | ERROR | FAIL |" >> "$RESULTS"
  ((FAILED++))
fi

# Test 2
RESULT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" --format plain "MATCH (c:SeldonCrisis) RETURN count(c);" 2>&1 | tail -1)
if [[ "$RESULT" == "3" ]]; then
  echo "| T002 | Seldon Crises exist | 3 crises | PASS |" >> "$RESULTS"
  ((PASSED++))
else
  echo "| T002 | Seldon Crises exist | $RESULT | FAIL |" >> "$RESULTS"
  ((FAILED++))
fi

# Test 3-5: Individual crises
for crisis in "Great Resignation Cascade" "Supply Chain Collapse" "Medical Device Pandemic"; do
  RESULT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" --format plain "MATCH (c:SeldonCrisis {name: '$crisis'}) RETURN count(c);" 2>&1 | tail -1)
  if [[ "$RESULT" == "1" ]]; then
    echo "| Crisis | $crisis | Found | PASS |" >> "$RESULTS"
    ((PASSED++))
  else
    echo "| Crisis | $crisis | Not found | FAIL |" >> "$RESULTS"
    ((FAILED++))
  fi
done

TOTAL=$((PASSED + FAILED))
PASS_RATE=$(awk "BEGIN {printf \"%.1f\", ($PASSED/$TOTAL)*100}")

echo "" >> "$RESULTS"
echo "## Summary" >> "$RESULTS"
echo "- Total: $TOTAL" >> "$RESULTS"
echo "- Passed: $PASSED" >> "$RESULTS"
echo "- Failed: $FAILED" >> "$RESULTS"
echo "- Pass Rate: ${PASS_RATE}%" >> "$RESULTS"

cat "$RESULTS"
