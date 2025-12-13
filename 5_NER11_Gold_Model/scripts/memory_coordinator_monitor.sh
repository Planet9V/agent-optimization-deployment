#!/bin/bash
# Memory Coordinator - Continuous Neo4j Metrics Monitoring
# Stores graph state updates every 5 minutes to Claude-Flow reasoning bank

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/logs/memory_coordinator.log"

mkdir -p "$PROJECT_ROOT/logs"

log_message() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1" | tee -a "$LOG_FILE"
}

log_message "Memory coordinator started - monitoring every 5 minutes"

# Initial notification
npx claude-flow@alpha hooks notify --message "Memory coordinator monitoring initialized"

# Continuous monitoring loop
while true; do
    # Get current Neo4j metrics
    NODE_COUNT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
        "MATCH (n) RETURN count(n) as total" --format plain 2>/dev/null | tail -1)

    REL_COUNT=$(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
        "MATCH ()-[r]->() RETURN count(r) as total" --format plain 2>/dev/null | tail -1)

    # Get label distribution
    LABEL_STATS=$(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
        "CALL db.labels() YIELD label CALL apoc.cypher.run('MATCH (n:'+label+') RETURN count(n) as count', {}) YIELD value RETURN label, value.count as count ORDER BY count DESC LIMIT 10" \
        --format plain 2>/dev/null)

    TIMESTAMP=$(date +%s)
    TIMESTAMP_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    if [ -n "$NODE_COUNT" ] && [ -n "$REL_COUNT" ]; then
        # Store to reasoning bank
        npx claude-flow@alpha memory store \
            "neo4j-metrics-$TIMESTAMP" \
            "{\"nodes\":$NODE_COUNT,\"relationships\":$REL_COUNT,\"timestamp\":\"$TIMESTAMP_ISO\",\"source\":\"E01_monitoring\"}" \
            --reasoningbank 2>&1 | grep -E "(✅|Memory ID)" >> "$LOG_FILE"

        log_message "Stored metrics: nodes=$NODE_COUNT, relationships=$REL_COUNT"

        # Notify coordination system
        npx claude-flow@alpha hooks notify \
            --message "Neo4j state: $NODE_COUNT nodes, $REL_COUNT relationships" 2>&1 | grep -E "(✅|Notification)" >> "$LOG_FILE"
    else
        log_message "WARNING: Unable to retrieve Neo4j metrics"
    fi

    # Wait 5 minutes
    sleep 300
done
