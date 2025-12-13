#!/bin/bash
# PROC-102: Kaggle Dataset Enrichment for CVE/CWE
# Auto-generated from procedure template
# Integrated with claude-flow memory and reasoning bank

set -euo pipefail

# Configuration
NEO4J_CONTAINER="openspg-neo4j"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASS="neo4j@openspg"
WORK_DIR="/tmp/kaggle_enrichment"
LOG_FILE="/var/log/aeon/proc_102_$(date +%Y%m%d_%H%M%S).log"
DATASET_ID="stanislavvinokur/cve-and-cwe-dataset-1999-2025"

# Logging functions
log_info() { echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $*" | tee -a "$LOG_FILE"; }
log_warn() { echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARN: $*" | tee -a "$LOG_FILE"; }
log_error() { echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" | tee -a "$LOG_FILE"; }

# Cypher execution helper
cypher_query() {
    docker exec "$NEO4J_CONTAINER" cypher-shell \
        -u "$NEO4J_USER" -p "$NEO4J_PASS" \
        -d neo4j "$@"
}

# Store state in claude-flow memory
store_memory() {
    local key=$1
    local value=$2
    npx claude-flow@alpha hooks post-task \
        --task-id "proc-102-$key" \
        --memory-key "aeon-procedures/proc-102/$key" \
        --memory-value "$value" 2>/dev/null || true
}

check_preconditions() {
    log_info "Checking pre-conditions..."

    # Check Neo4j
    docker ps | grep -q "$NEO4J_CONTAINER" || {
        log_error "Neo4j container not running"
        return 1
    }

    # Check Kaggle auth
    if [ ! -f ~/.kaggle/kaggle.json ]; then
        log_warn "Kaggle credentials not found at ~/.kaggle/kaggle.json"
        log_warn "Please create credentials file or provide manually"
        return 1
    fi

    # Check CVE count
    CVE_TOTAL=$(cypher_query "MATCH (c:CVE) RETURN count(c) as total" -d neo4j --format plain | tail -1)
    log_info "Found $CVE_TOTAL CVE nodes"

    if [ "$CVE_TOTAL" -lt 1000 ]; then
        log_warn "CVE count low ($CVE_TOTAL). Ensure E30 ingestion complete."
    fi

    store_memory "preconditions" "{\"neo4j_running\":true,\"cve_count\":$CVE_TOTAL,\"timestamp\":\"$(date -Iseconds)\"}"
}

download_datasets() {
    log_info "Downloading Kaggle dataset: $DATASET_ID"
    mkdir -p "$WORK_DIR"

    # Download and unzip
    kaggle datasets download "$DATASET_ID" \
        -p "$WORK_DIR" --unzip --force 2>&1 | tee -a "$LOG_FILE"

    if [ ! -f "$WORK_DIR"/*.csv ]; then
        log_error "CSV file not found after download"
        return 1
    fi

    # Find and rename to standard name
    CSV_FILE=$(ls "$WORK_DIR"/*.csv | head -1)
    cp "$CSV_FILE" "$WORK_DIR/CVE_CWE_2025.csv"

    CSV_SIZE=$(ls -lh "$WORK_DIR/CVE_CWE_2025.csv" | awk '{print $5}')
    log_info "Downloaded: CVE_CWE_2025.csv ($CSV_SIZE)"

    # Count rows
    ROW_COUNT=$(wc -l < "$WORK_DIR/CVE_CWE_2025.csv")
    log_info "Dataset contains $ROW_COUNT rows"

    store_memory "download" "{\"file\":\"CVE_CWE_2025.csv\",\"size\":\"$CSV_SIZE\",\"rows\":$ROW_COUNT,\"timestamp\":\"$(date -Iseconds)\"}"
}

copy_to_neo4j() {
    log_info "Copying data to Neo4j import directory..."
    docker cp "$WORK_DIR/CVE_CWE_2025.csv" "$NEO4J_CONTAINER:/var/lib/neo4j/import/"
    docker exec "$NEO4J_CONTAINER" chown neo4j:neo4j /var/lib/neo4j/import/CVE_CWE_2025.csv
    log_info "File copied to Neo4j import directory"
}

create_constraints() {
    log_info "Creating CWE constraint..."
    cypher_query "CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE" -d neo4j
    store_memory "constraints" "{\"cwe_constraint\":\"created\",\"timestamp\":\"$(date -Iseconds)\"}"
}

enrich_cvss_scores() {
    log_info "Enriching CVEs with CVSS scores (batch size: 5000)..."

    RESULT=$(cypher_query -d neo4j "
    CALL apoc.periodic.iterate(
      \"LOAD CSV WITH HEADERS FROM 'file:///CVE_CWE_2025.csv' AS row RETURN row\",
      \"MATCH (cve:CVE {id: row.\\\`CVE-ID\\\`})
       SET cve.cvssV31BaseScore = CASE WHEN row.\\\`CVSS-V3\\\` IS NOT NULL AND row.\\\`CVSS-V3\\\` <> ''
                                       THEN toFloat(row.\\\`CVSS-V3\\\`) ELSE cve.cvssV31BaseScore END,
           cve.cvssV2BaseScore = CASE WHEN row.\\\`CVSS-V2\\\` IS NOT NULL AND row.\\\`CVSS-V2\\\` <> ''
                                      THEN toFloat(row.\\\`CVSS-V2\\\`) ELSE cve.cvssV2BaseScore END,
           cve.cvssV4BaseScore = CASE WHEN row.\\\`CVSS-V4\\\` IS NOT NULL AND row.\\\`CVSS-V4\\\` <> ''
                                      THEN toFloat(row.\\\`CVSS-V4\\\`) ELSE cve.cvssV4BaseScore END,
           cve.cvssV31BaseSeverity = CASE WHEN row.SEVERITY IS NOT NULL AND row.SEVERITY <> ''
                                          THEN toUpper(trim(row.SEVERITY)) ELSE cve.cvssV31BaseSeverity END,
           cve.kaggle_enriched_timestamp = datetime()
       RETURN count(*)\",
      {batchSize: 5000, parallel: false}
    ) YIELD batches, total, errorMessages
    RETURN batches, total, errorMessages
    ")

    echo "$RESULT" | tee -a "$LOG_FILE"
    store_memory "cvss_enrichment" "{\"result\":\"$RESULT\",\"timestamp\":\"$(date -Iseconds)\"}"
}

create_cwe_relationships() {
    log_info "Creating CVE→CWE IS_WEAKNESS_TYPE relationships (batch size: 5000)..."

    RESULT=$(cypher_query -d neo4j "
    CALL apoc.periodic.iterate(
      \"LOAD CSV WITH HEADERS FROM 'file:///CVE_CWE_2025.csv' AS row
       WHERE row.\\\`CWE-ID\\\` IS NOT NULL
         AND row.\\\`CWE-ID\\\` <> ''
         AND row.\\\`CWE-ID\\\` <> 'NVD-CWE-Other'
         AND row.\\\`CWE-ID\\\` <> 'NVD-CWE-noinfo'
       RETURN row\",
      \"MATCH (cve:CVE {id: row.\\\`CVE-ID\\\`})
       MERGE (cwe:CWE {id: row.\\\`CWE-ID\\\`})
       ON CREATE SET cwe.source = 'kaggle:cve_cwe_2025',
                     cwe.created_timestamp = datetime()
       MERGE (cve)-[r:IS_WEAKNESS_TYPE]->(cwe)
       ON CREATE SET r.source = 'kaggle:cve_cwe_2025',
                     r.created_timestamp = datetime()
       RETURN count(*)\",
      {batchSize: 5000, parallel: false}
    ) YIELD batches, total, errorMessages
    RETURN batches, total, errorMessages
    ")

    echo "$RESULT" | tee -a "$LOG_FILE"
    store_memory "cwe_relationships" "{\"result\":\"$RESULT\",\"timestamp\":\"$(date -Iseconds)\"}"
}

verify_results() {
    log_info "Verifying enrichment results..."

    # Check CVSS coverage
    log_info "CVSS Coverage:"
    cypher_query -d neo4j "
    MATCH (c:CVE)
    WITH count(c) AS total,
         count(c.cvssV31BaseScore) AS has_cvss31,
         count(c.kaggle_enriched_timestamp) AS kaggle_enriched
    RETURN total, has_cvss31, kaggle_enriched,
           round(100.0 * has_cvss31 / total, 2) AS cvss31_coverage_pct
    " | tee -a "$LOG_FILE"

    # Check CWE relationships
    log_info "CWE Relationships:"
    cypher_query -d neo4j "
    MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
    RETURN count(r) AS cwe_relationships,
           count(DISTINCT cwe) AS unique_cwes
    " | tee -a "$LOG_FILE"

    # Store final results
    FINAL_STATS=$(cypher_query -d neo4j "
    MATCH (c:CVE)
    WITH count(c) AS total, count(c.cvssV31BaseScore) AS enriched
    RETURN '{\"total_cves\":' || total || ',\"cvss_enriched\":' || enriched || ',\"coverage_pct\":' || round(100.0*enriched/total,2) || '}'
    " --format plain | tail -1)

    store_memory "final_results" "$FINAL_STATS"
}

cleanup() {
    log_info "Cleaning up temporary files..."
    rm -rf "$WORK_DIR"
    docker exec "$NEO4J_CONTAINER" rm -f /var/lib/neo4j/import/CVE_CWE_2025.csv || true
}

main() {
    mkdir -p /var/log/aeon
    mkdir -p "$(dirname "$LOG_FILE")"

    log_info "========================================="
    log_info "PROC-102: Kaggle Dataset Enrichment"
    log_info "========================================="

    check_preconditions || {
        log_error "Pre-condition check failed"
        exit 1
    }

    download_datasets || {
        log_error "Dataset download failed"
        exit 1
    }

    copy_to_neo4j
    create_constraints
    enrich_cvss_scores
    create_cwe_relationships
    verify_results
    cleanup

    log_info "========================================="
    log_info "PROC-102 COMPLETED SUCCESSFULLY"
    log_info "========================================="
}

main "$@"
