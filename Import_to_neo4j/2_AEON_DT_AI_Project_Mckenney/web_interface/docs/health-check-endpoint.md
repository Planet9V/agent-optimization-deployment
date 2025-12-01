# Health Check Endpoint Documentation

## Overview

The `/app/api/health/route.ts` endpoint provides comprehensive health monitoring for all OpenSPG backend services.

## Endpoint

```
GET /api/health
```

## Services Monitored

1. **Neo4j** - Graph database (`bolt://openspg-neo4j:7687`)
2. **MySQL** - Relational database (`openspg-mysql:3306`)
3. **Qdrant** - Vector database (`http://openspg-qdrant:6333`)
4. **MinIO** - Object storage (`openspg-minio:9000`)

## Response Format

### Successful Response (200)

All services healthy:

```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T10:30:00.000Z",
  "services": {
    "neo4j": {
      "status": "ok",
      "responseTime": 45,
      "details": {
        "uri": "bolt://openspg-neo4j:7687",
        "database": "neo4j"
      }
    },
    "mysql": {
      "status": "ok",
      "responseTime": 23,
      "details": {
        "host": "openspg-mysql",
        "port": 3306,
        "database": "openspg"
      }
    },
    "qdrant": {
      "status": "ok",
      "responseTime": 67,
      "details": {
        "url": "http://openspg-qdrant:6333",
        "collections": 3
      }
    },
    "minio": {
      "status": "ok",
      "responseTime": 34,
      "details": {
        "endpoint": "openspg-minio:9000",
        "buckets": 2
      }
    }
  },
  "overallHealth": "4/4 services healthy",
  "metadata": {
    "environment": "development",
    "nodeVersion": "v20.10.0"
  }
}
```

### Degraded Response (207)

Some services unhealthy:

```json
{
  "status": "degraded",
  "timestamp": "2025-11-15T10:30:00.000Z",
  "services": {
    "neo4j": {
      "status": "ok",
      "responseTime": 45,
      "details": { "uri": "bolt://openspg-neo4j:7687", "database": "neo4j" }
    },
    "mysql": {
      "status": "error",
      "responseTime": 2003,
      "message": "Connection timeout",
      "details": { "host": "openspg-mysql", "port": 3306 }
    },
    "qdrant": {
      "status": "ok",
      "responseTime": 67,
      "details": { "url": "http://openspg-qdrant:6333", "collections": 3 }
    },
    "minio": {
      "status": "ok",
      "responseTime": 34,
      "details": { "endpoint": "openspg-minio:9000", "buckets": 2 }
    }
  },
  "overallHealth": "3/4 services healthy"
}
```

### Unhealthy Response (503)

Most services down:

```json
{
  "status": "unhealthy",
  "timestamp": "2025-11-15T10:30:00.000Z",
  "services": {
    "neo4j": {
      "status": "timeout",
      "message": "Neo4j timeout after 5000ms"
    },
    "mysql": {
      "status": "error",
      "responseTime": 1523,
      "message": "ECONNREFUSED",
      "details": { "host": "openspg-mysql", "port": 3306 }
    },
    "qdrant": {
      "status": "ok",
      "responseTime": 67,
      "details": { "url": "http://openspg-qdrant:6333", "collections": 3 }
    },
    "minio": {
      "status": "error",
      "responseTime": 234,
      "message": "Connection refused",
      "details": { "endpoint": "openspg-minio:9000" }
    }
  },
  "overallHealth": "1/4 services healthy"
}
```

## HTTP Status Codes

- **200** - All services healthy (`status: "healthy"`)
- **207** - Some services degraded (`status: "degraded"`)
- **503** - Services unhealthy (`status: "unhealthy"`)

## Service Status Types

Each service can have one of these statuses:

- `"ok"` - Service connected successfully
- `"error"` - Service connection failed with error
- `"timeout"` - Service did not respond within 5 seconds

## Implementation Details

### Connection Libraries Used

- **Neo4j**: `/lib/neo4j-enhanced.ts` - `getNeo4jDriver()`
- **MySQL**: `/lib/mysql.ts` - `getMySQLPool()`
- **Qdrant**: `/lib/qdrant.ts` - `getQdrantClient()`
- **MinIO**: `/lib/minio.ts` - `getMinIOClient()`

### Timeout Configuration

```typescript
const SERVICE_TIMEOUT = 5000; // 5 second timeout per service
```

### Parallel Execution

All health checks run in parallel using `Promise.all()` for optimal performance.

## Usage Examples

### cURL

```bash
# Basic health check
curl http://localhost:3000/api/health

# Pretty-printed JSON
curl -s http://localhost:3000/api/health | jq .

# Check HTTP status
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health
```

### Using Test Script

```bash
# Run the provided test script
./scripts/test-health.sh
```

### JavaScript/TypeScript

```typescript
const response = await fetch('http://localhost:3000/api/health');
const health = await response.json();

console.log('Overall Status:', health.status);
console.log('Healthy Services:', health.overallHealth);

// Check specific service
if (health.services.neo4j.status === 'ok') {
  console.log('Neo4j Response Time:', health.services.neo4j.responseTime, 'ms');
}
```

### Monitoring Integration

```bash
# Kubernetes liveness probe
livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10

# Docker Compose healthcheck
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Error Handling

The endpoint handles failures gracefully:

1. **Service Timeout**: Returns `timeout` status if service doesn't respond within 5 seconds
2. **Connection Errors**: Captures error messages and includes them in response
3. **Catastrophic Failure**: Returns 503 with error details if the health check itself fails

## Performance Metrics

Expected response times for healthy services:

- **Neo4j**: 20-100ms
- **MySQL**: 10-50ms
- **Qdrant**: 30-150ms
- **MinIO**: 20-80ms

Total endpoint response time (parallel execution): ~100-200ms

## Environment Variables

The health check uses these environment variables (with defaults):

```bash
# Neo4j
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=neo4j@openspg

# MySQL
MYSQL_HOST=openspg-mysql
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=openspg
MYSQL_DATABASE=openspg

# Qdrant
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY= # Optional

# MinIO
MINIO_ENDPOINT=openspg-minio:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false
```

## Testing

Run the comprehensive test suite:

```bash
# Jest tests
npm test tests/health-check.test.ts

# Manual verification
./scripts/test-health.sh

# Load test example
for i in {1..10}; do
  curl -s http://localhost:3000/api/health | jq -r '.status'
done
```

## Troubleshooting

### All Services Timeout

**Issue**: All services show `timeout` status

**Solutions**:
1. Check if services are running: `docker-compose ps`
2. Verify network connectivity between containers
3. Check firewall rules

### Specific Service Errors

**Neo4j Connection Failed**:
```bash
# Test Neo4j directly
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "RETURN 1"
```

**MySQL Connection Failed**:
```bash
# Test MySQL directly
docker exec openspg-mysql mysql -u root -popenspg -e "SELECT 1"
```

**Qdrant Connection Failed**:
```bash
# Test Qdrant directly
curl http://localhost:6333/collections
```

**MinIO Connection Failed**:
```bash
# Test MinIO directly
curl http://localhost:9000/minio/health/live
```

## Contributing

When modifying the health check endpoint:

1. Update service checks in `/app/api/health/route.ts`
2. Update this documentation
3. Add corresponding tests in `/tests/health-check.test.ts`
4. Verify all services before committing

## Related Files

- `/app/api/health/route.ts` - Main endpoint implementation
- `/lib/neo4j-enhanced.ts` - Neo4j connection library
- `/lib/mysql.ts` - MySQL connection library
- `/lib/qdrant.ts` - Qdrant connection library
- `/lib/minio.ts` - MinIO connection library
- `/tests/health-check.test.ts` - Test suite
- `/scripts/test-health.sh` - Manual test script
