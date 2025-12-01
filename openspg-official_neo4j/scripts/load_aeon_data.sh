#!/bin/bash
# ============================================================================
# AEON Cyber Digital Twin - Data Loading Pipeline
# ============================================================================
# Created: 2025-11-26
# Purpose: Consistent data loading process for AEON Neo4j database
# Usage: ./load_aeon_data.sh [phase]
#   Phases: schema, sample, mitre, all
# ============================================================================

set -e

NEO4J_HOST="localhost"
NEO4J_PORT="7687"
NEO4J_USER="neo4j"
NEO4J_PASS="neo4j@openspg"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_DIR="$SCRIPT_DIR/../schema"
MITRE_DIR="/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/scripts/import_batches"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_neo4j() {
    log_info "Checking Neo4j connectivity..."
    if docker exec openspg-neo4j cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" "RETURN 1" > /dev/null 2>&1; then
        log_info "Neo4j is running and accessible"
        return 0
    else
        log_error "Cannot connect to Neo4j"
        return 1
    fi
}

run_cypher_file() {
    local file="$1"
    local desc="$2"
    log_info "Loading: $desc"
    if [ -f "$file" ]; then
        cat "$file" | docker exec -i openspg-neo4j cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" 2>&1
        if [ $? -eq 0 ]; then
            log_info "✓ $desc loaded successfully"
        else
            log_error "✗ Failed to load $desc"
            return 1
        fi
    else
        log_error "File not found: $file"
        return 1
    fi
}

load_schema() {
    log_info "============================================"
    log_info "PHASE 1: Loading Schema (Constraints & Indexes)"
    log_info "============================================"

    run_cypher_file "$SCHEMA_DIR/01_constraints.cypher" "Constraints"
    run_cypher_file "$SCHEMA_DIR/02_indexes.cypher" "Indexes"

    log_info "Schema loading complete"
}

load_sample_data() {
    log_info "============================================"
    log_info "PHASE 2: Loading Sample Reference Data"
    log_info "============================================"

    run_cypher_file "$SCHEMA_DIR/03_sample_data.cypher" "Sample Data (Sectors, Orgs, Threat Actors)"

    log_info "Sample data loading complete"
}

load_mitre() {
    log_info "============================================"
    log_info "PHASE 3: Loading MITRE ATT&CK Data"
    log_info "============================================"

    if [ -d "$MITRE_DIR" ]; then
        run_cypher_file "$MITRE_DIR/batch1_entities.cypher" "MITRE ATT&CK Entities (16,367 lines)"
        run_cypher_file "$MITRE_DIR/batch2_relationships.cypher" "MITRE ATT&CK Relationships (102,968 lines)"
        log_info "MITRE ATT&CK loading complete"
    else
        log_warn "MITRE data directory not found: $MITRE_DIR"
        log_warn "Skipping MITRE data loading"
    fi
}

verify_data() {
    log_info "============================================"
    log_info "PHASE 4: Verifying Data Load"
    log_info "============================================"

    echo "MATCH (n) RETURN labels(n) AS type, count(*) AS count ORDER BY count DESC LIMIT 20;" | \
        docker exec -i openspg-neo4j cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" 2>&1

    log_info "Data verification complete"
}

show_usage() {
    echo "AEON Data Loading Pipeline"
    echo ""
    echo "Usage: $0 [phase]"
    echo ""
    echo "Phases:"
    echo "  schema  - Load constraints and indexes only"
    echo "  sample  - Load sample reference data"
    echo "  mitre   - Load MITRE ATT&CK data"
    echo "  verify  - Verify data counts"
    echo "  all     - Load everything (schema + sample + mitre)"
    echo ""
    echo "Examples:"
    echo "  $0 schema    # Just apply schema"
    echo "  $0 all       # Full data load"
    echo "  $0 verify    # Check what's loaded"
}

# Main
main() {
    local phase="${1:-help}"

    check_neo4j || exit 1

    case "$phase" in
        schema)
            load_schema
            ;;
        sample)
            load_sample_data
            ;;
        mitre)
            load_mitre
            ;;
        verify)
            verify_data
            ;;
        all)
            load_schema
            load_sample_data
            load_mitre
            verify_data
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            log_error "Unknown phase: $phase"
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
