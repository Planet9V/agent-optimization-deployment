# AEON Digital Twin - Backend Access & Integration Guide

**Document Version:** 2.0.0
**Created:** 2025-01-04
**Backend Services:** Neo4j 5.25, Qdrant 1.15.1, MySQL 3.11.3, MinIO 8.0.1, OpenSPG
**Purpose:** Complete backend integration instructions for frontend developers

---

## Table of Contents

1. [Overview](#overview)
2. [Neo4j Graph Database](#neo4j-graph-database)
3. [Qdrant Vector Database](#qdrant-vector-database)
4. [MySQL Relational Database](#mysql-relational-database)
5. [MinIO Object Storage](#minio-object-storage)
6. [OpenSPG Server](#openspg-server)
7. [Hybrid Search Implementation](#hybrid-search-implementation)
8. [API Route Patterns](#api-route-patterns)
9. [Error Handling](#error-handling)
10. [Security Best Practices](#security-best-practices)
11. [Testing & Debugging](#testing--debugging)

---

## 1. Overview

### 1.1 Backend Architecture

The AEON Digital Twin platform integrates **5 backend services**, each serving a specific purpose:

| Service | Technology | Port | Purpose |
|---------|-----------|------|---------|
| **Neo4j** | Graph Database | 7687 (Bolt), 7474 (HTTP) | CVE knowledge graph, threat intelligence relationships |
| **Qdrant** | Vector Database | 6333 | Semantic search, document embeddings, similarity queries |
| **MySQL** | Relational DB | 3306 | User data, saved searches, tags, metadata |
| **MinIO** | Object Storage | 9000 (API), 9001 (Console) | File uploads, PDF storage, reports |
| **OpenSPG** | Knowledge Graph Pipeline | 8887 | Document processing, entity extraction, graph enrichment |

### 1.2 Integration Strategy

**Server Components (Preferred):**
- Direct backend access from Next.js Server Components
- Zero API routes needed for simple queries
- Better security (credentials never exposed to client)

**API Routes (When Needed):**
- Client-side data fetching
- Real-time updates and polling
- Streaming responses (AI chat, large datasets)

**Environment Variables:**
All backend credentials stored in `.env.local` (never committed to Git)

### 1.3 Quick Setup

```bash
# Create .env.local
cp .env.example .env.local

# Configure backend URLs
OPENAI_API_KEY=sk-your-key-here
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=
DATABASE_URL=mysql://root:openspg@openspg-mysql:3306/openspg
MINIO_ENDPOINT=openspg-minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false
OPENSPG_SERVER_URL=http://openspg-server:8887

# Verify connections
curl http://localhost:3000/api/health
```

---

## 2. Neo4j Graph Database

### 2.1 Connection Setup

**Package:**
```bash
npm install neo4j-driver@5.25.0
```

**Client Configuration (`lib/neo4j-enhanced.ts`):**

```typescript
import neo4j, { Driver, Session, Result, auth } from 'neo4j-driver';

// Singleton driver instance
let driver: Driver | null = null;

export function getNeo4jDriver(): Driver {
  if (!driver) {
    driver = neo4j.driver(
      process.env.NEO4J_URI!,
      auth.basic(process.env.NEO4J_USER!, process.env.NEO4J_PASSWORD!),
      {
        maxConnectionPoolSize: 50,
        connectionAcquisitionTimeout: 60000, // 60 seconds
        connectionTimeout: 30000,             // 30 seconds
        maxTransactionRetryTime: 30000,       // 30 seconds
      }
    );

    // Verify connectivity on initialization
    driver.verifyConnectivity()
      .then(() => console.log('✅ Neo4j connected'))
      .catch(err => console.error('❌ Neo4j connection failed:', err));
  }

  return driver;
}

export async function runCypherQuery(
  cypher: string,
  params: Record<string, any> = {}
): Promise<any[]> {
  const driver = getNeo4jDriver();
  const session: Session = driver.session({ database: 'neo4j' });

  try {
    const result: Result = await session.run(cypher, params);
    return result.records.map(record => record.toObject());
  } catch (error) {
    console.error('Cypher query error:', error);
    throw error;
  } finally {
    await session.close();
  }
}

// Transaction helper for write operations
export async function runCypherTransaction(
  transactionWork: (tx: any) => Promise<any>
): Promise<any> {
  const driver = getNeo4jDriver();
  const session = driver.session({ database: 'neo4j' });

  try {
    return await session.writeTransaction(transactionWork);
  } catch (error) {
    console.error('Transaction error:', error);
    throw error;
  } finally {
    await session.close();
  }
}

// Cleanup on application shutdown
export async function closeNeo4jConnection() {
  if (driver) {
    await driver.close();
    driver = null;
  }
}
```

### 2.2 Common Query Patterns

#### 2.2.1 Read Queries (Graph Traversal)

```typescript
// Get all CVE nodes with relationships
export async function getCVEWithRelationships(cveId: string) {
  const cypher = `
    MATCH (cve:CVE {id: $cveId})
    OPTIONAL MATCH (cve)-[r]-(related)
    RETURN cve, type(r) as relationshipType, related
    LIMIT 100
  `;

  return await runCypherQuery(cypher, { cveId });
}

// Find shortest path between two nodes
export async function findShortestPath(startId: string, endId: string) {
  const cypher = `
    MATCH (start {id: $startId}), (end {id: $endId})
    MATCH path = shortestPath((start)-[*..10]-(end))
    RETURN path
  `;

  return await runCypherQuery(cypher, { startId, endId });
}

// Graph traversal with depth limit
export async function getThreatActorNetwork(actorId: string) {
  const cypher = `
    MATCH (actor:ThreatActor {id: $actorId})
    CALL apoc.path.subgraphNodes(actor, {
      relationshipFilter: 'USES|TARGETS|ASSOCIATED_WITH',
      maxLevel: 3
    })
    YIELD node
    RETURN node
  `;

  return await runCypherQuery(cypher, { actorId });
}
```

#### 2.2.2 Aggregation Queries

```typescript
// Count nodes by type
export async function getNodeCounts() {
  const cypher = `
    CALL db.labels() YIELD label
    CALL {
      WITH label
      MATCH (n)
      WHERE label IN labels(n)
      RETURN count(n) as count
    }
    RETURN label, count
    ORDER BY count DESC
  `;

  return await runCypherQuery(cypher);
}

// Severity distribution
export async function getSeverityDistribution() {
  const cypher = `
    MATCH (cve:CVE)
    RETURN cve.severity as severity, count(*) as count
    ORDER BY count DESC
  `;

  return await runCypherQuery(cypher);
}
```

#### 2.2.3 Full-Text Search

```typescript
// Setup full-text index (run once)
export async function createFullTextIndex() {
  const cypher = `
    CREATE FULLTEXT INDEX cve_fulltext IF NOT EXISTS
    FOR (cve:CVE)
    ON EACH [cve.id, cve.description, cve.summary]
  `;

  return await runCypherQuery(cypher);
}

// Search using full-text index
export async function searchCVEs(searchTerm: string) {
  const cypher = `
    CALL db.index.fulltext.queryNodes('cve_fulltext', $searchTerm)
    YIELD node, score
    RETURN node, score
    ORDER BY score DESC
    LIMIT 20
  `;

  return await runCypherQuery(cypher, { searchTerm });
}
```

### 2.3 Server Component Usage

```tsx
// app/graph/data/page.tsx
import { runCypherQuery } from '@/lib/neo4j-enhanced';

export default async function GraphDataPage() {
  // Direct backend access in Server Component
  const nodeCounts = await runCypherQuery(`
    CALL db.labels() YIELD label
    CALL {
      WITH label
      MATCH (n) WHERE label IN labels(n)
      RETURN count(n) as count
    }
    RETURN label, count
    ORDER BY count DESC
  `);

  return (
    <div>
      <h1>Graph Statistics</h1>
      <ul>
        {nodeCounts.map((item: any) => (
          <li key={item.label}>
            {item.label}: {item.count}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### 2.4 API Route Pattern

```typescript
// app/api/graph/query/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { runCypherQuery } from '@/lib/neo4j-enhanced';

export async function POST(request: NextRequest) {
  try {
    const { query, params } = await request.json();

    // Security: Only allow READ queries
    if (!/^(MATCH|RETURN|WITH|CALL|OPTIONAL MATCH)/i.test(query.trim())) {
      return NextResponse.json(
        { error: 'Only read queries are allowed' },
        { status: 400 }
      );
    }

    const results = await runCypherQuery(query, params);

    return NextResponse.json({
      success: true,
      results,
      count: results.length,
    });
  } catch (error: any) {
    console.error('Neo4j query error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

### 2.5 Visualization Data Format

```typescript
// Format Neo4j results for vis-network
export function formatGraphForVisualization(records: any[]) {
  const nodes: any[] = [];
  const edges: any[] = [];
  const nodeIds = new Set();

  records.forEach(record => {
    // Extract nodes
    if (record.node) {
      const node = record.node;
      if (!nodeIds.has(node.identity.toString())) {
        nodes.push({
          id: node.identity.toString(),
          label: node.properties.id || node.properties.name,
          group: node.labels[0],
          title: JSON.stringify(node.properties, null, 2),
        });
        nodeIds.add(node.identity.toString());
      }
    }

    // Extract relationships
    if (record.relationship) {
      const rel = record.relationship;
      edges.push({
        from: rel.start.toString(),
        to: rel.end.toString(),
        label: rel.type,
        arrows: 'to',
      });
    }
  });

  return { nodes, edges };
}
```

---

## 3. Qdrant Vector Database

### 3.1 Connection Setup

**Package:**
```bash
npm install @qdrant/js-client-rest@1.15.1
```

**Client Configuration (`lib/qdrant-client.ts`):**

```typescript
import { QdrantClient } from '@qdrant/js-client-rest';

let client: QdrantClient | null = null;

export function getQdrantClient(): QdrantClient {
  if (!client) {
    client = new QdrantClient({
      url: process.env.QDRANT_URL!,
      apiKey: process.env.QDRANT_API_KEY,
    });

    console.log('✅ Qdrant client initialized');
  }

  return client;
}

// Collection management
export async function ensureCollection(
  collectionName: string,
  vectorSize: number = 1536
) {
  const client = getQdrantClient();

  try {
    await client.getCollection(collectionName);
    console.log(`Collection ${collectionName} exists`);
  } catch (error) {
    console.log(`Creating collection ${collectionName}...`);
    await client.createCollection(collectionName, {
      vectors: {
        size: vectorSize,
        distance: 'Cosine',
      },
    });
  }
}
```

### 3.2 Embedding Generation

```typescript
// lib/embeddings.ts
import { OpenAI } from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });

  return response.data[0].embedding;
}

export async function generateBatchEmbeddings(texts: string[]): Promise<number[][]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: texts,
  });

  return response.data.map(item => item.embedding);
}
```

### 3.3 Vector Search Operations

```typescript
// lib/qdrant-client.ts (continued)

import { generateEmbedding } from './embeddings';

export async function semanticSearch(
  collectionName: string,
  query: string,
  limit: number = 10,
  filter?: any
) {
  const client = getQdrantClient();

  // Generate embedding for query
  const queryVector = await generateEmbedding(query);

  // Search Qdrant
  const results = await client.search(collectionName, {
    vector: queryVector,
    limit,
    with_payload: true,
    with_vector: false,
    filter,
  });

  return results;
}

export async function insertDocuments(
  collectionName: string,
  documents: Array<{ id: string; text: string; metadata: any }>
) {
  const client = getQdrantClient();

  // Generate embeddings for all documents
  const embeddings = await generateBatchEmbeddings(
    documents.map(doc => doc.text)
  );

  // Prepare points for insertion
  const points = documents.map((doc, index) => ({
    id: doc.id,
    vector: embeddings[index],
    payload: {
      text: doc.text,
      ...doc.metadata,
    },
  }));

  // Insert into Qdrant
  await client.upsert(collectionName, {
    wait: true,
    points,
  });

  return points.length;
}

export async function searchWithFilters(
  collectionName: string,
  query: string,
  filters: {
    severity?: string[];
    dateRange?: { start: string; end: string };
    tags?: string[];
  }
) {
  const client = getQdrantClient();
  const queryVector = await generateEmbedding(query);

  // Build Qdrant filter
  const filter: any = {
    must: [],
  };

  if (filters.severity?.length) {
    filter.must.push({
      key: 'severity',
      match: { any: filters.severity },
    });
  }

  if (filters.dateRange) {
    filter.must.push({
      key: 'timestamp',
      range: {
        gte: filters.dateRange.start,
        lte: filters.dateRange.end,
      },
    });
  }

  if (filters.tags?.length) {
    filter.must.push({
      key: 'tags',
      match: { any: filters.tags },
    });
  }

  const results = await client.search(collectionName, {
    vector: queryVector,
    limit: 20,
    with_payload: true,
    filter: filter.must.length > 0 ? filter : undefined,
  });

  return results;
}
```

### 3.4 API Route Example

```typescript
// app/api/search/vector/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { semanticSearch } from '@/lib/qdrant-client';

export async function POST(request: NextRequest) {
  try {
    const { query, collection, limit, filters } = await request.json();

    if (!query || !collection) {
      return NextResponse.json(
        { error: 'Query and collection are required' },
        { status: 400 }
      );
    }

    const results = await semanticSearch(
      collection,
      query,
      limit || 10,
      filters
    );

    return NextResponse.json({
      success: true,
      results,
      count: results.length,
    });
  } catch (error: any) {
    console.error('Qdrant search error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

---

## 4. MySQL Relational Database

### 4.1 Prisma ORM Setup

**Packages:**
```bash
npm install @prisma/client@5.22.0 prisma@5.22.0
```

**Database URL (`.env.local`):**
```env
DATABASE_URL="mysql://root:openspg@openspg-mysql:3306/openspg"
```

**Prisma Schema (`prisma/schema.prisma`):**

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      String   @default("user")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  savedSearches SavedSearch[]
  tags          Tag[]

  @@map("users")
}

model SavedSearch {
  id        String   @id @default(cuid())
  userId    String
  name      String
  query     String   @db.Text
  filters   Json?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@map("saved_searches")
}

model Tag {
  id          String   @id @default(cuid())
  name        String   @unique
  color       String?
  description String?  @db.Text
  userId      String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  user   User          @relation(fields: [userId], references: [id], onDelete: Cascade)
  tagged TaggedEntity[]

  @@index([userId])
  @@map("tags")
}

model TaggedEntity {
  id         String   @id @default(cuid())
  tagId      String
  entityId   String
  entityType String
  createdAt  DateTime @default(now())

  tag Tag @relation(fields: [tagId], references: [id], onDelete: Cascade)

  @@unique([tagId, entityId])
  @@index([entityId])
  @@map("tagged_entities")
}

model Customer {
  id        String   @id @default(cuid())
  name      String
  email     String?  @unique
  phone     String?
  company   String?
  notes     String?  @db.Text
  status    String   @default("active")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([status])
  @@map("customers")
}

model ActivityLog {
  id          String   @id @default(cuid())
  userId      String?
  action      String
  entityType  String
  entityId    String?
  metadata    Json?
  ipAddress   String?
  userAgent   String?  @db.Text
  createdAt   DateTime @default(now())

  @@index([userId])
  @@index([createdAt])
  @@map("activity_logs")
}
```

**Generate Prisma Client:**
```bash
npx prisma generate
npx prisma db push
```

### 4.2 Prisma Client Configuration

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

declare global {
  var prisma: PrismaClient | undefined;
}

export const prisma = global.prisma || new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  global.prisma = prisma;
}

// Connection test
prisma.$connect()
  .then(() => console.log('✅ MySQL (Prisma) connected'))
  .catch(err => console.error('❌ MySQL connection failed:', err));
```

### 4.3 Common Database Operations

#### 4.3.1 User Management

```typescript
// lib/db/users.ts
import { prisma } from '@/lib/prisma';

export async function createUser(data: {
  email: string;
  name: string;
  role?: string;
}) {
  return await prisma.user.create({
    data,
  });
}

export async function getUserById(id: string) {
  return await prisma.user.findUnique({
    where: { id },
    include: {
      savedSearches: true,
      tags: true,
    },
  });
}

export async function updateUser(id: string, data: any) {
  return await prisma.user.update({
    where: { id },
    data,
  });
}
```

#### 4.3.2 Saved Searches

```typescript
// lib/db/saved-searches.ts
import { prisma } from '@/lib/prisma';

export async function getUserSavedSearches(userId: string) {
  return await prisma.savedSearch.findMany({
    where: { userId },
    orderBy: { createdAt: 'desc' },
  });
}

export async function createSavedSearch(data: {
  userId: string;
  name: string;
  query: string;
  filters?: any;
}) {
  return await prisma.savedSearch.create({
    data: {
      ...data,
      filters: data.filters || {},
    },
  });
}

export async function deleteSavedSearch(id: string, userId: string) {
  return await prisma.savedSearch.deleteMany({
    where: {
      id,
      userId, // Ensure user owns the search
    },
  });
}
```

#### 4.3.3 Tags and Tagging

```typescript
// lib/db/tags.ts
import { prisma } from '@/lib/prisma';

export async function getAllTags(userId: string) {
  return await prisma.tag.findMany({
    where: { userId },
    include: {
      _count: {
        select: { tagged: true },
      },
    },
    orderBy: { name: 'asc' },
  });
}

export async function createTag(data: {
  name: string;
  color?: string;
  description?: string;
  userId: string;
}) {
  return await prisma.tag.create({
    data,
  });
}

export async function assignTag(
  tagId: string,
  entityId: string,
  entityType: string
) {
  return await prisma.taggedEntity.create({
    data: {
      tagId,
      entityId,
      entityType,
    },
  });
}

export async function getEntitiesByTag(tagId: string) {
  return await prisma.taggedEntity.findMany({
    where: { tagId },
    include: {
      tag: true,
    },
  });
}
```

### 4.4 API Route Example

```typescript
// app/api/customers/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const status = searchParams.get('status');

    const customers = await prisma.customer.findMany({
      where: status ? { status } : undefined,
      orderBy: { createdAt: 'desc' },
    });

    return NextResponse.json({
      success: true,
      customers,
      count: customers.length,
    });
  } catch (error: any) {
    console.error('Error fetching customers:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();

    const customer = await prisma.customer.create({
      data,
    });

    return NextResponse.json({
      success: true,
      customer,
    }, { status: 201 });
  } catch (error: any) {
    console.error('Error creating customer:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

---

## 5. MinIO Object Storage

### 5.1 Connection Setup

**Package:**
```bash
npm install minio@8.0.1
```

**Client Configuration (`lib/minio-client.ts`):**

```typescript
import * as Minio from 'minio';

let minioClient: Minio.Client | null = null;

export function getMinioClient(): Minio.Client {
  if (!minioClient) {
    minioClient = new Minio.Client({
      endPoint: process.env.MINIO_ENDPOINT!,
      port: parseInt(process.env.MINIO_PORT!),
      useSSL: process.env.MINIO_USE_SSL === 'true',
      accessKey: process.env.MINIO_ACCESS_KEY!,
      secretKey: process.env.MINIO_SECRET_KEY!,
    });

    console.log('✅ MinIO client initialized');
  }

  return minioClient;
}

// Ensure bucket exists
export async function ensureBucket(bucketName: string) {
  const client = getMinioClient();

  const exists = await client.bucketExists(bucketName);

  if (!exists) {
    console.log(`Creating bucket: ${bucketName}`);
    await client.makeBucket(bucketName, 'us-east-1');
  }
}
```

### 5.2 File Upload Operations

```typescript
// lib/minio-client.ts (continued)

export async function uploadFile(
  bucketName: string,
  filename: string,
  file: Buffer,
  metadata?: Minio.ItemBucketMetadata
) {
  const client = getMinioClient();
  await ensureBucket(bucketName);

  // Upload file
  await client.putObject(bucketName, filename, file, file.length, metadata);

  // Generate presigned URL (valid for 1 hour)
  const url = await client.presignedGetObject(bucketName, filename, 3600);

  return {
    filename,
    bucket: bucketName,
    size: file.length,
    url,
  };
}

export async function uploadStream(
  bucketName: string,
  filename: string,
  stream: NodeJS.ReadableStream,
  size: number,
  metadata?: Minio.ItemBucketMetadata
) {
  const client = getMinioClient();
  await ensureBucket(bucketName);

  await client.putObject(bucketName, filename, stream, size, metadata);

  return {
    filename,
    bucket: bucketName,
    size,
  };
}
```

### 5.3 File Download Operations

```typescript
// lib/minio-client.ts (continued)

export async function getFile(bucketName: string, filename: string): Promise<Buffer> {
  const client = getMinioClient();

  const dataStream = await client.getObject(bucketName, filename);

  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    dataStream.on('data', chunk => chunks.push(chunk));
    dataStream.on('end', () => resolve(Buffer.concat(chunks)));
    dataStream.on('error', reject);
  });
}

export async function getPresignedDownloadUrl(
  bucketName: string,
  filename: string,
  expirySeconds: number = 3600
): Promise<string> {
  const client = getMinioClient();
  return await client.presignedGetObject(bucketName, filename, expirySeconds);
}

export async function listFiles(bucketName: string, prefix?: string) {
  const client = getMinioClient();
  const stream = client.listObjects(bucketName, prefix, true);

  const files: any[] = [];

  return new Promise((resolve, reject) => {
    stream.on('data', obj => files.push(obj));
    stream.on('end', () => resolve(files));
    stream.on('error', reject);
  });
}
```

### 5.4 File Management

```typescript
// lib/minio-client.ts (continued)

export async function deleteFile(bucketName: string, filename: string) {
  const client = getMinioClient();
  await client.removeObject(bucketName, filename);
}

export async function deleteFiles(bucketName: string, filenames: string[]) {
  const client = getMinioClient();
  await client.removeObjects(bucketName, filenames);
}

export async function getFileMetadata(bucketName: string, filename: string) {
  const client = getMinioClient();
  return await client.statObject(bucketName, filename);
}
```

### 5.5 Upload API Route

```typescript
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { uploadFile } from '@/lib/minio-client';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // Convert File to Buffer
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // Generate unique filename
    const filename = `${Date.now()}-${file.name}`;

    // Upload to MinIO
    const result = await uploadFile('uploads', filename, buffer, {
      'Content-Type': file.type,
      'X-Uploaded-By': 'aeon-ui',
    });

    return NextResponse.json({
      success: true,
      file: {
        ...result,
        originalName: file.name,
        contentType: file.type,
      },
    });
  } catch (error: any) {
    console.error('File upload error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

---

## 6. OpenSPG Server

### 6.1 Connection Setup

OpenSPG uses HTTP REST API for document processing and knowledge graph operations.

```typescript
// lib/openspg-client.ts

const OPENSPG_BASE_URL = process.env.OPENSPG_SERVER_URL!;

export async function opneSPGRequest(
  endpoint: string,
  method: string = 'GET',
  body?: any
) {
  const url = `${OPENSPG_BASE_URL}${endpoint}`;

  const options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);

  if (!response.ok) {
    throw new Error(`OpenSPG request failed: ${response.statusText}`);
  }

  return await response.json();
}
```

### 6.2 Document Processing

```typescript
// lib/openspg-client.ts (continued)

export async function processDocument(
  documentUrl: string,
  options?: {
    extractEntities?: boolean;
    buildGraph?: boolean;
    language?: string;
  }
) {
  return await opneSPGRequest('/api/v1/process', 'POST', {
    documentUrl,
    options: {
      extractEntities: options?.extractEntities ?? true,
      buildGraph: options?.buildGraph ?? true,
      language: options?.language ?? 'en',
    },
  });
}

export async function getProcessingStatus(jobId: string) {
  return await opneSPGRequest(`/api/v1/status/${jobId}`);
}

export async function getProcessingResults(jobId: string) {
  return await opneSPGRequest(`/api/v1/results/${jobId}`);
}
```

### 6.3 Entity Extraction

```typescript
// lib/openspg-client.ts (continued)

export async function extractEntities(text: string) {
  return await opneSPGRequest('/api/v1/extract', 'POST', {
    text,
    entityTypes: ['CVE', 'ThreatActor', 'Malware', 'Technique'],
  });
}

export async function enrichGraph(entityId: string, entityType: string) {
  return await opneSPGRequest('/api/v1/enrich', 'POST', {
    entityId,
    entityType,
    sources: ['external_threat_intel', 'cve_database'],
  });
}
```

### 6.4 API Route Example

```typescript
// app/api/pipeline/process/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { processDocument, getProcessingStatus } from '@/lib/openspg-client';

export async function POST(request: NextRequest) {
  try {
    const { documentUrl } = await request.json();

    if (!documentUrl) {
      return NextResponse.json(
        { error: 'Document URL is required' },
        { status: 400 }
      );
    }

    // Start processing
    const result = await processDocument(documentUrl);

    return NextResponse.json({
      success: true,
      jobId: result.jobId,
      status: result.status,
    });
  } catch (error: any) {
    console.error('Document processing error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const jobId = searchParams.get('jobId');

    if (!jobId) {
      return NextResponse.json(
        { error: 'Job ID is required' },
        { status: 400 }
      );
    }

    const status = await getProcessingStatus(jobId);

    return NextResponse.json({
      success: true,
      ...status,
    });
  } catch (error: any) {
    console.error('Status check error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

---

## 7. Hybrid Search Implementation

### 7.1 Combined Neo4j + Qdrant Search

```typescript
// lib/hybrid-search.ts
import { runCypherQuery } from './neo4j-enhanced';
import { semanticSearch } from './qdrant-client';

export async function hybridSearch(query: string, options?: {
  neo4jWeight?: number;
  qdrantWeight?: number;
  limit?: number;
}) {
  const neo4jWeight = options?.neo4jWeight ?? 0.5;
  const qdrantWeight = options?.qdrantWeight ?? 0.5;
  const limit = options?.limit ?? 20;

  // Parallel search execution
  const [neo4jResults, qdrantResults] = await Promise.all([
    // Neo4j full-text search
    runCypherQuery(`
      CALL db.index.fulltext.queryNodes('cve_fulltext', $query)
      YIELD node, score
      RETURN node, score
      ORDER BY score DESC
      LIMIT ${limit}
    `, { query }),

    // Qdrant vector search
    semanticSearch('threat_intel', query, limit),
  ]);

  // Combine and rank results
  const combinedResults = mergeAndRankResults(
    neo4jResults,
    qdrantResults,
    neo4jWeight,
    qdrantWeight
  );

  return combinedResults.slice(0, limit);
}

function mergeAndRankResults(
  neo4jResults: any[],
  qdrantResults: any[],
  neo4jWeight: number,
  qdrantWeight: number
) {
  const resultsMap = new Map();

  // Add Neo4j results
  neo4jResults.forEach(result => {
    const id = result.node.properties.id;
    resultsMap.set(id, {
      id,
      source: 'neo4j',
      data: result.node.properties,
      neo4jScore: result.score,
      qdrantScore: 0,
      combinedScore: result.score * neo4jWeight,
    });
  });

  // Add Qdrant results
  qdrantResults.forEach(result => {
    const id = result.id;
    if (resultsMap.has(id)) {
      // Merge with existing Neo4j result
      const existing = resultsMap.get(id);
      existing.qdrantScore = result.score;
      existing.combinedScore += result.score * qdrantWeight;
      existing.source = 'both';
    } else {
      // New result from Qdrant only
      resultsMap.set(id, {
        id,
        source: 'qdrant',
        data: result.payload,
        neo4jScore: 0,
        qdrantScore: result.score,
        combinedScore: result.score * qdrantWeight,
      });
    }
  });

  // Sort by combined score
  return Array.from(resultsMap.values())
    .sort((a, b) => b.combinedScore - a.combinedScore);
}
```

### 7.2 Hybrid Search API

```typescript
// app/api/search/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { hybridSearch } from '@/lib/hybrid-search';

export async function POST(request: NextRequest) {
  try {
    const { query, neo4jWeight, qdrantWeight, limit } = await request.json();

    if (!query) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      );
    }

    const results = await hybridSearch(query, {
      neo4jWeight,
      qdrantWeight,
      limit,
    });

    return NextResponse.json({
      success: true,
      results,
      count: results.length,
      weights: {
        neo4j: neo4jWeight || 0.5,
        qdrant: qdrantWeight || 0.5,
      },
    });
  } catch (error: any) {
    console.error('Hybrid search error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

---

## 8. API Route Patterns

### 8.1 Standard REST Patterns

```typescript
// GET /api/resource - List all resources
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') || '1');
  const limit = parseInt(searchParams.get('limit') || '20');

  // Fetch data
  const data = await fetchData({ page, limit });

  return NextResponse.json({
    success: true,
    data,
    pagination: {
      page,
      limit,
      total: data.length,
    },
  });
}

// POST /api/resource - Create resource
export async function POST(request: NextRequest) {
  const body = await request.json();

  // Validate input
  if (!body.requiredField) {
    return NextResponse.json(
      { error: 'Required field missing' },
      { status: 400 }
    );
  }

  // Create resource
  const created = await createResource(body);

  return NextResponse.json(
    { success: true, data: created },
    { status: 201 }
  );
}

// GET /api/resource/[id] - Get single resource
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const resource = await getResourceById(params.id);

  if (!resource) {
    return NextResponse.json(
      { error: 'Resource not found' },
      { status: 404 }
    );
  }

  return NextResponse.json({
    success: true,
    data: resource,
  });
}

// PUT /api/resource/[id] - Update resource
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json();

  const updated = await updateResource(params.id, body);

  return NextResponse.json({
    success: true,
    data: updated,
  });
}

// DELETE /api/resource/[id] - Delete resource
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await deleteResource(params.id);

  return NextResponse.json(
    { success: true, message: 'Resource deleted' },
    { status: 200 }
  );
}
```

### 8.2 Health Check Endpoint

```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server';
import { getNeo4jDriver } from '@/lib/neo4j-enhanced';
import { getQdrantClient } from '@/lib/qdrant-client';
import { prisma } from '@/lib/prisma';
import { getMinioClient } from '@/lib/minio-client';

export async function GET() {
  const health = {
    timestamp: new Date().toISOString(),
    neo4j: { connected: false, error: null as string | null },
    qdrant: { connected: false, error: null as string | null },
    mysql: { connected: false, error: null as string | null },
    minio: { connected: false, error: null as string | null },
    openspg: { connected: false, error: null as string | null },
  };

  // Check Neo4j
  try {
    const driver = getNeo4jDriver();
    await driver.verifyConnectivity();
    health.neo4j.connected = true;
  } catch (error: any) {
    health.neo4j.error = error.message;
  }

  // Check Qdrant
  try {
    const client = getQdrantClient();
    await client.getCollections();
    health.qdrant.connected = true;
  } catch (error: any) {
    health.qdrant.error = error.message;
  }

  // Check MySQL
  try {
    await prisma.$queryRaw`SELECT 1`;
    health.mysql.connected = true;
  } catch (error: any) {
    health.mysql.error = error.message;
  }

  // Check MinIO
  try {
    const client = getMinioClient();
    await client.listBuckets();
    health.minio.connected = true;
  } catch (error: any) {
    health.minio.error = error.message;
  }

  // Check OpenSPG
  try {
    const response = await fetch(`${process.env.OPENSPG_SERVER_URL}/health`);
    health.openspg.connected = response.ok;
  } catch (error: any) {
    health.openspg.error = error.message;
  }

  const allHealthy = Object.values(health)
    .filter(v => typeof v === 'object' && 'connected' in v)
    .every(v => v.connected);

  return NextResponse.json(health, {
    status: allHealthy ? 200 : 503,
  });
}
```

---

## 9. Error Handling

### 9.1 Standardized Error Responses

```typescript
// lib/errors.ts

export class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export function handleApiError(error: any) {
  if (error instanceof ApiError) {
    return {
      error: error.message,
      code: error.code,
      statusCode: error.statusCode,
    };
  }

  console.error('Unexpected error:', error);

  return {
    error: 'Internal server error',
    code: 'INTERNAL_ERROR',
    statusCode: 500,
  };
}
```

### 9.2 Error Handling Middleware

```typescript
// lib/api-utils.ts

export function withErrorHandling(
  handler: (request: NextRequest, context?: any) => Promise<NextResponse>
) {
  return async (request: NextRequest, context?: any) => {
    try {
      return await handler(request, context);
    } catch (error: any) {
      const errorResponse = handleApiError(error);

      return NextResponse.json(
        {
          success: false,
          error: errorResponse.error,
          code: errorResponse.code,
        },
        { status: errorResponse.statusCode }
      );
    }
  };
}
```

### 9.3 Retry Logic

```typescript
// lib/retry.ts

export async function retryOperation<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  delayMs: number = 1000
): Promise<T> {
  let lastError: Error | null = null;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (error: any) {
      lastError = error;
      console.warn(`Retry ${i + 1}/${maxRetries} failed:`, error.message);

      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, delayMs * (i + 1)));
      }
    }
  }

  throw lastError;
}
```

---

## 10. Security Best Practices

### 10.1 Input Validation

```typescript
// lib/validation.ts
import { z } from 'zod';

// Example schema for search request
export const searchRequestSchema = z.object({
  query: z.string().min(1).max(500),
  limit: z.number().int().min(1).max(100).optional(),
  filters: z.object({
    severity: z.array(z.enum(['critical', 'high', 'medium', 'low'])).optional(),
    dateRange: z.object({
      start: z.string().datetime(),
      end: z.string().datetime(),
    }).optional(),
  }).optional(),
});

export function validateRequest<T>(schema: z.ZodSchema<T>, data: any): T {
  try {
    return schema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new ApiError(400, 'Invalid request data', 'VALIDATION_ERROR');
    }
    throw error;
  }
}
```

### 10.2 SQL Injection Prevention

```typescript
// ✅ SAFE: Using Prisma (parameterized queries)
const customers = await prisma.customer.findMany({
  where: {
    name: {
      contains: userInput, // Prisma handles escaping
    },
  },
});

// ❌ UNSAFE: Raw SQL with string concatenation
// DO NOT DO THIS!
const customers = await prisma.$queryRawUnsafe(
  `SELECT * FROM customers WHERE name = '${userInput}'`
);
```

### 10.3 Cypher Injection Prevention

```typescript
// ✅ SAFE: Using parameterized queries
const results = await runCypherQuery(
  'MATCH (n {id: $id}) RETURN n',
  { id: userInput }
);

// ❌ UNSAFE: String concatenation
// DO NOT DO THIS!
const results = await runCypherQuery(
  `MATCH (n {id: '${userInput}'}) RETURN n`
);
```

### 10.4 Rate Limiting

```typescript
// lib/rate-limit.ts
import { LRUCache } from 'lru-cache';

const rateLimitCache = new LRUCache<string, number>({
  max: 500,
  ttl: 60000, // 1 minute
});

export function rateLimit(identifier: string, maxRequests: number = 10): boolean {
  const count = rateLimitCache.get(identifier) || 0;

  if (count >= maxRequests) {
    return false; // Rate limit exceeded
  }

  rateLimitCache.set(identifier, count + 1);
  return true;
}

// Usage in API route
export async function POST(request: NextRequest) {
  const ip = request.headers.get('x-forwarded-for') || 'unknown';

  if (!rateLimit(ip, 10)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    );
  }

  // Handle request...
}
```

---

## 11. Testing & Debugging

### 11.1 Connection Testing

```bash
# Test Neo4j connection
curl -X POST http://localhost:3000/api/graph/query \
  -H "Content-Type: application/json" \
  -d '{"query": "MATCH (n) RETURN count(n) as nodeCount"}'

# Test Qdrant connection
curl http://localhost:6333/collections

# Test MySQL connection
curl http://localhost:3000/api/customers

# Test MinIO connection
curl http://localhost:9000/minio/health/live

# Test OpenSPG connection
curl http://localhost:8887/health

# Test all backends
curl http://localhost:3000/api/health
```

### 11.2 Debugging Tips

```typescript
// Enable detailed logging
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});

// Neo4j query logging
const result = await session.run(cypher, params);
console.log('Cypher executed:', cypher);
console.log('Parameters:', params);
console.log('Result count:', result.records.length);

// Qdrant search logging
console.log('Vector search query:', query);
console.log('Query vector:', queryVector.slice(0, 5), '...');
console.log('Results:', results.length);
```

### 11.3 Performance Monitoring

```typescript
// lib/monitoring.ts

export async function monitoredQuery<T>(
  operation: string,
  fn: () => Promise<T>
): Promise<T> {
  const startTime = Date.now();

  try {
    const result = await fn();
    const duration = Date.now() - startTime;

    console.log(`✅ ${operation} completed in ${duration}ms`);

    return result;
  } catch (error) {
    const duration = Date.now() - startTime;

    console.error(`❌ ${operation} failed after ${duration}ms:`, error);

    throw error;
  }
}

// Usage
const results = await monitoredQuery(
  'Neo4j CVE search',
  () => runCypherQuery('MATCH (cve:CVE) RETURN cve LIMIT 10')
);
```

---

## Appendix A: Environment Variables Reference

### Complete `.env.local` Template

```bash
# ========================================
# AEON Digital Twin Backend Configuration
# ========================================

# OpenAI API (AI Chat)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Neo4j Graph Database
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg
NEO4J_DATABASE=neo4j

# Qdrant Vector Database
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

# MySQL Database (via Prisma)
DATABASE_URL="mysql://root:openspg@openspg-mysql:3306/openspg"

# MinIO Object Storage
MINIO_ENDPOINT=openspg-minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false

# OpenSPG Knowledge Graph Pipeline
OPENSPG_SERVER_URL=http://openspg-server:8887

# Next.js Configuration
NEXT_PUBLIC_APP_NAME=AEON Digital Twin
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=change-me-in-production
```

---

## Appendix B: API Endpoint Reference

### Complete API Endpoint List

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | System health check for all backends |
| `/api/graph/query` | POST | Execute Cypher query on Neo4j |
| `/api/graph/data` | GET | Get graph visualization data |
| `/api/search` | POST | Hybrid search (Neo4j + Qdrant) |
| `/api/search/vector` | POST | Qdrant semantic search only |
| `/api/chat` | POST | AI chat with streaming (Vercel AI SDK) |
| `/api/customers` | GET, POST | List/create customers (MySQL) |
| `/api/customers/[id]` | GET, PUT, DELETE | Get/update/delete customer |
| `/api/tags` | GET, POST | List/create tags (MySQL) |
| `/api/tags/[id]` | DELETE | Delete tag |
| `/api/tags/assign` | POST | Assign tag to entity |
| `/api/upload` | POST | Upload file to MinIO |
| `/api/upload/[filename]` | GET | Get presigned download URL |
| `/api/pipeline/process` | POST | Start document processing (OpenSPG) |
| `/api/pipeline/status/[jobId]` | GET | Check processing status |
| `/api/analytics/metrics` | GET | Aggregated metrics |
| `/api/analytics/timeseries` | GET | Time-series data |
| `/api/analytics/export` | GET | Export analytics data |
| `/api/activity/recent` | GET | Recent activity feed |
| `/api/observability/performance` | GET | Performance metrics |
| `/api/observability/system` | GET | System metrics |

---

**Document Status:** COMPLETE
**Last Updated:** 2025-01-04
**Version:** 2.0.0
**Target Directory:** `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Front End UI Builder`
