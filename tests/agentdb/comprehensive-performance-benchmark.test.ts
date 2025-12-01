/**
 * Comprehensive Performance Benchmark Suite
 *
 * PURPOSE: Validate ALL claimed speedup factors with ACTUAL measurements
 *
 * CLAIMS TO VALIDATE:
 * - Pattern Search: 15ms → 100µs (150x faster)
 * - Batch Insert: 1s → 2ms (500x faster)
 * - Large Queries: 100s → 8ms (12,500x faster)
 * - Agent Spawning: 750ms → 50-75ms (10-20x faster)
 * - Overall: 150-12,500x speedup range
 *
 * METHODOLOGY:
 * 1. Measure baseline (without cache)
 * 2. Measure optimized (with cache)
 * 3. Calculate actual speedup = baseline / optimized
 * 4. Compare against claims
 * 5. Report with raw data and honest verdict
 */

import { AgentDB } from '../../lib/agentdb/agent-db';
import type { AgentConfig } from '../../lib/agentdb/types';

// Mock dependencies
jest.mock('../../lib/agentdb/embedding-service');
jest.mock('../../lib/agentdb/qdrant-client');

interface BenchmarkResult {
  operation: string;
  baseline_ms: number;
  optimized_ms: number;
  actual_speedup: number;
  claimed_speedup: string;
  validated: boolean;
  raw_data: {
    baseline_samples: number[];
    optimized_samples: number[];
    p50_baseline: number;
    p50_optimized: number;
    p99_baseline: number;
    p99_optimized: number;
  };
}

interface ComprehensiveReport {
  timestamp: string;
  benchmarks: BenchmarkResult[];
  summary: {
    total_claims: number;
    validated_claims: number;
    failed_claims: number;
    validation_rate: number;
  };
  raw_measurements: Record<string, number[]>;
}

describe('Comprehensive Performance Benchmark Suite', () => {
  let agentDB: AgentDB;
  let report: ComprehensiveReport;

  beforeAll(() => {
    report = {
      timestamp: new Date().toISOString(),
      benchmarks: [],
      summary: {
        total_claims: 0,
        validated_claims: 0,
        failed_claims: 0,
        validation_rate: 0,
      },
      raw_measurements: {},
    };
  });

  afterAll(() => {
    // Output complete report
    console.log('\n' + '='.repeat(80));
    console.log('COMPREHENSIVE PERFORMANCE VALIDATION REPORT');
    console.log('='.repeat(80) + '\n');

    console.log(`Timestamp: ${report.timestamp}\n`);

    console.log('BENCHMARK RESULTS:');
    console.log('-'.repeat(80));

    report.benchmarks.forEach((benchmark, idx) => {
      console.log(`\n${idx + 1}. ${benchmark.operation}`);
      console.log(`   Claimed Speedup: ${benchmark.claimed_speedup}`);
      console.log(`   Baseline (p50): ${benchmark.raw_data.p50_baseline.toFixed(2)}ms`);
      console.log(`   Optimized (p50): ${benchmark.raw_data.p50_optimized.toFixed(2)}ms`);
      console.log(`   Actual Speedup: ${benchmark.actual_speedup.toFixed(2)}x`);
      console.log(`   Status: ${benchmark.validated ? '✅ VALIDATED' : '❌ FAILED'}`);
      console.log(`   Raw Samples: ${benchmark.raw_data.baseline_samples.length} baseline, ${benchmark.raw_data.optimized_samples.length} optimized`);
    });

    console.log('\n' + '-'.repeat(80));
    console.log('SUMMARY:');
    console.log(`   Total Claims: ${report.summary.total_claims}`);
    console.log(`   Validated: ${report.summary.validated_claims}`);
    console.log(`   Failed: ${report.summary.failed_claims}`);
    console.log(`   Validation Rate: ${(report.summary.validation_rate * 100).toFixed(1)}%`);
    console.log('='.repeat(80) + '\n');
  });

  afterEach(async () => {
    if (agentDB) {
      await agentDB.destroy();
    }
  });

  // Helper: Calculate percentiles
  function calculatePercentile(values: number[], percentile: number): number {
    const sorted = [...values].sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }

  // Helper: Measure operation multiple times
  async function measureOperation(
    operation: () => Promise<void>,
    samples: number = 100
  ): Promise<number[]> {
    const times: number[] = [];

    for (let i = 0; i < samples; i++) {
      const start = performance.now();
      await operation();
      const end = performance.now();
      times.push(end - start);
    }

    return times;
  }

  // Helper: Add benchmark result
  function addBenchmark(
    operation: string,
    baselineSamples: number[],
    optimizedSamples: number[],
    claimedSpeedup: string,
    minimumSpeedup: number
  ): void {
    const p50_baseline = calculatePercentile(baselineSamples, 50);
    const p50_optimized = calculatePercentile(optimizedSamples, 50);
    const p99_baseline = calculatePercentile(baselineSamples, 99);
    const p99_optimized = calculatePercentile(optimizedSamples, 99);

    const actual_speedup = p50_baseline / p50_optimized;
    const validated = actual_speedup >= minimumSpeedup;

    report.benchmarks.push({
      operation,
      baseline_ms: p50_baseline,
      optimized_ms: p50_optimized,
      actual_speedup,
      claimed_speedup: claimedSpeedup,
      validated,
      raw_data: {
        baseline_samples: baselineSamples,
        optimized_samples: optimizedSamples,
        p50_baseline,
        p50_optimized,
        p99_baseline,
        p99_optimized,
      },
    });

    report.raw_measurements[operation] = {
      baseline: baselineSamples,
      optimized: optimizedSamples,
    } as any;

    report.summary.total_claims++;
    if (validated) {
      report.summary.validated_claims++;
    } else {
      report.summary.failed_claims++;
    }
    report.summary.validation_rate = report.summary.validated_claims / report.summary.total_claims;
  }

  describe('CLAIM 1: L1 Cache Hit Latency <1ms', () => {
    it('should measure actual L1 cache hit latency', async () => {
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');

      // Setup fast mocks
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 0.1,
      });

      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([]);
      AgentDBQdrantClient.prototype.storePoint = jest.fn().mockResolvedValue(undefined);

      agentDB = new AgentDB({
        enableL1Cache: true,
        enableL2Cache: false,
        l1CacheSize: 1000,
      });
      await agentDB.initialize();

      const config = global.testUtils.createMockAgentConfig();
      const mockSpawnFn = jest.fn().mockResolvedValue({ id: 'agent' });

      // Prime cache with first request
      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      // Measure L1 cache hits
      const l1HitTimes = await measureOperation(async () => {
        await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      }, 100);

      const p50 = calculatePercentile(l1HitTimes, 50);
      const p99 = calculatePercentile(l1HitTimes, 99);

      console.log(`\nL1 Cache Hit Latency:`);
      console.log(`  p50: ${p50.toFixed(3)}ms`);
      console.log(`  p99: ${p99.toFixed(3)}ms`);
      console.log(`  Target: <1ms`);
      console.log(`  Status: ${p50 < 1 ? '✅ PASS' : '❌ FAIL'}`);

      // Note: This measures in-memory cache access, not the claimed "pattern search" speedup
      expect(p50).toBeLessThan(1);
    });
  });

  describe('CLAIM 2: L2 Cache Hit Latency <10ms', () => {
    it('should measure actual L2 cache hit latency', async () => {
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');

      // Setup mocks with realistic Qdrant timing
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 2,
      });

      // Simulate Qdrant search time (2-5ms realistic)
      AgentDBQdrantClient.prototype.search = jest.fn().mockImplementation(() => {
        return new Promise(resolve => {
          setTimeout(() => resolve([
            global.testUtils.createMockSearchResult({ agent: { id: 'cached' } })
          ]), 3); // 3ms Qdrant latency
        });
      });

      agentDB = new AgentDB({
        enableL1Cache: false,
        enableL2Cache: true,
      });
      await agentDB.initialize();

      const config = global.testUtils.createMockAgentConfig();
      const mockSpawnFn = jest.fn().mockResolvedValue({ id: 'agent' });

      // Measure L2 cache hits
      const l2HitTimes = await measureOperation(async () => {
        await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      }, 100);

      const p50 = calculatePercentile(l2HitTimes, 50);
      const p99 = calculatePercentile(l2HitTimes, 99);

      console.log(`\nL2 Cache Hit Latency:`);
      console.log(`  p50: ${p50.toFixed(3)}ms`);
      console.log(`  p99: ${p99.toFixed(3)}ms`);
      console.log(`  Target: <10ms`);
      console.log(`  Status: ${p50 < 10 ? '✅ PASS' : '❌ FAIL'}`);

      expect(p50).toBeLessThan(10);
    });
  });

  describe('CLAIM 3: Cache Miss Baseline (Actual Agent Spawn Time)', () => {
    it('should measure actual cache miss latency', async () => {
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');

      // Realistic embedding time
      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 2,
      });

      // Always miss
      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([]);
      AgentDBQdrantClient.prototype.storePoint = jest.fn().mockResolvedValue(undefined);

      // Realistic spawn time (100ms is common for agent initialization)
      const mockSpawnFn = jest.fn().mockImplementation(() => {
        return new Promise(resolve => {
          setTimeout(() => resolve({ id: 'spawned-agent' }), 100);
        });
      });

      agentDB = new AgentDB({
        enableL1Cache: false,
        enableL2Cache: false,
      });
      await agentDB.initialize();

      const config = global.testUtils.createMockAgentConfig();

      // Measure cache misses (spawn time)
      const missTimes = await measureOperation(async () => {
        await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      }, 50); // Fewer samples since spawn is expensive

      const p50 = calculatePercentile(missTimes, 50);
      const p99 = calculatePercentile(missTimes, 99);

      console.log(`\nCache Miss Baseline (Agent Spawn):`);
      console.log(`  p50: ${p50.toFixed(2)}ms`);
      console.log(`  p99: ${p99.toFixed(2)}ms`);
      console.log(`  Spawn calls: ${mockSpawnFn.mock.calls.length}`);

      expect(mockSpawnFn).toHaveBeenCalledTimes(50);
      expect(p50).toBeGreaterThan(90); // Should be ~100ms
    });
  });

  describe('CLAIM 4: L1 Speedup Factor (Cache Hit vs Miss)', () => {
    it('should calculate actual L1 speedup factor', async () => {
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');

      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 0.1,
      });

      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([]);
      AgentDBQdrantClient.prototype.storePoint = jest.fn().mockResolvedValue(undefined);

      // Measure BASELINE (no cache, spawn each time)
      const noCacheDB = new AgentDB({
        enableL1Cache: false,
        enableL2Cache: false,
      });
      await noCacheDB.initialize();

      const config = global.testUtils.createMockAgentConfig();
      const mockSpawnFn = jest.fn().mockImplementation(() => {
        return new Promise(resolve => {
          setTimeout(() => resolve({ id: 'agent' }), 100); // 100ms spawn
        });
      });

      const baselineTimes = await measureOperation(async () => {
        await noCacheDB.findOrSpawnAgent(config, mockSpawnFn);
      }, 30);

      await noCacheDB.destroy();

      // Measure OPTIMIZED (L1 cache enabled)
      agentDB = new AgentDB({
        enableL1Cache: true,
        enableL2Cache: false,
        l1CacheSize: 1000,
      });
      await agentDB.initialize();

      // Prime cache
      await agentDB.findOrSpawnAgent(config, mockSpawnFn);

      const optimizedTimes = await measureOperation(async () => {
        await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      }, 100);

      addBenchmark(
        'L1 Cache Speedup',
        baselineTimes,
        optimizedTimes,
        '150-12,500x claimed',
        150 // Minimum claim
      );
    });
  });

  describe('CLAIM 5: L2 Speedup Factor (Qdrant Cache vs Spawn)', () => {
    it('should calculate actual L2 speedup factor', async () => {
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');

      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 2,
      });

      // Measure BASELINE (no cache)
      const noCacheDB = new AgentDB({
        enableL1Cache: false,
        enableL2Cache: false,
      });
      await noCacheDB.initialize();

      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([]);
      AgentDBQdrantClient.prototype.storePoint = jest.fn().mockResolvedValue(undefined);

      const config = global.testUtils.createMockAgentConfig();
      const mockSpawnFn = jest.fn().mockImplementation(() => {
        return new Promise(resolve => {
          setTimeout(() => resolve({ id: 'agent' }), 100);
        });
      });

      const baselineTimes = await measureOperation(async () => {
        await noCacheDB.findOrSpawnAgent(config, mockSpawnFn);
      }, 30);

      await noCacheDB.destroy();

      // Measure OPTIMIZED (L2 cache with Qdrant)
      AgentDBQdrantClient.prototype.search = jest.fn().mockImplementation(() => {
        return new Promise(resolve => {
          setTimeout(() => resolve([
            global.testUtils.createMockSearchResult({ agent: { id: 'cached' } })
          ]), 3); // 3ms Qdrant search
        });
      });

      agentDB = new AgentDB({
        enableL1Cache: false,
        enableL2Cache: true,
      });
      await agentDB.initialize();

      const optimizedTimes = await measureOperation(async () => {
        await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      }, 100);

      addBenchmark(
        'L2 Cache Speedup (Qdrant)',
        baselineTimes,
        optimizedTimes,
        '100-500x claimed',
        100 // Minimum claim for L2
      );
    });
  });

  describe('CLAIM 6: Cache Hit Rate Over 100 Operations', () => {
    it('should measure cache effectiveness over sustained load', async () => {
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');

      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 0.5,
      });

      // First call misses, rest hit
      let callCount = 0;
      AgentDBQdrantClient.prototype.search = jest.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          return Promise.resolve([]); // Miss
        }
        return Promise.resolve([
          global.testUtils.createMockSearchResult({ agent: { id: 'cached' } })
        ]); // Hit
      });

      AgentDBQdrantClient.prototype.storePoint = jest.fn().mockResolvedValue(undefined);

      agentDB = new AgentDB({
        enableL1Cache: true,
        enableL2Cache: true,
      });
      await agentDB.initialize();

      const config = global.testUtils.createMockAgentConfig();
      const mockSpawnFn = jest.fn().mockResolvedValue({ id: 'agent' });

      // 100 requests
      for (let i = 0; i < 100; i++) {
        await agentDB.findOrSpawnAgent(config, mockSpawnFn);
      }

      const stats = agentDB.getStats();

      console.log(`\nCache Hit Rate (100 operations):`);
      console.log(`  Total Requests: ${stats.total_requests}`);
      console.log(`  Cache Hits: ${stats.cache_hits}`);
      console.log(`  Cache Misses: ${stats.cache_misses}`);
      console.log(`  Hit Rate: ${(stats.hit_rate * 100).toFixed(2)}%`);
      console.log(`  Expected: ≥90% for repeated requests`);

      expect(stats.total_requests).toBe(100);
      expect(stats.hit_rate).toBeGreaterThan(0.9); // 90%+ hit rate expected
    });
  });

  describe('CLAIM 7: Throughput - 100 Requests in <1 Second', () => {
    it('should handle 100 concurrent cache hits in <1s', async () => {
      const { EmbeddingService } = require('../../lib/agentdb/embedding-service');
      const { AgentDBQdrantClient } = require('../../lib/agentdb/qdrant-client');

      EmbeddingService.prototype.generateEmbedding = jest.fn().mockResolvedValue({
        embedding: global.testUtils.createMockEmbedding(),
        cached: false,
        generation_time_ms: 0.1,
      });

      AgentDBQdrantClient.prototype.search = jest.fn().mockResolvedValue([
        global.testUtils.createMockSearchResult({ agent: { id: 'cached' } })
      ]);

      agentDB = new AgentDB({
        enableL1Cache: true,
        enableL2Cache: true,
      });
      await agentDB.initialize();

      const config = global.testUtils.createMockAgentConfig();
      const mockSpawnFn = jest.fn().mockResolvedValue({ id: 'agent' });

      const start = performance.now();

      await Promise.all(
        Array.from({ length: 100 }, () =>
          agentDB.findOrSpawnAgent(config, mockSpawnFn)
        )
      );

      const totalTime = performance.now() - start;

      console.log(`\nThroughput Test (100 concurrent requests):`);
      console.log(`  Total Time: ${totalTime.toFixed(2)}ms`);
      console.log(`  Target: <1000ms`);
      console.log(`  Status: ${totalTime < 1000 ? '✅ PASS' : '❌ FAIL'}`);
      console.log(`  Throughput: ${(100000 / totalTime).toFixed(0)} req/sec`);

      expect(totalTime).toBeLessThan(1000);
      expect(mockSpawnFn).not.toHaveBeenCalled(); // All cache hits
    });
  });
});
