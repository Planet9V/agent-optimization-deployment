#!/usr/bin/env python3
"""
Visualize benchmark results with charts and statistical analysis
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List

def load_results(filepath: str) -> Dict:
    """Load benchmark results from JSON"""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_speedup_chart(results: Dict, output_path: str):
    """Create speedup comparison chart"""
    queries = list(results["queries"].keys())
    l1_speedups = [results["queries"][q]["speedup_l1"] for q in queries]
    l2_speedups = [results["queries"][q]["speedup_l2"] for q in queries]

    x = np.arange(len(queries))
    width = 0.35

    fig, ax = plt.subplots(figsize=(14, 8))

    bars1 = ax.bar(x - width/2, l1_speedups, width, label='L1 Cache Hit', color='#2ecc71')
    bars2 = ax.bar(x + width/2, l2_speedups, width, label='L2 Cache Hit', color='#3498db')

    # Add target line at 150x
    ax.axhline(y=150, color='red', linestyle='--', linewidth=2, label='Minimum Claimed (150x)')
    ax.axhline(y=12500, color='orange', linestyle='--', linewidth=2, label='Maximum Claimed (12,500x)')

    ax.set_xlabel('Query Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Speedup Factor (x)', fontsize=12, fontweight='bold')
    ax.set_title('Neo4j Cache Speedup Analysis\n(Cache Hit vs Cache Miss)',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([q.replace('_', ' ').title() for q in queries], rotation=45, ha='right')
    ax.legend(loc='upper left')
    ax.set_yscale('log')  # Use log scale for large speedups
    ax.grid(True, alpha=0.3)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}x',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"📊 Speedup chart saved to: {output_path}")
    plt.close()

def create_latency_chart(results: Dict, output_path: str):
    """Create latency comparison chart"""
    queries = list(results["queries"].keys())
    cache_miss = [results["queries"][q]["cache_miss"]["p50_ms"] for q in queries]
    l2_hit = [results["queries"][q]["l2_hit"]["p50_ms"] for q in queries]
    l1_hit = [results["queries"][q]["l1_hit"]["p50_ms"] for q in queries]

    x = np.arange(len(queries))
    width = 0.25

    fig, ax = plt.subplots(figsize=(14, 8))

    bars1 = ax.bar(x - width, cache_miss, width, label='Cache Miss (Cold)', color='#e74c3c')
    bars2 = ax.bar(x, l2_hit, width, label='L2 Cache Hit', color='#f39c12')
    bars3 = ax.bar(x + width, l1_hit, width, label='L1 Cache Hit', color='#2ecc71')

    # Add target lines
    ax.axhline(y=1.0, color='green', linestyle='--', linewidth=2, label='L1 Target (<1ms)')
    ax.axhline(y=10.0, color='blue', linestyle='--', linewidth=2, label='L2 Target (<10ms)')

    ax.set_xlabel('Query Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latency (milliseconds)', fontsize=12, fontweight='bold')
    ax.set_title('Neo4j Query Latency Analysis (p50)\n(Lower is Better)',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([q.replace('_', ' ').title() for q in queries], rotation=45, ha='right')
    ax.legend(loc='upper left')
    ax.set_yscale('log')  # Use log scale for wide range
    ax.grid(True, alpha=0.3)

    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}ms',
                   ha='center', va='bottom', fontsize=8, rotation=90)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"📊 Latency chart saved to: {output_path}")
    plt.close()

def create_percentile_chart(results: Dict, output_path: str):
    """Create percentile distribution chart for L1 cache hits"""
    queries = list(results["queries"].keys())

    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(queries))
    width = 0.2

    p50_values = [results["queries"][q]["l1_hit"]["p50_ms"] for q in queries]
    p95_values = [results["queries"][q]["l1_hit"]["p95_ms"] for q in queries]
    p99_values = [results["queries"][q]["l1_hit"]["p99_ms"] for q in queries]

    bars1 = ax.bar(x - width, p50_values, width, label='p50 (Median)', color='#2ecc71')
    bars2 = ax.bar(x, p95_values, width, label='p95', color='#f39c12')
    bars3 = ax.bar(x + width, p99_values, width, label='p99', color='#e74c3c')

    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Target (<1ms)')

    ax.set_xlabel('Query Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('L1 Cache Hit Latency (milliseconds)', fontsize=12, fontweight='bold')
    ax.set_title('L1 Cache Hit Latency Distribution\n(Percentile Analysis)',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([q.replace('_', ' ').title() for q in queries], rotation=45, ha='right')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"📊 Percentile chart saved to: {output_path}")
    plt.close()

def create_summary_report(results: Dict, output_path: str):
    """Create markdown summary report"""
    overall = results["overall"]

    report = f"""# Neo4j Cache Performance Benchmark Report

**Generated:** {results["timestamp"]}
**Iterations:** {results["iterations"]} per scenario

## Executive Summary

### 🎯 Speedup Analysis

| Metric | Value |
|--------|-------|
| **Average L1 Speedup** | {overall['avg_l1_speedup']}x |
| **Maximum L1 Speedup** | {overall['max_l1_speedup']}x |
| **Minimum L1 Speedup** | {overall['min_l1_speedup']}x |
| **Average L2 Speedup** | {overall['avg_l2_speedup']}x |

### ⏱️ Latency Analysis

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Average L1 Hit** | {overall['avg_l1_latency_ms']:.3f}ms | <1ms | {'✅ PASS' if overall['l1_target_achieved'] else '❌ FAIL'} |
| **Average L2 Hit** | {overall['avg_l2_latency_ms']:.3f}ms | <10ms | {'✅ PASS' if overall['l2_target_achieved'] else '❌ FAIL'} |

### 🔬 Validation Results

**Claimed Speedup Range:** {overall['claimed_speedup_range']}

{overall['validation']}

## Detailed Query Results

"""

    for query_name, stats in results["queries"].items():
        report += f"""
### {query_name.replace('_', ' ').title()}

| Scenario | p50 (ms) | p95 (ms) | p99 (ms) | Speedup |
|----------|----------|----------|----------|---------|
| Cache Miss | {stats['cache_miss']['p50_ms']:.3f} | {stats['cache_miss']['p95_ms']:.3f} | {stats['cache_miss']['p99_ms']:.3f} | - |
| L2 Hit | {stats['l2_hit']['p50_ms']:.3f} | {stats['l2_hit']['p95_ms']:.3f} | {stats['l2_hit']['p99_ms']:.3f} | {stats['speedup_l2']}x |
| L1 Hit | {stats['l1_hit']['p50_ms']:.3f} | {stats['l1_hit']['p95_ms']:.3f} | {stats['l1_hit']['p99_ms']:.3f} | {stats['speedup_l1']}x |

**Target Achievement:**
- L1 Target (<1ms): {'✅ ACHIEVED' if stats['meets_l1_target'] else '❌ MISSED'}
- L2 Target (<10ms): {'✅ ACHIEVED' if stats['meets_l2_target'] else '❌ MISSED'}

"""

    report += """
## Methodology

### Test Scenarios

1. **Cache MISS (Cold Cache):**
   - Clear page cache before measurement
   - 10 iterations to establish baseline
   - Represents worst-case disk I/O latency

2. **L2 Cache HIT (Warm Cache):**
   - Single warmup query
   - 50 iterations after 1s settle time
   - Represents memory-resident data access

3. **L1 Cache HIT (Hot Cache):**
   - Repeated access without cache clear
   - 100 iterations for statistical significance
   - Represents optimal cached query execution

### Statistical Analysis

- **p50 (Median):** 50th percentile, typical performance
- **p95:** 95th percentile, near-worst case
- **p99:** 99th percentile, worst case
- **Speedup:** Ratio of cache_miss_p50 / cache_hit_p50

## Recommendations

### Performance Optimization
"""

    # Add recommendations based on results
    if overall['avg_l1_speedup'] < 150:
        report += """
1. ⚠️ **Cache Configuration:** L1 speedup below claimed minimum. Consider:
   - Increasing page cache size (`dbms.memory.pagecache.size`)
   - Adjusting heap size (`dbms.memory.heap.max_size`)
   - Reviewing query patterns for cache efficiency

"""
    else:
        report += """
1. ✅ **Cache Performance:** Speedup meets or exceeds claims. Maintain current configuration.

"""

    if not overall['l1_target_achieved']:
        report += """
2. ⚠️ **Latency Targets:** L1 hits exceed 1ms target. Investigate:
   - Query optimization opportunities
   - Index coverage and usage
   - Network latency between driver and database

"""

    report += """
### Monitoring

- Track cache hit ratios in production
- Monitor p95/p99 latencies for SLA compliance
- Alert on cache miss spikes indicating configuration issues

## Conclusion

This benchmark provides empirical validation of Neo4j cache performance claims through:
- Statistical rigor (100+ iterations)
- Multiple query patterns
- Percentile analysis (p50, p95, p99)
- Real-world speedup calculations

Results can guide cache configuration, query optimization, and capacity planning decisions.
"""

    with open(output_path, 'w') as f:
        f.write(report)

    print(f"📄 Summary report saved to: {output_path}")

def main():
    results_file = "/home/jim/2_OXOT_Projects_Dev/tests/performance/benchmark_results.json"
    output_dir = "/home/jim/2_OXOT_Projects_Dev/tests/performance"

    print("📊 Loading benchmark results...")
    results = load_results(results_file)

    print("🎨 Creating visualizations...")
    create_speedup_chart(results, f"{output_dir}/speedup_chart.png")
    create_latency_chart(results, f"{output_dir}/latency_chart.png")
    create_percentile_chart(results, f"{output_dir}/percentile_chart.png")

    print("📝 Generating summary report...")
    create_summary_report(results, f"{output_dir}/BENCHMARK_REPORT.md")

    print("\n✅ Visualization complete!")
    print(f"📁 Output directory: {output_dir}")

if __name__ == "__main__":
    main()
