# Cross-GAP Integration Test Suite
**File**: README.md
**Created**: 2025-11-19 00:57:00 UTC
**Version**: v1.0.0
**Purpose**: Integration testing across all GAPs to verify system coherence
**Status**: ACTIVE

---

## Executive Summary

**Mission**: Test ALL GAPs working together as a unified system

**Coverage**: 7 GAP components, 15 integration scenarios, 45+ test cases

**Architecture**: Real services (PostgreSQL, Redis, Qdrant, Neo4j), real workflows, real data flows

**Runtime**: ~15-20 minutes for complete suite

---

## Test Architecture

### Test Categories

#### 1. GAP-001 + GAP-002: Parallel Spawning with AgentDB Cache
**File**: `gap001-gap002-parallel-cache.test.ts`
**Focus**: Verify parallel agent spawning leverages AgentDB L1/L2 caching
**Services**: ruv-swarm MCP, AgentDB, Qdrant
**Test Count**: 8 tests
**Runtime**: ~3 minutes

**Test Scenarios**:
- Spawn 5 agents in parallel, verify L1 cache hits
- Second spawn uses cached agent definitions (L1 memory)
- Third spawn after L1 eviction uses L2 (Qdrant persistence)
- Cross-session cache restoration
- Performance validation (10-20x speedup maintained with caching)
- Cache invalidation and refresh
- Concurrent spawning with cache contention
- Cache hit rate metrics collection

---

#### 2. GAP-002 + GAP-006: Worker Caching with Job Management
**File**: `gap002-gap006-worker-cache.test.ts`
**Focus**: Verify job workers leverage AgentDB for state persistence
**Services**: AgentDB, Qdrant, PostgreSQL, Redis
**Test Count**: 7 tests
**Runtime**: ~3 minutes

**Test Scenarios**:
- Worker state stored in AgentDB L1/L2 cache
- Job execution context persisted to Qdrant
- Worker resurrection from cached state after crash
- Job resumption from checkpoint with cached context
- Cross-worker context sharing via AgentDB
- Performance: cache hit reduces worker init time
- Cache consistency during concurrent job processing

---

#### 3. GAP-003 + ALL: Query Control Orchestration
**File**: `gap003-orchestration.test.ts`
**Focus**: Verify query control coordinates all system components
**Services**: Query Control, AgentDB, PostgreSQL, Redis, Qdrant, ruv-swarm
**Test Count**: 12 tests
**Runtime**: ~5 minutes

**Test Scenarios**:
- **GAP-003 + GAP-001**: Query control pauses during parallel agent spawn
- **GAP-003 + GAP-002**: Query checkpoint stored in AgentDB/Qdrant
- **GAP-003 + GAP-004**: Query accessing Neo4j schema checkpoints correctly
- **GAP-003 + GAP-006**: Query control integrates with job management
- Model switching during active job processing
- Permission mode changes affecting worker access
- Query pause cascades to all dependent workers
- Query resume restores full system state
- Query termination cleans up all resources
- Multi-query orchestration (3+ concurrent queries)
- Query control dashboard reflects all system components
- End-to-end query lifecycle with all services

---

#### 4. GAP-004 + GAP-005: R6 Temporal on Schema (Future)
**File**: `gap004-gap005-temporal-schema.test.ts`
**Focus**: Verify temporal tracking on Neo4j equipment schema
**Services**: Neo4j, PostgreSQL (when GAP-005 implemented)
**Test Count**: 6 tests (designed, pending GAP-005)
**Runtime**: ~2 minutes

**Planned Scenarios** (for when GAP-005 implemented):
- Equipment state changes tracked with R6 temporal metadata
- CVE impact timeline linked to equipment deployment
- Attack pattern trending correlated with equipment vulnerabilities
- Temporal queries spanning equipment and threat data
- Version history for equipment configurations
- Time-travel queries for incident reconstruction

---

#### 5. GAP-004 + GAP-007: Equipment + Advanced Features (Future)
**File**: `gap004-gap007-equipment-advanced.test.ts`
**Focus**: Verify advanced features on equipment schema
**Services**: Neo4j (when GAP-007 implemented)
**Test Count**: 6 tests (designed, pending GAP-007)
**Runtime**: ~2 minutes

**Planned Scenarios** (for when GAP-007 implemented):
- Psychometric profiling applied to equipment operators
- AI curiosity detects gaps in equipment coverage
- Predictive threat forecasting for equipment vulnerabilities
- Equipment risk scoring with advanced analytics
- Operator behavior patterns affecting equipment security
- 12-month threat predictions for equipment classes

---

#### 6. Full System Integration
**File**: `full-system-integration.test.ts`
**Focus**: Complete end-to-end workflows using all GAPs
**Services**: ALL (PostgreSQL, Redis, Qdrant, Neo4j, ruv-swarm, Query Control)
**Test Count**: 6 tests
**Runtime**: ~5 minutes

**Test Scenarios**:
- **Scenario 1**: Threat analysis workflow
  - Query control starts analysis (GAP-003)
  - Spawns 3 parallel workers (GAP-001)
  - Workers cache threat data (GAP-002)
  - Query Neo4j equipment schema (GAP-004)
  - Process jobs with retry logic (GAP-006)
  - Complete with full audit trail

- **Scenario 2**: Equipment deployment pipeline
  - Job creates new equipment in Neo4j (GAP-006 + GAP-004)
  - AgentDB caches equipment metadata (GAP-002)
  - Query control monitors deployment (GAP-003)
  - Parallel validation workers (GAP-001)
  - Full checkpoint/resume cycle

- **Scenario 3**: System recovery after failure
  - Simulate service crash mid-operation
  - Query control checkpoints state (GAP-003)
  - AgentDB persists to Qdrant (GAP-002)
  - Jobs retry with exponential backoff (GAP-006)
  - Workers restore from cache (GAP-001 + GAP-002)
  - Neo4j data remains consistent (GAP-004)

- **Scenario 4**: High-load concurrent operations
  - 5 concurrent queries (GAP-003)
  - 20 parallel agent spawns (GAP-001)
  - 50 job executions (GAP-006)
  - 100 AgentDB cache operations (GAP-002)
  - Neo4j query load (GAP-004)
  - System remains stable

- **Scenario 5**: Cross-component data consistency
  - Create equipment in Neo4j (GAP-004)
  - Query control tracks creation (GAP-003)
  - Job processes equipment tagging (GAP-006)
  - AgentDB caches equipment metadata (GAP-002)
  - Verify data consistency across all stores

- **Scenario 6**: Performance benchmark across all GAPs
  - Measure end-to-end latency
  - Verify performance targets:
    - Parallel spawn: 10-20x speedup (GAP-001)
    - Cache hits: 150-12,500x speedup (GAP-002)
    - Query control: <7ms operations (GAP-003)
    - Neo4j queries: <100ms (GAP-004)
    - Job processing: <5s average (GAP-006)

---

## Test Environment

### Required Services

#### Always Required
- **PostgreSQL 16+**: aeon-postgres-dev (aeon_saas_dev database)
- **Redis 7+**: For job queue and caching
- **Qdrant**: For AgentDB L2 cache and memory storage
- **Neo4j 5.x**: For GAP-004 schema

#### Optional (for specific tests)
- **ruv-swarm MCP**: For parallel agent spawning tests
- **Query Control Service**: Running on port 3000
- **Docker Network**: openspg-network (for service communication)

### Environment Variables

```bash
# PostgreSQL (aeon-postgres-dev)
export POSTGRES_HOST=172.18.0.5
export POSTGRES_PORT=5432
export POSTGRES_DB=aeon_saas_dev
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres

# Redis
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=1

# Qdrant (openspg-qdrant)
export QDRANT_URL=http://172.18.0.3:6333

# Neo4j (openspg-neo4j)
export NEO4J_URI=bolt://172.18.0.6:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

# Query Control
export QUERY_CONTROL_URL=http://localhost:3000

# Test Configuration
export TEST_TIMEOUT=300000
export SUPPRESS_LOGS=true
```

---

## Running Tests

### Quick Start - All Integration Tests

```bash
# Run complete integration test suite
./tests/integration/run-all-tests.sh

# Run with verbose logging
SUPPRESS_LOGS=false ./tests/integration/run-all-tests.sh

# Run with coverage report
npm run test:integration:coverage
```

### Run Specific Test Suites

```bash
# GAP-001 + GAP-002 tests only
npm run test:integration -- gap001-gap002

# GAP-003 orchestration tests only
npm run test:integration -- gap003-orchestration

# Full system integration tests only
npm run test:integration -- full-system

# Run single test file
npx jest tests/integration/gap001-gap002-parallel-cache.test.ts
```

### Run with Docker Auto-Setup

```bash
# Automatically start required services
AUTO_DOCKER=true ./tests/integration/run-all-tests.sh

# Cleanup Docker containers after tests
CLEANUP_DOCKER=true ./tests/integration/run-all-tests.sh
```

---

## Test Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Integration Test Execution                   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. Environment Setup                                           │
│     - Verify all services running                               │
│     - Connect to PostgreSQL, Redis, Qdrant, Neo4j              │
│     - Initialize test databases and collections                │
│     - Seed initial data                                         │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Test Execution                                              │
│                                                                 │
│     ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│     │  GAP-001    │   │  GAP-002    │   │  GAP-003    │      │
│     │  Parallel   │──▶│  AgentDB    │──▶│   Query     │      │
│     │  Spawning   │   │   Cache     │   │  Control    │      │
│     └─────────────┘   └─────────────┘   └─────────────┘      │
│            │                 │                 │               │
│            │                 ▼                 │               │
│            │          ┌─────────────┐          │               │
│            │          │   Qdrant    │          │               │
│            │          │  Persistence│          │               │
│            │          └─────────────┘          │               │
│            │                                    │               │
│            └────────────────┬───────────────────┘               │
│                             ▼                                   │
│                      ┌─────────────┐                            │
│                      │  GAP-004    │                            │
│                      │   Neo4j     │                            │
│                      │   Schema    │                            │
│                      └─────────────┘                            │
│                             │                                   │
│                             ▼                                   │
│                      ┌─────────────┐                            │
│                      │  GAP-006    │                            │
│                      │    Job      │                            │
│                      │ Management  │                            │
│                      └─────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. Verification                                                │
│     - Query all databases for expected state                   │
│     - Verify data consistency across services                  │
│     - Check performance metrics                                │
│     - Validate audit trails                                    │
│     - Confirm cache hit rates                                  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Cleanup                                                     │
│     - Truncate test tables                                     │
│     - Flush Redis                                              │
│     - Clear Qdrant collections                                 │
│     - Delete Neo4j test nodes                                  │
│     - Close all connections                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Test Utilities

### Shared Test Setup (`setup.ts`)

Provides common utilities:
- Multi-database connection management
- Service health checks
- Test data generators
- State verification helpers
- Performance measurement utilities
- Cleanup functions

### Integration Test Base Class (`base-integration-test.ts`)

```typescript
export abstract class BaseIntegrationTest {
  protected postgres: Pool;
  protected redis: Redis;
  protected qdrant: QdrantClient;
  protected neo4j: Driver;

  async setupAll(): Promise<void>;
  async teardownAll(): Promise<void>;
  async cleanupBetweenTests(): Promise<void>;

  protected async verifyAllServices(): Promise<void>;
  protected async seedTestData(): Promise<void>;
  protected async captureSystemState(): Promise<SystemSnapshot>;
  protected async compareSystemState(before: SystemSnapshot, after: SystemSnapshot): Promise<void>;
}
```

---

## Success Criteria

### Integration Test Goals

**Primary Goals**:
- ✅ All 45+ test cases passing
- ✅ No data inconsistencies between services
- ✅ Performance targets met across all GAPs
- ✅ Zero test flakiness (<0.1% failure rate)
- ✅ Complete audit trail for all operations

**Performance Targets**:
- GAP-001 parallel spawning: 10-20x faster than sequential
- GAP-002 cache hit rate: >80% after warmup
- GAP-003 query control latency: <7ms average
- GAP-004 Neo4j queries: <100ms average
- GAP-006 job processing: <5s average
- Full system workflow: <30s end-to-end

**Quality Targets**:
- Code coverage: >80% for integration paths
- No memory leaks during long-running tests
- Proper resource cleanup (no dangling connections)
- Error recovery within 5 seconds
- Consistent behavior across 100+ test runs

---

## Debugging Integration Tests

### Enable Verbose Logging

```bash
export SUPPRESS_LOGS=false
export DEBUG=integration:*
./tests/integration/run-all-tests.sh
```

### Run Single Test with Debugger

```bash
node --inspect-brk ./node_modules/.bin/jest \
  tests/integration/gap003-orchestration.test.ts \
  -t "query pause cascades to all workers"
```

### Inspect Service State During Tests

```bash
# PostgreSQL
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev \
  -c "SELECT * FROM jobs WHERE status = 'processing';"

# Redis
docker exec openspg-redis redis-cli KEYS "job:*"

# Qdrant
curl http://172.18.0.3:6333/collections/agentdb_cache/points/search \
  -X POST -H "Content-Type: application/json" \
  -d '{"vector": [0.1, 0.2, ...], "limit": 5}'

# Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p password \
  "MATCH (e:Equipment) WHERE e.equipmentId STARTS WITH 'TEST-' RETURN e LIMIT 10;"
```

### Capture Test Snapshots

```bash
# Before test execution
npm run integration:snapshot -- before

# After test execution
npm run integration:snapshot -- after

# Compare snapshots
npm run integration:snapshot -- compare
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Cross-GAP Integration Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Nightly at 2 AM UTC

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: aeon_saas_dev
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      qdrant:
        image: qdrant/qdrant:latest
        ports:
          - 6333:6333

      neo4j:
        image: neo4j:5-enterprise
        env:
          NEO4J_AUTH: neo4j/password
          NEO4J_ACCEPT_LICENSE_AGREEMENT: yes
        ports:
          - 7687:7687
          - 7474:7474

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run database migrations
        run: npm run migrate:test

      - name: Seed Neo4j schema
        run: npm run neo4j:seed:test

      - name: Run integration tests
        run: ./tests/integration/run-all-tests.sh
        env:
          POSTGRES_HOST: localhost
          REDIS_HOST: localhost
          QDRANT_URL: http://localhost:6333
          NEO4J_URI: bolt://localhost:7687

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/integration/lcov.info
          flags: integration

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: integration-test-results
          path: tests/integration/results/

      - name: Notify on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Integration tests failed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Test Maintenance

### Adding New Integration Tests

1. Identify GAP interaction points
2. Create test file following naming convention: `gapXXX-gapYYY-description.test.ts`
3. Extend `BaseIntegrationTest` class
4. Implement test scenarios
5. Update this README with new coverage
6. Add to test runner script

### Updating Test Data

Modify generators in `setup.ts`:
- `generateTestAgent()`
- `generateTestJob()`
- `generateTestEquipment()`
- `generateTestQuery()`

### Performance Tuning

Adjust timeouts in `jest.config.integration.js`:
```javascript
module.exports = {
  testTimeout: 300000, // 5 minutes
  maxWorkers: 1, // Serial execution
  // ... other config
};
```

---

## Troubleshooting

### Common Issues

**Services not available**
```bash
# Check service health
docker ps | grep -E "postgres|redis|qdrant|neo4j"

# Restart services
docker-compose -f docker-compose.dev.yml restart
```

**Database connection errors**
```bash
# Test PostgreSQL connection
psql -h 172.18.0.5 -U postgres -d aeon_saas_dev -c "SELECT 1;"

# Test Redis connection
redis-cli -h localhost ping

# Test Qdrant connection
curl http://172.18.0.3:6333/collections
```

**Test timeouts**
- Increase `TEST_TIMEOUT` environment variable
- Check for deadlocks: `SELECT * FROM pg_stat_activity WHERE state = 'active';`
- Monitor long-running queries in Neo4j browser

**Flaky tests**
- Add retry logic in test setup
- Increase wait times between operations
- Check for race conditions in concurrent operations
- Review service logs for intermittent errors

**Memory issues**
- Reduce test parallelism: `maxWorkers: 1`
- Cleanup between tests more aggressively
- Monitor with: `docker stats`

---

## Performance Benchmarks

Expected performance on standard hardware (8 CPU, 16GB RAM):

| Test Suite | Test Count | Duration | Avg per Test | Services |
|-----------|-----------|----------|--------------|----------|
| GAP-001+002 | 8 | ~3min | 22.5s | ruv-swarm, AgentDB, Qdrant |
| GAP-002+006 | 7 | ~3min | 25.7s | AgentDB, Qdrant, PostgreSQL, Redis |
| GAP-003 Orchestration | 12 | ~5min | 25s | All services |
| Full System | 6 | ~5min | 50s | All services |
| **Total (Current)** | **33** | **~16min** | **29s** | All |
| GAP-004+005 (Future) | 6 | ~2min | 20s | Neo4j, PostgreSQL |
| GAP-004+007 (Future) | 6 | ~2min | 20s | Neo4j |
| **Total (With Future)** | **45** | **~20min** | **27s** | All |

---

## Documentation Standards

All integration tests must include:
- Clear test description
- Documented service dependencies
- Expected outcomes
- Performance expectations
- Cleanup procedures
- Error handling

Example:
```typescript
describe('GAP-003: Query Control Orchestration', () => {
  /**
   * Test: Query pause cascades to all dependent workers
   *
   * Services: Query Control, AgentDB, PostgreSQL, ruv-swarm
   *
   * Flow:
   * 1. Start query with 3 parallel workers
   * 2. Pause query via Query Control API
   * 3. Verify all workers receive pause signal
   * 4. Verify worker states persisted to AgentDB
   * 5. Resume query
   * 6. Verify workers resume processing
   *
   * Expected: <2s pause propagation, 100% worker state consistency
   *
   * Performance: Pause propagation <500ms, Resume <1s
   */
  test('query pause cascades to all workers', async () => {
    // Test implementation
  }, 60000);
});
```

---

## License

MIT License - Cross-GAP Integration Test Suite

---

**Document Status**: ✅ COMPLETE
**Next Action**: Implement test files starting with `gap001-gap002-parallel-cache.test.ts`
**Estimated Implementation Time**: 8-12 hours for complete suite
