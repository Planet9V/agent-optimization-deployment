#!/bin/bash
# Final COMMUNICATIONS deployment using temp files

echo "Creating missing nodes and relationships..."

# Create temporary Cypher files in container
python3 << 'PYTHON_EOF'
import json

with open('/home/jim/2_OXOT_Projects_Dev/temp/sector-COMMUNICATIONS-generated-data.json') as f:
    data = json.load(f)

# Generate relationship creation script
rels = []
for rel in data['relationships']:
    rels.append(f"MATCH (from {{id: '{rel['from']}'}}), (to {{id: '{rel['to']}'}}) CREATE (from)-[:{rel['type']}]->(to);")

# Write in chunks
chunk_size = 5000
for i in range(0, len(rels), chunk_size):
    chunk = rels[i:i+chunk_size]
    with open(f'/tmp/rels_chunk_{i//chunk_size}.cypher', 'w') as f:
        f.write('\n'.join(chunk))

print(f"Created {(len(rels) + chunk_size - 1) // chunk_size} relationship files")

# Generate missing nodes script
nodes_created = 0
missing_nodes = []
for node in data['nodes']:
    labels = ':'.join(node['labels'])
    props = [f"id: '{node['id']}'"]

    for key, value in node['properties'].items():
        if isinstance(value, str):
            val_safe = value.replace("'", "\\'").replace('"', '\\"')
            props.append(f'{key}: "{val_safe}"')
        elif isinstance(value, (int, float)):
            props.append(f'{key}: {value}')

    props_str = ', '.join(props)
    missing_nodes.append(f"MERGE (:{labels} {{{props_str}}});")

# Write nodes in chunks
for i in range(0, len(missing_nodes), chunk_size):
    chunk = missing_nodes[i:i+chunk_size]
    with open(f'/tmp/nodes_chunk_{i//chunk_size}.cypher', 'w') as f:
        f.write('\n'.join(chunk))

print(f"Created {(len(missing_nodes) + chunk_size - 1) // chunk_size} node files")
PYTHON_EOF

# Copy files to container and execute
echo "Deploying missing nodes..."
for file in /tmp/nodes_chunk_*.cypher; do
    if [ -f "$file" ]; then
        docker cp "$file" openspg-neo4j:/tmp/
        filename=$(basename "$file")
        docker exec openspg-neo4j bash -c "cat /tmp/$filename | cypher-shell -u neo4j -p 'neo4j@openspg'" > /dev/null 2>&1
        echo "  Processed $filename"
    fi
done

echo "Creating relationships..."
for file in /tmp/rels_chunk_*.cypher; do
    if [ -f "$file" ]; then
        docker cp "$file" openspg-neo4j:/tmp/
        filename=$(basename "$file")
        docker exec openspg-neo4j bash -c "cat /tmp/$filename | cypher-shell -u neo4j -p 'neo4j@openspg'" > /dev/null 2>&1
        echo "  Processed $filename"
    fi
done

# Verify
echo ""
echo "Verification:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n) WHERE 'COMMUNICATIONS' IN labels(n) RETURN count(n) as total_nodes;"

docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (n)-[r]->(m) WHERE 'COMMUNICATIONS' IN labels(n) RETURN count(r) as total_relationships;"

# Cleanup
rm -f /tmp/nodes_chunk_*.cypher /tmp/rels_chunk_*.cypher
docker exec openspg-neo4j bash -c "rm -f /tmp/nodes_chunk_*.cypher /tmp/rels_chunk_*.cypher"

echo ""
echo "✅ Deployment complete!"
