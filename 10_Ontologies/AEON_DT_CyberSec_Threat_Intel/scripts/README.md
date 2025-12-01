# Cybersecurity Threat Intelligence Graph Analysis Scripts

Complete suite of 11 production-ready Python scripts for Neo4j graph operations, validation, and monitoring.

## 📁 Directory Structure

```
scripts/
├── graph_operations/          # Core graph analysis operations (4 scripts)
│   ├── attack_path_simulator.py
│   ├── risk_scorer.py
│   ├── reachability_analyzer.py
│   └── vulnerability_correlator.py
├── validation/                # Data quality and performance validation (4 scripts)
│   ├── data_integrity_checker.py
│   ├── schema_compliance_validator.py
│   ├── performance_benchmarker.py
│   └── audit_report_generator.py
├── monitoring/                # Real-time monitoring and statistics (3 scripts)
│   ├── graph_statistics.py
│   ├── ingestion_status_monitor.py
│   └── performance_dashboard.py
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Neo4j Connection

All scripts accept connection parameters:

```python
uri = "bolt://localhost:7687"
user = "neo4j"
password = "your_password"
```

Or set environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
```

### 3. Run Scripts

```bash
# Make scripts executable
chmod +x graph_operations/*.py validation/*.py monitoring/*.py

# Run individual scripts
python graph_operations/attack_path_simulator.py
python validation/data_integrity_checker.py
python monitoring/graph_statistics.py
```

## 📊 Graph Operations Scripts

### 1. Attack Path Simulator (`attack_path_simulator.py`)

**Purpose**: Find and analyze attack paths through the network.

**Features**:
- BFS/DFS attack path finding
- Firewall rule validation along paths
- Protocol compliance checking
- CVSS-weighted path scoring
- Multi-hop path enumeration (1-20 hops)
- D3.js visualization export

**Usage**:
```python
from attack_path_simulator import AttackPathSimulator

simulator = AttackPathSimulator(uri, user, password)

# Find attack paths from DMZ to critical assets
paths = simulator.find_attack_paths(
    source_zone="dmz",
    target_criticality="critical",
    max_hops=15
)

# Export for visualization
simulator.export_for_visualization(paths, "attack_paths.json")

# Generate report
report = simulator.generate_attack_report(paths)
```

**Output**: JSON with attack paths, risk scores, and visualization data.

---

### 2. Risk Scorer (`risk_scorer.py`)

**Purpose**: Multi-factor risk scoring and prioritization.

**Features**:
- 5-factor scoring model:
  - CVSS Score (40%)
  - Asset Criticality (25%)
  - Exploit Availability (20%)
  - Threat Intelligence (10%)
  - Network Exposure (5%)
- Dynamic threshold tuning
- Now/Next/Never classification
- Justification reporting
- Historical trend analysis

**Usage**:
```python
from risk_scorer import RiskScorer

scorer = RiskScorer(uri, user, password)

# Calculate risk for specific CVE
risk = scorer.calculate_vulnerability_risk("CVE-2023-12345")
print(f"Risk Score: {risk.total_score:.2f}")
print(f"Classification: {risk.classification}")

# Prioritize all vulnerabilities
priorities = scorer.prioritize_vulnerabilities(limit=100)
report = scorer.generate_risk_report(priorities)
```

**Output**: Risk scores with Now/Next/Never classifications.

---

### 3. Reachability Analyzer (`reachability_analyzer.py`)

**Purpose**: Network path and connectivity analysis.

**Features**:
- Layer 3/4 network path analysis
- Firewall rule validation
- Security zone crossing detection
- Protocol-aware routing
- Shortest path calculation (Dijkstra)
- Network visualization output

**Usage**:
```python
from reachability_analyzer import ReachabilityAnalyzer

analyzer = ReachabilityAnalyzer(uri, user, password)

# Check if destination is reachable
is_reachable, path = analyzer.check_reachability(
    source="web-server-1",
    destination="database-1",
    protocol="TCP",
    port=5432
)

if is_reachable:
    # Analyze zone crossings
    crossings = analyzer.analyze_zone_crossings(path)

    # Validate firewall rules
    validation = analyzer.validate_firewall_rules(path)
```

**Output**: Network paths with zone crossings and firewall validation.

---

### 4. Vulnerability Correlator (`vulnerability_correlator.py`)

**Purpose**: Match CVEs to assets using CPE and software versions.

**Features**:
- CPE matching with version comparison
- Software version parsing (semver)
- Transitive dependency analysis
- SBOM integration support
- Confidence scoring
- Batch correlation for assets

**Usage**:
```python
from vulnerability_correlator import VulnerabilityCorrelator

correlator = VulnerabilityCorrelator(uri, user, password)

# Correlate vulnerabilities to asset
matches = correlator.correlate_asset("web-server-1")

# Find transitive vulnerabilities
transitive = correlator.find_transitive_vulnerabilities("web-server-1", max_depth=3)

# Correlate from SBOM
sbom_data = {...}  # Load SBOM
matches = correlator.correlate_sbom(sbom_data)

# Generate report
report = correlator.generate_correlation_report(matches)
```

**Output**: CVE-to-asset correlations with confidence scores.

---

## ✅ Validation Scripts

### 5. Data Integrity Checker (`data_integrity_checker.py`)

**Purpose**: Validate graph data integrity and consistency.

**Features**:
- Orphaned node detection
- Duplicate entity identification
- Relationship consistency checks
- Property completeness validation
- Constraint violation detection
- Auto-fix with dry-run mode

**Usage**:
```python
from data_integrity_checker import DataIntegrityChecker

checker = DataIntegrityChecker(uri, user, password)

# Run all integrity checks
report = checker.run_all_checks()

print(f"Health Score: {report['summary']['health_score']}/100")
print(f"Critical Issues: {report['summary']['critical']}")

# Auto-fix issues (dry run)
checker.auto_fix(dry_run=True)
```

**Output**: Integrity report with health score and fixable issues.

---

### 6. Schema Compliance Validator (`schema_compliance_validator.py`)

**Purpose**: Validate graph compliance with ontology schema.

**Features**:
- Node type validation against schema
- Relationship type validation
- Property type checking
- Constraint enforcement verification
- Gap analysis reporting

**Usage**:
```python
from schema_compliance_validator import SchemaComplianceValidator

validator = SchemaComplianceValidator(uri, user, password)

# Run validation
report = validator.validate_all()

print(f"Compliance Score: {report['summary']['compliance_score']}/100")

# Export schema definition
validator.export_schema("schema.json")
```

**Output**: Compliance report with violations and recommendations.

---

### 7. Performance Benchmarker (`performance_benchmarker.py`)

**Purpose**: Benchmark query performance and detect regressions.

**Features**:
- 7 use case query benchmarks
- Index effectiveness analysis
- Query plan inspection (PROFILE)
- Latency tracking with percentiles
- Regression detection
- Performance report generation

**Usage**:
```python
from performance_benchmarker import PerformanceBenchmarker

benchmarker = PerformanceBenchmarker(uri, user, password)

# Check indexes
index_report = benchmarker.check_indexes()

# Run benchmark suite
results = benchmarker.run_benchmark(iterations=5)

# Set baseline for regression detection
benchmarker.set_baseline(results)

# Generate report
report = benchmarker.generate_report(results)
```

**Output**: Performance metrics with P50/P95/P99 latencies.

---

### 8. Audit Report Generator (`audit_report_generator.py`)

**Purpose**: Generate compliance and audit reports.

**Features**:
- Data freshness reports (CVE update lag)
- Coverage analysis (% assets with vulnerabilities)
- Update history tracking
- Query audit logs
- IEC 62443 compliance checks
- NERC-CIP compliance attestation

**Usage**:
```python
from audit_report_generator import AuditReportGenerator

auditor = AuditReportGenerator(uri, user, password)

# Generate full audit
report = auditor.generate_full_audit()

print(f"Overall Health: {report['overall_health']['score']:.1f}")
print(f"IEC 62443 Compliance: {report['compliance']['iec_62443']['score']:.1f}%")

# Export report
auditor.export_report(report, "audit_report.json")
```

**Output**: Comprehensive audit with compliance scores.

---

## 📈 Monitoring Scripts

### 9. Graph Statistics (`graph_statistics.py`)

**Purpose**: Collect and analyze graph statistics and metrics.

**Features**:
- Node counts by type
- Relationship counts by type
- Growth trends over time
- Density analysis
- Hotspot identification
- Distribution analysis

**Usage**:
```python
from graph_statistics import GraphStatistics

stats = GraphStatistics(uri, user, password)

# Print summary to console
stats.print_summary()

# Export full statistics
stats.export_statistics("graph_stats.json")

# Generate dashboard data
dashboard = stats.generate_dashboard_data()
```

**Output**: Comprehensive graph statistics and metrics.

---

### 10. Ingestion Status Monitor (`ingestion_status_monitor.py`)

**Purpose**: Monitor document ingestion and entity extraction status.

**Features**:
- Documents processed count
- Entities extracted tracking
- Error monitoring
- Processing rate (entities/second)
- ETA calculation
- Continuous monitoring mode

**Usage**:
```python
from ingestion_status_monitor import IngestionStatusMonitor

monitor = IngestionStatusMonitor(uri, user, password)

# Set baseline
monitor.set_baseline()

# Display status
monitor.print_status_dashboard()

# Continuous monitoring (10s intervals, 60 min duration)
monitor.monitor_continuous(interval_seconds=10, duration_minutes=60)
```

**Output**: Real-time ingestion status with ETA and error tracking.

---

### 11. Performance Dashboard (`performance_dashboard.py`)

**Purpose**: Real-time Streamlit dashboard for performance monitoring.

**Features**:
- Query latency histogram
- Throughput metrics (queries/sec)
- Resource utilization (CPU, memory)
- Error rate tracking
- Interactive Streamlit dashboard
- Auto-refresh capability

**Usage (Streamlit)**:
```bash
# Install Streamlit
pip install streamlit

# Run dashboard
streamlit run performance_dashboard.py
```

**Usage (Console)**:
```bash
# Run console version
python performance_dashboard.py
```

**Output**: Real-time performance dashboard with auto-refresh.

---

## 🔧 Configuration

### Environment Variables

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
```

### Script Configuration

Most scripts support configuration via constructor parameters:

```python
script = ScriptClass(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)
```

## 📝 Dependencies

Core requirements:
- `neo4j>=5.0.0` - Neo4j driver
- `packaging>=21.0` - Version comparison
- `streamlit>=1.20.0` - Dashboard (optional)

See `requirements.txt` for complete list.

## 🎯 Use Cases

### Security Operations

1. **Attack Surface Analysis**
   ```bash
   python graph_operations/attack_path_simulator.py
   python graph_operations/reachability_analyzer.py
   ```

2. **Risk Prioritization**
   ```bash
   python graph_operations/risk_scorer.py
   python graph_operations/vulnerability_correlator.py
   ```

### Quality Assurance

1. **Data Validation**
   ```bash
   python validation/data_integrity_checker.py
   python validation/schema_compliance_validator.py
   ```

2. **Performance Testing**
   ```bash
   python validation/performance_benchmarker.py
   python validation/audit_report_generator.py
   ```

### Operations Monitoring

1. **Real-time Monitoring**
   ```bash
   streamlit run monitoring/performance_dashboard.py
   python monitoring/ingestion_status_monitor.py
   ```

2. **Statistics Collection**
   ```bash
   python monitoring/graph_statistics.py
   ```

## 🔍 Troubleshooting

### Connection Issues

If scripts fail to connect to Neo4j:

1. Check Neo4j is running: `systemctl status neo4j`
2. Verify connection details: `bolt://localhost:7687`
3. Test credentials: `cypher-shell -u neo4j -p password`

### Performance Issues

If queries are slow:

1. Check indexes: Run `performance_benchmarker.py`
2. Review query plans: Use `PROFILE` in queries
3. Monitor resources: Run `performance_dashboard.py`

### Data Issues

If data validation fails:

1. Run integrity checker: `data_integrity_checker.py`
2. Check schema compliance: `schema_compliance_validator.py`
3. Review audit report: `audit_report_generator.py`

## 📚 Additional Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Cypher Query Language](https://neo4j.com/docs/cypher-manual/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

These scripts are production-ready and follow best practices:
- Type hints for better IDE support
- Comprehensive error handling
- Logging for troubleshooting
- Modular design for extensibility
- Detailed docstrings

## 📄 License

See project LICENSE file.

---

**All 11 scripts are complete, tested, and ready for production use.**
