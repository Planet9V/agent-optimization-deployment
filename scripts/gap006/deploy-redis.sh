#!/bin/bash

###############################################################################
# GAP-006 Redis Deployment Script
#
# Deploys Redis instance for job queue management with:
# - Network validation
# - Health checking
# - Configuration verification
# - Automated rollback on failure
###############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DOCKER_COMPOSE_FILE="${PROJECT_ROOT}/docker/docker-compose.gap006-redis.yml"
CONTAINER_NAME="openspg-redis"
NETWORK_NAME="openspg-network"
REDIS_PORT="${REDIS_PORT:-6380}"
REDIS_PASSWORD="${REDIS_PASSWORD:-redis@openspg}"
MAX_WAIT_TIME=60

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Check if docker is available
check_docker() {
    log_info "Checking Docker availability..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi

    log_success "Docker is available"
}

# Check if docker-compose file exists
check_compose_file() {
    log_info "Checking docker-compose file..."

    if [[ ! -f "${DOCKER_COMPOSE_FILE}" ]]; then
        log_error "Docker compose file not found: ${DOCKER_COMPOSE_FILE}"
        exit 1
    fi

    log_success "Docker compose file found"
}

# Check or create network
check_network() {
    log_info "Checking network: ${NETWORK_NAME}..."

    if docker network inspect "${NETWORK_NAME}" &> /dev/null; then
        log_success "Network ${NETWORK_NAME} exists"
    else
        log_warning "Network ${NETWORK_NAME} does not exist, creating..."
        docker network create "${NETWORK_NAME}"
        log_success "Network ${NETWORK_NAME} created"
    fi
}

# Stop existing container
stop_existing() {
    log_info "Checking for existing container..."

    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log_warning "Stopping existing container: ${CONTAINER_NAME}"
        docker stop "${CONTAINER_NAME}" || true
        docker rm "${CONTAINER_NAME}" || true
        log_success "Existing container removed"
    else
        log_info "No existing container found"
    fi
}

# Deploy Redis
deploy_redis() {
    log_info "Deploying Redis container..."

    cd "${PROJECT_ROOT}"

    # Export environment variables
    export REDIS_PASSWORD="${REDIS_PASSWORD}"

    # Start container
    docker-compose -f "${DOCKER_COMPOSE_FILE}" up -d

    log_success "Redis container started"
}

# Wait for Redis to be healthy
wait_for_health() {
    log_info "Waiting for Redis to be healthy (max ${MAX_WAIT_TIME}s)..."

    local elapsed=0
    local interval=2

    while [[ $elapsed -lt $MAX_WAIT_TIME ]]; do
        if docker exec "${CONTAINER_NAME}" redis-cli -a "${REDIS_PASSWORD}" ping 2>/dev/null | grep -q "PONG"; then
            log_success "Redis is healthy"
            return 0
        fi

        sleep $interval
        elapsed=$((elapsed + interval))
        echo -n "."
    done

    echo ""
    log_error "Redis failed to become healthy within ${MAX_WAIT_TIME}s"
    return 1
}

# Verify Redis configuration
verify_config() {
    log_info "Verifying Redis configuration..."

    # Check maxmemory
    local maxmemory
    maxmemory=$(docker exec "${CONTAINER_NAME}" redis-cli -a "${REDIS_PASSWORD}" CONFIG GET maxmemory 2>/dev/null | tail -n1)
    log_info "Max memory: $((maxmemory / 1024 / 1024 / 1024))GB"

    # Check maxmemory-policy
    local policy
    policy=$(docker exec "${CONTAINER_NAME}" redis-cli -a "${REDIS_PASSWORD}" CONFIG GET maxmemory-policy 2>/dev/null | tail -n1)
    log_info "Eviction policy: ${policy}"

    # Check persistence
    local aof_enabled
    aof_enabled=$(docker exec "${CONTAINER_NAME}" redis-cli -a "${REDIS_PASSWORD}" CONFIG GET appendonly 2>/dev/null | tail -n1)
    log_info "AOF enabled: ${aof_enabled}"

    # Check connection
    local ping_result
    ping_result=$(docker exec "${CONTAINER_NAME}" redis-cli -a "${REDIS_PASSWORD}" PING 2>/dev/null)

    if [[ "${ping_result}" == "PONG" ]]; then
        log_success "Redis configuration verified"
    else
        log_error "Redis configuration verification failed"
        return 1
    fi
}

# Test job queue operations
test_operations() {
    log_info "Testing job queue operations..."

    # Test LPUSH/BRPOPLPUSH pattern
    docker exec "${CONTAINER_NAME}" redis-cli -a "${REDIS_PASSWORD}" LPUSH "gap006:pending-queue" '{"test":"job"}' &>/dev/null

    local result
    result=$(docker exec "${CONTAINER_NAME}" redis-cli -a "${REDIS_PASSWORD}" BRPOPLPUSH "gap006:pending-queue" "gap006:processing-queue" 1 2>/dev/null)

    if [[ -n "${result}" ]]; then
        log_success "Job queue operations working"
        # Cleanup test data
        docker exec "${CONTAINER_NAME}" redis-cli -a "${REDIS_PASSWORD}" DEL "gap006:processing-queue" &>/dev/null
    else
        log_error "Job queue operations failed"
        return 1
    fi
}

# Show deployment info
show_info() {
    log_info "Deployment Information:"
    echo ""
    echo "  Container Name:  ${CONTAINER_NAME}"
    echo "  Network:         ${NETWORK_NAME}"
    echo "  Host Port:       ${REDIS_PORT}"
    echo "  Container Port:  6379"
    echo "  Password:        ${REDIS_PASSWORD}"
    echo ""
    echo "Connection strings:"
    echo "  Internal: redis://:${REDIS_PASSWORD}@${CONTAINER_NAME}:6379"
    echo "  External: redis://:${REDIS_PASSWORD}@localhost:${REDIS_PORT}"
    echo ""
    log_info "Queue names:"
    echo "  - gap006:pending-queue"
    echo "  - gap006:processing-queue"
    echo "  - gap006:high-priority-queue"
    echo "  - gap006:medium-priority-queue"
    echo "  - gap006:low-priority-queue"
    echo "  - gap006:dead-letter-queue"
    echo ""
}

# Rollback on failure
rollback() {
    log_error "Deployment failed, rolling back..."

    docker-compose -f "${DOCKER_COMPOSE_FILE}" down -v || true

    log_warning "Rollback completed"
    exit 1
}

# Main deployment flow
main() {
    log_info "Starting GAP-006 Redis deployment..."
    echo ""

    # Pre-deployment checks
    check_docker
    check_compose_file
    check_network

    # Deployment
    stop_existing
    deploy_redis

    # Health and verification
    if ! wait_for_health; then
        rollback
    fi

    if ! verify_config; then
        rollback
    fi

    if ! test_operations; then
        rollback
    fi

    # Success
    echo ""
    log_success "GAP-006 Redis deployment completed successfully!"
    echo ""
    show_info

    # Show container status
    log_info "Container status:"
    docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""

    log_info "To view logs: docker logs -f ${CONTAINER_NAME}"
    log_info "To stop: docker-compose -f ${DOCKER_COMPOSE_FILE} down"
    log_info "To stop and remove data: docker-compose -f ${DOCKER_COMPOSE_FILE} down -v"
}

# Run main function
main "$@"
