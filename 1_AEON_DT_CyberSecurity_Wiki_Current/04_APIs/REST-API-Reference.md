# REST API Reference - AEON DT System

**File:** REST-API-Reference.md
**Created:** 2025-11-03 17:21:28 CST
**Version:** v1.0.0
**Purpose:** Consolidated REST API reference for all AEON DT services
**Status:** ACTIVE
**Tags:** #api #rest #endpoints #integration #reference

---

## Quick Reference Table

| Service | Base URL | Port | Auth Method | Status |
|---------|----------|------|-------------|--------|
| AEON UI Health | http://localhost:3000 | 3000 | None | ✅ Active |
| Neo4j REST | http://localhost:7474 | 7474 | Basic Auth | ✅ Active |
| Qdrant Vector DB | http://localhost:6333 | 6333 | API Key | ✅ Active |
| MinIO S3 Storage | http://localhost:9000 | 9000 | AWS Signature | ✅ Active |
| OpenSPG Server | http://172.18.0.2:8887 | 8887 | TBD | ⚠️ Unknown |

---

## 1. AEON UI Health API

**Base URL:** `http://localhost:3000`
**Version:** Current (2025-11-03)
**Authentication:** None required for health checks

### Endpoints

#### GET /api/health
Health check endpoint for all system services.

**Request:**
```http
GET /api/health HTTP/1.1
Host: localhost:3000
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T23:21:28.749Z",
  "checks": {
    "neo4j": {
      "status": "healthy"
    },
    "qdrant": {
      "status": "healthy"
    },
    "mysql": {
      "status": "healthy"
    },
    "minio": {
      "status": "healthy"
    }
  },
  "environment": {
    "nodeEnv": "production",
    "appName": "AEON UI"
  }
}
```

**Status Codes:**
- `200 OK` - All services healthy
- `503 Service Unavailable` - One or more services unhealthy

**Rate Limiting:** None
**Caching:** No caching recommended (real-time health status)

---

## 2. Neo4j REST API

**Base URL:** `http://localhost:7474`
**Version:** Neo4j 5.x
**Authentication:** Basic Auth (username/password)
**Content-Type:** `application/json`

### Authentication

```http
Authorization: Basic <base64(username:password)>
```

### Endpoints

#### POST /db/{database}/tx/commit
Execute Cypher queries in a single transaction.

**Request:**
```http
POST /db/neo4j/tx/commit HTTP/1.1
Host: localhost:7474
Content-Type: application/json
Authorization: Basic bmVvNGo6cGFzc3dvcmQ=

{
  "statements": [
    {
      "statement": "MATCH (n:Person) RETURN n LIMIT 10",
      "parameters": {}
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "results": [
    {
      "columns": ["n"],
      "data": [
        {
          "row": [{"name": "John Doe", "age": 30}],
          "meta": [{"id": 1, "type": "node", "deleted": false}]
        }
      ]
    }
  ],
  "errors": []
}
```

**Error Response (401 Unauthorized):**
```json
{
  "errors": [
    {
      "code": "Neo.ClientError.Security.Unauthorized",
      "message": "No authentication header supplied."
    }
  ]
}
```

#### POST /db/{database}/tx
Begin a new transaction.

**Request:**
```http
POST /db/neo4j/tx HTTP/1.1
Host: localhost:7474
Content-Type: application/json
Authorization: Basic bmVvNGo6cGFzc3dvcmQ=

{
  "statements": [
    {
      "statement": "CREATE (n:Person {name: $name}) RETURN n",
      "parameters": {"name": "Alice"}
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "commit": "http://localhost:7474/db/neo4j/tx/1/commit",
  "results": [...],
  "transaction": {
    "expires": "Sun, 03 Nov 2025 23:31:28 GMT"
  },
  "errors": []
}
```

#### POST /db/{database}/tx/{id}/commit
Commit an open transaction.

#### DELETE /db/{database}/tx/{id}
Rollback an open transaction.

**Status Codes:**
- `200 OK` - Query executed successfully
- `201 Created` - Transaction created
- `401 Unauthorized` - Authentication failed
- `404 Not Found` - Database or transaction not found
- `422 Unprocessable Entity` - Invalid Cypher query

**Rate Limiting:** Connection pool limits (default: 50 concurrent)
**Timeout:** 60 seconds per transaction

---

## 3. Qdrant Vector Database API

**Base URL:** `http://localhost:6333`
**Version:** 1.15.4
**Authentication:** API Key (optional)
**Content-Type:** `application/json`

### Authentication

```http
api-key: <your-api-key>
```

### Endpoints

#### GET /
Service information and version.

**Response (200 OK):**
```json
{
  "title": "qdrant - vector search engine",
  "version": "1.15.4",
  "commit": "20db14f87c861f3958ad50382cf0b69396e40c10"
}
```

#### GET /collections
List all collections.

**Request:**
```http
GET /collections HTTP/1.1
Host: localhost:6333
api-key: your-api-key-here
```

**Response (200 OK):**
```json
{
  "result": {
    "collections": [
      {
        "name": "cybersecurity_embeddings",
        "vectors_count": 1000,
        "points_count": 1000,
        "status": "green"
      }
    ]
  },
  "status": "ok",
  "time": 0.001
}
```

#### PUT /collections/{collection_name}
Create a new collection.

**Request:**
```http
PUT /collections/my_collection HTTP/1.1
Host: localhost:6333
api-key: your-api-key-here
Content-Type: application/json

{
  "vectors": {
    "size": 384,
    "distance": "Cosine"
  }
}
```

#### POST /collections/{collection_name}/points
Insert or update points.

**Request:**
```http
POST /collections/my_collection/points HTTP/1.1
Host: localhost:6333
api-key: your-api-key-here
Content-Type: application/json

{
  "points": [
    {
      "id": 1,
      "vector": [0.1, 0.2, 0.3, ...],
      "payload": {
        "text": "Sample document",
        "category": "cybersecurity"
      }
    }
  ]
}
```

#### POST /collections/{collection_name}/points/search
Vector similarity search.

**Request:**
```http
POST /collections/my_collection/points/search HTTP/1.1
Host: localhost:6333
api-key: your-api-key-here
Content-Type: application/json

{
  "vector": [0.1, 0.2, 0.3, ...],
  "limit": 10,
  "with_payload": true
}
```

**Response (200 OK):**
```json
{
  "result": [
    {
      "id": 1,
      "score": 0.95,
      "payload": {
        "text": "Similar document",
        "category": "cybersecurity"
      }
    }
  ],
  "status": "ok",
  "time": 0.005
}
```

#### DELETE /collections/{collection_name}
Delete a collection.

**Status Codes:**
- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid API key
- `404 Not Found` - Collection not found
- `422 Unprocessable Entity` - Invalid vector dimensions

**Rate Limiting:** Configurable per instance
**Timeout:** 30 seconds per request

---

## 4. MinIO S3 Storage API

**Base URL:** `http://localhost:9000`
**Version:** S3 Compatible API
**Authentication:** AWS Signature Version 4
**Content-Type:** Varies by operation

### Authentication

MinIO uses AWS Signature Version 4 signing process:

```http
Authorization: AWS4-HMAC-SHA256
  Credential=<access-key>/20251103/us-east-1/s3/aws4_request,
  SignedHeaders=host;x-amz-date,
  Signature=<signature>
```

### Common Endpoints

#### GET /
List all buckets.

**Request:**
```http
GET / HTTP/1.1
Host: localhost:9000
Authorization: AWS4-HMAC-SHA256 ...
```

**Response (200 OK):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ListAllMyBucketsResult>
  <Buckets>
    <Bucket>
      <Name>aeon-documents</Name>
      <CreationDate>2025-11-01T10:00:00.000Z</CreationDate>
    </Bucket>
  </Buckets>
</ListAllMyBucketsResult>
```

#### PUT /{bucket}
Create a new bucket.

#### GET /{bucket}
List objects in a bucket.

**Request:**
```http
GET /aeon-documents?max-keys=100 HTTP/1.1
Host: localhost:9000
Authorization: AWS4-HMAC-SHA256 ...
```

#### PUT /{bucket}/{key}
Upload an object.

**Request:**
```http
PUT /aeon-documents/document.pdf HTTP/1.1
Host: localhost:9000
Authorization: AWS4-HMAC-SHA256 ...
Content-Type: application/pdf
Content-Length: 12345

[binary data]
```

#### GET /{bucket}/{key}
Download an object.

#### DELETE /{bucket}/{key}
Delete an object.

#### HEAD /{bucket}/{key}
Get object metadata.

**Status Codes:**
- `200 OK` - Request successful
- `204 No Content` - Delete successful
- `403 Forbidden` - Access denied
- `404 Not Found` - Bucket or object not found
- `409 Conflict` - Bucket already exists

**Rate Limiting:** None by default
**Timeout:** Configurable (default: 300 seconds)
**Max Object Size:** 5TB

---

## 5. OpenSPG Server API

**Base URL:** `http://172.18.0.2:8887`
**Version:** TBD
**Authentication:** TBD
**Status:** ⚠️ Discovery in progress

### Notes
- Service is containerized at internal IP
- Endpoints require discovery
- Authentication method unknown
- Recommend using Docker networking for access

---

## Integration Examples

### Python - Multi-Service Health Check

```python
import requests
import json

def check_aeon_health():
    """Check AEON system health across all services."""
    response = requests.get('http://localhost:3000/api/health')
    health = response.json()

    print(f"System Status: {health['status']}")
    print(f"Timestamp: {health['timestamp']}")

    for service, status in health['checks'].items():
        print(f"  {service}: {status['status']}")

    return health['status'] == 'healthy'

if __name__ == '__main__':
    if check_aeon_health():
        print("✅ All services operational")
    else:
        print("❌ One or more services down")
```

### Python - Neo4j Query

```python
import requests
from base64 import b64encode

def query_neo4j(cypher_query, parameters=None):
    """Execute Cypher query against Neo4j."""
    auth = b64encode(b'neo4j:password').decode('utf-8')
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }

    payload = {
        'statements': [{
            'statement': cypher_query,
            'parameters': parameters or {}
        }]
    }

    response = requests.post(
        'http://localhost:7474/db/neo4j/tx/commit',
        headers=headers,
        json=payload
    )

    return response.json()

# Example usage
result = query_neo4j(
    "MATCH (n:Threat) WHERE n.severity = $sev RETURN n LIMIT 10",
    parameters={'sev': 'high'}
)
print(json.dumps(result, indent=2))
```

### Python - Qdrant Vector Search

```python
import requests

def search_vectors(collection, query_vector, limit=10):
    """Search for similar vectors in Qdrant."""
    headers = {
        'api-key': 'your-api-key-here',
        'Content-Type': 'application/json'
    }

    payload = {
        'vector': query_vector,
        'limit': limit,
        'with_payload': True
    }

    response = requests.post(
        f'http://localhost:6333/collections/{collection}/points/search',
        headers=headers,
        json=payload
    )

    return response.json()

# Example usage
query = [0.1] * 384  # 384-dimensional vector
results = search_vectors('cybersecurity_embeddings', query)
for hit in results['result']:
    print(f"Score: {hit['score']}, Text: {hit['payload']['text']}")
```

### Python - MinIO S3 Operations

```python
from minio import Minio

def upload_to_minio(bucket, object_name, file_path):
    """Upload file to MinIO bucket."""
    client = Minio(
        'localhost:9000',
        access_key='minioadmin',
        secret_key='minioadmin',
        secure=False
    )

    # Create bucket if not exists
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

    # Upload file
    client.fput_object(bucket, object_name, file_path)
    print(f"✅ Uploaded {object_name} to {bucket}")

# Example usage
upload_to_minio('aeon-documents', 'threat-report.pdf', '/path/to/file.pdf')
```

---

## Error Handling Best Practices

### Retry Logic
```python
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retries():
    """Create HTTP session with retry logic."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

session = create_session_with_retries()
response = session.get('http://localhost:3000/api/health')
```

### Timeout Configuration
```python
# Always set timeouts to prevent hanging
try:
    response = requests.get(
        'http://localhost:6333/collections',
        timeout=(5, 30)  # (connect timeout, read timeout)
    )
except requests.Timeout:
    print("❌ Request timed out")
except requests.ConnectionError:
    print("❌ Connection failed")
```

---

## API Versioning Strategy

Current implementation uses **no explicit versioning** for local services. Production deployment should consider:

1. **URI Versioning:** `/api/v1/health`, `/api/v2/health`
2. **Header Versioning:** `Accept: application/vnd.aeon.v1+json`
3. **Semantic Versioning:** Follow semver for API changes

---

## Security Considerations

1. **Neo4j:** Change default password immediately
2. **Qdrant:** Enable API key authentication for production
3. **MinIO:** Use strong access keys, enable TLS
4. **Network:** Place services behind reverse proxy with TLS
5. **Authentication:** Implement OAuth2/JWT for production APIs
6. **Rate Limiting:** Configure rate limits for all public endpoints

---

## Monitoring & Observability

### Health Check Monitoring
```bash
# Simple uptime monitoring script
#!/bin/bash
while true; do
  STATUS=$(curl -s http://localhost:3000/api/health | jq -r '.status')
  if [ "$STATUS" != "healthy" ]; then
    echo "❌ System unhealthy at $(date)"
    # Send alert
  fi
  sleep 60
done
```

### Metrics Collection
- Track response times for each endpoint
- Monitor error rates and status codes
- Log authentication failures
- Track API usage per client

---

## Related Documentation

- [[Neo4j-Service-Guide]] - Detailed Neo4j configuration
- [[Qdrant-Vector-Database]] - Vector search implementation
- [[MinIO-Object-Storage]] - S3-compatible storage setup
- [[AEON-UI-Architecture]] - Frontend API integration
- [[OpenSPG-Knowledge-Graph]] - Knowledge graph operations

---

## Version History

- v1.0.0 (2025-11-03): Initial consolidated API reference
  - AEON UI Health API documented
  - Neo4j REST API endpoints cataloged
  - Qdrant vector search API documented
  - MinIO S3 API reference added
  - Integration examples included

---

**Last Verified:** 2025-11-03 17:21:28 CST
**Next Review:** 2025-11-10
**Maintainer:** AEON DT Development Team
