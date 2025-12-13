#!/bin/bash
################################################################################
# AEON SYSTEM HEALTH CHECK - Complete Diagnostics
#
# Tests all Docker containers, APIs, databases, and key services
# Use this to verify system is ready for development
#
# Usage: ./SYSTEM_HEALTH_CHECK.sh
################################################################################

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "AEON SYSTEM HEALTH CHECK - $(date)"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

PASS=0
FAIL=0

check_service() {
    local name=$1
    local test_command=$2
    local expected=$3

    echo -n "Testing $name... "
    result=$(eval "$test_command" 2>/dev/null)

    if echo "$result" | grep -q "$expected"; then
        echo "✅ PASS"
        ((PASS++))
        return 0
    else
        echo "❌ FAIL"
        ((FAIL++))
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. DOCKER CONTAINERS (9 total)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

check_service "ner11-gold-api (NER + Phase B)" "docker ps --filter name=ner11-gold-api --format '{{.Status}}'" "Up"
check_service "aeon-saas-dev (Next.js UI)" "docker ps --filter name=aeon-saas-dev --format '{{.Status}}'" "Up"
check_service "openspg-neo4j (Graph DB)" "docker ps --filter name=openspg-neo4j --format '{{.Status}}'" "Up"
check_service "openspg-qdrant (Vector DB)" "docker ps --filter name=openspg-qdrant --format '{{.Status}}'" "Up"
check_service "openspg-server (Reasoning)" "docker ps --filter name=openspg-server --format '{{.Status}}'" "Up"
check_service "aeon-postgres-dev (App DB)" "docker ps --filter name=aeon-postgres-dev --format '{{.Status}}'" "Up"
check_service "openspg-mysql (Metadata)" "docker ps --filter name=openspg-mysql --format '{{.Status}}'" "Up"
check_service "openspg-minio (Storage)" "docker ps --filter name=openspg-minio --format '{{.Status}}'" "Up"
check_service "openspg-redis (Cache)" "docker ps --filter name=openspg-redis --format '{{.Status}}'" "Up"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. API ENDPOINTS (10 critical)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

check_service "NER API Health" "curl -s http://localhost:8000/health" "healthy"
check_service "NER API Info" "curl -s http://localhost:8000/info" "version"
check_service "Next.js Health" "curl -s http://localhost:3000/api/health" "healthy"
check_service "Threat Intel Dashboard" "curl -s http://localhost:8000/api/v2/threat-intel/dashboard/summary -H 'x-customer-id: dev'" "total"
check_service "Risk Dashboard" "curl -s http://localhost:8000/api/v2/risk/dashboard -H 'x-customer-id: dev'" "risk"
check_service "SBOM Dashboard" "curl -s http://localhost:8000/api/v2/sbom/dashboard/summary -H 'x-customer-id: dev'" "sbom"
check_service "Equipment Dashboard" "curl -s http://localhost:8000/api/v2/equipment/dashboard/summary -H 'x-customer-id: dev'" "equipment"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. DATABASE CONNECTIONS (4 databases)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

check_service "Neo4j Bolt (7687)" "docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' -d neo4j 'RETURN 1'" "1"
check_service "Neo4j HTTP (7474)" "curl -s http://localhost:7474" "Neo4j"
check_service "Qdrant REST (6333)" "curl -s http://localhost:6333/collections" "collections"
check_service "PostgreSQL (5432)" "docker exec aeon-postgres-dev pg_isready" "accepting"
check_service "MySQL (3306)" "docker exec openspg-mysql mysqladmin ping -h localhost" "alive"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. DATA VERIFICATION (5 key datasets)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

check_service "Neo4j has nodes (>1M)" "docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' -d neo4j 'MATCH (n) RETURN count(n) as c LIMIT 1' --format plain | grep -oP '\d+'" "1[0-9]{6}"
check_service "CVE nodes (>300K)" "docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' -d neo4j 'MATCH (c:CVE) RETURN count(c) as c LIMIT 1' --format plain | grep -oP '\d+'" "[3-9][0-9]{5}"
check_service "Qdrant collections (>5)" "curl -s http://localhost:6333/collections | grep -o '\"name\"' | wc -l" "[5-9]"
check_service "Qdrant entities (>100K)" "curl -s 'http://localhost:6333/collections/ner11_entities_hierarchical' | grep -oP '\"points_count\":\K[0-9]+'" "[1-9][0-9]{5}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. PERFORMANCE CHECK (response times)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -n "NER API response time... "
time=$(curl -s -w "%{time_total}" -o /dev/null -X POST http://localhost:8000/ner -H "Content-Type: application/json" -d '{"text":"test"}')
if (( $(echo "$time < 1.0" | bc -l) )); then
    echo "✅ ${time}s (good)"
    ((PASS++))
else
    echo "⚠️  ${time}s (slow)"
    ((FAIL++))
fi

echo -n "Neo4j query response time... "
time=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:7474/browser/)
if (( $(echo "$time < 2.0" | bc -l) )); then
    echo "✅ ${time}s (good)"
    ((PASS++))
else
    echo "⚠️  ${time}s (slow)"
    ((FAIL++))
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "SUMMARY"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "✅ PASSED: $PASS checks"
echo "❌ FAILED: $FAIL checks"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 ALL SYSTEMS OPERATIONAL - Ready for development"
    exit 0
elif [ $FAIL -lt 5 ]; then
    echo "⚠️  MOSTLY OPERATIONAL - Some issues need attention"
    exit 1
else
    echo "🚨 CRITICAL ISSUES - System not ready"
    exit 2
fi
