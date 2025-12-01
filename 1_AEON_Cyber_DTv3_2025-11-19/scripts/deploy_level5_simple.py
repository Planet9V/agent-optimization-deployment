#!/usr/bin/env python3
"""Simple Level 5 Deployment to Neo4j"""
import subprocess
import sys
from datetime import datetime, timedelta

def cypher(query, desc=""):
    """Execute Cypher query"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {desc}")
    cmd = ['docker', 'exec', '-i', 'openspg-neo4j',
           'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg']
    result = subprocess.run(cmd, input=query, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:200]}")
    else:
        print(f"  OK: {result.stdout.strip()[:100]}")
    return result.returncode == 0

print("="*80)
print("LEVEL 5 DEPLOYMENT TO NEO4J")
print("="*80)

# 1. Indexes
print("\n1. Creating indexes...")
cypher("CREATE INDEX IF NOT EXISTS FOR (n:InformationEvent) ON (n.eventId);", "InfoEvent index")
cypher("CREATE INDEX IF NOT EXISTS FOR (n:GeopoliticalEvent) ON (n.eventId);", "GeoEvent index")
cypher("CREATE INDEX IF NOT EXISTS FOR (n:CognitiveBias) ON (n.biasId);", "Bias index")

# 2. ThreatFeeds (3)
print("\n2. Creating ThreatFeed nodes (3)...")
for i in range(1, 4):
    cypher(f"""
CREATE (tf:ThreatFeed:Level5 {{
  feedId: 'TF-{i:03d}',
  feedName: 'Feed_{i}',
  reliability: {0.7 + i * 0.1:.2f}
}}) RETURN tf.feedId;
""", f"ThreatFeed {i}")

# 3. EventProcessors (10)
print("\n3. Creating EventProcessor nodes (10)...")
for i in range(1, 11):
    cypher(f"""
CREATE (ep:EventProcessor:Level5 {{
  processorId: 'EP-{i:03d}',
  processorName: 'Processor_{i}',
  latency: {i * 0.5:.1f}
}}) RETURN ep.processorId;
""", f"EventProcessor {i}")

# 4. CognitiveBiases (30)
print("\n4. Creating CognitiveBias nodes (30)...")
biases = [
    "availability_bias", "confirmation_bias", "recency_bias", "normalcy_bias",
    "authority_bias", "bandwagon_effect", "hindsight_bias", "planning_fallacy",
    "sunk_cost_fallacy", "status_quo_bias", "zero_risk_bias", "neglect_of_probability",
    "clustering_illusion", "gambler_fallacy", "hot_hand_fallacy", "illusion_of_control",
    "overconfidence_bias", "pessimism_bias", "optimism_bias", "self_serving_bias",
    "attribution_bias", "halo_effect", "horn_effect", "contrast_effect",
    "primacy_effect", "anchoring_bias", "framing_effect", "groupthink",
    "fundamental_attribution_error", "outcome_bias"
]
for i, bias_name in enumerate(biases, 1):
    cypher(f"""
CREATE (cb:CognitiveBias:Level5 {{
  biasId: 'CB-{i:03d}',
  biasName: '{bias_name}',
  currentLevel: {6.0 + (i % 10) * 0.2:.1f}
}}) RETURN cb.biasId;
""", f"Bias {i}/{30}")

# 5. InformationEvents (5000) - in batches
print("\n5. Creating InformationEvent nodes (5000)...")
event_types = ['CVE_DISCLOSURE', 'BREACH_REPORT', 'VULNERABILITY_SCAN', 'PATCH_RELEASE', 'THREAT_INTEL']
severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
sources = ['NVD', 'CISA', 'SecurityFeed', 'MediaReport', 'Internal']
sectors = ['Financial', 'Healthcare', 'Government', 'Energy', 'IT', 'Retail']

start_date = datetime(2025, 1, 1)
batch_size = 100

for batch in range(50):  # 50 batches of 100
    start_id = batch * 100 + 1
    end_id = (batch + 1) * 100

    events = []
    for i in range(start_id, end_id + 1):
        etype = event_types[i % len(event_types)]
        sev = severities[i % len(severities)]
        src = sources[i % len(sources)]
        sec = sectors[i % len(sectors)]

        cvss = 5.0 + (i % 5)
        epss = 0.5 + (i % 5) * 0.1
        fear = round(cvss * 0.7, 1)
        reality = round(cvss * 0.8, 1)
        gap = round(fear - reality, 1)

        days = (i * 365) // 5000
        ts = (start_date + timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")

        events.append(f"""{{
  eventId: 'IE-2025-{i:05d}',
  eventType: '{etype}',
  timestamp: '{ts}',
  source: '{src}',
  severity: '{sev}',
  cvssScore: {cvss:.1f},
  epssScore: {epss:.2f},
  sector: '{sec}',
  fearFactor: {fear},
  realityFactor: {reality},
  fearRealityGap: {gap}
}}""")

    cypher_query = f"""
UNWIND [{','.join(events)}] AS event
CREATE (ie:InformationEvent:Level5)
SET ie = event
RETURN count(ie);
"""

    cypher(cypher_query, f"InformationEvents batch {batch+1}/50 ({start_id}-{end_id})")

# 6. GeopoliticalEvents (500) - in batches
print("\n6. Creating GeopoliticalEvent nodes (500)...")
event_types_geo = ['SANCTIONS', 'CONFLICT', 'DIPLOMATIC', 'ECONOMIC', 'ELECTION']
countries = [
    "['US','RU']", "['US','CN']", "['UA','RU']", "['US','IR']",
    "['CN','TW']", "['IL','IR']", "['US','KP']", "['IN','PK']"
]
apts = [
    "['APT28','APT29']", "['APT40','APT41']", "['Sandworm']",
    "['APT33','APT34']", "['Lazarus']"
]

batch_size_geo = 50
for batch in range(10):  # 10 batches of 50
    start_id = batch * 50 + 1
    end_id = (batch + 1) * 50

    events = []
    for i in range(start_id, end_id + 1):
        etype = event_types_geo[i % len(event_types_geo)]
        ctry = countries[i % len(countries)]
        apt = apts[i % len(apts)]

        tension = round(5.0 + (i % 50) * 0.1, 1)
        corr = round(0.30 + (i % 70) * 0.01, 2)

        days = (i * 365) // 500
        ts = (start_date + timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")

        events.append(f"""{{
  eventId: 'GE-2025-{i:03d}',
  eventType: '{etype}',
  timestamp: '{ts}',
  countries: {ctry},
  tensionLevel: {tension},
  cyberCorrelation: {corr},
  aptGroups: {apt}
}}""")

    cypher_query = f"""
UNWIND [{','.join(events)}] AS event
CREATE (ge:GeopoliticalEvent:Level5)
SET ge = event
RETURN count(ge);
"""

    cypher(cypher_query, f"GeopoliticalEvents batch {batch+1}/10 ({start_id}-{end_id})")

# 7. Verify
print("\n" + "="*80)
print("VERIFICATION")
print("="*80)
cypher("MATCH (n:InformationEvent) RETURN count(n) as count;", "InformationEvent count")
cypher("MATCH (n:GeopoliticalEvent) RETURN count(n) as count;", "GeopoliticalEvent count")
cypher("MATCH (n:ThreatFeed) RETURN count(n) as count;", "ThreatFeed count")
cypher("MATCH (n:CognitiveBias) RETURN count(n) as count;", "CognitiveBias count")
cypher("MATCH (n:EventProcessor) RETURN count(n) as count;", "EventProcessor count")
cypher("MATCH (n:Level5) RETURN count(n) as count;", "Total Level5 nodes")
cypher("MATCH (n) RETURN count(n) as total;", "Total database nodes")

print("\n" + "="*80)
print("DEPLOYMENT COMPLETE")
print("="*80)
