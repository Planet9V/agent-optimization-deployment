# Production Monitoring & Alerting Guide

**File**: MONITORING_GUIDE.md
**Created**: 2025-11-12
**Purpose**: Comprehensive monitoring for GAP-001, QW-001, QW-002 deployments
**Status**: ACTIVE

---

## Executive Summary

This guide establishes monitoring and alerting for three critical optimizations:
- **GAP-001**: Parallel agent spawning (10-37x speedup)
- **QW-001**: Parallel S3 uploads (5-10x speedup)
- **QW-002**: MCP integration tracking

**Monitoring Philosophy**: Observe, Alert, Respond, Learn

---

## Monitoring Architecture

```
┌────────────────────────────────────────────────┐
│         Application Instrumentation            │
│  - Performance metrics                         │
│  - Error tracking                              │
│  - Business metrics                            │
└─────────────┬──────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────────┐
│           Log Aggregation Layer                │
│  - pm2 logs                                    │
│  - Application logs                            │
│  - System logs                                 │
└─────────────┬──────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────────┐
│          Metrics Collection                    │
│  - Prometheus/StatsD                           │
│  - Custom metrics endpoint                     │
│  - Health checks                               │
└─────────────┬──────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────────┐
│            Alert Manager                       │
│  - Threshold-based alerts                      │
│  - Anomaly detection                           │
│  - On-call routing                             │
└─────────────┬──────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────────┐
│        Notification Channels                   │
│  - PagerDuty/OpsGenie                         │
│  - Slack                                       │
│  - Email                                       │
└────────────────────────────────────────────────┘
```

---

## Key Performance Indicators (KPIs)

### GAP-001: Parallel Agent Spawning

#### Primary Metrics

**agent.spawn.duration**
- **Description**: Time to spawn agents (milliseconds)
- **Target**: < 250ms for 5 agents
- **Critical Threshold**: > 500ms (50% degradation)
- **Alert**: Warning if > 350ms for 10 minutes

**agent.spawn.speedup_factor**
- **Description**: Speedup compared to sequential baseline
- **Target**: 10-37x
- **Critical Threshold**: < 5x (50% below minimum target)
- **Alert**: Critical if < 8x for 5 minutes

**agent.spawn.success_rate**
- **Description**: Percentage of successful spawns
- **Target**: 100%
- **Critical Threshold**: < 95%
- **Alert**: Warning if < 98%, Critical if < 95%

**agent.spawn.fallback_rate**
- **Description**: Percentage using fallback (sequential) spawning
- **Target**: 0%
- **Critical Threshold**: > 10%
- **Alert**: Warning if > 5%, Investigation if > 10%

#### Secondary Metrics

**agent.spawn.batch_count**
- **Description**: Number of batches created for dependency management
- **Target**: Varies by agent count and dependencies
- **Alert**: Investigation if > 2x expected

**agent.spawn.coordination_overhead**
- **Description**: Time spent in coordination between batches
- **Target**: < 5% of total duration
- **Alert**: Warning if > 10%

**mcp.agents_spawn_parallel.latency**
- **Description**: MCP tool call latency
- **Target**: < 100ms
- **Critical Threshold**: > 500ms
- **Alert**: Warning if > 200ms for 10 minutes

#### Logging Examples

```bash
# Successful parallel spawn
[2025-11-12T15:30:45.123Z] INFO: Parallel Agent Spawning (GAP-001)
  Agents: 5
  Duration: 187ms
  Speedup: 20.05x
  Success: 5/5
  Batches: 2

# Performance degradation warning
[2025-11-12T15:45:22.456Z] WARN: Agent spawn performance degraded
  Agents: 5
  Duration: 412ms (target: <250ms)
  Speedup: 9.10x (below 10x target)
  Batches: 2

# Fallback activation
[2025-11-12T16:00:33.789Z] ERROR: MCP parallel spawn failed, fallback to sequential
  Error: MCP connection timeout
  Agents: 5
  Fallback Duration: 3750ms
```

---

### QW-001: Parallel S3 Uploads

#### Primary Metrics

**upload.duration**
- **Description**: Total upload time for batch (milliseconds)
- **Target**: < 700ms for 20 files
- **Critical Threshold**: > 2000ms (3x baseline)
- **Alert**: Warning if > 1000ms for 10 minutes

**upload.speedup_factor**
- **Description**: Speedup compared to sequential baseline
- **Target**: 5-10x
- **Critical Threshold**: < 3x
- **Alert**: Warning if < 4x for 10 minutes

**upload.success_rate**
- **Description**: Percentage of files uploaded successfully
- **Target**: 100%
- **Critical Threshold**: < 90%
- **Alert**: Warning if < 95%, Critical if < 90%

**upload.partial_failure_rate**
- **Description**: Percentage of batches with partial failures (HTTP 207)
- **Target**: 0%
- **Critical Threshold**: > 10%
- **Alert**: Investigation if > 5%

#### Secondary Metrics

**upload.file_size_avg**
- **Description**: Average file size in batch
- **Target**: < 100MB (per file limit)
- **Alert**: Warning if approaching limit

**upload.concurrent_operations**
- **Description**: Number of parallel uploads in progress
- **Target**: Match file count (up to 20)
- **Alert**: Investigation if < file count (not parallelizing)

**s3.connection_errors**
- **Description**: S3/MinIO connection failures
- **Target**: 0
- **Critical Threshold**: > 5 per minute
- **Alert**: Critical if > 3 per minute

#### Logging Examples

```bash
# Successful parallel upload
[2025-11-12T15:30:45.123Z] INFO: [Upload] Completed in 687ms
  Files: 20
  Success: 20/20
  Speedup: 10.89x
  Partial Failures: 0

# Partial failure (HTTP 207)
[2025-11-12T15:45:22.456Z] WARN: [Upload] Partial success in 542ms
  Files: 20
  Success: 18/20
  Failed: 2
  Failures: [
    { file: "large-doc.pdf", error: "S3 timeout" },
    { file: "network-issue.pdf", error: "Connection reset" }
  ]

# Complete failure
[2025-11-12T16:00:33.789Z] ERROR: [Upload] All files failed in 123ms
  Files: 5
  Success: 0/5
  Error: "S3 connection refused"
  Status: 500
```

---

### QW-002: MCP Integration Tracking

#### Primary Metrics

**mcp.store.success_rate**
- **Description**: Percentage of successful MCP storage operations
- **Target**: 100%
- **Critical Threshold**: < 90%
- **Alert**: Warning if < 95%, Critical if < 90%

**mcp.store.latency**
- **Description**: Time to store data in MCP (milliseconds)
- **Target**: < 150ms
- **Critical Threshold**: > 500ms
- **Alert**: Warning if > 300ms for 10 minutes

**mcp.query.latency**
- **Description**: Time to query data from MCP (milliseconds)
- **Target**: < 100ms
- **Critical Threshold**: > 300ms
- **Alert**: Warning if > 200ms for 10 minutes

**mcp.graceful_degradation_rate**
- **Description**: Percentage of operations falling back to local-only
- **Target**: 0%
- **Critical Threshold**: > 10%
- **Alert**: Investigation if > 5%

#### Secondary Metrics

**agent_activities.stored_count**
- **Description**: Number of agent activities stored
- **Target**: Grows with agent usage
- **Alert**: Investigation if stagnant for > 1 hour

**agent_metrics.stored_count**
- **Description**: Number of metric snapshots stored
- **Target**: Grows with agent activity
- **Alert**: Investigation if not growing

**wiki_notifications.queued_count**
- **Description**: Number of pending wiki notifications
- **Target**: < 10
- **Critical Threshold**: > 100
- **Alert**: Warning if > 50, Critical if > 100

**mcp.database_size**
- **Description**: Size of .swarm/memory.db (MB)
- **Target**: Grows linearly with usage
- **Critical Threshold**: > 1GB
- **Alert**: Warning if > 500MB, Investigation if > 1GB

#### Logging Examples

```bash
# Successful MCP storage
[2025-11-12T15:30:45.123Z] INFO: Agent activity stored in MCP
  Namespace: agent-activities
  Key: agent-abc123-spawn
  TTL: 604800s (7 days)
  Latency: 87ms

# MCP graceful degradation
[2025-11-12T15:45:22.456Z] WARN: Failed to persist agent spawn to MCP
  Agent: agent-def456
  Error: MCP connection timeout
  Fallback: Local tracking active
  Impact: No cross-session persistence

# Database growth warning
[2025-11-12T16:00:33.789Z] WARN: MCP memory database growing large
  Database: .swarm/memory.db
  Size: 523MB
  Records: ~2.5M
  Recommendation: Review TTL settings and cleanup policy
```

---

## System Health Metrics

### Application Performance

**api.response_time**
- **Description**: Average API response time (milliseconds)
- **Target**: < 100ms (p50), < 500ms (p95), < 2000ms (p99)
- **Alert**: Warning if p95 > 1000ms, Critical if p99 > 5000ms

**api.request_rate**
- **Description**: Requests per second
- **Target**: Varies by load
- **Alert**: Investigation if drops > 50% suddenly

**api.error_rate**
- **Description**: Percentage of requests resulting in 5xx errors
- **Target**: < 0.1%
- **Critical Threshold**: > 1%
- **Alert**: Warning if > 0.5%, Critical if > 1%

### Resource Utilization

**system.cpu_usage**
- **Description**: CPU utilization percentage
- **Target**: < 70%
- **Critical Threshold**: > 90%
- **Alert**: Warning if > 80% for 10 minutes

**system.memory_usage**
- **Description**: Memory utilization percentage
- **Target**: < 80%
- **Critical Threshold**: > 95%
- **Alert**: Warning if > 85%, Critical if > 95%

**system.disk_usage**
- **Description**: Disk utilization percentage
- **Target**: < 70%
- **Critical Threshold**: > 90%
- **Alert**: Warning if > 80%, Critical if > 90%

**node.event_loop_lag**
- **Description**: Node.js event loop delay (milliseconds)
- **Target**: < 50ms
- **Critical Threshold**: > 200ms
- **Alert**: Warning if > 100ms, Critical if > 200ms

---

## Monitoring Commands

### Real-Time Monitoring

```bash
# 1. Application status
pm2 status app

# 2. Real-time logs
pm2 logs app --lines 100

# 3. Live performance monitoring
pm2 monit

# 4. Filter for GAP-001 metrics
pm2 logs app | grep "Parallel Agent Spawning"

# 5. Filter for QW-001 metrics
pm2 logs app | grep "\[Upload\] Completed"

# 6. Filter for QW-002 metrics
pm2 logs app | grep "MCP"

# 7. Error monitoring
pm2 logs app | grep -i "error\|exception\|failed"

# 8. Performance warnings
pm2 logs app | grep -i "warn\|degraded\|slow"
```

### Health Checks

```bash
# Application health endpoint
curl http://localhost:3000/api/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "1.1.0",
#   "timestamp": "2025-11-12T15:30:45.123Z",
#   "uptime": 86400,
#   "memory": {
#     "used": 245,
#     "total": 512
#   }
# }

# MCP health check
npx claude-flow@alpha --version

# Database size check
ls -lh .swarm/memory.db

# Disk space check
df -h

# Memory check
free -h

# CPU check
top -bn1 | grep "Cpu(s)"
```

### Metrics Collection

```bash
# Create metrics collection script
cat > /opt/monitoring/collect-metrics.sh << 'EOF'
#!/bin/bash

TIMESTAMP=$(date -Iseconds)
METRICS_FILE="/var/log/app-metrics.log"

# Agent spawning metrics
SPAWN_DURATION=$(pm2 logs app --lines 100 --nostream | \
  grep "Parallel Agent Spawning" | \
  tail -1 | \
  sed -n 's/.*Duration: \([0-9]*\)ms.*/\1/p')

SPAWN_SPEEDUP=$(pm2 logs app --lines 100 --nostream | \
  grep "Speedup:" | \
  tail -1 | \
  sed -n 's/.*Speedup: \([0-9.]*\)x.*/\1/p')

# Upload metrics
UPLOAD_DURATION=$(pm2 logs app --lines 100 --nostream | \
  grep "\[Upload\] Completed" | \
  tail -1 | \
  sed -n 's/.*in \([0-9]*\)ms.*/\1/p')

# System metrics
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
MEM_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1)

# Log metrics
echo "$TIMESTAMP,spawn_duration,$SPAWN_DURATION" >> $METRICS_FILE
echo "$TIMESTAMP,spawn_speedup,$SPAWN_SPEEDUP" >> $METRICS_FILE
echo "$TIMESTAMP,upload_duration,$UPLOAD_DURATION" >> $METRICS_FILE
echo "$TIMESTAMP,cpu_usage,$CPU_USAGE" >> $METRICS_FILE
echo "$TIMESTAMP,mem_usage,$MEM_USAGE" >> $METRICS_FILE
echo "$TIMESTAMP,disk_usage,$DISK_USAGE" >> $METRICS_FILE
EOF

chmod +x /opt/monitoring/collect-metrics.sh

# Run every minute via cron
echo "* * * * * /opt/monitoring/collect-metrics.sh" | crontab -
```

---

## Alert Configuration

### Alert Severity Levels

**🔴 CRITICAL (P1)**:
- Page on-call engineer immediately
- 5-minute SLA for acknowledgment
- Executive notification if not resolved in 30 minutes

**🟡 WARNING (P2)**:
- Slack notification to engineering channel
- 15-minute SLA for acknowledgment
- Escalate to CRITICAL if not resolved in 1 hour

**🔵 INFO (P3)**:
- Email notification
- 24-hour SLA for acknowledgment
- Trend monitoring and investigation

### Alert Rules

#### GAP-001 Alert Rules

```yaml
# Agent spawn performance degradation
- alert: AgentSpawnPerformanceDegraded
  expr: agent_spawn_duration > 350
  for: 10m
  severity: WARNING
  annotations:
    summary: "Agent spawn duration above target"
    description: "5-agent spawn taking >350ms (target: <250ms)"
    action: "Check MCP connectivity and system resources"

# Agent spawn critical failure
- alert: AgentSpawnCriticalFailure
  expr: agent_spawn_speedup < 8
  for: 5m
  severity: CRITICAL
  annotations:
    summary: "Agent spawn speedup below minimum"
    description: "Speedup factor <8x (minimum target: 10x)"
    action: "Execute Level 1 rollback immediately"

# High fallback rate
- alert: AgentSpawnHighFallbackRate
  expr: agent_spawn_fallback_rate > 10
  for: 10m
  severity: WARNING
  annotations:
    summary: "High rate of fallback to sequential spawning"
    description: "Fallback rate >10% indicates MCP issues"
    action: "Investigate MCP connection and errors"

# MCP timeout
- alert: MCPAgentSpawnTimeout
  expr: mcp_agents_spawn_parallel_latency > 500
  for: 5m
  severity: WARNING
  annotations:
    summary: "MCP agent spawn tool timing out"
    description: "MCP latency >500ms (target: <100ms)"
    action: "Check claude-flow service health"
```

#### QW-001 Alert Rules

```yaml
# Upload performance degradation
- alert: UploadPerformanceDegraded
  expr: upload_duration > 1000
  for: 10m
  severity: WARNING
  annotations:
    summary: "Upload duration above target"
    description: "20-file upload taking >1000ms (target: <700ms)"
    action: "Check S3/MinIO connectivity and performance"

# High partial failure rate
- alert: UploadHighPartialFailureRate
  expr: upload_partial_failure_rate > 5
  for: 10m
  severity: WARNING
  annotations:
    summary: "High rate of partial upload failures"
    description: "HTTP 207 responses >5%"
    action: "Investigate S3 errors and network issues"

# Upload critical failure
- alert: UploadCriticalFailure
  expr: upload_success_rate < 90
  for: 5m
  severity: CRITICAL
  annotations:
    summary: "Upload success rate critically low"
    description: "Success rate <90%"
    action: "Execute Level 1 rollback immediately"

# S3 connection errors
- alert: S3ConnectionErrors
  expr: s3_connection_errors > 3
  for: 1m
  severity: CRITICAL
  annotations:
    summary: "High rate of S3 connection failures"
    description: "S3 errors >3/min"
    action: "Check S3/MinIO service health"
```

#### QW-002 Alert Rules

```yaml
# MCP storage failure
- alert: MCPStorageFailure
  expr: mcp_store_success_rate < 95
  for: 10m
  severity: WARNING
  annotations:
    summary: "MCP storage success rate low"
    description: "Storage success <95%"
    action: "Check MCP service and disk space"

# High graceful degradation
- alert: MCPHighDegradationRate
  expr: mcp_graceful_degradation_rate > 5
  for: 10m
  severity: WARNING
  annotations:
    summary: "High rate of MCP fallback to local-only"
    description: "Degradation rate >5%"
    action: "Investigate MCP connectivity issues"

# Database size warning
- alert: MCPDatabaseLarge
  expr: mcp_database_size > 500
  for: 1h
  severity: INFO
  annotations:
    summary: "MCP memory database growing large"
    description: "Database >500MB"
    action: "Review TTL settings and cleanup policy"

# Wiki notification queue backup
- alert: WikiNotificationQueueBackup
  expr: wiki_notifications_queued_count > 50
  for: 30m
  severity: WARNING
  annotations:
    summary: "Wiki notification queue backing up"
    description: "Queue >50 notifications"
    action: "Check Wiki Agent processing"
```

---

## Dashboard Configuration

### Recommended Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│                    System Overview                       │
│  - Overall Health Status                                 │
│  - Request Rate & Error Rate                            │
│  - CPU/Memory/Disk Usage                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│           GAP-001: Parallel Agent Spawning              │
│  - Spawn Duration (line chart)                          │
│  - Speedup Factor (line chart)                          │
│  - Success Rate (gauge)                                 │
│  - Fallback Rate (bar chart)                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│           QW-001: Parallel S3 Uploads                   │
│  - Upload Duration (line chart)                         │
│  - Success Rate (gauge)                                 │
│  - Partial Failure Rate (line chart)                    │
│  - Files Uploaded (counter)                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│           QW-002: MCP Integration                       │
│  - Storage Success Rate (gauge)                         │
│  - Storage Latency (line chart)                         │
│  - Database Size (trend)                                │
│  - Activities Stored (counter)                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                Recent Alerts & Issues                    │
│  - Active Alerts                                        │
│  - Recent Incidents                                     │
│  - Error Log Sample                                     │
└─────────────────────────────────────────────────────────┘
```

### Grafana Dashboard Example

```json
{
  "dashboard": {
    "title": "Agent Optimizations Monitoring",
    "panels": [
      {
        "id": 1,
        "title": "Agent Spawn Duration",
        "type": "graph",
        "targets": [{
          "expr": "agent_spawn_duration",
          "legendFormat": "Duration (ms)"
        }],
        "yaxis": {
          "label": "Milliseconds",
          "min": 0,
          "max": 500
        },
        "thresholds": [
          { "value": 250, "color": "green", "label": "Target" },
          { "value": 350, "color": "yellow", "label": "Warning" },
          { "value": 500, "color": "red", "label": "Critical" }
        ]
      },
      {
        "id": 2,
        "title": "Agent Spawn Speedup Factor",
        "type": "graph",
        "targets": [{
          "expr": "agent_spawn_speedup",
          "legendFormat": "Speedup (x)"
        }],
        "yaxis": {
          "label": "Speedup Factor",
          "min": 0,
          "max": 40
        },
        "thresholds": [
          { "value": 10, "color": "green", "label": "Minimum Target" },
          { "value": 8, "color": "yellow", "label": "Warning" },
          { "value": 5, "color": "red", "label": "Critical" }
        ]
      }
    ]
  }
}
```

---

## Incident Response Playbook

### Response Workflow

```
Alert Triggered
      ↓
Acknowledge (< 5 min)
      ↓
Assess Severity
      ↓
┌─────┴─────┐
│           │
CRITICAL   WARNING
│           │
│           ├→ Investigate
│           ├→ Document
│           └→ Plan Fix
│
├→ Page On-Call
├→ Execute Rollback (if needed)
├→ Investigate
└→ Post-Incident Review
```

### Response Commands

```bash
# 1. Acknowledge alert
echo "ACKNOWLEDGED: $(date)" >> /var/log/incident-log.txt

# 2. Gather diagnostic information
pm2 status app
pm2 logs app --lines 200 > /tmp/incident-logs.txt
df -h > /tmp/incident-disk.txt
free -h > /tmp/incident-memory.txt
top -bn1 > /tmp/incident-cpu.txt

# 3. Check recent deployments
git log --oneline -10
git describe --tags

# 4. Execute rollback (if needed)
# See ROLLBACK_PROCEDURES.md

# 5. Collect metrics for analysis
/opt/monitoring/collect-metrics.sh
```

---

## Regular Maintenance Tasks

### Daily Tasks

```bash
# Morning health check
curl http://production-domain/api/health

# Check error rate
pm2 logs app --lines 1000 | grep -i error | wc -l

# Verify performance metrics
tail -100 /var/log/app-metrics.log

# Check disk space
df -h

# Review overnight alerts
cat /var/log/alerts.log | grep $(date -d yesterday +%Y-%m-%d)
```

### Weekly Tasks

```bash
# Generate performance report
node scripts/generate-weekly-report.js

# Review slow queries/operations
pm2 logs app --lines 10000 | grep "slow\|timeout"

# Check database growth
ls -lh .swarm/memory.db

# Review and cleanup old logs
find /var/log -name "*.log" -mtime +30 -delete

# Verify backups
ls -lt /backups/app-backups/ | head -10
```

### Monthly Tasks

```bash
# Review alert thresholds
# Adjust based on performance trends

# Update monitoring dashboards
# Add new metrics, remove obsolete ones

# Capacity planning review
# Analyze resource usage trends

# Incident retrospective
# Review all incidents from past month

# Monitoring system health check
# Verify all monitoring tools functional
```

---

## Troubleshooting Guide

### Common Issues & Solutions

#### Issue: High Agent Spawn Duration

**Symptoms**:
- Spawn duration > 350ms
- Speedup factor < 10x

**Investigation**:
```bash
# Check MCP connectivity
npx claude-flow@alpha --version

# Check system resources
top -bn1
free -h

# Review recent spawns
pm2 logs app | grep "Parallel Agent Spawning" | tail -20
```

**Solutions**:
1. Restart MCP service: `npm run mcp:restart`
2. Reduce concurrent spawns: Adjust `maxConcurrency` parameter
3. Check for resource contention: Kill unnecessary processes

---

#### Issue: Upload Timeouts

**Symptoms**:
- HTTP 207 responses frequent
- Timeout errors in logs
- Upload duration > 2000ms

**Investigation**:
```bash
# Check S3/MinIO connectivity
curl http://minio-endpoint/health

# Check network latency
ping minio-endpoint

# Review upload logs
pm2 logs app | grep "\[Upload\]" | tail -20
```

**Solutions**:
1. Restart S3/MinIO service
2. Reduce parallel upload count: Lower file batch limit
3. Increase timeout: Adjust S3 client timeout settings
4. Check network: Verify network connectivity and bandwidth

---

#### Issue: MCP Storage Failures

**Symptoms**:
- "Failed to persist" warnings
- High degradation rate
- Database not growing

**Investigation**:
```bash
# Check MCP service
npx claude-flow@alpha memory query "test:probe" --reasoningbank

# Check disk space
df -h

# Check database permissions
ls -la .swarm/memory.db

# Check database size
ls -lh .swarm/memory.db
```

**Solutions**:
1. Restart MCP service: `npm run mcp:restart`
2. Free disk space: Clean up old logs and backups
3. Fix permissions: `chmod 666 .swarm/memory.db`
4. Compact database: Run cleanup script

---

## Contact Information

### Monitoring Team

**Primary Contact**: _______________
**Email**: _______________
**Phone**: _______________
**Slack**: #monitoring-team

### On-Call Schedule

**Week of 2025-11-12**:
- Monday-Wednesday: _______________
- Thursday-Saturday: _______________
- Sunday: _______________

### Escalation Path

```
Level 1: On-Call Engineer (5 min SLA)
    ↓ If not resolved in 30 min
Level 2: Tech Lead (15 min SLA)
    ↓ If not resolved in 1 hour
Level 3: Engineering Manager (30 min SLA)
    ↓ If critical and not resolved in 2 hours
Level 4: CTO (immediate)
```

---

**End of Monitoring Guide**
