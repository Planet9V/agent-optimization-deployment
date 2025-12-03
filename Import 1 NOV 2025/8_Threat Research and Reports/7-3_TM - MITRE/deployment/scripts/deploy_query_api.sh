#!/bin/bash
# File: deploy_query_api.sh
# Created: 2025-11-08
# Purpose: Deploy Query Execution API with validation
# Status: ACTIVE

set -e
set -u

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEPLOYMENT_DIR="$PROJECT_ROOT/deployment"
ENV_FILE="${ENV_FILE:-$PROJECT_ROOT/.env}"
DOCKER_IMAGE="${DOCKER_IMAGE:-aeon-query-api:latest}"
CONTAINER_NAME="${CONTAINER_NAME:-aeon-query-api}"
API_PORT="${API_PORT:-8001}"
HEALTH_CHECK_RETRIES="${HEALTH_CHECK_RETRIES:-10}"
HEALTH_CHECK_INTERVAL="${HEALTH_CHECK_INTERVAL:-5}"

# Logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validation
validate_environment() {
    log_info "Validating environment..."

    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file not found: $ENV_FILE"
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        log_error "Docker not installed"
        exit 1
    fi

    # Check port availability
    if lsof -Pi :$API_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warn "Port $API_PORT is already in use"
        read -p "Stop existing service? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker stop $CONTAINER_NAME 2>/dev/null || true
            docker rm $CONTAINER_NAME 2>/dev/null || true
        else
            log_error "Cannot deploy with port conflict"
            exit 1
        fi
    fi

    # Validate Neo4j connection
    source "$ENV_FILE"
    if [ -z "${NEO4J_URI:-}" ] || [ -z "${NEO4J_USER:-}" ] || [ -z "${NEO4J_PASSWORD:-}" ]; then
        log_error "Neo4j credentials not configured"
        exit 1
    fi

    # Check if Neo4j is accessible
    log_info "Checking Neo4j connectivity..."
    if ! timeout 5 bash -c "echo > /dev/tcp/${NEO4J_URI#*://}" 2>/dev/null; then
        log_error "Cannot connect to Neo4j at $NEO4J_URI"
        exit 1
    fi

    log_info "Environment validation passed"
}

# Build image
build_image() {
    log_info "Building Docker image: $DOCKER_IMAGE"

    cd "$DEPLOYMENT_DIR/docker"
    docker build -f Dockerfile.query_api -t "$DOCKER_IMAGE" "$PROJECT_ROOT"

    if [ $? -eq 0 ]; then
        log_info "Docker image built successfully"
    else
        log_error "Docker image build failed"
        exit 1
    fi
}

# Deploy
deploy_container() {
    log_info "Deploying container: $CONTAINER_NAME"

    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true

    docker run -d \
        --name "$CONTAINER_NAME" \
        --env-file "$ENV_FILE" \
        -p "$API_PORT:8000" \
        --restart unless-stopped \
        --health-cmd="curl -f http://localhost:8000/health || exit 1" \
        --health-interval=30s \
        --health-timeout=10s \
        --health-retries=3 \
        "$DOCKER_IMAGE"

    if [ $? -eq 0 ]; then
        log_info "Container deployed successfully"
    else
        log_error "Container deployment failed"
        exit 1
    fi
}

# Health check
health_check() {
    log_info "Performing health check..."

    local retries=0
    while [ $retries -lt $HEALTH_CHECK_RETRIES ]; do
        if curl -sf "http://localhost:$API_PORT/health" > /dev/null; then
            log_info "Health check passed"
            health_status=$(curl -s "http://localhost:$API_PORT/health")
            echo "$health_status" | jq '.' 2>/dev/null || echo "$health_status"
            return 0
        fi

        retries=$((retries + 1))
        log_warn "Health check attempt $retries/$HEALTH_CHECK_RETRIES failed, retrying..."
        sleep $HEALTH_CHECK_INTERVAL
    done

    log_error "Health check failed"
    return 1
}

# Integration test
integration_test() {
    log_info "Running integration tests..."

    # Test query execution
    test_query='MATCH (n:Technique) RETURN n.name LIMIT 5'
    response=$(curl -s -X POST "http://localhost:$API_PORT/api/v1/query/execute" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$test_query\"}")

    if echo "$response" | jq -e '.results' > /dev/null 2>&1; then
        log_info "Query execution test passed"
        echo "$response" | jq '.'
    else
        log_error "Query execution test failed"
        echo "Response: $response"
        return 1
    fi

    # Test query validation
    invalid_query='INVALID CYPHER QUERY'
    response=$(curl -s -X POST "http://localhost:$API_PORT/api/v1/query/validate" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$invalid_query\"}")

    if echo "$response" | jq -e '.valid == false' > /dev/null 2>&1; then
        log_info "Query validation test passed"
    else
        log_error "Query validation test failed"
        return 1
    fi

    log_info "Integration tests passed"
}

# Rollback
rollback() {
    log_error "Deployment failed, initiating rollback..."

    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true

    if docker images | grep -q "$DOCKER_IMAGE.backup"; then
        log_info "Restoring previous version..."
        docker tag "$DOCKER_IMAGE.backup" "$DOCKER_IMAGE"
        deploy_container
    fi

    log_error "Rollback completed"
    exit 1
}

# Main
main() {
    log_info "Starting Query API deployment..."
    log_info "Project root: $PROJECT_ROOT"
    log_info "API port: $API_PORT"
    log_info "Container name: $CONTAINER_NAME"

    # Backup current image
    if docker images | grep -q "$DOCKER_IMAGE"; then
        log_info "Backing up current image..."
        docker tag "$DOCKER_IMAGE" "$DOCKER_IMAGE.backup"
    fi

    validate_environment || exit 1
    build_image || rollback
    deploy_container || rollback

    sleep 3

    health_check || rollback
    integration_test || rollback

    log_info "========================================="
    log_info "Query API deployment completed successfully!"
    log_info "API URL: http://localhost:$API_PORT"
    log_info "Health endpoint: http://localhost:$API_PORT/health"
    log_info "API docs: http://localhost:$API_PORT/docs"
    log_info "Container logs: docker logs -f $CONTAINER_NAME"
    log_info "========================================="
}

trap rollback ERR
main "$@"
