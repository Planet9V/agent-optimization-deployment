# AEON UI - Docker Quick Start

## One-Command Deployment

```bash
./scripts/deploy.sh start
```

## Prerequisites Check

```bash
# 1. Verify OpenSPG network exists
docker network inspect openspg-network

# 2. Ensure environment file exists
ls -l .env.production
```

## Configuration (First Time Only)

```bash
# Generate secure secret
openssl rand -base64 32

# Edit .env.production (paste the secret)
nano .env.production
# Update: NEXTAUTH_SECRET=<paste-secret-here>
```

## Deployment Commands

```bash
# Start service
./scripts/deploy.sh start

# Stop service
./scripts/deploy.sh stop

# Restart service
./scripts/deploy.sh restart

# View logs
./scripts/deploy.sh logs

# Check health
./scripts/deploy.sh health

# Show status
./scripts/deploy.sh status
```

## Access Points

- **Web UI**: http://localhost:3000
- **Health Check**: http://localhost:3000/api/health
- **Container IP**: http://172.18.0.8:3000 (internal)

## Verification

```bash
# Test health endpoint
curl http://localhost:3000/api/health

# Check service status
docker-compose -f docker-compose.aeon-ui.yml ps

# View recent logs
docker-compose -f docker-compose.aeon-ui.yml logs --tail=50
```

## Troubleshooting

### Service won't start
```bash
# Check OpenSPG infrastructure
docker ps | grep openspg

# Check network
docker network inspect openspg-network

# View errors
./scripts/deploy.sh logs
```

### Health check failing
```bash
# Wait 60 seconds for startup
sleep 60

# Check health manually
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui wget -O- http://localhost:3000/api/health
```

### Database connection issues
```bash
# Test Neo4j connectivity
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui ping openspg-neo4j

# Test MySQL connectivity
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui ping openspg-mysql

# Check environment variables
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui env | grep -E '(NEO4J|MYSQL)'
```

## Manual Docker Commands

```bash
# Build image
docker-compose -f docker-compose.aeon-ui.yml build

# Start in foreground (for debugging)
docker-compose -f docker-compose.aeon-ui.yml up

# Start in background
docker-compose -f docker-compose.aeon-ui.yml up -d

# Stop and remove
docker-compose -f docker-compose.aeon-ui.yml down

# Rebuild and restart
docker-compose -f docker-compose.aeon-ui.yml up -d --build
```

## Network Configuration

```
openspg-network (172.18.0.0/16)
├── 172.18.0.2 → openspg-neo4j
├── 172.18.0.3 → openspg-mysql
├── 172.18.0.4 → openspg-qdrant
├── 172.18.0.5 → openspg-minio
├── 172.18.0.6 → openspg-server
└── 172.18.0.8 → aeon-ui ← THIS SERVICE
```

## Documentation

- **Full Guide**: `/docs/DOCKER_DEPLOYMENT.md`
- **Configuration**: `/docker-compose.aeon-ui.yml`
- **Summary**: `/DEPLOYMENT_SUMMARY.md`

---

**Quick Start**: `./scripts/deploy.sh start` → http://localhost:3000
