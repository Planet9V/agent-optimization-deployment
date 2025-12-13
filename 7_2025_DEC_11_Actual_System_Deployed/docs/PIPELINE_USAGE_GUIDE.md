# Pipeline Usage Guide - E30 Hierarchical Enrichment

**Document:** PIPELINE_USAGE_GUIDE.md
**Created:** 2025-12-12
**Version:** 1.0.0
**Status:** PRODUCTION-READY
**For:** Data Engineers & Developers

---

## Critical Rule: ALWAYS Use Hierarchical Pipeline

**PRIMARY PIPELINE:**
```
/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py
```

**NEVER USE:**
- `06_bulk_graph_ingestion.py` (deprecated, no hierarchical enrichment)
- `load_comprehensive_taxonomy.py` (deprecated, taxonomy only)
- Direct Cypher writes without enrichment
- Any custom scripts that bypass HierarchicalEntityProcessor

---

## Table of Contents

1. [Quick Start Guide](#quick-start-guide)
2. [Pipeline Architecture](#pipeline-architecture)
3. [Step-by-Step Usage](#step-by-step-usage)
4. [Verification Procedures](#verification-procedures)
5. [Common Use Cases](#common-use-cases)
6. [Error Handling](#error-handling)
7. [Performance Optimization](#performance-optimization)

---

## Quick Start Guide

### Prerequisites Check

```bash
# 1. Verify NER11 API running
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"ner11"}

# 2. Verify Neo4j running
curl http://localhost:7474
# Expected: Neo4j Browser page

# 3. Verify Python dependencies
python3 -c "import neo4j, requests; print('Dependencies OK')"
# Expected: Dependencies OK

# 4. Verify pipeline exists
ls -l /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py
# Expected: File exists
```

### Simple Example (5 minutes)

```python
#!/usr/bin/env python3
"""
Simple example: Process single cybersecurity document
File: /tmp/example_ingestion.py
"""
import sys
from pathlib import Path

# Add pipeline directory to path
pipeline_dir = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines")
sys.path.insert(0, str(pipeline_dir))

from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

# Sample document
document_text = """
APT29, also known as Cozy Bear, exploited CVE-2024-12345, a critical
vulnerability in Microsoft Exchange Server. The group used WellMess malware
to target government organizations in the United States and Europe.
"""

# Initialize pipeline with hierarchical enrichment
with NER11ToNeo4jPipeline(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="neo4j@openspg",
    ner11_api_url="http://localhost:8000"
) as pipeline:

    # Process document
    print("Processing document...")
    stats = pipeline.process_document(document_text, "example_doc_001")

    # Show results
    print("\n✅ INGESTION COMPLETE")
    print(f"  Entities extracted: {stats['entities_extracted']}")
    print(f"  Nodes created/merged: {stats['nodes_created']}")
    print(f"  Relationships created: {stats['relationships_created']}")
    print(f"  Errors: {stats['errors']}")

    # Validate hierarchical enrichment
    print("\n🔍 VALIDATING ENRICHMENT...")
    validation = pipeline.validate_ingestion()

    print(f"  Total nodes in database: {validation['total_nodes']:,}")
    print(f"  Baseline preserved: {'✅' if validation['node_count_preserved'] else '❌'}")
    print(f"  Validation passed: {'✅' if validation['validation_passed'] else '⚠️'}")
```

**Run it:**
```bash
python3 /tmp/example_ingestion.py
```

**Expected Output:**
```
Processing document...

✅ INGESTION COMPLETE
  Entities extracted: 6
  Nodes created/merged: 6
  Relationships created: 4
  Errors: 0

🔍 VALIDATING ENRICHMENT...
  Total nodes in database: 1,207,038
  Baseline preserved: ✅
  Validation passed: ✅
```

---

## Pipeline Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    05_ner11_to_neo4j_hierarchical.py            │
│                                                                 │
│  ┌───────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│  │  NER11 API    │  │ Hierarchical     │  │ Neo4j Mapper  │  │
│  │  Client       │─▶│ Entity Processor │─▶│               │  │
│  │               │  │ (566 types)      │  │ (60→16 labels)│  │
│  └───────────────┘  └──────────────────┘  └────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Neo4j Driver                         │  │
│  │  • MERGE-based node creation (no duplicates)             │  │
│  │  • Relationship extraction and creation                  │  │
│  │  • Built-in validation                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Input Document (Text)
       ↓
NER11 API (Entity Extraction)
       ↓ entities: [{text, label, start, end}, ...]
Hierarchical Entity Processor (Enrichment)
       ↓ enriched: {super_label, tier1, tier2, tier, hierarchy_path, discriminators}
NER11ToNeo4jMapper (Label Mapping)
       ↓ neo4j: {super_label, discriminator_property, discriminator_value}
Neo4j Node Creation (MERGE)
       ↓ node: ThreatActor{name, super_label, tier1, tier2, tier, actorType, ...}
Relationship Extraction (Pattern-based)
       ↓ relationships: [(ThreatActor)-[USES]->(Malware), ...]
Neo4j Relationship Creation (MERGE)
       ↓ relationships created
Validation (Node count, tier distribution)
       ↓
✅ Complete with hierarchical enrichment
```

### Key Components

**1. HierarchicalEntityProcessor** (`00_hierarchical_entity_processor.py`)
- 566-type taxonomy
- Super label assignment (16 labels)
- Tier categorization (tier1, tier2, tier)
- Property discriminators (actorType, malwareFamily, etc.)
- Hierarchy path generation

**2. NER11ToNeo4jMapper** (`04_ner11_to_neo4j_mapper.py`)
- Maps 60 NER labels → 16 Neo4j super labels
- Defines discriminator properties
- Provides label-specific enrichment logic

**3. NER11ToNeo4jPipeline** (`05_ner11_to_neo4j_hierarchical.py`)
- Orchestrates complete ingestion workflow
- MERGE-based node creation (preserves existing)
- Relationship extraction and creation
- Built-in validation

---

## Step-by-Step Usage

### Use Case 1: Single Document Ingestion

**Scenario:** Ingest a single cybersecurity report into Neo4j

```python
#!/usr/bin/env python3
"""
Use Case 1: Single Document Ingestion
Processes one document with full hierarchical enrichment
"""
import sys
from pathlib import Path

pipeline_dir = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines")
sys.path.insert(0, str(pipeline_dir))

from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

def ingest_single_document(file_path: str, document_id: str):
    """Ingest single document from file."""

    # Read document
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Initialize pipeline
    with NER11ToNeo4jPipeline() as pipeline:
        # Process document
        stats = pipeline.process_document(text, document_id)

        # Report results
        print(f"Document: {document_id}")
        print(f"  Entities: {stats['entities_extracted']}")
        print(f"  Nodes: {stats['nodes_created']}")
        print(f"  Relationships: {stats['relationships_created']}")

        return stats

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python ingest_single.py <file_path> <document_id>")
        sys.exit(1)

    file_path = sys.argv[1]
    doc_id = sys.argv[2]

    ingest_single_document(file_path, doc_id)
```

**Run it:**
```bash
python3 ingest_single.py /path/to/report.txt "report_20251212"
```

### Use Case 2: Batch Directory Ingestion

**Scenario:** Ingest all documents from a directory

```python
#!/usr/bin/env python3
"""
Use Case 2: Batch Directory Ingestion
Processes all .txt files in directory with hierarchical enrichment
"""
import sys
from pathlib import Path
from datetime import datetime

pipeline_dir = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines")
sys.path.insert(0, str(pipeline_dir))

from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

def batch_ingest_directory(directory_path: str, file_pattern: str = "*.txt"):
    """Batch ingest all documents from directory."""

    directory = Path(directory_path)
    files = list(directory.glob(file_pattern))

    print(f"Found {len(files)} files matching pattern '{file_pattern}'")

    # Track overall statistics
    total_stats = {
        "documents_processed": 0,
        "entities_extracted": 0,
        "nodes_created": 0,
        "relationships_created": 0,
        "errors": 0
    }

    # Initialize pipeline once for batch processing
    with NER11ToNeo4jPipeline() as pipeline:

        for idx, file_path in enumerate(files, 1):
            print(f"\n[{idx}/{len(files)}] Processing: {file_path.name}")

            # Read document
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # Generate document ID from filename
                doc_id = file_path.stem

                # Process document
                stats = pipeline.process_document(text, doc_id)

                # Accumulate statistics
                total_stats["documents_processed"] += 1
                total_stats["entities_extracted"] += stats['entities_extracted']
                total_stats["nodes_created"] += stats['nodes_created']
                total_stats["relationships_created"] += stats['relationships_created']
                total_stats["errors"] += stats['errors']

                print(f"  ✅ Entities: {stats['entities_extracted']}, "
                      f"Nodes: {stats['nodes_created']}, "
                      f"Relationships: {stats['relationships_created']}")

            except Exception as e:
                print(f"  ❌ Error: {e}")
                total_stats["errors"] += 1

        # Final validation
        print("\n" + "="*60)
        print("BATCH INGESTION COMPLETE")
        print("="*60)
        print(f"Documents processed: {total_stats['documents_processed']}")
        print(f"Total entities: {total_stats['entities_extracted']}")
        print(f"Total nodes: {total_stats['nodes_created']}")
        print(f"Total relationships: {total_stats['relationships_created']}")
        print(f"Errors: {total_stats['errors']}")

        # Validate database
        print("\n🔍 VALIDATING DATABASE...")
        validation = pipeline.validate_ingestion()
        print(f"  Total nodes: {validation['total_nodes']:,}")
        print(f"  Baseline preserved: {'✅' if validation['node_count_preserved'] else '❌'}")
        print(f"  Validation passed: {'✅' if validation['validation_passed'] else '⚠️'}")

    return total_stats

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_ingest.py <directory_path> [file_pattern]")
        sys.exit(1)

    directory = sys.argv[1]
    pattern = sys.argv[2] if len(sys.argv) > 2 else "*.txt"

    batch_ingest_directory(directory, pattern)
```

**Run it:**
```bash
python3 batch_ingest.py /path/to/documents "*.txt"
```

### Use Case 3: CSV Data Ingestion

**Scenario:** Ingest structured data from CSV

```python
#!/usr/bin/env python3
"""
Use Case 3: CSV Data Ingestion
Processes CSV file with structured threat intelligence data
"""
import sys
import csv
from pathlib import Path

pipeline_dir = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines")
sys.path.insert(0, str(pipeline_dir))

from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

def ingest_csv_data(csv_path: str, text_column: str = "description"):
    """
    Ingest CSV data with threat intelligence descriptions.

    Args:
        csv_path: Path to CSV file
        text_column: Name of column containing text to process
    """

    # Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} rows from CSV")

    # Initialize pipeline
    with NER11ToNeo4jPipeline() as pipeline:

        for idx, row in enumerate(rows, 1):
            # Get text from specified column
            text = row.get(text_column, "")

            if not text or len(text.strip()) < 10:
                print(f"[{idx}/{len(rows)}] Skipping row (no text)")
                continue

            # Generate document ID from row data
            doc_id = row.get('id', f"csv_row_{idx}")

            print(f"[{idx}/{len(rows)}] Processing: {doc_id}")

            # Process document
            stats = pipeline.process_document(text, doc_id)

            print(f"  Entities: {stats['entities_extracted']}, "
                  f"Nodes: {stats['nodes_created']}")

        # Final validation
        print("\n✅ CSV INGESTION COMPLETE")
        validation = pipeline.validate_ingestion()
        print(f"  Database nodes: {validation['total_nodes']:,}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_csv.py <csv_path> [text_column]")
        sys.exit(1)

    csv_file = sys.argv[1]
    column = sys.argv[2] if len(sys.argv) > 2 else "description"

    ingest_csv_data(csv_file, column)
```

**Run it:**
```bash
python3 ingest_csv.py /path/to/data.csv "description"
```

---

## Verification Procedures

### How to Verify Hierarchical Enrichment Working

**After each ingestion, verify:**

#### 1. Check Entities Were Enriched

```cypher
// Get sample of recently created nodes
MATCH (n)
WHERE n.created_at > datetime() - duration('PT1H')
RETURN
    labels(n)[0] as label,
    n.name as name,
    n.super_label as super_label,
    n.tier1 as tier1,
    n.tier as tier,
    n.hierarchy_path as path,
    CASE
        WHEN n.super_label IS NULL THEN '❌ NO ENRICHMENT'
        WHEN n.tier IS NULL THEN '⚠️ PARTIAL ENRICHMENT'
        ELSE '✅ FULLY ENRICHED'
    END as status
ORDER BY n.created_at DESC
LIMIT 10;
```

**Expected:** All nodes should have `✅ FULLY ENRICHED` status

#### 2. Check Super Label Distribution

```cypher
// Verify super labels assigned
MATCH (n)
WHERE n.created_at > datetime() - duration('PT1H')
RETURN
    n.super_label as super_label,
    count(n) as count
ORDER BY count DESC;
```

**Expected:** Multiple super labels (ThreatActor, Malware, Vulnerability, etc.)

#### 3. Check Tier Distribution

```cypher
// Verify tier properties assigned
MATCH (n)
WHERE n.created_at > datetime() - duration('PT1H') AND n.tier IS NOT NULL
RETURN
    n.tier as tier,
    n.tier1 as tier1_category,
    count(n) as count
ORDER BY tier, count DESC;
```

**Expected:** Mix of tier 1, 2, and potentially 3 nodes

#### 4. Check Property Discriminators

```cypher
// Verify discriminator properties (for applicable super labels)
MATCH (n:ThreatActor)
WHERE n.created_at > datetime() - duration('PT1H')
RETURN
    n.name,
    n.actorType,
    CASE WHEN n.actorType IS NULL THEN '⚠️' ELSE '✅' END as has_discriminator
LIMIT 10;
```

**Expected:** Most ThreatActors should have `actorType` property

#### 5. Validate Hierarchy Paths

```cypher
// Check hierarchy path structure
MATCH (n)
WHERE n.created_at > datetime() - duration('PT1H')
  AND n.hierarchy_path IS NOT NULL
RETURN
    n.hierarchy_path as path,
    n.name as name
LIMIT 10;
```

**Expected:** Paths like `TECHNICAL/ThreatActor/APT29`, `TECHNICAL/Vulnerability/CVE-2024-12345`

---

## Common Use Cases

### Use Case 4: Re-process Failed Documents

```python
#!/usr/bin/env python3
"""
Use Case 4: Re-process Failed Documents
Retry documents that failed in previous ingestion run
"""
import sys
import json
from pathlib import Path

pipeline_dir = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines")
sys.path.insert(0, str(pipeline_dir))

from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

def retry_failed_documents(failed_log_path: str):
    """
    Retry documents that failed in previous run.

    Args:
        failed_log_path: Path to JSON file with failed document IDs
    """

    # Load failed document list
    with open(failed_log_path, 'r') as f:
        failed_docs = json.load(f)

    print(f"Retrying {len(failed_docs)} failed documents")

    # Initialize pipeline
    with NER11ToNeo4jPipeline() as pipeline:

        for doc_info in failed_docs:
            doc_id = doc_info['document_id']
            file_path = doc_info['file_path']

            print(f"\nRetrying: {doc_id}")

            try:
                # Read document
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # Process document
                stats = pipeline.process_document(text, doc_id)

                if stats['errors'] == 0:
                    print(f"  ✅ SUCCESS: {stats['entities_extracted']} entities")
                else:
                    print(f"  ⚠️ PARTIAL SUCCESS with {stats['errors']} errors")

            except Exception as e:
                print(f"  ❌ FAILED AGAIN: {e}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python retry_failed.py <failed_log.json>")
        sys.exit(1)

    retry_failed_documents(sys.argv[1])
```

### Use Case 5: Incremental Daily Ingestion

```python
#!/usr/bin/env python3
"""
Use Case 5: Incremental Daily Ingestion
Process only new documents added since last run
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

pipeline_dir = Path("/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines")
sys.path.insert(0, str(pipeline_dir))

from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

STATE_FILE = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json"

def load_ingestion_state():
    """Load last ingestion timestamp."""
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            return datetime.fromisoformat(state.get('last_run', '2000-01-01'))
    except:
        return datetime(2000, 1, 1)

def save_ingestion_state():
    """Save current timestamp as last ingestion."""
    state = {
        'last_run': datetime.now().isoformat(),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def incremental_ingest(source_directory: str):
    """Process only documents added since last run."""

    last_run = load_ingestion_state()
    print(f"Last ingestion: {last_run}")

    # Find new documents
    source_dir = Path(source_directory)
    new_files = [
        f for f in source_dir.glob("*.txt")
        if datetime.fromtimestamp(f.stat().st_mtime) > last_run
    ]

    print(f"Found {len(new_files)} new documents")

    if not new_files:
        print("No new documents to process")
        return

    # Process new documents
    with NER11ToNeo4jPipeline() as pipeline:
        for file_path in new_files:
            print(f"Processing: {file_path.name}")

            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            stats = pipeline.process_document(text, file_path.stem)
            print(f"  Entities: {stats['entities_extracted']}")

    # Update state
    save_ingestion_state()
    print("✅ Incremental ingestion complete")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python incremental_ingest.py <source_directory>")
        sys.exit(1)

    incremental_ingest(sys.argv[1])
```

---

## Error Handling

### Common Errors and Solutions

#### Error 1: NER11 API Connection Refused

**Error Message:**
```
requests.exceptions.ConnectionError: Failed to establish connection to http://localhost:8000
```

**Diagnosis:**
```bash
# Check if NER11 API is running
curl http://localhost:8000/health
```

**Solution:**
```bash
# Start NER11 API
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 api/ner11_api.py &

# Verify it's running
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

#### Error 2: Neo4j Connection Failed

**Error Message:**
```
neo4j.exceptions.ServiceUnavailable: Unable to connect to bolt://localhost:7687
```

**Diagnosis:**
```bash
# Check Neo4j status
sudo systemctl status neo4j
```

**Solution:**
```bash
# Start Neo4j
sudo systemctl start neo4j

# Wait for startup
sleep 10

# Verify connection
cypher-shell -u neo4j -p neo4j@openspg "RETURN 1;"
```

#### Error 3: No Entities Extracted

**Symptom:**
```python
stats = pipeline.process_document(text, doc_id)
# stats['entities_extracted'] = 0
```

**Diagnosis:**
- Document text too short (<50 characters)
- Document language not English
- NER11 API not detecting entities in text

**Solution:**
```python
# Add text length check
if len(text.strip()) < 50:
    print(f"Warning: Document too short ({len(text)} chars), skipping")
    continue

# Add entity extraction validation
stats = pipeline.process_document(text, doc_id)
if stats['entities_extracted'] == 0:
    print(f"Warning: No entities extracted from {doc_id}")
    # Log for manual review
    with open('/tmp/no_entities.log', 'a') as f:
        f.write(f"{doc_id}: {text[:100]}...\n")
```

#### Error 4: Validation Failed (Tier2 < Tier1)

**Symptom:**
```python
validation = pipeline.validate_ingestion()
# validation['tier2_greater_than_tier1'] = False
```

**Diagnosis:**
- Most entities assigned to tier1 categories
- Taxonomy needs more tier2/tier3 depth

**Solution:**
- This is a taxonomy configuration issue, not a pipeline error
- Continue ingestion (validation will pass with more tier2 entities over time)
- See MAINTENANCE_GUIDE.md for taxonomy expansion

---

## Performance Optimization

### Batch Processing Optimization

**Use connection pooling for large batches:**

```python
#!/usr/bin/env python3
"""
Optimized batch processing with connection pooling
"""
from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

# Initialize pipeline ONCE for entire batch
with NER11ToNeo4jPipeline() as pipeline:

    # Process multiple documents using same connection
    for doc_id, text in document_iterator:
        stats = pipeline.process_document(text, doc_id)

    # Connection closed automatically after batch
```

**Benefits:**
- Reduces Neo4j connection overhead
- Faster batch processing
- Better resource utilization

### Parallel Processing (Advanced)

**For very large batches (1000+ documents):**

```python
#!/usr/bin/env python3
"""
Parallel document processing (advanced)
WARNING: Requires sufficient system resources
"""
from multiprocessing import Pool
from ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

def process_document_worker(args):
    """Worker function for parallel processing."""
    doc_id, text = args

    # Each worker creates its own pipeline connection
    with NER11ToNeo4jPipeline() as pipeline:
        stats = pipeline.process_document(text, doc_id)
        return stats

# Create document list
documents = [
    ("doc_001", "text 1..."),
    ("doc_002", "text 2..."),
    # ... more documents
]

# Process in parallel (use number of CPU cores)
with Pool(processes=4) as pool:
    results = pool.map(process_document_worker, documents)

# Aggregate results
total_entities = sum(r['entities_extracted'] for r in results)
print(f"Total entities: {total_entities}")
```

**Considerations:**
- Only use for large batches (>1000 documents)
- Monitor system resources (CPU, memory, Neo4j connections)
- Limit to 4-8 parallel workers to avoid overwhelming Neo4j

---

## Best Practices

### DO

✅ **Always use hierarchical pipeline** (`05_ner11_to_neo4j_hierarchical.py`)
✅ **Validate enrichment** after ingestion
✅ **Check NER11 API** before starting batch jobs
✅ **Log document IDs** that fail for retry
✅ **Run validation queries** periodically
✅ **Monitor pipeline statistics** for anomalies

### DON'T

❌ **Don't use legacy pipelines** (`06_bulk_graph_ingestion.py`, etc.)
❌ **Don't bypass HierarchicalEntityProcessor**
❌ **Don't create nodes directly** with Cypher without enrichment
❌ **Don't ignore validation failures**
❌ **Don't run without error handling**

---

## Support & Documentation

**Pipeline Location:**
```
/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py
```

**Related Documentation:**
- `MAINTENANCE_GUIDE.md` - Schema health monitoring
- `TROUBLESHOOTING_GUIDE.md` - Common issues and solutions
- `MIGRATION_REPORT.md` - Historical context and results

**Logs:**
```
/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json
/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_final_stats.json
```

**Contact:** AEON Data Engineering Team

---

**Guide Prepared By:** AEON Documentation Specialist
**Last Updated:** 2025-12-12
**Next Review:** 2026-03-12 (quarterly)

**END OF PIPELINE USAGE GUIDE**
