# Enhancement 02: STIX 2.1 Integration - Prerequisites and Requirements

**File:** PREREQUISITES.md
**Created:** 2025-11-25 14:45:00 UTC
**Version:** v1.0.0
**Enhancement:** ENH-002-STIX-INTEGRATION
**Status:** ACTIVE

---

## Document Purpose

This document defines all prerequisites, requirements, dependencies, and pre-execution validation steps necessary for successful STIX 2.1 Threat Intelligence Integration into the AEON Digital Twin Neo4j knowledge graph.

**Target Audience**: Enhancement execution team (10-agent swarm), system administrators, project stakeholders

---

## Table of Contents

1. [Data Prerequisites](#data-prerequisites)
2. [Infrastructure Prerequisites](#infrastructure-prerequisites)
3. [Software Prerequisites](#software-prerequisites)
4. [Knowledge Prerequisites](#knowledge-prerequisites)
5. [Security Prerequisites](#security-prerequisites)
6. [Pre-Execution Validation](#pre-execution-validation)
7. [Resource Allocation](#resource-allocation)
8. [Contingency Planning](#contingency-planning)

---

## Data Prerequisites

### STIX Training Data Files

**Requirement**: Access to 5 STIX 2.1 training data files containing threat intelligence

**File Location**: `/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/`

**Required Files**:

1. **01_STIX_Attack_Patterns.md**
   - **Description**: STIX attack-pattern objects with kill chain phases and MITRE ATT&CK external references
   - **Expected Content**: 50-100 attack patterns
   - **Format**: Markdown with embedded JSON code blocks
   - **Size Estimate**: 500 KB - 2 MB
   - **Validation**: File exists, readable, contains JSON code blocks

2. **02_STIX_Threat_Actors.md**
   - **Description**: STIX threat-actor and intrusion-set objects with actor profiles, aliases, motivations
   - **Expected Content**: 30-50 threat actors
   - **Format**: Markdown with embedded JSON code blocks
   - **Size Estimate**: 300 KB - 1 MB
   - **Validation**: File exists, readable, contains valid STIX threat-actor objects

3. **03_STIX_Indicators_IOCs.md**
   - **Description**: STIX indicator objects (IOCs) including file hashes, IP addresses, domains
   - **Expected Content**: 500-1,000 indicators
   - **Format**: Markdown with embedded JSON code blocks
   - **Size Estimate**: 1 MB - 5 MB
   - **Validation**: File exists, readable, contains valid STIX indicator patterns

4. **04_STIX_Malware_Infrastructure.md**
   - **Description**: STIX malware and tool objects with malware families, capabilities, infrastructure
   - **Expected Content**: 100-200 malware/tools
   - **Format**: Markdown with embedded JSON code blocks
   - **Size Estimate**: 500 KB - 2 MB
   - **Validation**: File exists, readable, contains valid STIX malware objects

5. **05_STIX_Campaigns_Reports.md**
   - **Description**: STIX campaign and report objects with campaign timelines, objectives, attribution
   - **Expected Content**: 20-40 campaigns
   - **Format**: Markdown with embedded JSON code blocks
   - **Size Estimate**: 300 KB - 1 MB
   - **Validation**: File exists, readable, contains valid STIX campaign objects

**Validation Command**:
```bash
# Verify all STIX training files exist
ls -lh /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/01_STIX_*.md \
      /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/02_STIX_*.md \
      /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/03_STIX_*.md \
      /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/04_STIX_*.md \
      /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/05_STIX_*.md
```

**Expected Output**: 5 files listed with sizes between 300 KB - 5 MB

### STIX Data Quality Assumptions

**Schema Compliance**:
- All STIX objects conform to STIX 2.1 specification
- Required properties present: `type`, `id`, `created`, `modified`
- STIX identifiers follow format: `<type>--<uuid>` (e.g., `threat-actor--bef4c620-...`)
- Timestamps in ISO 8601 format (e.g., `2023-01-15T10:30:00.000Z`)

**Relationship Integrity**:
- All STIX relationship objects (`type: "relationship"`) reference valid source and target STIX IDs
- External references include MITRE ATT&CK IDs where applicable (e.g., `T1566.001`)
- Circular references avoided (no A → B → A chains)

**Content Quality**:
- Threat actor objects include: `name`, `description`, `aliases`, `threat_actor_types`
- Attack patterns include: `name`, `description`, `kill_chain_phases`
- Malware objects include: `name`, `malware_types`, `is_family`
- Indicators include: `pattern` (STIX pattern language), `indicator_types`
- Campaigns include: `name`, `description`, `first_seen`, `last_seen`

---

## Infrastructure Prerequisites

### Neo4j Database Requirements

**Version**: Neo4j 5.x or later (tested with Neo4j 5.14.1)

**Database Status**: Running and accessible

**Connection Details**:
- **URI**: `bolt://localhost:7687` (or custom URI)
- **Authentication**: Username and password required
- **Protocol**: Bolt protocol (default port 7687)

**Database Capacity**:
- **Disk Space**: Minimum 5 GB free space (recommended 10 GB)
- **Memory**: Minimum 4 GB allocated to Neo4j (recommended 8 GB)
- **CPU**: Multi-core recommended for batch operations

**Existing Data**:
- **MITRE ATT&CK Framework**: 691 technique nodes must exist
- **Node Label**: `AttackPattern` (or custom label for MITRE techniques)
- **Required Property**: `external_id` (e.g., "T1566.001")
- **Relationship**: `(:AttackPattern)-[:PART_OF]->(:Tactic)` recommended

**Verification Query**:
```cypher
// Verify MITRE ATT&CK nodes exist
MATCH (n:AttackPattern)
WHERE n.external_id IS NOT NULL
RETURN count(n) AS mitre_technique_count,
       count(DISTINCT n.external_id) AS unique_techniques,
       collect(DISTINCT n.external_id)[0..5] AS sample_ids
```

**Expected Result**:
```
mitre_technique_count: ~691
unique_techniques: ~691
sample_ids: ["T1566.001", "T1078", "T1190", ...]
```

**Database Permissions**:
- **Read**: Required to query existing MITRE nodes
- **Write**: Required to create new STIX nodes and relationships
- **Index Management**: Required to create indexes on STIX ID properties
- **Constraint Management**: Required to enforce STIX ID uniqueness

### Network Connectivity

**Local Database**:
- Neo4j accessible via localhost (default setup)
- No firewall blocking port 7687

**Remote Database** (if applicable):
- Network connectivity to remote Neo4j instance
- SSL/TLS configuration if required
- Firewall rules allow bolt protocol (port 7687)

---

## Software Prerequisites

### Python Environment

**Python Version**: Python 3.9 or later (tested with Python 3.11)

**Verification Command**:
```bash
python3 --version
# Expected: Python 3.9.x or later
```

### Required Python Libraries

**Core Libraries**:

1. **stix2** (Version 3.0.1)
   - **Purpose**: STIX 2.1 parsing, validation, and object manipulation
   - **Installation**: `pip install stix2==3.0.1`
   - **Validation**: `python3 -c "import stix2; print(stix2.__version__)"`

2. **neo4j** (Version 5.14.1)
   - **Purpose**: Neo4j Python driver for database operations
   - **Installation**: `pip install neo4j==5.14.1`
   - **Validation**: `python3 -c "import neo4j; print(neo4j.__version__)"`

3. **jsonschema** (Version 4.20.0)
   - **Purpose**: JSON schema validation for STIX objects
   - **Installation**: `pip install jsonschema==4.20.0`
   - **Validation**: `python3 -c "import jsonschema; print(jsonschema.__version__)"`

4. **pandas** (Version 2.1.3)
   - **Purpose**: Data manipulation and reporting
   - **Installation**: `pip install pandas==2.1.3`
   - **Validation**: `python3 -c "import pandas; print(pandas.__version__)"`

5. **pytest** (Version 7.4.3)
   - **Purpose**: Testing framework for validation suite
   - **Installation**: `pip install pytest==7.4.3`
   - **Validation**: `pytest --version`

6. **python-dotenv** (Version 1.0.0)
   - **Purpose**: Environment variable management (.env file support)
   - **Installation**: `pip install python-dotenv==1.0.0`
   - **Validation**: `python3 -c "import dotenv; print(dotenv.__version__)"`

**Bulk Installation**:
```bash
# Create requirements.txt
cat > requirements.txt <<EOF
stix2==3.0.1
neo4j==5.14.1
jsonschema==4.20.0
pandas==2.1.3
pytest==7.4.3
python-dotenv==1.0.0
EOF

# Install all dependencies
pip install -r requirements.txt
```

**Verification Script**:
```bash
# Verify all libraries installed correctly
python3 <<EOF
import sys
try:
    import stix2
    import neo4j
    import jsonschema
    import pandas
    import pytest
    import dotenv
    print("✓ All required libraries installed successfully")
    sys.exit(0)
except ImportError as e:
    print(f"✗ Missing library: {e}")
    sys.exit(1)
EOF
```

### Environment Configuration

**Environment Variables** (`.env` file):
```bash
# Neo4j Database Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_secure_password_here

# STIX Training Data Location
STIX_TRAINING_DATA_PATH=/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/

# Output Directory
STIX_OUTPUT_PATH=/home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_02_STIX_Integration/

# Performance Configuration
STIX_BATCH_SIZE=1000
STIX_TIMEOUT_SECONDS=300
NEO4J_MAX_CONNECTION_POOL_SIZE=50
```

**Security Note**: Never commit `.env` file to version control. Add `.env` to `.gitignore`.

---

## Knowledge Prerequisites

### STIX 2.1 Specification Understanding

**Required Knowledge**:
1. **STIX Object Types**: SDOs (Domain Objects) vs. SROs (Relationship Objects)
2. **STIX Identifier Format**: `<type>--<uuid>` pattern
3. **STIX Properties**: Common properties (`type`, `id`, `created`, `modified`, `spec_version`)
4. **STIX Relationships**: `relationship_type`, `source_ref`, `target_ref`
5. **STIX External References**: Linking to MITRE ATT&CK via `external_references` array

**Reference Documentation**:
- OASIS STIX 2.1 Specification: https://docs.oasis-open.org/cti/stix/v2.1/
- STIX 2.1 Objects Reference: https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html
- Python STIX 2.1 Library Docs: https://stix2.readthedocs.io/

### Neo4j Graph Database Understanding

**Required Knowledge**:
1. **Cypher Query Language**: Basic syntax for creating nodes and relationships
2. **Graph Data Model**: Nodes, relationships, properties, labels
3. **Batch Operations**: `UNWIND` pattern for bulk node/relationship creation
4. **Indexes and Constraints**: Performance optimization and data integrity
5. **Transaction Management**: Ensuring atomicity of batch operations

**Reference Documentation**:
- Neo4j Cypher Manual: https://neo4j.com/docs/cypher-manual/current/
- Neo4j Python Driver Docs: https://neo4j.com/docs/python-manual/current/
- Neo4j Performance Tuning: https://neo4j.com/docs/operations-manual/current/performance/

### MITRE ATT&CK Framework Understanding

**Required Knowledge**:
1. **Technique Hierarchy**: Tactics → Techniques → Sub-techniques
2. **Technique Identifiers**: Format (e.g., T1566 = Phishing, T1566.001 = Spearphishing Attachment)
3. **STIX Representation**: MITRE publishes ATT&CK in STIX 2.1 format
4. **External Reference Mapping**: Linking STIX attack patterns to MITRE techniques

**Reference Documentation**:
- MITRE ATT&CK Website: https://attack.mitre.org/
- MITRE ATT&CK STIX Data: https://github.com/mitre/cti
- STIX to ATT&CK Mapping: https://github.com/mitre-attack/attack-stix-data

---

## Security Prerequisites

### Database Security

**Authentication**:
- Secure Neo4j username and password configured
- Credentials stored in `.env` file (not hardcoded)
- `.env` file has restricted permissions (chmod 600)

**Authorization**:
- Database user has read/write permissions
- Database user can create indexes and constraints
- Principle of least privilege applied

**Network Security**:
- Neo4j accessible only from trusted hosts
- SSL/TLS enabled for remote connections (if applicable)
- Firewall rules restrict access to Neo4j port

### Data Security

**STIX Data Classification**:
- **Sensitivity**: Unclassified threat intelligence (public sources)
- **Distribution**: TLP:WHITE or TLP:GREEN (Traffic Light Protocol)
- **Compliance**: No classified or proprietary data in training files

**Data Handling**:
- STIX training data stored securely (file permissions 644 or more restrictive)
- No sensitive data (passwords, API keys) in STIX objects
- Audit trail for data ingestion (who, what, when)

### Code Security

**Secure Coding Practices**:
- Input validation for STIX objects (schema validation)
- SQL injection prevention (parameterized Cypher queries)
- Error handling (no sensitive information in error messages)
- Dependency vulnerability scanning (pip-audit or safety)

**Dependency Audit**:
```bash
# Check for known vulnerabilities in Python dependencies
pip install pip-audit
pip-audit
```

---

## Pre-Execution Validation

### Checklist: Phase 1 Prerequisites (STIX Parsing)

- [ ] **Data Files Accessible**: All 5 STIX training files exist and are readable
- [ ] **Python Environment**: Python 3.9+ installed
- [ ] **STIX Library**: `stix2` library installed and importable
- [ ] **JSON Schema Library**: `jsonschema` library installed
- [ ] **Pandas Library**: `pandas` library installed for reporting
- [ ] **Output Directory**: Enhancement_02_STIX_Integration directory exists with write permissions
- [ ] **Disk Space**: Minimum 1 GB free space for intermediate files

**Validation Script** (Phase 1):
```bash
#!/bin/bash
# Phase 1 Pre-Execution Validation

echo "=== Phase 1 Prerequisites Validation ==="

# Check STIX training files
STIX_DATA_PATH="/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/"
for file in "01_STIX_Attack_Patterns.md" "02_STIX_Threat_Actors.md" "03_STIX_Indicators_IOCs.md" "04_STIX_Malware_Infrastructure.md" "05_STIX_Campaigns_Reports.md"; do
  if [ -f "${STIX_DATA_PATH}${file}" ]; then
    echo "✓ ${file} exists"
  else
    echo "✗ ${file} NOT FOUND"
    exit 1
  fi
done

# Check Python environment
python3 -c "import stix2, jsonschema, pandas" 2>/dev/null
if [ $? -eq 0 ]; then
  echo "✓ Python libraries installed"
else
  echo "✗ Python libraries missing"
  exit 1
fi

# Check output directory
OUTPUT_DIR="/home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_02_STIX_Integration/"
if [ -d "${OUTPUT_DIR}" ] && [ -w "${OUTPUT_DIR}" ]; then
  echo "✓ Output directory accessible"
else
  echo "✗ Output directory not writable"
  exit 1
fi

# Check disk space (minimum 1 GB free)
FREE_SPACE=$(df -BG "${OUTPUT_DIR}" | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "${FREE_SPACE}" -ge 1 ]; then
  echo "✓ Sufficient disk space (${FREE_SPACE} GB free)"
else
  echo "✗ Insufficient disk space (${FREE_SPACE} GB free, need 1+ GB)"
  exit 1
fi

echo "=== Phase 1 Prerequisites: PASSED ==="
```

### Checklist: Phase 2 Prerequisites (Neo4j Ingestion)

- [ ] **Neo4j Running**: Neo4j database accessible via bolt protocol
- [ ] **Neo4j Authentication**: Valid username/password in `.env` file
- [ ] **MITRE Nodes Exist**: 691 MITRE ATT&CK technique nodes in database
- [ ] **Database Permissions**: Write permissions and index creation allowed
- [ ] **Neo4j Driver**: `neo4j` Python library installed
- [ ] **Phase 1 Outputs**: `stix_objects.pkl` and JSON files from Phase 1 exist
- [ ] **Disk Space**: Minimum 5 GB free space in Neo4j database directory

**Validation Script** (Phase 2):
```bash
#!/bin/bash
# Phase 2 Pre-Execution Validation

echo "=== Phase 2 Prerequisites Validation ==="

# Check Phase 1 outputs exist
OUTPUT_DIR="/home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_02_STIX_Integration/"
for file in "stix_objects.pkl" "threat_actors.json" "attack_pattern_mitre_mappings.json" "malware_tools.json" "indicators.json" "campaigns.json"; do
  if [ -f "${OUTPUT_DIR}${file}" ]; then
    echo "✓ ${file} exists (Phase 1 output)"
  else
    echo "✗ ${file} NOT FOUND (Phase 1 incomplete)"
    exit 1
  fi
done

# Check Neo4j connectivity and MITRE nodes
python3 <<EOF
from neo4j import GraphDatabase
import os

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "")

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run("MATCH (n:AttackPattern) WHERE n.external_id IS NOT NULL RETURN count(n) AS count")
        mitre_count = result.single()["count"]
        if mitre_count >= 600:  # Allow some variance
            print(f"✓ Neo4j accessible with {mitre_count} MITRE nodes")
        else:
            print(f"✗ MITRE nodes insufficient ({mitre_count} found, expected ~691)")
            exit(1)
    driver.close()
except Exception as e:
    print(f"✗ Neo4j connection failed: {e}")
    exit(1)
EOF

if [ $? -ne 0 ]; then
  exit 1
fi

echo "=== Phase 2 Prerequisites: PASSED ==="
```

### Checklist: Phase 3 Prerequisites (Validation)

- [ ] **Phase 2 Complete**: Neo4j ingestion completed successfully
- [ ] **STIX Nodes Exist**: 3,000-5,000 STIX nodes in Neo4j database
- [ ] **STIX Relationships Exist**: 5,000-10,000 STIX relationships in database
- [ ] **Pytest Installed**: `pytest` library installed for test suite
- [ ] **Validation Queries**: Cypher validation queries prepared
- [ ] **Documentation Templates**: Markdown templates for final reports

**Validation Script** (Phase 3):
```bash
#!/bin/bash
# Phase 3 Pre-Execution Validation

echo "=== Phase 3 Prerequisites Validation ==="

# Check Phase 2 outputs exist
OUTPUT_DIR="/home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_02_STIX_Integration/"
if [ -f "${OUTPUT_DIR}ingestion_report.json" ]; then
  echo "✓ ingestion_report.json exists (Phase 2 output)"
else
  echo "✗ ingestion_report.json NOT FOUND (Phase 2 incomplete)"
  exit 1
fi

# Check STIX nodes in Neo4j
python3 <<EOF
from neo4j import GraphDatabase
import os

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "")

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        # Count STIX nodes (have stix_id property)
        result = session.run("MATCH (n) WHERE n.stix_id IS NOT NULL RETURN count(n) AS count")
        stix_node_count = result.single()["count"]

        # Count STIX relationships (have stix_source property or are between STIX nodes)
        result = session.run("""
            MATCH (s)-[r]->(t)
            WHERE s.stix_id IS NOT NULL AND t.stix_id IS NOT NULL
            RETURN count(r) AS count
        """)
        stix_rel_count = result.single()["count"]

        print(f"✓ Neo4j contains {stix_node_count} STIX nodes and {stix_rel_count} STIX relationships")

        if stix_node_count < 3000:
            print(f"⚠ Warning: STIX node count ({stix_node_count}) below expected minimum (3,000)")
        if stix_rel_count < 5000:
            print(f"⚠ Warning: STIX relationship count ({stix_rel_count}) below expected minimum (5,000)")

    driver.close()
except Exception as e:
    print(f"✗ Neo4j query failed: {e}")
    exit(1)
EOF

# Check pytest installed
pytest --version >/dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✓ pytest installed"
else
  echo "✗ pytest NOT FOUND"
  exit 1
fi

echo "=== Phase 3 Prerequisites: PASSED ==="
```

---

## Resource Allocation

### Compute Resources

**CPU**:
- **Phase 1 (Parsing)**: 2-4 CPU cores recommended for parallel parsing
- **Phase 2 (Ingestion)**: 4-8 CPU cores recommended for batch Neo4j operations
- **Phase 3 (Validation)**: 2-4 CPU cores for validation queries

**Memory**:
- **Phase 1 (Parsing)**: 4 GB RAM minimum, 8 GB recommended
- **Phase 2 (Ingestion)**: 8 GB RAM minimum, 16 GB recommended (Neo4j + Python)
- **Phase 3 (Validation)**: 4 GB RAM minimum, 8 GB recommended

**Disk Space**:
- **STIX Training Data**: ~5 MB (input files)
- **Intermediate Files** (Phase 1): ~500 MB (pickled objects, JSON)
- **Neo4j Database Growth** (Phase 2): ~500 MB - 1 GB (STIX nodes and relationships)
- **Reports and Logs** (Phase 3): ~50 MB (validation reports, test outputs)
- **Total Recommended Free Space**: 10 GB (safety margin)

### Time Allocation

**Phase 1: STIX Parsing and Validation**
- **Agent 1 (STIX Parser)**: 2-3 hours
- **Agents 2-6 (STIX Specialists)**: 3-4 hours (parallel)
- **Total Phase 1 Duration**: 5-7 hours (1 business day)

**Phase 2: Neo4j Mapping and Ingestion**
- **Agent 7 (Schema Mapper)**: 2-3 hours
- **Agent 8 (Ingestion Specialist)**: 4-5 hours (includes batch operations)
- **Total Phase 2 Duration**: 6-8 hours (1 business day)

**Phase 3: Validation and Reporting**
- **Agent 9 (Validation Engineer)**: 3-4 hours
- **Agent 10 (Documentation Specialist)**: 3-4 hours
- **Total Phase 3 Duration**: 6-8 hours (1 business day)

**Total Enhancement Duration**: 3 business days (17-23 hours total agent time)

---

## Contingency Planning

### Potential Issues and Mitigations

#### Issue 1: STIX Files Malformed or Incomplete

**Symptoms**:
- JSON parsing errors
- STIX schema validation failures
- Missing required properties

**Mitigation**:
1. Use lenient parsing mode (extract valid objects, skip invalid)
2. Generate detailed validation report highlighting issues
3. Proceed with valid objects, document invalid objects separately
4. Request corrected STIX files from data source if critical data missing

**Rollback**: None required (parsing errors do not affect database)

#### Issue 2: Neo4j Database Unavailable or Inaccessible

**Symptoms**:
- Connection timeout errors
- Authentication failures
- Network connectivity issues

**Mitigation**:
1. Verify Neo4j service status (`systemctl status neo4j`)
2. Check network connectivity (`ping`, `telnet`)
3. Validate credentials in `.env` file
4. Review Neo4j logs for errors (`/var/log/neo4j/neo4j.log`)
5. Retry connection with exponential backoff

**Rollback**: None required (no database changes attempted)

#### Issue 3: MITRE ATT&CK Nodes Missing or Incomplete

**Symptoms**:
- MITRE node count < 600
- Missing `external_id` property on MITRE nodes
- STIX attack patterns cannot be linked

**Mitigation**:
1. Verify MITRE data source and re-import if necessary
2. Use fuzzy matching on attack pattern names as fallback
3. Document unlinked STIX attack patterns for manual review
4. Proceed with partial linkage, generate report of unlinked patterns

**Rollback**: None required (STIX data still valuable without MITRE links)

#### Issue 4: Neo4j Performance Degradation During Ingestion

**Symptoms**:
- Ingestion taking > 10 minutes per 1,000 objects
- Database unresponsive
- High CPU or memory usage

**Mitigation**:
1. Reduce batch size (from 1,000 to 500 or 250 objects)
2. Increase Neo4j heap memory allocation (`dbms.memory.heap.max_size`)
3. Create indexes before bulk ingestion (if not already done)
4. Pause ingestion, optimize database, resume
5. Split ingestion into smaller batches with pauses between

**Rollback**: Safe to restart ingestion (MERGE operations are idempotent)

#### Issue 5: Validation Queries Fail or Return Unexpected Results

**Symptoms**:
- Cypher syntax errors
- Empty result sets
- Data integrity violations detected

**Mitigation**:
1. Review Cypher query syntax against Neo4j version
2. Verify node labels and property names match ingestion schema
3. Investigate data integrity issues (orphaned relationships, missing nodes)
4. Document issues in validation report
5. Provide recommendations for data cleanup or re-ingestion

**Rollback**: None required (validation is read-only)

### Emergency Rollback Procedures

**Phase 1 Rollback** (Parsing Errors):
- Delete intermediate files (`.pkl`, `.json`)
- No database impact
- Re-run Phase 1 with corrected data or parameters

**Phase 2 Rollback** (Ingestion Errors):
- Delete all STIX nodes and relationships:
  ```cypher
  // Delete all STIX relationships
  MATCH ()-[r]->()
  WHERE r.stix_source IS NOT NULL OR r.stix_relationship_id IS NOT NULL
  DELETE r;

  // Delete all STIX nodes
  MATCH (n)
  WHERE n.stix_id IS NOT NULL
  DELETE n;
  ```
- Verify MITRE nodes still exist
- Re-run Phase 2 with corrected data or parameters

**Phase 3 Rollback** (Validation Errors):
- No rollback necessary (read-only operations)
- Investigate and document issues
- Proceed to Phase 2 rollback only if critical data integrity issues detected

---

## Appendix: Quick Reference Commands

### Environment Setup
```bash
# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Verify installations
python3 -c "import stix2, neo4j, jsonschema, pandas, pytest; print('All libraries OK')"
```

### Neo4j Connection Test
```bash
# Test Neo4j connectivity
python3 <<EOF
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
with driver.session() as session:
    result = session.run("RETURN 'Neo4j Connected' AS message")
    print(result.single()["message"])
driver.close()
EOF
```

### File Integrity Check
```bash
# Verify STIX file integrity
md5sum /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/01_STIX_*.md \
       /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/02_STIX_*.md \
       /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/03_STIX_*.md \
       /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/04_STIX_*.md \
       /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/05_STIX_*.md > stix_files_md5.txt
```

### Disk Space Check
```bash
# Check available disk space
df -h /home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/
df -h /var/lib/neo4j/  # Adjust path to Neo4j data directory
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0.0 | 2025-11-25 | Code Implementation Agent | Initial prerequisites documentation with validation scripts and contingency planning |

---

**Status**: ACTIVE - Prerequisites validation ready
**Approval**: Prerequisites must be verified before Phase 1 execution
**Next Step**: Execute Phase 1 pre-execution validation script
**Contact**: Enhancement 02 execution team
