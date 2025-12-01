#!/bin/bash
set -euo pipefail

# update-schema-registry.sh
# Updates the schema registry with a new sector

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REGISTRY_FILE="$PROJECT_ROOT/schema-registry.json"
BACKUP_DIR="$PROJECT_ROOT/backups/schema-registry"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${BLUE}[SUCCESS]${NC} $1"
}

# Check arguments
if [ $# -lt 1 ]; then
    log_error "Usage: $0 <sector-name>"
    log_error "Example: $0 Healthcare"
    exit 1
fi

SECTOR="$1"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."

    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed"
        exit 1
    fi

    if ! docker ps | grep -q openspg-neo4j; then
        log_error "Neo4j container 'openspg-neo4j' is not running"
        exit 1
    fi

    if [ ! -f "$REGISTRY_FILE" ]; then
        log_error "Schema registry not found at: $REGISTRY_FILE"
        log_error "Run initialize-schema-registry.sh first"
        exit 1
    fi

    log_info "All dependencies satisfied"
}

# Execute Cypher query
execute_cypher() {
    local query="$1"
    docker exec openspg-neo4j cypher-shell -u neo4j -p your_password --format plain "$query" 2>&1
}

# Backup registry
backup_registry() {
    log_info "Backing up schema registry..."
    local backup_file="$BACKUP_DIR/schema-registry_$(date +%Y%m%d_%H%M%S).json"
    cp "$REGISTRY_FILE" "$backup_file"
    log_info "Backup created at: $backup_file"
}

# Extract sector patterns
extract_sector_data() {
    log_info "Extracting patterns from $SECTOR sector..."

    # Get labels
    local labels_query="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$SECTOR')
    WITH DISTINCT labels(n) AS nodeLabels
    UNWIND nodeLabels AS label
    RETURN DISTINCT label
    ORDER BY label;"

    local labels=$(execute_cypher "$labels_query" | grep -v "^label$" | grep -v "^$" | jq -R -s -c 'split("\n") | map(select(length > 0))')

    # Get relationship types
    local rels_query="MATCH (n)-[r]->(m)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$SECTOR')
       OR ANY(label IN labels(m) WHERE label CONTAINS '$SECTOR')
    RETURN DISTINCT type(r) AS relType
    ORDER BY relType;"

    local rels=$(execute_cypher "$rels_query" | grep -v "^relType$" | grep -v "^$" | jq -R -s -c 'split("\n") | map(select(length > 0))')

    # Get common properties
    local props_query="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$SECTOR')
    WITH DISTINCT keys(n) AS propertyKeys
    UNWIND propertyKeys AS key
    RETURN DISTINCT key
    ORDER BY key
    LIMIT 20;"

    local props=$(execute_cypher "$props_query" | grep -v "^key$" | grep -v "^$" | jq -R -s -c 'split("\n") | map(select(length > 0))')

    # Get node count
    local count_query="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$SECTOR')
    RETURN count(n) AS count;"

    local node_count=$(execute_cypher "$count_query" | grep -v "^count$" | grep -v "^$" | head -1)

    echo "{\"labels\": $labels, \"relationshipTypes\": $rels, \"commonProperties\": $props, \"nodeCount\": ${node_count:-0}}"
}

# Detect cross-sector patterns
detect_cross_sector_patterns() {
    log_info "Detecting cross-sector patterns for $SECTOR..."

    # Find common relationships with other sectors
    local query="MATCH (a)-[r]->(b)
    WHERE ANY(la IN labels(a) WHERE la CONTAINS '$SECTOR')
      AND NOT ANY(lb IN labels(b) WHERE lb CONTAINS '$SECTOR')
    RETURN DISTINCT type(r) AS relType, labels(b)[0] AS targetLabel
    ORDER BY relType
    LIMIT 10;"

    local cross_rels=$(execute_cypher "$query" | grep -v "^relType" | grep -v "^$")

    local cross_sector_json="{"
    local first=true

    while IFS=$'\t' read -r rel_type target_label; do
        local target_sector=$(echo "$target_label" | cut -d'_' -f1)

        if [ "$first" = true ]; then
            first=false
        else
            cross_sector_json="${cross_sector_json},"
        fi

        local query_name="${SECTOR}_${target_sector}_${rel_type}"
        local query_cypher="MATCH (a:${SECTOR}_*)-[:${rel_type}]->(b:${target_sector}_*) RETURN a, b LIMIT 10"

        cross_sector_json="${cross_sector_json}\"$query_name\": \"$query_cypher\""
    done <<< "$cross_rels"

    cross_sector_json="${cross_sector_json}}"

    echo "$cross_sector_json"
}

# Update registry file
update_registry() {
    log_info "Updating schema registry..."

    local sector_data=$(extract_sector_data)
    local cross_sector_patterns=$(detect_cross_sector_patterns)

    local labels=$(echo "$sector_data" | jq -r '.labels')
    local rels=$(echo "$sector_data" | jq -r '.relationshipTypes')
    local props=$(echo "$sector_data" | jq -r '.commonProperties')
    local node_count=$(echo "$sector_data" | jq -r '.nodeCount')

    # Update registry using jq
    local updated_registry=$(jq --arg sector "$SECTOR" \
                                --argjson labels "$labels" \
                                --argjson rels "$rels" \
                                --argjson props "$props" \
                                --arg count "$node_count" \
                                --argjson cross_queries "$cross_sector_patterns" \
                                '.sectors[$sector] = {
                                    "nodeCount": ($count | tonumber),
                                    "labels": $labels,
                                    "relationshipTypes": $rels,
                                    "commonProperties": $props,
                                    "namingConvention": "\($sector)_<EntityType>",
                                    "validated": true,
                                    "lastUpdated": now | todate
                                } |
                                .crossSectorPatterns.crossSectorQueries += $cross_queries' \
                                "$REGISTRY_FILE")

    echo "$updated_registry" > "$REGISTRY_FILE"
    log_success "Registry updated with $SECTOR sector"
}

# Store in Qdrant memory
store_in_memory() {
    log_info "Storing updated registry in Qdrant..."

    if command -v curl &> /dev/null; then
        local registry_content=$(cat "$REGISTRY_FILE")

        curl -X PUT "http://localhost:6333/collections/schema_registry/points" \
            -H "Content-Type: application/json" \
            -d "{
                \"points\": [{
                    \"id\": 1,
                    \"vector\": [0.1, 0.2, 0.3, 0.4],
                    \"payload\": {
                        \"type\": \"schema_registry\",
                        \"version\": \"1.0.0\",
                        \"lastUpdated\": \"$(date -Iseconds)\",
                        \"sectors\": $(echo "$registry_content" | jq -c '.sectors | keys'),
                        \"content\": $(echo "$registry_content" | jq -c '.')
                    }
                }]
            }" 2>/dev/null && log_success "Registry stored in Qdrant" || log_warn "Failed to store in Qdrant (may not be running)"
    else
        log_warn "curl not available, skipping Qdrant storage"
    fi
}

# Commit to git
commit_to_git() {
    log_info "Committing changes to git..."

    if git rev-parse --git-dir > /dev/null 2>&1; then
        cd "$PROJECT_ROOT"

        git add "$REGISTRY_FILE"

        if git diff --cached --quiet; then
            log_warn "No changes to commit"
        else
            git commit -m "feat(schema): Add $SECTOR sector to schema registry

- Added $SECTOR sector patterns
- Updated cross-sector queries
- Automated update via governance script

Generated by: update-schema-registry.sh
Date: $(date -Iseconds)" || log_warn "Git commit failed (may have conflicts)"

            log_success "Changes committed to git"
        fi
    else
        log_warn "Not a git repository, skipping commit"
    fi
}

# Display summary
display_summary() {
    echo ""
    echo "========================================="
    echo "SCHEMA REGISTRY UPDATE SUMMARY"
    echo "========================================="
    echo "Sector: $SECTOR"
    echo "Updated: $(date)"
    echo ""
    echo "Current Registry:"
    jq ".sectors.\"$SECTOR\"" "$REGISTRY_FILE"
    echo ""
    echo "Total Sectors: $(jq '.sectors | keys | length' "$REGISTRY_FILE")"
    echo "========================================="
}

# Main execution
main() {
    log_info "Starting schema registry update for sector: $SECTOR"

    check_dependencies
    backup_registry
    update_registry
    store_in_memory
    commit_to_git
    display_summary

    log_success "Schema registry update complete!"
}

main "$@"
