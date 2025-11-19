# Migration Guide: Existing Data → Phase 1 Schema

**Quick Start for Migration**

## 🚀 Step-by-Step Execution

### 1. Backup Database (CRITICAL)
```bash
# Stop Neo4j
sudo systemctl stop neo4j

# Create backup
neo4j-admin database backup neo4j --to-path=/home/jim/neo4j_backup_2025-10-29

# Restart Neo4j
sudo systemctl start neo4j

# Verify backup exists
ls -lh /home/jim/neo4j_backup_2025-10-29/
```

### 2. Run Schema Migration
```bash
# Connect with existing credentials
cypher-shell -u neo4j -p neo4j@openspg -f scripts/migrate_phase1_schema.cypher
```

### 3. Install Python Dependencies
```bash
cd /home/jim/2_OXOT_Projects_Dev
source venv/bin/activate  # Or create: python3 -m venv venv
pip install lxml neo4j python-dotenv tqdm
```

### 4. Import CAPEC Data
```bash
python3 src/ingestors/capec_xml_importer.py
```

### 5. Import ATT&CK Data
```bash
python3 src/ingestors/attack_stix_importer.py
```

### 6. Validate Migration
```bash
cypher-shell -u neo4j -p neo4j@openspg -f schemas/validation/phase1_validation_queries.cypher
```

## ✅ Expected Results

**Before Migration:**
- CVE nodes: ~19
- Relationships: ~200

**After Migration:**
- CVE nodes: 2,000-5,000
- CAPEC nodes: ~559
- ATT&CK Techniques: ~193
- **New capability**: 8+ hop attack chains

## 🔄 Rollback (if needed)
```bash
sudo systemctl stop neo4j
neo4j-admin database restore neo4j --from-path=/home/jim/neo4j_backup_2025-10-29 --force
sudo systemctl start neo4j
```

## 📚 Documentation
- Full strategy: `docs/Migration_Strategy_Existing_to_Phase1.md`
- Validation: `schemas/validation/phase1_validation_queries.cypher`
