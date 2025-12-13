# Service Management Procedures

**File:** SERVICE_CONTROL.md
**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** Service lifecycle management and control procedures
**Status:** ACTIVE

## Executive Summary

Complete procedures for starting, stopping, restarting, and scaling individual services with health verification and data persistence guarantees.

**Critical Principle:** Always verify data persistence and health status after service operations.

---

## Service Dependency Map

```
┌─────────────┐
│  Frontend   │ (Port 3000)
│  (React)    │
└──────┬──────┘
       │ depends on
       ▼
┌─────────────┐
│     API     │ (Port 8000)
│  (FastAPI)  │
└──────┬──────┘
       │ depends on
       ▼
┌─────────────┐
│  PostgreSQL │ (Port 5432)
│  (Database) │
└─────────────┘
```

**Startup Order (Required):**
1. PostgreSQL (database layer)
2. API (application layer)
3. Frontend (presentation layer)

**Shutdown Order (Required):**
1. Frontend (graceful connection closure)
2. API (complete pending requests)
3. PostgreSQL (flush WAL, checkpoint data)

---

## Starting Individual Services

### Start PostgreSQL Database

```bash
# Start database container only
docker-compose up -d postgres

# Wait for initialization (30-60 seconds)
echo "Waiting for PostgreSQL..."
sleep 15

# Verify database is ready
docker-compose exec postgres pg_isready -U postgres
# Expected: "/var/run/postgresql:5432 - accepting connections"

# Check database logs for errors
docker-compose logs postgres | tail -20

# Verify data volume is mounted
docker-compose exec postgres ls -lh /var/lib/postgresql/data
# Expected: Directory with database files (base/, global/, pg_wal/)

# Test connection with psql
docker-compose exec postgres psql -U postgres -c "SELECT version();"
# Expected: PostgreSQL version information
```

**Health Verification:**
```bash
# Check active connections
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
# Expected: At least 1 connection

# Verify disk space
docker-compose exec postgres df -h /var/lib/postgresql/data
# Expected: Sufficient space available (>5GB recommended)

# Check replication status (if applicable)
docker-compose exec postgres psql -U postgres -c "SELECT * FROM pg_stat_replication;"
```

**Troubleshooting:**
- **Container exits immediately:** Check logs for initialization errors
  ```bash
  docker-compose logs postgres | grep -E "FATAL|ERROR"
  ```
- **Port already in use:** Check if another PostgreSQL instance is running
  ```bash
  lsof -i :5432
  sudo systemctl status postgresql  # Linux
  ```
- **Permission denied errors:** Fix volume permissions
  ```bash
  docker-compose down
  sudo chown -R 999:999 volumes/postgres_data/
  docker-compose up -d postgres
  ```

---

### Start API Service

```bash
# Ensure PostgreSQL is running first
docker-compose ps postgres | grep -q "Up" || docker-compose up -d postgres
sleep 10

# Start API container
docker-compose up -d api

# Monitor startup logs
docker-compose logs -f api --tail=50

# Wait for "Application startup complete" message
# Expected within 60 seconds
```

**Health Verification:**
```bash
# Wait for API initialization
sleep 20

# Test health endpoint
curl -X GET http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "...", "version": "..."}

# Test database connectivity
curl -X GET http://localhost:8000/api/v1/db/health
# Expected: {"database": "connected", "pool_size": 10}

# Test model loading
curl -X GET http://localhost:8000/api/v1/models/status
# Expected: {"models_loaded": true}

# Verify API documentation accessible
curl -I http://localhost:8000/docs
# Expected: HTTP/1.1 200 OK

# Check container resource usage
docker stats ner11_api_1 --no-stream
# Expected: CPU <50%, Memory <2GB under normal load
```

**Troubleshooting:**
- **Database connection failed:** Verify PostgreSQL is accessible
  ```bash
  docker-compose exec api nc -zv postgres 5432
  # Expected: Connection to postgres 5432 port [tcp/postgresql] succeeded!
  ```
- **Model loading failed:** Check model files exist and are readable
  ```bash
  docker-compose exec api ls -lh /app/models/
  ```
- **Port 8000 already in use:** Identify and stop conflicting process
  ```bash
  lsof -i :8000
  kill -9 <PID>  # Or modify docker-compose.yml port mapping
  ```

---

### Start Frontend Service

```bash
# Ensure API is running first
docker-compose ps api | grep -q "Up" || docker-compose up -d postgres api
sleep 15

# Start frontend container
docker-compose up -d frontend

# Monitor build process
docker-compose logs -f frontend --tail=50

# Wait for "webpack compiled successfully" message
# Expected within 120 seconds
```

**Health Verification:**
```bash
# Wait for build completion
sleep 30

# Test frontend accessibility
curl -I http://localhost:3000
# Expected: HTTP/1.1 200 OK

# Test React app loaded
curl -s http://localhost:3000 | grep -o "<div id=\"root\">"
# Expected: <div id="root">

# Test API proxy working
curl -s http://localhost:3000/api/v1/health | jq '.'
# Expected: API health response

# Verify static assets served
curl -I http://localhost:3000/static/js/main.chunk.js
# Expected: HTTP/1.1 200 OK, Content-Type: application/javascript

# Check container resource usage
docker stats ner11_frontend_1 --no-stream
# Expected: CPU <30%, Memory <512MB
```

**Troubleshooting:**
- **Build fails:** Check Node.js version and dependencies
  ```bash
  docker-compose exec frontend node --version
  docker-compose exec frontend npm ls
  ```
- **API proxy not working:** Verify proxy configuration
  ```bash
  docker-compose exec frontend cat package.json | grep -A 5 "proxy"
  ```
- **Port 3000 already in use:** Change port mapping or stop conflicting process
  ```bash
  # Edit docker-compose.yml: "3001:3000" instead of "3000:3000"
  docker-compose up -d frontend
  ```

---

## Stopping Services Gracefully

### Stop Frontend (Presentation Layer First)

```bash
# Graceful shutdown with 30-second timeout
docker-compose stop -t 30 frontend

# Verify container stopped
docker-compose ps frontend
# Expected: State = "Exit 0"

# Check for orphaned processes
docker-compose ps -a | grep frontend
# Expected: One stopped container only

# Verify no lingering network connections
netstat -an | grep :3000
# Expected: No output (port released)
```

**Data Persistence Verification:**
```bash
# Frontend has no persistent data, but verify logs if needed
docker-compose logs frontend --tail=50 > logs/frontend_last_session.log
```

---

### Stop API (Application Layer Second)

```bash
# Allow time for pending requests to complete
echo "Waiting for active requests to complete..."
sleep 5

# Graceful shutdown with 60-second timeout (for pending transactions)
docker-compose stop -t 60 api

# Verify container stopped cleanly
docker-compose ps api
# Expected: State = "Exit 0" (not "Exit 137" which indicates SIGKILL)

# Check for database connection cleanup
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity WHERE application_name = 'fastapi';"
# Expected: 0 connections
```

**Data Persistence Verification:**
```bash
# Verify API logs preserved
docker-compose logs api --tail=100 > logs/api_last_session.log

# Check for uncommitted transactions (should be 0)
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'idle in transaction';"
# Expected: 0
```

**Troubleshooting:**
- **Container won't stop (timeout):** Force kill and investigate
  ```bash
  docker-compose kill api
  docker-compose logs api | grep -E "ERROR|FATAL" | tail -20
  ```
- **Database connections not released:** Manually terminate
  ```bash
  docker-compose exec postgres psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE application_name = 'fastapi';"
  ```

---

### Stop PostgreSQL (Database Layer Last)

```bash
# Ensure API is stopped first
docker-compose ps api | grep -q "Up" && docker-compose stop -t 60 api

# Allow PostgreSQL to flush WAL and checkpoint
echo "Flushing PostgreSQL write-ahead log..."
docker-compose exec postgres psql -U postgres -c "CHECKPOINT;"

# Graceful shutdown with 120-second timeout (for checkpoint completion)
docker-compose stop -t 120 postgres

# Verify clean shutdown in logs
docker-compose logs postgres | tail -20 | grep -E "database system is shut down|shutdown complete"
# Expected: "database system is shut down"
```

**Data Persistence Verification:**
```bash
# Verify WAL files flushed
docker-compose exec postgres ls -lh /var/lib/postgresql/data/pg_wal/
# Expected: Minimal WAL files (only checkpoint segments)

# Check data directory integrity
docker volume inspect ner11_postgres_data
# Expected: Volume exists and is not corrupted

# Verify last checkpoint time (when restarted)
# docker-compose up -d postgres
# docker-compose exec postgres psql -U postgres -c "SELECT pg_last_xact_replay_timestamp();"
```

**Troubleshooting:**
- **Shutdown timeout:** Data is still being written, extend timeout or force stop
  ```bash
  docker-compose stop -t 180 postgres  # 3 minutes
  # If still timing out:
  docker-compose kill postgres
  # Check for corruption on restart
  ```
- **Data corruption suspected:** Run integrity check on restart
  ```bash
  docker-compose up -d postgres
  docker-compose exec postgres psql -U postgres -c "SELECT pg_catalog.pg_database_size(current_database());"
  # Compare size with expected baseline
  ```

---

## Restarting Services with Health Verification

### Restart PostgreSQL

```bash
# Graceful restart
docker-compose restart -t 120 postgres

# Wait for database to be ready
sleep 15
docker-compose exec postgres pg_isready -U postgres

# Verify data integrity after restart
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM vendor_equipment;"
# Expected: Same count as before restart

# Check for recovery errors
docker-compose logs postgres | grep -E "PANIC|FATAL" | tail -10
# Expected: No critical errors
```

---

### Restart API

```bash
# Restart with health check
docker-compose restart -t 60 api

# Wait for initialization
sleep 20

# Comprehensive health check
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/api/v1/db/health
curl -X GET http://localhost:8000/api/v1/models/status

# Verify all endpoints responding
./scripts/startup_verify.sh
```

---

### Restart Frontend

```bash
# Restart with rebuild if needed
docker-compose restart -t 30 frontend

# Monitor rebuild process
docker-compose logs -f frontend --tail=50

# Verify build successful
curl -I http://localhost:3000
curl -s http://localhost:3000/api/v1/health | jq '.'
```

---

## Scaling Services

### Horizontal Scaling (Multiple Replicas)

**Note:** Requires load balancer configuration (nginx or Traefik)

```bash
# Scale API service to 3 replicas
docker-compose up -d --scale api=3

# Verify all replicas healthy
docker-compose ps api
# Expected: 3 containers all showing "Up"

# Check load distribution (requires load balancer)
for i in {1..10}; do
    curl -s http://localhost:8000/health | jq -r '.instance_id'
done
# Expected: Different instance IDs showing round-robin

# Scale down to 1 replica
docker-compose up -d --scale api=1
```

**Limitations:**
- PostgreSQL: Should NOT be scaled horizontally (use replication instead)
- Frontend: Can be scaled with proper load balancer configuration

---

### Vertical Scaling (Resource Allocation)

**Increase Memory Allocation:**

Edit `docker-compose.yml`:
```yaml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 4G  # Increase from 2G
          cpus: '2.0'  # Increase from 1.0
        reservations:
          memory: 2G
          cpus: '1.0'
```

Apply changes:
```bash
docker-compose down
docker-compose up -d

# Verify new limits
docker inspect ner11_api_1 | jq '.[0].HostConfig.Memory'
# Expected: 4294967296 (4GB in bytes)
```

---

## Service Dependency Management

### Proper Startup Order with Dependencies

Edit `docker-compose.yml` to enforce dependencies:

```yaml
services:
  postgres:
    # No dependencies

  api:
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  frontend:
    depends_on:
      api:
        condition: service_healthy
```

**Verify dependency ordering:**
```bash
docker-compose up -d

# Should start in order: postgres → api → frontend
docker-compose logs | grep "Container .* Started"
```

---

## Quick Reference Commands

```bash
# Start specific service
docker-compose up -d <service_name>

# Stop specific service
docker-compose stop -t 60 <service_name>

# Restart specific service
docker-compose restart -t 60 <service_name>

# View service logs
docker-compose logs -f <service_name>

# Check service status
docker-compose ps <service_name>

# Scale service
docker-compose up -d --scale <service_name>=<count>

# Remove stopped service container
docker-compose rm -f <service_name>

# Rebuild and restart service
docker-compose up -d --build <service_name>
```

---

## Health Check Automation Script

```bash
#!/bin/bash
# save as: scripts/health_check.sh

SERVICE=$1
MAX_RETRIES=10
RETRY_DELAY=5

if [ -z "$SERVICE" ]; then
    echo "Usage: $0 <service_name>"
    exit 1
fi

echo "Checking health of $SERVICE..."

case $SERVICE in
    postgres)
        CMD="docker-compose exec postgres pg_isready -U postgres"
        ;;
    api)
        CMD="curl -f http://localhost:8000/health"
        ;;
    frontend)
        CMD="curl -f http://localhost:3000"
        ;;
    *)
        echo "Unknown service: $SERVICE"
        exit 1
        ;;
esac

for i in $(seq 1 $MAX_RETRIES); do
    if eval "$CMD" > /dev/null 2>&1; then
        echo "✅ $SERVICE is healthy"
        exit 0
    fi
    echo "Attempt $i/$MAX_RETRIES failed, retrying in ${RETRY_DELAY}s..."
    sleep $RETRY_DELAY
done

echo "❌ $SERVICE failed health check after $MAX_RETRIES attempts"
exit 1
```

**Usage:**
```bash
chmod +x scripts/health_check.sh
./scripts/health_check.sh postgres
./scripts/health_check.sh api
./scripts/health_check.sh frontend
```

---

## Related Runbooks

- **Startup:** docs/runbooks/daily/STARTUP_PROCEDURE.md
- **Backup:** docs/runbooks/backup-recovery/BACKUP_PROCEDURES.md
- **Incidents:** docs/runbooks/incident-response/
- **Scaling:** docs/runbooks/scaling/RESOURCE_SCALING.md

---

**Document Version History:**
- v1.0.0 (2025-12-04): Initial service management procedures

**Last Verified:** 2025-12-04
**Next Review Date:** 2025-12-18
