# PROCEDURE MAINTENANCE GUIDE - TRUTH KEEPING

**Generated**: 2025-12-12
**Purpose**: Ensure all procedures stay aligned with actual system state
**Status**: Active Reference Document

---

## The Problem

**Too many old files** → confusion about what's real
**Outdated procedures** → waste time, break things
**No single truth** → everyone guessing

## The Solution

**Every procedure MUST reference actual system state** from verified truth sources.

---

## SECTION 1: TRUTH SOURCES

### 1.1 API Truth Source

**File**: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/ALL_APIS_MASTER_TABLE.md`

**Contains**: 181 production APIs
- 5 NER11 APIs (port 8000, no auth)
- 135 Phase B APIs (port 8000, auth required)
- 41 Next.js APIs (port 3000, Clerk auth)

**How to Use**:
```bash
# Always reference specific API from master table
# Example: "Use API #43 (POST /ner) from ALL_APIS_MASTER_TABLE.md"

# Verify API exists
grep -n "POST /ner" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/ALL_APIS_MASTER_TABLE.md

# Get exact curl example
grep -A 1 "Extract Entities" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/ALL_APIS_MASTER_TABLE.md
```

**When to Update Procedures**:
- New API added → Update all affected procedures
- API endpoint changed → Update references
- Auth requirements changed → Update access examples

---

### 1.2 Schema Truth Source

**File**: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE.md`

**Contains**:
- **631 Node Labels** (17 super labels)
- **183 Relationship Types**
- **1M+ nodes** in production

**Key Super Labels**:
```
Vulnerability (314,538 nodes)
Measurement (297,158 nodes)
Asset (200,275 nodes)
Control (65,199 nodes)
Organization (56,144 nodes)
Indicator (11,601 nodes)
ThreatActor (10,599 nodes)
Protocol (8,776 nodes)
Location (4,830 nodes)
Technique (3,526 nodes)
Event (2,291 nodes)
Software (1,694 nodes)
Malware (302 nodes)
PsychTrait (161 nodes)
EconomicMetric (39 nodes)
Role (15 nodes)
Campaign (1 node)
```

**How to Use**:
```bash
# Verify label exists before using in procedure
grep "fine_grained_type.*vulnerability" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE.md

# Get relationship types
grep -A 10 "Complete Relationship Types" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE.md
```

**When to Update Procedures**:
- New label added → Update Neo4j queries
- Property changed → Update MATCH patterns
- Relationship type changed → Update traversals

---

### 1.3 Qdrant Collections Truth Source

**Location**: `localhost:6333`

**Current Collections** (18 total):
```
ner11_threat_intel
phase-b-activation
ner11_model_registry
ner11_vendor_equipment
aeon-ice
aeon-final
ner11_entities_hierarchical
aeon-review
aeon-execution
phase_b_qa_reports
ner11_sbom
ner11_risk_scoring
aeon-actual-system
aeon-sprint1
ner11_remediation
development_process
taxonomy_embeddings
aeon_session_state
```

**How to Verify**:
```bash
# List all collections
python3 -c "
from qdrant_client import QdrantClient
client = QdrantClient('localhost', port=6333)
collections = client.get_collections()
for c in collections.collections:
    print(f'{c.name}: {c.vectors_count} vectors')
"

# Verify collection exists before referencing
python3 -c "
from qdrant_client import QdrantClient
client = QdrantClient('localhost', port=6333)
try:
    info = client.get_collection('ner11_threat_intel')
    print(f'Collection exists: {info.vectors_count} vectors')
except:
    print('Collection NOT found')
"
```

**When to Update Procedures**:
- New collection created → Update search procedures
- Collection renamed → Update references
- Vector dimension changed → Update ingestion scripts

---

### 1.4 Running Containers Truth Source

**How to Verify**:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Current Production Containers**:
```
ner11-gold-api       (Port 8000 - NER APIs)
openspg-neo4j        (Port 7687, 7474 - Neo4j)
openspg-qdrant       (Port 6333 - Vector DB)
aeon-saas-dev        (Port 3000 - Next.js)
aeon-postgres-dev    (Port 5432 - PostgreSQL)
openspg-mysql        (Port 3306 - MySQL)
openspg-redis        (Port 6379 - Redis)
openspg-minio        (Port 9000 - Object storage)
openspg-server       (Port 8887 - OpenSPG)
```

**When to Update Procedures**:
- Container renamed → Update connection strings
- Port changed → Update API access examples
- New service added → Document integration points

---

## SECTION 2: WHEN TO UPDATE PROCEDURES

### 2.1 API Changes Trigger Updates

**Event**: New API added to ALL_APIS_MASTER_TABLE.md

**Affected Procedures**: Any procedure that deals with that domain

**Example**:
```
New API: POST /api/v2/equipment/scan-status
Affected: PROC-103-equipment-monitoring.md
Action: Add section showing how to use scan-status API
```

**Update Checklist**:
- [ ] Add API reference with number from master table
- [ ] Update curl examples with actual endpoint
- [ ] Update auth headers if changed
- [ ] Test the actual API call
- [ ] Document expected responses

---

### 2.2 Schema Changes Trigger Updates

**Event**: New label or relationship type added to COMPLETE_SCHEMA_REFERENCE.md

**Affected Procedures**: Any procedure with Neo4j queries

**Example**:
```
New Label: ScanResult (fine_grained_type: scan_result)
Affected: PROC-104-security-scanning.md
Action: Update MATCH patterns to use new label
```

**Update Checklist**:
- [ ] Update MATCH patterns with correct label names
- [ ] Update WHERE clauses with correct property names
- [ ] Update CREATE statements with new structure
- [ ] Test queries return expected results
- [ ] Update example outputs

---

### 2.3 Data Source Changes Trigger Updates

**Event**: Qdrant collection renamed/created/deleted

**Affected Procedures**: Any procedure that searches or ingests to that collection

**Example**:
```
Collection renamed: threat_intel → ner11_threat_intel
Affected: PROC-101-threat-ingestion.md
Action: Update collection references in search/insert
```

**Update Checklist**:
- [ ] Update collection names in code examples
- [ ] Verify collection exists before documenting
- [ ] Update vector dimensions if changed
- [ ] Test search/insert operations
- [ ] Update sample queries

---

### 2.4 Infrastructure Changes Trigger Updates

**Event**: Container renamed, port changed, service upgraded

**Affected Procedures**: Any procedure accessing that service

**Example**:
```
Event: Neo4j upgraded, port changed 7687 → 7688
Affected: All procedures with Neo4j connections
Action: Update bolt:// connection strings
```

**Update Checklist**:
- [ ] Update connection strings (host, port)
- [ ] Update authentication if changed
- [ ] Update docker exec commands with new container names
- [ ] Test connections work
- [ ] Update troubleshooting sections

---

## SECTION 3: HOW TO WRITE PROCEDURES

### 3.1 Procedure Template (Updated)

```markdown
# PROC-XXX: [Procedure Title]

**Category**: [Ingestion/Query/Analysis/Maintenance]
**Last Updated**: YYYY-MM-DD
**Status**: Active

---

## REFERENCES

**APIs Used** (from ALL_APIS_MASTER_TABLE.md):
- API #43: POST /ner (Extract entities)
- API #67: POST /search/semantic (Vector search)

**Schema Elements** (from COMPLETE_SCHEMA_REFERENCE.md):
- Labels: Vulnerability (fine_grained_type: vulnerability)
- Relationships: EXPLOITS, AFFECTS, MITIGATES

**Data Sources**:
- Qdrant Collection: ner11_threat_intel (verified 2025-12-12)
- Neo4j Database: bolt://localhost:7687

**Containers**:
- ner11-gold-api (port 8000)
- openspg-neo4j (port 7687)

---

## PREREQUISITES

### Verification Steps

1. **Verify APIs are available**:
   ```bash
   curl http://localhost:8000/health
   # Expected: {"status": "healthy", "model": "ner11"}
   ```

2. **Verify Neo4j connection**:
   ```bash
   docker exec openspg-neo4j cypher-shell -u neo4j -p password "RETURN 1"
   # Expected: 1
   ```

3. **Verify Qdrant collection exists**:
   ```bash
   python3 -c "
   from qdrant_client import QdrantClient
   client = QdrantClient('localhost', port=6333)
   info = client.get_collection('ner11_threat_intel')
   print(f'Vectors: {info.vectors_count}')
   "
   ```

---

## EXECUTION STEPS

### Step 1: [First Action]

**Command**:
```bash
# Actual tested command
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"APT29 exploited CVE-2024-12345"}'
```

**Expected Result**:
```json
{
  "entities": [
    {"text": "APT29", "label": "threat_actor"},
    {"text": "CVE-2024-12345", "label": "vulnerability"}
  ]
}
```

**Validation**:
```bash
# Verify entities were extracted
echo $result | jq '.entities | length'
# Expected: > 0
```

---

### Step 2: [Second Action]

**Neo4j Query** (using actual schema):
```cypher
MATCH (v:Vulnerability {fine_grained_type: 'vulnerability'})
WHERE v.cve_id = 'CVE-2024-12345'
RETURN v.cvssV31BaseSeverity, v.epss_score
```

**Expected Result**:
```
cvssV31BaseSeverity: CRITICAL
epss_score: 0.95
```

**Validation**:
```cypher
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})
RETURN count(v) as node_count
// Expected: node_count = 1
```

---

## VALIDATION SECTION

### Success Criteria

1. **API Response**: Status 200, entities extracted
2. **Neo4j Data**: Node exists with correct properties
3. **Qdrant Search**: Vector stored, searchable
4. **Data Quality**: No duplicates, correct relationships

### Validation Queries

**Query 1: Verify data exists**:
```cypher
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})
RETURN v.name, v.cvssV31BaseSeverity
```

**Query 2: Verify relationships**:
```cypher
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})-[r]->(n)
RETURN type(r), labels(n), count(*)
```

**Query 3: Verify vector search**:
```python
from qdrant_client import QdrantClient
client = QdrantClient('localhost', port=6333)
results = client.search(
    collection_name='ner11_threat_intel',
    query_vector=[...],  # from API response
    limit=5
)
print(f"Found {len(results)} similar threats")
```

---

## TROUBLESHOOTING

### Issue 1: API Not Responding

**Symptom**: `curl: (7) Failed to connect to localhost:8000`

**Check**:
```bash
docker ps | grep ner11-gold-api
# Verify container is running
```

**Fix**:
```bash
docker restart ner11-gold-api
# Wait 10 seconds for health check
curl http://localhost:8000/health
```

---

### Issue 2: Neo4j Query Returns Empty

**Symptom**: Query returns 0 results

**Check Schema**:
```bash
# Verify label exists
grep "Vulnerability" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE.md
```

**Check Data**:
```cypher
MATCH (v:Vulnerability)
RETURN count(v), collect(DISTINCT v.fine_grained_type)[0..5]
// Verify label and discriminator exist
```

---

## NOTES

- Last verified: 2025-12-12
- Data sources checked against production
- All commands tested and working
```

---

### 3.2 Always Reference Specific APIs

**❌ WRONG** (vague, untestable):
```markdown
Use the NER API to extract entities
```

**✅ CORRECT** (specific, verifiable):
```markdown
Use API #43 (POST /ner) from ALL_APIS_MASTER_TABLE.md:
```bash
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"your text here"}'
```
Reference: ALL_APIS_MASTER_TABLE.md line 43
```

---

### 3.3 Always Use Current Label Names

**❌ WRONG** (outdated schema):
```cypher
MATCH (v:CVE)
WHERE v.id = 'CVE-2024-12345'
```

**✅ CORRECT** (current schema from COMPLETE_SCHEMA_REFERENCE.md):
```cypher
MATCH (v:Vulnerability {fine_grained_type: 'vulnerability'})
WHERE v.cve_id = 'CVE-2024-12345'
RETURN v.cvssV31BaseSeverity, v.epss_score

-- Reference: COMPLETE_SCHEMA_REFERENCE.md
-- Super Label: Vulnerability (314,538 nodes)
-- Discriminator: fine_grained_type = 'vulnerability'
```

---

### 3.4 Always Verify Data Sources Exist

**❌ WRONG** (assume collection exists):
```python
client.search(collection_name='threat_data', ...)
```

**✅ CORRECT** (verify first):
```python
# Verify collection exists (as of 2025-12-12)
# See PROCEDURE_MAINTENANCE_GUIDE.md Section 1.3
from qdrant_client import QdrantClient
client = QdrantClient('localhost', port=6333)

# Use verified collection name
results = client.search(
    collection_name='ner11_threat_intel',  # Verified in production
    query_vector=embedding,
    limit=10
)
```

---

### 3.5 Include Validation Queries

Every procedure MUST include validation queries that:
1. Verify data was created/updated
2. Check relationships are correct
3. Confirm expected counts
4. Test data quality

**Example**:
```cypher
-- Validation Query 1: Verify node exists
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})
RETURN count(v) as node_count
-- Expected: node_count = 1

-- Validation Query 2: Verify properties
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})
RETURN
  v.cvssV31BaseSeverity IS NOT NULL as has_severity,
  v.epss_score IS NOT NULL as has_epss
-- Expected: has_severity = true, has_epss = true

-- Validation Query 3: Verify relationships
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})-[r:AFFECTS]->(a)
RETURN count(r) as relationship_count
-- Expected: relationship_count > 0
```

---

### 3.6 Test Before Documenting

**NEVER document commands you haven't tested!**

**Testing Workflow**:
1. Write command
2. Test in terminal
3. Verify expected result
4. Copy EXACT working command to procedure
5. Include actual output as example

**Example**:
```bash
# Step 1: Test command
curl http://localhost:8000/health

# Step 2: Verify works
# {"status":"healthy","model":"ner11"}

# Step 3: Document in procedure with actual output
```

---

## SECTION 4: QUALITY CHECKLIST

### Before Publishing a Procedure

Use this checklist for EVERY procedure:

```markdown
## Procedure Quality Checklist

### References Section
- [ ] References specific API numbers from ALL_APIS_MASTER_TABLE.md
- [ ] Uses current label names from COMPLETE_SCHEMA_REFERENCE.md
- [ ] Lists Qdrant collections with verification date
- [ ] Includes container names and ports

### Prerequisites Section
- [ ] Includes verification steps for all services
- [ ] Has expected output for each verification
- [ ] Tests are copy-pasteable
- [ ] Verification covers APIs, Neo4j, Qdrant

### Execution Steps
- [ ] Commands are tested and working
- [ ] Neo4j queries use correct schema
- [ ] API calls include full curl examples
- [ ] Expected results are documented
- [ ] Each step has validation

### Validation Section
- [ ] Includes queries to verify success
- [ ] Has expected outputs for each query
- [ ] Tests data quality (no duplicates, etc.)
- [ ] Covers all data stores affected

### Data Sources
- [ ] All Qdrant collections verified to exist
- [ ] All Neo4j labels verified in schema
- [ ] All APIs verified in master table
- [ ] All containers verified running

### Testability
- [ ] Every command is copy-pasteable
- [ ] Every query returns expected results
- [ ] Validation queries confirm success
- [ ] Troubleshooting steps are actionable

### Documentation
- [ ] Includes last verified date
- [ ] References truth sources
- [ ] Has working examples
- [ ] Troubleshooting section exists
```

---

## SECTION 5: MAINTENANCE WORKFLOW

### Monthly Procedure Review

**Schedule**: 1st of each month

**Process**:
1. **Verify Truth Sources**:
   ```bash
   # Check API count
   grep -c "^###" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/ALL_APIS_MASTER_TABLE.md
   # Expected: 181 (as of 2025-12-12)

   # Check schema labels
   grep "Total Labels:" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE.md
   # Expected: 631 (as of 2025-12-12)

   # Check Qdrant collections
   python3 -c "from qdrant_client import QdrantClient; client = QdrantClient('localhost', port=6333); print(len(client.get_collections().collections))"
   # Expected: 18 (as of 2025-12-12)
   ```

2. **Test All Procedures**:
   ```bash
   # List all procedures
   ls -1 /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/13_procedures/PROC-*.md

   # For each procedure:
   # 1. Run verification steps
   # 2. Execute commands
   # 3. Run validation queries
   # 4. Update "Last Verified" date
   ```

3. **Update Changed Procedures**:
   - If APIs changed → Update API references
   - If schema changed → Update Neo4j queries
   - If collections changed → Update search code
   - If containers changed → Update connection strings

4. **Archive Outdated Procedures**:
   ```bash
   # Move old procedures to archive
   mkdir -p /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/13_procedures/archive/$(date +%Y-%m)

   # Move outdated procedures
   mv PROC-OLD-*.md archive/$(date +%Y-%m)/
   ```

---

### When New API is Added

**Workflow**:
1. Add API to ALL_APIS_MASTER_TABLE.md with number
2. Test API with curl
3. Identify affected procedures
4. Update procedures with new API reference
5. Test updated procedures
6. Update "Last Updated" date

**Example**:
```bash
# New API added: POST /api/v2/threat/analyze
# API #182 in ALL_APIS_MASTER_TABLE.md

# Find procedures that need updating
grep -l "threat.*analyze" /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/13_procedures/*.md

# Update PROC-105-threat-analysis.md:
# - Add reference to API #182
# - Update curl examples
# - Test and verify
# - Update "Last Updated" date
```

---

### When Schema Changes

**Workflow**:
1. Update COMPLETE_SCHEMA_REFERENCE.md
2. Find procedures with affected labels
3. Update MATCH patterns
4. Test queries return correct results
5. Update validation queries
6. Update "Last Updated" date

**Example**:
```bash
# Schema change: New label EquipmentScan added
# fine_grained_type: equipment_scan

# Find affected procedures
grep -l "Equipment" /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/13_procedures/*.md

# Update procedures:
# Old: MATCH (e:Equipment)
# New: MATCH (e:Asset {fine_grained_type: 'equipment'})
#      MATCH (s:Measurement {fine_grained_type: 'equipment_scan'})

# Test queries, update procedures
```

---

## SECTION 6: COMMON MISTAKES TO AVOID

### Mistake 1: Using Made-Up Collection Names

**❌ WRONG**:
```python
client.search(collection_name='threat_data', ...)  # Does this exist?
```

**✅ CORRECT**:
```python
# From PROCEDURE_MAINTENANCE_GUIDE.md Section 1.3
# Verified collection: ner11_threat_intel (2025-12-12)
client.search(collection_name='ner11_threat_intel', ...)
```

---

### Mistake 2: Using Old Label Names

**❌ WRONG**:
```cypher
MATCH (c:CVE)  -- This label doesn't exist!
```

**✅ CORRECT**:
```cypher
-- From COMPLETE_SCHEMA_REFERENCE.md
-- Super Label: Vulnerability
-- Discriminator: fine_grained_type = 'vulnerability'
MATCH (v:Vulnerability {fine_grained_type: 'vulnerability'})
WHERE v.cve_id = 'CVE-2024-12345'
```

---

### Mistake 3: Vague API References

**❌ WRONG**:
```markdown
Use the search API
```

**✅ CORRECT**:
```markdown
Use API #44 (POST /search/semantic) from ALL_APIS_MASTER_TABLE.md:
```bash
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query":"ransomware","limit":10}'
```
```

---

### Mistake 4: No Validation Queries

**❌ WRONG**:
```markdown
Run the ingestion script.
```

**✅ CORRECT**:
```markdown
Run the ingestion script:
```bash
python ingest.py
```

Validate results:
```cypher
MATCH (v:Vulnerability)
WHERE v.created_date >= datetime() - duration({days: 1})
RETURN count(v) as new_vulns
-- Expected: new_vulns > 0
```
```

---

### Mistake 5: Untested Commands

**❌ WRONG**:
```bash
# This should work
curl http://localhost:8000/api/endpoint
```

**✅ CORRECT**:
```bash
# Tested 2025-12-12
curl http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"test"}'
# Returns: {"entities":[...]}
```

---

## SECTION 7: PROCEDURE TYPES

### Type 1: Ingestion Procedures

**Purpose**: Add data to Neo4j/Qdrant

**Must Include**:
- Source data location (actual file/API)
- API references from master table
- Schema validation against COMPLETE_SCHEMA_REFERENCE.md
- Duplicate check queries
- Validation queries (count, properties, relationships)

**Example**: PROC-101-kaggle-enrichment.md

---

### Type 2: Query Procedures

**Purpose**: Extract data from Neo4j/Qdrant

**Must Include**:
- Exact Neo4j schema from COMPLETE_SCHEMA_REFERENCE.md
- API references for search endpoints
- Sample queries with expected outputs
- Performance considerations
- Result validation

**Example**: PROC-201-threat-search.md

---

### Type 3: Analysis Procedures

**Purpose**: Analyze existing data

**Must Include**:
- Data source verification (collections, labels)
- Analysis queries with schema validation
- Expected results with thresholds
- Visualization/export steps
- Quality checks

**Example**: PROC-301-vulnerability-analysis.md

---

### Type 4: Maintenance Procedures

**Purpose**: Keep system healthy

**Must Include**:
- Health check commands for all services
- Performance metrics queries
- Cleanup procedures
- Backup/restore steps
- Troubleshooting guide

**Example**: PROC-401-system-health.md

---

## SECTION 8: QDRANT-SPECIFIC GUIDELINES

### Always Verify Collection Exists

```python
from qdrant_client import QdrantClient

client = QdrantClient('localhost', port=6333)

# Get all collections
collections = client.get_collections()
collection_names = [c.name for c in collections.collections]

# Verify target collection exists
if 'ner11_threat_intel' not in collection_names:
    raise ValueError("Collection ner11_threat_intel not found!")

# Proceed with operation
info = client.get_collection('ner11_threat_intel')
print(f"Collection has {info.vectors_count} vectors")
```

---

### Document Vector Dimensions

```python
# From collection verification (2025-12-12)
# Collection: ner11_threat_intel
# Vector dimension: 384 (all-MiniLM-L6-v2)
# Distance metric: Cosine

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions

embedding = model.encode("ransomware attack")
assert len(embedding) == 384, "Vector dimension mismatch!"

results = client.search(
    collection_name='ner11_threat_intel',
    query_vector=embedding.tolist(),
    limit=10
)
```

---

### Include Search Examples

```python
# Example 1: Semantic search for threat actors
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

model = SentenceTransformer('all-MiniLM-L6-v2')
client = QdrantClient('localhost', port=6333)

query = "APT29 tactics"
embedding = model.encode(query)

results = client.search(
    collection_name='ner11_threat_intel',
    query_vector=embedding.tolist(),
    limit=5,
    score_threshold=0.7
)

for result in results:
    print(f"Score: {result.score:.3f} - {result.payload.get('text', 'N/A')}")
```

---

## SECTION 9: NEO4J-SPECIFIC GUIDELINES

### Always Use Current Schema

```cypher
-- ❌ WRONG: Old schema (no discriminator)
MATCH (v:CVE)
WHERE v.id = 'CVE-2024-12345'

-- ✅ CORRECT: Current schema from COMPLETE_SCHEMA_REFERENCE.md
MATCH (v:Vulnerability {fine_grained_type: 'vulnerability'})
WHERE v.cve_id = 'CVE-2024-12345'
RETURN v
```

---

### Reference Super Labels

```cypher
-- From COMPLETE_SCHEMA_REFERENCE.md
-- 17 Super Labels with discriminators

-- Super Label: Vulnerability (314,538 nodes)
MATCH (v:Vulnerability)
WHERE v.fine_grained_type = 'vulnerability'

-- Super Label: Asset (200,275 nodes)
MATCH (a:Asset)
WHERE a.fine_grained_type = 'equipment'

-- Super Label: ThreatActor (10,599 nodes)
MATCH (t:ThreatActor)
WHERE t.fine_grained_type = 'apt_group'
```

---

### Include Relationship Validation

```cypher
-- After creating relationships, validate they exist

-- Create relationship
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})
MATCH (a:Asset {asset_id: 'server-001'})
MERGE (v)-[r:AFFECTS]->(a)

-- Validate relationship was created
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})-[r:AFFECTS]->(a:Asset)
RETURN count(r) as relationship_count
-- Expected: relationship_count = 1
```

---

### Use Correct Property Names

```cypher
-- From COMPLETE_SCHEMA_REFERENCE.md
-- Vulnerability properties:
-- - cve_id (string)
-- - cvssV2BaseScore (float)
-- - cvssV31BaseSeverity (string)
-- - epss_score (float)
-- - epss_percentile (float)

MATCH (v:Vulnerability {fine_grained_type: 'vulnerability'})
WHERE v.cvssV31BaseSeverity = 'CRITICAL'
  AND v.epss_score > 0.8
RETURN v.cve_id, v.epss_score
ORDER BY v.epss_score DESC
LIMIT 10
```

---

## SECTION 10: QUICK REFERENCE

### Truth Source Files

```bash
# APIs (181 total)
/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/ALL_APIS_MASTER_TABLE.md

# Schema (631 labels, 183 relationships)
/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE.md

# Collections (18 total)
python3 -c "from qdrant_client import QdrantClient; client = QdrantClient('localhost', port=6333); [print(c.name) for c in client.get_collections().collections]"

# Containers
docker ps --format "{{.Names}}\t{{.Ports}}"
```

---

### Verification Commands

```bash
# Verify API exists
grep "POST /ner" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/ALL_APIS_MASTER_TABLE.md

# Verify label exists
grep "Vulnerability" /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/COMPLETE_SCHEMA_REFERENCE.md

# Verify collection exists
python3 -c "from qdrant_client import QdrantClient; client = QdrantClient('localhost', port=6333); print(client.get_collection('ner11_threat_intel'))"

# Verify container running
docker ps | grep ner11-gold-api
```

---

### Common Neo4j Queries

```cypher
-- Count nodes by super label
MATCH (n)
RETURN labels(n)[0] as super_label, count(*) as count
ORDER BY count DESC

-- List discriminator types
MATCH (n:Vulnerability)
RETURN DISTINCT n.fine_grained_type, count(*) as count

-- Verify relationship types
MATCH ()-[r]->()
RETURN DISTINCT type(r), count(*) as count
ORDER BY count DESC
```

---

## CONCLUSION

**Remember**:
1. **Always reference truth sources** (APIs, schema, collections, containers)
2. **Verify before documenting** (test commands, check data sources)
3. **Include validation queries** (prove it works)
4. **Update when system changes** (monthly review, immediate updates)
5. **Test everything** (no untested commands in procedures)

**Procedures are executable truth, not documentation theater.**

---

**Last Updated**: 2025-12-12
**Next Review**: 2025-01-12
**Maintained By**: AEON Development Team
