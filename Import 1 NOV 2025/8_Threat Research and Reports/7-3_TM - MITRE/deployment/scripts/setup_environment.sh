#!/bin/bash
# File: setup_environment.sh
# Created: 2025-11-08
# Purpose: Environment setup and dependency installation
# Status: ACTIVE

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

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

# Check system requirements
check_requirements() {
    log_section "Checking System Requirements"

    local missing_deps=()

    # Check Docker
    if command -v docker &> /dev/null; then
        docker_version=$(docker --version)
        log_info "✓ Docker installed: $docker_version"
    else
        log_error "✗ Docker not installed"
        missing_deps+=("docker")
    fi

    # Check Docker Compose
    if command -v docker-compose &> /dev/null; then
        compose_version=$(docker-compose --version)
        log_info "✓ Docker Compose installed: $compose_version"
    else
        log_warn "✗ Docker Compose not installed (optional)"
    fi

    # Check curl
    if command -v curl &> /dev/null; then
        log_info "✓ curl installed"
    else
        log_error "✗ curl not installed"
        missing_deps+=("curl")
    fi

    # Check jq
    if command -v jq &> /dev/null; then
        log_info "✓ jq installed"
    else
        log_warn "✗ jq not installed (optional but recommended)"
    fi

    # Check Python
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version)
        log_info "✓ Python installed: $python_version"
    else
        log_error "✗ Python 3 not installed"
        missing_deps+=("python3")
    fi

    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again"
        exit 1
    fi

    log_info "All required dependencies installed"
}

# Setup environment file
setup_env_file() {
    log_section "Setting Up Environment File"

    if [ -f "$ENV_FILE" ]; then
        log_warn "Environment file already exists: $ENV_FILE"
        read -p "Overwrite? (y/n): " overwrite
        if [[ ! $overwrite =~ ^[Yy]$ ]]; then
            log_info "Keeping existing environment file"
            return
        fi

        # Backup existing
        cp "$ENV_FILE" "$ENV_FILE.backup.$(date +%Y%m%d-%H%M%S)"
        log_info "Backed up existing environment file"
    fi

    # Create environment file
    cat > "$ENV_FILE" << 'EOF'
# AEON Backend API Environment Configuration
# Created: 2025-11-08

# Neo4j Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=changeme
NEO4J_DATABASE=neo4j

# API Configuration
NER_API_PORT=8000
QUERY_API_PORT=8001
API_HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Performance
MAX_WORKERS=4
TIMEOUT=30
MAX_RETRIES=3

# Security
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:8001
API_KEY_ENABLED=false
# API_KEY=your-secret-key-here

# Monitoring
METRICS_ENABLED=true
METRICS_PORT=9090

# Development
DEBUG=false
RELOAD=true
EOF

    log_info "Environment file created: $ENV_FILE"
    log_warn "IMPORTANT: Update Neo4j credentials and other settings"
}

# Setup directories
setup_directories() {
    log_section "Setting Up Project Directories"

    local dirs=(
        "$PROJECT_ROOT/logs"
        "$PROJECT_ROOT/data"
        "$PROJECT_ROOT/.snapshots"
        "$PROJECT_ROOT/deployment/monitoring/prometheus"
        "$PROJECT_ROOT/deployment/monitoring/grafana"
    )

    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_info "Created directory: $dir"
        else
            log_info "Directory exists: $dir"
        fi
    done
}

# Install Python dependencies
install_python_deps() {
    log_section "Installing Python Dependencies"

    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        log_info "Installing from requirements.txt..."
        python3 -m pip install --upgrade pip
        python3 -m pip install -r "$PROJECT_ROOT/requirements.txt"
        log_info "Python dependencies installed"
    else
        log_warn "No requirements.txt found, skipping Python dependencies"
    fi
}

# Setup Neo4j
setup_neo4j() {
    log_section "Setting Up Neo4j"

    read -p "Start Neo4j container? (y/n): " start_neo4j
    if [[ ! $start_neo4j =~ ^[Yy]$ ]]; then
        log_info "Skipping Neo4j setup"
        return
    fi

    # Check if Neo4j is already running
    if docker ps | grep -q neo4j; then
        log_info "Neo4j container already running"
        return
    fi

    log_info "Starting Neo4j container..."

    docker run -d \
        --name neo4j \
        -p 7474:7474 \
        -p 7687:7687 \
        -e NEO4J_AUTH=neo4j/changeme \
        -v neo4j_data:/data \
        -v neo4j_logs:/logs \
        --restart unless-stopped \
        neo4j:latest

    log_info "Neo4j started successfully"
    log_info "Neo4j Browser: http://localhost:7474"
    log_info "Default credentials: neo4j/changeme"
    log_warn "IMPORTANT: Change the default password on first login"

    # Wait for Neo4j to be ready
    log_info "Waiting for Neo4j to be ready..."
    sleep 10

    local retries=0
    while [ $retries -lt 30 ]; do
        if curl -sf http://localhost:7474 > /dev/null; then
            log_info "Neo4j is ready"
            break
        fi
        retries=$((retries + 1))
        sleep 2
    done
}

# Make scripts executable
make_scripts_executable() {
    log_section "Making Scripts Executable"

    chmod +x "$SCRIPT_DIR"/*.sh
    log_info "All scripts in $SCRIPT_DIR are now executable"
}

# Display summary
display_summary() {
    log_section "Setup Complete"

    echo "Next steps:"
    echo "1. Review and update environment file: $ENV_FILE"
    echo "2. Update Neo4j password in environment file"
    echo "3. Configure API keys if needed"
    echo ""
    echo "Deploy services:"
    echo "  - NER API:   $SCRIPT_DIR/deploy_ner_v8_api.sh"
    echo "  - Query API: $SCRIPT_DIR/deploy_query_api.sh"
    echo ""
    echo "Check health:"
    echo "  $SCRIPT_DIR/health_check_all.sh"
    echo ""
    echo "View logs:"
    echo "  docker logs -f aeon-ner-api"
    echo "  docker logs -f aeon-query-api"
}

# Main execution
main() {
    log_info "Starting AEON Backend API environment setup..."
    log_info "Project root: $PROJECT_ROOT"

    check_requirements
    setup_directories
    setup_env_file
    make_scripts_executable

    read -p "Install Python dependencies? (y/n): " install_deps
    if [[ $install_deps =~ ^[Yy]$ ]]; then
        install_python_deps
    fi

    setup_neo4j

    display_summary
}

main "$@"
