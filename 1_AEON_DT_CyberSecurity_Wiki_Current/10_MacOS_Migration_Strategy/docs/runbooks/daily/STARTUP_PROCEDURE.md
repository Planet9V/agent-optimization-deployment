# Daily Startup Procedure

**File:** STARTUP_PROCEDURE.md
**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** Complete startup procedure for NER11 Gold Model system
**Status:** ACTIVE

## Executive Summary

This runbook provides step-by-step procedures for daily system startup, including service health checks, database validation, API verification, and troubleshooting for common startup issues.

**Expected Total Startup Time:** 3-5 minutes
**Critical Success Criteria:** All services healthy, API responding, database connected

---

## Pre-Startup Checklist

```bash
# 1. Verify Docker is running
docker info > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Docker is running"
else
    echo "❌ Docker is not running - starting Docker..."
    # macOS: open -a Docker
    # Linux: sudo systemctl start docker
fi

# 2. Check available disk space (minimum 10GB required)
df -h | grep -E "/$|/var/lib/docker"
# Expected: At least 10GB free on root and Docker volumes

# 3. Check available memory (minimum 4GB required)
free -h | grep Mem
# Expected: At least 4GB available memory

# 4. Verify network connectivity
ping -c 3 8.8.8.8 > /dev/null 2>&1
echo "✅ Network connectivity verified"
```

**Decision Point:** If any pre-startup check fails, resolve before proceeding.

---

## Step 1: Start Core Infrastructure (Database First)

```bash
# Start PostgreSQL container first (dependency for API)
cd /path/to/project/5_NER11_Gold_Model

docker-compose up -d postgres

# Wait for PostgreSQL to be ready (30-60 seconds)
echo "Waiting for PostgreSQL to initialize..."
sleep 10

# Verify PostgreSQL is accepting connections
docker-compose exec postgres pg_isready -U postgres
# Expected output: "/var/run/postgresql:5432 - accepting connections"
```

**Troubleshooting:**
- If `pg_isready` fails after 60 seconds → See INCIDENT_RESPONSE/DATABASE_CONNECTION_ISSUES.md
- If container exits immediately → Check logs: `docker-compose logs postgres`

**Expected Startup Time:** 30-60 seconds

---

## Step 2: Start Backend API Service

```bash
# Start API container
docker-compose up -d api

# Monitor API startup logs
docker-compose logs -f api --tail=50

# Wait for API initialization message
# Expected log: "INFO:     Uvicorn running on http://0.0.0.0:8000"
# Expected log: "INFO:     Application startup complete"
```

**Health Check Commands:**
```bash
# Wait 20 seconds for API to initialize
sleep 20

# Test basic health endpoint
curl -X GET http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "...", "version": "..."}

# Test database connection through API
curl -X GET http://localhost:8000/api/v1/db/health
# Expected: {"database": "connected", "pool_size": 10, "active_connections": 1}

# Test model loading status
curl -X GET http://localhost:8000/api/v1/models/status
# Expected: {"models_loaded": true, "available_models": [...]}
```

**Troubleshooting:**
- If API doesn't start within 60 seconds → Check logs: `docker-compose logs api`
- If database connection fails → Verify PostgreSQL is running: `docker-compose ps postgres`
- If model loading fails → See INCIDENT_RESPONSE/MODEL_LOADING_FAILURES.md

**Expected Startup Time:** 45-90 seconds

---

## Step 3: Start Frontend Service

```bash
# Start frontend container
docker-compose up -d frontend

# Monitor frontend build process
docker-compose logs -f frontend --tail=50

# Wait for build completion message
# Expected log: "webpack compiled successfully"
# Expected log: "Compiled successfully!"
```

**Health Check Commands:**
```bash
# Wait 30 seconds for build completion
sleep 30

# Test frontend accessibility
curl -I http://localhost:3000
# Expected: "HTTP/1.1 200 OK"

# Test API proxy functionality
curl -X GET http://localhost:3000/api/v1/health
# Expected: Same response as direct API call (proxy working)
```

**Troubleshooting:**
- If build fails → Check Node.js version compatibility in logs
- If API proxy doesn't work → Verify proxy configuration in `frontend/package.json`
- If port 3000 is already in use → See SERVICE_MANAGEMENT/PORT_CONFLICTS.md

**Expected Startup Time:** 60-120 seconds

---

## Step 4: Comprehensive Service Verification

```bash
# Check all container status
docker-compose ps

# Expected output:
#       Name                      Command               State           Ports
# -------------------------------------------------------------------------------------
# ner11_postgres_1     docker-entrypoint.sh postgres   Up      0.0.0.0:5432->5432/tcp
# ner11_api_1          uvicorn main:app --host 0.0.0.0 Up      0.0.0.0:8000->8000/tcp
# ner11_frontend_1     npm start                       Up      0.0.0.0:3000->3000/tcp
```

**All services should show "Up" status.**

---

## Step 5: API Endpoint Health Verification

```bash
# Create verification script
cat > /tmp/verify_api.sh << 'EOF'
#!/bin/bash
BASE_URL="http://localhost:8000"

echo "Testing critical API endpoints..."

# Phase B2 - Vendor Equipment
curl -s -X GET "$BASE_URL/api/v1/vendor-equipment/health" | jq '.'

# Phase B3 - Threat Intelligence
curl -s -X GET "$BASE_URL/api/v1/threat-intelligence/health" | jq '.'

# Phase B4 - Compliance
curl -s -X GET "$BASE_URL/api/v1/compliance/health" | jq '.'

# E10 - Economic Impact
curl -s -X GET "$BASE_URL/api/v1/economic-impact/health" | jq '.'

# E11 - Demographics
curl -s -X GET "$BASE_URL/api/v1/demographics/health" | jq '.'

# E12 - Prioritization
curl -s -X GET "$BASE_URL/api/v1/prioritization/health" | jq '.'

echo "✅ All endpoints verified"
EOF

chmod +x /tmp/verify_api.sh
/tmp/verify_api.sh
```

**Expected Output:** All endpoints return `{"status": "healthy"}` or similar success response.

**Troubleshooting:**
- If any endpoint returns 404 → Module not loaded, check `api/__init__.py` imports
- If any endpoint returns 500 → Check API logs for specific error
- If timeout occurs → API may be overloaded, check resource usage

---

## Step 6: Database Connection Validation

```bash
# Test database connection pool
docker-compose exec postgres psql -U postgres -d ner11_db -c "\conninfo"
# Expected: "You are connected to database 'ner11_db' as user 'postgres'..."

# Check active connections
docker-compose exec postgres psql -U postgres -d ner11_db -c "SELECT count(*) FROM pg_stat_activity;"
# Expected: At least 2-3 connections (API connection pool)

# Verify critical tables exist
docker-compose exec postgres psql -U postgres -d ner11_db -c "\dt"
# Expected: List of tables including vendor_equipment, threat_intelligence, etc.

# Test sample query
docker-compose exec postgres psql -U postgres -d ner11_db -c "SELECT COUNT(*) FROM vendor_equipment;"
# Expected: Row count (may be 0 if no data yet)
```

**Troubleshooting:**
- If connection refused → PostgreSQL container not running or not ready
- If table doesn't exist → Run migrations: `docker-compose exec api alembic upgrade head`
- If query times out → Check database performance metrics

---

## Step 7: Frontend Build and Serving Validation

```bash
# Verify frontend build artifacts
docker-compose exec frontend ls -lh /app/build
# Expected: build directory with static files

# Test React app loading
curl -s http://localhost:3000 | grep -o "<title>.*</title>"
# Expected: "<title>NER11 Gold Model</title>" or similar

# Test static asset serving
curl -I http://localhost:3000/static/js/main.chunk.js
# Expected: "HTTP/1.1 200 OK" with "Content-Type: application/javascript"

# Test API integration from frontend
curl -s http://localhost:3000/api/v1/health | jq '.'
# Expected: API health response (proves proxy working)
```

**Troubleshooting:**
- If build artifacts missing → Frontend build failed, check logs
- If title tag wrong → Check `public/index.html` in frontend directory
- If static assets 404 → Build incomplete, restart frontend container

---

## Step 8: Dashboard Access Points for Monitoring

```bash
# Primary Dashboards
echo "🖥️  Access Points:"
echo "Frontend UI:        http://localhost:3000"
echo "API Documentation:  http://localhost:8000/docs"
echo "API Redoc:          http://localhost:8000/redoc"
echo "Health Dashboard:   http://localhost:8000/health"

# Database Admin (if pgAdmin installed)
echo "pgAdmin:            http://localhost:5050"
echo "  Username: admin@ner11.local"
echo "  Password: [check .env file]"

# Container Stats Dashboard
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
```

**Expected Access:**
- All URLs should be accessible without errors
- API documentation should load Swagger UI
- Frontend should display application interface

---

## Expected Startup Time Summary

| Service    | Startup Time | Health Check Time | Total Time |
|------------|--------------|-------------------|------------|
| PostgreSQL | 30-60s       | 10s               | 40-70s     |
| API        | 45-90s       | 20s               | 65-110s    |
| Frontend   | 60-120s      | 30s               | 90-150s    |
| **TOTAL**  |              |                   | **3-5 min** |

---

## Troubleshooting Startup Delays

### If PostgreSQL takes longer than 60 seconds:
```bash
# Check initialization logs
docker-compose logs postgres | grep -E "database system is ready|initdb"

# Common causes:
# - First-time initialization (can take 90-120s)
# - Large database restore in progress
# - Disk I/O performance issues

# Solution: Wait for "database system is ready to accept connections"
```

### If API takes longer than 90 seconds:
```bash
# Check model loading progress
docker-compose logs api | grep -E "Loading model|Model loaded|ERROR"

# Common causes:
# - Large ML models being loaded into memory
# - Database migration running
# - External API dependencies timeout

# Solution: Monitor logs for specific bottleneck
```

### If Frontend takes longer than 120 seconds:
```bash
# Check build process
docker-compose logs frontend | grep -E "webpack|Compiling|Failed"

# Common causes:
# - Node modules installation on first run
# - TypeScript compilation errors
# - Large dependency tree

# Solution: Check for compilation errors in logs
```

---

## Complete Startup Verification Script

```bash
#!/bin/bash
# save as: scripts/startup_verify.sh

set -e

echo "🚀 Starting NER11 Gold Model System Verification..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

verify_service() {
    local service=$1
    local check_cmd=$2
    local expected=$3

    echo -n "Checking $service... "

    if eval "$check_cmd" | grep -q "$expected"; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        return 1
    fi
}

# Pre-checks
echo "📋 Pre-startup checks..."
verify_service "Docker" "docker info 2>&1" "Server Version"
verify_service "Disk Space" "df -h /" "Available"
verify_service "Network" "ping -c 1 8.8.8.8 2>&1" "1 packets transmitted"

# Service checks
echo ""
echo "🐳 Container status..."
verify_service "PostgreSQL" "docker-compose ps postgres" "Up"
verify_service "API" "docker-compose ps api" "Up"
verify_service "Frontend" "docker-compose ps frontend" "Up"

# Health checks
echo ""
echo "🏥 Health endpoint checks..."
sleep 5  # Give services time to stabilize

verify_service "API Health" "curl -s http://localhost:8000/health" "healthy"
verify_service "Database Health" "curl -s http://localhost:8000/api/v1/db/health" "connected"
verify_service "Frontend Access" "curl -I http://localhost:3000 2>&1" "200 OK"

# Endpoint verification
echo ""
echo "🔌 API endpoint verification..."
verify_service "Vendor Equipment API" "curl -s http://localhost:8000/api/v1/vendor-equipment/health" "healthy"
verify_service "Threat Intelligence API" "curl -s http://localhost:8000/api/v1/threat-intelligence/health" "healthy"
verify_service "Compliance API" "curl -s http://localhost:8000/api/v1/compliance/health" "healthy"

echo ""
echo -e "${GREEN}✅ All startup verification checks passed!${NC}"
echo ""
echo "🖥️  Access Points:"
echo "   Frontend:    http://localhost:3000"
echo "   API Docs:    http://localhost:8000/docs"
echo "   API Health:  http://localhost:8000/health"
echo ""
```

**Usage:**
```bash
chmod +x scripts/startup_verify.sh
./scripts/startup_verify.sh
```

---

## Quick Reference Commands

```bash
# Full startup sequence
docker-compose up -d

# Check all services
docker-compose ps

# View all logs
docker-compose logs -f

# Run verification
./scripts/startup_verify.sh

# Access dashboards
open http://localhost:3000      # Frontend
open http://localhost:8000/docs # API Documentation
```

---

## Escalation Criteria

**Contact DevOps Team if:**
- Startup time exceeds 10 minutes
- Any service fails to start after 3 restart attempts
- Database connection issues persist
- API endpoints return consistent 500 errors
- Memory usage exceeds 90% during startup
- Disk space drops below 5GB during startup

**Emergency Contacts:**
- DevOps On-Call: [PHONE NUMBER]
- Database Admin: [PHONE NUMBER]
- Development Lead: [PHONE NUMBER]

---

## Related Runbooks

- **Service Management:** docs/runbooks/service-management/SERVICE_CONTROL.md
- **Database Issues:** docs/runbooks/incident-response/DATABASE_CONNECTION_ISSUES.md
- **Model Loading:** docs/runbooks/incident-response/MODEL_LOADING_FAILURES.md
- **Network Issues:** docs/runbooks/incident-response/NETWORK_CONNECTIVITY_ISSUES.md

---

**Document Version History:**
- v1.0.0 (2025-12-04): Initial comprehensive startup procedure

**Last Verified:** 2025-12-04
**Next Review Date:** 2025-12-18
