# Neo4j Cache Performance Benchmarks

## Overview

This benchmark suite validates Neo4j cache performance claims (150-12,500x speedup) through statistical measurement of:

- **L1 Cache Hit Latency:** <1ms target (hot cache, repeated access)
- **L2 Cache Hit Latency:** <10ms target (warm cache, first access)
- **Cache Miss Latency:** Baseline disk I/O performance
- **Speedup Factors:** Actual measured improvements

## Quick Start

### Prerequisites

1. **Neo4j running** on `localhost:7687`
2. **Python 3.7+** with pip
3. **Test data** loaded in Neo4j (Assets, CriticalInfrastructure nodes)

### Run Benchmarks

```bash
# Set Neo4j credentials
export NEO4J_PASSWORD="your_password"

# Run complete benchmark suite
./tests/performance/run_benchmarks.sh
```

### Expected Output

```
🚀 Neo4j Cache Performance Benchmark Suite
==========================================
📍 Neo4j Connection: bolt://localhost:7687

⏱️  Running benchmark suite...

🔬 Benchmarking: Node Lookup by ID
  📊 Measuring cache MISS (cold cache)...
  📊 Measuring L2 cache HIT...
  📊 Measuring L1 cache HIT...
  ✅ L1 Speedup: 245.3x (target: 150-12,500x)
  ✅ L2 Speedup: 102.7x
  📈 L1 p50: 0.423ms (target: <1ms)
  📈 L2 p50: 1.008ms (target: <10ms)

[... additional queries ...]

📊 PERFORMANCE BENCHMARK SUMMARY
=================================
🎯 SPEEDUP ANALYSIS:
  Average L1 Speedup: 287.5x
  Maximum L1 Speedup: 542.8x
  Minimum L1 Speedup: 156.2x

⏱️  LATENCY ANALYSIS:
  Average L1 Hit: 0.512ms (target: <1ms)
  Average L2 Hit: 2.341ms (target: <10ms)
  L1 Target: ✅ ACHIEVED
  L2 Target: ✅ ACHIEVED

🔬 VALIDATION:
  Claimed Range: 150-12,500x
  ✅ VALIDATED: Max speedup 542.8x meets minimum claim of 150x
```

## Benchmark Methodology

### Test Scenarios

1. **Cache MISS (Cold Cache)**
   - Clear page cache before measurement
   - 10 iterations for baseline
   - Represents disk I/O latency

2. **L2 Cache HIT (Warm Cache)**
   - Single warmup query
   - 50 iterations after 1s settle
   - Represents memory-resident data

3. **L1 Cache HIT (Hot Cache)**
   - Repeated access without clear
   - 100 iterations for statistics
   - Represents optimal cache performance

### Queries Tested

| Query Type | Description | Tests |
|------------|-------------|-------|
| `node_lookup_by_id` | Direct node access by internal ID | Cache efficiency for simple lookups |
| `property_lookup` | Indexed property search | Index + cache interaction |
| `relationship_traversal` | 1-hop traversal | Relationship cache performance |
| `pattern_matching` | 2-hop variable-length path | Complex pattern cache behavior |
| `aggregation` | Group by with count | Aggregation cache effectiveness |

### Statistical Metrics

- **p50 (Median):** Typical performance, 50th percentile
- **p95:** Near-worst case, 95th percentile
- **p99:** Worst case, 99th percentile
- **Speedup:** `cache_miss_p50 / cache_hit_p50`

## Results & Artifacts

After running benchmarks, you'll find:

### Data
- `benchmark_results.json` - Raw benchmark data with all metrics

### Reports
- `BENCHMARK_REPORT.md` - Detailed markdown report with recommendations

### Charts
- `speedup_chart.png` - Speedup factors (L1/L2 vs claimed range)
- `latency_chart.png` - Absolute latencies (cold/warm/hot cache)
- `percentile_chart.png` - L1 latency distribution (p50/p95/p99)

## Interpreting Results

### ✅ Success Criteria

- **L1 Speedup:** ≥150x minimum (claimed range: 150-12,500x)
- **L1 Latency:** <1ms p50
- **L2 Latency:** <10ms p50
- **Cache Hit Rate:** >80% in production (monitor separately)

### Example Validation

```json
{
  "overall": {
    "avg_l1_speedup": 287.5,
    "max_l1_speedup": 542.8,
    "avg_l1_latency_ms": 0.512,
    "l1_target_achieved": true,
    "validation": "✅ VALIDATED: Max speedup 542.8x meets minimum claim of 150x"
  }
}
```

## Troubleshooting

### Low Speedup (<150x)

**Possible Causes:**
- Insufficient page cache size
- Cold cache not properly cleared
- Network latency dominating measurements
- Small dataset fits entirely in memory

**Solutions:**
1. Check Neo4j config: `dbms.memory.pagecache.size`
2. Increase dataset size for realistic testing
3. Run benchmarks on Neo4j server (eliminate network)
4. Review query execution plans

### High L1 Latency (>1ms)

**Possible Causes:**
- Unoptimized queries
- Missing indexes
- GC pauses
- Network overhead

**Solutions:**
1. Add indexes on frequently queried properties
2. Optimize query patterns
3. Tune JVM GC settings
4. Use local driver connection

### Inconsistent Results

**Possible Causes:**
- Background processes
- Insufficient warmup
- Small iteration count
- Concurrent Neo4j access

**Solutions:**
1. Run on dedicated system
2. Increase iteration count
3. Add longer warmup period
4. Ensure exclusive Neo4j access

## Configuration

### Environment Variables

```bash
# Neo4j connection
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"

# Benchmark parameters (optional)
export BENCHMARK_ITERATIONS=100  # Iterations per scenario
export BENCHMARK_WARMUP=5        # Warmup queries
```

### Customization

Edit `cache_benchmark.py` to:
- Add custom queries
- Adjust iteration counts
- Change cache clear strategy
- Modify statistical analysis

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Performance Benchmarks

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2am

jobs:
  benchmark:
    runs-on: ubuntu-latest
    services:
      neo4j:
        image: neo4j:5.15-enterprise
        env:
          NEO4J_AUTH: neo4j/benchmark_password
          NEO4J_ACCEPT_LICENSE_AGREEMENT: yes
        ports:
          - 7687:7687

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install neo4j matplotlib numpy

      - name: Load test data
        run: python scripts/load_test_data.py

      - name: Run benchmarks
        env:
          NEO4J_PASSWORD: benchmark_password
        run: ./tests/performance/run_benchmarks.sh

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: benchmark-results
          path: tests/performance/
```

## Contributing

To add new benchmark queries:

1. Edit `cache_benchmark.py`
2. Add query to `run_benchmarks()` method:
   ```python
   self.results["queries"]["my_query"] = self.benchmark_query(
       name="My Query Description",
       query="MATCH ... RETURN ...",
       params={"param": "value"}
   )
   ```
3. Run benchmarks and verify results
4. Update documentation

## References

- [Neo4j Performance Tuning](https://neo4j.com/docs/operations-manual/current/performance/)
- [Page Cache Configuration](https://neo4j.com/docs/operations-manual/current/performance/memory-configuration/)
- [Query Tuning Guide](https://neo4j.com/docs/cypher-manual/current/query-tuning/)

## License

Same as parent project.
