#!/usr/bin/env python3
"""
CRITICAL_MANUFACTURING Sector Deployment Script
Executes Cypher script to deploy 28,000 equipment nodes (upgrade from 400)
Total deployment: ~54,700 nodes
"""

import os
import sys
import time
from neo4j import GraphDatabase

# Neo4j connection details from environment or defaults
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Allow override from command line
if len(sys.argv) > 1:
    NEO4J_PASSWORD = sys.argv[1]
if len(sys.argv) > 2:
    NEO4J_URI = sys.argv[2]
if len(sys.argv) > 3:
    NEO4J_USER = sys.argv[3]

def execute_cypher_file(driver, filepath):
    """Execute Cypher script from file with proper transaction handling"""

    print(f"Reading Cypher script: {filepath}")
    with open(filepath, 'r') as f:
        cypher_content = f.read()

    # Split into phases based on comments
    phases = []
    current_phase = []
    current_phase_name = "Initialization"

    for line in cypher_content.split('\n'):
        if line.strip().startswith('// PHASE'):
            if current_phase:
                phases.append((current_phase_name, '\n'.join(current_phase)))
            current_phase_name = line.strip().replace('//', '').strip()
            current_phase = []
        else:
            current_phase.append(line)

    if current_phase:
        phases.append((current_phase_name, '\n'.join(current_phase)))

    print(f"\nFound {len(phases)} deployment phases")

    # Execute each phase
    total_start = time.time()

    with driver.session() as session:
        for i, (phase_name, phase_cypher) in enumerate(phases, 1):
            # Skip empty phases
            if not phase_cypher.strip() or phase_cypher.strip().startswith('//'):
                continue

            print(f"\n{'='*60}")
            print(f"Executing Phase {i}/{len(phases)}: {phase_name}")
            print(f"{'='*60}")

            phase_start = time.time()

            try:
                # Split by semicolons for individual statements
                statements = [s.strip() for s in phase_cypher.split(';') if s.strip() and not s.strip().startswith('//')]

                for j, statement in enumerate(statements, 1):
                    if not statement:
                        continue

                    stmt_start = time.time()
                    result = session.run(statement)
                    summary = result.consume()
                    stmt_duration = time.time() - stmt_start

                    nodes_created = summary.counters.nodes_created
                    rels_created = summary.counters.relationships_created

                    if nodes_created > 0 or rels_created > 0:
                        print(f"  Statement {j}/{len(statements)}: "
                              f"{nodes_created} nodes, {rels_created} rels "
                              f"({stmt_duration:.2f}s)")

                phase_duration = time.time() - phase_start
                print(f"Phase {i} completed in {phase_duration:.2f}s")

            except Exception as e:
                print(f"ERROR in Phase {i}: {e}")
                print(f"Failed statement preview: {phase_cypher[:200]}...")
                raise

    total_duration = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"DEPLOYMENT COMPLETE")
    print(f"Total time: {total_duration:.2f}s ({total_duration/60:.2f} minutes)")
    print(f"{'='*60}")

def verify_deployment(driver):
    """Verify the deployment by counting nodes"""

    print("\n" + "="*60)
    print("DEPLOYMENT VERIFICATION")
    print("="*60)

    with driver.session() as session:
        # Count by node type
        queries = {
            "ManufacturingEquipment": "MATCH (n:ManufacturingEquipment) RETURN count(n) as count",
            "ManufacturingMeasurement": "MATCH (n:ManufacturingMeasurement) RETURN count(n) as count",
            "ManufacturingProperty": "MATCH (n:ManufacturingProperty) RETURN count(n) as count",
            "ManufacturingProcess": "MATCH (n:ManufacturingProcess) RETURN count(n) as count",
            "ManufacturingControl": "MATCH (n:ManufacturingControl) RETURN count(n) as count",
            "ManufacturingAlert": "MATCH (n:ManufacturingAlert) RETURN count(n) as count",
            "ManufacturingZone": "MATCH (n:ManufacturingZone) RETURN count(n) as count",
            "MajorManufacturingAsset": "MATCH (n:MajorManufacturingAsset) RETURN count(n) as count",
            "CRITICAL_MANUFACTURING (all)": "MATCH (n:CRITICAL_MANUFACTURING) RETURN count(n) as count",
        }

        total_nodes = 0
        for label, query in queries.items():
            result = session.run(query)
            count = result.single()['count']
            print(f"  {label:30s}: {count:>8,} nodes")
            total_nodes += count

        print(f"\n  {'Total CRITICAL_MANUFACTURING':30s}: {total_nodes:>8,} nodes")

        # Count relationships
        rel_query = """
        MATCH (n:CRITICAL_MANUFACTURING)-[r]->()
        RETURN type(r) as rel_type, count(r) as count
        ORDER BY count DESC
        """
        result = session.run(rel_query)
        print("\n  Relationships:")
        total_rels = 0
        for record in result:
            print(f"    {record['rel_type']:25s}: {record['count']:>8,}")
            total_rels += record['count']
        print(f"  {'Total Relationships':27s}: {total_rels:>8,}")

def main():
    """Main deployment execution"""

    print("="*60)
    print("CRITICAL_MANUFACTURING SECTOR DEPLOYMENT")
    print("Upgrade: 400 → 28,000 equipment nodes")
    print("Total: ~54,700 nodes")
    print("="*60)

    # Connect to Neo4j
    print(f"\nConnecting to Neo4j at {NEO4J_URI}...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        # Test connection
        with driver.session() as session:
            result = session.run("RETURN 1")
            result.consume()
        print("✅ Connected successfully")

        # Execute deployment
        execute_cypher_file(driver, "deploy-critical-manufacturing.cypher")

        # Verify deployment
        verify_deployment(driver)

        print("\n✅ CRITICAL_MANUFACTURING SECTOR DEPLOYMENT COMPLETE")

    except Exception as e:
        print(f"\n❌ DEPLOYMENT FAILED: {e}")
        raise
    finally:
        driver.close()

if __name__ == "__main__":
    main()
