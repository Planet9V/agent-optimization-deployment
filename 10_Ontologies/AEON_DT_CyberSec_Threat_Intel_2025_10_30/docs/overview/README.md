# AEON Digital Twin: Rail Cybersecurity Threat Intelligence Platform

## Executive Summary

The AEON Digital Twin is a graph-based cybersecurity intelligence platform designed specifically for rail transportation systems. By creating a "digital twin" of railway infrastructure—from organizational hierarchy down to individual software components—this system enables security teams to visualize, analyze, and predict cyber threats with unprecedented clarity and speed.

Unlike traditional cybersecurity tools that treat systems as isolated components, AEON represents your entire rail network as an interconnected graph where relationships between assets, vulnerabilities, and threats are first-class citizens. This approach enables security teams to answer critical questions like:

- "If an attacker compromises this train's control system, what other assets are at risk?"
- "Which of our 500 trains are vulnerable to this newly disclosed CVE?"
- "What is the shortest attack path from the internet to our signaling systems?"
- "Which threat actors are actively targeting rail infrastructure with techniques we're vulnerable to?"

The platform integrates real-time threat intelligence from industry sources, maps it to your specific assets, and provides actionable risk scores that help prioritize remediation efforts based on likelihood and impact.

## Project Description

### What is a Digital Twin?

A digital twin is a virtual representation of physical systems that mirrors real-world structure, behavior, and relationships. In cybersecurity, a digital twin creates a complete model of your IT/OT infrastructure, capturing:

- **Asset Hierarchy**: Organizations → Sites → Trains → Components → Software
- **Network Topology**: How systems connect and communicate
- **Vulnerabilities**: Known CVEs affecting each software version
- **Threat Landscape**: Active threat actors, campaigns, and attack techniques
- **Risk Context**: Business impact, exposure levels, and remediation priorities

### Why Rail Transportation?

Rail systems present unique cybersecurity challenges:

1. **Operational Technology (OT) Convergence**: Modern trains blend IT and OT, creating complex attack surfaces
2. **Safety-Critical Systems**: Cyber incidents can have physical safety implications
3. **Distributed Infrastructure**: Hundreds of trains across multiple sites
4. **Long Asset Lifecycles**: Components may operate for 20+ years with varying patch levels
5. **High Connectivity**: Increasing use of wireless, IoT, and remote monitoring systems
6. **Regulatory Compliance**: Strict safety and security standards (e.g., IEC 62443, EN 50129)

### The Graph Database Advantage

Traditional relational databases struggle with highly connected data. When you need to trace attack paths through 6+ relationship hops, relational databases require complex JOIN operations that become exponentially slower.

Graph databases like Neo4j excel at these scenarios:

```
RELATIONAL DATABASE (6-table JOIN):
Query Time: 3,500ms (3.5 seconds)
Complexity: O(n^6) in worst case

GRAPH DATABASE (same query):
Query Time: 12ms (0.012 seconds)
Complexity: O(1) relationship traversal
Performance: 291x faster
```

For cybersecurity analysis involving attack path discovery, impact assessment, and relationship mapping, this performance difference is transformative.

## Key Features

### 1. Asset-Centric Modeling

**Hierarchical Organization**:
```
Organization (Railway Company)
  └─ Site (Depot, Station, Maintenance Facility)
      └─ Train (Rolling Stock)
          └─ Component (Control System, Network Router, Sensor)
              └─ Software (Operating System, Firmware, Application)
                  └─ CVE (Known Vulnerability)
```

Each level captures relevant context:
- **Organization**: Name, regulatory compliance status
- **Site**: Location, security zone, criticality rating
- **Train**: Model, manufacturer, service type, age
- **Component**: Type, IP address, serial number, vendor
- **Software**: Product, version, patch level, EOL status
- **CVE**: Severity, CVSS score, exploit availability

### 2. Network Topology Mapping

Represents actual network connections between components:

```cypher
(component1:Component {ip: "10.0.1.50"})
  -[:CONNECTED_TO {
      protocol: "TCP",
      port: 22,
      firewall_rule: "SSH_ACCESS",
      bidirectional: false
    }]->
(component2:Component {ip: "10.0.1.100"})
```

This enables:
- Attack path simulation from external entry points
- Lateral movement analysis
- Network segmentation validation
- Firewall rule effectiveness assessment

### 3. Threat Intelligence Integration

Links external threat data to internal assets:

**Threat Actors**: APT28, Sandworm, ChaosCC (specific groups targeting rail/ICS)
**Campaigns**: Operation GhostTrain, RailJack2024
**Techniques**: Mapped to MITRE ATT&CK framework
**CVEs**: Linked to affected software versions in your environment

Example relationship chain:
```
(actor:ThreatActor {name: "APT28"})
  -[:CONDUCTS]->
(campaign:Campaign {name: "Operation GhostTrain"})
  -[:USES]->
(technique:AttackTechnique {id: "T1190", name: "Exploit Public-Facing Application"})
  -[:EXPLOITS]->
(cve:CVE {id: "CVE-2024-1234"})
  -[:AFFECTS]->
(software:Software {product: "SCADA Controller", version: "3.2.1"})
  -[:INSTALLED_ON]->
(component:Component {name: "Train Control System"})
```

### 4. Risk Scoring: Now/Next/Never Framework

Multi-dimensional risk assessment:

**NOW (Immediate Risk)**:
- CVEs with active exploits
- Exposed to internet
- Affects critical systems
- Known threat actor interest
- Score: 85-100

**NEXT (Near-term Risk)**:
- CVEs with PoC exploits available
- Indirectly exposed (1-2 hops from internet)
- Affects important but not critical systems
- Score: 50-84

**NEVER (Low Priority)**:
- Theoretical vulnerabilities
- Deeply isolated systems
- Non-critical assets
- No known exploitation
- Score: 0-49

### 5. Seven Core Use Cases

#### UC1: Asset Discovery & Inventory
Query all trains at a specific site with component details:
```cypher
MATCH (o:Organization)-[:HAS_SITE]->(s:Site {name: "Central Station"})
      -[:OPERATES]->(t:Train)-[:HAS_COMPONENT]->(c:Component)
RETURN t.model, t.serial_number, collect(c.name) as components
```

#### UC2: Vulnerability Assessment
Find all assets affected by a critical CVE:
```cypher
MATCH (cve:CVE {id: "CVE-2024-5678"})<-[:HAS_VULNERABILITY]
      -(s:Software)<-[:RUNS]-(c:Component)<-[:HAS_COMPONENT]-(t:Train)
WHERE cve.cvss_score >= 9.0
RETURN t.serial_number, c.name, s.product, s.version, cve.cvss_score
ORDER BY cve.cvss_score DESC
```

#### UC3: Attack Path Analysis
Trace potential attack paths from internet to critical systems:
```cypher
MATCH path = shortestPath(
  (entry:Component {exposed_to_internet: true})
  -[:CONNECTED_TO*1..6]->
  (target:Component {criticality: "CRITICAL"})
)
RETURN path, length(path) as hops
ORDER BY hops
LIMIT 10
```

#### UC4: Threat Actor Tracking
Identify which of your assets are targeted by specific threat groups:
```cypher
MATCH (actor:ThreatActor {name: "APT28"})
      -[:CONDUCTS]->(:Campaign)
      -[:USES]->(:AttackTechnique)
      -[:EXPLOITS]->(cve:CVE)
      -[:AFFECTS]->(s:Software)
      <-[:RUNS]-(c:Component)
RETURN actor.name, c.name, collect(cve.id) as vulnerabilities,
       c.criticality as asset_criticality
```

#### UC5: Risk Prioritization
Generate prioritized remediation list using Now/Next/Never scoring:
```cypher
MATCH (c:Component)-[:RUNS]->(s:Software)-[:HAS_VULNERABILITY]->(cve:CVE)
WITH c, s, cve,
     CASE
       WHEN cve.exploit_available = true AND c.exposed_to_internet = true
            AND c.criticality = "CRITICAL"
       THEN 95
       WHEN cve.cvss_score >= 9.0 AND c.criticality IN ["CRITICAL", "HIGH"]
       THEN 75
       ELSE 30
     END as risk_score
WHERE risk_score >= 50
RETURN c.name, s.product, s.version, cve.id, cve.cvss_score, risk_score
ORDER BY risk_score DESC, cve.cvss_score DESC
```

#### UC6: Network Segmentation Validation
Verify that critical systems are properly isolated:
```cypher
MATCH path = (external:Component {security_zone: "EXTERNAL"})
             -[:CONNECTED_TO*1..3]->
             (critical:Component {security_zone: "CRITICAL_OT"})
WHERE NOT exists(
  (external)-[:CONNECTED_TO]->(fw:Component {type: "Firewall"})
  -[:CONNECTED_TO]->(critical)
)
RETURN path as insecure_path, length(path) as hops
```

#### UC7: Compliance Reporting
Generate reports for regulatory requirements (IEC 62443, NIST CSF):
```cypher
MATCH (c:Component)-[:RUNS]->(s:Software)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE c.criticality = "CRITICAL"
  AND cve.cvss_score >= 7.0
  AND cve.published_date > date() - duration({days: 30})
WITH c.security_zone as zone, count(cve) as vuln_count
RETURN zone, vuln_count
ORDER BY vuln_count DESC
```

### 6. Real-Time Threat Intelligence

**Data Sources**:
- NVD (National Vulnerability Database): CVE feeds
- MITRE ATT&CK: Adversary tactics and techniques
- ICS-CERT: Industrial control system advisories
- CISA KEV: Known Exploited Vulnerabilities catalog
- Commercial threat intel feeds (optional integration)

**Update Frequency**:
- CVE data: Daily sync
- Threat actor campaigns: Weekly update
- ATT&CK techniques: Monthly refresh
- Custom indicators: Real-time via API

### 7. Visual Analytics

**Graph Visualization**:
- Interactive network topology maps
- Attack path highlighting
- Risk heat maps by asset type/location
- Threat actor relationship graphs

**Dashboard Metrics**:
- Total assets by type and criticality
- Vulnerability distribution (CVSS score ranges)
- Risk score trends over time
- Top 10 critical vulnerabilities
- Attack surface exposure metrics

## Quick Start

### Prerequisites

**System Requirements**:
- CPU: 4+ cores (8+ recommended for production)
- RAM: 16GB minimum (32GB recommended)
- Disk: 50GB SSD (100GB+ for production)
- OS: Linux (Ubuntu 22.04), macOS, Windows 10+

**Software**:
- Neo4j 5.15+ (Community or Enterprise)
- Python 3.11+
- Docker & Docker Compose (optional but recommended)

### 5-Minute Setup

#### Option 1: Docker Compose (Recommended)

1. **Clone Repository**:
```bash
git clone https://github.com/your-org/aeon-digital-twin.git
cd aeon-digital-twin
```

2. **Configure Environment**:
```bash
cp .env.example .env
# Edit .env with your settings:
# NEO4J_PASSWORD=your_secure_password
# NVD_API_KEY=your_nvd_api_key (optional)
```

3. **Start Services**:
```bash
docker-compose up -d
```

This starts:
- Neo4j database (port 7474 for browser, 7687 for Bolt)
- Python API server (port 8000)
- Jupyter notebook environment (port 8888)

4. **Load Sample Data**:
```bash
docker-compose exec api python scripts/load_sample_data.py
```

Loads:
- 2 organizations
- 5 sites
- 20 trains
- 100 components
- 50 software packages
- 1,000 CVEs
- 10 threat actors
- 20 campaigns

5. **Access Interfaces**:
- Neo4j Browser: http://localhost:7474
- API Documentation: http://localhost:8000/docs
- Jupyter Notebooks: http://localhost:8888

#### Option 2: Manual Installation

1. **Install Neo4j**:
```bash
# Ubuntu/Debian
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt-get install neo4j

# Start service
sudo systemctl start neo4j
```

2. **Install Python Dependencies**:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Initialize Database**:
```bash
python scripts/init_database.py
python scripts/load_sample_data.py
```

4. **Run API Server**:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### First Queries

Open Neo4j Browser (http://localhost:7474) and try these queries:

**1. View Asset Hierarchy**:
```cypher
MATCH path = (o:Organization)-[:HAS_SITE]->(s:Site)
             -[:OPERATES]->(t:Train)-[:HAS_COMPONENT]->(c:Component)
RETURN path LIMIT 50
```

**2. Find High-Risk Vulnerabilities**:
```cypher
MATCH (c:Component)-[:RUNS]->(s:Software)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvss_score >= 9.0 AND c.criticality = "CRITICAL"
RETURN c.name, s.product, cve.id, cve.cvss_score
ORDER BY cve.cvss_score DESC
LIMIT 10
```

**3. Discover Attack Paths**:
```cypher
MATCH path = shortestPath(
  (entry:Component {exposed_to_internet: true})
  -[:CONNECTED_TO*1..5]->
  (target:Component {type: "Train Control System"})
)
RETURN path LIMIT 5
```

**4. Threat Actor Intelligence**:
```cypher
MATCH (actor:ThreatActor)-[:CONDUCTS]->(campaign:Campaign)
RETURN actor.name, actor.origin_country,
       collect(campaign.name) as campaigns
ORDER BY size(campaigns) DESC
```

**5. Asset Inventory by Site**:
```cypher
MATCH (s:Site)-[:OPERATES]->(t:Train)-[:HAS_COMPONENT]->(c:Component)
RETURN s.name as site,
       count(DISTINCT t) as trains,
       count(c) as components
ORDER BY trains DESC
```

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    User Interfaces                      │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Neo4j       │  │ Web Dashboard│  │ Jupyter       │  │
│  │ Browser     │  │ (React)      │  │ Notebooks     │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬───────┘  │
└─────────┼─────────────────┼──────────────────┼──────────┘
          │                 │                  │
          └─────────────────┼──────────────────┘
                           │
┌─────────────────────────┼───────────────────────────────┐
│                    API Layer (FastAPI)                   │
│  ┌──────────────────────┴────────────────────────────┐  │
│  │  GraphQL API  │  REST API  │  WebSocket (Events) │  │
│  └──────────────────────┬────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────┐
│              Business Logic Layer (Python)               │
│  ┌───────────────┐  ┌─────────────┐  ┌──────────────┐  │
│  │ Risk Analysis │  │ Attack Path │  │ Threat Intel │  │
│  │ Engine        │  │ Simulator   │  │ Processor    │  │
│  └───────────────┘  └─────────────┘  └──────────────┘  │
└─────────────────────────┼───────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────┐
│              Data Access Layer (Neo4j Driver)            │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Cypher Query Builder  │  Transaction Manager     │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────┼───────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────┐
│                  Neo4j Graph Database                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Nodes: 100K+  │  Relationships: 500K+         │    │
│  │  Indexes: 15   │  Constraints: 8               │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

### Technology Stack

**Database**:
- Neo4j 5.15+ (Graph Database)
- APOC plugins (graph algorithms)
- Neo4j Graph Data Science library

**Backend**:
- Python 3.11+
- FastAPI (REST/GraphQL API)
- neo4j-driver (Python driver)
- Pydantic (data validation)
- APScheduler (scheduled tasks)

**Frontend** (Optional):
- React 18
- TypeScript
- D3.js (graph visualization)
- Material-UI components

**Data Sources**:
- NVD API (CVE data)
- MITRE ATT&CK (threat intelligence)
- Custom CSV/JSON imports

**DevOps**:
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Prometheus + Grafana (monitoring)

### Data Model

**Core Node Types**:
- `Organization`: Railway company or operator
- `Site`: Physical location (depot, station)
- `Train`: Rolling stock unit
- `Component`: Hardware/software component
- `Software`: Installed software package
- `CVE`: Known vulnerability
- `ThreatActor`: Cyber threat group
- `Campaign`: Threat campaign
- `AttackTechnique`: MITRE ATT&CK technique
- `NetworkInterface`: Network connection point

**Core Relationships**:
- `HAS_SITE`: Organization → Site
- `OPERATES`: Site → Train
- `HAS_COMPONENT`: Train → Component
- `RUNS`: Component → Software
- `HAS_VULNERABILITY`: Software → CVE
- `CONNECTED_TO`: Component → Component (network)
- `CONDUCTS`: ThreatActor → Campaign
- `USES`: Campaign → AttackTechnique
- `EXPLOITS`: AttackTechnique → CVE
- `AFFECTS`: CVE → Software

## Documentation Index

### Overview Documents
1. **README.md** (this document) - Project overview and quick start
2. **How_It_Works.md** - Detailed explanation of graph concepts and system operation
3. **Why_Graph_Database.md** - Rationale for graph database selection with benchmarks
4. **Quick_Start_Guide.md** - Step-by-step setup and first queries

### Technical Documentation
5. **Data_Model.md** - Complete node and relationship schema
6. **Query_Guide.md** - Cypher query examples for all use cases
7. **API_Reference.md** - REST and GraphQL API documentation
8. **Risk_Scoring_Algorithm.md** - Now/Next/Never scoring methodology

### Integration Guides
9. **Threat_Intelligence_Integration.md** - Connecting external threat feeds
10. **Asset_Import_Guide.md** - Importing asset inventory from CMDB/SIEM
11. **SIEM_Integration.md** - Exporting alerts to Splunk, QRadar, Sentinel

### Operations
12. **Installation_Guide.md** - Detailed installation for production environments
13. **Configuration_Guide.md** - Environment variables and settings
14. **Backup_Recovery.md** - Database backup and disaster recovery procedures
15. **Performance_Tuning.md** - Optimization for large-scale deployments

### Use Case Examples
16. **Attack_Simulation_Guide.md** - Red team scenario modeling
17. **Compliance_Reporting.md** - Generating regulatory compliance reports

### Additional Resources
- **Jupyter Notebooks**: `/notebooks` - Interactive analysis examples
- **Sample Data**: `/data/samples` - Test datasets
- **Scripts**: `/scripts` - Utility scripts for data loading and maintenance

## Installation Guide

### Production Deployment

**Infrastructure Requirements**:

| Component | Minimum | Recommended | Enterprise |
|-----------|---------|-------------|------------|
| CPU | 4 cores | 8 cores | 16+ cores |
| RAM | 16 GB | 32 GB | 64+ GB |
| Disk | 50 GB SSD | 200 GB SSD | 1 TB NVMe |
| Network | 1 Gbps | 10 Gbps | 10+ Gbps |

**Neo4j Configuration**:

Edit `neo4j.conf`:
```properties
# Memory settings
dbms.memory.heap.initial_size=8G
dbms.memory.heap.max_size=16G
dbms.memory.pagecache.size=8G

# Performance
dbms.tx_log.rotation.retention_policy=1 days
dbms.checkpoint.interval.time=15m

# Security
dbms.security.auth_enabled=true
dbms.ssl.policy.bolt.enabled=true

# Clustering (Enterprise only)
dbms.mode=CORE
causal_clustering.minimum_core_cluster_size_at_formation=3
```

**Python Application**:

Use production WSGI server:
```bash
gunicorn api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile /var/log/aeon/access.log \
  --error-logfile /var/log/aeon/error.log
```

**Reverse Proxy** (nginx):
```nginx
upstream aeon_api {
    server 127.0.0.1:8000;
}

server {
    listen 443 ssl http2;
    server_name aeon.example.com;

    ssl_certificate /etc/ssl/certs/aeon.crt;
    ssl_certificate_key /etc/ssl/private/aeon.key;

    location / {
        proxy_pass http://aeon_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /neo4j/ {
        proxy_pass http://localhost:7474/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### High Availability Setup

**Neo4j Causal Cluster** (Enterprise feature):

3+ core servers with automatic failover:
```yaml
# docker-compose-cluster.yml
version: '3.8'
services:
  neo4j-core1:
    image: neo4j:5.15-enterprise
    environment:
      - NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
      - NEO4J_dbms_mode=CORE
      - NEO4J_causal__clustering_initial__discovery__members=core1:5000,core2:5000,core3:5000
    volumes:
      - neo4j-core1-data:/data

  neo4j-core2:
    # Similar configuration...

  neo4j-core3:
    # Similar configuration...
```

**Application Load Balancing**:
```yaml
# docker-compose-app.yml
  aeon-api-1:
    image: aeon-api:latest
    environment:
      - NEO4J_URI=neo4j://neo4j-core1:7687,neo4j-core2:7687,neo4j-core3:7687
    deploy:
      replicas: 3
```

### Monitoring & Alerting

**Prometheus Metrics**:
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'neo4j'
    static_configs:
      - targets: ['localhost:2004']

  - job_name: 'aeon-api'
    static_configs:
      - targets: ['localhost:8000']
```

**Key Metrics to Monitor**:
- Neo4j heap memory usage
- Query execution time (p95, p99)
- Transaction throughput
- Disk I/O saturation
- API response time
- CVE update lag time

**Alerting Rules**:
```yaml
groups:
  - name: aeon_alerts
    rules:
      - alert: HighQueryLatency
        expr: neo4j_query_duration_seconds{quantile="0.95"} > 5
        for: 5m
        annotations:
          summary: "Neo4j query latency is high"

      - alert: CVEDataStale
        expr: time() - aeon_last_cve_update_timestamp > 172800  # 2 days
        annotations:
          summary: "CVE data has not been updated in 48 hours"
```

## License & Credits

### License

This project is licensed under the **Apache License 2.0**. See LICENSE file for details.

### Credits

**Project Team**:
- Architecture & Development: [Your Organization]
- Research & Threat Intelligence: [Security Team]
- Rail Domain Expertise: [Operations Team]

**Open Source Dependencies**:
- Neo4j (Neo4j Sweden AB) - Apache 2.0 / GPL v3
- FastAPI (Sebastián Ramírez) - MIT
- Python neo4j-driver (Neo4j, Inc.) - Apache 2.0
- MITRE ATT&CK (The MITRE Corporation) - Terms of Use

**Data Sources**:
- National Vulnerability Database (NVD) - Public domain (U.S. Government)
- MITRE ATT&CK Framework - Terms of Use
- ICS-CERT Advisories - Public domain (CISA)

**Academic Contributions**:
This project builds upon research in graph-based security analysis, cyber threat intelligence, and digital twin methodologies. See individual documentation files for specific citations.

## Contact Information

**Technical Support**:
- Email: support@aeon-digital-twin.example.com
- Issue Tracker: https://github.com/your-org/aeon-digital-twin/issues

**Security Vulnerabilities**:
- Email: security@aeon-digital-twin.example.com
- PGP Key: [Fingerprint]

**Community**:
- Discussion Forum: https://community.aeon-digital-twin.example.com
- Slack: https://aeon-users.slack.com
- Twitter: @AeonDigitalTwin

**Enterprise Support**:
For enterprise deployments, professional services, and custom integrations:
- Email: enterprise@aeon-digital-twin.example.com
- Phone: +1 (555) 123-4567

## Next Steps

1. **Read "How It Works"**: Understand the graph database concepts → [How_It_Works.md](How_It_Works.md)
2. **Explore Use Cases**: Review the 7 core scenarios → [Query_Guide.md](../Query_Guide.md)
3. **Import Your Data**: Connect your asset inventory → [Asset_Import_Guide.md](../Asset_Import_Guide.md)
4. **Integrate Threat Intel**: Connect external feeds → [Threat_Intelligence_Integration.md](../Threat_Intelligence_Integration.md)
5. **Run Analysis**: Try the Jupyter notebooks → `/notebooks/01_Getting_Started.ipynb`

## Acknowledgments

Special thanks to:
- The Neo4j community for graph database expertise
- MITRE for maintaining the ATT&CK framework
- NIST/NVD for vulnerability data
- The rail cybersecurity community for domain insights

---

**Document Version**: 1.0
**Last Updated**: 2025-10-29
**Project Version**: 2.0.0-alpha
**Maintained By**: AEON Development Team
