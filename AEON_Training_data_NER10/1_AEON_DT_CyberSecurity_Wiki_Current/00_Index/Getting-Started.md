# Getting Started with AEON DT Cybersecurity Platform

**Last Updated**: 2025-11-03 17:22:00 CST
**Version**: 1.0.0
**Status**: ACTIVE
**Tags**: #getting-started #tutorial #quickstart #onboarding

---

## Welcome to AEON DT

This guide will help you quickly access and start using the AEON Digital Twin Cybersecurity Platform infrastructure.

**What You'll Learn**:
- Access all platform services
- Run your first queries
- Upload and manage data
- Navigate the web interface
- Troubleshoot common issues

**Time to Complete**: ~15 minutes

---

## Prerequisites

### System Requirements
- Docker Desktop installed and running
- Network access to localhost
- Web browser (Chrome, Firefox, Safari, or Edge)
- Basic command-line knowledge
- Optional: Python 3.9+ for API integration

### Verify Services Are Running
```bash
# Check all containers are running
docker ps | grep -E "aeon-ui|openspg"

# You should see 6 containers:
# - aeon-ui
# - openspg-neo4j
# - openspg-qdrant
# - openspg-mysql
# - openspg-minio
# - openspg-server
```

---

## Quick Start (5 Steps to Success)

### Step 1: Access the AEON UI Dashboard

**URL**: http://localhost:3000

**What You'll See**:
- System overview with real-time metrics
- 115 documents indexed
- 12,256 entities in knowledge graph
- 14,645 relationships mapped

**Navigation**:
- Click on metrics cards to explore data
- Use health check: http://localhost:3000/api/health

**Credentials**: None required for initial access

**Troubleshooting**:
```bash
# If page doesn't load, check container status
docker logs aeon-ui --tail 50

# Restart if needed
docker restart aeon-ui
```

---

### Step 2: Explore the Knowledge Graph (Neo4j)

**Browser UI**: http://localhost:7474
**Bolt Connection**: bolt://localhost:7687

**Credentials**:
- Username: `neo4j`
- Password: `neo4j@openspg`

**Your First Query**:
```cypher
// See a sample of the knowledge graph
MATCH (n)
RETURN n
LIMIT 25
```

**Common Queries**:
```cypher
// Count all entities
MATCH (n) RETURN count(n) as total_entities

// Find all entity types
MATCH (n) RETURN DISTINCT labels(n) as types, count(*) as count
ORDER BY count DESC

// Find relationships
MATCH ()-[r]->() RETURN type(r) as relationship_type, count(*) as count
ORDER BY count DESC
LIMIT 10
```

**Quick Tips**:
- Use `Ctrl+Enter` to execute queries
- Click nodes to expand relationships
- Use the schema view (database icon) to explore structure

---

### Step 3: Vector Search with Qdrant

**API Endpoint**: http://localhost:6333
**Dashboard**: http://localhost:6333/dashboard

**API Key**: `deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=`

**List Collections**:
```bash
curl -X GET http://localhost:6333/collections \
  -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ="
```

**Available Collections**:
- `implementation_decisions` - Architectural decisions
- `schema_knowledge` - Ontology mappings
- `agent_shared_memory` - Swarm coordination
- `operation_logs` - System audit trail

**Python Example**:
```python
from qdrant_client import QdrantClient

client = QdrantClient(
    url="http://localhost:6333",
    api_key="deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ="
)

# List all collections
collections = client.get_collections()
print(collections)

# Search in a collection
results = client.search(
    collection_name="schema_knowledge",
    query_vector=[0.1] * 3072,  # Example vector
    limit=5
)
```

---

### Step 4: Object Storage with MinIO

**Web Console**: http://localhost:9001
**S3 API Endpoint**: http://localhost:9000

**Credentials**:
- Access Key: `minio`
- Secret Key: `minio@openspg`

**Using the Web Console**:
1. Navigate to http://localhost:9001
2. Login with credentials above
3. Click "Create Bucket" to make a new bucket
4. Upload files via drag-and-drop

**Using Python (boto3)**:
```python
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minio',
    aws_secret_access_key='minio@openspg'
)

# List buckets
buckets = s3.list_buckets()
print(buckets)

# Upload a file
s3.upload_file('local_file.pdf', 'my-bucket', 'uploaded_file.pdf')
```

---

### Step 5: Check System Health

**Health Check Endpoint**: http://localhost:3000/api/health

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T...",
  "checks": {
    "neo4j": {"status": "healthy"},
    "qdrant": {"status": "healthy"},
    "mysql": {"status": "healthy"},
    "minio": {"status": "healthy"}
  }
}
```

**Using Command Line**:
```bash
# Check all services
curl -s http://localhost:3000/api/health | python3 -m json.tool

# Individual service checks
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "RETURN 'OK'"
docker exec openspg-mysql mysql -uroot -popenspg -e "SELECT 1"
```

---

## Common Workflows

### Workflow 1: Query Knowledge Graph from UI

1. Access AEON UI: http://localhost:3000
2. Navigate to "Graph" section (when implemented)
3. Enter Cypher query or use visual builder
4. View results as graph or table
5. Export results if needed

**Current Status**: UI infrastructure ready, graph visualization pending Phase 4

### Workflow 2: Upload Documents for Processing

1. Access AEON UI: http://localhost:3000
2. Navigate to "Documents" section (when implemented)
3. Drag and drop files (PDF, TXT, MD, DOCX)
4. Monitor processing progress
5. View extracted entities in Neo4j

**Current Status**: UI infrastructure ready, upload interface pending Phase 2

### Workflow 3: Vector Similarity Search

1. Use Qdrant API or Python client
2. Generate embedding for your query
3. Search relevant collection
4. Review results with confidence scores
5. Retrieve original documents from MinIO

**Current Status**: Fully operational via API

---

## Troubleshooting Common Issues

### Issue 1: AEON UI Shows "Unhealthy"

**Symptoms**: Health check returns degraded status

**Diagnosis**:
```bash
# Check logs
docker logs aeon-ui --tail 100

# Test database connections
curl http://localhost:3000/api/health
```

**Common Causes**:
- Database not ready yet (wait 30 seconds after startup)
- Network connectivity issue
- Environment variables incorrect

**Solution**:
```bash
# Restart container
docker restart aeon-ui

# Verify environment
docker exec aeon-ui env | grep -E "NEO4J|QDRANT|MYSQL|MINIO"
```

### Issue 2: Neo4j Browser Won't Load

**Symptoms**: http://localhost:7474 doesn't respond

**Diagnosis**:
```bash
# Check if Neo4j is running
docker ps | grep neo4j

# Check logs
docker logs openspg-neo4j --tail 50
```

**Solution**:
```bash
# Restart Neo4j
docker restart openspg-neo4j

# Wait for startup (check logs for "Started.")
docker logs -f openspg-neo4j
```

### Issue 3: Qdrant API Returns 401

**Symptoms**: "Unauthorized" errors when accessing API

**Diagnosis**:
- Missing API key in request headers
- Incorrect API key value

**Solution**:
```bash
# Always include API key header
curl -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
  http://localhost:6333/collections
```

### Issue 4: MinIO Access Denied

**Symptoms**: Cannot login to web console or API calls fail

**Diagnosis**:
- Incorrect credentials
- Bucket permissions

**Solution**:
```bash
# Verify credentials
# Access Key: minio
# Secret Key: minio@openspg

# Check MinIO is running
docker logs openspg-minio --tail 50
```

### Issue 5: Containers Won't Start

**Symptoms**: Docker containers exit immediately

**Diagnosis**:
```bash
# Check exit codes and reasons
docker ps -a | grep -E "aeon-ui|openspg"

# View logs for errors
docker logs <container-name>
```

**Common Causes**:
- Port conflicts (3000, 7687, 6333, 3306, 9000 already in use)
- Insufficient Docker resources
- Network conflicts

**Solution**:
```bash
# Check port availability
netstat -an | grep -E "3000|7687|6333|3306|9000"

# Stop conflicting services
# Then restart containers
docker-compose up -d
```

---

## Next Steps

### For Developers

1. **Explore the Wiki**: [[Master-Index]]
   - Read [[Docker-Architecture]] for infrastructure details
   - Review [[REST-API-Reference]] for integration
   - Check [[Cypher-Query-API]] for graph queries

2. **Set Up Development Environment**:
   ```bash
   # Clone repositories
   # Install dependencies
   # Configure development database connections
   ```

3. **Review API Documentation**:
   - [[Neo4j-Database]]
   - [[Qdrant-Vector-Database]]
   - [[MinIO-Object-Storage]]
   - [[AEON-UI-Application]]

### For System Administrators

1. **Review Security Settings**: [[Credentials-Management]]
   - **⚠️ CRITICAL**: Change all default passwords
   - Enable TLS/SSL encryption
   - Configure firewall rules

2. **Set Up Monitoring**:
   - Configure health check alerts
   - Set up log aggregation
   - Monitor resource usage

3. **Plan Backups**:
   - Neo4j graph database backups
   - MySQL database backups
   - MinIO object storage backups
   - Configuration backups

### For Data Scientists

1. **Understand the Knowledge Graph**:
   - Review entity types and relationships
   - Explore ontology structure
   - Learn Cypher query language

2. **Work with Vectors**:
   - Understand embedding models
   - Use Qdrant for similarity search
   - Combine graph + vector search

3. **Access Data**:
   - Query Neo4j for structured data
   - Search Qdrant for semantic similarity
   - Retrieve documents from MinIO

---

## Resources

### Documentation
- [[Master-Index]] - Complete wiki navigation
- [[Docker-Architecture]] - Infrastructure overview
- [[Network-Topology]] - Network configuration
- [[REST-API-Reference]] - API integration guide

### External Resources
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [MinIO Documentation](https://docs.min.io/)
- [Next.js Documentation](https://nextjs.org/docs)

### Support
- Check [[Daily-Updates]] for recent changes
- Review troubleshooting guides in service pages
- Docker logs: `docker logs <container-name>`

---

## Quick Reference Card

### Service Access
| Service | URL | Credentials |
|---------|-----|-------------|
| AEON UI | http://localhost:3000 | None |
| Neo4j Browser | http://localhost:7474 | neo4j / neo4j@openspg |
| Qdrant API | http://localhost:6333 | API Key required |
| MinIO Console | http://localhost:9001 | minio / minio@openspg |

### Container Management
```bash
# View all containers
docker ps

# View logs
docker logs <container-name>

# Restart container
docker restart <container-name>

# Execute command in container
docker exec -it <container-name> bash
```

### Health Checks
```bash
# Overall system health
curl http://localhost:3000/api/health

# Individual services
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "RETURN 1"
docker exec openspg-mysql mysql -uroot -popenspg -e "SELECT 1"
curl http://localhost:6333/collections
curl http://localhost:9000/minio/health/live
```

---

**Status**: Getting Started Guide Complete
**Next**: Explore the wiki and start building!

**Backlinks**: [[Master-Index]] | [[Docker-Architecture]] | [[AEON-UI-Application]] | [[Neo4j-Database]] | [[Qdrant-Vector-Database]] | [[MinIO-Object-Storage]]
