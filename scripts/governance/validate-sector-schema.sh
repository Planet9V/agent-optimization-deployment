#!/bin/bash
set -euo pipefail

# validate-sector-schema.sh
# Validates a sector's schema against the schema registry

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REGISTRY_FILE="$PROJECT_ROOT/schema-registry.json"
TEMP_DIR="$PROJECT_ROOT/temp"
OUTPUT_DIR="$PROJECT_ROOT/validation-reports"

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
REPORT_FILE="$OUTPUT_DIR/${SECTOR}_validation_$(date +%Y%m%d_%H%M%S).json"

# Create output directory
mkdir -p "$OUTPUT_DIR"

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

# Validate label patterns
validate_label_patterns() {
    log_info "Validating label patterns for $SECTOR..."

    local query="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$SECTOR')
    WITH DISTINCT labels(n) AS nodeLabels
    UNWIND nodeLabels AS label
    RETURN DISTINCT label
    ORDER BY label;"

    local actual_labels=$(execute_cypher "$query" | grep -v "^label$" | grep -v "^$")
    local expected_pattern=$(jq -r '.governance.namingStandard' "$REGISTRY_FILE")

    local valid_count=0
    local invalid_count=0
    local invalid_labels=""

    while IFS= read -r label; do
        if [[ "$label" =~ ^${SECTOR}_[A-Z][a-zA-Z]+$ ]]; then
            ((valid_count++))
        else
            ((invalid_count++))
            invalid_labels="${invalid_labels}\"$label\","
        fi
    done <<< "$actual_labels"

    # Remove trailing comma
    invalid_labels="${invalid_labels%,}"

    echo "{\"valid\": $valid_count, \"invalid\": $invalid_count, \"invalidLabels\": [$invalid_labels]}"
}

# Validate relationship types
validate_relationship_types() {
    log_info "Validating relationship types for $SECTOR..."

    local query="MATCH (n)-[r]->(m)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$SECTOR')
       OR ANY(label IN labels(m) WHERE label CONTAINS '$SECTOR')
    RETURN DISTINCT type(r) AS relType
    ORDER BY relType;"

    local actual_rels=$(execute_cypher "$query" | grep -v "^relType$" | grep -v "^$")

    local valid_count=0
    local invalid_count=0
    local invalid_rels=""

    while IFS= read -r rel; do
        if [[ "$rel" =~ ^[A-Z_]+$ ]]; then
            ((valid_count++))
        else
            ((invalid_count++))
            invalid_rels="${invalid_rels}\"$rel\","
        fi
    done <<< "$actual_rels"

    # Remove trailing comma
    invalid_rels="${invalid_rels%,}"

    echo "{\"valid\": $valid_count, \"invalid\": $invalid_count, \"invalidTypes\": [$invalid_rels]}"
}

# Validate required properties
validate_required_properties() {
    log_info "Validating required properties for $SECTOR..."

    local required_props=$(jq -r '.governance.requiredProperties[]' "$REGISTRY_FILE" | tr '\n' ',' | sed 's/,$//')

    local query="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$SECTOR')
    WITH n, keys(n) AS props
    WHERE NOT ALL(req IN ['id', 'name', 'sector'] WHERE req IN props)
    RETURN count(n) AS missingCount;"

    local missing_count=$(execute_cypher "$query" | grep -v "^missingCount$" | grep -v "^$" | head -1)

    local query_total="MATCH (n)
    WHERE ANY(label IN labels(n) WHERE label CONTAINS '$SECTOR')
    RETURN count(n) AS total;"

    local total_count=$(execute_cypher "$query_total" | grep -v "^total$" | grep -v "^$" | head -1)

    local compliant_count=$((total_count - missing_count))

    echo "{\"total\": ${total_count:-0}, \"compliant\": ${compliant_count:-0}, \"missing\": ${missing_count:-0}}"
}

# Test cross-sector queries
test_cross_sector_queries() {
    log_info "Testing cross-sector queries for $SECTOR..."

    local query_results="{"
    local first=true

    # Get cross-sector queries from registry
    local queries=$(jq -r '.crossSectorPatterns.crossSectorQueries | keys[]' "$REGISTRY_FILE" 2>/dev/null || echo "")

    if [ -n "$queries" ]; then
        while IFS= read -r query_name; do
            local query_cypher=$(jq -r ".crossSectorPatterns.crossSectorQueries.\"$query_name\"" "$REGISTRY_FILE")

            # Modify query to include sector
            local modified_query="${query_cypher/LIMIT/WHERE ANY(l IN labels(a) WHERE l CONTAINS '$SECTOR') OR ANY(l IN labels(b) WHERE l CONTAINS '$SECTOR') LIMIT}"

            local result_count=$(execute_cypher "$modified_query" 2>/dev/null | wc -l)

            if [ "$first" = true ]; then
                first=false
            else
                query_results="${query_results},"
            fi

            query_results="${query_results}\"$query_name\": {\"executed\": true, \"resultCount\": $((result_count - 2))}"
        done <<< "$queries"
    fi

    query_results="${query_results}}"
    echo "$query_results"
}

# Check for cross-sector relationships
check_cross_sector_relationships() {
    log_info "Checking cross-sector relationships for $SECTOR..."

    local query="MATCH (a)-[r]->(b)
    WHERE ANY(la IN labels(a) WHERE la CONTAINS '$SECTOR')
      AND NOT ANY(lb IN labels(b) WHERE lb CONTAINS '$SECTOR')
    RETURN DISTINCT labels(b)[0] AS targetSector, count(r) AS relationshipCount
    ORDER BY relationshipCount DESC
    LIMIT 5;"

    local results=$(execute_cypher "$query" | grep -v "^targetSector" | grep -v "^$")

    local cross_sector_json="["
    local first=true

    while IFS=$'\t' read -r target_sector count; do
        if [ "$first" = true ]; then
            first=false
        else
            cross_sector_json="${cross_sector_json},"
        fi
        cross_sector_json="${cross_sector_json}{\"targetSector\": \"$target_sector\", \"count\": $count}"
    done <<< "$results"

    cross_sector_json="${cross_sector_json}]"
    echo "$cross_sector_json"
}

# Generate validation report
generate_report() {
    log_info "Generating validation report..."

    local label_validation=$(validate_label_patterns)
    local rel_validation=$(validate_relationship_types)
    local prop_validation=$(validate_required_properties)
    local query_tests=$(test_cross_sector_queries)
    local cross_sector=$(check_cross_sector_relationships)

    # Calculate overall score
    local label_valid=$(echo "$label_validation" | jq -r '.valid')
    local label_invalid=$(echo "$label_validation" | jq -r '.invalid')
    local rel_valid=$(echo "$rel_validation" | jq -r '.valid')
    local rel_invalid=$(echo "$rel_validation" | jq -r '.invalid')
    local prop_compliant=$(echo "$prop_validation" | jq -r '.compliant')
    local prop_total=$(echo "$prop_validation" | jq -r '.total')

    local total_checks=$((label_valid + label_invalid + rel_valid + rel_invalid))
    local passed_checks=$((label_valid + rel_valid + prop_compliant))
    local score=$((passed_checks * 100 / (total_checks + prop_total)))

    local status="FAIL"
    [ $score -ge 80 ] && status="PASS"
    [ $score -ge 95 ] && status="EXCELLENT"

    cat > "$REPORT_FILE" <<EOF
{
  "sector": "$SECTOR",
  "validatedAt": "$(date -Iseconds)",
  "overallStatus": "$status",
  "score": $score,
  "validations": {
    "labelPatterns": $label_validation,
    "relationshipTypes": $rel_validation,
    "requiredProperties": $prop_validation
  },
  "crossSectorTests": $query_tests,
  "crossSectorRelationships": $cross_sector,
  "recommendations": [
    $([ $label_invalid -gt 0 ] && echo "\"Fix $label_invalid invalid label patterns\",")
    $([ $rel_invalid -gt 0 ] && echo "\"Fix $rel_invalid invalid relationship types\",")
    $([ $(echo "$prop_validation" | jq -r '.missing') -gt 0 ] && echo "\"Add required properties to $(echo "$prop_validation" | jq -r '.missing') nodes\",")
    "Validation complete"
  ]
}
EOF

    log_info "Validation report created at: $REPORT_FILE"
}

# Display summary
display_summary() {
    echo ""
    echo "========================================="
    echo "VALIDATION REPORT: $SECTOR"
    echo "========================================="
    jq '.' "$REPORT_FILE"
    echo ""

    local status=$(jq -r '.overallStatus' "$REPORT_FILE")
    local score=$(jq -r '.score' "$REPORT_FILE")

    if [ "$status" = "EXCELLENT" ]; then
        log_success "Validation EXCELLENT - Score: $score%"
    elif [ "$status" = "PASS" ]; then
        log_success "Validation PASSED - Score: $score%"
    else
        log_error "Validation FAILED - Score: $score%"
    fi
}

# Main execution
main() {
    log_info "Starting schema validation for sector: $SECTOR"

    check_dependencies
    generate_report
    display_summary

    log_info "Validation complete!"
}

main "$@"
