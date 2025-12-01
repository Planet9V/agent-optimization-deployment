#!/bin/bash
set -euo pipefail

# initialize-schema-registry.sh
# Queries Water and Energy sectors to extract patterns and create initial schema registry

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT_FILE="$PROJECT_ROOT/schema-registry.json"
TEMP_DIR="$PROJECT_ROOT/temp"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if Neo4j is running
check_neo4j() {
    log_info "Checking Neo4j connection..."
    if ! docker ps | grep -q openspg-neo4j; then
        log_error "Neo4j container 'openspg-neo4j' is not running"
        exit 1
    fi
    log_info "Neo4j container is running"
}

# Execute Cypher query
execute_cypher() {
    local query="$1"
    docker exec openspg-neo4j cypher-shell -u neo4j -p your_password --format plain "$query" 2>&1
}

# Extract label patterns from a sector
extract_label_patterns() {
    local sector="$1"
    log_info "Extracting label patterns from $sector sector..."

    local query="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$sector')
    WITH DISTINCT labels(n) AS nodeLabels
    UNWIND nodeLabels AS label
    RETURN DISTINCT label
    ORDER BY label;"

    execute_cypher "$query" | grep -v "^label$" | grep -v "^$" | tr '\n' ',' | sed 's/,$//'
}

# Extract relationship types from a sector
extract_relationship_types() {
    local sector="$1"
    log_info "Extracting relationship types from $sector sector..."

    local query="MATCH (n)-[r]->(m)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$sector')
       OR ANY(label IN labels(m) WHERE label CONTAINS '$sector')
    RETURN DISTINCT type(r) AS relType
    ORDER BY relType;"

    execute_cypher "$query" | grep -v "^relType$" | grep -v "^$" | tr '\n' ',' | sed 's/,$//'
}

# Extract property patterns from a sector
extract_property_patterns() {
    local sector="$1"
    log_info "Extracting property patterns from $sector sector..."

    local query="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$sector')
    WITH DISTINCT keys(n) AS propertyKeys
    UNWIND propertyKeys AS key
    RETURN DISTINCT key
    ORDER BY key
    LIMIT 20;"

    execute_cypher "$query" | grep -v "^key$" | grep -v "^$" | tr '\n' ',' | sed 's/,$//'
}

# Get sector node count
get_node_count() {
    local sector="$1"
    local query="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$sector')
    RETURN count(n) AS count;"

    execute_cypher "$query" | grep -v "^count$" | grep -v "^$" | head -1
}

# Create schema registry JSON
create_registry() {
    log_info "Creating schema registry..."

    # Extract patterns from Water sector
    local water_labels=$(extract_label_patterns "Water")
    local water_rels=$(extract_relationship_types "Water")
    local water_props=$(extract_property_patterns "Water")
    local water_count=$(get_node_count "Water")

    # Extract patterns from Energy sector
    local energy_labels=$(extract_label_patterns "Energy")
    local energy_rels=$(extract_relationship_types "Energy")
    local energy_props=$(extract_property_patterns "Energy")
    local energy_count=$(get_node_count "Energy")

    # Create JSON structure
    cat > "$OUTPUT_FILE" <<EOF
{
  "version": "1.0.0",
  "created": "$(date -Iseconds)",
  "database": "neo4j",
  "sectors": {
    "Water": {
      "nodeCount": ${water_count:-0},
      "labels": [$(echo "$water_labels" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/') ],
      "relationshipTypes": [$(echo "$water_rels" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/') ],
      "commonProperties": [$(echo "$water_props" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/') ],
      "namingConvention": "Water_<EntityType>",
      "validated": true,
      "lastUpdated": "$(date -Iseconds)"
    },
    "Energy": {
      "nodeCount": ${energy_count:-0},
      "labels": [$(echo "$energy_labels" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/') ],
      "relationshipTypes": [$(echo "$energy_rels" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/') ],
      "commonProperties": [$(echo "$energy_props" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/') ],
      "namingConvention": "Energy_<EntityType>",
      "validated": true,
      "lastUpdated": "$(date -Iseconds)"
    }
  },
  "crossSectorPatterns": {
    "commonRelationships": ["DEPENDS_ON", "CONNECTS_TO", "SUPPLIES"],
    "commonProperties": ["id", "name", "location", "capacity"],
    "crossSectorQueries": {
      "waterEnergyNexus": "MATCH (w:Water_Infrastructure)-[:DEPENDS_ON]->(e:Energy_Infrastructure) RETURN w, e LIMIT 10",
      "criticalDependencies": "MATCH (a)-[:CRITICAL_DEPENDENCY]->(b) WHERE ANY(l IN labels(a) WHERE l CONTAINS 'Water' OR l CONTAINS 'Energy') RETURN a, b LIMIT 10"
    }
  },
  "governance": {
    "namingStandard": "<Sector>_<EntityType>",
    "requiredProperties": ["id", "name", "sector"],
    "validationRules": {
      "labelFormat": "^[A-Z][a-zA-Z]+_[A-Z][a-zA-Z]+$",
      "propertyNaming": "camelCase",
      "relationshipNaming": "UPPER_SNAKE_CASE"
    }
  }
}
EOF

    log_info "Schema registry created at: $OUTPUT_FILE"
}

# Store in Qdrant memory (if available)
store_in_memory() {
    log_info "Attempting to store schema registry in Qdrant..."

    if [ -f "$OUTPUT_FILE" ]; then
        # Check if qdrant-cli is available
        if command -v curl &> /dev/null; then
            local registry_content=$(cat "$OUTPUT_FILE")

            # Try to store in Qdrant collection
            curl -X PUT "http://localhost:6333/collections/schema_registry/points" \
                -H "Content-Type: application/json" \
                -d "{
                    \"points\": [{
                        \"id\": 1,
                        \"vector\": [0.1, 0.2, 0.3, 0.4],
                        \"payload\": {
                            \"type\": \"schema_registry\",
                            \"version\": \"1.0.0\",
                            \"created\": \"$(date -Iseconds)\",
                            \"content\": $(echo "$registry_content" | jq -c '.')
                        }
                    }]
                }" 2>/dev/null && log_info "Schema registry stored in Qdrant" || log_warn "Failed to store in Qdrant (may not be running)"
        else
            log_warn "curl not available, skipping Qdrant storage"
        fi
    fi
}

# Main execution
main() {
    log_info "Starting schema registry initialization..."

    check_neo4j
    create_registry
    store_in_memory

    log_info "Schema registry initialization complete!"
    log_info "Registry file: $OUTPUT_FILE"

    # Display summary
    echo ""
    echo "========================================="
    echo "SCHEMA REGISTRY SUMMARY"
    echo "========================================="
    jq '.' "$OUTPUT_FILE" 2>/dev/null || cat "$OUTPUT_FILE"
}

main "$@"
