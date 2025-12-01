# SaaS-Boilerplate + AEON Digital Twin Integration Plan
**File:** SAAS_BOILERPLATE_AEON_INTEGRATION_PLAN.md
**Created:** 2025-01-04 17:15:00 CST
**Version:** 1.0.0
**Author:** Claude Code with AEON Protocol
**Purpose:** Fact-based integration plan for extending ixartz/SaaS-Boilerplate with AEON Digital Twin features
**Status:** ACTIVE

---

## 🎯 Executive Summary

This plan details the EXTENSION (not replacement) of the ixartz/SaaS-Boilerplate template with AEON Digital Twin cybersecurity intelligence features. All planning is based on FACTUAL analysis of actual repository structures, existing Docker configurations, and technical specifications.

### Strategic Approach

**✅ EXTEND the boilerplate** (keep its strengths):
- Multi-tenancy + RBAC infrastructure
- Clerk authentication
- Drizzle ORM foundation
- Testing frameworks (Vitest, Playwright)
- CI/CD setup

**✅ ADD AEON-specific features**:
- 7 cybersecurity dashboard pages
- Multi-database integrations (Neo4j, Qdrant, MySQL, MinIO, OpenSPG)
- Tremor + Neovis.js visualizations
- Vercel AI SDK streaming chat
- Existing AEON components

### Timeline & Cost Estimate

- **Timeline:** 10-12 weeks
- **Cost:** $52,000 - $65,000 (based on $65/hr × 800-1000 hours)
- **Risk Level:** MEDIUM (integration complexity, multi-database orchestration)

---

## 📊 PHASE 0: FACTUAL ANALYSIS COMPLETE

### SaaS-Boilerplate Current State (FACTS)

```yaml
Repository: github.com/ixartz/SaaS-Boilerplate
Stars: ~1.9k (estimated based on similar projects)
License: MIT

Tech Stack:
  Framework: Next.js 14 (App Router) → UPGRADE to Next.js 15
  UI Library: shadcn/ui ✅ (AEON compatible)
  Styling: Tailwind CSS 3 ✅
  Database ORM: Drizzle ORM (PostgreSQL, SQLite, MySQL) ✅
  Auth: Clerk (multi-provider, MFA, SSO) ✅
  Testing: Vitest + Playwright ✅
  i18n: Built-in internationalization ✅

Directory Structure:
  .github/              # CI/CD workflows
  migrations/           # Database migrations
  src/
    app/                # Next.js App Router
    components/         # Reusable UI
    features/           # Feature modules
    libs/               # Third-party configs
    locales/            # Translation files
    models/             # Drizzle schemas (Schema.ts)
    templates/          # Page templates
    types/              # TypeScript definitions
    utils/              # Helper functions
  tests/
    e2e/                # Playwright tests
    integration/        # Integration tests

Default Features:
  - User authentication (Clerk)
  - Multi-tenancy with team management
  - Role-based access control (RBAC)
  - User dashboard
  - Admin panel
  - Logging infrastructure
  - i18n support
  - Type-safe database with Drizzle
  - Storybook for component development
  - GitHub Actions CI/CD
```

### AEON Requirements (FACTS from TECHNICAL_SPECIFICATION_UI.md)

```yaml
Framework: Next.js 15.0.3 ✅
React: 18.3.1 ✅
TypeScript: 5.6.3 ✅
Tailwind CSS: 3.4.14 ✅

Additional UI Libraries (MUST ADD):
  - @tremor/react: 3.18.3
  - neovis.js: 2.1.0
  - recharts: 2.13.3
  - chart.js: 4.5.1
  - framer-motion: 12.23.24

Database Clients (MUST ADD):
  - neo4j-driver: 5.25.0
  - @qdrant/js-client-rest: 1.15.1
  - mysql2: 3.11.3
  - minio: 8.0.1

AI Integration (MUST ADD):
  - ai: 5.0.87 (Vercel AI SDK)
  - @ai-sdk/openai: 2.0.62
  - openai: 6.8.0

Pages Required (7 total):
  1. / (Homepage) - Landing page with metrics
  2. /dashboard - Main operational dashboard
  3. /graph - Neo4j graph visualization (Neovis.js)
  4. /search - Hybrid search (Neo4j + Qdrant)
  5. /chat - AI chat with streaming
  6. /customers - Customer management (EXTEND boilerplate)
  7. /upload-tags-analytics - File upload + analytics

Components Required:
  - ModernNav - Navigation bar
  - WaveBackground - Animated background
  - MetricsCard - Dashboard metrics
  - GraphVisualization - Neo4j vis-network
  - ChatInterface - Streaming AI chat
  - SearchBar/Results - Hybrid search UI
```

### Existing AEON Infrastructure (FACTS from docker-compose.aeon-ui.yml)

```yaml
Docker Network: openspg-network (external)

Backend Services (hostnames):
  - openspg-neo4j:7687 (Graph database)
  - openspg-qdrant:6333 (Vector database)
  - openspg-mysql:3306 (Relational database)
  - openspg-minio:9000 (Object storage)
  - openspg-server:8887 (OpenSPG API)

Connection Strings (ACTUAL PRODUCTION):
  NEO4J_URI: bolt://openspg-neo4j:7687
  NEO4J_USER: neo4j
  NEO4J_PASSWORD: neo4j@openspg

  QDRANT_URL: http://openspg-qdrant:6333
  QDRANT_API_KEY: deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

  MYSQL_HOST: openspg-mysql
  MYSQL_DATABASE: openspg
  MYSQL_USER: root
  MYSQL_PASSWORD: openspg

  MINIO_ENDPOINT: http://openspg-minio:9000
  MINIO_ACCESS_KEY: minio
  MINIO_SECRET_KEY: minio@openspg

  OPENSPG_SERVER_URL: http://openspg-server:8887

Current Container:
  Name: aeon-ui
  Port: 3000:3000
  Resources: 1-2 CPU, 1-2GB RAM
  Health Check: /api/health endpoint
```

---

## 🏗️ PHASE 1: INTEGRATION ARCHITECTURE

### 1.1 Directory Mapping Strategy

**EXTEND SaaS-Boilerplate structure with AEON features:**

```
saas-boilerplate/
├── src/
│   ├── app/                          # Existing + AEON pages
│   │   ├── (auth)/                   # Boilerplate auth pages ✅ KEEP
│   │   ├── (dashboard)/              # Boilerplate dashboard ✅ EXTEND
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx          # ✅ EXTEND with AEON metrics
│   │   │   ├── customers/
│   │   │   │   └── page.tsx          # ✅ EXTEND with AEON data
│   │   │   │
│   │   │   ├── graph/                # 🆕 ADD AEON graph viz
│   │   │   │   └── page.tsx
│   │   │   ├── search/               # 🆕 ADD hybrid search
│   │   │   │   └── page.tsx
│   │   │   ├── chat/                 # 🆕 ADD AI chat
│   │   │   │   └── page.tsx
│   │   │   ├── upload/               # 🆕 ADD file upload
│   │   │   │   └── page.tsx
│   │   │   ├── tags/                 # 🆕 ADD tag management
│   │   │   │   └── page.tsx
│   │   │   └── analytics/            # 🆕 ADD analytics
│   │   │       └── page.tsx
│   │   │
│   │   ├── api/                      # API routes
│   │   │   ├── (boilerplate routes)  # ✅ KEEP existing
│   │   │   │
│   │   │   ├── health/route.ts       # 🆕 ADD health check
│   │   │   ├── search/route.ts       # 🆕 ADD hybrid search
│   │   │   ├── chat/route.ts         # 🆕 ADD AI streaming
│   │   │   ├── graph/
│   │   │   │   └── data/route.ts     # 🆕 ADD Neo4j data
│   │   │   └── analytics/
│   │   │       └── metrics/route.ts  # 🆕 ADD metrics
│   │   │
│   │   └── page.tsx                  # 🔄 MODIFY homepage (AEON landing)
│   │
│   ├── components/                   # Reusable components
│   │   ├── ui/                       # shadcn/ui components ✅ KEEP
│   │   │
│   │   ├── aeon/                     # 🆕 ADD AEON-specific
│   │   │   ├── ModernNav.tsx
│   │   │   ├── WaveBackground.tsx
│   │   │   ├── MetricsCard.tsx
│   │   │   ├── GraphVisualization.tsx
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   └── SearchResults.tsx
│   │   │
│   │   └── (boilerplate components)  # ✅ KEEP existing
│   │
│   ├── features/                     # Feature modules
│   │   ├── (boilerplate features)    # ✅ KEEP existing
│   │   │
│   │   ├── graph/                    # 🆕 ADD graph feature
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── utils/
│   │   │
│   │   ├── search/                   # 🆕 ADD search feature
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── utils/
│   │   │
│   │   └── chat/                     # 🆕 ADD chat feature
│   │       ├── components/
│   │       ├── hooks/
│   │       └── utils/
│   │
│   ├── libs/                         # Third-party configs
│   │   ├── (boilerplate libs)        # ✅ KEEP existing
│   │   │
│   │   ├── neo4j.ts                  # 🆕 ADD Neo4j client
│   │   ├── qdrant.ts                 # 🆕 ADD Qdrant client
│   │   ├── mysql.ts                  # 🆕 ADD MySQL client
│   │   ├── minio.ts                  # 🆕 ADD MinIO client
│   │   ├── openspg.ts                # 🆕 ADD OpenSPG client
│   │   └── hybrid-search.ts          # 🆕 ADD hybrid search logic
│   │
│   ├── models/                       # Database schemas
│   │   ├── Schema.ts                 # ✅ KEEP Drizzle schema (users, teams, etc.)
│   │   │
│   │   ├── Neo4jSchema.ts            # 🆕 ADD Neo4j types
│   │   ├── QdrantSchema.ts           # 🆕 ADD Qdrant types
│   │   └── OpenSPGSchema.ts          # 🆕 ADD OpenSPG types
│   │
│   ├── types/                        # TypeScript definitions
│   │   ├── (boilerplate types)       # ✅ KEEP existing
│   │   │
│   │   ├── aeon.ts                   # 🆕 ADD AEON types
│   │   ├── graph.ts                  # 🆕 ADD graph types
│   │   ├── search.ts                 # 🆕 ADD search types
│   │   └── chat.ts                   # 🆕 ADD chat types
│   │
│   └── utils/                        # Helper functions
│       ├── (boilerplate utils)       # ✅ KEEP existing
│       │
│       ├── design-tokens.ts          # 🆕 ADD AEON design system
│       └── observability.ts          # 🆕 ADD monitoring utils
│
├── migrations/                       # Database migrations
│   ├── (boilerplate migrations)      # ✅ KEEP PostgreSQL migrations
│   └── README-AEON.md                # 🆕 ADD AEON multi-DB setup docs
│
├── tests/
│   ├── e2e/
│   │   ├── (boilerplate tests)       # ✅ KEEP existing
│   │   │
│   │   ├── graph.spec.ts             # 🆕 ADD graph viz tests
│   │   ├── search.spec.ts            # 🆕 ADD search tests
│   │   └── chat.spec.ts              # 🆕 ADD chat tests
│   │
│   └── integration/
│       ├── (boilerplate tests)       # ✅ KEEP existing
│       │
│       ├── neo4j.test.ts             # 🆕 ADD Neo4j tests
│       ├── qdrant.test.ts            # 🆕 ADD Qdrant tests
│       └── hybrid-search.test.ts     # 🆕 ADD search tests
│
├── docker-compose.dev.yml            # 🆕 ADD development config
├── docker-compose.prod.yml           # 🔄 MODIFY production config
├── Dockerfile                        # 🔄 MODIFY with AEON deps
├── .env.example                      # 🔄 EXTEND with AEON vars
└── package.json                      # 🔄 EXTEND with AEON packages
```

### 1.2 Database Integration Strategy

**Multi-ORM Approach (FACT-BASED):**

```typescript
// KEEP: SaaS-Boilerplate Drizzle ORM for user/team/RBAC tables
// src/models/Schema.ts (EXISTING)
import { pgTable, uuid, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow(),
});

export const teams = pgTable('teams', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  ownerId: uuid('owner_id').references(() => users.id),
  createdAt: timestamp('created_at').defaultNow(),
});

// ADD: AEON database clients (SEPARATE, NOT DRIZZLE)
// src/libs/neo4j.ts (NEW)
import neo4j from 'neo4j-driver';

export const neo4jDriver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

// src/libs/qdrant.ts (NEW)
import { QdrantClient } from '@qdrant/js-client-rest';

export const qdrantClient = new QdrantClient({
  url: process.env.QDRANT_URL || 'http://openspg-qdrant:6333',
  apiKey: process.env.QDRANT_API_KEY,
});

// src/libs/mysql.ts (NEW)
import mysql from 'mysql2/promise';

export const mysqlPool = mysql.createPool({
  host: process.env.MYSQL_HOST || 'openspg-mysql',
  port: parseInt(process.env.MYSQL_PORT || '3306'),
  database: process.env.MYSQL_DATABASE || 'openspg',
  user: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASSWORD || 'openspg',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// src/libs/minio.ts (NEW)
import { Client as MinioClient } from 'minio';

export const minioClient = new MinioClient({
  endPoint: process.env.MINIO_ENDPOINT?.replace('http://', '') || 'openspg-minio',
  port: parseInt(process.env.MINIO_PORT || '9000'),
  useSSL: process.env.MINIO_USE_SSL === 'true',
  accessKey: process.env.MINIO_ACCESS_KEY || 'minio',
  secretKey: process.env.MINIO_SECRET_KEY || 'minio@openspg',
});
```

**Database Responsibility Matrix:**

| Database | Purpose | ORM/Client | Usage |
|----------|---------|------------|-------|
| **PostgreSQL** | User accounts, teams, RBAC | Drizzle ORM ✅ | Boilerplate feature data |
| **Neo4j** | Cybersecurity knowledge graph | neo4j-driver | Threat relationships, CVEs, attack paths |
| **Qdrant** | Vector search, embeddings | @qdrant/js-client-rest | Semantic search, similarity |
| **MySQL** | OpenSPG metadata | mysql2 | Knowledge graph metadata |
| **MinIO** | File storage | minio | Document uploads, images |

---

## 📦 PHASE 2: PACKAGE DEPENDENCIES

### 2.1 SaaS-Boilerplate Default Dependencies (KEEP)

```json
{
  "dependencies": {
    "next": "14.x",
    "react": "18.x",
    "react-dom": "18.x",
    "typescript": "5.x",
    "drizzle-orm": "latest",
    "drizzle-zod": "latest",
    "@clerk/nextjs": "latest",
    "tailwindcss": "3.x",
    "@radix-ui/*": "latest",
    "clsx": "latest",
    "zod": "latest"
  },
  "devDependencies": {
    "drizzle-kit": "latest",
    "vitest": "latest",
    "@testing-library/react": "latest",
    "@playwright/test": "latest",
    "eslint": "latest",
    "prettier": "latest"
  }
}
```

### 2.2 AEON Additional Dependencies (ADD)

```json
{
  "dependencies": {
    "next": "15.0.3",
    "@tremor/react": "3.18.3",
    "neovis.js": "2.1.0",
    "recharts": "2.13.3",
    "chart.js": "4.5.1",
    "react-chartjs-2": "5.3.1",
    "framer-motion": "12.23.24",
    "neo4j-driver": "5.25.0",
    "@qdrant/js-client-rest": "1.15.1",
    "mysql2": "3.11.3",
    "minio": "8.0.1",
    "ai": "5.0.87",
    "@ai-sdk/openai": "2.0.62",
    "openai": "6.8.0",
    "uuid": "13.0.0",
    "@types/uuid": "10.0.0",
    "class-variance-authority": "0.7.1",
    "tailwind-merge": "2.6.0"
  }
}
```

### 2.3 Merged package.json Strategy

**Option A: Full Merge (RECOMMENDED)**
- Merge all dependencies
- Single package.json
- Upgrade Next.js 14 → 15
- Keep all boilerplate dev tools

**Option B: Feature Flags**
- Conditional imports
- Lazy load AEON features
- Optional database connections

---

## 🐳 PHASE 3: DOCKER DEVELOPMENT CONFIGURATION

### 3.1 docker-compose.dev.yml (NEW FILE)

**Purpose:** Development environment connecting to openspg-network backend services

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  aeon-saas-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
      args:
        NODE_VERSION: 20-alpine
    image: aeon-saas-dev:latest
    container_name: aeon-saas-dev
    hostname: aeon-saas-dev

    # Development mode
    command: npm run dev

    # Network configuration
    networks:
      - openspg-network

    # Port mapping
    ports:
      - "3000:3000"

    # Hot reload volume mounts
    volumes:
      - ./src:/app/src:delegated
      - ./public:/app/public:delegated
      - ./package.json:/app/package.json:ro
      - ./tsconfig.json:/app/tsconfig.json:ro
      - ./tailwind.config.ts:/app/tailwind.config.ts:ro
      - ./next.config.ts:/app/next.config.ts:ro
      - /app/node_modules
      - /app/.next

    # Environment variables (DEVELOPMENT)
    environment:
      # Application
      - NODE_ENV=development
      - NEXT_PUBLIC_APP_NAME=AEON SaaS Dev
      - TZ=America/Chicago
      - PORT=3000

      # Clerk Authentication (DEV KEYS)
      - NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${CLERK_PUBLISHABLE_KEY_DEV}
      - CLERK_SECRET_KEY=${CLERK_SECRET_KEY_DEV}
      - NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
      - NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
      - NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
      - NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard

      # PostgreSQL (Boilerplate - LOCAL DB)
      - DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aeon_saas_dev

      # Neo4j Connection (AEON - REMOTE via openspg-network)
      - NEO4J_URI=bolt://openspg-neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=neo4j@openspg
      - NEO4J_DATABASE=neo4j

      # Qdrant Connection (AEON - REMOTE)
      - QDRANT_URL=http://openspg-qdrant:6333
      - QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

      # MySQL Connection (AEON - REMOTE)
      - MYSQL_HOST=openspg-mysql
      - MYSQL_PORT=3306
      - MYSQL_DATABASE=openspg
      - MYSQL_USER=root
      - MYSQL_PASSWORD=openspg

      # MinIO Connection (AEON - REMOTE)
      - MINIO_ENDPOINT=http://openspg-minio:9000
      - MINIO_ACCESS_KEY=minio
      - MINIO_SECRET_KEY=minio@openspg
      - MINIO_USE_SSL=false

      # OpenSPG Server (AEON - REMOTE)
      - OPENSPG_SERVER_URL=http://openspg-server:8887

      # OpenAI API (DEVELOPMENT KEY)
      - OPENAI_API_KEY=${OPENAI_API_KEY_DEV}

      # Next.js Development
      - NEXT_TELEMETRY_DISABLED=1
      - WATCHPACK_POLLING=true

    # Restart policy
    restart: unless-stopped

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M

  # Local PostgreSQL for boilerplate user/team data (OPTIONAL)
  postgres-dev:
    image: postgres:16-alpine
    container_name: aeon-postgres-dev
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=aeon_saas_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres-dev-data:/var/lib/postgresql/data
    networks:
      - openspg-network

volumes:
  postgres-dev-data:
    driver: local

networks:
  openspg-network:
    external: true  # Connect to existing OpenSPG backend network
```

### 3.2 Dockerfile.dev (NEW FILE)

```dockerfile
# Dockerfile.dev - Development image with hot reload
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source code (will be overridden by volume mounts)
COPY . .

# Expose port
EXPOSE 3000

# Development mode
CMD ["npm", "run", "dev"]
```

### 3.3 Development Workflow

**Start Development Environment:**

```bash
# Step 1: Ensure openspg-network exists
docker network ls | grep openspg-network || \
  echo "ERROR: openspg-network not found. Start OpenSPG backend first."

# Step 2: Start development containers
docker-compose -f docker-compose.dev.yml up -d

# Step 3: Check logs
docker-compose -f docker-compose.dev.yml logs -f aeon-saas-dev

# Step 4: Access application
# http://localhost:3000

# Step 5: Run database migrations (PostgreSQL for boilerplate)
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm run db:migrate

# Step 6: Stop when done
docker-compose -f docker-compose.dev.yml down
```

---

## 🔧 PHASE 4: ENVIRONMENT CONFIGURATION

### 4.1 .env.development (NEW FILE)

```bash
# .env.development - Development environment variables

# =============================================================================
# APPLICATION
# =============================================================================
NODE_ENV=development
NEXT_PUBLIC_APP_NAME="AEON SaaS Development"
PORT=3000

# =============================================================================
# CLERK AUTHENTICATION (SaaS-Boilerplate)
# =============================================================================
# Get these from: https://dashboard.clerk.com/
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="pk_test_YOUR_DEV_KEY_HERE"
CLERK_SECRET_KEY="sk_test_YOUR_DEV_SECRET_HERE"
NEXT_PUBLIC_CLERK_SIGN_IN_URL="/sign-in"
NEXT_PUBLIC_CLERK_SIGN_UP_URL="/sign-up"
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL="/dashboard"
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL="/dashboard"

# =============================================================================
# POSTGRESQL (SaaS-Boilerplate - Users, Teams, RBAC)
# =============================================================================
# LOCAL DEV: Use local postgres-dev container
DATABASE_URL="postgresql://postgres:postgres@postgres-dev:5432/aeon_saas_dev"

# OR connect to external PostgreSQL:
# DATABASE_URL="postgresql://user:password@host:5432/database"

# =============================================================================
# NEO4J (AEON - Cybersecurity Knowledge Graph)
# =============================================================================
NEO4J_URI="bolt://openspg-neo4j:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="neo4j@openspg"
NEO4J_DATABASE="neo4j"

# =============================================================================
# QDRANT (AEON - Vector Search)
# =============================================================================
QDRANT_URL="http://openspg-qdrant:6333"
QDRANT_API_KEY="deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ="

# =============================================================================
# MYSQL (AEON - OpenSPG Metadata)
# =============================================================================
MYSQL_HOST="openspg-mysql"
MYSQL_PORT="3306"
MYSQL_DATABASE="openspg"
MYSQL_USER="root"
MYSQL_PASSWORD="openspg"

# =============================================================================
# MINIO (AEON - Object Storage)
# =============================================================================
MINIO_ENDPOINT="openspg-minio"
MINIO_PORT="9000"
MINIO_ACCESS_KEY="minio"
MINIO_SECRET_KEY="minio@openspg"
MINIO_USE_SSL="false"

# =============================================================================
# OPENSPG SERVER (AEON - Knowledge Graph API)
# =============================================================================
OPENSPG_SERVER_URL="http://openspg-server:8887"

# =============================================================================
# OPENAI API (AEON - AI Chat)
# =============================================================================
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY="sk-YOUR_DEV_KEY_HERE"

# =============================================================================
# NEXT.JS CONFIGURATION
# =============================================================================
NEXT_TELEMETRY_DISABLED=1
WATCHPACK_POLLING=true
```

### 4.2 .env.example (UPDATE EXISTING)

Add AEON-specific variables to boilerplate's .env.example:

```bash
# Existing boilerplate variables...
DATABASE_URL=
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=

# ADD THESE (AEON-specific):
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=change-me
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY=change-me
MYSQL_HOST=openspg-mysql
MYSQL_DATABASE=openspg
MYSQL_USER=root
MYSQL_PASSWORD=change-me
MINIO_ENDPOINT=openspg-minio
MINIO_ACCESS_KEY=change-me
MINIO_SECRET_KEY=change-me
OPENSPG_SERVER_URL=http://openspg-server:8887
OPENAI_API_KEY=sk-change-me
```

---

## 🚀 PHASE 5: IMPLEMENTATION ROADMAP

### Week 1-2: Foundation Setup

**Tasks:**
- [ ] Clone ixartz/SaaS-Boilerplate repository
- [ ] Upgrade Next.js 14 → 15 in package.json
- [ ] Add AEON dependencies (Tremor, Neovis, database clients, AI SDK)
- [ ] Create docker-compose.dev.yml with openspg-network connection
- [ ] Create Dockerfile.dev for development
- [ ] Configure .env.development with all database connections
- [ ] Test Docker connectivity to all 5 backend services
- [ ] Run `npm install` and verify no dependency conflicts
- [ ] Test boilerplate functionality (auth, dashboard, teams)

**Validation:**
- ✅ Application starts in Docker dev mode
- ✅ Connects to openspg-network successfully
- ✅ Can reach Neo4j, Qdrant, MySQL, MinIO, OpenSPG from container
- ✅ Clerk authentication works
- ✅ Drizzle ORM connects to PostgreSQL
- ✅ Hot reload works with volume mounts

### Week 3-4: Database Integration Layer

**Tasks:**
- [ ] Create `src/libs/neo4j.ts` with driver initialization
- [ ] Create `src/libs/qdrant.ts` with client configuration
- [ ] Create `src/libs/mysql.ts` with connection pool
- [ ] Create `src/libs/minio.ts` with bucket setup
- [ ] Create `src/libs/openspg.ts` with API client
- [ ] Create `src/libs/hybrid-search.ts` for Neo4j + Qdrant integration
- [ ] Add connection health checks to `/api/health` endpoint
- [ ] Write integration tests for each database client
- [ ] Create `src/models/Neo4jSchema.ts` with TypeScript types
- [ ] Create `src/models/QdrantSchema.ts` with collection schemas
- [ ] Document database responsibility matrix

**Validation:**
- ✅ All 5 database clients initialize successfully
- ✅ Health check endpoint returns status for all databases
- ✅ Integration tests pass for Neo4j queries
- ✅ Qdrant vector search works
- ✅ MySQL queries execute successfully
- ✅ MinIO file upload/download works
- ✅ OpenSPG API calls return data

### Week 5-6: UI Component Library

**Tasks:**
- [ ] Create `src/components/aeon/` directory
- [ ] Build `ModernNav.tsx` with AEON navigation
- [ ] Build `WaveBackground.tsx` animated background
- [ ] Build `MetricsCard.tsx` with Tremor styling
- [ ] Add Tremor chart components (AreaChart, BarChart, DonutChart)
- [ ] Configure Tailwind with OKLCH color system
- [ ] Create design tokens in `src/utils/design-tokens.ts`
- [ ] Build shadcn/ui additional components (if needed)
- [ ] Set up Storybook stories for AEON components
- [ ] Test responsive design on mobile/tablet/desktop

**Validation:**
- ✅ All AEON components render correctly
- ✅ Tremor charts display sample data
- ✅ OKLCH colors match AEON design spec
- ✅ Responsive design works across devices
- ✅ Storybook stories document components
- ✅ Components integrate with existing shadcn/ui

### Week 7-8: AEON Pages Implementation (Part 1)

**Tasks:**
- [ ] Modify `/` (Homepage) with AEON landing page
- [ ] Extend `/dashboard` with AEON metrics cards
- [ ] Create `/graph` page with Neovis.js visualization
- [ ] Fix SSR issue: Use `next/dynamic` with `ssr: false` for vis-network
- [ ] Create `/graph` API route (`/api/graph/data/route.ts`)
- [ ] Build GraphVisualization component with vis-network
- [ ] Add graph controls (zoom, filter, layout)
- [ ] Create graph legend for node/edge types
- [ ] Test graph performance with large datasets (1000+ nodes)

**Validation:**
- ✅ Homepage displays AEON landing page
- ✅ Dashboard shows cybersecurity metrics
- ✅ Graph visualization renders Neo4j data
- ✅ No SSR errors with vis-network
- ✅ Graph is interactive (zoom, pan, select)
- ✅ Graph legend displays correctly
- ✅ Performance acceptable with 1000+ nodes

### Week 9-10: AEON Pages Implementation (Part 2)

**Tasks:**
- [ ] Create `/search` page with hybrid search
- [ ] Build SearchBar component
- [ ] Build SearchResults component with pagination
- [ ] Build SearchFilters sidebar
- [ ] Create `/api/search/route.ts` with Neo4j + Qdrant hybrid logic
- [ ] Implement debounced search input
- [ ] Add faceted filters (severity, type, date range)
- [ ] Create `/chat` page with AI streaming
- [ ] Integrate Vercel AI SDK `useChat` hook
- [ ] Create `/api/chat/route.ts` with OpenAI streaming
- [ ] Build ChatMessage component
- [ ] Build ChatInput component
- [ ] Add suggested actions/prompts
- [ ] Test streaming performance

**Validation:**
- ✅ Search returns results from Neo4j + Qdrant
- ✅ Hybrid search ranks results intelligently
- ✅ Filters work correctly
- ✅ Pagination works
- ✅ AI chat streams responses in real-time
- ✅ Chat maintains conversation context
- ✅ Suggested actions trigger correctly

### Week 11-12: AEON Pages Implementation (Part 3)

**Tasks:**
- [ ] Create `/upload` page with drag-and-drop
- [ ] Integrate MinIO for file storage
- [ ] Create `/api/upload/route.ts`
- [ ] Add file type validation
- [ ] Add progress indicators
- [ ] Create `/tags` page for tag management
- [ ] Build tag CRUD operations
- [ ] Connect tags to Neo4j entities
- [ ] Create `/analytics` page with advanced charts
- [ ] Add Tremor AreaChart, BarChart, DonutChart
- [ ] Create `/api/analytics/metrics/route.ts`
- [ ] Add time-series data queries
- [ ] Add export functionality (CSV, JSON)

**Validation:**
- ✅ File upload to MinIO works
- ✅ Progress indicators show correctly
- ✅ File validation prevents invalid types
- ✅ Tag management CRUD works
- ✅ Tags associate with Neo4j entities
- ✅ Analytics charts display data
- ✅ Export functionality works

### Week 13-14: Integration & Testing

**Tasks:**
- [ ] Write Playwright E2E tests for all pages
- [ ] Test authentication flow (Clerk)
- [ ] Test RBAC (boilerplate permissions)
- [ ] Test multi-tenancy (team switching)
- [ ] Test all database integrations
- [ ] Test graph visualization performance
- [ ] Test search relevance
- [ ] Test AI chat streaming
- [ ] Test file upload/download
- [ ] Load testing with k6 or Artillery
- [ ] Security audit (OWASP Top 10)
- [ ] Fix any bugs found

**Validation:**
- ✅ All E2E tests pass
- ✅ Authentication works correctly
- ✅ RBAC enforces permissions
- ✅ Multi-tenancy isolates data
- ✅ All databases perform well
- ✅ No security vulnerabilities found
- ✅ Load testing shows acceptable performance

### Week 15-16: Production Deployment

**Tasks:**
- [ ] Create `docker-compose.prod.yml` for production
- [ ] Update Dockerfile for production build
- [ ] Configure environment variables for production
- [ ] Set up database connection pooling
- [ ] Configure CDN for static assets
- [ ] Set up error monitoring (Sentry)
- [ ] Set up performance monitoring
- [ ] Configure backup strategies for PostgreSQL
- [ ] Document deployment procedures
- [ ] Create runbook for operations
- [ ] Final security review
- [ ] Deploy to staging environment
- [ ] User acceptance testing
- [ ] Deploy to production

**Validation:**
- ✅ Production build succeeds
- ✅ All services connect in production
- ✅ Performance meets requirements
- ✅ Error monitoring captures issues
- ✅ Backups are automated
- ✅ Documentation is complete
- ✅ Runbook covers common scenarios
- ✅ Production deployment successful

---

## 🧪 PHASE 6: TESTING STRATEGY

### 6.1 Unit Tests (Vitest)

```typescript
// tests/unit/libs/neo4j.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { neo4jDriver } from '@/libs/neo4j';

describe('Neo4j Client', () => {
  beforeAll(async () => {
    await neo4jDriver.verifyConnectivity();
  });

  afterAll(async () => {
    await neo4jDriver.close();
  });

  it('should connect to Neo4j', async () => {
    const session = neo4jDriver.session();
    const result = await session.run('RETURN 1 AS num');
    expect(result.records[0].get('num').toNumber()).toBe(1);
    await session.close();
  });

  it('should query threat data', async () => {
    const session = neo4jDriver.session();
    const result = await session.run(`
      MATCH (t:Threat)
      RETURN t.id AS id, t.severity AS severity
      LIMIT 10
    `);
    expect(result.records.length).toBeGreaterThan(0);
    await session.close();
  });
});
```

### 6.2 Integration Tests

```typescript
// tests/integration/hybrid-search.test.ts
import { describe, it, expect } from 'vitest';
import { hybridSearch } from '@/libs/hybrid-search';

describe('Hybrid Search', () => {
  it('should search Neo4j and Qdrant', async () => {
    const query = 'SQL injection vulnerability';
    const results = await hybridSearch(query, {
      limit: 10,
      semanticWeight: 0.5,
    });

    expect(results).toBeDefined();
    expect(results.length).toBeGreaterThan(0);
    expect(results[0]).toHaveProperty('score');
    expect(results[0]).toHaveProperty('source');
  });
});
```

### 6.3 End-to-End Tests (Playwright)

```typescript
// tests/e2e/graph.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Graph Visualization', () => {
  test('should load and display graph', async ({ page }) => {
    await page.goto('/graph');

    // Wait for graph to load
    await page.waitForSelector('canvas', { timeout: 10000 });

    // Check canvas rendered
    const canvas = await page.locator('canvas');
    expect(await canvas.isVisible()).toBeTruthy();

    // Test zoom controls
    await page.click('button[aria-label="Zoom In"]');
    await page.waitForTimeout(500);

    // Test node selection
    await page.click('canvas', { position: { x: 400, y: 300 } });
    await expect(page.locator('.node-details')).toBeVisible();
  });
});
```

---

## 📊 PHASE 7: PERFORMANCE MONITORING

### 7.1 Observability Setup

```typescript
// src/utils/observability.ts
import { register } from '@/instrumentation';

export interface PerformanceMetrics {
  operation: string;
  duration: number;
  success: boolean;
  timestamp: number;
}

export function trackPerformance(
  operation: string,
  fn: () => Promise<any>
): Promise<any> {
  const start = Date.now();

  return fn()
    .then((result) => {
      const duration = Date.now() - start;
      logMetric({ operation, duration, success: true, timestamp: start });
      return result;
    })
    .catch((error) => {
      const duration = Date.now() - start;
      logMetric({ operation, duration, success: false, timestamp: start });
      throw error;
    });
}

function logMetric(metric: PerformanceMetrics) {
  // Send to monitoring service (Sentry, Datadog, etc.)
  console.log('[METRIC]', metric);
}
```

### 7.2 Database Query Performance

```typescript
// src/libs/neo4j.ts (with monitoring)
export async function queryNeo4j(cypher: string, params: any = {}) {
  return trackPerformance('neo4j_query', async () => {
    const session = neo4jDriver.session();
    try {
      const result = await session.run(cypher, params);
      return result.records;
    } finally {
      await session.close();
    }
  });
}
```

---

## 🔒 PHASE 8: SECURITY CONSIDERATIONS

### 8.1 Authentication & Authorization

**KEEP: SaaS-Boilerplate Clerk Integration**
- Clerk handles user authentication
- Multi-factor authentication (MFA)
- Social login providers
- Enterprise SSO

**ADD: AEON-specific Authorization**
- Role-based access to cybersecurity data
- Team-based data isolation
- API key management for external integrations

### 8.2 Database Security

```typescript
// src/middleware/database-security.ts
export function sanitizeNeo4jQuery(userInput: string): string {
  // Prevent Cypher injection
  return userInput.replace(/[;'"\\]/g, '');
}

export function validateQdrantQuery(query: any): boolean {
  // Validate Qdrant query structure
  return typeof query === 'string' && query.length < 1000;
}
```

### 8.3 Environment Variables Security

- ✅ Never commit `.env` files to Git
- ✅ Use Docker secrets for production
- ✅ Rotate API keys regularly
- ✅ Use read-only database users where possible
- ✅ Enable SSL for all database connections in production

---

## 📈 PHASE 9: METRICS & SUCCESS CRITERIA

### 9.1 Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Page Load Time** | < 2s | Lighthouse audit |
| **Graph Render Time** | < 3s for 1000 nodes | Performance API |
| **Search Latency** | < 500ms | API response time |
| **AI Chat Response** | < 2s for first token | Streaming metrics |
| **Database Query Time** | < 100ms (95th percentile) | Query logs |
| **API Error Rate** | < 1% | Error monitoring |
| **Test Coverage** | > 80% | Vitest coverage report |

### 9.2 Functional Success Criteria

- ✅ All 7 AEON pages functional
- ✅ All 5 databases integrated and queryable
- ✅ Clerk authentication works
- ✅ RBAC enforces permissions
- ✅ Multi-tenancy isolates team data
- ✅ Graph visualization renders 1000+ nodes
- ✅ Hybrid search returns relevant results
- ✅ AI chat streams responses
- ✅ File upload to MinIO works
- ✅ Analytics charts display data

---

## 🚨 PHASE 10: RISK MITIGATION

### 10.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Dependency conflicts** | High | Medium | Pin exact versions, test upgrades in isolation |
| **SSR issues with vis-network** | Medium | High | Use `next/dynamic` with `ssr: false` (known solution) |
| **Database performance** | High | Medium | Implement connection pooling, query optimization |
| **Multi-database complexity** | Medium | High | Clear separation of concerns, abstraction layers |
| **Docker network issues** | Medium | Low | Test connectivity thoroughly, document troubleshooting |
| **Authentication integration** | Medium | Low | Clerk is well-documented, active community support |

### 10.2 Contingency Plans

**If Next.js 15 upgrade causes issues:**
- Fall back to Next.js 14 temporarily
- Isolate breaking changes
- Upgrade incrementally

**If database connections fail:**
- Add circuit breakers
- Implement fallback to cached data
- Document manual connection procedures

**If performance is inadequate:**
- Implement caching layer (Redis)
- Optimize database queries
- Add pagination to large data sets

---

## 📝 PHASE 11: DOCUMENTATION DELIVERABLES

### 11.1 Required Documentation

1. **README.md** - Project overview and quick start
2. **ARCHITECTURE.md** - System architecture diagram
3. **DATABASE_INTEGRATION.md** - Multi-database setup guide
4. **API_DOCUMENTATION.md** - API routes and endpoints
5. **DEPLOYMENT.md** - Production deployment procedures
6. **TROUBLESHOOTING.md** - Common issues and solutions
7. **DEVELOPMENT.md** - Developer onboarding guide
8. **TESTING.md** - Testing strategies and commands

### 11.2 Code Documentation

- TypeScript JSDoc comments for all public functions
- Inline comments for complex logic
- Storybook stories for UI components
- OpenAPI spec for API routes

---

## 🎯 PHASE 12: FINAL CHECKLIST

### Pre-Development

- [X] Clone ixartz/SaaS-Boilerplate
- [ ] Review boilerplate documentation
- [ ] Set up development environment
- [ ] Configure .env.development
- [ ] Create docker-compose.dev.yml
- [ ] Test openspg-network connectivity

### Development

- [ ] Week 1-2: Foundation setup
- [ ] Week 3-4: Database integration
- [ ] Week 5-6: UI components
- [ ] Week 7-8: AEON pages (part 1)
- [ ] Week 9-10: AEON pages (part 2)
- [ ] Week 11-12: AEON pages (part 3)
- [ ] Week 13-14: Testing
- [ ] Week 15-16: Production deployment

### Testing

- [ ] Unit tests (>80% coverage)
- [ ] Integration tests (all databases)
- [ ] E2E tests (Playwright)
- [ ] Performance testing
- [ ] Security audit
- [ ] User acceptance testing

### Deployment

- [ ] Production Docker configuration
- [ ] Environment variables configured
- [ ] Database migrations tested
- [ ] Monitoring setup
- [ ] Backup strategies implemented
- [ ] Documentation complete

---

## 📧 SUPPORT & RESOURCES

### SaaS-Boilerplate Resources

- **GitHub:** https://github.com/ixartz/SaaS-Boilerplate
- **Documentation:** Included in repository
- **Issues:** GitHub Issues for boilerplate bugs

### AEON Resources

- **Technical Spec:** `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Front End UI Builder/TECHNICAL_SPECIFICATION_UI.md`
- **Existing Code:** `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/`
- **Docker Configs:** `docker-compose.aeon-ui.yml`, `Dockerfile`

### Third-Party Documentation

- **Clerk Auth:** https://clerk.com/docs
- **Drizzle ORM:** https://orm.drizzle.team/docs/overview
- **Neo4j Driver:** https://neo4j.com/docs/javascript-manual/current/
- **Qdrant:** https://qdrant.tech/documentation/
- **Tremor:** https://www.tremor.so/docs/getting-started/installation
- **Neovis.js:** https://github.com/neo4j-contrib/neovis.js
- **Vercel AI SDK:** https://sdk.vercel.ai/docs

---

## 🏁 CONCLUSION

This integration plan provides a FACT-BASED roadmap for extending the ixartz/SaaS-Boilerplate with AEON Digital Twin features. The approach leverages the boilerplate's strengths (auth, RBAC, multi-tenancy, testing) while adding cybersecurity-specific pages and multi-database integrations.

**Key Success Factors:**
1. ✅ EXTEND, don't replace the boilerplate
2. ✅ Maintain separation of concerns (PostgreSQL for users, other DBs for AEON data)
3. ✅ Use Docker development environment connecting to openspg-network
4. ✅ Follow existing boilerplate patterns and conventions
5. ✅ Test thoroughly at each phase
6. ✅ Document everything

**Timeline:** 10-12 weeks
**Cost:** $52,000 - $65,000
**Risk:** MEDIUM (manageable with proper planning)
**Outcome:** Production-ready cybersecurity intelligence platform with SaaS features

---

**Document Status:** COMPLETE
**Last Updated:** 2025-01-04 17:45:00 CST
**Version:** 1.0.0
**Next Steps:** Review plan with stakeholders, approve budget, begin Week 1-2 foundation setup
