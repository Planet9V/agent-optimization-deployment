# GAP-006 Integration Test Suite

Comprehensive integration tests for the GAP-006 Job Management System that test REAL functionality with actual PostgreSQL, Redis, Qdrant, and ruv-swarm integration.

## Test Coverage

### 1. Job Lifecycle Tests (`job-lifecycle.test.ts`)
Tests complete job workflow with real database and service interactions:

- **Complete Job Workflow**: create → acquire → process → complete
  - Worker spawning via ruv-swarm MCP
  - Job creation and queuing
  - Job acquisition by workers
  - Processing state management
  - Completion with results
  - Execution history tracking

- **Concurrent Processing**: Multiple workers processing jobs in parallel
  - 3 workers processing 6 jobs concurrently
  - Load distribution verification
  - No job conflicts or race conditions

- **Retry Logic**: Job failure and retry mechanism
  - Automatic retry after failure
  - Exponential backoff verification
  - Dead letter queue after max retries exceeded
  - Retry count tracking

- **Priority Queue**: Job priority ordering
  - High priority jobs acquired first
  - FIFO within same priority level
  - Priority-based scheduling

- **Timeout Handling**: Job timeout detection
  - Automatic failure on timeout
  - Timeout metadata recording

**Test Count**: 8 integration tests
**Estimated Runtime**: ~60 seconds
**Coverage**: JobService, WorkerService, PostgreSQL, Redis

---

### 2. Worker Health Tests (`worker-health.test.ts`)
Tests worker heartbeat monitoring, failure detection, and predictive analytics:

- **Heartbeat Monitoring**: Regular health checks
  - Periodic heartbeat recording
  - Timestamp verification
  - Health log persistence

- **Missed Heartbeat Detection**: Health degradation alerts
  - Heartbeat pause simulation
  - Health score degradation
  - Alert creation and severity tracking

- **Failure Detection**: Worker crash handling
  - Crash simulation and detection
  - Status transition to FAILED
  - Failure metadata recording

- **Auto-Recovery**: Transient failure recovery
  - Recovery after temporary failures
  - Status restoration to ACTIVE
  - Recovery event logging

- **Predictive Analytics**: Machine learning-based failure prediction
  - Health score trend analysis
  - Failure probability calculation
  - Recommended action generation

- **Anomaly Detection**: Statistical anomaly identification
  - Metric baseline establishment
  - Spike detection
  - Severity scoring

- **Load Balancing**: Health-aware job distribution
  - Optimal worker selection
  - Health score consideration
  - Load capacity verification

- **Worker Evacuation**: Preemptive job reassignment
  - Job evacuation on predicted failure
  - Job reassignment to healthy workers
  - Draining status management

**Test Count**: 8 integration tests
**Estimated Runtime**: ~80 seconds
**Coverage**: WorkerService, HealthMonitorService, PostgreSQL, Redis

---

### 3. State Persistence Tests (`state-persistence.test.ts`)
Tests Qdrant memory storage, state snapshots, and disaster recovery:

- **Full Snapshot**: Complete system state capture
  - Worker state serialization
  - Job state serialization
  - PostgreSQL persistence
  - Qdrant vector storage

- **Incremental Snapshot**: Delta-based state capture
  - Change tracking
  - Base snapshot reference
  - Efficient storage

- **Full Restoration**: Complete system recovery
  - State deserialization
  - Database restoration
  - Redis cache rebuilding
  - Processing state recovery

- **Conflict Resolution**: Smart merge strategies
  - Conflict detection
  - Merge strategy application
  - New data preservation

- **Execution Context Storage**: Qdrant memory integration
  - Context serialization
  - Vector embedding
  - Retrieval verification

- **Semantic Search**: Similar execution discovery
  - Natural language queries
  - Vector similarity scoring
  - Relevance ranking

- **Pattern Matching**: Execution pattern similarity
  - Pattern extraction
  - Vector comparison
  - Similarity threshold

- **Auto-Snapshot Scheduling**: Background snapshot creation
  - Periodic snapshot triggers
  - Retention policy
  - Cleanup automation

- **Point-in-Time Recovery**: Temporal state restoration
  - Timestamp-based recovery
  - State reconstruction
  - Data consistency verification

**Test Count**: 9 integration tests
**Estimated Runtime**: ~150 seconds
**Coverage**: StatePersistenceService, Qdrant, PostgreSQL, Redis

---

## Total Test Suite

- **Total Tests**: 25 integration tests
- **Total Runtime**: ~5 minutes
- **Services Tested**: PostgreSQL, Redis, Qdrant, ruv-swarm
- **Code Coverage Target**: 80% lines, 75% functions, 70% branches

---

## Running Tests

### Quick Start

```bash
# Run all integration tests
./run-tests.sh

# Run specific test file
./run-tests.sh job-lifecycle

# Run with coverage report
npm run test:integration:coverage
```

### Prerequisites

1. **Node.js 18+**
2. **PostgreSQL 16+** (or Docker)
3. **Redis 7+** (or Docker)
4. **Qdrant** (or Docker)

### Environment Variables

```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=gap006_test
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=1
export QDRANT_URL=http://localhost:6333
```

### Docker Setup (Automated)

The test runner automatically starts required services if not available:

```bash
# Run with automatic Docker setup
./run-tests.sh

# Cleanup Docker containers after tests
CLEANUP_DOCKER=true ./run-tests.sh
```

### Manual Docker Setup

```bash
# PostgreSQL
docker run -d \
  --name gap006-test-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16-alpine

# Redis
docker run -d \
  --name gap006-test-redis \
  -p 6379:6379 \
  redis:7-alpine

# Qdrant
docker run -d \
  --name gap006-test-qdrant \
  -p 6333:6333 \
  qdrant/qdrant:latest
```

---

## Test Architecture

### Test Environment Setup (`setup.ts`)

Provides shared utilities:
- Database connection management
- Redis connection management
- Migration execution
- Cleanup functions
- Test data generators
- State verification helpers

### Test Configuration (`jest.config.js`)

- **Preset**: ts-jest for TypeScript support
- **Environment**: Node.js
- **Timeout**: 30 seconds per test
- **Workers**: 1 (serial execution to avoid conflicts)
- **Coverage**: 80% threshold

### Test Setup (`jest.setup.ts`)

- Global timeout configuration
- Unhandled rejection handling
- Environment validation
- Test utilities (UUID generation, retry logic)

---

## Test Data Flow

```
┌─────────────────────────────────────────────────┐
│           Integration Test Execution            │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│     1. setupTestEnvironment()                   │
│        - Initialize PostgreSQL connection       │
│        - Initialize Redis connection            │
│        - Initialize Qdrant client               │
│        - Run database migrations                │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│     2. Test Execution                           │
│        - Spawn workers (ruv-swarm MCP)          │
│        - Create jobs (JobService)               │
│        - Process jobs (WorkerService)           │
│        - Monitor health (HealthMonitorService)  │
│        - Store state (StatePersistenceService)  │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│     3. Verification                             │
│        - Query PostgreSQL for state             │
│        - Check Redis cache                      │
│        - Search Qdrant vectors                  │
│        - Verify execution logs                  │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│     4. Cleanup                                  │
│        - Truncate database tables               │
│        - Flush Redis                            │
│        - Clear Qdrant collections               │
│        - Close connections                      │
└─────────────────────────────────────────────────┘
```

---

## Test Output

### Success Output

```
╔════════════════════════════════════════════════════╗
║     GAP-006 Integration Test Suite Runner         ║
╚════════════════════════════════════════════════════╝

[1/6] Checking prerequisites...
✓ All prerequisites satisfied

[2/6] Setting up test environment...
✓ Environment configured

[3/6] Verifying database connectivity...
✓ Database services ready

[4/6] Preparing test database...
✓ Test database prepared

[5/6] Installing test dependencies...
✓ Dependencies installed

[6/6] Running integration tests...

PASS tests/gap006/integration/job-lifecycle.test.ts (15.2s)
PASS tests/gap006/integration/worker-health.test.ts (18.5s)
PASS tests/gap006/integration/state-persistence.test.ts (22.8s)

Test Suites: 3 passed, 3 total
Tests:       25 passed, 25 total
Snapshots:   0 total
Time:        56.5s

Coverage:
  Lines   : 82.5% ( 165/200 )
  Functions: 76.3% ( 58/76 )
  Branches: 71.8% ( 46/64 )
  Statements: 83.1% ( 166/200 )

╔════════════════════════════════════════════════════╗
║          ALL INTEGRATION TESTS PASSED ✓            ║
╚════════════════════════════════════════════════════╝
```

---

## Debugging Tests

### Enable Verbose Logging

```bash
export SUPPRESS_LOGS=false
./run-tests.sh
```

### Run Single Test

```bash
npx jest tests/gap006/integration/job-lifecycle.test.ts -t "complete job workflow"
```

### Inspect Database State

```bash
# During test execution (add breakpoint)
psql -h localhost -U postgres -d gap006_test -c "SELECT * FROM jobs;"
redis-cli -n 1 KEYS "*"
curl http://localhost:6333/collections/gap006_state/points
```

---

## Continuous Integration

### GitHub Actions Integration

```yaml
name: GAP-006 Integration Tests

on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

      qdrant:
        image: qdrant/qdrant:latest
        ports:
          - 6333:6333

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Run integration tests
        run: ./tests/gap006/integration/run-tests.sh

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/integration/lcov.info
```

---

## Maintenance

### Adding New Tests

1. Create test file in `/tests/gap006/integration/`
2. Import test utilities from `./setup`
3. Follow naming convention: `*.test.ts`
4. Update this README with new test coverage

### Updating Test Data

Modify generators in `setup.ts`:
- `generateTestJobPayload()`
- `generateTestWorkerConfig()`

### Adjusting Timeouts

Modify in `jest.config.js` or individual test files:
```typescript
test('long running test', async () => {
  // test code
}, 60000); // 60 second timeout
```

---

## Troubleshooting

### Common Issues

**Database connection failed**
- Verify PostgreSQL is running: `psql -h localhost -U postgres -c "SELECT 1"`
- Check credentials in environment variables

**Redis connection failed**
- Verify Redis is running: `redis-cli ping`
- Check port availability: `lsof -i :6379`

**Qdrant connection failed**
- Verify Qdrant is running: `curl http://localhost:6333/collections`
- Check Docker container: `docker ps | grep qdrant`

**Tests timeout**
- Increase timeout in jest.config.js
- Check for deadlocks in database
- Verify network connectivity

**Flaky tests**
- Add retry logic using `testUtils.retry()`
- Increase wait times in `waitFor()` calls
- Check for race conditions

---

## Performance Benchmarks

Expected test performance on standard hardware:

| Test Suite | Test Count | Duration | Avg per Test |
|-----------|-----------|----------|--------------|
| Job Lifecycle | 8 | ~60s | 7.5s |
| Worker Health | 8 | ~80s | 10s |
| State Persistence | 9 | ~150s | 16.7s |
| **Total** | **25** | **~5min** | **12s** |

---

## License

MIT License - GAP-006 Integration Test Suite
