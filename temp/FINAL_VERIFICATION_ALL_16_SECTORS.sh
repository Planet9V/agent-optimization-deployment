#!/bin/bash
echo "=== FINAL VERIFICATION - ALL 16 CISA SECTORS ==="
echo "Timestamp: $(date)"
echo ""

echo "Querying all sectors..."
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN [
  'WATER','ENERGY','COMMUNICATIONS','EMERGENCY_SERVICES',
  'FOOD_AGRICULTURE','FINANCIAL_SERVICES','INFORMATION_TECHNOLOGY',
  'GOVERNMENT_FACILITIES','Healthcare','CHEMICAL','COMMERCIAL_FACILITIES',
  'Transportation','SECTOR_DEFENSE_INDUSTRIAL_BASE'
])
WITH CASE
  WHEN 'WATER' IN labels(n) THEN 'WATER'
  WHEN 'ENERGY' IN labels(n) THEN 'ENERGY'
  WHEN 'COMMUNICATIONS' IN labels(n) THEN 'COMMUNICATIONS'
  WHEN 'EMERGENCY_SERVICES' IN labels(n) THEN 'EMERGENCY_SERVICES'
  WHEN 'FOOD_AGRICULTURE' IN labels(n) THEN 'FOOD_AGRICULTURE'
  WHEN 'FINANCIAL_SERVICES' IN labels(n) THEN 'FINANCIAL_SERVICES'
  WHEN 'INFORMATION_TECHNOLOGY' IN labels(n) THEN 'INFORMATION_TECHNOLOGY'
  WHEN 'GOVERNMENT_FACILITIES' IN labels(n) THEN 'GOVERNMENT_FACILITIES'
  WHEN 'Healthcare' IN labels(n) THEN 'HEALTHCARE'
  WHEN 'CHEMICAL' IN labels(n) THEN 'CHEMICAL'
  WHEN 'COMMERCIAL_FACILITIES' IN labels(n) THEN 'COMMERCIAL_FACILITIES'
  WHEN 'Transportation' IN labels(n) THEN 'TRANSPORTATION'
  WHEN 'SECTOR_DEFENSE_INDUSTRIAL_BASE' IN labels(n) THEN 'DEFENSE_INDUSTRIAL_BASE'
  ELSE 'OTHER'
END as sector, count(n) as nodes
RETURN sector, nodes ORDER BY sector;
" | tee temp/final_verification_results.txt

echo ""
echo "Checking for Nuclear and Dams (different label patterns)..."
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "
MATCH (n) WHERE any(label IN labels(n) WHERE label CONTAINS 'Nuclear')
RETURN count(DISTINCT n) as NUCLEAR_nodes;
"

docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "
MATCH (n) WHERE any(label IN labels(n) WHERE label CONTAINS 'Dams')
RETURN count(DISTINCT n) as DAMS_nodes;
"

echo ""
echo "Critical Manufacturing verification..."
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "
MATCH (n) WHERE any(label IN labels(n) WHERE label CONTAINS 'Manufacturing')
RETURN count(DISTINCT n) as CRITICAL_MANUFACTURING_nodes;
"

echo ""
echo "=== VERIFICATION COMPLETE ==="
