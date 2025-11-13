#!/bin/bash
# AgentDB Test Execution Script

set -e

echo "========================================"
echo "AgentDB Test Suite Execution"
echo "========================================"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
    fi
}

# Parse arguments
RUN_COVERAGE=false
RUN_INTEGRATION=false
RUN_WATCH=false
TEST_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage)
            RUN_COVERAGE=true
            shift
            ;;
        --integration)
            RUN_INTEGRATION=true
            shift
            ;;
        --watch)
            RUN_WATCH=true
            shift
            ;;
        --file)
            TEST_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--coverage] [--integration] [--watch] [--file <test-file>]"
            exit 1
            ;;
    esac
done

# Set environment variables
export NODE_ENV=test

if [ "$RUN_INTEGRATION" = true ]; then
    export TEST_INTEGRATION=true
    export QDRANT_URL=${QDRANT_URL:-http://localhost:6333}
    echo -e "${YELLOW}Integration tests enabled${NC}"
    echo "Qdrant URL: $QDRANT_URL"
    echo ""
fi

# Build Jest command
JEST_CMD="jest --config=tests/agentdb/jest.config.js"

if [ "$RUN_COVERAGE" = true ]; then
    JEST_CMD="$JEST_CMD --coverage"
fi

if [ "$RUN_WATCH" = true ]; then
    JEST_CMD="$JEST_CMD --watch"
fi

if [ -n "$TEST_FILE" ]; then
    JEST_CMD="$JEST_CMD tests/agentdb/$TEST_FILE"
else
    JEST_CMD="$JEST_CMD tests/agentdb"
fi

# Run tests
echo "Running command: $JEST_CMD"
echo ""

if eval $JEST_CMD; then
    print_status 0 "All tests passed"

    if [ "$RUN_COVERAGE" = true ]; then
        echo ""
        echo "========================================"
        echo "Coverage Report"
        echo "========================================"
        echo ""

        # Show coverage summary
        if [ -f tests/agentdb/coverage/coverage-summary.json ]; then
            echo "Coverage reports generated:"
            echo "  - HTML: tests/agentdb/coverage/index.html"
            echo "  - LCOV: tests/agentdb/coverage/lcov.info"
            echo "  - JSON: tests/agentdb/coverage/coverage-summary.json"
        fi
    fi

    if [ -d tests/agentdb/reports ]; then
        echo ""
        echo "Test reports generated:"
        echo "  - JUnit XML: tests/agentdb/reports/junit.xml"
        echo "  - HTML Report: tests/agentdb/reports/index.html"
    fi

    exit 0
else
    print_status 1 "Tests failed"
    exit 1
fi
