#!/usr/bin/env python3
"""
Fast deployment using batch CREATE statements
"""

import json
import subprocess

def execute_cypher_file(statements):
    """Execute Cypher statements via stdin"""
    cmd = ['docker', 'exec', '-i', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg']
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate(input='\n'.join(statements))
    return proc.returncode == 0, stdout, stderr

print("Loading data...")
with open('/home/jim/2_OXOT_Projects_Dev/temp/sector-COMMUNICATIONS-generated-data.json', 'r') as f:
    data = json.load(f)

nodes = data['nodes']
relationships = data['relationships']

print(f"Creating {len(nodes)} nodes...")

# Create all nodes as individual CREATE statements
all_statements = []

# Indexes first
all_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:COMMUNICATIONS) ON (n.id);")
all_statements.append("CREATE CONSTRAINT IF NOT EXISTS FOR (n:COMMUNICATIONS) REQUIRE n.id IS UNIQUE;")

# Nodes
for idx, node in enumerate(nodes):
    labels = ':'.join(node['labels'])
    props = node['properties']

    prop_parts = [f"id: '{node['id']}'"]
    for key, value in props.items():
        if isinstance(value, str):
            val_safe = value.replace("'", "\\'").replace('"', '\\"')
            prop_parts.append(f'{key}: "{val_safe}"')
        elif isinstance(value, (int, float)):
            prop_parts.append(f'{key}: {value}')

    props_str = ', '.join(prop_parts)
    all_statements.append(f"CREATE (:{labels} {{{props_str}}});")

    if (idx + 1) % 1000 == 0:
        print(f"  Prepared {idx + 1}/{len(nodes)} node statements")

print(f"Creating {len(relationships)} relationships...")

# Relationships
for idx, rel in enumerate(relationships):
    all_statements.append(
        f"MATCH (from {{id: '{rel['from']}'}}), (to {{id: '{rel['to']}'}}) "
        f"MERGE (from)-[:{rel['type']}]->(to);"
    )

    if (idx + 1) % 1000 == 0:
        print(f"  Prepared {idx + 1}/{len(relationships)} relationship statements")

print(f"\nTotal statements: {len(all_statements)}")
print("Executing all statements...")

success, stdout, stderr = execute_cypher_file(all_statements)

if success:
    print("✅ Deployment successful!")
else:
    print(f"⚠️  Deployment completed with warnings")
    if stderr:
        print(f"Stderr (first 500 chars): {stderr[:500]}")

# Verify
print("\nVerifying...")
verify_cmd = ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg',
              "MATCH (n) WHERE 'COMMUNICATIONS' IN labels(n) RETURN count(n) as total;"]
result = subprocess.run(verify_cmd, capture_output=True, text=True)
print(f"Verification: {result.stdout}")

