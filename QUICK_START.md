# OpenSPG Quick Start Guide

## ⚡ 30-Second Deployment

```bash
cd /home/jim/2_OXOT_Projects_Dev
docker-compose up -d
```

Wait 2-3 minutes for health checks, then access:
- **OpenSPG UI**: http://localhost:8887 (openspg / openspg@kag)

## 📦 What's Running?

| Service | Container | Port(s) | Purpose |
|---------|-----------|---------|---------|
| OpenSPG | openspg-server | 8887 | Main app |
| MySQL | openspg-mysql | 3306 | Metadata |
| Neo4j | **openspg-neo4j** | 7474, 7687 | Graph DB |
| MinIO | openspg-minio | 9000, 9001 | Files |

## 🔑 Credentials

```yaml
OpenSPG: openspg / openspg@kag
Neo4j:   neo4j / neo4j@openspg
MySQL:   root / openspg
MinIO:   minio / minio@openspg
```

## 🔧 Essential Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose stop

# Status
docker-compose ps

# Logs
docker-compose logs -f

# Logs (single service)
docker-compose logs -f neo4j

# Restart
docker-compose restart

# Clean install (⚠️ deletes data)
docker-compose down -v
docker-compose up -d
```

## ✅ Verify Installation

```bash
# Check all services are healthy
docker-compose ps

# Test Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 'Connected!' AS status"

# Test MySQL
docker exec openspg-mysql mysql -u root -popenspg -e "SHOW DATABASES;"

# Access web interfaces
curl http://localhost:8887
curl http://localhost:7474
curl http://localhost:9001
```

## 🚨 Troubleshooting

### Neo4j won't start
```bash
# Check logs
docker logs openspg-neo4j --tail=50

# Common fix: increase memory
# Edit docker-compose.yml:
# NEO4J_server_memory_heap_max__size=8G

# Restart
docker-compose restart neo4j
```

### Port conflicts
```bash
# Check what's using ports
sudo netstat -tulpn | grep -E '3306|7474|7687|8887|9000|9001'

# Kill conflicting process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
# ports:
#   - "13306:3306"  # Changed MySQL to 13306
```

### OpenSPG can't connect to Neo4j
```bash
# Verify Neo4j is healthy
docker-compose ps

# Check network
docker exec openspg-server ping openspg-neo4j

# Check connection string in logs
docker logs openspg-server | grep neo4j

# Restart OpenSPG
docker-compose restart openspg-server
```

## 💾 Backup

```bash
# Quick backup (all data)
docker-compose stop
mkdir -p backups/$(date +%Y%m%d)
for vol in $(docker volume ls --format "{{.Name}}" | grep openspg); do
  docker run --rm -v $vol:/data -v $(pwd)/backups/$(date +%Y%m%d):/backup alpine tar czf /backup/${vol}.tar.gz /data
done
docker-compose start
```

## 🔄 Update

```bash
# Pull latest images
docker-compose pull

# Recreate containers (keeps data)
docker-compose up -d --force-recreate

# Verify
docker-compose ps
```

## 📊 Resource Usage

```bash
# Monitor containers
docker stats

# Check disk space
df -h
docker system df

# Clean unused data
docker system prune -a
```

## 🆘 Emergency Reset

```bash
# ⚠️ WARNING: Deletes ALL data!

# Stop and remove everything
docker-compose down -v

# Clean old data
docker volume prune -f
docker network prune -f

# Fresh start
docker-compose up -d
```

## 📚 Full Documentation

For complete documentation, see:
- **Deployment Guide**: `docs/OPENSPG_DEPLOYMENT_GUIDE.md`
- **README**: `README.md`
- **Docker Compose**: `docker-compose.yml`

## 🎯 Next Steps

1. ✅ Start services: `docker-compose up -d`
2. ✅ Verify health: `docker-compose ps`
3. ✅ Access UI: http://localhost:8887
4. ✅ Create first project
5. ✅ Import data
6. ✅ Build knowledge graph

## 💡 Pro Tips

- **Health Checks**: Wait for all services to show "healthy" status
- **Logs**: Use `docker-compose logs -f` to debug issues
- **Volumes**: Data persists across restarts (stored in Docker volumes)
- **Network**: All services communicate via `openspg-network`
- **Production**: Change default passwords before deploying!

---

**Quick Reference Created:** 2025-01-26
**Neo4j Version:** 5.26-community (LTS)
**Container Name:** openspg-neo4j ✅
