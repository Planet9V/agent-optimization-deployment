# AEON Backend API Deployment Steps

**File:** DEPLOYMENT_STEPS.md
**Created:** 2025-11-08
**Purpose:** Step-by-step deployment guide with validation gates
**Status:** ACTIVE

## Overview

This guide provides detailed steps for deploying AEON backend APIs in development and production environments.

## Prerequisites

- Docker and Docker Compose installed
- Git repository access
- Environment configuration prepared
- Deployment checklist completed

## Deployment Methods

### Method 1: Individual Scripts (Recommended for Development)
### Method 2: Docker Compose (Recommended for Production)

---

## Method 1: Individual Script Deployment

### Step 1: Initial Setup

```bash
# Navigate to project root
cd "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE"

# Run environment setup
./deployment/scripts/setup_environment.sh
```

**Validation:**
- Environment file created: `.env`
- Required directories created
- Scripts are executable
- Neo4j container running (optional)

### Step 2: Configure Environment

```bash
# Edit environment file
nano .env

# Required settings:
# - NEO4J_URI
# - NEO4J_USER
# - NEO4J_PASSWORD
# - NER_API_PORT (default: 8000)
# - QUERY_API_PORT (default: 8001)
```

**Validation:**
- All required variables set
- Neo4j credentials correct
- Ports available

### Step 3: Deploy NER API

```bash
# Deploy NER v8 API
./deployment/scripts/deploy_ner_v8_api.sh
```

**Process:**
1. Environment validation
2. Docker image build
3. Container deployment
4. Health check (10 retries, 5s interval)
5. Integration test

**Validation Gate:**
- Container running: `docker ps | grep aeon-ner-api`
- Health check passing: `curl http://localhost:8000/health`
- API docs accessible: http://localhost:8000/docs

**Expected Output:**
```
[INFO] Starting NER v8 API deployment...
[INFO] Validating environment...
[INFO] Building Docker image: aeon-ner-api:latest
[INFO] Container deployed successfully
[INFO] Health check passed
[INFO] NER endpoint test passed
=========================================
NER v8 API deployment completed successfully!
API URL: http://localhost:8000
=========================================
```

### Step 4: Deploy Query API

```bash
# Deploy Query Execution API
./deployment/scripts/deploy_query_api.sh
```

**Process:**
1. Environment validation
2. Docker image build
3. Container deployment
4. Health check
5. Integration test

**Validation Gate:**
- Container running: `docker ps | grep aeon-query-api`
- Health check passing: `curl http://localhost:8001/health`
- API docs accessible: http://localhost:8001/docs

### Step 5: Comprehensive Health Check

```bash
# Run full system health check
./deployment/scripts/health_check_all.sh
```

**Checks Performed:**
- NER API health
- Query API health
- Neo4j connectivity
- Docker container status
- Functional tests
- System resources

**Validation Gate:**
- All health checks passing
- No errors in logs
- Integration tests successful

**Expected Output:**
```
========================================
AEON Backend API Health Check
========================================

Service Health Checks:
[INFO] ✓ NER API is healthy
[INFO] ✓ Query API is healthy
[INFO] ✓ Neo4j is reachable

Docker Container Status:
[INFO] ✓ Container 'aeon-ner-api': running (Health: healthy)
[INFO] ✓ Container 'aeon-query-api': running (Health: healthy)
[INFO] ✓ Container 'neo4j': running (Health: healthy)

NER API Functional Test:
[INFO] ✓ NER API functional test passed (3 entities extracted)

Query API Functional Test:
[INFO] ✓ Query API functional test passed (3 results)

Health Check Summary:
Total checks: 8
Passed: 8
Failed: 0

Success rate: 100%

✓ All health checks passed!
```

---

## Method 2: Docker Compose Deployment

### Step 1: Configuration

```bash
# Navigate to project root
cd "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE"

# Configure environment
cp .env.example .env
nano .env
```

### Step 2: Build Images

```bash
cd deployment/docker

# Build all images
docker-compose build

# Verify builds
docker images | grep aeon
```

**Validation:**
- `aeon-ner-api:latest` exists
- `aeon-query-api:latest` exists
- No build errors

### Step 3: Start Services (Development)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

**Validation:**
- All containers running: `docker-compose ps`
- Health checks passing
- No errors in logs

### Step 4: Start Services (Production)

```bash
# Start with production overrides
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Verify deployment
docker-compose ps
```

**Production Features:**
- Increased resource limits
- Multiple replicas
- Monitoring stack (Prometheus + Grafana)
- Production logging

### Step 5: Verify Deployment

```bash
# Health checks
curl http://localhost:8000/health  # NER API
curl http://localhost:8001/health  # Query API
curl http://localhost:7474         # Neo4j Browser

# Run comprehensive check
cd ../..
./deployment/scripts/health_check_all.sh
```

---

## Post-Deployment Validation

### Immediate Validation (0-5 minutes)

```bash
# Check container status
docker ps

# Check logs for errors
docker logs aeon-ner-api --tail 50
docker logs aeon-query-api --tail 50
docker logs neo4j --tail 50

# Test API endpoints
curl -X POST http://localhost:8000/api/v1/extract-entities \
  -H "Content-Type: application/json" \
  -d '{"text": "MITRE ATT&CK describes APT29 tactics"}'

curl -X POST http://localhost:8001/api/v1/query/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "MATCH (n:Technique) RETURN n.name LIMIT 5"}'
```

### Short-term Monitoring (5-30 minutes)

```bash
# Monitor logs continuously
docker logs -f aeon-ner-api

# Watch resource usage
docker stats aeon-ner-api aeon-query-api neo4j

# Run health check every 5 minutes
watch -n 300 ./deployment/scripts/health_check_all.sh
```

### Extended Monitoring (30+ minutes)

- Check Prometheus metrics: http://localhost:9090
- View Grafana dashboards: http://localhost:3000
- Monitor error rates
- Track response times
- Review log aggregations

---

## Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Stop conflicting service
docker stop <container_name>

# Or use different port
export NER_API_PORT=8002
./deployment/scripts/deploy_ner_v8_api.sh
```

### Issue: Neo4j Connection Failed

```bash
# Check Neo4j status
docker logs neo4j

# Test connection
docker exec -it neo4j cypher-shell -u neo4j -p changeme

# Restart Neo4j
docker restart neo4j
```

### Issue: Health Check Failing

```bash
# Check container logs
docker logs aeon-ner-api

# Check inside container
docker exec -it aeon-ner-api bash
curl http://localhost:8000/health

# Restart container
docker restart aeon-ner-api
```

### Issue: Build Failures

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check disk space
df -h
```

---

## Rollback Procedure

### Quick Rollback

```bash
./deployment/scripts/rollback_deployment.sh
```

Follow on-screen menu to:
1. Rollback NER API
2. Rollback Query API
3. Rollback both APIs
4. Rollback to specific tag

### Manual Rollback

```bash
# Stop current containers
docker stop aeon-ner-api aeon-query-api
docker rm aeon-ner-api aeon-query-api

# Restore backup images
docker tag aeon-ner-api:latest.backup aeon-ner-api:latest
docker tag aeon-query-api:latest.backup aeon-query-api:latest

# Redeploy
./deployment/scripts/deploy_ner_v8_api.sh
./deployment/scripts/deploy_query_api.sh
```

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Health check
./deployment/scripts/health_check_all.sh

# Log review
docker logs aeon-ner-api --since 24h | grep ERROR
docker logs aeon-query-api --since 24h | grep ERROR
```

### Weekly Maintenance

- Review metrics and trends
- Check disk space
- Update dependencies
- Review security alerts
- Performance optimization

### Monthly Tasks

- Security updates
- Dependency updates
- Performance review
- Capacity planning
- Disaster recovery test

---

## Production Deployment Checklist

- [ ] All pre-deployment checks completed
- [ ] Stakeholders notified
- [ ] Maintenance window scheduled
- [ ] Backup created
- [ ] Deployment executed
- [ ] Validation completed
- [ ] Monitoring confirmed
- [ ] Stakeholders notified of completion
- [ ] Documentation updated

---

## Support & Resources

**Scripts Location:** `/deployment/scripts/`
- `deploy_ner_v8_api.sh` - Deploy NER API
- `deploy_query_api.sh` - Deploy Query API
- `health_check_all.sh` - Comprehensive health check
- `rollback_deployment.sh` - Rollback procedure
- `setup_environment.sh` - Environment setup

**Docker Location:** `/deployment/docker/`
- `Dockerfile.ner_api` - NER API image
- `Dockerfile.query_api` - Query API image
- `docker-compose.yml` - Service orchestration
- `docker-compose.prod.yml` - Production overrides

**Documentation:** `/deployment/docs/`
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment checklist
- `DEPLOYMENT_STEPS.md` - This guide
- `ROLLBACK_PROCEDURES.md` - Rollback guide
- `MONITORING_SETUP.md` - Monitoring configuration

---

**Last Updated:** 2025-11-08
**Version:** 1.0
