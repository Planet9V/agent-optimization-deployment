# Next.js AEON UI Deployment Guide
**File**: NEXT_JS_DEPLOYMENT_GUIDE.md
**Created**: 2025-11-03 15:50:00 UTC
**Version**: v1.0.0
**Author**: System Architecture Designer
**Purpose**: Step-by-step guide for deploying AEON UI Next.js container
**Status**: ACTIVE

---

## Prerequisites

### System Requirements
- Docker Engine 20.10+
- Docker Compose 2.0+
- Running OpenSPG infrastructure on `openspg-network`
- 4GB available RAM
- 10GB available disk space

### Verify Existing Infrastructure
```bash
# Check running containers
docker ps --filter "name=openspg"

# Verify network exists
docker network inspect openspg-network

# Check shared volume
docker volume inspect openspg-shared-data

# Expected output:
# ✅ openspg-neo4j (healthy)
# ✅ openspg-mysql (healthy)
# ✅ openspg-minio (healthy)
# ⚠️ openspg-qdrant (may be unhealthy)
# ⚠️ openspg-server (may be unhealthy)
```

---

## Step 1: Prepare Next.js Project

### 1.1 Initialize Next.js Application
```bash
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface

# Option A: Create new Next.js app
npx create-next-app@latest . --typescript --tailwind --app

# Option B: Use existing project (skip if already exists)
```

### 1.2 Install Dependencies
```bash
# Core Next.js dependencies
npm install next@latest react@latest react-dom@latest

# Database clients
npm install neo4j-driver mysql2 @qdrant/js-client-rest minio

# UI components
npm install @radix-ui/react-dialog @radix-ui/react-tabs @radix-ui/react-select
npm install lucide-react clsx tailwind-merge

# Authentication
npm install next-auth

# Development dependencies
npm install --save-dev @types/node @types/react typescript
```

### 1.3 Configure Next.js
Create or update `next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker
  output: 'standalone',

  // Environment variables available to browser
  env: {
    NEO4J_URI: process.env.NEO4J_URI,
    QDRANT_URL: process.env.QDRANT_URL,
  },

  // CORS headers for API routes
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: process.env.NEXTAUTH_URL || '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ];
  },

  // Rewrites for backend proxy (if needed)
  async rewrites() {
    return [
      {
        source: '/api/openspg/:path*',
        destination: `${process.env.OPENSPG_SERVER_URL}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
```

---

## Step 2: Create Database Connection Modules

### 2.1 Neo4j Connection (`src/lib/neo4j.ts`)
```typescript
import neo4j, { Driver, Session } from 'neo4j-driver';

let driver: Driver | null = null;

export function getNeo4jDriver(): Driver {
  if (!driver) {
    const uri = process.env.NEO4J_URI || 'bolt://localhost:7687';
    const user = process.env.NEO4J_USER || 'neo4j';
    const password = process.env.NEO4J_PASSWORD || 'password';

    driver = neo4j.driver(uri, neo4j.auth.basic(user, password), {
      maxConnectionPoolSize: 50,
      connectionAcquisitionTimeout: 60000,
    });
  }
  return driver;
}

export function getSession(): Session {
  const database = process.env.NEO4J_DATABASE || 'neo4j';
  return getNeo4jDriver().session({ database });
}

export async function closeNeo4jDriver(): Promise<void> {
  if (driver) {
    await driver.close();
    driver = null;
  }
}
```

### 2.2 Qdrant Connection (`src/lib/qdrant.ts`)
```typescript
import { QdrantClient } from '@qdrant/js-client-rest';

let client: QdrantClient | null = null;

export function getQdrantClient(): QdrantClient {
  if (!client) {
    const url = process.env.QDRANT_URL || 'http://localhost:6333';
    const apiKey = process.env.QDRANT_API_KEY;

    client = new QdrantClient({
      url,
      apiKey,
    });
  }
  return client;
}
```

### 2.3 MySQL Connection (`src/lib/mysql.ts`)
```typescript
import mysql from 'mysql2/promise';

let pool: mysql.Pool | null = null;

export function getMySQLPool(): mysql.Pool {
  if (!pool) {
    pool = mysql.createPool({
      host: process.env.MYSQL_HOST || 'localhost',
      port: parseInt(process.env.MYSQL_PORT || '3306'),
      user: process.env.MYSQL_USER || 'root',
      password: process.env.MYSQL_PASSWORD || 'password',
      database: process.env.MYSQL_DATABASE || 'openspg',
      waitForConnections: true,
      connectionLimit: 10,
      queueLimit: 0,
    });
  }
  return pool;
}

export async function closeMySQLPool(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
  }
}
```

---

## Step 3: Create Health Check API

### 3.1 Health Check Endpoint (`src/app/api/health/route.ts`)
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { getNeo4jDriver } from '@/lib/neo4j';
import { getQdrantClient } from '@/lib/qdrant';
import { getMySQLPool } from '@/lib/mysql';

async function checkNeo4j() {
  try {
    const driver = getNeo4jDriver();
    await driver.verifyConnectivity();
    return { status: 'healthy', message: 'Connected' };
  } catch (error) {
    return { status: 'unhealthy', message: error.message };
  }
}

async function checkQdrant() {
  try {
    const client = getQdrantClient();
    await client.getCollections();
    return { status: 'healthy', message: 'Connected' };
  } catch (error) {
    return { status: 'unhealthy', message: error.message };
  }
}

async function checkMySQL() {
  try {
    const pool = getMySQLPool();
    await pool.query('SELECT 1');
    return { status: 'healthy', message: 'Connected' };
  } catch (error) {
    return { status: 'unhealthy', message: error.message };
  }
}

export async function GET(request: NextRequest) {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    services: {
      neo4j: await checkNeo4j(),
      qdrant: await checkQdrant(),
      mysql: await checkMySQL(),
    },
  };

  const allHealthy = Object.values(health.services).every(
    (s) => s.status === 'healthy'
  );

  health.status = allHealthy ? 'healthy' : 'degraded';

  return NextResponse.json(health, { status: allHealthy ? 200 : 503 });
}
```

---

## Step 4: Environment Setup

### 4.1 Create Environment File
```bash
# Copy example to .env.local
cp .env.example .env.local

# Edit with your values
nano .env.local

# For Docker deployment, use container names:
# NEO4J_URI=bolt://openspg-neo4j:7687
# QDRANT_URL=http://openspg-qdrant:6333
# etc.
```

### 4.2 Generate Secrets
```bash
# Generate NextAuth secret
openssl rand -base64 32

# Add to .env.local:
# NEXTAUTH_SECRET=<generated-secret>
```

### 4.3 Validate Environment
Create `src/lib/env-validation.ts`:

```typescript
const requiredEnvVars = [
  'NEO4J_URI',
  'NEO4J_USER',
  'NEO4J_PASSWORD',
  'QDRANT_URL',
  'MYSQL_HOST',
  'MYSQL_DATABASE',
  'NEXTAUTH_SECRET',
];

export function validateEnvironment() {
  const missing = requiredEnvVars.filter((varName) => !process.env[varName]);

  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(', ')}`
    );
  }
}

// Run validation at startup
if (process.env.NODE_ENV === 'production') {
  validateEnvironment();
}
```

---

## Step 5: Build and Test Locally

### 5.1 Development Mode
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open browser
# http://localhost:3000
# http://localhost:3000/api/health
```

### 5.2 Production Build Test
```bash
# Build for production
npm run build

# Start production server
npm run start

# Test health endpoint
curl http://localhost:3000/api/health
```

---

## Step 6: Docker Deployment

### 6.1 Build Docker Image
```bash
# Build image
docker build -t aeon-ui:latest .

# Verify image
docker images | grep aeon-ui

# Expected output:
# aeon-ui    latest    <image-id>    <size>
```

### 6.2 Deploy with Docker Compose
```bash
# Deploy container
docker-compose -f docker-compose.aeon-ui.yml up -d

# Check status
docker ps | grep aeon-ui

# View logs
docker logs -f aeon-ui

# Expected output:
# ✅ Container started
# ✅ Listening on port 3000
# ✅ Health checks passing
```

### 6.3 Verify Deployment
```bash
# Check health endpoint
curl http://localhost:3000/api/health

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2025-11-03T15:50:00.000Z",
#   "services": {
#     "neo4j": { "status": "healthy", "message": "Connected" },
#     "qdrant": { "status": "healthy", "message": "Connected" },
#     "mysql": { "status": "healthy", "message": "Connected" }
#   }
# }

# Check container health
docker inspect aeon-ui --format='{{.State.Health.Status}}'
# Expected: healthy

# Verify network connectivity
docker exec aeon-ui ping -c 3 openspg-neo4j
docker exec aeon-ui ping -c 3 openspg-qdrant
docker exec aeon-ui ping -c 3 openspg-mysql
```

---

## Step 7: Troubleshooting

### 7.1 Container Won't Start
```bash
# Check logs
docker logs aeon-ui

# Common issues:
# - Missing environment variables
# - Port 3000 already in use
# - Network not found

# Solution: Verify environment and network
docker network ls | grep openspg
docker port aeon-ui
```

### 7.2 Cannot Connect to Neo4j
```bash
# Test from container
docker exec -it aeon-ui sh
apk add curl
curl -v http://openspg-neo4j:7474

# Check Neo4j credentials
docker exec aeon-ui env | grep NEO4J

# Verify Neo4j is running
docker ps | grep neo4j
docker logs openspg-neo4j
```

### 7.3 Health Check Failing
```bash
# Check health endpoint manually
docker exec aeon-ui wget -O- http://localhost:3000/api/health

# Check service connectivity
docker exec aeon-ui ping openspg-neo4j
docker exec aeon-ui ping openspg-qdrant

# Restart container
docker restart aeon-ui
```

### 7.4 Qdrant Unhealthy
```bash
# Check Qdrant status
docker ps | grep qdrant
docker logs openspg-qdrant

# Test API key
curl -H "api-key: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=" \
  http://localhost:6333/collections

# Restart Qdrant if needed
docker restart openspg-qdrant
```

---

## Step 8: Post-Deployment Verification

### 8.1 Service Connectivity Matrix
```bash
# Create test script
cat > test-connectivity.sh << 'EOF'
#!/bin/bash
echo "Testing AEON UI connectivity..."

# Neo4j
echo "Neo4j HTTP:" $(curl -s -o /dev/null -w "%{http_code}" http://localhost:7474)
echo "Neo4j Bolt: " $(docker exec aeon-ui nc -zv openspg-neo4j 7687 2>&1 | grep succeeded)

# Qdrant
echo "Qdrant API:" $(curl -s -o /dev/null -w "%{http_code}" http://localhost:6333)

# MySQL
echo "MySQL:" $(docker exec aeon-ui nc -zv openspg-mysql 3306 2>&1 | grep succeeded)

# MinIO
echo "MinIO API:" $(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/minio/health/live)

# AEON UI
echo "AEON UI:" $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health)
EOF

chmod +x test-connectivity.sh
./test-connectivity.sh
```

### 8.2 Performance Check
```bash
# Monitor resource usage
docker stats aeon-ui --no-stream

# Expected output:
# CONTAINER    CPU %    MEM USAGE / LIMIT    MEM %    NET I/O
# aeon-ui      <5%      <1GB / 2GB          <50%     ...
```

### 8.3 Log Verification
```bash
# Check logs for errors
docker logs aeon-ui | grep -i error
docker logs aeon-ui | grep -i warning

# Tail logs
docker logs -f aeon-ui
```

---

## Step 9: Security Hardening

### 9.1 Rotate Credentials
```bash
# Generate new secrets
NEW_NEXTAUTH_SECRET=$(openssl rand -base64 32)
NEW_NEO4J_PASSWORD=$(openssl rand -base64 24)

# Update Neo4j password
docker exec -it openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg \
  "ALTER USER neo4j SET PASSWORD '$NEW_NEO4J_PASSWORD'"

# Update .env.local with new credentials
# Rebuild and redeploy container
```

### 9.2 Network Isolation
```bash
# Verify only necessary ports exposed
docker port aeon-ui

# Expected: Only port 3000
# 3000/tcp -> 0.0.0.0:3000

# Verify internal network
docker network inspect openspg-network | grep aeon-ui
```

### 9.3 File Permissions
```bash
# Ensure .env files are not world-readable
chmod 600 .env.local
chmod 600 .env.production

# Add to .gitignore
echo ".env.local" >> .gitignore
echo ".env.production" >> .gitignore
```

---

## Step 10: Backup and Recovery

### 10.1 Backup Configuration
```bash
# Backup environment variables
cp .env.local .env.backup

# Export Docker volumes
docker run --rm -v aeon-ui-logs:/data -v $(pwd):/backup \
  alpine tar czf /backup/aeon-ui-logs-backup.tar.gz -C /data .

# Backup database connection scripts
tar czf aeon-ui-config-backup.tar.gz src/lib/*.ts
```

### 10.2 Recovery Procedure
```bash
# Stop container
docker-compose -f docker-compose.aeon-ui.yml down

# Restore volumes
docker run --rm -v aeon-ui-logs:/data -v $(pwd):/backup \
  alpine tar xzf /backup/aeon-ui-logs-backup.tar.gz -C /data

# Restore configuration
tar xzf aeon-ui-config-backup.tar.gz

# Restart container
docker-compose -f docker-compose.aeon-ui.yml up -d
```

---

## Step 11: Monitoring and Maintenance

### 11.1 Setup Health Monitoring
```bash
# Create monitoring script
cat > monitor-aeon-ui.sh << 'EOF'
#!/bin/bash
while true; do
  STATUS=$(curl -s http://localhost:3000/api/health | jq -r '.status')
  if [ "$STATUS" != "healthy" ]; then
    echo "[$(date)] ALERT: AEON UI unhealthy - Status: $STATUS"
    docker logs aeon-ui --tail 50
  fi
  sleep 60
done
EOF

chmod +x monitor-aeon-ui.sh
```

### 11.2 Log Rotation
```bash
# Configure Docker log rotation
# Add to docker-compose.aeon-ui.yml:
services:
  aeon-ui:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Deployment Checklist

- [ ] ✅ OpenSPG infrastructure running
- [ ] ✅ Next.js project initialized
- [ ] ✅ Dependencies installed
- [ ] ✅ Database connection modules created
- [ ] ✅ Health check endpoint implemented
- [ ] ✅ Environment variables configured
- [ ] ✅ Docker image built successfully
- [ ] ✅ Container deployed to openspg-network
- [ ] ✅ Health checks passing
- [ ] ✅ Service connectivity verified
- [ ] ✅ Security credentials rotated
- [ ] ✅ Backup procedure tested
- [ ] ✅ Monitoring enabled

---

## Next Steps

1. **Implement UI Components**: Build graph visualization and search interfaces
2. **Add Authentication**: Configure NextAuth.js with role-based access
3. **Setup Monitoring**: Integrate Prometheus/Grafana for metrics
4. **Configure Backups**: Automated backup for application state
5. **Load Testing**: Verify performance under realistic load
6. **Documentation**: API documentation and user guides

---

**Deployment Status**: Ready for production
**Last Updated**: 2025-11-03
**Next Review**: 2025-12-03
