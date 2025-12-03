# Systematic Ingestion Plan - Approval Required

**Created**: 2025-12-02 15:52:00 UTC
**Status**: AWAITING APPROVAL
**Approach**: DEFINED E30 NER11 Process with Full Validation

---

## EXECUTIVE SUMMARY

This plan will ingest **specialized cybersecurity content** into the E30 NER11 Gold knowledge graph using the complete validated pipeline:
- NER11 API (60 labels) → HierarchicalEntityProcessor (566 types) → RelationshipExtractor (13 types) → Qdrant + Neo4j

**Total Documents**: ~150-200 documents across 5 specialized areas
**Estimated Entities**: 15,000-20,000 new entities
**Estimated Relationships**: 8,000-12,000 new relationships
**Estimated Time**: 2-3 hours
**Risk Level**: LOW (all data preserved, validated pipeline)

---

## DOCUMENT SOURCES

### Source 1: Express Attack Briefs (EABs)
**Directory**: `/home/jim/2_OXOT_Projects_Dev/3_EAB_40`
**Document Count**: [COUNTING...]
**Content Type**: Structured attack briefings
**Expected Value**: High-quality attack technique entities, threat actor profiles

### Source 2: McKenney-Lacan Calculus
**Directory**: `/home/jim/2_OXOT_Projects_Dev/1_2025_11-25_documentation_no_NER11/mckenney-lacan-calculus-2025-11-28`
**Document Count**: [COUNTING...]
**Content Type**: Psychometric analysis framework
**Expected Value**: Cognitive bias entities, personality trait relationships

### Source 3: AEON Training Data (NER10)
**Directory**: `/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see`
**Document Count**: [COUNTING...]
**Content Type**: Protocol data, attack frameworks, cyber attack datasets
**Expected Value**: Protocol entities (Modbus, DNP3), attack patterns, framework mappings

### Source 4: Threat Research (Additional)
**Directory**: `/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/8_Threat Research and Reports`
**Document Count**: 39 (already counted)
**Status**: NOT YET INGESTED (was queued as Batch 6)
**Expected Value**: Advanced threat intelligence

### Source 5: Organization Research
**Directory**: `/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/6_Organizations_research`
**Document Count**: [COUNTING...]
**Content Type**: Organization profiles, vendor research
**Expected Value**: Organization entities, vendor relationships

---

## DEFINED INGESTION PROCESS (E30 NER11 Pipeline)

### Step 1: Pre-Ingestion Validation ✅ REQUIRED
```bash
# 1.1 Verify all services healthy
curl http://localhost:8000/health  # NER11 API
curl http://localhost:6333/collections/ner11_entities_hierarchical  # Qdrant
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"  # Neo4j

# 1.2 Record baseline state
BASELINE_QDRANT=$(curl -s http://localhost:6333/collections/ner11_entities_hierarchical | python3 -c "import sys, json; print(json.load(sys.stdin)['result']['points_count'])")
BASELINE_NEO4J=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "MATCH (n) RETURN count(n)" --format plain | tail -1)

echo "Baseline Qdrant: $BASELINE_QDRANT"
echo "Baseline Neo4j: $BASELINE_NEO4J"

# 1.3 Create backup checkpoint
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL apoc.export.cypher.all('/backup/pre_ingestion_$(date +%Y%m%d_%H%M%S).cypher', {format: 'cypher-shell'})"
```

### Step 2: Document Discovery and Analysis
```bash
# 2.1 Scan each directory
for dir in 3_EAB_40 mckenney-lacan-calculus AEON_Training_data_NER10 "8_Threat Research" "6_Organizations"; do
  find "$dir" -type f \( -name "*.md" -o -name "*.txt" \) | wc -l
done

# 2.2 Sample analysis (test 1-2 docs from each source)
# Verify entity extraction quality before bulk processing
```

### Step 3: Batch Processing with Validation

**For Each Source Directory**:

```python
# Use the validated ingestion pipeline:
python3 scripts/ingest_wiki_documents.py \
  --wiki-root "/path/to/source" \
  --limit 50  # Process in batches of 50

# Pipeline executes:
# 3.1 NER11 API: Extract entities (60 labels)
# 3.2 HierarchicalEntityProcessor: Classify to 566 types
# 3.3 RelationshipExtractor: Extract relationships (13 types, 3 methods)
# 3.4 Qdrant: Store with embeddings (384-dim vectors)
# 3.5 Neo4j: Create nodes with MERGE (preserve existing)
# 3.6 Neo4j: Create relationships with MERGE
# 3.7 Validation: Check Tier2 >= Tier1
# 3.8 Log: Record to JSON

# After each batch:
# 3.9 Verify data growth (not loss)
# 3.10 Check quality metrics
```

### Step 4: Post-Ingestion Validation ✅ REQUIRED
```bash
# 4.1 Verify data growth (not loss)
FINAL_QDRANT=$(curl -s http://localhost:6333/collections/ner11_entities_hierarchical | python3 -c "import sys, json; print(json.load(sys.stdin)['result']['points_count'])")
FINAL_NEO4J=$(docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "MATCH (n) RETURN count(n)" --format plain | tail -1)

if [ $FINAL_NEO4J -lt $BASELINE_NEO4J ]; then
  echo "❌ DATA LOSS DETECTED - ABORT"
  exit 1
fi

# 4.2 Validate tier hierarchy
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) WHERE n.ner_label IS NOT NULL
   RETURN count(DISTINCT n.ner_label) AS tier1,
          count(DISTINCT n.fine_grained_type) AS tier2"
# Must have: tier2 >= tier1

# 4.3 Test APIs with new data
curl -X POST http://localhost:8000/search/semantic -d '{"query":"test","limit":5}'
curl -X POST http://localhost:8000/search/hybrid -d '{"query":"test","expand_graph":true}'

# 4.4 Generate quality report
```

### Step 5: Documentation Update
```bash
# 5.1 Update blotter with results
# 5.2 Update API docs with new entity counts
# 5.3 Update frontend guides with new capabilities
# 5.4 Commit changes to git
```

---

## PROPOSED EXECUTION ORDER (Requires Approval)

### Batch 1: Express Attack Briefs (EABs)
**Priority**: HIGH
**Reason**: Structured attack intelligence, high entity density
**Expected Output**: 3,000-5,000 entities, 1,500-2,000 relationships
**Processing Time**: ~30 minutes

### Batch 2: McKenney-Lacan Calculus
**Priority**: HIGH
**Reason**: Psychometric framework (Phase 4 dependency)
**Expected Output**: 1,000-2,000 entities, 500-1,000 relationships
**Processing Time**: ~15 minutes

### Batch 3: AEON Training Data (NER10)
**Priority**: MEDIUM
**Reason**: Protocol and framework reference data
**Expected Output**: 5,000-8,000 entities, 3,000-5,000 relationships
**Processing Time**: ~45 minutes

### Batch 4: Threat Research (Remaining)
**Priority**: MEDIUM
**Reason**: Additional threat intelligence
**Expected Output**: 3,000-4,000 entities, 1,500-2,000 relationships
**Processing Time**: ~20 minutes

### Batch 5: Organization Research
**Priority**: LOW
**Reason**: Vendor and organization profiles
**Expected Output**: 2,000-3,000 entities, 1,000-1,500 relationships
**Processing Time**: ~15 minutes

---

## RISK ASSESSMENT

### Data Safety Risks:
- **Risk**: Neo4j node deletion
- **Mitigation**: Using MERGE (not CREATE), backup before start
- **Probability**: VERY LOW (proven safe over 409 documents)

### Quality Risks:
- **Risk**: Poor entity extraction on specialized content
- **Mitigation**: Test 1-2 docs from each source first
- **Probability**: LOW (NER11 handles technical content well)

### Performance Risks:
- **Risk**: System slowdown with 60K+ entities
- **Mitigation**: Monitor performance, process in batches
- **Probability**: MEDIUM (should be fine, may need optimization)

---

## AGENT DEPLOYMENT PLAN

**Claude-Flow Swarm** (using existing mesh topology):
1. **Coordinator Agent**: Orchestrates batch execution
2. **Quality Agent**: Validates each batch completion
3. **Research Agent**: Identifies blind spots, fetches missing context
4. **Deep Research Agent**: Analyzes complex patterns needing additional research
5. **Documentation Agent**: Updates wiki with results
6. **Validation Agent**: Checks data integrity after each batch

**ruv-Swarm** (neural network coordination):
7. **Pattern Recognition Agent**: Learns relationship patterns
8. **Quality Control Agent**: Grades output quality
9. **Optimization Agent**: Tunes extraction parameters

---

## EXPECTED FINAL STATE

**Entities**: 49,139 → 64,000-69,000 (+15,000-20,000)
**Hierarchical Nodes**: 1,163 → 1,500-1,800 (+350-650)
**Relationships**: 244,803 → 252,000-257,000 (+8,000-12,000)
**Tier1 Labels**: 49 → 55+ (expect more diversity)
**Tier2 Types**: 55 → 80-100 (better taxonomy coverage)

---

## VALIDATION CHECKPOINTS

After EACH batch:
- ✅ Verify Neo4j node count ≥ baseline
- ✅ Verify Qdrant points increased
- ✅ Validate Tier2 ≥ Tier1
- ✅ Test API endpoints still respond
- ✅ Check relationship extraction working

If ANY checkpoint fails:
- ⏸️ STOP processing
- 🔍 Investigate issue
- 🔧 Fix before continuing

---

## APPROVAL REQUIRED

**Questions for You**:

1. ✅ **Approve execution order?** (EABs → McKenney → Training → Threat → Orgs)
2. ✅ **Approve risk mitigations?** (MERGE, backups, validation checkpoints)
3. ✅ **Approve agent deployment?** (9 specialized agents with research capability)
4. ✅ **Any directories to exclude?** (Or process all as listed)
5. ✅ **Any special handling needed?** (For specific document types)

**Please confirm approval to proceed with this plan.**

---

**Current System State**:
- Qdrant: 49,139 entities
- Neo4j: 1,163 hierarchical nodes
- All services: HEALTHY
- Backups: Can be created on demand

**Ready to execute** upon your approval.
