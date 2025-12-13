# AEON API Quick Start Guide

**Last Updated:** 2025-12-13
**API Version:** 3.3.0

## Prerequisites

- AEON backend running on `http://localhost:8000`
- Customer ID for authentication
- curl or HTTP client installed

## Authentication

All API requests require the `X-Customer-ID` header:

```bash
curl -H "X-Customer-ID: your-customer-id" \
     http://localhost:8000/api/v2/sbom/sboms
```

## Getting Started

### 1. Check System Health

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "3.3.0",
  "services": {
    "neo4j": "connected",
    "qdrant": "connected"
  }
}
```

### 2. View API Documentation

Open interactive API docs in your browser:
```
http://localhost:8000/docs
```

Or download OpenAPI spec:
```bash
curl http://localhost:8000/openapi.json > openapi.json
```

---

## Common Use Cases

### SBOM Management

#### List all SBOMs
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/sbom/sboms
```

#### Create new SBOM
```bash
curl -X POST \
     -H "X-Customer-ID: customer123" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "myapp-v1.0",
       "version": "1.0.0",
       "format": "cyclonedx"
     }' \
     http://localhost:8000/api/v2/sbom/sboms
```

#### Get SBOM details
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/sbom/sboms/{sbom_id}
```

#### Find vulnerable components
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/sbom/components/vulnerable
```

#### Get critical vulnerabilities
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/sbom/vulnerabilities/critical
```

### Threat Intelligence

#### Search threat actors
```bash
curl -H "X-Customer-ID: customer123" \
     "http://localhost:8000/api/v2/threat-intel/actors/search?q=APT29"
```

#### Get active campaigns
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/threat-intel/campaigns/active
```

#### Get threat dashboard
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/threat-intel/dashboard/summary
```

### Risk Management

#### Get high-risk entities
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/risk/scores/high-risk
```

#### Get risk matrix
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/risk/dashboard/risk-matrix
```

#### List internet-facing assets
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/risk/exposure/internet-facing
```

### Compliance

#### Get compliance dashboard
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/compliance/dashboard/summary
```

#### List controls for framework
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/compliance/controls/by-framework/NIST-CSF
```

#### Identify compliance gaps
```bash
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/compliance/gaps/critical
```

### Alerts

#### Get active alerts
```bash
curl -H "X-Customer-ID: customer123" \
     "http://localhost:8000/api/v2/alerts/by-status/active"
```

#### Get critical alerts
```bash
curl -H "X-Customer-ID: customer123" \
     "http://localhost:8000/api/v2/alerts/by-severity/critical"
```

#### Acknowledge alert
```bash
curl -X POST \
     -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/alerts/{alert_id}/acknowledge
```

### Search

#### Semantic search
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
       "query": "ransomware attacks",
       "limit": 10
     }' \
     http://localhost:8000/search/semantic
```

#### Hybrid search (semantic + keyword)
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
       "query": "critical CVEs",
       "limit": 20
     }' \
     http://localhost:8000/search/hybrid
```

#### Named Entity Recognition
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Microsoft Azure vulnerability CVE-2023-1234 affects authentication"
     }' \
     http://localhost:8000/ner
```

---

## Pagination

Most list endpoints support pagination:

```bash
curl -H "X-Customer-ID: customer123" \
     "http://localhost:8000/api/v2/sbom/sboms?skip=0&limit=50"
```

Parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

---

## Filtering

Common filter parameters:

```bash
# By severity
?severity=critical

# By status
?status=active

# By date range
?start_date=2025-01-01&end_date=2025-12-31

# Search
?q=search_term
```

---

## Sorting

```bash
# Sort by field (ascending)
?sort_by=created_at&sort_order=asc

# Sort by field (descending)
?sort_by=risk_score&sort_order=desc
```

---

## Error Handling

### Common Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Missing X-Customer-ID |
| 404 | Not Found | Resource doesn't exist |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | Internal error |

### Error Response Format

```json
{
  "detail": "Error description",
  "error": "Technical error message"
}
```

---

## Rate Limiting

- **Limit:** 1000 requests/hour per customer
- **Burst:** Up to 100 requests/minute

Rate limit headers in response:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1702468800
```

---

## JavaScript/TypeScript Example

```typescript
const API_BASE = 'http://localhost:8000';
const CUSTOMER_ID = 'customer123';

const headers = {
  'X-Customer-ID': CUSTOMER_ID,
  'Content-Type': 'application/json'
};

// Fetch SBOMs
async function getSBOMs() {
  const response = await fetch(`${API_BASE}/api/v2/sbom/sboms`, {
    headers
  });
  return response.json();
}

// Search threats
async function searchThreats(query: string) {
  const response = await fetch(
    `${API_BASE}/api/v2/threat-intel/actors/search?q=${query}`,
    { headers }
  );
  return response.json();
}

// Semantic search
async function semanticSearch(query: string) {
  const response = await fetch(`${API_BASE}/search/semantic`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ query, limit: 10 })
  });
  return response.json();
}
```

---

## Python Example

```python
import requests

API_BASE = 'http://localhost:8000'
CUSTOMER_ID = 'customer123'

headers = {
    'X-Customer-ID': CUSTOMER_ID,
    'Content-Type': 'application/json'
}

# Fetch SBOMs
def get_sboms():
    response = requests.get(
        f'{API_BASE}/api/v2/sbom/sboms',
        headers=headers
    )
    return response.json()

# Search threats
def search_threats(query):
    response = requests.get(
        f'{API_BASE}/api/v2/threat-intel/actors/search',
        headers=headers,
        params={'q': query}
    )
    return response.json()

# Semantic search
def semantic_search(query):
    response = requests.post(
        f'{API_BASE}/search/semantic',
        headers=headers,
        json={'query': query, 'limit': 10}
    )
    return response.json()

# Usage
sboms = get_sboms()
threats = search_threats('APT29')
results = semantic_search('ransomware')
```

---

## Next Steps

1. **Explore Full API:** See [COMPLETE_API_REFERENCE.md](./COMPLETE_API_REFERENCE.md) for all 230 endpoints
2. **Interactive Docs:** Visit http://localhost:8000/docs for Swagger UI
3. **OpenAPI Spec:** Download from http://localhost:8000/openapi.json
4. **Integration:** Check backend connection patterns in [BACKEND_CONNECTION_PATTERNS.md](./BACKEND_CONNECTION_PATTERNS.md)

---

## Support

- **Documentation:** [Complete API Reference](./COMPLETE_API_REFERENCE.md)
- **Backend Setup:** [Docker Quick Start](../../DOCKER_QUICK_START.md)
- **System Health:** [Backend Quick Reference](./BACKEND_QUICK_REFERENCE.md)

---

**Generated:** 2025-12-13
**API Version:** 3.3.0
**Guide Version:** 1.0.0
