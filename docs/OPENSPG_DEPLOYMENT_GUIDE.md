# OpenSPG Production Deployment Guide

**Created:** 2025-01-26
**Version:** 1.0.0
**Neo4j Version:** 5.26-community (LTS)
**Status:** Production-Ready

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Architecture Overview](#architecture-overview)
4. [Configuration Details](#configuration-details)
5. [Data Persistence](#data-persistence)
6. [Health Checks](#health-checks)
7. [Access Information](#access-information)
8. [Troubleshooting](#troubleshooting)
9. [Production Considerations](#production-considerations)
10. [Backup & Recovery](#backup--recovery)

---

## 🚀 Quick Start

### Prerequisites
```bash
# Verify Docker and Docker Compose are installed
docker --version          # Requires Docker 20.10+
docker-compose --version  # Requires Docker Compose 2.0+

# Verify system resources
free -h                   # Check available RAM (16GB+ recommended)
df -h                     # Check available disk space (50GB+ recommended)
```

### Deployment Steps

```bash
# 1. Navigate to deployment directory
cd /home/jim/2_OXOT_Projects_Dev

# 2. Start all services
docker-compose up -d

# 3. Monitor startup progress
docker-compose logs -f

# 4. Verify all services are healthy
docker-compose ps

# Expected output:
# openspg-server   Up (healthy)   0.0.0.0:8887->8887/tcp
# openspg-mysql    Up (healthy)   0.0.0.0:3306->3306/tcp
# openspg-neo4j    Up (healthy)   0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp
# openspg-minio    Up (healthy)   0.0.0.0:9000->9000/tcp, 0.0.0.0:9001->9001/tcp

# 5. Wait for all health checks to pass (2-3 minutes)
watch -n 2 'docker-compose ps'
```

### First Access

```bash
# Access OpenSPG Web UI
open http://localhost:8887

# Default credentials:
# Username: openspg
# Password: openspg@kag

# Access Neo4j Browser
open http://localhost:7474

# Neo4j credentials:
# Username: neo4j
# Password: neo4j@openspg

# Access MinIO Console
open http://localhost:9001

# MinIO credentials:
# Username: minio
# Password: minio@openspg
```

---

## 💻 System Requirements

### Minimum Requirements
- **CPU:** 4 cores
- **RAM:** 16GB
- **Disk:** 50GB SSD
- **OS:** Linux, macOS, Windows (with WSL2)

### Recommended Requirements
- **CPU:** 8+ cores
- **RAM:** 32GB+
- **Disk:** 100GB+ SSD
- **OS:** Linux (Ubuntu 20.04+, CentOS 8+)

### Port Requirements
Ensure the following ports are available:
- `3306` - MySQL
- `7474` - Neo4j HTTP
- `7687` - Neo4j Bolt
- `8887` - OpenSPG Server
- `9000` - MinIO API
- `9001` - MinIO Console

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────┐
│         OpenSPG Server (8887)                   │
│   - REST API & Web UI                           │
│   - Knowledge Graph Management                  │
│   - KGDSL Reasoning Engine                      │
└──────────┬──────────────┬───────────┬──────────┘
           │              │           │
     ┌─────▼─────┐  ┌────▼────┐  ┌──▼─────┐
     │   MySQL   │  │  Neo4j  │  │ MinIO  │
     │   (3306)  │  │ 7474/87 │  │ 9000/1 │
     │           │  │         │  │        │
     │ Metadata  │  │ Graph + │  │  File  │
     │  Schema   │  │ Search  │  │Storage │
     │  Users    │  │ APOC    │  │   S3   │
     └───────────┘  └─────────┘  └────────┘
```

### Container Roles

| Container | Purpose | Dependencies | Data Persistence |
|-----------|---------|--------------|------------------|
| **openspg-server** | Main application | mysql, neo4j, minio | `/app/logs` |
| **openspg-mysql** | Schema & metadata | None | `/var/lib/mysql` |
| **openspg-neo4j** | Graph storage + search | None | `/data`, `/logs` |
| **openspg-minio** | File storage | None | `/data` |

---

## ⚙️ Configuration Details

### OpenSPG Server Configuration

**Memory Allocation:**
```yaml
Initial Heap: 2GB (-Xms2048m)
Maximum Heap: 8GB (-Xmx8192m)
```

**Key Parameters:**
```bash
--server.repository.impl.jdbc.host=mysql
--builder.model.execute.num=20              # Concurrent processing threads
--cloudext.graphstore.url=neo4j://...       # Graph database connection
--cloudext.searchengine.url=neo4j://...     # Search engine connection
```

### MySQL Configuration

**Database Settings:**
```yaml
Character Set: utf8mb4
Collation: utf8mb4_general_ci
Max Connections: 1000
Buffer Pool Size: 2GB
Authentication: mysql_native_password
```

**Default Database:** `openspg`
**Root Password:** `openspg` (⚠️ Change in production!)

### Neo4j Configuration

**Version:** Neo4j 5.26 Community (LTS)
**Container Name:** `openspg-neo4j` (as requested)

**Memory Settings:**
```yaml
Initial Heap: 2GB
Maximum Heap: 4GB
Page Cache: 2GB
Transaction Memory: 2GB
```

**APOC Plugin:**
- ✅ Installed and enabled
- ✅ Export/import enabled
- ✅ All procedures unrestricted

**Performance Tuning:**
```yaml
Transaction Log Retention: 2GB size-based rotation
Bolt Protocol: Enabled (0.0.0.0:7687)
HTTP Protocol: Enabled (0.0.0.0:7474)
Default Database: neo4j
```

### MinIO Configuration

**Storage Backend:** S3-compatible object storage
**Access:** API (9000), Console (9001)
**Credentials:**
- User: `minio`
- Password: `minio@openspg`

---

## 💾 Data Persistence

All data is persisted using Docker named volumes:

### Volume Mapping

| Volume Name | Service | Mount Point | Purpose |
|-------------|---------|-------------|---------|
| `openspg-mysql-data` | MySQL | `/var/lib/mysql` | Database files |
| `openspg-mysql-logs` | MySQL | `/var/log/mysql` | MySQL logs |
| `openspg-neo4j-data` | Neo4j | `/data` | Graph database |
| `openspg-neo4j-logs` | Neo4j | `/logs` | Neo4j logs |
| `openspg-neo4j-import` | Neo4j | `/var/lib/neo4j/import` | Import directory |
| `openspg-neo4j-plugins` | Neo4j | `/plugins` | APOC plugins |
| `openspg-minio-data` | MinIO | `/data` | Object storage |
| `openspg-server-logs` | Server | `/app/logs` | Application logs |

### Volume Management

```bash
# List all volumes
docker volume ls | grep openspg

# Inspect a volume
docker volume inspect openspg-neo4j-data

# Backup a volume
docker run --rm -v openspg-neo4j-data:/data -v $(pwd):/backup alpine tar czf /backup/neo4j-backup.tar.gz /data

# Restore a volume
docker run --rm -v openspg-neo4j-data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/neo4j-backup.tar.gz --strip 1"

# Remove all volumes (⚠️ DANGER: Data loss!)
docker-compose down -v
```

---

## 🏥 Health Checks

### Automated Health Monitoring

Each service includes health checks:

**OpenSPG Server:**
```yaml
Check: curl -f http://localhost:8887/health
Interval: 30s
Timeout: 10s
Start Period: 60s
```

**MySQL:**
```yaml
Check: mysqladmin ping
Interval: 10s
Timeout: 5s
Start Period: 30s
```

**Neo4j:**
```yaml
Check: cypher-shell -u neo4j -p neo4j@openspg "RETURN 1"
Interval: 10s
Timeout: 10s
Start Period: 60s
```

**MinIO:**
```yaml
Check: curl -f http://localhost:9000/minio/health/live
Interval: 30s
Timeout: 10s
Start Period: 10s
```

### Manual Health Verification

```bash
# Check service status
docker-compose ps

# Check logs for errors
docker-compose logs --tail=100 openspg-server
docker-compose logs --tail=100 openspg-neo4j

# Verify Neo4j connectivity
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "MATCH (n) RETURN count(n) AS nodeCount"

# Verify MySQL connectivity
docker exec openspg-mysql mysql -u root -popenspg -e "SHOW DATABASES;"

# Verify MinIO connectivity
curl http://localhost:9000/minio/health/live
```

---

## 🔐 Access Information

### Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **OpenSPG Web UI** | http://localhost:8887 | Main application interface |
| **OpenSPG API** | http://localhost:8887/api | REST API endpoints |
| **Neo4j Browser** | http://localhost:7474 | Graph database browser |
| **MinIO Console** | http://localhost:9001 | Object storage console |

### Default Credentials

| Service | Username | Password | Notes |
|---------|----------|----------|-------|
| **OpenSPG** | `openspg` | `openspg@kag` | Web UI login |
| **Neo4j** | `neo4j` | `neo4j@openspg` | Database access |
| **MySQL** | `root` | `openspg` | Root access |
| **MinIO** | `minio` | `minio@openspg` | Storage admin |

⚠️ **SECURITY WARNING:** Change all default passwords in production!

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Services Won't Start

```bash
# Check port conflicts
sudo netstat -tulpn | grep -E '3306|7474|7687|8887|9000|9001'

# Kill conflicting processes or change ports in docker-compose.yml
sudo kill -9 <PID>

# Restart services
docker-compose restart
```

#### 2. Neo4j Container Fails Health Check

```bash
# Check Neo4j logs
docker logs openspg-neo4j --tail=100

# Common issues:
# - Memory: Increase heap size in docker-compose.yml
# - APOC: Verify plugin is installed
# - Password: Ensure NEO4J_AUTH format is correct

# Manual verification
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"
```

#### 3. OpenSPG Server Can't Connect to Neo4j

```bash
# Verify network connectivity
docker exec openspg-server ping openspg-neo4j

# Check connection string in logs
docker logs openspg-server | grep "cloudext.graphstore.url"

# Verify Neo4j is accepting connections
docker exec openspg-neo4j netstat -tulpn | grep 7687
```

#### 4. Out of Memory Errors

```bash
# Check container resource usage
docker stats

# Adjust memory limits in docker-compose.yml:
# - Increase Neo4j heap: NEO4J_server_memory_heap_max__size
# - Increase OpenSPG heap: -Xmx parameter
# - Increase system swap space

# Restart with new configuration
docker-compose down
docker-compose up -d
```

#### 5. Data Not Persisting

```bash
# Verify volumes exist
docker volume ls | grep openspg

# Check volume mounts
docker inspect openspg-neo4j | grep Mounts -A 20

# Recreate volumes if corrupted
docker-compose down
docker volume rm openspg-neo4j-data
docker-compose up -d
```

### Log Analysis

```bash
# View all logs
docker-compose logs -f

# Service-specific logs
docker-compose logs -f openspg-server
docker-compose logs -f openspg-neo4j

# Filter for errors
docker-compose logs | grep -i error

# Export logs to file
docker-compose logs > openspg-logs.txt
```

---

## 🏭 Production Considerations

### Security Hardening

```bash
# 1. Change all default passwords
# Edit docker-compose.yml:
# - NEO4J_AUTH=neo4j/YOUR_STRONG_PASSWORD
# - MYSQL_ROOT_PASSWORD=YOUR_STRONG_PASSWORD
# - MINIO_ROOT_PASSWORD=YOUR_STRONG_PASSWORD

# 2. Restrict network access
# Add firewall rules:
sudo ufw allow 8887/tcp  # OpenSPG only
sudo ufw deny 3306/tcp   # MySQL (internal only)
sudo ufw deny 7474/tcp   # Neo4j (internal only)
sudo ufw deny 9000/tcp   # MinIO (internal only)

# 3. Enable SSL/TLS
# Configure reverse proxy (nginx/traefik) with Let's Encrypt certificates

# 4. Implement authentication
# Configure OpenSPG RBAC and user management

# 5. Regular security updates
docker-compose pull
docker-compose up -d
```

### Performance Tuning

```yaml
# For high-load production environments:

# OpenSPG Server:
JAVA_OPTS: "-Xms4096m -Xmx16384m"
builder.model.execute.num: 50  # Increase concurrent threads

# MySQL:
innodb_buffer_pool_size: 8G
max_connections: 2000

# Neo4j:
NEO4J_server_memory_heap_max__size: 16G
NEO4J_server_memory_pagecache_size: 8G
NEO4J_dbms_memory_transaction_total_max: 4G

# System:
# Increase ulimits, disable swap, use SSD storage
```

### Monitoring Setup

```bash
# Install monitoring stack (Prometheus + Grafana)
# Add to docker-compose.yml:

prometheus:
  image: prom/prometheus:latest
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 💾 Backup & Recovery

### Automated Backup Script

Create `/home/jim/2_OXOT_Projects_Dev/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backup/openspg/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Starting OpenSPG backup..."

# Backup MySQL
docker exec openspg-mysql mysqldump -u root -popenspg --all-databases > "$BACKUP_DIR/mysql-backup.sql"

# Backup Neo4j
docker exec openspg-neo4j neo4j-admin database dump neo4j --to-path=/tmp
docker cp openspg-neo4j:/tmp/neo4j.dump "$BACKUP_DIR/neo4j-backup.dump"

# Backup MinIO data
docker run --rm -v openspg-minio-data:/data -v "$BACKUP_DIR":/backup alpine tar czf /backup/minio-backup.tar.gz /data

echo "Backup completed: $BACKUP_DIR"

# Keep only last 7 days
find /backup/openspg -type d -mtime +7 -exec rm -rf {} +
```

Make executable and schedule:
```bash
chmod +x backup.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /home/jim/2_OXOT_Projects_Dev/backup.sh" | crontab -
```

### Manual Backup

```bash
# Stop services gracefully
docker-compose stop

# Backup all volumes
for vol in $(docker volume ls --format "{{.Name}}" | grep openspg); do
  docker run --rm -v $vol:/data -v $(pwd)/backup:/backup alpine tar czf /backup/${vol}-$(date +%Y%m%d).tar.gz /data
done

# Restart services
docker-compose start
```

### Recovery Process

```bash
# 1. Stop all services
docker-compose down

# 2. Remove existing volumes
docker volume rm openspg-neo4j-data openspg-mysql-data openspg-minio-data

# 3. Restore from backup
docker volume create openspg-neo4j-data
docker run --rm -v openspg-neo4j-data:/data -v $(pwd)/backup:/backup alpine sh -c "cd /data && tar xzf /backup/openspg-neo4j-data-20250126.tar.gz --strip 1"

# Repeat for other volumes

# 4. Restart services
docker-compose up -d

# 5. Verify data integrity
docker-compose logs -f
```

---

## 📊 Resource Monitoring

### Real-Time Monitoring

```bash
# Container resource usage
docker stats

# System resource usage
htop

# Disk usage
df -h
du -sh /var/lib/docker/volumes/*
```

### Log Rotation

Create `/etc/logrotate.d/docker-compose`:

```
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  size 10M
  missingok
  delaycompress
  copytruncate
}
```

---

## 🎯 Production Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Configure SSL/TLS certificates
- [ ] Set up automated backups
- [ ] Configure monitoring and alerting
- [ ] Implement log aggregation
- [ ] Set resource limits and quotas
- [ ] Configure firewall rules
- [ ] Test disaster recovery procedures
- [ ] Document custom configurations
- [ ] Set up CI/CD pipelines
- [ ] Configure auto-scaling (if using orchestrator)
- [ ] Implement rate limiting
- [ ] Set up external authentication (LDAP/OAuth)
- [ ] Configure data retention policies
- [ ] Perform load testing
- [ ] Create runbooks for common issues

---

## 📚 Additional Resources

- **OpenSPG Documentation**: https://openspg.github.io/v2/docs_en
- **Neo4j Operations Manual**: https://neo4j.com/docs/operations-manual/current/
- **Docker Compose Reference**: https://docs.docker.com/compose/compose-file/
- **MinIO Documentation**: https://min.io/docs/minio/linux/index.html

---

## 🆘 Support

For issues and questions:
- **GitHub Issues**: https://github.com/OpenSPG/openspg/issues
- **Community**: OpenKG collaboration platform
- **Documentation**: https://openspg.yuque.com/ndx6g9/docs_en

---

**Document Version:** 1.0.0
**Last Updated:** 2025-01-26
**Maintainer:** OpenSPG Community
