# Backend Connection Patterns for AEON Web UI

**Date:** 2025-11-04
**Status:** ✅ All 5 Backend Services Operational
**Network:** openspg-network (Docker bridge)

## Overview

This document provides connection patterns and examples for all 5 OpenSPG backend services accessible from the AEON Web UI (aeon-saas-dev container).

## Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    openspg-network (Docker Bridge)           │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ aeon-saas-dev│  │openspg-neo4j │  │openspg-qdrant│      │
│  │  (Next.js)   │  │ (Graph DB)   │  │ (Vector DB)  │      │
│  │  Port: 3000  │  │ Port: 7687   │  │ Port: 6333   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                   │              │
│         └─────────────────┴───────────────────┤              │
│                                               │              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │openspg-mysql │  │openspg-minio │  │openspg-server│      │
│  │  (SQL DB)    │  │(Object Store)│  │  (API Server)│      │
│  │  Port: 3306  │  │ Port: 9000   │  │ Port: 8887   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Connection Patterns

### 1. Neo4j Graph Database

**Purpose:** Store and query cybersecurity knowledge graph, threat intelligence, CVE relationships

#### Environment Variables
```bash
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg
```

#### Node.js Connection Pattern
```javascript
const neo4j = require('neo4j-driver');

// Create driver
const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  ),
  {
    maxConnectionLifetime: 3 * 60 * 60 * 1000, // 3 hours
    maxConnectionPoolSize: 50,
    connectionAcquisitionTimeout: 2 * 60 * 1000, // 2 minutes
  }
);

// Query example
async function queryCVEs(severity) {
  const session = driver.session();
  try {
    const result = await session.run(
      'MATCH (cve:CVE {severity: $severity}) RETURN cve LIMIT 10',
      { severity }
    );
    return result.records.map(record => record.get('cve').properties);
  } finally {
    await session.close();
  }
}

// Always close driver on app shutdown
process.on('exit', () => driver.close());
```

#### Next.js API Route Pattern
```javascript
// app/api/graph/cve/[id]/route.ts
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI!,
  neo4j.auth.basic(
    process.env.NEO4J_USER!,
    process.env.NEO4J_PASSWORD!
  )
);

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const session = driver.session();

  try {
    const result = await session.run(
      'MATCH (cve:CVE {id: $id}) RETURN cve',
      { id: params.id }
    );

    if (result.records.length === 0) {
      return Response.json({ error: 'CVE not found' }, { status: 404 });
    }

    return Response.json(result.records[0].get('cve').properties);
  } catch (error) {
    console.error('Neo4j query error:', error);
    return Response.json({ error: 'Database query failed' }, { status: 500 });
  } finally {
    await session.close();
  }
}
```

### 2. Qdrant Vector Database

**Purpose:** Semantic search, document embeddings, similarity search for threat intelligence

#### Environment Variables
```bash
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=
```

#### Node.js Connection Pattern
```javascript
const fetch = require('node-fetch');

class QdrantClient {
  constructor() {
    this.baseUrl = process.env.QDRANT_URL || 'http://openspg-qdrant:6333';
    this.apiKey = process.env.QDRANT_API_KEY;
  }

  async listCollections() {
    const response = await fetch(`${this.baseUrl}/collections`, {
      headers: { 'api-key': this.apiKey }
    });
    return response.json();
  }

  async search(collection, vector, limit = 10) {
    const response = await fetch(
      `${this.baseUrl}/collections/${collection}/points/search`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'api-key': this.apiKey
        },
        body: JSON.stringify({
          vector,
          limit,
          with_payload: true
        })
      }
    );
    return response.json();
  }

  async upsert(collection, points) {
    const response = await fetch(
      `${this.baseUrl}/collections/${collection}/points`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'api-key': this.apiKey
        },
        body: JSON.stringify({ points })
      }
    );
    return response.json();
  }
}

// Usage
const qdrant = new QdrantClient();
const results = await qdrant.search('threat-intel', [0.1, 0.2, ...], 5);
```

#### Next.js API Route Pattern
```javascript
// app/api/search/semantic/route.ts
export async function POST(request: Request) {
  const { query, collection = 'threat-intel', limit = 10 } = await request.json();

  // 1. Generate embedding from query using OpenAI
  const embedding = await generateEmbedding(query);

  // 2. Search Qdrant
  const response = await fetch(
    `${process.env.QDRANT_URL}/collections/${collection}/points/search`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': process.env.QDRANT_API_KEY!
      },
      body: JSON.stringify({
        vector: embedding,
        limit,
        with_payload: true
      })
    }
  );

  const results = await response.json();
  return Response.json(results);
}
```

### 3. MySQL Relational Database

**Purpose:** OpenSPG metadata, schema definitions, project configurations

#### Environment Variables
```bash
MYSQL_HOST=openspg-mysql
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=openspg
MYSQL_DATABASE=openspg
```

#### Node.js Connection Pattern
```javascript
const mysql = require('mysql2/promise');

// Create connection pool
const pool = mysql.createPool({
  host: process.env.MYSQL_HOST || 'openspg-mysql',
  port: process.env.MYSQL_PORT || 3306,
  user: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASSWORD || 'openspg',
  database: process.env.MYSQL_DATABASE || 'openspg',
  connectionLimit: 10,
  waitForConnections: true,
  queueLimit: 0
});

// Query example
async function getProjects() {
  const [rows] = await pool.execute(
    'SELECT * FROM kg_project WHERE status = ?',
    ['ACTIVE']
  );
  return rows;
}

// Prepared statement example
async function getProjectById(id) {
  const [rows] = await pool.execute(
    'SELECT * FROM kg_project WHERE id = ?',
    [id]
  );
  return rows[0];
}

// Transaction example
async function createProject(name, description) {
  const connection = await pool.getConnection();
  await connection.beginTransaction();

  try {
    const [result] = await connection.execute(
      'INSERT INTO kg_project (name, description, created_at) VALUES (?, ?, NOW())',
      [name, description]
    );
    await connection.commit();
    return result.insertId;
  } catch (error) {
    await connection.rollback();
    throw error;
  } finally {
    connection.release();
  }
}
```

#### Next.js API Route Pattern
```javascript
// app/api/projects/route.ts
import mysql from 'mysql2/promise';

const pool = mysql.createPool({
  host: process.env.MYSQL_HOST!,
  port: parseInt(process.env.MYSQL_PORT || '3306'),
  user: process.env.MYSQL_USER!,
  password: process.env.MYSQL_PASSWORD!,
  database: process.env.MYSQL_DATABASE!,
  connectionLimit: 10
});

export async function GET() {
  try {
    const [rows] = await pool.execute('SELECT * FROM kg_project');
    return Response.json(rows);
  } catch (error) {
    console.error('MySQL error:', error);
    return Response.json({ error: 'Database query failed' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  const { name, description } = await request.json();

  try {
    const [result] = await pool.execute(
      'INSERT INTO kg_project (name, description) VALUES (?, ?)',
      [name, description]
    );
    return Response.json({ id: result.insertId }, { status: 201 });
  } catch (error) {
    console.error('MySQL error:', error);
    return Response.json({ error: 'Insert failed' }, { status: 500 });
  }
}
```

### 4. MinIO Object Storage

**Purpose:** File uploads, document storage, threat intelligence reports, backups

#### Environment Variables
```bash
MINIO_ENDPOINT=openspg-minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_BUCKET=aeon-uploads
MINIO_USE_SSL=false
```

#### Node.js Connection Pattern
```javascript
const Minio = require('minio');

// Create MinIO client
const minioClient = new Minio.Client({
  endPoint: process.env.MINIO_ENDPOINT || 'openspg-minio',
  port: parseInt(process.env.MINIO_PORT || '9000'),
  useSSL: process.env.MINIO_USE_SSL === 'true',
  accessKey: process.env.MINIO_ACCESS_KEY || 'minio',
  secretKey: process.env.MINIO_SECRET_KEY || 'minio@openspg'
});

// Upload file
async function uploadFile(bucketName, objectName, stream, size, metadata = {}) {
  // Ensure bucket exists
  const bucketExists = await minioClient.bucketExists(bucketName);
  if (!bucketExists) {
    await minioClient.makeBucket(bucketName, 'us-east-1');
  }

  await minioClient.putObject(bucketName, objectName, stream, size, metadata);
  return { bucket: bucketName, object: objectName };
}

// Download file
async function downloadFile(bucketName, objectName) {
  const stream = await minioClient.getObject(bucketName, objectName);
  return stream;
}

// Get presigned URL (for direct browser uploads/downloads)
async function getPresignedUrl(bucketName, objectName, expiry = 3600) {
  const url = await minioClient.presignedGetObject(bucketName, objectName, expiry);
  return url;
}

// List objects
async function listObjects(bucketName, prefix = '', recursive = false) {
  const stream = minioClient.listObjectsV2(bucketName, prefix, recursive);
  const objects = [];

  return new Promise((resolve, reject) => {
    stream.on('data', obj => objects.push(obj));
    stream.on('error', reject);
    stream.on('end', () => resolve(objects));
  });
}
```

#### Next.js API Route Pattern
```javascript
// app/api/upload/route.ts
import { Client as MinioClient } from 'minio';

const minio = new MinioClient({
  endPoint: process.env.MINIO_ENDPOINT!,
  port: parseInt(process.env.MINIO_PORT || '9000'),
  useSSL: false,
  accessKey: process.env.MINIO_ACCESS_KEY!,
  secretKey: process.env.MINIO_SECRET_KEY!
});

export async function POST(request: Request) {
  const formData = await request.formData();
  const file = formData.get('file') as File;

  if (!file) {
    return Response.json({ error: 'No file provided' }, { status: 400 });
  }

  const bucket = process.env.MINIO_BUCKET || 'aeon-uploads';
  const objectName = `${Date.now()}-${file.name}`;

  try {
    // Convert File to Buffer
    const buffer = Buffer.from(await file.arrayBuffer());

    // Upload to MinIO
    await minio.putObject(
      bucket,
      objectName,
      buffer,
      buffer.length,
      {
        'Content-Type': file.type,
        'X-Uploaded-By': 'aeon-web-ui'
      }
    );

    // Generate presigned URL for download
    const url = await minio.presignedGetObject(bucket, objectName, 24 * 60 * 60);

    return Response.json({
      bucket,
      object: objectName,
      url,
      size: buffer.length
    });
  } catch (error) {
    console.error('MinIO upload error:', error);
    return Response.json({ error: 'Upload failed' }, { status: 500 });
  }
}
```

### 5. OpenSPG Server

**Purpose:** Knowledge graph operations, schema management, SPARQL queries

#### Environment Variables
```bash
OPENSPG_SERVER_URL=http://openspg-server:8887
```

#### Node.js Connection Pattern
```javascript
class OpenSPGClient {
  constructor() {
    this.baseUrl = process.env.OPENSPG_SERVER_URL || 'http://openspg-server:8887';
  }

  async getProjects() {
    const response = await fetch(`${this.baseUrl}/api/v1/project/list`, {
      headers: { 'Content-Type': 'application/json' }
    });
    return response.json();
  }

  async createSchema(projectId, schema) {
    const response = await fetch(
      `${this.baseUrl}/api/v1/schema/create`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId,
          schema
        })
      }
    );
    return response.json();
  }

  async executeQuery(projectId, query) {
    const response = await fetch(
      `${this.baseUrl}/api/v1/query/execute`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId,
          query
        })
      }
    );
    return response.json();
  }
}

// Usage
const openspg = new OpenSPGClient();
const projects = await openspg.getProjects();
```

#### Next.js API Route Pattern
```javascript
// app/api/openspg/query/route.ts
export async function POST(request: Request) {
  const { projectId, query } = await request.json();

  const response = await fetch(
    `${process.env.OPENSPG_SERVER_URL}/api/v1/query/execute`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectId, query })
    }
  );

  if (!response.ok) {
    return Response.json(
      { error: 'OpenSPG query failed' },
      { status: response.status }
    );
  }

  const data = await response.json();
  return Response.json(data);
}
```

## Connection Pooling Best Practices

### Neo4j
- Use single driver instance (singleton pattern)
- Set `maxConnectionPoolSize: 50`
- Set `maxConnectionLifetime: 3 hours`
- Always close sessions after use
- Close driver on app shutdown

### MySQL
- Use connection pooling (`mysql2/promise` pool)
- Set `connectionLimit: 10` for web apps
- Set `waitForConnections: true`
- Release connections after use
- Use transactions for multi-statement operations

### Qdrant
- HTTP client with connection keep-alive
- Implement retry logic for transient failures
- Cache collection metadata
- Use batch operations for bulk upserts

### MinIO
- Reuse client instance
- Use presigned URLs for direct browser uploads/downloads
- Implement multipart upload for large files
- Set appropriate expiry times for presigned URLs

### OpenSPG Server
- HTTP client with connection keep-alive
- Implement request timeout (30s default)
- Cache project metadata
- Use error handling for API failures

## Error Handling Pattern

```javascript
async function safeBackendCall(operation, serviceName) {
  try {
    return await operation();
  } catch (error) {
    console.error(`${serviceName} error:`, error);

    // Log to monitoring service
    await logError(serviceName, error);

    // Return graceful error response
    return {
      success: false,
      error: `${serviceName} temporarily unavailable`,
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    };
  }
}

// Usage
const result = await safeBackendCall(
  () => qdrant.search('threat-intel', vector),
  'Qdrant'
);
```

## Health Check Integration

```javascript
// app/api/health/route.ts
export async function GET() {
  const checks = await Promise.allSettled([
    checkNeo4j(),
    checkQdrant(),
    checkMySQL(),
    checkMinIO(),
    checkOpenSPG()
  ]);

  const services = ['Neo4j', 'Qdrant', 'MySQL', 'MinIO', 'OpenSPG'];
  const health = checks.map((result, i) => ({
    service: services[i],
    status: result.status === 'fulfilled' ? 'healthy' : 'unhealthy',
    error: result.status === 'rejected' ? result.reason.message : undefined
  }));

  const allHealthy = health.every(s => s.status === 'healthy');

  return Response.json(
    { services: health, overall: allHealthy ? 'healthy' : 'degraded' },
    { status: allHealthy ? 200 : 503 }
  );
}
```

## Testing Connectivity

Run the comprehensive test suite:

```bash
# From host
docker exec aeon-saas-dev npm test tests/backend-connectivity.test.js

# From inside container
docker exec -it aeon-saas-dev /bin/sh
npm test tests/backend-connectivity.test.js
```

## Troubleshooting

### Connection Refused
- Verify service is running: `docker ps --filter "name=openspg"`
- Check network connectivity: `docker network inspect openspg-network`
- Verify environment variables are set correctly

### Authentication Failures
- Check credentials in `.env.development`
- Verify API keys are correctly formatted
- Ensure credentials match docker-compose configuration

### Timeout Errors
- Increase timeout values in client configuration
- Check service health: `docker logs <service-name>`
- Verify network latency is acceptable

### Data Not Found
- Verify data has been imported into services
- Check database/collection names
- Verify query syntax is correct

## Status Summary

✅ **Neo4j**: Fully operational - Graph queries working
✅ **Qdrant**: Fully operational - Vector search working
✅ **MySQL**: Fully operational - SQL queries working
✅ **MinIO**: Fully operational - Object storage working
✅ **OpenSPG**: Fully operational - API server responding

**Last Verified:** 2025-11-04
**Network:** openspg-network (bridge)
**All Services:** 100% connectivity achieved from aeon-saas-dev container
