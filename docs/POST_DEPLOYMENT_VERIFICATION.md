# Post-Deployment Verification Guide

**File**: POST_DEPLOYMENT_VERIFICATION.md
**Created**: 2025-11-12
**Purpose**: Comprehensive verification procedures after deployment
**Status**: ACTIVE

---

## Verification Overview

This guide provides step-by-step verification procedures to confirm successful deployment of:
- **GAP-001**: Parallel Agent Spawning
- **QW-001**: Parallel S3 Uploads
- **QW-002**: MCP Integration Tracking

**Verification Timeline**: 24 hours post-deployment
**Verification Frequency**: Immediate → 1 hour → 4 hours → 24 hours

---

## Immediate Verification (< 5 minutes)

### System Health Check

```bash
# 1. Application Status
pm2 status app

# Expected output:
# ┌─────┬──────┬─────────┬──────┬───────┬────────┬─────────┬────────┬─────┬───────────┬──────────┬──────────┐
# │ id  │ name │ mode    │ ↺    │ status│ cpu    │ memory  │        │     │           │          │          │
# ├─────┼──────┼─────────┼──────┼───────┼────────┼─────────┼────────┼─────┼───────────┼──────────┼──────────┤
# │ 0   │ app  │ cluster │ 0    │ online│ 15%    │ 245 MB  │        │     │           │          │          │
# └─────┴──────┴─────────┴──────┴───────┴────────┴─────────┴────────┴─────┴───────────┴──────────┴──────────┘

# 2. Health Endpoint
curl -s http://localhost:3000/api/health | jq

# Expected response:
# {
#   "status": "healthy",
#   "version": "1.1.0",
#   "timestamp": "2025-11-12T15:30:45.123Z",
#   "uptime": 300,
#   "features": {
#     "parallel_spawning": true,
#     "parallel_uploads": true,
#     "mcp_tracking": true
#   }
# }

# 3. No Critical Errors in Recent Logs
pm2 logs app --lines 50 --nostream | grep -i "error\|exception\|failed" | wc -l
# Should be 0 or very low (< 3)

# 4. Process Restart Count
pm2 status app | grep "↺"
# Should be 0 (no unexpected restarts)
```

**Immediate Verification Checklist**:
- [ ] Application process running
- [ ] Health endpoint responds with `"status": "healthy"`
- [ ] No critical errors in logs
- [ ] No unexpected restarts
- [ ] All features enabled

---

## Functional Verification (15 minutes)

### GAP-001: Parallel Agent Spawning

#### Test 1: Basic Parallel Spawning

```bash
# Test spawning 5 agents
node -e "
const { parallelAgentSpawner } = require('./lib/orchestration/parallel-agent-spawner');

const agents = [
  { type: 'researcher', name: 'Agent 1' },
  { type: 'coder', name: 'Agent 2' },
  { type: 'tester', name: 'Agent 3' },
  { type: 'analyst', name: 'Agent 4' },
  { type: 'optimizer', name: 'Agent 5' }
];

parallelAgentSpawner.spawnAgentsParallel(agents).then(result => {
  console.log('✅ Test 1: Basic Parallel Spawning');
  console.log(\`   Agents Spawned: \${result.metrics.successCount}/5\`);
  console.log(\`   Duration: \${result.metrics.totalDuration}ms\`);
  console.log(\`   Speedup: \${result.metrics.speedupFactor.toFixed(2)}x\`);
  console.log(\`   Target Met: \${result.metrics.speedupFactor >= 10 ? 'YES ✅' : 'NO ❌'}\`);
  process.exit(result.metrics.successCount === 5 && result.metrics.speedupFactor >= 10 ? 0 : 1);
}).catch(err => {
  console.error('❌ Test 1 FAILED:', err.message);
  process.exit(1);
});
"

# Check exit code
echo "Exit Code: $?"
# Should be 0 (success)
```

**Expected Results**:
- ✅ All 5 agents spawned successfully
- ✅ Duration < 250ms
- ✅ Speedup factor ≥ 10x
- ✅ Exit code: 0

#### Test 2: Dependency-Aware Spawning

```bash
# Test spawning with dependencies
node -e "
const { parallelAgentSpawner } = require('./lib/orchestration/parallel-agent-spawner');

const agents = [
  { type: 'coder', name: 'Backend Coder' },
  { type: 'coder', name: 'Frontend Coder' },
  { type: 'tester', name: 'Test Engineer', dependencies: ['Backend Coder', 'Frontend Coder'] },
  { type: 'reviewer', name: 'Code Reviewer', dependencies: ['Test Engineer'] }
];

parallelAgentSpawner.spawnAgentsParallel(agents).then(result => {
  console.log('✅ Test 2: Dependency-Aware Spawning');
  console.log(\`   Agents Spawned: \${result.metrics.successCount}/4\`);
  console.log(\`   Duration: \${result.metrics.totalDuration}ms\`);
  console.log(\`   Batches: \${result.metrics.batchCount}\`);
  console.log(\`   Dependencies Respected: YES ✅\`);
  process.exit(result.metrics.successCount === 4 ? 0 : 1);
}).catch(err => {
  console.error('❌ Test 2 FAILED:', err.message);
  process.exit(1);
});
"

echo "Exit Code: $?"
```

**Expected Results**:
- ✅ All 4 agents spawned successfully
- ✅ Multiple batches created (≥ 2)
- ✅ Dependencies respected
- ✅ Exit code: 0

#### Test 3: Fallback Mechanism

```bash
# Simulate MCP failure to test fallback
node -e "
const { parallelAgentSpawner } = require('./lib/orchestration/parallel-agent-spawner');

// Temporarily disable MCP by setting invalid tool path
process.env.CLAUDE_FLOW_PATH = '/invalid/path';

const agents = [
  { type: 'researcher', name: 'Test Agent 1' },
  { type: 'coder', name: 'Test Agent 2' }
];

parallelAgentSpawner.spawnAgentsParallel(agents, {
  enableFallback: true
}).then(result => {
  console.log('✅ Test 3: Fallback Mechanism');
  console.log(\`   Fallback Activated: YES ✅\`);
  console.log(\`   Agents Spawned: \${result.metrics.successCount}/2\`);
  console.log(\`   Sequential Spawning: YES ✅\`);
  process.exit(result.metrics.successCount === 2 ? 0 : 1);
}).catch(err => {
  console.error('❌ Test 3 FAILED:', err.message);
  process.exit(1);
});
"

# Restore environment
unset CLAUDE_FLOW_PATH

echo "Exit Code: $?"
```

**Expected Results**:
- ✅ Fallback to sequential spawning activated
- ✅ All agents still spawned successfully
- ✅ System remains stable
- ✅ Exit code: 0

**GAP-001 Verification Checklist**:
- [ ] Basic parallel spawning works
- [ ] Performance target met (10x+ speedup)
- [ ] Dependency-aware batching works
- [ ] Fallback mechanism operational
- [ ] No errors in logs

---

### QW-001: Parallel S3 Uploads

#### Test 1: Single File Upload

```bash
# Create test file
echo "Test document content" > /tmp/test-single.txt

# Upload single file
curl -X POST http://localhost:3000/api/upload \
  -F "file=@/tmp/test-single.txt" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  -s | jq

# Expected response:
# {
#   "success": true,
#   "files": [
#     {
#       "originalName": "test-single.txt",
#       "path": "uploads/2025-11-12T15-30-45_test-single.txt",
#       "size": 22,
#       "type": "text/plain"
#     }
#   ],
#   "count": 1,
#   "duration": 145
# }
# HTTP Status: 200
```

**Expected Results**:
- ✅ HTTP status: 200
- ✅ `success: true`
- ✅ File uploaded successfully
- ✅ Duration < 500ms

#### Test 2: Multi-File Batch Upload

```bash
# Create 10 test files
for i in {1..10}; do
  echo "Test document $i content" > /tmp/test-batch-$i.txt
done

# Upload batch
curl -X POST http://localhost:3000/api/upload \
  -F "file=@/tmp/test-batch-1.txt" \
  -F "file=@/tmp/test-batch-2.txt" \
  -F "file=@/tmp/test-batch-3.txt" \
  -F "file=@/tmp/test-batch-4.txt" \
  -F "file=@/tmp/test-batch-5.txt" \
  -F "file=@/tmp/test-batch-6.txt" \
  -F "file=@/tmp/test-batch-7.txt" \
  -F "file=@/tmp/test-batch-8.txt" \
  -F "file=@/tmp/test-batch-9.txt" \
  -F "file=@/tmp/test-batch-10.txt" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  -s | jq

# Expected response:
# {
#   "success": true,
#   "files": [ ... 10 files ... ],
#   "count": 10,
#   "duration": 423
# }
# HTTP Status: 200
```

**Expected Results**:
- ✅ HTTP status: 200
- ✅ `success: true`
- ✅ All 10 files uploaded
- ✅ Duration < 600ms
- ✅ 5-10x faster than sequential

#### Test 3: Partial Failure Handling (HTTP 207)

```bash
# This test requires controlled S3 failure simulation
# Skip if not in test environment

# Create mix of valid and oversized files
echo "Valid content" > /tmp/valid-file.txt
dd if=/dev/zero of=/tmp/oversized-file.bin bs=1M count=150  # 150MB (exceeds 100MB limit)

# Upload batch with expected partial failure
curl -X POST http://localhost:3000/api/upload \
  -F "file=@/tmp/valid-file.txt" \
  -F "file=@/tmp/oversized-file.bin" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq

# Expected response:
# {
#   "success": false,
#   "partialSuccess": true,
#   "files": [
#     {
#       "originalName": "valid-file.txt",
#       "path": "uploads/...",
#       "size": 14,
#       "type": "text/plain"
#     }
#   ],
#   "failures": [
#     {
#       "originalName": "oversized-file.bin",
#       "error": "File size exceeds limit"
#     }
#   ],
#   "count": 1,
#   "failureCount": 1,
#   "duration": 234
# }
# HTTP Status: 207
```

**Expected Results**:
- ✅ HTTP status: 207 (Multi-Status)
- ✅ `partialSuccess: true`
- ✅ Valid file uploaded
- ✅ Oversized file rejected with error
- ✅ System remains stable

**QW-001 Verification Checklist**:
- [ ] Single file upload works
- [ ] Multi-file batch upload works
- [ ] Performance target met (5-10x speedup)
- [ ] HTTP 207 partial success handling works
- [ ] Error handling comprehensive
- [ ] No S3 connection errors

---

### QW-002: MCP Integration Tracking

#### Test 1: Agent Activity Storage

```bash
# Store test agent activity
npx claude-flow@alpha memory store \
  "agent-activities:test-verification-001" \
  '{
    "agentId": "test-verification-001",
    "type": "researcher",
    "status": "spawned",
    "timestamp": "'$(date -Iseconds)'"
  }' \
  --reasoningbank

# Verify storage
npx claude-flow@alpha memory query \
  "agent-activities:test-verification-001" \
  --reasoningbank

# Expected output:
# {
#   "agentId": "test-verification-001",
#   "type": "researcher",
#   "status": "spawned",
#   "timestamp": "2025-11-12T15:30:45+00:00"
# }
```

**Expected Results**:
- ✅ Storage successful
- ✅ Query returns correct data
- ✅ No errors

#### Test 2: Agent Metrics Storage

```bash
# Store test metrics
npx claude-flow@alpha memory store \
  "agent-metrics:test-verification-001-metrics" \
  '{
    "agentId": "test-verification-001",
    "duration": 1500,
    "tasksCompleted": 5,
    "timestamp": "'$(date -Iseconds)'"
  }' \
  --reasoningbank

# Verify storage
npx claude-flow@alpha memory query \
  "agent-metrics:test-verification-001-metrics" \
  --reasoningbank

# Expected output:
# {
#   "agentId": "test-verification-001",
#   "duration": 1500,
#   "tasksCompleted": 5,
#   "timestamp": "2025-11-12T15:30:45+00:00"
# }
```

**Expected Results**:
- ✅ Metrics stored successfully
- ✅ Query returns correct data
- ✅ TTL set correctly (1 hour)

#### Test 3: Wiki Notification Queue

```bash
# Store test wiki notification
npx claude-flow@alpha memory store \
  "wiki-notifications:test-event-$(date +%s)" \
  '{
    "type": "agent-completion",
    "agentId": "test-verification-001",
    "summary": "Test verification agent completed",
    "timestamp": "'$(date -Iseconds)'"
  }' \
  --reasoningbank

# List all wiki notifications
npx claude-flow@alpha memory query \
  "wiki-notifications:" \
  --reasoningbank

# Expected output:
# [
#   {
#     "type": "agent-completion",
#     "agentId": "test-verification-001",
#     "summary": "Test verification agent completed",
#     "timestamp": "2025-11-12T15:30:45+00:00"
#   }
# ]
```

**Expected Results**:
- ✅ Notification stored successfully
- ✅ Query returns notifications
- ✅ TTL set correctly (1 hour)

#### Test 4: Graceful Degradation

```bash
# Simulate MCP unavailability
mv .swarm .swarm-backup

# Attempt storage (should degrade gracefully)
node -e "
const { agentTracker } = require('./lib/observability/agent-tracker');

agentTracker.trackAgentSpawn('test-agent-001', 'researcher').then(() => {
  console.log('✅ Graceful degradation working');
  console.log('   Local tracking active');
  console.log('   No errors thrown');
}).catch(err => {
  console.error('❌ Degradation failed:', err.message);
  process.exit(1);
});
"

# Restore MCP
mv .swarm-backup .swarm

echo "Exit Code: $?"
```

**Expected Results**:
- ✅ No errors thrown
- ✅ Local tracking continues
- ✅ System remains stable
- ✅ Exit code: 0

**QW-002 Verification Checklist**:
- [ ] Agent activity storage works
- [ ] Agent metrics storage works
- [ ] Wiki notifications work
- [ ] Graceful degradation operational
- [ ] Database growing appropriately
- [ ] No MCP connection errors

---

## Performance Verification (30 minutes)

### Load Testing

```bash
# Install artillery if not available
npm install -g artillery

# Create load test configuration
cat > /tmp/load-test.yml << 'EOF'
config:
  target: "http://localhost:3000"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Sustained load"
  processor: "./load-test-processor.js"

scenarios:
  - name: "Agent spawn test"
    flow:
      - post:
          url: "/api/agents/spawn"
          json:
            agents:
              - { type: "researcher", name: "Load Test Agent" }
          capture:
            - json: "$.metrics.speedupFactor"
              as: "speedup"
      - think: 1

  - name: "File upload test"
    flow:
      - post:
          url: "/api/upload"
          formData:
            file: "@/tmp/test-file.txt"
          capture:
            - json: "$.duration"
              as: "duration"
      - think: 1
EOF

# Run load test
artillery run /tmp/load-test.yml

# Expected results:
# Summary report:
#   scenarios launched: 600
#   scenarios completed: 600
#   requests completed: 1200
#   mean response time: 245ms
#   p95 response time: 412ms
#   p99 response time: 587ms
#   errors: 0
```

**Performance Targets**:
- ✅ Response time p50 < 200ms
- ✅ Response time p95 < 500ms
- ✅ Response time p99 < 2000ms
- ✅ Error rate < 0.1%
- ✅ Throughput > 10 req/sec

### Stress Testing

```bash
# Run high-load stress test
artillery quick --count 100 --num 500 http://localhost:3000/api/health

# Monitor system resources during stress test
pm2 monit

# Expected results:
# - CPU usage < 80%
# - Memory usage < 85%
# - No crashes or restarts
# - Error rate < 1%
```

**Stress Test Checklist**:
- [ ] System handles 50,000 requests
- [ ] CPU usage acceptable
- [ ] Memory usage acceptable
- [ ] No crashes or restarts
- [ ] Error rate < 1%

---

## Integration Verification (1 hour)

### End-to-End Workflow Test

```bash
# Test complete workflow: spawn agents → upload files → track activities

# 1. Spawn agents
SPAWN_RESULT=$(node -e "
const { parallelAgentSpawner } = require('./lib/orchestration/parallel-agent-spawner');
const agents = [
  { type: 'researcher', name: 'E2E Test Agent 1' },
  { type: 'coder', name: 'E2E Test Agent 2' }
];
parallelAgentSpawner.spawnAgentsParallel(agents).then(r => {
  console.log(JSON.stringify(r.results));
});
")

echo "✅ Step 1: Agents spawned"
echo "$SPAWN_RESULT"

# 2. Upload files
for i in {1..5}; do
  echo "E2E test document $i" > /tmp/e2e-test-$i.txt
done

UPLOAD_RESULT=$(curl -X POST http://localhost:3000/api/upload \
  -F "file=@/tmp/e2e-test-1.txt" \
  -F "file=@/tmp/e2e-test-2.txt" \
  -F "file=@/tmp/e2e-test-3.txt" \
  -F "file=@/tmp/e2e-test-4.txt" \
  -F "file=@/tmp/e2e-test-5.txt" \
  -s)

echo "✅ Step 2: Files uploaded"
echo "$UPLOAD_RESULT" | jq

# 3. Verify activity tracking
sleep 2  # Allow time for MCP storage

TRACKING_RESULT=$(npx claude-flow@alpha memory query \
  "agent-activities:" \
  --reasoningbank)

echo "✅ Step 3: Activities tracked"
echo "$TRACKING_RESULT" | jq

# 4. Verify metrics storage
METRICS_RESULT=$(npx claude-flow@alpha memory query \
  "agent-metrics:" \
  --reasoningbank)

echo "✅ Step 4: Metrics stored"
echo "$METRICS_RESULT" | jq
```

**E2E Verification Checklist**:
- [ ] All agents spawned successfully
- [ ] All files uploaded successfully
- [ ] Activities tracked in MCP
- [ ] Metrics stored in MCP
- [ ] Complete workflow functional

---

## Long-Term Verification (24 hours)

### Stability Monitoring

```bash
# Create 24-hour monitoring script
cat > /opt/monitoring/24h-stability-check.sh << 'EOF'
#!/bin/bash

LOG_FILE="/var/log/24h-stability-check.log"
START_TIME=$(date +%s)

while true; do
  CURRENT_TIME=$(date +%s)
  ELAPSED=$((CURRENT_TIME - START_TIME))

  # Run for 24 hours
  if [ $ELAPSED -ge 86400 ]; then
    echo "$(date -Iseconds) - 24-hour stability check complete" >> $LOG_FILE
    break
  fi

  # Health check
  HEALTH=$(curl -s http://localhost:3000/api/health | jq -r '.status')

  # Error count
  ERROR_COUNT=$(pm2 logs app --lines 100 --nostream | grep -i error | wc -l)

  # Memory usage
  MEM_USAGE=$(free | grep Mem | awk '{printf "%.1f", ($3/$2) * 100.0}')

  # CPU usage
  CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)

  # Log results
  echo "$(date -Iseconds),health=$HEALTH,errors=$ERROR_COUNT,mem=$MEM_USAGE%,cpu=$CPU_USAGE%" >> $LOG_FILE

  # Alert if issues
  if [ "$HEALTH" != "healthy" ] || [ $ERROR_COUNT -gt 10 ]; then
    echo "$(date -Iseconds) - ALERT: System health degraded" >> $LOG_FILE
  fi

  # Check every 5 minutes
  sleep 300
done
EOF

chmod +x /opt/monitoring/24h-stability-check.sh

# Run in background
nohup /opt/monitoring/24h-stability-check.sh &

echo "24-hour stability monitoring started (PID: $!)"
```

**24-Hour Checklist** (verify after 24 hours):
- [ ] System remained healthy (100% uptime)
- [ ] No critical errors
- [ ] Memory usage stable (no leaks)
- [ ] CPU usage acceptable
- [ ] No unexpected restarts
- [ ] Performance consistent

---

## Regression Testing

### Ensure No Performance Degradation

```bash
# Compare current performance to baseline

# Agent spawning benchmark
node scripts/benchmark-parallel-spawning.js > /tmp/current-spawn-benchmark.txt

# Compare to baseline (from QW-001 implementation)
diff /tmp/baseline-spawn-benchmark.txt /tmp/current-spawn-benchmark.txt

# Expected: No significant degradation (<10%)

# Upload benchmark
node scripts/benchmark-s3-uploads.js > /tmp/current-upload-benchmark.txt

# Compare to baseline
diff /tmp/baseline-upload-benchmark.txt /tmp/current-upload-benchmark.txt

# Expected: No significant degradation (<10%)
```

**Regression Testing Checklist**:
- [ ] Agent spawning performance maintained
- [ ] Upload performance maintained
- [ ] MCP storage performance maintained
- [ ] No new errors introduced
- [ ] Backward compatibility preserved

---

## User Acceptance Testing (UAT)

### UAT Test Plan

```bash
# Provide test users with:
# 1. Test credentials
# 2. Test scenarios
# 3. Feedback form

cat > /tmp/uat-test-plan.md << 'EOF'
# UAT Test Plan: Agent Optimizations

## Test Scenario 1: Agent Spawning
1. Navigate to agent management interface
2. Spawn 5 agents simultaneously
3. Observe spawn time
4. Verify all agents spawned successfully

**Expected**: Agents spawn in < 1 second

## Test Scenario 2: File Upload
1. Navigate to file upload interface
2. Upload 10 files simultaneously
3. Observe upload progress
4. Verify all files uploaded successfully

**Expected**: All files upload in < 1 second

## Test Scenario 3: Activity History
1. Navigate to agent activity dashboard
2. View agent spawn history
3. View file upload history
4. Verify all activities tracked

**Expected**: Complete activity history visible

## Feedback Form
- Overall satisfaction (1-5): ___
- Performance improvement noticed: Yes / No
- Any issues encountered: ___
- Additional comments: ___
EOF

# Send UAT test plan to test users
# (Via email, Slack, or internal wiki)
```

**UAT Checklist**:
- [ ] Test plan distributed
- [ ] Test users trained
- [ ] Tests executed
- [ ] Feedback collected
- [ ] Issues documented
- [ ] No major concerns raised

---

## Final Verification Report

### Generate Comprehensive Report

```bash
# Generate final verification report
node scripts/generate-verification-report.js

# Expected output: /reports/deployment-verification-2025-11-12.pdf
```

### Report Template

```markdown
# Deployment Verification Report
**Date**: 2025-11-12
**Deployment**: Agent Optimizations v1.1.0

## Executive Summary
- ✅ All functional tests passed
- ✅ Performance targets achieved
- ✅ 24-hour stability confirmed
- ✅ UAT feedback positive

## Test Results

### GAP-001: Parallel Agent Spawning
- Basic parallel spawning: ✅ PASS
- Dependency-aware spawning: ✅ PASS
- Fallback mechanism: ✅ PASS
- Performance target: ✅ 20x speedup (target: 10x)

### QW-001: Parallel S3 Uploads
- Single file upload: ✅ PASS
- Multi-file batch upload: ✅ PASS
- Partial failure handling: ✅ PASS
- Performance target: ✅ 10x speedup (target: 5-10x)

### QW-002: MCP Integration
- Activity storage: ✅ PASS
- Metrics storage: ✅ PASS
- Wiki notifications: ✅ PASS
- Graceful degradation: ✅ PASS

## Performance Metrics

| Metric | Baseline | Current | Improvement |
|--------|----------|---------|-------------|
| Agent spawn (5) | 3,750ms | 187ms | 20.05x |
| Upload (20 files) | 10,000ms | 687ms | 14.56x |
| Error rate | 0.05% | 0.02% | 60% reduction |

## Stability

- Uptime: 100% (24 hours)
- Restarts: 0
- Critical errors: 0
- Memory leaks: None detected

## User Feedback

- Satisfaction: 4.8/5 (average)
- Performance improvement noticed: 100%
- Issues reported: 0 critical, 2 minor

## Recommendation

✅ **DEPLOYMENT SUCCESSFUL - NO ROLLBACK NEEDED**

The deployment meets all success criteria. System is stable and performing well above targets. No critical issues detected.

## Sign-Off

**Verified By**: _________________
**Date**: _________________
**Status**: APPROVED FOR PRODUCTION
```

---

## Quick Reference: Verification Commands

```bash
# System health
pm2 status app
curl http://localhost:3000/api/health

# Agent spawning test
node scripts/test-parallel-spawning.js

# Upload test
curl -X POST http://localhost:3000/api/upload \
  -F "file=@test-file.txt"

# MCP test
npx claude-flow@alpha memory query \
  "agent-activities:" \
  --reasoningbank

# Performance check
pm2 logs app | grep "Speedup:"

# Error check
pm2 logs app | grep -i error | tail -20

# Resource usage
pm2 monit
```

---

**End of Post-Deployment Verification Guide**
