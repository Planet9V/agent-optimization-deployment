#!/bin/bash
#
# NVD Daily Sync - Cron Wrapper Script
#
# File: daily_sync.sh
# Created: 2025-11-01
# Version: 1.0.0
# Author: Automation Agent
# Purpose: Shell wrapper for daily NVD CVE sync with enrichment
# Status: ACTIVE
#
# Cron schedule recommendation:
# 0 2 * * * /path/to/automation/daily_sync.sh >> /var/log/nvd_sync_cron.log 2>&1

set -euo pipefail

# ============================================
# Configuration
# ============================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.yaml"
LOG_DIR="${SCRIPT_DIR}/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Log files
SYNC_LOG="${LOG_DIR}/nvd_sync_${TIMESTAMP}.log"
ENRICHMENT_LOG="${LOG_DIR}/enrichment_${TIMESTAMP}.log"
CRON_LOG="${LOG_DIR}/cron_${TIMESTAMP}.log"

# Python executable (adjust if using virtual environment)
PYTHON="${SCRIPT_DIR}/venv/bin/python3"
if [ ! -f "$PYTHON" ]; then
    PYTHON="python3"
fi

# Email for notifications (optional)
NOTIFICATION_EMAIL="${NOTIFICATION_EMAIL:-}"

# ============================================
# Functions
# ============================================

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "${CRON_LOG}"
}

error() {
    echo "[ERROR] [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "${CRON_LOG}" >&2
}

send_notification() {
    local subject="$1"
    local message="$2"

    if [ -n "$NOTIFICATION_EMAIL" ]; then
        echo "$message" | mail -s "$subject" "$NOTIFICATION_EMAIL"
    fi
}

cleanup_old_logs() {
    # Keep logs for 30 days
    find "$LOG_DIR" -name "*.log" -type f -mtime +30 -delete
    log "Cleaned up logs older than 30 days"
}

# ============================================
# Pre-flight Checks
# ============================================

preflight_checks() {
    log "Running pre-flight checks..."

    # Check if configuration file exists
    if [ ! -f "$CONFIG_FILE" ]; then
        error "Configuration file not found: $CONFIG_FILE"
        exit 1
    fi

    # Create log directory if it doesn't exist
    mkdir -p "$LOG_DIR"

    # Check Python installation
    if ! command -v "$PYTHON" &> /dev/null; then
        error "Python not found: $PYTHON"
        exit 1
    fi

    # Check required Python packages
    if ! "$PYTHON" -c "import requests, neo4j, yaml" 2>/dev/null; then
        error "Required Python packages not installed. Run: pip install -r requirements.txt"
        exit 1
    fi

    # Check environment variables
    if [ -z "${NVD_API_KEY:-}" ]; then
        log "WARNING: NVD_API_KEY not set. Rate limit: 5 requests/30s (consider setting API key for 50 req/30s)"
    fi

    if [ -z "${VULNCHECK_API_TOKEN:-}" ]; then
        log "WARNING: VULNCHECK_API_TOKEN not set. XDB enrichment will be skipped."
    fi

    log "Pre-flight checks completed successfully"
}

# ============================================
# Main Execution
# ============================================

main() {
    local exit_code=0

    log "=========================================="
    log "NVD Daily Sync - Starting"
    log "=========================================="

    # Run pre-flight checks
    preflight_checks

    # Step 1: Sync CVEs from NVD
    log "Step 1/3: Syncing CVEs from NVD API..."

    if "$PYTHON" "${SCRIPT_DIR}/nvd_daily_sync.py" --config "$CONFIG_FILE" >> "$SYNC_LOG" 2>&1; then
        log "NVD sync completed successfully"
    else
        exit_code=$?
        error "NVD sync failed with exit code: $exit_code"
        send_notification "NVD Sync Failed" "$(tail -n 50 "$SYNC_LOG")"
    fi

    # Step 2: Run enrichment pipeline
    log "Step 2/3: Running enrichment pipeline..."

    if "$PYTHON" "${SCRIPT_DIR}/enrichment_pipeline.py" --config "$CONFIG_FILE" >> "$ENRICHMENT_LOG" 2>&1; then
        log "Enrichment pipeline completed successfully"
    else
        local enrich_exit=$?
        error "Enrichment pipeline failed with exit code: $enrich_exit"
        send_notification "CVE Enrichment Failed" "$(tail -n 50 "$ENRICHMENT_LOG")"
        exit_code=$enrich_exit
    fi

    # Step 3: Cleanup old logs
    log "Step 3/3: Cleaning up old logs..."
    cleanup_old_logs

    # Extract metrics from logs
    log "=========================================="
    log "Daily Sync Summary"
    log "=========================================="

    # NVD Sync metrics
    if [ -f "$SYNC_LOG" ]; then
        grep -E "CVEs (fetched|created|updated):" "$SYNC_LOG" | tee -a "${CRON_LOG}" || true
        grep "Duration:" "$SYNC_LOG" | head -1 | tee -a "${CRON_LOG}" || true
    fi

    # Enrichment metrics
    if [ -f "$ENRICHMENT_LOG" ]; then
        grep -E "(EPSS|KEV|Priority) (enriched|flagged|calculated):" "$ENRICHMENT_LOG" | tee -a "${CRON_LOG}" || true
        grep "Duration:" "$ENRICHMENT_LOG" | head -1 | tee -a "${CRON_LOG}" || true
    fi

    log "=========================================="

    # Send success notification if configured
    if [ $exit_code -eq 0 ] && [ -n "$NOTIFICATION_EMAIL" ]; then
        send_notification "NVD Daily Sync Successful" "Daily sync and enrichment completed successfully. See attached logs for details."
    fi

    log "NVD Daily Sync - Completed with exit code: $exit_code"

    return $exit_code
}

# Execute main function
main
exit $?
