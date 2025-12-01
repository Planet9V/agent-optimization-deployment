# Rollback Procedures

**File**: ROLLBACK_PROCEDURES.md
**Created**: 2025-11-12
**Purpose**: Emergency rollback procedures for GAP-001, QW-001, QW-002
**Status**: ACTIVE

---

## Emergency Contact Information

**Deployment Lead**: _______________
**Phone**: _______________
**Email**: _______________

**On-Call Engineer**: _______________
**Phone**: _______________
**Email**: _______________

---

## Rollback Decision Criteria

### When to Rollback

Execute rollback immediately if ANY of the following occur:

**🔴 CRITICAL (Immediate Rollback)**:
- Application crashes or becomes unresponsive
- Data loss or corruption detected
- Security vulnerability discovered
- Error rate > 5% for > 5 minutes
- Complete feature failure affecting all users

**🟡 MAJOR (Rollback within 30 minutes)**:
- Performance degradation > 50% from baseline
- Partial feature failure affecting > 25% of users
- Memory leak detected
- Error rate 1-5% sustained for > 15 minutes
- User-reported critical bugs

**🟢 MINOR (Monitor, Consider Rollback)**:
- Performance degradation 25-50% from baseline
- Non-critical bugs affecting < 10% of users
- Error rate < 1%
- Minor UX issues

---

## Rollback Overview

### Three-Level Rollback Strategy

```
Level 1: Feature Toggle (Fastest - 2 minutes)
  ↓ If insufficient
Level 2: Code Rollback (Fast - 15 minutes)
  ↓ If insufficient
Level 3: Full System Restore (Thorough - 45 minutes)
```

---

## Level 1: Feature Toggle Rollback (2 minutes)

### Quick Disable via Environment Variables

```bash
# SSH into production server
ssh user@prod-server

# Disable features via environment variables
cat >> /opt/app/.env << 'EOF'
# Emergency feature toggles (2025-11-12)
ENABLE_PARALLEL_SPAWNING=false
ENABLE_PARALLEL_UPLOADS=false
ENABLE_MCP_TRACKING=false
EOF

# Restart application
pm2 restart app

# Verify application started
pm2 status app

# Check health
curl http://localhost:3000/api/health
```

**Expected Behavior**:
- Parallel spawning disabled → Falls back to sequential (slower but stable)
- Parallel uploads disabled → Falls back to sequential (slower but stable)
- MCP tracking disabled → Local-only tracking (no persistence)

**Verification Commands**:
```bash
# Verify sequential spawning active
tail -f /var/log/app.log | grep "sequential spawning"

# Verify sequential uploads active
tail -f /var/log/app.log | grep "sequential upload"

# Verify MCP disabled
grep "MCP.*unavailable" /var/log/app.log
```

**Level 1 Checklist**:
- [ ] Environment variables updated
- [ ] Application restarted
- [ ] Health check passes
- [ ] Features disabled confirmed
- [ ] System stable
- [ ] Incident logged

**Time to Complete**: 2 minutes
**Impact**: Features disabled, system stable
**Data Loss**: None

---

## Level 2: Code Rollback (15 minutes)

### Git Revert to Previous Stable Version

```bash
# SSH into production server
ssh user@prod-server

# Navigate to application directory
cd /opt/app

# Check current version
git log --oneline -5
git tag --list | sort -V

# Identify last stable version
git tag --list | grep stable | tail -1
# Example output: v1.0.0-stable

# Create backup of current state (just in case)
tar -czf /tmp/backup-before-rollback-$(date +%Y%m%d-%H%M%S).tar.gz .

# Checkout stable version
git fetch origin
git checkout v1.0.0-stable

# Verify correct version
git log --oneline -1
git describe --tags

# Clean and reinstall dependencies
rm -rf node_modules package-lock.json
npm ci --production

# Rebuild application
NODE_ENV=production npm run build

# Restart with zero-downtime
pm2 reload app

# Verify application health
pm2 status app
curl http://localhost:3000/api/health

# Monitor for 5 minutes
pm2 logs app --lines 50
```

**Level 2 Checklist**:
- [ ] Current state backed up
- [ ] Stable version identified
- [ ] Code reverted successfully
- [ ] Dependencies reinstalled
- [ ] Build completed
- [ ] Application restarted
- [ ] Health check passes
- [ ] 5-minute stability confirmed
- [ ] Incident documented

**Time to Complete**: 15 minutes
**Impact**: Full rollback to stable version
**Data Loss**: In-memory data only (cleared on restart)

---

## Level 3: Full System Restore (45 minutes)

### Complete Restoration from Backup

```bash
# SSH into production server
ssh user@prod-server

# Stop application
pm2 stop app

# Navigate to application directory
cd /opt/app

# List available backups
ls -lht /backups/app-backups/

# Identify pre-deployment backup
# Example: backup-20251111-140000.tar.gz (day before deployment)

# Move current directory (safety)
cd /opt
mv app app-failed-$(date +%Y%m%d-%H%M%S)

# Extract backup
mkdir app
cd app
tar -xzf /backups/app-backups/backup-20251111-140000.tar.gz

# Verify extraction
ls -la
cat package.json | grep version

# Verify database backup (if applicable)
ls -la /backups/db-backups/

# Restore database (if needed)
# Example for PostgreSQL:
# psql -U postgres -d appdb < /backups/db-backups/backup-20251111-140000.sql

# Verify environment configuration
cat .env | head -20

# Reinstall dependencies (from backup's package-lock.json)
npm ci --production

# Verify build artifacts present
ls -la .next/ dist/ build/

# If build artifacts missing, rebuild
if [ ! -d ".next" ]; then
  NODE_ENV=production npm run build
fi

# Restart application
pm2 start app

# Verify startup
pm2 status app
sleep 10
curl http://localhost:3000/api/health

# Monitor for 15 minutes
pm2 logs app --lines 100
pm2 monit
```

**Level 3 Checklist**:
- [ ] Application stopped
- [ ] Failed directory archived
- [ ] Backup identified and extracted
- [ ] Database restored (if applicable)
- [ ] Environment configuration verified
- [ ] Dependencies installed
- [ ] Build artifacts present
- [ ] Application started successfully
- [ ] Health check passes
- [ ] 15-minute stability confirmed
- [ ] Full incident report created

**Time to Complete**: 45 minutes
**Impact**: Complete system restoration
**Data Loss**: All changes since backup (assess impact)

---

## Component-Specific Rollback Procedures

### GAP-001: Parallel Agent Spawning Rollback

**Symptoms**:
- Agent spawning failures
- Timeouts during spawn
- MCP connection errors
- Dependency resolution issues

**Rollback Steps**:
```bash
# Option 1: Disable via environment variable
export ENABLE_PARALLEL_SPAWNING=false
pm2 restart app

# Option 2: Revert specific file
cd /opt/app
git checkout v1.0.0-stable -- lib/orchestration/parallel-agent-spawner.ts
npm run build
pm2 restart app

# Verification
tail -f /var/log/app.log | grep "sequential agent spawning"
```

**Expected Behavior After Rollback**:
- Agents spawn sequentially (750ms per agent)
- No dependency batching
- No MCP calls for spawning
- Slower but stable operation

---

### QW-001: Parallel S3 Uploads Rollback

**Symptoms**:
- Upload failures
- Timeout errors
- HTTP 207 errors
- S3/MinIO connection issues
- Memory exhaustion

**Rollback Steps**:
```bash
# Option 1: Disable via environment variable
export ENABLE_PARALLEL_UPLOADS=false
pm2 restart app

# Option 2: Revert specific file
cd /opt/app
git checkout v1.0.0-stable -- app/api/upload/route.ts
npm run build
pm2 restart app

# Option 3: Restore original upload logic (manual)
cat > app/api/upload/route.ts << 'EOF'
// Original sequential upload implementation
// (Insert backed up code here)
EOF
npm run build
pm2 restart app

# Verification
curl -X POST http://localhost:3000/api/upload \
  -F "file=@test-file.pdf"

# Check logs for sequential pattern
tail -f /var/log/app.log | grep "sequential upload"
```

**Expected Behavior After Rollback**:
- Files upload sequentially
- No Promise.allSettled() usage
- No HTTP 207 Multi-Status responses
- Slower upload times
- Traditional error responses only

---

### QW-002: MCP Integration Rollback

**Symptoms**:
- MCP connection failures
- Memory database errors
- Agent tracking failures
- Wiki notification failures

**Rollback Steps**:
```bash
# Option 1: Disable via environment variable
export ENABLE_MCP_TRACKING=false
pm2 restart app

# Option 2: Revert MCP integration files
cd /opt/app
git checkout v1.0.0-stable -- lib/observability/mcp-integration.ts
git checkout v1.0.0-stable -- lib/observability/agent-tracker.ts
npm run build
pm2 restart app

# Option 3: Remove MCP integration (emergency)
rm lib/observability/mcp-integration.ts

# Comment out MCP calls in agent-tracker.ts
sed -i 's/await mcpIntegration/\/\/ await mcpIntegration/g' \
  lib/observability/agent-tracker.ts

npm run build
pm2 restart app

# Verification
grep "MCP.*disabled" /var/log/app.log
```

**Expected Behavior After Rollback**:
- Agent tracking continues locally only
- No persistent memory storage
- No wiki notifications
- No cross-session data retention
- Standard logging only

---

## Database Rollback (If Applicable)

### PostgreSQL Rollback

```bash
# List available database backups
ls -lht /backups/db-backups/

# Identify pre-deployment backup
# Example: db-backup-20251111-140000.sql

# Create current database backup (safety)
pg_dump -U postgres appdb > /tmp/db-backup-before-rollback.sql

# Stop application
pm2 stop app

# Drop current database
psql -U postgres -c "DROP DATABASE appdb;"

# Recreate database
psql -U postgres -c "CREATE DATABASE appdb;"

# Restore from backup
psql -U postgres appdb < /backups/db-backups/db-backup-20251111-140000.sql

# Verify restoration
psql -U postgres appdb -c "SELECT COUNT(*) FROM agents;"

# Restart application
pm2 start app
```

### SQLite Rollback (MCP Memory Database)

```bash
# Stop application
pm2 stop app

# Backup current memory database
cp .swarm/memory.db .swarm/memory.db.rollback-backup

# Restore pre-deployment backup
cp /backups/memory-backups/memory-20251111-140000.db .swarm/memory.db

# Verify restoration
sqlite3 .swarm/memory.db "SELECT COUNT(*) FROM agent_activities;"

# Restart application
pm2 start app
```

---

## Post-Rollback Verification

### System Health Verification

```bash
# 1. Application Status
pm2 status app
pm2 logs app --lines 50

# 2. Health Endpoint
curl http://localhost:3000/api/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "1.0.0-stable",
#   "timestamp": "2025-11-12T..."
# }

# 3. Core Functionality Tests
# Test agent spawning
curl -X POST http://localhost:3000/api/agents/spawn \
  -H "Content-Type: application/json" \
  -d '{"agents": [{"type": "researcher", "name": "Test"}]}'

# Test file upload
curl -X POST http://localhost:3000/api/upload \
  -F "file=@test-document.pdf"

# Test agent tracking (if MCP enabled)
npx claude-flow@alpha memory query "agent-activities:" --reasoningbank

# 4. Error Rate Check
tail -100 /var/log/app.log | grep -i error | wc -l
# Should be 0 or very low

# 5. Performance Check
# Response time should be normal (even if slower than optimized version)
time curl http://localhost:3000/api/health

# 6. Database Connectivity
# (If applicable - test database queries)
psql -U postgres appdb -c "SELECT 1;"
```

**Post-Rollback Checklist**:
- [ ] Application running
- [ ] Health endpoint responds
- [ ] Core features functional
- [ ] Error rate acceptable
- [ ] Performance acceptable
- [ ] Database accessible
- [ ] Logs normal
- [ ] 30-minute stability achieved

---

## Communication Protocol

### Incident Communication Template

```markdown
# Production Incident: Rollback Executed

**Incident Date**: 2025-11-12
**Incident Time**: [TIME]
**Severity**: [CRITICAL/MAJOR/MINOR]
**Rollback Level**: [1/2/3]
**Status**: [IN PROGRESS/COMPLETED]

## Issue Description
[Describe what went wrong]

## Affected Features
- [ ] Agent spawning (GAP-001)
- [ ] File uploads (QW-001)
- [ ] MCP tracking (QW-002)

## Rollback Actions Taken
1. [Action 1]
2. [Action 2]
3. [Action 3]

## Current System Status
- Application: [RUNNING/STOPPED/DEGRADED]
- Health: [HEALTHY/UNHEALTHY]
- Performance: [NORMAL/DEGRADED]
- Data Integrity: [INTACT/COMPROMISED]

## User Impact
- Affected Users: [COUNT or PERCENTAGE]
- Impact Duration: [MINUTES]
- Data Loss: [YES/NO - describe if yes]

## Next Steps
1. [Immediate action 1]
2. [Immediate action 2]
3. [Investigation plan]

## Incident Owner
Name: _______________
Contact: _______________
```

### Notification Channels

1. **Immediate (< 5 minutes)**:
   - On-call engineer notified via phone
   - Deployment lead notified
   - Status page updated

2. **Within 15 minutes**:
   - Engineering team Slack notification
   - Management email notification
   - Customer support briefing

3. **Within 1 hour**:
   - Incident report created
   - Root cause analysis initiated
   - Customer communication (if applicable)

---

## Root Cause Analysis (Post-Rollback)

### Investigation Steps

```bash
# 1. Collect logs from failure period
pm2 logs app --lines 1000 > /tmp/incident-logs-$(date +%Y%m%d-%H%M%S).log

# 2. Extract error messages
grep -i "error\|exception\|failed" /tmp/incident-logs-*.log > /tmp/errors.log

# 3. Analyze error patterns
cat /tmp/errors.log | cut -d: -f1 | sort | uniq -c | sort -rn

# 4. Check system resources at time of incident
# (If monitoring tools available)
# Review CPU, memory, disk, network metrics

# 5. Review deployment differences
git diff v1.0.0-stable v1.1.0-agent-optimizations

# 6. Reproduce issue in staging (if possible)
# Deploy failed version to staging
# Run comprehensive tests
# Document reproduction steps
```

### RCA Template

```markdown
# Root Cause Analysis: [Incident Name]

**Date**: 2025-11-12
**Incident**: [Brief description]
**Rollback Level**: [1/2/3]

## Timeline
- 14:00 - Deployment started
- 14:30 - Issue first detected
- 14:35 - Rollback initiated
- 14:50 - Rollback completed
- 15:00 - System stable

## Root Cause
[Technical explanation of what caused the failure]

## Contributing Factors
1. [Factor 1]
2. [Factor 2]

## Why It Wasn't Caught Earlier
- Testing gaps: [describe]
- Monitoring gaps: [describe]
- Code review gaps: [describe]

## Corrective Actions
1. **Immediate** (< 24 hours):
   - [Action 1]
2. **Short-term** (< 1 week):
   - [Action 2]
3. **Long-term** (< 1 month):
   - [Action 3]

## Prevention Measures
- Improved testing: [specific tests to add]
- Enhanced monitoring: [specific alerts to add]
- Code review checklist: [items to add]
- Deployment process: [changes to make]

## Lessons Learned
[Key takeaways for team]
```

---

## Rollback Testing & Validation

### Quarterly Rollback Drills

```bash
# Schedule: Every quarter
# Duration: 2 hours
# Participants: All deployment team members

# Drill procedure:
1. Deploy to staging environment
2. Simulate failure scenario
3. Execute rollback procedure
4. Time the rollback process
5. Verify system restoration
6. Document lessons learned
7. Update procedures if needed

# Drill checklist:
- [ ] All team members available
- [ ] Staging environment ready
- [ ] Failure scenario documented
- [ ] Rollback executed successfully
- [ ] Time target met (Level 2: < 15 min)
- [ ] System fully restored
- [ ] Improvements identified
- [ ] Documentation updated
```

---

## Emergency Rollback Contact Tree

```
Incident Detected
       ↓
On-Call Engineer
   ↓         ↓
Tech Lead   Deployment Lead
   ↓              ↓
Dev Team    Operations Manager
                  ↓
            Executive Team
            (if critical)
```

---

## Quick Reference Card

```bash
# EMERGENCY ROLLBACK COMMANDS

# Level 1: Feature Toggle (2 min)
echo "ENABLE_PARALLEL_SPAWNING=false" >> .env
echo "ENABLE_PARALLEL_UPLOADS=false" >> .env
echo "ENABLE_MCP_TRACKING=false" >> .env
pm2 restart app

# Level 2: Code Rollback (15 min)
git checkout v1.0.0-stable
npm ci --production
npm run build
pm2 reload app

# Level 3: Full Restore (45 min)
pm2 stop app
mv app app-failed-$(date +%Y%m%d-%H%M%S)
tar -xzf /backups/app-backups/[backup-file].tar.gz -C app
cd app && npm ci --production
pm2 start app

# Health Check
curl http://localhost:3000/api/health

# Monitor
pm2 logs app --lines 100
pm2 monit
```

---

**End of Rollback Procedures**
