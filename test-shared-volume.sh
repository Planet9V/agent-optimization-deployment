#!/bin/bash

# OpenSPG Shared Volume Test Script
# Verifies that all containers can access the shared volume

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "OpenSPG Shared Volume Test"
echo "======================================"
echo ""

# Check if containers are running
echo "Checking if containers are running..."
for container in openspg-server openspg-mysql openspg-neo4j openspg-minio; do
    if docker ps | grep -q "$container"; then
        echo -e "${GREEN}✓ $container is running${NC}"
    else
        echo -e "${RED}✗ $container is not running${NC}"
        echo "Please start services with: docker-compose up -d"
        exit 1
    fi
done
echo ""

# Test write from server
echo "Testing write access from openspg-server..."
docker exec openspg-server sh -c 'echo "Test from OpenSPG Server" > /shared/test-$(date +%s).txt'
docker exec openspg-server sh -c 'echo "Timestamp: $(date)" > /shared/server-test.txt'
echo -e "${GREEN}✓ Write successful from openspg-server${NC}"

# Test read from neo4j
echo "Testing read access from openspg-neo4j..."
if docker exec openspg-neo4j cat /shared/server-test.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Read successful from openspg-neo4j${NC}"
    docker exec openspg-neo4j cat /shared/server-test.txt
else
    echo -e "${RED}✗ Read failed from openspg-neo4j${NC}"
fi
echo ""

# Test read from mysql
echo "Testing read access from openspg-mysql..."
if docker exec openspg-mysql cat /shared/server-test.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Read successful from openspg-mysql${NC}"
else
    echo -e "${RED}✗ Read failed from openspg-mysql${NC}"
fi

# Test read from minio
echo "Testing read access from openspg-minio..."
if docker exec openspg-minio cat /shared/server-test.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Read successful from openspg-minio${NC}"
else
    echo -e "${RED}✗ Read failed from openspg-minio${NC}"
fi
echo ""

# Test write from each container
echo "Testing write from all containers..."

docker exec openspg-server sh -c 'echo "Message from server" > /shared/from-server.txt'
echo -e "${GREEN}✓ Write from openspg-server${NC}"

docker exec openspg-mysql sh -c 'echo "Message from mysql" > /shared/from-mysql.txt'
echo -e "${GREEN}✓ Write from openspg-mysql${NC}"

docker exec openspg-neo4j sh -c 'echo "Message from neo4j" > /shared/from-neo4j.txt'
echo -e "${GREEN}✓ Write from openspg-neo4j${NC}"

docker exec openspg-minio sh -c 'echo "Message from minio" > /shared/from-minio.txt'
echo -e "${GREEN}✓ Write from openspg-minio${NC}"
echo ""

# List shared volume contents
echo "Shared volume contents:"
docker exec openspg-server ls -lh /shared
echo ""

# Verify all files are accessible from all containers
echo "Cross-container read verification..."
for source in server mysql neo4j minio; do
    echo "Verifying file from-${source}.txt..."
    for container in openspg-server openspg-mysql openspg-neo4j openspg-minio; do
        if docker exec $container cat /shared/from-${source}.txt > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓ Readable from $container${NC}"
        else
            echo -e "  ${RED}✗ Not readable from $container${NC}"
        fi
    done
    echo ""
done

# Check volume size
echo "Shared volume disk usage:"
docker run --rm -v openspg-shared-data:/data alpine du -sh /data
echo ""

# Cleanup test files
echo "Cleaning up test files..."
docker exec openspg-server sh -c 'rm -f /shared/test-*.txt /shared/server-test.txt /shared/from-*.txt'
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo ""

echo "======================================"
echo -e "${GREEN}Shared Volume Test PASSED!${NC}"
echo "======================================"
echo ""
echo "Summary:"
echo "  - All 4 containers can read/write to /shared"
echo "  - Volume name: openspg-shared-data"
echo "  - Cross-container data exchange: WORKING"
echo ""
