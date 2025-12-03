# NER11 Gold Standard - Container Infrastructure Guide

**File**: 01_NER11_CONTAINER_INFRASTRUCTURE_v1.0_2025-12-03.md
**Created**: 2025-12-03 00:00:00 UTC
**Modified**: 2025-12-03 00:00:00 UTC
**Version**: v1.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete infrastructure documentation for NER11 containerized deployment
**Status**: ACTIVE

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           NER11 GOLD STANDARD - CONTAINER INFRASTRUCTURE                     ║
║                                                                              ║
║   ┌─────────────────────────────────────────────────────────────────────┐   ║
║   │                      PRODUCTION ARCHITECTURE                         │   ║
║   │                                                                      │   ║
║   │    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    │   ║
║   │    │ NER11    │    │ Qdrant   │    │ Neo4j    │    │ Frontend │    │   ║
║   │    │ API      │◄───│ Vectors  │◄───│ Graph    │◄───│ App      │    │   ║
║   │    │ :8000    │    │ :6333    │    │ :7687    │    │ :3000    │    │   ║
║   │    └──────────┘    └──────────┘    └──────────┘    └──────────┘    │   ║
║   │                                                                      │   ║
║   └─────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. Infrastructure Overview

### 1.1 Container Stack

| Container | Image | Port | Purpose | Status |
|-----------|-------|------|---------|--------|
| NER11 API | Python 3.11 + spaCy | 8000 | Entity extraction, search | PRODUCTION |
| Qdrant | qdrant/qdrant:latest | 6333, 6334 | Vector database | PRODUCTION |
| Neo4j | neo4j:5.x | 7687, 7474 | Graph database | PRODUCTION |
| Frontend | Node.js 18 | 3000 | Web UI | DEVELOPMENT |

### 1.2 Network Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              HOST NETWORK                                    │
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                        aeon-network (bridge)                          │  │
│   │                                                                       │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│   │  │   ner11     │  │   qdrant    │  │   neo4j     │  │  frontend   │ │  │
│   │  │             │  │             │  │             │  │             │ │  │
│   │  │ 0.0.0.0:8000│  │ 0.0.0.0:6333│  │ 0.0.0.0:7687│  │ 0.0.0.0:3000│ │  │
│   │  │             │  │ 0.0.0.0:6334│  │ 0.0.0.0:7474│  │             │ │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│   │                                                                       │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Docker Compose Configuration

### 2.1 Production docker-compose.yml

```yaml
# docker-compose.yml
# NER11 Gold Standard Production Stack
# Version: 1.0.0

version: '3.8'

services:
  # ============================================
  # NER11 API Service
  # ============================================
  ner11-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ner11-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=models/ner11_v3/model-best
      - FALLBACK_MODEL=en_core_web_trf
      - USE_FALLBACK_NER=true
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD:-neo4j@openspg}
      - QDRANT_HOST=qdrant
      - QDRANT_PORT=6333
      - QDRANT_COLLECTION=ner11_entities_hierarchical
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models:ro
      - ./logs:/app/logs
    depends_on:
      neo4j:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    networks:
      - aeon-network
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G

  # ============================================
  # Qdrant Vector Database
  # ============================================
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
      - qdrant_snapshots:/qdrant/snapshots
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__SERVICE__HTTP_PORT=6333
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - aeon-network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  # ============================================
  # Neo4j Graph Database
  # ============================================
  neo4j:
    image: neo4j:5.15.0
    container_name: openspg-neo4j
    restart: unless-stopped
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD:-neo4j@openspg}
      - NEO4J_PLUGINS=["apoc"]
      - NEO4J_dbms_memory_pagecache_size=2G
      - NEO4J_dbms_memory_heap_initial__size=1G
      - NEO4J_dbms_memory_heap_max__size=2G
      - NEO4J_dbms_security_procedures_unrestricted=apoc.*
      - NEO4J_dbms_security_procedures_allowlist=apoc.*
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
      - neo4j_import:/var/lib/neo4j/import
      - neo4j_plugins:/plugins
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7474"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 90s
    networks:
      - aeon-network
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 6G
        reservations:
          cpus: '2'
          memory: 4G

networks:
  aeon-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16

volumes:
  qdrant_data:
    driver: local
  qdrant_snapshots:
    driver: local
  neo4j_data:
    driver: local
  neo4j_logs:
    driver: local
  neo4j_import:
    driver: local
  neo4j_plugins:
    driver: local
```

### 2.2 Dockerfile for NER11 API

```dockerfile
# Dockerfile
# NER11 Gold Standard API Container
# Version: 1.0.0

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_trf

# Copy application code
COPY serve_model.py .
COPY utils/ ./utils/
COPY pipelines/ ./pipelines/

# Create logs directory
RUN mkdir -p /app/logs

# Create non-root user
RUN useradd -m -u 1000 ner11user && \
    chown -R ner11user:ner11user /app

USER ner11user

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "serve_model:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.3 Requirements File

```text
# requirements.txt
# NER11 Gold Standard Dependencies
# Version: 1.0.0

# Core Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0

# NLP
spacy>=3.7.2
spacy-transformers>=1.3.0
torch>=2.0.0

# Vector Database
qdrant-client>=1.6.0
sentence-transformers>=2.2.0

# Graph Database
neo4j>=5.14.0

# Utilities
python-dotenv>=1.0.0
httpx>=0.25.0
requests>=2.31.0

# Monitoring
prometheus-client>=0.19.0

# Development (optional)
pytest>=7.4.0
black>=23.11.0
isort>=5.12.0
```

---

## 3. Deployment Procedures

### 3.1 Initial Deployment

```bash
#!/bin/bash
# deploy.sh - Initial deployment script

set -e

echo "=== NER11 Gold Standard Deployment ==="
echo "Date: $(date)"

# 1. Create required directories
echo "1. Creating directories..."
mkdir -p models logs

# 2. Copy model files (if not already present)
if [ ! -d "models/ner11_v3" ]; then
    echo "ERROR: Model files not found at models/ner11_v3"
    echo "Please copy the model files before deployment"
    exit 1
fi

# 3. Verify model checksums
echo "2. Verifying model checksums..."
META_CHECKSUM=$(md5sum models/ner11_v3/model-best/meta.json | awk '{print $1}')
NER_CHECKSUM=$(md5sum models/ner11_v3/model-best/ner/model | awk '{print $1}')

if [ "$META_CHECKSUM" != "0710e14d78a87d54866208cc6a5c8de3" ]; then
    echo "ERROR: meta.json checksum mismatch!"
    exit 1
fi

if [ "$NER_CHECKSUM" != "f326672a81a00c54be06422aae07ecf1" ]; then
    echo "ERROR: ner/model checksum mismatch!"
    exit 1
fi

echo "   Checksums verified!"

# 4. Set environment variables
echo "3. Setting environment variables..."
export NEO4J_PASSWORD="${NEO4J_PASSWORD:-neo4j@openspg}"

# 5. Build and start containers
echo "4. Building containers..."
docker-compose build

echo "5. Starting services..."
docker-compose up -d

# 6. Wait for services to be healthy
echo "6. Waiting for services to be healthy..."
sleep 30

# Check Neo4j
echo "   Checking Neo4j..."
until docker exec openspg-neo4j cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "RETURN 1" 2>/dev/null; do
    echo "   Waiting for Neo4j..."
    sleep 5
done
echo "   Neo4j: OK"

# Check Qdrant
echo "   Checking Qdrant..."
until curl -s http://localhost:6333/health > /dev/null 2>&1; do
    echo "   Waiting for Qdrant..."
    sleep 5
done
echo "   Qdrant: OK"

# Check NER11 API
echo "   Checking NER11 API..."
until curl -s http://localhost:8000/health > /dev/null 2>&1; do
    echo "   Waiting for NER11 API..."
    sleep 5
done
echo "   NER11 API: OK"

# 7. Verify deployment
echo "7. Verifying deployment..."
HEALTH=$(curl -s http://localhost:8000/health)
STATUS=$(echo $HEALTH | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

if [ "$STATUS" = "healthy" ]; then
    echo "=== Deployment Successful ==="
    echo "NER11 API: http://localhost:8000"
    echo "Neo4j Browser: http://localhost:7474"
    echo "Qdrant Dashboard: http://localhost:6333/dashboard"
else
    echo "=== Deployment Warning ==="
    echo "API status: $STATUS"
    echo "Full health: $HEALTH"
fi
```

### 3.2 Update Deployment

```bash
#!/bin/bash
# update.sh - Update deployment with new model or code

set -e

echo "=== NER11 Update Deployment ==="

# 1. Pull latest changes (if using git)
# git pull origin main

# 2. Stop API container only
echo "1. Stopping API container..."
docker-compose stop ner11-api

# 3. Rebuild API container
echo "2. Rebuilding API container..."
docker-compose build ner11-api

# 4. Start API container
echo "3. Starting API container..."
docker-compose up -d ner11-api

# 5. Verify health
echo "4. Waiting for API to be healthy..."
sleep 30
curl http://localhost:8000/health | python3 -m json.tool

echo "=== Update Complete ==="
```

### 3.3 Rollback Procedure

```bash
#!/bin/bash
# rollback.sh - Rollback to previous version

set -e

BACKUP_TAG="${1:-previous}"

echo "=== NER11 Rollback to $BACKUP_TAG ==="

# 1. Stop current deployment
echo "1. Stopping current deployment..."
docker-compose down

# 2. Restore model from backup
echo "2. Restoring model from backup..."
BACKUP_DIR="/mnt/d/1_Apps_to_Build/AEON_Cyber_Digital_Twin_backups"
LATEST_BACKUP=$(ls -td ${BACKUP_DIR}/ner11_v3_* | head -1)

rm -rf models/ner11_v3
cp -r "${LATEST_BACKUP}/ner11_v3" models/

# 3. Verify checksums
echo "3. Verifying restored model..."
META_CHECKSUM=$(md5sum models/ner11_v3/model-best/meta.json | awk '{print $1}')
if [ "$META_CHECKSUM" != "0710e14d78a87d54866208cc6a5c8de3" ]; then
    echo "ERROR: Restored model checksum mismatch!"
    exit 1
fi

# 4. Restart deployment
echo "4. Starting deployment..."
docker-compose up -d

# 5. Verify health
echo "5. Verifying health..."
sleep 30
curl http://localhost:8000/health

echo "=== Rollback Complete ==="
```

---

## 4. Container Management

### 4.1 Container Operations

```bash
# Start all containers
docker-compose up -d

# Stop all containers
docker-compose down

# View container status
docker-compose ps

# View logs
docker-compose logs -f ner11-api
docker-compose logs -f qdrant
docker-compose logs -f neo4j

# Restart specific container
docker-compose restart ner11-api

# Scale API (for load testing)
docker-compose up -d --scale ner11-api=3
```

### 4.2 Container Health Monitoring

```bash
#!/bin/bash
# container_health.sh

echo "=== Container Health Check ==="
echo "Timestamp: $(date)"
echo ""

# Check container status
echo "Container Status:"
docker-compose ps
echo ""

# Check NER11 API
echo "NER11 API Health:"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""

# Check Qdrant
echo "Qdrant Health:"
curl -s http://localhost:6333/health
echo ""

# Check Neo4j
echo "Neo4j Health:"
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1"
echo ""

# Resource usage
echo "Resource Usage:"
docker stats --no-stream
```

### 4.3 Volume Management

```bash
# List volumes
docker volume ls | grep -E "qdrant|neo4j"

# Inspect volume
docker volume inspect ner11_qdrant_data

# Backup Qdrant volume
docker run --rm -v ner11_qdrant_data:/data -v $(pwd):/backup alpine \
    tar cvf /backup/qdrant_backup.tar /data

# Restore Qdrant volume
docker run --rm -v ner11_qdrant_data:/data -v $(pwd):/backup alpine \
    tar xvf /backup/qdrant_backup.tar -C /

# Clean up unused volumes (CAUTION)
docker volume prune
```

---

## 5. Environment Configuration

### 5.1 Environment Variables Reference

```bash
# .env file template
# Copy to .env and customize

# ===========================================
# NER11 API Configuration
# ===========================================
MODEL_PATH=models/ner11_v3/model-best
FALLBACK_MODEL=en_core_web_trf
USE_FALLBACK_NER=true
NER_API_URL=http://localhost:8000
LOG_LEVEL=INFO

# ===========================================
# Neo4j Configuration
# ===========================================
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg

# ===========================================
# Qdrant Configuration
# ===========================================
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=ner11_entities_hierarchical

# ===========================================
# Resource Limits
# ===========================================
API_CPU_LIMIT=4
API_MEMORY_LIMIT=8g
QDRANT_CPU_LIMIT=2
QDRANT_MEMORY_LIMIT=4g
NEO4J_CPU_LIMIT=4
NEO4J_MEMORY_LIMIT=6g
```

### 5.2 Production vs Development Configuration

```yaml
# docker-compose.override.yml (Development)
version: '3.8'

services:
  ner11-api:
    volumes:
      - ./serve_model.py:/app/serve_model.py:ro
      - ./utils:/app/utils:ro
      - ./pipelines:/app/pipelines:ro
    command: ["uvicorn", "serve_model:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    environment:
      - LOG_LEVEL=DEBUG

  neo4j:
    environment:
      - NEO4J_dbms_memory_pagecache_size=512M
      - NEO4J_dbms_memory_heap_initial__size=512M
      - NEO4J_dbms_memory_heap_max__size=1G
```

---

## 6. Networking Configuration

### 6.1 Network Setup

```bash
# Create custom network (if not using docker-compose)
docker network create --driver bridge --subnet 172.28.0.0/16 aeon-network

# List networks
docker network ls

# Inspect network
docker network inspect aeon-network

# Connect container to network
docker network connect aeon-network ner11-api
```

### 6.2 Port Mappings

| Service | Container Port | Host Port | Protocol | Access |
|---------|---------------|-----------|----------|--------|
| NER11 API | 8000 | 8000 | HTTP | External |
| Qdrant REST | 6333 | 6333 | HTTP | External |
| Qdrant gRPC | 6334 | 6334 | gRPC | Internal |
| Neo4j Bolt | 7687 | 7687 | Bolt | External |
| Neo4j HTTP | 7474 | 7474 | HTTP | External |

### 6.3 Firewall Configuration

```bash
# Allow NER11 API
sudo ufw allow 8000/tcp comment 'NER11 API'

# Allow Neo4j (production - restrict to specific IPs)
sudo ufw allow from 192.168.1.0/24 to any port 7687 comment 'Neo4j Bolt'
sudo ufw allow from 192.168.1.0/24 to any port 7474 comment 'Neo4j Browser'

# Allow Qdrant (production - restrict to specific IPs)
sudo ufw allow from 192.168.1.0/24 to any port 6333 comment 'Qdrant REST'
```

---

## 7. Monitoring and Logging

### 7.1 Container Logs

```bash
# View real-time logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f ner11-api

# View last 100 lines
docker-compose logs --tail 100 ner11-api

# Export logs to file
docker-compose logs ner11-api > logs/ner11_$(date +%Y%m%d).log
```

### 7.2 Prometheus Metrics (Optional)

```yaml
# Add to docker-compose.yml
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - aeon-network
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ner11-api'
    static_configs:
      - targets: ['ner11-api:8000']
    metrics_path: '/metrics'
```

### 7.3 Health Check Dashboard Script

```bash
#!/bin/bash
# dashboard.sh - Simple health dashboard

watch -n 5 '
echo "=== NER11 Infrastructure Dashboard ==="
echo "Time: $(date)"
echo ""
echo "Container Status:"
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "NER11 API:"
curl -s http://localhost:8000/health | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"  Status: {d[\"status\"]}  |  Model: {d[\"model_checksum\"]}  |  Version: {d[\"version\"]}\")
" 2>/dev/null || echo "  Status: UNAVAILABLE"
echo ""
echo "Qdrant:"
curl -s http://localhost:6333/collections/ner11_entities_hierarchical | python3 -c "
import sys, json
d = json.load(sys.stdin)
r = d.get(\"result\", {})
print(f\"  Entities: {r.get(\"points_count\", 0):,}  |  Status: {d.get(\"status\")}\")
" 2>/dev/null || echo "  Status: UNAVAILABLE"
echo ""
echo "Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
'
```

---

## 8. Security Configuration

### 8.1 Container Security

```yaml
# Security-hardened docker-compose additions
services:
  ner11-api:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### 8.2 Network Security

```bash
# Create internal-only network for service communication
docker network create --internal aeon-internal

# Expose only necessary services externally
# NER11 API: exposed
# Neo4j/Qdrant: internal only (accessed via API)
```

### 8.3 Secrets Management

```yaml
# docker-compose.yml with secrets
secrets:
  neo4j_password:
    file: ./secrets/neo4j_password.txt

services:
  neo4j:
    secrets:
      - neo4j_password
    environment:
      - NEO4J_AUTH=neo4j/$(cat /run/secrets/neo4j_password)
```

---

## 9. Troubleshooting

### 9.1 Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| API won't start | Container exits immediately | Check logs: `docker-compose logs ner11-api` |
| Model not loading | "not_loaded" in health check | Verify volume mount and model path |
| Neo4j connection failed | "not_connected" | Check Neo4j container health |
| Qdrant unavailable | "not_available" | Check Qdrant container health |
| Out of memory | Container killed | Increase memory limits |

### 9.2 Debug Commands

```bash
# Enter container shell
docker exec -it ner11-api /bin/bash

# Check Python environment
docker exec ner11-api python -c "import spacy; print(spacy.__version__)"

# Check model loading
docker exec ner11-api python -c "
import spacy
nlp = spacy.load('/app/models/ner11_v3/model-best')
print('Model loaded:', nlp.pipe_names)
"

# Check network connectivity
docker exec ner11-api curl -v http://qdrant:6333/health
docker exec ner11-api curl -v http://neo4j:7474
```

### 9.3 Recovery Procedures

```bash
# Reset Qdrant collection
docker exec ner11-api python -c "
from qdrant_client import QdrantClient
client = QdrantClient(host='qdrant', port=6333)
client.recreate_collection(
    collection_name='ner11_entities_hierarchical',
    vectors_config={'size': 384, 'distance': 'Cosine'}
)
print('Collection recreated')
"

# Reset Neo4j (CAUTION - deletes all data)
docker-compose down
docker volume rm ner11_neo4j_data
docker-compose up -d neo4j
```

---

## 10. Related Documentation

| Document | Path | Description |
|----------|------|-------------|
| Architecture | `01_ARCHITECTURE/08_NER11_GOLD_MODEL_ARCHITECTURE_v1.0_2025-12-03.md` | System architecture |
| Specification | `03_SPECIFICATIONS/09_NER11_GOLD_MODEL_SPECIFICATION_v1.0_2025-12-03.md` | Model specifications |
| Procedures | `13_Procedures/01_NER11_OPERATIONS_PROCEDURES_v1.0_2025-12-03.md` | Operational procedures |
| Data Flow | `01_ARCHITECTURE/07_DATA_FLOW_ARCHITECTURE_v4.0_2025-12-02.md` | Data flow architecture |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2025-12-03 | Initial comprehensive infrastructure documentation |

---

**Document End**
