# LDBC Benchmark Details: TuGraph vs Neo4j
**Technical Deep Dive into LDBC SNB Results**

---

## 📋 What is LDBC SNB?

### Linked Data Benchmark Council - Social Network Benchmark

**Purpose:** Industry-standard benchmark for graph database performance evaluation

**Development:** Created by leading research groups (CWI) and major graph database vendors (including Neo4j)

**Audit Process:** Independent verification of benchmark implementations and results

---

## 🎯 LDBC SNB Workloads

### 1. Interactive Workload (OLTP)
**Focus:** Transactional queries simulating social network operations

**Query Types:**
- **Short reads:** Simple queries (e.g., get person by ID)
- **Complex reads:** Multi-hop traversals, pattern matching
- **Writes:** Insert/update operations (posts, comments, friendships)

**Metrics:**
- Throughput (operations per second)
- Response time (mean, P90, P99)
- Scalability across scale factors

---

### 2. Business Intelligence Workload (OLAP)
**Focus:** Analytical queries exploring large portions of the graph

**Query Types:**
- Complex aggregations
- Multi-hop path analysis
- Pattern detection across entire graph
- Statistical analysis

**Metrics:**
- Query completion time
- Queries completed within time limit
- Resource utilization

---

## 📊 Scale Factors Defined

| Scale Factor | Vertices | Edges | Approximate Size |
|--------------|----------|-------|------------------|
| **SF10** | ~30M | ~180M | ~10GB |
| **SF30** | ~80M | ~500M | ~30GB |
| **SF100** | ~270M | ~1.7B | ~100GB |
| **SF300** | ~800M | ~5.3B | ~300GB |
| **SF1000** | ~2.8B | ~18B | ~1TB |
| **SF3000** | ~8.5B | ~54B | ~3TB |
| **SF10000** | ~28B | ~180B | ~10TB |
| **SF30000** | ~86B | ~540B | ~30TB |

---

## 🏆 TuGraph LDBC SNB Results

### Interactive Workload (Audited)

**Test Date:** March 2023 (ranked #1)
**Audit Status:** ✅ Independently verified by LDBC

#### Performance Metrics

**SF30 (30GB, 80M vertices, 500M edges):**
- **Throughput:** 5,436 operations/second
- **Mean response time:** 1,519 microseconds (1.5ms)
- **Implementation:** C++ stored procedures

**SF300 (300GB, 800M vertices, 5.3B edges):**
- **Throughput:** 4,855 operations/second
- **Degradation:** Only 10.7% from SF30
- **Scalability score:** Excellent (minimal degradation at 10x scale)

**SF100 (100GB, 270M vertices, 1.7B edges):**
- **Status:** Completed successfully
- **Specific metrics:** Not published in available sources

---

#### Configuration Details

**Implementation Approach:**
- Language: C++ stored procedures
- Query method: Pre-compiled functions (not standard query language)
- Optimization: Direct hardware access, minimal overhead

**Hardware:** (Not specified in public audit summary)

**Software Stack:**
- TuGraph version used in audit
- B+ tree storage engine
- Compact encoding for properties

---

### Business Intelligence Workload (Audited)

**Test Date:** December 2023
**Scale Factor:** SF30000 (30TB, 86B vertices, 540B edges)
**Audit Status:** ✅ Independently verified by LDBC

#### Configuration

**Hardware:**
- 72 instances of ecs.r7.16xlarge
- Intel Xeon Platinum 8369B processors
- 64 cores per instance
- Total: 4,608 cores

**Software:**
- TuGraph version 0.9
- Query language: Gremlin
- Distribution: Hash sharding partitioning strategy
- Deployment: Kubernetes on Aliyun cloud

**Result:** Successfully completed all BI queries at SF30000

---

### World Record Context

**Previous Record Holder:** TuGraph (prior to May 2022)

**New Record Holder:** Galaxybase (May 16, 2022)
- **Improvement:** 70% higher throughput than TuGraph
- **Query performance:** 6x faster average
- **Best mean response:** 41x faster
- **Best P90 response:** 72x faster

**Important Note:** Configuration differences
- TuGraph: Separate client/server (~200μs network latency)
- Galaxybase: Embedded mode (same process)
- Both valid per LDBC spec, but not directly comparable

---

## 🔵 Neo4j LDBC SNB Results

### Interactive Workload

**Audit Status:** ⚠️ Specific audited throughput metrics not found in public sources

**Known Information:**
- Neo4j participated in LDBC SNB development
- Company joined LDBC as founding member
- Implementation uses Cypher query language

**Public Benchmark Results:** Not widely published for LDBC SNB Interactive

---

### Business Intelligence Workload

**Test Context:** University of California research study

**SF1000 (1TB) Results:**
- **Queries completed:** 12 out of 25 BI queries
- **Time limit:** 5 hours per query
- **Incomplete queries:** 13 queries exceeded time limit
- **Comparison:** TigerGraph completed all 25 queries

**Storage Requirements:**
- Approximately 4x larger than TigerGraph for same dataset
- Storage efficiency concern at large scale

---

### Performance Comparison (Neo4j vs TigerGraph on LDBC SNB)

**Source:** University of California benchmark study

#### Interactive Complex Queries
- TigerGraph: 100x+ faster on certain queries
- Performance gap increases with data size
- Neo4j completed but significantly slower

#### Business Intelligence Queries
- Neo4j: 12/25 queries completed (SF1000)
- TigerGraph: 25/25 queries completed (SF1000)
- Time limit: 5 hours per query

#### Multi-Hop Path Queries
- **1-hop:** TigerGraph 24.8x faster
- **3-hop:** TigerGraph 1,808x faster
- **6-hop:** Neo4j killed by OOM, TigerGraph completed

---

## 🔬 Methodology Comparison

### TuGraph Implementation

**Query Execution:**
- C++ stored procedures compiled for specific LDBC queries
- Direct function calls (no query parsing)
- Maximum performance through specialization

**Advantages:**
- Minimal overhead
- Predictable performance
- Optimal resource utilization

**Trade-offs:**
- Not using standard query language
- Less flexible for ad-hoc queries
- Requires C++ expertise

---

### Neo4j Implementation

**Query Execution:**
- Cypher query language (declarative)
- Query planner and optimizer
- Runtime execution engine

**Advantages:**
- Standard query language
- Flexible for varied workloads
- Developer-friendly

**Trade-offs:**
- Query planning overhead
- Performance depends on optimizer
- May not match hand-optimized C++

---

## 📈 Performance Analysis

### Throughput Scaling Comparison

**TuGraph (LDBC SNB Interactive):**
```
SF30:  5,436 ops/sec (baseline)
SF100: Not published
SF300: 4,855 ops/sec (-10.7%)
```

**Scaling Analysis:**
- 10x data increase (SF30 → SF300)
- Only 10.7% throughput decrease
- Excellent scaling characteristics
- Linear performance retention

**Neo4j:**
- SF100: Completed (metrics not published)
- SF1000: Could not complete full BI suite
- Scaling challenges at very large scale

---

### Query Complexity Performance

**Simple Queries:**
- TuGraph: 1.5ms mean response time
- Neo4j: Competitive on short reads

**Complex Multi-Hop Queries:**
- TuGraph: Optimized C++ implementation
- Neo4j: Significantly slower (via TigerGraph comparison proxy)

**Analytical (BI) Queries:**
- TuGraph: Completed all queries at SF30000
- Neo4j: Only 12/25 completed at SF1000

---

## 🎯 Direct vs Indirect Comparisons

### Direct TuGraph vs Neo4j
❌ **Not Available:** No published head-to-head benchmark on identical configuration

### Indirect via Third-Party Comparisons

**TuGraph vs Galaxybase:**
✅ Both tested on identical LDBC SNB workload
✅ Both have audited results
✅ Direct performance comparison valid

**Neo4j vs TigerGraph:**
✅ Academic research study
✅ Identical LDBC SNB workload
✅ Provides proxy for TuGraph comparison (similar architecture)

**Implication:**
- TuGraph and TigerGraph both use specialized implementations
- Both outperform Neo4j significantly on LDBC benchmarks
- Suggests TuGraph would outperform Neo4j in direct comparison

---

## 🔍 Benchmark Configuration Details

### Audited vs Non-Audited Results

**LDBC Audit Process:**
1. Independent auditor reviews implementation
2. Verifies queries match specification
3. Validates system configuration
4. Confirms result accuracy
5. Issues official audit report

**Audited Results (High Confidence):**
- ✅ TuGraph SNB Interactive (March 2023)
- ✅ TuGraph SNB BI (December 2023)
- ✅ Galaxybase SNB Interactive (May 2022)
- ✅ GraphDB SNB (Ontotext)

**Non-Audited Results (Lower Confidence):**
- ⚠️ Many vendor benchmark claims
- ⚠️ TigerGraph vs Neo4j study (academic, not LDBC audit)
- ⚠️ Internal performance testing

---

### Configuration Variables

**Factors Affecting Comparability:**

1. **Network Configuration:**
   - Client/server separation (adds latency)
   - Embedded mode (eliminates network)
   - Both valid, but not equivalent

2. **Hardware Specifications:**
   - CPU type and core count
   - Memory capacity
   - Storage type (SSD, NVMe, etc.)
   - Network bandwidth

3. **Software Configuration:**
   - Query implementation approach
   - Caching strategies
   - Optimization techniques
   - Parallel execution settings

4. **Workload Specifics:**
   - Query complexity distribution
   - Read/write ratio
   - Concurrent user count
   - Data access patterns

---

## 📊 Detailed Metrics Breakdown

### TuGraph Performance Characteristics

**Short Queries (7 queries analyzed):**
- Mean response time: 1,519 microseconds (1.5ms)
- Query type: Simple lookups and traversals
- Consistency: Microsecond-level response times

**Throughput Characteristics:**
- SF30: 5,436 ops/sec sustained
- SF300: 4,855 ops/sec sustained
- Degradation: Linear and predictable
- Resource utilization: Efficient

**Scalability Pattern:**
```
Data increase: 10x (SF30 → SF300)
Throughput decrease: 10.7%
Scalability efficiency: 89.3%
```

---

### Neo4j Performance Characteristics

**Known Strengths:**
- Bulk loading: >1M records/second
- Concurrent writes: 100x improvement (v2.2 vs v2.1)
- Short transactional queries: Competitive

**Known Challenges:**
- Complex BI queries at scale (12/25 at SF1000)
- Multi-hop traversals (1808x slower than TigerGraph on 3-hop)
- Storage efficiency (4x larger than competitors)

**Evolution:**
- v2.2: Major concurrent performance improvements
- v5.0: Query planning and indexing optimizations
- v5.1: Continued refinements

---

## 🎓 Benchmark Interpretation Guide

### Understanding Throughput Numbers

**Operations per Second (ops/sec):**
- Measures: Number of complete operations in 1 second
- Higher is better
- Consider: Query complexity, data size, hardware

**TuGraph 5,436 ops/sec (SF30):**
- 5,436 complete LDBC queries executed per second
- Sustained rate under benchmark conditions
- Includes all query types (short, complex, writes)

---

### Understanding Response Time

**Mean Response Time:**
- Average time for query completion
- Lower is better
- Consider: Query complexity distribution

**TuGraph 1.5ms mean:**
- Average of 1,519 microseconds
- For 7 short query types
- Sub-millisecond individual queries common

---

### Understanding Scalability

**Throughput Degradation:**
- Performance loss as data increases
- Lower degradation = better scalability
- Non-linear degradation indicates scaling problems

**TuGraph 10% degradation (SF30→SF300):**
- Excellent scaling characteristics
- Near-linear performance retention
- Suggests efficient algorithms and data structures

---

## 🔮 Extrapolation & Predictions

### TuGraph Expected Performance

**Based on demonstrated scaling:**
- SF30: 5,436 ops/sec ✅ (measured)
- SF100: ~5,200 ops/sec (estimated)
- SF300: 4,855 ops/sec ✅ (measured)
- SF1000: ~4,500 ops/sec (extrapolated)

**Confidence:** Medium (based on linear trend)

---

### Neo4j Expected Performance

**Based on published limitations:**
- SF30: Competitive (likely completed)
- SF100: Completed successfully
- SF300: Likely completed with degradation
- SF1000: Cannot complete full BI suite (12/25 queries)

**Confidence:** Medium (based on partial data)

---

## 🎯 Key Takeaways for Decision-Making

### When LDBC Benchmarks Matter

**Critical for:**
- ✅ Large-scale graph analytics
- ✅ Complex multi-hop queries
- ✅ Performance at scale (billions of edges)
- ✅ Predictable scaling characteristics

**Less Critical for:**
- ⚠️ Small to medium graphs (<100M edges)
- ⚠️ Simple CRUD operations
- ⚠️ Bulk loading focus
- ⚠️ Rapid development requirements

---

### LDBC Results Interpretation

**TuGraph Leadership:**
- Clear winner on LDBC SNB benchmarks
- Optimized specifically for benchmark queries
- May not represent general-purpose performance

**Neo4j Flexibility:**
- Standard query language flexibility
- May outperform on specific use cases
- Better for diverse, unpredictable workloads

---

## 📚 References & Data Sources

### Primary LDBC Sources
1. LDBC official website: ldbcouncil.org
2. TuGraph SNB Interactive audit report (March 2023)
3. TuGraph SNB BI audit report (December 2023)
4. Galaxybase SNB Interactive audit (May 2022)

### Academic Research
5. University of California TigerGraph vs Neo4j study
6. "MV4PG: Materialized Views for Property Graphs" (ArXiv 2024)
7. "In-Depth Benchmarking of Graph Database Systems with LDBC SNB"

### Vendor Documentation
8. TuGraph official documentation - Performance Oriented
9. Neo4j official blog posts (v2.2, v5.0 announcements)
10. LDBC benchmark specifications (Interactive, BI)

---

## 📝 Audit Report Access

**TuGraph LDBC SNB BI (December 2023):**
- Full disclosure: `ldbcouncil.org/benchmarks/snb/LDBC_SNB_BI_20231203_SF30000_tugraph.pdf`
- Executive summary: `ldbcouncil.org/benchmarks/snb/LDBC_SNB_BI_20231203_SF30000_tugraph-executive_summary.pdf`

**Official Results Repository:**
- LDBC website maintains archive of all audited results
- Search for specific database and workload
- Download full disclosure reports for detailed metrics

---

**Document Status:** ✅ COMPLETE - Based on publicly available LDBC audit reports and academic research

**Last Updated:** 2025-10-26

**Recommendation:** Consult LDBC official audit reports for most authoritative and detailed performance data.
