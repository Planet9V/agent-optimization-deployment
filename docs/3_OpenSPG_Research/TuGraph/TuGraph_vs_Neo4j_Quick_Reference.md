# TuGraph vs Neo4j: Quick Performance Reference
**Evidence-Based Benchmark Summary**

---

## 🎯 Key Performance Metrics

### LDBC SNB Interactive Benchmark

| Metric | TuGraph | Neo4j | Source |
|--------|---------|-------|--------|
| **Throughput (SF30)** | 5,436 ops/sec | Not published | LDBC audit |
| **Throughput (SF300)** | 4,855 ops/sec | Not completed | LDBC audit |
| **Scaling degradation** | 10% (SF30→SF300) | Unable to complete SF1000 | LDBC audit |
| **Mean response time** | 1.5ms (short queries) | Not specified | TuGraph docs |
| **BI queries completed** | Full suite | 12/25 (SF1000) | Research study |
| **Ranking** | #1 (March 2023) | Not ranked | LDBC official |

---

## ⚡ Write Performance

| Metric | TuGraph | Neo4j |
|--------|---------|-------|
| **Bulk loading** | "Fast" (no metrics) | >1M records/sec |
| **Concurrent writes** | Not published | 100x improvement (v2.2) |
| **Write throughput** | Millions of vertices/sec | Millions of records/sec |
| **Optimization** | C++ stored procedures | Transaction bundling |

**Winner:** Neo4j (published metrics and proven bulk loading)

---

## 📊 Query Performance Patterns

### Complex BI Queries (Analytical)
- **TuGraph:** Optimized C++ implementation, full suite completion
- **Neo4j:** Only 12/25 queries completed in 5 hours at SF1000
- **Winner:** TuGraph

### Multi-Hop Path Queries (Proxy: TigerGraph vs Neo4j)
- 1-hop: TigerGraph 24.8x faster than Neo4j
- 3-hop: TigerGraph 1,808x faster than Neo4j
- 6-hop: Neo4j OOM killed, TigerGraph completed
- **Implication:** TuGraph likely similar to TigerGraph performance

### Short Interactive Queries
- **TuGraph:** 1.5ms mean response time
- **Neo4j:** Optimized for read-heavy workloads
- **Result:** Both competitive, workload-dependent

---

## 🔄 Concurrent User Performance

### Neo4j Metrics
- **Concurrent query throughput:** 280 qps (specific query, v5.1)
- **Performance improvement:** 10x faster under concurrent load (v2.2 vs v2.1)
- **Architecture:** In-memory page cache for concurrency

### TuGraph Metrics
- **Concurrent throughput:** Not published
- **Architecture:** High-performance single-machine design
- **Capability:** Millions of vertex visits/sec

**Winner:** Inconclusive (different measurement approaches)

---

## 💾 Storage & Memory

| Aspect | TuGraph | Neo4j |
|--------|---------|-------|
| **Storage efficiency** | Compact encoding, no pointers | 4x larger (vs competitors) |
| **Data structure** | B+ tree (balanced read/write) | Native graph storage |
| **Memory strategy** | Compact encoding | In-memory page cache |
| **Maximum scale tested** | SF300 (5.3B edges) | SF100 (1.7B edges) |

**Winner:** TuGraph (storage efficiency and scale)

---

## 🏗️ Architecture Comparison

### TuGraph
- **Type:** Single-machine, high-performance
- **Query implementation:** C++ stored procedures (benchmarks)
- **Storage:** B+ tree with compact encoding
- **Focus:** Graph analytics, maximum performance
- **Scalability:** Vertical (single machine)

### Neo4j
- **Type:** Single-server (Community), native graph
- **Query language:** Cypher (standard, declarative)
- **Storage:** Native graph storage with disk/memory
- **Focus:** General-purpose, flexibility
- **Scalability:** Vertical (non-distributed)

---

## 🎓 Use Case Recommendations

### Choose TuGraph When:
✅ **Maximum performance** is critical
✅ **Large-scale analytics** (billions of edges)
✅ **Known query patterns** can be pre-optimized
✅ **C++ stored procedures** acceptable
✅ **Single-machine deployment** sufficient
✅ **Read-heavy workloads** with specific patterns

**Example:** Financial fraud detection with known pattern queries

---

### Choose Neo4j When:
✅ **Standard query language** (Cypher) required
✅ **Rapid development** and flexibility needed
✅ **Bulk data loading** is primary operation
✅ **Concurrent transactions** are critical
✅ **Mature ecosystem** and tooling important
✅ **General-purpose** graph applications

**Example:** Social network application with diverse query patterns

---

## ⚠️ Important Caveats

### Benchmark Configuration Differences
- **TuGraph:** C++ stored procedures (not standard query language)
- **Neo4j:** Cypher query language (more flexible, potentially slower)
- **Testing:** Different hardware, network configurations
- **Audit status:** TuGraph has audited LDBC results; Neo4j metrics less public

### Missing Direct Comparisons
❌ No head-to-head test on identical hardware/configuration
❌ Neo4j audited LDBC throughput not publicly available
❌ Direct concurrent user scaling comparison missing
❌ Detailed memory usage comparison not published

---

## 📈 Performance Trends

### TuGraph Evolution
- LDBC SNB Interactive #1 (March 2023)
- Surpassed by Galaxybase (May 2022) - 70% higher throughput
- Continuous optimization focus

### Neo4j Evolution
- v2.2: 100x write throughput improvement
- v5.0: Query planning and indexing optimizations
- v5.1: Continued performance enhancements
- Focus on concurrent performance and scalability

---

## 🔬 Benchmark Reliability

### High Confidence ✅
- TuGraph LDBC SNB Interactive: 5,436 ops/sec (SF30)
- TuGraph scaling: 10% degradation SF30→SF300
- Neo4j bulk loading: >1M records/sec
- Neo4j concurrent improvements: 100x (v2.2)

### Medium Confidence ⚠️
- Comparative query performance (indirect via TigerGraph)
- Storage efficiency comparisons (different benchmarks)
- BI query completion rates

### Data Gaps ❌
- Direct TuGraph vs Neo4j on same hardware
- Neo4j LDBC audited throughput
- Concurrent user scaling for TuGraph
- Detailed memory usage comparison

---

## 📚 Key Sources

1. **LDBC Official Audits** - TuGraph SNB Interactive results
2. **ArXiv Research** - MV4PG materialized views study (2024)
3. **University Studies** - TigerGraph vs Neo4j comparative analysis
4. **Official Documentation** - TuGraph and Neo4j performance specs
5. **Independent Benchmarks** - Galaxybase, GraphDB, Memgraph comparisons

---

## 💡 Bottom Line

### Performance Winner: TuGraph
- LDBC benchmark leadership
- Superior scaling characteristics
- Optimized for analytics workloads

### Flexibility Winner: Neo4j
- Standard query language (Cypher)
- Proven bulk loading performance
- Mature ecosystem and tooling

### Real-World Decision Factors:
1. **Workload type:** Analytics (TuGraph) vs General-purpose (Neo4j)
2. **Query patterns:** Known/fixed (TuGraph) vs Dynamic/diverse (Neo4j)
3. **Development speed:** Slow/optimized (TuGraph) vs Fast/flexible (Neo4j)
4. **Scale requirements:** Billions of edges (TuGraph) vs Moderate scale (Neo4j)
5. **Operational complexity:** C++ expertise (TuGraph) vs Standard SQL-like (Neo4j)

---

**⚠️ Critical Recommendation:**
Run application-specific benchmarks with your actual workload on target hardware before making final decision. Published benchmarks provide direction but not absolute guarantees for your use case.

**Last Updated:** 2025-10-26
