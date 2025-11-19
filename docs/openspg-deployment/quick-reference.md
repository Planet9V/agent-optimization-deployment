# OpenSPG Docker Compose - Quick Reference

**File:** 2025-10-26_OpenSPG_Quick-Reference.md
**Purpose:** Quick deployment and troubleshooting reference

---

## Quick Deploy Commands

```bash
# Download and start
curl -o docker-compose.yml https://raw.githubusercontent.com/OpenSPG/openspg/master/dev/release/docker-compose.yml
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f openspg-server
```

---

## Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| OpenSPG Server | 8887 | API endpoint |
| MySQL | 3306 | Database |
| Neo4j Browser | 7474 | Web UI |
| Neo4j Bolt | 7687 | Graph queries |
| MinIO API | 9000 | S3 API |
| MinIO Console | 9001 | Web UI |

---

## Default Credentials

| Service | Username | Password |
|---------|----------|----------|
| MySQL | root | openspg |
| Neo4j | neo4j | neo4j@openspg |
| MinIO | minio | minio@openspg |

**⚠️ CHANGE THESE IN PRODUCTION!**

---

## Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart single service
docker-compose restart openspg-server

# View logs
docker-compose logs -f [service-name]

# Execute command in container
docker-compose exec openspg-server bash
docker-compose exec openspg-mysql mysql -uroot -popenspg

# Check resource usage
docker stats

# Update images
docker-compose pull
docker-compose up -d
```

---

## Quick Troubleshooting

**Server won't start:**
```bash
# Check dependencies are healthy
docker-compose ps
docker-compose logs openspg-mysql
docker-compose logs openspg-neo4j
```

**Out of memory:**
```bash
# Reduce heap in docker-compose.yml
JAVA_OPTS: -Xms1g -Xmx4g
```

**Connection errors:**
```bash
# Check service is running
docker-compose ps

# Test connectivity
curl http://localhost:8887
curl http://localhost:7474
curl http://localhost:9000/minio/health/live
```

---

## Resource Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 16GB
- Disk: 20GB

**Recommended:**
- CPU: 8 cores
- RAM: 24GB
- Disk: 100GB SSD

---

## Backup Commands

```bash
# MySQL backup
docker-compose exec openspg-mysql mysqldump -uroot -popenspg openspg > backup.sql

# Neo4j backup (requires volume configuration)
tar -czf neo4j-backup.tar.gz neo4j-data/

# Restore MySQL
docker-compose exec -T openspg-mysql mysql -uroot -popenspg openspg < backup.sql
```

---

## Production Security Checklist

- [ ] Change MySQL root password
- [ ] Change Neo4j password
- [ ] Change MinIO credentials
- [ ] Add persistent volumes
- [ ] Configure firewall
- [ ] Enable SSL/TLS
- [ ] Set up backups
- [ ] Configure monitoring

---

## Service URLs

- **OpenSPG API:** http://localhost:8887
- **Neo4j Browser:** http://localhost:7474
- **MinIO Console:** http://localhost:9001

---

**Status:** COMPLETE
