# PIPELINE OPERATIONS GUIDE

**File:** PIPELINE_OPERATIONS_GUIDE.md
**Created:** 2025-12-12
**Version:** 1.0.0
**Purpose:** Complete operational documentation for production pipelines
**Status:** ACTIVE

---

## Table of Contents

1. [Pipeline Overview](#pipeline-overview)
2. [E30 Bulk Ingestion Pipeline](#e30-bulk-ingestion-pipeline)
3. [Hierarchical Entity Pipeline](#hierarchical-entity-pipeline)
4. [PROC-102 Kaggle Enrichment](#proc-102-kaggle-enrichment)
5. [Complete Workflow Example](#complete-workflow-example)
6. [Troubleshooting](#troubleshooting)

---

## Pipeline Overview

The AEON cybersecurity knowledge graph system uses three primary production pipelines:

| Pipeline | Purpose | Input | Output |
|----------|---------|-------|--------|
| **Hierarchical Entity Pipeline** | Process single documents with NER11 | Document text | Neo4j nodes + relationships |
| **E30 Bulk Ingestion** | Mass corpus processing | Training corpus directory | 15K+ hierarchical nodes |
| **PROC-102 Kaggle Enrichment** | CVE/CWE data enrichment | Kaggle dataset | CVSS scores + CWE relationships |

**Pipeline Dependencies:**
```
Training Corpus → Bulk Ingestion (E30) → Kaggle Enrichment (PROC-102) → Production Graph
                      ↓
              Hierarchical Pipeline
                  (per document)
```

---

## Hierarchical Entity Pipeline

### Overview

**File:** `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py`

The hierarchical pipeline processes individual documents through:
1. NER11 API entity extraction
2. Hierarchical taxonomy enrichment (566 types)
3. Neo4j node creation with MERGE
4. Relationship extraction and creation

### Critical Fix at Line 285

**Issue:** Hierarchical properties were not being applied to existing nodes during MERGE operations.

**Fix Applied (Lines 285-291):**
```cypher
ON MATCH SET
    n.ner_label = $ner_label,
    n.fine_grained_type = $fine_grained_type,
    n.specific_instance = $specific_instance,
    n.hierarchy_path = $hierarchy_path,
    n.tier = $tier,
    n.updated_at = datetime()
```

**Why This Matters:**
- Without `ON MATCH SET`, existing nodes (from 1.1M baseline) wouldn't receive hierarchical enrichment
- This ensures ALL nodes (new and existing) have consistent schema properties
- Preserves node identity while adding missing hierarchical metadata

### Key Features

**1. MERGE Strategy (Preserves Existing Nodes)**
- Uses `MERGE` instead of `CREATE` to avoid duplicates
- `ON CREATE SET` for new nodes
- `ON MATCH SET` for existing nodes (critical fix)
- Preserves 1,104,066 baseline nodes

**2. Hierarchical Enrichment**
- 566 fine-grained entity types
- 16 Neo4j super labels (Tier 1)
- Tier 2 specific types (actorType, malwareFamily, etc.)
- Hierarchy path tracking

**3. Relationship Extraction**
Pattern-based relationship creation:
- `EXPLOITS`: ThreatActor/Malware → Vulnerability
- `USES`: ThreatActor → Malware/AttackPattern
- `TARGETS`: ThreatActor → Asset/Organization
- `AFFECTS`: Vulnerability → Software/Asset
- `ATTRIBUTED_TO`: Campaign → ThreatActor
- `MITIGATES`: Control → Vulnerability
- `INDICATES`: Indicator → Malware/ThreatActor

**Proximity Validation:** Only creates relationships if entities are within 500 characters in source text.

### Usage

**Basic Usage:**
```python
from pipelines.ner11_to_neo4j_hierarchical import NER11ToNeo4jPipeline

# Initialize pipeline
with NER11ToNeo4jPipeline(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="neo4j@openspg",
    ner11_api_url="http://localhost:8000"
) as pipeline:

    # Process single document
    doc_stats = pipeline.process_document(
        text="APT29 exploited CVE-2020-0688...",
        document_id="apt29_report_2020"
    )

    print(f"Entities: {doc_stats['entities_extracted']}")
    print(f"Nodes: {doc_stats['nodes_created']}")
    print(f"Relationships: {doc_stats['relationships_created']}")

    # Validate ingestion
    validation = pipeline.validate_ingestion()
    print(f"Validation: {'✅ PASS' if validation['validation_passed'] else '❌ FAIL'}")
```

**Test Script:**
```bash
# Test with sample document
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines
python 05_ner11_to_neo4j_hierarchical.py

# Expected output:
# - Entity extraction from sample APT29 document
# - Hierarchical enrichment demonstration
# - Node creation with MERGE
# - Relationship extraction
# - Validation report
```

### Prerequisites

1. **Neo4j Running:**
   ```bash
   docker ps | grep openspg-neo4j
   ```

2. **NER11 API Available:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Python Dependencies:**
   ```bash
   pip install neo4j requests
   ```

### Output Statistics

```python
{
    "document_id": "apt29_report_2020",
    "entities_extracted": 15,      # From NER11 API
    "nodes_created": 12,            # New nodes + merged existing
    "relationships_created": 8,     # Pattern-based relationships
    "errors": 0
}
```

---

## E30 Bulk Ingestion Pipeline

### Overview

**File:** `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/06_bulk_graph_ingestion.py`

Mass processing pipeline for entire training corpus with:
- Idempotent processing (skip already processed)
- Progress tracking (tqdm)
- JSONL logging
- Comprehensive validation
- Rate limiting (2s delay to prevent spaCy overload)

### Architecture

**Components:**
1. **Document Discovery:** Finds all `.txt`, `.json`, `.md` files in corpus
2. **State Management:** Tracks processed documents to enable resume
3. **Batch Processing:** Progress updates every 10 documents
4. **Rate Limiting:** 2-second delay between NER11 API calls
5. **Validation:** Pre/post-ingestion metrics comparison

**State Files:**
- `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json` - Processing state
- `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl` - Document logs
- `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_final_stats.json` - Final statistics

### Command Line Usage

**Full Corpus Processing:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines

# Process all documents (with skip of already processed)
python 06_bulk_graph_ingestion.py

# Expected runtime: Several hours (depends on corpus size)
# Progress bar shows: documents processed, entities, nodes
```

**Limited Processing (Testing):**
```bash
# Process first 10 documents only
python 06_bulk_graph_ingestion.py --max-docs 10

# Process first 5 documents (quick test)
python 06_bulk_graph_ingestion.py --test-run
```

**Reprocess All (Ignore State):**
```bash
# Process all documents including previously processed
python 06_bulk_graph_ingestion.py --no-skip
```

**Custom Batch Size:**
```bash
# Update progress every 20 documents
python 06_bulk_graph_ingestion.py --batch-size 20
```

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--max-docs` | int | None | Limit documents to process (None = all) |
| `--no-skip` | flag | False | Reprocess already-processed documents |
| `--batch-size` | int | 10 | Progress update frequency |
| `--test-run` | flag | False | Quick test with first 5 documents |

### Processing Flow

```
[START] Initialize Processor
   ↓
[STEP 1] Record Baseline Metrics
   - Query Neo4j for current node count
   - Store baseline: 1,104,066 nodes (critical for validation)
   ↓
[STEP 2] Discover Documents
   - Find all .txt, .json, .md files in corpus
   - Filter out hashes.txt, summaries, __pycache__
   ↓
[STEP 3] Load Processing State
   - Read ingestion_state.json
   - Skip already processed documents (unless --no-skip)
   ↓
[STEP 4] Process Documents (with tqdm progress bar)
   For each document:
     - Generate document ID (SHA256 hash of path)
     - Read content (handle JSON extraction)
     - Call hierarchical pipeline
     - Rate limit (2s delay)
     - Log to JSONL
     - Update statistics
     - Save state every batch_size documents
   ↓
[STEP 5] Post-Ingestion Validation
   - Query Neo4j for final node count
   - Compare to baseline (must be >= baseline)
   - Check tier distribution (tier2 > tier1)
   - Generate validation report
   ↓
[STEP 6] Save Final Statistics
   - Write ingestion_final_stats.json
   - Print summary
   ↓
[END] Return exit code (0 = success, 1 = validation failed)
```

### Rate Limiting

**Why 2-second delay?**
- Prevents overwhelming spaCy container with concurrent requests
- Default: `rate_limit_delay: 2.0` seconds
- Can be adjusted in processor initialization

**Example Custom Rate:**
```python
processor = BulkGraphIngestionProcessor(rate_limit_delay=1.0)  # 1 second
```

### Idempotent Processing

**Document ID Generation:**
```python
def _get_document_id(self, file_path: Path) -> str:
    return hashlib.sha256(str(file_path).encode()).hexdigest()[:16]
```

**State Tracking:**
```json
{
  "processed_documents": [
    "a1b2c3d4e5f6g7h8",
    "i9j0k1l2m3n4o5p6"
  ],
  "failed_documents": [
    "q7r8s9t0u1v2w3x4"
  ],
  "last_updated": "2025-12-12T10:30:00"
}
```

**Resume Capability:**
- If processing interrupted, re-run same command
- Pipeline automatically skips processed documents
- Only processes new/failed documents

### Validation Criteria

**Critical Validations:**
1. **Node Preservation:** `total_nodes >= baseline_nodes`
2. **Hierarchy Depth:** `tier2_count > tier1_count`

**Validation Report:**
```json
{
  "timestamp": "2025-12-12T10:45:00",
  "baseline_nodes": 1104066,
  "current_nodes": 1119234,
  "nodes_added": 15168,
  "node_preservation": true,
  "tier1_count": 5432,
  "tier2_count": 12856,
  "tier2_greater_than_tier1": true,
  "validation_passed": true,
  "super_label_distribution": {
    "ThreatActor": 1234,
    "Malware": 2345,
    "Vulnerability": 3456
  }
}
```

### Expected Output

**Console Output:**
```
[2025-12-12 10:00:00] INFO: ================================================================================
[2025-12-12 10:00:00] INFO: BULK GRAPH INGESTION - CORPUS PROCESSING
[2025-12-12 10:00:00] INFO: ================================================================================
[2025-12-12 10:00:01] INFO: Recording baseline Neo4j metrics...
[2025-12-12 10:00:02] INFO: Baseline recorded: 1,104,066 nodes
[2025-12-12 10:00:03] INFO: Found 500 documents in corpus
[2025-12-12 10:00:04] INFO: Skipping 485 already processed documents
[2025-12-12 10:00:05] INFO: Processing 15 documents...

Processing documents: 100%|████████████████| 15/15 [00:35<00:00,  2.3s/doc]

[2025-12-12 10:00:40] INFO: Validating post-ingestion Neo4j state...
[2025-12-12 10:00:42] INFO: ✅ POST-INGESTION VALIDATION PASSED
[2025-12-12 10:00:42] INFO:   Nodes: 1,104,235 (baseline: 1,104,066)
[2025-12-12 10:00:42] INFO:   Added: 169 new nodes
[2025-12-12 10:00:42] INFO:   Tier 1: 45
[2025-12-12 10:00:42] INFO:   Tier 2: 124

================================================================================
BULK INGESTION PROGRESS SUMMARY
================================================================================

Documents:
  Found:     500
  Processed: 15
  Skipped:   485
  Failed:    0

Entities & Nodes:
  Entities extracted: 234
  Nodes created:      169
  Relationships:      98

Validation:
  Baseline nodes: 1,104,066
  Current nodes:  1,104,235
  Nodes added:    169
  Status: ✅ PASS

================================================================================
```

### Troubleshooting

**Problem:** "Neo4j container not running"
```bash
# Solution: Start Neo4j
docker start openspg-neo4j
docker ps | grep openspg-neo4j
```

**Problem:** "NER11 API error: Connection refused"
```bash
# Solution: Start NER11 container
docker start openspg-ner11
curl http://localhost:8000/health
```

**Problem:** "Validation failed: node count decreased"
```bash
# This is CRITICAL - check logs for errors
tail -100 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl

# Check for Neo4j connection issues
docker logs openspg-neo4j --tail 50
```

**Problem:** Processing is very slow
```bash
# Reduce rate limit (be careful not to overload spaCy)
# Edit line 92 in 06_bulk_graph_ingestion.py:
# rate_limit_delay: float = 1.0  # Reduced from 2.0
```

---

## PROC-102 Kaggle Enrichment

### Overview

**File:** `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/proc_102_kaggle_enrichment.sh`

Procedure to enrich existing CVE nodes with:
- CVSS v2, v3.1, v4 scores
- CVSS severity ratings
- CWE weakness type relationships

**Data Source:** Kaggle dataset `stanislavvinokur/cve-and-cwe-dataset-1999-2025`

### Prerequisites

**1. Kaggle API Credentials:**
```bash
# Install Kaggle CLI
pip install kaggle

# Create credentials file
mkdir -p ~/.kaggle
cat > ~/.kaggle/kaggle.json <<EOF
{
  "username": "your_kaggle_username",
  "key": "your_kaggle_api_key"
}
EOF
chmod 600 ~/.kaggle/kaggle.json
```

**Get API Key:**
1. Go to https://www.kaggle.com/settings
2. Scroll to "API" section
3. Click "Create New API Token"
4. Save downloaded `kaggle.json`

**2. Neo4j with APOC:**
```bash
# Verify APOC is installed
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  "RETURN apoc.version() AS version"
```

**3. Existing CVE Nodes:**
```bash
# Check CVE count (should be > 1000 from E30 ingestion)
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  -d neo4j \
  "MATCH (c:CVE) RETURN count(c) as total"
```

### Complete Procedure

**Execute:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts
bash proc_102_kaggle_enrichment.sh
```

**What Happens:**

1. **Pre-condition Checks**
   - Verify Neo4j container running
   - Check Kaggle credentials exist
   - Count existing CVE nodes

2. **Dataset Download**
   - Downloads `stanislavvinokur/cve-and-cwe-dataset-1999-2025` from Kaggle
   - Extracts CSV to `/tmp/kaggle_enrichment/`
   - Reports file size and row count

3. **Data Import to Neo4j**
   - Copies CSV to Neo4j import directory
   - Creates CWE constraint: `UNIQUE (c.id)`

4. **CVSS Score Enrichment**
   - Batch size: 5000 CVEs per batch
   - Enriches properties:
     - `cvssV31BaseScore` (float)
     - `cvssV2BaseScore` (float)
     - `cvssV4BaseScore` (float)
     - `cvssV31BaseSeverity` (CRITICAL/HIGH/MEDIUM/LOW)
     - `kaggle_enriched_timestamp` (datetime)

5. **CWE Relationship Creation**
   - Creates `CWE` nodes (if not exist)
   - Creates `IS_WEAKNESS_TYPE` relationships
   - Filters out invalid CWE IDs:
     - `NVD-CWE-Other`
     - `NVD-CWE-noinfo`
   - Sets relationship properties:
     - `source: "kaggle:cve_cwe_2025"`
     - `created_timestamp`

6. **Verification**
   - Reports CVSS coverage percentage
   - Reports CWE relationship count
   - Reports unique CWE count

7. **Cleanup**
   - Removes temporary files
   - Removes CSV from Neo4j import directory

### Expected Output

```bash
[2025-12-12 11:00:00] INFO: =========================================
[2025-12-12 11:00:00] INFO: PROC-102: Kaggle Dataset Enrichment
[2025-12-12 11:00:00] INFO: =========================================
[2025-12-12 11:00:01] INFO: Checking pre-conditions...
[2025-12-12 11:00:02] INFO: Found 234567 CVE nodes
[2025-12-12 11:00:03] INFO: Downloading Kaggle dataset: stanislavvinokur/cve-and-cwe-dataset-1999-2025
[2025-12-12 11:00:45] INFO: Downloaded: CVE_CWE_2025.csv (245M)
[2025-12-12 11:00:46] INFO: Dataset contains 256789 rows
[2025-12-12 11:00:47] INFO: Copying data to Neo4j import directory...
[2025-12-12 11:00:48] INFO: Creating CWE constraint...
[2025-12-12 11:00:49] INFO: Enriching CVEs with CVSS scores (batch size: 5000)...
[2025-12-12 11:05:23] INFO: batches: 52, total: 256789, errorMessages: []
[2025-12-12 11:05:24] INFO: Creating CVE→CWE IS_WEAKNESS_TYPE relationships (batch size: 5000)...
[2025-12-12 11:08:45] INFO: batches: 48, total: 238456, errorMessages: []
[2025-12-12 11:08:46] INFO: Verifying enrichment results...
[2025-12-12 11:08:47] INFO: CVSS Coverage:
total    | has_cvss31 | kaggle_enriched | cvss31_coverage_pct
234567   | 198234     | 256789         | 84.51
[2025-12-12 11:08:48] INFO: CWE Relationships:
cwe_relationships | unique_cwes
238456           | 987
[2025-12-12 11:08:49] INFO: Cleaning up temporary files...
[2025-12-12 11:08:50] INFO: =========================================
[2025-12-12 11:08:50] INFO: PROC-102 COMPLETED SUCCESSFULLY
[2025-12-12 11:08:50] INFO: =========================================
```

### CVSS Enrichment Details

**Properties Added to CVE Nodes:**
```cypher
// Example enriched CVE node
(cve:CVE {
  id: "CVE-2020-0688",
  description: "...",
  cvssV31BaseScore: 8.8,           // Added by PROC-102
  cvssV2BaseScore: 9.0,            // Added by PROC-102
  cvssV4BaseScore: 8.5,            // Added by PROC-102
  cvssV31BaseSeverity: "HIGH",     // Added by PROC-102
  kaggle_enriched_timestamp: datetime("2025-12-12T11:05:23") // Added by PROC-102
})
```

**Batch Processing Query:**
```cypher
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///CVE_CWE_2025.csv' AS row RETURN row",
  "MATCH (cve:CVE {id: row.`CVE-ID`})
   SET cve.cvssV31BaseScore = CASE WHEN row.`CVSS-V3` IS NOT NULL AND row.`CVSS-V3` <> ''
                                   THEN toFloat(row.`CVSS-V3`) ELSE cve.cvssV31BaseScore END,
       cve.cvssV2BaseScore = CASE WHEN row.`CVSS-V2` IS NOT NULL AND row.`CVSS-V2` <> ''
                                  THEN toFloat(row.`CVSS-V2`) ELSE cve.cvssV2BaseScore END,
       cve.cvssV4BaseScore = CASE WHEN row.`CVSS-V4` IS NOT NULL AND row.`CVSS-V4` <> ''
                                  THEN toFloat(row.`CVSS-V4`) ELSE cve.cvssV4BaseScore END,
       cve.cvssV31BaseSeverity = CASE WHEN row.SEVERITY IS NOT NULL AND row.SEVERITY <> ''
                                      THEN toUpper(trim(row.SEVERITY)) ELSE cve.cvssV31BaseSeverity END,
       cve.kaggle_enriched_timestamp = datetime()
   RETURN count(*)",
  {batchSize: 5000, parallel: false}
) YIELD batches, total, errorMessages
RETURN batches, total, errorMessages
```

### CWE Relationship Details

**Relationship Pattern:**
```cypher
(cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
```

**Example:**
```cypher
(cve:CVE {id: "CVE-2020-0688"})-[:IS_WEAKNESS_TYPE {
  source: "kaggle:cve_cwe_2025",
  created_timestamp: datetime("2025-12-12T11:08:23")
}]->(cwe:CWE {
  id: "CWE-502",
  source: "kaggle:cve_cwe_2025",
  created_timestamp: datetime("2025-12-12T11:08:23")
})
```

**Filtering Invalid CWE IDs:**
- Excludes: `NVD-CWE-Other`, `NVD-CWE-noinfo`
- Only creates relationships for valid CWE identifiers

### Troubleshooting

**Problem:** "Kaggle credentials not found"
```bash
# Solution: Create credentials file
mkdir -p ~/.kaggle
# Download kaggle.json from https://www.kaggle.com/settings
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

**Problem:** "Dataset download failed"
```bash
# Solution: Test Kaggle CLI manually
kaggle datasets download stanislavvinokur/cve-and-cwe-dataset-1999-2025 -p /tmp/test

# Check authentication
kaggle datasets list --user your_kaggle_username
```

**Problem:** "APOC procedure not found"
```bash
# Solution: Verify APOC installation
docker exec openspg-neo4j ls /var/lib/neo4j/plugins/
# Should show: apoc-5.x.x-core.jar

# If missing, reinstall Neo4j with APOC
```

**Problem:** Low CVSS coverage percentage
```bash
# This is expected - not all CVEs have CVSS scores in dataset
# Coverage typically 60-85% depending on CVE publication dates
# Check specific CVE:
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  -d neo4j \
  "MATCH (c:CVE {id: 'CVE-2020-0688'}) RETURN c"
```

---

## Complete Workflow Example

### End-to-End Processing

**Scenario:** Process new cybersecurity corpus and enrich with Kaggle data

**Step 1: Prepare Corpus**
```bash
# Add new documents to training data
cp /path/to/new/reports/*.txt \
   /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data/new_batch/
```

**Step 2: Verify Prerequisites**
```bash
# Check all containers running
docker ps | grep -E "openspg-(neo4j|ner11)"

# Test NER11 API
curl http://localhost:8000/health

# Test Neo4j
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  "MATCH (n) RETURN count(n) as total LIMIT 1"
```

**Step 3: Run Bulk Ingestion (E30)**
```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines

# Test with first 5 documents
python 06_bulk_graph_ingestion.py --test-run

# If successful, run full ingestion
python 06_bulk_graph_ingestion.py

# Monitor progress (separate terminal)
tail -f /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl
```

**Step 4: Verify Ingestion Results**
```bash
# Check final statistics
cat /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_final_stats.json

# Verify specific entities in Neo4j
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  -d neo4j \
  "MATCH (n) WHERE n.tier IS NOT NULL RETURN labels(n), n.tier, count(*) ORDER BY count(*) DESC LIMIT 10"
```

**Step 5: Run Kaggle Enrichment (PROC-102)**
```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts

# Execute enrichment procedure
bash proc_102_kaggle_enrichment.sh

# Expected runtime: 5-10 minutes
# Monitor log: tail -f /var/log/aeon/proc_102_*.log
```

**Step 6: Validate Final Graph**
```bash
# Check CVSS coverage
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  -d neo4j \
  "MATCH (c:CVE)
   RETURN count(c) as total_cves,
          count(c.cvssV31BaseScore) as with_cvss,
          round(100.0 * count(c.cvssV31BaseScore) / count(c), 2) as coverage_pct"

# Check CWE relationships
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  -d neo4j \
  "MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
   RETURN count(r) as relationships, count(DISTINCT cwe) as unique_cwes"

# Check hierarchical properties
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  -d neo4j \
  "MATCH (n)
   WHERE n.fine_grained_type IS NOT NULL
   RETURN n.tier, count(*) as count
   ORDER BY n.tier"
```

**Step 7: Sample Queries**
```bash
# Find high-severity CVEs with CWE mappings
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  -d neo4j \
  "MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
   WHERE cve.cvssV31BaseSeverity = 'HIGH'
   RETURN cve.id, cve.cvssV31BaseScore, cwe.id
   ORDER BY cve.cvssV31BaseScore DESC
   LIMIT 10"

# Find threat actors and their malware
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  -d neo4j \
  "MATCH (ta:ThreatActor)-[r:USES]->(m:Malware)
   WHERE ta.fine_grained_type IS NOT NULL
   RETURN ta.name, ta.fine_grained_type, collect(m.name) as malware
   LIMIT 10"
```

### Performance Expectations

| Phase | Duration | Output |
|-------|----------|--------|
| E30 Bulk Ingestion (500 docs) | 30-40 minutes | ~15K nodes, ~10K relationships |
| PROC-102 Enrichment (250K CVEs) | 5-10 minutes | CVSS scores + CWE relationships |
| Total Processing | 35-50 minutes | Production-ready knowledge graph |

**Optimization Tips:**
- Run ingestion during off-hours (less system load)
- Use SSD storage for Neo4j data
- Allocate sufficient memory to Neo4j (4-8GB recommended)
- Monitor Docker resource usage: `docker stats`

---

## Troubleshooting

### Common Issues

**1. Rate Limiting Issues**

**Symptom:** NER11 API returning 429 errors
```bash
# Check NER11 container logs
docker logs openspg-ner11 --tail 100
```

**Solution:**
```python
# Increase rate_limit_delay in bulk processor
# Edit line 92 in 06_bulk_graph_ingestion.py:
rate_limit_delay: float = 3.0  # Increased from 2.0
```

**2. Neo4j Memory Issues**

**Symptom:** "Out of memory" errors during batch processing
```bash
# Check Neo4j heap usage
docker exec openspg-neo4j neo4j-admin report
```

**Solution:**
```bash
# Increase Neo4j heap size
docker stop openspg-neo4j
# Edit neo4j.conf: dbms.memory.heap.max_size=4G
docker start openspg-neo4j
```

**3. State File Corruption**

**Symptom:** Processing starts from beginning despite previous progress
```bash
# Check state file
cat /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json
```

**Solution:**
```bash
# Backup corrupted state
mv ingestion_state.json ingestion_state.json.backup

# Recreate from JSONL log
python /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/rebuild_state_from_log.py
```

**4. Validation Failures**

**Symptom:** Node count decreased after ingestion
```bash
# This is CRITICAL - investigate immediately
grep "Node count decreased" /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/*.log
```

**Solution:**
```bash
# Check for accidental DELETE queries
docker exec openspg-neo4j cat /var/log/neo4j/query.log | grep -i delete

# Restore from backup if necessary
docker exec openspg-neo4j neo4j-admin restore --from=/backups/latest
```

### Diagnostic Commands

**Check System Health:**
```bash
# All containers running?
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Neo4j accessible?
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "RETURN 1"

# NER11 API healthy?
curl -f http://localhost:8000/health || echo "NER11 API DOWN"

# Disk space available?
df -h | grep -E "(Filesystem|neo4j|ner11)"
```

**Performance Monitoring:**
```bash
# Watch processing progress
watch -n 5 'tail -1 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl'

# Monitor Neo4j query performance
docker exec openspg-neo4j cypher-shell \
  -u neo4j -p neo4j@openspg \
  "CALL dbms.queryJmx('org.neo4j:*') YIELD name, attributes WHERE name =~ '.*Store.*' RETURN name, attributes"

# Check Docker resource usage
docker stats --no-stream openspg-neo4j openspg-ner11
```

### Recovery Procedures

**Resume After Crash:**
```bash
# 1. Check what was last processed
tail -20 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl

# 2. Verify state file is intact
cat /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json | jq '.last_updated'

# 3. Resume processing (automatic resume)
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines
python 06_bulk_graph_ingestion.py
```

**Reset Processing State:**
```bash
# WARNING: This will reprocess all documents
rm /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json
python 06_bulk_graph_ingestion.py --no-skip
```

---

## Pipeline Maintenance

### Regular Maintenance Tasks

**Weekly:**
- Backup Neo4j database
- Review processing logs for errors
- Check disk space usage

**Monthly:**
- Update Kaggle dataset (PROC-102)
- Verify hierarchical schema consistency
- Review relationship extraction patterns

**Quarterly:**
- Archive old processing logs
- Update NER11 model if available
- Performance benchmark testing

### Backup Procedures

**Neo4j Database Backup:**
```bash
# Stop Neo4j
docker stop openspg-neo4j

# Create backup
docker run --rm \
  -v openspg-neo4j-data:/data \
  -v $(pwd)/backups:/backup \
  neo4j:5.23.0 \
  neo4j-admin database dump neo4j --to-path=/backup

# Restart Neo4j
docker start openspg-neo4j
```

**State File Backup:**
```bash
# Backup processing state
cp /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json \
   /home/jim/backups/ingestion_state_$(date +%Y%m%d).json
```

---

## Contact & Support

**Documentation Location:**
- This guide: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/PIPELINE_OPERATIONS_GUIDE.md`
- Related docs: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/`

**Pipeline Source Files:**
- Hierarchical: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py`
- Bulk: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/06_bulk_graph_ingestion.py`
- PROC-102: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/scripts/proc_102_kaggle_enrichment.sh`

**Log Files:**
- Ingestion log: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/neo4j_ingestion.jsonl`
- State file: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/ingestion_state.json`
- PROC-102 logs: `/var/log/aeon/proc_102_*.log`

---

**Version:** 1.0.0
**Last Updated:** 2025-12-12
**Status:** Production Ready
