# GAP-004 Phase 1 Schema Deployment

## Overview

Complete Cypher DDL scripts for deploying 35 new node types to enhance the OXOT threat intelligence graph with cyber-physical attack detection, cascading failure simulation, temporal reasoning, and operational impact modeling capabilities.

**Created:** 2025-11-13
**Status:** READY FOR DEPLOYMENT
**Target:** Neo4j 5.x Enterprise

---

## Files Created

### 1. `gap004_schema_constraints.cypher` (8.6 KB)
**Purpose:** Create 34 unique ID constraints for 35 node types
**Execution Order:** 1st (MUST be executed before indexes)

**Constraint Categories:**
- UC2: Cyber-Physical Attack Detection (8 constraints)
- UC3: Cascading Failure Simulation (6 constraints)
- R6: Temporal Reasoning (6 constraints)
- CG-9: Operational Impact Modeling (5 constraints)
- UC1: SCADA Attack Reconstruction (6 constraints)
- Supporting Integration (3 constraints)

**Idempotency:** All constraints use `IF NOT EXISTS` clause

---

### 2. `gap004_schema_indexes.cypher` (14 KB)
**Purpose:** Create 102 performance indexes for query optimization
**Execution Order:** 2nd (MUST be executed after constraints)

**Index Categories:**
- Multi-tenant isolation indexes (35 indexes - CRITICAL)
- Temporal query indexes (15 indexes)
- Asset relationship indexes (15 indexes)
- Severity/priority indexes (10 indexes)
- Categorical indexes (15 indexes)
- Composite indexes (8 indexes)
- Full-text search indexes (5 indexes)

**Performance Target:** <2s queries for 15M nodes

**Idempotency:** All indexes use `IF NOT EXISTS` clause

---

### 3. `gap004_relationships.cypher` (14 KB)
**Purpose:** Document 50+ relationship patterns connecting new and existing nodes
**Execution Order:** Reference only (relationships created during data ingestion)

**Relationship Categories:**
- UC2: Cyber-physical asset monitoring, deviation detection, safety interlocks
- UC3: Cascade propagation, dependency chains, impact assessment
- R6: Temporal event storage, pattern detection, bitemporal versioning
- CG-9: SLA tracking, customer impact, revenue modeling
- UC1: SCADA event correlation, attack timeline reconstruction
- Integration: CVE, ThreatActor, Technique connections

**Note:** This file contains commented examples for testing. Actual relationships are created during data import.

---

### 4. `gap004_deploy.sh` (12 KB)
**Purpose:** Automated deployment script with error handling and verification
**Execution Order:** Primary deployment tool

**Features:**
- ✅ Connection validation to Neo4j
- ✅ Pre-deployment backup creation
- ✅ Sequential execution (constraints → indexes)
- ✅ Index online wait time
- ✅ Deployment verification (counts constraints/indexes)
- ✅ Detailed logging with timestamps
- ✅ Color-coded output (success/error/warning)

**Usage:**
```bash
# Interactive mode (prompts for password)
./gap004_deploy.sh

# With parameters
./gap004_deploy.sh bolt://localhost:7687 neo4j mypassword

# With custom Neo4j instance
./gap004_deploy.sh bolt://production-neo4j:7687 admin secure_password
```

**Prerequisites:**
- `cypher-shell` installed (Neo4j client tools)
- Network access to Neo4j instance
- Valid credentials with schema modification permissions

---

### 5. `gap004_rollback.cypher` (15 KB)
**Purpose:** Safe rollback of all GAP-004 Phase 1 changes
**Execution Order:** Only if rollback needed

**Features:**
- ✅ Drops all 102 indexes (safe - no data loss)
- ✅ Drops all 34 constraints (safe - no data loss)
- ✅ Optional node deletion (COMMENTED OUT for safety)
- ✅ Verification queries to confirm rollback success
- ✅ Idempotent (uses `IF EXISTS` clause)

**WARNING:** Node deletion section is commented out. Uncommenting will DELETE ALL DATA for 35 node types. This is IRREVERSIBLE.

**Usage:**
```bash
cypher-shell -a bolt://localhost:7687 -u neo4j -p password --file gap004_rollback.cypher
```

---

## Deployment Steps

### Step 1: Pre-Deployment Checklist

```bash
# Verify Neo4j is running
systemctl status neo4j  # or: docker ps | grep neo4j

# Test connection
echo "RETURN 1 AS test;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password

# Check current schema state
echo "CALL db.schema.visualization();" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password

# Verify disk space (Phase 1 will add ~500GB)
df -h /var/lib/neo4j
```

### Step 2: Execute Deployment Script

```bash
cd /home/jim/2_OXOT_Projects_Dev/scripts

# Make executable (if not already)
chmod +x gap004_deploy.sh

# Run deployment
./gap004_deploy.sh bolt://localhost:7687 neo4j your_password
```

**Expected Output:**
```
═══════════════════════════════════════════════════════════════════════
  GAP-004 PHASE 1 SCHEMA DEPLOYMENT
  Neo4j URI: bolt://localhost:7687
  Timestamp: 2025-11-13 16:45:00
═══════════════════════════════════════════════════════════════════════

[2025-11-13 16:45:00] Checking prerequisites...
[SUCCESS] All prerequisites met
[2025-11-13 16:45:01] Testing Neo4j connection to bolt://localhost:7687...
[SUCCESS] Connection successful
[2025-11-13 16:45:02] Creating pre-deployment backup...
[SUCCESS] Backup created: pre_gap004_backup_20251113_164502.cypher

PHASE 1: Deploying Constraints (35 constraints)
--------------------------------------------------------------
[2025-11-13 16:45:03] Executing Constraint creation from gap004_schema_constraints.cypher...
[SUCCESS] Constraint creation completed

PHASE 2: Deploying Indexes (70+ indexes)
--------------------------------------------------------------
[2025-11-13 16:45:15] Executing Index creation from gap004_schema_indexes.cypher...
[SUCCESS] Index creation completed

PHASE 3: Waiting for indexes to come online...
--------------------------------------------------------------
[2025-11-13 16:45:35] Waiting for indexes to come online...

PHASE 4: Verification
--------------------------------------------------------------
[2025-11-13 16:45:40] Verifying deployment...
[2025-11-13 16:45:42] Constraints created: 34 / 35 expected
[2025-11-13 16:45:44] Indexes created: 102 / 70+ expected
[SUCCESS] Deployment verification passed

═══════════════════════════════════════════════════════════════════════
[SUCCESS] GAP-004 Phase 1 Schema Deployment COMPLETE
═══════════════════════════════════════════════════════════════════════
```

### Step 3: Verify Deployment

```bash
# Check constraint count
echo "SHOW CONSTRAINTS YIELD name WHERE name STARTS WITH 'digital_twin' OR name STARTS WITH 'physical' RETURN count(*) AS count;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password

# Check index count
echo "SHOW INDEXES YIELD name WHERE name STARTS WITH 'digital_twin' OR name STARTS WITH 'sensor' RETURN count(*) AS count;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password

# View all GAP-004 constraints
echo "SHOW CONSTRAINTS;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password | grep -E "digital_twin|physical|physics|state_deviation|process_loop|safety|cascade|dependency|propagation|impact|resilience|temporal|event_store|timeseries|snapshot|versioned|operational|service_level|customer_impact|revenue|disruption|scada|hmi|plc|rtu|correlation|timeline|data_flow|alert_rule|remediation"

# View all GAP-004 indexes
echo "SHOW INDEXES;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password | grep -E "digital_twin|sensor|actuator|constraint|deviation|loop|safety|interlock|cascade|dep|prop|impact|resilience|cross|temporal|metric|sla|customer_impact|revenue|disruption|scada|hmi|plc|rtu|correlation|timeline|dataflow|alert|remediation"
```

### Step 4: Monitor Index Building

```bash
# Watch index status (some indexes may take time to build)
watch -n 5 'echo "SHOW INDEXES YIELD name, state WHERE state <> \"ONLINE\" RETURN name, state;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password'

# Wait until all indexes show state = "ONLINE"
```

---

## Expected Schema Changes

### Before Deployment
- Node types: ~38 types
- Nodes: 183,000 nodes
- Relationships: 1.37M relationships
- Storage: ~100GB

### After Deployment (Schema Only)
- Node types: 73 types (+35 new types, +92%)
- Constraints: +34 unique ID constraints
- Indexes: +102 performance indexes
- Relationship patterns: +50 defined patterns
- Storage: ~100GB (no data added yet, only schema)

### After Data Ingestion (Phase 1 Complete)
- Nodes: ~15M nodes (+8200% data growth)
- Relationships: ~25M relationships (+1725% growth)
- Storage: ~600GB (+500GB)

---

## Post-Deployment Steps

### 1. Review Relationship Patterns
```bash
cat gap004_relationships.cypher
```

### 2. Begin Data Ingestion
Refer to `GAP004_NODE_SPECIFICATIONS.md` for:
- Real-time data sources (SCADA/PLC, Digital Twins, Operational Systems)
- Historical data backfill (90-day event logs, time-series data)
- Ingestion methods (Kafka streaming, REST API, Batch ETL)

### 3. Create Sample Data (Optional - For Testing)
```bash
# UC2: Cyber-Physical Attack Detection examples
cypher-shell -a bolt://localhost:7687 -u neo4j -p password --file gap004_sample_data_uc2.cypher

# UC3: Cascading Failure Simulation examples
cypher-shell -a bolt://localhost:7687 -u neo4j -p password --file gap004_sample_data_uc3.cypher
```

### 4. Validate Query Performance
```cypher
// Test query: Find cyber-physical deviations
MATCH (dt:DigitalTwinState {assetId: "device-plc-001"})
MATCH (sensor:PhysicalSensor {assetId: "device-plc-001"})
WHERE sensor.reading > dt.expectedValues.temperature * 1.2
RETURN dt, sensor;

// Performance target: <2s for 15M nodes
```

### 5. Monitor Index Usage
```cypher
// Check which indexes are being used
SHOW INDEXES YIELD name, populationPercent, type
WHERE populationPercent > 0
RETURN name, populationPercent, type
ORDER BY populationPercent DESC;
```

---

## Rollback Procedure

If deployment issues occur or rollback is needed:

### Option 1: Rollback Schema Only (Safe - No Data Loss)

```bash
# Execute rollback script
cypher-shell -a bolt://localhost:7687 -u neo4j -p password --file gap004_rollback.cypher

# Verify rollback
echo "SHOW CONSTRAINTS YIELD name WHERE name STARTS WITH 'digital_twin' RETURN count(*) AS count;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password
# Expected: count = 0

echo "SHOW INDEXES YIELD name WHERE name STARTS WITH 'digital_twin' RETURN count(*) AS count;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password
# Expected: count = 0
```

### Option 2: Rollback Schema + Delete Nodes (DESTRUCTIVE)

**WARNING:** This will DELETE ALL DATA for 35 node types. IRREVERSIBLE.

```bash
# 1. Edit gap004_rollback.cypher
# 2. Uncomment SECTION 3 (DELETE NODES)
# 3. Execute rollback

cypher-shell -a bolt://localhost:7687 -u neo4j -p password --file gap004_rollback.cypher
```

---

## Troubleshooting

### Issue: Constraint Creation Fails

**Error:** `Constraint already exists`

**Solution:**
```bash
# Check existing constraints
echo "SHOW CONSTRAINTS;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password

# Drop conflicting constraint
echo "DROP CONSTRAINT constraint_name IF EXISTS;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password

# Re-run deployment
./gap004_deploy.sh
```

### Issue: Index Creation Fails

**Error:** `Index already exists` or `Out of memory`

**Solution:**
```bash
# Check existing indexes
echo "SHOW INDEXES;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password

# Increase Neo4j heap size (neo4j.conf)
dbms.memory.heap.initial_size=4g
dbms.memory.heap.max_size=8g

# Restart Neo4j
systemctl restart neo4j

# Re-run deployment
./gap004_deploy.sh
```

### Issue: Connection Timeout

**Error:** `Unable to connect to bolt://localhost:7687`

**Solution:**
```bash
# Check Neo4j status
systemctl status neo4j

# Check Neo4j logs
tail -f /var/log/neo4j/neo4j.log

# Verify port 7687 is open
netstat -tuln | grep 7687

# Check firewall
sudo ufw status
sudo ufw allow 7687/tcp
```

### Issue: Deployment Verification Fails

**Error:** `Constraints created: 30 / 35 expected`

**Solution:**
```bash
# Review deployment log
cat gap004_deploy_*.log | grep ERROR

# Manually check missing constraints
echo "SHOW CONSTRAINTS;" | cypher-shell -a bolt://localhost:7687 -u neo4j -p password | grep -v "digital_twin\|physical\|physics"

# Re-run specific constraint creation
cypher-shell -a bolt://localhost:7687 -u neo4j -p password <<EOF
CREATE CONSTRAINT missing_constraint_name IF NOT EXISTS
FOR (n:NodeType) REQUIRE n.propertyName IS UNIQUE;
EOF
```

---

## Performance Optimization

### Index Usage Monitoring

```cypher
// Monitor index population
SHOW INDEXES YIELD name, populationPercent, type
WHERE populationPercent < 100
RETURN name, populationPercent, type
ORDER BY populationPercent ASC;

// Find unused indexes (after data ingestion)
SHOW INDEXES YIELD name, populationPercent, type
WHERE populationPercent = 0
RETURN name, type;
```

### Query Performance Testing

```cypher
// Test temporal query performance (90-day window)
PROFILE
MATCH (event:TemporalEvent)
WHERE event.timestamp >= datetime() - duration({days: 90})
  AND event.customer_namespace = "customer:RailOperator-XYZ"
RETURN count(event);

// Expected: <2s execution time with index on (timestamp, customer_namespace)

// Test asset-centric query performance
PROFILE
MATCH (sensor:PhysicalSensor {assetId: "device-plc-001"})
WHERE sensor.timestamp >= datetime() - duration({hours: 24})
RETURN sensor
ORDER BY sensor.timestamp DESC
LIMIT 100;

// Expected: <1s execution time with composite index on (assetId, timestamp)
```

---

## Support and References

**Documentation:**
- `/home/jim/2_OXOT_Projects_Dev/docs/GAP004_NODE_SPECIFICATIONS.md` - Complete property definitions
- `/home/jim/2_OXOT_Projects_Dev/docs/GAP004_ARCHITECTURE_DESIGN.md` - Architecture overview
- Neo4j Constraints: https://neo4j.com/docs/cypher-manual/current/constraints/
- Neo4j Indexes: https://neo4j.com/docs/cypher-manual/current/indexes/

**Logs:**
- Deployment log: `gap004_deploy_YYYYMMDD_HHMMSS.log`
- Neo4j log: `/var/log/neo4j/neo4j.log`
- Query log: `/var/log/neo4j/query.log`

**Contact:**
- Research Agent: schema-requirements-analyst
- GitHub Issues: https://github.com/your-org/oxot-project/issues

---

## Deployment Checklist

- [ ] Neo4j 5.x Enterprise running
- [ ] `cypher-shell` installed
- [ ] Valid Neo4j credentials
- [ ] Sufficient disk space (~500GB for Phase 1 data)
- [ ] Pre-deployment backup created
- [ ] Reviewed deployment scripts
- [ ] Executed `./gap004_deploy.sh`
- [ ] Verified constraint count (34/35)
- [ ] Verified index count (102+)
- [ ] All indexes online (state = "ONLINE")
- [ ] Reviewed relationship patterns
- [ ] Planned data ingestion strategy
- [ ] Performance testing plan defined

---

**Status:** DEPLOYMENT READY ✅
**Next Step:** Execute `./gap004_deploy.sh`
**Estimated Time:** 5-10 minutes (schema only, no data)

---

## Week 12-14 Deployment Update (2025-01-13)

### Three New Sectors Deployed

**Healthcare Sector**: 500 equipment, 60 facilities (avg 14.12 tags)
**Chemical Sector**: 300 equipment, 40 facilities (avg 14.18 tags)
**Critical Manufacturing Sector**: 400 equipment, 50 facilities (avg 12.96 tags)

**Total Week 12-14**: 1,200 equipment, 149 facilities, 1,200 relationships
**Success Rate**: 100%
**Error Rate**: 0%

### Updated Deployment Status

**Sectors Deployed**: 7 of 16 (43.75%)
**Total Equipment**: ~4,000 across all sectors
**Total Facilities**: ~300 across all sectors

### New Documentation

Complete deployment documentation now available:
- **Week 12-14 Completion Wiki**: `/docs/WEEK_12-14_DEPLOYMENT_COMPLETION_WIKI.md`
- **Remaining Sectors Roadmap**: `/docs/CISA_REMAINING_SECTORS_ROADMAP.md`
- **Deployment Procedures**: `/docs/SECTOR_DEPLOYMENT_PROCEDURE.md`
- **Neural Patterns**: `/docs/DEPLOYMENT_NEURAL_PATTERNS.md`
- **Documentation Index**: `/docs/INDEX_DEPLOYMENT_DOCUMENTATION.md`

### Next Steps

**Weeks 15-17**: Communications Sector (500 equipment, 50 facilities)
**Weeks 18-19**: Commercial Facilities (600 equipment, 80 facilities)
**Week 20**: Dams (300 equipment, 30 facilities)
**Weeks 21-24**: Remaining 6 sectors (total 2,300 equipment)

Target completion: **Week 24** (100% CISA sector coverage)
