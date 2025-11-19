#!/bin/bash
#
# deploy-to-dev.sh - Main deployment script for agent optimization implementations
# Created: 2025-11-12
# Purpose: Automated deployment with validation and rollback support
#

set -euo pipefail

# ═══════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/jim/2_OXOT_Projects_Dev/tests"
LOG_DIR="/var/log/deployment"
LOG_FILE="${LOG_DIR}/deploy-$(date +%Y%m%d-%H%M%S).log"
REPO_URL="https://github.com/yourusername/agent-optimization.git"
BACKUP_DIR="${PROJECT_ROOT}/backups"
DRY_RUN=false

# ═══════════════════════════════════════════════════
# COLOR CODES
# ═══════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════
# LOGGING FUNCTIONS
# ═══════════════════════════════════════════════════

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "${LOG_FILE}"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*" | tee -a "${LOG_FILE}"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "${LOG_FILE}"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" | tee -a "${LOG_FILE}"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "${LOG_FILE}"
}

log_step() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}[STEP]${NC} $*"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}\n"
}

# ═══════════════════════════════════════════════════
# ERROR HANDLING
# ═══════════════════════════════════════════════════

cleanup_on_error() {
    log_error "Deployment failed! Rolling back changes..."
    if [[ -d "${BACKUP_DIR}/last_known_good" ]]; then
        log_info "Restoring from backup..."
        cp -r "${BACKUP_DIR}/last_known_good/"* "${PROJECT_ROOT}/" 2>/dev/null || true
        log_success "Backup restored"
    fi
    exit 1
}

trap cleanup_on_error ERR

# ═══════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════

validate_environment() {
    log_step "Validating Environment"

    # Check if running as appropriate user
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root is not recommended"
    fi

    # Check required commands
    local required_commands=("git" "node" "npm" "tsc" "jest")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Required command not found: $cmd"
            exit 1
        fi
        log_success "Found: $cmd"
    done

    # Check Node.js version
    local node_version=$(node --version | cut -d'v' -f2)
    local required_version="18.0.0"
    if [[ "$(printf '%s\n' "$required_version" "$node_version" | sort -V | head -n1)" != "$required_version" ]]; then
        log_error "Node.js version $node_version is below required $required_version"
        exit 1
    fi
    log_success "Node.js version: $node_version"

    # Check disk space (require at least 1GB free)
    local available_space=$(df "${PROJECT_ROOT}" | awk 'NR==2 {print $4}')
    if [[ $available_space -lt 1048576 ]]; then
        log_error "Insufficient disk space. Required: 1GB, Available: $((available_space/1024))MB"
        exit 1
    fi
    log_success "Disk space: $((available_space/1024/1024))GB available"

    # Validate project root exists
    if [[ ! -d "${PROJECT_ROOT}" ]]; then
        log_error "Project root does not exist: ${PROJECT_ROOT}"
        exit 1
    fi
    log_success "Project root validated: ${PROJECT_ROOT}"
}

# ═══════════════════════════════════════════════════
# BACKUP FUNCTIONS
# ═══════════════════════════════════════════════════

create_backup() {
    log_step "Creating Backup"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create backup at: ${BACKUP_DIR}/backup-$(date +%Y%m%d-%H%M%S)"
        return 0
    fi

    mkdir -p "${BACKUP_DIR}"
    local backup_name="backup-$(date +%Y%m%d-%H%M%S)"

    # Create backup of current state
    log_info "Backing up current deployment..."
    cp -r "${PROJECT_ROOT}" "${BACKUP_DIR}/${backup_name}" 2>/dev/null || {
        log_warning "Partial backup created (some files may be in use)"
    }

    # Create symlink to last known good
    rm -f "${BACKUP_DIR}/last_known_good"
    ln -s "${BACKUP_DIR}/${backup_name}" "${BACKUP_DIR}/last_known_good"

    log_success "Backup created: ${backup_name}"

    # Clean old backups (keep last 5)
    log_info "Cleaning old backups..."
    ls -t "${BACKUP_DIR}" | grep "backup-" | tail -n +6 | xargs -I {} rm -rf "${BACKUP_DIR}/{}" 2>/dev/null || true
}

# ═══════════════════════════════════════════════════
# DEPLOYMENT FUNCTIONS
# ═══════════════════════════════════════════════════

pull_from_repository() {
    log_step "Pulling from Repository"

    cd "${PROJECT_ROOT}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would pull from: ${REPO_URL}"
        return 0
    fi

    # Check if git repository exists
    if [[ -d ".git" ]]; then
        log_info "Fetching latest changes..."
        git fetch origin

        local current_branch=$(git rev-parse --abbrev-ref HEAD)
        log_info "Current branch: ${current_branch}"

        # Check for uncommitted changes
        if [[ -n $(git status -s) ]]; then
            log_warning "Uncommitted changes detected. Stashing..."
            git stash save "Auto-stash before deployment $(date +%Y%m%d-%H%M%S)"
        fi

        # Pull latest changes
        log_info "Pulling latest changes..."
        git pull origin "${current_branch}"

        local commit_hash=$(git rev-parse --short HEAD)
        log_success "Updated to commit: ${commit_hash}"
    else
        log_info "No git repository found. Skipping pull..."
    fi
}

install_dependencies() {
    log_step "Installing Dependencies"

    cd "${PROJECT_ROOT}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would run: npm ci"
        return 0
    fi

    if [[ -f "package-lock.json" ]]; then
        log_info "Running npm ci for clean install..."
        npm ci --silent
    else
        log_info "Running npm install..."
        npm install --silent
    fi

    log_success "Dependencies installed"
}

compile_typescript() {
    log_step "Compiling TypeScript"

    cd "${PROJECT_ROOT}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would run: npm run build"
        return 0
    fi

    # Clean previous build
    if [[ -d "dist" ]]; then
        log_info "Cleaning previous build..."
        rm -rf dist
    fi

    # Run TypeScript compiler
    log_info "Compiling TypeScript..."
    if npm run build 2>&1 | tee -a "${LOG_FILE}"; then
        log_success "TypeScript compilation successful"
    else
        log_error "TypeScript compilation failed"
        exit 1
    fi

    # Verify output
    if [[ ! -d "dist" ]] || [[ -z "$(ls -A dist)" ]]; then
        log_error "Build output directory is empty"
        exit 1
    fi

    log_success "Build artifacts created in dist/"
}

run_tests() {
    log_step "Running Tests"

    cd "${PROJECT_ROOT}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would run: npm test"
        return 0
    fi

    log_info "Executing test suite..."

    # Run tests with coverage
    if npm test -- --coverage --silent 2>&1 | tee -a "${LOG_FILE}"; then
        log_success "All tests passed"
    else
        log_error "Tests failed. Deployment aborted."
        exit 1
    fi

    # Check coverage threshold (optional)
    if [[ -f "coverage/coverage-summary.json" ]]; then
        local coverage=$(node -pe "JSON.parse(require('fs').readFileSync('coverage/coverage-summary.json')).total.lines.pct")
        log_info "Code coverage: ${coverage}%"

        if (( $(echo "$coverage < 70" | bc -l) )); then
            log_warning "Coverage below 70% threshold"
        fi
    fi
}

deploy_implementations() {
    log_step "Deploying Implementations"

    cd "${PROJECT_ROOT}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would deploy implementations"
        return 0
    fi

    # Copy build artifacts to deployment location
    local deploy_locations=(
        "/home/jim/2_OXOT_Projects_Dev/implementations"
        "/home/jim/.local/share/agent-optimization"
    )

    for location in "${deploy_locations[@]}"; do
        if [[ -d "$location" ]]; then
            log_info "Deploying to: $location"
            mkdir -p "$location"
            cp -r dist/* "$location/"
            log_success "Deployed to $location"
        fi
    done

    # Set proper permissions
    log_info "Setting file permissions..."
    find dist -type f -name "*.js" -exec chmod 644 {} \;
    find dist -type d -exec chmod 755 {} \;

    log_success "Implementations deployed successfully"
}

verify_deployment() {
    log_step "Verifying Deployment"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would verify deployment"
        return 0
    fi

    # Run health check script
    if [[ -f "${SCRIPT_DIR}/health-check.sh" ]]; then
        log_info "Running health checks..."
        bash "${SCRIPT_DIR}/health-check.sh" --quick
    else
        log_warning "Health check script not found"
    fi

    # Verify key files exist
    local required_files=(
        "dist/agent-optimization.js"
        "dist/performance-benchmarks.js"
        "package.json"
    )

    for file in "${required_files[@]}"; do
        if [[ -f "${PROJECT_ROOT}/${file}" ]]; then
            log_success "Verified: ${file}"
        else
            log_error "Missing required file: ${file}"
            exit 1
        fi
    done

    log_success "Deployment verification complete"
}

# ═══════════════════════════════════════════════════
# NOTIFICATION FUNCTIONS
# ═══════════════════════════════════════════════════

send_notification() {
    local status="$1"
    local message="$2"

    # Log to file
    log "NOTIFICATION" "${status}: ${message}"

    # Send email notification (if configured)
    if command -v mail &> /dev/null && [[ -n "${NOTIFY_EMAIL:-}" ]]; then
        echo "${message}" | mail -s "Deployment ${status}" "${NOTIFY_EMAIL}"
    fi

    # Send Slack notification (if configured)
    if [[ -n "${SLACK_WEBHOOK_URL:-}" ]]; then
        local color="good"
        [[ "$status" == "FAILED" ]] && color="danger"

        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"Deployment ${status}\",\"attachments\":[{\"color\":\"${color}\",\"text\":\"${message}\"}]}" \
            "${SLACK_WEBHOOK_URL}" 2>/dev/null || true
    fi
}

# ═══════════════════════════════════════════════════
# MAIN DEPLOYMENT FLOW
# ═══════════════════════════════════════════════════

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                log_warning "DRY-RUN MODE ENABLED - No changes will be made"
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --dry-run    Simulate deployment without making changes"
                echo "  --help       Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Create log directory
    mkdir -p "${LOG_DIR}"

    # Start deployment
    local start_time=$(date +%s)
    log_info "=========================================="
    log_info "Deployment started at $(date)"
    log_info "Log file: ${LOG_FILE}"
    log_info "=========================================="

    # Execute deployment steps
    validate_environment
    create_backup
    pull_from_repository
    install_dependencies
    compile_typescript
    run_tests
    deploy_implementations
    verify_deployment

    # Calculate duration
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    # Success notification
    log_success "=========================================="
    log_success "Deployment completed successfully!"
    log_success "Duration: ${duration} seconds"
    log_success "=========================================="

    send_notification "SUCCESS" "Deployment completed successfully in ${duration} seconds"
}

# ═══════════════════════════════════════════════════
# SCRIPT ENTRY POINT
# ═══════════════════════════════════════════════════

main "$@"
