# CREDENTIALS QUICK REFERENCE CARD

**File:** CREDENTIALS_QUICK_REFERENCE.md
**Created:** 2025-12-12
**Version:** v1.0.0
**Classification:** INTERNAL USE ONLY

---

## 🚀 QUICK START (Development Environment)

### 1️⃣ Setup Environment Variables
```bash
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed
cp .env.example .env
# Edit .env with your actual values (if needed)
```

### 2️⃣ Start All Services
```bash
docker-compose up -d
```

### 3️⃣ Verify Services
```bash
docker ps
# All containers should be "Up"
```

---

## 📊 SERVICE ENDPOINTS (Development)

| Service | URL | Credentials | Notes |
|---------|-----|-------------|-------|
| **Neo4j Browser** | http://localhost:7474 | neo4j / neo4j@openspg | Graph DB UI |
| **Neo4j Bolt** | bolt://localhost:7687 | neo4j / neo4j@openspg | Direct connection |
| **PostgreSQL** | localhost:5432 | postgres / postgres | DB: aeon_saas_dev |
| **MySQL** | localhost:3306 | root / openspg | DB: openspg |
| **Qdrant API** | http://localhost:6333 | No auth | Vector DB |
| **Qdrant Dashboard** | http://localhost:6333/dashboard | No auth | Vector DB UI |
| **Redis** | localhost:6379 | No auth | Cache |
| **MinIO API** | http://localhost:9000 | minio / minio@openspg | S3-compatible |
| **MinIO Console** | http://localhost:9001 | minio / minio@openspg | Storage UI |
| **OpenSPG Server** | http://localhost:8887 | Via services | KG server |
| **NER11 API** | http://localhost:8000 | No auth | NER API |
| **NER11 Docs** | http://localhost:8000/docs | No auth | Swagger UI |
| **AEON SaaS** | http://localhost:3000 | App-level | Frontend |

---

## 🔌 CONNECTION STRINGS

### Python Examples

**Neo4j:**
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg")
)
```

**PostgreSQL:**
```python
import psycopg2

conn = psycopg2.connect(
    "postgresql://postgres:postgres@localhost:5432/aeon_saas_dev"
)
```

**Qdrant:**
```python
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)
# No authentication required in development
```

**Redis:**
```python
import redis

client = redis.Redis(host="localhost", port=6379, db=0)
# No password required in development
```

**MinIO:**
```python
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minio',
    aws_secret_access_key='minio@openspg'
)
```

---

## 🐳 DOCKER COMMANDS

### Service Management
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart neo4j

# View logs
docker-compose logs -f neo4j

# Check service health
docker-compose ps
```

### Database Access
```bash
# Neo4j Cypher Shell
docker exec -it openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg

# PostgreSQL psql
docker exec -it aeon-postgres-dev psql -U postgres -d aeon_saas_dev

# MySQL shell
docker exec -it openspg-mysql mysql -u root -popenspg openspg

# Redis CLI
docker exec -it openspg-redis redis-cli
```

---

## 🔍 HEALTH CHECKS

### Quick Verification Script
```bash
#!/bin/bash
echo "=== Service Health Check ==="

# Neo4j
echo -n "Neo4j: "
curl -s http://localhost:7474 > /dev/null && echo "✅ OK" || echo "❌ DOWN"

# PostgreSQL
echo -n "PostgreSQL: "
docker exec aeon-postgres-dev pg_isready -U postgres > /dev/null 2>&1 && echo "✅ OK" || echo "❌ DOWN"

# Qdrant
echo -n "Qdrant: "
curl -s http://localhost:6333/health > /dev/null && echo "✅ OK" || echo "❌ DOWN"

# Redis
echo -n "Redis: "
docker exec openspg-redis redis-cli ping > /dev/null 2>&1 && echo "✅ OK" || echo "❌ DOWN"

# MinIO
echo -n "MinIO: "
curl -s http://localhost:9000/minio/health/live > /dev/null && echo "✅ OK" || echo "❌ DOWN"

# NER11 API
echo -n "NER11 API: "
curl -s http://localhost:8000/health > /dev/null && echo "✅ OK" || echo "❌ DOWN"

# AEON SaaS
echo -n "AEON SaaS: "
curl -s http://localhost:3000 > /dev/null && echo "✅ OK" || echo "❌ DOWN"
```

---

## ⚠️ TROUBLESHOOTING

### Service Won't Start
```bash
# Check logs
docker-compose logs <service_name>

# Check port conflicts
sudo lsof -i :<port_number>

# Restart Docker
sudo systemctl restart docker
```

### Database Connection Errors
```bash
# Verify credentials
docker exec <container_name> env | grep -i password

# Check network
docker network inspect aeon-network

# Reset database (CAUTION: Destroys data)
docker-compose down -v
docker-compose up -d
```

### Cannot Access Web UI
```bash
# Check if port is exposed
docker ps | grep <service_name>

# Check firewall
sudo ufw status

# Try localhost vs 127.0.0.1
curl http://127.0.0.1:<port>
```

---

## 🛡️ SECURITY REMINDERS

### ⛔ NEVER DO THIS:
- Commit .env file to Git
- Use development passwords in production
- Expose database ports to the internet
- Share credentials in Slack/email
- Hardcode passwords in code

### ✅ ALWAYS DO THIS:
- Use .env for local configuration
- Rotate credentials every 90 days
- Use strong passwords in production
- Enable authentication on all services
- Review .gitignore before committing

---

## 📚 FULL DOCUMENTATION

For complete details, see:
- **docs/CREDENTIALS_AND_SECRETS_GUIDE.md** - Full security guide
- **.env.example** - Environment variable template
- **.gitignore** - Files excluded from version control

---

## 🆘 EMERGENCY CONTACTS

**Security Issue?** → security@example.com
**System Down?** → ops@example.com
**Questions?** → dev-team@example.com

---

**Last Updated:** 2025-12-12
**Review Credentials Guide for production deployment requirements**
