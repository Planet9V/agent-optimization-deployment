# AEON Digital Twin CyberSec Threat Intelligence - Ingestion Scripts

Complete production-ready ingestion scripts for loading cybersecurity threat intelligence data into Neo4j.

## 📋 Overview

This collection provides 5 specialized ingestion scripts for the AEON Digital Twin Cybersecurity Threat Intelligence system:

1. **nvd_cve_importer.py** - NVD CVE vulnerability data
2. **mitre_attack_importer.py** - MITRE ATT&CK framework
3. **asset_hierarchy_loader.py** - Organizational asset hierarchies
4. **network_topology_loader.py** - Network topology and security zones
5. **threat_intel_importer.py** - STIX/TAXII threat intelligence feeds

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
export NVD_API_KEY="your_nvd_api_key"  # Optional but recommended
```

### Basic Usage

```bash
# Import CVE data from NVD
python nvd_cve_importer.py

# Import MITRE ATT&CK framework
python mitre_attack_importer.py

# Load asset hierarchy from CSV
python asset_hierarchy_loader.py

# Load network topology
python network_topology_loader.py

# Import threat intelligence from STIX bundle
python threat_intel_importer.py
```

## 📊 Script Details

### 1. NVD CVE Importer

**Purpose**: Import CVE vulnerability data from NVD API 2.0

**Features**:
- Rate limiting (50 requests/30 seconds)
- Incremental updates using lastModifiedDate
- CPE parsing and linking
- CWE/CAPEC relationship creation
- Error recovery with exponential backoff
- Progress logging and metrics

**Usage**:
```python
from nvd_cve_importer import NVDImporter

importer = NVDImporter(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password",
    api_key="your_nvd_api_key"
)

# Incremental update (last 7 days)
importer.incremental_update(days_back=7)

# Full import for specific year
importer.full_import(year=2024)

importer.close()
```

**Data Model**:
- Nodes: `CVE`, `CPE`, `CWE`, `Reference`
- Relationships: `AFFECTS`, `HAS_WEAKNESS`, `HAS_REFERENCE`

**Configuration**:
```bash
# Required
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="password"

# Optional (recommended for higher rate limits)
export NVD_API_KEY="your_api_key"
```

### 2. MITRE ATT&CK Importer

**Purpose**: Import MITRE ATT&CK framework (STIX 2.1 format)

**Features**:
- Technique hierarchy modeling (Tactic→Technique→SubTechnique)
- Platform filtering (Windows, Linux, ICS)
- Mitigation linking
- Threat group and software tracking
- Reference extraction

**Usage**:
```python
from mitre_attack_importer import MITREAttackImporter

importer = MITREAttackImporter(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Import enterprise matrix with platform filter
platform_filter = {'Windows', 'Linux', 'Network'}
importer.import_full_matrix(
    matrix='enterprise',
    platform_filter=platform_filter
)

importer.close()
```

**Data Model**:
- Nodes: `AttackTactic`, `AttackTechnique`, `Mitigation`, `ThreatActor`, `Malware`
- Relationships: `USES_TACTIC`, `SUBTECHNIQUE_OF`, `MITIGATES`, `USES`

**Supported Matrices**:
- `enterprise` - Enterprise ATT&CK
- `ics` - Industrial Control Systems ATT&CK
- `mobile` - Mobile ATT&CK

### 3. Asset Hierarchy Loader

**Purpose**: Load organizational asset hierarchies (Organization→Site→Train→Component)

**Features**:
- CSV/JSON/API import support
- Automatic criticality assignment (IEC 62443 based)
- CPE matching to software
- Duplicate detection and merging
- Validation and error handling

**Usage**:
```python
from asset_hierarchy_loader import AssetHierarchyLoader

loader = AssetHierarchyLoader(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Load from CSV
assets = loader.load_from_csv('assets.csv')
loader.import_assets(assets)

# Link to software using CPE
loader.link_to_software('cpe_mappings.csv')

loader.close()
```

**CSV Format** (`assets.csv`):
```csv
id,name,type,parent_id,criticality,status,properties
ORG-001,Railway Corp,organization,,,active,"{}"
SITE-001,Main Station,site,ORG-001,CRITICAL,active,"{}"
TRAIN-001,Express Line 1,train,SITE-001,CRITICAL,active,"{}"
PLC-001,Signaling PLC,plc,TRAIN-001,CRITICAL,active,"{}"
```

**Data Model**:
- Nodes: `Organization`, `Site`, `Train`, `Component`, `PLC`, `HMI`, `SCADA`, `Server`, etc.
- Relationships: `BELONGS_TO`, `RUNS_SOFTWARE`

**Criticality Levels**: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`

### 4. Network Topology Loader

**Purpose**: Load network topology and security zones (IEC 62443 compliant)

**Features**:
- Firewall rule parsing (iptables, Cisco ACL)
- Network segment modeling with VLAN support
- Security zone assignment (CONTROL, DMZ, CORPORATE, etc.)
- IP address→device mapping
- Protocol validation

**Usage**:
```python
from network_topology_loader import NetworkTopologyLoader

loader = NetworkTopologyLoader(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Load segments from CSV
segments = loader.load_segments_from_csv('network_segments.csv')
loader.import_segments(segments)

# Parse and load firewall rules
rules = loader.parse_iptables_rules('iptables.rules')
loader.import_firewall_rules(rules)

# Link devices to segments
loader.link_devices_to_segments()

loader.close()
```

**CSV Format** (`network_segments.csv`):
```csv
id,name,zone,network,vlan_id,description
SEG-001,Control Network,CONTROL,10.1.0.0/24,100,Critical signaling systems
SEG-002,Process Network,PROCESS,10.2.0.0/24,200,Monitoring and data collection
SEG-003,DMZ,DMZ,10.3.0.0/24,300,External interfaces
```

**Data Model**:
- Nodes: `NetworkSegment`, `NetworkDevice`, `FirewallRule`
- Relationships: `IN_SEGMENT`, `HAS_RULE`, `ALLOWS_ACCESS_TO`

**Security Zones**:
- `CONTROL` - Critical control systems (level 4)
- `PROCESS` - Process control and monitoring (level 3)
- `DMZ` - Demilitarized zone (level 2)
- `CORPORATE` - Corporate network (level 1)
- `EXTERNAL` - External networks (level 0)

### 5. Threat Intelligence Importer

**Purpose**: Import STIX/TAXII threat intelligence feeds

**Features**:
- STIX 2.1 bundle parsing
- TAXII 2.0 server integration
- ThreatActor and Campaign modeling
- Indicator of Compromise (IoC) tracking
- Sector/geography filtering
- Confidence scoring

**Usage**:
```python
from threat_intel_importer import ThreatIntelImporter

importer = ThreatIntelImporter(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Load from STIX bundle
objects = importer.load_from_stix_bundle('threat_intel_bundle.json')
importer.import_full_feed(objects, filter_sectors=True)

# Or fetch from TAXII server
objects = importer.fetch_from_taxii(
    server_url='https://taxii.example.com',
    collection_id='threat-feed',
    username='user',
    password='pass'
)
importer.import_full_feed(objects)

importer.close()
```

**Data Model**:
- Nodes: `ThreatActor`, `Campaign`, `Indicator`, `Reference`
- Relationships: `ATTRIBUTED_TO`, `USES`, `INDICATES`, `TARGETS`

**Supported Indicator Types**:
- `ipv4-addr`, `ipv6-addr`, `domain-name`, `url`
- `file`, `email-addr`, `mutex`, `windows-registry-key`

**Filtering**: Automatically filters for railway-relevant sectors:
- transportation, rail, critical-infrastructure
- industrial-control-systems, ics, scada

## 🔧 Configuration

### Environment Variables

```bash
# Neo4j connection
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"

# NVD API (optional but recommended)
export NVD_API_KEY="your_nvd_api_key"
```

### Logging

All scripts write logs to individual log files:
- `nvd_importer.log`
- `mitre_attack_importer.log`
- `asset_loader.log`
- `network_loader.log`
- `threat_intel_importer.log`

Configure logging level via:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance

### Batch Sizes
- CVE import: 1000 CVEs per batch
- MITRE ATT&CK: 500 techniques per batch
- Assets: 1000 assets per batch
- Firewall rules: 500 rules per batch
- Indicators: 1000 indicators per batch

### Rate Limits
- NVD API: 50 requests per 30 seconds (without API key)
- NVD API: Higher limits with API key
- TAXII: Depends on server configuration

### Estimated Import Times
- CVE (1 year): ~10-15 minutes
- MITRE ATT&CK (full): ~2-3 minutes
- Assets (10,000): ~5-10 minutes
- Network topology (1,000 segments): ~3-5 minutes
- Threat intel (10,000 objects): ~10-15 minutes

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html tests/
```

## 🔒 Security Considerations

1. **API Keys**: Store API keys securely using environment variables or secrets management
2. **Database Credentials**: Never commit credentials to version control
3. **Rate Limiting**: Respect API rate limits to avoid blocking
4. **Data Validation**: All input data is validated before import
5. **Error Handling**: Comprehensive error handling with detailed logging

## 📚 Data Sources

- **NVD CVE**: https://nvd.nist.gov/developers
- **MITRE ATT&CK**: https://attack.mitre.org/
- **STIX/TAXII**: https://oasis-open.github.io/cti-documentation/

## 🤝 Integration

These scripts integrate with the AEON Digital Twin Cybersecurity Threat Intelligence ontology:

```cypher
// Example: Find vulnerable assets
MATCH (asset:Component)-[:RUNS_SOFTWARE]->(cpe:CPE)
MATCH (cve:CVE)-[:AFFECTS]->(cpe)
WHERE cve.baseSeverity = 'CRITICAL'
RETURN asset.name, cve.id, cve.baseScore

// Example: Find attack paths
MATCH (actor:ThreatActor)-[:USES]->(technique:AttackTechnique)
MATCH (technique)-[:USES_TACTIC]->(tactic:AttackTactic)
MATCH (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)
WHERE technique.name CONTAINS 'Exploit'
RETURN actor.name, technique.name, tactic.name, cve.id
```

## 📄 License

Part of the AEON Digital Twin project.

## 🆘 Support

For issues or questions:
1. Check the log files for detailed error messages
2. Verify Neo4j connection and credentials
3. Ensure all dependencies are installed
4. Review API rate limits and quotas

## 🔄 Maintenance

### Regular Updates
- CVE data: Daily incremental updates recommended
- MITRE ATT&CK: Quarterly full updates
- Threat intel: Daily or weekly depending on feed
- Assets/Network: As infrastructure changes

### Cleanup
```cypher
// Remove old CVE data (example: older than 5 years)
MATCH (cve:CVE)
WHERE datetime(cve.published) < datetime() - duration('P5Y')
DETACH DELETE cve
```

## 🚀 Future Enhancements

- [ ] Parallel batch processing for faster imports
- [ ] Incremental update optimization with change detection
- [ ] Real-time streaming import via message queues
- [ ] Data deduplication and conflict resolution
- [ ] Automated scheduling with cron/systemd
- [ ] Monitoring and alerting integration
- [ ] Data quality metrics and reporting
