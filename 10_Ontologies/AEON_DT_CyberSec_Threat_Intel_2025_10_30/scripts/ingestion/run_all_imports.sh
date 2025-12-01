#!/bin/bash
# AEON Digital Twin CyberSec Threat Intel - Complete Import Workflow
# This script runs all ingestion scripts in the correct order

set -e  # Exit on error

echo "============================================="
echo "AEON Digital Twin - Threat Intel Import"
echo "============================================="
echo ""

# Check environment variables
if [ -z "$NEO4J_URI" ]; then
    echo "ERROR: NEO4J_URI not set"
    echo "Export: export NEO4J_URI='bolt://localhost:7687'"
    exit 1
fi

if [ -z "$NEO4J_USER" ]; then
    echo "ERROR: NEO4J_USER not set"
    echo "Export: export NEO4J_USER='neo4j'"
    exit 1
fi

if [ -z "$NEO4J_PASSWORD" ]; then
    echo "ERROR: NEO4J_PASSWORD not set"
    echo "Export: export NEO4J_PASSWORD='your_password'"
    exit 1
fi

echo "Neo4j Configuration:"
echo "  URI: $NEO4J_URI"
echo "  User: $NEO4J_USER"
echo ""

# Check if NVD API key is set
if [ -z "$NVD_API_KEY" ]; then
    echo "WARNING: NVD_API_KEY not set (will use lower rate limits)"
    echo "Recommended: export NVD_API_KEY='your_api_key'"
    echo ""
fi

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies if needed
if ! python3 -c "import neo4j" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# 1. Import NVD CVE data
echo "============================================="
echo "Step 1: Importing NVD CVE data"
echo "============================================="
python3 nvd_cve_importer.py
echo ""

# 2. Import MITRE ATT&CK framework
echo "============================================="
echo "Step 2: Importing MITRE ATT&CK framework"
echo "============================================="
python3 mitre_attack_importer.py
echo ""

# 3. Load asset hierarchy
echo "============================================="
echo "Step 3: Loading asset hierarchy"
echo "============================================="
if [ -f "examples/assets.csv" ]; then
    python3 asset_hierarchy_loader.py
else
    echo "WARNING: examples/assets.csv not found, skipping..."
fi
echo ""

# 4. Load network topology
echo "============================================="
echo "Step 4: Loading network topology"
echo "============================================="
if [ -f "examples/network_segments.csv" ]; then
    python3 network_topology_loader.py
else
    echo "WARNING: examples/network_segments.csv not found, skipping..."
fi
echo ""

# 5. Import threat intelligence
echo "============================================="
echo "Step 5: Importing threat intelligence"
echo "============================================="
if [ -f "threat_intel_bundle.json" ]; then
    python3 threat_intel_importer.py
else
    echo "WARNING: threat_intel_bundle.json not found, skipping..."
    echo "Note: You need to provide a STIX bundle or TAXII server configuration"
fi
echo ""

echo "============================================="
echo "Import Complete!"
echo "============================================="
echo ""
echo "Check log files for details:"
echo "  - nvd_importer.log"
echo "  - mitre_attack_importer.log"
echo "  - asset_loader.log"
echo "  - network_loader.log"
echo "  - threat_intel_importer.log"
echo ""
echo "Connect to Neo4j and run queries to explore the data:"
echo "  bolt://$NEO4J_URI"
echo ""
