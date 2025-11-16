#!/bin/bash

##############################################################################
# GAP-006 Integration Test Setup Verification
# Validates test environment before running tests
##############################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   GAP-006 Integration Test Setup Verification     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

ERRORS=0

# Function to check command
check_command() {
  local cmd=$1
  local name=$2

  if command -v "$cmd" >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} $name is installed"
    return 0
  else
    echo -e "${RED}✗${NC} $name is NOT installed"
    ERRORS=$((ERRORS + 1))
    return 1
  fi
}

# Function to check service
check_service() {
  local cmd=$1
  local name=$2
  local fix_hint=$3

  if eval "$cmd" >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} $name is accessible"
    return 0
  else
    echo -e "${RED}✗${NC} $name is NOT accessible"
    echo -e "${YELLOW}  → Fix: $fix_hint${NC}"
    ERRORS=$((ERRORS + 1))
    return 1
  fi
}

# Check Prerequisites
echo -e "${YELLOW}[1/5] Checking System Prerequisites${NC}"
echo ""

check_command "node" "Node.js"
if command -v node >/dev/null 2>&1; then
  NODE_VERSION=$(node --version)
  echo -e "      Version: $NODE_VERSION"
fi

check_command "npm" "npm"
if command -v npm >/dev/null 2>&1; then
  NPM_VERSION=$(npm --version)
  echo -e "      Version: $NPM_VERSION"
fi

check_command "psql" "PostgreSQL client"
check_command "redis-cli" "Redis client"
check_command "curl" "curl"

echo ""

# Check Services
echo -e "${YELLOW}[2/5] Checking Service Connectivity${NC}"
echo ""

# PostgreSQL
POSTGRES_HOST=${POSTGRES_HOST:-localhost}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}

check_service \
  "PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d postgres -c 'SELECT 1'" \
  "PostgreSQL ($POSTGRES_HOST:$POSTGRES_PORT)" \
  "docker run -d --name gap006-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16-alpine"

# Redis
REDIS_HOST=${REDIS_HOST:-localhost}
REDIS_PORT=${REDIS_PORT:-6379}

check_service \
  "redis-cli -h $REDIS_HOST -p $REDIS_PORT ping" \
  "Redis ($REDIS_HOST:$REDIS_PORT)" \
  "docker run -d --name gap006-redis -p 6379:6379 redis:7-alpine"

# Qdrant
QDRANT_URL=${QDRANT_URL:-http://localhost:6333}

check_service \
  "curl -s $QDRANT_URL/collections" \
  "Qdrant ($QDRANT_URL)" \
  "docker run -d --name gap006-qdrant -p 6333:6333 qdrant/qdrant:latest"

echo ""

# Check Environment Variables
echo -e "${YELLOW}[3/5] Checking Environment Variables${NC}"
echo ""

ENV_VARS=(
  "POSTGRES_HOST:${POSTGRES_HOST}"
  "POSTGRES_PORT:${POSTGRES_PORT}"
  "POSTGRES_USER:${POSTGRES_USER}"
  "POSTGRES_DB:${POSTGRES_DB:-gap006_test}"
  "REDIS_HOST:${REDIS_HOST}"
  "REDIS_PORT:${REDIS_PORT}"
  "REDIS_DB:${REDIS_DB:-1}"
  "QDRANT_URL:${QDRANT_URL}"
)

for var_info in "${ENV_VARS[@]}"; do
  IFS=':' read -r var_name var_value <<< "$var_info"
  if [ -n "$var_value" ]; then
    echo -e "${GREEN}✓${NC} $var_name = $var_value"
  else
    echo -e "${YELLOW}⚠${NC} $var_name is not set (using default)"
  fi
done

echo ""

# Check Test Files
echo -e "${YELLOW}[4/5] Checking Test Files${NC}"
echo ""

TEST_FILES=(
  "setup.ts"
  "job-lifecycle.test.ts"
  "worker-health.test.ts"
  "state-persistence.test.ts"
  "jest.config.js"
  "jest.setup.ts"
  "run-tests.sh"
  "README.md"
)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for file in "${TEST_FILES[@]}"; do
  if [ -f "$SCRIPT_DIR/$file" ]; then
    FILE_SIZE=$(wc -l < "$SCRIPT_DIR/$file")
    echo -e "${GREEN}✓${NC} $file ($FILE_SIZE lines)"
  else
    echo -e "${RED}✗${NC} $file is MISSING"
    ERRORS=$((ERRORS + 1))
  fi
done

echo ""

# Check Dependencies
echo -e "${YELLOW}[5/5] Checking Node Dependencies${NC}"
echo ""

PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if [ -f "$PROJECT_ROOT/package.json" ]; then
  echo -e "${GREEN}✓${NC} package.json found"

  # Check for required dependencies
  REQUIRED_DEPS=("jest" "ts-jest" "@types/jest" "pg" "ioredis" "@qdrant/js-client-rest")

  for dep in "${REQUIRED_DEPS[@]}"; do
    if grep -q "\"$dep\"" "$PROJECT_ROOT/package.json"; then
      echo -e "${GREEN}✓${NC} $dep declared in package.json"
    else
      echo -e "${YELLOW}⚠${NC} $dep NOT found in package.json"
    fi
  done
else
  echo -e "${RED}✗${NC} package.json NOT found in $PROJECT_ROOT"
  ERRORS=$((ERRORS + 1))
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"

# Summary
if [ $ERRORS -eq 0 ]; then
  echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
  echo -e "${GREEN}║       ALL CHECKS PASSED - READY TO TEST ✓          ║${NC}"
  echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo -e "${BLUE}Run tests with:${NC}"
  echo -e "  ${YELLOW}./run-tests.sh${NC}"
  echo ""
  exit 0
else
  echo -e "${RED}╔════════════════════════════════════════════════════╗${NC}"
  echo -e "${RED}║       SETUP INCOMPLETE - $ERRORS ERRORS FOUND          ║${NC}"
  echo -e "${RED}╚════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo -e "${BLUE}Fix the errors above before running tests${NC}"
  echo ""
  exit 1
fi
