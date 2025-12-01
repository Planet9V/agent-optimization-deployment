# AEON Digital Twin: Quick Start Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Options](#installation-options)
3. [Option 1: Docker Compose (Recommended)](#option-1-docker-compose-recommended)
4. [Option 2: Manual Installation](#option-2-manual-installation)
5. [Loading Sample Data](#loading-sample-data)
6. [First Queries](#first-queries)
7. [Next Steps](#next-steps)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum**:
- **CPU**: 4 cores (2.0 GHz+)
- **RAM**: 16GB
- **Storage**: 50GB SSD
- **OS**: Linux (Ubuntu 22.04+), macOS (12+), Windows 10+

**Recommended for Production**:
- **CPU**: 8+ cores
- **RAM**: 32GB+
- **Storage**: 100GB+ NVMe SSD
- **OS**: Linux (Ubuntu 22.04 LTS)

### Software Prerequisites

**Required**:
1. **Neo4j 5.15+** (graph database)
2. **Python 3.11+** (application runtime)
3. **Git** (version control)

**Optional but Recommended**:
4. **Docker** & **Docker Compose** (containerized deployment)
5. **Jupyter** (interactive notebooks)

### Skills Required

- **Basic Linux/Terminal**: File navigation, command execution
- **Basic Python**: Understanding virtual environments (if not using Docker)
- **Basic Cypher**: Neo4j query language (covered in this guide)
- **Cybersecurity Concepts**: CVE, CVSS, network topology

**Time to Complete**: 15-30 minutes for basic setup, 1-2 hours for full exploration

## Installation Options

Two paths available:

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **Docker Compose** | Quick setup, isolated environment, easy cleanup | Requires Docker (4GB+ disk) | Evaluation, development |
| **Manual Installation** | Full control, production-ready | More setup steps, system-wide changes | Production, customization |

**Recommendation**: Start with Docker Compose for evaluation, migrate to manual installation for production.

## Option 1: Docker Compose (Recommended)

### Step 1: Install Docker

**Ubuntu/Debian**:
```bash
# Remove old versions
sudo apt-get remove docker docker-engine docker.io containerd runc

# Install dependencies
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
sudo docker run hello-world
```

**macOS**:
```bash
# Install via Homebrew
brew install --cask docker

# Or download Docker Desktop from:
# https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
docker compose version
```

**Windows**:
1. Download Docker Desktop: https://www.docker.com/products/docker-desktop
2. Install and restart
3. Verify in PowerShell: `docker --version`

### Step 2: Clone Repository

```bash
# Clone the AEON repository
git clone https://github.com/your-org/aeon-digital-twin.git
cd aeon-digital-twin

# Verify files
ls -la
# Expected: docker-compose.yml, .env.example, requirements.txt, scripts/
```

### Step 3: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration (use your preferred editor)
nano .env
```

**Key configuration settings**:
```bash
# Neo4j Configuration
NEO4J_AUTH=neo4j/YourSecurePassword123!  # CHANGE THIS!
NEO4J_EDITION=community  # or 'enterprise' if licensed

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=$(openssl rand -hex 32)  # Generate random key

# Optional: External Threat Intelligence
NVD_API_KEY=your_nvd_api_key_here  # Get from https://nvd.nist.gov/developers/request-an-api-key
MITRE_API_ENABLED=true

# Logging
LOG_LEVEL=INFO  # DEBUG for development, WARNING for production
```

**Security Notes**:
- ⚠️ **NEVER** commit `.env` to version control (already in `.gitignore`)
- 🔐 Use strong passwords (20+ characters, mixed case, numbers, symbols)
- 🔑 Generate API secret key with `openssl rand -hex 32`

### Step 4: Start Services

```bash
# Start all services (Neo4j, API, Jupyter)
docker compose up -d

# Expected output:
# [+] Running 4/4
#  ✔ Network aeon-network      Created
#  ✔ Container aeon-neo4j       Started
#  ✔ Container aeon-api         Started
#  ✔ Container aeon-jupyter     Started

# Verify services are running
docker compose ps

# Expected output:
# NAME            IMAGE                  STATUS          PORTS
# aeon-neo4j      neo4j:5.15            Up 30 seconds   0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp
# aeon-api        aeon-api:latest       Up 20 seconds   0.0.0.0:8000->8000/tcp
# aeon-jupyter    jupyter/base:latest   Up 20 seconds   0.0.0.0:8888->8888/tcp
```

**Service Ports**:
- **7474**: Neo4j Browser (web UI)
- **7687**: Neo4j Bolt (database connection)
- **8000**: AEON API (REST/GraphQL)
- **8888**: Jupyter Notebooks

### Step 5: Verify Installation

```bash
# Check Neo4j is ready (may take 30-60 seconds for first startup)
curl -X GET http://localhost:7474/browser/

# Check API is responsive
curl -X GET http://localhost:8000/health

# Expected API response:
# {"status":"healthy","neo4j":"connected","version":"2.0.0"}

# View logs if issues
docker compose logs neo4j
docker compose logs api
```

### Step 6: Access Web Interfaces

**Neo4j Browser**:
1. Open browser: http://localhost:7474
2. Connect URL: `bolt://localhost:7687`
3. Username: `neo4j`
4. Password: `<your password from .env>`
5. Click "Connect"

**AEON API Documentation**:
- Open: http://localhost:8000/docs
- Interactive Swagger UI for testing API endpoints

**Jupyter Notebooks**:
1. Open: http://localhost:8888
2. Token from logs: `docker compose logs jupyter | grep token`
3. Navigate to `/notebooks/01_Getting_Started.ipynb`

**Screenshot of Neo4j Browser**:
```
┌─────────────────────────────────────────────────────┐
│ Neo4j Browser                                       │
│ Connected to: bolt://localhost:7687                 │
│ Database: neo4j                                     │
├─────────────────────────────────────────────────────┤
│  Query Editor:                                      │
│  ┌───────────────────────────────────────────────┐ │
│  │ MATCH (n) RETURN count(n) AS node_count      │ │
│  └───────────────────────────────────────────────┘ │
│                                        [Run Query]  │
├─────────────────────────────────────────────────────┤
│  Results:                                           │
│  ┌───────────────────────────────────────────────┐ │
│  │ node_count                                    │ │
│  │ 0                                             │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Option 2: Manual Installation

### Step 1: Install Neo4j

**Ubuntu/Debian**:
```bash
# Add Neo4j repository
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list

# Install Neo4j Community Edition
sudo apt-get update
sudo apt-get install -y neo4j=1:5.15.0

# Configure Neo4j
sudo nano /etc/neo4j/neo4j.conf

# Key settings:
# dbms.default_listen_address=0.0.0.0
# dbms.connector.bolt.enabled=true
# dbms.connector.http.enabled=true
# dbms.memory.heap.initial_size=2G
# dbms.memory.heap.max_size=4G
# dbms.memory.pagecache.size=2G

# Start Neo4j
sudo systemctl enable neo4j
sudo systemctl start neo4j

# Verify status
sudo systemctl status neo4j
```

**macOS**:
```bash
# Install via Homebrew
brew install neo4j

# Start Neo4j
neo4j start

# Access browser: http://localhost:7474
```

**Windows**:
1. Download Neo4j Desktop: https://neo4j.com/download/
2. Install and create new DBMS
3. Start database instance

### Step 2: Install Python and Dependencies

```bash
# Check Python version (must be 3.11+)
python3 --version

# If Python 3.11+ not available, install:
# Ubuntu:
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev

# Clone repository
git clone https://github.com/your-org/aeon-digital-twin.git
cd aeon-digital-twin

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Expected packages:
# - neo4j (Python driver)
# - fastapi (API framework)
# - uvicorn (ASGI server)
# - pydantic (data validation)
# - python-dotenv (environment variables)
# - requests (HTTP client)
# - pandas (data processing)
# - jupyter (notebooks)
```

### Step 3: Configure Environment

```bash
# Copy example environment
cp .env.example .env

# Edit configuration
nano .env
```

**Configuration for manual installation**:
```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=YourSecurePassword123!  # CHANGE THIS!

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
API_SECRET_KEY=$(openssl rand -hex 32)

# Optional: NVD API Key
NVD_API_KEY=your_nvd_api_key_here
```

### Step 4: Initialize Database

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Run database initialization script
python scripts/init_database.py

# Expected output:
# [INFO] Connecting to Neo4j at bolt://localhost:7687
# [INFO] Creating constraints...
# [SUCCESS] Created constraint: component_uuid_unique
# [SUCCESS] Created constraint: cve_id_unique
# [INFO] Creating indexes...
# [SUCCESS] Created index: component_criticality
# [SUCCESS] Created index: cve_cvss_score
# [INFO] Database initialization complete!
```

### Step 5: Start API Server

```bash
# Development mode (auto-reload on code changes)
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

# Production mode (with Gunicorn for performance)
gunicorn api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

**Verify API**:
```bash
# In another terminal
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","neo4j":"connected","version":"2.0.0"}
```

## Loading Sample Data

Sample data provides a realistic rail infrastructure for exploration and testing.

### Docker Compose Environment

```bash
# Run sample data loader
docker compose exec api python scripts/load_sample_data.py

# With custom options
docker compose exec api python scripts/load_sample_data.py \
  --organizations 2 \
  --sites 5 \
  --trains 20 \
  --components-per-train 5 \
  --cves 1000
```

### Manual Installation

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Run sample data loader
python scripts/load_sample_data.py

# Expected output:
# [INFO] Loading sample data...
# [INFO] Creating organizations... (2)
# [SUCCESS] Created: National Rail Company
# [SUCCESS] Created: Regional Transit Authority
# [INFO] Creating sites... (5)
# [SUCCESS] Created: Central Depot (London)
# [SUCCESS] Created: North Station (Manchester)
# ...
# [INFO] Creating trains... (20)
# [SUCCESS] Created: EMU500-2024-001 at Central Depot
# ...
# [INFO] Creating components... (100)
# [SUCCESS] Created: Train Control System on EMU500-2024-001
# ...
# [INFO] Creating software... (50)
# [SUCCESS] Created: Siemens TCMS v5.2.1
# ...
# [INFO] Loading CVEs from NVD... (1000)
# [SUCCESS] Loaded: CVE-2024-12345 (CVSS: 9.8)
# ...
# [INFO] Creating threat actors... (10)
# [SUCCESS] Created: APT28 (Russia)
# ...
# [INFO] Creating campaigns... (20)
# [SUCCESS] Created: Operation GhostTrain
# ...
# [INFO] Linking relationships...
# [SUCCESS] Created 2,500 relationships
# [INFO] Sample data loading complete!
# [INFO] Summary:
#   - Organizations: 2
#   - Sites: 5
#   - Trains: 20
#   - Components: 100
#   - Software: 50
#   - CVEs: 1,000
#   - Threat Actors: 10
#   - Campaigns: 20
#   - Total Nodes: 1,207
#   - Total Relationships: 2,500
```

### Verify Sample Data

**Neo4j Browser**:
```cypher
// Count nodes by type
MATCH (n)
RETURN labels(n) AS node_type, count(n) AS count
ORDER BY count DESC
```

**Expected Results**:
```
node_type           count
["CVE"]             1000
["Component"]       100
["Software"]        50
["Train"]           20
["Campaign"]        20
["Site"]            5
["Organization"]    2
["ThreatActor"]     10
```

**Visualize Sample Network**:
```cypher
// Show asset hierarchy for one train
MATCH path = (o:Organization)-[:HAS_SITE]->(s:Site)
             -[:OPERATES]->(t:Train {serial_number: "EMU500-2024-001"})
             -[:HAS_COMPONENT]->(c:Component)
             -[:RUNS]->(sw:Software)
RETURN path
LIMIT 50
```

## First Queries

Try these five queries to explore the sample data.

### Query 1: Asset Inventory by Site

**What it does**: Count trains and components at each site.

```cypher
MATCH (s:Site)-[:OPERATES]->(t:Train)-[:HAS_COMPONENT]->(c:Component)
RETURN s.name AS site,
       s.location.latitude AS latitude,
       s.location.longitude AS longitude,
       count(DISTINCT t) AS trains,
       count(c) AS components
ORDER BY trains DESC
```

**Expected Output**:
```
site              latitude  longitude  trains  components
Central Depot     51.5074   -0.1278    8       40
North Station     53.4808   -2.2426    6       30
East Maintenance  51.5155   0.0922     4       20
West Yard         51.5074   -0.1749    2       10
```

**Interpretation**: Central Depot has the most assets (8 trains, 40 components), making it a critical location for security focus.

### Query 2: High-Severity Vulnerabilities

**What it does**: Find all critical CVEs (CVSS ≥ 9.0) affecting your assets.

```cypher
MATCH (c:Component)-[:RUNS]->(s:Software)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvss_v3_score >= 9.0
RETURN c.name AS component,
       c.criticality AS criticality,
       s.product AS software,
       s.version AS version,
       cve.cve_id AS vulnerability,
       cve.cvss_v3_score AS cvss_score,
       cve.severity AS severity,
       cve.exploit_available AS has_exploit
ORDER BY cve.cvss_v3_score DESC, c.criticality DESC
LIMIT 20
```

**Expected Output**:
```
component               criticality  software            version  vulnerability      cvss_score  severity  has_exploit
Train Control System    CRITICAL     Siemens TCMS       5.2.1    CVE-2024-12345     9.8         CRITICAL  true
SCADA Controller        CRITICAL     Schneider SCADA    3.1.0    CVE-2024-23456     9.8         CRITICAL  true
HMI Display             HIGH         Siemens WinCC      7.5      CVE-2023-34567     9.1         CRITICAL  false
Network Router          HIGH         Cisco IOS          15.2     CVE-2024-45678     9.0         CRITICAL  true
```

**Interpretation**: 4 critical vulnerabilities found, 3 with available exploits. Prioritize patching Train Control System and SCADA Controller (CRITICAL assets with exploits).

### Query 3: Attack Path Discovery

**What it does**: Find shortest paths from internet-exposed components to critical systems.

```cypher
MATCH path = shortestPath(
  (entry:Component {exposed_to_internet: true})
  -[:CONNECTED_TO*1..5]->(target:Component {criticality: "CRITICAL"})
)
RETURN [n IN nodes(path) | n.name] AS attack_path,
       length(path) AS hops,
       [n IN nodes(path) | n.security_zone] AS zones_traversed
ORDER BY hops
LIMIT 10
```

**Expected Output**:
```
attack_path                                              hops  zones_traversed
["Web Portal", "App Server", "Database", "SCADA"]        3     ["DMZ", "WEB_TIER", "DATA_TIER", "CRITICAL_OT"]
["VPN Gateway", "Management Server", "Train Control"]    2     ["DMZ", "CORPORATE_IT", "CRITICAL_OT"]
["Remote Access", "Jump Host", "Engineering Station"]    2     ["DMZ", "OPERATIONS_IT", "CRITICAL_OT"]
```

**Interpretation**: Shortest attack path is 2 hops (VPN Gateway → Management Server → Train Control). This violates segmentation best practices (should require 4+ hops with multiple firewall layers).

**🚨 Action Required**: Review network segmentation between DMZ and CRITICAL_OT zones.

### Query 4: Threat Actor Intelligence

**What it does**: Identify which threat actors target your assets and what vulnerabilities they exploit.

```cypher
MATCH (actor:ThreatActor)-[:CONDUCTS]->(campaign:Campaign)
      -[:USES]->(technique:AttackTechnique)
      -[:EXPLOITS]->(cve:CVE)
      -[:AFFECTS]->(sw:Software)
      <-[:RUNS]-(c:Component)
WHERE c.criticality IN ["CRITICAL", "HIGH"]
RETURN actor.name AS threat_actor,
       actor.origin_country AS origin,
       campaign.name AS campaign,
       technique.technique_id AS att_ck_technique,
       cve.cve_id AS vulnerability,
       count(DISTINCT c) AS exposed_components
ORDER BY exposed_components DESC
LIMIT 10
```

**Expected Output**:
```
threat_actor  origin   campaign              att_ck_technique  vulnerability      exposed_components
APT28         Russia   Operation GhostTrain  T1190             CVE-2024-12345     23
Sandworm      Russia   RailStrike            T1133             CVE-2024-23456     18
ChaosCC       China    DragonRail            T1078             N/A                45
Lazarus       N.Korea  TrainHeist            T1190             CVE-2023-34567     12
```

**Interpretation**:
- **APT28** is actively targeting 23 of your components using CVE-2024-12345
- **ChaosCC** has the highest exposure (45 components) via valid account abuse (no CVE, credential-based)
- **Priority**: Patch CVE-2024-12345 immediately, enforce MFA on all accounts

### Query 5: Network Segmentation Audit

**What it does**: Find components that can communicate across security zones without firewall intermediation (segmentation violations).

```cypher
MATCH path = (src:Component)-[:CONNECTED_TO*1..2]->(dst:Component)
WHERE src.security_zone <> dst.security_zone
  AND NOT exists(
    (src)-[:CONNECTED_TO]->(:Component {component_type: "Firewall"})
    -[:CONNECTED_TO]->(dst)
  )
WITH src, dst, path,
     src.security_zone AS src_zone,
     dst.security_zone AS dst_zone
RETURN src.name AS source_component,
       src_zone,
       dst.name AS destination_component,
       dst_zone,
       length(path) AS hops,
       [rel IN relationships(path) | rel.protocol + ":" + toString(rel.port)] AS protocols
ORDER BY dst_zone DESC, hops
LIMIT 20
```

**Expected Output**:
```
source_component     src_zone        destination_component  dst_zone       hops  protocols
Web Application      WEB_TIER        SCADA Controller       CRITICAL_OT    2     ["HTTP:8080", "Modbus:502"]
File Server          CORPORATE_IT    Train Database         CRITICAL_OT    1     ["SQL:5432"]
Remote Desktop       DMZ             Control HMI            CRITICAL_OT    2     ["RDP:3389", "VNC:5900"]
```

**Interpretation**: 3 critical segmentation violations found:
1. **Web Application → SCADA**: HTTP/Modbus access without firewall (2 hops)
2. **File Server → Train Database**: Direct SQL access from corporate IT to critical OT (1 hop)
3. **Remote Desktop → Control HMI**: RDP access from DMZ to critical OT (2 hops)

**🚨 Immediate Actions**:
1. Deploy industrial DMZ firewall between WEB_TIER and CRITICAL_OT
2. Remove direct SQL access from File Server to Train Database
3. Enforce jump host for remote access to OT systems

## Next Steps

### 1. Read Conceptual Documentation

- **[How It Works](How_It_Works.md)**: Understand graph database concepts, asset modeling, attack path simulation
- **[Why Graph Database](Why_Graph_Database.md)**: Performance benchmarks, use case justification, trade-offs

### 2. Explore Advanced Queries

Open `/docs/Query_Guide.md` for comprehensive Cypher query examples covering:
- Vulnerability assessment (7 query patterns)
- Attack path analysis (5 algorithms)
- Threat intelligence correlation (4 scenarios)
- Risk scoring (Now/Next/Never methodology)
- Compliance reporting (IEC 62443, NIST CSF)

### 3. Import Your Asset Data

Follow `/docs/Asset_Import_Guide.md` to import from:
- **CMDB** (Configuration Management Database): ServiceNow, Jira
- **SIEM** (Security Information and Event Management): Splunk, QRadar
- **Network Scanners**: Nmap, Nessus, Qualys
- **Spreadsheets**: CSV/Excel with asset inventory

**Quick import example**:
```bash
# Prepare your CSV with columns: name, type, ip_address, criticality
python scripts/import_assets.py \
  --csv-file /path/to/assets.csv \
  --organization "Your Company" \
  --site "Your Site"
```

### 4. Integrate Threat Intelligence Feeds

Connect external threat intelligence sources:

**National Vulnerability Database (NVD)**:
```bash
# Configure NVD API key in .env
NVD_API_KEY=your_nvd_api_key

# Run daily CVE sync
python scripts/sync_nvd_cves.py --days-back 7
```

**MITRE ATT&CK**:
```bash
# Download latest ATT&CK data
python scripts/sync_mitre_attack.py
```

**CISA Known Exploited Vulnerabilities (KEV)**:
```bash
# Sync CISA KEV catalog
python scripts/sync_cisa_kev.py
```

See `/docs/Threat_Intelligence_Integration.md` for detailed setup.

### 5. Run Jupyter Notebooks

Interactive analysis notebooks in `/notebooks`:

**01_Getting_Started.ipynb**:
- Basic Cypher queries
- Data visualization with Python
- Asset inventory reports

**02_Vulnerability_Analysis.ipynb**:
- CVE impact assessment
- Risk scoring calculations
- Patch prioritization

**03_Attack_Path_Simulation.ipynb**:
- Red team scenario modeling
- Lateral movement analysis
- Network segmentation validation

**04_Threat_Intelligence.ipynb**:
- Threat actor profiling
- Campaign tracking
- ATT&CK technique mapping

**05_Compliance_Reporting.ipynb**:
- IEC 62443 compliance checks
- NIST Cybersecurity Framework mapping
- Automated report generation

**Start Jupyter**:
```bash
# Docker Compose
docker compose exec jupyter jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# Manual installation
source venv/bin/activate
jupyter notebook
```

### 6. Set Up Automated Updates

Schedule daily threat intelligence updates:

**Cron Job (Linux)**:
```bash
# Edit crontab
crontab -e

# Add daily updates at 2 AM
0 2 * * * cd /path/to/aeon-digital-twin && /path/to/venv/bin/python scripts/sync_nvd_cves.py --days-back 1 >> logs/nvd_sync.log 2>&1
0 3 * * * cd /path/to/aeon-digital-twin && /path/to/venv/bin/python scripts/sync_cisa_kev.py >> logs/kev_sync.log 2>&1
```

**Task Scheduler (Windows)**:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 2:00 AM
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `scripts/sync_nvd_cves.py --days-back 1`
7. Start in: `C:\path\to\aeon-digital-twin`

## Troubleshooting

### Issue: Neo4j Won't Start

**Symptoms**:
- `docker compose ps` shows `aeon-neo4j` status as "Restarting" or "Exit 1"
- Error: "Failed to start Neo4j"

**Solutions**:

1. **Check port conflicts**:
```bash
# Check if ports 7474 or 7687 are in use
sudo netstat -tuln | grep 7474
sudo netstat -tuln | grep 7687

# Kill conflicting processes
sudo fuser -k 7474/tcp
sudo fuser -k 7687/tcp
```

2. **Check memory allocation**:
```bash
# Neo4j requires 2GB+ RAM
free -h

# Adjust Docker memory limits in docker-compose.yml:
services:
  neo4j:
    mem_limit: 4g
    memswap_limit: 4g
```

3. **Check logs**:
```bash
docker compose logs neo4j

# Common errors:
# - "Out of memory" → Increase mem_limit
# - "Permission denied" → Fix file permissions: sudo chown -R 7474:7474 data/neo4j
# - "Address already in use" → Port conflict (see solution 1)
```

### Issue: "Connection Refused" When Accessing Neo4j Browser

**Symptoms**:
- Browser shows "Connection refused" at http://localhost:7474
- Neo4j container is running

**Solutions**:

1. **Wait for initialization** (first startup takes 30-60 seconds):
```bash
# Monitor Neo4j startup
docker compose logs -f neo4j

# Wait for: "Started."
```

2. **Check firewall rules**:
```bash
# Linux: Allow ports 7474 and 7687
sudo ufw allow 7474/tcp
sudo ufw allow 7687/tcp

# Verify firewall status
sudo ufw status
```

3. **Try alternate connection URL**:
```
# If localhost doesn't work, try:
http://127.0.0.1:7474
# or
http://<your-ip-address>:7474
```

### Issue: API Returns "Neo4j connection failed"

**Symptoms**:
- `curl http://localhost:8000/health` returns `{"status":"unhealthy","neo4j":"disconnected"}`

**Solutions**:

1. **Verify Neo4j credentials in .env**:
```bash
# Check .env file
cat .env | grep NEO4J

# Should match Docker Compose neo4j service:
# NEO4J_AUTH=neo4j/YourPassword
```

2. **Test Neo4j connection manually**:
```bash
# Docker Compose
docker compose exec api python -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://neo4j:7687', auth=('neo4j', 'YourPassword'))
with driver.session() as session:
    result = session.run('RETURN 1 AS test')
    print(result.single()['test'])
driver.close()
"

# Expected output: 1
```

3. **Check network connectivity**:
```bash
# Docker Compose services should be on same network
docker network inspect aeon-network

# Verify aeon-neo4j and aeon-api are listed
```

### Issue: Sample Data Load Fails with "Memory Error"

**Symptoms**:
- `python scripts/load_sample_data.py` crashes with "MemoryError"
- Neo4j logs show "OutOfMemoryError: Java heap space"

**Solutions**:

1. **Increase Neo4j heap memory**:
```yaml
# Edit docker-compose.yml
services:
  neo4j:
    environment:
      - NEO4J_dbms_memory_heap_initial__size=2G  # Increase from 1G
      - NEO4J_dbms_memory_heap_max__size=4G      # Increase from 2G
```

2. **Load data in smaller batches**:
```bash
# Load smaller dataset
python scripts/load_sample_data.py \
  --organizations 1 \
  --sites 2 \
  --trains 10 \
  --cves 100
```

3. **Monitor memory usage**:
```bash
# Check container memory
docker stats aeon-neo4j

# If usage near limit, increase Docker resource allocation:
# Docker Desktop → Settings → Resources → Memory: 8GB+
```

### Issue: Cypher Query Returns "No Results"

**Symptoms**:
- Query runs successfully but returns 0 rows
- Expected data based on sample load

**Solutions**:

1. **Verify data exists**:
```cypher
// Count all nodes
MATCH (n) RETURN count(n) AS total_nodes

// If 0, sample data didn't load
// Re-run: python scripts/load_sample_data.py
```

2. **Check query filters**:
```cypher
// Example: If no results for CRITICAL components
MATCH (c:Component {criticality: "CRITICAL"})
RETURN c

// Try without filter first
MATCH (c:Component)
RETURN c.criticality, count(c)
// Check what criticality values exist
```

3. **Verify relationship direction**:
```cypher
// Wrong direction (no results)
MATCH (cve:CVE)-[:HAS_VULNERABILITY]->(sw:Software)
RETURN cve, sw

// Correct direction
MATCH (sw:Software)-[:HAS_VULNERABILITY]->(cve:CVE)
RETURN sw, cve
```

### Issue: Slow Query Performance

**Symptoms**:
- Queries take >5 seconds
- Neo4j Browser shows "Query took 12000ms"

**Solutions**:

1. **Create indexes**:
```bash
# Run index creation script
python scripts/init_database.py

# Verify indexes exist
# Neo4j Browser:
SHOW INDEXES
```

2. **Profile query**:
```cypher
PROFILE
MATCH (c:Component)-[:RUNS]->(s:Software)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvss_v3_score >= 9.0
RETURN c, s, cve

// Look for "AllNodesScan" (bad) vs "NodeIndexSeek" (good)
```

3. **Limit result set**:
```cypher
// Add LIMIT to queries
MATCH (c:Component)
RETURN c
LIMIT 100  // Prevent loading thousands of nodes
```

### Getting Help

**Documentation**:
- Full documentation: `/docs/` directory
- API reference: http://localhost:8000/docs

**Community Support**:
- GitHub Issues: https://github.com/your-org/aeon-digital-twin/issues
- Discussion Forum: https://community.aeon-digital-twin.example.com
- Slack: https://aeon-users.slack.com

**Commercial Support**:
- Email: support@aeon-digital-twin.example.com
- Enterprise support plans available

**Neo4j Community**:
- Neo4j Community Forum: https://community.neo4j.com
- Neo4j Documentation: https://neo4j.com/docs/

---

**Document Version**: 1.0
**Last Updated**: 2025-10-29
**Estimated Setup Time**: 15-30 minutes (Docker), 45-60 minutes (Manual)
**Maintainer**: AEON Development Team

## Quick Reference Card

**Essential Commands**:
```bash
# Docker Compose
docker compose up -d              # Start all services
docker compose down               # Stop all services
docker compose logs -f <service>  # View logs
docker compose ps                 # Check service status

# Load Data
python scripts/load_sample_data.py

# Access Interfaces
http://localhost:7474             # Neo4j Browser
http://localhost:8000/docs        # API Documentation
http://localhost:8888             # Jupyter Notebooks

# Essential Cypher Queries
MATCH (n) RETURN count(n)                                    # Count all nodes
MATCH (c:Component) RETURN c LIMIT 100                       # List components
MATCH ()-[r]->() RETURN type(r), count(r)                   # Count relationships
SHOW INDEXES                                                 # List indexes
```

**Next Steps Checklist**:
- [ ] Neo4j Browser accessible
- [ ] Sample data loaded
- [ ] First 5 queries executed
- [ ] Read "How It Works" documentation
- [ ] Import your own asset data
- [ ] Set up threat intelligence feeds
- [ ] Explore Jupyter notebooks
- [ ] Schedule automated updates

Happy analyzing! 🔐🚂
