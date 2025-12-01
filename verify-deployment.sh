#!/bin/bash

# OpenSPG Deployment Verification Script
# Checks that all services are running and healthy

set -e

echo "======================================"
echo "OpenSPG Deployment Verification"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_service() {
    local service=$1
    local port=$2
    echo -n "Checking $service on port $port... "
    
    if docker-compose ps | grep -q "$service.*Up"; then
        echo -e "${GREEN}✓ Running${NC}"
        return 0
    else
        echo -e "${RED}✗ Not running${NC}"
        return 1
    fi
}

check_health() {
    local container=$1
    echo -n "Checking $container health... "
    
    health=$(docker inspect --format='{{.State.Health.Status}}' $container 2>/dev/null || echo "none")
    
    if [ "$health" = "healthy" ]; then
        echo -e "${GREEN}✓ Healthy${NC}"
        return 0
    elif [ "$health" = "starting" ]; then
        echo -e "${YELLOW}⏳ Starting...${NC}"
        return 1
    elif [ "$health" = "none" ]; then
        echo -e "${YELLOW}⚠ No health check${NC}"
        return 0
    else
        echo -e "${RED}✗ Unhealthy${NC}"
        return 1
    fi
}

test_connection() {
    local name=$1
    local url=$2
    echo -n "Testing $name connection... "
    
    if curl -s -f "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Connected${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed${NC}"
        return 1
    fi
}

# Check Docker is running
echo "Checking Docker..."
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Check services
echo "Checking Services:"
check_service "openspg-server" "8887"
check_service "openspg-mysql" "3306"
check_service "openspg-neo4j" "7474/7687"
check_service "openspg-minio" "9000/9001"
echo ""

# Check health
echo "Checking Health:"
check_health "openspg-server"
check_health "openspg-mysql"
check_health "openspg-neo4j"
check_health "openspg-minio"
echo ""

# Test connections
echo "Testing Connections:"
test_connection "MinIO" "http://localhost:9000/minio/health/live"
test_connection "Neo4j" "http://localhost:7474"
echo ""

# Test Neo4j with cypher-shell
echo -n "Testing Neo4j query... "
if docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Query successful${NC}"
else
    echo -e "${RED}✗ Query failed${NC}"
fi

# Test MySQL
echo -n "Testing MySQL query... "
if docker exec openspg-mysql mysql -u root -popenspg -e "SELECT 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Query successful${NC}"
else
    echo -e "${RED}✗ Query failed${NC}"
fi
echo ""

# Show volume info
echo "Data Volumes:"
docker volume ls | grep openspg | while read driver name; do
    size=$(docker run --rm -v $name:/data alpine du -sh /data 2>/dev/null | cut -f1)
    echo "  - $name: $size"
done
echo ""

# Show resource usage
echo "Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep -E "CONTAINER|openspg"
echo ""

echo "======================================"
echo -e "${GREEN}Verification Complete!${NC}"
echo "======================================"
echo ""
echo "Access Points:"
echo "  - OpenSPG UI:   http://localhost:8887"
echo "  - Neo4j Browser: http://localhost:7474"
echo "  - MinIO Console: http://localhost:9001"
echo ""
echo "Credentials:"
echo "  - OpenSPG: openspg / openspg@kag"
echo "  - Neo4j:   neo4j / neo4j@openspg"
echo "  - MySQL:   root / openspg"
echo "  - MinIO:   minio / minio@openspg"
echo ""
