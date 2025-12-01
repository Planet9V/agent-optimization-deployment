#!/bin/bash

# ============================================================================
# QDRANT STARTUP SCRIPT WITH VALIDATION
# ============================================================================
# Purpose: Automated startup of Qdrant with prerequisite checks
# Created: 2025-10-31
# Usage: ./start-qdrant.sh
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  QDRANT VECTOR DATABASE STARTUP VALIDATOR                 ║${NC}"
echo -e "${BLUE}║  OpenSPG Cybersecurity Platform Integration                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# PREREQUISITE CHECKS
# ============================================================================

echo -e "${YELLOW}[1/7] Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker installed$(NC}: $(docker --version)"
echo ""

echo -e "${YELLOW}[2/7] Checking Docker Compose installation...${NC}"
if ! docker-compose --version &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose installed:${NC} $(docker-compose --version)"
echo ""

echo -e "${YELLOW}[3/7] Checking OpenSPG network existence...${NC}"
if ! docker network inspect openspg-network &> /dev/null; then
    echo -e "${RED}✗ OpenSPG network not found.${NC}"
    echo -e "${YELLOW}  Creating openspg-network...${NC}"
    docker network create openspg-network
    echo -e "${GREEN}✓ Network created successfully${NC}"
else
    echo -e "${GREEN}✓ OpenSPG network exists${NC}"
    CONTAINER_COUNT=$(docker network inspect openspg-network --format '{{len .Containers}}')
    echo -e "  Connected containers: ${CONTAINER_COUNT}"
fi
echo ""

echo -e "${YELLOW}[4/7] Checking OpenSPG shared volume...${NC}"
if ! docker volume inspect openspg-shared-data &> /dev/null; then
    echo -e "${YELLOW}  Shared volume not found. Creating...${NC}"
    docker volume create openspg-shared-data
    echo -e "${GREEN}✓ Shared volume created${NC}"
else
    echo -e "${GREEN}✓ Shared volume exists${NC}"
fi
echo ""

echo -e "${YELLOW}[5/7] Checking .env.qdrant configuration file...${NC}"
if [ ! -f .env.qdrant ]; then
    echo -e "${RED}✗ .env.qdrant not found${NC}"
    echo -e "${YELLOW}  Please create .env.qdrant with QDRANT_API_KEY${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Configuration file exists${NC}"
echo ""

echo -e "${YELLOW}[6/7] Checking backup directory...${NC}"
if [ ! -d "$HOME/qdrant-backups" ]; then
    echo -e "${YELLOW}  Creating backup directory...${NC}"
    mkdir -p "$HOME/qdrant-backups"/{snapshots,exports,configs}
    echo -e "${GREEN}✓ Backup directory created${NC}"
else
    echo -e "${GREEN}✓ Backup directory exists${NC}"
fi
echo ""

echo -e "${YELLOW}[7/7] Checking for existing Qdrant containers...${NC}"
if docker ps -a --format '{{.Names}}' | grep -q '^openspg-qdrant$'; then
    CONTAINER_STATUS=$(docker inspect --format='{{.State.Status}}' openspg-qdrant)
    if [ "$CONTAINER_STATUS" == "running" ]; then
        echo -e "${YELLOW}  Qdrant container already running${NC}"
        echo -e "${BLUE}  Use 'docker-compose -f docker-compose.qdrant.yml restart' to restart${NC}"
        exit 0
    else
        echo -e "${YELLOW}  Removing stopped Qdrant container...${NC}"
        docker rm openspg-qdrant
    fi
fi
echo -e "${GREEN}✓ No conflicting containers${NC}"
echo ""

# ============================================================================
# START QDRANT
# ============================================================================

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE} Starting Qdrant Vector Database...${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

docker-compose -f docker-compose.qdrant.yml up -d

echo ""
echo -e "${YELLOW}Waiting for Qdrant to become healthy (max 60 seconds)...${NC}"

# Wait for health check
TIMEOUT=60
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
    if docker inspect --format='{{.State.Health.Status}}' openspg-qdrant 2>/dev/null | grep -q 'healthy'; then
        echo -e "${GREEN}✓ Qdrant is healthy!${NC}"
        break
    fi
    echo -n "."
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done

if [ $ELAPSED -ge $TIMEOUT ]; then
    echo -e "${RED}✗ Qdrant health check timeout${NC}"
    echo -e "${YELLOW}Check logs: docker-compose -f docker-compose.qdrant.yml logs${NC}"
    exit 1
fi

echo ""

# ============================================================================
# CONNECTIVITY TESTS
# ============================================================================

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE} Running Connectivity Tests...${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Testing API access from host...${NC}"
source .env.qdrant
if curl -s -H "api-key: $QDRANT_API_KEY" http://localhost:6333/health | grep -q 'ok'; then
    echo -e "${GREEN}✓ Host → Qdrant: SUCCESS${NC}"
else
    echo -e "${RED}✗ Host → Qdrant: FAILED${NC}"
fi
echo ""

echo -e "${YELLOW}Testing DNS resolution from OpenSPG containers...${NC}"
if docker ps --format '{{.Names}}' | grep -q 'openspg-server'; then
    if docker exec openspg-server ping -c 1 openspg-qdrant &> /dev/null; then
        echo -e "${GREEN}✓ DNS resolution: openspg-qdrant is reachable${NC}"
    else
        echo -e "${YELLOW}⚠ DNS resolution test failed (may not have ping installed)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ OpenSPG server not running, skipping DNS test${NC}"
fi
echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN} Qdrant Deployment Successful!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Access Information:${NC}"
echo -e "  • Web UI:      http://localhost:6333/dashboard"
echo -e "  • API:         http://localhost:6333"
echo -e "  • From OpenSPG containers: http://openspg-qdrant:6333"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo -e "  • View logs:   docker-compose -f docker-compose.qdrant.yml logs -f"
echo -e "  • Check status: docker-compose -f docker-compose.qdrant.yml ps"
echo -e "  • Stop Qdrant: docker-compose -f docker-compose.qdrant.yml down"
echo -e "  • Restart:     docker-compose -f docker-compose.qdrant.yml restart"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "  1. Initialize collections (Phase 1 of Qdrant integration)"
echo -e "  2. Index 34 markdown documentation files"
echo -e "  3. Test semantic search accuracy"
echo -e "  4. Integrate with 12-wave Neo4j implementation"
echo ""
echo -e "${GREEN}Ready for Option B execution!${NC}"
echo ""
