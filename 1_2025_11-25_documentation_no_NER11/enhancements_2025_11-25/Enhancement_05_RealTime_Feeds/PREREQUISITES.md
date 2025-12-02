# PREREQUISITES - Real-Time Threat Feed Integration

**Document**: Prerequisites and Environment Setup
**Version**: 1.0.0
**Created**: 2025-11-25
**Status**: ACTIVE
**Updated**: 2025-11-25

## System Requirements

### Hardware Specifications

**Minimum**:
- CPU: 4 cores @ 2.5+ GHz
- RAM: 8 GB (for development)
- Storage: 50 GB SSD (for Neo4j, logs, cache)
- Network: 100 Mbps minimum sustained bandwidth

**Recommended for Production**:
- CPU: 8+ cores @ 3.0+ GHz
- RAM: 16-32 GB
- Storage: 500 GB SSD (multi-region replication)
- Network: 1 Gbps, redundant connections

### Software Stack

**Required**:
- Python 3.11+ (API clients, processors)
- Java 11+ (Neo4j database)
- Docker 20.10+ (containerization)
- Docker Compose 1.29+ (orchestration)
- Git 2.30+ (version control)
- PostgreSQL 13+ (optional - for audit logs)

**Optional but Recommended**:
- Kubernetes 1.24+ (production orchestration)
- Prometheus 2.40+ (metrics collection)
- Grafana 9.0+ (dashboards)
- ELK Stack 8.0+ (centralized logging)
- Redis 6.0+ (caching/sessions)

## API Keys & Credentials

### 1. VulnCheck API Key

**Source**: https://vulncheck.com/
**Authorization**: Application/Account Settings
**Required**: Yes (critical for zero-day intelligence)

**Setup Steps**:
1. Create account at https://vulncheck.com/
2. Navigate to Settings → API Keys
3. Generate new API key
4. Save key securely: `VULNCHECK_API_KEY=<key>`

**Verification**:
```bash
curl -H "Authorization: Bearer $VULNCHECK_API_KEY" \
  https://api.vulncheck.com/v3/vulnerabilities?limit=1
# Should return 200 with vulnerability data
```

**Rate Limits**:
- Standard: 300 requests/minute
- Enterprise: 1,000+ requests/minute

**Cost**: Freemium tier (limited records) to $X/month enterprise

---

### 2. NVD API Key (Optional)

**Source**: https://nvd.nist.gov/developers
**Authorization**: Self-service registration
**Required**: No (public access available, but key recommended)

**Setup Steps**:
1. Go to https://nvd.nist.gov/developers
2. Click "Request API Key"
3. Verify email
4. Save key: `NVD_API_KEY=<key>`

**Verification**:
```bash
curl "https://services.nvd.nist.gov/rest/json/cves/2.0" \
  -H "X-API-KEY: $NVD_API_KEY"
# Should return 200 with CVE data
```

**Rate Limits**:
- Without key: 5 requests/30 seconds
- With key: 30 requests/30 seconds

**Cost**: Free

---

### 3. CISA KEV Feed (No Authentication)

**Source**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
**Format**: CSV (automated download)
**Frequency**: Updated weekly (Thursdays)

**Verification**:
```bash
curl -o known_exploited_vulnerabilities.csv \
  https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv
# Should download CSV file (500KB+)
```

**Cost**: Free

---

### 4. MITRE ATT&CK Framework (No Authentication)

**Source**: https://github.com/mitre-attack/attack-stix-data
**Format**: STIX 2.1 JSON
**Frequency**: Updated quarterly (with patches)

**Verification**:
```bash
curl -o enterprise-attack.json \
  https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack.json
# Should download JSON (50MB+)
```

**Cost**: Free

---

### 5. STIX/TAXII Feed (Source-Dependent)

**Common Providers**:
- Anomali Limo (free community feed)
- Cert-EU TAXII feed (EU threat intel)
- US-CERT CISA TAXII servers (government feeds)
- Commercial: Mandiant, ThreatStream, Recorded Future

**Setup Example (Anomali Limo)**:
```bash
export TAXII_DISCOVERY_URL="https://cti-taxii.mitre.org"
export TAXII_USERNAME="guest"
export TAXII_PASSWORD="guest"
```

**Cost**: Free (community) to $XXX/month (commercial)

---

### 6. Optional: Threat Intelligence News Sources

**Free Sources**:
- Krebs on Security RSS: https://krebsonsecurity.com/feed/
- Bleeping Computer: https://www.bleepingcomputer.com/feed/
- SecurityWeek: https://www.securityweek.com/feed/
- Ars Technica Security: https://arstechnica.com/feed/

**Commercial**:
- Threat Intelligence Platform subscriptions
- Dark web monitoring services

**Cost**: Free to $XXX/month

---

## Environment Configuration

### Development Environment Setup

**1. Clone Repository**:
```bash
cd /home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_05_RealTime_Feeds
git clone <repo> .
```

**2. Create `.env` File**:
```bash
# API Keys
VULNCHECK_API_KEY=<your-api-key>
NVD_API_KEY=<optional-api-key>
TAXII_DISCOVERY_URL=<taxii-server-url>
TAXII_USERNAME=<username>
TAXII_PASSWORD=<password>

# Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<secure-password>
NEO4J_DATABASE=aeon_threat

# Message Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
RABBITMQ_QUEUE=threat-feed-ingestion

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/aeon/realtime-feeds.log
ELK_ENABLED=false
ELK_HOST=localhost:9200

# Notifications
SLACK_WEBHOOK_URL=<webhook-url>
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=alerts@aeon-dt.security

# Monitoring
PROMETHEUS_PORT=8888
PROMETHEUS_ENABLED=false
```

**3. Don't Commit `.env`**:
```bash
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

**4. Use Secure Secret Management** (Production):
```bash
# Kubernetes secrets
kubectl create secret generic aeon-apikeys \
  --from-literal=vulncheck-api-key=$VULNCHECK_API_KEY \
  --from-literal=nvd-api-key=$NVD_API_KEY

# Docker secrets (Swarm)
echo $VULNCHECK_API_KEY | docker secret create vulncheck_api_key -
```

---

## Database Prerequisites

### Existing Level 5 Knowledge Graph State

**Current Verified Nodes** (as of 2025-11-25):
- 5,001 InformationEvent nodes
- 12,000+ relationship edges
- 8 main entity types
- 4 metadata layers

**Node Types**:
1. Vulnerability (CVEs)
2. ThreatActor (APT groups)
3. Campaign (coordinated activities)
4. Malware (malware families)
5. MitreTechnique (ATT&CK techniques)
6. Asset (infrastructure targets)
7. Indicator (IoCs)
8. InformationEvent (base entity)

**Query Existing Nodes**:
```cypher
MATCH (n:Vulnerability)
RETURN count(n) as vulnerability_count;

MATCH (n:ThreatActor)
RETURN count(n) as actor_count;

MATCH (n:InformationEvent)
RETURN count(n) as total_events;
```

### Neo4j Setup

**Installation** (Docker):
```bash
docker run -d \
  --name neo4j \
  --env NEO4J_AUTH=neo4j/yourpassword \
  --env NEO4JLABS_PLUGINS='["apoc"]' \
  -p 7474:7474 \
  -p 7687:7687 \
  -v neo4j_data:/data \
  -v neo4j_logs:/logs \
  neo4j:5.7
```

**Installation** (Linux Package):
```bash
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 5' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update && sudo apt install neo4j
sudo systemctl start neo4j
```

**Verify Installation**:
```bash
# Access Neo4j Browser
open http://localhost:7474

# Or use cypher-shell
cypher-shell -a bolt://localhost:7687 -u neo4j -p yourpassword
```

**Plugins Required**:
- APOC (Awesome Procedures on Cypher)
- Graph Data Science (GDS) - optional for ML features

**Enable APOC**:
```cypher
SHOW SETTING apoc.trigger.enabled;
SHOW SETTING apoc.import.file.enabled;
```

---

## Python Dependencies

### Requirements.txt

```
# API Clients
requests>=2.31.0
aiohttp>=3.9.0  # Async HTTP
pydantic>=2.5.0  # Data validation

# Neo4j
neo4j>=5.13.0
py2neo>=2021.2.3  # Alternative ORM

# Data Processing
pandas>=2.1.0
numpy>=1.24.0
python-dateutil>=2.8.2

# STIX Support
stix2>=3.1.0
taxii2-client>=2.3.0

# Message Queue
pika>=1.3.0  # RabbitMQ
redis>=5.0.0  # Optional

# Web Framework
flask>=3.0.0
fastapi>=0.104.0  # Alternative
uvicorn>=0.24.0

# Monitoring & Logging
prometheus-client>=0.19.0
python-json-logger>=2.0.7
sentry-sdk>=1.38.0

# Security & Crypto
cryptography>=41.0.0
PyJWT>=2.8.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
responses>=0.24.0  # Mock HTTP

# Development
black>=23.10.0  # Code formatting
flake8>=6.1.0  # Linting
mypy>=1.7.0  # Type checking
pre-commit>=3.5.0
```

**Install**:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Message Queue Setup

### RabbitMQ (Recommended)

**Docker Installation**:
```bash
docker run -d \
  --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=guest \
  -e RABBITMQ_DEFAULT_PASS=guest \
  rabbitmq:3.12-management
```

**Access Management Console**:
- URL: http://localhost:15672
- Username: guest
- Password: guest

**Create Queues**:
```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create main ingestion queue
channel.queue_declare(queue='threat-feed-ingestion', durable=True)

# Create priority queues
channel.queue_declare(queue='threat-feed-critical', durable=True)
channel.queue_declare(queue='threat-feed-high', durable=True)
channel.queue_declare(queue='threat-feed-normal', durable=True)

# Create DLQ (dead letter queue)
channel.queue_declare(queue='threat-feed-dlq', durable=True)

connection.close()
```

### Redis (Optional - for Caching)

**Docker Installation**:
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7.2 redis-server --appendonly yes
```

---

## Logging & Audit Infrastructure

### ELK Stack Setup (Optional)

**Docker Compose**:
```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elastic_data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  elastic_data:
```

**Start**:
```bash
docker-compose up -d
```

---

## Webhook Ingestion Server

### Port Requirements

**Ensure These Ports Are Available**:
- 5000: Flask webhook receiver
- 5001: Backup webhook receiver
- 9090: Prometheus metrics

**Firewall Rules** (Production):
```bash
# Allow internal access only
sudo ufw allow from 10.0.0.0/8 to any port 5000
sudo ufw allow from 10.0.0.0/8 to any port 9090

# OR allow specific IPs
sudo ufw allow from 203.0.113.50 to any port 5000  # VulnCheck
```

---

## Network Prerequisites

### API Connectivity Test

```bash
#!/bin/bash
# test_api_connectivity.sh

echo "Testing VulnCheck..."
curl -I -H "Authorization: Bearer $VULNCHECK_API_KEY" \
  https://api.vulncheck.com/v3/vulnerabilities && echo "✓ VulnCheck OK" || echo "✗ VulnCheck FAILED"

echo "Testing NVD..."
curl -I "https://services.nvd.nist.gov/rest/json/cves/2.0?startIndex=0" && echo "✓ NVD OK" || echo "✗ NVD FAILED"

echo "Testing MITRE..."
curl -I "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack.json" && echo "✓ MITRE OK" || echo "✗ MITRE FAILED"

echo "Testing CISA..."
curl -I "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv" && echo "✓ CISA OK" || echo "✗ CISA FAILED"

echo "Testing Neo4j..."
curl -I -u neo4j:$NEO4J_PASSWORD "http://localhost:7474/db/neo4j/browser/" && echo "✓ Neo4j OK" || echo "✗ Neo4j FAILED"

echo "Testing RabbitMQ..."
curl -I -u guest:guest "http://localhost:15672/api/overview" && echo "✓ RabbitMQ OK" || echo "✗ RabbitMQ FAILED"
```

---

## Knowledge Graph Alignment

### Current Schema Verification

**Verify Existing Level 5 Nodes**:
```cypher
// Count entities by type
MATCH (n:InformationEvent)
RETURN labels(n) as types, count(*) as count
ORDER BY count DESC;

// Verify relationships exist
MATCH (n)-[r]->()
RETURN type(r) as rel_type, count(*) as count
ORDER BY count DESC;

// Check temporal distribution
MATCH (n:InformationEvent)
RETURN date(n.createdAt) as date, count(*) as events
ORDER BY date DESC
LIMIT 30;
```

### Schema Extension Requirements

**New Properties to Add**:
```cypher
# Add real-time feed tracking
ALTER NODE InformationEvent
  ADD PROPERTY sourceApi STRING,
  ADD PROPERTY ingestedAt DATETIME,
  ADD PROPERTY dedupHash STRING,
  ADD PROPERTY rawData STRING;

# Add alert system fields
ALTER NODE Vulnerability
  ADD PROPERTY alertGenerated BOOLEAN DEFAULT false,
  ADD PROPERTY alertLevel STRING,
  ADD PROPERTY lastAlertTime DATETIME;
```

---

## Security Checklist

### Pre-Production Validation

- [ ] All API keys rotated within last 90 days
- [ ] API keys not stored in git/code
- [ ] TLS 1.3 enabled for all connections
- [ ] Neo4j authentication required (not default password)
- [ ] RabbitMQ credentials changed from default
- [ ] Firewall rules restricting API ports
- [ ] Network segmentation (separate VLAN for threat data)
- [ ] Encryption at rest for sensitive data
- [ ] Encryption in transit for all API calls
- [ ] Rate limiting configured on all endpoints
- [ ] CORS properly configured (if applicable)
- [ ] SSL certificate validation enabled
- [ ] Audit logging enabled and tested
- [ ] Incident response playbook prepared

---

## Validation Checklist

**Before proceeding with integration**:

- [ ] All 6 API keys validated and accessible
- [ ] Neo4j instance running with 5,001+ existing nodes
- [ ] Message queue operational (RabbitMQ or Redis)
- [ ] Python environment with all dependencies installed
- [ ] Network connectivity to all external APIs confirmed
- [ ] Database backup taken (pre-ingestion safety)
- [ ] Logging infrastructure operational
- [ ] Webhook receiver server ready
- [ ] Monitoring/metrics collection configured
- [ ] Security review completed
- [ ] Disaster recovery procedures documented

---

## Support & Troubleshooting

### Common Issues

**API Key Errors**:
```
Error: 401 Unauthorized
Solution: Verify API key is valid and not expired
- Check source provider account settings
- Confirm key copied without whitespace
- Verify environment variable is set
```

**Connection Refused (Neo4j)**:
```
Error: ConnectionError: Unable to connect to neo4j://localhost:7687
Solution:
- Verify Neo4j service is running: sudo systemctl status neo4j
- Check default port (7687 for bolt, 7474 for HTTP)
- Verify credentials: NEO4J_USERNAME and NEO4J_PASSWORD
```

**Rate Limit Exceeded**:
```
Error: 429 Too Many Requests
Solution:
- Implement backoff strategy (exponential)
- Reduce request batch size
- Upgrade API tier if available
- Use cached responses where applicable
```

**Message Queue Full**:
```
Error: Queue depth exceeds threshold
Solution:
- Increase consumer threads
- Scale processor horizontally
- Check for blocking operations
- Monitor queue metrics
```

### Support Contacts

- VulnCheck Support: https://vulncheck.com/contact
- NVD Support: nvd@nist.gov
- CISA: cisa@cisa.dhs.gov
- Neo4j Support: https://community.neo4j.com/

---

**Status**: Prerequisites document complete
**Last Updated**: 2025-11-25
**Next Step**: Review TASKMASTER_REALTIME_v1.0.md for implementation details
