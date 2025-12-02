# Neo4j Schema v3.1 Migration - Quick Start Guide

**Migration Script**: `/5_NER11_Gold_Model/neo4j_migrations/01_schema_v3.1_migration.cypher`
**Estimated Time**: 45-70 minutes
**Database**: openspg-neo4j (1,104,066 nodes)

---

## ⚠️ CRITICAL: Execute Steps in Order

### Step 0: Backup Database (MANDATORY - Bash Shell)

**DO NOT SKIP THIS STEP**

```bash
# Create backup directory
mkdir -p /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/neo4j_backups
BACKUP_DIR="/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/neo4j_backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Stop Neo4j
docker stop openspg-neo4j

# Copy data directory
docker cp openspg-neo4j:/data "$BACKUP_DIR/neo4j_data"

# Create database dump
docker run --rm \
  --volumes-from openspg-neo4j \
  -v "$BACKUP_DIR":/backup \
  neo4j:5.23.0 \
  neo4j-admin database dump neo4j --to-path=/backup

# Create metadata
cat > "$BACKUP_DIR/backup_metadata.txt" << EOF
Backup Date: $(date)
Database: openspg-neo4j
Total Nodes: 1,104,066 (expected)
Total Labels: 193+
Migration Version: v3.0 → v3.1
EOF

# Restart Neo4j
docker start openspg-neo4j
sleep 30

# Verify backup
echo "Backup location: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"

# Test connectivity
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN count(n) as total_nodes;"
```

**Verification Checklist**:
- ✅ Backup directory exists: `$BACKUP_DIR`
- ✅ neo4j_data directory copied
- ✅ Database dump file exists
- ✅ Metadata file created
- ✅ Neo4j restarted successfully
- ✅ Node count = 1,104,066

**⚠️ DO NOT PROCEED UNTIL ALL CHECKS PASS ⚠️**

---

### Step 1: Open Cypher Shell

```bash
docker exec -it openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg"
```

---

### Step 2: Pre-Flight Verification (2-3 minutes)

Copy and execute **Section 1** from migration script (lines 127-181).

**Critical Checks**:
1. Baseline node count = 1,104,066
2. Total labels = 193+
3. Existing v3.1 labels identified

**STOP if baseline doesn't match 1,104,066 nodes**

---

### Step 3: Create Constraints (1-2 minutes)

Copy and execute **Section 2** from migration script (lines 189-254).

Creates 17 unique constraints (idempotent - safe to re-run).

---

### Step 4: Add Hierarchical Properties (15-30 minutes)

Copy and execute **Section 3** from migration script (lines 262-478).

**What this does**:
- Enhances 17 label types with hierarchical properties
- Adds: fine_grained_type, hierarchy_level, hierarchy_path, ner_label
- Preserves all existing nodes and properties

**Progress tracking**:
- Each query returns count of enhanced nodes
- Watch for "X_enhanced" results

---

### Step 5: Create Performance Indexes (10-20 minutes)

Copy and execute **Section 4** from migration script (lines 485-575).

**What this does**:
- Creates 17 fine_grained_type indexes
- Creates 6 composite indexes
- Creates 2 global hierarchy indexes
- Creates 4 full-text search indexes

**Note**: Indexes build in background, may take time on large node counts.

---

### Step 6: Post-Migration Validation (3-5 minutes)

Copy and execute **Section 5** from migration script (lines 582-653).

**CRITICAL VALIDATION**:
```cypher
MATCH (n)
WITH count(n) as total_nodes
RETURN total_nodes as post_migration_node_count;
```

**MUST RETURN: 1,104,066 nodes**

**If node count doesn't match**:
- ⚠️ DO NOT PROCEED
- Execute rollback procedure (Section 6)
- Investigate discrepancy

**Additional Validations**:
- Check hierarchical property coverage
- Verify fine_grained_type distribution
- Confirm schema_version tagging
- Test sample queries

---

## Quick Reference: What Changed

### New Labels Added (6)
- `PsychTrait` - Cognitive biases, personality traits
- `EconomicMetric` - Financial impact, costs
- `Protocol` - ICS/Network protocols
- `Role` - Job roles, access levels
- `Software` - Applications, libraries
- `Control` - Security controls

### New Properties Added (4)
- `fine_grained_type` - 566-type discriminator (e.g., "programmable_logic_controller")
- `hierarchy_level` - Depth: 0 (base), 1 (type), 2 (subtype)
- `hierarchy_path` - Full path (e.g., "Asset/OT/programmable_logic_controller")
- `ner_label` - NER11 entity mapping (e.g., "ASSET")

### Indexes Created (33)
- 17 fine_grained_type indexes (one per label)
- 6 composite indexes (multi-property queries)
- 2 global hierarchy indexes (cross-label queries)
- 4 full-text search indexes (name/alias search)
- 17 unique constraints (ID uniqueness)

---

## Rollback Procedure (If Needed)

### Option A: Remove v3.1 Properties Only

```cypher
MATCH (n)
WHERE n.schema_version = '3.1'
REMOVE n.fine_grained_type, n.hierarchy_level, n.hierarchy_path,
       n.ner_label, n.schema_version
RETURN count(n) as nodes_rolled_back;
```

### Option B: Full Database Restore

```bash
# Stop Neo4j
docker stop openspg-neo4j

# Restore from backup
docker cp "$BACKUP_DIR/neo4j_data/." openspg-neo4j:/data

# Restart Neo4j
docker start openspg-neo4j
sleep 30

# Verify restoration
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN count(n) as restored_nodes;"
```

---

## Post-Migration Testing

### Test 1: Query Specific Entity Type
```cypher
// Find all PLCs (if any exist)
MATCH (n:Asset)
WHERE n.fine_grained_type = 'programmable_logic_controller'
RETURN count(n), collect(n.name)[0..5] as sample_names;
```

### Test 2: Query Cognitive Biases
```cypher
// Find all cognitive biases
MATCH (n:PsychTrait)
WHERE n.traitType = 'CognitiveBias'
RETURN count(n), collect(n.name)[0..5] as sample_biases;
```

### Test 3: Verify Index Usage
```cypher
// Check index usage on fine_grained_type
PROFILE MATCH (n:Asset)
WHERE n.fine_grained_type = 'server'
RETURN count(n);
```

Look for "Index Seek" in the execution plan.

---

## Troubleshooting

### Issue: Node count mismatch after migration

**Symptom**: Post-migration node count ≠ 1,104,066

**Solution**:
1. Stop immediately - DO NOT continue
2. Execute rollback Option B (full restore)
3. Investigate discrepancy before retrying
4. Check Neo4j logs: `docker logs openspg-neo4j`

### Issue: Indexes not created

**Symptom**: `SHOW INDEXES` shows fewer than 33 indexes

**Solution**:
1. Check for index creation errors in output
2. Re-run Section 4 (idempotent - safe to retry)
3. Verify Neo4j memory settings (may need more heap)

### Issue: Query performance slow

**Symptom**: Queries on fine_grained_type are slow

**Solution**:
1. Check index status: `SHOW INDEXES`
2. Wait for indexes to finish building (may take time)
3. Check index state: should be "ONLINE" not "POPULATING"

---

## Success Criteria

**Migration is successful if**:
- ✅ Post-migration node count = 1,104,066
- ✅ All 33 indexes created and ONLINE
- ✅ Sample queries using fine_grained_type return results
- ✅ No errors in Neo4j logs
- ✅ Hierarchical properties exist on v3.1 labels

---

## Next Steps After Migration

1. **Immediate**: Document validation results
2. **Week 1**: Update application code to use fine_grained_type queries
3. **Week 1**: Benchmark query performance improvements
4. **Week 2**: Train team on new hierarchical query patterns
5. **Month 1**: Monitor database performance metrics

---

## Support & References

- **Migration Script**: `/5_NER11_Gold_Model/neo4j_migrations/01_schema_v3.1_migration.cypher`
- **Validation Report**: `/5_NER11_Gold_Model/pipelines/TASK_2_1_MIGRATION_VALIDATION_REPORT.md`
- **Schema Spec**: `/6_NER11_Gold_Model_Enhancement/neo4j_integration/01_SCHEMA_V3.1_SPECIFICATION.md`
- **TASKMASTER**: Task 2.1 - Neo4j Schema Migration

---

**Last Updated**: 2025-12-01
**Script Version**: v2.0.0
**Status**: ✅ Production-Ready
