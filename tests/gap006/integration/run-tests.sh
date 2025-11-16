#!/bin/bash

##############################################################################
# GAP-006 Integration Test Runner
# Executes integration tests with proper environment setup and cleanup
##############################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     GAP-006 Integration Test Suite Runner         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"

command -v node >/dev/null 2>&1 || {
  echo -e "${RED}Error: Node.js is required but not installed.${NC}" >&2
  exit 1
}

command -v npm >/dev/null 2>&1 || {
  echo -e "${RED}Error: npm is required but not installed.${NC}" >&2
  exit 1
}

command -v psql >/dev/null 2>&1 || {
  echo -e "${RED}Error: PostgreSQL client is required but not installed.${NC}" >&2
  exit 1
}

command -v redis-cli >/dev/null 2>&1 || {
  echo -e "${RED}Error: Redis client is required but not installed.${NC}" >&2
  exit 1
}

echo -e "${GREEN}✓ All prerequisites satisfied${NC}"

# Set up test environment variables
echo -e "${YELLOW}[2/6] Setting up test environment...${NC}"

export NODE_ENV=test
export POSTGRES_HOST=${POSTGRES_HOST:-localhost}
export POSTGRES_PORT=${POSTGRES_PORT:-5432}
export POSTGRES_DB=${POSTGRES_DB:-gap006_test}
export POSTGRES_USER=${POSTGRES_USER:-postgres}
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
export REDIS_HOST=${REDIS_HOST:-localhost}
export REDIS_PORT=${REDIS_PORT:-6379}
export REDIS_DB=${REDIS_DB:-1}
export QDRANT_URL=${QDRANT_URL:-http://localhost:6333}

echo -e "${GREEN}✓ Environment configured${NC}"

# Check database connectivity
echo -e "${YELLOW}[3/6] Verifying database connectivity...${NC}"

if ! PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d postgres -c "SELECT 1" >/dev/null 2>&1; then
  echo -e "${RED}Error: Cannot connect to PostgreSQL${NC}" >&2
  echo -e "${YELLOW}Starting PostgreSQL with Docker...${NC}"
  docker run -d \
    --name gap006-test-postgres \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -p $POSTGRES_PORT:5432 \
    postgres:16-alpine
  sleep 5
fi

if ! redis-cli -h $REDIS_HOST -p $REDIS_PORT ping >/dev/null 2>&1; then
  echo -e "${RED}Error: Cannot connect to Redis${NC}" >&2
  echo -e "${YELLOW}Starting Redis with Docker...${NC}"
  docker run -d \
    --name gap006-test-redis \
    -p $REDIS_PORT:6379 \
    redis:7-alpine
  sleep 2
fi

# Check Qdrant
if ! curl -s "$QDRANT_URL/collections" >/dev/null 2>&1; then
  echo -e "${RED}Warning: Cannot connect to Qdrant at $QDRANT_URL${NC}" >&2
  echo -e "${YELLOW}Starting Qdrant with Docker...${NC}"
  docker run -d \
    --name gap006-test-qdrant \
    -p 6333:6333 \
    qdrant/qdrant:latest
  sleep 5
fi

echo -e "${GREEN}✓ Database services ready${NC}"

# Create test database if needed
echo -e "${YELLOW}[4/6] Preparing test database...${NC}"

PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB;" >/dev/null 2>&1
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d postgres -c "CREATE DATABASE $POSTGRES_DB;" >/dev/null 2>&1

echo -e "${GREEN}✓ Test database prepared${NC}"

# Install dependencies
echo -e "${YELLOW}[5/6] Installing test dependencies...${NC}"

cd "$PROJECT_ROOT"
npm install --silent >/dev/null 2>&1

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Run tests
echo -e "${YELLOW}[6/6] Running integration tests...${NC}"
echo ""

TEST_FILTER=${1:-""}

if [ -n "$TEST_FILTER" ]; then
  echo -e "${YELLOW}Running filtered tests: $TEST_FILTER${NC}"
  npx jest tests/gap006/integration --testPathPattern="$TEST_FILTER" --verbose --coverage
else
  echo -e "${YELLOW}Running all integration tests${NC}"
  npx jest tests/gap006/integration --verbose --coverage
fi

TEST_EXIT_CODE=$?

# Cleanup
echo ""
echo -e "${YELLOW}Cleaning up test environment...${NC}"

# Optional: Remove Docker containers if we started them
if [ "${CLEANUP_DOCKER:-false}" = "true" ]; then
  docker rm -f gap006-test-postgres gap006-test-redis gap006-test-qdrant 2>/dev/null || true
fi

echo -e "${GREEN}✓ Cleanup complete${NC}"
echo ""

# Report results
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
  echo -e "${GREEN}║          ALL INTEGRATION TESTS PASSED ✓            ║${NC}"
  echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
else
  echo -e "${RED}╔════════════════════════════════════════════════════╗${NC}"
  echo -e "${RED}║          INTEGRATION TESTS FAILED ✗                ║${NC}"
  echo -e "${RED}╚════════════════════════════════════════════════════╝${NC}"
fi

exit $TEST_EXIT_CODE
