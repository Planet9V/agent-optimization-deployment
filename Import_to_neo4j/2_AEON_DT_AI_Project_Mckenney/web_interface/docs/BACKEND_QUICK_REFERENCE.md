# Backend Services Quick Reference

## Service URLs

### Development (localhost)
```bash
Neo4j Browser:  http://localhost:7474
Neo4j Bolt:     bolt://localhost:7687
Qdrant API:     http://localhost:6333
Qdrant Console: http://localhost:6333/dashboard
MySQL:          localhost:3306
MinIO API:      http://localhost:9000
MinIO Console:  http://localhost:9001
```

### Production (Docker network)
```bash
Neo4j:   bolt://openspg-neo4j:7687
Qdrant:  http://openspg-qdrant:6333
MySQL:   openspg-mysql:3306
MinIO:   openspg-minio:9000
```

## Credentials

### Neo4j
```
Username: neo4j
Password: neo4j@openspg
Database: neo4j
```

### Qdrant
```
URL: http://localhost:6333
API Key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=
```

### MySQL
```
Host:     localhost
Port:     3306
Database: openspg
Username: root
Password: openspg
```

### MinIO
```
Endpoint:   localhost
Port:       9000
Access Key: minio
Secret Key: minio@openspg
Bucket:     aeon-documents
```

## Verification Commands

### Quick Health Check
```bash
# All services
node scripts/verify-backend-connections.js

# Individual services
docker ps | grep openspg
curl http://localhost:6333/health
curl http://localhost:9000/minio/health/live
```

### Integration Tests
```bash
# Full integration test suite
node scripts/test-backend-integration.js
```

### Docker Commands
```bash
# View all containers
docker ps -a

# Check specific service
docker logs openspg-neo4j
docker logs openspg-qdrant
docker logs openspg-mysql
docker logs openspg-minio

# Restart a service
docker restart openspg-neo4j

# View container stats
docker stats
```

## Data Statistics

- **Neo4j:** 568,163 nodes loaded
- **Qdrant:** 19 collections active
- **MySQL:** 34 tables in openspg database
- **MinIO:** aeon-documents bucket created

---

## API Endpoints

**API Version:** 3.3.0
**Base URL:** `http://localhost:8000`
**Total Endpoints:** 230
**Authentication:** X-Customer-ID header required

### Quick API Overview

| Phase | Category | Endpoints | Base Path |
|-------|----------|-----------|-----------|
| **B2** | SBOM Management | 33 | `/api/v2/sbom/` |
| **B2** | Vendor & Equipment | 19 | `/api/v2/vendor-equipment/` |
| **B3** | Threat Intelligence | 25 | `/api/v2/threat-intel/` |
| **B3** | Risk Management | 27 | `/api/v2/risk/` |
| **B3** | Remediation | 26 | `/api/v2/remediation/` |
| **B4** | Compliance | 21 | `/api/v2/compliance/` |
| **B5** | Alerts | 19 | `/api/v2/alerts/` |
| **B5** | Demographics | 24 | `/api/v2/demographics/` |
| **B5** | Economic Analysis | 27 | `/api/v2/economic/` |
| - | Psychometric | 8 | `/api/v2/psychometric/` |
| - | Search Services | 3 | `/search/`, `/ner` |
| - | System Health | 1 | `/health` |

### Common API Examples

```bash
# Check API health
curl http://localhost:8000/health

# List all SBOMs
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/sbom/sboms

# Get critical vulnerabilities
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/sbom/vulnerabilities/critical

# Search threats
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/threat-intel/actors/search?q=APT29

# Get compliance dashboard
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/compliance/dashboard/summary

# Semantic search
curl -X POST -H "Content-Type: application/json" \
     -d '{"query": "ransomware", "limit": 10}' \
     http://localhost:8000/search/semantic
```

### Complete API Documentation

See **[COMPLETE_API_REFERENCE.md](./COMPLETE_API_REFERENCE.md)** for:
- Detailed endpoint descriptions
- Request/response examples
- Authentication details
- Error handling
- Rate limiting
- WebSocket support

## Common Operations

### Neo4j Queries
```javascript
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'neo4j@openspg')
);

const session = driver.session();
const result = await session.run('MATCH (n) RETURN n LIMIT 10');
```

### Qdrant Search
```javascript
import { QdrantClient } from '@qdrant/js-client-rest';

const client = new QdrantClient({
  url: 'http://localhost:6333',
  apiKey: process.env.QDRANT_API_KEY
});

const collections = await client.getCollections();
```

### MySQL Queries
```javascript
import mysql from 'mysql2/promise';

const connection = await mysql.createConnection({
  host: 'localhost',
  port: 3306,
  user: 'root',
  password: 'openspg',
  database: 'openspg'
});

const [rows] = await connection.execute('SELECT * FROM table_name');
```

### MinIO Upload
```javascript
import Minio from 'minio';

const minioClient = new Minio.Client({
  endPoint: 'localhost',
  port: 9000,
  useSSL: false,
  accessKey: 'minio',
  secretKey: 'minio@openspg'
});

await minioClient.putObject('aeon-documents', 'file.txt', buffer);
```

## Environment Variables

### For Development (.env.local)
```bash
NEO4J_URI=bolt://localhost:7687
QDRANT_URL=http://localhost:6333
MYSQL_HOST=localhost
MINIO_ENDPOINT=localhost
```

### For Production
```bash
NEO4J_URI=bolt://openspg-neo4j:7687
QDRANT_URL=http://openspg-qdrant:6333
MYSQL_HOST=openspg-mysql
MINIO_ENDPOINT=openspg-minio
```

## Troubleshooting

### Service Not Responding
```bash
# Check if container is running
docker ps | grep <service-name>

# Restart the service
docker restart <container-name>

# Check logs for errors
docker logs <container-name>
```

### Connection Refused
- Verify container is running: `docker ps`
- Check port mappings: `docker port <container-name>`
- Verify environment variables in `.env.local`

### Data Not Showing Up
- For Neo4j: Check browser at http://localhost:7474
- For Qdrant: Check dashboard at http://localhost:6333/dashboard
- For MySQL: Use `docker exec openspg-mysql mysql -uroot -popenspg -e "SHOW DATABASES;"`
- For MinIO: Check console at http://localhost:9001

## Useful Links

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MinIO Documentation](https://min.io/docs/)

## Support

For issues or questions:
1. Check service logs: `docker logs <container-name>`
2. Run verification: `node scripts/verify-backend-connections.js`
3. Run integration tests: `node scripts/test-backend-integration.js`
4. Check this documentation

---

**Last Updated:** 2025-11-03
**Status:** All services operational ✅
