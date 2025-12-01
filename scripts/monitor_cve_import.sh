#!/bin/bash
# Monitor CVE Bulk Import Progress

echo "=========================================="
echo "CVE Bulk Import - Real-Time Monitoring"
echo "=========================================="
echo ""

# Check if import is running
if pgrep -f "import_cve_bulk.py" > /dev/null; then
    echo "✓ Import process is RUNNING"
    ps aux | grep import_cve_bulk.py | grep -v grep
else
    echo "✗ Import process is NOT running"
fi

echo ""
echo "----------------------------------------"
echo "Neo4j CVE Count"
echo "----------------------------------------"

# Count CVEs in Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n:CVE {namespace: 'CybersecurityKB'})
   RETURN count(n) as total_cves;" 2>/dev/null | tail -1

echo ""
echo "----------------------------------------"
echo "CVEs by Year"
echo "----------------------------------------"

# Count by year
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n:CVE {namespace: 'CybersecurityKB'})
   WHERE n.published_date IS NOT NULL
   WITH n.published_date.year as year, count(*) as count
   RETURN year, count
   ORDER BY year DESC
   LIMIT 10;" 2>/dev/null

echo ""
echo "----------------------------------------"
echo "Progress File Status"
echo "----------------------------------------"

PROGRESS_FILE="/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder/cve_import_progress.json"

if [ -f "$PROGRESS_FILE" ]; then
    echo "✓ Progress file exists"
    echo ""
    cat "$PROGRESS_FILE" | python3 -m json.tool 2>/dev/null | head -20
else
    echo "✗ No progress file found"
fi

echo ""
echo "----------------------------------------"
echo "Latest Import Log (last 20 lines)"
echo "----------------------------------------"

if [ -f "/tmp/cve_bulk_import.log" ]; then
    tail -20 /tmp/cve_bulk_import.log
else
    echo "No log file found at /tmp/cve_bulk_import.log"
fi

echo ""
echo "=========================================="
echo "Run this script again to refresh status:"
echo "bash /home/jim/2_OXOT_Projects_Dev/scripts/monitor_cve_import.sh"
echo "=========================================="
