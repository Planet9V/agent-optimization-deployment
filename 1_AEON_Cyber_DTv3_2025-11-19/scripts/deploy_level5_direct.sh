#!/bin/bash
# Direct Level 5 Deployment to Neo4j
# Uses efficient UNWIND batching

LOG_FILE="/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/reports/level5_deployment_log.txt"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

run_cypher() {
    local query="$1"
    local desc="$2"
    log_message "Executing: $desc"
    echo "$query" | docker exec -i openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' 2>&1 | tee -a "$LOG_FILE"
    log_message "✓ Completed: $desc"
}

log_message "================================================================================"
log_message "LEVEL 5 INFORMATION STREAMS - DIRECT NEO4J DEPLOYMENT"
log_message "================================================================================"
log_message "Start time: $(date '+%Y-%m-%d %H:%M:%S')"

# Step 1: Create indexes
log_message "Creating indexes..."
run_cypher "CREATE INDEX IF NOT EXISTS FOR (n:InformationEvent) ON (n.eventId);" "InformationEvent.eventId index"
run_cypher "CREATE INDEX IF NOT EXISTS FOR (n:GeopoliticalEvent) ON (n.eventId);" "GeopoliticalEvent.eventId index"
run_cypher "CREATE INDEX IF NOT EXISTS FOR (n:CognitiveBias) ON (n.biasId);" "CognitiveBias.biasId index"

# Step 2: Create ThreatFeeds (3 nodes)
log_message "Creating ThreatFeed nodes..."
run_cypher "
CREATE (tf:ThreatFeed:DataSource:Integration:RealTime:Level5 {
  feedId: 'TF-001',
  feedName: 'CISA_AIS',
  feedType: 'STIX',
  reliability: 0.95,
  latency: 2
})
RETURN tf.feedId;
" "ThreatFeed TF-001"

run_cypher "
CREATE (tf:ThreatFeed:DataSource:Integration:RealTime:Level5 {
  feedId: 'TF-002',
  feedName: 'Commercial_Aggregate',
  feedType: 'Multiple',
  reliability: 0.85,
  latency: 5
})
RETURN tf.feedId;
" "ThreatFeed TF-002"

run_cypher "
CREATE (tf:ThreatFeed:DataSource:Integration:RealTime:Level5 {
  feedId: 'TF-003',
  feedName: 'OSINT_Collection',
  feedType: 'Custom',
  reliability: 0.70,
  latency: 15
})
RETURN tf.feedId;
" "ThreatFeed TF-003"

# Step 3: Create EventProcessors (10 nodes)
log_message "Creating EventProcessor nodes..."
for i in {1..10}; do
    run_cypher "
    CREATE (ep:EventProcessor:Pipeline:Processing:Level5 {
      processorId: 'EP-$(printf "%03d" $i)',
      processorName: 'Processor_$i',
      processorType: 'analysis',
      eventsProcessed: $((i * 500)),
      latency: $(echo "scale=1; $i * 0.5" | bc)
    })
    RETURN ep.processorId;
    " "EventProcessor EP-$(printf "%03d" $i)"
done

# Step 4: Create CognitiveBiases (30 nodes)
log_message "Creating CognitiveBias nodes..."
biases=("availability_bias" "confirmation_bias" "recency_bias" "normalcy_bias" "authority_bias"
        "bandwagon_effect" "hindsight_bias" "planning_fallacy" "sunk_cost_fallacy" "status_quo_bias"
        "zero_risk_bias" "neglect_of_probability" "clustering_illusion" "gambler_fallacy" "hot_hand_fallacy"
        "illusion_of_control" "overconfidence_bias" "pessimism_bias" "optimism_bias" "self_serving_bias"
        "attribution_bias" "halo_effect" "horn_effect" "contrast_effect" "primacy_effect"
        "anchoring_bias" "framing_effect" "groupthink" "fundamental_attribution_error" "outcome_bias")

for i in {1..30}; do
    bias="${biases[$((i-1))]}"
    run_cypher "
    CREATE (cb:CognitiveBias:Psychology:Decision:Level4:Level5 {
      biasId: 'CB-$(printf "%03d" $i)',
      biasName: '$bias',
      category: 'DECISION',
      activationThreshold: $(echo "scale=1; 5 + ($i % 20) * 0.2" | bc),
      currentLevel: $(echo "scale=1; 6 + ($i % 15) * 0.1" | bc)
    })
    RETURN cb.biasId;
    " "CognitiveBias CB-$(printf "%03d" $i)"
done

# Step 5: Create InformationEvents (5000 nodes) - in batches of 100
log_message "Creating InformationEvent nodes (5000 in batches)..."
python3 <<'PYTHON_SCRIPT'
import subprocess
from datetime import datetime, timedelta

def run_batch_cypher(batch_num, start_id, end_id):
    events = []
    event_types = ['CVE_DISCLOSURE', 'BREACH_REPORT', 'VULNERABILITY_SCAN', 'PATCH_RELEASE', 'THREAT_INTEL']
    severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    sources = ['NVD', 'CISA', 'SecurityFeed', 'MediaReport', 'Internal']
    sectors = ['Financial Services', 'Healthcare', 'Government', 'Energy', 'IT', 'Retail']

    start_date = datetime(2025, 1, 1)

    for i in range(start_id, end_id + 1):
        event_type = event_types[i % len(event_types)]
        severity = severities[i % len(severities)]
        source = sources[i % len(sources)]
        sector = sectors[i % len(sectors)]

        if severity == 'CRITICAL':
            cvss = 9.0 + (i % 10) * 0.1
            epss = 0.85 + (i % 15) * 0.01
        elif severity == 'HIGH':
            cvss = 7.0 + (i % 20) * 0.1
            epss = 0.50 + (i % 40) * 0.01
        elif severity == 'MEDIUM':
            cvss = 4.0 + (i % 30) * 0.1
            epss = 0.20 + (i % 30) * 0.01
        else:
            cvss = 2.0 + (i % 20) * 0.1
            epss = 0.05 + (i % 10) * 0.01

        fear_factor = round(min(10.0, cvss * 0.7), 1)
        reality_factor = round(min(10.0, cvss * 0.8), 1)
        fear_reality_gap = round(fear_factor - reality_factor, 1)

        days_offset = (i * 365) // 5000
        timestamp = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%dT%H:%M:%SZ")

        events.append(f"""
        {{
          eventId: 'IE-2025-{i:05d}',
          eventType: '{event_type}',
          timestamp: '{timestamp}',
          source: '{source}',
          severity: '{severity}',
          cvssScore: {cvss:.1f},
          epssScore: {epss:.2f},
          affectedSector: '{sector}',
          fearFactor: {fear_factor},
          realityFactor: {reality_factor},
          fearRealityGap: {fear_reality_gap}
        }}""")

    cypher_query = f"""
    UNWIND [{','.join(events)}] AS event
    CREATE (ie:InformationEvent:Event:Information:RealTime:Level5)
    SET ie = event
    RETURN count(ie) as created;
    """

    cmd = ['docker', 'exec', '-i', 'openspg-neo4j',
           'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg']

    result = subprocess.run(cmd, input=cypher_query, capture_output=True, text=True)
    print(f"Batch {batch_num}: Events {start_id}-{end_id} - {result.stdout.strip()}")

# Create 5000 events in batches of 100
for batch in range(50):
    start_id = batch * 100 + 1
    end_id = min((batch + 1) * 100, 5000)
    run_batch_cypher(batch + 1, start_id, end_id)
    print(f"✓ Batch {batch + 1} complete")

print("✓ All 5000 InformationEvent nodes created")
PYTHON_SCRIPT

# Step 6: Create GeopoliticalEvents (500 nodes) - in batches of 50
log_message "Creating GeopoliticalEvent nodes (500 in batches)..."
python3 <<'PYTHON_SCRIPT2'
import subprocess
from datetime import datetime, timedelta

def run_geo_batch(batch_num, start_id, end_id):
    events = []
    event_types = ['SANCTIONS', 'CONFLICT', 'DIPLOMATIC', 'ECONOMIC', 'ELECTION']
    country_pairs = [
        "['US', 'RU']", "['US', 'CN']", "['UA', 'RU']", "['US', 'IR']",
        "['CN', 'TW']", "['IL', 'IR']", "['US', 'KP']", "['IN', 'PK']"
    ]
    apt_groups = [
        "['APT28', 'APT29']", "['APT40', 'APT41']", "['Sandworm']",
        "['APT33', 'APT34']", "['Lazarus', 'Kimsuky']"
    ]

    start_date = datetime(2025, 1, 1)

    for i in range(start_id, end_id + 1):
        event_type = event_types[i % len(event_types)]
        countries = country_pairs[i % len(country_pairs)]
        apts = apt_groups[i % len(apt_groups)]

        tension_level = round(5.0 + (i % 50) * 0.1, 1)
        cyber_correlation = round(0.30 + (i % 70) * 0.01, 2)

        days_offset = (i * 365) // 500
        timestamp = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%dT%H:%M:%SZ")

        events.append(f"""
        {{
          eventId: 'GE-2025-{i:03d}',
          eventType: '{event_type}',
          timestamp: '{timestamp}',
          countries: {countries},
          tensionLevel: {tension_level},
          cyberCorrelation: {cyber_correlation},
          aptGroups: {apts}
        }}""")

    cypher_query = f"""
    UNWIND [{','.join(events)}] AS event
    CREATE (ge:GeopoliticalEvent:Event:Geopolitical:RealTime:Level5)
    SET ge = event
    RETURN count(ge) as created;
    """

    cmd = ['docker', 'exec', '-i', 'openspg-neo4j',
           'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg']

    result = subprocess.run(cmd, input=cypher_query, capture_output=True, text=True)
    print(f"Batch {batch_num}: GeoEvents {start_id}-{end_id} - {result.stdout.strip()}")

# Create 500 events in batches of 50
for batch in range(10):
    start_id = batch * 50 + 1
    end_id = min((batch + 1) * 50, 500)
    run_geo_batch(batch + 1, start_id, end_id)
    print(f"✓ Batch {batch + 1} complete")

print("✓ All 500 GeopoliticalEvent nodes created")
PYTHON_SCRIPT2

# Step 7: Verify deployment
log_message "================================================================================"
log_message "VERIFICATION"
log_message "================================================================================"

run_cypher "MATCH (n:InformationEvent) RETURN count(n) as count;" "InformationEvent count"
run_cypher "MATCH (n:GeopoliticalEvent) RETURN count(n) as count;" "GeopoliticalEvent count"
run_cypher "MATCH (n:ThreatFeed) RETURN count(n) as count;" "ThreatFeed count"
run_cypher "MATCH (n:CognitiveBias) RETURN count(n) as count;" "CognitiveBias count"
run_cypher "MATCH (n:EventProcessor) RETURN count(n) as count;" "EventProcessor count"
run_cypher "MATCH (n:Level5) RETURN count(n) as count;" "Total Level5 nodes"
run_cypher "MATCH (n) RETURN count(n) as total_nodes;" "Total database nodes"

log_message "================================================================================"
log_message "DEPLOYMENT COMPLETE"
log_message "================================================================================"
log_message "End time: $(date '+%Y-%m-%d %H:%M:%S')"
