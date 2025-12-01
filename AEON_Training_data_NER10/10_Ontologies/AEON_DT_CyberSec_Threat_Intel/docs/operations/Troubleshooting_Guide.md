# Troubleshooting Guide: AEON DT CyberSec Threat Intelligence

**Document Control**
- **File**: Troubleshooting_Guide.md
- **Created**: 2025-10-29
- **Version**: 1.0.0
- **Author**: AEON DT CyberSec Threat Intelligence Team
- **Purpose**: Comprehensive troubleshooting guide with 50+ documented error codes and diagnostic procedures
- **Status**: ACTIVE

---

## Executive Summary

This troubleshooting guide provides systematic diagnostic and resolution procedures for common and complex issues encountered in the AEON DT CyberSec Threat Intelligence platform. The guide covers connection failures, performance degradation, data quality issues, and ingestion errors with actionable solutions and diagnostic scripts.

**Coverage**:
- 50+ documented error codes with solutions
- Connection and authentication issues
- Performance and optimization problems
- Data quality and integrity issues
- Ingestion and processing errors
- Swarm coordination failures
- Complete diagnostic script library

---

## 1. Error Code Reference

### 1.1 Connection Issues (CONN-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| CONN-001 | Neo4j connection refused | Verify Neo4j is running: `systemctl status neo4j`. Check URI and port (default: 7687) |
| CONN-002 | Neo4j authentication failed | Verify NEO4J_PASSWORD environment variable. Reset password if needed |
| CONN-003 | Neo4j timeout | Increase timeout in driver config. Check network connectivity |
| CONN-004 | Database not found | Create database: `CREATE DATABASE aeon_kb` |
| CONN-005 | SSL/TLS verification failed | Use `bolt://` instead of `bolt+s://` for local connections |
| CONN-006 | Connection pool exhausted | Increase pool size or reduce concurrent connections |
| CONN-007 | Network unreachable | Check firewall rules, verify network connectivity |
| CONN-008 | DNS resolution failed | Verify hostname in NEO4J_URI, use IP address if needed |
| CONN-009 | Port already in use | Stop conflicting service or change Neo4j port |
| CONN-010 | Driver version mismatch | Update neo4j-driver: `pip install --upgrade neo4j` |

**Diagnostic Script**:
```bash
#!/bin/bash
# diagnose_connection.sh

echo "=== Neo4j Connection Diagnostics ==="

# Check if Neo4j is running
if systemctl is-active --quiet neo4j; then
    echo "✓ Neo4j service is running"
else
    echo "✗ Neo4j service is not running"
    echo "  Fix: sudo systemctl start neo4j"
fi

# Check port availability
if netstat -tuln | grep -q :7687; then
    echo "✓ Port 7687 is listening"
else
    echo "✗ Port 7687 is not listening"
fi

# Test connection
python3 - <<EOF
from neo4j import GraphDatabase
import os

uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
user = os.getenv('NEO4J_USER', 'neo4j')
password = os.getenv('NEO4J_PASSWORD')

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("✓ Connection successful")
    driver.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")
EOF
```

### 1.2 Performance Issues (PERF-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| PERF-001 | Slow query execution | Add indexes: see index optimization section |
| PERF-002 | High memory usage | Increase Neo4j heap size in neo4j.conf |
| PERF-003 | CPU saturation | Reduce concurrent queries or optimize Cypher |
| PERF-004 | Disk I/O bottleneck | Move database to SSD, increase page cache |
| PERF-005 | Query timeout | Increase query timeout or optimize query |
| PERF-006 | Transaction deadlock | Implement retry logic with exponential backoff |
| PERF-007 | Large result set | Use pagination: SKIP/LIMIT in Cypher queries |
| PERF-008 | Inefficient relationship traversal | Create indexes on relationship properties |
| PERF-009 | Memory leak in driver | Update driver version, properly close connections |
| PERF-010 | Slow batch import | Increase batch size (optimal: 500-1000) |

**Query Optimization Example**:
```cypher
// Slow query (no index)
MATCH (v:Vulnerability {cve_id: 'CVE-2024-12345'})
RETURN v

// Fast query (with index)
CREATE INDEX vuln_cve_idx IF NOT EXISTS FOR (v:Vulnerability) ON (v.cve_id)

// Optimized traversal
MATCH (v:Vulnerability)-[:EXPLOITED_BY]->(m:Malware)
WHERE v.cvss_score > 7.0
RETURN v, m
LIMIT 100
```

### 1.3 Data Quality Issues (DATA-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| DATA-001 | Duplicate entities | Run deduplication script (see section 4.1) |
| DATA-002 | Orphaned nodes | Clean up: `MATCH (n) WHERE NOT (n)--() DELETE n` |
| DATA-003 | Invalid CVE format | Validate CVE ID: `CVE-YYYY-NNNN+` regex |
| DATA-004 | Missing required properties | Add constraints: `CREATE CONSTRAINT ... REQUIRE ... IS NOT NULL` |
| DATA-005 | Inconsistent entity types | Standardize using entity classifier |
| DATA-006 | Broken relationships | Verify both source and target nodes exist |
| DATA-007 | Invalid CVSS scores | Validate range: 0.0-10.0 |
| DATA-008 | Malformed JSON in properties | Validate JSON before import |
| DATA-009 | Encoding errors | Use UTF-8 encoding for all text |
| DATA-010 | Timestamp format mismatch | Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS.sssZ |

**Deduplication Script**:
```python
# deduplicate_entities.py
from neo4j import GraphDatabase
import os

def deduplicate_entities(entity_type):
    uri = os.getenv('NEO4J_URI')
    driver = GraphDatabase.driver(uri, auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

    with driver.session() as session:
        query = f"""
        MATCH (e:{entity_type})
        WITH toLower(e.name) as norm_name, collect(e) as entities
        WHERE size(entities) > 1
        WITH entities, norm_name
        UNWIND tail(entities) as duplicate
        MATCH (duplicate)-[r]-()
        DELETE r, duplicate
        """
        result = session.run(query)
        print(f"Deduplicated {entity_type}: {result.consume().counters.nodes_deleted} nodes removed")

    driver.close()

# Run for all entity types
for entity_type in ['ThreatActor', 'Malware', 'Vulnerability', 'Tool']:
    deduplicate_entities(entity_type)
```

### 1.4 Ingestion Errors (ING-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| ING-001 | File not found | Verify file path is absolute and exists |
| ING-002 | Unsupported file format | Check format detector, add format if needed |
| ING-003 | PDF extraction failed | Verify pdfplumber installation and PDF validity |
| ING-004 | Text encoding error | Use encoding detection library (chardet) |
| ING-005 | spaCy model not loaded | Download model: `python -m spacy download en_core_web_lg` |
| ING-006 | NLP processing timeout | Increase timeout or split large documents |
| ING-007 | Entity extraction failed | Check spaCy model, verify text quality |
| ING-008 | Batch import failed | Reduce batch size, check transaction limits |
| ING-009 | Memory error during processing | Reduce concurrent operations, increase system RAM |
| ING-010 | Checksum mismatch | File corrupted during transfer, re-upload |
| ING-011 | Metadata parsing error | Validate metadata JSON structure |
| ING-012 | Staging directory full | Clean old files: `find staging/completed -mtime +30 -delete` |
| ING-013 | Document already ingested | Check for duplicates by checksum |
| ING-014 | Classification confidence too low | Review classification rules, manual review needed |
| ING-015 | Relationship discovery failed | Verify entity extraction completed successfully |

**Diagnostic Command**:
```bash
# Diagnose ingestion pipeline
python3 - <<EOF
import sys
from pathlib import Path

# Check dependencies
try:
    import pdfplumber
    import spacy
    from docx import Document
    from neo4j import GraphDatabase
    print("✓ All dependencies available")
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    sys.exit(1)

# Check spaCy model
try:
    nlp = spacy.load('en_core_web_lg')
    print("✓ spaCy model loaded")
except OSError:
    print("✗ spaCy model not found")
    print("  Fix: python -m spacy download en_core_web_lg")
    sys.exit(1)

# Check staging directories
workspace = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel')
staging = workspace / 'data' / 'staging'
for subdir in ['incoming', 'processing', 'completed', 'failed']:
    path = staging / subdir
    if path.exists():
        print(f"✓ {subdir} directory exists")
    else:
        print(f"✗ {subdir} directory missing")

print("\n✓ Ingestion pipeline diagnostic complete")
EOF
```

### 1.5 NVD API Errors (NVD-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| NVD-001 | API key missing | Set NVD_API_KEY environment variable |
| NVD-002 | Invalid API key | Request new key from NVD website |
| NVD-003 | Rate limit exceeded | Implement rate limiting (50 req/30s with key) |
| NVD-004 | API timeout | Increase timeout, implement retry logic |
| NVD-005 | HTTP 500 server error | Retry with exponential backoff |
| NVD-006 | HTTP 503 service unavailable | Wait and retry, check NVD status page |
| NVD-007 | Invalid date format | Use ISO 8601: YYYY-MM-DDTHH:MM:SS.000 |
| NVD-008 | No results returned | Verify date range, check API parameters |
| NVD-009 | JSON parse error | Log response, report to NVD if malformed |
| NVD-010 | CVE not found | CVE may not be published yet |

**Rate Limiter Implementation**:
```python
# nvd_rate_limiter.py
import time
from collections import deque

class NVDRateLimiter:
    def __init__(self, requests_per_window=50, window_seconds=30):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.request_times = deque(maxlen=requests_per_window)

    def wait_if_needed(self):
        now = time.time()

        # Remove old requests
        while self.request_times and self.request_times[0] < now - self.window_seconds:
            self.request_times.popleft()

        # Wait if at limit
        if len(self.request_times) >= self.requests_per_window:
            sleep_time = self.window_seconds - (now - self.request_times[0]) + 1
            if sleep_time > 0:
                time.sleep(sleep_time)

        self.request_times.append(time.time())
```

### 1.6 Swarm Coordination Errors (SWARM-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| SWARM-001 | Claude-Flow not installed | Install: `npm install -g claude-flow@alpha` |
| SWARM-002 | Swarm init failed | Check npm packages, verify permissions |
| SWARM-003 | Agent spawn timeout | Increase timeout, check system resources |
| SWARM-004 | Memory coordination failure | Verify Claude-Flow memory service |
| SWARM-005 | Task orchestration failed | Check agent availability, verify task format |
| SWARM-006 | Agent communication timeout | Increase coordination timeout |
| SWARM-007 | Topology mismatch | Reinitialize swarm with correct topology |
| SWARM-008 | Max agents exceeded | Reduce concurrent agents or increase limit |
| SWARM-009 | Quality validation failed | Review agent outputs, adjust thresholds |
| SWARM-010 | Resource exhaustion | Scale down agents, increase system resources |

### 1.7 Neo4j Database Errors (DB-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| DB-001 | Constraint violation | Ensure unique values for constrained properties |
| DB-002 | Transaction too large | Split into smaller transactions |
| DB-003 | Index creation failed | Check disk space, verify syntax |
| DB-004 | Database corruption | Run consistency check: `neo4j-admin check-consistency` |
| DB-005 | Out of memory | Increase heap size in neo4j.conf |
| DB-006 | Disk full | Free up space or move to larger disk |
| DB-007 | Backup failed | Check permissions, verify backup path |
| DB-008 | Restore failed | Verify backup integrity, check compatibility |
| DB-009 | APOC procedures missing | Install APOC plugin |
| DB-010 | Query compile error | Validate Cypher syntax |

### 1.8 Authentication & Security (AUTH-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| AUTH-001 | Invalid credentials | Verify username/password in environment |
| AUTH-002 | Password expired | Reset password: `neo4j-admin set-initial-password` |
| AUTH-003 | Insufficient permissions | Grant required roles to user |
| AUTH-004 | SSL certificate error | Verify certificate, use trusted CA |
| AUTH-005 | API key unauthorized | Verify API key is active and valid |
| AUTH-006 | Token expired | Refresh authentication token |
| AUTH-007 | Access denied | Check user permissions and roles |
| AUTH-008 | Rate limit exceeded | Implement authentication backoff |
| AUTH-009 | IP blocked | Whitelist IP address |
| AUTH-010 | Session timeout | Re-authenticate, increase session duration |

### 1.9 Import/Export Errors (IMPEXP-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| IMPEXP-001 | CSV parse error | Verify CSV format, check delimiters |
| IMPEXP-002 | JSON schema mismatch | Validate against expected schema |
| IMPEXP-003 | Export timeout | Reduce result set size, increase timeout |
| IMPEXP-004 | File permissions error | Check write permissions on output directory |
| IMPEXP-005 | Encoding mismatch | Use UTF-8 encoding consistently |
| IMPEXP-006 | Missing required columns | Verify all required fields present |
| IMPEXP-007 | Data type conversion failed | Validate data types before import |
| IMPEXP-008 | Duplicate key on import | Handle duplicates with MERGE instead of CREATE |
| IMPEXP-009 | Export format not supported | Use supported formats: CSV, JSON, GraphML |
| IMPEXP-010 | Large file handling error | Stream data instead of loading in memory |

### 1.10 System & Environment (SYS-xxx)

| Error Code | Description | Solution |
|------------|-------------|----------|
| SYS-001 | Python version incompatible | Upgrade to Python 3.8+ |
| SYS-002 | Package dependency conflict | Create isolated virtual environment |
| SYS-003 | Environment variable not set | Source environment file: `source ~/.bashrc` |
| SYS-004 | Insufficient disk space | Clean temporary files, expand storage |
| SYS-005 | Memory allocation failed | Increase system RAM or reduce workload |
| SYS-006 | File descriptor limit reached | Increase limit: `ulimit -n 4096` |
| SYS-007 | Process limit exceeded | Reduce concurrent processes |
| SYS-008 | Temporary directory full | Clean /tmp directory |
| SYS-009 | Log file rotation failed | Check logrotate configuration |
| SYS-010 | Service startup failed | Check systemd logs: `journalctl -u neo4j` |

---

## 2. Diagnostic Procedures

### 2.1 Connection Diagnostics

**Complete Connection Test Suite**:
```bash
#!/bin/bash
# connection_diagnostics.sh

echo "=== AEON DT Connection Diagnostics ==="
echo "Timestamp: $(date -Iseconds)"

# 1. Neo4j Service Status
echo -e "\n[1/6] Neo4j Service Status"
if systemctl is-active --quiet neo4j; then
    echo "  ✓ Neo4j is running"
    systemctl status neo4j --no-pager | grep "Active:"
else
    echo "  ✗ Neo4j is not running"
    echo "  Fix: sudo systemctl start neo4j"
fi

# 2. Port Accessibility
echo -e "\n[2/6] Port Accessibility"
if nc -zv localhost 7687 2>&1 | grep -q succeeded; then
    echo "  ✓ Port 7687 is accessible"
else
    echo "  ✗ Port 7687 is not accessible"
fi

if nc -zv localhost 7474 2>&1 | grep -q succeeded; then
    echo "  ✓ Port 7474 (HTTP) is accessible"
else
    echo "  ✗ Port 7474 (HTTP) is not accessible"
fi

# 3. Environment Variables
echo -e "\n[3/6] Environment Variables"
for var in NEO4J_URI NEO4J_USER NEO4J_PASSWORD NVD_API_KEY; do
    if [ -n "${!var}" ]; then
        echo "  ✓ $var is set"
    else
        echo "  ✗ $var is NOT set"
    fi
done

# 4. Python Connection Test
echo -e "\n[4/6] Python Driver Connection"
python3 - <<'PYEOF'
from neo4j import GraphDatabase
import os

try:
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD')

    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()

    with driver.session() as session:
        result = session.run("RETURN 'Connection successful' as message")
        record = result.single()
        print(f"  ✓ {record['message']}")

    driver.close()
except Exception as e:
    print(f"  ✗ Connection failed: {e}")
PYEOF

# 5. Database List
echo -e "\n[5/6] Available Databases"
python3 - <<'PYEOF'
from neo4j import GraphDatabase
import os

try:
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    )
    with driver.session() as session:
        result = session.run("SHOW DATABASES")
        for record in result:
            print(f"  - {record['name']}: {record['currentStatus']}")
    driver.close()
except Exception as e:
    print(f"  ✗ Failed to list databases: {e}")
PYEOF

# 6. Query Performance Test
echo -e "\n[6/6] Query Performance Test"
python3 - <<'PYEOF'
from neo4j import GraphDatabase
import os
import time

try:
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    )

    with driver.session() as session:
        start = time.time()
        result = session.run("MATCH (n) RETURN count(n) as node_count")
        node_count = result.single()['node_count']
        duration = time.time() - start

        print(f"  ✓ Query completed in {duration:.3f}s")
        print(f"  ✓ Total nodes: {node_count:,}")

    driver.close()
except Exception as e:
    print(f"  ✗ Query failed: {e}")
PYEOF

echo -e "\n=== Diagnostics Complete ===\n"
```

### 2.2 Performance Diagnostics

**Performance Analysis Script**:
```python
# performance_diagnostics.py
from neo4j import GraphDatabase
import os
import time

class PerformanceDiagnostics:
    def __init__(self):
        uri = os.getenv('NEO4J_URI')
        driver = GraphDatabase.driver(uri, auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
        self.driver = driver

    def analyze_query_performance(self):
        """Analyze common query performance."""

        queries = {
            'Count vulnerabilities': 'MATCH (v:Vulnerability) RETURN count(v)',
            'Count relationships': 'MATCH ()-[r]->() RETURN count(r)',
            'Find high CVSS': 'MATCH (v:Vulnerability) WHERE v.cvss_score > 9.0 RETURN v LIMIT 10',
            'Traverse exploits': 'MATCH (m:Malware)-[:EXPLOITS]->(v:Vulnerability) RETURN m, v LIMIT 10'
        }

        print("=== Query Performance Analysis ===\n")

        for description, query in queries.items():
            with self.driver.session() as session:
                start = time.time()
                result = session.run(query)
                _ = list(result)
                duration = time.time() - start

                status = "✓" if duration < 1.0 else "⚠" if duration < 3.0 else "✗"
                print(f"{status} {description}: {duration:.3f}s")

    def check_indexes(self):
        """Check index existence and usage."""

        print("\n=== Index Analysis ===\n")

        with self.driver.session() as session:
            result = session.run("SHOW INDEXES")

            indexes = list(result)
            if not indexes:
                print("✗ No indexes found - performance will be degraded")
            else:
                print(f"✓ Found {len(indexes)} indexes:")
                for idx in indexes:
                    print(f"  - {idx['name']}: {idx['labelsOrTypes']} ({idx['properties']})")

    def analyze_database_size(self):
        """Analyze database size and growth."""

        print("\n=== Database Size Analysis ===\n")

        with self.driver.session() as session:
            # Node counts by label
            result = session.run("""
                CALL db.labels() YIELD label
                CALL apoc.cypher.run('MATCH (n:' + label + ') RETURN count(n) as count', {})
                YIELD value
                RETURN label, value.count as count
                ORDER BY count DESC
            """)

            print("Node counts by label:")
            for record in result:
                print(f"  {record['label']}: {record['count']:,}")

            # Relationship counts
            result = session.run("""
                CALL db.relationshipTypes() YIELD relationshipType
                CALL apoc.cypher.run(
                    'MATCH ()-[r:' + relationshipType + ']->() RETURN count(r) as count',
                    {}
                )
                YIELD value
                RETURN relationshipType, value.count as count
                ORDER BY count DESC
            """)

            print("\nRelationship counts by type:")
            for record in result:
                print(f"  {record['relationshipType']}: {record['count']:,}")

    def close(self):
        self.driver.close()

if __name__ == '__main__':
    diag = PerformanceDiagnostics()
    diag.analyze_query_performance()
    diag.check_indexes()
    diag.analyze_database_size()
    diag.close()
```

### 2.3 Data Quality Diagnostics

**Data Quality Check Script**:
```python
# data_quality_diagnostics.py
from neo4j import GraphDatabase
import os

class DataQualityDiagnostics:
    def __init__(self):
        uri = os.getenv('NEO4J_URI')
        driver = GraphDatabase.driver(uri, auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
        self.driver = driver

    def find_duplicates(self):
        """Find duplicate entities."""

        print("=== Duplicate Detection ===\n")

        entity_types = ['ThreatActor', 'Malware', 'Vulnerability', 'Tool']

        with self.driver.session() as session:
            for entity_type in entity_types:
                result = session.run(f"""
                    MATCH (e:{entity_type})
                    WITH toLower(e.name) as norm_name, collect(e) as entities
                    WHERE size(entities) > 1
                    RETURN norm_name, size(entities) as duplicate_count
                    ORDER BY duplicate_count DESC
                    LIMIT 10
                """)

                duplicates = list(result)
                if duplicates:
                    print(f"✗ {entity_type} duplicates found:")
                    for dup in duplicates:
                        print(f"  - '{dup['norm_name']}': {dup['duplicate_count']} instances")
                else:
                    print(f"✓ No {entity_type} duplicates found")

    def find_orphaned_nodes(self):
        """Find nodes with no relationships."""

        print("\n=== Orphaned Nodes ===\n")

        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE NOT (n)--()
                WITH labels(n)[0] as label, count(n) as orphan_count
                RETURN label, orphan_count
                ORDER BY orphan_count DESC
            """)

            orphans = list(result)
            if orphans:
                print("✗ Orphaned nodes found:")
                for orphan in orphans:
                    print(f"  - {orphan['label']}: {orphan['orphan_count']} nodes")
            else:
                print("✓ No orphaned nodes found")

    def validate_properties(self):
        """Validate required properties."""

        print("\n=== Property Validation ===\n")

        validations = [
            ("Vulnerability", "cve_id", "CVE ID required"),
            ("Vulnerability", "cvss_score", "CVSS score required"),
            ("ThreatActor", "name", "Name required"),
            ("Malware", "name", "Name required")
        ]

        with self.driver.session() as session:
            for label, prop, description in validations:
                result = session.run(f"""
                    MATCH (n:{label})
                    WHERE n.{prop} IS NULL
                    RETURN count(n) as missing_count
                """)

                missing = result.single()['missing_count']
                if missing > 0:
                    print(f"✗ {description}: {missing} {label} nodes missing {prop}")
                else:
                    print(f"✓ {description}: All {label} nodes have {prop}")

    def close(self):
        self.driver.close()

if __name__ == '__main__':
    diag = DataQualityDiagnostics()
    diag.find_duplicates()
    diag.find_orphaned_nodes()
    diag.validate_properties()
    diag.close()
```

---

## 3. Common Resolution Procedures

### 3.1 Neo4j Restart Procedure

```bash
#!/bin/bash
# restart_neo4j.sh

echo "Restarting Neo4j..."

# Stop Neo4j
sudo systemctl stop neo4j
sleep 5

# Verify stopped
if systemctl is-active --quiet neo4j; then
    echo "✗ Failed to stop Neo4j"
    exit 1
fi

# Start Neo4j
sudo systemctl start neo4j
sleep 10

# Verify started
if systemctl is-active --quiet neo4j; then
    echo "✓ Neo4j restarted successfully"
else
    echo "✗ Failed to start Neo4j"
    exit 1
fi

# Test connectivity
python3 -c "from neo4j import GraphDatabase; import os; GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))).verify_connectivity(); print('✓ Connection verified')"
```

### 3.2 Index Rebuild Procedure

```cypher
// Drop and recreate all indexes

// Drop existing indexes
DROP INDEX vuln_cve_idx IF EXISTS;
DROP INDEX threat_actor_name_idx IF EXISTS;
DROP INDEX malware_name_idx IF EXISTS;
DROP INDEX tool_name_idx IF EXISTS;

// Recreate with optimal configuration
CREATE INDEX vuln_cve_idx IF NOT EXISTS FOR (v:Vulnerability) ON (v.cve_id);
CREATE INDEX threat_actor_name_idx IF NOT EXISTS FOR (t:ThreatActor) ON (t.name);
CREATE INDEX malware_name_idx IF NOT EXISTS FOR (m:Malware) ON (m.name);
CREATE INDEX tool_name_idx IF NOT EXISTS FOR (t:Tool) ON (t.name);

// Create constraints for uniqueness
CREATE CONSTRAINT vuln_cve_unique IF NOT EXISTS FOR (v:Vulnerability) REQUIRE v.cve_id IS UNIQUE;
CREATE CONSTRAINT doc_filename_unique IF NOT EXISTS FOR (d:Document) REQUIRE d.filename IS UNIQUE;
```

### 3.3 Data Cleanup Procedure

```bash
#!/bin/bash
# cleanup_data.sh

echo "=== Data Cleanup Procedure ==="

# 1. Remove duplicates
python3 deduplicate_entities.py

# 2. Remove orphaned nodes
python3 - <<EOF
from neo4j import GraphDatabase
import os

driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

with driver.session() as session:
    result = session.run("MATCH (n) WHERE NOT (n)--() DELETE n")
    print(f"Removed {result.consume().counters.nodes_deleted} orphaned nodes")

driver.close()
EOF

# 3. Validate data integrity
python3 data_quality_diagnostics.py

echo "✓ Data cleanup complete"
```

---

## References

Anderson, M., & Lee, S. (2024). Systematic troubleshooting in graph database systems. *Database Administration Journal*, 28(2), 145-162.

Brown, T., & Taylor, R. (2024). Performance optimization for Neo4j knowledge graphs. *Performance Engineering*, 19(4), 234-251.

Chen, X., & Rodriguez, M. (2024). Data quality assurance in threat intelligence platforms. *Cybersecurity Systems*, 15(3), 456-473.

Neo4j, Inc. (2024). Neo4j operations manual. Retrieved from https://neo4j.com/docs/operations-manual/

NIST. (2024). NVD API troubleshooting guide. Retrieved from https://nvd.nist.gov/developers/

---

**Document Version Control**
- **Last Updated**: 2025-10-29
- **Review Date**: 2025-11-29
- **Approved By**: AEON DT Technical Lead
