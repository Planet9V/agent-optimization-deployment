# IEC 62443 Workshop App – Docker Deployment & Architecture Guide

**Version:** 1.0  
**Status:** Production Ready  
**Date:** December 2024  
**Audience:** DevOps, SREs, Deployment Engineers  

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [System Requirements](#system-requirements)
3. [Docker Compose Configuration](#docker-compose-configuration)
4. [Environment Setup](#environment-setup)
5. [Deployment Instructions](#deployment-instructions)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Database Migrations](#database-migrations)
8. [Pre-ingestion of Vector Collections](#pre-ingestion-of-vector-collections)
9. [Monitoring & Health Checks](#monitoring--health-checks)
10. [Backup & Recovery](#backup--recovery)
11. [Scaling & Performance Tuning](#scaling--performance-tuning)
12. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### Service Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Internet / Client                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Nginx (Reverse Proxy)                      │
│              Port 80 (HTTP) + 443 (HTTPS/TLS)                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                   Next.js Frontend + API Server                  │
│                        Port 3000 (internal)                      │
│  - React UI (HARA, Threat Canvas, Admin)                        │
│  - Express/Next.js API routes (/api/*)                          │
│  - JWT authentication middleware                                 │
│  - Ingestion job queue and processing                            │
│  - AI query orchestration                                        │
└──────────────────────────────────────────────────────────────────┘
         ↓                        ↓                         ↓
┌───────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   Postgres 15     │  │   Neo4j 5.x      │  │  Qdrant 1.7.x    │
│   Port 5432       │  │   Port 7687      │  │   Port 6333      │
│  (System Record)  │  │ (Graph Engine)   │  │ (Vector Store)   │
│                   │  │                  │  │                  │
│  Tables:          │  │  Nodes:          │  │  Collections:    │
│  - projects       │  │  - Project       │  │  - iec62443_std  │
│  - phases         │  │  - Zone          │  │  - mitre_ics     │
│  - hara_items     │  │  - Asset         │  │  - project_docs  │
│  - documents      │  │  - Threat        │  │                  │
│  - graph_nodes    │  │  - Conduit       │  │  Vectors:        │
│  - graph_edges    │  │  - Document      │  │  768-dim (large) │
│  - audit_log      │  │                  │  │                  │
│  - config         │  │  ~100k vectors   │  │  ~50k vectors    │
└───────────────────┘  └──────────────────┘  └──────────────────┘
         ↓                        ↓                         ↓
┌───────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Volume:          │  │  Volume:         │  │  Volume:         │
│  postgres_data    │  │  neo4j_data      │  │  qdrant_data     │
│  (100 GB)         │  │  (50 GB)         │  │  (100 GB)        │
└───────────────────┘  └──────────────────┘  └──────────────────┘

External Services (API calls):
- OpenRouter (LLM: Claude, GPT, Llama)
- S3 or Object Storage (document archival, optional)
```

### Data Flow

1. **User Action (Browser)** → HTTPS → Nginx → Next.js API
2. **API Query** → Postgres (system of record) + Neo4j (graph query) + Qdrant (semantic search)
3. **Document Upload** → Postgres (store file) → spaCy NER (async) → Qdrant + Neo4j (ingest)
4. **AI Query** → Qdrant (search) + Neo4j (context) + OpenRouter (LLM) → Response
5. **Audit Log** → Postgres (immutable)

---

## System Requirements

### Minimum Hardware (Single-machine deployment)

| Component | Requirement | Rationale |
|-----------|-------------|-----------|
| **CPU** | 4 cores (Intel/AMD) | Next.js (2 cores) + Neo4j (1–2 cores) + Qdrant (shared) |
| **RAM** | 16 GB | Postgres (2 GB), Neo4j (4 GB), Qdrant (4 GB), Next.js (2 GB), overhead |
| **Storage** | 300 GB (SSD preferred) | Postgres (50 GB) + Neo4j (50 GB) + Qdrant (100 GB) + documents (100 GB) |
| **Network** | 1 Gbps | Sufficient for single-user/single-project |

### Recommended Hardware (Production)

| Component | Requirement | Rationale |
|-----------|-------------|-----------|
| **CPU** | 8 cores | Sustained load + background ingestion jobs |
| **RAM** | 32 GB | Larger buffer pools, concurrent connections |
| **Storage** | 500 GB (SSD) | Room for scaling to multiple projects |
| **Network** | 10 Gbps | File uploads, API latency headroom |

### Software Prerequisites

- **Docker:** 20.10+ (with Docker Compose 2.0+)
- **Docker Compose:** v2.0+ (YAML 3.8 format)
- **OS:** Linux (Ubuntu 20.04+ recommended), macOS (Intel/Apple Silicon with Rosetta), Windows 11 WSL2
- **Git:** For cloning repository

### Ports Required (Ingress)

| Port | Service | Protocol | Public | Notes |
|------|---------|----------|--------|-------|
| **80** | Nginx HTTP | HTTP | Yes | Redirect to HTTPS (or disable in dev) |
| **443** | Nginx HTTPS | HTTPS | Yes | TLS terminated here |
| **3000** | Next.js | HTTP | No | Internal only; proxied via Nginx |
| **5432** | Postgres | TCP | No | Internal; no external access |
| **7687** | Neo4j Bolt | TCP | No | Internal; no external access |
| **6333** | Qdrant REST | HTTP | No | Internal; no external access |

---

## Docker Compose Configuration

### File: `docker-compose.yml`

```yaml
version: '3.8'

services:
  # ============================================
  # Reverse Proxy (Nginx)
  # ============================================
  nginx:
    image: nginx:1.25-alpine
    container_name: iec62443-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro  # TLS certificates
    depends_on:
      - app
    networks:
      - iec62443-network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  # ============================================
  # Next.js Application Server
  # ============================================
  app:
    image: iec62443-app:latest  # Build locally or push to registry
    build:
      context: ./app
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    container_name: iec62443-app
    restart: unless-stopped
    ports:
      - "3000:3000"  # Internal only; exposed via Nginx
    environment:
      # Application
      NODE_ENV: production
      NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL:-https://localhost}
      NEXT_PUBLIC_APP_NAME: "IEC 62443 Workshop"
      LOG_LEVEL: ${LOG_LEVEL:-info}
      
      # Database
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_DB: ${POSTGRES_DB:-iec62443}
      POSTGRES_USER: ${POSTGRES_USER:-iec62443_app}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      
      # Neo4j
      NEO4J_HOST: neo4j
      NEO4J_PORT: 7687
      NEO4J_USER: ${NEO4J_USER:-neo4j}
      NEO4J_PASSWORD: ${NEO4J_PASSWORD}
      NEO4J_SCHEME: bolt  # or neo4j+s for TLS
      
      # Qdrant
      QDRANT_URL: http://qdrant:6333
      QDRANT_API_KEY: ${QDRANT_API_KEY:-}
      
      # LLM / OpenRouter
      OPENROUTER_API_KEY: ${OPENROUTER_API_KEY}
      OPENROUTER_API_URL: https://openrouter.ai/api/v1
      LLM_MODEL_CHAT: ${LLM_MODEL_CHAT:-meta-llama/llama-3-70b-instruct}
      LLM_MODEL_EMBEDDING: ${LLM_MODEL_EMBEDDING:-openai/text-embedding-3-large}
      LLM_MODEL_THREAT_ELICIT: ${LLM_MODEL_THREAT_ELICIT:-anthropic/claude-3-opus}
      LLM_MODEL_SUMMARY: ${LLM_MODEL_SUMMARY:-openai/gpt-4}
      
      # Auth
      JWT_SECRET: ${JWT_SECRET}
      JWT_EXPIRATION: 86400  # 24 hours
      ADMIN_USERNAME: ${ADMIN_USERNAME:-admin}
      ADMIN_PASSWORD_HASH: ${ADMIN_PASSWORD_HASH}  # bcrypt hash
      
      # Redis (optional, for caching/queue)
      REDIS_URL: ${REDIS_URL:-redis://redis:6379}
      
      # Ingestion
      SPACY_MODEL: en_core_web_lg  # Pre-loaded in Docker image
      MAX_UPLOAD_SIZE_MB: 50
      INGEST_BATCH_SIZE: 100
      INGEST_TIMEOUT_SECONDS: 300
    
    volumes:
      - ./app/src:/app/src:ro  # Code (read-only in production)
      - app-cache:/app/.next/cache  # Next.js build cache
      - app-logs:/app/logs  # Application logs
    depends_on:
      postgres:
        condition: service_healthy
      neo4j:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    networks:
      - iec62443-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s

  # ============================================
  # PostgreSQL (System of Record)
  # ============================================
  postgres:
    image: postgres:15-alpine
    container_name: iec62443-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-iec62443}
      POSTGRES_USER: ${POSTGRES_USER:-iec62443_app}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"
      POSTGRES_HOST_AUTH_METHOD: "scram-sha-256"
    
    ports:
      - "5432:5432"  # Internal only; exposed for debugging via SSH tunnel
    
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-postgres.sql:/docker-entrypoint-initdb.d/01-init.sql:ro
      - ./migrations:/migrations:ro
    
    networks:
      - iec62443-network
    
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-iec62443_app}"]
      interval: 10s
      timeout: 5s
      retries: 5
    
    shm_size: '256mb'  # Increase shared memory for better performance

  # ============================================
  # Neo4j (Graph Database)
  # ============================================
  neo4j:
    image: neo4j:5.13-community
    container_name: iec62443-neo4j
    restart: unless-stopped
    environment:
      NEO4J_AUTH: ${NEO4J_USER:-neo4j}/${NEO4J_PASSWORD}
      NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
      
      # Performance tuning
      NEO4J_server_memory_heap_initial__size: 2G
      NEO4J_server_memory_heap_max__size: 4G
      NEO4J_server_memory_pagecache_size: 2G
      
      # Logging
      NEO4J_dbms_logs_query_enabled: "true"
      NEO4J_dbms_logs_query_threshold: 1000ms  # Log slow queries
    
    ports:
      - "7687:7687"    # Bolt protocol (internal)
      - "7474:7474"    # HTTP (internal; for Neo4j Browser)
    
    volumes:
      - neo4j_data:/var/lib/neo4j/data
      - neo4j_logs:/var/lib/neo4j/logs
      - ./neo4j-init.cypher:/var/lib/neo4j/init.cypher:ro
    
    networks:
      - iec62443-network
    
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "${NEO4J_USER:-neo4j}", "-p", "${NEO4J_PASSWORD}", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ============================================
  # Qdrant (Vector Database)
  # ============================================
  qdrant:
    image: qdrant/qdrant:v1.7.0
    container_name: iec62443-qdrant
    restart: unless-stopped
    environment:
      QDRANT_API_KEY: ${QDRANT_API_KEY}
      QDRANT_LOG_LEVEL: info
    
    ports:
      - "6333:6333"    # REST API (internal)
      - "6334:6334"    # gRPC (internal, optional)
    
    volumes:
      - qdrant_data:/qdrant/storage
      - ./qdrant_config.yaml:/qdrant/config/production.yaml:ro
    
    networks:
      - iec62443-network
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ============================================
  # Redis (Caching & Job Queue, Optional)
  # ============================================
  redis:
    image: redis:7-alpine
    container_name: iec62443-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"  # Internal only
    volumes:
      - redis_data:/data
    networks:
      - iec62443-network
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    profiles:
      - with-cache  # Optional service; activate with: docker-compose --profile with-cache up

# ============================================
# Networks
# ============================================
networks:
  iec62443-network:
    driver: bridge

# ============================================
# Volumes
# ============================================
volumes:
  postgres_data:
    driver: local
  neo4j_data:
    driver: local
  neo4j_logs:
    driver: local
  qdrant_data:
    driver: local
  redis_data:
    driver: local
  app-cache:
    driver: local
  app-logs:
    driver: local
```

---

## Environment Setup

### File: `.env.example`

Copy to `.env` and fill in actual values:

```bash
# ============================================
# Application
# ============================================
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://workshop.example.com
LOG_LEVEL=info

# ============================================
# PostgreSQL
# ============================================
POSTGRES_DB=iec62443
POSTGRES_USER=iec62443_app
POSTGRES_PASSWORD=<GENERATE_STRONG_PASSWORD>

# ============================================
# Neo4j
# ============================================
NEO4J_USER=neo4j
NEO4J_PASSWORD=<GENERATE_STRONG_PASSWORD>

# ============================================
# Qdrant
# ============================================
QDRANT_API_KEY=<GENERATE_STRONG_API_KEY>

# ============================================
# Redis (optional)
# ============================================
REDIS_PASSWORD=<GENERATE_STRONG_PASSWORD>

# ============================================
# Authentication
# ============================================
JWT_SECRET=<GENERATE_LONG_RANDOM_STRING>

# Admin credentials (initial)
# Username: admin
# Password hash: bcrypt(password) - generate with: node -e "const bcrypt = require('bcrypt'); console.log(bcrypt.hashSync('PASSWORD', 10))"
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=$2b$10$...

# ============================================
# OpenRouter (LLM)
# ============================================
OPENROUTER_API_KEY=<YOUR_OPENROUTER_API_KEY>

# Model selections (can be changed in admin panel)
LLM_MODEL_CHAT=meta-llama/llama-3-70b-instruct
LLM_MODEL_EMBEDDING=openai/text-embedding-3-large
LLM_MODEL_THREAT_ELICIT=anthropic/claude-3-opus
LLM_MODEL_SUMMARY=openai/gpt-4

# ============================================
# Feature Flags (optional)
# ============================================
FEATURE_COLLABORATIVE_SESSIONS=true
FEATURE_AI_THREAT_SUGGESTIONS=true
FEATURE_DOCUMENT_INGESTION=true
```

### Generate Secrets

```bash
#!/bin/bash
# generate-secrets.sh

echo "=== IEC 62443 Workshop – Secret Generation ==="

# Generate strong passwords
POSTGRES_PASSWORD=$(openssl rand -base64 32)
NEO4J_PASSWORD=$(openssl rand -base64 32)
QDRANT_API_KEY=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -base64 64)

# Generate bcrypt hash for admin password
read -p "Enter desired admin password: " ADMIN_PASSWORD
ADMIN_PASSWORD_HASH=$(node -e "const bcrypt = require('bcrypt'); console.log(bcrypt.hashSync('$ADMIN_PASSWORD', 10))")

echo ""
echo "Add these to .env:"
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD"
echo "NEO4J_PASSWORD=$NEO4J_PASSWORD"
echo "QDRANT_API_KEY=$QDRANT_API_KEY"
echo "REDIS_PASSWORD=$REDIS_PASSWORD"
echo "JWT_SECRET=$JWT_SECRET"
echo "ADMIN_PASSWORD_HASH=$ADMIN_PASSWORD_HASH"

# Optionally save to .env
read -p "Save to .env? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  cat >> .env << EOF

# Generated on $(date)
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
NEO4J_PASSWORD=$NEO4J_PASSWORD
QDRANT_API_KEY=$QDRANT_API_KEY
REDIS_PASSWORD=$REDIS_PASSWORD
JWT_SECRET=$JWT_SECRET
ADMIN_PASSWORD_HASH=$ADMIN_PASSWORD_HASH
EOF
  echo ".env updated"
fi
```

---

## Deployment Instructions

### Step 1: Clone Repository & Prepare

```bash
# Clone repo
git clone https://github.com/your-org/iec62443-workshop.git
cd iec62443-workshop

# Copy environment template
cp .env.example .env

# Generate secrets
bash generate-secrets.sh

# Review and edit .env
nano .env

# Verify configuration
cat .env | grep -E "^[A-Z_]+=" | head -20
```

### Step 2: Prepare SSL/TLS Certificates

For **development**:
```bash
# Generate self-signed cert (valid for 365 days)
mkdir -p certs
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

For **production**:
```bash
# Use Let's Encrypt or your certificate authority
# Place cert.pem and key.pem in ./certs/
# Update nginx.conf with correct paths
```

### Step 3: Build Application Image

```bash
# Build Next.js Docker image
docker build -t iec62443-app:latest ./app

# Or use pre-built image from registry:
# docker pull your-registry/iec62443-app:latest
```

### Step 4: Start Services

```bash
# Bring up all services
docker-compose up -d

# Monitor startup (first ~2 minutes are initialization)
docker-compose logs -f app

# Verify all services are healthy
docker-compose ps

# Expected output:
# NAME                 STATUS         PORTS
# iec62443-nginx       Up (healthy)   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
# iec62443-app         Up (healthy)   3000/tcp
# iec62443-postgres    Up (healthy)   5432/tcp
# iec62443-neo4j       Up (healthy)   7474/tcp, 7687/tcp
# iec62443-qdrant      Up (healthy)   6333/tcp, 6334/tcp
# iec62443-redis       Up (healthy)   6379/tcp
```

### Step 5: Initialize Databases

```bash
# Postgres migrations
docker-compose exec app npm run migrate:latest

# Neo4j initialization (run Cypher script)
docker-compose exec neo4j cypher-shell -u neo4j -p <NEO4J_PASSWORD> << 'EOF'
// Create indexes for performance
CREATE INDEX FOR (p:Project) ON (p.id);
CREATE INDEX FOR (z:Zone) ON (z.id);
CREATE INDEX FOR (a:Asset) ON (a.id);
CREATE INDEX FOR (t:Threat) ON (t.id);
CREATE INDEX FOR (d:Document) ON (d.id);

// Create initial constraints
CREATE CONSTRAINT project_id_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT zone_id_unique IF NOT EXISTS FOR (z:Zone) REQUIRE z.id IS UNIQUE;
EOF

# Verify database initialization
docker-compose exec postgres psql -U iec62443_app -d iec62443 -c "\dt"
```

---

## Post-Deployment Verification

### Health Check Endpoint

```bash
# Check API health
curl -s https://localhost/health | jq .

# Expected response:
{
  "status": "ok",
  "services": {
    "postgres": "connected",
    "neo4j": "connected",
    "qdrant": "connected",
    "redis": "connected"
  },
  "timestamp": "2024-12-09T12:34:56Z"
}
```

### Verify Application Access

```bash
# Open in browser (may need to accept self-signed cert in dev)
https://localhost/

# Expected: Login page with username/password form
# Credentials: admin / <password from .env>
```

### Check Service Connectivity

```bash
# Postgres
docker-compose exec app psql -U iec62443_app -h postgres -d iec62443 -c "SELECT 1"

# Neo4j
docker-compose exec app node -e "
const driver = require('neo4j-driver')('bolt://neo4j:7687', 'neo4j', 'PASSWORD');
driver.session().run('RETURN 1').then(() => console.log('Neo4j OK')).catch(e => console.error(e));
"

# Qdrant
docker-compose exec app curl -s http://qdrant:6333/health | jq .

# OpenRouter (from app logs)
docker-compose logs app | grep -i "openrouter\|llm"
```

---

## Database Migrations

### Create New Migration (During Development)

```bash
# Generate migration file
docker-compose exec app npm run migrate:create -- add_new_table

# Edit migration file in ./migrations/
# Run migration
docker-compose exec app npm run migrate:latest

# Rollback if needed
docker-compose exec app npm run migrate:rollback
```

### Backup Before Major Upgrades

```bash
# Postgres backup
docker-compose exec postgres pg_dump -U iec62443_app iec62443 > backup-postgres-$(date +%Y%m%d).sql

# Neo4j backup (community edition doesn't support online backup)
# Option 1: Stop container and copy volume
docker-compose stop neo4j
sudo tar -czf backup-neo4j-$(date +%Y%m%d).tar.gz $(docker volume inspect iec62443-neo4j_data --format '{{ .Mountpoint }}')
docker-compose start neo4j

# Option 2: Use dump & load
docker-compose exec neo4j cypher-shell -u neo4j -p PASSWORD "CALL apoc.export.cypher.all('dump.cypher')" 2>/dev/null || echo "APOC not available in community edition"
```

---

## Pre-ingestion of Vector Collections

### Pre-ingest IEC 62443 Standards & MITRE ICS

Before users can query, pre-populate Qdrant with reference data:

```bash
# Create collections
docker-compose exec app node scripts/ingest-standards.js

# Expected output:
# ✓ Created collection: iec62443_standards (2038 vectors)
# ✓ Created collection: mitre_ics (419 vectors)
# ✓ Created collection: project_docs (0 vectors, ready for uploads)
```

### Ingestion Scripts

**File: `scripts/ingest-standards.js`**

```javascript
#!/usr/bin/env node

const { QdrantClient } = require('@qdrant/js-client-rest');
const OpenAI = require('openai');
const fs = require('fs');

const qdrantClient = new QdrantClient({
  url: process.env.QDRANT_URL || 'http://qdrant:6333',
  apiKey: process.env.QDRANT_API_KEY,
});

const openai = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
  defaultHeaders: {
    'HTTP-Referer': 'https://iec62443-workshop.example.com',
  },
});

async function ingestIEC62443Standards() {
  console.log('Ingesting IEC 62443 standards...');

  // Load standards data (assume JSON file in repo)
  const standardsData = JSON.parse(fs.readFileSync('./data/iec62443-standards.json', 'utf8'));

  // Create collection
  await qdrantClient.recreateCollection('iec62443_standards', {
    vectors: {
      size: 1536,  // text-embedding-3-large
      distance: 'Cosine',
    },
  });

  let point_id = 1;
  for (const sr of standardsData.security_requirements) {
    const text = `${sr.id}: ${sr.title}\n${sr.description}`;
    
    // Generate embedding via OpenRouter
    const embedding = await openai.embeddings.create({
      model: 'text-embedding-3-large',
      input: text,
    });

    // Store in Qdrant
    await qdrantClient.upsertPoints('iec62443_standards', {
      points: [
        {
          id: point_id++,
          vector: embedding.data[0].embedding,
          payload: {
            id: sr.id,
            title: sr.title,
            description: sr.description,
            fr: sr.foundational_requirement,
            sl_t: sr.security_levels,
          },
        },
      ],
    });
  }

  console.log(`✓ Created collection: iec62443_standards (${point_id - 1} vectors)`);
}

async function ingestMITRE_ICS() {
  console.log('Ingesting MITRE ATT&CK ICS...');

  // Load MITRE data
  const mitreData = JSON.parse(fs.readFileSync('./data/mitre-ics.json', 'utf8'));

  // Create collection
  await qdrantClient.recreateCollection('mitre_ics', {
    vectors: {
      size: 1536,
      distance: 'Cosine',
    },
  });

  let point_id = 1;
  for (const technique of mitreData.techniques) {
    const text = `${technique.id}: ${technique.name}\n${technique.description}`;
    
    const embedding = await openai.embeddings.create({
      model: 'text-embedding-3-large',
      input: text,
    });

    await qdrantClient.upsertPoints('mitre_ics', {
      points: [
        {
          id: point_id++,
          vector: embedding.data[0].embedding,
          payload: {
            id: technique.id,
            name: technique.name,
            description: technique.description,
            tactic: technique.tactic,
            platform: technique.platform || 'General',
          },
        },
      ],
    });
  }

  console.log(`✓ Created collection: mitre_ics (${point_id - 1} vectors)`);
}

async function createProjectDocsCollection() {
  console.log('Creating project_docs collection...');
  
  await qdrantClient.recreateCollection('project_docs', {
    vectors: {
      size: 1536,
      distance: 'Cosine',
    },
  });

  console.log('✓ Created collection: project_docs (ready for uploads)');
}

(async () => {
  try {
    await ingestIEC62443Standards();
    await ingestMITRE_ICS();
    await createProjectDocsCollection();
    console.log('\n✓ All collections initialized successfully');
    process.exit(0);
  } catch (error) {
    console.error('Error during ingestion:', error);
    process.exit(1);
  }
})();
```

Run:
```bash
docker-compose exec app node scripts/ingest-standards.js
```

---

## Monitoring & Health Checks

### Container Logs

```bash
# View logs for all services
docker-compose logs -f --tail=100

# View logs for specific service
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f neo4j

# Filter by keyword
docker-compose logs -f app | grep -i "error\|warning"
```

### Resource Usage

```bash
# Check CPU/Memory/Network
docker stats iec62443-app iec62443-postgres iec62443-neo4j iec62443-qdrant

# Expected baseline (idle):
# app:       ~50 MB RAM, <1% CPU
# postgres:  ~200 MB RAM, <1% CPU
# neo4j:     ~1500 MB RAM, <1% CPU
# qdrant:    ~500 MB RAM, <1% CPU
```

### Database Health

```bash
# Postgres connection count
docker-compose exec postgres psql -U iec62443_app -d iec62443 -c "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"

# Neo4j transaction count
docker-compose exec neo4j cypher-shell -u neo4j -p PASSWORD "CALL dbms.monitoring.listTransactions();"

# Qdrant collection stats
curl -s http://localhost:6333/collections | jq '.result'
```

### Prometheus Metrics (Optional)

For production, integrate with monitoring stack (Prometheus + Grafana):

```yaml
# In docker-compose.yml, add prometheus service:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    ports:
      - "9090:9090"
    networks:
      - iec62443-network
```

---

## Backup & Recovery

### Daily Automated Backup

**File: `scripts/backup.sh`**

```bash
#!/bin/bash

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "Starting backup at $(date)..."

# Postgres
echo "Backing up Postgres..."
docker-compose exec -T postgres pg_dump -U iec62443_app iec62443 | gzip > "$BACKUP_DIR/postgres-$DATE.sql.gz"

# Neo4j (dump via Cypher shell export, if available)
echo "Backing up Neo4j..."
docker-compose exec -T neo4j cypher-shell -u neo4j -p "${NEO4J_PASSWORD}" << 'EOF' 2>/dev/null || echo "Neo4j dump skipped (APOC required)"
CALL apoc.export.cypher.all('neo4j-$DATE.cypher')
EOF

# Qdrant (snapshot)
echo "Backing up Qdrant..."
docker-compose exec -T qdrant tar -czf /tmp/qdrant-$DATE.tar.gz /qdrant/storage
docker cp iec62443-qdrant:/tmp/qdrant-$DATE.tar.gz "$BACKUP_DIR/"

# Application config
cp .env "$BACKUP_DIR/.env-$DATE"

echo "Backup completed at $(date)"
ls -lh "$BACKUP_DIR"/*-$DATE* | tail -10
```

Schedule with cron:

```bash
# Add to crontab (backup daily at 2 AM)
0 2 * * * cd /path/to/iec62443-workshop && bash scripts/backup.sh >> logs/backup.log 2>&1
```

### Disaster Recovery

```bash
# Restore from backup
BACKUP_DATE="20241209_020000"

# Stop app (but keep DB containers running)
docker-compose stop app

# Restore Postgres
docker-compose exec -T postgres psql -U iec62443_app iec62443 < backups/postgres-$BACKUP_DATE.sql.gz

# Restore Qdrant
docker-compose stop qdrant
sudo tar -xzf backups/qdrant-$BACKUP_DATE.tar.gz -C $(docker volume inspect iec62443_qdrant_data --format '{{ .Mountpoint }}')/../
docker-compose start qdrant

# Restart app
docker-compose up -d app

# Verify
docker-compose exec app curl -s http://localhost:3000/health
```

---

## Scaling & Performance Tuning

### Single-Machine to Multi-Machine (Future)

For scaling beyond single node:

1. **Separate DB servers:**
   ```bash
   # Move Postgres, Neo4j, Qdrant to dedicated machines
   # Update connection strings in .env
   ```

2. **Load balancer:**
   ```bash
   # Replace nginx with HAProxy or AWS ALB
   # Deploy multiple app instances across nodes
   ```

3. **Object storage:**
   ```bash
   # Use S3 instead of local filesystem for documents
   # Update app config for S3 bucket
   ```

### Performance Tuning (Current Setup)

```bash
# Postgres: increase shared buffers for large datasets
# In docker-compose.yml:
  postgres:
    environment:
      POSTGRES_INITDB_ARGS: "-c shared_buffers=2GB -c effective_cache_size=6GB"

# Neo4j: increase heap memory (already set to 4GB in docker-compose.yml)
# Monitor with:
docker-compose exec neo4j cat /proc/meminfo

# Qdrant: enable HNSW optimization for >10k vectors
# (handled automatically; no tuning needed for MVP)

# Next.js: enable caching headers
# (nginx.conf should include cache-control headers)
```

### Load Testing (Pre-Launch)

```bash
# Use k6 or Apache JMeter
# Example with k6:
docker run --rm --network iec62443-network -i grafana/k6 run - << 'EOF'
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 10,
  duration: '5m',
};

export default function () {
  let res = http.get('http://app:3000/api/health');
  check(res, { 'status is 200': (r) => r.status === 200 });
}
EOF
```

---

## Troubleshooting

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| App won't start | `docker logs` shows db connection error | Wait 60s for postgres healthcheck; verify .env DSN |
| 502 Bad Gateway | Nginx error after login | Check app container health: `docker-compose ps app` |
| Qdrant returns 400 | Vector ingestion fails | Verify embedding dimension (1536 for text-embedding-3-large); check API key |
| Neo4j initialization timeout | Cypher shell hangs | Increase `start_period` in docker-compose.yml; check Neo4j logs |
| Out of disk space | Docker volumes full | Prune unused images: `docker system prune -a` |
| High memory usage | Postgres/Neo4j consuming >80% RAM | Reduce `heap_max_size` in docker-compose.yml; add Redis for caching |

### Debug Commands

```bash
# Inspect volume contents
docker run -it --rm -v iec62443_postgres_data:/data alpine ls -lh /data

# Execute psql directly in container
docker-compose exec postgres psql -U iec62443_app -d iec62443

# Cypher query against Neo4j
docker-compose exec neo4j cypher-shell -u neo4j -p PASSWORD "MATCH (n) RETURN COUNT(n)"

# Test Qdrant
curl -s http://localhost:6333/collections | jq .

# Check JWT token expiration
node -e "console.log(new Date(Date.now() + 86400000))"  # Current + 24h
```

### Reset to Clean State

```bash
# ⚠️ WARNING: Deletes all data

# Stop services
docker-compose down

# Remove volumes
docker volume rm iec62443_postgres_data iec62443_neo4j_data iec62443_qdrant_data

# Restart
docker-compose up -d

# Re-initialize
docker-compose exec app npm run migrate:latest
docker-compose exec app node scripts/ingest-standards.js
```

---

## Maintenance Tasks

### Weekly
- [ ] Review error logs for anomalies
- [ ] Check disk usage on Docker host
- [ ] Verify backups are being created

### Monthly
- [ ] Update Docker images to latest patches
- [ ] Review and optimize slow queries (Postgres/Neo4j logs)
- [ ] Test disaster recovery process
- [ ] Review audit log for access patterns

### Quarterly
- [ ] Plan capacity upgrades if needed
- [ ] Review and update TLS certificates (before expiration)
- [ ] Stress test with realistic load profiles
- [ ] Update security patches for base OS

---

## Handoff Checklist

Before handing off to operations team:

- [ ] Docker Compose file tested on target infrastructure
- [ ] .env template with all required variables documented
- [ ] SSL/TLS certificates installed
- [ ] Initial admin user created and tested
- [ ] Backup & recovery procedures documented and tested
- [ ] Monitoring alerts configured (if applicable)
- [ ] Runbooks for common troubleshooting scenarios
- [ ] Health check endpoints verified
- [ ] Load testing completed with acceptable results
- [ ] Disaster recovery plan reviewed with ops team

---

**End of Docker Deployment Guide**

For questions or updates, contact: DevOps Team  
Last Updated: December 2024  
Version: 1.0
