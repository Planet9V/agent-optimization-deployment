# Cyber DT Utilities Quick Reference

Fast lookup guide for utility scripts and configurations.

## Setup (First Time)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download spaCy model
python -m spacy download en_core_web_lg

# 3. Configure Neo4j connection
cp config/neo4j_connection.env.example config/neo4j_connection.env
# Edit: config/neo4j_connection.env

# 4. Make environment available
export $(cat config/neo4j_connection.env | xargs)
```

---

## Database Backup & Restore

### Quick Backup
```bash
cd scripts/utilities
./backup_database.sh /backups cyber-dt-backups
# Creates: neo4j-YYYY-MM-DD_HH-MM-SS.dump.gz + checksum
```

### Quick Restore
```bash
./restore_database.sh /backups/neo4j-2025-10-29_15-30-45.dump.gz
# Requires explicit "YES" confirmation
```

### Verify Backup (No Restore)
```bash
./restore_database.sh /path/to/backup.dump.gz --verify-only
# Checks backup integrity without restore
```

---

## Test Data Management

### View Database Stats
```bash
python clear_test_data.py --stats
# Shows: total nodes, label types
```

### Dry Run (Preview)
```bash
python clear_test_data.py --namespace test_2024 --dry-run
# Shows what would be deleted
```

### Delete by Namespace
```bash
python clear_test_data.py --namespace test_2024
# Deletes all nodes in 'test_2024' namespace
```

### Delete by Node Type
```bash
python clear_test_data.py --type TEST_CVE
# Deletes all TEST_CVE nodes
```

### Full Cleanup
```bash
python clear_test_data.py --namespace dev_01 --cleanup-orphans --rebuild-indexes
# Namespace delete + orphan cleanup + index rebuild
```

---

## Schema Export

### Export All Formats
```bash
python export_schema_diagram.py --all
# Creates: schema.mmd, schema.graphml, schema.html, schema.json in docs/schema/
```

### Export Specific Formats
```bash
# Mermaid only (GitHub-friendly)
python export_schema_diagram.py --mermaid

# GraphML for yEd
python export_schema_diagram.py --graphml

# Interactive HTML
python export_schema_diagram.py --html

# Raw JSON
python export_schema_diagram.py --json
```

### Custom Output Directory
```bash
python export_schema_diagram.py --all --output /path/to/output
```

---

## Configuration Files

### NVD API (`config/nvd_api_config.yaml`)
- **Get API Key**: https://nvd.nist.gov/developers/request-an-api-key
- **Edit these fields**:
  - `api_key`: Your NVD API key
  - `min_score`: Minimum CVSS score (default: 0.0)
  - `years`: Limit to specific years
  - `namespace`: Data isolation namespace

### Neo4j Connection (`config/neo4j_connection.env`)
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password-here
NEO4J_DATABASE=neo4j
```

### Logging (`config/logging_config.yaml`)
- All logs go to `processing/logs/`
- Log files:
  - `cyberdt.log` - Main application
  - `errors.log` - Errors only
  - `nvd_import.log` - NVD operations
  - `database.log` - Database operations
  - `spacy_nlp.log` - NLP operations

### spaCy NLP (`config/spacy_config.yaml`)
- Default model: `en_core_web_lg`
- Custom patterns included for CVE, CWE, CAPEC, CVSS
- Batch size: 1000
- Parallel processes: 4 (adjust to CPU cores)

### Swarm Coordination (`config/swarm_coordination.yaml`)
- Agent types: researcher, coder, analyzer, integrator, reviewer
- Auto-scaling: 3-10 agents
- Coordination memory namespace: `cyber_dt`
- Checkpoint interval: 5 minutes

---

## Common Tasks

### Daily Operations
```bash
# Check database health
python clear_test_data.py --stats

# View recent logs
tail -50 processing/logs/cyberdt.log

# Check errors
tail -20 processing/logs/errors.log
```

### Weekly Maintenance
```bash
# Backup database
./backup_database.sh /backups cyber-dt-backups

# Clean test data
python clear_test_data.py --namespace test_weekly --cleanup-orphans

# Export schema
python export_schema_diagram.py --all
```

### Monthly Review
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Test restoration
./restore_database.sh /backups/neo4j-latest.dump.gz --verify-only

# Review logs for patterns
grep ERROR processing/logs/*.log | sort | uniq -c
```

---

## Troubleshooting

### Connection Issues
```bash
# Test Neo4j connection
python -c "from neo4j import GraphDatabase; \
    GraphDatabase.driver('bolt://localhost:7687', \
    auth=('neo4j', 'password')).verify_connectivity()"
```

### Script Help
```bash
# Backup help
./scripts/utilities/backup_database.sh --help

# Clear data help
python scripts/utilities/clear_test_data.py --help

# Export schema help
python scripts/utilities/export_schema_diagram.py --help
```

### Log Analysis
```bash
# Find errors in last hour
find processing/logs -name "*.log" -mmin -60 -exec grep ERROR {} +

# Count errors by type
grep -h ERROR processing/logs/*.log | cut -d: -f5 | sort | uniq -c
```

---

## File Locations

```
/home/jim/2_OXOT_Projects_Dev/
├── scripts/utilities/          ← Utility scripts
│   ├── backup_database.sh
│   ├── restore_database.sh
│   ├── clear_test_data.py
│   └── export_schema_diagram.py
├── config/                     ← Configuration files
│   ├── neo4j_connection.env
│   ├── nvd_api_config.yaml
│   ├── spacy_config.yaml
│   ├── logging_config.yaml
│   └── swarm_coordination.yaml
├── processing/                 ← Generated data
│   └── logs/                   ← Log files
├── backups/                    ← Database backups
└── docs/schema/                ← Exported schemas
```

---

## Environment Setup

### Recommended `.bashrc` alias
```bash
# Add to ~/.bashrc
alias neo-backup='~/2_OXOT_Projects_Dev/scripts/utilities/backup_database.sh'
alias neo-clean='python ~/2_OXOT_Projects_Dev/scripts/utilities/clear_test_data.py'
alias neo-schema='python ~/2_OXOT_Projects_Dev/scripts/utilities/export_schema_diagram.py'
```

Then source: `. ~/.bashrc`

Use shortcuts:
```bash
neo-backup /backups cyber-dt
neo-clean --stats
neo-schema --all
```

---

## Performance Tuning

### For Large Datasets
```yaml
# In config/spacy_config.yaml
batch_size: 5000              # Increase for larger batches
n_process: 8                  # Match your CPU cores

# In config/nvd_api_config.yaml
rate_limit.requests: 50       # Check NVD limits
rate_limit.period: 30
```

### For Limited Memory
```yaml
# Reduce batch sizes and parallel processes
batch_size: 500
n_process: 2

# In logging
maxBytes: 5242880  # 5MB instead of 10MB
```

---

## Version & Support

- **Created**: 2025-10-29
- **Status**: Production Ready
- **Python**: 3.8+
- **Neo4j**: 5.x
- **Documentation**: See UTILITY_SCRIPTS_SETUP.md

---

## Quick Links

- **Main Guide**: `UTILITY_SCRIPTS_SETUP.md`
- **Configuration Examples**: Individual YAML files in `config/`
- **Logs**: `processing/logs/`
- **Scripts**: `scripts/utilities/`

---

**Last Updated**: 2025-10-29
**Status**: COMPLETE - Ready for Production Use
