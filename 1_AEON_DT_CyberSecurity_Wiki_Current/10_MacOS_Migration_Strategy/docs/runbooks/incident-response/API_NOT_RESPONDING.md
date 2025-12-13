# Incident Response: API Not Responding

**File:** API_NOT_RESPONDING.md
**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** Diagnosis and recovery procedures for unresponsive API
**Status:** ACTIVE

## Incident Classification

**Severity:** CRITICAL
**Response Time:** 15 minutes
**Escalation:** After 30 minutes if unresolved

---

## Symptoms

- API health endpoint not responding (timeout or connection refused)
- HTTP 502/503/504 errors from frontend
- Container shows "unhealthy" status
- No response to `curl http://localhost:8000/health`

---

## Decision Tree

```
API Not Responding
├─ Container Running? → No → [Jump to Container Not Running]
│                     → Yes ↓
│
├─ Container Healthy? → No → [Jump to Container Unhealthy]
│                     → Yes ↓
│
├─ Port Accessible? → No → [Jump to Port/Network Issues]
│                   → Yes ↓
│
├─ App Responding? → No → [Jump to Application Hang]
│                  → Yes ↓
│
└─ Database Connected? → No → [Jump to Database Connection Issues]
                       → Yes → [Unknown Issue - Escalate]
```

---

## Diagnostic Procedure

### Step 1: Check Container Status

```bash
# Check if API container is running
docker-compose ps api

# Expected: State = "Up"
# If not: Proceed to "Container Not Running"
```

**Container Stopped/Exited:**
```bash
# Check recent logs for crash reason
docker-compose logs api --tail=100 | grep -E "ERROR|FATAL|Exception"

# Common crash patterns:
# - "ModuleNotFoundError" → Missing dependencies
# - "MemoryError" → OOM killed
# - "psycopg2.OperationalError" → Database connection failed
# - "Address already in use" → Port conflict

# Attempt restart
docker-compose up -d api

# Monitor startup
docker-compose logs -f api --tail=50

# Wait 30 seconds and check health
sleep 30
curl -X GET http://localhost:8000/health
```

---

### Step 2: Check Container Health

```bash
# Check container health status
docker inspect ner11_api_1 | jq '.[0].State.Health'

# Possible states:
# - "starting": Still initializing (wait)
# - "healthy": Container thinks it's healthy (port/network issue)
# - "unhealthy": Container detected internal problem
# - null: No healthcheck configured

# If "unhealthy", check healthcheck logs
docker inspect ner11_api_1 | jq '.[0].State.Health.Log[-5:]'
```

**Container Unhealthy:**
```bash
# Check what the healthcheck is testing
docker inspect ner11_api_1 | jq '.[0].Config.Healthcheck'

# Common issues:
# - Healthcheck command failing
# - Application not binding to correct port
# - Database connection in healthcheck failing

# Check if application process is running inside container
docker-compose exec api ps aux | grep uvicorn
# Expected: uvicorn process running

# If process missing, check for startup errors
docker-compose logs api | grep -A 10 "Application startup"

# Try manual health check from inside container
docker-compose exec api curl -f http://localhost:8000/health
```

---

### Step 3: Check Port Accessibility

```bash
# Check if port 8000 is listening
netstat -tuln | grep :8000
# or
ss -tuln | grep :8000

# Expected: "LISTEN" on 0.0.0.0:8000 or :::8000

# If not listening, check port mapping
docker-compose ps api | grep -o "0.0.0.0:[0-9]*->8000"
# Expected: "0.0.0.0:8000->8000"

# Test from host machine
curl -v http://localhost:8000/health

# Test from another container (network connectivity)
docker-compose exec frontend curl -v http://api:8000/health
```

**Port Not Accessible:**
```bash
# Check if another process is using port 8000
lsof -i :8000
# or
fuser 8000/tcp

# If conflict found, either:
# 1. Stop conflicting process: kill -9 <PID>
# 2. Change API port in docker-compose.yml: "8001:8000"

# Check Docker network
docker network inspect ner11_default | jq '.[0].Containers'
# Verify API container is connected

# Test internal container networking
docker-compose exec api nc -zv postgres 5432
# Expected: "Connection to postgres 5432 port [tcp/postgresql] succeeded!"
```

---

### Step 4: Check Application Process

```bash
# Check if Uvicorn is running
docker-compose exec api ps aux | grep uvicorn

# Expected:
# root  1  0.0  1.5  uvicorn main:app --host 0.0.0.0 --port 8000

# If process present but not responding, check for deadlock
docker-compose exec api kill -SIGUSR1 1
docker-compose logs api --tail=50
# Look for stack traces showing where threads are stuck

# Check application logs for errors
docker-compose logs api --tail=200 | grep -E "ERROR|CRITICAL|Exception|Traceback"

# Common issues:
# - Model loading stuck
# - Database query hanging
# - Memory exhausted (OOM)
# - Thread deadlock

# Check memory usage inside container
docker stats ner11_api_1 --no-stream
# If memory at limit, may be OOM killed soon
```

---

### Step 5: Check Database Connectivity

```bash
# Test database connection from API container
docker-compose exec api python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='postgres',
        database='ner11_db',
        user='postgres',
        password='password'
    )
    print('✅ Database connection successful')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"

# If connection fails, check PostgreSQL status
docker-compose ps postgres
# Expected: State = "Up"

# Check PostgreSQL is accepting connections
docker-compose exec postgres pg_isready -U postgres
# Expected: "accepting connections"

# Check connection pool exhaustion
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
# If count near max_connections, pool exhausted
```

---

## Recovery Procedures

### Procedure 1: Graceful Restart

```bash
# Attempt graceful restart with health verification
docker-compose restart -t 60 api

# Wait for startup
sleep 30

# Verify health
curl -X GET http://localhost:8000/health

# If still not responding, proceed to hard restart
```

---

### Procedure 2: Hard Restart with Log Capture

```bash
# Capture logs before restart
docker-compose logs api > /tmp/api_crash_$(date +%Y%m%d_%H%M%S).log

# Stop container forcefully
docker-compose kill api

# Remove container (forces clean slate)
docker-compose rm -f api

# Restart container
docker-compose up -d api

# Monitor startup process
docker-compose logs -f api --tail=50

# Wait for "Application startup complete" message

# Verify health
sleep 30
curl -X GET http://localhost:8000/health
```

---

### Procedure 3: Data Consistency Verification

```bash
# After restart, verify data integrity

# Test database connectivity
curl -X GET http://localhost:8000/api/v1/db/health
# Expected: {"database": "connected"}

# Test critical endpoints
curl -X GET http://localhost:8000/api/v1/vendor-equipment/
curl -X GET http://localhost:8000/api/v1/threat-intelligence/health

# Verify row counts match expected (no data loss)
docker-compose exec postgres psql -U postgres ner11_db -c "
SELECT
  'vendor_equipment' as table_name,
  COUNT(*) as row_count
FROM vendor_equipment
UNION ALL
SELECT
  'threat_intelligence',
  COUNT(*)
FROM threat_intelligence;
"

# Compare with baseline (from backup or previous snapshot)
```

---

### Procedure 4: Rollback to Previous Version (if recent deployment)

```bash
# Check recent git commits
git log --oneline -5

# Identify last working commit
git log --grep="working" --oneline

# Rollback code to previous version
git checkout <previous_commit_hash>

# Rebuild and restart container
docker-compose build api
docker-compose up -d api

# Monitor logs
docker-compose logs -f api --tail=50

# Verify health
sleep 30
curl -X GET http://localhost:8000/health
```

---

## Root Cause Analysis

### Common Root Causes

```yaml
memory_exhaustion:
  symptoms:
    - Container killed without error
    - OOM in docker logs
    - Memory usage at limit before crash
  investigation:
    - Check: docker stats (memory usage)
    - Check: dmesg | grep -i oom
  solution:
    - Increase memory limit in docker-compose.yml
    - Optimize model loading (lazy loading)
    - Implement memory caching strategy

database_connection_pool_exhausted:
  symptoms:
    - "could not obtain connection from pool"
    - High connection count in pg_stat_activity
    - Timeout errors
  investigation:
    - Check: active connections vs max_connections
    - Check: long-running queries
  solution:
    - Increase connection pool size
    - Kill idle connections
    - Optimize query performance

application_deadlock:
  symptoms:
    - Process running but not responding
    - CPU usage low, memory stable
    - No errors in logs
  investigation:
    - Send SIGUSR1 to dump thread stacks
    - Check for mutex/lock patterns
  solution:
    - Restart application
    - Fix deadlock in code
    - Implement timeout on locks

port_conflict:
  symptoms:
    - "Address already in use"
    - Container starts then exits
  investigation:
    - Check: lsof -i :8000
    - Check: docker-compose ps
  solution:
    - Kill conflicting process
    - Change port mapping in docker-compose.yml

dependency_failure:
  symptoms:
    - ModuleNotFoundError
    - ImportError
  investigation:
    - Check: pip list inside container
    - Check: requirements.txt vs installed
  solution:
    - Rebuild container: docker-compose build --no-cache api
    - Verify dependencies: docker-compose exec api pip check
```

---

## Prevention Measures

### Proactive Monitoring

```bash
# Add healthcheck to docker-compose.yml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 60s

# Monitor API response time
*/5 * * * * curl -w "%{time_total}\n" -o /dev/null -s http://localhost:8000/health >> /var/log/api_response_time.log

# Alert on high memory usage
*/1 * * * * MEMORY=$(docker stats ner11_api_1 --no-stream --format "{{.MemPerc}}" | sed 's/%//'); if [ $(echo "$MEMORY > 85" | bc) -eq 1 ]; then echo "ALERT: API memory usage at ${MEMORY}%" | mail -s "API Memory Alert" admin@example.com; fi
```

---

### Resource Limits Configuration

```yaml
# docker-compose.yml recommended limits
services:
  api:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
        reservations:
          memory: 2G
          cpus: '1.0'
    restart: unless-stopped
```

---

## Escalation Criteria

**Escalate to DevOps Team if:**
- API fails to start after 3 restart attempts
- Data corruption suspected
- Memory issues persist after resource increase
- Deadlock pattern identified but root cause unclear
- Issue recurs within 24 hours

**Emergency Escalation (CTO) if:**
- Data loss detected
- Security breach suspected (unusual errors)
- Complete service outage >1 hour
- Customer-facing impact confirmed

---

## Post-Incident Checklist

```bash
# 1. Document incident timeline
cat > /incidents/api_down_$(date +%Y%m%d).md << EOF
# API Incident - $(date)

## Timeline
- [TIME]: Incident detected
- [TIME]: Initial diagnosis
- [TIME]: Recovery action taken
- [TIME]: Service restored

## Root Cause
[Description]

## Impact
- Duration: [X minutes]
- Affected endpoints: [List]
- Data integrity: [Verified/Compromised]

## Prevention Measures
[Actions to prevent recurrence]
EOF

# 2. Verify data integrity post-recovery
./scripts/verify_data_integrity.sh

# 3. Update monitoring/alerting
# Add specific checks for identified root cause

# 4. Schedule post-mortem meeting
# Review incident response effectiveness

# 5. Update runbook with lessons learned
# Add new diagnostic steps or solutions
```

---

## Quick Reference Commands

```bash
# Check API status
docker-compose ps api

# View recent logs
docker-compose logs api --tail=100

# Test health endpoint
curl -X GET http://localhost:8000/health

# Graceful restart
docker-compose restart -t 60 api

# Hard restart
docker-compose kill api && docker-compose rm -f api && docker-compose up -d api

# Check memory usage
docker stats ner11_api_1 --no-stream

# Check database connectivity
docker-compose exec api python -c "import psycopg2; psycopg2.connect(host='postgres', database='ner11_db', user='postgres', password='password')"
```

---

## Related Runbooks

- **Database Issues:** DATABASE_CONNECTION_ISSUES.md
- **Performance:** PERFORMANCE_DEGRADATION.md
- **Model Loading:** MODEL_LOADING_FAILURES.md

---

**Document Version History:**
- v1.0.0 (2025-12-04): Initial API incident response procedures

**Last Verified:** 2025-12-04
**Next Review Date:** 2025-12-18
