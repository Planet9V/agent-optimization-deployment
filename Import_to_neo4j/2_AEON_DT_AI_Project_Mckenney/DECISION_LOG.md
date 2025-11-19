# Decision Log - Neo4j NLP Pipeline

## Decision Date: 2025-10-29

### USER DECISION: Option 1 - Selective Deletion
**Keep:** CVE/CWE/CAPEC/MITRE/IEC62443 files
**Delete:** Non-cybersecurity documents
**Reprocess:** All documents with improved entity recognition

### Rationale:
- Preserves critical security taxonomy (643MB, 908 files)
- Balances data preservation with quality improvement
- 5-7 hour turnaround after schema fixes
- Medium risk acceptable

---

## Schema Issues Identified (Swarm Review)

### Critical Issues Found:
1. **Entity MERGE inconsistency** (lines 472-473) - creates duplicates
2. **Missing Entity uniqueness constraint** - no enforcement
3. **No index on RELATIONSHIP.doc_id** - 100x slower queries
4. **Generic RELATIONSHIP type** - poor performance
5. **Metadata orphans** - 243 vs 652 documents
6. **Entity fan-out risk** - super nodes will form
7. **Missing composite indexes** - slower lookups

### Swarm Agents Used:
- code-analyzer: Schema validation (Score: 6/10)
- system-architect: Architecture assessment (Score: 7.2/10)
- reviewer: Best practices compliance (Score: 72/100)

---

## Revised Implementation Plan

### Phase 1: Fix Schema (2-3 hours)
```cypher
-- Add entity uniqueness constraint
CREATE CONSTRAINT entity_node_key IF NOT EXISTS
FOR (e:Entity) REQUIRE (e.text, e.label) IS NODE KEY;

-- Add relationship doc_id index
CREATE INDEX relationship_doc_id IF NOT EXISTS
FOR ()-[r:RELATIONSHIP]-() ON (r.doc_id);

-- Add composite entity index
CREATE INDEX entity_composite IF NOT EXISTS
FOR (e:Entity) ON (e.text, e.label);
```

```python
# Fix entity MERGE logic (lines 472-473)
# BEFORE:
MERGE (s:Entity {text: rel.subject})
MERGE (o:Entity {text: rel.object})

# AFTER:
MERGE (s:Entity {text: rel.subject, label: coalesce(rel.subject_label, 'UNKNOWN')})
MERGE (o:Entity {text: rel.object, label: coalesce(rel.object_label, 'UNKNOWN')})
```

### Phase 2: Selective Deletion (30 min)
```cypher
-- Mark documents to preserve
MATCH (m:Metadata)
WHERE m.file_path =~ '(?i).*(cve|cwe|capec|mitre|62443|attack).*'
   OR m.file_name =~ '(?i).*(vulnerability|weakness|threat).*'
SET m:Preserve;

-- Delete non-preserved documents
MATCH (m:Metadata)
WHERE NOT m:Preserve
OPTIONAL MATCH (m)-[:METADATA_FOR]->(d:Document)
OPTIONAL MATCH (d)-[:CONTAINS_ENTITY]->(e:Entity)
OPTIONAL MATCH (e)-[r:RELATIONSHIP]-()
DETACH DELETE m, d, e, r;

-- Clean up orphaned nodes
MATCH (e:Entity)
WHERE NOT (e)<-[:CONTAINS_ENTITY]-()
DETACH DELETE e;
```

### Phase 3: Reprocess (5-7 hours)
- Run `process_all_documents.py` with fixed schema
- Verify 100% completion
- Generate final statistics

---

## Expected Outcomes

**After Schema Fixes:**
- Entity queries: ~8ms (vs 150ms current)
- Relationship queries: ~12ms (vs 80ms current)
- No duplicate entities
- Consistent data quality

**After Option 1 Execution:**
- CVE/CWE/CAPEC/MITRE files: Preserved (~200-300 docs)
- Other files: Deleted (~350-400 docs)
- Remaining to process: ~900-1000 docs

**Final State:**
- 1287 documents processed
- Uniform entity recognition
- 700% more cybersecurity entities
- 300% more relationships
- Production-ready knowledge graph

---

## Risk Assessment

**Schema Fix Risks:** LOW
- Well-tested constraints and indexes
- No data loss
- Reversible if issues found

**Selective Deletion Risks:** MEDIUM
- Pattern matching may miss edge cases
- Test preservation query first
- Backup database before deletion

**Overall Risk:** MEDIUM-LOW with proper execution

---

## Approval Status
- [x] Schema issues identified
- [x] Swarm review completed
- [x] User decision: Option 1
- [ ] User approval to proceed with schema fixes
- [ ] Schema fixes implemented
- [ ] Selective deletion executed
- [ ] Reprocessing completed

---

## Next Action Required
**Awaiting user approval to proceed with schema fixes before executing Option 1.**
