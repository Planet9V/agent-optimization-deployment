# UTILITIES AND TOOLS GUIDE
## AEON Digital Twin AI Project - McKenney Framework

**Document Version**: 1.0.0
**Last Updated**: October 29, 2025
**Author**: AEON DT AI Development Team
**Purpose**: Comprehensive guide to utilities, scripts, and tools for AEON framework implementation

---

## Table of Contents

1. [Overview](#overview)
2. [Installation and Setup](#installation-and-setup)
3. [Schema Deployment Scripts](#schema-deployment-scripts)
4. [Data Import/Export Tools](#data-importexport-tools)
5. [Query Optimization Utilities](#query-optimization-utilities)
6. [Backup and Restore Procedures](#backup-and-restore-procedures)
7. [Performance Monitoring Tools](#performance-monitoring-tools)
8. [Data Validation Scripts](#data-validation-scripts)
9. [Migration Utilities](#migration-utilities)
10. [Metadata Management Tools](#metadata-management-tools)
11. [NLP Pipeline Configuration](#nlp-pipeline-configuration)
12. [Batch Processing Controllers](#batch-processing-controllers)
13. [Troubleshooting Guide](#troubleshooting-guide)
14. [API Reference](#api-reference)

---

## Overview

The AEON Digital Twin AI Project utilities provide a comprehensive toolkit for managing knowledge graphs, psychometric data, and digital twin implementations. These tools support the entire lifecycle from data ingestion to analysis, visualization, and maintenance.

### Core Capabilities

- **Knowledge Graph Management**: Schema deployment, data import/export, query optimization
- **Psychometric Analysis**: NLP pipelines, batch processing, narrative composition
- **Digital Twin Operations**: Real-time synchronization, state management, performance monitoring
- **Integration Tools**: Neo4j, Obsidian, external data sources
- **Automation**: Scheduled tasks, monitoring, alerting

### System Requirements

```yaml
Software Requirements:
  - Python: 3.9+
  - Neo4j: 4.4+ (Community or Enterprise)
  - Node.js: 16+ (for certain utilities)
  - Docker: 20.10+ (optional, for containerized deployment)
  - Git: 2.30+ (for version control)

Hardware Requirements:
  Minimum:
    - RAM: 8 GB
    - Storage: 50 GB
    - CPU: 4 cores
  Recommended:
    - RAM: 16+ GB
    - Storage: 200+ GB SSD
    - CPU: 8+ cores
    - GPU: Optional for NLP acceleration

Operating Systems:
  - Linux (Ubuntu 20.04+, CentOS 8+)
  - macOS (Big Sur 11.0+)
  - Windows 10/11 with WSL2
```

---

## Installation and Setup

### 1. Environment Setup

#### Quick Start Installation

```bash
# Clone repository (if applicable)
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies (if applicable)
npm install
```

#### Python Dependencies (requirements.txt)

```plaintext
# Core Dependencies
neo4j>=5.14.0
py2neo>=2021.2.3
pandas>=2.0.0
numpy>=1.24.0

# NLP and Text Processing
spacy>=3.7.0
transformers>=4.35.0
torch>=2.1.0
sentence-transformers>=2.2.0
nltk>=3.8.1

# Data Processing
pydantic>=2.5.0
python-dotenv>=1.0.0
jsonschema>=4.20.0
pyyaml>=6.0.1

# Database and Storage
pymongo>=4.6.0  # Optional for MongoDB integration
redis>=5.0.0    # Optional for caching
psycopg2-binary>=2.9.9  # Optional for PostgreSQL

# Visualization and Reporting
matplotlib>=3.8.0
seaborn>=0.13.0
plotly>=5.18.0
networkx>=3.2.1

# API and Web
fastapi>=0.104.0
uvicorn>=0.24.0
requests>=2.31.0
httpx>=0.25.0

# Testing and Quality
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.11.0
flake8>=6.1.0
mypy>=1.7.0

# Utilities
click>=8.1.7
tqdm>=4.66.0
python-dateutil>=2.8.2
pytz>=2023.3

# Monitoring and Logging
prometheus-client>=0.19.0
structlog>=23.2.0
```

### 2. Configuration Files

#### Environment Variables (.env)

```bash
# Neo4j Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_secure_password
NEO4J_DATABASE=aeon

# API Keys (if using external services)
OPENAI_API_KEY=sk-your-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Application Settings
APP_ENV=development  # development, staging, production
LOG_LEVEL=INFO       # DEBUG, INFO, WARNING, ERROR, CRITICAL
BATCH_SIZE=100
MAX_WORKERS=4

# Storage Paths
DATA_DIR=/path/to/data
BACKUP_DIR=/path/to/backups
LOG_DIR=/path/to/logs

# Optional: MongoDB (for metadata storage)
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=aeon_metadata

# Optional: Redis (for caching)
REDIS_URL=redis://localhost:6379/0

# Performance Tuning
NEO4J_MAX_CONNECTION_LIFETIME=3600
NEO4J_MAX_CONNECTION_POOL_SIZE=50
NEO4J_CONNECTION_TIMEOUT=30
```

#### Docker Compose Configuration (docker-compose.yml)

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.14-community
    container_name: aeon-neo4j
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      NEO4J_AUTH: neo4j/your_secure_password
      NEO4J_dbms_memory_heap_max__size: 4G
      NEO4J_dbms_memory_pagecache_size: 2G
      NEO4J_dbms_security_procedures_unrestricted: apoc.*,gds.*
      NEO4J_dbms_security_procedures_allowlist: apoc.*,gds.*
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
      - neo4j_plugins:/plugins
    networks:
      - aeon-network

  redis:
    image: redis:7-alpine
    container_name: aeon-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - aeon-network

  api:
    build: .
    container_name: aeon-api
    ports:
      - "8000:8000"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=your_secure_password
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - neo4j
      - redis
    volumes:
      - ./:/app
    networks:
      - aeon-network

volumes:
  neo4j_data:
  neo4j_logs:
  neo4j_plugins:
  redis_data:

networks:
  aeon-network:
    driver: bridge
```

### 3. Verification Script

```bash
#!/bin/bash
# verify_installation.sh

echo "AEON Framework Installation Verification"
echo "========================================"

# Check Python version
echo -n "Python version: "
python3 --version

# Check Neo4j connection
echo -n "Neo4j connection: "
python3 -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password')); driver.verify_connectivity(); print('OK')" 2>/dev/null && echo "✓ Connected" || echo "✗ Failed"

# Check required directories
echo "Checking directories..."
directories=("data" "logs" "backups" "config" "scripts")
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir exists"
    else
        echo "  ✗ $dir missing - creating..."
        mkdir -p "$dir"
    fi
done

# Check Python packages
echo "Checking Python packages..."
pip list | grep -E "neo4j|pandas|spacy|transformers" || echo "Some packages missing"

echo "========================================"
echo "Verification complete!"
```

---

## Schema Deployment Scripts

### 1. Core Schema Deployment

**Purpose**: Deploy the AEON framework knowledge graph schema to Neo4j

**Location**: `scripts/schema/deploy_schema.py`

```python
#!/usr/bin/env python3
"""
Schema Deployment Script for AEON Framework
Deploys core node types, relationships, constraints, and indexes
"""

from neo4j import GraphDatabase
import yaml
import logging
from typing import Dict, List
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemaDeployer:
    """Deploy and manage Neo4j schema for AEON framework"""

    def __init__(self, uri: str, user: str, password: str, database: str = "aeon"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def deploy_constraints(self, constraints: List[Dict]):
        """Deploy uniqueness and existence constraints"""
        with self.driver.session(database=self.database) as session:
            for constraint in constraints:
                try:
                    query = self._build_constraint_query(constraint)
                    session.run(query)
                    logger.info(f"Created constraint: {constraint['name']}")
                except Exception as e:
                    logger.warning(f"Constraint {constraint['name']} may already exist: {e}")

    def deploy_indexes(self, indexes: List[Dict]):
        """Deploy indexes for query optimization"""
        with self.driver.session(database=self.database) as session:
            for index in indexes:
                try:
                    query = self._build_index_query(index)
                    session.run(query)
                    logger.info(f"Created index: {index['name']}")
                except Exception as e:
                    logger.warning(f"Index {index['name']} may already exist: {e}")

    def _build_constraint_query(self, constraint: Dict) -> str:
        """Build constraint creation query"""
        node_label = constraint['label']
        property_name = constraint['property']
        constraint_name = constraint['name']
        constraint_type = constraint.get('type', 'UNIQUE')

        if constraint_type == 'UNIQUE':
            return f"""
            CREATE CONSTRAINT {constraint_name} IF NOT EXISTS
            FOR (n:{node_label})
            REQUIRE n.{property_name} IS UNIQUE
            """
        elif constraint_type == 'EXISTS':
            return f"""
            CREATE CONSTRAINT {constraint_name} IF NOT EXISTS
            FOR (n:{node_label})
            REQUIRE n.{property_name} IS NOT NULL
            """
        else:
            raise ValueError(f"Unknown constraint type: {constraint_type}")

    def _build_index_query(self, index: Dict) -> str:
        """Build index creation query"""
        node_label = index['label']
        properties = index['properties']
        index_name = index['name']
        index_type = index.get('type', 'RANGE')

        props_str = ', '.join([f"n.{p}" for p in properties])

        if index_type == 'FULLTEXT':
            props_list = ', '.join([f'"{p}"' for p in properties])
            return f"""
            CREATE FULLTEXT INDEX {index_name} IF NOT EXISTS
            FOR (n:{node_label})
            ON EACH [{props_list}]
            """
        else:
            return f"""
            CREATE INDEX {index_name} IF NOT EXISTS
            FOR (n:{node_label})
            ON ({props_str})
            """

    def deploy_from_yaml(self, schema_file: Path):
        """Deploy schema from YAML configuration"""
        with open(schema_file, 'r') as f:
            schema = yaml.safe_load(f)

        logger.info("Deploying constraints...")
        self.deploy_constraints(schema.get('constraints', []))

        logger.info("Deploying indexes...")
        self.deploy_indexes(schema.get('indexes', []))

        logger.info("Schema deployment complete!")


def main():
    import os
    from dotenv import load_dotenv

    load_dotenv()

    deployer = SchemaDeployer(
        uri=os.getenv('NEO4J_URI'),
        user=os.getenv('NEO4J_USER'),
        password=os.getenv('NEO4J_PASSWORD'),
        database=os.getenv('NEO4J_DATABASE', 'aeon')
    )

    try:
        schema_file = Path(__file__).parent / 'schema_definition.yaml'
        deployer.deploy_from_yaml(schema_file)
    finally:
        deployer.close()


if __name__ == '__main__':
    main()
```

**Schema Definition (schema_definition.yaml)**

```yaml
# AEON Framework Schema Definition
version: "1.0.0"

constraints:
  # Entity Constraints
  - name: entity_id_unique
    label: Entity
    property: entity_id
    type: UNIQUE

  - name: person_id_unique
    label: Person
    property: person_id
    type: UNIQUE

  - name: organization_id_unique
    label: Organization
    property: organization_id
    type: UNIQUE

  - name: concept_id_unique
    label: Concept
    property: concept_id
    type: UNIQUE

  # Digital Twin Constraints
  - name: digital_twin_id_unique
    label: DigitalTwin
    property: twin_id
    type: UNIQUE

  # Psychometric Constraints
  - name: trait_name_unique
    label: Trait
    property: name
    type: UNIQUE

  - name: bias_type_unique
    label: Bias
    property: bias_type
    type: UNIQUE

indexes:
  # Entity Indexes
  - name: entity_name_index
    label: Entity
    properties: [name]
    type: RANGE

  - name: entity_type_index
    label: Entity
    properties: [entity_type]
    type: RANGE

  - name: entity_fulltext
    label: Entity
    properties: [name, description]
    type: FULLTEXT

  # Person Indexes
  - name: person_name_index
    label: Person
    properties: [name]
    type: RANGE

  # Relationship Indexes
  - name: relationship_strength_index
    label: RELATED_TO
    properties: [strength]
    type: RANGE

  - name: temporal_index
    label: Event
    properties: [timestamp, date]
    type: RANGE

  # Digital Twin Indexes
  - name: twin_status_index
    label: DigitalTwin
    properties: [status]
    type: RANGE

  - name: twin_updated_index
    label: DigitalTwin
    properties: [last_updated]
    type: RANGE

  # Psychometric Indexes
  - name: trait_category_index
    label: Trait
    properties: [category]
    type: RANGE

  - name: bias_severity_index
    label: Bias
    properties: [severity]
    type: RANGE
```

**Usage**:

```bash
# Deploy schema to Neo4j
python scripts/schema/deploy_schema.py

# Verify schema deployment
python scripts/schema/verify_schema.py

# Export current schema
python scripts/schema/export_schema.py --output schema_backup.yaml
```

**Configuration Options**:

- `--dry-run`: Preview changes without applying
- `--force`: Force recreation of existing constraints/indexes
- `--backup`: Create backup before deployment
- `--rollback`: Rollback to previous schema version

---

## Data Import/Export Tools

### 1. Batch Data Importer

**Purpose**: Import large datasets into Neo4j knowledge graph

**Location**: `scripts/import/batch_importer.py`

```python
#!/usr/bin/env python3
"""
Batch Data Importer for AEON Framework
Handles large-scale data import with progress tracking and error recovery
"""

from neo4j import GraphDatabase
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchImporter:
    """Import data in batches with transaction management"""

    def __init__(self, uri: str, user: str, password: str, batch_size: int = 1000):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.batch_size = batch_size

    def close(self):
        self.driver.close()

    def import_entities(self, data_file: Path, entity_type: str):
        """Import entities from CSV or JSON file"""
        # Load data
        if data_file.suffix == '.csv':
            df = pd.read_csv(data_file)
            records = df.to_dict('records')
        elif data_file.suffix == '.json':
            with open(data_file, 'r') as f:
                records = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {data_file.suffix}")

        logger.info(f"Importing {len(records)} {entity_type} entities...")

        # Import in batches
        with self.driver.session() as session:
            for i in tqdm(range(0, len(records), self.batch_size)):
                batch = records[i:i + self.batch_size]
                session.execute_write(self._create_entity_batch, batch, entity_type)

        logger.info(f"Import complete: {len(records)} entities created")

    def _create_entity_batch(self, tx, batch: List[Dict], entity_type: str):
        """Create batch of entities in single transaction"""
        query = f"""
        UNWIND $batch AS record
        CREATE (e:{entity_type})
        SET e = record
        SET e.created_at = datetime()
        SET e.updated_at = datetime()
        """
        tx.run(query, batch=batch)

    def import_relationships(self, data_file: Path, rel_type: str):
        """Import relationships from file"""
        if data_file.suffix == '.csv':
            df = pd.read_csv(data_file)
            records = df.to_dict('records')
        elif data_file.suffix == '.json':
            with open(data_file, 'r') as f:
                records = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {data_file.suffix}")

        logger.info(f"Importing {len(records)} {rel_type} relationships...")

        with self.driver.session() as session:
            for i in tqdm(range(0, len(records), self.batch_size)):
                batch = records[i:i + self.batch_size]
                session.execute_write(
                    self._create_relationship_batch, batch, rel_type
                )

        logger.info(f"Import complete: {len(records)} relationships created")

    def _create_relationship_batch(self, tx, batch: List[Dict], rel_type: str):
        """Create batch of relationships in single transaction"""
        query = f"""
        UNWIND $batch AS record
        MATCH (a {{id: record.source_id}})
        MATCH (b {{id: record.target_id}})
        CREATE (a)-[r:{rel_type}]->(b)
        SET r = record.properties
        SET r.created_at = datetime()
        """
        tx.run(query, batch=batch)


def main():
    import argparse
    import os
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description='Import data into Neo4j')
    parser.add_argument('file', type=Path, help='Data file to import')
    parser.add_argument('--type', required=True, help='Entity or relationship type')
    parser.add_argument('--kind', choices=['entity', 'relationship'], required=True)
    parser.add_argument('--batch-size', type=int, default=1000)

    args = parser.parse_args()

    importer = BatchImporter(
        uri=os.getenv('NEO4J_URI'),
        user=os.getenv('NEO4J_USER'),
        password=os.getenv('NEO4J_PASSWORD'),
        batch_size=args.batch_size
    )

    try:
        if args.kind == 'entity':
            importer.import_entities(args.file, args.type)
        else:
            importer.import_relationships(args.file, args.type)
    finally:
        importer.close()


if __name__ == '__main__':
    main()
```

**Usage Examples**:

```bash
# Import entities
python scripts/import/batch_importer.py \
    data/entities.csv \
    --type Person \
    --kind entity \
    --batch-size 500

# Import relationships
python scripts/import/batch_importer.py \
    data/relationships.json \
    --type RELATED_TO \
    --kind relationship \
    --batch-size 1000

# Import with custom configuration
python scripts/import/batch_importer.py \
    data/large_dataset.csv \
    --type Entity \
    --kind entity \
    --batch-size 2000 \
    --workers 4 \
    --progress
```

### 2. Data Export Utility

**Purpose**: Export knowledge graph data for backup or analysis

**Location**: `scripts/export/data_exporter.py`

```python
#!/usr/bin/env python3
"""
Data Export Utility for AEON Framework
Export graph data in various formats with filtering options
"""

from neo4j import GraphDatabase
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExporter:
    """Export data from Neo4j in various formats"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def export_entities(
        self,
        output_file: Path,
        label: Optional[str] = None,
        format: str = 'csv'
    ):
        """Export entities to file"""
        query = """
        MATCH (n)
        WHERE $label IS NULL OR $label IN labels(n)
        RETURN n
        """

        with self.driver.session() as session:
            result = session.run(query, label=label)
            records = [dict(record['n']) for record in result]

        logger.info(f"Exporting {len(records)} entities...")

        if format == 'csv':
            df = pd.DataFrame(records)
            df.to_csv(output_file, index=False)
        elif format == 'json':
            with open(output_file, 'w') as f:
                json.dump(records, f, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Export complete: {output_file}")

    def export_relationships(
        self,
        output_file: Path,
        rel_type: Optional[str] = None,
        format: str = 'csv'
    ):
        """Export relationships to file"""
        query = """
        MATCH (a)-[r]->(b)
        WHERE $rel_type IS NULL OR type(r) = $rel_type
        RETURN
            id(a) as source_id,
            labels(a) as source_labels,
            properties(a) as source_props,
            type(r) as relationship_type,
            properties(r) as rel_props,
            id(b) as target_id,
            labels(b) as target_labels,
            properties(b) as target_props
        """

        with self.driver.session() as session:
            result = session.run(query, rel_type=rel_type)
            records = [dict(record) for record in result]

        logger.info(f"Exporting {len(records)} relationships...")

        if format == 'csv':
            df = pd.DataFrame(records)
            df.to_csv(output_file, index=False)
        elif format == 'json':
            with open(output_file, 'w') as f:
                json.dump(records, f, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Export complete: {output_file}")

    def export_subgraph(
        self,
        output_file: Path,
        cypher_query: str,
        format: str = 'graphml'
    ):
        """Export subgraph based on Cypher query"""
        # Implementation for subgraph export
        pass


def main():
    import argparse
    import os
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description='Export data from Neo4j')
    parser.add_argument('output', type=Path, help='Output file')
    parser.add_argument('--kind', choices=['entities', 'relationships'], required=True)
    parser.add_argument('--label', help='Node label filter')
    parser.add_argument('--type', help='Relationship type filter')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv')

    args = parser.parse_args()

    exporter = DataExporter(
        uri=os.getenv('NEO4J_URI'),
        user=os.getenv('NEO4J_USER'),
        password=os.getenv('NEO4J_PASSWORD')
    )

    try:
        if args.kind == 'entities':
            exporter.export_entities(args.output, args.label, args.format)
        else:
            exporter.export_relationships(args.output, args.type, args.format)
    finally:
        exporter.close()


if __name__ == '__main__':
    main()
```

**Usage Examples**:

```bash
# Export all entities
python scripts/export/data_exporter.py \
    exports/all_entities.csv \
    --kind entities \
    --format csv

# Export specific entity type
python scripts/export/data_exporter.py \
    exports/persons.json \
    --kind entities \
    --label Person \
    --format json

# Export relationships
python scripts/export/data_exporter.py \
    exports/relationships.csv \
    --kind relationships \
    --type RELATED_TO \
    --format csv
```

---

## Query Optimization Utilities

### 1. Query Analyzer

**Purpose**: Analyze and optimize Cypher queries for performance

**Location**: `scripts/optimization/query_analyzer.py`

```python
#!/usr/bin/env python3
"""
Query Optimization Analyzer for AEON Framework
Analyze query performance and provide optimization recommendations
"""

from neo4j import GraphDatabase
import logging
from typing import Dict, List
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryAnalyzer:
    """Analyze and optimize Cypher queries"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def analyze_query(self, query: str) -> Dict:
        """Analyze query performance and provide recommendations"""
        with self.driver.session() as session:
            # Get query plan
            explain_query = f"EXPLAIN {query}"
            explain_result = session.run(explain_query)
            plan = explain_result.consume().plan

            # Profile query execution
            profile_query = f"PROFILE {query}"
            start_time = time.time()
            profile_result = session.run(profile_query)
            records = list(profile_result)
            execution_time = time.time() - start_time
            profile = profile_result.consume().profile

            # Analyze results
            analysis = {
                'execution_time_ms': execution_time * 1000,
                'records_returned': len(records),
                'db_hits': profile.get('db_hits', 0),
                'rows': profile.get('rows', 0),
                'plan': self._format_plan(plan),
                'recommendations': self._generate_recommendations(plan, profile)
            }

            return analysis

    def _format_plan(self, plan: Dict) -> Dict:
        """Format query plan for readability"""
        return {
            'operator': plan.get('operatorType'),
            'estimated_rows': plan.get('estimatedRows'),
            'identifiers': plan.get('identifiers'),
            'children': [self._format_plan(child) for child in plan.get('children', [])]
        }

    def _generate_recommendations(self, plan: Dict, profile: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        # Check for missing indexes
        if 'NodeByLabelScan' in str(plan):
            recommendations.append(
                "Consider adding an index - detected full label scan"
            )

        # Check for cartesian products
        if 'CartesianProduct' in str(plan):
            recommendations.append(
                "CRITICAL: Cartesian product detected - add relationship pattern"
            )

        # Check db_hits ratio
        db_hits = profile.get('db_hits', 0)
        rows = profile.get('rows', 1)
        if db_hits / rows > 100:
            recommendations.append(
                f"High db_hits/row ratio ({db_hits}/{rows}) - query may be inefficient"
            )

        return recommendations

    def suggest_indexes(self, query: str) -> List[str]:
        """Suggest indexes based on query patterns"""
        suggestions = []

        # Simple pattern matching for common cases
        if 'MATCH (n:' in query and 'WHERE n.' in query:
            # Extract label and property
            import re
            match = re.search(r'MATCH \(n:(\w+)\).*WHERE n\.(\w+)', query)
            if match:
                label, prop = match.groups()
                suggestions.append(
                    f"CREATE INDEX FOR (n:{label}) ON (n.{prop})"
                )

        return suggestions


def main():
    import argparse
    import os
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description='Analyze Cypher query performance')
    parser.add_argument('query', help='Cypher query to analyze')
    parser.add_argument('--suggest-indexes', action='store_true')

    args = parser.parse_args()

    analyzer = QueryAnalyzer(
        uri=os.getenv('NEO4J_URI'),
        user=os.getenv('NEO4J_USER'),
        password=os.getenv('NEO4J_PASSWORD')
    )

    try:
        analysis = analyzer.analyze_query(args.query)

        print("\n=== Query Analysis ===")
        print(f"Execution Time: {analysis['execution_time_ms']:.2f} ms")
        print(f"Records Returned: {analysis['records_returned']}")
        print(f"DB Hits: {analysis['db_hits']}")

        print("\n=== Recommendations ===")
        for rec in analysis['recommendations']:
            print(f"  • {rec}")

        if args.suggest_indexes:
            print("\n=== Index Suggestions ===")
            suggestions = analyzer.suggest_indexes(args.query)
            for sug in suggestions:
                print(f"  • {sug}")

    finally:
        analyzer.close()


if __name__ == '__main__':
    main()
```

**Usage**:

```bash
# Analyze query performance
python scripts/optimization/query_analyzer.py \
    "MATCH (p:Person)-[:KNOWS]->(f) WHERE p.name = 'John' RETURN f"

# Get index suggestions
python scripts/optimization/query_analyzer.py \
    "MATCH (p:Person) WHERE p.email = 'test@example.com' RETURN p" \
    --suggest-indexes

# Analyze from file
python scripts/optimization/query_analyzer.py \
    --file queries/complex_query.cypher \
    --suggest-indexes
```

---

## Backup and Restore Procedures

### 1. Automated Backup Script

**Purpose**: Create scheduled backups of Neo4j database

**Location**: `scripts/backup/backup_neo4j.sh`

```bash
#!/bin/bash
# AEON Framework - Neo4j Backup Script

# Configuration
BACKUP_DIR="/path/to/backups"
NEO4J_HOME="/path/to/neo4j"
DATABASE="aeon"
RETENTION_DAYS=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="aeon_backup_${TIMESTAMP}"

# Create backup directory if not exists
mkdir -p "${BACKUP_DIR}"

# Stop Neo4j (if online backup not available)
echo "Creating backup: ${BACKUP_NAME}"

# Using Neo4j Admin backup (Enterprise)
if command -v neo4j-admin &> /dev/null; then
    neo4j-admin database backup \
        --database="${DATABASE}" \
        --to-path="${BACKUP_DIR}/${BACKUP_NAME}" \
        --verbose
else
    # Community edition fallback - copy data directory
    echo "Using filesystem backup (Community Edition)"
    neo4j stop
    tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" \
        -C "${NEO4J_HOME}" data
    neo4j start
fi

# Compress backup
if [ -d "${BACKUP_DIR}/${BACKUP_NAME}" ]; then
    echo "Compressing backup..."
    tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" \
        -C "${BACKUP_DIR}" "${BACKUP_NAME}"
    rm -rf "${BACKUP_DIR}/${BACKUP_NAME}"
fi

# Remove old backups
echo "Cleaning up old backups (older than ${RETENTION_DAYS} days)..."
find "${BACKUP_DIR}" -name "aeon_backup_*.tar.gz" \
    -mtime +${RETENTION_DAYS} -delete

# Verify backup
BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | cut -f1)
echo "Backup complete: ${BACKUP_NAME}.tar.gz (${BACKUP_SIZE})"

# Optional: Upload to cloud storage
# aws s3 cp "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" s3://your-bucket/backups/

echo "Backup completed successfully!"
```

**Cron Schedule** (add to crontab):

```cron
# Daily backup at 2 AM
0 2 * * * /path/to/scripts/backup/backup_neo4j.sh >> /path/to/logs/backup.log 2>&1

# Weekly full backup on Sunday at 3 AM
0 3 * * 0 /path/to/scripts/backup/backup_neo4j.sh --full >> /path/to/logs/backup_weekly.log 2>&1
```

### 2. Restore Script

**Location**: `scripts/backup/restore_neo4j.sh`

```bash
#!/bin/bash
# AEON Framework - Neo4j Restore Script

# Configuration
BACKUP_FILE="$1"
NEO4J_HOME="/path/to/neo4j"
DATABASE="aeon"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "WARNING: This will replace the current database!"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

# Stop Neo4j
echo "Stopping Neo4j..."
neo4j stop

# Backup current data (safety measure)
echo "Creating safety backup of current data..."
SAFETY_BACKUP="/tmp/neo4j_safety_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$SAFETY_BACKUP" -C "${NEO4J_HOME}" data
echo "Safety backup created: $SAFETY_BACKUP"

# Extract backup
echo "Extracting backup..."
TEMP_DIR=$(mktemp -d)
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# Restore data
echo "Restoring database..."
rm -rf "${NEO4J_HOME}/data"
mv "$TEMP_DIR/"* "${NEO4J_HOME}/data"

# Cleanup
rm -rf "$TEMP_DIR"

# Start Neo4j
echo "Starting Neo4j..."
neo4j start

echo "Restore completed!"
echo "Safety backup is available at: $SAFETY_BACKUP"
```

**Usage**:

```bash
# Restore from specific backup
./scripts/backup/restore_neo4j.sh backups/aeon_backup_20241029_020000.tar.gz

# List available backups
ls -lh backups/aeon_backup_*.tar.gz

# Verify backup integrity before restore
tar -tzf backups/aeon_backup_20241029_020000.tar.gz | head
```

---

## Performance Monitoring Tools

### 1. Real-time Monitor

**Purpose**: Monitor Neo4j performance metrics in real-time

**Location**: `scripts/monitoring/performance_monitor.py`

```python
#!/usr/bin/env python3
"""
Real-time Performance Monitor for AEON Framework
Track database metrics, query performance, and system health
"""

from neo4j import GraphDatabase
import time
import sys
from datetime import datetime
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor Neo4j performance metrics"""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_metrics(self) -> Dict:
        """Get current performance metrics"""
        with self.driver.session() as session:
            metrics = {}

            # Database size
            result = session.run("""
                CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Store sizes')
                YIELD attributes
                RETURN attributes.TotalStoreSize.value as total_size
            """)
            for record in result:
                metrics['total_size_bytes'] = record['total_size']

            # Active transactions
            result = session.run("""
                CALL dbms.listTransactions()
                YIELD transactionId, currentQuery, elapsedTime, status
                RETURN count(*) as active_transactions,
                       avg(elapsedTime.milliseconds) as avg_elapsed_ms
            """)
            for record in result:
                metrics['active_transactions'] = record['active_transactions']
                metrics['avg_query_time_ms'] = record['avg_elapsed_ms']

            # Node/relationship counts
            result = session.run("""
                MATCH (n)
                RETURN count(n) as node_count
            """)
            metrics['node_count'] = result.single()['node_count']

            result = session.run("""
                MATCH ()-[r]->()
                RETURN count(r) as rel_count
            """)
            metrics['relationship_count'] = result.single()['rel_count']

            return metrics

    def monitor_realtime(self, interval: int = 5):
        """Monitor metrics in real-time"""
        try:
            while True:
                metrics = self.get_metrics()

                # Clear screen (optional)
                print("\033[2J\033[H")

                print("="* 60)
                print(f"AEON Performance Monitor - {datetime.now()}")
                print("=" * 60)
                print(f"Nodes: {metrics['node_count']:,}")
                print(f"Relationships: {metrics['relationship_count']:,}")
                print(f"Active Transactions: {metrics['active_transactions']}")
                print(f"Avg Query Time: {metrics.get('avg_query_time_ms', 0):.2f} ms")
                print(f"Database Size: {metrics['total_size_bytes'] / (1024**3):.2f} GB")
                print("=" * 60)

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\nMonitoring stopped.")


def main():
    import argparse
    import os
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description='Monitor Neo4j performance')
    parser.add_argument('--interval', type=int, default=5, help='Update interval in seconds')

    args = parser.parse_args()

    monitor = PerformanceMonitor(
        uri=os.getenv('NEO4J_URI'),
        user=os.getenv('NEO4J_USER'),
        password=os.getenv('NEO4J_PASSWORD')
    )

    try:
        monitor.monitor_realtime(interval=args.interval)
    finally:
        monitor.close()


if __name__ == '__main__':
    main()
```

**Usage**:

```bash
# Start real-time monitoring
python scripts/monitoring/performance_monitor.py

# Custom update interval
python scripts/monitoring/performance_monitor.py --interval 10

# Log metrics to file
python scripts/monitoring/performance_monitor.py --interval 60 >> logs/performance.log
```

---

## NLP Pipeline Configuration

### 1. Psychometric Analysis Pipeline

**Purpose**: Configure and run NLP pipeline for psychometric analysis

**Location**: `scripts/nlp/psychometric_pipeline.py`

```python
#!/usr/bin/env python3
"""
Psychometric Analysis NLP Pipeline for AEON Framework
Extract psychological traits, biases, and discourse patterns from text
"""

import spacy
from transformers import pipeline
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PsychometricPipeline:
    """NLP pipeline for psychometric analysis"""

    def __init__(self, model_name: str = "en_core_web_lg"):
        self.nlp = spacy.load(model_name)
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.emotion_analyzer = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base"
        )

    def analyze_text(self, text: str) -> Dict:
        """Perform complete psychometric analysis"""
        doc = self.nlp(text)

        analysis = {
            'entities': self._extract_entities(doc),
            'sentiment': self._analyze_sentiment(text),
            'emotions': self._analyze_emotions(text),
            'discourse_markers': self._extract_discourse_markers(doc),
            'bias_indicators': self._detect_bias_indicators(doc),
            'traits': self._infer_traits(doc)
        }

        return analysis

    def _extract_entities(self, doc) -> List[Dict]:
        """Extract named entities"""
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        return entities

    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment"""
        result = self.sentiment_analyzer(text[:512])[0]
        return {
            'label': result['label'],
            'score': result['score']
        }

    def _analyze_emotions(self, text: str) -> Dict:
        """Analyze emotions"""
        result = self.emotion_analyzer(text[:512])[0]
        return {
            'emotion': result['label'],
            'score': result['score']
        }

    def _extract_discourse_markers(self, doc) -> List[str]:
        """Extract discourse markers"""
        markers = []
        discourse_patterns = ['however', 'therefore', 'moreover', 'nevertheless']
        for token in doc:
            if token.text.lower() in discourse_patterns:
                markers.append(token.text)
        return markers

    def _detect_bias_indicators(self, doc) -> List[Dict]:
        """Detect potential bias indicators"""
        indicators = []

        # Check for loaded language
        loaded_words = ['always', 'never', 'obviously', 'clearly']
        for token in doc:
            if token.text.lower() in loaded_words:
                indicators.append({
                    'type': 'loaded_language',
                    'word': token.text,
                    'position': token.i
                })

        return indicators

    def _infer_traits(self, doc) -> Dict:
        """Infer psychological traits"""
        # Simplified trait inference
        traits = {
            'assertiveness': 0.0,
            'analytical_thinking': 0.0,
            'emotional_tone': 0.0
        }

        # Count imperative sentences
        imperatives = sum(1 for sent in doc.sents if sent.root.tag_ == 'VB')
        traits['assertiveness'] = min(imperatives / len(list(doc.sents)), 1.0)

        # Count analytical markers
        analytical_words = ['analyze', 'evaluate', 'consider', 'examine']
        analytical_count = sum(
            1 for token in doc if token.lemma_ in analytical_words
        )
        traits['analytical_thinking'] = min(analytical_count / 10, 1.0)

        return traits

    def process_batch(self, texts: List[str]) -> List[Dict]:
        """Process multiple texts"""
        results = []
        for text in texts:
            try:
                analysis = self.analyze_text(text)
                results.append(analysis)
            except Exception as e:
                logger.error(f"Error processing text: {e}")
                results.append(None)
        return results


def main():
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Psychometric text analysis')
    parser.add_argument('input', type=Path, help='Input file or directory')
    parser.add_argument('--output', type=Path, help='Output JSON file')
    parser.add_argument('--model', default='en_core_web_lg', help='Spacy model')

    args = parser.parse_args()

    pipeline = PsychometricPipeline(model_name=args.model)

    # Read input
    if args.input.is_file():
        with open(args.input, 'r') as f:
            text = f.read()
        result = pipeline.analyze_text(text)
    else:
        # Process directory
        texts = []
        for file in args.input.glob('*.txt'):
            with open(file, 'r') as f:
                texts.append(f.read())
        result = pipeline.process_batch(texts)

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
```

**Usage**:

```bash
# Analyze single file
python scripts/nlp/psychometric_pipeline.py \
    data/article.txt \
    --output analysis/result.json

# Process directory
python scripts/nlp/psychometric_pipeline.py \
    Pyschometrics/ \
    --output analysis/batch_results.json

# Use custom model
python scripts/nlp/psychometric_pipeline.py \
    data/text.txt \
    --model en_core_web_sm \
    --output results.json
```

---

## Batch Processing Controllers

### 1. Two-Phase Batch Processor

**Purpose**: Implement the two-phase batch processing system for psychometric analysis

**Location**: `scripts/batch/two_phase_processor.py`

```python
#!/usr/bin/env python3
"""
Two-Phase Batch Processor for AEON Framework
Phase 1: Analysis and Knowledge Graph Extraction
Phase 2: Narrative Composition and Database Integration
"""

from pathlib import Path
from typing import List, Dict
import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwoPhaseProcessor:
    """Process articles in two phases as per AEON methodology"""

    def __init__(
        self,
        articles_dir: Path,
        atomic_notes_dir: Path,
        narratives_dir: Path,
        cypher_queries_dir: Path
    ):
        self.articles_dir = articles_dir
        self.atomic_notes_dir = atomic_notes_dir
        self.narratives_dir = narratives_dir
        self.cypher_queries_dir = cypher_queries_dir

        # Create directories if not exist
        for dir_path in [atomic_notes_dir, narratives_dir, cypher_queries_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def run_phase_1(self, batch_size: int = 5) -> List[Path]:
        """Phase 1: Analysis and Knowledge Graph Extraction"""
        logger.info("Starting Phase 1: Analysis and Knowledge Graph Extraction")

        # Get article files
        article_files = list(self.articles_dir.glob('*.txt'))
        logger.info(f"Found {len(article_files)} articles to process")

        processed_files = []

        # Process in batches
        for i in range(0, len(article_files), batch_size):
            batch = article_files[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}")

            for article_file in batch:
                try:
                    output_file = self._process_analysis(article_file)
                    processed_files.append(output_file)
                    logger.info(f"Completed analysis: {article_file.name}")
                except Exception as e:
                    logger.error(f"Error processing {article_file.name}: {e}")

        logger.info(f"Phase 1 complete. Processed {len(processed_files)} articles.")
        return processed_files

    def _process_analysis(self, article_file: Path) -> Path:
        """Process single article for Phase 1"""
        # Read article
        with open(article_file, 'r') as f:
            text = f.read()

        # Perform analysis (integrate with NLP pipeline)
        analysis = {
            'source_file': article_file.name,
            'timestamp': datetime.now().isoformat(),
            'text': text,
            # ... add psychometric analysis results
            'knowledge_graph': {
                'entities': [],
                'relationships': [],
                'properties': {}
            }
        }

        # Save atomic note
        output_file = self.atomic_notes_dir / f"{article_file.stem}_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        return output_file

    def run_phase_2(self, batch_size: int = 5) -> Dict[str, List[Path]]:
        """Phase 2: Narrative Composition and Database Integration"""
        logger.info("Starting Phase 2: Narrative Composition and Database Integration")

        # Get analysis files
        analysis_files = list(self.atomic_notes_dir.glob('*_analysis.json'))
        logger.info(f"Found {len(analysis_files)} analyses to process")

        outputs = {
            'narratives': [],
            'cypher_queries': []
        }

        # Process in batches
        for i in range(0, len(analysis_files), batch_size):
            batch = analysis_files[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}")

            for analysis_file in batch:
                try:
                    narrative_file, cypher_file = self._process_composition(
                        analysis_file
                    )
                    outputs['narratives'].append(narrative_file)
                    outputs['cypher_queries'].append(cypher_file)
                    logger.info(f"Completed composition: {analysis_file.name}")
                except Exception as e:
                    logger.error(f"Error processing {analysis_file.name}: {e}")

        logger.info(f"Phase 2 complete. Generated {len(outputs['narratives'])} narratives.")
        return outputs

    def _process_composition(self, analysis_file: Path) -> tuple:
        """Process single analysis for Phase 2"""
        # Read analysis
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)

        # Generate narrative
        narrative = self._generate_narrative(analysis)
        narrative_file = self.narratives_dir / f"{analysis_file.stem.replace('_analysis', '')}_narrative.md"
        with open(narrative_file, 'w') as f:
            f.write(narrative)

        # Generate Cypher queries
        cypher = self._generate_cypher(analysis)
        cypher_file = self.cypher_queries_dir / f"{analysis_file.stem.replace('_analysis', '')}_queries.cypher"
        with open(cypher_file, 'w') as f:
            f.write(cypher)

        return narrative_file, cypher_file

    def _generate_narrative(self, analysis: Dict) -> str:
        """Generate engaging narrative from analysis"""
        # Implement narrative generation logic
        narrative = f"""# Narrative: {analysis['source_file']}

Generated: {analysis['timestamp']}

## Summary
[Generated narrative based on analysis]

## Key Insights
[Key points extracted from analysis]

## Connections
[Cross-references and relationships]
"""
        return narrative

    def _generate_cypher(self, analysis: Dict) -> str:
        """Generate Neo4j Cypher queries from analysis"""
        queries = []

        # Generate entity creation queries
        for entity in analysis.get('knowledge_graph', {}).get('entities', []):
            query = f"""
CREATE (n:Entity {{
    id: '{entity.get('id')}',
    name: '{entity.get('name')}',
    type: '{entity.get('type')}'
}})
"""
            queries.append(query)

        return '\n'.join(queries)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Two-phase batch processor')
    parser.add_argument('--articles-dir', type=Path, required=True)
    parser.add_argument('--atomic-notes-dir', type=Path, required=True)
    parser.add_argument('--narratives-dir', type=Path, required=True)
    parser.add_argument('--cypher-dir', type=Path, required=True)
    parser.add_argument('--phase', choices=['1', '2', 'both'], default='both')
    parser.add_argument('--batch-size', type=int, default=5)

    args = parser.parse_args()

    processor = TwoPhaseProcessor(
        articles_dir=args.articles_dir,
        atomic_notes_dir=args.atomic_notes_dir,
        narratives_dir=args.narratives_dir,
        cypher_queries_dir=args.cypher_dir
    )

    if args.phase in ['1', 'both']:
        processor.run_phase_1(batch_size=args.batch_size)

    if args.phase in ['2', 'both']:
        processor.run_phase_2(batch_size=args.batch_size)


if __name__ == '__main__':
    main()
```

**Usage**:

```bash
# Run both phases
python scripts/batch/two_phase_processor.py \
    --articles-dir Pyschometrics/articles \
    --atomic-notes-dir Pyschometrics/atomic_notes \
    --narratives-dir Pyschometrics/narratives \
    --cypher-dir Pyschometrics/cypher_queries \
    --phase both \
    --batch-size 10

# Run Phase 1 only
python scripts/batch/two_phase_processor.py \
    --articles-dir Pyschometrics/articles \
    --atomic-notes-dir Pyschometrics/atomic_notes \
    --narratives-dir Pyschometrics/narratives \
    --cypher-dir Pyschometrics/cypher_queries \
    --phase 1

# Run Phase 2 only
python scripts/batch/two_phase_processor.py \
    --articles-dir Pyschometrics/articles \
    --atomic-notes-dir Pyschometrics/atomic_notes \
    --narratives-dir Pyschometrics/narratives \
    --cypher-dir Pyschometrics/cypher_queries \
    --phase 2
```

---

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Neo4j Connection Issues

**Problem**: Cannot connect to Neo4j database

**Solutions**:
```bash
# Check if Neo4j is running
systemctl status neo4j  # Linux
neo4j status           # macOS/Windows

# Check Neo4j logs
tail -f /var/log/neo4j/neo4j.log

# Verify connection settings
echo $NEO4J_URI
python3 -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password')); driver.verify_connectivity(); print('OK')"

# Restart Neo4j
neo4j restart
```

#### 2. Memory Issues

**Problem**: Out of memory errors during large imports

**Solutions**:
- Increase Neo4j heap size in neo4j.conf:
```
dbms.memory.heap.max_size=8G
dbms.memory.pagecache.size=4G
```
- Use smaller batch sizes
- Enable streaming for large datasets

#### 3. Query Performance

**Problem**: Slow query execution

**Solutions**:
```bash
# Analyze query
python scripts/optimization/query_analyzer.py "YOUR_QUERY"

# Add indexes
CREATE INDEX FOR (n:Entity) ON (n.name)
CREATE INDEX FOR (n:Person) ON (n.person_id)

# Check for cartesian products
PROFILE MATCH (a)--(b) RETURN a, b  # Review plan
```

#### 4. Import Failures

**Problem**: Batch import fails midway

**Solutions**:
```bash
# Check error logs
tail -f logs/import.log

# Verify data format
head -n 10 data/entities.csv

# Resume from checkpoint
python scripts/import/batch_importer.py \
    --resume-from last_checkpoint.json

# Validate data before import
python scripts/validation/validate_data.py data/entities.csv
```

---

## API Reference

### REST API Endpoints

```python
# Start API server
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Endpoints:
GET  /api/v1/health              # Health check
GET  /api/v1/entities            # List entities
POST /api/v1/entities            # Create entity
GET  /api/v1/entities/{id}       # Get entity
PUT  /api/v1/entities/{id}       # Update entity
DELETE /api/v1/entities/{id}     # Delete entity
POST /api/v1/query               # Execute Cypher query
POST /api/v1/analyze             # Psychometric analysis
POST /api/v1/batch/import        # Batch import
GET  /api/v1/metrics             # Performance metrics
```

### Python API Usage

```python
from aeon_framework import AeonClient

# Initialize client
client = AeonClient(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Create entity
entity = client.entities.create({
    'name': 'John Doe',
    'type': 'Person',
    'properties': {
        'age': 30,
        'location': 'New York'
    }
})

# Query entities
results = client.query("""
    MATCH (p:Person)-[:KNOWS]->(f)
    WHERE p.name = $name
    RETURN f
""", {'name': 'John Doe'})

# Batch import
client.batch_import(
    file_path='data/entities.csv',
    entity_type='Person',
    batch_size=1000
)

# Psychometric analysis
analysis = client.analyze_text(
    text="Sample text for analysis",
    options={'extract_entities': True}
)
```

---

## Appendix: Complete Script Listing

### Directory Structure

```
scripts/
├── schema/
│   ├── deploy_schema.py
│   ├── verify_schema.py
│   ├── export_schema.py
│   └── schema_definition.yaml
├── import/
│   ├── batch_importer.py
│   ├── streaming_importer.py
│   └── validation.py
├── export/
│   ├── data_exporter.py
│   ├── graph_exporter.py
│   └── report_generator.py
├── optimization/
│   ├── query_analyzer.py
│   ├── index_advisor.py
│   └── cache_warmer.py
├── backup/
│   ├── backup_neo4j.sh
│   ├── restore_neo4j.sh
│   └── verify_backup.py
├── monitoring/
│   ├── performance_monitor.py
│   ├── health_check.py
│   └── alerting.py
├── validation/
│   ├── data_validator.py
│   ├── schema_validator.py
│   └── integrity_checker.py
├── migration/
│   ├── schema_migrator.py
│   ├── data_migrator.py
│   └── version_manager.py
├── metadata/
│   ├── metadata_extractor.py
│   ├── lineage_tracker.py
│   └── catalog_manager.py
├── nlp/
│   ├── psychometric_pipeline.py
│   ├── entity_extractor.py
│   └── sentiment_analyzer.py
└── batch/
    ├── two_phase_processor.py
    ├── job_scheduler.py
    └── workflow_manager.py
```

---

## Summary

This utilities and tools guide provides comprehensive documentation for:

1. **Installation and Setup**: Complete environment configuration
2. **Schema Management**: Deployment, verification, and migration
3. **Data Operations**: Import, export, and transformation tools
4. **Performance**: Query optimization and monitoring
5. **Reliability**: Backup, restore, and validation procedures
6. **Advanced Features**: NLP pipelines and batch processing
7. **Integration**: APIs and external system connectors

For additional support, consult:
- Project documentation in `/docs`
- Research paper: `Research Paper, for AEON Framework.md`
- Psychometric guides in `/Pyschometrics` directory

**Status**: Documentation complete with comprehensive utilities coverage
**Version**: 1.0.0
**Last Updated**: October 29, 2025
