# Enhancement 1 Deployment - Quick Start Guide

## Prerequisites Check

```bash
# 1. Verify database is running
docker ps | grep openspg-neo4j

# 2. Check input file exists
ls -lh /home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/data/enhancement1_has_bias_relationships_VALIDATED.json

# 3. Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19
```

## Deploy in 3 Commands

### 1. Pre-Deployment Verification
```bash
python3 scripts/verify_enhancement1_deployment.py
```

**Expected**: HAS_BIAS relationships: 0

### 2. Execute Deployment
```bash
python3 scripts/deploy_enhancement1_relationships.py
```

**Expected**:
- 36 batches processed
- 18,000 relationships created
- No errors

### 3. Post-Deployment Verification
```bash
python3 scripts/verify_enhancement1_deployment.py
```

**Expected**: HAS_BIAS relationships: 18,000

## Monitoring Deployment

Watch for:
- ✓ Batch progress: "Batch 1/36", "Batch 2/36", etc.
- ✓ Progress percentage: "2.8% complete", "5.6% complete", etc.
- ✓ Final count: "18,000 relationships created"
- ✗ Any error messages

## Troubleshooting

### Issue: Input file not found
```bash
# Check if Hour 2 completed
ls -lh data/enhancement1_has_bias_relationships_VALIDATED.json
```

### Issue: Database connection error
```bash
# Restart Neo4j container
docker restart openspg-neo4j
sleep 10  # Wait for startup
```

### Issue: Partial deployment
```bash
# Check deployment log
cat reports/enhancement1_deployment_log.txt | grep -i error

# Verify current count
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH ()-[r:HAS_BIAS]->() RETURN count(r) as count"
```

## Rollback (if needed)

```bash
# Delete all HAS_BIAS relationships
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH ()-[r:HAS_BIAS]->() DELETE r"
```

## Quick Verification Queries

```bash
# Count relationships
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH ()-[r:HAS_BIAS]->() RETURN count(r)"

# Sample relationships
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH (s)-[r:HAS_BIAS]->(b) RETURN s.id, b.biasId, r.strength LIMIT 5"

# Property statistics
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
  "MATCH ()-[r:HAS_BIAS]->() RETURN avg(r.strength) as avg_strength, avg(r.activationThreshold) as avg_threshold"
```

## Success Checklist

- [ ] Pre-deployment verification shows 0 relationships
- [ ] Deployment script runs without errors
- [ ] All 36 batches complete successfully
- [ ] Post-deployment verification shows 18,000 relationships
- [ ] Sample queries return correct data
- [ ] Deployment log has no errors

## Estimated Timeline

- Pre-deployment verification: 10 seconds
- Deployment execution: 2-3 minutes
- Post-deployment verification: 10 seconds
- **Total**: ~3-4 minutes

---

**Status**: Ready for deployment
**Last Updated**: 2025-11-23
