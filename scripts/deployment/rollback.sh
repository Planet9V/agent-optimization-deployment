#!/bin/bash
#
# rollback.sh - Emergency rollback script for agent optimization deployment
# Created: 2025-11-12
# Purpose: Immediate rollback to previous stable version with state preservation
#

set -euo pipefail

# ═══════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/jim/2_OXOT_Projects_Dev/tests"
BACKUP_DIR="${PROJECT_ROOT}/backups"
LOG_DIR="/var/log/deployment"
ROLLBACK_LOG="${LOG_DIR}/rollback-$(date +%Y%m%d-%H%M%S).log"
METRICS_BACKUP_DIR="${BACKUP_DIR}/metrics"
DB_BACKUP_DIR="${BACKUP_DIR}/database"
DRY_RUN=false
FORCE=false
TARGET_VERSION=""

# ═══════════════════════════════════════════════════
# COLOR CODES
# ═══════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# ═══════════════════════════════════════════════════
# LOGGING FUNCTIONS
# ═══════════════════════════════════════════════════

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*" | tee -a "${ROLLBACK_LOG}"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "${ROLLBACK_LOG}"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" | tee -a "${ROLLBACK_LOG}"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "${ROLLBACK_LOG}"
}

log_critical() {
    echo -e "${MAGENTA}[CRITICAL]${NC} $*" | tee -a "${ROLLBACK_LOG}"
}

log_step() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}[STEP]${NC} $*"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}\n"
}

# ═══════════════════════════════════════════════════
# ERROR HANDLING
# ═══════════════════════════════════════════════════

rollback_failed() {
    log_critical "ROLLBACK FAILED! System may be in inconsistent state."
    log_critical "Manual intervention required."
    log_critical "Backup location: ${BACKUP_DIR}"
    log_critical "Log file: ${ROLLBACK_LOG}"
    exit 2
}

trap rollback_failed ERR

# ═══════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════

validate_environment() {
    log_step "Validating Environment"

    # Check if backup directory exists
    if [[ ! -d "${BACKUP_DIR}" ]]; then
        log_error "Backup directory does not exist: ${BACKUP_DIR}"
        exit 1
    fi
    log_success "Backup directory found"

    # Check if last_known_good exists
    if [[ ! -L "${BACKUP_DIR}/last_known_good" ]] && [[ -z "$TARGET_VERSION" ]]; then
        log_error "No last_known_good backup found and no target version specified"
        log_info "Available backups:"
        ls -lt "${BACKUP_DIR}" | grep "backup-" | head -5
        exit 1
    fi

    # Check disk space
    local available_space=$(df "${PROJECT_ROOT}" | awk 'NR==2 {print $4}')
    if [[ $available_space -lt 524288 ]]; then  # 512MB
        log_warning "Low disk space: $((available_space/1024))MB available"
        if [[ "$FORCE" != "true" ]]; then
            log_error "Insufficient disk space. Use --force to override."
            exit 1
        fi
    fi
    log_success "Disk space validated"
}

list_available_backups() {
    log_step "Available Backups"

    if [[ ! -d "${BACKUP_DIR}" ]]; then
        log_error "No backups directory found"
        return 1
    fi

    echo ""
    echo "Available rollback targets:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    local count=0
    for backup in $(ls -t "${BACKUP_DIR}" | grep "backup-"); do
        count=$((count + 1))
        local backup_path="${BACKUP_DIR}/${backup}"
        local backup_date=$(stat -c %y "$backup_path" 2>/dev/null | cut -d' ' -f1,2)
        local backup_size=$(du -sh "$backup_path" 2>/dev/null | cut -f1)

        echo "  ${count}. ${backup}"
        echo "     Date: ${backup_date}"
        echo "     Size: ${backup_size}"

        # Check if this is the last_known_good
        if [[ -L "${BACKUP_DIR}/last_known_good" ]]; then
            local lkg=$(readlink "${BACKUP_DIR}/last_known_good")
            if [[ "$lkg" == *"$backup"* ]]; then
                echo -e "     ${GREEN}[LAST KNOWN GOOD]${NC}"
            fi
        fi
        echo ""

        [[ $count -ge 5 ]] && break
    done

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ═══════════════════════════════════════════════════
# BACKUP PRESERVATION FUNCTIONS
# ═══════════════════════════════════════════════════

preserve_current_state() {
    log_step "Preserving Current State"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would preserve current state"
        return 0
    fi

    local emergency_backup="${BACKUP_DIR}/emergency-$(date +%Y%m%d-%H%M%S)"

    log_info "Creating emergency backup before rollback..."
    mkdir -p "$emergency_backup"

    # Backup current deployment
    log_info "Backing up current files..."
    cp -r "${PROJECT_ROOT}" "$emergency_backup/" 2>/dev/null || {
        log_warning "Some files could not be backed up"
    }

    log_success "Emergency backup created: $emergency_backup"
}

preserve_logs() {
    log_step "Preserving Logs"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would preserve logs"
        return 0
    fi

    local logs_backup="${BACKUP_DIR}/logs-$(date +%Y%m%d-%H%M%S)"

    log_info "Backing up logs..."
    mkdir -p "$logs_backup"

    # Copy deployment logs
    if [[ -d "${LOG_DIR}" ]]; then
        cp -r "${LOG_DIR}"/* "$logs_backup/" 2>/dev/null || true
    fi

    # Copy application logs
    if [[ -d "${PROJECT_ROOT}/logs" ]]; then
        cp -r "${PROJECT_ROOT}/logs"/* "$logs_backup/" 2>/dev/null || true
    fi

    log_success "Logs preserved: $logs_backup"
}

preserve_metrics() {
    log_step "Preserving Metrics"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would preserve metrics"
        return 0
    fi

    local metrics_dir="${PROJECT_ROOT}/monitoring/metrics"

    if [[ -d "$metrics_dir" ]]; then
        log_info "Backing up metrics..."
        mkdir -p "${METRICS_BACKUP_DIR}"

        local metrics_backup="${METRICS_BACKUP_DIR}/metrics-$(date +%Y%m%d-%H%M%S)"
        cp -r "$metrics_dir" "$metrics_backup" 2>/dev/null || {
            log_warning "Some metrics could not be backed up"
        }

        log_success "Metrics preserved: $metrics_backup"
    else
        log_info "No metrics directory found, skipping"
    fi
}

preserve_database() {
    log_step "Preserving Database State"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would preserve database state"
        return 0
    fi

    # Check for database files
    local db_files=()

    # SQLite databases
    if compgen -G "${PROJECT_ROOT}/*.db" > /dev/null; then
        db_files+=("${PROJECT_ROOT}"/*.db)
    fi

    if [[ ${#db_files[@]} -gt 0 ]]; then
        log_info "Backing up database files..."
        mkdir -p "${DB_BACKUP_DIR}"

        local db_backup="${DB_BACKUP_DIR}/db-$(date +%Y%m%d-%H%M%S)"
        mkdir -p "$db_backup"

        for db_file in "${db_files[@]}"; do
            cp "$db_file" "$db_backup/" 2>/dev/null || {
                log_warning "Could not backup: $(basename "$db_file")"
            }
            log_success "Backed up: $(basename "$db_file")"
        done
    else
        log_info "No database files found, skipping"
    fi
}

# ═══════════════════════════════════════════════════
# ROLLBACK FUNCTIONS
# ═══════════════════════════════════════════════════

determine_rollback_target() {
    log_step "Determining Rollback Target"

    if [[ -n "$TARGET_VERSION" ]]; then
        ROLLBACK_TARGET="${BACKUP_DIR}/${TARGET_VERSION}"

        if [[ ! -d "$ROLLBACK_TARGET" ]]; then
            log_error "Specified target does not exist: $TARGET_VERSION"
            exit 1
        fi

        log_info "Using specified target: $TARGET_VERSION"
    else
        # Use last_known_good
        if [[ -L "${BACKUP_DIR}/last_known_good" ]]; then
            ROLLBACK_TARGET=$(readlink -f "${BACKUP_DIR}/last_known_good")
            log_info "Using last_known_good: $(basename "$ROLLBACK_TARGET")"
        else
            log_error "No rollback target available"
            exit 1
        fi
    fi

    log_success "Rollback target: $ROLLBACK_TARGET"
}

stop_services() {
    log_step "Stopping Services"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would stop services"
        return 0
    fi

    # Stop monitoring dashboard
    if [[ -f "${PROJECT_ROOT}/monitoring/dashboard.pid" ]]; then
        local pid=$(cat "${PROJECT_ROOT}/monitoring/dashboard.pid")
        if kill -0 "$pid" 2>/dev/null; then
            log_info "Stopping monitoring dashboard (PID: $pid)..."
            kill "$pid" 2>/dev/null || true
            sleep 2
            log_success "Monitoring dashboard stopped"
        fi
    fi

    # Stop any Node.js processes in project directory
    log_info "Stopping Node.js processes..."
    pkill -f "${PROJECT_ROOT}" 2>/dev/null || true

    sleep 2
    log_success "Services stopped"
}

restore_files() {
    log_step "Restoring Files from Backup"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would restore from: $ROLLBACK_TARGET"
        return 0
    fi

    log_info "Restoring files from: $ROLLBACK_TARGET"

    # Create temporary staging area
    local staging="${PROJECT_ROOT}/.rollback-staging"
    mkdir -p "$staging"

    # Copy files to staging
    log_info "Copying files to staging area..."
    cp -r "${ROLLBACK_TARGET}/tests/"* "$staging/" 2>/dev/null || {
        log_error "Failed to copy files from backup"
        exit 1
    }

    # Remove current deployment (except backups and logs)
    log_info "Removing current deployment..."
    find "${PROJECT_ROOT}" -mindepth 1 -maxdepth 1 \
        ! -name 'backups' \
        ! -name 'logs' \
        ! -name '.rollback-staging' \
        -exec rm -rf {} + 2>/dev/null || true

    # Move staged files to project root
    log_info "Installing rolled-back version..."
    mv "$staging"/* "${PROJECT_ROOT}/" 2>/dev/null || {
        log_error "Failed to move files from staging"
        exit 1
    }

    # Cleanup staging
    rm -rf "$staging"

    log_success "Files restored successfully"
}

restore_database() {
    log_step "Restoring Database State"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would restore database"
        return 0
    fi

    # Find most recent database backup
    local latest_db_backup=$(ls -t "${DB_BACKUP_DIR}" 2>/dev/null | head -1)

    if [[ -n "$latest_db_backup" ]]; then
        log_info "Restoring database from: $latest_db_backup"

        cp "${DB_BACKUP_DIR}/${latest_db_backup}"/*.db "${PROJECT_ROOT}/" 2>/dev/null || {
            log_warning "No database files to restore"
            return 0
        }

        log_success "Database restored"
    else
        log_info "No database backups found, skipping"
    fi
}

reinstall_dependencies() {
    log_step "Reinstalling Dependencies"

    cd "${PROJECT_ROOT}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would reinstall dependencies"
        return 0
    fi

    if [[ -f "package.json" ]]; then
        log_info "Installing dependencies..."

        # Remove node_modules and package-lock
        rm -rf node_modules package-lock.json 2>/dev/null || true

        # Fresh install
        npm install --silent 2>&1 | tee -a "${ROLLBACK_LOG}"

        log_success "Dependencies reinstalled"
    else
        log_warning "No package.json found"
    fi
}

rebuild_project() {
    log_step "Rebuilding Project"

    cd "${PROJECT_ROOT}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would rebuild project"
        return 0
    fi

    if [[ -f "package.json" ]] && grep -q '"build"' package.json; then
        log_info "Running build..."

        npm run build 2>&1 | tee -a "${ROLLBACK_LOG}" || {
            log_error "Build failed"
            exit 1
        }

        log_success "Project rebuilt successfully"
    else
        log_info "No build script found, skipping"
    fi
}

restart_services() {
    log_step "Restarting Services"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would restart services"
        return 0
    fi

    # Start monitoring if script exists
    if [[ -f "${PROJECT_ROOT}/monitoring/start-monitoring.sh" ]]; then
        log_info "Starting monitoring dashboard..."
        bash "${PROJECT_ROOT}/monitoring/start-monitoring.sh" 2>&1 | tee -a "${ROLLBACK_LOG}"
        log_success "Monitoring dashboard started"
    fi

    log_success "Services restarted"
}

verify_rollback() {
    log_step "Verifying Rollback"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would verify rollback"
        return 0
    fi

    # Check critical files exist
    local critical_files=(
        "package.json"
        "tsconfig.json"
    )

    for file in "${critical_files[@]}"; do
        if [[ ! -f "${PROJECT_ROOT}/${file}" ]]; then
            log_error "Critical file missing after rollback: $file"
            exit 1
        fi
        log_success "Verified: $file"
    done

    # Run health check if available
    if [[ -f "${SCRIPT_DIR}/health-check.sh" ]]; then
        log_info "Running health checks..."
        bash "${SCRIPT_DIR}/health-check.sh" --post-rollback || {
            log_warning "Health checks reported issues"
        }
    fi

    log_success "Rollback verification complete"
}

# ═══════════════════════════════════════════════════
# NOTIFICATION FUNCTIONS
# ═══════════════════════════════════════════════════

send_notification() {
    local status="$1"
    local message="$2"

    # Log notification
    log_info "NOTIFICATION: ${status} - ${message}"

    # Email notification (if configured)
    if command -v mail &> /dev/null && [[ -n "${NOTIFY_EMAIL:-}" ]]; then
        echo "${message}" | mail -s "Rollback ${status}" "${NOTIFY_EMAIL}"
    fi

    # Slack notification (if configured)
    if [[ -n "${SLACK_WEBHOOK_URL:-}" ]]; then
        local color="warning"
        [[ "$status" == "SUCCESS" ]] && color="good"
        [[ "$status" == "FAILED" ]] && color="danger"

        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"Rollback ${status}\",\"attachments\":[{\"color\":\"${color}\",\"text\":\"${message}\"}]}" \
            "${SLACK_WEBHOOK_URL}" 2>/dev/null || true
    fi
}

# ═══════════════════════════════════════════════════
# MAIN ROLLBACK FLOW
# ═══════════════════════════════════════════════════

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                log_warning "DRY-RUN MODE ENABLED"
                shift
                ;;
            --force)
                FORCE=true
                log_warning "FORCE MODE ENABLED"
                shift
                ;;
            --list)
                list_available_backups
                exit 0
                ;;
            --to)
                TARGET_VERSION="$2"
                shift 2
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --dry-run     Simulate rollback without making changes"
                echo "  --force       Force rollback even with warnings"
                echo "  --list        List available backup versions"
                echo "  --to VERSION  Rollback to specific version"
                echo "  --help        Show this help message"
                echo ""
                echo "Examples:"
                echo "  $0 --list                    # Show available backups"
                echo "  $0                           # Rollback to last known good"
                echo "  $0 --to backup-20251112-1045 # Rollback to specific version"
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

    # Start rollback
    local start_time=$(date +%s)
    log_critical "=========================================="
    log_critical "EMERGENCY ROLLBACK INITIATED"
    log_critical "Time: $(date)"
    log_critical "Log: ${ROLLBACK_LOG}"
    log_critical "=========================================="

    # Confirmation prompt (unless force mode)
    if [[ "$FORCE" != "true" ]] && [[ "$DRY_RUN" != "true" ]]; then
        echo ""
        read -p "$(echo -e "${YELLOW}Are you sure you want to rollback? [yes/NO]:${NC} ")" -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
            log_info "Rollback cancelled by user"
            exit 0
        fi
    fi

    # Execute rollback steps
    validate_environment
    determine_rollback_target
    preserve_current_state
    preserve_logs
    preserve_metrics
    preserve_database
    stop_services
    restore_files
    restore_database
    reinstall_dependencies
    rebuild_project
    restart_services
    verify_rollback

    # Calculate duration
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    # Success notification
    log_success "=========================================="
    log_success "ROLLBACK COMPLETED SUCCESSFULLY"
    log_success "Duration: ${duration} seconds"
    log_success "Target: $(basename "$ROLLBACK_TARGET")"
    log_success "=========================================="

    send_notification "SUCCESS" "Rollback completed successfully to $(basename "$ROLLBACK_TARGET") in ${duration} seconds"
}

# ═══════════════════════════════════════════════════
# SCRIPT ENTRY POINT
# ═══════════════════════════════════════════════════

main "$@"
