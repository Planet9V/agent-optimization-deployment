---
title: CVE Intelligence Tools Reference (Part 1 of 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 458
status: published
tags: [neocoder, mcp, documentation]
---


# CVE Intelligence Tools Reference

[← Back to Specialized Tools](04_Specialized_Tools.md) | [Next: Advanced Topics →](../06_Advanced_Topics/01_Hybrid_Reasoning.md)

## Overview

Real-time CVE intelligence tools for NVD API integration, gap analysis, and delta tracking. Complements batch ingestion with live queries and synchronization capabilities.

**Phase**: 2.14
**Status**: Production Ready
**API Key**: Required (5000 req/30s with key vs 50 req/30s without)

---

## Live Query Tools

### Live CVE Lookup

Fetch single CVE from NVD API in real-time.

**Endpoint**: `GET /nvd/live/{cve_id}`

**Parameters**:
- `cve_id` (str, path): CVE identifier (e.g., "CVE-2021-44228")

**Returns**:
```json
{
  "cve_id": "CVE-2021-44228",
  "description": "Apache Log4j2 remote code execution vulnerability",
  "cvss_score": 10.0,
  "severity": "CRITICAL",
  "published_date": "2021-12-10T10:00:00Z",
  "modified_date": "2021-12-14T12:00:00Z",
  "references": ["https://nvd.nist.gov/..."],
  "cwe_ids": ["CWE-502"],
  "source": "nvd_live",
  "in_neo4j": false
}
```

**Example**:
```bash
# curl
curl http://localhost:8002/nvd/live/CVE-2021-44228

# Python
import requests
response = requests.get("http://neocoder:8002/nvd/live/CVE-2021-44228")
cve_data = response.json()
```

**Use Cases**:
- Real-time CVE verification for threat intelligence
- Quick lookup during incident response
- Validation of CVE details from external sources
- Hybrid reasoning fallback when CVE not in Neo4j

**Caching**: 5-minute TTL, ~70-90% cache hit rate for repeated queries

---

### Gap Analysis

Compare Neo4j state vs NVD available CVEs to identify missing data.

**Endpoint**: `POST /nvd/gap-analysis`

**Request Body**:
```json
{
  "year": 2021,
  "min_cvss": 7.0
}
```

**Parameters**:
- `year` (int, optional): Filter by year (e.g., 2021)
- `min_cvss` (float, optional): Minimum CVSS score (e.g., 7.0 for HIGH+)

**Returns**:
```json
{
  "year": 2021,
  "min_cvss": 7.0,
  "total_in_neo4j": 0,
  "total_in_nvd": 23099,
  "missing_count": 23099,
  "outdated_count": 0,
  "missing_cves": ["CVE-2021-44228", "CVE-2021-44832", "..."],
  "outdated_cves": [],
  "analysis_time": "2025-10-25T19:30:00Z"
}
```

**Example**:
```bash
# Find all missing 2021 CVEs
curl -X POST http://localhost:8002/nvd/gap-analysis \
  -H "Content-Type: application/json" \
  -d '{"year": 2021}'

# Find missing HIGH+ severity CVEs from 2023
curl -X POST http://localhost:8002/nvd/gap-analysis \
  -H "Content-Type: application/json" \
  -d '{"year": 2023, "min_cvss": 7.0}'
```

**Use Cases**:
- Validate batch ingestion completeness
- Identify data gaps for targeted remediation
- Audit CVE coverage by year and severity
- Prioritize re-ingestion efforts

**Performance**: 10-20 seconds for year-wide analysis

---

### Delta Check

Check what CVEs are new or modified in NVD since timestamp.

**Endpoint**: `POST /nvd/delta-check`

**Request Body**:
```json
{
  "since_hours": 24
}
```

**Parameters**:
- `since_hours` (int, optional): Check changes in last N hours (default: 24)
- `since_timestamp` (str, optional): ISO timestamp to check from

**Returns**:
```json
{
  "since_timestamp": "2025-10-24T19:30:00Z",
  "check_timestamp": "2025-10-25T19:30:00Z",
  "total_new": 47,
  "total_modified": 12,
  "new_cves": [
    {
      "cve_id": "CVE-2025-1234",
      "published_date": "2025-10-25T10:00:00Z",
      "cvss_score": 9.8,
      "severity": "CRITICAL"
    }
  ],
  "modified_cves": [
    {
      "cve_id": "CVE-2024-5678",
      "modified_date": "2025-10-25T14:00:00Z",
      "cvss_score": 7.5,
      "severity": "HIGH"
    }
  ]
}
```

**Example**:
```bash
# Check last 24 hours
curl -X POST http://localhost:8002/nvd/delta-check \
  -H "Content-Type: application/json" \
  -d '{"since_hours": 24}'

# Check since specific timestamp
curl -X POST http://localhost:8002/nvd/delta-check \
  -H "Content-Type: application/json" \
  -d '{"since_timestamp": "2025-10-20T00:00:00Z"}'
```

**Use Cases**:
- Continuous monitoring for new CVEs
- Automated alerts for CRITICAL vulnerabilities
- Trigger incremental ingestion pipeline
- Track CVE modification activity

**Automation Example**:
```bash
#!/bin/bash
# Hourly cron job for delta monitoring
DELTA=$(curl -s -X POST http://localhost:8002/nvd/delta-check \
  -d '{"since_hours": 1}')

NEW_COUNT=$(echo $DELTA | jq '.total_new')

if [ $NEW_COUNT -gt 0 ]; then
  echo "Found $NEW_COUNT new CVEs - triggering ingestion"
  curl -X POST http://localhost:8002/ingest/cve -d '{"days_back": 1}'
fi
```

**Performance**: 5-10 seconds for daily delta

---

### Batch Fetch

Fetch multiple CVEs from NVD in parallel with rate limiting.

**Endpoint**: `POST /nvd/batch-fetch`

**Request Body**:
```json
{
  "cve_ids": ["CVE-2021-44228", "CVE-2022-22965", "CVE-2023-1234"]
}
```

**Parameters**:
- `cve_ids` (list[str]): List of CVE IDs to fetch (max 100)

**Returns**:
```json
{
  "requested": 3,
  "found": 3,
  "cves": [
    {
      "cve_id": "CVE-2021-44228",
      "description": "...",
      "cvss_score": 10.0,
      "severity": "CRITICAL",
      "..."
    },
    {
      "cve_id": "CVE-2022-22965",
      "..."
    }
  ]
}
```

**Example**:
```python
import requests

# Fetch specific CVEs identified from gap analysis
gap = requests.post("http://localhost:8002/nvd/gap-analysis",
                   json={"year": 2021, "min_cvss": 9.0}).json()

missing_critical = gap["missing_cves"][:100]  # First 100

batch = requests.post("http://localhost:8002/nvd/batch-fetch",
                     json={"cve_ids": missing_critical}).json()

print(f"Fetched {batch['found']} of {batch['requested']} CVEs")
```

**Use Cases**:
- Targeted synchronization after gap analysis
- Priority CVE data retrieval (CRITICAL severity)
- Backfill specific CVE lists
- Parallel fetching within rate limits

**Performance**: 5-10 seconds for 100 CVEs (parallel execution)

---

## Integration Patterns

### Hybrid Reasoning Pattern

Combine Neo4j graph, Qdrant semantic search, and live NVD API.

```python
async def get_cve_intelligence(cve_id: str) -> dict:
    """
    Multi-source CVE intelligence retrieval

    Priority:
    1. Neo4j graph (fastest, includes relationships)
    2. Qdrant vector (semantic context)
    3. Live NVD API (real-time fallback)
    """
    # Try Neo4j first
    neo4j_result = await query_neo4j(f"""
        MATCH (cve:CVE {{cve_id: '{cve_id}'}})
        OPTIONAL MATCH (cve)-[:HAS_WEAKNESS]->(cwe:CWE)
        RETURN cve, collect(cwe) as weaknesses
    """)

    if neo4j_result:
        return {
            "source": "neo4j",
            "data": neo4j_result,
            "relationships": True
        }

    # Fallback to live NVD
    nvd_result = await fetch_live_cve(cve_id)

    return {
        "source": "nvd_live",
        "data": nvd_result,
        "relationships": False,
        "note": "Not yet ingested to Neo4j"
    }
```

### Gap Remediation Workflow

Systematic approach to fixing data gaps.

```python
# Step 1: Identify gaps
gap_2021 = requests.post("http://localhost:8002/nvd/gap-analysis",
                        json={"year": 2021}).json()

print(f"Missing {gap_2021['missing_count']} CVEs from 2021")

# Step 2: Prioritize by severity
high_priority = requests.post("http://localhost:8002/nvd/gap-analysis",
                             json={"year": 2021, "min_cvss": 7.0}).json()

# Step 3: Batch fetch high-priority CVEs
missing_high = high_priority["missing_cves"][:100]
batch_data = requests.post("http://localhost:8002/nvd/batch-fetch",
                          json={"cve_ids": missing_high}).json()

# Step 4: Trigger full re-ingestion for complete coverage
requests.post("http://localhost:8002/ingest/cve",
             json={"year": 2021})
```

### Continuous Monitoring Pattern

Automated delta tracking with ingestion triggers.

```python
import schedule
import time

def monitor_nvd_updates():
    """Hourly check for new CVEs"""
    delta = requests.post("http://localhost:8002/nvd/delta-check",
                         json={"since_hours": 1}).json()

    if delta["total_new"] > 0:
        print(f"Found {delta['total_new']} new CVEs")

        # Check for CRITICAL CVEs
        critical = [cve for cve in delta["new_cves"]
                   if cve["severity"] == "CRITICAL"]

        if critical:
            # Immediate ingestion for CRITICAL
            cve_ids = [cve["cve_id"] for cve in critical]
            requests.post("http://localhost:8002/nvd/batch-fetch",
                         json={"cve_ids": cve_ids})

            # Alert notification
            notify_security_team(critical)

    if delta["total_modified"] > 0:
        print(f"Found {delta['total_modified']} modified CVEs")

# Schedule hourly monitoring
schedule.every().hour.do(monitor_nvd_updates)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Best Practices

### Rate Limit Management

**With API Key (Recommended)**:
- 5000 requests/30 seconds
- Suitable for large-scale operations
- Batch fetch supports up to 100 CVEs in 5-10 seconds

**Without API Key**:
- 50 requests/30 seconds
- Limited to small queries
- Not recommended for production

### Caching Strategy

**Live Lookup**:
- 5-minute TTL for individual CVEs
- Cache hit rate: 70-90% for repeated queries
- Reduces API calls by ~80%

**Gap Analysis**:
- No caching (always fresh comparison)
- Results should be acted upon immediately

**Delta Check**:
- Short-term caching (1 minute) for identical queries
- Prevents duplicate checks in rapid succession

### Error Handling

**404 Not Found**:
```python
try:
    cve = requests.get(f"http://localhost:8002/nvd/live/{cve_id}")
    cve.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print(f"CVE {cve_id} not found in NVD")
```

**503 Service Unavailable**:
```python
# NVD Live Intelligence module not loaded
# Check logs: docker logs neocoder
# Verify nvd_live_client.py is present
```

### Integration with AgentZero

**Tool Definition**:
```python
{
    "name": "nvd_live_lookup",
    "description": "Get real-time CVE intelligence from NVD",
    "endpoint": "http://neocoder:8002/nvd/live/{cve_id}",
    "method": "GET",
    "parameters": {
        "cve_id": {
            "type": "string",
            "description": "CVE identifier (e.g., CVE-2021-44228)",
            "required": True
        }
    }
}
```

**Usage in Agent**:
```python
def analyze_vulnerability(cve_id: str):
    """Agent tool for CVE analysis"""
    cve_data = requests.get(
        f"http://neocoder:8002/nvd/live/{cve_id}"
    ).json()

    return f"""
    CVE: {cve_data['cve_id']}
    Severity: {cve_data['severity']} ({cve_data['cvss_score']})
    Published: {cve_data['published_date']}
    CWE: {', '.join(cve_data['cwe_ids'])}

    Description: {cve_data['description']}
    """
```

---
