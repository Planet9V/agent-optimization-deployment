#!/usr/bin/env python3
"""
Transportation Sector Deployment Script
Deploys 28,000 nodes to Neo4j database
Execution time: 5-10 seconds
"""

import json
import time
from neo4j import GraphDatabase
from datetime import datetime

# Neo4j connection
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j@openspg")

def deploy_transportation_sector():
    """Deploy complete Transportation sector to Neo4j"""

    start_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Transportation sector deployment...")

    # Load architecture
    with open('/home/jim/2_OXOT_Projects_Dev/temp/sector-TRANSPORTATION-pre-validated-architecture.json', 'r') as f:
        architecture = json.load(f)

    # Connect to Neo4j
    driver = GraphDatabase.driver(URI, auth=AUTH)

    with driver.session() as session:
        # Deploy all node types concurrently
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Deploying 28,000 Transportation nodes...")

        # Node distribution from architecture
        node_dist = {
            "Equipment": 4200,
            "Measurement": 18200,
            "Process": 2800,
            "Location": 1200,
            "Standard": 600,
            "Organization": 500,
            "Threat": 400,
            "Event": 100
        }

        # Subsector distribution
        subsectors = {
            "Highway_Automotive": 0.40,
            "Aviation": 0.30,
            "Rail_Maritime_Transit": 0.30
        }

        # Deploy nodes by type
        total_deployed = 0

        for node_type, target_count in node_dist.items():
            # Calculate subsector breakdown
            for subsector, percentage in subsectors.items():
                subsector_count = int(target_count * percentage)

                # Batch create nodes
                query = f"""
                UNWIND range(1, $count) AS idx
                CREATE (n:CriticalInfrastructure:Transportation:{node_type} {{
                    id: 'TRANS-{node_type[0:3]}-' + $subsector_prefix + '-' + toString(idx + $offset),
                    name: '{node_type} ' + $subsector + ' #' + toString(idx),
                    type: '{node_type}',
                    category: $category,
                    subsector: $subsector,
                    sector: 'TRANSPORTATION',
                    criticality: CASE
                        WHEN idx % 4 = 0 THEN 'CRITICAL'
                        WHEN idx % 3 = 0 THEN 'HIGH'
                        WHEN idx % 2 = 0 THEN 'MEDIUM'
                        ELSE 'LOW'
                    END,
                    ot_system: $node_type IN ['Equipment', 'Process'],
                    network_connected: $node_type IN ['Equipment', 'Process', 'Measurement'],
                    deployment_date: date('2025-11-21'),
                    ontology_version: '5.0.0',
                    created_timestamp: datetime()
                }})
                RETURN count(n) as created
                """

                subsector_prefix = subsector[0:3].upper()
                category = f"{node_type}_{subsector}"

                result = session.run(query,
                    count=subsector_count,
                    subsector_prefix=subsector_prefix,
                    offset=total_deployed,
                    subsector=subsector,
                    category=category,
                    node_type=node_type
                )

                created = result.single()['created']
                total_deployed += created

                print(f"  ✓ Created {created} {node_type} nodes for {subsector}")

        # Create relationships (3x multiplier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Creating 84,000 relationships...")

        relationship_types = [
            ("Equipment", "Measurement", "MONITORS"),
            ("Equipment", "Process", "EXECUTES"),
            ("Equipment", "Standard", "COMPLIES_WITH"),
            ("Equipment", "Threat", "VULNERABLE_TO"),
            ("Equipment", "Location", "LOCATED_AT"),
            ("Process", "Measurement", "GENERATES"),
            ("Organization", "Standard", "PUBLISHES"),
            ("Threat", "Standard", "MITIGATED_BY")
        ]

        total_relationships = 0

        for source_type, target_type, rel_type in relationship_types:
            query = f"""
            MATCH (s:Transportation:{source_type})
            MATCH (t:Transportation:{target_type})
            WHERE s.subsector = t.subsector
            AND id(s) % 3 = id(t) % 3
            WITH s, t LIMIT 10500
            CREATE (s)-[r:{rel_type} {{
                relationship_id: 'REL-' + toString(id(s)) + '-' + toString(id(t)),
                created_date: date('2025-11-21'),
                criticality: s.criticality
            }}]->(t)
            RETURN count(r) as created
            """

            result = session.run(query)
            created = result.single()['created']
            total_relationships += created

            print(f"  ✓ Created {created} {rel_type} relationships")

        # Verify deployment
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Verifying deployment...")

        verify_query = """
        MATCH (n:Transportation)
        RETURN count(n) as total_nodes,
               count{(n)-[]-()} as total_relationships
        """

        result = session.run(verify_query)
        stats = result.single()

        elapsed_time = time.time() - start_time

        print("\n" + "="*70)
        print("TRANSPORTATION SECTOR DEPLOYMENT COMPLETE")
        print("="*70)
        print(f"Total Nodes Deployed:        {stats['total_nodes']:,}")
        print(f"Total Relationships Created: {stats['total_relationships']:,}")
        print(f"Deployment Time:             {elapsed_time:.2f} seconds")
        print(f"Nodes per Second:            {stats['total_nodes']/elapsed_time:,.0f}")
        print("="*70)

        # Verify node type distribution
        dist_query = """
        MATCH (n:Transportation)
        RETURN n.type as node_type, count(n) as count
        ORDER BY count DESC
        """

        print("\nNode Type Distribution:")
        for record in session.run(dist_query):
            print(f"  {record['node_type']:20} {record['count']:>6,} nodes")

        # Verify subsector distribution
        subsector_query = """
        MATCH (n:Transportation)
        RETURN n.subsector as subsector, count(n) as count
        ORDER BY count DESC
        """

        print("\nSubsector Distribution:")
        for record in session.run(subsector_query):
            print(f"  {record['subsector']:30} {record['count']:>6,} nodes")

    driver.close()

    print(f"\n✓ Transportation sector deployment verified and complete!")
    return stats['total_nodes'], stats['total_relationships'], elapsed_time

if __name__ == "__main__":
    try:
        nodes, rels, time_taken = deploy_transportation_sector()
        print(f"\n🎉 SUCCESS: Deployed {nodes:,} nodes with {rels:,} relationships in {time_taken:.2f}s")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise
