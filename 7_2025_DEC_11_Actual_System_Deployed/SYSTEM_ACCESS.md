# SYSTEM ACCESS - OXOT Platform

**Last Updated**: 2025-12-12
**Environment**: Development
**Status**: Operational

---

## SERVICES & PORTS

### NER11-GOLD-API (Backend API)
- **URL**: `http://localhost:8000`
- **Status**: ✅ RUNNING
- **Health Check**: `curl http://localhost:8000/health`
- **API Docs**: `http://localhost:8000/docs` (Swagger/OpenAPI)
- **Total APIs**: 140 endpoints
- **Working APIs**: 36 (26%)

### AEON-SAAS-DEV (Frontend/Next.js)
- **URL**: `http://localhost:3000`
- **Status**: ⚠️ RUNNING (APIs failing)
- **Health Check**: `curl http://localhost:3000/api/health`
- **Total APIs**: 41 endpoints
- **Working APIs**: 0 (0%) - **ALL FAILING**

---

## AUTHENTICATION

### Development Environment
```bash
# Standard header for all requests
x-customer-id: dev
```

### Write Operations (DELETE, some PUT)
```bash
# Additional header required
x-access-level: WRITE
```

### Future Production (Not Yet Implemented)
```bash
# Will require JWT token
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## DATABASE ACCESS

### PostgreSQL (Primary Database)
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `oxot_dev`
- **User**: (Check `.env` file)
- **Password**: (Check `.env` file)

**Connection String**:
```
postgresql://user:password@localhost:5432/oxot_dev
```

### Qdrant (Vector Database)
- **Host**: `localhost`
- **Port**: `6333`
- **Web UI**: `http://localhost:6333/dashboard`
- **Collections**:
  - `sbom_components`
  - `vulnerabilities`
  - `threat_intel`
  - `risk_scores`

### Neo4j (Graph Database)
- **Host**: `localhost`
- **Bolt Port**: `7687`
- **HTTP Port**: `7474`
- **Browser UI**: `http://localhost:7474`
- **User**: `neo4j`
- **Password**: (Check `.env` file)

---

## QUICK START

### 1. Check Services Running
```bash
# Check NER11 backend
curl http://localhost:8000/health

# Check AEON frontend
curl http://localhost:3000/api/health

# Check PostgreSQL
psql -h localhost -p 5432 -U your_user -d oxot_dev -c "SELECT version();"

# Check Qdrant
curl http://localhost:6333/health

# Check Neo4j
curl http://localhost:7474/
```

### 2. Test API Access
```bash
# List SBOMs
curl -X GET http://localhost:8000/api/v2/sbom/sboms \
  -H 'x-customer-id: dev'

# Get SBOM dashboard
curl -X GET http://localhost:8000/api/v2/sbom/dashboard/summary \
  -H 'x-customer-id: dev'

# Get threat intel summary
curl -X GET http://localhost:8000/api/v2/threat-intel/dashboard/summary \
  -H 'x-customer-id: dev'

# Get risk dashboard
curl -X GET http://localhost:8000/api/v2/risk/dashboard/summary \
  -H 'x-customer-id: dev'
```

### 3. Create Test Data
```bash
# Create a test SBOM
curl -X POST http://localhost:8000/api/v2/sbom/sboms \
  -H 'x-customer-id: dev' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Test Application",
    "version": "1.0.0",
    "description": "Test SBOM for development"
  }'

# Create a test vendor
curl -X POST http://localhost:8000/api/v2/vendor-equipment/vendors \
  -H 'x-customer-id: dev' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Test Vendor Inc",
    "website": "https://testvendor.com"
  }'
```

---

## ENVIRONMENT VARIABLES

### Required `.env` File
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/oxot_dev
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=oxot_dev

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=  # Optional for dev

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password

# API Keys (if needed)
NER_API_KEY=your_ner_api_key
OPENAI_API_KEY=your_openai_key  # If using AI features

# Application
ENVIRONMENT=development
LOG_LEVEL=debug
PORT=8000
```

---

## API REQUEST EXAMPLES

### JavaScript/Fetch
```javascript
// Standard GET request
fetch('http://localhost:8000/api/v2/sbom/sboms', {
  headers: {
    'x-customer-id': 'dev'
  }
})
.then(res => res.json())
.then(data => console.log(data))

// POST request with data
fetch('http://localhost:8000/api/v2/sbom/sboms', {
  method: 'POST',
  headers: {
    'x-customer-id': 'dev',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'My SBOM',
    version: '1.0.0'
  })
})
.then(res => res.json())
.then(data => console.log(data))

// DELETE request (requires WRITE access)
fetch('http://localhost:8000/api/v2/sbom/sboms/123', {
  method: 'DELETE',
  headers: {
    'x-customer-id': 'dev',
    'x-access-level': 'WRITE'
  }
})
.then(res => res.json())
.then(data => console.log(data))
```

### Python/Requests
```python
import requests

# Standard GET
response = requests.get(
    'http://localhost:8000/api/v2/sbom/sboms',
    headers={'x-customer-id': 'dev'}
)
print(response.json())

# POST with data
response = requests.post(
    'http://localhost:8000/api/v2/sbom/sboms',
    headers={
        'x-customer-id': 'dev',
        'Content-Type': 'application/json'
    },
    json={
        'name': 'My SBOM',
        'version': '1.0.0'
    }
)
print(response.json())

# DELETE (requires WRITE)
response = requests.delete(
    'http://localhost:8000/api/v2/sbom/sboms/123',
    headers={
        'x-customer-id': 'dev',
        'x-access-level': 'WRITE'
    }
)
print(response.json())
```

### cURL
```bash
# GET request
curl -X GET http://localhost:8000/api/v2/sbom/sboms \
  -H 'x-customer-id: dev'

# POST request
curl -X POST http://localhost:8000/api/v2/sbom/sboms \
  -H 'x-customer-id: dev' \
  -H 'Content-Type: application/json' \
  -d '{"name":"My SBOM","version":"1.0.0"}'

# DELETE request
curl -X DELETE http://localhost:8000/api/v2/sbom/sboms/123 \
  -H 'x-customer-id: dev' \
  -H 'x-access-level: WRITE'
```

---

## KNOWN ISSUES

### ❌ AEON-SAAS-DEV APIs Not Working
**Status**: All 41 APIs returning 500 errors
**Impact**: Frontend features unavailable
**Workaround**: Use ner11-gold-api directly for now
**Action**: Backend team investigating database connection issue

### ❌ Remediation Subsystem Broken
**Status**: All 27 remediation APIs failing with 500 errors
**Impact**: Cannot create/manage remediation tasks, plans, SLAs
**Workaround**: Manual tracking until fixed
**Action**: Requires database schema fix

### ⚠️ No Test Data
**Status**: Most APIs return empty results (404)
**Impact**: GET endpoints work but return no data
**Workaround**: Use POST endpoints to create test data first
**Action**: See `UI_DEVELOPER_GUIDE.md` for data creation examples

---

## TROUBLESHOOTING

### Service Not Responding
```bash
# Check if service is running
ps aux | grep python  # For NER11-GOLD-API
ps aux | grep node    # For AEON-SAAS-DEV

# Check ports in use
lsof -i :8000  # NER11
lsof -i :3000  # AEON
lsof -i :5432  # PostgreSQL
lsof -i :6333  # Qdrant
lsof -i :7687  # Neo4j Bolt
lsof -i :7474  # Neo4j HTTP

# Restart services (example)
# cd /path/to/ner11-gold-api && python main.py
# cd /path/to/aeon-saas-dev && npm run dev
```

### 401 Unauthorized
```bash
# Add missing header
curl -X GET http://localhost:8000/api/endpoint \
  -H 'x-customer-id: dev'
```

### 403 Forbidden
```bash
# Add WRITE access header for write operations
curl -X DELETE http://localhost:8000/api/endpoint/123 \
  -H 'x-customer-id: dev' \
  -H 'x-access-level: WRITE'
```

### 404 Not Found
```bash
# Likely no data - create test data first
curl -X POST http://localhost:8000/api/v2/sbom/sboms \
  -H 'x-customer-id: dev' \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test","version":"1.0"}'
```

### 422 Validation Error
```bash
# Missing required fields in request body
# Check API documentation for required fields
curl http://localhost:8000/docs  # View Swagger docs
```

### 500 Server Error
```bash
# API is broken - report to backend team
# See DEFINITIVE_API_AUDIT_2025-12-12.md for list of broken APIs
```

---

## DATABASE QUERIES

### PostgreSQL - Check Data
```sql
-- Connect to database
psql -h localhost -p 5432 -U your_user -d oxot_dev

-- Check SBOMs
SELECT COUNT(*) FROM sboms;

-- Check vendors
SELECT COUNT(*) FROM vendors;

-- Check vulnerabilities
SELECT COUNT(*) FROM vulnerabilities;

-- Check threat actors
SELECT COUNT(*) FROM threat_actors;
```

### Qdrant - Check Collections
```bash
# List collections
curl http://localhost:6333/collections

# Check collection size
curl http://localhost:6333/collections/sbom_components

# Search in collection
curl -X POST http://localhost:6333/collections/sbom_components/points/search \
  -H 'Content-Type: application/json' \
  -d '{"vector":[0.1,0.2,0.3],"limit":5}'
```

### Neo4j - Check Graph
```cypher
// Connect via browser: http://localhost:7474

// Count nodes
MATCH (n) RETURN count(n);

// Count relationships
MATCH ()-[r]->() RETURN count(r);

// Check node types
MATCH (n) RETURN DISTINCT labels(n), count(n);

// Sample data
MATCH (n) RETURN n LIMIT 10;
```

---

## NEXT STEPS

1. **Verify Access**: Run health checks on all services
2. **Create Test Data**: Use POST endpoints to populate database
3. **Check Documentation**: See `DEFINITIVE_API_AUDIT_2025-12-12.md` for complete API status
4. **Build UI**: Use `UI_DEVELOPER_GUIDE.md` for frontend integration
5. **Report Issues**: Contact backend team for broken APIs (500 errors)

---

*For complete API testing results, see: DEFINITIVE_API_AUDIT_2025-12-12.md*
*For UI integration guide, see: UI_DEVELOPER_GUIDE.md*
*For project organization, see: README.md*
