# AEON MITRE Query API

Production-ready backend query execution engine for 24 MITRE ATT&CK graph query patterns.

**File:** README.md
**Created:** 2025-11-08
**Version:** v1.0.0
**Status:** ACTIVE

---

## Overview

FastAPI backend service that executes Neo4j Cypher queries for 8 key AEON capability questions with 3 complexity levels each (Simple, Intermediate, Advanced) = 24 total query patterns.

### 8 Key Capabilities

1. **CVE Impact Analysis** - Does this CVE impact my equipment?
2. **Attack Path Discovery** - Is there an attack path to vulnerability?
3. **Today's CVE Impact** - Does new CVE today impact facility equipment?
4. **Threat Actor Pathways** - Pathway for threat actor to vulnerability?
5. **CVE Threat Landscape** - For CVE today, pathway for threat actor?
6. **Equipment Inventory** - How many pieces of equipment type?
7. **Software Inventory** - Do I have specific application or OS?
8. **Asset Location** - Where is specific application/vulnerability/OS/library?

---

## Architecture

```
query_api/
├── config/
│   ├── __init__.py
│   ├── settings.py       # Configuration management
│   ├── database.py       # Neo4j connection pooling
│   └── cache.py          # Redis caching
├── queries/
│   ├── __init__.py
│   ├── base.py           # Base query executor
│   ├── cve_impact.py     # Questions 1 & 3
│   ├── attack_path.py    # Questions 2, 4 & 5
│   └── asset_management.py # Questions 6, 7 & 8
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── README.md
```

---

## Quick Start

### 1. Install Dependencies

```bash
cd /home/jim/2_OXOT_Projects_Dev/Import\ 1\ NOV\ 2025/7-3_TM\ -\ MITRE/deployment/query_api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Required Configuration:**
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

REDIS_HOST=localhost
REDIS_PORT=6379

API_KEYS=your-secret-api-key
```

### 3. Start API Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Test API

```bash
# Health check
curl http://localhost:8000/health

# Query CVE impact (with API key)
curl -X POST http://localhost:8000/api/v1/query/cve-impact \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{"cveId": "CVE-2023-12345", "complexity": "simple"}'
```

---

## API Endpoints

### Health & Status

- **GET** `/` - API root information
- **GET** `/health` - Health check endpoint

### Question 1: CVE Impact

- **POST** `/api/v1/query/cve-impact`
  - Parameters: `cveId`, `complexity` (simple|intermediate|advanced)

### Question 2: Attack Path

- **POST** `/api/v1/query/attack-path`
  - Parameters: `threatActorName`, `vulnerabilityId`, `complexity`

### Question 3: Today's CVE Facility Impact

- **POST** `/api/v1/query/cve-facility-impact`
  - Parameters: `facilityId`, `facilityIds`, `minSeverity`, `today`, `complexity`

### Question 4: Threat Actor Pathway

- **POST** `/api/v1/query/threat-actor-path`
  - Parameters: `threatActorName`, `vulnerabilityId`, `cveId`, `complexity`

### Question 5: CVE Threat Path

- **POST** `/api/v1/query/cve-threat-path`
  - Parameters: `today`, `severityFilter`, `minCVSS`, `complexity`

### Question 6: Equipment Count

- **GET** `/api/v1/query/equipment-count`
  - Parameters: `equipmentType`, `facilityId`, `criticalityLevel`, `complexity`

### Question 7: Software Check

- **GET** `/api/v1/query/software-check`
  - Parameters: `softwareName`, `version`, `vendor`, `softwareType`, `complexity`

### Question 8: Asset Location

- **GET** `/api/v1/query/asset-location`
  - Parameters: `itemName`, `itemId`, `searchTerm`, `version`, `complexity`

---

## Query Complexity Levels

### Simple Queries
- Direct relationships only
- Minimal graph traversal (1-2 hops)
- Fast execution (<1 second)
- Basic result format

### Intermediate Queries
- Multiple relationship paths
- Moderate graph traversal (3-5 hops)
- Moderate execution (1-5 seconds)
- Enriched result format

### Advanced Queries
- Complete relationship analysis
- Deep graph traversal (5+ hops)
- Comprehensive execution (5-30 seconds)
- Full context result format with risk assessment

---

## Features

### Connection Pooling
- Neo4j async driver with configurable pool size
- Automatic connection management
- Connection acquisition timeout control

### Query Caching
- Redis-based result caching
- Configurable TTL (default: 1 hour)
- Cache key generation from query + parameters
- Pattern-based cache invalidation

### API Security
- API key authentication via header
- Multiple API key support
- CORS configuration
- Request validation with Pydantic

### Error Handling
- Comprehensive exception handling
- Database connection failure recovery
- Cache unavailability fallback
- Structured error responses

### Monitoring
- Request/response logging
- Query execution time tracking
- Cache hit/miss metrics
- Database connection health

---

## Configuration Options

### Neo4j Settings

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j
NEO4J_MAX_CONNECTION_POOL_SIZE=50
NEO4J_CONNECTION_ACQUISITION_TIMEOUT=60
```

### Redis Settings

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
CACHE_TTL=3600
```

### API Settings

```bash
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_KEY_HEADER=X-API-Key
API_KEYS=key1,key2,key3
```

### Query Settings

```bash
MAX_QUERY_TIMEOUT=30
DEFAULT_PAGE_SIZE=100
MAX_PAGE_SIZE=1000
```

### Logging Settings

```bash
LOG_LEVEL=INFO
LOG_FORMAT=json
```

---

## Usage Examples

### Python Client

```python
import httpx

async def query_cve_impact(cve_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/query/cve-impact",
            headers={"X-API-Key": "your-api-key"},
            json={
                "cveId": cve_id,
                "complexity": "advanced",
                "use_cache": True
            }
        )
        return response.json()

# Usage
result = await query_cve_impact("CVE-2023-12345")
print(f"Affected equipment: {result['data'][0]['totalEquipmentImpacted']}")
```

### cURL Examples

```bash
# CVE Impact (Simple)
curl -X POST http://localhost:8000/api/v1/query/cve-impact \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"cveId": "CVE-2023-12345", "complexity": "simple"}'

# Attack Path (Advanced)
curl -X POST http://localhost:8000/api/v1/query/attack-path \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "threatActorName": "APT28",
    "vulnerabilityId": "VULN-2023-001",
    "complexity": "advanced"
  }'

# Equipment Count (Intermediate)
curl -X GET "http://localhost:8000/api/v1/query/equipment-count?equipmentType=Server&complexity=intermediate" \
  -H "X-API-Key: your-api-key"

# Software Check (Advanced)
curl -X GET "http://localhost:8000/api/v1/query/software-check?softwareName=Apache&complexity=advanced" \
  -H "X-API-Key: your-api-key"
```

---

## Performance

### Query Execution Times (Average)

| Complexity | Execution Time | Use Case |
|------------|---------------|----------|
| Simple | < 1 second | Quick lookups, dashboards |
| Intermediate | 1-5 seconds | Detailed analysis |
| Advanced | 5-30 seconds | Comprehensive reports |

### Caching Impact

- **Cache Hit**: < 50ms response time
- **Cache Miss**: Query execution + cache storage
- **Cache TTL**: 1 hour (configurable)

### Optimization Recommendations

1. **Use Simple queries** for real-time dashboards
2. **Enable caching** for frequently accessed data
3. **Use Advanced queries** for scheduled reports
4. **Configure connection pool** based on concurrent load
5. **Monitor slow queries** and adjust complexity as needed

---

## Production Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  query-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - REDIS_HOST=redis
      - API_KEYS=${API_KEYS}
    depends_on:
      - neo4j
      - redis

  neo4j:
    image: neo4j:5.14
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### Systemd Service

```ini
[Unit]
Description=AEON MITRE Query API
After=network.target neo4j.service redis.service

[Service]
Type=notify
User=aeon
WorkingDirectory=/opt/aeon/query_api
Environment="PATH=/opt/aeon/query_api/venv/bin"
ExecStart=/opt/aeon/query_api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Troubleshooting

### Connection Issues

```bash
# Test Neo4j connection
cypher-shell -a bolt://localhost:7687 -u neo4j -p password

# Test Redis connection
redis-cli ping

# Check API logs
tail -f /var/log/aeon/query-api.log
```

### Common Errors

**Error:** `Neo4j connection failed`
- **Solution:** Verify NEO4J_URI, credentials, and Neo4j service status

**Error:** `Redis cache unavailable`
- **Solution:** API continues without caching. Check Redis service.

**Error:** `Invalid API key`
- **Solution:** Verify API_KEYS configuration and request header

**Error:** `Query timeout`
- **Solution:** Increase MAX_QUERY_TIMEOUT or use simpler complexity

---

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Adding New Queries

1. Create query executor in `queries/` inheriting from `QueryExecutor`
2. Implement `get_query_simple()`, `get_query_intermediate()`, `get_query_advanced()`
3. Add endpoint in `main.py`
4. Update documentation

### Code Style

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

---

## Support

- **Documentation:** See AEON_CAPABILITY_QUERY_PATTERNS.md
- **Issues:** Check logs at `/var/log/aeon/query-api.log`
- **Performance:** Monitor with `/health` endpoint

---

## License

AEON Internal Use Only

---

**Generated with Backend API Developer Agent**
**Created:** 2025-11-08
**Status:** Production Ready
