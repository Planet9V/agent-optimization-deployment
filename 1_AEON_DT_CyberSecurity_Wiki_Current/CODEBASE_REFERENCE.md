# AEON Cyber Digital Twin - Codebase Reference

**Version**: 1.0.0
**Last Updated**: 2024-11-22
**Repository Root**: `/home/jim/2_OXOT_Projects_Dev/`

[← Back to Main Index](00_MAIN_INDEX.md)

---

## 📁 Directory Structure

```
/home/jim/2_OXOT_Projects_Dev/
│
├── 1_AEON_Cyber_DTv3_2025-11-19/          # Main AEON project
│   ├── 00_GOVERNANCE/                      # Governance documents
│   ├── 01_ARCHITECTURE/                    # Architecture specs
│   ├── 02_TECHNICAL_SPECS/                # Technical specifications
│   ├── 03_BUSINESS_CASE/                  # Business documentation
│   ├── 04_IMPLEMENTATION/                 # Implementation guides
│   ├── 05_TRAINING_DATA/                  # Training datasets
│   └── 06_REFERENCE_ARTIFACTS/            # Reference materials
│
├── 1_AEON_DT_CyberSecurity_Wiki_Current/  # THIS WIKI
│   ├── 00_MAIN_INDEX.md                   # Main index
│   ├── API_REFERENCE.md                   # API documentation
│   ├── QUERIES_LIBRARY.md                 # Cypher queries
│   ├── MAINTENANCE_GUIDE.md               # Maintenance procedures
│   ├── REPRODUCIBILITY_GUIDE.md           # Deployment guide
│   ├── ARCHITECTURE_OVERVIEW.md           # System architecture
│   ├── CODEBASE_REFERENCE.md             # This file
│   └── sectors/                           # Sector documentation
│       ├── WATER_SECTOR.md
│       ├── ENERGY_SECTOR.md
│       └── [14 more sector files]
│
├── scripts/                                # Deployment scripts
│   ├── deploy_communications_sector.cypher
│   ├── deploy_energy_expansion_sector.cypher
│   ├── deploy_financial_services_sector.cypher
│   ├── deploy_emergency_services_sector.cypher
│   ├── deploy_nuclear_sector.cypher
│   ├── deploy_dams_sector.cypher
│   ├── deploy_defense_industrial_base_sector.cypher
│   ├── deploy_commercial_facilities_sector.cypher
│   ├── deploy_food_agriculture_sector.cypher
│   ├── deploy_government_expansion_sector.cypher
│   ├── deploy_it_sector.cypher
│   └── universal_location_migration/
│       ├── WATER_SECTOR_IMPLEMENTATION.cypher
│       └── WATER_PHASE1_FACILITIES.cypher
│
├── tests/                                  # Test files and reports
│   ├── agentdb/
│   │   └── reports/                       # Deployment reports
│   │       ├── CHEMICAL_SECTOR_DEPLOYMENT_REPORT.md
│   │       └── chemical_deployment.cypher
│   ├── docs/
│   │   └── GAP004_MANUFACTURING_SECTOR_DEPLOYMENT_REPORT.md
│   └── scripts/
│       ├── manufacturing_deployment_gap004.cypher
│       └── manufacturing_equipment_deployment.cypher
│
├── docs/                                   # Documentation
│   └── WATER_SECTOR_IMPLEMENTATION_COMPLETE.md
│
├── openspg-official_neo4j/                # OpenSPG integration
│   ├── docs/
│   │   └── COMMUNICATIONS_SECTOR_COMPLETION_REPORT.md
│   └── scripts/
│       ├── communications_sector_complete.cypher
│       └── validate_communications.cypher
│
├── temp/                                   # Temporary files
│   ├── sector-*-pre-validated-architecture.json
│   └── *-SECTOR-*-REPORT.md
│
└── Import 1 NOV 2025/                     # Import data
    └── 7-3_TM - MITRE/
        └── scripts/
            └── neo4j_mitre_import.cypher
```

---

## 🔧 Key Script Files

### Sector Deployment Scripts

| File | Purpose | Nodes | Location |
|------|---------|-------|----------|
| `deploy_communications_sector.cypher` | Deploy Communications infrastructure | 40,759 | `/scripts/` |
| `deploy_energy_expansion_sector.cypher` | Deploy Energy sector expansion | 35,475 | `/scripts/` |
| `deploy_financial_services_sector.cypher` | Deploy Financial Services | 28,000 | `/scripts/` |
| `deploy_emergency_services_sector.cypher` | Deploy Emergency Services | 28,000 | `/scripts/` |
| `deploy_nuclear_sector.cypher` | Deploy Nuclear sector | 10,448 | `/scripts/` |
| `deploy_dams_sector.cypher` | Deploy Dams sector | 35,184 | `/scripts/` |
| `deploy_defense_industrial_base_sector.cypher` | Deploy Defense Industrial Base | 38,800 | `/scripts/` |
| `deploy_commercial_facilities_sector.cypher` | Deploy Commercial Facilities | 28,000 | `/scripts/` |
| `deploy_food_agriculture_sector.cypher` | Deploy Food & Agriculture | 28,000 | `/scripts/` |
| `deploy_government_expansion_sector.cypher` | Deploy Government Facilities | 27,000 | `/scripts/` |
| `deploy_it_sector.cypher` | Deploy Information Technology | 28,000 | `/scripts/` |

### Manufacturing Sector Scripts
```
/tests/scripts/
├── manufacturing_deployment_gap004.cypher     # Main deployment (93,900 nodes)
├── manufacturing_equipment_deployment.cypher  # Equipment deployment
└── manufacturing_5d_tagging.cypher           # 5D tagging system
```

### Water Sector Scripts
```
/scripts/universal_location_migration/
├── WATER_SECTOR_IMPLEMENTATION.cypher        # Complete implementation
└── WATER_PHASE1_FACILITIES.cypher           # Phase 1 facilities
```

---

## 📄 Governance Documents

### Location: `/1_AEON_Cyber_DTv3_2025-11-19/00_GOVERNANCE/`

Key Files:
- Schema governance standards
- Naming conventions
- Data quality requirements
- Compliance mappings

---

## 📊 Report Files

### Deployment Reports

| Report | Sector | Location |
|--------|--------|----------|
| `CHEMICAL_SECTOR_DEPLOYMENT_REPORT.md` | Chemical | `/tests/agentdb/reports/` |
| `GAP004_MANUFACTURING_SECTOR_DEPLOYMENT_REPORT.md` | Manufacturing | `/tests/docs/` |
| `COMMUNICATIONS_SECTOR_COMPLETION_REPORT.md` | Communications | `/openspg-official_neo4j/docs/` |
| `WATER_SECTOR_IMPLEMENTATION_COMPLETE.md` | Water | `/docs/` |

### Status Reports
- `100_PERCENT_COMPLETION_REPORT.md` - Overall completion status
- `ACCURATE_FINAL_STATUS_2025-11-21.md` - Final deployment status

---

## 🔐 Security & Compliance Files

### MITRE ATT&CK Import
```
/Import 1 NOV 2025/7-3_TM - MITRE/scripts/
└── neo4j_mitre_import.cypher              # MITRE framework import
```

### CVE Integration Scripts
```
/scripts/
├── normalize_cve_ids.cypher               # CVE ID normalization
├── validate_cve_ids.cypher                # CVE validation
├── merge_duplicate_cve_nodes.cypher       # Duplicate removal
└── rollback_cve_normalization.cypher      # Rollback capability
```

---

## 🛠️ Utility Scripts

### Database Maintenance
```cypher
// Location: /scripts/

// Schema migration
migrate_phase1_schema.cypher

// Constraint creation
gap004_missing_base_constraints.cypher

// Data validation
validate_communications.cypher
```

### Helper Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `fix_priority_field.cypher` | Fix priority field issues | One-time fix |
| `export_critical_metadata.cypher` | Export critical data | Backup |
| `merge_duplicate_cve_nodes.cypher` | Remove duplicates | Maintenance |

---

## 📋 Configuration Files

### Project Configuration
```
/1_AEON_Cyber_DTv3_2025-11-19/
├── .claude-flow/                          # Claude-flow configs
│   └── metrics/
│       ├── performance.json
│       ├── system-metrics.json
│       └── task-metrics.json
├── .hive-mind/                            # Hive-mind database
│   ├── hive.db
│   ├── hive.db-shm
│   └── hive.db-wal
└── .swarm/                                # Swarm memory
    └── memory.db
```

---

## 🗄️ Data Files

### Pre-validated Architectures
```
/temp/
├── sector-CHEMICAL-pre-validated-architecture.json
├── sector-COMMUNICATIONS-pre-validated-architecture.json
├── sector-COMMERCIAL_FACILITIES-pre-validated-architecture.json
├── sector-EMERGENCY_SERVICES-pre-validated-architecture.json
├── sector-FINANCIAL_SERVICES-pre-validated-architecture.json
├── sector-FOOD_AGRICULTURE-pre-validated-architecture.json
├── sector-GOVERNMENT_FACILITIES-pre-validated-architecture.json
└── sector-NUCLEAR-pre-validated-architecture.json
```

### Deployment Metadata
```
/temp/
├── sector-COMMUNICATIONS-deployment-metadata.json
├── sector-COMMUNICATIONS-schema-validation.json
└── sector-COMMUNICATIONS-final-validation.json
```

---

## 🚀 Execution Commands

### Deploy Single Sector
```bash
# Template
cypher-shell < /home/jim/2_OXOT_Projects_Dev/scripts/deploy_[sector_name]_sector.cypher

# Example: Deploy Water sector
cypher-shell < /home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/WATER_SECTOR_IMPLEMENTATION.cypher
```

### Deploy All Sectors
```bash
#!/bin/bash
# Location: Create as /home/jim/2_OXOT_Projects_Dev/scripts/deploy_all.sh

SCRIPTS_DIR="/home/jim/2_OXOT_Projects_Dev/scripts"

for script in $SCRIPTS_DIR/deploy_*_sector.cypher; do
  echo "Executing: $script"
  cypher-shell < "$script"
  sleep 5
done
```

### Validation Queries
```bash
# Check sector deployment
echo "MATCH (n) WHERE n.sector IS NOT NULL RETURN n.sector, count(n) ORDER BY count(n) DESC;" | cypher-shell

# Verify total nodes
echo "MATCH (n) RETURN count(n) as totalNodes;" | cypher-shell
```

---

## 📝 Template Files

### New Sector Template
```cypher
// Template location: Create as /scripts/templates/sector_template.cypher

// [SECTOR_NAME] Sector Deployment
// Created: [DATE]
// Target Nodes: [NUMBER]

// Create facilities
UNWIND range(1, [FACILITY_COUNT]) as i
CREATE (f:Facility {
  facilityId: '[SECTOR_CODE]-FAC-' + toString(i),
  name: '[Sector] Facility ' + toString(i),
  facilityType: '[FACILITY_TYPE]',
  sector: '[SECTOR_NAME]',
  state: 'CA',
  city: 'City',
  createdAt: datetime()
});

// Create equipment
MATCH (f:Facility {sector: '[SECTOR_NAME]'})
WITH f
UNWIND range(1, [EQUIPMENT_PER_FACILITY]) as j
CREATE (e:Equipment {
  equipmentId: 'EQ-[SECTOR_CODE]-' + f.facilityId + '-' + toString(j),
  equipmentType: '[Equipment Type]',
  sector: '[SECTOR_NAME]',
  tags: [
    'SECTOR_[SECTOR_NAME]',
    'EQUIP_TYPE_[TYPE]',
    'OPS_STATUS_OPERATIONAL'
  ],
  createdAt: datetime()
})-[:LOCATED_AT]->(f);
```

---

## 🔄 Version Control

### Git Configuration
```bash
# Repository information
Repository: /home/jim/2_OXOT_Projects_Dev/
Current Branch: gap-002-critical-fix
Main Branch: [not specified]

# Recent commits
e0b992d - feat(SESSION-END): Store critical learnings
25ffbac - fix(TASKMASTER): Revise to match schema
7bf37b1 - docs(ENFORCEMENT): How to follow TASKMASTER
5e77b06 - docs(ENFORCEMENT): Create exact prompt template
b1109ba - feat(SECTOR-16): Information Technology COMPLETE
```

### Modified Files (as of session start)
```
.claude-flow/metrics/performance.json
.claude-flow/metrics/system-metrics.json
.claude-flow/metrics/task-metrics.json
.hive-mind/hive.db-shm
.hive-mind/hive.db-wal
.swarm/memory.db
```

---

## 🔗 Quick Links

### Essential Scripts
- [All deployment scripts](/home/jim/2_OXOT_Projects_Dev/scripts/)
- [Manufacturing deployment](/home/jim/2_OXOT_Projects_Dev/tests/scripts/manufacturing_deployment_gap004.cypher)
- [Water implementation](/home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/WATER_SECTOR_IMPLEMENTATION.cypher)
- [MITRE import](/home/jim/2_OXOT_Projects_Dev/Import%201%20NOV%202025/7-3_TM%20-%20MITRE/scripts/neo4j_mitre_import.cypher)

### Key Documentation
- [100% Completion Report](/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/100_PERCENT_COMPLETION_REPORT.md)
- [Final Status](/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/ACCURATE_FINAL_STATUS_2025-11-21.md)

### Wiki Pages
- [Main Index](00_MAIN_INDEX.md)
- [API Reference](API_REFERENCE.md)
- [Queries Library](QUERIES_LIBRARY.md)
- [Maintenance Guide](MAINTENANCE_GUIDE.md)
- [Reproducibility Guide](REPRODUCIBILITY_GUIDE.md)
- [Architecture Overview](ARCHITECTURE_OVERVIEW.md)

---

**Wiki Navigation**: [Main](00_MAIN_INDEX.md) | [API](API_REFERENCE.md) | [Architecture](ARCHITECTURE_OVERVIEW.md) | [Maintenance](MAINTENANCE_GUIDE.md)