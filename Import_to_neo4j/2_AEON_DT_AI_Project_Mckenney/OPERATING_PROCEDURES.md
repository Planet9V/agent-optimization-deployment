# OPERATING PROCEDURES: Document Ingestion System
# AEON Digital Twin Knowledge Graph

**File:** OPERATING_PROCEDURES.md
**Created:** 2025-10-29 02:00:00 UTC
**Modified:** 2025-10-29 02:00:00 UTC
**Version:** v1.0.0
**Author:** AEON Project Team
**Purpose:** Standard Operating Procedures for Document Ingestion to Neo4j Knowledge Graph
**Status:** ACTIVE

---

## TABLE OF CONTENTS

1. [Pre-Ingestion Procedures](#1-pre-ingestion-procedures)
2. [Document Ingestion Procedures](#2-document-ingestion-procedures)
3. [Quality Assurance Procedures](#3-quality-assurance-procedures)
4. [Metadata Management Procedures](#4-metadata-management-procedures)
5. [Performance Optimization Procedures](#5-performance-optimization-procedures)
6. [Troubleshooting Procedures](#6-troubleshooting-procedures)
7. [Backup and Recovery Procedures](#7-backup-and-recovery-procedures)
8. [Compliance and Audit Procedures](#8-compliance-and-audit-procedures)

---

## 1. PRE-INGESTION PROCEDURES

### 1.1 Environment Validation Checklist

**Objective:** Ensure system readiness before document processing

**Frequency:** Before each ingestion session

**☑️ VALIDATION CHECKLIST:**

```bash
# 1. Check Python environment
□ Python version 3.8+ verified
□ Virtual environment activated
□ Required packages installed (requirements.txt)

# 2. Verify Neo4j connectivity
□ Neo4j server running (check port 7687)
□ Authentication credentials valid
□ Database accessible and responsive

# 3. Validate spaCy models
□ en_core_web_sm installed
□ en_core_web_lg installed (optional, for enhanced processing)
□ Model loading test successful

# 4. Verify directory structure
□ Input directory exists and accessible
□ Output/logs directory exists
□ Backup directory available
□ Processed files tracking directory ready

# 5. Resource availability
□ Sufficient disk space (minimum 10GB free)
□ Adequate RAM (minimum 8GB available)
□ Neo4j heap size configured appropriately
```

**EXECUTION STEPS:**

**Step 1: System Validation Script**
```bash
#!/bin/bash
# File: scripts/pre_ingestion_check.sh

echo "=== Pre-Ingestion System Validation ==="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"

# Python environment check
echo -n "Python version: "
python3 --version || { echo "ERROR: Python not found"; exit 1; }

# Virtual environment check
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment: $VIRTUAL_ENV"
else
    echo "⚠ WARNING: No virtual environment detected"
fi

# Package verification
echo "Checking required packages..."
python3 -c "import spacy, neo4j, hashlib, json" 2>/dev/null && echo "✓ Core packages installed" || { echo "ERROR: Missing packages"; exit 1; }

# Neo4j connectivity
echo "Testing Neo4j connection..."
python3 -c "
from neo4j import GraphDatabase
try:
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password'))
    with driver.session() as session:
        result = session.run('RETURN 1')
    driver.close()
    print('✓ Neo4j connection successful')
except Exception as e:
    print(f'ERROR: Neo4j connection failed - {e}')
    exit(1)
"

# spaCy model check
echo "Validating spaCy models..."
python3 -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✓ spaCy model loaded')" || { echo "ERROR: spaCy model not found"; exit 1; }

# Directory structure
echo "Checking directory structure..."
for dir in input output logs backups metadata; do
    if [ -d "$dir" ]; then
        echo "✓ Directory exists: $dir"
    else
        echo "⚠ Creating directory: $dir"
        mkdir -p "$dir"
    fi
done

# Disk space check
available_space=$(df -h . | awk 'NR==2 {print $4}')
echo "Available disk space: $available_space"

echo "=== Pre-Ingestion Validation Complete ==="
```

**Step 2: Configuration Validation**
```python
# File: scripts/validate_config.py

import os
import json
import sys
from pathlib import Path

def validate_configuration():
    """Validate configuration before ingestion"""

    print("=== Configuration Validation ===")

    # Check environment variables
    required_env_vars = [
        'NEO4J_URI',
        'NEO4J_USER',
        'NEO4J_PASSWORD',
        'SPACY_MODEL'
    ]

    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"⚠ Missing: {var}")
        else:
            # Mask sensitive values
            value = os.getenv(var)
            if 'PASSWORD' in var:
                value = '*' * len(value)
            print(f"✓ Found: {var} = {value}")

    if missing_vars:
        print(f"\nERROR: Missing required environment variables: {missing_vars}")
        return False

    # Validate config file if exists
    config_path = Path('config/ingestion_config.json')
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
            print(f"✓ Configuration file loaded: {config_path}")

            # Validate config structure
            required_keys = ['batch_size', 'max_workers', 'entity_types', 'relationship_types']
            for key in required_keys:
                if key in config:
                    print(f"  ✓ {key}: {config[key]}")
                else:
                    print(f"  ⚠ Missing config key: {key}")
        except Exception as e:
            print(f"ERROR: Invalid configuration file - {e}")
            return False
    else:
        print("⚠ No configuration file found, using defaults")

    print("=== Configuration Validation Complete ===\n")
    return True

if __name__ == "__main__":
    if not validate_configuration():
        sys.exit(1)
```

**Step 3: Database Pre-flight Check**
```python
# File: scripts/database_preflight.py

from neo4j import GraphDatabase
import os
import sys

def preflight_check():
    """Comprehensive database health check"""

    print("=== Database Pre-flight Check ===")

    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'password')

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))

        with driver.session() as session:
            # Test connection
            result = session.run("RETURN 1 as test")
            assert result.single()['test'] == 1
            print("✓ Database connection established")

            # Check database version
            version_result = session.run("CALL dbms.components() YIELD versions")
            version = version_result.single()['versions'][0]
            print(f"✓ Neo4j version: {version}")

            # Count existing nodes
            count_result = session.run("MATCH (n) RETURN count(n) as count")
            node_count = count_result.single()['count']
            print(f"✓ Current node count: {node_count}")

            # Verify indexes exist
            index_result = session.run("SHOW INDEXES")
            indexes = [record['name'] for record in index_result]
            if indexes:
                print(f"✓ Indexes found: {len(indexes)}")
                for idx in indexes:
                    print(f"  - {idx}")
            else:
                print("⚠ No indexes found - performance may be degraded")

            # Check constraints
            constraint_result = session.run("SHOW CONSTRAINTS")
            constraints = [record['name'] for record in constraint_result]
            if constraints:
                print(f"✓ Constraints found: {len(constraints)}")
            else:
                print("⚠ No constraints found")

            # Test write capability
            session.run("CREATE (t:Test {timestamp: datetime()}) DELETE t")
            print("✓ Write capability verified")

        driver.close()
        print("=== Pre-flight Check Complete ===\n")
        return True

    except Exception as e:
        print(f"ERROR: Database pre-flight failed - {e}")
        return False

if __name__ == "__main__":
    if not preflight_check():
        sys.exit(1)
```

**DECISION TREE: Pre-Ingestion Validation**

```
START
  ↓
Check Python Environment
  ├─ PASS → Continue
  └─ FAIL → Install/Fix Python → Retry
           └─ Still FAIL → ESCALATE to DevOps
  ↓
Verify Neo4j Connection
  ├─ PASS → Continue
  └─ FAIL → Check Neo4j Status
           ├─ Not Running → Start Neo4j → Retry
           ├─ Auth Failed → Reset Credentials → Retry
           └─ Still FAIL → ESCALATE to Database Admin
  ↓
Validate spaCy Models
  ├─ PASS → Continue
  └─ FAIL → Download Models → Retry
           └─ Still FAIL → ESCALATE to ML Team
  ↓
Check Directory Structure
  ├─ PASS → Continue
  └─ FAIL → Create Directories → Retry
           └─ Permission Denied → ESCALATE to System Admin
  ↓
Verify Resources
  ├─ PASS → PROCEED TO INGESTION
  └─ FAIL → Free Resources → Retry
           └─ Insufficient → ESCALATE to Infrastructure Team
```

---

## 2. DOCUMENT INGESTION PROCEDURES

### 2.1 Single Document Ingestion Workflow

**Objective:** Process individual document with full validation

**When to Use:**
- Testing new document types
- Processing high-priority single documents
- Debugging ingestion issues
- Manual quality verification needed

**EXECUTION STEPS:**

**Step 1: Document Preparation**
```bash
# File: scripts/prepare_document.sh

#!/bin/bash
DOCUMENT_PATH=$1

echo "=== Document Preparation ==="
echo "Document: $DOCUMENT_PATH"

# Validate document exists
if [ ! -f "$DOCUMENT_PATH" ]; then
    echo "ERROR: Document not found"
    exit 1
fi

# Check file format
FILE_EXT="${DOCUMENT_PATH##*.}"
SUPPORTED_FORMATS=("md" "txt" "pdf" "docx")

if [[ ! " ${SUPPORTED_FORMATS[@]} " =~ " ${FILE_EXT} " ]]; then
    echo "ERROR: Unsupported format: $FILE_EXT"
    echo "Supported formats: ${SUPPORTED_FORMATS[@]}"
    exit 1
fi

# Check file size
FILE_SIZE=$(stat -f%z "$DOCUMENT_PATH" 2>/dev/null || stat -c%s "$DOCUMENT_PATH")
MAX_SIZE=$((100 * 1024 * 1024))  # 100MB

if [ $FILE_SIZE -gt $MAX_SIZE ]; then
    echo "WARNING: Large file detected ($(($FILE_SIZE / 1024 / 1024))MB)"
    echo "Consider splitting into smaller documents"
fi

# Calculate SHA256 hash
FILE_HASH=$(sha256sum "$DOCUMENT_PATH" | awk '{print $1}')
echo "Document hash: $FILE_HASH"

# Check if already processed
if grep -q "$FILE_HASH" metadata/processed_files.log 2>/dev/null; then
    echo "WARNING: Document already processed"
    read -p "Reprocess? (y/n): " REPROCESS
    if [ "$REPROCESS" != "y" ]; then
        echo "Skipping document"
        exit 0
    fi
fi

echo "✓ Document preparation complete"
```

**Step 2: Entity Extraction**
```python
# File: scripts/extract_entities.py

import spacy
import json
import sys
from pathlib import Path
from typing import Dict, List

class EntityExtractor:
    """Extract entities from document using spaCy"""

    def __init__(self, model_name='en_core_web_sm'):
        print(f"Loading spaCy model: {model_name}")
        self.nlp = spacy.load(model_name)

        # Configure entity types to extract
        self.entity_types = {
            'PERSON': 'Person',
            'ORG': 'Organization',
            'GPE': 'Location',
            'DATE': 'Date',
            'EVENT': 'Event',
            'PRODUCT': 'Product',
            'LAW': 'Law',
            'WORK_OF_ART': 'Work',
            'NORP': 'Group',
            'FAC': 'Facility'
        }

    def extract(self, text: str) -> Dict:
        """Extract entities from text"""

        print("Processing document with spaCy...")
        doc = self.nlp(text)

        entities = {
            'by_type': {},
            'by_label': [],
            'relationships': []
        }

        # Extract entities by type
        for ent in doc.ents:
            if ent.label_ in self.entity_types:
                category = self.entity_types[ent.label_]

                if category not in entities['by_type']:
                    entities['by_type'][category] = []

                entity_data = {
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                }

                # Avoid duplicates
                if entity_data not in entities['by_type'][category]:
                    entities['by_type'][category].append(entity_data)
                    entities['by_label'].append(entity_data)

        # Extract relationships (simple co-occurrence based)
        sentences = list(doc.sents)
        for sent in sentences:
            sent_entities = [ent for ent in sent.ents if ent.label_ in self.entity_types]

            # Create relationships between entities in same sentence
            for i, ent1 in enumerate(sent_entities):
                for ent2 in sent_entities[i+1:]:
                    relationship = {
                        'source': ent1.text,
                        'source_type': self.entity_types[ent1.label_],
                        'target': ent2.text,
                        'target_type': self.entity_types[ent2.label_],
                        'context': sent.text,
                        'relation_type': 'CO_OCCURS_WITH'
                    }
                    entities['relationships'].append(relationship)

        # Statistics
        print(f"✓ Extracted {len(entities['by_label'])} entities")
        print(f"✓ Found {len(entities['relationships'])} relationships")
        for ent_type, ents in entities['by_type'].items():
            print(f"  - {ent_type}: {len(ents)}")

        return entities

def main(document_path: str):
    """Main extraction workflow"""

    print(f"=== Entity Extraction: {document_path} ===")

    # Read document
    with open(document_path, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"Document length: {len(text)} characters")

    # Extract entities
    extractor = EntityExtractor()
    entities = extractor.extract(text)

    # Save results
    output_path = Path(document_path).stem + '_entities.json'
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / output_path
    with open(output_file, 'w') as f:
        json.dump(entities, f, indent=2)

    print(f"✓ Results saved to: {output_file}")
    print("=== Extraction Complete ===\n")

    return entities

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_entities.py <document_path>")
        sys.exit(1)

    main(sys.argv[1])
```

**Step 3: Neo4j Ingestion**
```python
# File: scripts/ingest_to_neo4j.py

from neo4j import GraphDatabase
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import hashlib

class Neo4jIngester:
    """Ingest entities and relationships into Neo4j"""

    def __init__(self):
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = os.getenv('NEO4J_USER', 'neo4j')
        self.password = os.getenv('NEO4J_PASSWORD', 'password')
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def create_document_node(self, tx, doc_metadata):
        """Create document node with metadata"""
        query = """
        MERGE (d:Document {sha256: $sha256})
        SET d.filename = $filename,
            d.processed_at = datetime($processed_at),
            d.file_size = $file_size,
            d.entity_count = $entity_count,
            d.relationship_count = $relationship_count
        RETURN d
        """
        result = tx.run(query, **doc_metadata)
        return result.single()[0]

    def create_entity_node(self, tx, entity, doc_sha256):
        """Create entity node and link to document"""

        # Determine node label
        label = entity.get('label', 'Entity')
        category = self._get_category(label)

        query = f"""
        MERGE (e:{category} {{name: $name}})
        SET e.label = $label,
            e.first_seen = COALESCE(e.first_seen, datetime($timestamp)),
            e.last_seen = datetime($timestamp),
            e.occurrence_count = COALESCE(e.occurrence_count, 0) + 1

        WITH e
        MATCH (d:Document {{sha256: $doc_sha256}})
        MERGE (e)-[r:MENTIONED_IN]->(d)
        SET r.start_char = $start,
            r.end_char = $end

        RETURN e
        """

        params = {
            'name': entity['text'],
            'label': entity['label'],
            'start': entity['start'],
            'end': entity['end'],
            'doc_sha256': doc_sha256,
            'timestamp': datetime.now().isoformat()
        }

        result = tx.run(query, **params)
        return result.single()[0]

    def create_relationship(self, tx, relationship, doc_sha256):
        """Create relationship between entities"""

        source_category = relationship['source_type']
        target_category = relationship['target_type']
        relation_type = relationship.get('relation_type', 'RELATED_TO')

        query = f"""
        MATCH (source:{source_category} {{name: $source_name}})
        MATCH (target:{target_category} {{name: $target_name}})
        MATCH (d:Document {{sha256: $doc_sha256}})

        MERGE (source)-[r:{relation_type}]->(target)
        SET r.context = $context,
            r.last_updated = datetime($timestamp),
            r.strength = COALESCE(r.strength, 0) + 1

        MERGE (r)-[:FOUND_IN]->(d)

        RETURN r
        """

        params = {
            'source_name': relationship['source'],
            'target_name': relationship['target'],
            'doc_sha256': doc_sha256,
            'context': relationship.get('context', ''),
            'timestamp': datetime.now().isoformat()
        }

        result = tx.run(query, **params)
        return result.single()[0] if result.single() else None

    def _get_category(self, label):
        """Map spaCy label to Neo4j node category"""
        mapping = {
            'PERSON': 'Person',
            'ORG': 'Organization',
            'GPE': 'Location',
            'DATE': 'Date',
            'EVENT': 'Event',
            'PRODUCT': 'Product',
            'LAW': 'Law',
            'WORK_OF_ART': 'Work',
            'NORP': 'Group',
            'FAC': 'Facility'
        }
        return mapping.get(label, 'Entity')

    def ingest(self, document_path, entities_data):
        """Main ingestion workflow"""

        print(f"=== Ingesting to Neo4j: {document_path} ===")

        # Calculate document hash
        with open(document_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Prepare document metadata
        doc_metadata = {
            'sha256': file_hash,
            'filename': Path(document_path).name,
            'processed_at': datetime.now().isoformat(),
            'file_size': os.path.getsize(document_path),
            'entity_count': len(entities_data['by_label']),
            'relationship_count': len(entities_data['relationships'])
        }

        with self.driver.session() as session:
            # Create document node
            print("Creating document node...")
            session.execute_write(self.create_document_node, doc_metadata)
            print("✓ Document node created")

            # Create entity nodes
            print(f"Creating {doc_metadata['entity_count']} entity nodes...")
            for entity in entities_data['by_label']:
                session.execute_write(self.create_entity_node, entity, file_hash)
            print("✓ Entity nodes created")

            # Create relationships
            print(f"Creating {doc_metadata['relationship_count']} relationships...")
            for relationship in entities_data['relationships']:
                session.execute_write(self.create_relationship, relationship, file_hash)
            print("✓ Relationships created")

        print("=== Ingestion Complete ===\n")
        return file_hash

def main(document_path, entities_file):
    """Main ingestion workflow"""

    # Load entities data
    with open(entities_file, 'r') as f:
        entities_data = json.load(f)

    # Ingest to Neo4j
    ingester = Neo4jIngester()
    try:
        file_hash = ingester.ingest(document_path, entities_data)

        # Log successful processing
        with open('metadata/processed_files.log', 'a') as f:
            f.write(f"{file_hash}\t{document_path}\t{datetime.now().isoformat()}\n")

        print(f"✓ Document hash logged: {file_hash}")

    finally:
        ingester.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ingest_to_neo4j.py <document_path> <entities_json>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
```

**SINGLE DOCUMENT INGESTION CHECKLIST:**

```
□ Step 1: Document Preparation
  □ File exists and accessible
  □ Format supported
  □ Size within limits
  □ Hash calculated
  □ Duplicate check performed

□ Step 2: Entity Extraction
  □ spaCy model loaded
  □ Text parsed successfully
  □ Entities extracted
  □ Relationships identified
  □ Results saved to JSON

□ Step 3: Neo4j Ingestion
  □ Database connection established
  □ Document node created
  □ All entity nodes created
  □ All relationships created
  □ Metadata logged

□ Step 4: Validation
  □ Query document in Neo4j
  □ Verify entity count
  □ Verify relationship count
  □ Check for errors in logs

□ Step 5: Post-Processing
  □ Update processed files log
  □ Generate ingestion report
  □ Archive source document (if configured)
```

---

### 2.2 Batch Ingestion Workflow

**Objective:** Process multiple documents efficiently with parallel processing

**When to Use:**
- Processing document collections
- Regular scheduled ingestion
- Large-scale knowledge graph construction

**BATCH PROCESSING STRATEGY:**

**Configuration:**
```json
{
  "batch_processing": {
    "batch_size": 10,
    "max_workers": 4,
    "chunk_size": 5,
    "timeout_per_document": 300,
    "retry_attempts": 3,
    "error_threshold": 0.1,
    "progress_checkpoint_interval": 10
  },
  "quality_gates": {
    "min_entities_per_doc": 1,
    "max_entities_per_doc": 1000,
    "min_relationships_per_doc": 0,
    "require_document_validation": true
  }
}
```

**Step 1: Batch Preparation**
```python
# File: scripts/batch_prepare.py

import os
import json
from pathlib import Path
from typing import List, Dict
import hashlib

class BatchPreparer:
    """Prepare documents for batch processing"""

    def __init__(self, input_dir: str, config_path: str = 'config/ingestion_config.json'):
        self.input_dir = Path(input_dir)

        with open(config_path) as f:
            self.config = json.load(f)

        self.batch_size = self.config['batch_processing']['batch_size']
        self.supported_formats = ['.md', '.txt', '.pdf', '.docx']

    def scan_documents(self) -> List[Path]:
        """Scan input directory for documents"""

        print(f"=== Scanning Directory: {self.input_dir} ===")

        documents = []
        for ext in self.supported_formats:
            documents.extend(self.input_dir.rglob(f'*{ext}'))

        print(f"✓ Found {len(documents)} documents")
        return documents

    def filter_processed(self, documents: List[Path]) -> List[Path]:
        """Filter out already processed documents"""

        # Load processed files log
        processed_hashes = set()
        log_file = Path('metadata/processed_files.log')

        if log_file.exists():
            with open(log_file) as f:
                for line in f:
                    if line.strip():
                        hash_value = line.split('\t')[0]
                        processed_hashes.add(hash_value)

        print(f"Found {len(processed_hashes)} previously processed documents")

        # Filter documents
        unprocessed = []
        for doc in documents:
            with open(doc, 'rb') as f:
                doc_hash = hashlib.sha256(f.read()).hexdigest()

            if doc_hash not in processed_hashes:
                unprocessed.append(doc)

        print(f"✓ {len(unprocessed)} documents to process")
        print(f"✓ {len(documents) - len(unprocessed)} documents already processed (skipped)")

        return unprocessed

    def create_batches(self, documents: List[Path]) -> List[List[Path]]:
        """Split documents into batches"""

        batches = []
        for i in range(0, len(documents), self.batch_size):
            batch = documents[i:i + self.batch_size]
            batches.append(batch)

        print(f"✓ Created {len(batches)} batches (size: {self.batch_size})")
        return batches

    def prepare(self) -> Dict:
        """Complete batch preparation workflow"""

        documents = self.scan_documents()
        unprocessed = self.filter_processed(documents)
        batches = self.create_batches(unprocessed)

        manifest = {
            'total_documents': len(documents),
            'already_processed': len(documents) - len(unprocessed),
            'to_process': len(unprocessed),
            'batch_count': len(batches),
            'batch_size': self.batch_size,
            'batches': [[str(doc) for doc in batch] for batch in batches]
        }

        # Save manifest
        manifest_file = Path('metadata/batch_manifest.json')
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"✓ Batch manifest saved: {manifest_file}")
        print("=== Batch Preparation Complete ===\n")

        return manifest

def main(input_dir: str):
    preparer = BatchPreparer(input_dir)
    manifest = preparer.prepare()

    print("\n📊 BATCH STATISTICS:")
    print(f"Total documents found: {manifest['total_documents']}")
    print(f"Already processed: {manifest['already_processed']}")
    print(f"To process: {manifest['to_process']}")
    print(f"Batches: {manifest['batch_count']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python batch_prepare.py <input_directory>")
        sys.exit(1)

    main(sys.argv[1])
```

**Step 2: Parallel Batch Processing**
```python
# File: scripts/batch_process.py

import json
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict
import time
from datetime import datetime

# Import extraction and ingestion modules
from extract_entities import EntityExtractor
from ingest_to_neo4j import Neo4jIngester

class BatchProcessor:
    """Process document batches with parallel execution"""

    def __init__(self, manifest_path: str = 'metadata/batch_manifest.json'):
        with open(manifest_path) as f:
            self.manifest = json.load(f)

        with open('config/ingestion_config.json') as f:
            self.config = json.load(f)

        self.max_workers = self.config['batch_processing']['max_workers']
        self.timeout = self.config['batch_processing']['timeout_per_document']

        self.results = {
            'successful': [],
            'failed': [],
            'skipped': []
        }

    def process_document(self, doc_path: str) -> Dict:
        """Process single document (worker function)"""

        start_time = time.time()
        result = {
            'document': doc_path,
            'status': 'unknown',
            'error': None,
            'processing_time': 0,
            'entity_count': 0,
            'relationship_count': 0
        }

        try:
            print(f"Processing: {doc_path}")

            # Read document
            with open(doc_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # Extract entities
            extractor = EntityExtractor()
            entities = extractor.extract(text)

            result['entity_count'] = len(entities['by_label'])
            result['relationship_count'] = len(entities['relationships'])

            # Ingest to Neo4j
            ingester = Neo4jIngester()
            try:
                file_hash = ingester.ingest(doc_path, entities)
                result['status'] = 'success'
                result['hash'] = file_hash
            finally:
                ingester.close()

        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            print(f"ERROR processing {doc_path}: {e}")

        finally:
            result['processing_time'] = time.time() - start_time

        return result

    def process_batch(self, batch: List[str]) -> List[Dict]:
        """Process batch with parallel workers"""

        print(f"\n=== Processing Batch ({len(batch)} documents) ===")
        batch_results = []

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all documents
            futures = {
                executor.submit(self.process_document, doc): doc
                for doc in batch
            }

            # Collect results as they complete
            for future in as_completed(futures, timeout=self.timeout * len(batch)):
                doc = futures[future]
                try:
                    result = future.result()
                    batch_results.append(result)

                    if result['status'] == 'success':
                        self.results['successful'].append(result)
                        print(f"✓ {doc} - {result['entity_count']} entities, {result['relationship_count']} relationships")
                    else:
                        self.results['failed'].append(result)
                        print(f"✗ {doc} - {result['error']}")

                except Exception as e:
                    error_result = {
                        'document': doc,
                        'status': 'failed',
                        'error': str(e),
                        'processing_time': 0
                    }
                    batch_results.append(error_result)
                    self.results['failed'].append(error_result)
                    print(f"✗ {doc} - Worker exception: {e}")

        return batch_results

    def run(self):
        """Run complete batch processing workflow"""

        print("=== BATCH PROCESSING START ===")
        print(f"Total batches: {len(self.manifest['batches'])}")
        print(f"Max workers: {self.max_workers}")
        print(f"Timeout per document: {self.timeout}s\n")

        start_time = time.time()

        # Process each batch
        for i, batch in enumerate(self.manifest['batches'], 1):
            print(f"\n{'='*60}")
            print(f"Batch {i}/{len(self.manifest['batches'])}")
            print(f"{'='*60}")

            batch_results = self.process_batch(batch)

            # Save checkpoint
            self._save_checkpoint(i, batch_results)

            # Display progress
            self._display_progress()

        # Generate final report
        total_time = time.time() - start_time
        self._generate_report(total_time)

    def _save_checkpoint(self, batch_num: int, batch_results: List[Dict]):
        """Save processing checkpoint"""

        checkpoint = {
            'batch_number': batch_num,
            'timestamp': datetime.now().isoformat(),
            'results': batch_results
        }

        checkpoint_file = Path(f'metadata/checkpoint_batch_{batch_num}.json')
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    def _display_progress(self):
        """Display current progress statistics"""

        total = len(self.results['successful']) + len(self.results['failed']) + len(self.results['skipped'])
        success_rate = (len(self.results['successful']) / total * 100) if total > 0 else 0

        print(f"\n📊 PROGRESS STATISTICS:")
        print(f"Processed: {total}/{self.manifest['to_process']}")
        print(f"Successful: {len(self.results['successful'])} ({success_rate:.1f}%)")
        print(f"Failed: {len(self.results['failed'])}")
        print(f"Skipped: {len(self.results['skipped'])}")

    def _generate_report(self, total_time: float):
        """Generate final batch processing report"""

        report = {
            'start_time': datetime.now().isoformat(),
            'total_time_seconds': total_time,
            'manifest': self.manifest,
            'results': self.results,
            'statistics': {
                'total_processed': len(self.results['successful']) + len(self.results['failed']),
                'successful': len(self.results['successful']),
                'failed': len(self.results['failed']),
                'skipped': len(self.results['skipped']),
                'success_rate': (len(self.results['successful']) /
                                (len(self.results['successful']) + len(self.results['failed'])) * 100)
                                if (len(self.results['successful']) + len(self.results['failed'])) > 0 else 0,
                'avg_processing_time': sum(r['processing_time'] for r in self.results['successful']) /
                                      len(self.results['successful']) if self.results['successful'] else 0
            }
        }

        # Save report
        report_file = Path(f'logs/batch_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n{'='*60}")
        print("BATCH PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"Total time: {total_time:.2f}s")
        print(f"Documents processed: {report['statistics']['total_processed']}")
        print(f"Success rate: {report['statistics']['success_rate']:.1f}%")
        print(f"Avg processing time: {report['statistics']['avg_processing_time']:.2f}s")
        print(f"Report saved: {report_file}")

def main():
    processor = BatchProcessor()
    processor.run()

if __name__ == "__main__":
    main()
```

**BATCH INGESTION CHECKLIST:**

```
□ Pre-Batch Setup
  □ Batch manifest created
  □ Configuration validated
  □ Worker pool configured
  □ Error thresholds set

□ Batch Execution
  □ Documents scanned
  □ Duplicates filtered
  □ Batches created
  □ Parallel processing initiated
  □ Progress monitored

□ Quality Gates
  □ Entity count validation
  □ Relationship validation
  □ Error rate monitoring
  □ Checkpoint saves

□ Post-Batch Processing
  □ Results aggregated
  □ Report generated
  □ Logs archived
  □ Errors documented
  □ Reprocessing queue created (if needed)
```

---

## 3. QUALITY ASSURANCE PROCEDURES

### 3.1 Entity Extraction Validation

**Objective:** Ensure entity extraction accuracy and completeness

**VALIDATION SCRIPT:**
```python
# File: scripts/validate_entities.py

import json
from pathlib import Path
from typing import Dict, List
import spacy

class EntityValidator:
    """Validate entity extraction quality"""

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

        self.quality_thresholds = {
            'min_entities_per_doc': 1,
            'max_entities_per_doc': 1000,
            'min_unique_ratio': 0.3,  # Minimum ratio of unique entities
            'max_duplicate_ratio': 0.7,  # Maximum ratio of duplicate entities
            'min_relationship_ratio': 0.1  # Min relationships per entity
        }

    def validate_entity_count(self, entities: Dict) -> Dict:
        """Validate entity count is within acceptable range"""

        entity_count = len(entities['by_label'])

        result = {
            'check': 'entity_count',
            'passed': True,
            'details': {}
        }

        if entity_count < self.quality_thresholds['min_entities_per_doc']:
            result['passed'] = False
            result['details']['error'] = f"Too few entities: {entity_count}"
            result['details']['severity'] = 'warning'

        if entity_count > self.quality_thresholds['max_entities_per_doc']:
            result['passed'] = False
            result['details']['error'] = f"Too many entities: {entity_count}"
            result['details']['severity'] = 'warning'

        result['details']['entity_count'] = entity_count
        return result

    def validate_entity_diversity(self, entities: Dict) -> Dict:
        """Validate diversity of extracted entities"""

        result = {
            'check': 'entity_diversity',
            'passed': True,
            'details': {}
        }

        # Check entity types represented
        type_distribution = {}
        for ent in entities['by_label']:
            label = ent['label']
            type_distribution[label] = type_distribution.get(label, 0) + 1

        result['details']['type_distribution'] = type_distribution
        result['details']['unique_types'] = len(type_distribution)

        # Check for over-representation of single type
        if type_distribution:
            max_type = max(type_distribution.values())
            total = sum(type_distribution.values())
            max_ratio = max_type / total if total > 0 else 0

            if max_ratio > 0.8:
                result['passed'] = False
                result['details']['warning'] = f"Single type dominates: {max_ratio:.1%}"

        return result

    def validate_relationships(self, entities: Dict) -> Dict:
        """Validate relationship extraction quality"""

        result = {
            'check': 'relationships',
            'passed': True,
            'details': {}
        }

        entity_count = len(entities['by_label'])
        relationship_count = len(entities['relationships'])

        if entity_count > 0:
            ratio = relationship_count / entity_count
            result['details']['relationship_entity_ratio'] = ratio

            if ratio < self.quality_thresholds['min_relationship_ratio']:
                result['passed'] = False
                result['details']['warning'] = f"Low relationship ratio: {ratio:.2f}"

        result['details']['relationship_count'] = relationship_count
        return result

    def validate_all(self, entities_file: str) -> Dict:
        """Run all validation checks"""

        print(f"=== Validating: {entities_file} ===")

        with open(entities_file) as f:
            entities = json.load(f)

        results = {
            'file': entities_file,
            'validations': [],
            'overall_passed': True
        }

        # Run validations
        validations = [
            self.validate_entity_count(entities),
            self.validate_entity_diversity(entities),
            self.validate_relationships(entities)
        ]

        for validation in validations:
            results['validations'].append(validation)
            if not validation['passed']:
                results['overall_passed'] = False

            # Display result
            status = "✓" if validation['passed'] else "✗"
            print(f"{status} {validation['check']}: {validation['details']}")

        print(f"\nOverall: {'PASS' if results['overall_passed'] else 'FAIL'}")
        print("=== Validation Complete ===\n")

        return results

def main(entities_file: str):
    validator = EntityValidator()
    results = validator.validate_all(entities_file)

    # Save validation report
    report_file = Path(entities_file).stem + '_validation.json'
    report_path = Path('logs') / report_file

    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Validation report saved: {report_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python validate_entities.py <entities_json>")
        sys.exit(1)

    main(sys.argv[1])
```

### 3.2 Graph Quality Validation

**VALIDATION QUERIES:**
```cypher
// File: scripts/graph_validation_queries.cypher

// 1. Check for orphaned nodes (no relationships)
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n) as type, count(n) as orphan_count
ORDER BY orphan_count DESC;

// 2. Validate relationship integrity
MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(r) as count
ORDER BY count DESC;

// 3. Check for duplicate entities
MATCH (n)
WITH labels(n)[0] as type, n.name as name, collect(n) as nodes
WHERE size(nodes) > 1
RETURN type, name, size(nodes) as duplicate_count
ORDER BY duplicate_count DESC
LIMIT 20;

// 4. Validate document linkages
MATCH (d:Document)
OPTIONAL MATCH (e)-[:MENTIONED_IN]->(d)
RETURN d.filename, count(e) as entity_count
ORDER BY entity_count DESC
LIMIT 20;

// 5. Check entity occurrence counts
MATCH (e)
WHERE e.occurrence_count IS NOT NULL
RETURN labels(e)[0] as type,
       avg(e.occurrence_count) as avg_occurrences,
       max(e.occurrence_count) as max_occurrences
ORDER BY avg_occurrences DESC;

// 6. Validate relationship contexts
MATCH ()-[r]->()
WHERE r.context IS NULL OR r.context = ''
RETURN type(r) as relationship_type, count(r) as missing_context_count
ORDER BY missing_context_count DESC;

// 7. Check temporal consistency
MATCH (d:Document)
WHERE d.processed_at IS NOT NULL
RETURN date(d.processed_at) as date, count(d) as documents_processed
ORDER BY date DESC
LIMIT 30;
```

**VALIDATION EXECUTION SCRIPT:**
```python
# File: scripts/run_graph_validation.py

from neo4j import GraphDatabase
import os
from datetime import datetime
import json

class GraphValidator:
    """Validate Neo4j graph quality"""

    def __init__(self):
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = os.getenv('NEO4J_USER', 'neo4j')
        self.password = os.getenv('NEO4J_PASSWORD', 'password')
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def run_validation_query(self, query: str, description: str):
        """Execute validation query and return results"""

        print(f"\n{description}")
        print("-" * 60)

        with self.driver.session() as session:
            result = session.run(query)
            records = [dict(record) for record in result]

            if records:
                for record in records[:10]:  # Show first 10
                    print(record)

                if len(records) > 10:
                    print(f"... and {len(records) - 10} more")
            else:
                print("No issues found")

        return records

    def validate_all(self):
        """Run all graph validations"""

        print("=== GRAPH QUALITY VALIDATION ===")
        print(f"Timestamp: {datetime.now().isoformat()}\n")

        validations = [
            ("MATCH (n) WHERE NOT (n)--() RETURN labels(n) as type, count(n) as orphan_count ORDER BY orphan_count DESC",
             "1. Checking for orphaned nodes..."),

            ("MATCH ()-[r]->() RETURN type(r) as relationship_type, count(r) as count ORDER BY count DESC",
             "2. Validating relationship distribution..."),

            ("MATCH (n) WITH labels(n)[0] as type, n.name as name, collect(n) as nodes WHERE size(nodes) > 1 RETURN type, name, size(nodes) as duplicate_count ORDER BY duplicate_count DESC LIMIT 20",
             "3. Checking for duplicate entities..."),

            ("MATCH (d:Document) OPTIONAL MATCH (e)-[:MENTIONED_IN]->(d) RETURN d.filename, count(e) as entity_count ORDER BY entity_count DESC LIMIT 20",
             "4. Validating document linkages..."),

            ("MATCH ()-[r]->() WHERE r.context IS NULL OR r.context = '' RETURN type(r) as relationship_type, count(r) as missing_context_count ORDER BY missing_context_count DESC",
             "5. Checking relationship context completeness...")
        ]

        results = {}
        for query, description in validations:
            records = self.run_validation_query(query, description)
            results[description] = records

        # Save validation report
        report = {
            'timestamp': datetime.now().isoformat(),
            'validations': results
        }

        report_file = f'logs/graph_validation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n=== VALIDATION COMPLETE ===")
        print(f"Report saved: {report_file}")

        return results

def main():
    validator = GraphValidator()
    try:
        validator.validate_all()
    finally:
        validator.close()

if __name__ == "__main__":
    main()
```

**QUALITY ASSURANCE CHECKLIST:**

```
□ Entity Extraction Quality
  □ Entity count within thresholds
  □ Entity type diversity acceptable
  □ Relationship extraction ratio adequate
  □ No excessive duplicates
  □ Context preservation verified

□ Graph Integrity
  □ No orphaned nodes
  □ Relationship distribution normal
  □ Document linkages complete
  □ Temporal consistency maintained
  □ No missing critical attributes

□ Data Quality
  □ Entity names normalized
  □ Relationship contexts populated
  □ Metadata complete
  □ Hash integrity verified
  □ No data corruption detected

□ Performance Quality
  □ Query response times acceptable
  □ Index utilization optimal
  □ Memory usage within limits
  □ Transaction completion successful
```

---

## 4. METADATA MANAGEMENT PROCEDURES

### 4.1 Tracking Processed Documents

**METADATA SCHEMA:**
```json
{
  "processed_files_log": {
    "format": "TSV",
    "fields": [
      "sha256_hash",
      "file_path",
      "processed_timestamp",
      "entity_count",
      "relationship_count",
      "processing_time_seconds",
      "status",
      "error_message"
    ]
  }
}
```

**TRACKING SCRIPT:**
```python
# File: scripts/metadata_tracker.py

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import csv

class MetadataTracker:
    """Track document processing metadata"""

    def __init__(self, metadata_dir: str = 'metadata'):
        self.metadata_dir = Path(metadata_dir)
        self.metadata_dir.mkdir(exist_ok=True)

        self.log_file = self.metadata_dir / 'processed_files.log'
        self.index_file = self.metadata_dir / 'document_index.json'

        # Initialize index
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """Load document index"""
        if self.index_file.exists():
            with open(self.index_file) as f:
                return json.load(f)
        return {}

    def _save_index(self):
        """Save document index"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def calculate_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def is_processed(self, file_path: str) -> bool:
        """Check if document already processed"""
        file_hash = self.calculate_hash(file_path)
        return file_hash in self.index

    def get_metadata(self, file_path: str) -> Optional[Dict]:
        """Retrieve metadata for document"""
        file_hash = self.calculate_hash(file_path)
        return self.index.get(file_hash)

    def log_processing(self, file_path: str, result: Dict):
        """Log document processing result"""

        file_hash = self.calculate_hash(file_path)
        timestamp = datetime.now().isoformat()

        # Update index
        self.index[file_hash] = {
            'file_path': str(file_path),
            'hash': file_hash,
            'processed_at': timestamp,
            'entity_count': result.get('entity_count', 0),
            'relationship_count': result.get('relationship_count', 0),
            'processing_time': result.get('processing_time', 0),
            'status': result.get('status', 'unknown'),
            'error': result.get('error')
        }

        self._save_index()

        # Append to log file
        with open(self.log_file, 'a') as f:
            f.write(f"{file_hash}\t{file_path}\t{timestamp}\t")
            f.write(f"{result.get('entity_count', 0)}\t{result.get('relationship_count', 0)}\t")
            f.write(f"{result.get('processing_time', 0):.2f}\t{result.get('status', 'unknown')}\t")
            f.write(f"{result.get('error', '')}\n")

        print(f"✓ Metadata logged for: {file_path}")

    def get_statistics(self) -> Dict:
        """Calculate processing statistics"""

        total = len(self.index)
        successful = sum(1 for v in self.index.values() if v['status'] == 'success')
        failed = sum(1 for v in self.index.values() if v['status'] == 'failed')

        total_entities = sum(v['entity_count'] for v in self.index.values())
        total_relationships = sum(v['relationship_count'] for v in self.index.values())
        total_time = sum(v['processing_time'] for v in self.index.values())

        return {
            'total_documents': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'total_entities': total_entities,
            'total_relationships': total_relationships,
            'avg_entities_per_doc': total_entities / total if total > 0 else 0,
            'avg_relationships_per_doc': total_relationships / total if total > 0 else 0,
            'total_processing_time': total_time,
            'avg_processing_time': total_time / total if total > 0 else 0
        }

    def export_report(self, output_file: str = None):
        """Export processing report"""

        if output_file is None:
            output_file = f"logs/metadata_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow([
                'Hash', 'File Path', 'Processed At', 'Entity Count',
                'Relationship Count', 'Processing Time', 'Status', 'Error'
            ])

            # Write data
            for hash_val, data in self.index.items():
                writer.writerow([
                    hash_val,
                    data['file_path'],
                    data['processed_at'],
                    data['entity_count'],
                    data['relationship_count'],
                    f"{data['processing_time']:.2f}",
                    data['status'],
                    data.get('error', '')
                ])

        print(f"✓ Report exported: {output_file}")
        return output_file

def main():
    """Display current metadata statistics"""

    tracker = MetadataTracker()
    stats = tracker.get_statistics()

    print("=== METADATA STATISTICS ===")
    print(f"Total documents: {stats['total_documents']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")
    print(f"\nTotal entities: {stats['total_entities']}")
    print(f"Total relationships: {stats['total_relationships']}")
    print(f"Avg entities/doc: {stats['avg_entities_per_doc']:.1f}")
    print(f"Avg relationships/doc: {stats['avg_relationships_per_doc']:.1f}")
    print(f"\nTotal processing time: {stats['total_processing_time']:.2f}s")
    print(f"Avg processing time: {stats['avg_processing_time']:.2f}s/doc")

    # Export report
    report_file = tracker.export_report()
    print(f"\nFull report: {report_file}")

if __name__ == "__main__":
    main()
```

### 4.2 Reprocessing Failed Documents

**REPROCESSING WORKFLOW:**
```python
# File: scripts/reprocess_failed.py

from metadata_tracker import MetadataTracker
from pathlib import Path
import json

class FailedDocumentReprocessor:
    """Reprocess failed documents"""

    def __init__(self):
        self.tracker = MetadataTracker()

    def identify_failed(self):
        """Identify all failed documents"""

        failed = []
        for hash_val, data in self.tracker.index.items():
            if data['status'] == 'failed':
                failed.append(data)

        return failed

    def create_reprocessing_queue(self):
        """Create queue of documents to reprocess"""

        failed = self.identify_failed()

        print(f"=== Failed Document Analysis ===")
        print(f"Total failed documents: {len(failed)}")

        # Categorize by error type
        error_categories = {}
        for doc in failed:
            error = doc.get('error', 'Unknown')
            if error not in error_categories:
                error_categories[error] = []
            error_categories[error].append(doc['file_path'])

        print("\nError categories:")
        for error, files in error_categories.items():
            print(f"  {error}: {len(files)} documents")

        # Save reprocessing queue
        queue_file = 'metadata/reprocessing_queue.json'
        with open(queue_file, 'w') as f:
            json.dump({
                'total': len(failed),
                'by_error': error_categories,
                'documents': failed
            }, f, indent=2)

        print(f"\n✓ Reprocessing queue saved: {queue_file}")
        return failed

    def reprocess_documents(self, retry_count: int = 3):
        """Reprocess failed documents with retry logic"""

        failed = self.create_reprocessing_queue()

        if not failed:
            print("No failed documents to reprocess")
            return

        print(f"\n=== Starting Reprocessing ({len(failed)} documents) ===")

        # Import processing functions
        from extract_entities import EntityExtractor
        from ingest_to_neo4j import Neo4jIngester

        results = {
            'success': [],
            'still_failed': []
        }

        for doc_data in failed:
            file_path = doc_data['file_path']
            print(f"\nReprocessing: {file_path}")

            success = False
            last_error = None

            # Retry logic
            for attempt in range(1, retry_count + 1):
                try:
                    print(f"  Attempt {attempt}/{retry_count}")

                    # Read document
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()

                    # Extract entities
                    extractor = EntityExtractor()
                    entities = extractor.extract(text)

                    # Ingest to Neo4j
                    ingester = Neo4jIngester()
                    try:
                        file_hash = ingester.ingest(file_path, entities)

                        # Log success
                        self.tracker.log_processing(file_path, {
                            'status': 'success',
                            'entity_count': len(entities['by_label']),
                            'relationship_count': len(entities['relationships']),
                            'processing_time': 0
                        })

                        results['success'].append(file_path)
                        success = True
                        print(f"  ✓ Reprocessing successful")
                        break

                    finally:
                        ingester.close()

                except Exception as e:
                    last_error = str(e)
                    print(f"  ✗ Attempt {attempt} failed: {e}")

                    if attempt < retry_count:
                        print(f"  Retrying...")

            if not success:
                results['still_failed'].append({
                    'file_path': file_path,
                    'error': last_error
                })
                print(f"  ✗ All attempts failed")

        # Generate report
        print(f"\n=== Reprocessing Complete ===")
        print(f"Successfully reprocessed: {len(results['success'])}")
        print(f"Still failed: {len(results['still_failed'])}")

        # Save report
        report_file = f"logs/reprocessing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Report saved: {report_file}")

        return results

def main():
    reprocessor = FailedDocumentReprocessor()
    reprocessor.reprocess_documents()

if __name__ == "__main__":
    from datetime import datetime
    main()
```

---

## 5. PERFORMANCE OPTIMIZATION PROCEDURES

### 5.1 Batch Size Tuning

**OBJECTIVE:** Determine optimal batch size for your hardware and data

**BENCHMARKING SCRIPT:**
```python
# File: scripts/benchmark_batch_sizes.py

import time
import json
from pathlib import Path
from typing import List, Dict
import matplotlib.pyplot as plt

class BatchSizeBenchmark:
    """Benchmark different batch sizes"""

    def __init__(self, sample_documents: List[str]):
        self.sample_documents = sample_documents
        self.results = []

    def benchmark_batch_size(self, batch_size: int, max_workers: int) -> Dict:
        """Benchmark specific batch size configuration"""

        print(f"\n=== Benchmarking: batch_size={batch_size}, max_workers={max_workers} ===")

        # Simulate batch processing
        from batch_process import BatchProcessor

        # Temporarily modify config
        config_path = 'config/ingestion_config.json'
        with open(config_path) as f:
            config = json.load(f)

        original_batch_size = config['batch_processing']['batch_size']
        original_max_workers = config['batch_processing']['max_workers']

        config['batch_processing']['batch_size'] = batch_size
        config['batch_processing']['max_workers'] = max_workers

        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        # Run benchmark
        start_time = time.time()

        try:
            processor = BatchProcessor()
            # Process limited sample
            sample_batch = self.sample_documents[:batch_size * 2]
            batch_results = processor.process_batch(sample_batch)

            elapsed_time = time.time() - start_time

            # Calculate metrics
            throughput = len(sample_batch) / elapsed_time if elapsed_time > 0 else 0
            avg_time_per_doc = elapsed_time / len(sample_batch) if sample_batch else 0

            result = {
                'batch_size': batch_size,
                'max_workers': max_workers,
                'total_time': elapsed_time,
                'documents_processed': len(sample_batch),
                'throughput': throughput,
                'avg_time_per_doc': avg_time_per_doc
            }

            print(f"✓ Time: {elapsed_time:.2f}s")
            print(f"✓ Throughput: {throughput:.2f} docs/s")
            print(f"✓ Avg per doc: {avg_time_per_doc:.2f}s")

            self.results.append(result)
            return result

        finally:
            # Restore original config
            config['batch_processing']['batch_size'] = original_batch_size
            config['batch_processing']['max_workers'] = original_max_workers

            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)

    def run_benchmarks(self):
        """Run comprehensive benchmarks"""

        print("=== BATCH SIZE BENCHMARKING ===")

        # Test different configurations
        configurations = [
            (5, 2),
            (10, 2),
            (10, 4),
            (20, 4),
            (20, 8),
            (50, 8)
        ]

        for batch_size, max_workers in configurations:
            self.benchmark_batch_size(batch_size, max_workers)

        # Analyze results
        self.analyze_results()

    def analyze_results(self):
        """Analyze benchmark results and recommend configuration"""

        print("\n=== BENCHMARK ANALYSIS ===")

        # Find optimal configuration
        optimal = max(self.results, key=lambda x: x['throughput'])

        print(f"\n🏆 OPTIMAL CONFIGURATION:")
        print(f"Batch size: {optimal['batch_size']}")
        print(f"Max workers: {optimal['max_workers']}")
        print(f"Throughput: {optimal['throughput']:.2f} docs/s")
        print(f"Avg time per doc: {optimal['avg_time_per_doc']:.2f}s")

        # Save results
        report_file = 'logs/batch_size_benchmark.json'
        with open(report_file, 'w') as f:
            json.dump({
                'results': self.results,
                'optimal': optimal
            }, f, indent=2)

        print(f"\n✓ Benchmark report saved: {report_file}")

        # Generate visualization
        self.plot_results()

    def plot_results(self):
        """Plot benchmark results"""

        batch_sizes = [r['batch_size'] for r in self.results]
        throughputs = [r['throughput'] for r in self.results]

        plt.figure(figsize=(10, 6))
        plt.plot(batch_sizes, throughputs, marker='o')
        plt.xlabel('Batch Size')
        plt.ylabel('Throughput (docs/s)')
        plt.title('Batch Size Performance Comparison')
        plt.grid(True)

        plot_file = 'logs/batch_size_performance.png'
        plt.savefig(plot_file)
        print(f"✓ Performance plot saved: {plot_file}")

def main():
    # Get sample documents
    sample_dir = Path('input')
    sample_documents = list(sample_dir.glob('*.md'))[:100]  # Limit to 100 samples

    if not sample_documents:
        print("ERROR: No sample documents found")
        return

    print(f"Using {len(sample_documents)} sample documents")

    benchmark = BatchSizeBenchmark([str(d) for d in sample_documents])
    benchmark.run_benchmarks()

if __name__ == "__main__":
    main()
```

### 5.2 Index Optimization

**INDEX CREATION SCRIPT:**
```cypher
// File: scripts/create_indexes.cypher

// ===================================
// AEON Knowledge Graph Index Creation
// ===================================

// Document indexes
CREATE INDEX document_sha256 IF NOT EXISTS
FOR (d:Document) ON (d.sha256);

CREATE INDEX document_processed_at IF NOT EXISTS
FOR (d:Document) ON (d.processed_at);

// Entity indexes
CREATE INDEX person_name IF NOT EXISTS
FOR (p:Person) ON (p.name);

CREATE INDEX organization_name IF NOT EXISTS
FOR (o:Organization) ON (o.name);

CREATE INDEX location_name IF NOT EXISTS
FOR (l:Location) ON (l.name);

CREATE INDEX concept_name IF NOT EXISTS
FOR (c:Concept) ON (c.name);

// Composite indexes for performance
CREATE INDEX entity_name_label IF NOT EXISTS
FOR (e:Entity) ON (e.name, e.label);

// Full-text search indexes
CREATE FULLTEXT INDEX entity_fulltext IF NOT EXISTS
FOR (n:Person|Organization|Location|Concept)
ON EACH [n.name];

// Relationship indexes
CREATE INDEX relationship_context IF NOT EXISTS
FOR ()-[r:RELATED_TO]-() ON (r.context);

// Show created indexes
SHOW INDEXES;
```

**INDEX MAINTENANCE SCRIPT:**
```python
# File: scripts/maintain_indexes.py

from neo4j import GraphDatabase
import os
from datetime import datetime

class IndexManager:
    """Manage Neo4j indexes for optimal performance"""

    def __init__(self):
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = os.getenv('NEO4J_USER', 'neo4j')
        self.password = os.getenv('NEO4J_PASSWORD', 'password')
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def create_indexes(self):
        """Create all necessary indexes"""

        print("=== Creating Indexes ===")

        with open('scripts/create_indexes.cypher') as f:
            queries = f.read().split(';')

        with self.driver.session() as session:
            for query in queries:
                query = query.strip()
                if query and not query.startswith('//'):
                    try:
                        session.run(query)
                        print(f"✓ Executed: {query[:50]}...")
                    except Exception as e:
                        print(f"✗ Error: {e}")

        print("=== Index Creation Complete ===")

    def analyze_index_usage(self):
        """Analyze index usage and effectiveness"""

        print("\n=== Index Usage Analysis ===")

        queries = [
            ("SHOW INDEXES", "Current indexes"),
            ("CALL db.indexes()", "Detailed index information"),
            ("CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Primitive count') YIELD attributes RETURN attributes", "Database statistics")
        ]

        with self.driver.session() as session:
            for query, description in queries:
                print(f"\n{description}:")
                print("-" * 60)
                try:
                    result = session.run(query)
                    for record in result:
                        print(dict(record))
                except Exception as e:
                    print(f"Error: {e}")

    def rebuild_indexes(self):
        """Rebuild indexes for optimization"""

        print("\n=== Rebuilding Indexes ===")
        print("⚠ This may take several minutes...")

        with self.driver.session() as session:
            # Get all indexes
            result = session.run("SHOW INDEXES")
            indexes = [record['name'] for record in result]

            for index_name in indexes:
                print(f"\nRebuilding: {index_name}")
                try:
                    # Drop and recreate
                    session.run(f"DROP INDEX {index_name} IF EXISTS")
                    print(f"  ✓ Dropped {index_name}")

                    # Indexes will be recreated by create_indexes()
                except Exception as e:
                    print(f"  ✗ Error: {e}")

        # Recreate all indexes
        self.create_indexes()
        print("\n=== Index Rebuild Complete ===")

def main():
    manager = IndexManager()
    try:
        # Create indexes
        manager.create_indexes()

        # Analyze usage
        manager.analyze_index_usage()

        # Optionally rebuild
        # manager.rebuild_indexes()

    finally:
        manager.close()

if __name__ == "__main__":
    main()
```

---

## 6. TROUBLESHOOTING PROCEDURES

### 6.1 Common Errors and Solutions

**ERROR RESOLUTION GUIDE:**

```markdown
## Error: spaCy Model Not Found

**Symptoms:**
- OSError: [E050] Can't find model 'en_core_web_sm'
- Import errors when loading spaCy

**Solutions:**
1. Install model: `python -m spacy download en_core_web_sm`
2. Verify installation: `python -c "import spacy; spacy.load('en_core_web_sm')"`
3. Check Python environment activation
4. Reinstall spaCy: `pip install --upgrade spacy`

**Prevention:**
- Add model check to pre-ingestion validation
- Document model dependencies in requirements.txt
- Use virtual environment for consistency

---

## Error: Neo4j Connection Failed

**Symptoms:**
- neo4j.exceptions.ServiceUnavailable
- Connection refused errors
- Authentication failed errors

**Solutions:**
1. Check Neo4j is running: `systemctl status neo4j` or `neo4j status`
2. Verify connection details:
   - URI: bolt://localhost:7687
   - Username/password correct
3. Test connection: `neo4j console` or Neo4j Browser
4. Check firewall: `sudo ufw status`
5. Review Neo4j logs: `tail -f /var/log/neo4j/neo4j.log`

**Prevention:**
- Implement connection retry logic
- Add connection health checks
- Monitor Neo4j service status
- Set up connection pooling

---

## Error: Memory Exhausted

**Symptoms:**
- MemoryError during processing
- System becomes unresponsive
- Neo4j heap space errors

**Solutions:**
1. Reduce batch size in configuration
2. Decrease max_workers
3. Increase system RAM
4. Configure Neo4j heap size:
   ```
   dbms.memory.heap.initial_size=2g
   dbms.memory.heap.max_size=4g
   ```
5. Process documents sequentially
6. Clear cache: `CALL apoc.periodic.commit("MATCH (n) RETURN count(*)", {})`

**Prevention:**
- Monitor memory usage during processing
- Set memory limits in configuration
- Use memory-efficient data structures
- Implement garbage collection

---

## Error: Entity Extraction Timeout

**Symptoms:**
- Processing hangs on specific documents
- Timeout errors in logs
- Slow processing speed

**Solutions:**
1. Increase timeout: `timeout_per_document = 600`
2. Skip problematic documents
3. Split large documents into chunks
4. Use smaller spaCy model
5. Process on more powerful hardware

**Prevention:**
- Set reasonable timeouts
- Implement document size limits
- Add progress monitoring
- Use async processing

---

## Error: Duplicate Node Creation

**Symptoms:**
- Multiple nodes for same entity
- Inconsistent entity references
- Database bloat

**Solutions:**
1. Use MERGE instead of CREATE
2. Add unique constraints:
   ```cypher
   CREATE CONSTRAINT unique_person_name IF NOT EXISTS
   FOR (p:Person) REQUIRE p.name IS UNIQUE;
   ```
3. Normalize entity names before ingestion
4. Clean up duplicates:
   ```cypher
   MATCH (n:Person)
   WITH n.name as name, collect(n) as nodes
   WHERE size(nodes) > 1
   FOREACH (node in tail(nodes) | DETACH DELETE node);
   ```

**Prevention:**
- Implement entity normalization
- Use unique constraints
- Add deduplication step
- Validate before ingestion
```

### 6.2 Diagnostic Tools

**DIAGNOSTIC SCRIPT:**
```python
# File: scripts/diagnose_system.py

import os
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime

class SystemDiagnostics:
    """Comprehensive system diagnostics"""

    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': []
        }

    def check_python_environment(self):
        """Check Python environment"""

        print("\n=== Python Environment ===")
        check = {
            'name': 'Python Environment',
            'status': 'unknown',
            'details': {}
        }

        try:
            # Python version
            py_version = sys.version
            print(f"Python version: {py_version}")
            check['details']['python_version'] = py_version

            # Virtual environment
            venv = os.getenv('VIRTUAL_ENV')
            if venv:
                print(f"✓ Virtual environment: {venv}")
                check['details']['virtual_env'] = venv
            else:
                print("⚠ No virtual environment detected")

            # Installed packages
            try:
                import spacy
                import neo4j
                print("✓ Core packages installed")
                check['details']['core_packages'] = 'installed'
            except ImportError as e:
                print(f"✗ Missing packages: {e}")
                check['details']['core_packages'] = f'missing: {e}'

            check['status'] = 'ok'

        except Exception as e:
            print(f"✗ Error: {e}")
            check['status'] = 'error'
            check['details']['error'] = str(e)

        self.results['checks'].append(check)

    def check_neo4j_connectivity(self):
        """Check Neo4j connectivity"""

        print("\n=== Neo4j Connectivity ===")
        check = {
            'name': 'Neo4j Connectivity',
            'status': 'unknown',
            'details': {}
        }

        try:
            from neo4j import GraphDatabase

            uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
            user = os.getenv('NEO4J_USER', 'neo4j')
            password = os.getenv('NEO4J_PASSWORD', 'password')

            driver = GraphDatabase.driver(uri, auth=(user, password))

            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                assert result.single()['test'] == 1

                # Get version
                version_result = session.run("CALL dbms.components() YIELD versions")
                version = version_result.single()['versions'][0]

                # Get node count
                count_result = session.run("MATCH (n) RETURN count(n) as count")
                node_count = count_result.single()['count']

                print(f"✓ Connected to Neo4j {version}")
                print(f"✓ Current node count: {node_count}")

                check['details']['neo4j_version'] = version
                check['details']['node_count'] = node_count
                check['status'] = 'ok'

            driver.close()

        except Exception as e:
            print(f"✗ Connection failed: {e}")
            check['status'] = 'error'
            check['details']['error'] = str(e)

        self.results['checks'].append(check)

    def check_spacy_models(self):
        """Check spaCy models"""

        print("\n=== spaCy Models ===")
        check = {
            'name': 'spaCy Models',
            'status': 'unknown',
            'details': {}
        }

        try:
            import spacy

            models = ['en_core_web_sm', 'en_core_web_lg']
            available = []
            missing = []

            for model in models:
                try:
                    nlp = spacy.load(model)
                    print(f"✓ {model} loaded successfully")
                    available.append(model)
                except OSError:
                    print(f"✗ {model} not found")
                    missing.append(model)

            check['details']['available'] = available
            check['details']['missing'] = missing

            if available:
                check['status'] = 'ok'
            else:
                check['status'] = 'error'

        except Exception as e:
            print(f"✗ Error: {e}")
            check['status'] = 'error'
            check['details']['error'] = str(e)

        self.results['checks'].append(check)

    def check_directories(self):
        """Check directory structure"""

        print("\n=== Directory Structure ===")
        check = {
            'name': 'Directory Structure',
            'status': 'unknown',
            'details': {}
        }

        required_dirs = ['input', 'output', 'logs', 'metadata', 'backups', 'config']

        existing = []
        missing = []

        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                print(f"✓ {dir_name}/ exists")
                existing.append(dir_name)
            else:
                print(f"✗ {dir_name}/ missing")
                missing.append(dir_name)

        check['details']['existing'] = existing
        check['details']['missing'] = missing
        check['status'] = 'ok' if not missing else 'warning'

        self.results['checks'].append(check)

    def check_disk_space(self):
        """Check available disk space"""

        print("\n=== Disk Space ===")
        check = {
            'name': 'Disk Space',
            'status': 'unknown',
            'details': {}
        }

        try:
            result = subprocess.run(['df', '-h', '.'], capture_output=True, text=True)
            output_lines = result.stdout.strip().split('\n')

            if len(output_lines) > 1:
                disk_info = output_lines[1].split()
                print(f"Available: {disk_info[3]}")
                print(f"Used: {disk_info[4]}")

                check['details']['available'] = disk_info[3]
                check['details']['used_percentage'] = disk_info[4]
                check['status'] = 'ok'

        except Exception as e:
            print(f"✗ Error: {e}")
            check['status'] = 'error'
            check['details']['error'] = str(e)

        self.results['checks'].append(check)

    def run_diagnostics(self):
        """Run all diagnostic checks"""

        print("="*60)
        print("SYSTEM DIAGNOSTICS")
        print("="*60)

        self.check_python_environment()
        self.check_neo4j_connectivity()
        self.check_spacy_models()
        self.check_directories()
        self.check_disk_space()

        # Generate report
        report_file = f'logs/diagnostics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n{'='*60}")
        print(f"DIAGNOSTICS COMPLETE")
        print(f"Report saved: {report_file}")
        print(f"{'='*60}")

        # Summary
        ok_count = sum(1 for c in self.results['checks'] if c['status'] == 'ok')
        total_checks = len(self.results['checks'])

        print(f"\nPassed: {ok_count}/{total_checks} checks")

        # Recommendations
        errors = [c for c in self.results['checks'] if c['status'] == 'error']
        if errors:
            print("\n⚠ ISSUES FOUND:")
            for check in errors:
                print(f"  - {check['name']}: {check['details'].get('error', 'Unknown error')}")

def main():
    diagnostics = SystemDiagnostics()
    diagnostics.run_diagnostics()

if __name__ == "__main__":
    main()
```

---

## 7. BACKUP AND RECOVERY PROCEDURES

### 7.1 Database Backup Procedures

**BACKUP SCRIPT:**
```bash
#!/bin/bash
# File: scripts/backup_database.sh

echo "=== Neo4j Database Backup ==="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"

# Configuration
BACKUP_DIR="backups/neo4j"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_NAME="neo4j_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Stop Neo4j (optional, for consistency)
read -p "Stop Neo4j for backup? (y/n): " STOP_NEO4J

if [ "$STOP_NEO4J" = "y" ]; then
    echo "Stopping Neo4j..."
    sudo systemctl stop neo4j
fi

# Create backup using neo4j-admin
echo "Creating backup..."
neo4j-admin dump --database=neo4j --to="${BACKUP_PATH}.dump"

if [ $? -eq 0 ]; then
    echo "✓ Backup created: ${BACKUP_PATH}.dump"

    # Compress backup
    echo "Compressing backup..."
    gzip "${BACKUP_PATH}.dump"
    echo "✓ Backup compressed: ${BACKUP_PATH}.dump.gz"

    # Calculate size
    SIZE=$(du -h "${BACKUP_PATH}.dump.gz" | cut -f1)
    echo "Backup size: $SIZE"

else
    echo "✗ Backup failed"
    exit 1
fi

# Restart Neo4j if stopped
if [ "$STOP_NEO4J" = "y" ]; then
    echo "Restarting Neo4j..."
    sudo systemctl start neo4j
    sleep 5
    sudo systemctl status neo4j
fi

# Cleanup old backups (keep last 7 days)
echo "Cleaning up old backups..."
find "$BACKUP_DIR" -name "*.dump.gz" -mtime +7 -delete
echo "✓ Old backups removed"

# Log backup
echo "${TIMESTAMP}\t${BACKUP_NAME}\t${SIZE}\tsuccess" >> "${BACKUP_DIR}/backup.log"

echo "=== Backup Complete ==="
```

**INCREMENTAL BACKUP:**
```python
# File: scripts/incremental_backup.py

from neo4j import GraphDatabase
import os
import json
from datetime import datetime
from pathlib import Path
import subprocess

class IncrementalBackup:
    """Perform incremental database backups"""

    def __init__(self):
        self.backup_dir = Path('backups/incremental')
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.backup_dir / 'backup_state.json'
        self.load_state()

    def load_state(self):
        """Load backup state"""
        if self.state_file.exists():
            with open(self.state_file) as f:
                self.state = json.load(f)
        else:
            self.state = {
                'last_backup': None,
                'last_document_count': 0,
                'backups': []
            }

    def save_state(self):
        """Save backup state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def check_if_backup_needed(self) -> bool:
        """Determine if backup is needed"""

        from neo4j import GraphDatabase

        uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        user = os.getenv('NEO4J_USER', 'neo4j')
        password = os.getenv('NEO4J_PASSWORD', 'password')

        driver = GraphDatabase.driver(uri, auth=(user, password))

        with driver.session() as session:
            result = session.run("MATCH (d:Document) RETURN count(d) as count")
            current_count = result.single()['count']

        driver.close()

        last_count = self.state['last_document_count']
        new_documents = current_count - last_count

        print(f"Current documents: {current_count}")
        print(f"Last backup: {last_count}")
        print(f"New documents: {new_documents}")

        # Backup if 10+ new documents
        if new_documents >= 10:
            print("✓ Backup needed")
            return True
        else:
            print("✓ No backup needed")
            return False

    def create_backup(self):
        """Create incremental backup"""

        if not self.check_if_backup_needed():
            return

        print("\n=== Creating Incremental Backup ===")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"incremental_{timestamp}"
        backup_path = self.backup_dir / f"{backup_name}.dump"

        # Create backup
        cmd = [
            'neo4j-admin',
            'dump',
            '--database=neo4j',
            f'--to={backup_path}'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ Backup created: {backup_path}")

            # Compress
            subprocess.run(['gzip', str(backup_path)])
            compressed_path = f"{backup_path}.gz"

            # Get size
            size = os.path.getsize(compressed_path)

            # Update state
            backup_info = {
                'timestamp': timestamp,
                'name': backup_name,
                'path': str(compressed_path),
                'size_bytes': size
            }

            self.state['backups'].append(backup_info)
            self.state['last_backup'] = timestamp

            # Update document count
            from neo4j import GraphDatabase
            uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
            user = os.getenv('NEO4J_USER', 'neo4j')
            password = os.getenv('NEO4J_PASSWORD', 'password')
            driver = GraphDatabase.driver(uri, auth=(user, password))

            with driver.session() as session:
                result = session.run("MATCH (d:Document) RETURN count(d) as count")
                self.state['last_document_count'] = result.single()['count']

            driver.close()

            self.save_state()

            print(f"✓ Backup size: {size / 1024 / 1024:.2f} MB")
            print("✓ State updated")

        else:
            print(f"✗ Backup failed: {result.stderr}")

def main():
    backup = IncrementalBackup()
    backup.create_backup()

if __name__ == "__main__":
    main()
```

### 7.2 Restore Procedures

**RESTORE SCRIPT:**
```bash
#!/bin/bash
# File: scripts/restore_database.sh

echo "=== Neo4j Database Restore ==="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"

# List available backups
echo -e "\nAvailable backups:"
ls -lh backups/neo4j/*.dump.gz

# Select backup
read -p "Enter backup filename: " BACKUP_FILE

if [ ! -f "backups/neo4j/$BACKUP_FILE" ]; then
    echo "✗ Backup file not found"
    exit 1
fi

# Confirmation
echo -e "\n⚠️  WARNING: This will replace current database!"
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# Stop Neo4j
echo "Stopping Neo4j..."
sudo systemctl stop neo4j

# Decompress backup
echo "Decompressing backup..."
BACKUP_PATH="backups/neo4j/$BACKUP_FILE"
gunzip -c "$BACKUP_PATH" > "/tmp/restore.dump"

# Restore database
echo "Restoring database..."
neo4j-admin load --database=neo4j --from=/tmp/restore.dump --force

if [ $? -eq 0 ]; then
    echo "✓ Database restored successfully"

    # Cleanup
    rm /tmp/restore.dump

    # Start Neo4j
    echo "Starting Neo4j..."
    sudo systemctl start neo4j
    sleep 5

    # Verify
    sudo systemctl status neo4j

    echo "=== Restore Complete ==="
else
    echo "✗ Restore failed"
    exit 1
fi
```

---

## 8. COMPLIANCE AND AUDIT PROCEDURES

### 8.1 Data Lineage Tracking

**LINEAGE TRACKER:**
```python
# File: scripts/track_lineage.py

from neo4j import GraphDatabase
import os
import json
from datetime import datetime
from typing import Dict, List

class DataLineageTracker:
    """Track data lineage for compliance"""

    def __init__(self):
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = os.getenv('NEO4J_USER', 'neo4j')
        self.password = os.getenv('NEO4J_PASSWORD', 'password')
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def track_document_lineage(self, doc_hash: str) -> Dict:
        """Track complete lineage for document"""

        print(f"=== Tracking Lineage: {doc_hash} ===")

        with self.driver.session() as session:
            # Get document metadata
            doc_query = """
            MATCH (d:Document {sha256: $hash})
            RETURN d
            """
            doc_result = session.run(doc_query, hash=doc_hash)
            doc_record = doc_result.single()

            if not doc_record:
                print("Document not found")
                return None

            document = dict(doc_record['d'])

            # Get all entities from document
            entities_query = """
            MATCH (e)-[:MENTIONED_IN]->(d:Document {sha256: $hash})
            RETURN labels(e)[0] as type, e.name as name, count(*) as mentions
            """
            entities_result = session.run(entities_query, hash=doc_hash)
            entities = [dict(record) for record in entities_result]

            # Get all relationships from document
            rels_query = """
            MATCH ()-[r]->(d:Document {sha256: $hash})
            RETURN type(r) as relationship, count(r) as count
            """
            rels_result = session.run(rels_query, hash=doc_hash)
            relationships = [dict(record) for record in rels_result]

            lineage = {
                'document': document,
                'entities': entities,
                'relationships': relationships,
                'timestamp': datetime.now().isoformat()
            }

            print(f"✓ Document: {document.get('filename')}")
            print(f"✓ Entities: {len(entities)}")
            print(f"✓ Relationships: {sum(r['count'] for r in relationships)}")

            return lineage

    def generate_lineage_report(self, output_file: str = None):
        """Generate comprehensive lineage report"""

        print("\n=== Generating Lineage Report ===")

        with self.driver.session() as session:
            # Get all documents
            docs_query = "MATCH (d:Document) RETURN d.sha256 as hash"
            docs_result = session.run(docs_query)
            doc_hashes = [record['hash'] for record in docs_result]

            print(f"Processing {len(doc_hashes)} documents...")

            lineages = []
            for doc_hash in doc_hashes:
                lineage = self.track_document_lineage(doc_hash)
                if lineage:
                    lineages.append(lineage)

            # Generate report
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_documents': len(lineages),
                'lineages': lineages
            }

            if output_file is None:
                output_file = f'logs/lineage_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)

            print(f"\n✓ Lineage report saved: {output_file}")

            return report

def main():
    tracker = DataLineageTracker()
    try:
        tracker.generate_lineage_report()
    finally:
        tracker.close()

if __name__ == "__main__":
    main()
```

### 8.2 Audit Logging

**AUDIT LOGGER:**
```python
# File: scripts/audit_logger.py

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class AuditLogger:
    """Comprehensive audit logging for compliance"""

    def __init__(self, log_dir: str = 'logs/audit'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logger
        self.logger = logging.getLogger('audit')
        self.logger.setLevel(logging.INFO)

        # File handler
        log_file = self.log_dir / f'audit_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log_event(self, event_type: str, details: Dict[str, Any]):
        """Log audit event"""

        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details
        }

        self.logger.info(json.dumps(event))

    def log_document_processing(self, document_path: str, status: str, details: Dict):
        """Log document processing event"""
        self.log_event('document_processing', {
            'document': document_path,
            'status': status,
            **details
        })

    def log_database_operation(self, operation: str, details: Dict):
        """Log database operation"""
        self.log_event('database_operation', {
            'operation': operation,
            **details
        })

    def log_system_event(self, event: str, details: Dict):
        """Log system event"""
        self.log_event('system_event', {
            'event': event,
            **details
        })

    def log_error(self, error_type: str, error_message: str, context: Dict):
        """Log error event"""
        self.log_event('error', {
            'error_type': error_type,
            'error_message': error_message,
            'context': context
        })

# Global audit logger instance
audit_logger = AuditLogger()

def main():
    """Demonstrate audit logging"""

    # Example usage
    audit_logger.log_document_processing(
        document_path='/path/to/document.md',
        status='success',
        details={
            'entity_count': 42,
            'relationship_count': 18,
            'processing_time': 3.5
        }
    )

    audit_logger.log_database_operation(
        operation='backup',
        details={
            'backup_file': 'backup_20251029.dump.gz',
            'size_mb': 245.8
        }
    )

    print("✓ Audit events logged")

if __name__ == "__main__":
    main()
```

---

## APPENDICES

### Appendix A: Quick Reference Checklists

**DAILY OPERATIONS CHECKLIST:**
```
□ System Health Check
  □ Neo4j running and responsive
  □ Disk space adequate (>10GB free)
  □ No errors in logs
  □ Backup status verified

□ Ingestion Pipeline
  □ New documents identified
  □ Batch processing scheduled
  □ Quality checks passed
  □ Metadata updated

□ Monitoring
  □ Performance metrics reviewed
  □ Error rates acceptable
  □ Resource usage normal
  □ Audit logs reviewed
```

**WEEKLY MAINTENANCE CHECKLIST:**
```
□ Database Maintenance
  □ Full backup created
  □ Indexes optimized
  □ Statistics updated
  □ Old logs archived

□ Quality Assurance
  □ Random document validation
  □ Graph integrity check
  □ Duplicate detection run
  □ Lineage verification

□ Performance Review
  □ Processing speed analyzed
  □ Bottlenecks identified
  □ Optimization opportunities noted
  □ Resource usage trends reviewed
```

### Appendix B: Contact Information

**ESCALATION CONTACTS:**
```
Database Administrator:
- Name: [Admin Name]
- Email: admin@example.com
- Phone: [Phone Number]
- Availability: 24/7

System Administrator:
- Name: [Sysadmin Name]
- Email: sysadmin@example.com
- Phone: [Phone Number]
- Availability: Business hours

ML/NLP Team:
- Name: [ML Team Lead]
- Email: ml@example.com
- Availability: Business hours

DevOps Team:
- Name: [DevOps Lead]
- Email: devops@example.com
- Phone: [Phone Number]
- Availability: 24/7
```

### Appendix C: Configuration Templates

**MINIMAL CONFIGURATION:**
```json
{
  "ingestion": {
    "batch_size": 10,
    "max_workers": 2,
    "timeout_per_document": 300
  },
  "neo4j": {
    "uri": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "password"
  },
  "spacy": {
    "model": "en_core_web_sm"
  }
}
```

**PRODUCTION CONFIGURATION:**
```json
{
  "ingestion": {
    "batch_size": 50,
    "max_workers": 8,
    "timeout_per_document": 600,
    "retry_attempts": 3,
    "error_threshold": 0.05
  },
  "neo4j": {
    "uri": "bolt://neo4j-server:7687",
    "user": "neo4j",
    "password": "${NEO4J_PASSWORD}",
    "connection_pool_size": 50
  },
  "spacy": {
    "model": "en_core_web_lg",
    "batch_size": 100
  },
  "quality": {
    "min_entities_per_doc": 1,
    "max_entities_per_doc": 1000,
    "min_relationship_ratio": 0.1
  },
  "backup": {
    "enabled": true,
    "schedule": "0 2 * * *",
    "retention_days": 30
  },
  "monitoring": {
    "enabled": true,
    "metrics_interval": 60
  }
}
```

---

## DOCUMENT REVISION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0.0 | 2025-10-29 | AEON Project Team | Initial comprehensive operating procedures |

---

**END OF OPERATING PROCEDURES**

*For questions or support, contact the AEON Project Team*
