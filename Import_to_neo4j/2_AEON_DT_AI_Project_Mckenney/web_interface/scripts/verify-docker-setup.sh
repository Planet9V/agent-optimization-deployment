#!/bin/bash

# AEON SaaS Docker Development Setup Verification Script
# Verifies that all prerequisites and configurations are in place

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "AEON SaaS Docker Setup Verification"
echo "=========================================="
echo ""

# Check counter
CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

# Function to print success
print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

# Function to print error
print_error() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# 1. Check Docker
echo "1. Checking Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    print_success "Docker installed: $DOCKER_VERSION"

    # Check if Docker daemon is running
    if docker ps &> /dev/null; then
        print_success "Docker daemon is running"
    else
        print_error "Docker daemon is not running. Start Docker Desktop or service."
    fi
else
    print_error "Docker is not installed. Install from: https://docs.docker.com/get-docker/"
fi

# 2. Check Docker Compose
echo ""
echo "2. Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | awk '{print $4}' | sed 's/,//')
    print_success "Docker Compose installed: $COMPOSE_VERSION"
else
    print_error "Docker Compose is not installed"
fi

# 3. Check for openspg-network
echo ""
echo "3. Checking openspg-network..."
if docker network ls | grep -q openspg-network; then
    print_success "openspg-network exists"

    # Check network details
    NETWORK_DRIVER=$(docker network inspect openspg-network -f '{{.Driver}}' 2>/dev/null)
    echo "   Network driver: $NETWORK_DRIVER"
else
    print_error "openspg-network not found"
    echo "   Create it with: docker network create openspg-network"
fi

# 4. Check for AEON backend services
echo ""
echo "4. Checking AEON backend services..."
BACKEND_SERVICES=("openspg-neo4j" "openspg-qdrant" "openspg-mysql" "openspg-minio" "openspg-server")

for service in "${BACKEND_SERVICES[@]}"; do
    if docker ps --format '{{.Names}}' | grep -q "^${service}$"; then
        print_success "$service is running"
    else
        print_warning "$service is not running (may be optional for development)"
    fi
done

# 5. Check required files
echo ""
echo "5. Checking required configuration files..."

if [ -f "docker-compose.dev.yml" ]; then
    print_success "docker-compose.dev.yml exists"
else
    print_error "docker-compose.dev.yml not found"
fi

if [ -f "Dockerfile.dev" ]; then
    print_success "Dockerfile.dev exists"
else
    print_error "Dockerfile.dev not found"
fi

if [ -f ".env.development" ]; then
    print_success ".env.development exists"

    # Check for placeholder values
    if grep -q "your_development_key_here" .env.development 2>/dev/null; then
        print_warning ".env.development contains placeholder values - update with real keys"
    fi

    if grep -q "your-openai-api-key-here" .env.development 2>/dev/null; then
        print_warning ".env.development missing OpenAI API key (required for chat features)"
    fi
else
    print_error ".env.development not found"
    if [ -f ".env.development.example" ]; then
        echo "   Create it with: cp .env.development.example .env.development"
    fi
fi

if [ -f ".env.development.example" ]; then
    print_success ".env.development.example exists"
else
    print_warning ".env.development.example not found (template file)"
fi

if [ -f "scripts/init-db.sql" ]; then
    print_success "scripts/init-db.sql exists"
else
    print_error "scripts/init-db.sql not found"
fi

# 6. Check package.json
echo ""
echo "6. Checking package.json..."
if [ -f "package.json" ]; then
    print_success "package.json exists"

    # Check for required dependencies
    REQUIRED_DEPS=("next" "react" "neo4j-driver" "@qdrant/js-client-rest" "mysql2" "minio")
    for dep in "${REQUIRED_DEPS[@]}"; do
        if grep -q "\"${dep}\"" package.json; then
            echo "   ✓ $dep dependency found"
        else
            print_warning "$dep not found in package.json"
        fi
    done
else
    print_error "package.json not found"
fi

# 7. Check available ports
echo ""
echo "7. Checking port availability..."
check_port() {
    local port=$1
    local service=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $port is already in use (required for $service)"
        echo "   PID: $(lsof -ti:$port)"
    else
        print_success "Port $port is available ($service)"
    fi
}

check_port 3000 "Next.js development server"
check_port 5432 "PostgreSQL development database"
check_port 8080 "Adminer database UI"

# 8. Check disk space
echo ""
echo "8. Checking disk space..."
AVAILABLE_SPACE=$(df -h . | awk 'NR==2 {print $4}')
echo "   Available space: $AVAILABLE_SPACE"

# Try to estimate required space
REQUIRED_GB=5
if [ $(df . | awk 'NR==2 {print $4}') -gt $((REQUIRED_GB * 1024 * 1024)) ]; then
    print_success "Sufficient disk space available (>5GB recommended)"
else
    print_warning "Low disk space (>5GB recommended for development)"
fi

# Summary
echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Passed:${NC} $CHECKS_PASSED"
echo -e "${RED}Failed:${NC} $CHECKS_FAILED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review and update .env.development with your API keys"
    echo "2. Start the development environment:"
    echo "   docker-compose -f docker-compose.dev.yml up"
    echo "3. Access the application at http://localhost:3000"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some critical checks failed.${NC}"
    echo "Please resolve the issues above before starting the development environment."
    echo ""
    exit 1
fi
