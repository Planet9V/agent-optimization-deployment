# Quick Start - Bulk Graph Ingestion

**Fast-track guide for Task 2.4 bulk ingestion**

## Prerequisites Check (2 minutes)

```bash
# 1. Neo4j running?
docker ps | grep neo4j

# 2. NER11 API running?
curl http://localhost:8000/health

# 3. Corpus exists?
ls /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/training_data/
```

## Quick Test Run (3 minutes)

```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model

# Test with 3 documents
python pipelines/test_bulk_ingestion.py
```

**Expected output:**
```
✅ ALL PREREQUISITES MET
✅ TEST SUCCESSFUL - READY FOR FULL CORPUS PROCESSING
```

## Full Corpus Processing (10-15 minutes)

```bash
# Process all documents
python pipelines/06_bulk_graph_ingestion.py

# Watch progress:
# Processing documents: 100%|████| 42/42 [10:23<00:00]
# Processed 42, Entities: 1,847, Nodes: 15,234
```

## Verify Results (1 minute)

```bash
# Check final statistics
cat logs/ingestion_final_stats.json
```

**Success criteria:**
- ✅ `validation_passed: true`
- ✅ `nodes_added: 15000+`
- ✅ `documents_failed: 0`

## Neo4j Verification

```cypher
// Check total nodes (should be ~1,119,300)
MATCH (n) RETURN count(n) as total;

// Check new entities
MATCH (n)
WHERE n.created_at IS NOT NULL
RETURN labels(n)[0] as type, count(n) as count
ORDER BY count DESC;
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Neo4j not responding | `docker start neo4j-openspg` |
| NER11 API failed | `python serve_model.py` |
| Validation failed | Check logs: `tail logs/neo4j_ingestion.jsonl` |

## Files Created

- `logs/neo4j_ingestion.jsonl` - Processing log
- `logs/ingestion_state.json` - Resume state
- `logs/ingestion_final_stats.json` - Final statistics

---

**Total Time**: ~15 minutes for full corpus
**Documents**: 42 processed
**New Nodes**: ~15,000
**Existing Nodes**: 1,104,066 preserved
