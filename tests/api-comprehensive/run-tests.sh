#!/bin/bash

# Comprehensive API Testing Script
# Tests all 232 APIs after middleware fixes

set -e

echo "🚀 Comprehensive API Testing Framework"
echo "========================================"

# Configuration
BASE_URL="${API_BASE_URL:-http://localhost:3000}"
RESULTS_DIR="$(dirname "$0")/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "\n${YELLOW}Configuration:${NC}"
echo "  Base URL: $BASE_URL"
echo "  Results Dir: $RESULTS_DIR"
echo "  Timestamp: $TIMESTAMP"

# Create results directory
mkdir -p "$RESULTS_DIR"

# Function to check if API is available
check_api_availability() {
    echo -e "\n${YELLOW}Checking API availability...${NC}"

    if curl -s --max-time 5 "$BASE_URL/api/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API is available${NC}"
        return 0
    else
        echo -e "${RED}❌ API is not available at $BASE_URL${NC}"
        echo "Please ensure:"
        echo "  1. The container is running"
        echo "  2. Middleware fixes have been applied"
        echo "  3. The API is accessible at $BASE_URL"
        return 1
    fi
}

# Function to run all tests
run_all_tests() {
    echo -e "\n${YELLOW}Running comprehensive API tests...${NC}"

    # Compile TypeScript
    echo "Compiling TypeScript..."
    npx ts-node test-all-apis.ts

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ All tests completed${NC}"
    else
        echo -e "${RED}❌ Tests failed${NC}"
        exit 1
    fi
}

# Function to run category-specific tests
run_category_test() {
    local category=$1
    echo -e "\n${YELLOW}Running $category tests...${NC}"

    npx ts-node test-all-apis.ts "$category"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $category tests completed${NC}"
    else
        echo -e "${RED}❌ $category tests failed${NC}"
        exit 1
    fi
}

# Function to display help
show_help() {
    echo "Usage: ./run-tests.sh [OPTION] [CATEGORY]"
    echo ""
    echo "Options:"
    echo "  --all               Test all 232 APIs (default)"
    echo "  --category <name>   Test specific category only"
    echo "  --check             Check API availability only"
    echo "  --help              Display this help message"
    echo ""
    echo "Categories:"
    echo "  ner, sbom, vendor_equipment, threat_intel, risk_scoring,"
    echo "  remediation, compliance, scanning, alerts, economic,"
    echo "  demographics, prioritization, nextjs, openspg"
    echo ""
    echo "Examples:"
    echo "  ./run-tests.sh                    # Test all APIs"
    echo "  ./run-tests.sh --category sbom    # Test SBOM APIs only"
    echo "  ./run-tests.sh --check            # Check API availability"
}

# Main execution
main() {
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --check)
            check_api_availability
            exit $?
            ;;
        --category)
            if [ -z "$2" ]; then
                echo -e "${RED}Error: Category name required${NC}"
                show_help
                exit 1
            fi
            check_api_availability || exit 1
            run_category_test "$2"
            ;;
        --all|"")
            check_api_availability || exit 1
            run_all_tests
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
