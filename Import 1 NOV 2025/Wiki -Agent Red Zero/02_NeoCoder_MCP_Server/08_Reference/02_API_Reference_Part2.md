---
title: API Reference (Part 2)
category: 08_Reference
last_updated: 2025-10-25
line_count: 220
status: published
tags: [neocoder, mcp, documentation]
---

## CVE Intelligence APIs (Phase 2.14)

**NEW**: Real-time NVD queries, gap analysis, and delta tracking using NVD API key.

### Live CVE Lookup

#### `GET /nvd/live/{cve_id}`

Fetch single CVE from NVD API in real-time.

**Parameters**:
- `cve_id` (str, path): CVE identifier

**Returns**:
```python
{
    "cve_id": str,
    "description": str,
    "cvss_score": float | None,
    "severity": str | None,
    "published_date": str | None,  # ISO 8601
    "modified_date": str | None,   # ISO 8601
    "references": List[str],
    "cwe_ids": List[str],
    "source": "nvd_live",
    "in_neo4j": bool
}
```

**Example**:
```bash
curl http://localhost:8002/nvd/live/CVE-2021-44228
```

---

### Gap Analysis

#### `POST /nvd/gap-analysis`

Compare Neo4j state vs NVD available CVEs.

**Request Body**:
```python
{
    "year": int | None,        # Filter by year
    "min_cvss": float | None   # Minimum CVSS score
}
```

**Returns**:
```python
{
    "year": int | None,
    "min_cvss": float | None,
    "total_in_neo4j": int,
    "total_in_nvd": int,
    "missing_count": int,
    "outdated_count": int,
    "missing_cves": List[str],    # First 100
    "outdated_cves": List[str],   # First 100
    "analysis_time": str          # ISO 8601
}
```

**Example**:
```bash
curl -X POST http://localhost:8002/nvd/gap-analysis \
  -H "Content-Type: application/json" \
  -d '{"year": 2021, "min_cvss": 7.0}'
```

---

### Delta Check

#### `POST /nvd/delta-check`

Check what CVEs are new or modified in NVD since timestamp.

**Request Body**:
```python
{
    "since_hours": int | None,      # Check last N hours (default: 24)
    "since_timestamp": str | None   # ISO timestamp
}
```

**Returns**:
```python
{
    "since_timestamp": str,     # ISO 8601
    "check_timestamp": str,     # ISO 8601
    "total_new": int,
    "total_modified": int,
    "new_cves": List[{
        "cve_id": str,
        "published_date": str,
        "cvss_score": float | None,
        "severity": str | None
    }],
    "modified_cves": List[{
        "cve_id": str,
        "modified_date": str,
        "cvss_score": float | None,
        "severity": str | None
    }]
}
```

**Example**:
```bash
curl -X POST http://localhost:8002/nvd/delta-check \
  -H "Content-Type: application/json" \
  -d '{"since_hours": 24}'
```

---

### Batch Fetch

#### `POST /nvd/batch-fetch`

Fetch multiple CVEs from NVD in parallel.

**Request Body**:
```python
{
    "cve_ids": List[str]  # Max 100 CVE IDs
}
```

**Returns**:
```python
{
    "requested": int,
    "found": int,
    "cves": List[{
        "cve_id": str,
        "description": str,
        "cvss_score": float | None,
        "severity": str | None,
        "published_date": str | None,
        "modified_date": str | None,
        "references": List[str],
        "cwe_ids": List[str],
        "source": "nvd_live",
        "in_neo4j": bool
    }]
}
```

**Example**:
```bash
curl -X POST http://localhost:8002/nvd/batch-fetch \
  -H "Content-Type: application/json" \
  -d '{"cve_ids": ["CVE-2021-44228", "CVE-2022-22965"]}'
```

---

## Error Responses

All APIs return standardized error format on failure:

```python
{
    "success": False,
    "error_code": str,  # e.g., "validation_error", "database_error"
    "message": str,
    "details": Dict  # Additional error context
}
```

**Common Error Codes**:
- `validation_error`: Invalid parameters
- `database_error`: Neo4j/Qdrant operation failed
- `not_found`: Resource doesn't exist
- `permission_denied`: Insufficient permissions
- `internal_error`: Unexpected error occurred

## Data Types

### EntityType

```python
Literal["concept", "technology", "person", "organization"]
```

### IncarnationType

```python
Literal["knowledge_graph", "coding", "code_analysis", "research",
        "decision_support", "data_analysis", "complex_system"]
```

### WorkflowStatus

```python
Literal["in_progress", "completed", "failed", "rolled_back"]
```

### RelationshipType

```python
Literal["RELATES_TO", "CITED_BY", "DERIVED_FROM", "SUPERSEDES",
        "HAS_FILE", "DEFINES", "IMPORTS", "CALLS", "INHERITS"]
```

## Related Documentation

- [Core Tools](../05_Tools_Reference/01_Core_Tools.md) - System tools
- [Knowledge Graph Tools](../05_Tools_Reference/02_Knowledge_Graph_Tools.md) - Entity management
- [Code Analysis Tools](../05_Tools_Reference/03_Code_Analysis_Tools.md) - Analysis tools
- [Specialized Tools](../05_Tools_Reference/04_Specialized_Tools.md) - Research and synthesis
- [CVE Intelligence Tools](../05_Tools_Reference/05_CVE_Intelligence_Tools.md) - **NEW** Phase 2.14 real-time NVD integration

---
*Last Updated: 2025-10-25 | Phase 2.14 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
