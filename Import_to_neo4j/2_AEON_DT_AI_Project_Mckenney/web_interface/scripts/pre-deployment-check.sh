#!/bin/bash

################################################################################
# Pre-Deployment Checklist Script
# File: pre-deployment-check.sh
# Created: 2025-11-15
# Purpose: Verify all prerequisites before deploying web interface
################################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_check() {
    echo -e "${YELLOW}[CHECK]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[✓ PASS]${NC} $1"
    ((CHECKS_PASSED++))
}

print_fail() {
    echo -e "${RED}[✗ FAIL]${NC} $1"
    ((CHECKS_FAILED++))
}

print_warn() {
    echo -e "${YELLOW}[⚠ WARN]${NC} $1"
    ((CHECKS_WARNING++))
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

################################################################################
# Check Functions
################################################################################

check_docker_installed() {
    print_check "Verifying Docker is installed..."
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d ' ' -f3 | cut -d ',' -f1)
        print_pass "Docker is installed (version: $DOCKER_VERSION)"
        return 0
    else
        print_fail "Docker is not installed"
        return 1
    fi
}

check_docker_running() {
    print_check "Verifying Docker daemon is running..."
    if docker info &> /dev/null; then
        print_pass "Docker daemon is running"
        return 0
    else
        print_fail "Docker daemon is not running"
        return 1
    fi
}

check_docker_network() {
    print_check "Verifying Docker network 'mckenney-network' exists..."
    if docker network inspect mckenney-network &> /dev/null; then
        print_pass "Docker network 'mckenney-network' exists"

        # Get network details
        NETWORK_DRIVER=$(docker network inspect mckenney-network --format '{{.Driver}}')
        NETWORK_SCOPE=$(docker network inspect mckenney-network --format '{{.Scope}}')
        print_info "Network driver: $NETWORK_DRIVER, Scope: $NETWORK_SCOPE"
        return 0
    else
        print_fail "Docker network 'mckenney-network' does not exist"
        print_info "Create it with: docker network create mckenney-network"
        return 1
    fi
}

check_required_services() {
    print_check "Verifying required services are running..."

    REQUIRED_SERVICES=("neo4j" "neo4j-importer" "aeon-backend" "gemini-service")
    ALL_RUNNING=true

    for service in "${REQUIRED_SERVICES[@]}"; do
        if docker ps --filter "name=$service" --filter "status=running" --format '{{.Names}}' | grep -q "^${service}$"; then
            print_pass "Service '$service' is running"

            # Get service health status
            HEALTH=$(docker inspect --format='{{.State.Health.Status}}' "$service" 2>/dev/null || echo "no-healthcheck")
            if [ "$HEALTH" != "no-healthcheck" ]; then
                print_info "Health status: $HEALTH"
            fi
        else
            print_fail "Service '$service' is not running"
            ALL_RUNNING=false
        fi
    done

    if [ "$ALL_RUNNING" = true ]; then
        return 0
    else
        print_info "Start services with: docker compose up -d"
        return 1
    fi
}

check_port_availability() {
    print_check "Verifying port 3000 is available..."

    if lsof -Pi :3000 -sTCP:LISTEN -t &> /dev/null; then
        PROCESS=$(lsof -Pi :3000 -sTCP:LISTEN | tail -n 1)
        print_fail "Port 3000 is already in use"
        print_info "Process using port: $PROCESS"
        return 1
    else
        print_pass "Port 3000 is available"
        return 0
    fi
}

check_environment_file() {
    print_check "Verifying .env file exists and is valid..."

    ENV_FILE="$(dirname "$0")/../.env"

    if [ ! -f "$ENV_FILE" ]; then
        print_fail ".env file not found at: $ENV_FILE"
        print_info "Copy from .env.example: cp .env.example .env"
        return 1
    fi

    print_pass ".env file exists"

    # Check for required environment variables
    REQUIRED_VARS=("NEO4J_URI" "NEO4J_USERNAME" "NEO4J_PASSWORD" "BACKEND_URL" "GEMINI_URL")
    MISSING_VARS=()

    for var in "${REQUIRED_VARS[@]}"; do
        if ! grep -q "^${var}=" "$ENV_FILE"; then
            MISSING_VARS+=("$var")
        fi
    done

    if [ ${#MISSING_VARS[@]} -eq 0 ]; then
        print_pass "All required environment variables are present"
        return 0
    else
        print_fail "Missing required environment variables: ${MISSING_VARS[*]}"
        return 1
    fi
}

check_health_endpoints() {
    print_check "Verifying health check endpoint dependencies..."

    # Check Neo4j
    NEO4J_URI=${NEO4J_URI:-"bolt://localhost:7687"}
    print_info "Checking Neo4j at: $NEO4J_URI"

    if docker exec neo4j cypher-shell -u neo4j -p password "RETURN 1;" &> /dev/null; then
        print_pass "Neo4j is accessible"
    else
        print_warn "Could not verify Neo4j connectivity (may require credentials)"
    fi

    # Check Backend
    BACKEND_URL=${BACKEND_URL:-"http://localhost:5001"}
    print_info "Checking Backend at: $BACKEND_URL"

    if curl -s -f "${BACKEND_URL}/health" &> /dev/null; then
        print_pass "Backend health endpoint is accessible"
    else
        print_warn "Backend health endpoint not accessible (service may not be ready)"
    fi

    # Check Gemini
    GEMINI_URL=${GEMINI_URL:-"http://localhost:5002"}
    print_info "Checking Gemini at: $GEMINI_URL"

    if curl -s -f "${GEMINI_URL}/health" &> /dev/null; then
        print_pass "Gemini health endpoint is accessible"
    else
        print_warn "Gemini health endpoint not accessible (service may not be ready)"
    fi

    return 0
}

check_node_installed() {
    print_check "Verifying Node.js is installed..."

    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_pass "Node.js is installed ($NODE_VERSION)"

        # Check if version is adequate (v14+)
        MAJOR_VERSION=$(node --version | cut -d 'v' -f2 | cut -d '.' -f1)
        if [ "$MAJOR_VERSION" -ge 14 ]; then
            print_pass "Node.js version is adequate (>= v14)"
        else
            print_warn "Node.js version may be too old (recommended: v14+)"
        fi
        return 0
    else
        print_fail "Node.js is not installed"
        return 1
    fi
}

check_npm_installed() {
    print_check "Verifying npm is installed..."

    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_pass "npm is installed (version: $NPM_VERSION)"
        return 0
    else
        print_fail "npm is not installed"
        return 1
    fi
}

check_dependencies_installed() {
    print_check "Verifying project dependencies are installed..."

    PROJECT_DIR="$(dirname "$0")/.."

    if [ -d "$PROJECT_DIR/node_modules" ]; then
        print_pass "node_modules directory exists"

        # Check for key dependencies
        KEY_DEPS=("react" "react-dom" "vite" "axios")
        MISSING_DEPS=()

        for dep in "${KEY_DEPS[@]}"; do
            if [ ! -d "$PROJECT_DIR/node_modules/$dep" ]; then
                MISSING_DEPS+=("$dep")
            fi
        done

        if [ ${#MISSING_DEPS[@]} -eq 0 ]; then
            print_pass "Key dependencies are installed"
            return 0
        else
            print_warn "Some dependencies may be missing: ${MISSING_DEPS[*]}"
            print_info "Run: npm install"
            return 0
        fi
    else
        print_fail "node_modules directory not found"
        print_info "Run: npm install"
        return 1
    fi
}

check_disk_space() {
    print_check "Verifying sufficient disk space..."

    AVAILABLE_SPACE=$(df -h . | tail -1 | awk '{print $4}' | sed 's/G//')

    if [ "${AVAILABLE_SPACE%.*}" -ge 1 ]; then
        print_pass "Sufficient disk space available (${AVAILABLE_SPACE}G)"
        return 0
    else
        print_warn "Low disk space: ${AVAILABLE_SPACE}G available"
        return 0
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    print_header "Pre-Deployment Checklist - Web Interface"

    echo -e "${BLUE}Starting comprehensive pre-deployment checks...${NC}\n"

    # System Checks
    print_header "System Prerequisites"
    check_docker_installed
    check_docker_running
    check_node_installed
    check_npm_installed
    check_disk_space

    # Docker Environment
    print_header "Docker Environment"
    check_docker_network
    check_required_services

    # Application Configuration
    print_header "Application Configuration"
    check_environment_file
    check_dependencies_installed

    # Network & Connectivity
    print_header "Network & Connectivity"
    check_port_availability
    check_health_endpoints

    # Summary
    print_header "Summary"

    TOTAL_CHECKS=$((CHECKS_PASSED + CHECKS_FAILED + CHECKS_WARNING))

    echo -e "${GREEN}Passed:${NC}   $CHECKS_PASSED"
    echo -e "${RED}Failed:${NC}   $CHECKS_FAILED"
    echo -e "${YELLOW}Warnings:${NC} $CHECKS_WARNING"
    echo -e "${BLUE}Total:${NC}    $TOTAL_CHECKS"

    echo ""

    if [ $CHECKS_FAILED -eq 0 ]; then
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}✓ All critical checks passed!${NC}"
        echo -e "${GREEN}✓ System is ready for deployment${NC}"
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

        if [ $CHECKS_WARNING -gt 0 ]; then
            echo -e "\n${YELLOW}Note: $CHECKS_WARNING warning(s) detected. Review above for details.${NC}"
        fi

        echo -e "\n${BLUE}Next steps:${NC}"
        echo -e "  1. Review any warnings above"
        echo -e "  2. Build the application: ${GREEN}npm run build${NC}"
        echo -e "  3. Start the container: ${GREEN}docker compose up -d web-interface${NC}"
        echo -e "  4. Access at: ${GREEN}http://localhost:3000${NC}"

        exit 0
    else
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}✗ $CHECKS_FAILED critical check(s) failed!${NC}"
        echo -e "${RED}✗ System is NOT ready for deployment${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

        echo -e "\n${YELLOW}Please resolve the failed checks above before deploying.${NC}"

        exit 1
    fi
}

# Run main function
main
