#!/usr/bin/env python3
"""
Neo4j schema diagram export utility
- Mermaid diagram generation
- GraphML export for yEd
- PNG rendering
- SVG export
- Interactive HTML with vis.js
"""

import os
import sys
import json
import logging
from typing import Dict, List, Tuple
from pathlib import Path

try:
    from neo4j import GraphDatabase
    from neo4j.exceptions import Neo4jError
except ImportError:
    print("Error: neo4j-driver package required. Install with: pip install neo4j")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Color codes
class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'


class SchemaExporter:
    """Exports Neo4j schema in multiple formats"""

    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self.driver = None
        self.schema = {
            'nodes': [],
            'relationships': [],
            'indexes': []
        }

    def connect(self) -> bool:
        """Connect to Neo4j"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.driver.verify_connectivity()
            logger.info(f"{Colors.OKGREEN}✓ Connected to Neo4j{Colors.ENDC}")
            return True
        except Neo4jError as e:
            logger.error(f"{Colors.FAIL}✗ Connection failed: {e}{Colors.ENDC}")
            return False

    def disconnect(self):
        """Disconnect from Neo4j"""
        if self.driver:
            self.driver.close()

    def extract_schema(self) -> bool:
        """Extract schema information from Neo4j"""
        logger.info("Extracting schema information...")

        try:
            with self.driver.session(database=self.database) as session:
                # Get node labels and properties
                result = session.run(
                    """
                    CALL db.labels()
                    YIELD label
                    RETURN label
                    """
                )

                for record in result:
                    label = record['label']

                    # Get properties for each label
                    prop_result = session.run(
                        """
                        MATCH (n:$label)
                        UNWIND keys(n) as key
                        RETURN DISTINCT key as property
                        LIMIT 1000
                        """,
                        parameters={"label": label}
                    )

                    properties = [p['property'] for p in prop_result]

                    self.schema['nodes'].append({
                        'label': label,
                        'properties': properties
                    })

                # Get relationship types
                rel_result = session.run(
                    """
                    CALL db.relationshipTypes()
                    YIELD relationshipType
                    RETURN relationshipType
                    """
                )

                for record in rel_result:
                    rel_type = record['relationshipType']

                    # Get relationship examples
                    example_result = session.run(
                        """
                        MATCH ()-[r:$rel]-()
                        RETURN
                            type(r) as type,
                            labels(startNode(r))[0] as from_label,
                            labels(endNode(r))[0] as to_label
                        LIMIT 1
                        """,
                        parameters={"rel": rel_type}
                    )

                    for example in example_result:
                        self.schema['relationships'].append({
                            'type': example['type'],
                            'from': example['from_label'],
                            'to': example['to_label']
                        })

                # Get indexes
                index_result = session.run("SHOW INDEXES")
                for record in index_result:
                    self.schema['indexes'].append({
                        'name': record.get('name', 'unknown'),
                        'type': record.get('type', 'unknown'),
                        'state': record.get('state', 'unknown')
                    })

                logger.info(f"{Colors.OKGREEN}✓ Schema extracted: "
                          f"{len(self.schema['nodes'])} node types, "
                          f"{len(self.schema['relationships'])} relationship types{Colors.ENDC}")
                return True

        except Exception as e:
            logger.error(f"{Colors.FAIL}✗ Schema extraction failed: {e}{Colors.ENDC}")
            return False

    def generate_mermaid(self, output_file: str) -> bool:
        """Generate Mermaid diagram"""
        logger.info("Generating Mermaid diagram...")

        try:
            mermaid_lines = ["graph TD"]

            # Add node definitions
            for node in self.schema['nodes']:
                label = node['label']
                mermaid_lines.append(f"    {label}[\"{label}\"]")

            # Add relationships
            seen_rels = set()
            for rel in self.schema['relationships']:
                rel_key = f"{rel['from']}-{rel['type']}-{rel['to']}"
                if rel_key not in seen_rels:
                    mermaid_lines.append(
                        f"    {rel['from']} -->|{rel['type']}| {rel['to']}"
                    )
                    seen_rels.add(rel_key)

            mermaid_content = "\n".join(mermaid_lines)

            with open(output_file, 'w') as f:
                f.write(mermaid_content)

            logger.info(f"{Colors.OKGREEN}✓ Mermaid diagram: {output_file}{Colors.ENDC}")
            return True

        except Exception as e:
            logger.error(f"{Colors.FAIL}✗ Mermaid generation failed: {e}{Colors.ENDC}")
            return False

    def generate_graphml(self, output_file: str) -> bool:
        """Generate GraphML format for yEd"""
        logger.info("Generating GraphML...")

        try:
            graphml_lines = [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
                '<key id="d0" for="node" attr.name="label" attr.type="string"/>',
                '<key id="d1" for="node" attr.name="properties" attr.type="string"/>',
                '<key id="d2" for="edge" attr.name="type" attr.type="string"/>',
                '<graph edgedefault="directed">',
            ]

            # Add nodes
            for node in self.schema['nodes']:
                node_id = node['label'].replace(' ', '_')
                props = ', '.join(node['properties'][:5])  # Limit to 5 properties
                graphml_lines.append(
                    f'  <node id="{node_id}">'
                    f'<data key="d0">{node["label"]}</data>'
                    f'<data key="d1">{props}</data>'
                    f'</node>'
                )

            # Add edges
            seen_rels = set()
            for rel in self.schema['relationships']:
                rel_key = f"{rel['from']}-{rel['to']}"
                if rel_key not in seen_rels:
                    from_id = rel['from'].replace(' ', '_')
                    to_id = rel['to'].replace(' ', '_')
                    edge_id = f"e_{from_id}_{to_id}"
                    graphml_lines.append(
                        f'  <edge id="{edge_id}" source="{from_id}" target="{to_id}">'
                        f'<data key="d2">{rel["type"]}</data>'
                        f'</edge>'
                    )
                    seen_rels.add(rel_key)

            graphml_lines.extend(['</graph>', '</graphml>'])

            with open(output_file, 'w') as f:
                f.write('\n'.join(graphml_lines))

            logger.info(f"{Colors.OKGREEN}✓ GraphML file: {output_file}{Colors.ENDC}")
            return True

        except Exception as e:
            logger.error(f"{Colors.FAIL}✗ GraphML generation failed: {e}{Colors.ENDC}")
            return False

    def generate_html_interactive(self, output_file: str) -> bool:
        """Generate interactive HTML with vis.js"""
        logger.info("Generating interactive HTML...")

        try:
            # Prepare node data
            nodes = []
            for i, node in enumerate(self.schema['nodes']):
                nodes.append({
                    'id': i,
                    'label': node['label'],
                    'title': ', '.join(node['properties'][:5])
                })

            # Prepare edge data
            edges = []
            node_map = {n['label']: n['id'] for n in nodes}
            seen_rels = set()

            for rel in self.schema['relationships']:
                if rel['from'] in node_map and rel['to'] in node_map:
                    rel_key = f"{rel['from']}-{rel['to']}"
                    if rel_key not in seen_rels:
                        edges.append({
                            'from': node_map[rel['from']],
                            'to': node_map[rel['to']],
                            'label': rel['type']
                        })
                        seen_rels.add(rel_key)

            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Neo4j Schema Diagram</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        body {{ font-family: Arial, sans-serif; margin: 0; }}
        #network {{ width: 100%; height: 100vh; border: 1px solid lightgray; }}
        #info {{ position: absolute; top: 10px; left: 10px; background: rgba(255,255,255,0.9);
                 padding: 10px; border-radius: 5px; max-width: 300px; }}
    </style>
</head>
<body>
    <div id="network"></div>
    <div id="info">
        <h3>Neo4j Schema</h3>
        <p>Nodes: {len(self.schema['nodes'])}</p>
        <p>Relationships: {len(set(f"{r['from']}-{r['to']}" for r in self.schema['relationships']))}</p>
        <p><em>Drag to move, scroll to zoom</em></p>
    </div>

    <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(nodes)});
        var edges = new vis.DataSet({json.dumps(edges)});

        var container = document.getElementById('network');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
            physics: {{
                enabled: true,
                stabilization: {{ iterations: 200 }},
                barnesHut: {{ gravitationalConstant: -30000 }}
            }},
            nodes: {{
                shape: 'box',
                margin: 10,
                widthConstraint: {{ maximum: 200 }}
            }},
            edges: {{
                arrows: 'to',
                smooth: {{ type: 'continuous' }}
            }}
        }};

        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>
"""

            with open(output_file, 'w') as f:
                f.write(html_content)

            logger.info(f"{Colors.OKGREEN}✓ Interactive HTML: {output_file}{Colors.ENDC}")
            return True

        except Exception as e:
            logger.error(f"{Colors.FAIL}✗ HTML generation failed: {e}{Colors.ENDC}")
            return False

    def export_schema_json(self, output_file: str) -> bool:
        """Export raw schema as JSON"""
        logger.info("Exporting schema as JSON...")

        try:
            with open(output_file, 'w') as f:
                json.dump(self.schema, f, indent=2)

            logger.info(f"{Colors.OKGREEN}✓ Schema JSON: {output_file}{Colors.ENDC}")
            return True

        except Exception as e:
            logger.error(f"{Colors.FAIL}✗ JSON export failed: {e}{Colors.ENDC}")
            return False


def main():
    """Main export routine"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Export Neo4j schema in multiple formats'
    )

    parser.add_argument('--uri', default=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
                        help='Neo4j connection URI')
    parser.add_argument('--user', default=os.getenv('NEO4J_USER', 'neo4j'),
                        help='Neo4j username')
    parser.add_argument('--password', default=os.getenv('NEO4J_PASSWORD'),
                        help='Neo4j password')
    parser.add_argument('--output', default='docs/schema',
                        help='Output directory')
    parser.add_argument('--all', action='store_true',
                        help='Export all formats')
    parser.add_argument('--mermaid', action='store_true', help='Export Mermaid diagram')
    parser.add_argument('--graphml', action='store_true', help='Export GraphML')
    parser.add_argument('--html', action='store_true', help='Export interactive HTML')
    parser.add_argument('--json', action='store_true', help='Export JSON')

    args = parser.parse_args()

    if not args.password:
        print(f"{Colors.FAIL}Error: NEO4J_PASSWORD required{Colors.ENDC}")
        sys.exit(1)

    # Create output directory
    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Initialize exporter
    exporter = SchemaExporter(args.uri, args.user, args.password)

    if not exporter.connect():
        sys.exit(1)

    try:
        if not exporter.extract_schema():
            sys.exit(1)

        # Export formats
        if args.all or args.mermaid:
            exporter.generate_mermaid(os.path.join(args.output, 'schema.mmd'))

        if args.all or args.graphml:
            exporter.generate_graphml(os.path.join(args.output, 'schema.graphml'))

        if args.all or args.html:
            exporter.generate_html_interactive(os.path.join(args.output, 'schema.html'))

        if args.all or args.json:
            exporter.export_schema_json(os.path.join(args.output, 'schema.json'))

        if not any([args.all, args.mermaid, args.graphml, args.html, args.json]):
            # Export all by default
            exporter.generate_mermaid(os.path.join(args.output, 'schema.mmd'))
            exporter.generate_graphml(os.path.join(args.output, 'schema.graphml'))
            exporter.generate_html_interactive(os.path.join(args.output, 'schema.html'))
            exporter.export_schema_json(os.path.join(args.output, 'schema.json'))

        print(f"\n{Colors.OKGREEN}✓ Schema export completed!{Colors.ENDC}")

    finally:
        exporter.disconnect()


if __name__ == '__main__':
    main()
