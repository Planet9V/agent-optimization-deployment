#!/bin/bash
# AEON UI Production Deployment Script
# Usage: ./scripts/deploy.sh [start|stop|restart|logs|health]

set -e

COMPOSE_FILE="docker-compose.aeon-ui.yml"
SERVICE_NAME="aeon-ui"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
function print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

function print_error() {
    echo -e "${RED}✗${NC} $1"
}

function print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

function check_prerequisites() {
    echo "Checking prerequisites..."

    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running"
        exit 1
    fi
    print_success "Docker is running"

    # Check if openspg-network exists
    if ! docker network inspect openspg-network > /dev/null 2>&1; then
        print_error "openspg-network does not exist"
        print_warning "Please start OpenSPG infrastructure first"
        exit 1
    fi
    print_success "openspg-network exists"

    # Check if .env.production exists
    if [ ! -f .env.production ]; then
        print_warning ".env.production not found"
        print_warning "Creating from .env.example..."
        if [ -f .env.example ]; then
            cp .env.example .env.production
            print_warning "Please edit .env.production with production values"
        else
            print_error ".env.example not found. Cannot create .env.production"
            exit 1
        fi
    fi
    print_success ".env.production exists"
}

function check_health() {
    echo "Checking service health..."

    # Wait for container to be healthy
    for i in {1..30}; do
        if docker-compose -f $COMPOSE_FILE ps | grep -q "healthy"; then
            print_success "Service is healthy"
            return 0
        fi
        echo -n "."
        sleep 2
    done

    print_error "Service failed to become healthy"
    docker-compose -f $COMPOSE_FILE logs --tail=50 $SERVICE_NAME
    return 1
}

function start_service() {
    echo "Starting AEON UI..."
    check_prerequisites

    # Build and start
    docker-compose -f $COMPOSE_FILE build
    docker-compose -f $COMPOSE_FILE up -d

    print_success "Service started"

    # Check health
    check_health

    # Show access information
    echo ""
    echo "========================================="
    echo "AEON UI is now running!"
    echo "========================================="
    echo "Web UI: http://localhost:3000"
    echo "Health: http://localhost:3000/api/health"
    echo "Container IP: 172.18.0.8"
    echo ""
    echo "View logs: ./scripts/deploy.sh logs"
    echo "========================================="
}

function stop_service() {
    echo "Stopping AEON UI..."
    docker-compose -f $COMPOSE_FILE down
    print_success "Service stopped"
}

function restart_service() {
    echo "Restarting AEON UI..."
    docker-compose -f $COMPOSE_FILE restart
    print_success "Service restarted"
    check_health
}

function show_logs() {
    docker-compose -f $COMPOSE_FILE logs -f $SERVICE_NAME
}

function show_status() {
    echo "Service Status:"
    docker-compose -f $COMPOSE_FILE ps

    echo ""
    echo "Health Status:"
    docker-compose -f $COMPOSE_FILE exec $SERVICE_NAME wget -O- http://localhost:3000/api/health 2>/dev/null || echo "Health check unavailable"

    echo ""
    echo "Network Configuration:"
    docker inspect $SERVICE_NAME 2>/dev/null | grep -A 10 "Networks" || echo "Container not running"
}

# Main script
case "${1:-}" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    logs)
        show_logs
        ;;
    health)
        check_health
        ;;
    status)
        show_status
        ;;
    *)
        echo "AEON UI Deployment Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|logs|health|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Build and start the service"
        echo "  stop    - Stop the service"
        echo "  restart - Restart the service"
        echo "  logs    - View service logs (follow mode)"
        echo "  health  - Check service health"
        echo "  status  - Show service status and configuration"
        exit 1
        ;;
esac
