# Neo4j CAPEC v3.9 Import Execution Guide

**Generated**: 2025-11-08
**Purpose**: Step-by-step guide for importing CAPEC v3.9 data into Neo4j
**Expected Outcome**: 500-2,000 complete CVE→CWE→CAPEC→ATT&CK attack chains

---

## Executive Summary

This guide provides comprehensive procedures for importing CAPEC v3.9 data into Neo4j, including:
- Pre-flight checks and database backup
- Import execution procedures
- Validation and verification steps
- Rollback strategy for failures
- Post-import optimization

**Critical Data Being Imported**:
- 615 CAPEC attack patterns
- 1,214 CAPEC→CWE relationships
- 272 CAPEC→ATT&CK relationships
- 39 CAPEC→OWASP relationships ✅ **NEW**
- 37 CAPEC→WASC relationships
- **Total**: 1,562 relationships
- 143 "Golden Bridge" patterns enabling complete chains

---

## Prerequisites

### 1. Neo4j Requirements
- **Neo4j Version**: 4.0+ recommended (5.x optimal)
- **Database Status**: Running and accessible
- **Available Storage**: Minimum 2GB free space
- **Backup Capability**: neo4j-admin dump utility available

### 2. Files Required
- `data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher` (656KB)
- `scripts/neo4j_capec_import_validator.py` (validation script)
- `scripts/log4shell_chain_validator.py` (demonstration script)

### 3. Access Requirements
- Neo4j credentials (username/password)
- Database write permissions
- Cypher-shell or Neo4j Browser access
- Sufficient privileges for backup/restore operations

---

## Phase 1: Pre-Flight Checks

### Step 1.1: Verify Neo4j Status

```bash
# Check Neo4j is running
systemctl status neo4j
# OR
neo4j status

# Expected: Active (running)
```

### Step 1.2: Check Current Database State

```cypher
// Connect to Neo4j
cypher-shell -u neo4j -p <password>

// Check existing CAPEC nodes
MATCH (capec:AttackPattern)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN count(capec) AS existing_capec_nodes;

// Expected: 0 (if this is first import)
// If > 0: You have existing CAPEC v3.9 data (see rollback section)
```

### Step 1.3: Verify Database Space

```bash
# Check available disk space
df -h /var/lib/neo4j

# Minimum Required: 2GB free
# Recommended: 5GB+ free
```

### Step 1.4: Check Current Chain Status (Baseline)

```cypher
// Count existing complete chains (should be 0)
MATCH chain = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:Weakness)
             <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
             -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
RETURN count(DISTINCT chain) AS complete_chains;

// Expected: 0
// Record this baseline for comparison
```

---

## Phase 2: Database Backup

### Step 2.1: Create Full Database Backup

```bash
# Stop Neo4j (if required by your version)
sudo systemctl stop neo4j

# Create backup directory
sudo mkdir -p /var/backups/neo4j

# Perform database dump
sudo neo4j-admin dump \
  --database=neo4j \
  --to=/var/backups/neo4j/pre-capec-import-$(date +%Y%m%d-%H%M%S).dump

# Expected output: Dump successful

# Start Neo4j
sudo systemctl start neo4j

# Wait for startup
sleep 10
```

**Alternative: Online Backup (Neo4j Enterprise)**
```bash
neo4j-admin backup \
  --backup-dir=/var/backups/neo4j \
  --name=pre-capec-import-$(date +%Y%m%d-%H%M%S)
```

### Step 2.2: Verify Backup

```bash
# Check backup file exists
ls -lh /var/backups/neo4j/pre-capec-import-*.dump

# Expected: File size > 100MB (depending on existing data)

# Test backup integrity (optional but recommended)
sudo neo4j-admin check-consistency \
  --database=/var/backups/neo4j/pre-capec-import-*.dump
```

---

## Phase 3: Import Execution

### Step 3.1: Review Import File

```bash
# Check Cypher file exists and is readable
ls -lh data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher

# Expected: 656KB file

# Preview first 50 lines
head -50 data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher

# Check line count
wc -l data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher

# Expected: ~2,100 lines
```

### Step 3.2: Execute Import (Recommended Method)

**Option A: Via Cypher-Shell (Recommended)**

```bash
# Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion

# Execute import with progress monitoring
cat data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher | \
  cypher-shell -u neo4j -p <password> 2>&1 | \
  tee logs/capec_import_$(date +%Y%m%d-%H%M%S).log

# Expected:
# - MERGE statements executing
# - No errors
# - Completion message at end
```

**Option B: Via Neo4j Browser**

1. Open Neo4j Browser: http://localhost:7474
2. Login with credentials
3. Copy contents of `CAPEC_V3.9_NEO4J_IMPORT.cypher`
4. Paste into query editor
5. Click "Play" button
6. Monitor execution progress
7. **Note**: May timeout for large imports - use cypher-shell instead

**Option C: Batch Import (For Large Datasets)**

```bash
# Split import into batches if needed
split -l 500 data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher batch_

# Execute each batch
for batch in batch_*; do
  echo "Executing $batch..."
  cat $batch | cypher-shell -u neo4j -p <password>
  sleep 2
done

# Cleanup batch files
rm batch_*
```

### Step 3.3: Monitor Import Progress

```bash
# In separate terminal, monitor Neo4j logs
tail -f /var/log/neo4j/neo4j.log

# Watch for:
# - ✅ Successful MERGE operations
# - ⚠️  Constraint violations (should be none)
# - ❌ Errors (investigate immediately)
```

### Step 3.4: Expected Import Duration

- **Small datasets** (< 100k CVEs): 2-5 minutes
- **Medium datasets** (100k-500k CVEs): 5-15 minutes
- **Large datasets** (> 500k CVEs): 15-30 minutes

---

## Phase 4: Post-Import Validation

### Step 4.1: Basic Node Count Verification

```cypher
// Verify CAPEC nodes imported
MATCH (capec:AttackPattern)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN count(capec) AS capec_nodes;

// Expected: 615

// Verify abstraction level distribution
MATCH (capec:AttackPattern)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN capec.abstraction AS level, count(*) AS count
ORDER BY count DESC;

// Expected:
// Detailed:  341
// Standard:  197
// Meta:      77
```

### Step 4.2: Relationship Verification

```cypher
// Verify CAPEC→CWE relationships
MATCH ()-[r:EXPLOITS_WEAKNESS]->()
WHERE r.source = 'CAPEC_v3.9_XML'
RETURN count(r) AS capec_cwe_rels;

// Expected: 1,214

// Verify CAPEC→ATT&CK relationships
MATCH ()-[r:IMPLEMENTS_TECHNIQUE]->()
WHERE r.source = 'CAPEC_v3.9_XML'
RETURN count(r) AS capec_attack_rels;

// Expected: 272

// Total new relationships
// Expected: 1,486
```

### Step 4.3: Golden Bridge Validation

```cypher
// Count patterns with BOTH CWE and ATT&CK mappings
MATCH (capec:AttackPattern)-[:EXPLOITS_WEAKNESS]->(cwe:Weakness)
MATCH (capec)-[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN count(DISTINCT capec) AS golden_bridges;

// Expected: 143
```

### Step 4.4: Complete Chain Verification

```cypher
// Count complete CVE→CWE→CAPEC→ATT&CK chains
MATCH chain = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:Weakness)
             <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
             -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN count(DISTINCT chain) AS complete_chains;

// Expected: 500-2,000 (depending on CVE→CWE coverage)
// If 0: Check that CVE→CWE relationships exist in database
```

### Step 4.5: Automated Validation Script

```bash
# Run comprehensive validation
cd /home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion

# Update Neo4j credentials in script first
nano scripts/neo4j_capec_import_validator.py
# Update NEO4J_PASSWORD at line 16

# Execute validation
python3 scripts/neo4j_capec_import_validator.py

# Expected output:
# ✅ CAPEC Nodes: 615 (Expected: 615+)
# ✅ CAPEC→CWE: 1,214 relationships (Expected: 1,214+)
# ✅ CAPEC→ATT&CK: 272 relationships (Expected: 272+)
# ✅ Golden Bridges: 143 patterns (Expected: 143+)
# ✅ Complete Chains: 500-2,000 (Expected: 500-2,000)
# ✅ ALL VALIDATIONS PASSED - CAPEC IMPORT SUCCESSFUL
```

---

## Phase 5: Demonstration & Verification

### Step 5.1: Log4Shell Chain Validation

```bash
# Validate Log4Shell complete attack chains
python3 scripts/log4shell_chain_validator.py

# Expected output:
# ✅ FOUND multiple complete attack chains for CVE-2021-44228
# Shows: CVE-2021-44228 → CWE → CAPEC → ATT&CK techniques
# Validates: T1190, T1059, T1203 techniques are reachable
```

### Step 5.2: SBOM Risk Assessment Demo

```bash
# Run SBOM risk assessment demonstration
python3 scripts/sbom_risk_assessment_demo.py

# Expected output:
# 📦 Component risk assessments for Log4j, OpenSSL, Struts, Spring
# 🎯 ATT&CK techniques enabled by each CVE
# 📊 Risk scores and prioritization
# 💡 Business value demonstration complete
```

### Step 5.3: Sample Chain Queries

```cypher
// Example 1: Find all attack techniques enabled by a specific CVE
MATCH (cve:CVE {id: 'CVE-2021-44228'})
     -[:HAS_WEAKNESS]->(cwe:Weakness)
     <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
     -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN DISTINCT attack.id, attack.name
ORDER BY attack.id;

// Example 2: Find all CAPECs for a specific CWE
MATCH (capec:AttackPattern)-[:EXPLOITS_WEAKNESS]->(cwe:Weakness {id: 'CWE-89'})
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN capec.id, capec.name, capec.abstraction
ORDER BY capec.abstraction, capec.id;

// Example 3: Analyze attack surface for a software component
MATCH (product:Product {name: 'Apache Log4j'})
     -[:HAS_VULNERABILITY]->(cve:CVE)
     -[:HAS_WEAKNESS]->(cwe:Weakness)
     <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
     -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
     -[:PART_OF_TACTIC]->(tactic:Tactic)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN DISTINCT
    cve.id,
    attack.id AS technique,
    attack.name,
    tactic.name AS tactic
ORDER BY tactic.name, attack.id;
```

---

## Phase 6: Post-Import Optimization

### Step 6.1: Create Indexes (If Not Exists)

```cypher
// Create indexes for performance optimization
CREATE INDEX capec_id_index IF NOT EXISTS
FOR (n:AttackPattern) ON (n.id);

CREATE INDEX capec_source_index IF NOT EXISTS
FOR (n:AttackPattern) ON (n.source);

CREATE INDEX capec_abstraction_index IF NOT EXISTS
FOR (n:AttackPattern) ON (n.abstraction);

// Wait for indexes to build
CALL db.awaitIndexes(300);
```

### Step 6.2: Update Statistics

```cypher
// Update query planner statistics
CALL db.stats.collect();
```

### Step 6.3: Verify Performance

```cypher
// Test query performance (should be < 5 seconds)
PROFILE
MATCH chain = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:Weakness)
             <-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)
             -[:IMPLEMENTS_TECHNIQUE]->(attack:Technique)
WHERE capec.source = 'CAPEC_v3.9_XML'
  AND cve.id STARTS WITH 'CVE-2021'
RETURN count(chain)
LIMIT 100;

// Review query plan for full scans (should use indexes)
```

---

## Rollback Procedures

### Scenario 1: Import Failed Mid-Execution

**Symptoms**: Errors during import, incomplete data, database inconsistency

**Procedure**:

```bash
# 1. Stop Neo4j
sudo systemctl stop neo4j

# 2. Restore from backup
sudo neo4j-admin load \
  --from=/var/backups/neo4j/pre-capec-import-YYYYMMDD-HHMMSS.dump \
  --database=neo4j \
  --force

# 3. Start Neo4j
sudo systemctl start neo4j

# 4. Verify restore
cypher-shell -u neo4j -p <password> \
  "MATCH (capec:AttackPattern) WHERE capec.source = 'CAPEC_v3.9_XML' RETURN count(capec);"

# Expected: 0 (back to pre-import state)
```

### Scenario 2: Import Successful But Validation Failed

**Symptoms**: Nodes imported but counts don't match expectations

**Procedure**:

```cypher
// Option A: Remove only CAPEC v3.9 data
MATCH (capec:AttackPattern)
WHERE capec.source = 'CAPEC_v3.9_XML'
DETACH DELETE capec;

// Verify deletion
MATCH (capec:AttackPattern)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN count(capec);
// Expected: 0

// Then retry import
```

```bash
# Option B: Full database restore (if Option A insufficient)
# Follow Scenario 1 procedures
```

### Scenario 3: Performance Issues After Import

**Symptoms**: Slow queries, high memory usage, database unresponsive

**Procedure**:

```cypher
// 1. Check for missing indexes
SHOW INDEXES;

// 2. Rebuild indexes if needed
DROP INDEX capec_id_index IF EXISTS;
CREATE INDEX capec_id_index FOR (n:AttackPattern) ON (n.id);

// 3. Clear query cache
CALL db.clearQueryCaches();

// 4. Restart Neo4j (if needed)
// Exit cypher-shell
:exit
```

```bash
sudo systemctl restart neo4j
```

---

## Troubleshooting Common Issues

### Issue 1: "Database not found"

**Cause**: Default database name mismatch

**Solution**:
```bash
# Check active database
cypher-shell -u neo4j -p <password> "SHOW DATABASES;"

# Modify import command to specify database
cat data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher | \
  cypher-shell -u neo4j -p <password> -d <your-database-name>
```

### Issue 2: "Authentication failed"

**Cause**: Incorrect credentials

**Solution**:
```bash
# Reset Neo4j password
neo4j-admin set-initial-password <new-password>

# Retry import with correct password
```

### Issue 3: "Constraint violation"

**Cause**: Duplicate CAPEC nodes exist

**Solution**:
```cypher
// Check for existing CAPEC v3.9 nodes
MATCH (capec:AttackPattern)
WHERE capec.source = 'CAPEC_v3.9_XML'
RETURN count(capec);

// If > 0, remove before re-importing
MATCH (capec:AttackPattern)
WHERE capec.source = 'CAPEC_v3.9_XML'
DETACH DELETE capec;
```

### Issue 4: "Complete chains still 0"

**Cause**: Missing CVE→CWE relationships in database

**Solution**:
```cypher
// Verify CVE→CWE relationships exist
MATCH (cve:CVE)-[:HAS_WEAKNESS]->(cwe:Weakness)
RETURN count(*) AS cve_cwe_relationships;

// If 0: CVE data must be imported first with CWE mappings
// Refer to CVE/CWE import documentation
```

### Issue 5: "Import taking too long"

**Cause**: Large transaction size, insufficient memory

**Solution**:
```bash
# Increase heap size in neo4j.conf
sudo nano /etc/neo4j/neo4j.conf

# Add/modify:
# dbms.memory.heap.initial_size=2g
# dbms.memory.heap.max_size=4g

# Restart Neo4j
sudo systemctl restart neo4j

# Retry import
```

---

## Verification Checklist

Use this checklist to confirm successful import:

- [ ] **Pre-Flight**
  - [ ] Neo4j running and accessible
  - [ ] Database backup created successfully
  - [ ] Backup verified with check-consistency
  - [ ] Baseline chain count recorded (should be 0)

- [ ] **Import Execution**
  - [ ] Cypher file executed without errors
  - [ ] Import log shows successful MERGE statements
  - [ ] No constraint violations occurred
  - [ ] No authentication/permission errors

- [ ] **Validation**
  - [ ] 615 CAPEC nodes imported
  - [ ] 1,214 CAPEC→CWE relationships created
  - [ ] 272 CAPEC→ATT&CK relationships created
  - [ ] 143 Golden Bridge patterns verified
  - [ ] 500-2,000 complete chains exist
  - [ ] Automated validator passes all tests

- [ ] **Demonstration**
  - [ ] Log4Shell validator shows complete chains
  - [ ] SBOM risk assessment runs successfully
  - [ ] Sample queries return expected results
  - [ ] Query performance acceptable (< 5s)

- [ ] **Post-Import**
  - [ ] Indexes created successfully
  - [ ] Statistics updated
  - [ ] Performance optimized
  - [ ] Backup retained for rollback

---

## Success Metrics

### Technical Metrics

| Metric | Target | Verification Query |
|--------|--------|-------------------|
| CAPEC Nodes | 615 | `MATCH (c:AttackPattern) WHERE c.source = 'CAPEC_v3.9_XML' RETURN count(c)` |
| CAPEC→CWE | 1,214 | `MATCH ()-[r:EXPLOITS_WEAKNESS]->() WHERE r.source = 'CAPEC_v3.9_XML' RETURN count(r)` |
| CAPEC→ATT&CK | 272 | `MATCH ()-[r:IMPLEMENTS_TECHNIQUE]->() WHERE r.source = 'CAPEC_v3.9_XML' RETURN count(r)` |
| Golden Bridges | 143 | `MATCH (c:AttackPattern)-[:EXPLOITS_WEAKNESS]->(), (c)-[:IMPLEMENTS_TECHNIQUE]->() WHERE c.source = 'CAPEC_v3.9_XML' RETURN count(DISTINCT c)` |
| Complete Chains | 500-2,000 | `MATCH chain = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:Weakness)<-[:EXPLOITS_WEAKNESS]-(capec:AttackPattern)-[:IMPLEMENTS_TECHNIQUE]->(attack:Technique) WHERE capec.source = 'CAPEC_v3.9_XML' RETURN count(DISTINCT chain)` |

### Business Value Delivered

- ✅ **SBOM Risk Assessment**: CVE vulnerabilities now map to ATT&CK techniques
- ✅ **Threat Intelligence**: Complete attack chain visibility for security teams
- ✅ **Attack Surface Analysis**: Quantified attack paths from vulnerabilities to tactics
- ✅ **Security Control Mapping**: Link CVE remediations to ATT&CK mitigations
- ✅ **Red Team Planning**: Identify exploitable CVE-based attack paths

---

## Next Steps After Import

1. **Extract NER Training Data**: Run CAPEC description extractor for NER model training
2. **Integrate with SIEM**: Export attack chain data to security monitoring tools
3. **Create Dashboards**: Build visualization dashboards for attack chain analysis
4. **Automate Monitoring**: Set up alerts for new CVEs matching Golden Bridge patterns
5. **Expand Coverage**: Import additional threat intelligence sources (STIX, TAXII)

---

## Support & References

**Documentation**:
- CAPEC Analysis Report: `data/capec_analysis/CAPEC_V3.9_ANALYSIS_REPORT.json`
- Solution Documentation: `docs/CAPEC_ATTACK_CHAIN_SOLUTION.md`
- Validation Results: `data/capec_analysis/CAPEC_IMPORT_VALIDATION.json`

**Scripts**:
- Import File: `data/capec_analysis/CAPEC_V3.9_NEO4J_IMPORT.cypher`
- Validator: `scripts/neo4j_capec_import_validator.py`
- Log4Shell Demo: `scripts/log4shell_chain_validator.py`
- SBOM Demo: `scripts/sbom_risk_assessment_demo.py`

**Backup Location**: `/var/backups/neo4j/pre-capec-import-*.dump`

---

**Guide Version**: 1.0
**Last Updated**: 2025-11-08
**Maintained By**: CAPEC Integration Team
