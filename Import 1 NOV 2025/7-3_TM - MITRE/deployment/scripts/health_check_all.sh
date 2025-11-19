#!/bin/bash
# File: health_check_all.sh
# Created: 2025-11-08
# Purpose: Comprehensive health checks for all AEON APIs
# Status: ACTIVE

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
NER_API_URL="${NER_API_URL:-http://localhost:8000}"
QUERY_API_URL="${QUERY_API_URL:-http://localhost:8001}"
NEO4J_URL="${NEO4J_URL:-bolt://localhost:7687}"
TIMEOUT="${TIMEOUT:-10}"

# Status tracking
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

check_service() {
    local service_name=$1
    local url=$2
    local endpoint=${3:-/health}

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    log_info "Checking $service_name..."

    if response=$(curl -sf --max-time "$TIMEOUT" "$url$endpoint"); then
        log_info "✓ $service_name is healthy"

        # Parse and display details if JSON
        if echo "$response" | jq -e '.' >/dev/null 2>&1; then
            echo "$response" | jq '.'
        else
            echo "$response"
        fi

        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        log_error "✗ $service_name health check failed"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_neo4j() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    log_info "Checking Neo4j connectivity..."

    # Extract host and port from URL
    neo4j_host=$(echo "$NEO4J_URL" | sed -E 's|^[^:]+://([^:]+):.*|\1|')
    neo4j_port=$(echo "$NEO4J_URL" | sed -E 's|^[^:]+://[^:]+:([0-9]+).*|\1|')

    if timeout 5 bash -c "echo > /dev/tcp/$neo4j_host/$neo4j_port" 2>/dev/null; then
        log_info "✓ Neo4j is reachable at $neo4j_host:$neo4j_port"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        log_error "✗ Neo4j is not reachable at $neo4j_host:$neo4j_port"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_docker_containers() {
    log_section "Docker Container Status"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    containers=("aeon-ner-api" "aeon-query-api" "neo4j")
    all_running=true

    for container in "${containers[@]}"; do
        if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
            status=$(docker inspect --format='{{.State.Status}}' "$container")
            health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "N/A")

            log_info "✓ Container '$container': $status (Health: $health)"

            # Show resource usage
            stats=$(docker stats --no-stream --format "table {{.CPUPerc}}\t{{.MemUsage}}" "$container" | tail -n 1)
            echo "  Resource usage: $stats"
        else
            log_error "✗ Container '$container' is not running"
            all_running=false
        fi
    done

    if $all_running; then
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
}

test_ner_api() {
    log_section "NER API Functional Test"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    test_payload='{"text": "The APT29 group uses MITRE ATT&CK technique T1566 for phishing."}'

    log_info "Testing entity extraction..."

    if response=$(curl -sf --max-time "$TIMEOUT" -X POST "$NER_API_URL/api/v1/extract-entities" \
        -H "Content-Type: application/json" \
        -d "$test_payload"); then

        if echo "$response" | jq -e '.entities' >/dev/null 2>&1; then
            entity_count=$(echo "$response" | jq '.entities | length')
            log_info "✓ NER API functional test passed ($entity_count entities extracted)"
            echo "$response" | jq '.entities[:3]'  # Show first 3 entities
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            log_error "✗ Invalid response format"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        fi
    else
        log_error "✗ NER API functional test failed"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

test_query_api() {
    log_section "Query API Functional Test"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    test_query='MATCH (n:Technique) RETURN n.name, n.id LIMIT 3'

    log_info "Testing query execution..."

    if response=$(curl -sf --max-time "$TIMEOUT" -X POST "$QUERY_API_URL/api/v1/query/execute" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$test_query\"}"); then

        if echo "$response" | jq -e '.results' >/dev/null 2>&1; then
            result_count=$(echo "$response" | jq '.results | length')
            log_info "✓ Query API functional test passed ($result_count results)"
            echo "$response" | jq '.results[:3]'
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            log_error "✗ Invalid response format"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        fi
    else
        log_error "✗ Query API functional test failed"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_system_resources() {
    log_section "System Resource Status"

    log_info "CPU and Memory usage:"
    top -bn1 | head -5

    log_info "\nDisk usage:"
    df -h | grep -E '^/dev/'

    log_info "\nDocker disk usage:"
    docker system df
}

generate_report() {
    log_section "Health Check Summary"

    echo -e "Total checks: $TOTAL_CHECKS"
    echo -e "${GREEN}Passed: $PASSED_CHECKS${NC}"
    echo -e "${RED}Failed: $FAILED_CHECKS${NC}"

    success_rate=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
    echo -e "\nSuccess rate: $success_rate%"

    if [ $FAILED_CHECKS -eq 0 ]; then
        echo -e "\n${GREEN}✓ All health checks passed!${NC}"
        return 0
    else
        echo -e "\n${RED}✗ Some health checks failed${NC}"
        return 1
    fi
}

# Main execution
main() {
    log_section "AEON Backend API Health Check"

    echo "Timestamp: $(date)"
    echo "NER API: $NER_API_URL"
    echo "Query API: $QUERY_API_URL"
    echo "Neo4j: $NEO4J_URL"

    # Run all checks
    log_section "Service Health Checks"
    check_service "NER API" "$NER_API_URL"
    check_service "Query API" "$QUERY_API_URL"
    check_neo4j

    check_docker_containers

    # Functional tests
    test_ner_api
    test_query_api

    # System resources
    check_system_resources

    # Summary
    generate_report
}

main "$@"
