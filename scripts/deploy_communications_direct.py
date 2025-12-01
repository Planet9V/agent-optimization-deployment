#!/usr/bin/env python3
"""
Direct deployment to Neo4j using Python
"""

import json
import subprocess
import time

def execute_cypher(query):
    """Execute a Cypher query via docker exec"""
    cmd = [
        'docker', 'exec', 'openspg-neo4j',
        'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg',
        query
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def main():
    print("Loading data...")
    with open('/home/jim/2_OXOT_Projects_Dev/temp/sector-COMMUNICATIONS-generated-data.json', 'r') as f:
        data = json.load(f)

    nodes = data['nodes']
    relationships = data['relationships']

    print(f"Deploying {len(nodes)} nodes and {len(relationships)} relationships...")

    # Create indexes
    print("Creating indexes...")
    execute_cypher("CREATE INDEX IF NOT EXISTS FOR (n:COMMUNICATIONS) ON (n.id);")
    execute_cypher("CREATE INDEX IF NOT EXISTS FOR (n:CommunicationsDevice) ON (n.device_name);")
    execute_cypher("CREATE CONSTRAINT IF NOT EXISTS FOR (n:COMMUNICATIONS) REQUIRE n.id IS UNIQUE;")

    # Deploy nodes in batches
    batch_size = 100
    total_batches = (len(nodes) + batch_size - 1) // batch_size

    for i in range(0, len(nodes), batch_size):
        batch = nodes[i:i+batch_size]
        batch_num = i // batch_size + 1

        # Build UNWIND query
        node_data = []
        for node in batch:
            props = node['properties'].copy()
            labels = node['labels']

            # Escape strings
            for key, value in props.items():
                if isinstance(value, str):
                    props[key] = value.replace("'", "\\'").replace('"', '\\"')

            node_data.append({
                'id': node['id'],
                'labels': labels,
                'props': props
            })

        # Create query
        query = "UNWIND $nodes AS nodeData "
        query += "CREATE (n) "
        query += "SET n = nodeData.props "
        query += "WITH n, nodeData.labels AS labels "
        query += "CALL { WITH n, labels "
        query += "  UNWIND labels AS label "
        query += "  CALL apoc.create.addLabels(n, [label]) YIELD node "
        query += "  RETURN node "
        query += "} "
        query += "RETURN count(n);"

        # Since we can't pass parameters easily, build the query directly
        query_parts = []
        for node in batch:
            labels = ':'.join(node['labels'])
            props_list = []
            for key, value in node['properties'].items():
                if isinstance(value, str):
                    value_safe = value.replace("'", "\\'").replace('"', '\\"')
                    props_list.append(f'{key}: "{value_safe}"')
                elif isinstance(value, (int, float)):
                    props_list.append(f'{key}: {value}')

            props_str = ', '.join(props_list)
            query_parts.append(f"CREATE (:{labels} {{id: '{node['id']}', {props_str}}});")

        # Execute batch
        combined_query = ' '.join(query_parts)
        success, stdout, stderr = execute_cypher(combined_query)

        if success or batch_num % 10 == 0:
            print(f"  Batch {batch_num}/{total_batches} - {len(batch)} nodes")

        if stderr and "error" in stderr.lower():
            print(f"  WARNING: {stderr[:200]}")

        # Small delay to prevent overwhelming the database
        time.sleep(0.1)

    print("\nCreating relationships...")
    rel_batch_size = 50
    total_rel_batches = (len(relationships) + rel_batch_size - 1) // rel_batch_size

    for i in range(0, len(relationships), rel_batch_size):
        batch = relationships[i:i+rel_batch_size]
        batch_num = i // rel_batch_size + 1

        # Build relationship queries
        query_parts = []
        for rel in batch:
            query_parts.append(
                f"MATCH (from {{id: '{rel['from']}'}}), (to {{id: '{rel['to']}'}}) "
                f"CREATE (from)-[:{rel['type']}]->(to);"
            )

        combined_query = ' '.join(query_parts)
        success, stdout, stderr = execute_cypher(combined_query)

        if success or batch_num % 20 == 0:
            print(f"  Batch {batch_num}/{total_rel_batches} - {len(batch)} relationships")

        time.sleep(0.05)

    # Verification
    print("\nVerifying deployment...")
    success, stdout, stderr = execute_cypher(
        "MATCH (n) WHERE 'COMMUNICATIONS' IN labels(n) RETURN count(n) as total;"
    )
    print(f"Total nodes: {stdout}")

    print("\n✅ Deployment complete!")

if __name__ == "__main__":
    main()
