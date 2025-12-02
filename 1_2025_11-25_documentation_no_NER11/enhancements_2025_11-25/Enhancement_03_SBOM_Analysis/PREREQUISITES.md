# PREREQUISITES - SBOM Dependency Analysis Enhancement

**File**: `PREREQUISITES.md`
**Created**: 2025-11-25 14:45:00 UTC
**Modified**: 2025-11-25 14:45:00 UTC
**Version**: v1.0.0
**Author**: Infrastructure & Integration Team
**Purpose**: Complete specification of prerequisites and dependencies for SBOM analysis system
**Status**: ACTIVE

## System Requirements

### Compute Environment

#### Minimum Specifications
```yaml
CPU:
  cores: 4
  architecture: "x86_64"
  frequency: "2.0 GHz minimum"

Memory:
  ram: "8 GB minimum"
  heap_size: "4 GB default (configurable)"
  swap: "2 GB minimum"

Storage:
  sbom_cache: "5 GB"
  cve_database: "10 GB"
  logs_reports: "20 GB"
  total: "35 GB minimum"
```

#### Recommended Specifications
```yaml
CPU:
  cores: 8+
  architecture: "x86_64 with AVX support"
  frequency: "3.0 GHz or higher"

Memory:
  ram: "32 GB"
  heap_size: "16 GB"
  swap: "8 GB"

Storage:
  sbom_cache: "20 GB (SSD)"
  cve_database: "30 GB (SSD)"
  logs_reports: "50 GB (HDD)"
  total: "100 GB"
```

### Network Requirements

#### Connectivity
- **Internet**: Stable, non-filtered connection
- **Bandwidth**: 10 Mbps minimum for CVE data updates
- **Latency**: < 500ms average to API endpoints
- **Outbound Access**: Required to following domains

#### Required External Services
```
API Endpoints:
  registry.npmjs.org (npm registry)
  pypi.org (PyPI API)
  services.nvd.nist.gov (NVD API)
  api.github.com (GHSA and GH advisories)
  openssf.org (OSV database)
  first.org (EPSS scores)

DNS Resolution: Required
TLS/HTTPS: Required (enforced)
Proxy Support: Optional but documented
```

#### Firewall Rules
```
Outbound Rules Required:
  https://registry.npmjs.org/* (443)
  https://pypi.org/* (443)
  https://api.github.com/* (443)
  https://services.nvd.nist.gov/* (443)
  https://api.osv.dev/* (443)
  https://first.org/* (443)

Inbound Rules: None required (server mode optional)
```

---

## Software Dependencies

### Runtime Environment

#### Python (Recommended Option 1)
```yaml
Python:
  version: "3.9, 3.10, 3.11, or 3.12"
  installation: "https://www.python.org/downloads/"
  package_manager: "pip 21.0+"

Required Packages:
  requests: ">=2.28.0"          # HTTP client for APIs
  pydantic: ">=1.9.0"           # Data validation
  jsonschema: ">=4.0.0"         # Schema validation
  defusedxml: ">=0.0.13"        # Safe XML parsing
  beautifulsoup4: ">=4.11.0"    # HTML/XML parsing
  semver: ">=3.0.0"             # Semantic versioning
  python-dateutil: ">=2.8.0"    # Date handling
  cachetools: ">=5.2.0"         # Caching utilities
  pytest: ">=7.0.0"             # Testing (dev)
  pytest-cov: ">=4.0.0"         # Coverage (dev)

Virtual Environment:
  tool: "venv (built-in) or poetry"
  isolation: "Required"
```

#### Node.js (Recommended Option 2)
```yaml
Node.js:
  version: "16 LTS, 18 LTS, or 20 LTS"
  installation: "https://nodejs.org/"
  package_manager: "npm 8+ or yarn 3+"

Required Packages:
  axios: "^1.2.0"                # HTTP client
  @types/node: "^18.0.0"         # TypeScript types (optional)
  jsonschema: "^4.17.0"          # Schema validation
  semver: "^7.3.0"               # Version parsing
  date-fns: "^2.29.0"            # Date utilities
  chalk: "^4.1.0"                # CLI colors
  commander: "^9.4.0"            # CLI framework
  jest: "^29.0.0"                # Testing (dev)
  @types/jest: "^29.0.0"         # TS types (dev)
```

### Optional Database Backends

#### PostgreSQL (Recommended for Production)
```yaml
PostgreSQL:
  version: "12+ (13, 14, 15, 16 recommended)"
  purpose: "CVE data caching and SBOM history"

Installation:
  ubuntu: "sudo apt-get install postgresql-15"
  macos: "brew install postgresql@15"
  windows: "PostgreSQL installer from postgresql.org"
  docker: "docker pull postgres:15"

Required Extensions:
  pg_trgm: "Text search trigram index"
  hstore: "Key-value store (optional)"
  uuid-ossp: "UUID generation"

Configuration:
  max_connections: 20
  shared_buffers: "256MB"
  work_mem: "16MB"
  maintenance_work_mem: "64MB"
```

#### SQLite (Lightweight Alternative)
```yaml
SQLite:
  version: "3.35+ (included in Python 3.9+)"
  purpose: "Single-file database for small deployments"

Advantages:
  - No installation required
  - File-based portability
  - Suitable for local development
  - Zero configuration

Limitations:
  - Single concurrent writer only
  - Slower for very large datasets (100K+ CVEs)
  - Not suitable for distributed deployments
```

#### Redis (Optional Cache Layer)
```yaml
Redis:
  version: "6.2+ (7.0 recommended)"
  purpose: "In-memory cache for API responses and sessions"

Installation:
  ubuntu: "sudo apt-get install redis-server"
  macos: "brew install redis"
  docker: "docker pull redis:7-alpine"

Configuration:
  maxmemory: "2GB"
  maxmemory-policy: "allkeys-lru"
  timeout: "0"
  tcp-backlog: "511"
```

---

## SBOM Input Format Specifications

### Supported Format Matrix

| Format | Extension | Version | Support Level | Priority |
|--------|-----------|---------|---|---|
| CycloneDX JSON | .json | 1.3, 1.4 | FULL | HIGH |
| CycloneDX XML | .xml | 1.3, 1.4 | FULL | HIGH |
| SPDX JSON | .json | 2.2, 2.3 | FULL | HIGH |
| SPDX RDF/XML | .rdf, .xml | 2.2 | FULL | HIGH |
| npm package.json | package.json | any | FULL | HIGH |
| npm package-lock.json | package-lock.json | 1, 2, 3 | FULL | HIGH |
| Python requirements.txt | requirements.txt | PEP 440 | FULL | HIGH |
| Python poetry.lock | poetry.lock | 1.1+ | FULL | MEDIUM |
| pip-audit output | .json | any version | FULL | MEDIUM |
| cyclonedx-python | .json | 1.4 | FULL | MEDIUM |

### Format-Specific Input Specifications

#### CycloneDX JSON (Recommended)
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "serialNumber": "urn:uuid:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "version": 1,
  "metadata": {
    "timestamp": "2025-11-25T14:45:00Z",
    "tools": [
      {
        "vendor": "AEON-DT",
        "name": "sbom-generator",
        "version": "1.0.0"
      }
    ]
  },
  "components": [
    {
      "bom-ref": "pkg:npm/react@18.2.0",
      "type": "library",
      "name": "react",
      "version": "18.2.0",
      "purl": "pkg:npm/react@18.2.0",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "dependencies": [
        {
          "ref": "pkg:npm/loose-envify@1.4.0"
        }
      ]
    }
  ]
}
```

**File Size Limit**: 500 MB
**Component Count Limit**: 100,000+
**Required Fields**:
- bomFormat: "CycloneDX"
- specVersion: "1.3" or "1.4"
- components: Array of components

#### npm package.json + package-lock.json
```json
{
  "name": "aeon-dt-backend",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.1",
    "axios": "^1.2.0",
    "dotenv": "^16.0.3"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0"
  }
}
```

**Combined File Size**: < 100 MB
**Lock File Required**: Yes (for exact versions)
**Node Version**: Compatible with project's Node version

#### Python requirements.txt
```
# Production dependencies
django==4.1.3
requests==2.28.1
sqlalchemy==2.0.0
pydantic>=1.9.0,<2.0.0

# Optional dependencies
redis[hiredis]>=4.0.0

# Development dependencies (optional)
pytest==7.2.0
black==22.12.0
```

**File Size**: < 1 MB
**Format**: PEP 440 compliant
**Lock File Recommended**: Use pip-compile or poetry.lock for exact versions

---

## CVE Database Requirements

### NVD (National Vulnerability Database)

#### API Access
```yaml
Endpoint: "https://services.nvd.nist.gov/rest/json"
Format: "JSON REST API"
Rate Limit: "120 requests / 120 seconds (with API key)"
            "10 requests / 60 seconds (without API key)"
Authentication: "Optional API key increases limits"

API Key Registration:
  url: "https://nvd.nist.gov/developers/request-an-api-key"
  time_to_approval: "Immediate (within seconds)"
  cost: "Free"
  validity: "Unlimited"
```

#### Data Coverage
```yaml
Coverage:
  total_cves: "216,000+"
  datasources: ["CVE Numbering Authorities", "Vendors", "Security Research"]
  update_frequency: "Daily"
  avg_cves_per_day: "100-200"

Required Fields:
  - CVE ID
  - Affected versions (regex patterns)
  - CVSS 2.0 score (deprecated but available)
  - CVSS 3.0/3.1 score and vector
  - CWE references
  - References and links
  - Description
```

### OSV (Open Source Vulnerabilities)

#### API Access
```yaml
Endpoint: "https://api.osv.dev/v1"
Format: "JSON REST API"
Rate Limit: "No documented limit (fair use)"
Authentication: "None required"
Data Source: "Aggregate from multiple sources"

Database Query Methods:
  1. Query by package (ecosystem + name + version)
  2. Query by CVE ID
  3. Query by commit hash
  4. Batch queries supported
```

#### Data Coverage
```yaml
Coverage:
  total_advisories: "110,000+"
  ecosystems:
    - npm
    - PyPI
    - RubyGems
    - Maven
    - NuGet
    - Go
    - Pub
    - Composer
    - Packagist
    - Conan
    - Conda
    - Crates.io
  update_frequency: "Real-time"

Data Format Example:
{
  "id": "GHSA-3xgq-45jh-mhpw",
  "published": "2021-05-05T...",
  "withdrawn": null,
  "affected": [{
    "package": {
      "ecosystem": "npm",
      "name": "is-my-json-valid"
    },
    "ranges": [{
      "type": "SEMVER",
      "events": [
        {"introduced": "0"},
        {"fixed": "1.3.2"}
      ]
    }]
  }],
  "references": [...],
  "summary": "Regular expression DoS",
  "details": "..."
}
```

### GHSA (GitHub Security Advisories)

#### API Access
```yaml
Endpoint: "https://api.github.com/graphql"
Format: "GraphQL API"
Authentication: "GitHub token required (free tier sufficient)"
Rate Limit: "5,000 points per hour with token"

Token Requirements:
  type: "Personal Access Token (PAT)"
  scopes: "public_repo (read-only)"
  creation: "GitHub Settings > Developer settings > Personal access tokens"
  lifetime: "90 days (configurable)"
  cost: "Free"

GraphQL Query Example:
query {
  search(first: 100, type: REPOSITORY, query: "is:react") {
    nodes {
      ... on Repository {
        securityAdvisories(first: 10) {
          nodes {
            ghsaId
            cvss {
              score
              vectorString
            }
            references {
              url
            }
          }
        }
      }
    }
  }
}
```

#### Data Coverage
```yaml
Coverage:
  advisories: "45,000+"
  ecosystems: ["npm", "PyPI", "RubyGems", "Maven", "Go", "NuGet"]
  update_frequency: "Real-time (within minutes)"
  data_quality: "High (GitHub-curated)"
```

### EPSS (Exploit Prediction Scoring System)

#### Data Access
```yaml
Provider: "FIRST (Forum of Incident Response and Security Teams)"
Endpoint: "https://api.first.org/data/v1/epss"
Format: "JSON CSV Download"
Update Frequency: "Daily"
Historical Data: "Complete historical scores available"

Access Methods:
  1. Daily CSV download: "epss_scores-{date}.csv"
  2. REST API (beta): "Query individual CVEs"
  3. Bulk database: "Full dataset for offline use"

Registration:
  required: "Yes (free)"
  url: "https://www.first.org/epss"
  time_to_approval: "1-2 business days"
  cost: "Free"

CSV Format:
cve,epss,percentile,date
CVE-2021-43565,0.8945,96,2025-11-24
CVE-2021-44228,0.9677,99,2025-11-24
```

---

## Package Registry Integration

### npm Registry

#### API Endpoints
```yaml
Endpoints:
  metadata: "https://registry.npmjs.org/{package}"
  search: "https://registry.npmjs.org/-/search"
  package_list: "https://registry.npmjs.org/-/all"

Rate Limits:
  queries: "Unlimited (but respect server load)"
  concurrent: "10 parallel requests recommended"
  timeout: "30 seconds per request"
  backoff: "Exponential (1s, 2s, 4s, 8s max)"

Authentication: "None required (public API)"

Data Returned:
  - Package metadata (license, homepage, etc)
  - All published versions
  - Tarball checksums (sha512)
  - Dependency specifications
  - Maintainers and collaborators
  - Download statistics
  - Deprecation status
  - Last publish date
```

### PyPI API

#### REST Endpoints
```yaml
Endpoints:
  package_info: "https://pypi.org/pypi/{package}/json"
  project_files: "https://pypi.org/pypi/{package}/{version}/json"
  search: "https://pypi.org/pypi?:action=search&q={query}&c={classifier}"

Rate Limits:
  queries: "Unlimited"
  concurrent: "5 parallel requests recommended"
  timeout: "30 seconds"
  user_agent: "Required (identifying user/script)"

Authentication: "None required"

Data Structure:
{
  "info": {
    "name": "django",
    "version": "4.1.3",
    "author": "Django Software Foundation",
    "license": "BSD",
    "classifiers": ["Development Status :: 5 - Production/Stable"],
    "requires_python": ">=3.8",
    "requires_dist": [
      "sqlparse (>=0.2.2)",
      "asgiref (<4,>=3.5.2)"
    ]
  },
  "releases": {
    "4.1.3": [{...}],
    "4.1.2": [{...}]
  }
}
```

---

## Storage & Caching Infrastructure

### Database Schema Requirements

#### CVE Cache Table
```sql
CREATE TABLE cve_cache (
  id SERIAL PRIMARY KEY,
  cve_id VARCHAR(20) UNIQUE NOT NULL,
  package_id VARCHAR(255),
  cvss_score DECIMAL(4,1),
  cvss_vector VARCHAR(100),
  epss_score DECIMAL(5,4),
  epss_percentile INTEGER,
  affected_versions JSONB,
  remediation_available BOOLEAN,
  remediated_in VARCHAR(50),
  source VARCHAR(20),  -- 'nvd', 'osv', 'ghsa'
  last_updated TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_cve_id (cve_id),
  INDEX idx_package_id (package_id),
  INDEX idx_cvss_score (cvss_score DESC),
  INDEX idx_epss_score (epss_score DESC)
);
```

#### SBOM History Table
```sql
CREATE TABLE sbom_analysis_history (
  id SERIAL PRIMARY KEY,
  sbom_file_hash VARCHAR(64) UNIQUE,
  analysis_date TIMESTAMP,
  total_packages INTEGER,
  direct_dependencies INTEGER,
  transitive_dependencies INTEGER,
  vulnerability_count INTEGER,
  critical_count INTEGER,
  high_count INTEGER,
  medium_count INTEGER,
  low_count INTEGER,
  analysis_duration_seconds FLOAT,
  report_json JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_analysis_date (analysis_date),
  INDEX idx_sbom_hash (sbom_file_hash)
);
```

### Cache Invalidation Strategy
```yaml
CacheExpiry:
  cve_data: 24 hours
  epss_scores: 30 days
  package_metadata: 7 days
  registry_data: 12 hours
  sbom_analysis: Never (historical record)

Manual Invalidation Triggers:
  - New CVE published matching analysis package
  - Package version released after analysis
  - EPSS score update for high-risk CVE
  - Known security incident detected
```

---

## Authentication & Authorization

### Required Credentials

```yaml
APICredentials:
  nvd_api_key:
    source: "https://nvd.nist.gov/developers/request-an-api-key"
    required: "Optional (improves rate limits)"
    storage: ".env file (not git)"
    format: "Plain text string"

  github_token:
    source: "GitHub Settings > Developer settings > Tokens"
    required: "Yes (for GHSA data)"
    scopes: ["public_repo"]
    storage: ".env file (not git)"
    format: "ghp_xxxxxxxxxxxxxxxx"

  first_org_key:
    source: "https://www.first.org/epss"
    required: "Optional (for enhanced EPSS data)"
    storage: ".env file (not git)"
    format: "Plain text API key"

EnvironmentVariableFormat:
  NVD_API_KEY=xxxxx
  GITHUB_TOKEN=ghp_xxxxx
  FIRST_API_KEY=xxxxx
  DATABASE_URL=postgresql://user:pass@localhost/sbom_db
```

---

## Performance & Resource Consumption

### Expected Performance Metrics

| Operation | Avg Time | Max Time | Resource |
|-----------|----------|----------|----------|
| SBOM Parse (100 packages) | 2s | 5s | 50 MB RAM |
| Dependency Resolution (500 trans) | 15s | 30s | 200 MB RAM |
| CVE Lookup (500 packages) | 45s | 120s | 300 MB RAM |
| Risk Scoring (500 vulns) | 5s | 10s | 100 MB RAM |
| Full Analysis (500 packages) | 60s | 180s | 500 MB RAM |

### Scaling Considerations

```yaml
ScalingBottlenecks:
  api_rate_limits:
    issue: "CVE database APIs have rate limits"
    solution: "Implement caching, batch requests, use API keys"
    impact: "Linear growth with package count"

  network_latency:
    issue: "Multiple API calls across registries"
    solution: "Parallel requests, connection pooling"
    impact: "10-50ms per API call"

  database_performance:
    issue: "Large CVE dataset with frequent lookups"
    solution: "Proper indexing, connection pooling"
    impact: "Database becomes bottleneck at 50K+ CVEs"

  memory_usage:
    issue: "Building complete dependency graphs in memory"
    solution: "Streaming processing, chunking large graphs"
    impact: "2GB+ for 5000+ package graphs"
```

---

## Troubleshooting Prerequisites

### Common Issues & Resolution

#### Issue 1: API Rate Limiting
```
Symptom: HTTP 429 Too Many Requests
Cause: Exceeded API rate limits
Resolution:
  1. Implement caching with proper TTL
  2. Register for API keys (improves limits)
  3. Reduce concurrent requests
  4. Implement exponential backoff
  5. Check rate limit headers in response
```

#### Issue 2: Package Registry Connectivity
```
Symptom: Cannot connect to npm/PyPI registry
Cause: Network issues, firewall, DNS
Resolution:
  1. Test: curl https://registry.npmjs.org/react
  2. Check firewall rules allow outbound HTTPS
  3. Verify DNS resolution: nslookup registry.npmjs.org
  4. Try with different DNS server
  5. Check proxy configuration
```

#### Issue 3: Invalid SBOM Format
```
Symptom: "Failed to parse SBOM" error
Cause: Format not recognized or malformed
Resolution:
  1. Validate JSON/XML syntax
  2. Check file against schema
  3. Use online validator: cyclonedx.org/validator/
  4. Check for UTF-8 encoding
  5. Look for BOM or special characters
```

#### Issue 4: Memory Exhaustion
```
Symptom: Out of memory or process killed
Cause: Large SBOM or dependency graph
Resolution:
  1. Increase heap size: --max-old-space-size=4096
  2. Enable streaming/chunking
  3. Process in smaller batches
  4. Add disk-based caching
  5. Profile memory usage
```

---

## Validation Checklist

Before running analysis, verify:

```
System Requirements
  [ ] CPU cores: 4+ available
  [ ] RAM: 8GB+ available
  [ ] Disk: 35GB+ free
  [ ] Network: Stable, 10Mbps+

Software Installation
  [ ] Python 3.9+ installed OR Node.js 16+ installed
  [ ] Required packages installed (pip install -r requirements.txt)
  [ ] Virtual environment activated
  [ ] Database configured (if using PostgreSQL)

Network Connectivity
  [ ] Internet access available
  [ ] DNS resolution working
  [ ] Firewall allows HTTPS (443) outbound
  [ ] All required endpoints reachable

Data & Credentials
  [ ] SBOM file present and valid
  [ ] GitHub token configured (for GHSA)
  [ ] NVD API key configured (optional but recommended)
  [ ] Database credentials configured
  [ ] Write permissions for output directory

Configuration
  [ ] .env file created with required variables
  [ ] Database initialized and accessible
  [ ] Cache directory exists and writable
  [ ] Log directory exists and writable
```

---

**Status**: ACTIVE | **Version**: v1.0.0 | **Last Update**: 2025-11-25 14:45:00 UTC
