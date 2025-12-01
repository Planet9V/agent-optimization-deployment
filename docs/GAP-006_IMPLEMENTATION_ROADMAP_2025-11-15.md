# GAP-006 Implementation Roadmap
**File:** GAP-006_IMPLEMENTATION_ROADMAP_2025-11-15.md
**Created:** 2025-11-15 16:45:00 UTC
**Version:** v1.0.0
**Architecture Reference:** `/home/jim/2_OXOT_Projects_Dev/docs/GAP-006_ARCHITECTURE_DESIGN_2025-11-15.md`
**Status:** READY FOR EXECUTION

---

## Executive Summary

**Objective**: Implement production-grade Job Management & Reliability system (GAP-006) with persistent job storage, distributed worker architecture, and comprehensive error recovery.

**Timeline**: 6 weeks (42 days)
**Total Estimated Hours**: 112 hours
**Total Estimated Cost**: $1,904 (at $17/hour agent rate)
**Agents Required**: 12 specialized agents
**Infrastructure**: EXTENDS existing aeon-postgres-dev and openspg-network

**Key Deliverables**:
- PostgreSQL schema with 5 job management tables
- Redis integration on openspg-network
- Node.js distributed worker pool
- Exponential backoff error recovery with dead letter queue
- Comprehensive monitoring with Prometheus/Grafana dashboards
- Production-ready deployment with health checks

---

## Phase 1: Infrastructure Setup (Week 1 - Days 1-7)

**Objective**: Deploy Redis and prepare database for job management schema
**Duration**: 7 days
**Estimated Hours**: 16 hours
**Estimated Cost**: $272
**Agents Required**: 3

### Tasks

#### Task 1.1: Update Redis Docker Configuration
- **ID**: GAP006-T1.1
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__swarm_init`, `mcp__claude-flow__agent_spawn`
- **Duration**: 3 hours
- **Dependencies**: None
- **Deliverables**:
  - `docker-compose.redis.yml` updated with openspg-network configuration
  - Redis container configured with persistence (AOF + RDB)
  - Redis Commander deployed for monitoring

**Discrete Steps**:
```yaml
1. Read existing docker-compose.redis.yml
2. Update networks section to use openspg-network (external)
3. Configure Redis volumes for persistence
4. Add Redis Commander service for monitoring
5. Set environment variables (REDIS_PASSWORD=aeon_redis_dev)
6. Validate docker-compose syntax
7. Commit changes with descriptive message
```

**Expected Configuration**:
```yaml
services:
  aeon-redis:
    image: redis:7-alpine
    container_name: aeon-redis
    networks:
      - openspg-network
    ports:
      - "6379:6379"
    volumes:
      - aeon-redis-data:/data
      - ./config/redis.conf:/usr/local/etc/redis/redis.conf
    command: redis-server /usr/local/etc/redis/redis.conf

  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: aeon-redis-commander
    networks:
      - openspg-network
    ports:
      - "8081:8081"
    environment:
      - REDIS_HOSTS=local:aeon-redis:6379:0:aeon_redis_dev

networks:
  openspg-network:
    external: true

volumes:
  aeon-redis-data:
```

#### Task 1.2: Deploy and Test Redis
- **ID**: GAP006-T1.2
- **Owner**: cicd-engineer agent
- **MCP Tools**: `mcp__claude-flow__terminal_execute`, `mcp__claude-flow__health_check`
- **Duration**: 2 hours
- **Dependencies**: T1.1
- **Deliverables**:
  - Running aeon-redis container on openspg-network
  - Verified connectivity from aeon-saas-dev
  - Redis Commander accessible at localhost:8081

**Discrete Steps**:
```yaml
1. Start Redis with docker-compose -f docker-compose.redis.yml up -d
2. Verify container running: docker ps --filter "name=aeon-redis"
3. Check network assignment: docker network inspect openspg-network
4. Verify IP address assigned (172.18.0.x range)
5. Test connectivity from aeon-saas-dev container
6. Verify Redis Commander accessible
7. Test Redis commands: SET test_key test_value, GET test_key
```

**Validation Commands**:
```bash
# Verify Redis is running
docker ps --filter "name=aeon-redis" --format "{{.Names}} - {{.Status}}"

# Check network assignment
docker network inspect openspg-network | grep -A 10 aeon-redis

# Test Redis connectivity
docker exec aeon-redis redis-cli -a aeon_redis_dev PING

# Test from aeon-saas-dev container
docker exec aeon-saas-dev ping -c 3 aeon-redis
```

#### Task 1.3: Create Redis Configuration
- **ID**: GAP006-T1.3
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__config_manage`
- **Duration**: 2 hours
- **Dependencies**: T1.1
- **Deliverables**:
  - `/config/redis.conf` with production settings
  - AOF persistence enabled
  - RDB snapshots configured
  - Memory limits set

**Discrete Steps**:
```yaml
1. Create config directory: mkdir -p config
2. Create redis.conf with production settings
3. Enable AOF persistence (appendonly yes)
4. Configure RDB snapshots (save 900 1, save 300 10, save 60 10000)
5. Set maxmemory policy (maxmemory-policy allkeys-lru)
6. Configure password (requirepass aeon_redis_dev)
7. Set memory limit (maxmemory 256mb)
8. Restart Redis with new configuration
```

**Expected Configuration File**:
```conf
# Redis Configuration for GAP-006 Job Queue
# /config/redis.conf

# Network
bind 0.0.0.0
port 6379
requirepass aeon_redis_dev

# Persistence - AOF
appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Persistence - RDB
save 900 1
save 300 10
save 60 10000
dbfilename dump.rdb

# Memory Management
maxmemory 256mb
maxmemory-policy allkeys-lru

# Logging
loglevel notice
```

#### Task 1.4: Update Environment Configuration
- **ID**: GAP006-T1.4
- **Owner**: coder agent
- **MCP Tools**: `mcp__claude-flow__config_manage`
- **Duration**: 1 hour
- **Dependencies**: T1.2
- **Deliverables**:
  - Updated `.env` with GAP-006 configuration
  - Environment variables documented

**Discrete Steps**:
```yaml
1. Read existing .env file
2. Add GAP-006 section header
3. Add Redis configuration variables
4. Add worker configuration variables
5. Add monitoring configuration variables
6. Validate no duplicate keys
7. Document all new variables
```

**New Environment Variables**:
```env
# ===============================================
# GAP-006: Job Management & Reliability
# ===============================================

# Redis Configuration
REDIS_HOST=aeon-redis
REDIS_PORT=6379
REDIS_PASSWORD=aeon_redis_dev
REDIS_DB=0
REDIS_QUEUE_PREFIX=job:

# Worker Configuration
WORKER_ENABLED=true
WORKER_CONCURRENCY=5
WORKER_POLL_INTERVAL=1000
WORKER_HEARTBEAT_INTERVAL=30000
WORKER_LOCK_DURATION=300000
WORKER_AUTO_RESTART=true

# Job Configuration
JOB_DEFAULT_TIMEOUT=300000
JOB_MAX_RETRIES=3
JOB_RETRY_DELAY_BASE=1000
JOB_RETRY_BACKOFF_MULTIPLIER=2
JOB_DLQ_ENABLED=true

# Monitoring
MONITORING_ENABLED=true
METRICS_PORT=9090
PROMETHEUS_ENABLED=false
GRAFANA_ENABLED=false
```

#### Task 1.5: Infrastructure Validation
- **ID**: GAP006-T1.5
- **Owner**: production-validator agent
- **MCP Tools**: `mcp__claude-flow__health_check`, `mcp__claude-flow__diagnostic_run`
- **Duration**: 2 hours
- **Dependencies**: T1.2, T1.3, T1.4
- **Deliverables**:
  - Infrastructure validation report
  - All health checks passing
  - Network connectivity verified

**Discrete Steps**:
```yaml
1. Verify aeon-postgres-dev running and healthy
2. Verify aeon-redis running and healthy
3. Test network connectivity between services
4. Verify environment variables loaded correctly
5. Test Redis persistence (write, restart, read)
6. Verify Redis Commander dashboard functional
7. Generate infrastructure validation report
```

**Validation Checklist**:
```yaml
infrastructure_checklist:
  postgres:
    - [ ] Container running (aeon-postgres-dev)
    - [ ] Health check passing
    - [ ] Port 5432 accessible
    - [ ] Database aeon_saas_dev exists
    - [ ] Network: openspg-network (172.18.0.5)

  redis:
    - [ ] Container running (aeon-redis)
    - [ ] Health check passing
    - [ ] Port 6379 accessible
    - [ ] Password authentication working
    - [ ] Network: openspg-network (172.18.0.x)
    - [ ] Persistence configured (AOF + RDB)
    - [ ] Redis Commander accessible (localhost:8081)

  network:
    - [ ] aeon-redis reachable from aeon-saas-dev
    - [ ] aeon-postgres-dev reachable from aeon-saas-dev
    - [ ] All containers on openspg-network subnet

  environment:
    - [ ] .env file updated with GAP-006 variables
    - [ ] All required variables defined
    - [ ] No duplicate variable definitions
```

#### Task 1.6: Infrastructure Documentation
- **ID**: GAP006-T1.6
- **Owner**: api-docs agent
- **MCP Tools**: `mcp__claude-flow__memory_usage` (store)
- **Duration**: 2 hours
- **Dependencies**: T1.5
- **Deliverables**:
  - Infrastructure setup guide
  - Troubleshooting documentation
  - Memory stored in Qdrant

**Discrete Steps**:
```yaml
1. Create infrastructure setup guide document
2. Document Redis deployment steps
3. Document network configuration
4. Document environment variables
5. Create troubleshooting section
6. Store documentation in Qdrant (namespace: gap-006-implementation)
7. Update project README with GAP-006 infrastructure section
```

### Phase 1 Success Criteria
- ✅ Redis running on openspg-network with persistence enabled
- ✅ Redis accessible from aeon-saas-dev container
- ✅ Redis Commander dashboard functional
- ✅ Environment variables configured
- ✅ All infrastructure health checks passing
- ✅ Documentation complete and stored in Qdrant

---

## Phase 2: Database Schema (Week 1 - Days 8-14)

**Objective**: Create PostgreSQL schema for job management
**Duration**: 7 days
**Estimated Hours**: 20 hours
**Estimated Cost**: $340
**Agents Required**: 3

### Tasks

#### Task 2.1: Create Database Migration Script
- **ID**: GAP006-T2.1
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__agent_spawn`
- **Duration**: 4 hours
- **Dependencies**: Phase 1 complete
- **Deliverables**:
  - `scripts/migrations/001_gap006_job_tables.sql` migration script
  - 5 tables created (jobs, job_executions, job_dependencies, job_schedules, dead_letter_jobs)
  - Functions and triggers implemented
  - Indexes created

**Discrete Steps**:
```yaml
1. Create migrations directory: mkdir -p scripts/migrations
2. Create migration file 001_gap006_job_tables.sql
3. Define jobs table schema (from architecture document lines 108-188)
4. Define job_executions table schema (lines 190-225)
5. Define job_dependencies table schema (lines 227-255)
6. Define job_schedules table schema (lines 257-300)
7. Define dead_letter_jobs table schema (lines 302-337)
8. Create get_ready_jobs() function (lines 345-372)
9. Create retry_failed_jobs() function (lines 374-413)
10. Create update_updated_at() trigger function (lines 415-428)
11. Create indexes for all tables (lines 430-510)
12. Add migration metadata table
13. Validate SQL syntax with psql --dry-run
```

**Schema Overview** (from architecture lines 108-510):
```sql
-- Migration: 001_gap006_job_tables.sql
-- Creates: 5 tables, 3 functions, 5 triggers, 15 indexes

CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  job_type VARCHAR(100) NOT NULL,
  status job_status DEFAULT 'pending',
  priority INTEGER DEFAULT 50,
  payload JSONB,
  result JSONB,
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3,
  timeout_ms INTEGER DEFAULT 300000,
  scheduled_at TIMESTAMPTZ,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by VARCHAR(255),
  metadata JSONB
);

-- (Additional tables and functions from architecture document)
```

#### Task 2.2: Run Database Migration
- **ID**: GAP006-T2.2
- **Owner**: cicd-engineer agent
- **MCP Tools**: `mcp__claude-flow__terminal_execute`
- **Duration**: 2 hours
- **Dependencies**: T2.1
- **Deliverables**:
  - Migration executed successfully
  - All tables created
  - All functions and triggers created
  - All indexes created

**Discrete Steps**:
```yaml
1. Backup aeon_saas_dev database before migration
2. Execute migration: docker exec -i aeon-postgres-dev psql -U postgres -d aeon_saas_dev < scripts/migrations/001_gap006_job_tables.sql
3. Verify tables created: docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "\dt job*"
4. Verify functions created: docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "\df get_ready_jobs"
5. Verify triggers created
6. Verify indexes created: docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "\di job*"
7. Run ANALYZE to update statistics
```

**Validation Commands**:
```bash
# Verify all tables created
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "\dt job*"
# Expected: jobs, job_executions, job_dependencies, job_schedules, dead_letter_jobs

# Verify row counts (should be 0)
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "
  SELECT 'jobs' AS table, COUNT(*) FROM jobs
  UNION ALL SELECT 'job_executions', COUNT(*) FROM job_executions
  UNION ALL SELECT 'job_dependencies', COUNT(*) FROM job_dependencies
  UNION ALL SELECT 'job_schedules', COUNT(*) FROM job_schedules
  UNION ALL SELECT 'dead_letter_jobs', COUNT(*) FROM dead_letter_jobs;
"

# Verify functions exist
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "\df *job*"

# Verify indexes exist
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "\di job*"
```

#### Task 2.3: Test Database Functions
- **ID**: GAP006-T2.3
- **Owner**: tester agent
- **MCP Tools**: `mcp__claude-flow__agent_spawn`
- **Duration**: 4 hours
- **Dependencies**: T2.2
- **Deliverables**:
  - Test suite for database functions
  - All functions tested with multiple scenarios
  - Edge cases validated

**Discrete Steps**:
```yaml
1. Create test data insertion script
2. Test get_ready_jobs() with various scenarios:
   - Pending jobs with no dependencies
   - Jobs with satisfied dependencies
   - Jobs with unsatisfied dependencies
   - Scheduled jobs (future vs past)
   - Priority ordering
3. Test retry_failed_jobs() with:
   - Failed jobs below max_retries
   - Failed jobs at max_retries
   - Different retry_delay_ms values
4. Test update_updated_at() trigger:
   - Insert job → verify updated_at set
   - Update job → verify updated_at changed
5. Test cascading deletes and constraints
6. Generate test report
```

**Test Scenarios**:
```sql
-- Test 1: get_ready_jobs() with simple pending jobs
INSERT INTO jobs (job_type, status, priority) VALUES
  ('test_job_1', 'pending', 100),
  ('test_job_2', 'pending', 50),
  ('test_job_3', 'running', 75);

SELECT * FROM get_ready_jobs(10);
-- Expected: 2 rows (test_job_1, test_job_2 in priority order)

-- Test 2: get_ready_jobs() with dependencies
INSERT INTO jobs (job_type, status) VALUES ('parent_job', 'completed') RETURNING id AS parent_id;
INSERT INTO jobs (job_type, status) VALUES ('child_job', 'pending') RETURNING id AS child_id;
INSERT INTO job_dependencies (job_id, depends_on_job_id) VALUES (child_id, parent_id);

SELECT * FROM get_ready_jobs(10);
-- Expected: child_job included (parent completed)

-- Test 3: retry_failed_jobs()
INSERT INTO jobs (job_type, status, retry_count, max_retries, error_message) VALUES
  ('retry_job', 'failed', 2, 3, 'test error');

SELECT retry_failed_jobs(1000);
-- Expected: 1 job updated to pending, retry_count=3
```

#### Task 2.4: Create Database Access Layer
- **ID**: GAP006-T2.4
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__agent_spawn`
- **Duration**: 6 hours
- **Dependencies**: T2.2
- **Deliverables**:
  - TypeScript database access layer
  - Job repository class
  - Type definitions for all tables
  - Connection pooling configured

**Discrete Steps**:
```yaml
1. Create workers/src/db directory
2. Create postgres.ts connection module
3. Create types.ts with TypeScript interfaces for all tables
4. Create job-repository.ts with CRUD operations
5. Implement createJob(), updateJob(), deleteJob()
6. Implement getReadyJobs(), getJobById(), getJobsByStatus()
7. Implement markJobRunning(), markJobCompleted(), markJobFailed()
8. Implement moveToDeadLetterQueue()
9. Configure connection pooling (max 10 connections)
10. Add error handling and logging
11. Write unit tests for repository
```

**Expected Implementation**:
```typescript
// workers/src/db/postgres.ts
import { Pool } from 'pg';

export const pool = new Pool({
  host: process.env.POSTGRES_HOST || 'aeon-postgres-dev',
  port: parseInt(process.env.POSTGRES_PORT || '5432'),
  database: process.env.POSTGRES_DB || 'aeon_saas_dev',
  user: process.env.POSTGRES_USER || 'postgres',
  password: process.env.POSTGRES_PASSWORD,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// workers/src/db/job-repository.ts
export class JobRepository {
  async createJob(jobData: CreateJobInput): Promise<Job> { /* ... */ }
  async getReadyJobs(limit: number): Promise<Job[]> { /* ... */ }
  async markJobRunning(jobId: number, workerId: string): Promise<void> { /* ... */ }
  async markJobCompleted(jobId: number, result: any): Promise<void> { /* ... */ }
  async markJobFailed(jobId: number, error: string): Promise<void> { /* ... */ }
  async moveToDeadLetterQueue(jobId: number, reason: string): Promise<void> { /* ... */ }
}
```

#### Task 2.5: Database Performance Optimization
- **ID**: GAP006-T2.5
- **Owner**: perf-analyzer agent
- **MCP Tools**: `mcp__claude-flow__bottleneck_analyze`, `mcp__claude-flow__daa_optimization`
- **Duration**: 3 hours
- **Dependencies**: T2.3, T2.4
- **Deliverables**:
  - Query performance analysis
  - Index optimization recommendations
  - Connection pooling tuning
  - Performance baseline metrics

**Discrete Steps**:
```yaml
1. Generate test data (10,000 jobs with various statuses)
2. Run EXPLAIN ANALYZE on get_ready_jobs()
3. Run EXPLAIN ANALYZE on common update queries
4. Measure query latency at P50, P95, P99
5. Analyze index usage with pg_stat_user_indexes
6. Test concurrent query performance (10 simultaneous workers)
7. Optimize slow queries (target: <50ms for get_ready_jobs)
8. Tune connection pool settings
9. Generate performance baseline report
```

**Performance Targets**:
```yaml
query_performance:
  get_ready_jobs:
    p50: <10ms
    p95: <50ms
    p99: <100ms

  job_updates:
    p50: <5ms
    p95: <20ms
    p99: <50ms

  concurrent_workers:
    workers: 10
    qps_per_worker: 10
    total_qps: 100
    p95_latency: <100ms
```

#### Task 2.6: Database Documentation
- **ID**: GAP006-T2.6
- **Owner**: api-docs agent
- **MCP Tools**: `mcp__claude-flow__memory_usage`
- **Duration**: 2 hours
- **Dependencies**: T2.5
- **Deliverables**:
  - Database schema documentation
  - ERD diagram
  - API documentation for repository methods
  - Memory stored in Qdrant

**Discrete Steps**:
```yaml
1. Create database schema diagram (ERD)
2. Document all tables with column descriptions
3. Document all functions and their usage
4. Document repository API with examples
5. Create migration rollback procedure
6. Document performance tuning guidelines
7. Store all documentation in Qdrant (namespace: gap-006-implementation)
```

### Phase 2 Success Criteria
- ✅ All 5 tables created successfully
- ✅ All functions and triggers working
- ✅ All indexes created and optimized
- ✅ Database access layer implemented and tested
- ✅ Performance targets met (P95 <50ms for get_ready_jobs)
- ✅ Documentation complete and stored in Qdrant

---

## Phase 3: Worker Development (Week 2 - Days 15-21)

**Objective**: Implement distributed Node.js worker pool
**Duration**: 7 days
**Estimated Hours**: 24 hours
**Estimated Cost**: $408
**Agents Required**: 4

### Tasks

#### Task 3.1: Create Worker Project Scaffold
- **ID**: GAP006-T3.1
- **Owner**: base-template-generator agent
- **MCP Tools**: `mcp__claude-flow__agent_spawn`
- **Duration**: 3 hours
- **Dependencies**: Phase 2 complete
- **Deliverables**:
  - `workers/` directory structure
  - `package.json` with dependencies
  - `tsconfig.json` for TypeScript compilation
  - Dockerfile for worker containerization
  - Basic project setup complete

**Discrete Steps**:
```yaml
1. Create directory structure:
   workers/
   ├── Dockerfile
   ├── package.json
   ├── tsconfig.json
   └── src/
       ├── index.ts
       ├── core/
       │   ├── worker.ts
       │   ├── job-executor.ts
       │   ├── error-handler.ts
       │   └── health-monitor.ts
       ├── handlers/
       │   ├── base-handler.ts
       │   └── index.ts
       ├── services/
       │   ├── postgres.ts
       │   ├── redis.ts
       │   └── metrics.ts
       └── config/
           ├── worker-config.ts
           └── retry-config.ts

2. Initialize package.json with dependencies:
   - typescript, @types/node
   - pg, @types/pg (PostgreSQL client)
   - ioredis, @types/ioredis (Redis client)
   - dotenv (environment configuration)
   - winston (logging)
   - prom-client (Prometheus metrics)

3. Create tsconfig.json with strict mode enabled

4. Create Dockerfile for worker deployment

5. Create .dockerignore for build optimization
```

**Expected package.json**:
```json
{
  "name": "aeon-workers",
  "version": "1.0.0",
  "description": "GAP-006 Job Management Workers",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "test": "jest",
    "lint": "eslint src/**/*.ts"
  },
  "dependencies": {
    "pg": "^8.11.0",
    "ioredis": "^5.3.2",
    "dotenv": "^16.3.1",
    "winston": "^3.11.0",
    "prom-client": "^15.1.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "@types/node": "^20.10.6",
    "@types/pg": "^8.10.9",
    "@types/ioredis": "^5.0.0",
    "ts-node": "^10.9.2",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.1",
    "@types/jest": "^29.5.11",
    "eslint": "^8.56.0",
    "@typescript-eslint/parser": "^6.17.0",
    "@typescript-eslint/eslint-plugin": "^6.17.0"
  }
}
```

#### Task 3.2: Implement Core Worker Class
- **ID**: GAP006-T3.2
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode` (dev mode)
- **Duration**: 6 hours
- **Dependencies**: T3.1
- **Deliverables**:
  - `core/worker.ts` base worker implementation
  - Job polling loop with Redis BRPOPLPUSH
  - Heartbeat mechanism
  - Graceful shutdown handling
  - Unit tests

**Discrete Steps**:
```yaml
1. Implement Worker class constructor with configuration
2. Implement start() method with polling loop
3. Implement pollQueue() using Redis BRPOPLPUSH
4. Implement processJob() with error handling
5. Implement heartbeat() periodic health signal
6. Implement shutdown() graceful termination
7. Add logging for all worker lifecycle events
8. Add metrics collection (jobs_processed, errors, etc.)
9. Write unit tests for Worker class
10. Validate with integration test
```

**Expected Implementation** (from architecture lines 538-607):
```typescript
// src/core/worker.ts
export class Worker {
  private workerId: string;
  private redis: Redis;
  private jobRepository: JobRepository;
  private running: boolean = false;
  private currentJob: Job | null = null;

  async start(): Promise<void> {
    this.running = true;
    logger.info(`Worker ${this.workerId} started`);

    while (this.running) {
      try {
        const job = await this.pollQueue();
        if (job) {
          await this.processJob(job);
        }
      } catch (error) {
        logger.error('Worker error:', error);
      }
    }
  }

  private async pollQueue(): Promise<Job | null> {
    // BRPOPLPUSH pattern for atomic job acquisition
    const jobIdStr = await this.redis.brpoplpush(
      'job:queue:pending',
      'job:queue:processing',
      this.config.pollIntervalMs / 1000
    );

    if (!jobIdStr) return null;

    const jobId = parseInt(jobIdStr);
    return await this.jobRepository.getJobById(jobId);
  }

  private async processJob(job: Job): Promise<void> {
    this.currentJob = job;

    try {
      await this.jobRepository.markJobRunning(job.id, this.workerId);

      const handler = this.getHandler(job.job_type);
      const result = await handler.execute(job.payload);

      await this.jobRepository.markJobCompleted(job.id, result);
      await this.redis.lrem('job:queue:processing', 1, job.id.toString());

      this.currentJob = null;
    } catch (error) {
      await this.handleJobError(job, error);
    }
  }

  // Additional methods...
}
```

#### Task 3.3: Implement Job Executor and Handlers
- **ID**: GAP006-T3.3
- **Owner**: coder agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode`
- **Duration**: 5 hours
- **Dependencies**: T3.2
- **Deliverables**:
  - `core/job-executor.ts` job execution engine
  - `handlers/base-handler.ts` abstract handler class
  - Sample job handlers (at least 2)
  - Handler registration system
  - Unit tests

**Discrete Steps**:
```yaml
1. Create JobExecutor class with timeout management
2. Create BaseHandler abstract class with execute() method
3. Implement handler registry (Map<string, BaseHandler>)
4. Create sample handlers:
   - EmailNotificationHandler
   - DataProcessingHandler
5. Implement handler timeout wrapper
6. Add handler error recovery
7. Add metrics collection per handler
8. Write unit tests for each handler
9. Write integration tests for executor
```

**Expected Implementation**:
```typescript
// src/core/job-executor.ts
export class JobExecutor {
  private handlers: Map<string, BaseHandler> = new Map();

  registerHandler(jobType: string, handler: BaseHandler): void {
    this.handlers.set(jobType, handler);
  }

  async execute(job: Job): Promise<any> {
    const handler = this.handlers.get(job.job_type);
    if (!handler) {
      throw new Error(`No handler registered for job type: ${job.job_type}`);
    }

    const timeoutMs = job.timeout_ms || 300000;
    return await this.executeWithTimeout(handler, job, timeoutMs);
  }

  private async executeWithTimeout(handler: BaseHandler, job: Job, timeoutMs: number): Promise<any> {
    return Promise.race([
      handler.execute(job.payload),
      this.createTimeout(timeoutMs)
    ]);
  }
}

// src/handlers/base-handler.ts
export abstract class BaseHandler {
  abstract execute(payload: any): Promise<any>;

  async validate(payload: any): Promise<void> {
    // Override for validation
  }
}

// src/handlers/email-notification-handler.ts
export class EmailNotificationHandler extends BaseHandler {
  async execute(payload: { to: string; subject: string; body: string }): Promise<void> {
    await this.validate(payload);
    logger.info(`Sending email to ${payload.to}`);
    // Email sending implementation
  }
}
```

#### Task 3.4: Implement Error Recovery and Retry Logic
- **ID**: GAP006-T3.4
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__daa_fault_tolerance`
- **Duration**: 5 hours
- **Dependencies**: T3.3
- **Deliverables**:
  - `core/error-handler.ts` error recovery implementation
  - Exponential backoff retry logic
  - Dead letter queue integration
  - Error classification system
  - Unit tests

**Discrete Steps**:
```yaml
1. Create ErrorHandler class
2. Implement error classification:
   - Transient errors (retry)
   - Permanent errors (DLQ)
   - Unknown errors (retry with caution)
3. Implement exponential backoff calculation
4. Implement retry logic with max attempts
5. Implement moveToDeadLetterQueue() for permanent failures
6. Add error logging and monitoring
7. Add metrics for error rates by type
8. Write unit tests for retry scenarios
9. Write integration tests with actual failures
```

**Expected Implementation**:
```typescript
// src/core/error-handler.ts
export class ErrorHandler {
  async handleJobError(job: Job, error: Error, jobRepository: JobRepository): Promise<void> {
    const errorType = this.classifyError(error);

    if (errorType === ErrorType.PERMANENT || job.retry_count >= job.max_retries) {
      await this.moveToDeadLetterQueue(job, error, jobRepository);
      return;
    }

    await this.scheduleRetry(job, error, jobRepository);
  }

  private classifyError(error: Error): ErrorType {
    // Network errors, timeouts → TRANSIENT
    if (error.message.includes('ECONNREFUSED') || error.message.includes('timeout')) {
      return ErrorType.TRANSIENT;
    }

    // Validation errors, business logic errors → PERMANENT
    if (error instanceof ValidationError || error instanceof BusinessError) {
      return ErrorType.PERMANENT;
    }

    // Unknown → TRANSIENT (retry with caution)
    return ErrorType.TRANSIENT;
  }

  private async scheduleRetry(job: Job, error: Error, jobRepository: JobRepository): Promise<void> {
    const retryCount = job.retry_count + 1;
    const delayMs = this.calculateBackoff(retryCount);

    await jobRepository.updateJob(job.id, {
      status: 'pending',
      retry_count: retryCount,
      error_message: error.message,
      scheduled_at: new Date(Date.now() + delayMs)
    });

    logger.info(`Job ${job.id} scheduled for retry #${retryCount} in ${delayMs}ms`);
  }

  private calculateBackoff(retryCount: number): number {
    const baseDelay = 1000; // 1 second
    const multiplier = 2;
    return baseDelay * Math.pow(multiplier, retryCount - 1);
    // Retry 1: 1s, Retry 2: 2s, Retry 3: 4s, Retry 4: 8s, Retry 5: 16s
  }

  private async moveToDeadLetterQueue(job: Job, error: Error, jobRepository: JobRepository): Promise<void> {
    await jobRepository.moveToDeadLetterQueue(job.id, error.message);
    logger.error(`Job ${job.id} moved to DLQ after ${job.retry_count} retries`);

    // Emit alert for DLQ accumulation
    metricsCollector.incrementDLQJobs(job.job_type);
  }
}
```

#### Task 3.5: Implement Health Monitoring and Metrics
- **ID**: GAP006-T3.5
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__swarm_monitor`, `mcp__claude-flow__agent_metrics`
- **Duration**: 4 hours
- **Dependencies**: T3.4
- **Deliverables**:
  - `core/health-monitor.ts` health check implementation
  - Prometheus metrics collection
  - Worker heartbeat tracking
  - Health status API endpoint
  - Metrics dashboard data

**Discrete Steps**:
```yaml
1. Create HealthMonitor class
2. Implement heartbeat() method with Redis SET with TTL
3. Implement getWorkerHealth() to check all workers
4. Implement Prometheus metrics collection:
   - jobs_processed_total (counter)
   - jobs_failed_total (counter)
   - job_duration_seconds (histogram)
   - queue_depth_gauge (gauge)
   - worker_alive_gauge (gauge)
5. Create metrics HTTP endpoint (/metrics)
6. Add health check endpoint (/health)
7. Write unit tests for health monitor
8. Test metrics collection with sample data
```

**Expected Implementation**:
```typescript
// src/core/health-monitor.ts
export class HealthMonitor {
  private workerId: string;
  private redis: Redis;
  private heartbeatInterval: NodeJS.Timer | null = null;

  startHeartbeat(): void {
    this.heartbeatInterval = setInterval(
      () => this.sendHeartbeat(),
      30000 // 30 seconds
    );
  }

  private async sendHeartbeat(): Promise<void> {
    const key = `worker:heartbeat:${this.workerId}`;
    await this.redis.set(key, Date.now(), 'EX', 60); // 60 second TTL
    logger.debug(`Heartbeat sent for worker ${this.workerId}`);
  }

  async getWorkerHealth(): Promise<WorkerHealth[]> {
    const keys = await this.redis.keys('worker:heartbeat:*');
    const health: WorkerHealth[] = [];

    for (const key of keys) {
      const workerId = key.replace('worker:heartbeat:', '');
      const timestamp = await this.redis.get(key);
      const alive = timestamp !== null;
      const lastHeartbeat = alive ? new Date(parseInt(timestamp)) : null;

      health.push({ workerId, alive, lastHeartbeat });
    }

    return health;
  }
}

// src/services/metrics.ts
import { Counter, Histogram, Gauge, register } from 'prom-client';

export class MetricsCollector {
  private jobsProcessed: Counter;
  private jobsFailed: Counter;
  private jobDuration: Histogram;
  private queueDepth: Gauge;
  private workerAlive: Gauge;

  constructor() {
    this.jobsProcessed = new Counter({
      name: 'jobs_processed_total',
      help: 'Total number of jobs processed',
      labelNames: ['job_type', 'status']
    });

    this.jobsFailed = new Counter({
      name: 'jobs_failed_total',
      help: 'Total number of jobs failed',
      labelNames: ['job_type', 'error_type']
    });

    this.jobDuration = new Histogram({
      name: 'job_duration_seconds',
      help: 'Job execution duration in seconds',
      labelNames: ['job_type'],
      buckets: [0.1, 0.5, 1, 2, 5, 10, 30, 60]
    });

    this.queueDepth = new Gauge({
      name: 'queue_depth_gauge',
      help: 'Current job queue depth',
      labelNames: ['status']
    });

    this.workerAlive = new Gauge({
      name: 'worker_alive_gauge',
      help: 'Worker alive status (1=alive, 0=dead)',
      labelNames: ['worker_id']
    });
  }

  incrementJobProcessed(jobType: string, status: string): void {
    this.jobsProcessed.inc({ job_type: jobType, status });
  }

  recordJobDuration(jobType: string, durationSeconds: number): void {
    this.jobDuration.observe({ job_type: jobType }, durationSeconds);
  }

  updateQueueDepth(status: string, depth: number): void {
    this.queueDepth.set({ status }, depth);
  }

  updateWorkerHealth(workerId: string, alive: boolean): void {
    this.workerAlive.set({ worker_id: workerId }, alive ? 1 : 0);
  }

  getMetrics(): string {
    return register.metrics();
  }
}
```

#### Task 3.6: Worker Integration Testing
- **ID**: GAP006-T3.6
- **Owner**: tester agent
- **MCP Tools**: `mcp__claude-flow__agent_spawn` (tester)
- **Duration**: 4 hours
- **Dependencies**: T3.5
- **Deliverables**:
  - Integration test suite for workers
  - End-to-end job processing tests
  - Failure scenario tests
  - Performance tests
  - Test coverage report (>80%)

**Discrete Steps**:
```yaml
1. Create integration test environment
2. Write test: Job submission → processing → completion
3. Write test: Job failure → retry → success
4. Write test: Job failure → max retries → DLQ
5. Write test: Multiple workers processing concurrent jobs
6. Write test: Worker graceful shutdown
7. Write test: Worker crash recovery
8. Write test: Timeout handling
9. Run tests and measure coverage
10. Generate test report
```

**Test Scenarios**:
```typescript
// tests/integration/worker.test.ts
describe('Worker Integration Tests', () => {
  it('should process job successfully', async () => {
    // 1. Create job in database
    const job = await jobRepository.createJob({
      job_type: 'email_notification',
      payload: { to: 'test@example.com', subject: 'Test', body: 'Test body' }
    });

    // 2. Add job to Redis queue
    await redis.lpush('job:queue:pending', job.id.toString());

    // 3. Start worker
    const worker = new Worker(workerId, config);
    await worker.start();

    // 4. Wait for job completion (max 5 seconds)
    await waitForJobCompletion(job.id, 5000);

    // 5. Verify job marked as completed
    const updatedJob = await jobRepository.getJobById(job.id);
    expect(updatedJob.status).toBe('completed');
  });

  it('should retry failed job with exponential backoff', async () => {
    // 1. Create job that will fail
    const job = await jobRepository.createJob({
      job_type: 'failing_job',
      payload: { fail_count: 2 } // Fail 2 times, then succeed
    });

    await redis.lpush('job:queue:pending', job.id.toString());

    const worker = new Worker(workerId, config);
    await worker.start();

    // 2. Wait for retries and eventual success
    await waitForJobCompletion(job.id, 15000);

    // 3. Verify retry count
    const updatedJob = await jobRepository.getJobById(job.id);
    expect(updatedJob.retry_count).toBe(2);
    expect(updatedJob.status).toBe('completed');
  });

  it('should move job to DLQ after max retries', async () => {
    // Test permanent failure scenario
  });

  it('should handle worker graceful shutdown', async () => {
    // Test shutdown while processing job
  });
});
```

### Phase 3 Success Criteria
- ✅ Worker project scaffold created and building
- ✅ Core Worker class implemented with polling loop
- ✅ Job handlers implemented and registered
- ✅ Error recovery with exponential backoff working
- ✅ Dead letter queue integration functional
- ✅ Health monitoring and metrics collection operational
- ✅ Integration tests passing with >80% coverage

---

## Phase 4: API Integration (Week 2 - Days 22-28)

**Objective**: Create Next.js API endpoints for job management
**Duration**: 7 days
**Estimated Hours**: 18 hours
**Estimated Cost**: $306
**Agents Required**: 3

### Tasks

#### Task 4.1: Create Job Submission API
- **ID**: GAP006-T4.1
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode` (api mode)
- **Duration**: 4 hours
- **Dependencies**: Phase 3 complete
- **Deliverables**:
  - POST `/api/jobs` endpoint for job submission
  - Request validation with Zod schemas
  - Response with job ID and status
  - Error handling
  - API tests

**Discrete Steps**:
```yaml
1. Create app/api/jobs/route.ts
2. Implement POST handler with request validation
3. Create Zod schema for job submission
4. Implement job creation in PostgreSQL
5. Add job to Redis queue
6. Return job ID and initial status
7. Add error handling for validation failures
8. Add rate limiting (optional)
9. Write API tests with supertest
10. Document API with OpenAPI schema
```

**Expected Implementation**:
```typescript
// app/api/jobs/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { JobRepository } from '@/lib/job-repository';
import { redisClient } from '@/lib/redis';

const createJobSchema = z.object({
  job_type: z.string().min(1).max(100),
  payload: z.record(z.any()),
  priority: z.number().int().min(0).max(100).optional().default(50),
  max_retries: z.number().int().min(0).max(10).optional().default(3),
  timeout_ms: z.number().int().min(1000).max(600000).optional().default(300000),
  scheduled_at: z.string().datetime().optional(),
  metadata: z.record(z.any()).optional()
});

export async function POST(request: NextRequest) {
  try {
    // 1. Parse and validate request body
    const body = await request.json();
    const validatedData = createJobSchema.parse(body);

    // 2. Create job in database
    const jobRepository = new JobRepository();
    const job = await jobRepository.createJob({
      ...validatedData,
      created_by: request.headers.get('x-user-id') || 'api'
    });

    // 3. Add job to Redis queue (if not scheduled for future)
    if (!validatedData.scheduled_at || new Date(validatedData.scheduled_at) <= new Date()) {
      await redisClient.lpush('job:queue:pending', job.id.toString());
    }

    // 4. Return job ID and status
    return NextResponse.json({
      success: true,
      job_id: job.id,
      status: job.status,
      created_at: job.created_at
    }, { status: 201 });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({
        success: false,
        error: 'Validation failed',
        details: error.errors
      }, { status: 400 });
    }

    console.error('Job creation error:', error);
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}
```

#### Task 4.2: Create Job Status API
- **ID**: GAP006-T4.2
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode` (api mode)
- **Duration**: 3 hours
- **Dependencies**: T4.1
- **Deliverables**:
  - GET `/api/jobs/:id` endpoint for job status
  - GET `/api/jobs` endpoint for job listing with filters
  - Pagination support
  - Status filtering (pending, running, completed, failed)
  - API tests

**Discrete Steps**:
```yaml
1. Create app/api/jobs/[id]/route.ts for single job status
2. Implement GET handler for job by ID
3. Create app/api/jobs/route.ts GET handler for job listing
4. Implement pagination (limit, offset)
5. Implement filtering by status, job_type, created_by
6. Add sorting (created_at, updated_at, priority)
7. Return job execution history
8. Write API tests for both endpoints
9. Document API with OpenAPI schema
```

**Expected Implementation**:
```typescript
// app/api/jobs/[id]/route.ts
export async function GET(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const jobId = parseInt(params.id);
    const jobRepository = new JobRepository();

    const job = await jobRepository.getJobById(jobId);

    if (!job) {
      return NextResponse.json({
        success: false,
        error: 'Job not found'
      }, { status: 404 });
    }

    // Get execution history
    const executions = await jobRepository.getJobExecutions(jobId);

    return NextResponse.json({
      success: true,
      job: {
        ...job,
        executions
      }
    });

  } catch (error) {
    console.error('Get job error:', error);
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}

// app/api/jobs/route.ts (GET method)
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;

    const filters = {
      status: searchParams.get('status') as JobStatus | null,
      job_type: searchParams.get('job_type') || undefined,
      created_by: searchParams.get('created_by') || undefined,
      limit: parseInt(searchParams.get('limit') || '50'),
      offset: parseInt(searchParams.get('offset') || '0')
    };

    const jobRepository = new JobRepository();
    const jobs = await jobRepository.getJobs(filters);
    const totalCount = await jobRepository.getJobCount(filters);

    return NextResponse.json({
      success: true,
      jobs,
      pagination: {
        limit: filters.limit,
        offset: filters.offset,
        total: totalCount,
        has_more: (filters.offset + filters.limit) < totalCount
      }
    });

  } catch (error) {
    console.error('List jobs error:', error);
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}
```

#### Task 4.3: Create Job Cancellation API
- **ID**: GAP006-T4.3
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode` (api mode)
- **Duration**: 3 hours
- **Dependencies**: T4.2
- **Deliverables**:
  - DELETE `/api/jobs/:id` endpoint for job cancellation
  - Cancel logic for pending, running jobs
  - Graceful worker termination handling
  - API tests

**Discrete Steps**:
```yaml
1. Create DELETE handler in app/api/jobs/[id]/route.ts
2. Implement cancellation for pending jobs (remove from queue)
3. Implement cancellation for running jobs (signal worker)
4. Update job status to 'cancelled'
5. Remove from Redis queue
6. Add cancellation reason to metadata
7. Return cancellation confirmation
8. Write API tests for cancel scenarios
9. Document API with OpenAPI schema
```

**Expected Implementation**:
```typescript
// app/api/jobs/[id]/route.ts (DELETE method)
export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const jobId = parseInt(params.id);
    const jobRepository = new JobRepository();

    const job = await jobRepository.getJobById(jobId);

    if (!job) {
      return NextResponse.json({
        success: false,
        error: 'Job not found'
      }, { status: 404 });
    }

    // Can only cancel pending or running jobs
    if (!['pending', 'running'].includes(job.status)) {
      return NextResponse.json({
        success: false,
        error: `Cannot cancel job in ${job.status} status`
      }, { status: 400 });
    }

    // Remove from Redis queue (pending or processing)
    if (job.status === 'pending') {
      await redisClient.lrem('job:queue:pending', 1, jobId.toString());
    } else if (job.status === 'running') {
      await redisClient.lrem('job:queue:processing', 1, jobId.toString());
      // Signal worker to cancel (set cancellation flag in Redis)
      await redisClient.set(`job:cancel:${jobId}`, '1', 'EX', 300);
    }

    // Update job status to cancelled
    await jobRepository.updateJob(jobId, {
      status: 'cancelled',
      error_message: 'Job cancelled by user',
      completed_at: new Date()
    });

    return NextResponse.json({
      success: true,
      message: 'Job cancelled successfully',
      job_id: jobId
    });

  } catch (error) {
    console.error('Cancel job error:', error);
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}
```

#### Task 4.4: Create Monitoring Dashboard API
- **ID**: GAP006-T4.4
- **Owner**: backend-dev agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode` (api mode)
- **Duration**: 4 hours
- **Dependencies**: T4.3
- **Deliverables**:
  - GET `/api/jobs/metrics` endpoint for dashboard metrics
  - Queue depth statistics
  - Worker health status
  - Job throughput metrics
  - API tests

**Discrete Steps**:
```yaml
1. Create app/api/jobs/metrics/route.ts
2. Implement getQueueDepths() (pending, running, failed, dlq)
3. Implement getWorkerHealth() from Redis heartbeats
4. Implement getJobStatistics() (last hour, last 24h)
5. Implement getThroughputMetrics() (jobs/min)
6. Implement getErrorRates() by job type
7. Format response for dashboard consumption
8. Write API tests for metrics endpoint
9. Document API with OpenAPI schema
```

**Expected Implementation**:
```typescript
// app/api/jobs/metrics/route.ts
export async function GET(request: NextRequest) {
  try {
    const jobRepository = new JobRepository();
    const healthMonitor = new HealthMonitor(redisClient);

    // Get queue depths
    const queueDepths = {
      pending: await redisClient.llen('job:queue:pending'),
      processing: await redisClient.llen('job:queue:processing'),
      failed: await jobRepository.getJobCount({ status: 'failed' }),
      dlq: await jobRepository.getDLQCount()
    };

    // Get worker health
    const workerHealth = await healthMonitor.getWorkerHealth();

    // Get job statistics (last 24 hours)
    const now = new Date();
    const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);

    const stats = await jobRepository.getJobStatistics({
      from: yesterday,
      to: now
    });

    // Calculate throughput (jobs per minute)
    const throughput = {
      last_hour: await jobRepository.getThroughput({ minutes: 60 }),
      last_24h: await jobRepository.getThroughput({ minutes: 1440 })
    };

    // Get error rates by job type
    const errorRates = await jobRepository.getErrorRates();

    return NextResponse.json({
      success: true,
      metrics: {
        queue_depths: queueDepths,
        worker_health: workerHealth,
        statistics: stats,
        throughput,
        error_rates: errorRates,
        timestamp: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('Get metrics error:', error);
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}
```

#### Task 4.5: API Documentation and Testing
- **ID**: GAP006-T4.5
- **Owner**: api-docs agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode` (docs mode)
- **Duration**: 3 hours
- **Dependencies**: T4.4
- **Deliverables**:
  - OpenAPI 3.0 specification for all endpoints
  - API documentation website/page
  - Postman collection
  - API integration tests
  - Rate limiting documentation

**Discrete Steps**:
```yaml
1. Create OpenAPI 3.0 specification (docs/api/gap-006-openapi.yaml)
2. Document all endpoints with examples
3. Generate Postman collection from OpenAPI spec
4. Create API documentation page (Next.js route)
5. Write comprehensive integration tests
6. Document authentication requirements
7. Document rate limiting policies
8. Store documentation in Qdrant
```

### Phase 4 Success Criteria
- ✅ Job submission API working and validated
- ✅ Job status and listing API functional with filters
- ✅ Job cancellation API working for pending and running jobs
- ✅ Monitoring dashboard API returning real-time metrics
- ✅ OpenAPI documentation complete
- ✅ API integration tests passing

---

## Phase 5: Testing & Validation (Week 3 - Days 29-35)

**Objective**: Comprehensive testing and validation
**Duration**: 7 days
**Estimated Hours**: 20 hours
**Estimated Cost**: $340
**Agents Required**: 4

### Tasks

#### Task 5.1: Unit Test Suite
- **ID**: GAP006-T5.1
- **Owner**: tester agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode` (test mode)
- **Duration**: 5 hours
- **Dependencies**: Phase 4 complete
- **Deliverables**:
  - Unit tests for all worker components
  - Unit tests for all API endpoints
  - Unit tests for database repository
  - >85% code coverage
  - Test report

**Discrete Steps**:
```yaml
1. Write unit tests for Worker class (10+ tests)
2. Write unit tests for JobExecutor (8+ tests)
3. Write unit tests for ErrorHandler (12+ tests)
4. Write unit tests for HealthMonitor (6+ tests)
5. Write unit tests for JobRepository (15+ tests)
6. Write unit tests for API route handlers (12+ tests)
7. Run test coverage report
8. Fix coverage gaps to reach >85%
9. Generate test report with metrics
```

**Coverage Targets**:
```yaml
code_coverage:
  overall: >85%

  by_component:
    worker_core: >90%
    job_executor: >85%
    error_handler: >90%
    health_monitor: >80%
    job_repository: >85%
    api_routes: >80%
```

#### Task 5.2: Integration Test Suite
- **ID**: GAP006-T5.2
- **Owner**: tester agent
- **MCP Tools**: `mcp__claude-flow__sparc_mode` (test mode)
- **Duration**: 6 hours
- **Dependencies**: T5.1
- **Deliverables**:
  - End-to-end integration tests
  - Multi-worker coordination tests
  - Database transaction tests
  - Redis queue tests
  - Test report

**Discrete Steps**:
```yaml
1. Write test: Job submission via API → Worker processing → Completion
2. Write test: Job failure → Retry → Success
3. Write test: Job failure → DLQ after max retries
4. Write test: Multiple workers processing concurrent jobs
5. Write test: Worker crash → Job recovery
6. Write test: Redis failure → Worker reconnection
7. Write test: Database connection loss → Recovery
8. Write test: Job cancellation during execution
9. Write test: Scheduled jobs activation
10. Generate integration test report
```

#### Task 5.3: Load Testing
- **ID**: GAP006-T5.3
- **Owner**: perf-analyzer agent
- **MCP Tools**: `mcp__claude-flow__benchmark_run`, `mcp__claude-flow__bottleneck_analyze`
- **Duration**: 5 hours
- **Dependencies**: T5.2
- **Deliverables**:
  - Load test suite (k6 or Artillery)
  - Performance benchmarks
  - Bottleneck analysis
  - Capacity planning recommendations
  - Performance report

**Discrete Steps**:
```yaml
1. Create load test scenarios:
   - Sustained load: 100 jobs/min for 10 minutes
   - Burst load: 500 jobs in 1 minute
   - Concurrent workers: 5 workers processing simultaneously
2. Execute load tests and measure:
   - API latency (P50, P95, P99)
   - Worker throughput (jobs/min)
   - Queue depth over time
   - Database connection pool usage
   - Redis memory usage
3. Identify bottlenecks
4. Recommend capacity improvements
5. Generate performance report
```

**Performance Targets**:
```yaml
performance_slos:
  api_latency:
    job_submission_p95: <100ms
    job_status_p95: <50ms

  worker_throughput:
    jobs_per_minute: >100

  queue_depth:
    max_pending: <1000 (sustained)
    max_processing: <50

  database:
    query_latency_p95: <50ms
    connection_pool_usage: <80%

  redis:
    memory_usage: <256MB
    command_latency_p95: <10ms
```

#### Task 5.4: Failure Scenario Testing
- **ID**: GAP006-T5.4
- **Owner**: tester agent
- **MCP Tools**: `mcp__claude-flow__daa_fault_tolerance`
- **Duration**: 4 hours
- **Dependencies**: T5.3
- **Deliverables**:
  - Chaos engineering test suite
  - Failure recovery validation
  - Data consistency tests
  - Resilience report

**Discrete Steps**:
```yaml
1. Test scenario: Redis container stop → Worker reconnection
2. Test scenario: PostgreSQL restart → Worker recovery
3. Test scenario: Worker kill -9 during job → Job requeue
4. Test scenario: Network partition → Retry behavior
5. Test scenario: Full Redis memory → Eviction handling
6. Test scenario: Database deadlock → Retry logic
7. Test scenario: Corrupt job payload → Error handling
8. Verify data consistency after each failure
9. Generate resilience report
```

### Phase 5 Success Criteria
- ✅ Unit test suite passing with >85% coverage
- ✅ Integration test suite passing (100% success rate)
- ✅ Load tests meeting performance SLOs
- ✅ Failure scenario tests demonstrating resilience
- ✅ All test reports generated and reviewed

---

## Phase 6: Deployment (Week 3-4 - Days 36-42)

**Objective**: Production deployment with monitoring
**Duration**: 7 days
**Estimated Hours**: 14 hours
**Estimated Cost**: $238
**Agents Required**: 4

### Tasks

#### Task 6.1: Create Worker Docker Image
- **ID**: GAP006-T6.1
- **Owner**: cicd-engineer agent
- **MCP Tools**: `mcp__claude-flow__terminal_execute`
- **Duration**: 3 hours
- **Dependencies**: Phase 5 complete
- **Deliverables**:
  - Optimized Dockerfile for workers
  - Multi-stage build for size optimization
  - Docker image built and tested
  - Image pushed to registry (if applicable)

**Discrete Steps**:
```yaml
1. Create optimized Dockerfile with multi-stage build
2. Configure build arguments and environment variables
3. Build image: docker build -t aeon-workers:latest ./workers
4. Test image locally: docker run --network openspg-network aeon-workers:latest
5. Verify worker connects to Redis and PostgreSQL
6. Optimize image size (target: <200MB)
7. Tag image with version
8. Document Docker image usage
```

**Expected Dockerfile**:
```dockerfile
# Dockerfile (workers/)
# Multi-stage build for optimization

# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY tsconfig.json ./
COPY src ./src

RUN npm run build

# Stage 2: Runtime
FROM node:20-alpine
WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Copy dependencies and built code
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:9090/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

EXPOSE 9090

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

#### Task 6.2: Create Worker Deployment Configuration
- **ID**: GAP006-T6.2
- **Owner**: cicd-engineer agent
- **MCP Tools**: `mcp__claude-flow__config_manage`
- **Duration**: 2 hours
- **Dependencies**: T6.1
- **Deliverables**:
  - `docker-compose.workers.yml` for worker deployment
  - Worker scaling configuration (2-5 workers)
  - Resource limits configured
  - Restart policies set

**Discrete Steps**:
```yaml
1. Create docker-compose.workers.yml
2. Configure worker service with scaling (2-5 replicas)
3. Set resource limits (memory: 256MB, cpu: 0.5)
4. Configure restart policy (on-failure, max 3 attempts)
5. Set environment variables from .env
6. Configure networks (openspg-network)
7. Add dependency on aeon-redis and aeon-postgres-dev
8. Test worker deployment
```

**Expected docker-compose.workers.yml**:
```yaml
version: '3.8'

services:
  aeon-worker:
    image: aeon-workers:latest
    build:
      context: ./workers
      dockerfile: Dockerfile
    container_name: aeon-worker-${WORKER_ID:-1}
    networks:
      - openspg-network
    environment:
      - NODE_ENV=production
      - POSTGRES_HOST=aeon-postgres-dev
      - POSTGRES_PORT=5432
      - POSTGRES_DB=aeon_saas_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - REDIS_HOST=aeon-redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - WORKER_ID=${WORKER_ID:-worker-1}
      - WORKER_CONCURRENCY=${WORKER_CONCURRENCY:-5}
      - WORKER_POLL_INTERVAL=${WORKER_POLL_INTERVAL:-1000}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
    depends_on:
      - aeon-redis
      - aeon-postgres-dev
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:9090/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s

networks:
  openspg-network:
    external: true
```

#### Task 6.3: Deploy to Staging Environment
- **ID**: GAP006-T6.3
- **Owner**: cicd-engineer agent
- **MCP Tools**: `mcp__claude-flow__terminal_execute`, `mcp__claude-flow__health_check`
- **Duration**: 3 hours
- **Dependencies**: T6.2
- **Deliverables**:
  - Workers deployed to staging
  - Health checks passing
  - Smoke tests executed
  - Staging validation report

**Discrete Steps**:
```yaml
1. Deploy Redis: docker-compose -f docker-compose.redis.yml up -d
2. Run database migration on staging
3. Deploy workers: docker-compose -f docker-compose.workers.yml up -d --scale aeon-worker=3
4. Verify worker containers running
5. Execute smoke tests:
   - Submit test job via API
   - Verify job processed successfully
   - Check worker health endpoints
   - Verify metrics collection
6. Monitor for 1 hour for stability
7. Generate staging validation report
```

**Smoke Tests**:
```bash
#!/bin/bash
# smoke-tests.sh

echo "=== GAP-006 Staging Smoke Tests ==="

# Test 1: Submit job via API
echo "Test 1: Submit job"
JOB_RESPONSE=$(curl -s -X POST http://localhost:3000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"job_type":"test_job","payload":{"message":"smoke test"}}')
JOB_ID=$(echo $JOB_RESPONSE | jq -r '.job_id')
echo "Created job ID: $JOB_ID"

# Test 2: Wait for job completion
echo "Test 2: Wait for job completion (max 30s)"
for i in {1..30}; do
  STATUS=$(curl -s http://localhost:3000/api/jobs/$JOB_ID | jq -r '.job.status')
  echo "Attempt $i: Job status = $STATUS"
  if [ "$STATUS" = "completed" ]; then
    echo "✅ Job completed successfully"
    break
  fi
  sleep 1
done

# Test 3: Check worker health
echo "Test 3: Check worker health"
WORKERS=$(docker ps --filter "name=aeon-worker" --format "{{.Names}}")
for WORKER in $WORKERS; do
  HEALTH=$(docker inspect --format='{{.State.Health.Status}}' $WORKER)
  echo "Worker $WORKER: $HEALTH"
done

# Test 4: Check metrics endpoint
echo "Test 4: Check metrics endpoint"
METRICS=$(curl -s http://localhost:3000/api/jobs/metrics)
QUEUE_DEPTH=$(echo $METRICS | jq -r '.metrics.queue_depths.pending')
echo "Queue depth: $QUEUE_DEPTH"

echo "=== Smoke tests complete ==="
```

#### Task 6.4: Setup Monitoring and Alerting
- **ID**: GAP006-T6.4
- **Owner**: cicd-engineer agent
- **MCP Tools**: `mcp__claude-flow__swarm_monitor`, `mcp__claude-flow__config_manage`
- **Duration**: 4 hours
- **Dependencies**: T6.3
- **Deliverables**:
  - Prometheus configuration (if enabled)
  - Grafana dashboard (if enabled)
  - Alert rules configured
  - Monitoring documentation

**Discrete Steps**:
```yaml
1. Configure Prometheus scraping (if enabled):
   - Worker metrics endpoint (/metrics)
   - API metrics endpoint
2. Create Grafana dashboard (if enabled):
   - Queue depth over time
   - Worker health status
   - Job throughput
   - Error rates
   - P95 latency
3. Configure alert rules:
   - Queue depth > 1000 (warning)
   - Queue depth > 5000 (critical)
   - Worker down (critical)
   - Failure rate > 10% (warning)
   - DLQ accumulation > 50 (warning)
4. Test alert firing with simulated failures
5. Document monitoring setup
```

**Alert Rules** (from architecture lines 1616-1661):
```yaml
# alert-rules.yml
groups:
  - name: gap006_job_management
    interval: 30s
    rules:
      - alert: HighQueueDepth
        expr: queue_depth_gauge{status="pending"} > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pending queue depth exceeds 1000 jobs"
          description: "Consider scaling workers"

      - alert: CriticalQueueDepth
        expr: queue_depth_gauge{status="pending"} > 5000
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Pending queue depth exceeds 5000 jobs"
          description: "Immediate scaling required"

      - alert: WorkerDown
        expr: worker_alive_gauge == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Worker {{$labels.worker_id}} is not responding"
          description: "Restart worker immediately"

      - alert: HighFailureRate
        expr: (rate(jobs_failed_total[5m]) / rate(jobs_processed_total[5m])) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Job failure rate exceeds 10%"
          description: "Investigate failures"

      - alert: DLQAccumulation
        expr: queue_depth_gauge{status="dlq"} > 50
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Dead letter queue has > 50 jobs"
          description: "Review DLQ jobs"
```

#### Task 6.5: Production Deployment
- **ID**: GAP006-T6.5
- **Owner**: production-validator agent
- **MCP Tools**: `mcp__claude-flow__health_check`, `mcp__claude-flow__diagnostic_run`
- **Duration**: 3 hours
- **Dependencies**: T6.4
- **Deliverables**:
  - Production deployment executed
  - All services healthy
  - Production smoke tests passing
  - Production validation report

**Discrete Steps**:
```yaml
1. Final staging validation
2. Create production deployment checklist
3. Deploy to production:
   - Deploy Redis (already running)
   - Run database migration
   - Deploy workers (start with 2 replicas)
4. Execute production smoke tests
5. Monitor for 2 hours:
   - Worker health
   - Job processing
   - Error rates
   - Queue depths
6. Scale workers based on load (2-5 replicas)
7. Generate production validation report
8. Update runbook with deployment procedures
```

**Production Deployment Checklist**:
```yaml
pre_deployment:
  - [ ] Staging validation complete
  - [ ] All tests passing
  - [ ] Database migration tested
  - [ ] Rollback plan documented
  - [ ] Monitoring configured
  - [ ] Alert rules active

deployment:
  - [ ] Database migration executed
  - [ ] Redis verified healthy
  - [ ] Workers deployed (2 replicas initially)
  - [ ] Health checks passing
  - [ ] Smoke tests executed

post_deployment:
  - [ ] All services healthy for 2 hours
  - [ ] Zero error rate
  - [ ] Queue depths normal (<100)
  - [ ] Worker scaling tested (2→5→2)
  - [ ] Documentation updated
  - [ ] Team notified
```

#### Task 6.6: Documentation and Handoff
- **ID**: GAP006-T6.6
- **Owner**: api-docs agent
- **MCP Tools**: `mcp__claude-flow__memory_usage`
- **Duration**: 2 hours
- **Dependencies**: T6.5
- **Deliverables**:
  - Operations runbook
  - Deployment guide
  - Troubleshooting guide
  - API documentation final
  - All documentation in Qdrant

**Discrete Steps**:
```yaml
1. Create operations runbook:
   - Worker scaling procedures
   - Failure recovery procedures
   - DLQ management
   - Database maintenance
2. Create deployment guide:
   - Fresh deployment steps
   - Upgrade procedures
   - Rollback procedures
3. Create troubleshooting guide:
   - Common issues and resolutions
   - Log analysis
   - Debugging procedures
4. Update API documentation with production URLs
5. Store all documentation in Qdrant (namespace: gap-006-production)
6. Update project README with GAP-006 section
7. Conduct team handoff session
```

### Phase 6 Success Criteria
- ✅ Workers deployed to production with 2-5 replicas
- ✅ All health checks passing
- ✅ Production smoke tests successful
- ✅ Monitoring and alerting operational
- ✅ Zero critical errors in first 2 hours
- ✅ Complete documentation delivered

---

## Resource Requirements

### Agents Required (12 Total)

| Agent Type | Phases Used | Total Hours | Purpose |
|------------|-------------|-------------|---------|
| **backend-dev** | 1, 2, 3, 4 | 28h | Core development (Redis, DB, Workers, API) |
| **cicd-engineer** | 1, 6 | 14h | Infrastructure and deployment |
| **coder** | 1, 2, 3 | 12h | Implementation support |
| **tester** | 2, 3, 5 | 15h | Testing and validation |
| **production-validator** | 1, 6 | 6h | Production readiness |
| **api-docs** | 1, 2, 4, 6 | 9h | Documentation |
| **perf-analyzer** | 2, 5 | 8h | Performance optimization |
| **base-template-generator** | 3 | 3h | Project scaffolding |
| **backend-dev (specialist)** | 3, 4 | 10h | API and worker specialist |
| **system-architect** | Review | 2h | Architecture review |
| **reviewer** | Review | 3h | Code review |
| **code-analyzer** | Review | 2h | Code quality analysis |

**Total Agent Hours**: 112 hours
**Total Agent Cost**: $1,904 (at $17/hour)

### Infrastructure Requirements

**Existing Infrastructure (EXTENDS - No Additional Cost)**:
- ✅ aeon-postgres-dev (postgres:16-alpine) - Port 5432
- ✅ openspg-network (Docker network) - 172.18.0.0/24
- ✅ 7 existing containers on network

**New Infrastructure (GAP-006 Additions)**:
- Redis container (redis:7-alpine) - ~50MB memory
- Redis Commander (rediscommander/redis-commander) - ~30MB memory
- Worker containers (2-5 replicas) - 256MB each = 512MB-1.28GB total
- **Total New Memory**: ~600MB-1.4GB
- **Total New Storage**: ~500MB (Redis persistence + worker images)

### Time and Cost Summary

| Phase | Duration | Hours | Cost | Key Deliverables |
|-------|----------|-------|------|------------------|
| **Phase 1** | 7 days | 16h | $272 | Redis deployed, environment configured |
| **Phase 2** | 7 days | 20h | $340 | Database schema, migration, access layer |
| **Phase 3** | 7 days | 24h | $408 | Workers, error recovery, health monitoring |
| **Phase 4** | 7 days | 18h | $306 | API endpoints, job management |
| **Phase 5** | 7 days | 20h | $340 | Tests, load testing, validation |
| **Phase 6** | 7 days | 14h | $238 | Production deployment, monitoring |
| **TOTAL** | **42 days** | **112h** | **$1,904** | **Production-ready GAP-006** |

---

## Dependencies and Prerequisites

### Prerequisites Completed ✅
- ✅ aeon-postgres-dev running and healthy
- ✅ openspg-network configured (172.18.0.x)
- ✅ Docker Compose infrastructure operational
- ✅ Next.js application deployed (aeon-saas-dev)
- ✅ GAP-003 (Query Control) complete
- ✅ GAP-001 (Parallel Agent Spawning) operational

### Critical Path Dependencies

```
Phase 1 (Infrastructure)
  └─> Phase 2 (Database Schema)
       └─> Phase 3 (Worker Development)
            └─> Phase 4 (API Integration)
                 └─> Phase 5 (Testing)
                      └─> Phase 6 (Deployment)
```

**Parallel Opportunities**:
- Phase 2 Task 2.4 (Database Access Layer) can start after Task 2.2
- Phase 3 Task 3.2-3.5 can be developed in parallel by different agents
- Phase 4 Task 4.1-4.4 can be developed in parallel
- Phase 5 Task 5.1-5.4 can run concurrently

---

## Risk Management

### High-Priority Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Redis failure in production** | Low | High | AOF persistence, RDB snapshots, health monitoring, automatic restart |
| **Database connection pool exhaustion** | Medium | Medium | Connection pooling (max 10), query optimization, monitoring alerts |
| **Worker crashes under load** | Medium | Low | Auto-restart policy, health checks, resource limits, graceful shutdown |
| **Job duplication during failures** | Low | Medium | Redis BRPOPLPUSH atomic ops, PostgreSQL constraints, idempotent handlers |
| **DLQ accumulation unnoticed** | Medium | Low | Prometheus alerts (>50 jobs), dashboard monitoring, automated triage |
| **Memory leaks in workers** | Low | High | Resource limits (256MB), health monitoring, auto-restart on threshold |
| **Migration rollback complexity** | Low | High | Database backup before migration, rollback script tested, validation checkpoints |

### Disaster Recovery

**Backup Strategy**:
- PostgreSQL: Daily full backups with WAL archiving
- Redis: AOF persistence + daily RDB snapshots
- Job data: 30-day retention, then archived

**Recovery Procedures**:
1. Redis failure: Restart from AOF, workers resume polling
2. Database failure: Restore from backup, replay Redis queue
3. Worker failure: Auto-restart, jobs return to queue after timeout
4. Complete system failure: Restore DB → Restore Redis → Restart workers

---

## Success Metrics

### Key Performance Indicators (KPIs)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Job Submission Latency** | P95 < 100ms | API response time monitoring |
| **Job Execution Start** | P95 < 5s | Time from submit to worker start |
| **Job Completion Rate** | > 95% | (Completed jobs / Total jobs) × 100 |
| **Worker Uptime** | > 99.5% | Heartbeat monitoring over 30 days |
| **DLQ Rate** | < 1% | (DLQ jobs / Total jobs) × 100 |
| **System Throughput** | > 100 jobs/min | Completed jobs per minute sustained |
| **Zero Critical Errors** | 0 | First 2 hours post-deployment |
| **Test Coverage** | > 85% | Jest coverage report |

### Validation Checklist

```yaml
architecture_validation:
  - [ ] All 5 PostgreSQL tables created and indexed
  - [ ] Redis operational on openspg-network
  - [ ] Worker pool deployed (2-5 replicas)
  - [ ] Error recovery with exponential backoff working
  - [ ] Dead letter queue functional
  - [ ] API endpoints responding correctly

performance_validation:
  - [ ] Job submission P95 < 100ms
  - [ ] Worker throughput > 100 jobs/min
  - [ ] Database query latency P95 < 50ms
  - [ ] Redis command latency P95 < 10ms
  - [ ] Load test passing (100 jobs/min sustained)

reliability_validation:
  - [ ] Worker auto-restart working
  - [ ] Job retry after failure verified
  - [ ] DLQ accumulation for max retries confirmed
  - [ ] Redis persistence verified (restart recovery)
  - [ ] Database connection pool recovery tested

monitoring_validation:
  - [ ] Prometheus metrics collecting (if enabled)
  - [ ] Grafana dashboard displaying data (if enabled)
  - [ ] Alert rules firing correctly
  - [ ] Health endpoints responding
  - [ ] Logs aggregating properly

documentation_validation:
  - [ ] Operations runbook complete
  - [ ] Deployment guide ready
  - [ ] Troubleshooting guide available
  - [ ] API documentation published
  - [ ] All docs stored in Qdrant
```

---

## Next Steps After GAP-006

### Immediate (Post-Deployment)
1. Monitor production for 1 week with daily check-ins
2. Address any production issues immediately
3. Optimize worker count based on actual load patterns
4. Fine-tune alert thresholds based on real metrics

### Short-term (1-2 Weeks)
5. Implement advanced job types beyond base handlers
6. Add job dependency chains for complex workflows
7. Implement job scheduling for recurring tasks
8. Add job priority queue optimization

### Medium-term (1 Month)
9. Implement Grafana dashboard for visualization (if not done)
10. Add custom metrics for business-specific KPIs
11. Implement job archival strategy (move old jobs to cold storage)
12. Consider horizontal scaling beyond single server

### Long-term (2-3 Months)
13. Evaluate distributed worker architecture across multiple hosts
14. Consider Redis Cluster for high availability
15. Implement advanced monitoring with distributed tracing
16. Begin GAP-005 (Temporal Tracking) implementation

---

## Appendix A: MCP Tool Mapping

### MCP Tools Used by Phase

**Phase 1: Infrastructure Setup**
- `mcp__claude-flow__swarm_init` - Initialize coordination
- `mcp__claude-flow__agent_spawn` - Spawn infrastructure agents
- `mcp__claude-flow__terminal_execute` - Docker commands
- `mcp__claude-flow__health_check` - Infrastructure validation
- `mcp__claude-flow__config_manage` - Configuration management
- `mcp__claude-flow__memory_usage` - Store setup documentation

**Phase 2: Database Schema**
- `mcp__claude-flow__agent_spawn` - Database development agents
- `mcp__claude-flow__terminal_execute` - Migration execution
- `mcp__claude-flow__bottleneck_analyze` - Performance analysis
- `mcp__claude-flow__daa_optimization` - Query optimization
- `mcp__claude-flow__memory_usage` - Store schema documentation

**Phase 3: Worker Development**
- `mcp__claude-flow__agent_spawn` - Worker development agents
- `mcp__claude-flow__sparc_mode` - SPARC development workflow
- `mcp__claude-flow__daa_fault_tolerance` - Error recovery
- `mcp__claude-flow__swarm_monitor` - Worker health monitoring
- `mcp__claude-flow__agent_metrics` - Performance metrics

**Phase 4: API Integration**
- `mcp__claude-flow__agent_spawn` - API development agents
- `mcp__claude-flow__sparc_mode` - API mode development
- `mcp__claude-flow__memory_usage` - Store API documentation

**Phase 5: Testing & Validation**
- `mcp__claude-flow__agent_spawn` - Testing agents
- `mcp__claude-flow__sparc_mode` - Test mode
- `mcp__claude-flow__benchmark_run` - Load testing
- `mcp__claude-flow__bottleneck_analyze` - Performance analysis
- `mcp__claude-flow__daa_fault_tolerance` - Failure testing

**Phase 6: Deployment**
- `mcp__claude-flow__terminal_execute` - Deployment commands
- `mcp__claude-flow__health_check` - Production validation
- `mcp__claude-flow__diagnostic_run` - System diagnostics
- `mcp__claude-flow__swarm_monitor` - Production monitoring
- `mcp__claude-flow__config_manage` - Configuration
- `mcp__claude-flow__memory_usage` - Store production docs

---

## Appendix B: File Locations

```
/home/jim/2_OXOT_Projects_Dev/
├── docs/
│   ├── GAP-006_ARCHITECTURE_DESIGN_2025-11-15.md (EXISTING)
│   ├── GAP-006_IMPLEMENTATION_ROADMAP_2025-11-15.md (THIS FILE)
│   └── GAP-006_PREPARATION_COMPLETE_2025-11-15.md (TO BE CREATED)
│
└── Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/
    ├── docker-compose.dev.yml (EXISTING - No changes)
    ├── docker-compose.redis.yml (UPDATE - Task 1.1)
    ├── docker-compose.workers.yml (NEW - Task 6.2)
    │
    ├── .env (UPDATE - Task 1.4)
    │
    ├── config/
    │   └── redis.conf (NEW - Task 1.3)
    │
    ├── scripts/
    │   └── migrations/
    │       └── 001_gap006_job_tables.sql (NEW - Task 2.1)
    │
    ├── app/api/jobs/
    │   ├── route.ts (NEW - Tasks 4.1, 4.2)
    │   ├── [id]/route.ts (NEW - Tasks 4.2, 4.3)
    │   └── metrics/route.ts (NEW - Task 4.4)
    │
    ├── lib/
    │   ├── job-repository.ts (NEW - Task 2.4)
    │   └── redis.ts (NEW - Task 3.2)
    │
    └── workers/
        ├── Dockerfile (NEW - Task 3.1)
        ├── package.json (NEW - Task 3.1)
        ├── tsconfig.json (NEW - Task 3.1)
        ├── .dockerignore (NEW - Task 3.1)
        └── src/
            ├── index.ts (NEW - Task 3.2)
            ├── core/
            │   ├── worker.ts (NEW - Task 3.2)
            │   ├── job-executor.ts (NEW - Task 3.3)
            │   ├── error-handler.ts (NEW - Task 3.4)
            │   └── health-monitor.ts (NEW - Task 3.5)
            ├── handlers/
            │   ├── base-handler.ts (NEW - Task 3.3)
            │   ├── email-notification-handler.ts (NEW - Task 3.3)
            │   └── index.ts (NEW - Task 3.3)
            ├── services/
            │   ├── postgres.ts (NEW - Task 2.4)
            │   ├── redis.ts (NEW - Task 3.2)
            │   └── metrics.ts (NEW - Task 3.5)
            ├── config/
            │   ├── worker-config.ts (NEW - Task 3.1)
            │   └── retry-config.ts (NEW - Task 3.4)
            └── tests/
                ├── unit/ (NEW - Task 5.1)
                ├── integration/ (NEW - Task 5.2)
                └── load/ (NEW - Task 5.3)
```

---

## Appendix C: Quick Reference Commands

### Development Commands
```bash
# Build workers
cd workers && npm run build

# Run workers locally
cd workers && npm run dev

# Run tests
cd workers && npm test

# Run linter
cd workers && npm run lint
```

### Docker Commands
```bash
# Start Redis
docker-compose -f docker-compose.redis.yml up -d

# Deploy workers (3 replicas)
docker-compose -f docker-compose.workers.yml up -d --scale aeon-worker=3

# View worker logs
docker-compose -f docker-compose.workers.yml logs -f aeon-worker

# Check worker health
docker ps --filter "name=aeon-worker" --format "{{.Names}} - {{.Status}}"

# Restart workers
docker-compose -f docker-compose.workers.yml restart
```

### Database Commands
```bash
# Run migration
docker exec -i aeon-postgres-dev psql -U postgres -d aeon_saas_dev < scripts/migrations/001_gap006_job_tables.sql

# Verify tables
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "\dt job*"

# Check job counts
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "SELECT status, COUNT(*) FROM jobs GROUP BY status;"

# View DLQ jobs
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "SELECT * FROM dead_letter_jobs ORDER BY created_at DESC LIMIT 10;"
```

### Redis Commands
```bash
# Check Redis connection
docker exec aeon-redis redis-cli -a aeon_redis_dev PING

# View queue depths
docker exec aeon-redis redis-cli -a aeon_redis_dev LLEN job:queue:pending
docker exec aeon-redis redis-cli -a aeon_redis_dev LLEN job:queue:processing

# View worker heartbeats
docker exec aeon-redis redis-cli -a aeon_redis_dev KEYS "worker:heartbeat:*"

# Clear queue (DANGER - use only in dev)
docker exec aeon-redis redis-cli -a aeon_redis_dev DEL job:queue:pending
```

### API Commands
```bash
# Submit a job
curl -X POST http://localhost:3000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"job_type":"test_job","payload":{"message":"hello"}}'

# Get job status
curl http://localhost:3000/api/jobs/{job_id}

# List jobs
curl "http://localhost:3000/api/jobs?status=pending&limit=10"

# Get metrics
curl http://localhost:3000/api/jobs/metrics

# Cancel job
curl -X DELETE http://localhost:3000/api/jobs/{job_id}
```

### Monitoring Commands
```bash
# View Prometheus metrics (if enabled)
curl http://localhost:9090/metrics

# Check worker health
curl http://localhost:9090/health

# View Grafana dashboard (if enabled)
# Open: http://localhost:3001
```

---

**END OF ROADMAP**

**Next Action**: Proceed to Phase 1, Task 1.1 (Update Redis Docker Configuration)

**Status**: ✅ READY FOR EXECUTION
**Last Updated**: 2025-11-15 16:45:00 UTC
**Version**: v1.0.0
