# Docker Infrastructure Architecture Analysis
**File**: DOCKER_ARCHITECTURE_ANALYSIS.md
**Created**: 2025-11-03 15:45:00 UTC
**Version**: v1.0.0
**Author**: System Architecture Designer
**Purpose**: Analyze existing OpenSPG Docker infrastructure and design Next.js integration
**Status**: ACTIVE

---

## Executive Summary

This document analyzes the existing OpenSPG production infrastructure running in Docker containers and provides a detailed integration plan for adding a Next.js web interface (`aeon-ui`) that will connect to the existing graph database, vector database, and other services.

**Current Infrastructure**: 5 production containers on `openspg-network` (172.18.0.0/16)
**Integration Goal**: Add Next.js container with seamless connectivity to all backend services
**Security Model**: Internal network isolation with selective port exposure

---

## 1. Current Infrastructure Analysis

### 1.1 Network Configuration

**Network Name**: `openspg-network`
**Network Type**: Bridge
**Subnet**: 172.18.0.0/16
**Gateway**: 172.18.0.1

**Container IP Assignments**:
```
172.18.0.2 - openspg-minio      (Object Storage)
172.18.0.3 - openspg-neo4j      (Graph Database)
172.18.0.4 - openspg-server     (Application Server)
172.18.0.5 - openspg-mysql      (Relational Database)
172.18.0.6 - openspg-qdrant     (Vector Database)
172.18.0.7 - agent-zero-main    (External service)
```

**Available IPs for New Services**: 172.18.0.8+ (recommend 172.18.0.8 for aeon-ui)

---

### 1.2 Service Port Mappings

| Service | Container Port | Host Port | Protocol | Status |
|---------|---------------|-----------|----------|---------|
| **Neo4j Browser** | 7474 | 7474 | HTTP | Healthy |
| **Neo4j Bolt** | 7687 | 7687 | Bolt | Healthy |
| **MySQL** | 3306 | 3306 | MySQL | Healthy |
| **MinIO API** | 9000 | 9000 | HTTP | Healthy |
| **MinIO Console** | 9001 | 9001 | HTTP | Healthy |
| **Qdrant API** | 6333 | 6333 | HTTP | Unhealthy* |
| **Qdrant gRPC** | 6334 | 6334 | gRPC | Unhealthy* |
| **OpenSPG Server** | 8887 | 8887 | HTTP | Unhealthy* |

*Note: Unhealthy status may indicate service startup issues or health check configuration

**Port 3000**: Available for Next.js application (aeon-ui)

---

### 1.3 Volume Mounts

**openspg-server volumes**:
```
/var/lib/docker/volumes/openspg-server-logs/_data → /app/logs
/var/lib/docker/volumes/openspg-shared-data/_data → /shared
/etc/localtime → /etc/localtime (read-only)
```

**Key Observations**:
- Shared data volume (`openspg-shared-data`) for inter-service communication
- Log persistence for troubleshooting
- Timezone synchronization (Asia/Shanghai)

---

### 1.4 Environment Variables Analysis

#### Neo4j (openspg-neo4j)
```bash
NEO4J_AUTH=neo4j/neo4j@openspg
NEO4J_PLUGINS=["apoc"]
NEO4J_server_memory_heap_initial__size=2G
NEO4J_server_memory_heap_max__size=4G
NEO4J_server_memory_pagecache_size=2G
NEO4J_dbms_memory_transaction_total_max=2G
NEO4J_server_bolt_listen__address=0.0.0.0:7687
NEO4J_server_http_listen__address=0.0.0.0:7474
NEO4J_initial_dbms_default__database=neo4j
TZ=Asia/Shanghai
```

**Key Points**:
- Authentication: Username `neo4j`, Password `neo4j@openspg`
- APOC plugin enabled for advanced graph operations
- Bolt endpoint: `bolt://openspg-neo4j:7687` (internal) or `bolt://localhost:7687` (from host)
- HTTP endpoint: `http://openspg-neo4j:7474`

#### MySQL (openspg-mysql)
```bash
MYSQL_ROOT_PASSWORD=openspg
MYSQL_DATABASE=openspg
MYSQL_ROOT_HOST=%
TZ=Asia/Shanghai
```

**Connection Details**:
- Database: `openspg`
- Root password: `openspg`
- Internal endpoint: `mysql://openspg-mysql:3306/openspg`

#### MinIO (openspg-minio)
```bash
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio@openspg
TZ=Asia/Shanghai
```

**Connection Details**:
- Access Key: `minio`
- Secret Key: `minio@openspg`
- API endpoint: `http://openspg-minio:9000`
- Console: `http://openspg-minio:9001`

#### Qdrant (openspg-qdrant)
```bash
QDRANT__SERVICE__API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=
QDRANT__STORAGE__PERFORMANCE__MAX_SEARCH_THREADS=4
QDRANT__COLLECTION__DEFAULT_HNSW_M=16
QDRANT__COLLECTION__DEFAULT_HNSW_EF_CONSTRUCT=100
QDRANT__LOG_LEVEL=INFO
TZ=Asia/Shanghai
```

**Connection Details**:
- API endpoint: `http://openspg-qdrant:6333`
- API Key required: `deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=`

#### OpenSPG Server (openspg-server)
```bash
JAVA_OPTS=-Xms2048m -Xmx8192m -Dfile.encoding=UTF-8
TZ=Asia/Shanghai
```

---

## 2. Next.js Integration Architecture

### 2.1 Proposed Service Definition

**Service Name**: `aeon-ui`
**Base Image**: `node:20-alpine` or `node:20-slim`
**Port**: 3000 (host) → 3000 (container)
**Network**: `openspg-network`
**Expected IP**: 172.18.0.8

---

### 2.2 Docker Compose Service Definition

```yaml
services:
  aeon-ui:
    image: node:20-alpine
    container_name: aeon-ui
    hostname: aeon-ui
    networks:
      openspg-network:
        ipv4_address: 172.18.0.8  # Optional: auto-assign also works
    ports:
      - "3000:3000"
    environment:
      # Application
      - NODE_ENV=production
      - NEXT_PUBLIC_APP_NAME=AEON UI
      - TZ=Asia/Shanghai

      # Neo4j Connection (Graph Database)
      - NEO4J_URI=bolt://openspg-neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=neo4j@openspg
      - NEO4J_DATABASE=neo4j

      # Qdrant Connection (Vector Database)
      - QDRANT_URL=http://openspg-qdrant:6333
      - QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

      # MySQL Connection (Relational Database)
      - MYSQL_HOST=openspg-mysql
      - MYSQL_PORT=3306
      - MYSQL_DATABASE=openspg
      - MYSQL_USER=root
      - MYSQL_PASSWORD=openspg

      # MinIO Connection (Object Storage)
      - MINIO_ENDPOINT=http://openspg-minio:9000
      - MINIO_ACCESS_KEY=minio
      - MINIO_SECRET_KEY=minio@openspg
      - MINIO_USE_SSL=false

      # OpenSPG Server
      - OPENSPG_SERVER_URL=http://openspg-server:8887

      # Security
      - NEXTAUTH_URL=http://localhost:3000
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET:-change-me-in-production}

    volumes:
      - ./web_interface:/app
      - /app/node_modules
      - /app/.next
      - aeon-ui-logs:/app/logs
      - openspg-shared-data:/shared:ro  # Read-only access to shared data

    working_dir: /app
    command: >
      sh -c "
        npm install &&
        npm run build &&
        npm run start
      "

    restart: unless-stopped

    depends_on:
      - openspg-neo4j
      - openspg-qdrant
      - openspg-mysql
      - openspg-minio

    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  aeon-ui-logs:
    driver: local
  openspg-shared-data:
    external: true  # Reference existing shared volume

networks:
  openspg-network:
    external: true  # Reference existing network
```

---

### 2.3 Service Connectivity Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        openspg-network                          │
│                       (172.18.0.0/16)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌────────────────────────────┐       │
│  │ User Browser │────────▶│  aeon-ui (Next.js)         │       │
│  │  :3000       │  HTTP   │  172.18.0.8:3000           │       │
│  └──────────────┘         └────────────┬───────────────┘       │
│                                        │                        │
│                          ┌─────────────┴─────────────┐          │
│                          │                           │          │
│                ┌─────────▼────────┐      ┌──────────▼────────┐ │
│                │ openspg-neo4j    │      │ openspg-qdrant    │ │
│                │ 172.18.0.3       │      │ 172.18.0.6        │ │
│                │ :7687 (Bolt)     │      │ :6333 (HTTP)      │ │
│                │ :7474 (HTTP)     │      │ :6334 (gRPC)      │ │
│                │                  │      │                   │ │
│                │ 115 docs         │      │ Vector search     │ │
│                │ 12,256 entities  │      │ + embeddings      │ │
│                └──────────────────┘      └───────────────────┘ │
│                          │                           │          │
│                ┌─────────▼────────┐      ┌──────────▼────────┐ │
│                │ openspg-mysql    │      │ openspg-minio     │ │
│                │ 172.18.0.5       │      │ 172.18.0.2        │ │
│                │ :3306 (MySQL)    │      │ :9000 (API)       │ │
│                │                  │      │ :9001 (Console)   │ │
│                │ openspg DB       │      │ Object storage    │ │
│                └──────────────────┘      └───────────────────┘ │
│                          │                                      │
│                ┌─────────▼────────┐                            │
│                │ openspg-server   │                            │
│                │ 172.18.0.4       │                            │
│                │ :8887 (HTTP)     │                            │
│                │                  │                            │
│                │ Backend API      │                            │
│                └──────────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

External Access:
- Host:3000  → aeon-ui (Next.js web interface)
- Host:7474  → Neo4j Browser
- Host:7687  → Neo4j Bolt protocol
- Host:3306  → MySQL (if needed)
- Host:9000  → MinIO API
- Host:6333  → Qdrant API
```

---

## 3. Environment Variable Configuration

### 3.1 Development Environment (.env.development)

```bash
# Application
NODE_ENV=development
NEXT_PUBLIC_APP_NAME=AEON UI (Dev)
TZ=Asia/Shanghai
PORT=3000

# Neo4j (Graph Database)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg
NEO4J_DATABASE=neo4j

# Qdrant (Vector Database)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

# MySQL (Relational Database)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=openspg
MYSQL_USER=root
MYSQL_PASSWORD=openspg

# MinIO (Object Storage)
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false

# OpenSPG Server
OPENSPG_SERVER_URL=http://localhost:8887

# Security
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=development-secret-change-in-production

# Debug
DEBUG=true
LOG_LEVEL=debug
```

---

### 3.2 Production Environment (.env.production)

```bash
# Application
NODE_ENV=production
NEXT_PUBLIC_APP_NAME=AEON UI
TZ=Asia/Shanghai
PORT=3000

# Neo4j (Graph Database) - Internal network
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg
NEO4J_DATABASE=neo4j

# Qdrant (Vector Database) - Internal network
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

# MySQL (Relational Database) - Internal network
MYSQL_HOST=openspg-mysql
MYSQL_PORT=3306
MYSQL_DATABASE=openspg
MYSQL_USER=root
MYSQL_PASSWORD=openspg

# MinIO (Object Storage) - Internal network
MINIO_ENDPOINT=http://openspg-minio:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false

# OpenSPG Server - Internal network
OPENSPG_SERVER_URL=http://openspg-server:8887

# Security
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=<GENERATE_STRONG_SECRET_HERE>

# Performance
DEBUG=false
LOG_LEVEL=info
```

---

## 4. Security Considerations

### 4.1 Network Security

**Internal Network Isolation**:
- All services communicate via private `openspg-network` (172.18.0.0/16)
- Only necessary ports exposed to host
- Service-to-service communication uses container names (DNS resolution)

**Port Exposure Strategy**:
```
External (0.0.0.0) → Minimal necessary ports
Internal (172.18.x.x) → Full service communication
```

---

### 4.2 Credential Management

**Current State** (SECURITY RISK):
- Hardcoded credentials in environment variables
- Credentials visible in `docker inspect`
- No secrets management system

**Recommendations**:
1. **Docker Secrets** (Swarm mode) or **Environment files** (.env not in git)
2. **Vault integration** for production deployments
3. **Rotate credentials** immediately if exposed
4. **Least privilege access** for each service

**High Priority Credential Rotation**:
```bash
# Neo4j
NEO4J_PASSWORD=<strong-password>

# MySQL
MYSQL_ROOT_PASSWORD=<strong-password>

# MinIO
MINIO_ROOT_PASSWORD=<strong-password>

# Qdrant
QDRANT__SERVICE__API_KEY=<strong-api-key>

# NextAuth
NEXTAUTH_SECRET=$(openssl rand -base64 32)
```

---

### 4.3 CORS Configuration

**Next.js API Routes** (`next.config.js`):
```javascript
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: 'http://localhost:3000' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ];
  },
};
```

**Backend Services**:
- Configure OpenSPG Server to allow requests from `aeon-ui` container
- Neo4j: No CORS needed (Bolt protocol)
- Qdrant: API key authentication sufficient

---

### 4.4 Environment Variable Security

**Best Practices**:
1. **Never commit** `.env` files to git (add to `.gitignore`)
2. **Use `.env.example`** templates with placeholder values
3. **Validate** required environment variables at startup
4. **Sanitize logs** to prevent credential leakage
5. **Encrypt** sensitive environment variables at rest

**Startup Validation** (Next.js):
```typescript
// src/lib/env-validation.ts
const requiredEnvVars = [
  'NEO4J_URI',
  'NEO4J_USER',
  'NEO4J_PASSWORD',
  'QDRANT_URL',
  'QDRANT_API_KEY',
  'NEXTAUTH_SECRET',
];

requiredEnvVars.forEach((varName) => {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
});
```

---

## 5. Development Workflow

### 5.1 Local Development (Without Docker)

**Prerequisites**:
- Node.js 20+ installed
- Access to OpenSPG services via `localhost` ports

**Setup**:
```bash
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface
npm install
cp .env.example .env.development
# Edit .env.development with localhost endpoints
npm run dev
```

**Service Access**:
- Services accessible via host ports (7687, 6333, 3306, 9000, etc.)
- Environment uses `localhost` instead of container names

---

### 5.2 Docker Development Environment

**Build Development Image**:
```bash
docker build -t aeon-ui:dev -f Dockerfile.dev .
```

**Run with docker-compose**:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

**Hot Reload Support**:
```yaml
# docker-compose.dev.yml
services:
  aeon-ui:
    volumes:
      - ./web_interface:/app
      - /app/node_modules
      - /app/.next
    command: npm run dev
```

---

### 5.3 Production Deployment

**Multi-Stage Dockerfile**:
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
CMD ["npm", "run", "start"]
```

**Deploy**:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## 6. Health Checks and Monitoring

### 6.1 Service Health Endpoints

**aeon-ui Health Check**:
```typescript
// src/pages/api/health.ts
export default async function handler(req, res) {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    services: {
      neo4j: await checkNeo4j(),
      qdrant: await checkQdrant(),
      mysql: await checkMySQL(),
      minio: await checkMinIO(),
    },
  };

  const allHealthy = Object.values(health.services).every(s => s.status === 'healthy');
  res.status(allHealthy ? 200 : 503).json(health);
}
```

**Docker Health Check**:
```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

---

### 6.2 Service Status Monitoring

**Current Status**:
- ✅ Neo4j: Healthy
- ✅ MySQL: Healthy
- ✅ MinIO: Healthy
- ⚠️ Qdrant: Unhealthy (investigate)
- ⚠️ OpenSPG Server: Unhealthy (investigate)

**Monitoring Commands**:
```bash
# Check all services
docker ps --format "table {{.Names}}\t{{.Status}}"

# Check logs
docker logs openspg-qdrant --tail 50
docker logs openspg-server --tail 50

# Restart unhealthy services
docker restart openspg-qdrant
docker restart openspg-server
```

---

## 7. Integration Checklist

### 7.1 Pre-Integration Tasks

- [ ] Review and understand current infrastructure
- [ ] Document all service credentials
- [ ] Test connectivity to Neo4j, Qdrant, MySQL, MinIO
- [ ] Verify network isolation and security
- [ ] Create `.env.example` template
- [ ] Set up `.gitignore` for sensitive files

---

### 7.2 Integration Tasks

- [ ] Create Next.js project structure
- [ ] Configure environment variables
- [ ] Implement database connection modules
- [ ] Create health check endpoints
- [ ] Write Docker Compose service definition
- [ ] Build and test Docker image
- [ ] Test inter-service connectivity
- [ ] Implement error handling and logging

---

### 7.3 Post-Integration Tasks

- [ ] Verify all services are healthy
- [ ] Test end-to-end workflows
- [ ] Monitor resource usage (CPU, memory)
- [ ] Review security configuration
- [ ] Document deployment procedures
- [ ] Set up backup and recovery procedures
- [ ] Rotate default credentials

---

## 8. Troubleshooting Guide

### 8.1 Common Issues

**Issue**: Cannot connect to Neo4j from Next.js container
**Solution**:
```bash
# Verify network connectivity
docker exec -it aeon-ui ping openspg-neo4j

# Check Neo4j logs
docker logs openspg-neo4j

# Test Bolt connection
docker exec -it aeon-ui npm run test:neo4j
```

**Issue**: Qdrant API returns 401 Unauthorized
**Solution**:
```bash
# Verify API key in environment
docker exec -it aeon-ui env | grep QDRANT_API_KEY

# Test Qdrant API
curl -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" http://localhost:6333/collections
```

**Issue**: CORS errors in browser
**Solution**:
- Configure CORS in `next.config.js`
- Ensure `NEXTAUTH_URL` matches actual URL
- Check browser console for specific CORS error

---

### 8.2 Debugging Commands

```bash
# Inspect container environment
docker exec -it aeon-ui env

# Check network connectivity
docker network inspect openspg-network

# View real-time logs
docker logs -f aeon-ui

# Shell into container
docker exec -it aeon-ui sh

# Test service endpoints from container
docker exec -it aeon-ui wget -O- http://openspg-neo4j:7474
```

---

## 9. Performance Optimization

### 9.1 Resource Allocation

**Recommended Container Limits**:
```yaml
services:
  aeon-ui:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

**Monitoring**:
```bash
docker stats aeon-ui
```

---

### 9.2 Next.js Optimization

**Production Build**:
- Enable `output: 'standalone'` in `next.config.js`
- Optimize images with `next/image`
- Implement API route caching
- Use React Server Components where possible

**Database Connection Pooling**:
```typescript
// Connection pool for Neo4j
const driver = neo4j.driver(
  process.env.NEO4J_URI,
  neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASSWORD),
  { maxConnectionPoolSize: 50 }
);
```

---

## 10. Next Steps

### 10.1 Immediate Actions

1. **Investigate unhealthy services**: Fix Qdrant and OpenSPG Server health checks
2. **Rotate credentials**: Change all default passwords
3. **Create Docker Compose file**: Define `aeon-ui` service
4. **Set up Next.js project**: Initialize with proper structure
5. **Implement connection modules**: Create reusable database clients

---

### 10.2 Short-Term Goals

1. **Deploy aeon-ui container**: Test integration with backend services
2. **Implement basic UI**: Graph visualization, search, document management
3. **Set up monitoring**: Prometheus + Grafana for metrics
4. **Configure backups**: Automated backup for Neo4j and MySQL
5. **Write deployment docs**: Step-by-step guide for production

---

### 10.3 Long-Term Roadmap

1. **Implement authentication**: NextAuth.js with role-based access
2. **Add caching layer**: Redis for API response caching
3. **Horizontal scaling**: Load balancing for multiple aeon-ui instances
4. **CI/CD pipeline**: Automated testing and deployment
5. **Advanced features**: Real-time updates, collaborative editing

---

## Appendix A: Complete Docker Compose Example

```yaml
version: '3.8'

services:
  aeon-ui:
    build:
      context: ./web_interface
      dockerfile: Dockerfile
    container_name: aeon-ui
    hostname: aeon-ui
    networks:
      - openspg-network
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - TZ=Asia/Shanghai
      - NEO4J_URI=bolt://openspg-neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=neo4j@openspg
      - NEO4J_DATABASE=neo4j
      - QDRANT_URL=http://openspg-qdrant:6333
      - QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=
      - MYSQL_HOST=openspg-mysql
      - MYSQL_PORT=3306
      - MYSQL_DATABASE=openspg
      - MYSQL_USER=root
      - MYSQL_PASSWORD=openspg
      - MINIO_ENDPOINT=http://openspg-minio:9000
      - MINIO_ACCESS_KEY=minio
      - MINIO_SECRET_KEY=minio@openspg
      - OPENSPG_SERVER_URL=http://openspg-server:8887
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
    volumes:
      - aeon-ui-logs:/app/logs
      - openspg-shared-data:/shared:ro
    restart: unless-stopped
    depends_on:
      - openspg-neo4j
      - openspg-qdrant
      - openspg-mysql
      - openspg-minio
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  aeon-ui-logs:
    driver: local
  openspg-shared-data:
    external: true

networks:
  openspg-network:
    external: true
```

---

## Appendix B: Environment Variables Reference

| Variable | Service | Purpose | Example |
|----------|---------|---------|---------|
| `NEO4J_URI` | Neo4j | Bolt connection string | `bolt://openspg-neo4j:7687` |
| `NEO4J_USER` | Neo4j | Authentication username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j | Authentication password | `neo4j@openspg` |
| `NEO4J_DATABASE` | Neo4j | Default database name | `neo4j` |
| `QDRANT_URL` | Qdrant | HTTP API endpoint | `http://openspg-qdrant:6333` |
| `QDRANT_API_KEY` | Qdrant | API authentication key | `deqUCd5v5tL...` |
| `MYSQL_HOST` | MySQL | Database hostname | `openspg-mysql` |
| `MYSQL_PORT` | MySQL | Database port | `3306` |
| `MYSQL_DATABASE` | MySQL | Database name | `openspg` |
| `MYSQL_USER` | MySQL | Database username | `root` |
| `MYSQL_PASSWORD` | MySQL | Database password | `openspg` |
| `MINIO_ENDPOINT` | MinIO | Object storage endpoint | `http://openspg-minio:9000` |
| `MINIO_ACCESS_KEY` | MinIO | Access key | `minio` |
| `MINIO_SECRET_KEY` | MinIO | Secret key | `minio@openspg` |
| `OPENSPG_SERVER_URL` | OpenSPG | Backend API endpoint | `http://openspg-server:8887` |
| `NEXTAUTH_SECRET` | NextAuth | Session encryption key | `<random-secret>` |

---

**Document Status**: Complete
**Last Updated**: 2025-11-03
**Review Required**: Before production deployment
**Next Review Date**: 2025-12-03
