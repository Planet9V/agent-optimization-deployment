# OpenSPG Docker Compose Deployment Analysis

**File:** 2025-10-26_OpenSPG_Docker-Compose_Analysis.md
**Created:** 2025-10-26
**Purpose:** Complete analysis of OpenSPG docker-compose deployment configuration
**Status:** ACTIVE

## Executive Summary

OpenSPG deploys as a 4-service stack using Docker Compose with the following components:
- **OpenSPG Server**: Main application server (Java-based)
- **MySQL**: Relational database for metadata and configuration
- **Neo4j**: Graph database for knowledge graph storage
- **MinIO**: S3-compatible object storage for artifacts

All services use custom images from Alibaba Cloud Container Registry.

---

## Service Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OpenSPG Server                       │
│                   (Port 8887)                           │
│            JVM: 2GB-8GB | Java Application             │
└────────┬──────────┬──────────────┬─────────────────────┘
         │          │              │
         ▼          ▼              ▼
    ┌────────┐ ┌─────────┐  ┌──────────┐
    │ MySQL  │ │  Neo4j  │  │  MinIO   │
    │  3306  │ │7474/7687│  │9000/9001 │
    └────────┘ └─────────┘  └──────────┘
```

---

## Detailed Service Configurations

### 1. OpenSPG Server (openspg-server)

**Image:**
```
spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-server:latest
```

**Port Mapping:**
- `8887:8887` - HTTP API endpoint

**Environment Variables:**
```yaml
JAVA_OPTS: -Xms2g -Xmx8g
TZ: Asia/Shanghai
RUNNING_MODE: docker
MYSQL_URL: jdbc:mysql://openspg-mysql:3306/openspg?useUnicode=true&characterEncoding=utf-8&useSSL=false
MYSQL_USER: root
MYSQL_PASS: openspg
NEO4J_URI: bolt://openspg-neo4j:7687
NEO4J_USER: neo4j
NEO4J_PASS: neo4j@openspg
```

**Dependencies:**
- `openspg-mysql` (database ready)
- `openspg-neo4j` (graph database ready)
- `openspg-minio` (object storage ready)

**Resource Requirements:**
- Minimum Heap: 2GB
- Maximum Heap: 8GB
- Recommended RAM: 10GB+ (8GB heap + overhead)

**Restart Policy:** `always`

---

### 2. MySQL Database (openspg-mysql)

**Image:**
```
spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-mysql:latest
```

**Port Mapping:**
- `3306:3306` - MySQL protocol

**Environment Variables:**
```yaml
MYSQL_ROOT_PASSWORD: openspg
MYSQL_DATABASE: openspg
TZ: Asia/Shanghai
MYSQL_ROOT_HOST: '%'
LANG: C.UTF-8
```

**Character Set:**
- Encoding: UTF-8MB4 (full Unicode support including emojis)
- Collation: utf8mb4_unicode_ci

**Security Notes:**
- Root access allowed from any host (`%`)
- Default password: `openspg` (CHANGE IN PRODUCTION)
- No volume persistence defined (data lost on container removal)

**Restart Policy:** `always`

---

### 3. Neo4j Graph Database (openspg-neo4j)

**Image:**
```
spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-neo4j:latest
```

**Port Mappings:**
- `7474:7474` - HTTP browser interface
- `7687:7687` - Bolt protocol (graph queries)

**Environment Variables:**
```yaml
TZ: Asia/Shanghai
NEO4J_AUTH: neo4j/neo4j@openspg
NEO4J_PLUGINS: '["apoc"]'
NEO4J_apoc_export_file_enabled: 'true'
NEO4J_apoc_import_file_enabled: 'true'
NEO4J_apoc_import_file_use__neo4j__config: 'true'
NEO4J_server_memory_heap_initial__size: 1G
NEO4J_server_memory_heap_max__size: 4G
NEO4J_server_memory_pagecache_size: 1G
```

**Volumes:**
- `$HOME/dozerdb/logs:/logs` - Log file persistence

**Plugins:**
- **APOC** (Awesome Procedures on Cypher) enabled
- Import/Export file operations enabled

**Memory Configuration:**
- Initial Heap: 1GB
- Maximum Heap: 4GB
- Page Cache: 1GB
- Recommended RAM: 6GB+ (4GB heap + 1GB cache + overhead)

**Restart Policy:** `always`

---

### 4. MinIO Object Storage (openspg-minio)

**Image:**
```
spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-minio:latest
```

**Port Mappings:**
- `9000:9000` - S3-compatible API
- `9001:9001` - Web console UI

**Environment Variables:**
```yaml
TZ: Asia/Shanghai
MINIO_ROOT_USER: minio
MINIO_ROOT_PASSWORD: minio@openspg
```

**Command:**
```
server /data --console-address ":9001"
```

**Security Notes:**
- Default credentials: `minio` / `minio@openspg` (CHANGE IN PRODUCTION)
- No volume persistence defined (data lost on container removal)

**Restart Policy:** `always`

---

## Network Configuration

**Network Type:** Bridge (default)

All services communicate via Docker's internal DNS:
- `openspg-mysql` resolves to MySQL container
- `openspg-neo4j` resolves to Neo4j container
- `openspg-minio` resolves to MinIO container

---

## Deployment Requirements

### System Requirements

**Minimum Hardware:**
- CPU: 4 cores
- RAM: 16GB (2GB + 8GB + 6GB + overhead)
- Disk: 20GB available space

**Recommended Hardware:**
- CPU: 8 cores
- RAM: 24GB
- Disk: 100GB SSD

### Software Requirements

**Required:**
- Docker Engine 20.10+
- Docker Compose 2.0+

**Operating System:**
- Linux (any modern distribution)
- macOS 11+ (with Docker Desktop)
- Windows 10+ with WSL2 (Docker Desktop)

### Network Requirements

**Ports to Expose:**
- `8887` - OpenSPG Server API
- `3306` - MySQL (optional, for external access)
- `7474` - Neo4j Browser (optional)
- `7687` - Neo4j Bolt (optional)
- `9000` - MinIO API (optional)
- `9001` - MinIO Console (optional)

**Firewall Rules:**
- Allow inbound TCP 8887 (required for API access)
- Allow inbound TCP 7474, 7687, 9000, 9001 (optional admin access)
- Allow inbound TCP 3306 (only if remote database access needed)

---

## Deployment Guide

### Quick Start

```bash
# 1. Download docker-compose.yml
curl -o docker-compose.yml https://raw.githubusercontent.com/OpenSPG/openspg/master/dev/release/docker-compose.yml

# 2. Start all services
docker-compose up -d

# 3. Check service status
docker-compose ps

# 4. View logs
docker-compose logs -f

# 5. Access OpenSPG
# API: http://localhost:8887
# Neo4j Browser: http://localhost:7474
# MinIO Console: http://localhost:9001
```

### Step-by-Step Deployment

**1. Pre-deployment Checks**
```bash
# Verify Docker installation
docker --version
docker-compose --version

# Check available resources
free -h  # RAM
df -h    # Disk space
```

**2. Create deployment directory**
```bash
mkdir -p ~/openspg-deployment
cd ~/openspg-deployment
```

**3. Download configuration**
```bash
wget https://raw.githubusercontent.com/OpenSPG/openspg/master/dev/release/docker-compose.yml
```

**4. Review and customize (IMPORTANT)**
```bash
# Edit docker-compose.yml to change default passwords
nano docker-compose.yml

# Change these values for production:
# - MYSQL_ROOT_PASSWORD
# - NEO4J_AUTH (format: username/password)
# - MINIO_ROOT_USER and MINIO_ROOT_PASSWORD
```

**5. Create log directory for Neo4j**
```bash
mkdir -p $HOME/dozerdb/logs
```

**6. Pull images**
```bash
docker-compose pull
```

**7. Start services**
```bash
# Start in detached mode
docker-compose up -d

# Or start with logs visible
docker-compose up
```

**8. Verify deployment**
```bash
# Check all containers are running
docker-compose ps

# Expected output: All services "Up" status

# Check logs for errors
docker-compose logs openspg-server
docker-compose logs openspg-mysql
docker-compose logs openspg-neo4j
docker-compose logs openspg-minio
```

**9. Test connectivity**
```bash
# Test OpenSPG API
curl http://localhost:8887

# Test MySQL
docker-compose exec openspg-mysql mysql -uroot -popenspg -e "SHOW DATABASES;"

# Test Neo4j
curl http://localhost:7474

# Test MinIO
curl http://localhost:9000/minio/health/live
```

---

## Service Dependencies & Startup Order

```
1. openspg-mysql (starts first, no dependencies)
2. openspg-neo4j (starts first, no dependencies)
3. openspg-minio (starts first, no dependencies)
4. openspg-server (waits for all above to be healthy)
```

Docker Compose uses `depends_on` with `service_healthy` condition for proper orchestration.

---

## Configuration Management

### Environment Variables

**Server Configuration:**
- `JAVA_OPTS`: JVM tuning parameters
- `MYSQL_URL`: Database connection string
- `NEO4J_URI`: Graph database connection
- `RUNNING_MODE`: Deployment mode (docker/standalone)

**Database Configuration:**
- `MYSQL_ROOT_PASSWORD`: MySQL root password
- `MYSQL_DATABASE`: Default database name
- `NEO4J_AUTH`: Neo4j credentials (username/password)

**Storage Configuration:**
- `MINIO_ROOT_USER`: MinIO admin username
- `MINIO_ROOT_PASSWORD`: MinIO admin password

### Customization Options

**1. Change JVM Memory**
```yaml
JAVA_OPTS: -Xms4g -Xmx16g  # Increase to 4GB-16GB
```

**2. Change Neo4j Memory**
```yaml
NEO4J_server_memory_heap_max__size: 8G
NEO4J_server_memory_pagecache_size: 2G
```

**3. Add Volume Persistence**
```yaml
volumes:
  - ./mysql-data:/var/lib/mysql  # MySQL data
  - ./neo4j-data:/data           # Neo4j data
  - ./minio-data:/data           # MinIO data
```

---

## Data Persistence Strategy

### Current Configuration (WARNING)

**No persistent volumes defined** for:
- MySQL database data
- Neo4j graph data
- MinIO object storage

**Impact:**
- All data lost when containers are removed
- Suitable for development/testing only
- NOT suitable for production

### Recommended Production Configuration

Add volumes to docker-compose.yml:

```yaml
services:
  openspg-mysql:
    volumes:
      - mysql-data:/var/lib/mysql

  openspg-neo4j:
    volumes:
      - neo4j-data:/data
      - $HOME/dozerdb/logs:/logs

  openspg-minio:
    volumes:
      - minio-data:/data

volumes:
  mysql-data:
  neo4j-data:
  minio-data:
```

---

## Security Considerations

### Default Credentials (MUST CHANGE)

| Service | Username | Default Password | Priority |
|---------|----------|------------------|----------|
| MySQL | root | openspg | HIGH |
| Neo4j | neo4j | neo4j@openspg | HIGH |
| MinIO | minio | minio@openspg | HIGH |

### Security Hardening Checklist

- [ ] Change all default passwords
- [ ] Restrict MySQL root host from '%' to specific IPs
- [ ] Enable SSL/TLS for MySQL connections
- [ ] Configure Neo4j authentication and HTTPS
- [ ] Enable MinIO encryption at rest
- [ ] Use Docker secrets for password management
- [ ] Implement network segmentation
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Regular security updates for images

### Network Security

**Recommended Firewall Rules:**
```bash
# Allow only OpenSPG API externally
iptables -A INPUT -p tcp --dport 8887 -j ACCEPT

# Block direct database access from external networks
iptables -A INPUT -p tcp --dport 3306 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 3306 -j DROP

iptables -A INPUT -p tcp --dport 7474 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 7687 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 7474 -j DROP
iptables -A INPUT -p tcp --dport 7687 -j DROP
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check all services
docker-compose ps

# View resource usage
docker stats

# Check logs
docker-compose logs -f --tail=100
```

### Backup Procedures

**MySQL Backup:**
```bash
docker-compose exec openspg-mysql mysqldump -uroot -popenspg openspg > backup-$(date +%Y%m%d).sql
```

**Neo4j Backup:**
```bash
# Stop Neo4j
docker-compose stop openspg-neo4j

# Copy data directory (if volume configured)
tar -czf neo4j-backup-$(date +%Y%m%d).tar.gz neo4j-data/

# Restart Neo4j
docker-compose start openspg-neo4j
```

**MinIO Backup:**
```bash
# Use MinIO client (mc)
docker run --rm --network host minio/mc \
  mirror openspg-minio/bucket backup-folder/
```

### Log Management

**View Service Logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f openspg-server

# Last N lines
docker-compose logs --tail=500 openspg-server
```

**Neo4j Log Location:**
```bash
# Logs persisted to host
ls -lah $HOME/dozerdb/logs/
```

---

## Troubleshooting

### Common Issues

**1. Server fails to start**
```bash
# Check if dependencies are healthy
docker-compose ps

# View server logs
docker-compose logs openspg-server

# Common causes:
# - MySQL not ready (wait 30s and retry)
# - Neo4j not ready (wait 60s and retry)
# - Insufficient memory (check docker stats)
```

**2. Out of memory errors**
```bash
# Reduce JVM heap size
JAVA_OPTS: -Xms1g -Xmx4g

# Reduce Neo4j memory
NEO4J_server_memory_heap_max__size: 2G
```

**3. Connection refused errors**
```bash
# Check service is listening
docker-compose exec openspg-mysql netstat -tlnp
docker-compose exec openspg-neo4j netstat -tlnp

# Check firewall
sudo iptables -L -n

# Check Docker network
docker network inspect openspg_default
```

**4. Data persistence issues**
```bash
# Add volumes as described in Data Persistence section
# Restart containers
docker-compose down
docker-compose up -d
```

### Debug Mode

```bash
# Start with verbose logging
docker-compose --verbose up

# Check Docker daemon logs
journalctl -u docker -f

# Inspect container
docker-compose exec openspg-server bash
```

---

## Scaling Considerations

### Horizontal Scaling Limitations

**Current architecture does NOT support:**
- Multiple OpenSPG Server instances (single instance only)
- MySQL replication not configured
- Neo4j clustering not configured
- MinIO distributed mode not configured

### Vertical Scaling

**Increase resources per service:**
```yaml
services:
  openspg-server:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 12G
        reservations:
          cpus: '2'
          memory: 8G
```

---

## Migration & Upgrade

### Upgrade Procedure

```bash
# 1. Backup data (see Backup Procedures)

# 2. Pull latest images
docker-compose pull

# 3. Stop services
docker-compose down

# 4. Start with new images
docker-compose up -d

# 5. Verify upgrade
docker-compose logs -f
```

### Rollback Procedure

```bash
# 1. Stop services
docker-compose down

# 2. Restore backup data

# 3. Pin image versions in docker-compose.yml
# Change: :latest → :v1.2.3

# 4. Start services
docker-compose up -d
```

---

## Production Deployment Checklist

- [ ] Change all default passwords
- [ ] Configure persistent volumes
- [ ] Enable SSL/TLS for all services
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Configure automated backups
- [ ] Document disaster recovery procedures
- [ ] Test backup restoration
- [ ] Configure log rotation
- [ ] Set up health checks
- [ ] Configure resource limits
- [ ] Review security settings
- [ ] Plan upgrade strategy
- [ ] Set up staging environment
- [ ] Document operational procedures

---

## Service Access URLs

**After deployment, access services at:**

| Service | URL | Credentials |
|---------|-----|-------------|
| OpenSPG API | http://localhost:8887 | N/A |
| Neo4j Browser | http://localhost:7474 | neo4j / neo4j@openspg |
| MinIO Console | http://localhost:9001 | minio / minio@openspg |
| MySQL | localhost:3306 | root / openspg |

---

## References

- **Docker Compose File:** https://raw.githubusercontent.com/OpenSPG/openspg/master/dev/release/docker-compose.yml
- **OpenSPG Repository:** https://github.com/OpenSPG/openspg
- **Docker Documentation:** https://docs.docker.com
- **Neo4j Documentation:** https://neo4j.com/docs
- **MinIO Documentation:** https://min.io/docs

---

## Version History

- **v1.0** (2025-10-26): Initial analysis of docker-compose deployment

---

**Analysis Status:** COMPLETE
**Deliverable:** Full docker-compose analysis with deployment guide, security recommendations, and operational procedures documented.
