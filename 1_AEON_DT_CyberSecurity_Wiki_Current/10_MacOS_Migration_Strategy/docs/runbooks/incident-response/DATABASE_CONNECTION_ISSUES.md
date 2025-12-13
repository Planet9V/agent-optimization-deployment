# Incident Response: Database Connection Issues

**File:** DATABASE_CONNECTION_ISSUES.md
**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** Diagnosis and recovery for database connectivity problems
**Status:** ACTIVE

## Incident Classification

**Severity:** CRITICAL
**Response Time:** 10 minutes
**Escalation:** After 20 minutes if unresolved

---

## Symptoms

- API logs show `psycopg2.OperationalError: could not connect`
- Frontend displays database errors
- API health endpoint returns database disconnected
- Connection timeouts in application logs

---

## Decision Tree

```
Database Connection Issue
├─ PostgreSQL Running? → No → [Start PostgreSQL]
│                      → Yes ↓
│
├─ Accepting Connections? → No → [Check PostgreSQL Logs]
│                         → Yes ↓
│
├─ Network Reachable? → No → [Check Docker Network]
│                     → Yes ↓
│
├─ Connection Pool Full? → Yes → [Reset Connection Pool]
│                        → No ↓
│
├─ Authentication OK? → No → [Check Credentials]
│                     → Yes ↓
│
└─ Query Hanging? → Yes → [Check Long-Running Queries]
                  → No → [Unknown - Escalate]
```

---

## Diagnostic Procedure

### Step 1: Check PostgreSQL Container Status

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Expected: State = "Up"

# If stopped/exited, check logs for crash reason
docker-compose logs postgres --tail=100 | grep -E "FATAL|PANIC|ERROR"

# Common crash reasons:
# - "could not open file": Disk full or permissions issue
# - "checksum failure": Data corruption
# - "too many open files": File descriptor limit reached
```

**PostgreSQL Not Running:**
```bash
# Check disk space
df -h | grep -E "/$|/var"
# Ensure >5GB available

# Check data directory permissions
docker volume inspect ner11_postgres_data

# Start PostgreSQL
docker-compose up -d postgres

# Monitor startup
docker-compose logs -f postgres --tail=50

# Wait for "database system is ready to accept connections"
# Expected within 60 seconds

# Verify accepting connections
docker-compose exec postgres pg_isready -U postgres
# Expected: "accepting connections"
```

---

### Step 2: Verify PostgreSQL Accepting Connections

```bash
# Test connection from host
docker-compose exec postgres psql -U postgres -c "SELECT version();"

# Expected: PostgreSQL version info

# If connection refused, check postgresql.conf
docker-compose exec postgres cat /var/lib/postgresql/data/postgresql.conf | grep listen_addresses
# Expected: listen_addresses = '*' or '0.0.0.0'

# Check pg_hba.conf for authentication rules
docker-compose exec postgres cat /var/lib/postgresql/data/pg_hba.conf | grep -v "^#"
# Expected: Entry allowing connections from Docker network

# Check PostgreSQL logs for connection errors
docker-compose logs postgres | grep "connection"
```

---

### Step 3: Check Network Connectivity

```bash
# Test network connectivity from API container
docker-compose exec api ping -c 3 postgres
# Expected: 0% packet loss

# Test PostgreSQL port connectivity
docker-compose exec api nc -zv postgres 5432
# Expected: "Connection to postgres 5432 port [tcp/postgresql] succeeded!"

# Check Docker network
docker network inspect ner11_default | jq '.[0].Containers'
# Verify both API and PostgreSQL containers present

# Check for network isolation issues
docker-compose exec api nslookup postgres
# Expected: Resolves to internal IP
```

**Network Issues Detected:**
```bash
# Recreate Docker network
docker-compose down
docker network prune
docker-compose up -d

# Verify connectivity restored
docker-compose exec api nc -zv postgres 5432
```

---

### Step 4: Check Connection Pool Status

```bash
# Check total active connections
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Check connection breakdown by state
docker-compose exec postgres psql -U postgres -c "
SELECT
  state,
  count(*)
FROM pg_stat_activity
GROUP BY state;
"

# Expected states:
# - active: Currently executing query
# - idle: Waiting for new command
# - idle in transaction: In transaction but not executing

# Check max_connections limit
docker-compose exec postgres psql -U postgres -c "SHOW max_connections;"
# Default: 100

# Check connection pool utilization
docker-compose exec postgres psql -U postgres -c "
SELECT
  (SELECT count(*) FROM pg_stat_activity) AS current_connections,
  (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') AS max_connections,
  (SELECT count(*) FROM pg_stat_activity) * 100.0 /
    (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') AS utilization_percent;
"

# Alert if >80% utilization
```

**Connection Pool Exhausted:**
```bash
# Identify idle connections consuming pool
docker-compose exec postgres psql -U postgres -c "
SELECT
  pid,
  usename,
  application_name,
  state,
  state_change
FROM pg_stat_activity
WHERE state = 'idle'
  AND state_change < now() - interval '30 minutes'
ORDER BY state_change;
"

# Terminate long-idle connections
docker-compose exec postgres psql -U postgres -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
  AND state_change < now() - interval '30 minutes'
  AND pid <> pg_backend_pid();
"

# Verify connections released
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Restart API to reset connection pool
docker-compose restart api
```

---

### Step 5: Verify Authentication

```bash
# Test connection with credentials from .env
DB_USER=$(grep POSTGRES_USER .env | cut -d '=' -f2)
DB_PASS=$(grep POSTGRES_PASSWORD .env | cut -d '=' -f2)
DB_NAME=$(grep POSTGRES_DB .env | cut -d '=' -f2)

# Test connection from API container
docker-compose exec api python -c "
import psycopg2
import os

try:
    conn = psycopg2.connect(
        host='postgres',
        database='$DB_NAME',
        user='$DB_USER',
        password='$DB_PASS'
    )
    print('✅ Authentication successful')
    conn.close()
except Exception as e:
    print(f'❌ Authentication failed: {e}')
"

# If authentication fails, check credentials match
docker-compose exec postgres psql -U postgres -c "\du"
# Verify user exists with correct permissions
```

**Authentication Failure:**
```bash
# Reset password if needed
docker-compose exec postgres psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'new_password';"

# Update .env file
sed -i 's/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=new_password/' .env

# Restart API to pick up new password
docker-compose restart api

# Verify connection
docker-compose exec api curl http://localhost:8000/api/v1/db/health
```

---

### Step 6: Check for Long-Running Queries

```bash
# Identify long-running queries (>5 minutes)
docker-compose exec postgres psql -U postgres -c "
SELECT
  pid,
  now() - query_start AS duration,
  state,
  query
FROM pg_stat_activity
WHERE state <> 'idle'
  AND query_start < now() - interval '5 minutes'
ORDER BY query_start;
"

# Check for blocking queries
docker-compose exec postgres psql -U postgres -c "
SELECT
  blocked_locks.pid AS blocked_pid,
  blocked_activity.usename AS blocked_user,
  blocking_locks.pid AS blocking_pid,
  blocking_activity.usename AS blocking_user,
  blocked_activity.query AS blocked_statement,
  blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
  AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
  AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
  AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
  AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
  AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
  AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
  AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
  AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
  AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
  AND blocking_locks.pid <> blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
"
```

**Long-Running Queries Found:**
```bash
# Terminate specific query
docker-compose exec postgres psql -U postgres -c "SELECT pg_cancel_backend(<PID>);"

# If query won't cancel, force terminate
docker-compose exec postgres psql -U postgres -c "SELECT pg_terminate_backend(<PID>);"

# Check for deadlocks
docker-compose exec postgres psql -U postgres -c "SELECT * FROM pg_stat_database_conflicts WHERE deadlocks > 0;"
```

---

## Recovery Procedures

### Procedure 1: Reset Connection Pool

```bash
# Graceful reset (try first)
docker-compose restart -t 30 api

# Wait for API startup
sleep 20

# Verify database health
curl -X GET http://localhost:8000/api/v1/db/health
# Expected: {"database": "connected", "active_connections": 1-3}

# Check connection count reduced
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity WHERE application_name = 'fastapi';"
# Expected: <10 connections
```

---

### Procedure 2: PostgreSQL Reload Configuration

```bash
# Reload PostgreSQL without restart (preserves connections)
docker-compose exec postgres psql -U postgres -c "SELECT pg_reload_conf();"

# Verify configuration reloaded
docker-compose logs postgres | tail -10
# Expected: "received SIGHUP, reloading configuration files"

# Check connection limit changes applied
docker-compose exec postgres psql -U postgres -c "SHOW max_connections;"
```

---

### Procedure 3: PostgreSQL Graceful Restart

```bash
# ⚠️  WARNING: Will disconnect all clients

# Stop API first to prevent new connections
docker-compose stop api

# Checkpoint database (flush WAL)
docker-compose exec postgres psql -U postgres -c "CHECKPOINT;"

# Graceful restart
docker-compose restart -t 120 postgres

# Wait for ready
sleep 15
docker-compose exec postgres pg_isready -U postgres

# Restart API
docker-compose up -d api

# Verify connectivity
sleep 20
curl -X GET http://localhost:8000/api/v1/db/health
```

---

### Procedure 4: Data Integrity Check

```bash
# After recovery, verify database integrity

# Check for corruption
docker-compose exec postgres psql -U postgres ner11_db -c "
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"

# Compare table row counts with baseline
docker-compose exec postgres psql -U postgres ner11_db -c "
SELECT
  'vendor_equipment' AS table_name, COUNT(*) AS row_count FROM vendor_equipment
UNION ALL
SELECT 'threat_intelligence', COUNT(*) FROM threat_intelligence
UNION ALL
SELECT 'compliance_frameworks', COUNT(*) FROM compliance_frameworks;
"

# Run database consistency check
docker-compose exec postgres psql -U postgres -c "SELECT pg_database_size('ner11_db');"
# Compare with expected size

# Check for transaction wraparound issues
docker-compose exec postgres psql -U postgres -c "
SELECT
  datname,
  age(datfrozenxid) AS age
FROM pg_database
ORDER BY age DESC;
"
# Alert if age > 1 billion
```

---

## Root Cause Analysis

### Common Root Causes

```yaml
connection_pool_leak:
  symptoms:
    - Connections slowly increasing over time
    - Eventually hits max_connections
    - "FATAL: sorry, too many clients already"
  investigation:
    - Check: Connections not being closed in code
    - Check: Exception handling releasing connections
  solution:
    - Fix connection leak in application code
    - Implement connection timeout
    - Monitor connection pool metrics

database_overwhelmed:
  symptoms:
    - Slow query responses
    - Connection timeouts
    - High CPU/memory on PostgreSQL container
  investigation:
    - Check: Expensive queries
    - Check: Missing indexes
    - Check: VACUUM/ANALYZE needed
  solution:
    - Optimize slow queries
    - Add indexes
    - Run VACUUM ANALYZE
    - Scale database resources

network_instability:
  symptoms:
    - Intermittent connection failures
    - Packet loss in ping tests
    - DNS resolution failures
  investigation:
    - Check: Docker network health
    - Check: System network interfaces
  solution:
    - Recreate Docker network
    - Restart Docker daemon
    - Check host network configuration

authentication_mismatch:
  symptoms:
    - "FATAL: password authentication failed"
    - Consistent connection rejection
  investigation:
    - Check: .env credentials vs PostgreSQL
    - Check: pg_hba.conf rules
  solution:
    - Reset password
    - Update pg_hba.conf
    - Verify .env loaded correctly

database_corruption:
  symptoms:
    - "checksum failure" in logs
    - "could not read block" errors
    - PostgreSQL won't start
  investigation:
    - Check: Recent power loss/crash
    - Check: Disk errors in dmesg
  solution:
    - Restore from backup
    - Run pg_resetwal (last resort)
    - Replace failed disk
```

---

## Prevention Measures

### Connection Pool Configuration

**Recommended settings in API (config.py):**

```python
# Connection pool settings
DATABASE_POOL_SIZE = 10  # Max connections in pool
DATABASE_MAX_OVERFLOW = 20  # Extra connections if pool full
DATABASE_POOL_TIMEOUT = 30  # Seconds to wait for connection
DATABASE_POOL_RECYCLE = 3600  # Recycle connections after 1 hour
DATABASE_POOL_PRE_PING = True  # Test connection before use
```

---

### PostgreSQL Tuning

**Recommended postgresql.conf settings:**

```ini
# Connection settings
max_connections = 100
shared_buffers = 256MB  # 25% of system memory
effective_cache_size = 1GB  # 50-75% of system memory

# Checkpoint settings
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Query timeout
statement_timeout = 30000  # 30 seconds
idle_in_transaction_session_timeout = 60000  # 1 minute
```

---

### Monitoring Queries

```bash
# Add to cron for connection monitoring
*/5 * * * * docker-compose exec -T postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;" >> /var/log/postgres_connections.log

# Alert on high connection count
*/5 * * * * CONN=$(docker-compose exec -T postgres psql -U postgres -t -c "SELECT count(*) FROM pg_stat_activity;" | tr -d ' '); if [ $CONN -gt 80 ]; then echo "ALERT: $CONN connections" | mail -s "Database Connection Alert" admin@example.com; fi
```

---

## Escalation Criteria

**Escalate to Database Admin if:**
- Connection issues persist after pool reset
- Database corruption suspected
- Performance degradation with no obvious cause
- Replication lag increasing
- Transaction ID wraparound risk

**Emergency Escalation (CTO) if:**
- Data corruption confirmed
- Complete database failure
- Backup restoration required
- Potential data loss scenario

---

## Post-Incident Checklist

```bash
# 1. Document root cause
echo "Database Connection Incident - $(date)" >> /incidents/db_connection_issues.log
echo "Root Cause: [DESCRIPTION]" >> /incidents/db_connection_issues.log

# 2. Verify all connections healthy
docker-compose exec postgres psql -U postgres -c "SELECT * FROM pg_stat_activity;"

# 3. Check for data integrity issues
./scripts/verify_data_integrity.sh

# 4. Update connection pool settings if needed
# Edit api/config.py with optimized settings

# 5. Add specific monitoring for identified issue
# Update Prometheus rules or monitoring scripts

# 6. Schedule review of slow queries
docker-compose exec postgres psql -U postgres -c "SELECT * FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

---

## Quick Reference Commands

```bash
# Check PostgreSQL status
docker-compose ps postgres

# Check connections
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Test connectivity
docker-compose exec api nc -zv postgres 5432

# Reset connection pool
docker-compose restart api

# Terminate idle connections
docker-compose exec postgres psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle' AND state_change < now() - interval '30 minutes' AND pid <> pg_backend_pid();"

# Check database health
curl -X GET http://localhost:8000/api/v1/db/health
```

---

## Related Runbooks

- **API Issues:** API_NOT_RESPONDING.md
- **Performance:** PERFORMANCE_DEGRADATION.md
- **Data Corruption:** DATA_CORRUPTION.md

---

**Document Version History:**
- v1.0.0 (2025-12-04): Initial database connection procedures

**Last Verified:** 2025-12-04
**Next Review Date:** 2025-12-18
