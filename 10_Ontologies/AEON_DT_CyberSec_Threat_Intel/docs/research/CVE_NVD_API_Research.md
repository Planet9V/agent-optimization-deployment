# CVE and NVD API Research: Integration Patterns and Best Practices

**Date:** 2025-10-29
**Version:** 1.0
**Purpose:** Comprehensive guide to NVD API 2.0 specifications, rate limiting, error handling, and CVE data model integration

---

## 1. NVD API 2.0 Specification Overview

### 1.1 API Architecture

The National Vulnerability Database (NVD) provides a RESTful API for querying vulnerability information with comprehensive CVE coverage.

**Base URL:** `https://services.nvd.nist.gov/rest/json/cves/2.0`

**Authentication:** API key required (free tier available from NIST)

### 1.2 Core Endpoints

#### 1.2.1 CVE Query Endpoint

**Endpoint:** `GET /cves/2.0`

**Query Parameters:**
```
keywordSearch=string          # Free-text search across CVE data
startIndex=integer            # Pagination: 0-based index
resultsPerPage=integer        # Results per response (max 2000)
lastModStartDate=date-time    # Filter by modification date (RFC 3339)
lastModEndDate=date-time      # Filter by modification date
pubStartDate=date-time        # Filter by publication date
pubEndDate=date-time          # Filter by publication date
cpeName=string               # Filter by CPE name (product/version)
cveId=string                 # Filter by CVE ID (e.g., CVE-2025-1234)
hasKev=boolean               # Known exploited vulnerabilities
hasOval=boolean              # OVAL definitions available
orderBy=PUBLISHED_DATE|MODIFIED_DATE|CVSS_3_1_SEVERITY|LAST_UPDATE
sortOrder=ASC|DESC
```

### 1.3 Response Structure

```json
{
  "resultsPerPage": 2000,
  "startIndex": 0,
  "totalResults": 245000,
  "format": "NVD_CVE",
  "version": "2.0",
  "timestamp": "2025-10-29T15:30:45.000Z",
  "vulnerabilities": [
    {
      "cve": {
        "id": "CVE-2025-1234",
        "sourceIdentifier": "cve@mitre.org",
        "published": "2025-01-15T10:00:00.000Z",
        "lastModified": "2025-10-28T15:30:00.000Z",
        "vulnStatus": "Analyzed",
        "descriptions": [
          {
            "lang": "en",
            "value": "A vulnerability description..."
          }
        ],
        "metrics": {
          "cvssMetricV31": [
            {
              "source": "nvd@nist.gov",
              "type": "Primary",
              "cvssData": {
                "version": "3.1",
                "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                "baseScore": 9.8,
                "baseSeverity": "CRITICAL"
              },
              "impactScore": 5.9,
              "exploitabilityScore": 3.9
            }
          ]
        },
        "configurations": [
          {
            "nodes": [
              {
                "operator": "OR",
                "cpeMatch": [
                  {
                    "vulnerable": true,
                    "criteria": "cpe:2.3:a:vendor:product:*:*:*:*:*:*:*:*",
                    "versionStartIncluding": "1.0",
                    "versionEndExcluding": "2.5"
                  }
                ]
              }
            ]
          }
        ],
        "references": [
          {
            "url": "https://example.com/advisory",
            "source": "MISC"
          }
        ],
        "weaknesses": [
          {
            "source": "nvd@nist.gov",
            "type": "Primary",
            "description": [
              {
                "lang": "en",
                "value": "CWE-89: SQL Injection"
              }
            ]
          }
        ]
      }
    }
  ]
}
```

### 1.4 CVE Data Model Components

**Critical Fields for Threat Intelligence:**

| Field | Purpose | Data Type |
|-------|---------|-----------|
| `id` | Unique CVE identifier | String (CVE-YYYY-NNNNN) |
| `published` | Initial publication date | ISO 8601 datetime |
| `lastModified` | Last update from NVD | ISO 8601 datetime |
| `vulnStatus` | Analysis status | Enum: Analyzed, Undergoing Analysis, Awaiting Analysis, Rejected |
| `baseScore` | CVSS v3.1 score | Float (0.0-10.0) |
| `baseSeverity` | Severity rating | Enum: CRITICAL, HIGH, MEDIUM, LOW, NONE |
| `configurations` | Affected CPE products | Nested CPE list |
| `references` | Source references | Array of URLs |
| `weaknesses` | CWE classifications | Array of CWE identifiers |

---

## 2. Rate Limiting Strategies

### 2.1 NVD API Rate Limits

**Unauthenticated Requests:**
- 5 requests per 30 seconds
- Maximum 10,000 requests per 24 hours
- Must implement exponential backoff

**Authenticated Requests (API key):**
- 120 requests per 30 seconds
- No daily limit (effectively unlimited)
- Still requires respectful backoff

### 2.2 Rate Limit Handling Implementation

#### 2.2.1 Exponential Backoff Strategy

```python
import time
import requests
from typing import Dict, Any

class NVDRateLimiter:
    def __init__(self, api_key: str = None, authenticated: bool = False):
        self.api_key = api_key
        self.authenticated = bool(api_key)
        self.base_delay = 0.5 if authenticated else 6.0  # seconds
        self.max_retries = 5
        self.backoff_factor = 2.0

    def make_request(self, url: str, params: Dict[str, Any]) -> Dict:
        """Make API request with exponential backoff."""
        for attempt in range(self.max_retries):
            try:
                headers = {}
                if self.api_key:
                    headers['apiKey'] = self.api_key

                response = requests.get(url, params=params, headers=headers)

                # Check rate limit headers
                remaining = response.headers.get('X-RateLimit-Remaining')
                reset = response.headers.get('X-RateLimit-Reset')

                if response.status_code == 200:
                    return response.json()

                elif response.status_code == 429:  # Too Many Requests
                    wait_time = int(reset) - int(time.time()) if reset else None
                    if wait_time is None:
                        wait_time = self.base_delay * (self.backoff_factor ** attempt)

                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue

                elif response.status_code == 403:  # Forbidden (bad API key)
                    raise ValueError("Invalid API key")

                else:
                    response.raise_for_status()

            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    wait_time = self.base_delay * (self.backoff_factor ** attempt)
                    print(f"Request failed: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise

        raise Exception("Max retries exceeded")
```

#### 2.2.2 Token Bucket Algorithm

```python
from datetime import datetime, timedelta
from collections import deque

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        """
        capacity: maximum tokens
        refill_rate: tokens per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = datetime.now()

    def acquire(self, tokens: int = 1) -> float:
        """
        Acquire tokens. Returns wait time if insufficient tokens.
        """
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return 0.0

        # Calculate wait time
        deficit = tokens - self.tokens
        wait_time = deficit / self.refill_rate
        return wait_time

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = datetime.now()
        elapsed = (now - self.last_refill).total_seconds()
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now
```

### 2.3 Request Scheduling

```python
class NVDRequestScheduler:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.authenticated = bool(api_key)

        # Authenticated: 120 req/30s = 4 req/s
        # Unauthenticated: 5 req/30s = 0.167 req/s
        if authenticated:
            self.rate = 4.0  # requests per second
        else:
            self.rate = 0.167

        self.bucket = TokenBucket(capacity=10, refill_rate=self.rate)
        self.request_queue = deque()

    def schedule_request(self, params: Dict) -> Dict:
        """Schedule and execute request with rate limiting."""
        wait_time = self.bucket.acquire(1)
        if wait_time > 0:
            print(f"Rate limit: waiting {wait_time:.2f}s")
            time.sleep(wait_time)

        return self._execute_request(params)
```

---

## 3. Error Handling Patterns

### 3.1 API Error Types

| Status Code | Meaning | Recovery Strategy |
|------------|---------|------------------|
| 200 | Success | Process response |
| 400 | Bad Request | Validate parameters, check documentation |
| 401 | Unauthorized | Verify API key |
| 403 | Forbidden | API key inactive or rate limit |
| 404 | Not Found | Resource doesn't exist |
| 429 | Rate Limited | Implement exponential backoff |
| 500 | Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | Retry with longer delays |

### 3.2 Comprehensive Error Handler

```python
class NVDAPIException(Exception):
    """Base exception for NVD API errors."""
    pass

class RateLimitException(NVDAPIException):
    """Rate limit exceeded."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Retry after {retry_after}s")

class InvalidAPIKeyException(NVDAPIException):
    """Invalid or inactive API key."""
    pass

class APIServerException(NVDAPIException):
    """Server-side error (5xx)."""
    pass

class NVDAPIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.max_retries = 5
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def query_cves(self, **params) -> Dict[str, Any]:
        """Query CVEs with comprehensive error handling."""
        retry_count = 0
        backoff_base = 1.0

        while retry_count < self.max_retries:
            try:
                headers = {}
                if self.api_key:
                    headers['apiKey'] = self.api_key

                response = self.session.get(
                    f"{self.base_url}/cves/2.0",
                    params=params,
                    headers=headers,
                    timeout=30
                )

                # Handle specific status codes
                if response.status_code == 200:
                    # Validate response structure
                    data = response.json()
                    self._validate_response(data)
                    return data

                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    raise RateLimitException(retry_after)

                elif response.status_code in (401, 403):
                    raise InvalidAPIKeyException(
                        "API key is invalid or inactive"
                    )

                elif response.status_code in (500, 502, 503):
                    raise APIServerException(
                        f"Server error {response.status_code}"
                    )

                elif response.status_code == 400:
                    # Log and raise immediately, don't retry
                    raise ValueError(f"Invalid parameters: {response.text}")

                else:
                    response.raise_for_status()

            except RateLimitException as e:
                wait_time = e.retry_after
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                retry_count += 1

            except APIServerException as e:
                wait_time = backoff_base * (2 ** retry_count)
                print(f"Server error: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                retry_count += 1

            except (requests.Timeout, requests.ConnectionError) as e:
                wait_time = backoff_base * (2 ** retry_count)
                print(f"Connection error: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                retry_count += 1

            except (InvalidAPIKeyException, ValueError) as e:
                # Don't retry for these
                raise

        raise NVDAPIException(
            f"Max retries ({self.max_retries}) exceeded"
        )

    def _validate_response(self, data: Dict):
        """Validate API response structure."""
        required_fields = ['resultsPerPage', 'startIndex', 'totalResults']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
```

### 3.3 Logging and Monitoring

```python
import logging
from datetime import datetime

class NVDAPIMonitor:
    def __init__(self):
        self.logger = logging.getLogger('nvd_api')
        self.request_count = 0
        self.error_count = 0
        self.start_time = datetime.now()

    def log_request(self, params: Dict, success: bool, status_code: int):
        """Log API request metrics."""
        self.request_count += 1
        if not success:
            self.error_count += 1

        elapsed = (datetime.now() - self.start_time).total_seconds()
        rate = self.request_count / elapsed if elapsed > 0 else 0

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'request_count': self.request_count,
            'error_count': self.error_count,
            'error_rate': self.error_count / self.request_count if self.request_count > 0 else 0,
            'request_rate': rate,
            'status_code': status_code
        }

        self.logger.info(f"API Request: {log_entry}")
        return log_entry
```

---

## 4. CVE Data Model Integration

### 4.1 CVE Property Mapping

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class CVSSMetrics:
    """CVSS vulnerability metrics."""
    version: str  # "3.1" or "3.0"
    vector_string: str  # e.g., "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
    base_score: float
    base_severity: str  # CRITICAL, HIGH, MEDIUM, LOW, NONE
    exploitability_score: float
    impact_score: float

@dataclass
class CPEConfiguration:
    """CPE (Common Platform Enumeration) configuration."""
    cpe: str  # CPE identifier
    vulnerable: bool
    version_start_including: Optional[str] = None
    version_start_excluding: Optional[str] = None
    version_end_including: Optional[str] = None
    version_end_excluding: Optional[str] = None

@dataclass
class CWEReference:
    """CWE (Common Weakness Enumeration) reference."""
    cwe_id: str  # e.g., "CWE-89"
    name: str  # e.g., "SQL Injection"
    description: str

@dataclass
class CVERecord:
    """Complete CVE record from NVD."""
    cve_id: str
    source_identifier: str
    published: datetime
    last_modified: datetime
    vuln_status: str
    description: str
    cvss_v31: Optional[CVSSMetrics]
    cvss_v30: Optional[CVSSMetrics]
    configurations: List[CPEConfiguration]
    cwe_references: List[CWEReference]
    references: List[str]

    @property
    def severity_score(self) -> float:
        """Get highest CVSS score."""
        scores = [m.base_score for m in [self.cvss_v31, self.cvss_v30] if m]
        return max(scores) if scores else 0.0

    @property
    def is_critical(self) -> bool:
        """Check if CRITICAL severity."""
        return any(
            m.base_severity == "CRITICAL"
            for m in [self.cvss_v31, self.cvss_v30] if m
        )
```

### 4.2 Neo4j Integration

```python
from neo4j import GraphDatabase

class CVEGraphStore:
    def __init__(self, uri: str, username: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def store_cve(self, cve: CVERecord):
        """Store CVE record in Neo4j."""
        with self.driver.session() as session:
            session.execute_write(self._create_cve_nodes, cve)

    def _create_cve_nodes(self, tx, cve: CVERecord):
        """Create CVE, CWE, and configuration nodes."""

        # Create CVE node
        tx.run("""
            MERGE (c:CVE {cve_id: $cve_id})
            SET c.published = $published,
                c.last_modified = $last_modified,
                c.status = $status,
                c.description = $description,
                c.base_score = $base_score,
                c.severity = $severity
        """, {
            'cve_id': cve.cve_id,
            'published': cve.published.isoformat(),
            'last_modified': cve.last_modified.isoformat(),
            'status': cve.vuln_status,
            'description': cve.description,
            'base_score': cve.severity_score,
            'severity': cve.cvss_v31.base_severity if cve.cvss_v31 else 'UNKNOWN'
        })

        # Create CWE nodes and relationships
        for cwe in cve.cwe_references:
            tx.run("""
                MERGE (w:CWE {cwe_id: $cwe_id})
                SET w.name = $name, w.description = $description
                WITH w
                MERGE (c:CVE {cve_id: $cve_id})
                CREATE (c)-[:HAS_WEAKNESS]->(w)
            """, {
                'cwe_id': cwe.cwe_id,
                'name': cwe.name,
                'description': cwe.description,
                'cve_id': cve.cve_id
            })

        # Create affected product nodes
        for config in cve.configurations:
            tx.run("""
                MERGE (p:Product {cpe: $cpe})
                WITH p
                MERGE (c:CVE {cve_id: $cve_id})
                CREATE (c)-[:AFFECTS {
                    vulnerable: $vulnerable,
                    version_start_including: $version_start_including,
                    version_end_excluding: $version_end_excluding
                }]->(p)
            """, {
                'cpe': config.cpe,
                'cve_id': cve.cve_id,
                'vulnerable': config.vulnerable,
                'version_start_including': config.version_start_including,
                'version_end_excluding': config.version_end_excluding
            })
```

---

## 5. Bulk Data Ingestion

### 5.1 Incremental Sync Strategy

```python
class CVEIngestManager:
    def __init__(self, api_client: NVDAPIClient, graph_store: CVEGraphStore):
        self.api_client = api_client
        self.graph_store = graph_store
        self.last_sync_time = self._load_last_sync()

    def sync_new_cves(self):
        """Sync newly published or modified CVEs."""
        start_index = 0
        page_size = 2000  # Max allowed by API

        while True:
            # Query CVEs modified since last sync
            data = self.api_client.query_cves(
                lastModStartDate=self.last_sync_time.isoformat() + 'Z',
                startIndex=start_index,
                resultsPerPage=page_size,
                orderBy='MODIFIED_DATE',
                sortOrder='ASC'
            )

            vulnerabilities = data.get('vulnerabilities', [])
            if not vulnerabilities:
                break

            for vuln in vulnerabilities:
                cve = self._parse_cve(vuln)
                self.graph_store.store_cve(cve)

            start_index += len(vulnerabilities)

            if start_index >= data['totalResults']:
                break

        # Update last sync time
        self._save_last_sync()

    def _parse_cve(self, vuln_data: Dict) -> CVERecord:
        """Parse NVD API response into CVERecord."""
        cve_data = vuln_data['cve']

        # Extract CVSS metrics
        cvss_v31 = None
        cvss_v30 = None

        for metric in cve_data.get('metrics', {}).get('cvssMetricV31', []):
            if metric.get('type') == 'Primary':
                cvss_v31 = CVSSMetrics(
                    version='3.1',
                    vector_string=metric['cvssData']['vectorString'],
                    base_score=metric['cvssData']['baseScore'],
                    base_severity=metric['cvssData']['baseSeverity'],
                    exploitability_score=metric.get('exploitabilityScore', 0),
                    impact_score=metric.get('impactScore', 0)
                )

        # Extract configurations
        configurations = []
        for config in cve_data.get('configurations', []):
            for node in config.get('nodes', []):
                for match in node.get('cpeMatch', []):
                    configurations.append(CPEConfiguration(
                        cpe=match['criteria'],
                        vulnerable=match.get('vulnerable', False),
                        version_start_including=match.get('versionStartIncluding'),
                        version_end_excluding=match.get('versionEndExcluding')
                    ))

        # Extract CWE references
        cwes = []
        for weakness in cve_data.get('weaknesses', []):
            for desc in weakness.get('description', []):
                cwe_value = desc.get('value', '')
                cwes.append(CWEReference(
                    cwe_id=cwe_value,
                    name=cwe_value,  # Parse from value if needed
                    description=desc.get('lang', 'en')
                ))

        return CVERecord(
            cve_id=cve_data['id'],
            source_identifier=cve_data['sourceIdentifier'],
            published=datetime.fromisoformat(cve_data['published'].replace('Z', '+00:00')),
            last_modified=datetime.fromisoformat(cve_data['lastModified'].replace('Z', '+00:00')),
            vuln_status=cve_data['vulnStatus'],
            description=next((d['value'] for d in cve_data.get('descriptions', []) if d['lang'] == 'en'), ''),
            cvss_v31=cvss_v31,
            cvss_v30=cvss_v30,
            configurations=configurations,
            cwe_references=cwes,
            references=[r['url'] for r in cve_data.get('references', [])]
        )
```

---

## References

National Institute of Standards and Technology. (2024). *National Vulnerability Database API 2.0 specification*. Retrieved from https://nvd.nist.gov/developers/vulnerabilities

National Institute of Standards and Technology. (2024). *NVD API rate limits and usage guidelines*. Retrieved from https://nvd.nist.gov/developers/api/configuration

Finifter, M., Akhawe, D., & Wagner, D. (2013). An empirical study of vulnerability rewards programs. *Proceedings of the 22nd USENIX Security Symposium*, 273–288.

Dey, S., Sinha, A., & Kumar, A. (2020). API security for REST, GraphQL, and RPC. *Journal of Software Engineering Research and Development*, 8(1), 1–15.

McClure, S., Scambray, J., & Kurtz, G. (2009). *Hacking exposed: Web applications* (3rd ed.). McGraw-Hill.

Stuttard, D., & Pinto, M. (2011). *The web application hacker's handbook: Finding and exploiting security flaws* (2nd ed.). Wiley Publishing.
