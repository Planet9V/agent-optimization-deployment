# Data Flow Architecture - AEON Cyber DT v4.0

**File**: 07_DATA_FLOW_ARCHITECTURE_v4.0_2025-12-02.md
**Created**: 2025-12-02 22:00:00 UTC
**Modified**: 2025-12-02 22:00:00 UTC
**Version**: v4.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete data flow documentation for all system components
**Status**: ACTIVE

---

## Overview

This document describes the complete data flow architecture of the AEON Cyber Digital Twin system, including data ingestion, processing, storage, and retrieval pathways.

---

## 1. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL DATA SOURCES                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  NVD API   │  FIRST.org  │  MITRE ATT&CK  │  CWE/CAPEC  │  EMB3D  │  KEV   │
│  (CVEs)    │  (EPSS)     │  (Techniques)  │  (XML)      │  (STIX) │        │
└─────┬──────┴──────┬──────┴───────┬────────┴──────┬──────┴────┬────┴────┬───┘
      │             │              │               │           │         │
      ▼             ▼              ▼               ▼           ▼         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATA INGESTION LAYER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │ update_cve_     │  │ load_compre-    │  │    chunked_ingest.py        │  │
│  │ taxonomy.py     │  │ hensive_        │  │    (Document Processing)    │  │
│  │ (Weekly CVE)    │  │ taxonomy.py     │  │                             │  │
│  └────────┬────────┘  └────────┬────────┘  └─────────────┬───────────────┘  │
│           │                    │                         │                   │
│           ▼                    ▼                         ▼                   │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      NER11 API (localhost:8000)                        │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐ │ │
│  │  │ /ner         │  │ /search      │  │ /hybrid                      │ │ │
│  │  │ Entity       │  │ Semantic     │  │ Semantic + Graph             │ │ │
│  │  │ Extraction   │  │ Search       │  │ Search                       │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STORAGE LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────┐  ┌────────────────────────────────────────┐ │
│  │     Neo4j Graph Database   │  │         Qdrant Vector Database         │ │
│  │     (bolt://localhost:7687)│  │         (localhost:6333)               │ │
│  │                            │  │                                        │ │
│  │  • 332,750 nodes           │  │  • 49,000+ vectors                     │ │
│  │  • 11.2M relationships     │  │  • 384-dim embeddings                  │ │
│  │  • Full taxonomy           │  │  • Semantic search                     │ │
│  │                            │  │  • Collection: ner11_entities_         │ │
│  │  Labels:                   │  │    hierarchical                        │ │
│  │  CVE, CWE, CAPEC,          │  │                                        │ │
│  │  Technique, Tactic,        │  │  Payload:                              │ │
│  │  EMB3DThreat,              │  │  • text                                │ │
│  │  EMB3DMitigation,          │  │  • label                               │ │
│  │  EMB3DProperty,            │  │  • source_file                         │ │
│  │  KEV, Entity               │  │  • created_at                          │ │
│  └────────────────────────────┘  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API LAYER (Frontend Access)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐  ┌───────────────────┐  ┌───────────────────────────┐ │
│  │  NER11 REST API  │  │  Neo4j Bolt API   │  │  Qdrant REST/gRPC API     │ │
│  │  localhost:8000  │  │  localhost:7687   │  │  localhost:6333           │ │
│  │                  │  │                   │  │                           │ │
│  │  Endpoints:      │  │  Driver:          │  │  Endpoints:               │ │
│  │  POST /ner       │  │  neo4j-driver     │  │  POST /collections/       │ │
│  │  POST /search    │  │                   │  │    {name}/points/search   │ │
│  │  POST /hybrid    │  │  Auth:            │  │  GET /collections/{name}  │ │
│  │  GET /health     │  │  neo4j/           │  │                           │ │
│  │                  │  │  neo4j@openspg    │  │                           │ │
│  └──────────────────┘  └───────────────────┘  └───────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND APPLICATION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     React/Next.js Application                         │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │ Threat      │  │ Attack Path │  │ Vulnerability│  │ Entity      │  │   │
│  │  │ Search      │  │ Visualizer  │  │ Dashboard   │  │ Explorer    │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Flow Pathways

### 2.1 CVE Update Flow (Weekly)

```
NVD API → update_cve_taxonomy.py → Neo4j
                ↓
          FIRST.org EPSS API → Enrichment → Neo4j (update EPSS scores)
```

**Process**:
1. Script fetches CVEs modified in last 7 days from NVD API
2. For each CVE batch, fetches EPSS scores from FIRST.org
3. Calculates priority tier based on EPSS + CVSS
4. MERGE into Neo4j with upsert semantics
5. Creates HAS_WEAKNESS relationships to CWE nodes

**Script**: `scripts/update_cve_taxonomy.py`

**Cron Schedule**:
```bash
0 0 * * 0 cd /path/to/project && python3 scripts/update_cve_taxonomy.py --days 7
```

---

### 2.2 Comprehensive Taxonomy Load Flow

```
MITRE ATT&CK STIX → load_comprehensive_taxonomy.py → Neo4j (Technique, Tactic)
CWE XML           →                                → Neo4j (CWE)
CAPEC XML         →                                → Neo4j (CAPEC)
EMB3D STIX        →                                → Neo4j (EMB3DThreat, EMB3DMitigation)
```

**Process**:
1. Download latest data files to `NVS Full CVE CAPEC CWE EMBED/` directory
2. Run loader with `--source` flag or `--all`
3. Loader parses files and creates nodes/relationships
4. Cross-taxonomy links created (CAPEC→CWE, CVE→CWE, etc.)

**Script**: `scripts/load_comprehensive_taxonomy.py`

---

### 2.3 Document Ingestion Flow

```
Markdown Files → chunked_ingest.py → NER11 API → Neo4j (Entity)
                                        ↓
                                   Qdrant (Embeddings)
```

**Process**:
1. Script scans directory for .md files
2. Large documents (>50KB) split into chunks
3. Each chunk sent to NER11 `/ner` endpoint
4. Extracted entities stored in:
   - **Neo4j**: Entity nodes with text, label, source_file
   - **Qdrant**: Vector embeddings for semantic search

**Script**: `scripts/chunked_ingest.py`

---

### 2.4 Frontend Query Flow

```
User Query → Frontend → API Selection:
                          ├─ Entity Extraction: POST /ner
                          ├─ Semantic Search: POST /search
                          ├─ Hybrid Search: POST /hybrid
                          └─ Direct Graph: Neo4j Bolt
                                    ↓
                              Response → Frontend → User
```

---

## 3. API Integration Patterns

### 3.1 NER11 API Integration

**Base URL**: `http://localhost:8000`

#### Entity Extraction
```typescript
async function extractEntities(text: string) {
  const response = await fetch('http://localhost:8000/ner', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return response.json();
}
```

#### Semantic Search
```typescript
async function semanticSearch(query: string, limit: number = 10) {
  const response = await fetch('http://localhost:8000/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, limit })
  });
  return response.json();
}
```

---

### 3.2 Neo4j Integration

**Connection**: `bolt://localhost:7687`
**Auth**: `neo4j` / `neo4j@openspg`

```typescript
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'neo4j@openspg')
);

async function queryGraph(cypher: string, params: object = {}) {
  const session = driver.session();
  try {
    const result = await session.run(cypher, params);
    return result.records.map(r => r.toObject());
  } finally {
    await session.close();
  }
}
```

---

### 3.3 Qdrant Integration

**URL**: `http://localhost:6333`
**Collection**: `ner11_entities_hierarchical`

```typescript
async function vectorSearch(vector: number[], limit: number = 10) {
  const response = await fetch(
    'http://localhost:6333/collections/ner11_entities_hierarchical/points/search',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        vector,
        limit,
        with_payload: true
      })
    }
  );
  return response.json();
}
```

---

## 4. Data Update Schedules

| Data Source | Update Frequency | Script | Trigger |
|-------------|------------------|--------|---------|
| CVE | Weekly | update_cve_taxonomy.py | Cron (Sunday midnight) |
| EPSS | Daily (optional) | load_comprehensive_taxonomy.py --source epss | Manual |
| MITRE ATT&CK | Quarterly | load_comprehensive_taxonomy.py --source attack | Manual on release |
| CWE | Annual | load_comprehensive_taxonomy.py --source cwe | Manual on release |
| CAPEC | Annual | load_comprehensive_taxonomy.py --source capec | Manual on release |
| EMB3D | As released | load_comprehensive_taxonomy.py --source emb3d | Manual |
| Documents | Continuous | chunked_ingest.py | Manual/CI |

---

## 5. Error Handling and Recovery

### 5.1 API Failures

```python
# NER11 API recovery pattern
def process_with_retry(text, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json={"text": text}, timeout=60)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.Timeout:
            if not wait_for_api(60):
                break
            continue
    return None
```

### 5.2 Neo4j Connection Issues

```bash
# Health check
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"

# Restart if needed
docker restart openspg-neo4j
```

### 5.3 Qdrant Connection Issues

```bash
# Health check
curl http://localhost:6333/collections/ner11_entities_hierarchical

# Restart if needed
docker restart qdrant
```

---

## 6. Performance Considerations

### 6.1 Batch Operations

- **CVE Updates**: Process in batches of 2000 (NVD API limit)
- **EPSS Fetches**: Batch 100 CVEs per request
- **Document Ingestion**: Chunk documents >50KB
- **Neo4j Writes**: Use UNWIND for batch inserts

### 6.2 Rate Limits

| API | Rate Limit | Handling |
|-----|------------|----------|
| NVD | 5 req/30s (free) | 6s delay between requests |
| EPSS | Reasonable use | 1s delay between batches |
| NER11 | No limit | 3s delay for stability |

### 6.3 Caching

- **Neo4j**: Built-in query cache
- **Qdrant**: HNSW index for fast vector search
- **Frontend**: Implement response caching for repeated queries

---

## 7. Monitoring and Logging

### 7.1 Log Locations

```
/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/logs/
├── cve_update.log          # Weekly CVE updates
├── taxonomy_load.log       # Full taxonomy loads
├── epss_update.log         # EPSS updates
└── chunked_ingest.log      # Document ingestion
```

### 7.2 Health Checks

```bash
#!/bin/bash
# health_check.sh

# Check Neo4j
cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1" || echo "Neo4j DOWN"

# Check Qdrant
curl -s http://localhost:6333/collections/ner11_entities_hierarchical || echo "Qdrant DOWN"

# Check NER11 API
curl -s http://localhost:8000/health || echo "NER11 DOWN"
```

---

## 8. Security Considerations

### 8.1 Credentials

- **Neo4j**: Stored in environment or config, not in code
- **API Keys**: NVD API key optional but recommended for higher rate limits

### 8.2 Network

- All services run on localhost by default
- Configure firewall for production deployment
- Use HTTPS for external API calls

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v4.0.0 | 2025-12-02 | Complete data flow with all sources |
| v3.0.0 | 2025-11-19 | Initial architecture documentation |
