# AEON Cyber Digital Twin - Reproducibility Guide

**Version**: 1.0.0
**Last Updated**: 2024-11-22
**Time to Deploy**: ~4-6 hours for all 16 sectors
**Database Size**: ~50GB when complete

[← Back to Main Index](00_MAIN_INDEX.md)

---

## 📋 Prerequisites

### System Requirements
```yaml
Hardware:
  CPU: 8+ cores recommended
  RAM: 16GB minimum, 32GB recommended
  Storage: 100GB SSD recommended

Software:
  Neo4j: Version 5.x or higher
  Neo4j Plugins: APOC required
  Node.js: 18+ (for claude-flow)
  Python: 3.8+ (optional, for scripts)
  Git: Latest version
```

### Neo4j Installation
```bash
# Ubuntu/Debian
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt-get install neo4j=1:5.*

# Start Neo4j
sudo systemctl start neo4j
sudo systemctl enable neo4j

# Verify installation
neo4j status
```

### APOC Plugin Installation
```bash
# Download APOC plugin
cd /var/lib/neo4j/plugins
wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.13.0/apoc-5.13.0-core.jar

# Configure Neo4j to allow APOC
echo "dbms.security.procedures.unrestricted=apoc.*" >> /etc/neo4j/neo4j.conf
echo "dbms.security.procedures.allowlist=apoc.*" >> /etc/neo4j/neo4j.conf

# Restart Neo4j
sudo systemctl restart neo4j
```

---

## 🚀 Step-by-Step Deployment

### Step 1: Clone Repository
```bash
# Clone the AEON project
cd /home/jim/2_OXOT_Projects_Dev
git clone [repository_url] AEON_Cyber_DTv3

# Navigate to project
cd AEON_Cyber_DTv3
```

### Step 2: Database Setup
```cypher
// Connect to Neo4j
cypher-shell -u neo4j -p password

// Create constraints for data integrity
CREATE CONSTRAINT equipment_id IF NOT EXISTS FOR (e:Equipment) REQUIRE e.equipmentId IS UNIQUE;
CREATE CONSTRAINT facility_id IF NOT EXISTS FOR (f:Facility) REQUIRE f.facilityId IS UNIQUE;
CREATE CONSTRAINT cve_id IF NOT EXISTS FOR (c:CVE) REQUIRE c.id IS UNIQUE;

// Create indexes for performance
CREATE INDEX sector_index IF NOT EXISTS FOR (n:Equipment) ON (n.sector);
CREATE INDEX facility_sector_index IF NOT EXISTS FOR (f:Facility) ON (f.sector);
CREATE INDEX tag_index IF NOT EXISTS FOR (e:Equipment) ON (e.tags);
```

### Step 3: Deploy MITRE ATT&CK Framework
```bash
# Run MITRE import script
neo4j-shell < /home/jim/2_OXOT_Projects_Dev/Import\ 1\ NOV\ 2025/7-3_TM\ -\ MITRE/scripts/neo4j_mitre_import.cypher

# Verify MITRE deployment
echo "MATCH (n:Technique) RETURN count(n) as techniques;" | cypher-shell
# Expected: ~600+ techniques
```

### Step 4: Deploy CVE Database
```cypher
// Import CVE data (sample - full import from NIST feeds)
LOAD CSV WITH HEADERS FROM 'file:///cve_data.csv' AS row
CREATE (cve:CVE {
  id: row.cveId,
  description: row.description,
  baseScore: toFloat(row.cvssScore),
  severity: row.severity,
  publishedDate: date(row.published),
  modifiedDate: date(row.modified)
});

// Verify CVE import
MATCH (cve:CVE) RETURN count(cve) as totalCVEs;
// Expected: 100,000+
```

---

## 🏭 Deploy All 16 CISA Sectors

### Deployment Order and Commands

#### 1. Water Sector (27,200 nodes)
```bash
# Deploy Water infrastructure
neo4j-shell < /home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/WATER_SECTOR_IMPLEMENTATION.cypher

# Verify
echo "MATCH (n) WHERE n.sector = 'WATER' RETURN count(n);" | cypher-shell
```

#### 2. Energy Sector (35,475 nodes)
```bash
# Deploy Energy infrastructure
neo4j-shell < /home/jim/2_OXOT_Projects_Dev/scripts/deploy_energy_expansion_sector.cypher

# Verify
echo "MATCH (n) WHERE n.sector = 'ENERGY' RETURN count(n);" | cypher-shell
```

#### 3. Communications Sector (40,759 nodes)
```bash
# Deploy Communications infrastructure
neo4j-shell < /home/jim/2_OXOT_Projects_Dev/scripts/deploy_communications_sector.cypher

# Verify
echo "MATCH (n) WHERE n.sector = 'COMMUNICATIONS' RETURN count(n);" | cypher-shell
```

#### 4. Nuclear Sector (10,448 nodes)
```bash
# Deploy Nuclear infrastructure
neo4j-shell < /home/jim/2_OXOT_Projects_Dev/scripts/deploy_nuclear_sector.cypher

# Verify
echo "MATCH (n) WHERE n.sector = 'NUCLEAR' RETURN count(n);" | cypher-shell
```

#### 5. Critical Manufacturing (93,900 nodes)
```bash
# Deploy Manufacturing infrastructure
neo4j-shell < /home/jim/2_OXOT_Projects_Dev/tests/scripts/manufacturing_deployment_gap004.cypher

# Verify
echo "MATCH (n) WHERE n.sector = 'CRITICAL_MANUFACTURING' RETURN count(n);" | cypher-shell
```

#### 6-16. Remaining Sectors
```bash
# Deploy remaining sectors
for sector in financial_services emergency_services dams defense_industrial_base commercial_facilities food_agriculture government_expansion it; do
  echo "Deploying $sector..."
  neo4j-shell < /home/jim/2_OXOT_Projects_Dev/scripts/deploy_${sector}_sector.cypher
  sleep 5
done
```

### Batch Deployment Script
```bash
#!/bin/bash
# Full deployment script - deploy_all_sectors.sh

SCRIPTS_DIR="/home/jim/2_OXOT_Projects_Dev/scripts"
NEO4J_USER="neo4j"
NEO4J_PASS="password"

# Array of deployment scripts
declare -a sectors=(
  "deploy_communications_sector.cypher:COMMUNICATIONS:40759"
  "deploy_energy_expansion_sector.cypher:ENERGY:35475"
  "deploy_financial_services_sector.cypher:FINANCIAL_SERVICES:28000"
  "deploy_emergency_services_sector.cypher:EMERGENCY_SERVICES:28000"
  "deploy_nuclear_sector.cypher:NUCLEAR:10448"
  "deploy_dams_sector.cypher:DAMS:35184"
  "deploy_defense_industrial_base_sector.cypher:DEFENSE_INDUSTRIAL_BASE:38800"
  "deploy_commercial_facilities_sector.cypher:COMMERCIAL_FACILITIES:28000"
  "deploy_food_agriculture_sector.cypher:FOOD_AGRICULTURE:28000"
  "deploy_government_expansion_sector.cypher:GOVERNMENT_FACILITIES:27000"
  "deploy_it_sector.cypher:INFORMATION_TECHNOLOGY:28000"
)

# Deploy each sector
for sector_info in "${sectors[@]}"; do
  IFS=':' read -r script sector_name expected_count <<< "$sector_info"

  echo "================================================"
  echo "Deploying $sector_name (Expected: $expected_count nodes)"
  echo "================================================"

  # Run deployment
  cypher-shell -u $NEO4J_USER -p $NEO4J_PASS < "$SCRIPTS_DIR/$script"

  # Verify deployment
  actual_count=$(echo "MATCH (n) WHERE n.sector = '$sector_name' RETURN count(n) as c;" | \
                 cypher-shell -u $NEO4J_USER -p $NEO4J_PASS --format plain | tail -1)

  echo "Deployed: $actual_count nodes (Expected: $expected_count)"

  if [ "$actual_count" -lt "$((expected_count * 95 / 100))" ]; then
    echo "WARNING: Node count below 95% of expected!"
  fi

  sleep 5
done

echo "================================================"
echo "All sectors deployed. Running final verification..."
echo "================================================"

# Final verification
cypher-shell -u $NEO4J_USER -p $NEO4J_PASS << EOF
MATCH (n)
WHERE n.sector IS NOT NULL
RETURN n.sector as Sector, count(n) as Nodes
ORDER BY Nodes DESC;
EOF
```

---

## ✅ Verification Queries

### Overall Deployment Status
```cypher
// Check all 16 sectors are present
WITH ['WATER', 'ENERGY', 'HEALTHCARE', 'FOOD_AGRICULTURE', 'CHEMICAL',
      'CRITICAL_MANUFACTURING', 'DEFENSE_INDUSTRIAL_BASE', 'GOVERNMENT_FACILITIES',
      'NUCLEAR', 'COMMUNICATIONS', 'FINANCIAL_SERVICES', 'EMERGENCY_SERVICES',
      'INFORMATION_TECHNOLOGY', 'TRANSPORTATION', 'COMMERCIAL_FACILITIES', 'DAMS'] as expected
MATCH (n)
WHERE n.sector IS NOT NULL
WITH expected, collect(DISTINCT n.sector) as deployed
RETURN size(expected) as ExpectedSectors,
       size(deployed) as DeployedSectors,
       [s IN expected WHERE NOT s IN deployed] as MissingSectors,
       [s IN deployed WHERE NOT s IN expected] as UnexpectedSectors;
```

### Node Count Verification
```cypher
// Verify node counts match expectations
WITH {
  'WATER': 27200,
  'ENERGY': 35475,
  'HEALTHCARE': 28000,
  'FOOD_AGRICULTURE': 28000,
  'CHEMICAL': 32200,
  'CRITICAL_MANUFACTURING': 93900,
  'DEFENSE_INDUSTRIAL_BASE': 38800,
  'GOVERNMENT_FACILITIES': 27000,
  'NUCLEAR': 10448,
  'COMMUNICATIONS': 40759,
  'FINANCIAL_SERVICES': 28000,
  'EMERGENCY_SERVICES': 28000,
  'INFORMATION_TECHNOLOGY': 28000,
  'TRANSPORTATION': 28000,
  'COMMERCIAL_FACILITIES': 28000,
  'DAMS': 35184
} as expectations
MATCH (n)
WHERE n.sector IS NOT NULL
WITH expectations, n.sector as sector, count(n) as actual
WITH expectations[sector] as expected, actual, sector
RETURN sector,
       expected,
       actual,
       round((actual * 100.0 / expected) - 100, 2) as percentDifference,
       CASE
         WHEN abs(actual - expected) < expected * 0.05 THEN 'PASS'
         ELSE 'FAIL'
       END as status
ORDER BY sector;
```

### Data Integrity Check
```cypher
// Check for required properties
MATCH (e:Equipment)
WITH count(e) as total,
     count(CASE WHEN e.equipmentId IS NULL THEN 1 END) as missingId,
     count(CASE WHEN e.sector IS NULL THEN 1 END) as missingSector,
     count(CASE WHEN e.equipmentType IS NULL THEN 1 END) as missingType,
     count(CASE WHEN e.tags IS NULL OR size(e.tags) = 0 THEN 1 END) as missingTags
RETURN total as TotalEquipment,
       missingId as MissingIds,
       missingSector as MissingSectors,
       missingType as MissingTypes,
       missingTags as MissingTags,
       CASE
         WHEN missingId + missingSector + missingType + missingTags = 0 THEN 'PASS'
         ELSE 'FAIL'
       END as IntegrityCheck;
```

---

## 🔄 Incremental Updates

### Add New Equipment to Existing Sector
```cypher
// Template for incremental additions
:param batch => 100;
:param sector => 'WATER';

UNWIND range(1, $batch) as i
CREATE (e:Equipment {
  equipmentId: 'EQ-' + $sector + '-NEW-' + toString(timestamp()) + '-' + toString(i),
  equipmentType: 'New Equipment Type',
  sector: $sector,
  tags: [
    'SECTOR_' + $sector,
    'EQUIP_TYPE_NEW',
    'OPS_STATUS_OPERATIONAL'
  ],
  createdAt: datetime()
});
```

### Update Deployment Timestamps
```cypher
// Mark deployment completion
MERGE (deployment:DeploymentRecord {version: 'v5.0'})
SET deployment.completedAt = datetime(),
    deployment.totalNodes = 536966,
    deployment.sectors = 16,
    deployment.status = 'COMPLETE'
RETURN deployment;
```

---

## 🛠️ Troubleshooting Deployment

### Common Issues

#### Issue: Out of Memory During Import
```bash
# Increase Neo4j heap memory
echo "server.memory.heap.initial_size=4g" >> /etc/neo4j/neo4j.conf
echo "server.memory.heap.max_size=8g" >> /etc/neo4j/neo4j.conf
echo "server.memory.pagecache.size=4g" >> /etc/neo4j/neo4j.conf

# Restart Neo4j
sudo systemctl restart neo4j
```

#### Issue: Slow Import Performance
```cypher
// Create indexes before import
CREATE INDEX tmp_import_idx FOR (n:Equipment) ON (n.tempImportId);

// Use periodic commit for large imports
:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///large_dataset.csv' AS row
CREATE (e:Equipment {equipmentId: row.id, sector: row.sector});

// Drop temporary index after import
DROP INDEX tmp_import_idx;
```

#### Issue: Duplicate Nodes Created
```cypher
// Use MERGE instead of CREATE
MERGE (e:Equipment {equipmentId: 'UNIQUE-ID'})
ON CREATE SET
  e.sector = 'SECTOR',
  e.createdAt = datetime()
ON MATCH SET
  e.updatedAt = datetime();
```

---

## 📊 Performance Benchmarks

### Expected Import Times
| Sector | Nodes | Import Time | Verification Time |
|--------|-------|-------------|-------------------|
| WATER | 27,200 | ~5 min | 30 sec |
| ENERGY | 35,475 | ~7 min | 30 sec |
| COMMUNICATIONS | 40,759 | ~8 min | 30 sec |
| CRITICAL_MANUFACTURING | 93,900 | ~18 min | 45 sec |
| NUCLEAR | 10,448 | ~3 min | 20 sec |
| Others (avg) | 28,000 | ~5 min | 30 sec |
| **TOTAL** | **536,966** | **~4 hours** | **10 min** |

### Query Performance Targets
```cypher
// These queries should complete in <1 second
PROFILE MATCH (e:Equipment) WHERE e.sector = 'WATER' RETURN count(e);
PROFILE MATCH (f:Facility) WHERE f.sector = 'ENERGY' RETURN count(f);
PROFILE MATCH (n) WHERE 'OPS_CRITICALITY_CRITICAL' IN n.tags RETURN count(n);
```

---

## 📝 Post-Deployment Checklist

- [ ] All 16 sectors deployed
- [ ] Total nodes: 536,966 ± 5%
- [ ] All indexes created
- [ ] Constraints enforced
- [ ] CVE database linked
- [ ] MITRE ATT&CK integrated
- [ ] Backup created
- [ ] Documentation updated
- [ ] Performance verified
- [ ] API endpoints tested

---

## 🔐 Security Hardening

### Secure Neo4j Installation
```bash
# Change default password
neo4j-admin dbms set-initial-password your-secure-password

# Enable authentication
echo "dbms.security.auth_enabled=true" >> /etc/neo4j/neo4j.conf

# Restrict network access
echo "server.default_listen_address=127.0.0.1" >> /etc/neo4j/neo4j.conf

# Enable SSL
echo "dbms.connector.bolt.tls_level=REQUIRED" >> /etc/neo4j/neo4j.conf
```

---

**Wiki Navigation**: [Main](00_MAIN_INDEX.md) | [API](API_REFERENCE.md) | [Maintenance](MAINTENANCE_GUIDE.md) | [Architecture](ARCHITECTURE_OVERVIEW.md)