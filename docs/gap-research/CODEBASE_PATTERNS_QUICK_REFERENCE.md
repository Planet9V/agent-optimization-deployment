# Codebase Patterns Quick Reference
## GAP-003 Query Control Implementation Guide

**Quick Ref**: CODEBASE_PATTERNS_QUICK_REFERENCE.md
**Created**: 2025-11-13
**Use Case**: Fast lookup for reusable patterns during GAP-003 implementation

---

## 🎯 Pattern Lookup Table

| Need | Pattern Location | Reuse Level | Adaptation |
|------|-----------------|-------------|------------|
| **Parallel execution** | `lib/orchestration/parallel-agent-spawner.ts:296` | 🟢 95% | Query stage mapping |
| **Multi-level cache** | `lib/agentdb/agent-db.ts:76` | 🟢 90% | Query result schema |
| **Progress polling** | `app/components/upload/ProcessingStatus.tsx:14` | 🟡 80% | Query status endpoint |
| **Two-phase validation** | `app/api/upload/route.ts:295` | 🟡 75% | Query validation rules |
| **Dependency resolution** | `lib/orchestration/parallel-agent-spawner.ts:147` | 🟢 85% | Query stage deps |
| **Metrics tracking** | `lib/agentdb/agent-db.ts:486` | 🟢 90% | Query metrics schema |
| **TTL eviction** | `lib/agentdb/agent-db.ts:390` | 🟢 90% | Checkpoint TTL |
| **Result aggregation** | `app/api/upload/route.ts:331` | 🟢 90% | Query result collection |

**Legend**: 🟢 High reuse | 🟡 Medium reuse | 🔴 Low reuse

---

## 📦 Copy-Paste Patterns

### 1. Parallel Execution with Error Handling

```typescript
// SOURCE: lib/orchestration/parallel-agent-spawner.ts:295-340
// USE CASE: Execute query stages in parallel

async function executeQueryStagesParallel(
  stages: QueryStage[]
): Promise<{ successes: Result[]; failures: Error[] }> {

  // Execute all stages in parallel
  const results = await Promise.allSettled(
    stages.map(stage => this.executeStage(stage))
  );

  // Separate successes and failures
  const successes: Result[] = [];
  const failures: Error[] = [];

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      successes.push(result.value);
    } else {
      failures.push({
        stageId: stages[index].id,
        error: result.reason.message || 'Unknown error'
      });
    }
  });

  return { successes, failures };
}
```

**Adaptation needed**:
- Replace `QueryStage` with your stage type
- Implement `executeStage()` method
- Add checkpoint creation after each stage

---

### 2. Multi-Level Caching (L1 + L2)

```typescript
// SOURCE: lib/agentdb/agent-db.ts:76-120, 208-298
// USE CASE: Cache query results and checkpoints

import { LRUCache } from 'lru-cache';

class QueryCache {
  private l1Cache: LRUCache<string, QueryResult>;
  private l2Client: QdrantClient;

  constructor(options: CacheOptions) {
    // L1: In-memory LRU cache (fast, volatile)
    this.l1Cache = new LRUCache({
      max: options.l1Size || 1000,
      ttl: options.l1TTL || 3600000,  // 1 hour
      updateAgeOnGet: true,
      updateAgeOnHas: true
    });

    // L2: Qdrant vector database (slower, persistent)
    this.l2Client = new QdrantClient({
      url: options.qdrantUrl,
      collectionName: 'query-checkpoints'
    });
  }

  async get(queryId: string): Promise<QueryResult | null> {
    // Try L1 first (0.1-2ms)
    if (this.l1Cache.has(queryId)) {
      console.log('L1 cache HIT:', queryId);
      return this.l1Cache.get(queryId)!;
    }

    // Try L2 (5-10ms)
    const l2Result = await this.l2Client.get(queryId);
    if (l2Result) {
      console.log('L2 cache HIT:', queryId);
      // Promote to L1
      this.l1Cache.set(queryId, l2Result);
      return l2Result;
    }

    console.log('Cache MISS:', queryId);
    return null;
  }

  async set(queryId: string, result: QueryResult): Promise<void> {
    // Store in both L1 and L2
    this.l1Cache.set(queryId, result);
    await this.l2Client.store(queryId, result);
  }

  async delete(queryId: string): Promise<void> {
    this.l1Cache.delete(queryId);
    await this.l2Client.delete(queryId);
  }
}
```

**Adaptation needed**:
- Define `QueryResult` type
- Configure Qdrant collection for checkpoints
- Add TTL-based eviction (see pattern #6)

---

### 3. Progress Polling with Completion Detection

```typescript
// SOURCE: app/components/upload/ProcessingStatus.tsx:13-26
// USE CASE: Monitor query execution progress in UI

function useQueryProgress(queryIds: string[]) {
  const [statuses, setStatuses] = useState<QueryStatus[]>([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      // Fetch status for all queries
      const results = await Promise.all(
        queryIds.map(id =>
          fetch(`/api/query/status/${id}`).then(r => r.json())
        )
      );

      setStatuses(results);

      // Stop polling when all queries complete
      if (results.every(r => r.state === 'COMPLETED' || r.state === 'FAILED')) {
        clearInterval(interval);
      }
    }, 2000);  // 2-second polling interval

    return () => clearInterval(interval);
  }, [queryIds]);

  return statuses;
}
```

**Adaptation needed**:
- Implement `/api/query/status/:id` endpoint
- Define `QueryStatus` type with state field
- Consider WebSocket/SSE for real-time updates (optional)

---

### 4. Two-Phase Validation Pattern

```typescript
// SOURCE: app/api/upload/route.ts:295-325
// USE CASE: Validate query before execution

async function executeQuery(
  query: QueryRequest
): Promise<QueryResponse> {

  // PHASE 1: Validate all stages in parallel
  const validations = await Promise.allSettled(
    query.stages.map(stage => this.validateStage(stage))
  );

  // Check for validation failures
  const validationFailures = validations.filter(r => r.status === 'rejected');
  if (validationFailures.length > 0) {
    const errors = validationFailures.map((r: any) => r.reason.message);
    throw new Error(`Validation failed: ${errors.join(', ')}`);
  }

  // Extract validated stages
  const validatedStages = validations
    .filter((r): r is PromiseFulfilledResult<Stage> => r.status === 'fulfilled')
    .map(r => r.value);

  // PHASE 2: Execute validated stages in parallel
  const executions = await Promise.allSettled(
    validatedStages.map(stage => this.executeStage(stage))
  );

  // Aggregate results
  return this.aggregateResults(executions);
}
```

**Adaptation needed**:
- Implement `validateStage()` method
- Define validation rules for query stages
- Add checkpoint creation between phases

---

### 5. Dependency-Aware Batching

```typescript
// SOURCE: lib/orchestration/parallel-agent-spawner.ts:147-191
// USE CASE: Execute query stages respecting dependencies

function createDependencyBatches(
  stages: QueryStage[],
  batchSize: number
): QueryStage[][] {
  const batches: QueryStage[][] = [];
  const processed = new Set<string>();

  // Topological sort by dependencies
  const sortedStages: QueryStage[] = [];
  const queue = stages.filter(s =>
    !s.dependencies || s.dependencies.length === 0
  );

  while (queue.length > 0) {
    const stage = queue.shift()!;

    if (!processed.has(stage.id)) {
      sortedStages.push(stage);
      processed.add(stage.id);

      // Find stages that depend on this one
      stages.forEach(s => {
        if (s.dependencies?.includes(stage.id)) {
          const allDepsSatisfied = s.dependencies.every(dep =>
            processed.has(dep)
          );
          if (allDepsSatisfied && !processed.has(s.id)) {
            queue.push(s);
          }
        }
      });
    }
  }

  // Group into batches (parallel within, sequential between)
  for (let i = 0; i < sortedStages.length; i += batchSize) {
    batches.push(sortedStages.slice(i, i + batchSize));
  }

  return batches;
}

async function executeBatches(batches: QueryStage[][]) {
  const allResults = [];

  for (let i = 0; i < batches.length; i++) {
    const batch = batches[i];

    // Execute batch in parallel
    const batchResults = await Promise.allSettled(
      batch.map(stage => this.executeStage(stage))
    );

    allResults.push(...batchResults);

    // Coordination window between batches
    if (i < batches.length - 1) {
      await this.sleep(50);  // 50ms pause
    }
  }

  return allResults;
}
```

**Adaptation needed**:
- Add `dependencies` field to `QueryStage` type
- Implement cycle detection for dependency graph
- Add checkpoint creation after each batch

---

### 6. TTL-Based Eviction with Hot/Warm/Cold Tiers

```typescript
// SOURCE: lib/agentdb/agent-db.ts:30-34, 390-397
// USE CASE: Automatic checkpoint cleanup

interface TTLTier {
  name: 'hot' | 'warm' | 'cold';
  ttl_days: number;
  access_threshold: number;
}

class CheckpointManager {
  private readonly ttlTiers: TTLTier[] = [
    { name: 'hot', ttl_days: 7, access_threshold: 100 },   // Frequently accessed
    { name: 'warm', ttl_days: 3, access_threshold: 10 },   // Occasionally accessed
    { name: 'cold', ttl_days: 1, access_threshold: 0 }      // Rarely accessed
  ];

  calculateTTL(accessCount: number): number {
    for (const tier of this.ttlTiers) {
      if (accessCount >= tier.access_threshold) {
        return tier.ttl_days * 24 * 60 * 60 * 1000;  // Convert to milliseconds
      }
    }
    return 24 * 60 * 60 * 1000;  // Default: 1 day
  }

  async createCheckpoint(query: Query): Promise<void> {
    const ttl = this.calculateTTL(query.accessCount);

    const checkpoint = {
      queryId: query.id,
      state: query.state,
      data: query.data,
      created_at: Date.now(),
      ttl_expires: Date.now() + ttl,
      access_count: query.accessCount
    };

    await this.storage.store(checkpoint);
  }

  async updateAccessMetrics(queryId: string): Promise<void> {
    const checkpoint = await this.storage.get(queryId);

    checkpoint.access_count++;
    checkpoint.ttl_expires = Date.now() + this.calculateTTL(checkpoint.access_count);

    await this.storage.update(checkpoint);
  }
}
```

**Adaptation needed**:
- Adjust TTL tiers based on query patterns
- Implement background cleanup job for expired checkpoints
- Add access tracking to query lifecycle

---

### 7. Metrics Collection

```typescript
// SOURCE: lib/agentdb/agent-db.ts:486-523
// USE CASE: Track query performance metrics

interface QueryMetrics {
  total_queries: number;
  completed_queries: number;
  failed_queries: number;
  success_rate: number;
  avg_execution_time_ms: number;
  p50_latency_ms: number;
  p99_latency_ms: number;
  checkpoint_hits: number;
  checkpoint_misses: number;
  last_reset: number;
  uptime_ms: number;
}

class QueryMetricsTracker {
  private metrics: QueryMetrics;
  private latencies: number[] = [];

  recordQueryStart(): void {
    this.metrics.total_queries++;
  }

  recordQueryComplete(duration: number, success: boolean): void {
    if (success) {
      this.metrics.completed_queries++;
    } else {
      this.metrics.failed_queries++;
    }

    // Track latency
    this.latencies.push(duration);
    if (this.latencies.length > 1000) {
      this.latencies.shift();  // Keep last 1000 measurements
    }

    // Update metrics
    this.updateStats();
  }

  recordCheckpointHit(): void {
    this.metrics.checkpoint_hits++;
    this.updateStats();
  }

  recordCheckpointMiss(): void {
    this.metrics.checkpoint_misses++;
    this.updateStats();
  }

  private updateStats(): void {
    this.metrics.success_rate =
      this.metrics.completed_queries / this.metrics.total_queries;

    this.metrics.avg_execution_time_ms =
      this.latencies.reduce((a, b) => a + b, 0) / this.latencies.length;

    const sorted = [...this.latencies].sort((a, b) => a - b);
    this.metrics.p50_latency_ms = sorted[Math.floor(sorted.length * 0.5)];
    this.metrics.p99_latency_ms = sorted[Math.floor(sorted.length * 0.99)];

    this.metrics.uptime_ms = Date.now() - this.metrics.last_reset;
  }

  getMetrics(): QueryMetrics {
    return { ...this.metrics };
  }

  reset(): void {
    this.metrics = {
      total_queries: 0,
      completed_queries: 0,
      failed_queries: 0,
      success_rate: 0,
      avg_execution_time_ms: 0,
      p50_latency_ms: 0,
      p99_latency_ms: 0,
      checkpoint_hits: 0,
      checkpoint_misses: 0,
      last_reset: Date.now(),
      uptime_ms: 0
    };
    this.latencies = [];
  }
}
```

**Adaptation needed**:
- Add query-specific metrics (e.g., model switch count)
- Implement metrics export to monitoring system
- Add percentile calculations (p95, p99.9)

---

### 8. Result Aggregation with HTTP Status Codes

```typescript
// SOURCE: app/api/upload/route.ts:331-381
// USE CASE: Return partial success/failure for query stages

async function handleQueryExecution(
  stages: QueryStage[]
): Promise<Response> {

  const results = await Promise.allSettled(
    stages.map(stage => this.executeStage(stage))
  );

  const successes: StageResult[] = [];
  const failures: StageError[] = [];

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      successes.push(result.value);
    } else {
      failures.push({
        stageId: stages[index].id,
        error: result.reason.message || 'Unknown error'
      });
    }
  });

  // Determine HTTP status based on results
  if (failures.length === 0) {
    // All succeeded - HTTP 200
    return Response.json({
      success: true,
      results: successes,
      count: successes.length
    }, { status: 200 });

  } else if (successes.length === 0) {
    // All failed - HTTP 500
    return Response.json({
      success: false,
      error: 'All stages failed',
      failures
    }, { status: 500 });

  } else {
    // Partial success - HTTP 207 Multi-Status
    return Response.json({
      success: false,
      partialSuccess: true,
      results: successes,
      failures,
      successCount: successes.length,
      failureCount: failures.length
    }, { status: 207 });
  }
}
```

**Adaptation needed**:
- Define `StageResult` and `StageError` types
- Add checkpoint creation for partial success scenarios
- Implement retry logic for failed stages

---

## 🚫 Anti-Patterns to Avoid

### ❌ Don't: Sequential Execution When Parallel is Possible

```typescript
// BAD: Sequential execution
for (const stage of stages) {
  await executeStage(stage);  // Blocks on each stage
}

// GOOD: Parallel execution
const results = await Promise.allSettled(
  stages.map(stage => executeStage(stage))
);
```

---

### ❌ Don't: Ignore Partial Failures

```typescript
// BAD: All-or-nothing
const results = await Promise.all(stages.map(executeStage));

// GOOD: Handle partial success
const results = await Promise.allSettled(stages.map(executeStage));
const successes = results.filter(r => r.status === 'fulfilled');
const failures = results.filter(r => r.status === 'rejected');
```

---

### ❌ Don't: Skip Validation Phase

```typescript
// BAD: Execute without validation
const results = await executeStages(stages);

// GOOD: Two-phase validation + execution
const validated = await validateStages(stages);
const results = await executeStages(validated);
```

---

### ❌ Don't: Fixed Polling Intervals

```typescript
// BAD: Fixed 2-second polling
setInterval(() => fetchStatus(), 2000);

// BETTER: Adaptive polling (fast → slow)
let interval = 500;  // Start fast
const maxInterval = 5000;  // Max 5 seconds

const poll = async () => {
  const status = await fetchStatus();

  if (status.complete) return;

  // Slow down polling over time
  interval = Math.min(interval * 1.2, maxInterval);
  setTimeout(poll, interval);
};
```

---

### ❌ Don't: Skip Checkpoint Creation

```typescript
// BAD: No intermediate state saving
const results = await longRunningQuery();

// GOOD: Checkpoint after each stage
for (const stage of stages) {
  const result = await executeStage(stage);
  await createCheckpoint({ stage, result });  // Save progress
}
```

---

## 📊 Performance Targets

| Pattern | Current Performance | Target Performance | Notes |
|---------|-------------------|-------------------|-------|
| **Parallel execution** | 15-37x speedup | Maintain | Proven in GAP-001 |
| **Multi-level cache** | 150-12,500x speedup | Maintain | Proven in GAP-002 |
| **Checkpoint creation** | N/A | <15ms overhead | New feature |
| **Checkpoint resume** | N/A | <10ms penalty | New feature |
| **Model switching** | N/A | <20ms switch | New feature |
| **State transition** | N/A | <5ms latency | New feature |

---

## 🔧 Adaptation Checklist

When adapting a pattern, ensure:

- [ ] Type definitions updated for query domain
- [ ] Error handling preserved from source
- [ ] Metrics collection added
- [ ] Checkpoint creation integrated
- [ ] Tests written (unit + integration)
- [ ] Performance benchmarked
- [ ] Documentation updated

---

## 📚 Full Documentation

For detailed analysis, see:
- **Complete Analysis**: `docs/CODEBASE_ANALYSIS_QUERY_CONTROL_PATTERNS.md`
- **Executive Summary**: `docs/gap-research/CODEBASE_ANALYSIS_EXECUTIVE_SUMMARY.md`

---

**Quick Ref Version**: 1.0
**Last Updated**: 2025-11-13
**Next Review**: After GAP-003 Phase 1 implementation

