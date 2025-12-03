#!/bin/bash
# File: rollback_deployment.sh
# Created: 2025-11-08
# Purpose: Automated rollback procedure for failed deployments
# Status: ACTIVE

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show rollback options
show_menu() {
    echo "========================================="
    echo "AEON Backend API Rollback Menu"
    echo "========================================="
    echo "1) Rollback NER API"
    echo "2) Rollback Query API"
    echo "3) Rollback Both APIs"
    echo "4) Rollback to specific Docker tag"
    echo "5) Emergency stop all services"
    echo "6) Exit"
    echo "========================================="
}

# Rollback single service
rollback_service() {
    local service_name=$1
    local container_name=$2
    local image_name=$3

    log_info "Rolling back $service_name..."

    # Stop current container
    log_info "Stopping current container: $container_name"
    docker stop "$container_name" 2>/dev/null || true
    docker rm "$container_name" 2>/dev/null || true

    # Check for backup image
    if docker images | grep -q "$image_name.backup"; then
        log_info "Found backup image, restoring..."

        # Tag backup as current
        docker tag "$image_name.backup" "$image_name"

        # Redeploy using backup
        case $service_name in
            "NER API")
                CONTAINER_NAME="$container_name" DOCKER_IMAGE="$image_name" \
                    "$SCRIPT_DIR/deploy_ner_v8_api.sh"
                ;;
            "Query API")
                CONTAINER_NAME="$container_name" DOCKER_IMAGE="$image_name" \
                    "$SCRIPT_DIR/deploy_query_api.sh"
                ;;
        esac

        log_info "$service_name rollback completed"
    else
        log_error "No backup image found for $image_name"
        log_info "Available images:"
        docker images | grep "$image_name" || echo "No images found"

        read -p "Enter image tag to restore (or 'skip'): " tag
        if [ "$tag" != "skip" ]; then
            docker tag "$image_name:$tag" "$image_name"
            log_info "Tagged $image_name:$tag as current"
        fi
    fi
}

# Rollback to specific tag
rollback_to_tag() {
    echo "Available Docker images:"
    echo "NER API images:"
    docker images | grep "aeon-ner-api" || echo "None found"
    echo ""
    echo "Query API images:"
    docker images | grep "aeon-query-api" || echo "None found"

    echo ""
    read -p "Enter service (ner/query): " service
    read -p "Enter tag to restore: " tag

    case $service in
        ner)
            docker tag "aeon-ner-api:$tag" "aeon-ner-api:latest"
            CONTAINER_NAME="aeon-ner-api" "$SCRIPT_DIR/deploy_ner_v8_api.sh"
            ;;
        query)
            docker tag "aeon-query-api:$tag" "aeon-query-api:latest"
            CONTAINER_NAME="aeon-query-api" "$SCRIPT_DIR/deploy_query_api.sh"
            ;;
        *)
            log_error "Invalid service: $service"
            return 1
            ;;
    esac
}

# Emergency stop
emergency_stop() {
    log_warn "Emergency stop initiated - stopping all AEON services"

    read -p "Are you sure? This will stop all services. (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        log_info "Emergency stop cancelled"
        return
    fi

    log_info "Stopping NER API..."
    docker stop aeon-ner-api 2>/dev/null || true

    log_info "Stopping Query API..."
    docker stop aeon-query-api 2>/dev/null || true

    log_info "All services stopped"

    read -p "Remove containers? (yes/no): " remove
    if [ "$remove" == "yes" ]; then
        docker rm aeon-ner-api 2>/dev/null || true
        docker rm aeon-query-api 2>/dev/null || true
        log_info "Containers removed"
    fi
}

# Create deployment snapshot
create_snapshot() {
    local snapshot_name="aeon-snapshot-$(date +%Y%m%d-%H%M%S)"

    log_info "Creating deployment snapshot: $snapshot_name"

    # Tag current images
    docker tag aeon-ner-api:latest "aeon-ner-api:$snapshot_name" 2>/dev/null || true
    docker tag aeon-query-api:latest "aeon-query-api:$snapshot_name" 2>/dev/null || true

    # Export configuration
    mkdir -p "$PROJECT_ROOT/.snapshots"

    # Save container configs
    docker inspect aeon-ner-api > "$PROJECT_ROOT/.snapshots/$snapshot_name-ner-api.json" 2>/dev/null || true
    docker inspect aeon-query-api > "$PROJECT_ROOT/.snapshots/$snapshot_name-query-api.json" 2>/dev/null || true

    # Save environment
    cp "$PROJECT_ROOT/.env" "$PROJECT_ROOT/.snapshots/$snapshot_name.env" 2>/dev/null || true

    log_info "Snapshot created: $snapshot_name"
    echo "Tagged images: aeon-ner-api:$snapshot_name, aeon-query-api:$snapshot_name"
}

# Main menu loop
main() {
    while true; do
        echo ""
        show_menu
        read -p "Select option: " choice

        case $choice in
            1)
                rollback_service "NER API" "aeon-ner-api" "aeon-ner-api:latest"
                ;;
            2)
                rollback_service "Query API" "aeon-query-api" "aeon-query-api:latest"
                ;;
            3)
                rollback_service "NER API" "aeon-ner-api" "aeon-ner-api:latest"
                rollback_service "Query API" "aeon-query-api" "aeon-query-api:latest"
                ;;
            4)
                rollback_to_tag
                ;;
            5)
                emergency_stop
                ;;
            6)
                log_info "Exiting rollback menu"
                exit 0
                ;;
            *)
                log_error "Invalid option: $choice"
                ;;
        esac

        read -p "Press Enter to continue..."
    done
}

# Before starting, offer to create snapshot
echo "========================================="
echo "AEON Deployment Rollback Tool"
echo "========================================="
read -p "Create snapshot before rollback? (y/n): " create_snap
if [[ $create_snap =~ ^[Yy]$ ]]; then
    create_snapshot
fi

main "$@"
