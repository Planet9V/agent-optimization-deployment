# Enhancement 08: RAMS - Prerequisites and Dependencies

**File:** Enhancement_08_RAMS_Reliability/PREREQUISITES.md
**Created:** 2025-11-25 14:42:00 UTC
**Version:** v1.0.0
**Status:** ACTIVE
**Purpose:** Document required data files, software dependencies, and system prerequisites for RAMS enhancement

---

## 1. Data File Requirements

### 1.1 Required RAMS Training Files (8 Total)

**Location**: `AEON_Training_data_NER10/Training_Data_Check_to_see/[SECTORS]/`

**File Categories**:

```yaml
rams_file_requirements:
  category_1_reliability:
    file_count: 2
    file_patterns:
      - "*reliability*.md"
      - "*mtbf*.md"
      - "*failure_rate*.md"
    required_content:
      - Equipment identifiers (EQUIP-*, names)
      - MTBF values in hours
      - Failure rate (λ) values
      - Weibull parameters (β, η) if available
      - Operating hours or cycles
    minimum_entities_per_file: 30

  category_2_maintenance:
    file_count: 2
    file_patterns:
      - "*maintenance*.md"
      - "*mttr*.md"
      - "*preventive*.md"
    required_content:
      - Maintenance event timestamps
      - Maintenance type (Preventive, Corrective, Predictive)
      - Duration (scheduled and actual)
      - Maintenance tasks and procedures
      - Parts replaced
    minimum_entities_per_file: 50

  category_3_safety:
    file_count: 2
    file_patterns:
      - "*safety*.md"
      - "*sil*.md"
      - "*fmea*.md"
      - "*hazard*.md"
    required_content:
      - Safety classifications (SIL-1 through SIL-4)
      - Consequence categories (NEGLIGIBLE, MARGINAL, CRITICAL, CATASTROPHIC)
      - Likelihood categories (IMPROBABLE, REMOTE, OCCASIONAL, PROBABLE, FREQUENT)
      - Failure modes and effects
      - Protection layers
    minimum_entities_per_file: 15

  category_4_failure_analysis:
    file_count: 1
    file_patterns:
      - "*failure_analysis*.md"
      - "*failure_event*.md"
      - "*downtime*.md"
    required_content:
      - Failure timestamps
      - Failure modes (Bearing Seizure, Shaft Fracture, etc.)
      - Failure causes (Lubrication Loss, Fatigue, Corrosion)
      - Downtime hours
      - Repair actions
    minimum_entities_per_file: 40

  category_5_availability:
    file_count: 1
    file_patterns:
      - "*availability*.md"
      - "*uptime*.md"
      - "*system_availability*.md"
    required_content:
      - Availability targets (99.0%, 99.9%, 99.99%)
      - Actual availability percentages
      - Downtime breakdown (planned vs unplanned)
      - System availability models
    minimum_entities_per_file: 20
```

### 1.2 File Quality Standards

**Mandatory Quality Checks**:
```yaml
file_quality_standards:
  completeness:
    - file_size: "> 1 KB (substantive content)"
    - entity_density: "> 5 entities per 100 lines"
    - metadata_present: "sector, subsector, document type"

  consistency:
    - time_units: "hours (standardized)"
    - date_format: "ISO 8601 (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
    - equipment_naming: "consistent across files"
    - terminology: "RAMS standard terms (MTBF, MTTR, SIL, etc.)"

  accuracy:
    - mtbf_range: "100 to 50,000 hours (plausible for industrial equipment)"
    - mttr_range: "0.1 to 100 hours (plausible repair times)"
    - availability_range: "50.0% to 99.999% (valid availability)"
    - failure_rate_positive: "λ > 0"
    - timestamps_valid: "between 2000-01-01 and current date"

  readability:
    - markdown_valid: "valid markdown syntax"
    - tables_parseable: "markdown tables or structured lists"
    - headings_present: "section headings for navigation"
```

### 1.3 Expected Data Volume

```yaml
expected_data_volume:
  equipment_entities:
    minimum: 200
    typical: 300
    maximum: 500
    description: "Unique equipment with RAMS properties"

  failure_events:
    minimum: 1000
    typical: 2000
    maximum: 5000
    description: "Historical failure occurrences"

  maintenance_events:
    minimum: 2000
    typical: 3500
    maximum: 8000
    description: "Preventive and corrective maintenance records"

  reliability_models:
    minimum: 150
    typical: 200
    maximum: 400
    description: "Weibull models (requires ≥5 failures per equipment)"

  safety_analyses:
    minimum: 50
    typical: 100
    maximum: 200
    description: "Safety-critical equipment SIL classifications"

  total_nodes:
    minimum: 3400
    typical: 6100
    maximum: 14100

  total_relationships:
    minimum: 3200
    typical: 5600
    maximum: 13000
```

---

## 2. Software Dependencies

### 2.1 Core Platform Requirements

```yaml
platform_requirements:
  neo4j:
    version: ">= 5.0.0"
    edition: "Enterprise or Community"
    memory_heap: ">= 4 GB"
    memory_page_cache: ">= 2 GB"
    plugins:
      - apoc: ">= 5.0.0 (graph algorithms, utilities)"
      - gds: ">= 2.0.0 (graph data science, optional)"
    configuration:
      - dbms.security.procedures.unrestricted: "apoc.*,gds.*"
      - dbms.memory.transaction.total.max: "2g"
      - dbms.memory.heap.initial_size: "4g"
      - dbms.memory.heap.max_size: "8g"

  python:
    version: ">= 3.9"
    virtual_environment: "recommended (venv or conda)"
    packages:
      - scipy: ">= 1.9.0 (Weibull fitting, statistical tests)"
      - numpy: ">= 1.23.0 (numerical operations)"
      - pandas: ">= 1.5.0 (data manipulation)"
      - neo4j: ">= 5.0.0 (Neo4j driver)"
      - python-dateutil: ">= 2.8.0 (date parsing)"
      - pyyaml: ">= 6.0 (configuration files)"

  nodejs:
    version: ">= 18.0.0"
    packages:
      - "claude-flow@alpha (>= 2.0.0-alpha.91)"
      - neo4j-driver: ">= 5.0.0"

  optional_tools:
    - jupyter: ">= 1.0.0 (interactive analysis)"
    - matplotlib: ">= 3.6.0 (reliability plots)"
    - seaborn: ">= 0.12.0 (statistical visualizations)"
```

### 2.2 Python Package Installation

```bash
# Create virtual environment
python3 -m venv venv_rams
source venv_rams/bin/activate  # On Windows: venv_rams\Scripts\activate

# Install required packages
pip install --upgrade pip
pip install scipy>=1.9.0 numpy>=1.23.0 pandas>=1.5.0
pip install neo4j>=5.0.0 python-dateutil>=2.8.0 pyyaml>=6.0

# Optional visualization packages
pip install jupyter>=1.0.0 matplotlib>=3.6.0 seaborn>=0.12.0

# Verify installations
python -c "import scipy; print(f'scipy {scipy.__version__}')"
python -c "import numpy; print(f'numpy {numpy.__version__}')"
python -c "import pandas; print(f'pandas {pandas.__version__}')"
python -c "import neo4j; print(f'neo4j {neo4j.__version__}')"
```

### 2.3 Neo4j Setup

```bash
# Download and install Neo4j (if not already installed)
# Visit: https://neo4j.com/download/

# Start Neo4j
neo4j start

# Verify Neo4j is running
curl http://localhost:7474

# Install APOC plugin
# Copy apoc-5.x.x-core.jar to $NEO4J_HOME/plugins/
# Restart Neo4j

# Verify APOC installation
# Execute in Neo4j Browser:
RETURN apoc.version()
```

---

## 3. Neo4j Database Prerequisites

### 3.1 Existing Graph Schema Requirements

**Required Nodes** (from Enhancement 01):
```cypher
// Equipment nodes should already exist or be created
(:Equipment {
  equipment_id: "EQUIP-001",  // REQUIRED: Unique identifier
  name: "Main Turbine Generator",  // REQUIRED: Human-readable name
  equipment_type: "Rotating Equipment",  // RECOMMENDED
  location: "SITE-001",  // OPTIONAL
  criticality_level: "HIGH"  // OPTIONAL
})
```

**RAMS Enhancement Will Extend Equipment**:
```cypher
// RAMS properties added to existing Equipment nodes
SET e.mtbf_hours = 8760.0,
    e.mttr_hours = 8.5,
    e.failure_rate = 0.000114,
    e.availability_target = 99.9,
    e.current_availability = 99.87,
    e.safety_critical = true,
    e.safety_classification = "SIL-3"
```

### 3.2 Database Capacity Planning

```yaml
neo4j_capacity:
  estimated_disk_space:
    nodes: "~100 MB (6,000 nodes × 15 properties × 1 KB)"
    relationships: "~50 MB (5,500 relationships × 10 properties × 1 KB)"
    indexes: "~20 MB (5 indexes × 4 MB)"
    total_estimated: "170 MB (plus 30% overhead = 220 MB)"

  memory_requirements:
    heap_memory: "4-8 GB (for Weibull fitting and data processing)"
    page_cache: "2-4 GB (for graph traversal queries)"
    transaction_memory: "2 GB (for bulk ingestion)"

  performance_targets:
    ingestion_throughput: "> 50 entities/minute"
    query_response_time: "< 1 second (for dashboard queries)"
    concurrent_users: "10-50 (depending on query complexity)"
```

---

## 4. Claude-Flow MCP Server Requirements

### 4.1 Claude-Flow Installation

```bash
# Install Claude-Flow MCP server
npm install -g claude-flow@alpha

# Verify installation
npx claude-flow@alpha --version
# Expected: 2.0.0-alpha.91 or later

# Initialize Claude-Flow
npx claude-flow@alpha init

# Add to Claude MCP configuration
claude mcp add claude-flow npx claude-flow@alpha mcp start
```

### 4.2 Claude-Flow Configuration

```yaml
claude_flow_config:
  swarm_settings:
    max_agents: 10
    default_topology: "hierarchical"
    communication_protocol: "mesh"
    coordination_interval: "5 seconds"
    timeout_per_agent: "30 minutes"

  memory_settings:
    memory_backend: "serena"
    namespace: "rams-ingestion"
    retention_days: 30
    max_memory_per_agent: "100 MB"

  performance_settings:
    parallel_execution: true
    max_concurrent_tasks: 5
    batch_size: 500
    retry_attempts: 3

  neural_features:
    pattern_learning: true
    agent_optimization: true
    performance_tracking: true
```

---

## 5. Access Requirements

### 5.1 File System Access

```yaml
file_system_permissions:
  read_access:
    - AEON_Training_data_NER10/Training_Data_Check_to_see/
    - Enhancement_08_RAMS_Reliability/

  write_access:
    - Enhancement_08_RAMS_Reliability/results/
    - Enhancement_08_RAMS_Reliability/logs/
    - /tmp/ (temporary processing files)

  disk_space:
    minimum: "1 GB free space"
    recommended: "5 GB free space"
```

### 5.2 Neo4j Database Access

```yaml
neo4j_credentials:
  connection_uri: "neo4j://localhost:7687"  # or bolt://
  username: "neo4j"
  password: "<set_secure_password>"
  database: "aeon-digital-twin"  # or "neo4j" default

  required_privileges:
    - CREATE_NODE: true
    - CREATE_RELATIONSHIP: true
    - CREATE_CONSTRAINT: true
    - CREATE_INDEX: true
    - READ: true
    - WRITE: true
    - DELETE: false  # Not needed for ingestion
```

### 5.3 Network Access (if applicable)

```yaml
network_requirements:
  neo4j_server:
    protocol: "bolt:// or neo4j://"
    port: 7687
    tls: "optional (recommended for production)"

  http_api:
    port: 7474
    authentication: "basic auth or OAuth"

  firewall_rules:
    inbound: "Allow connections from RAMS processing server to Neo4j port 7687"
    outbound: "Allow Neo4j to Claude-Flow MCP if remote"
```

---

## 6. Validation and Testing Prerequisites

### 6.1 Sample Data Validation

**Before Full Execution, Validate**:
```bash
# Check file availability
find AEON_Training_data_NER10/Training_Data_Check_to_see/ -name "*reliability*.md" -o -name "*maintenance*.md" | wc -l
# Expected: ≥ 8 files

# Check file sizes
find AEON_Training_data_NER10/Training_Data_Check_to_see/ -name "*rams*.md" -exec du -h {} \; | sort -h
# Expected: All files > 1 KB

# Verify Neo4j connectivity
python -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('neo4j://localhost:7687', auth=('neo4j', 'password')); driver.verify_connectivity(); print('Neo4j connected')"

# Test Weibull fitting
python -c "from scipy.stats import weibull_min; import numpy as np; data = np.random.weibull(1.5, 100) * 8760; shape, loc, scale = weibull_min.fit(data, floc=0); print(f'Weibull fit: β={shape:.2f}, η={scale:.0f}')"
```

### 6.2 Neo4j Pre-Flight Checks

```cypher
// Check existing Equipment nodes
MATCH (e:Equipment)
RETURN count(e) AS equipment_count, collect(e.equipment_id)[0..5] AS sample_ids;
// Note: May be 0 if RAMS is first enhancement

// Verify APOC is available
RETURN apoc.version();

// Check database constraints
SHOW CONSTRAINTS;

// Verify write permissions
CREATE (test:TestNode {id: "test-123"})
RETURN test;
// Then delete: MATCH (test:TestNode {id: "test-123"}) DELETE test;

// Check database size
CALL apoc.meta.stats();
```

---

## 7. Environment Variables

### 7.1 Required Environment Variables

```bash
# Neo4j connection
export NEO4J_URI="neo4j://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_secure_password"
export NEO4J_DATABASE="aeon-digital-twin"

# Data directories
export RAMS_DATA_DIR="/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see"
export RAMS_OUTPUT_DIR="/home/jim/2_OXOT_Projects_Dev/Enhancement_08_RAMS_Reliability/results"

# Claude-Flow
export CLAUDE_FLOW_NAMESPACE="rams-ingestion"
export CLAUDE_FLOW_MAX_AGENTS=10

# Python settings
export PYTHONPATH="${PYTHONPATH}:/home/jim/2_OXOT_Projects_Dev/Enhancement_08_RAMS_Reliability"
```

### 7.2 Configuration File Template

**File**: `Enhancement_08_RAMS_Reliability/config.yaml`
```yaml
neo4j:
  uri: "neo4j://localhost:7687"
  user: "neo4j"
  password: "${NEO4J_PASSWORD}"  # Use environment variable
  database: "aeon-digital-twin"
  max_connection_lifetime: 3600
  max_connection_pool_size: 50

data_sources:
  rams_files_directory: "${RAMS_DATA_DIR}"
  output_directory: "${RAMS_OUTPUT_DIR}"
  file_patterns:
    - "*reliability*.md"
    - "*maintenance*.md"
    - "*safety*.md"
    - "*failure*.md"
    - "*availability*.md"

processing:
  batch_size: 500
  parallel_agents: true
  max_concurrent_tasks: 5
  validation_threshold: 0.90
  reliability_model_r_squared_threshold: 0.85

logging:
  level: "INFO"
  file: "${RAMS_OUTPUT_DIR}/logs/rams_ingestion.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## 8. Pre-Execution Checklist

```yaml
pre_execution_checklist:
  infrastructure:
    - [ ] Neo4j 5.x installed and running
    - [ ] APOC plugin installed and configured
    - [ ] Neo4j accessible (test connection)
    - [ ] Sufficient disk space (>1 GB free)
    - [ ] Sufficient memory (>8 GB RAM available)

  software_dependencies:
    - [ ] Python 3.9+ installed
    - [ ] scipy, numpy, pandas installed
    - [ ] neo4j Python driver installed
    - [ ] Node.js 18+ installed
    - [ ] Claude-Flow MCP server installed

  data_files:
    - [ ] 8 RAMS files identified and validated
    - [ ] Files meet quality standards (>1 KB, valid markdown)
    - [ ] File paths accessible from processing environment
    - [ ] Backup of original files created

  configuration:
    - [ ] Environment variables set
    - [ ] config.yaml created and validated
    - [ ] Neo4j credentials configured
    - [ ] Output directories created

  permissions:
    - [ ] Read access to RAMS data directory
    - [ ] Write access to results directory
    - [ ] Neo4j database write privileges
    - [ ] Create constraint/index privileges in Neo4j

  testing:
    - [ ] Sample Weibull fit executed successfully
    - [ ] Neo4j query executed successfully
    - [ ] Claude-Flow swarm init tested
    - [ ] Python imports verified (no errors)

  documentation:
    - [ ] README.md reviewed
    - [ ] TASKMASTER_RAMS_v1.0.md reviewed
    - [ ] PREREQUISITES.md (this file) reviewed
    - [ ] DATA_SOURCES.md reviewed
```

---

## 9. Post-Execution Requirements

### 9.1 Validation Queries (Run After Ingestion)

```cypher
// Verify node counts
MATCH (e:Equipment) RETURN count(e) AS equipment_count;
MATCH (f:FailureEvent) RETURN count(f) AS failure_count;
MATCH (m:MaintenanceEvent) RETURN count(m) AS maintenance_count;
MATCH (r:ReliabilityModel) RETURN count(r) AS model_count;
MATCH (s:SafetyAnalysis) RETURN count(s) AS safety_count;

// Verify relationship counts
MATCH ()-[r:EXPERIENCED_FAILURE]->() RETURN count(r);
MATCH ()-[r:RECEIVED_MAINTENANCE]->() RETURN count(r);
MATCH ()-[r:HAS_RELIABILITY_MODEL]->() RETURN count(r);
MATCH ()-[r:HAS_SAFETY_ANALYSIS]->() RETURN count(r);

// Check data quality
MATCH (e:Equipment)
WHERE e.mtbf_hours IS NULL OR e.mttr_hours IS NULL
RETURN count(e) AS equipment_missing_rams_properties;

// Verify reliability models
MATCH (r:ReliabilityModel)
WHERE r.goodness_of_fit_r_squared < 0.85
RETURN count(r) AS low_quality_models;

// Check safety coverage
MATCH (e:Equipment)
WHERE e.safety_critical = true
WITH count(e) AS total
MATCH (e:Equipment)-[:HAS_SAFETY_ANALYSIS]->()
WHERE e.safety_critical = true
RETURN total AS total_safety_critical,
       count(e) AS with_analysis,
       round(count(e) * 100.0 / total, 1) AS coverage_percent;
```

### 9.2 Cleanup and Archival

```yaml
post_execution_cleanup:
  temporary_files:
    - Delete: "/tmp/rams_processing_*"
    - Delete: "${RAMS_OUTPUT_DIR}/temp/*"

  log_archival:
    - Archive: "${RAMS_OUTPUT_DIR}/logs/rams_ingestion.log"
    - Compress: "gzip rams_ingestion.log"
    - Move to: "${RAMS_OUTPUT_DIR}/archives/YYYY-MM-DD/"

  backup:
    - Neo4j dump: "neo4j-admin database dump aeon-digital-twin"
    - Save to: "${RAMS_OUTPUT_DIR}/backups/neo4j-dump-YYYY-MM-DD.dump"

  documentation:
    - Generate: "Final ingestion report"
    - Review: "Validation results"
    - Sign-off: "Stakeholder approval"
```

---

## 10. Troubleshooting Common Issues

### Issue 1: Neo4j Connection Failure
**Symptoms**: `ServiceUnavailable` or connection timeout errors
**Solutions**:
1. Verify Neo4j is running: `neo4j status`
2. Check URI and port: Should be `neo4j://localhost:7687` (not 7474)
3. Verify credentials: Test with Neo4j Browser
4. Check firewall: Allow port 7687

### Issue 2: Weibull Fit Convergence Failure
**Symptoms**: `RuntimeError: Optimization did not converge`
**Solutions**:
1. Check data quality: Remove outliers, verify positive values
2. Ensure sufficient sample size: Need ≥5 failures
3. Try different initial guess: Use method of moments estimator
4. Use censored data handling if equipment still operational

### Issue 3: Memory Error During Processing
**Symptoms**: `MemoryError` or slow performance
**Solutions**:
1. Increase Python heap size: `export PYTHONMAXMEMORY=8192`
2. Process files in smaller batches
3. Reduce Neo4j batch size from 500 to 100
4. Increase system swap space

### Issue 4: APOC Not Available
**Symptoms**: `Unknown function 'apoc.version'`
**Solutions**:
1. Download APOC plugin: https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases
2. Copy to Neo4j plugins directory: `$NEO4J_HOME/plugins/`
3. Edit neo4j.conf: `dbms.security.procedures.unrestricted=apoc.*`
4. Restart Neo4j: `neo4j restart`

### Issue 5: Claude-Flow Agent Spawn Failure
**Symptoms**: Agents not spawning or timeout errors
**Solutions**:
1. Verify Claude-Flow installation: `npx claude-flow@alpha --version`
2. Check agent instructions: Ensure no syntax errors
3. Increase timeout: `--timeout 3600000` (1 hour)
4. Review logs: `~/.claude-flow/logs/`

---

## 11. Support and Resources

### Documentation
- **AEON Digital Twin Wiki**: `1_AEON_DT_CyberSecurity_Wiki_Current/`
- **Enhancement 08 README**: `Enhancement_08_RAMS_Reliability/README.md`
- **TASKMASTER**: `Enhancement_08_RAMS_Reliability/TASKMASTER_RAMS_v1.0.md`
- **Blotter**: `Enhancement_08_RAMS_Reliability/blotter.md`

### External Resources
- **Neo4j Documentation**: https://neo4j.com/docs/
- **APOC User Guide**: https://neo4j.com/labs/apoc/
- **scipy.stats**: https://docs.scipy.org/doc/scipy/reference/stats.html
- **Claude-Flow**: https://github.com/ruvnet/claude-flow
- **IEC 61508**: Functional Safety Standards
- **ReliaSoft**: Reliability Engineering Resources

### Contact
- **Project Lead**: [Your Name]
- **RAMS SME**: [Subject Matter Expert]
- **Neo4j Administrator**: [Database Admin]
- **Technical Support**: [Support Email]

---

**PREREQUISITES COMPLETE**

**Version:** v1.0.0
**Last Updated:** 2025-11-25
**Status:** ACTIVE
**Next Review:** Before swarm execution

✅ **All prerequisites documented**
📋 **Pre-execution checklist ready**
🔧 **Troubleshooting guide included**
📞 **Support resources listed**
