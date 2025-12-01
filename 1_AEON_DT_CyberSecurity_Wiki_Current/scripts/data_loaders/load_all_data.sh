#!/bin/bash
# AEON Cyber Digital Twin - Master Data Loading Script
# =====================================================
# Loads CVE, STIX, and EPSS data into Neo4j
#
# Usage:
#   ./load_all_data.sh [--cve-only|--stix-only|--epss-only]
#
# Environment Variables:
#   NEO4J_URI      - Neo4j connection URI (default: bolt://localhost:7687)
#   NEO4J_USER     - Neo4j username (default: neo4j)
#   NEO4J_PASSWORD - Neo4j password (required)
#
# Created: 2025-11-29

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${DATA_DIR:-/tmp/aeon_data_staging}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        AEON Cyber Digital Twin - Data Loader               ║${NC}"
echo -e "${BLUE}║        Version 1.0.0 - November 2025                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check required environment
if [ -z "$NEO4J_PASSWORD" ]; then
    echo -e "${RED}ERROR: NEO4J_PASSWORD environment variable is required${NC}"
    echo "Usage: NEO4J_PASSWORD='password' $0 [options]"
    exit 1
fi

# Set defaults
export NEO4J_URI="${NEO4J_URI:-bolt://localhost:7687}"
export NEO4J_USER="${NEO4J_USER:-neo4j}"

echo -e "${YELLOW}Neo4j Connection:${NC} $NEO4J_URI (user: $NEO4J_USER)"
echo ""

# Parse command line options
CVE_ONLY=false
STIX_ONLY=false
EPSS_ONLY=false
SKIP_DOWNLOAD=false

for arg in "$@"; do
    case $arg in
        --cve-only)
            CVE_ONLY=true
            shift
            ;;
        --stix-only)
            STIX_ONLY=true
            shift
            ;;
        --epss-only)
            EPSS_ONLY=true
            shift
            ;;
        --skip-download)
            SKIP_DOWNLOAD=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --cve-only       Only load CVE data"
            echo "  --stix-only      Only load STIX/MITRE ATT&CK data"
            echo "  --epss-only      Only enrich with EPSS scores"
            echo "  --skip-download  Skip data download (use existing files)"
            echo ""
            exit 0
            ;;
    esac
done

# Create data directory
mkdir -p "$DATA_DIR"

# Function to download CVE data
download_cve_data() {
    echo -e "${BLUE}[1/3] Downloading CVE data from NVD mirror...${NC}"

    for year in 2023 2024 2025; do
        if [ ! -f "$DATA_DIR/CVE-$year.json" ]; then
            echo "  Downloading CVE-$year.json.xz..."
            curl -L -o "$DATA_DIR/CVE-$year.json.xz" \
                "https://github.com/fkie-cad/nvd-json-data-feeds/releases/latest/download/CVE-$year.json.xz" \
                2>/dev/null
            echo "  Extracting CVE-$year.json..."
            xz -dk "$DATA_DIR/CVE-$year.json.xz" || true
        else
            echo "  CVE-$year.json already exists"
        fi
    done

    echo -e "${GREEN}  CVE data download complete${NC}"
}

# Function to download STIX data
download_stix_data() {
    echo -e "${BLUE}[2/3] Downloading STIX/MITRE ATT&CK data...${NC}"

    if [ ! -f "$DATA_DIR/enterprise-attack.json" ]; then
        echo "  Downloading enterprise-attack.json..."
        curl -L -o "$DATA_DIR/enterprise-attack.json" \
            "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json" \
            2>/dev/null
    else
        echo "  enterprise-attack.json already exists"
    fi

    echo -e "${GREEN}  STIX data download complete${NC}"
}

# Function to load CVE data
load_cve_data() {
    echo -e "${BLUE}Loading CVE data into Neo4j...${NC}"

    for year in 2023 2024 2025; do
        if [ -f "$DATA_DIR/CVE-$year.json" ]; then
            echo "  Loading CVE-$year.json..."
            python3 "$SCRIPT_DIR/load_cve_nvd.py" "$DATA_DIR/CVE-$year.json"
        fi
    done

    echo -e "${GREEN}  CVE data loaded${NC}"
}

# Function to load STIX data
load_stix_data() {
    echo -e "${BLUE}Loading STIX/MITRE ATT&CK data into Neo4j...${NC}"

    if [ -f "$DATA_DIR/enterprise-attack.json" ]; then
        python3 "$SCRIPT_DIR/load_stix_attack.py" "$DATA_DIR/enterprise-attack.json"
    fi

    echo -e "${GREEN}  STIX data loaded${NC}"
}

# Function to enrich with EPSS
enrich_epss() {
    echo -e "${BLUE}Enriching CVEs with EPSS scores...${NC}"
    python3 "$SCRIPT_DIR/enrich_epss.py" --batch 100 5000
    echo -e "${GREEN}  EPSS enrichment complete${NC}"
}

# Main execution
START_TIME=$(date +%s)

if [ "$EPSS_ONLY" = true ]; then
    enrich_epss
elif [ "$CVE_ONLY" = true ]; then
    if [ "$SKIP_DOWNLOAD" = false ]; then
        download_cve_data
    fi
    load_cve_data
elif [ "$STIX_ONLY" = true ]; then
    if [ "$SKIP_DOWNLOAD" = false ]; then
        download_stix_data
    fi
    load_stix_data
else
    # Full load
    if [ "$SKIP_DOWNLOAD" = false ]; then
        download_cve_data
        download_stix_data
    fi
    load_cve_data
    load_stix_data
    enrich_epss
fi

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    Loading Complete!                       ║${NC}"
echo -e "${GREEN}║                    Time: ${ELAPSED}s                              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"

# Show summary query
echo ""
echo -e "${YELLOW}Run these Cypher queries to verify the data:${NC}"
echo ""
echo "// Count all nodes"
echo "MATCH (n) RETURN labels(n)[0] AS Label, count(n) AS Count ORDER BY Count DESC"
echo ""
echo "// High-risk CVEs (CVSS >= 9.0)"
echo "MATCH (cve:CVE) WHERE cve.cvssBase >= 9.0 RETURN cve.cveId, cve.cvssBase, cve.severity LIMIT 10"
echo ""
echo "// MITRE ATT&CK techniques"
echo "MATCH (a:AttackPattern) RETURN a.mitreId, a.name LIMIT 10"
