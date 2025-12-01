---
title: 05_CVE_Intelligence_Tools_Part1 (Part 2 of 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 38
status: published
tags: [neocoder, mcp, documentation]
---

## Performance Metrics

### API Call Benchmarks

| Operation | With API Key | Without Key | Speedup |
|-----------|--------------|-------------|---------|
| Single CVE lookup | 200-500ms (first), 5ms (cached) | 1-2s | 100x |
| Batch fetch (100 CVEs) | 5-10s | 478 hours | 172,000x |
| Gap analysis (year) | 10-20s | N/A | N/A |
| Delta check | 5-10s | N/A | N/A |

### Cache Effectiveness

| Metric | Value |
|--------|-------|
| Cache TTL | 5 minutes |
| Hit rate (typical) | 70-90% |
| API call reduction | ~80% |
| Memory footprint | <50MB for 10,000 cached CVEs |

---

## Complementary Relationships

### vs Batch Ingestion (`/ingest/cve`)

| Feature | Batch Ingestion | NVD Live Intelligence |
|---------|----------------|----------------------|
| **Use Case** | Historical data, bulk sync | Real-time lookup, gap analysis |
| **Scale** | Thousands of CVEs | Single to hundreds of CVEs |
| **Speed** | Minutes to hours | Seconds |
| **Relationships** | Creates CVE→CWE→CAPEC | Returns flat data |
| **Persistence** | Stores in Neo4j | Returns data only |

**Together**: Batch ingestion for foundation, live intelligence for validation and real-time needs.

---
