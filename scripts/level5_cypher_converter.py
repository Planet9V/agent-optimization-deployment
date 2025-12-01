#!/usr/bin/env python3
"""
Convert Level 5 JSON data to Cypher statements
"""

import json
from datetime import datetime

def escape_string(s):
    """Escape string for Cypher"""
    if s is None:
        return 'null'
    if isinstance(s, str):
        return s.replace("'", "\\'").replace('"', '\\"')
    return str(s)

def dict_to_cypher_props(d):
    """Convert dictionary to Cypher property string"""
    props = []
    for key, value in d.items():
        if value is None:
            continue
        elif isinstance(value, str):
            props.append(f'{key}: "{escape_string(value)}"')
        elif isinstance(value, bool):
            props.append(f'{key}: {str(value).lower()}')
        elif isinstance(value, (int, float)):
            props.append(f'{key}: {value}')
        elif isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], str):
                escaped_list = [f'"{escape_string(v)}"' for v in value]
                props.append(f'{key}: [{", ".join(escaped_list)}]')
            else:
                props.append(f'{key}: {value}')
        elif isinstance(value, dict):
            # Store as JSON string
            import json
            props.append(f'{key}: "{escape_string(json.dumps(value))}"')
    return ', '.join(props)

def generate_cypher():
    """Generate Cypher statements from JSON data"""

    # Load data
    with open('/home/jim/2_OXOT_Projects_Dev/data/level5_generated_data.json', 'r') as f:
        data = json.load(f)

    cypher_statements = []

    # Header
    cypher_statements.append("// Level 5 Deployment - AEON Digital Twin")
    cypher_statements.append(f"// Generated: {datetime.now().isoformat()}")
    cypher_statements.append(f"// Total Nodes: {data['metadata']['total_nodes']}")
    cypher_statements.append("")

    # Create indexes
    cypher_statements.append("// Create Indexes")
    cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:InformationEvent) ON (n.eventId);")
    cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:GeopoliticalEvent) ON (n.eventId);")
    cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:ThreatFeed) ON (n.feedId);")
    cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:CognitiveBias) ON (n.biasId);")
    cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:EventProcessor) ON (n.processorId);")
    cypher_statements.append("")

    # InformationEvents - batch in groups of 100
    cypher_statements.append("// InformationEvents (5000 nodes)")
    events = data['data']['information_events']
    for i in range(0, len(events), 100):
        batch = events[i:i+100]
        cypher_statements.append(f"// Batch {i//100 + 1} of {len(events)//100 + 1}")

        for event in batch:
            props = dict_to_cypher_props(event)
            stmt = f'CREATE (ie:InformationEvent:Event:Information:RealTime:Level5 {{{props}, nodeType: "InformationEvent", level: 5, created: datetime()}});'
            cypher_statements.append(stmt)

        cypher_statements.append("")

    # GeopoliticalEvents
    cypher_statements.append("// GeopoliticalEvents (500 nodes)")
    for event in data['data']['geopolitical_events']:
        props = dict_to_cypher_props(event)
        stmt = f'CREATE (ge:GeopoliticalEvent:Event:Geopolitical:RealTime:Level5 {{{props}, nodeType: "GeopoliticalEvent", level: 5, created: datetime()}});'
        cypher_statements.append(stmt)
    cypher_statements.append("")

    # ThreatFeeds
    cypher_statements.append("// ThreatFeeds (3 nodes)")
    for feed in data['data']['threat_feeds']:
        props = dict_to_cypher_props(feed)
        stmt = f'CREATE (tf:ThreatFeed:DataSource:Integration:RealTime:Level5 {{{props}, nodeType: "ThreatFeed", level: 5, created: datetime()}});'
        cypher_statements.append(stmt)
    cypher_statements.append("")

    # CognitiveBiases
    cypher_statements.append("// CognitiveBiases (30 nodes)")
    for bias in data['data']['cognitive_biases']:
        # Check if exists first
        props = dict_to_cypher_props(bias)
        stmt = f'''
MERGE (cb:CognitiveBias {{biasName: "{bias['biasName']}"}})
ON CREATE SET cb:Psychology:Decision:Level4:Level5,
    cb += {{{props}}},
    cb.nodeType = "CognitiveBias",
    cb.level = 5,
    cb.created = datetime()
ON MATCH SET cb:Level5,
    cb += {{{props}}},
    cb.updated = datetime();'''
        cypher_statements.append(stmt)
    cypher_statements.append("")

    # EventProcessors
    cypher_statements.append("// EventProcessors (10 nodes)")
    for processor in data['data']['event_processors']:
        props = dict_to_cypher_props(processor)
        stmt = f'CREATE (ep:EventProcessor:Pipeline:Processing:Level5 {{{props}, nodeType: "EventProcessor", level: 5, created: datetime()}});'
        cypher_statements.append(stmt)
    cypher_statements.append("")

    # Basic Sectors (create if not exist)
    cypher_statements.append("// Create Basic Sectors if not exist")
    sectors = ['Energy', 'Water', 'Transportation', 'Healthcare',
               'Financial', 'Communications', 'Manufacturing', 'IT',
               'Chemical', 'Nuclear', 'Defense', 'Food',
               'Government', 'Emergency', 'Dams', 'Commercial']

    for sector in sectors:
        stmt = f'MERGE (s:Sector {{name: "{sector}"}}) SET s.sector = "{sector}", s.level = 2, s.created = datetime();'
        cypher_statements.append(stmt)
    cypher_statements.append("")

    # Relationships
    cypher_statements.append("// Create Relationships")

    # PUBLISHES relationships
    cypher_statements.append("// PUBLISHES: ThreatFeed -> InformationEvent")
    cypher_statements.append("""
MATCH (tf:ThreatFeed)
MATCH (ie:InformationEvent)
WITH tf, ie, rand() as r
WHERE r < 0.33
MERGE (tf)-[pub:PUBLISHES {
    created: datetime(),
    reliability: tf.reliability,
    latency: tf.latency
}]->(ie);
""")

    # ACTIVATES_BIAS relationships
    cypher_statements.append("// ACTIVATES_BIAS: InformationEvent -> CognitiveBias")
    cypher_statements.append("""
MATCH (ie:InformationEvent)
WHERE ie.fearRealityGap > 2.0
MATCH (cb:CognitiveBias)
WITH ie, cb, rand() as r
WHERE r < 0.2
MERGE (ie)-[ab:ACTIVATES_BIAS {
    created: datetime(),
    activationStrength: ie.fearRealityGap / 10.0,
    trigger: 'fear_reality_gap'
}]->(cb);
""")

    # AFFECTS_SECTOR relationships
    cypher_statements.append("// AFFECTS_SECTOR: InformationEvent -> Sector")
    cypher_statements.append("""
MATCH (ie:InformationEvent)
UNWIND ie.affectedSectors as sectorName
MATCH (s:Sector)
WHERE s.name = sectorName OR s.sector = sectorName
MERGE (ie)-[aff:AFFECTS_SECTOR {
    created: datetime(),
    severity: ie.severity,
    impact: ie.cvssScore / 10.0
}]->(s);
""")

    # PROCESSES_EVENT relationships
    cypher_statements.append("// PROCESSES_EVENT: EventProcessor -> Events")
    cypher_statements.append("""
MATCH (ep:EventProcessor)
MATCH (e:Event)
WHERE e:InformationEvent OR e:GeopoliticalEvent
WITH ep, e, rand() as r
WHERE r < 0.1
MERGE (ep)-[proc:PROCESSES_EVENT {
    created: datetime(),
    processingType: ep.processorType,
    latency: ep.latency
}]->(e);
""")

    # Validation queries
    cypher_statements.append("")
    cypher_statements.append("// Validation Queries")
    cypher_statements.append("MATCH (n:InformationEvent) RETURN 'InformationEvents' as type, count(n) as count;")
    cypher_statements.append("MATCH (n:GeopoliticalEvent) RETURN 'GeopoliticalEvents' as type, count(n) as count;")
    cypher_statements.append("MATCH (n:ThreatFeed) RETURN 'ThreatFeeds' as type, count(n) as count;")
    cypher_statements.append("MATCH (n:CognitiveBias) RETURN 'CognitiveBiases' as type, count(n) as count;")
    cypher_statements.append("MATCH (n:EventProcessor) RETURN 'EventProcessors' as type, count(n) as count;")
    cypher_statements.append("MATCH (n:Level5) RETURN 'Total Level5' as type, count(n) as count;")

    # Save to file
    output_file = '/home/jim/2_OXOT_Projects_Dev/scripts/level5_deployment.cypher'
    with open(output_file, 'w') as f:
        f.write('\n'.join(cypher_statements))

    print(f"Generated {len(cypher_statements)} Cypher statements")
    print(f"Saved to: {output_file}")

    # Also create a smaller test file with just a few nodes
    test_statements = []
    test_statements.append("// Level 5 Test Deployment - 10 nodes")
    test_statements.append("")

    # Just 10 InformationEvents
    for event in events[:10]:
        props = dict_to_cypher_props(event)
        stmt = f'CREATE (ie:InformationEvent:Event:Information:RealTime:Level5 {{{props}, nodeType: "InformationEvent", level: 5, created: datetime()}});'
        test_statements.append(stmt)

    # 1 ThreatFeed
    feed = data['data']['threat_feeds'][0]
    props = dict_to_cypher_props(feed)
    stmt = f'CREATE (tf:ThreatFeed:DataSource:Integration:RealTime:Level5 {{{props}, nodeType: "ThreatFeed", level: 5, created: datetime()}});'
    test_statements.append(stmt)

    test_statements.append("")
    test_statements.append("// Validate test deployment")
    test_statements.append("MATCH (n:Level5) RETURN count(n) as count;")

    test_file = '/home/jim/2_OXOT_Projects_Dev/scripts/level5_test.cypher'
    with open(test_file, 'w') as f:
        f.write('\n'.join(test_statements))

    print(f"Test file saved to: {test_file}")

if __name__ == "__main__":
    generate_cypher()