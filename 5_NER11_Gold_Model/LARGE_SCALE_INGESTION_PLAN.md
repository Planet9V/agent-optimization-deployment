# Large-Scale Ingestion Plan - 475 Documents

**Created**: 2025-12-02 07:45:00 UTC
**Mission**: Ingest all annual cybersecurity reports (2020-2024) + threat research
**Estimated Time**: 3-4 hours
**Expected Output**: 50,000+ entities, 15,000+ relationships

---

## Ingestion Batches

### Batch 1: 2024 Annual Reports (IN PROGRESS)
**Directory**: `/Import 1 NOV 2025/12_Reports - Annual Cyber Security/2024`
**Documents**: ~100 reports
**Status**: RUNNING (background process 594fd5)
**Expected**: 8,000-10,000 entities, 2,500-3,000 relationships

### Batch 2: 2023 Annual Reports
**Directory**: `/Import 1 NOV 2025/12_Reports - Annual Cyber Security/2023`
**Documents**: ~100 reports
**Status**: PENDING
**Expected**: 8,000-10,000 entities, 2,500-3,000 relationships

### Batch 3: 2022 Annual Reports
**Directory**: `/Import 1 NOV 2025/12_Reports - Annual Cyber Security/2022`
**Documents**: ~100 reports
**Status**: PENDING
**Expected**: 8,000-10,000 entities, 2,500-3,000 relationships

### Batch 4: 2021 Annual Reports
**Directory**: `/Import 1 NOV 2025/12_Reports - Annual Cyber Security/2021`
**Documents**: ~60 reports
**Status**: PENDING
**Expected**: 5,000-7,000 entities, 1,500-2,000 relationships

### Batch 5: 2020 Annual Reports
**Directory**: `/Import 1 NOV 2025/12_Reports - Annual Cyber Security/2020`
**Documents**: ~60 reports
**Status**: PENDING
**Expected**: 5,000-7,000 entities, 1,500-2,000 relationships

### Batch 6: Threat Research Reports
**Directory**: `/Import 1 NOV 2025/8_Threat Research and Reports`
**Documents**: 39 reports
**Status**: PENDING
**Expected**: 3,000-5,000 entities, 1,000-1,500 relationships

---

## Expected Final State

**Entities**:
- Current: 4,051 (Qdrant)
- Expected: 45,000-55,000 (+40,000-50,000)

**Relationships**:
- Current: 232,371
- Expected: 245,000-250,000 (+12,000-18,000 from our pipeline)

**Neo4j Nodes**:
- Current: 1,104,389
- Expected: 1,145,000-1,155,000 (+40,000-50,000)

**Hierarchical Classification**:
- Tier1 labels: 41 → 55+ (expect more label diversity)
- Tier2 types: 45 → 150+ (expect 566-type taxonomy to expand significantly)

---

## Quality Metrics to Track

### Entity Extraction Quality
- Confidence scores (target: >0.9 average)
- Label distribution (how balanced across 60 labels)
- Entity length (avoid very short/long extractions)

### Relationship Extraction Quality
- Precision (relationships that make sense)
- Recall (capturing obvious relationships)
- Confidence scores by method
- Relationship type distribution

### Hierarchy Effectiveness
- Tier2 > Tier1 validation (must always pass)
- Coverage of 566-type taxonomy
- Classification confidence
- Fine-grained type diversity

### API Enhancement Support
- How many enhancements can be supported with extracted data
- Which enhancements have sufficient entities
- Gap analysis for missing entity types

---

## Monitoring Commands

```bash
# Check Qdrant growth
watch -n 30 'curl -s http://localhost:6333/collections/ner11_entities_hierarchical | python3 -c "import sys, json; print(f\"Points: {json.load(sys.stdin)[\"result\"][\"points_count\"]}\")"'

# Check Neo4j growth
watch -n 30 'docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "MATCH (n) WHERE n.ner_label IS NOT NULL RETURN count(n)" --format plain 2>&1 | tail -1'

# Check background process
tail -f logs/ingestion_2024.log
```

---

**Status**: Batch 1 (2024) running, batches 2-6 queued
