# Migration Execution Guide
**Enhancement 27**: Entity Expansion Psychohistory
**Migration**: 24 Labels → 16 Super Labels
**Version**: 1.0
**Date**: 2025-11-28

---

## Quick Reference

| Item | Value |
|------|-------|
| Script file | cypher/03_migration_24_to_16.cypher |
| Test script | cypher/test_migration.cypher |
| Total phases | 11 |
| Estimated time | 45-60 minutes |
| Rollback method | Restore from backup |

---

## Pre-Execution Checklist

### 1. Environment Verification
```bash
# Verify Neo4j is running
cypher-shell -u neo4j -p password "RETURN 'Connected' as status;"

# Check Neo4j version (require 4.x or 5.x)
cypher-shell -u neo4j -p password "CALL dbms.components() YIELD versions RETURN versions[0];"

# Verify APOC is available
cypher-shell -u neo4j -p password "RETURN apoc.version() as apoc_version;"
```

### 2. Backup Creation
```bash
# Stop Neo4j for cold backup (recommended)
sudo systemctl stop neo4j

# Backup database files
sudo tar -czf /backup/neo4j-pre-e27-$(date +%Y%m%d-%H%M%S).tar.gz \
  /var/lib/neo4j/data/databases/ \
  /var/lib/neo4j/data/transactions/

# Or use APOC for hot backup (Neo4j running)
cypher-shell -u neo4j -p password \
  "CALL apoc.export.cypher.all('/backup/pre_e27_migration.cypher', {format: 'cypher-shell'});"

# Verify backup file exists and has content
ls -lh /backup/pre_e27_migration.cypher
```

### 3. Database Health Check
```bash
# Check for long-running transactions
cypher-shell -u neo4j -p password \
  "CALL dbms.listTransactions() YIELD transactionId, elapsedTime WHERE elapsedTime.milliseconds > 1000 RETURN count(*);"

# Check database constraints
cypher-shell -u neo4j -p password \
  "CALL db.constraints();"

# Check database indexes
cypher-shell -u neo4j -p password \
  "CALL db.indexes();"
```

### 4. Baseline Metrics
```bash
# Save pre-migration label counts
cypher-shell -u neo4j -p password \
  "CALL db.labels() YIELD label WITH label MATCH (n) WHERE label IN labels(n) RETURN label, count(n) as count ORDER BY label;" \
  > /tmp/pre_migration_labels.txt

# Save pre-migration node count
cypher-shell -u neo4j -p password \
  "MATCH (n) RETURN count(n) as total_nodes;" \
  > /tmp/pre_migration_total.txt
```

---

## Phase-by-Phase Execution

### Phase 1: Backup Verification ✅
**Already completed in pre-execution checklist**

---

### Phase 2: Add Discriminator Properties

#### Execute Phase 2
```bash
# Extract Phase 2 queries
sed -n '/^// PHASE 2:/,/^// PHASE 3:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 3:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 2
```cypher
// Check discriminator property addition
MATCH (n:ThreatActor)
RETURN
  'ThreatActor' as label,
  count(*) as total,
  sum(CASE WHEN n.actorType IS NULL THEN 1 ELSE 0 END) as missing_discriminator,
  collect(DISTINCT n.actorType)[0..5] as sample_values;

MATCH (n:AttackPattern)
RETURN
  'AttackPattern' as label,
  count(*) as total,
  sum(CASE WHEN n.patternType IS NULL THEN 1 ELSE 0 END) as missing_discriminator,
  collect(DISTINCT n.patternType)[0..5] as sample_values;

MATCH (n:Organization)
RETURN
  'Organization' as label,
  count(*) as total,
  sum(CASE WHEN n.orgType IS NULL THEN 1 ELSE 0 END) as missing_discriminator,
  collect(DISTINCT n.orgType)[0..5] as sample_values;

MATCH (n:Location)
RETURN
  'Location' as label,
  count(*) as total,
  sum(CASE WHEN n.locationType IS NULL THEN 1 ELSE 0 END) as missing_discriminator,
  collect(DISTINCT n.locationType)[0..5] as sample_values;

MATCH (n:Software)
RETURN
  'Software' as label,
  count(*) as total,
  sum(CASE WHEN n.softwareType IS NULL THEN 1 ELSE 0 END) as missing_discriminator,
  collect(DISTINCT n.softwareType)[0..5] as sample_values;
```

**Expected**: All `missing_discriminator` counts should be 0

---

### Phase 3: Consolidate Attack Labels

#### Execute Phase 3
```bash
sed -n '/^// PHASE 3:/,/^// PHASE 4:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 4:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 3
```cypher
// Check AttackTechnique migration
MATCH (n:AttackTechnique)
RETURN 'AttackTechnique still exists' as error, count(n) as count;
// Expected: 0 nodes

MATCH (n:AttackPattern)
WHERE n.migrated_from = 'AttackTechnique'
RETURN
  'Migrated to AttackPattern' as status,
  count(n) as migrated_count,
  min(n.migration_date) as first_migration,
  max(n.migration_date) as last_migration;
```

---

### Phase 4: Consolidate Vulnerability Labels

#### Execute Phase 4
```bash
sed -n '/^// PHASE 4:/,/^// PHASE 5:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 5:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 4
```cypher
// Check deprecated labels removed
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN ['CVE', 'Exploit', 'VulnerabilityReport'])
RETURN labels(n) as remaining_labels, count(n) as count;
// Expected: 0 nodes

// Check Vulnerability consolidation
MATCH (n:Vulnerability)
WHERE n.migrated_from IN ['CVE', 'Exploit', 'VulnerabilityReport']
RETURN
  n.migrated_from as source,
  n.vulnType as discriminator,
  count(n) as migrated_count
ORDER BY source;
```

---

### Phase 5: Consolidate Malware Labels

#### Execute Phase 5
```bash
sed -n '/^// PHASE 5:/,/^// PHASE 6:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 6:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 5
```cypher
MATCH (n:MalwareVariant)
RETURN 'MalwareVariant still exists' as error, count(n) as count;
// Expected: 0

MATCH (n:Malware)
WHERE n.migrated_from = 'MalwareVariant'
RETURN
  'Migrated to Malware' as status,
  count(n) as migrated_count,
  collect(DISTINCT n.malwareFamily)[0..10] as sample_families;
```

---

### Phase 6: Consolidate Control/Mitigation Labels

#### Execute Phase 6
```bash
sed -n '/^// PHASE 6:/,/^// PHASE 7:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 7:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 6
```cypher
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN ['Mitigation', 'ComplianceFramework', 'NERCCIPStandard'])
RETURN labels(n) as remaining_labels, count(n) as count;
// Expected: 0

MATCH (n:Control)
WHERE n.migrated_from IN ['Mitigation', 'ComplianceFramework', 'NERCCIPStandard']
RETURN
  n.migrated_from as source,
  n.controlType as discriminator,
  count(n) as migrated_count
ORDER BY source;
```

---

### Phase 7: Consolidate Event Labels

#### Execute Phase 7
```bash
sed -n '/^// PHASE 7:/,/^// PHASE 8:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 8:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 7
```cypher
MATCH (n:IncidentReport)
RETURN 'IncidentReport still exists' as error, count(n) as count;
// Expected: 0

MATCH (n:Event)
WHERE n.migrated_from = 'IncidentReport'
RETURN
  'Migrated to Event' as status,
  n.eventType as discriminator,
  count(n) as migrated_count;
```

---

### Phase 8: Consolidate Organization Labels

#### Execute Phase 8
```bash
sed -n '/^// PHASE 8:/,/^// PHASE 9:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 9:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 8
```cypher
MATCH (n:Sector)
RETURN 'Sector still exists' as error, count(n) as count;
// Expected: 0

MATCH (n:Organization)
WHERE n.migrated_from = 'Sector'
RETURN
  'Migrated to Organization' as status,
  n.orgType as discriminator,
  count(n) as migrated_count;
```

---

### Phase 9: Consolidate OT/Infrastructure Assets

#### Execute Phase 9
```bash
sed -n '/^// PHASE 9:/,/^// PHASE 10:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 10:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 9
```cypher
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN [
  'Substation', 'TransmissionLine', 'EnergyDevice',
  'EnergyManagementSystem', 'DistributedEnergyResource', 'WaterSystem'
])
RETURN labels(n) as remaining_labels, count(n) as count;
// Expected: 0

MATCH (n:Asset)
WHERE n.migrated_from IN [
  'Substation', 'TransmissionLine', 'EnergyDevice',
  'EnergyManagementSystem', 'DistributedEnergyResource', 'WaterSystem'
]
RETURN
  n.migrated_from as source,
  n.deviceType as discriminator,
  n.purdue_level as purdue_level,
  count(n) as migrated_count
ORDER BY source;
```

---

### Phase 10: Consolidate Indicator Labels

#### Execute Phase 10
```bash
sed -n '/^// PHASE 10:/,/^// PHASE 11:/p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// PHASE 11:' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 10
```cypher
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN ['Measurement', 'EnergyProperty', 'WaterProperty'])
RETURN labels(n) as remaining_labels, count(n) as count;
// Expected: 0

MATCH (n:Indicator)
WHERE n.migrated_from IN ['Measurement', 'EnergyProperty', 'WaterProperty']
RETURN
  n.migrated_from as source,
  n.indicatorType as discriminator,
  count(n) as migrated_count
ORDER BY source;
```

---

### Phase 11: Create New Super Labels

#### Execute Phase 11
```bash
sed -n '/^// PHASE 11:/,$p' cypher/03_migration_24_to_16.cypher | \
  grep -v '^// VERIFICATION' | \
  cypher-shell -u neo4j -p password
```

#### Verify Phase 11
```cypher
MATCH (n:_Schema)
WHERE n.label IN ['PsychTrait', 'EconomicMetric', 'Role', 'Protocol', 'Campaign']
RETURN
  n.label as new_label,
  n.created as creation_time,
  n.properties as schema_properties
ORDER BY n.label;
// Expected: 5 schema nodes
```

---

## Final Verification

### 1. Complete Deprecated Label Check
```cypher
// This should return 0 for all deprecated labels
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN [
  'AttackTechnique', 'CVE', 'Exploit', 'VulnerabilityReport',
  'MalwareVariant', 'Mitigation', 'ComplianceFramework', 'NERCCIPStandard',
  'IncidentReport', 'Sector', 'Substation', 'TransmissionLine',
  'EnergyDevice', 'EnergyManagementSystem', 'DistributedEnergyResource',
  'WaterSystem', 'Measurement', 'EnergyProperty', 'WaterProperty'
])
RETURN labels(n)[0] as deprecated_label, count(*) as remaining_count;
```

**Expected**: Query returns 0 rows

### 2. Final Label Inventory
```cypher
CALL db.labels() YIELD label
WHERE NOT label STARTS WITH '_'
WITH label
MATCH (n) WHERE label IN labels(n)
RETURN label, count(n) as node_count
ORDER BY label;
```

**Expected**: Should show 16 Super Labels:
1. Asset
2. AttackPattern
3. Campaign
4. Control
5. EconomicMetric
6. Event
7. Indicator
8. Location
9. Malware
10. Organization
11. Protocol
12. PsychTrait
13. Role
14. Software
15. ThreatActor
16. Vulnerability

### 3. Migration Completeness
```cypher
MATCH (n)
WHERE n.migrated_from IS NOT NULL
RETURN
  n.migrated_from as source_label,
  labels(n)[0] as current_label,
  count(*) as migrated_count
ORDER BY source_label;
```

**Expected**: Should show migrations for all 19 deprecated labels

### 4. Node Count Verification
```cypher
MATCH (n) RETURN count(n) as post_migration_total;
```

Compare with `/tmp/pre_migration_total.txt` - **should be identical**

### 5. Discriminator Coverage
```cypher
// All kept labels should have 100% discriminator coverage
MATCH (n:ThreatActor)
RETURN 'ThreatActor' as label,
  count(*) as total,
  sum(CASE WHEN n.actorType IS NULL THEN 1 ELSE 0 END) as missing
UNION ALL
MATCH (n:AttackPattern)
RETURN 'AttackPattern', count(*),
  sum(CASE WHEN n.patternType IS NULL THEN 1 ELSE 0 END)
UNION ALL
MATCH (n:Organization)
RETURN 'Organization', count(*),
  sum(CASE WHEN n.orgType IS NULL THEN 1 ELSE 0 END)
UNION ALL
MATCH (n:Location)
RETURN 'Location', count(*),
  sum(CASE WHEN n.locationType IS NULL THEN 1 ELSE 0 END)
UNION ALL
MATCH (n:Software)
RETURN 'Software', count(*),
  sum(CASE WHEN n.softwareType IS NULL THEN 1 ELSE 0 END);
```

**Expected**: All `missing` counts should be 0

---

## Post-Migration Tasks

### 1. Update Application Queries
Review and update application code to use new label structure:

```cypher
// OLD: Direct label queries
MATCH (n:CVE) RETURN n;

// NEW: Use discriminator
MATCH (n:Vulnerability)
WHERE n.vulnType = 'cve'
RETURN n;
```

### 2. Recreate Indexes (if needed)
```cypher
// Create indexes on discriminator properties
CREATE INDEX threat_actor_type IF NOT EXISTS FOR (n:ThreatActor) ON (n.actorType);
CREATE INDEX attack_pattern_type IF NOT EXISTS FOR (n:AttackPattern) ON (n.patternType);
CREATE INDEX org_type IF NOT EXISTS FOR (n:Organization) ON (n.orgType);
CREATE INDEX location_type IF NOT EXISTS FOR (n:Location) ON (n.locationType);
CREATE INDEX software_type IF NOT EXISTS FOR (n:Software) ON (n.softwareType);
CREATE INDEX vuln_type IF NOT EXISTS FOR (n:Vulnerability) ON (n.vulnType);
CREATE INDEX control_type IF NOT EXISTS FOR (n:Control) ON (n.controlType);
CREATE INDEX asset_type IF NOT EXISTS FOR (n:Asset) ON (n.deviceType);
CREATE INDEX indicator_type IF NOT EXISTS FOR (n:Indicator) ON (n.indicatorType);
CREATE INDEX event_type IF NOT EXISTS FOR (n:Event) ON (n.eventType);
```

### 3. Performance Testing
```bash
# Run application test suite
npm test

# Check query performance
cypher-shell -u neo4j -p password < queries/performance_test.cypher
```

### 4. Documentation Updates
- Update schema documentation
- Update API documentation
- Update query examples
- Update developer guides

### 5. Cleanup Migration Metadata (Optional)
```cypher
// After verifying everything works, optionally remove migration tracking
MATCH (n)
WHERE n.migrated_from IS NOT NULL
REMOVE n.migrated_from, n.migration_date;
```

---

## Rollback Procedure

If issues are detected:

### 1. Stop Application
```bash
sudo systemctl stop your-app-service
```

### 2. Restore from Backup
```bash
# Stop Neo4j
sudo systemctl stop neo4j

# Remove current database
sudo rm -rf /var/lib/neo4j/data/databases/neo4j

# Restore from backup
sudo tar -xzf /backup/neo4j-pre-e27-YYYYMMDD-HHMMSS.tar.gz -C /

# Or restore from APOC export
cypher-shell -u neo4j -p password < /backup/pre_e27_migration.cypher

# Start Neo4j
sudo systemctl start neo4j
```

### 3. Verify Rollback
```bash
cypher-shell -u neo4j -p password "MATCH (n) RETURN count(n) as total;"
diff /tmp/pre_migration_labels.txt <(cypher-shell -u neo4j -p password "CALL db.labels() YIELD label WITH label MATCH (n) WHERE label IN labels(n) RETURN label, count(n) ORDER BY label;")
```

---

## Success Criteria

✅ **Migration is successful when**:
1. All 19 deprecated labels have 0 nodes
2. All 16 Super Labels exist and have expected node counts
3. Total node count matches pre-migration count
4. All discriminator properties have 100% coverage
5. All migrated nodes have tracking metadata
6. Application tests pass
7. Query performance is acceptable
8. No errors in Neo4j logs

---

## Support

**Issues**: Document in `/docs/migration_issues.md`
**Questions**: Contact database team
**Emergency**: Rollback procedure above

---

**Version**: 1.0
**Generated**: 2025-11-28
**Author**: BLOCKER RESOLUTION AGENT 4
**Status**: READY FOR EXECUTION
