#!/bin/bash
# Monitor EPSS Enrichment Progress

echo "=== EPSS Enrichment Progress Monitor ==="
echo "Started: $(date)"
echo

while true; do
    clear
    echo "=== EPSS Enrichment Progress Monitor ==="
    echo "Current Time: $(date)"
    echo

    # Check if process is still running
    if ps aux | grep -q "[p]hase1_epss_enrichment.py"; then
        echo "Status: RUNNING ✓"
    else
        echo "Status: COMPLETED or STOPPED"
        break
    fi

    echo
    echo "--- Last 10 Log Lines ---"
    tail -n 10 /tmp/epss_enrichment_output.log 2>/dev/null || echo "No log file yet"

    echo
    echo "--- Checkpoints ---"
    ls -lh /tmp/epss_checkpoint_*.json 2>/dev/null | tail -n 5 || echo "No checkpoints yet"

    echo
    echo "--- Neo4j Enrichment Stats (sample 1000) ---"
    docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
        "MATCH (c:CVE) WHERE c.epss_score IS NOT NULL RETURN count(c) AS enriched LIMIT 1" 2>/dev/null || echo "Unable to query"

    echo
    echo "Press Ctrl+C to exit monitor..."
    sleep 30
done

echo
echo "Process completed. Final report:"
cat /tmp/epss_enrichment_report.txt 2>/dev/null || echo "No report found yet"
