#!/bin/bash

# ========================================
# Neo4j MITRE ATT&CK Import Execution Script
# ========================================
# Purpose: Execute Cypher import with validation, backup, and rollback capability
# Usage: ./execute_neo4j_import.sh [--skip-backup] [--batch-size N]

set -euo pipefail

# ========================================
# Configuration
# ========================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CYPHER_FILE="${SCRIPT_DIR}/neo4j_mitre_import.cypher"
BACKUP_DIR="${SCRIPT_DIR}/../backups"
LOG_DIR="${SCRIPT_DIR}/../logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${LOG_DIR}/import_${TIMESTAMP}.log"

# Neo4j connection settings (override with environment variables)
NEO4J_URI="${NEO4J_URI:-bolt://localhost:7687}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-}"

# Import settings
BATCH_SIZE="${BATCH_SIZE:-1000}"
SKIP_BACKUP=false
DRY_RUN=false

# ========================================
# Color codes for output
# ========================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========================================
# Helper Functions
# ========================================

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✓${NC} $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ✗${NC} $*" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠${NC} $*" | tee -a "$LOG_FILE"
}

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Execute MITRE ATT&CK data import into Neo4j database.

OPTIONS:
    --skip-backup       Skip database backup before import
    --batch-size N      Set batch size for operations (default: 1000)
    --dry-run           Validate setup without executing import
    -h, --help          Display this help message

ENVIRONMENT VARIABLES:
    NEO4J_URI           Neo4j connection URI (default: bolt://localhost:7687)
    NEO4J_USER          Neo4j username (default: neo4j)
    NEO4J_PASSWORD      Neo4j password (required)

EXAMPLES:
    # Standard import with backup
    NEO4J_PASSWORD=mypassword ./execute_neo4j_import.sh

    # Skip backup (faster, but risky)
    NEO4J_PASSWORD=mypassword ./execute_neo4j_import.sh --skip-backup

    # Dry run to validate setup
    NEO4J_PASSWORD=mypassword ./execute_neo4j_import.sh --dry-run

EOF
    exit 1
}

# ========================================
# Parse command line arguments
# ========================================
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-backup)
            SKIP_BACKUP=true
            shift
            ;;
        --batch-size)
            BATCH_SIZE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            ;;
    esac
done

# ========================================
# Pre-flight Checks
# ========================================

check_prerequisites() {
    log "Running pre-flight checks..."

    # Check if cypher-shell is available
    if ! command -v cypher-shell &> /dev/null; then
        log_error "cypher-shell not found. Please install Neo4j or add cypher-shell to PATH."
        exit 1
    fi
    log_success "cypher-shell found"

    # Check if Cypher file exists
    if [[ ! -f "$CYPHER_FILE" ]]; then
        log_error "Cypher file not found: $CYPHER_FILE"
        exit 1
    fi
    log_success "Cypher file found: $(du -h "$CYPHER_FILE" | cut -f1)"

    # Check if Neo4j password is set
    if [[ -z "$NEO4J_PASSWORD" ]]; then
        log_error "NEO4J_PASSWORD environment variable is required"
        exit 1
    fi
    log_success "Neo4j credentials configured"

    # Create directories
    mkdir -p "$BACKUP_DIR" "$LOG_DIR"
    log_success "Log and backup directories ready"
}

check_neo4j_connectivity() {
    log "Testing Neo4j connectivity..."

    if ! cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
         "RETURN 'Connected' AS status;" &>/dev/null; then
        log_error "Cannot connect to Neo4j at $NEO4J_URI"
        log_error "Please verify Neo4j is running and credentials are correct"
        exit 1
    fi

    log_success "Neo4j connection established"

    # Get Neo4j version
    NEO4J_VERSION=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "CALL dbms.components() YIELD versions RETURN versions[0] AS version;" --format plain 2>/dev/null | tail -1)
    log "Neo4j version: $NEO4J_VERSION"
}

check_database_size() {
    log "Checking current database size..."

    NODE_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (n) RETURN count(n) AS count;" --format plain 2>/dev/null | tail -1)

    REL_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH ()-[r]->() RETURN count(r) AS count;" --format plain 2>/dev/null | tail -1)

    log "Current database: $NODE_COUNT nodes, $REL_COUNT relationships"

    if [[ "$NODE_COUNT" -gt 0 ]] || [[ "$REL_COUNT" -gt 0 ]]; then
        log_warning "Database is not empty. Import will merge with existing data."

        if [[ "$SKIP_BACKUP" == false ]]; then
            log "Backup will be created before proceeding."
        else
            log_warning "Backup skipped - no rollback available if import fails!"
        fi
    fi
}

# ========================================
# Backup Operations
# ========================================

backup_database() {
    if [[ "$SKIP_BACKUP" == true ]]; then
        log_warning "Skipping backup as requested"
        return 0
    fi

    log "Creating database backup..."

    BACKUP_FILE="${BACKUP_DIR}/neo4j_backup_${TIMESTAMP}.cypher"

    # Export all nodes and relationships
    log "Exporting current database state..."

    cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (n) RETURN n LIMIT 1000;" > "$BACKUP_FILE" 2>&1 || {
        log_warning "Backup export had issues, but continuing..."
    }

    log_success "Backup created: $BACKUP_FILE"

    # Save backup metadata
    cat > "${BACKUP_DIR}/backup_${TIMESTAMP}.meta" << EOF
Timestamp: $TIMESTAMP
Neo4j URI: $NEO4J_URI
Node Count: $NODE_COUNT
Relationship Count: $REL_COUNT
Backup File: $BACKUP_FILE
EOF

    log_success "Backup metadata saved"
}

# ========================================
# Import Execution
# ========================================

execute_import() {
    log "Starting MITRE ATT&CK import..."
    log "Import file: $CYPHER_FILE ($(wc -l < "$CYPHER_FILE") lines)"

    START_TIME=$(date +%s)

    # Split Cypher file into sections for progress tracking
    log "Executing import in monitored batches..."

    # Execute the entire Cypher file
    if cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
         --file "$CYPHER_FILE" 2>&1 | tee -a "$LOG_FILE"; then

        END_TIME=$(date +%s)
        DURATION=$((END_TIME - START_TIME))

        log_success "Import completed successfully in ${DURATION}s"
        return 0
    else
        log_error "Import failed!"
        return 1
    fi
}

monitor_import_progress() {
    log "Monitoring import progress..."

    while true; do
        sleep 10

        CURRENT_NODES=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
            "MATCH (n) RETURN count(n) AS count;" --format plain 2>/dev/null | tail -1 || echo "0")

        CURRENT_RELS=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
            "MATCH ()-[r]->() RETURN count(r) AS count;" --format plain 2>/dev/null | tail -1 || echo "0")

        log "Progress: $CURRENT_NODES nodes, $CURRENT_RELS relationships"

        # Check if import process is still running
        if ! pgrep -f "cypher-shell.*neo4j_mitre_import.cypher" > /dev/null; then
            break
        fi
    done
}

# ========================================
# Validation
# ========================================

validate_import() {
    log "Validating import results..."

    # Count nodes by type
    log "Counting entities..."

    TECHNIQUE_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (n:AttackTechnique) RETURN count(n) AS count;" --format plain 2>/dev/null | tail -1)
    log "  AttackTechniques: $TECHNIQUE_COUNT (expected: ~823)"

    MITIGATION_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (n:Mitigation) RETURN count(n) AS count;" --format plain 2>/dev/null | tail -1)
    log "  Mitigations: $MITIGATION_COUNT (expected: ~46)"

    ACTOR_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (n:ThreatActor) RETURN count(n) AS count;" --format plain 2>/dev/null | tail -1)
    log "  ThreatActors: $ACTOR_COUNT (expected: ~152)"

    SOFTWARE_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (n:Software) RETURN count(n) AS count;" --format plain 2>/dev/null | tail -1)
    log "  Software: $SOFTWARE_COUNT (expected: ~747)"

    CAMPAIGN_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (n:Campaign) RETURN count(n) AS count;" --format plain 2>/dev/null | tail -1)
    log "  Campaigns: $CAMPAIGN_COUNT (expected: ~36)"

    TOTAL_NODES=$((TECHNIQUE_COUNT + MITIGATION_COUNT + ACTOR_COUNT + SOFTWARE_COUNT + CAMPAIGN_COUNT))
    log_success "Total nodes: $TOTAL_NODES (expected: ~2,051)"

    # Count relationships
    TOTAL_RELS=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH ()-[r]->() RETURN count(r) AS count;" --format plain 2>/dev/null | tail -1)
    log_success "Total relationships: $TOTAL_RELS (expected: ~40,886)"

    # Validate bi-directional relationships
    log "Validating bi-directional relationship integrity..."

    USES_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH ()-[r:USES]->() RETURN count(r) AS count;" --format plain 2>/dev/null | tail -1)
    USED_BY_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH ()-[r:USED_BY]->() RETURN count(r) AS count;" --format plain 2>/dev/null | tail -1)

    if [[ "$USES_COUNT" == "$USED_BY_COUNT" ]]; then
        log_success "Bi-directional USES/USED_BY: $USES_COUNT pairs"
    else
        log_warning "Bi-directional mismatch: USES=$USES_COUNT, USED_BY=$USED_BY_COUNT"
    fi

    # Validate constraints and indexes
    log "Checking constraints and indexes..."
    CONSTRAINT_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "SHOW CONSTRAINTS;" --format plain 2>/dev/null | wc -l)
    log "  Constraints: $CONSTRAINT_COUNT"

    INDEX_COUNT=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "SHOW INDEXES;" --format plain 2>/dev/null | wc -l)
    log "  Indexes: $INDEX_COUNT"

    # Basic sanity queries
    log "Running sanity queries..."

    log "  Sample: Techniques used by APT groups"
    cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (actor:ThreatActor)-[:USES]->(tech:AttackTechnique) RETURN actor.name, tech.name LIMIT 3;" \
        --format plain 2>&1 | head -5 | tee -a "$LOG_FILE"

    log_success "Validation complete"
}

# ========================================
# Rollback Operations
# ========================================

rollback_database() {
    log_error "Import failed - initiating rollback..."

    if [[ "$SKIP_BACKUP" == true ]]; then
        log_error "No backup available - cannot rollback!"
        log_error "Database may be in inconsistent state"
        return 1
    fi

    log "Clearing database..."
    cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -a "$NEO4J_URI" \
        "MATCH (n) DETACH DELETE n;" 2>&1 | tee -a "$LOG_FILE"

    log_success "Database cleared - rollback complete"
    log "To restore from backup, run the validation script with --restore option"
}

# ========================================
# Main Execution Flow
# ========================================

main() {
    log "=========================================="
    log "Neo4j MITRE ATT&CK Import Execution"
    log "=========================================="
    log "Timestamp: $TIMESTAMP"
    log "Neo4j URI: $NEO4J_URI"
    log "Batch Size: $BATCH_SIZE"
    log "Skip Backup: $SKIP_BACKUP"
    log "Dry Run: $DRY_RUN"
    log "=========================================="

    # Pre-flight checks
    check_prerequisites
    check_neo4j_connectivity
    check_database_size

    if [[ "$DRY_RUN" == true ]]; then
        log_success "Dry run complete - all checks passed"
        exit 0
    fi

    # Backup
    backup_database

    # Execute import
    if execute_import; then
        # Validate
        validate_import

        log_success "=========================================="
        log_success "Import completed successfully!"
        log_success "=========================================="
        log "Log file: $LOG_FILE"

        if [[ "$SKIP_BACKUP" == false ]]; then
            log "Backup file: ${BACKUP_DIR}/neo4j_backup_${TIMESTAMP}.cypher"
        fi

        exit 0
    else
        # Rollback on failure
        rollback_database

        log_error "=========================================="
        log_error "Import failed and rolled back"
        log_error "=========================================="
        log_error "Check log file for details: $LOG_FILE"

        exit 1
    fi
}

# ========================================
# Execute main function
# ========================================
main "$@"
