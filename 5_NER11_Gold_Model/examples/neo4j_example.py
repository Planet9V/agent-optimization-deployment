"""
NER11 Gold Standard - Neo4j Integration Example

This example demonstrates how to extract entities and populate a Neo4j graph.
"""

import sys
sys.path.append('../scripts')

from neo4j_integration import NER11Neo4jIntegrator

# Initialize integrator
print("Initializing NER11 Neo4j Integrator...")
integrator = NER11Neo4jIntegrator(
    model_path="../models/model-best",
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)
print("✓ Integrator initialized\n")

# Sample threat intelligence report
threat_report = """
THREAT INTELLIGENCE REPORT - APT29 Campaign Analysis

Executive Summary:
The APT29 threat actor group conducted a sophisticated cyber espionage 
campaign targeting critical infrastructure in the energy sector. The 
campaign exploited CVE-2023-12345, a zero-day vulnerability in Siemens 
S7-1200 PLCs.

Technical Analysis:
- Initial Access: Spear-phishing emails with malicious attachments
- Persistence: Scheduled tasks and registry modifications
- Lateral Movement: Pass-the-hash attacks and SMB exploitation
- Command & Control: Encrypted DNS tunneling to 185.220.101.42
- Data Exfiltration: Staged data collection and compression

Affected Systems:
- Siemens S7-1200 PLC (firmware v4.2.3)
- Schneider Electric Modicon M340
- Allen-Bradley ControlLogix 5000
- Rockwell Automation RSLogix 5000

Indicators of Compromise:
- MD5: 5d41402abc4b2a76b9719d911017c592
- SHA256: 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae
- Domain: malicious-c2.example.com
- IP: 185.220.101.42

Recommendations:
1. Patch CVE-2023-12345 immediately
2. Implement network segmentation
3. Enable multi-factor authentication
4. Conduct threat hunting activities
"""

# Process and ingest
print("Processing threat report...")
result = integrator.process_and_ingest(
    text=threat_report,
    source_doc="APT29_Campaign_Report_2025.txt",
    create_relationships=True
)

print(f"\n✓ Processing complete!")
print(f"  Entities extracted: {result['entity_count']}")
print(f"  Nodes created: {result['nodes_created']}")
print(f"  Relationships created: {result['relationships_created']}")

# Display extracted entities
print(f"\nExtracted Entities:")
print("=" * 70)
for text, entity_type in result['entities'][:20]:  # Show first 20
    print(f"  {text:<40} → {entity_type}")

if len(result['entities']) > 20:
    print(f"  ... and {len(result['entities']) - 20} more")

# Example Neo4j queries
print("\n" + "=" * 70)
print("Example Neo4j Queries:")
print("=" * 70)

queries = [
    ("Find all vulnerabilities", """
        MATCH (v:Vulnerability)
        RETURN v.text, v.count
        ORDER BY v.count DESC
        LIMIT 10
    """),
    
    ("Find threat actors and their targets", """
        MATCH (ta:ThreatActor)-[:EXPLOITS|TARGETS*1..2]->(target)
        RETURN ta.text, collect(DISTINCT target.text) as targets
    """),
    
    ("Find co-occurring entities", """
        MATCH (e1:Entity)-[r:CO_OCCURS]->(e2:Entity)
        WHERE r.count > 1
        RETURN e1.text, e2.text, r.count
        ORDER BY r.count DESC
        LIMIT 10
    """),
]

for title, query in queries:
    print(f"\n{title}:")
    print(f"```cypher")
    print(query.strip())
    print(f"```")

# Close connection
integrator.close()

print("\n" + "=" * 70)
print("✓ Neo4j integration example complete!")
print("\nNext steps:")
print("  - Open Neo4j Browser: http://localhost:7474")
print("  - Run the example queries above")
print("  - Explore the knowledge graph visually")
