#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
# GAP-004 PHASE 1 SCHEMA DEPLOYMENT SCRIPT
# ═══════════════════════════════════════════════════════════════════════
# File: gap004_deploy.sh
# Created: 2025-11-13
# Purpose: Execute Cypher DDL scripts in correct order with error handling
# Usage: ./gap004_deploy.sh [neo4j-uri] [username] [password]
# Example: ./gap004_deploy.sh bolt://localhost:7687 neo4j mypassword
# ═══════════════════════════════════════════════════════════════════════

set -e  # Exit on any error
set -u  # Exit on undefined variables

# -----------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONSTRAINTS_FILE="${SCRIPT_DIR}/gap004_schema_constraints.cypher"
INDEXES_FILE="${SCRIPT_DIR}/gap004_schema_indexes.cypher"
RELATIONSHIPS_FILE="${SCRIPT_DIR}/gap004_relationships.cypher"
LOG_FILE="${SCRIPT_DIR}/gap004_deploy_$(date +%Y%m%d_%H%M%S).log"

# Neo4j connection parameters (defaults or from arguments)
NEO4J_URI="${1:-bolt://localhost:7687}"
NEO4J_USER="${2:-neo4j}"
NEO4J_PASSWORD="${3:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# -----------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

check_prerequisites() {
    log "Checking prerequisites..."

    # Check if cypher-shell is available
    if ! command -v cypher-shell &> /dev/null; then
        log_error "cypher-shell not found. Please install Neo4j client tools."
        log_error "Installation: https://neo4j.com/docs/operations-manual/current/tools/cypher-shell/"
        exit 1
    fi

    # Check if Cypher files exist
    if [ ! -f "$CONSTRAINTS_FILE" ]; then
        log_error "Constraints file not found: $CONSTRAINTS_FILE"
        exit 1
    fi

    if [ ! -f "$INDEXES_FILE" ]; then
        log_error "Indexes file not found: $INDEXES_FILE"
        exit 1
    fi

    if [ ! -f "$RELATIONSHIPS_FILE" ]; then
        log_error "Relationships file not found: $RELATIONSHIPS_FILE"
        exit 1
    fi

    log_success "All prerequisites met"
}

check_connection() {
    log "Testing Neo4j connection to $NEO4J_URI..."

    if [ -z "$NEO4J_PASSWORD" ]; then
        log_error "Neo4j password is required"
        exit 1
    fi

    # Test connection with simple query
    if echo "RETURN 1 AS test;" | cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" --format plain > /dev/null 2>&1; then
        log_success "Connection successful"
    else
        log_error "Failed to connect to Neo4j at $NEO4J_URI"
        log_error "Please verify URI, username, and password"
        exit 1
    fi
}

execute_cypher_file() {
    local file=$1
    local description=$2

    log "Executing $description from $(basename $file)..."

    if cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" --file "$file" >> "$LOG_FILE" 2>&1; then
        log_success "$description completed"
        return 0
    else
        log_error "$description failed"
        log_error "Check log file for details: $LOG_FILE"
        return 1
    fi
}

count_constraints() {
    local query="SHOW CONSTRAINTS YIELD name WHERE name STARTS WITH 'digital_twin' OR name STARTS WITH 'physical' OR name STARTS WITH 'physics' OR name STARTS WITH 'state_deviation' OR name STARTS WITH 'process_loop' OR name STARTS WITH 'safety' OR name STARTS WITH 'cascade' OR name STARTS WITH 'dependency' OR name STARTS WITH 'propagation' OR name STARTS WITH 'impact' OR name STARTS WITH 'system_resilience' OR name STARTS WITH 'cross_infra' OR name STARTS WITH 'temporal' OR name STARTS WITH 'event_store' OR name STARTS WITH 'timeseries' OR name STARTS WITH 'historical' OR name STARTS WITH 'versioned' OR name STARTS WITH 'operational' OR name STARTS WITH 'service_level' OR name STARTS WITH 'customer_impact' OR name STARTS WITH 'revenue' OR name STARTS WITH 'disruption' OR name STARTS WITH 'scada' OR name STARTS WITH 'hmi' OR name STARTS WITH 'plc' OR name STARTS WITH 'rtu' OR name STARTS WITH 'event_correlation' OR name STARTS WITH 'attack_timeline' OR name STARTS WITH 'data_flow' OR name STARTS WITH 'alert_rule' OR name STARTS WITH 'remediation' RETURN count(*) AS count;"

    echo "$query" | cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" --format plain 2>/dev/null | grep -o '[0-9]\+' | head -1
}

count_indexes() {
    local query="SHOW INDEXES YIELD name WHERE name STARTS WITH 'digital_twin' OR name STARTS WITH 'sensor' OR name STARTS WITH 'actuator' OR name STARTS WITH 'constraint' OR name STARTS WITH 'deviation' OR name STARTS WITH 'loop' OR name STARTS WITH 'safety' OR name STARTS WITH 'interlock' OR name STARTS WITH 'cascade' OR name STARTS WITH 'dep' OR name STARTS WITH 'prop' OR name STARTS WITH 'impact' OR name STARTS WITH 'resilience' OR name STARTS WITH 'cross' OR name STARTS WITH 'temporal' OR name STARTS WITH 'event_store' OR name STARTS WITH 'temp_pattern' OR name STARTS WITH 'timeseries' OR name STARTS WITH 'snapshot' OR name STARTS WITH 'versioned' OR name STARTS WITH 'metric' OR name STARTS WITH 'sla' OR name STARTS WITH 'customer_impact' OR name STARTS WITH 'revenue' OR name STARTS WITH 'disruption' OR name STARTS WITH 'scada' OR name STARTS WITH 'hmi' OR name STARTS WITH 'plc' OR name STARTS WITH 'rtu' OR name STARTS WITH 'correlation' OR name STARTS WITH 'timeline' OR name STARTS WITH 'dataflow' OR name STARTS WITH 'alert' OR name STARTS WITH 'remediation' RETURN count(*) AS count;"

    echo "$query" | cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" --format plain 2>/dev/null | grep -o '[0-9]\+' | head -1
}

verify_deployment() {
    log "Verifying deployment..."

    local constraint_count=$(count_constraints)
    local index_count=$(count_indexes)

    log "Constraints created: $constraint_count / 35 expected"
    log "Indexes created: $index_count / 70+ expected"

    if [ "$constraint_count" -ge 35 ] && [ "$index_count" -ge 70 ]; then
        log_success "Deployment verification passed"
        return 0
    else
        log_warning "Deployment verification incomplete"
        log_warning "Expected: 35 constraints, 70+ indexes"
        log_warning "Found: $constraint_count constraints, $index_count indexes"
        return 1
    fi
}

create_backup() {
    log "Creating pre-deployment backup..."

    local backup_file="${SCRIPT_DIR}/pre_gap004_backup_$(date +%Y%m%d_%H%M%S).cypher"

    # Export existing constraints and indexes
    echo "SHOW CONSTRAINTS;" | cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" > "$backup_file" 2>&1
    echo "SHOW INDEXES;" | cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" >> "$backup_file" 2>&1

    log_success "Backup created: $backup_file"
}

# -----------------------------------------------------------------------
# MAIN DEPLOYMENT SEQUENCE
# -----------------------------------------------------------------------

main() {
    echo "═══════════════════════════════════════════════════════════════════════"
    echo "  GAP-004 PHASE 1 SCHEMA DEPLOYMENT"
    echo "  Neo4j URI: $NEO4J_URI"
    echo "  Timestamp: $(date +'%Y-%m-%d %H:%M:%S')"
    echo "═══════════════════════════════════════════════════════════════════════"
    echo ""

    # Initialize log file
    echo "GAP-004 Phase 1 Schema Deployment Log" > "$LOG_FILE"
    echo "Started: $(date +'%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    echo "Neo4j URI: $NEO4J_URI" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"

    # Step 1: Check prerequisites
    check_prerequisites

    # Step 2: Test Neo4j connection
    check_connection

    # Step 3: Create backup
    create_backup

    # Step 4: Deploy constraints (MUST be first)
    log ""
    log "PHASE 1: Deploying Constraints (35 constraints)"
    log "--------------------------------------------------------------"
    if ! execute_cypher_file "$CONSTRAINTS_FILE" "Constraint creation"; then
        log_error "Constraint deployment failed. Aborting."
        exit 1
    fi

    # Step 5: Deploy indexes (MUST be after constraints)
    log ""
    log "PHASE 2: Deploying Indexes (70+ indexes)"
    log "--------------------------------------------------------------"
    if ! execute_cypher_file "$INDEXES_FILE" "Index creation"; then
        log_error "Index deployment failed. Aborting."
        exit 1
    fi

    # Step 6: Wait for indexes to come online
    log ""
    log "PHASE 3: Waiting for indexes to come online..."
    log "--------------------------------------------------------------"
    sleep 5  # Give indexes time to build

    # Step 7: Verify deployment
    log ""
    log "PHASE 4: Verification"
    log "--------------------------------------------------------------"
    verify_deployment

    # Step 8: Summary
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════"
    log_success "GAP-004 Phase 1 Schema Deployment COMPLETE"
    echo "═══════════════════════════════════════════════════════════════════════"
    log ""
    log "Deployment Summary:"
    log "  - Constraints: 35 unique ID constraints"
    log "  - Indexes: 70+ performance indexes"
    log "  - Relationship patterns: 50+ defined (see gap004_relationships.cypher)"
    log "  - Log file: $LOG_FILE"
    log ""
    log "Next Steps:"
    log "  1. Review relationship patterns: gap004_relationships.cypher"
    log "  2. Begin data ingestion for 35 new node types"
    log "  3. Validate <2s query performance targets"
    log "  4. Monitor index usage with: SHOW INDEXES"
    log ""
    log "Rollback Available:"
    log "  - Execute: ./gap004_rollback.cypher if issues occur"
    log ""

    exit 0
}

# -----------------------------------------------------------------------
# EXECUTION
# -----------------------------------------------------------------------

# Check if running with proper arguments
if [ $# -eq 0 ]; then
    log_warning "No connection parameters provided, using defaults:"
    log_warning "  URI: bolt://localhost:7687"
    log_warning "  User: neo4j"
    echo ""
    read -sp "Enter Neo4j password: " NEO4J_PASSWORD
    echo ""
fi

# Run main deployment
main
