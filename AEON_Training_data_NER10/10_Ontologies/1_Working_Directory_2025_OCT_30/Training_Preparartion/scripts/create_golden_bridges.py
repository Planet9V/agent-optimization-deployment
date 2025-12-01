#!/usr/bin/env python3
"""
Create Golden Bridge Patterns - Add CWE relationships to CAPEC nodes with ATT&CK links

ROOT CAUSE:
- Dataset A: 606 CAPEC nodes with capecId property, have EXPLOITS_WEAKNESS → CWE
- Dataset B: 177 CAPEC nodes with id property, have IMPLEMENTS_TECHNIQUE → ATT&CK
- No overlap because different properties/labels

SOLUTION:
- Match Dataset A (capecId) to Dataset B (id)
- Add EXPLOITS_WEAKNESS relationships to Dataset B nodes
- Creates golden bridges: Dataset B nodes have BOTH CWE and ATT&CK links

Date: 2025-11-08
"""

import os
import subprocess
import json
from datetime import datetime

NEO4J_CONTAINER = "openspg-neo4j"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

def execute_cypher(query, description=""):
    """Execute Cypher query and return results"""
    print(f"\n{'='*80}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {description}")
    print(f"{'='*80}")
    print(f"Query: {query[:200]}..." if len(query) > 200 else f"Query: {query}")

    cmd = [
        "docker", "exec", NEO4J_CONTAINER,
        "cypher-shell", "-u", NEO4J_USER, "-p", NEO4J_PASSWORD,
        query
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"\n✅ SUCCESS:")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR:")
        print(e.stderr)
        return None

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     GOLDEN BRIDGE CREATION SCRIPT                            ║
║                                                                              ║
║  Purpose: Add CWE relationships to CAPEC nodes that have ATT&CK links       ║
║  Method: Match Dataset A (capecId) to Dataset B (id)                        ║
║  Result: Create golden bridges enabling complete attack chains              ║
╚══════════════════════════════════════════════════════════════════════════════╝

START TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")

    # Step 1: Count baseline
    print("\n" + "="*80)
    print("STEP 1: BASELINE METRICS")
    print("="*80)

    queries = {
        "capec_with_cwe": "MATCH (c)-[:EXPLOITS_WEAKNESS]->() RETURN count(DISTINCT c) AS count;",
        "capec_with_attack": "MATCH (c)-[:IMPLEMENTS_TECHNIQUE]->() RETURN count(DISTINCT c) AS count;",
        "golden_bridges_before": "MATCH (c)-[:EXPLOITS_WEAKNESS]->() MATCH (c)-[:IMPLEMENTS_TECHNIQUE]->() RETURN count(DISTINCT c) AS count;",
        "complete_chains_before": "MATCH (cve:CVE)-[:HAS_WEAKNESS|IS_WEAKNESS_TYPE]->(cwe)<-[:EXPLOITS_WEAKNESS]-(capec)-[:IMPLEMENTS_TECHNIQUE]->(attack) RETURN count(*) AS count;"
    }

    baseline = {}
    for name, query in queries.items():
        result = execute_cypher(query, f"Count {name}")
        if result:
            baseline[name] = result.strip()

    # Step 2: Test query to validate matching logic
    print("\n" + "="*80)
    print("STEP 2: VALIDATE MATCHING LOGIC")
    print("="*80)

    test_query = """
    MATCH (dataset_a)-[:EXPLOITS_WEAKNESS]->(cwe)
    WHERE dataset_a.capecId IS NOT NULL
    WITH DISTINCT dataset_a.capecId AS capec_id, COLLECT(DISTINCT cwe) AS cwes
    LIMIT 5
    MATCH (dataset_b)-[:IMPLEMENTS_TECHNIQUE]->()
    WHERE dataset_b.id = capec_id
    RETURN capec_id, size(cwes) AS cwe_count, labels(dataset_b) AS dataset_b_labels
    LIMIT 5;
    """

    execute_cypher(test_query, "Test: Can we match Dataset A capecId to Dataset B id?")

    # Step 3: Count how many matches we can create
    print("\n" + "="*80)
    print("STEP 3: COUNT POTENTIAL GOLDEN BRIDGES")
    print("="*80)

    count_query = """
    MATCH (dataset_a)-[:EXPLOITS_WEAKNESS]->(cwe)
    WHERE dataset_a.capecId IS NOT NULL
    WITH DISTINCT dataset_a.capecId AS capec_id
    MATCH (dataset_b)-[:IMPLEMENTS_TECHNIQUE]->()
    WHERE dataset_b.id = capec_id
    RETURN count(DISTINCT dataset_b) AS matchable_nodes;
    """

    execute_cypher(count_query, "Count: How many golden bridges can we create?")

    # Step 4: Create the golden bridge relationships
    print("\n" + "="*80)
    print("STEP 4: CREATE GOLDEN BRIDGE RELATIONSHIPS")
    print("="*80)

    bridge_query = """
    MATCH (dataset_a)-[r1:EXPLOITS_WEAKNESS]->(cwe)
    WHERE dataset_a.capecId IS NOT NULL
    WITH dataset_a.capecId AS capec_id, COLLECT(DISTINCT cwe) AS cwes
    MATCH (dataset_b:AttackPattern)-[:IMPLEMENTS_TECHNIQUE]->()
    WHERE dataset_b.id = capec_id
    UNWIND cwes AS cwe
    MERGE (dataset_b)-[r:EXPLOITS_WEAKNESS]->(cwe)
    ON CREATE SET r.source = 'golden_bridge_creation_2025-11-08',
                  r.created_at = datetime()
    RETURN count(r) AS relationships_created;
    """

    print("⚠️  CREATING RELATIONSHIPS - This will modify the database...")
    print("Press Ctrl+C within 5 seconds to abort...")
    import time
    time.sleep(5)

    result = execute_cypher(bridge_query, "CREATE: Golden bridge EXPLOITS_WEAKNESS relationships")

    if not result:
        print("\n❌ FAILED TO CREATE RELATIONSHIPS - ABORTING")
        return

    # Step 5: Validate golden bridges created
    print("\n" + "="*80)
    print("STEP 5: VALIDATE GOLDEN BRIDGES")
    print("="*80)

    validation_queries = {
        "golden_bridges_after": "MATCH (c)-[:EXPLOITS_WEAKNESS]->() MATCH (c)-[:IMPLEMENTS_TECHNIQUE]->() RETURN count(DISTINCT c) AS count;",
        "complete_chains_after": "MATCH (cve:CVE)-[:HAS_WEAKNESS|IS_WEAKNESS_TYPE]->(cwe)<-[:EXPLOITS_WEAKNESS]-(capec)-[:IMPLEMENTS_TECHNIQUE]->(attack) RETURN count(*) AS count;",
        "sample_complete_chain": "MATCH (cve:CVE)-[:HAS_WEAKNESS|IS_WEAKNESS_TYPE]->(cwe)<-[:EXPLOITS_WEAKNESS]-(capec)-[:IMPLEMENTS_TECHNIQUE]->(attack) RETURN cve.id, cwe.cwe_id, capec.id, attack.id LIMIT 1;"
    }

    after = {}
    for name, query in validation_queries.items():
        result = execute_cypher(query, f"Validate {name}")
        if result:
            after[name] = result.strip()

    # Step 6: Final summary
    print("\n" + "="*80)
    print("STEP 6: FINAL SUMMARY")
    print("="*80)

    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           GOLDEN BRIDGE FIX RESULTS                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

BASELINE (Before Fix):
- CAPEC with CWE links: {baseline.get('capec_with_cwe', 'N/A')}
- CAPEC with ATT&CK links: {baseline.get('capec_with_attack', 'N/A')}
- Golden bridges: {baseline.get('golden_bridges_before', 'N/A')}
- Complete chains: {baseline.get('complete_chains_before', 'N/A')}

AFTER FIX:
- Golden bridges: {after.get('golden_bridges_after', 'N/A')}
- Complete chains: {after.get('complete_chains_after', 'N/A')}

SAMPLE COMPLETE CHAIN:
{after.get('sample_complete_chain', 'N/A')}

END TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")

    # Step 7: Integrity validation
    print("\n" + "="*80)
    print("STEP 7: INTEGRITY VALIDATION")
    print("="*80)

    integrity_queries = {
        "cve_cwe_still_intact": "MATCH ()-[r:HAS_WEAKNESS|IS_WEAKNESS_TYPE]->() RETURN count(r) AS count;",
        "capec_cwe_still_intact": "MATCH ()-[r:EXPLOITS_WEAKNESS]->() RETURN count(r) AS count;",
        "capec_attack_still_intact": "MATCH ()-[r:IMPLEMENTS_TECHNIQUE]->() RETURN count(r) AS count;"
    }

    for name, query in integrity_queries.items():
        execute_cypher(query, f"Integrity check: {name}")

    print("\n✅ GOLDEN BRIDGE CREATION COMPLETE")

if __name__ == "__main__":
    main()
