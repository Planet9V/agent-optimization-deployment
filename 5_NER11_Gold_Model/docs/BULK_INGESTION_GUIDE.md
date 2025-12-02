# Bulk Graph Ingestion Guide

**Task 2.4 - Bulk Graph Ingestion Processor**

Complete guide for mass Neo4j graph population from training corpus.

## Overview

The Bulk Graph Ingestion Processor processes all available documents from the training corpus, extracts entities via NER11, enriches them with hierarchical taxonomy, and ingests into Neo4j knowledge graph.

### Key Features

- **Mass Processing**: Process entire training corpus (42+ documents)
- **Critical Node Preservation**: Maintains existing 1,104,066 nodes
- **Idempotent Processing**: Skip already processed documents
- **Progress Tracking**: Real-time progress with tqdm
- **Comprehensive Logging**: JSONL format for processing history
- **Robust Validation**: Pre/post-ingestion validation
- **Error Recovery**: Continue processing on errors
- **State Management**: Resume interrupted sessions

### Target Metrics

- **Documents**: Process all 42+ corpus documents
- **New Nodes**: Add 15,000+ hierarchical nodes
- **Node Preservation**: CRITICAL - existing 1,104,066 nodes must not decrease
- **Tier Distribution**: Tier 2 entities > Tier 1 entities
- **Relationships**: Create entity relationships based on patterns

## Prerequisites

### 1. Neo4j Database

Ensure Neo4j is running with correct credentials:

```bash
# Check Neo4j status
docker ps | grep neo4j

# If not running, start it
docker start neo4j-openspg
```

**Connection Details:**
- URI: `bolt://localhost:7687`
- Username: `neo4j`
- Password: `neo4j@openspg`

### 2. NER11 API

The NER11 API must be running for entity extraction:

```bash
# Start NER11 API (from project root)
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python serve_model.py

# Verify API is running
curl http://localhost:8000/health
```

### 3. Training Corpus

Verify training corpus is available:

```bash
ls -la /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data/
```

Expected: 42+ `.txt` and `.json` files containing cybersecurity documents.

### 4. Required Python Packages

```bash
pip install tqdm neo4j requests
```

## Usage

### Quick Start - Test Run

**RECOMMENDED:** Always run test first to validate setup:

```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# Run prerequisite checks
python pipelines/test_bulk_ingestion.py

# Expected output:
# ✅ ALL PREREQUISITES MET
# ✅ TEST SUCCESSFUL - READY FOR FULL CORPUS PROCESSING
```

The test processes 3 documents and validates:
- Document discovery works
- Entity extraction successful
- Node creation with MERGE works
- Existing nodes preserved
- Tier distribution correct

### Full Corpus Processing

After successful test run:

```bash
# Process entire corpus
python pipelines/06_bulk_graph_ingestion.py

# Process with document limit
python pipelines/06_bulk_graph_ingestion.py --max-docs 20

# Process all documents (including previously processed)
python pipelines/06_bulk_graph_ingestion.py --no-skip

# Custom batch size for progress updates
python pipelines/06_bulk_graph_ingestion.py --batch-size 5
```

### Command Line Options

```
--max-docs N          Maximum documents to process (default: all)
--no-skip             Process all documents, including already processed
--batch-size N        Documents per progress update (default: 10)
--test-run            Test mode: process first 5 documents only
```

## Processing Flow

### Phase 1: Initialization

1. **Load State**: Check for previously processed documents
2. **Connect Neo4j**: Establish database connection
3. **Initialize Pipeline**: Load hierarchical processor and mapper
4. **Record Baseline**: Capture current Neo4j node count

```
Baseline Metrics:
  Total nodes: 1,104,066
  Tier 1 entities: X
  Tier 2 entities: Y
```

### Phase 2: Document Discovery

1. **Scan Corpus**: Find all `.txt` and `.json` files
2. **Filter**: Exclude non-document files (hashes, summaries)
3. **Check State**: Identify already processed documents
4. **Build Queue**: Create processing queue

```
Found 42 documents in corpus
Skipping 0 already processed documents
Processing 42 documents...
```

### Phase 3: Document Processing

For each document:

1. **Read Content**: Load text from file (handle JSON extraction)
2. **NER11 Extraction**: Extract entities via API
3. **Hierarchical Enrichment**: Add 566-type taxonomy properties
4. **Neo4j Ingestion**: MERGE nodes (preserve existing)
5. **Relationship Extraction**: Create entity relationships
6. **Log Results**: Record to JSONL log

```
Processing documents: 100%|████████████| 42/42 [02:15<00:00, 0.31doc/s]
Processed 42, Entities: 1,847, Nodes: 15,234
```

### Phase 4: Validation

1. **Post-Ingestion Check**: Query Neo4j for current state
2. **Compare Baseline**: Verify nodes >= baseline
3. **Tier Distribution**: Validate tier 2 > tier 1
4. **Generate Report**: Create validation report

```
Validation:
  Baseline nodes: 1,104,066
  Current nodes:  1,119,300
  Nodes added:    15,234
  Status: ✅ PASS
```

## Output Files

### 1. Processing Log

**File**: `/logs/neo4j_ingestion.jsonl`

JSONL format with one entry per document:

```json
{
  "timestamp": "2025-12-01T14:23:45.123456",
  "document_path": "training_data/custom_data/source_files/...",
  "document_id": "abc123def456",
  "status": "success",
  "statistics": {
    "entities_extracted": 45,
    "nodes_created": 38,
    "relationships_created": 12,
    "errors": 0
  }
}
```

### 2. State File

**File**: `/logs/ingestion_state.json`

Tracks processed documents for idempotent processing:

```json
{
  "processed_documents": [
    "abc123def456",
    "def789ghi012"
  ],
  "failed_documents": [],
  "last_updated": "2025-12-01T14:30:00.000000"
}
```

### 3. Final Statistics

**File**: `/logs/ingestion_final_stats.json`

Complete processing statistics:

```json
{
  "session_start": "2025-12-01T14:20:00.000000",
  "session_end": "2025-12-01T14:30:00.000000",
  "documents_found": 42,
  "documents_processed": 42,
  "documents_skipped": 0,
  "documents_failed": 0,
  "total_entities": 1847,
  "total_nodes_created": 15234,
  "total_relationships": 4521,
  "validation_report": {
    "baseline_nodes": 1104066,
    "current_nodes": 1119300,
    "nodes_added": 15234,
    "node_preservation": true,
    "tier2_greater_than_tier1": true,
    "validation_passed": true
  }
}
```

## Validation Criteria

### Critical Validations

1. **Node Preservation** (CRITICAL)
   - Pre-ingestion: 1,104,066 nodes
   - Post-ingestion: >= 1,104,066 nodes
   - **MUST PASS**: Existing nodes cannot be deleted

2. **Tier Distribution** (IMPORTANT)
   - Tier 2 entity count > Tier 1 entity count
   - Validates hierarchical taxonomy depth

3. **Hierarchical Properties** (REQUIRED)
   - Nodes have `fine_grained_type` property
   - Nodes have `tier` property
   - Nodes have `hierarchy_path` property

### Validation Report Format

```
POST-INGESTION VALIDATION REPORT
================================

Baseline Metrics:
  Total nodes: 1,104,066
  Tier 1 count: 234,567
  Tier 2 count: 567,890

Current Metrics:
  Total nodes: 1,119,300
  Tier 1 count: 235,123
  Tier 2 count: 583,124

Changes:
  Nodes added: 15,234
  Tier 1 added: 556
  Tier 2 added: 15,234

Validation Results:
  ✅ Node count preserved (1,119,300 >= 1,104,066)
  ✅ Tier 2 > Tier 1 (583,124 > 235,123)
  ✅ Hierarchical properties present

Overall: ✅ VALIDATION PASSED
```

## Error Handling

### Common Issues

#### 1. Neo4j Connection Failed

```
Error: Failed to connect to Neo4j at bolt://localhost:7687
```

**Solution**:
```bash
# Check Neo4j is running
docker ps | grep neo4j

# Start if not running
docker start neo4j-openspg

# Verify connection
curl http://localhost:7474
```

#### 2. NER11 API Not Available

```
Error: NER11 API error: Connection refused
```

**Solution**:
```bash
# Start NER11 API
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python serve_model.py

# In another terminal, verify
curl http://localhost:8000/health
```

#### 3. Corpus Not Found

```
Error: Corpus directory not found
```

**Solution**:
```bash
# Verify corpus path
ls -la /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data/

# Check for documents
find /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data/ -name "*.txt" -o -name "*.json"
```

#### 4. Validation Failed - Node Count Decreased

```
❌ CRITICAL: Node count decreased! 1,100,000 < 1,104,066
```

**This should NEVER happen.** If it does:

1. **STOP PROCESSING** immediately
2. Check Neo4j query logs for DELETE operations
3. Review MERGE query implementation
4. Restore from backup if available
5. Report issue - this is a critical bug

### Recovery from Interruption

If processing is interrupted (Ctrl+C, network failure, etc.):

```bash
# Resume processing - will skip already processed documents
python pipelines/06_bulk_graph_ingestion.py

# Check state file to see progress
cat logs/ingestion_state.json

# Check log for last processed document
tail logs/neo4j_ingestion.jsonl
```

The processor is **idempotent** - it tracks processed documents and skips them on resume.

## Performance Optimization

### Batch Processing

Adjust batch size for progress updates:

```bash
# Larger batch = fewer progress updates (faster)
python pipelines/06_bulk_graph_ingestion.py --batch-size 20

# Smaller batch = more frequent updates (slower but better visibility)
python pipelines/06_bulk_graph_ingestion.py --batch-size 5
```

### Document Limits

For testing or phased processing:

```bash
# Process first 10 documents
python pipelines/06_bulk_graph_ingestion.py --max-docs 10

# Process next batch (skips first 10 already processed)
python pipelines/06_bulk_graph_ingestion.py --max-docs 20
```

### Neo4j Performance

For large-scale ingestion:

1. **Increase heap size** (edit `neo4j.conf`):
   ```
   dbms.memory.heap.initial_size=2g
   dbms.memory.heap.max_size=4g
   ```

2. **Disable unnecessary indexes** during ingestion (re-enable after)

3. **Monitor memory**: `docker stats neo4j-openspg`

## Verification

### Check Ingestion Results

```cypher
// Total node count
MATCH (n) RETURN count(n) as total_nodes;

// Nodes by super label
CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (n:' + label + ') RETURN count(n) as count', {})
YIELD value
RETURN label, value.count as count
ORDER BY count DESC;

// Tier distribution
MATCH (n)
WHERE n.tier IS NOT NULL
RETURN n.tier as tier, count(n) as count;

// Hierarchical properties
MATCH (n)
WHERE n.fine_grained_type IS NOT NULL
RETURN n.fine_grained_type, count(n) as count
ORDER BY count DESC
LIMIT 20;

// Sample enriched nodes
MATCH (n:ThreatActor)
RETURN n.name, n.ner_label, n.fine_grained_type, n.tier, n.hierarchy_path
LIMIT 10;
```

### Verify Relationships

```cypher
// Relationship counts by type
MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(r) as count
ORDER BY count DESC;

// Sample relationships
MATCH (source)-[r:EXPLOITS]->(target)
RETURN source.name, type(r), target.name
LIMIT 10;
```

## Integration with Phase 2

This processor completes **Task 2.4** of Phase 2:

- ✅ **Task 2.1**: Hierarchical Entity Processor (566 types)
- ✅ **Task 2.2**: NER11 to Neo4j Mapper (60→16 labels)
- ✅ **Task 2.3**: Neo4j Hierarchical Pipeline (single document)
- ✅ **Task 2.4**: Bulk Graph Ingestion (corpus processing) ← **THIS**

### Next Steps

After successful bulk ingestion:

1. **Task 2.5**: Search API implementation
2. **Phase 3**: Advanced graph analytics
3. **Production deployment**: Scale to larger corpora

## Troubleshooting

### Logs Location

```bash
# Processing log (JSONL)
tail -f logs/neo4j_ingestion.jsonl

# State file
cat logs/ingestion_state.json

# Final statistics
cat logs/ingestion_final_stats.json
```

### Debug Mode

For detailed debugging:

```python
# Edit 06_bulk_graph_ingestion.py
# Change logging level:
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Manual Validation

Run validation independently:

```python
from pipelines.import_bulk_ingestion import BulkGraphIngestionProcessor

processor = BulkGraphIngestionProcessor()
validation = processor.pipeline.validate_ingestion()

print(f"Total nodes: {validation['total_nodes']:,}")
print(f"Validation: {'PASS' if validation['validation_passed'] else 'FAIL'}")
processor.close()
```

## Success Criteria

Processing is successful when:

1. ✅ All documents processed (or max_docs reached)
2. ✅ Zero critical errors
3. ✅ Node count >= 1,104,066 (baseline preserved)
4. ✅ Tier 2 count > Tier 1 count
5. ✅ 15,000+ new nodes created
6. ✅ Relationships created successfully
7. ✅ Validation report shows PASS

## Support

For issues or questions:

1. Check logs: `logs/neo4j_ingestion.jsonl`
2. Review validation report in `logs/ingestion_final_stats.json`
3. Verify prerequisites with `test_bulk_ingestion.py`
4. Check Neo4j and NER11 API are running

---

**Document Version**: 1.0.0
**Last Updated**: 2025-12-01
**Task**: TASKMASTER Phase 2, Task 2.4
