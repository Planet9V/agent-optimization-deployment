#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Master Data Loading Execution Script
# Created: 2025-11-28
# Purpose: Execute complete CVE/CAPEC/CWE data loading pipeline
# ═══════════════════════════════════════════════════════════════

set -e  # Exit on error

SCRIPT_DIR="/home/jim/2_OXOT_Projects_Dev/scripts"
LOG_FILE="/home/jim/2_OXOT_Projects_Dev/BLOTTER"

echo "═══════════════════════════════════════════════════════════════"
echo "DATA LOADING PIPELINE - STARTED: $(date)"
echo "═══════════════════════════════════════════════════════════════"

# ───────────────────────────────────────────────────────────────
# Step 1: Setup Neo4j Schema
# ───────────────────────────────────────────────────────────────

echo ""
echo "[1/6] Setting up Neo4j schema and constraints..."
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  < "$SCRIPT_DIR/neo4j_schema_setup.cypher"

if [ $? -eq 0 ]; then
  echo "✅ Schema setup complete"
  echo "$(date) - Schema setup complete" >> "$LOG_FILE"
else
  echo "❌ Schema setup failed"
  echo "$(date) - Schema setup FAILED" >> "$LOG_FILE"
  exit 1
fi

# ───────────────────────────────────────────────────────────────
# Step 2: Load CWE Data
# ───────────────────────────────────────────────────────────────

echo ""
echo "[2/6] Loading CWE weakness data..."
python3 "$SCRIPT_DIR/load_cwe_data.py"

if [ $? -eq 0 ]; then
  CWE_COUNT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
    "MATCH (c:CWE) RETURN count(c) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)
  echo "✅ CWE data loaded: $CWE_COUNT weaknesses"
  echo "$(date) - CWE data loaded: $CWE_COUNT weaknesses" >> "$LOG_FILE"
else
  echo "❌ CWE loading failed"
  echo "$(date) - CWE loading FAILED" >> "$LOG_FILE"
  exit 1
fi

# ───────────────────────────────────────────────────────────────
# Step 3: Load CAPEC Data
# ───────────────────────────────────────────────────────────────

echo ""
echo "[3/6] Loading CAPEC attack patterns..."
python3 "$SCRIPT_DIR/load_capec_data.py"

if [ $? -eq 0 ]; then
  CAPEC_COUNT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
    "MATCH (c:CAPEC) RETURN count(c) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)
  echo "✅ CAPEC data loaded: $CAPEC_COUNT patterns"
  echo "$(date) - CAPEC data loaded: $CAPEC_COUNT patterns" >> "$LOG_FILE"
else
  echo "❌ CAPEC loading failed"
  echo "$(date) - CAPEC loading FAILED" >> "$LOG_FILE"
  exit 1
fi

# ───────────────────────────────────────────────────────────────
# Step 4: Load VulnCheck KEV Data
# ───────────────────────────────────────────────────────────────

echo ""
echo "[4/6] Loading VulnCheck KEV exploit data..."
python3 "$SCRIPT_DIR/load_vulncheck_kev.py"

if [ $? -eq 0 ]; then
  KEV_COUNT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
    "MATCH (c:CVE {hasExploit: true}) WHERE c.customer_namespace = 'shared:vulncheck-kev' RETURN count(c) AS count;" \
    2>/dev/null | grep -o '[0-9]*' | tail -1)
  echo "✅ VulnCheck KEV data loaded: $KEV_COUNT CVEs with exploits"
  echo "$(date) - VulnCheck KEV data loaded: $KEV_COUNT CVEs" >> "$LOG_FILE"
else
  echo "❌ VulnCheck KEV loading failed"
  echo "$(date) - VulnCheck KEV loading FAILED" >> "$LOG_FILE"
  exit 1
fi

# ───────────────────────────────────────────────────────────────
# Step 5: Verification Queries
# ───────────────────────────────────────────────────────────────

echo ""
echo "[5/6] Running verification queries..."

echo "Counting total entities..."
TOTAL_CVES=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (c:CVE) RETURN count(c) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)

TOTAL_CWES=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (c:CWE) RETURN count(c) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)

TOTAL_CAPECS=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (c:CAPEC) RETURN count(c) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)

echo "Counting relationships..."
CVE_CWE_RELS=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH ()-[r:IS_WEAKNESS_TYPE]->() RETURN count(r) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)

CVE_CAPEC_RELS=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH ()-[r:ENABLES_ATTACK_PATTERN]->() RETURN count(r) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)

CAPEC_CWE_RELS=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH ()-[r:EXPLOITS_WEAKNESS]->() RETURN count(r) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)

EXPLOIT_EVIDENCE=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (e:ExploitEvidence) RETURN count(e) AS count;" 2>/dev/null | grep -o '[0-9]*' | tail -1)

echo "✅ Verification complete"

# ───────────────────────────────────────────────────────────────
# Step 6: Generate Report
# ───────────────────────────────────────────────────────────────

echo ""
echo "[6/6] Generating final report..."

REPORT="
═══════════════════════════════════════════════════════════════
DATA LOADING COMPLETE - $(date)
═══════════════════════════════════════════════════════════════

ENTITY COUNTS:
  • CVEs:              $TOTAL_CVES
  • CWEs:              $TOTAL_CWES
  • CAPEC Patterns:    $TOTAL_CAPECS
  • Exploit Evidence:  $EXPLOIT_EVIDENCE

RELATIONSHIP COUNTS:
  • CVE → CWE:         $CVE_CWE_RELS
  • CVE → CAPEC:       $CVE_CAPEC_RELS
  • CAPEC → CWE:       $CAPEC_CWE_RELS

EXPLOIT INTELLIGENCE:
  • CVEs with exploits: $KEV_COUNT
  • Exploit evidence:   $EXPLOIT_EVIDENCE

STATUS: ✅ COMPLETE

Next steps:
1. Run NVD API updates for recent CVEs
2. Configure VulnCheck API for KEV updates
3. Test graph queries and relationships
4. Integrate with ICS/SCADA vulnerability data

═══════════════════════════════════════════════════════════════
"

echo "$REPORT"
echo "$REPORT" >> "$LOG_FILE"

echo ""
echo "📝 Full report logged to: $LOG_FILE"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ DATA LOADING PIPELINE COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
