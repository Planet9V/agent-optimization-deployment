#!/bin/bash
# COMMUNICATIONS Sector Validation Queries

echo "=== COMMUNICATIONS SECTOR VALIDATION ==="
echo ""

echo "1. Total COMMUNICATIONS nodes:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n) WHERE 'COMMUNICATIONS' IN labels(n) RETURN count(n) as total;"
echo ""

echo "2. CommunicationsDevice count:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n:CommunicationsDevice) RETURN count(n) as devices;"
echo ""

echo "3. NetworkMeasurement count:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n:NetworkMeasurement) RETURN count(n) as measurements;"
echo ""

echo "4. CommunicationsProperty count:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n:CommunicationsProperty) RETURN count(n) as properties;"
echo ""

echo "5. RoutingProcess count:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n:RoutingProcess) RETURN count(n) as processes;"
echo ""

echo "6. Relationship type breakdown:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n)-[r]->(m) WHERE 'COMMUNICATIONS' IN labels(n) WITH type(r) as rel_type, count(*) as cnt RETURN rel_type, cnt ORDER BY cnt DESC;"
echo ""

echo "7. Subsector distribution:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n) WHERE 'COMMUNICATIONS' IN labels(n) AND exists(n.subsector) WITH n.subsector as subsector, count(*) as cnt RETURN subsector, cnt ORDER BY cnt DESC;"
echo ""

echo "8. Total relationships:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n)-[r]->(m) WHERE 'COMMUNICATIONS' IN labels(n) RETURN count(r) as total_rels;"
