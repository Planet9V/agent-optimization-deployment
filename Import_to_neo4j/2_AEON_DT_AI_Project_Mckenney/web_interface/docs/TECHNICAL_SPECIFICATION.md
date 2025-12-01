# AEON Digital Twin - Technical Specification

**Document Version:** 1.0.0
**Last Updated:** 2025-11-04
**Project:** AEON Cybersecurity Intelligence Platform
**Framework:** Next.js 15 with App Router

---

## Executive Summary

AEON Digital Twin is a cybersecurity intelligence platform built with Next.js 15, featuring real-time threat intelligence visualization, AI-powered analysis, and multi-database integration. The application leverages Neo4j for graph-based knowledge representation, Qdrant for vector similarity search, MySQL for relational data, and MinIO for object storage.

---

## 1. Next.js Configuration

### 1.1 Version & Template
- **Next.js Version:** 15.0.3
- **React Version:** 18.3.1
- **TypeScript Version:** 5.6.3
- **Node Requirement:** >=20.0.0
- **NPM Requirement:** >=10.0.0
- **Template Base:** Custom Next.js 15 with App Router

### 1.2 Build Configuration (`next.config.ts`)

```typescript
{
  output: 'standalone',              // Docker-optimized output
  reactStrictMode: true,             // Development safety checks
  poweredByHeader: false,            // Security: Remove X-Powered-By
  compress: true,                    // Enable gzip compression
  staticPageGenerationTimeout: 120,  // Complex page generation timeout

  // Webpack Configuration
  webpack: {
    externals: ['vis-network', 'vis-data'],  // Server-side exclusions
    resolve: {
      fallback: {
        fs: false,
        net: false,
        tls: false
      }
    }
  },

  // Environment Variables
  env: {
    NEXT_PUBLIC_APP_NAME: 'AEON UI'
  },

  // Image Optimization
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: 'localhost' },
      { protocol: 'http', hostname: 'openspg-minio' }
    ]
  },

  // Server Actions
  experimental: {
    serverActions: {
      allowedOrigins: ['localhost:3000', 'aeon-ui:3000']
    }
  }
}
```

---

## 2. Dependencies Analysis

### 2.1 Core Framework Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `next` | 15.0.3 | React framework with App Router |
| `react` | 18.3.1 | UI library |
| `react-dom` | 18.3.1 | React DOM renderer |
| `typescript` | 5.6.3 | Type safety |

### 2.2 Database & Storage Integration

| Package | Version | Purpose |
|---------|---------|---------|
| `neo4j-driver` | 5.25.0 | Graph database client (knowledge graphs) |
| `@qdrant/js-client-rest` | 1.15.1 | Vector database client (semantic search) |
| `mysql2` | 3.11.3 | MySQL database client (relational data) |
| `minio` | 8.0.1 | S3-compatible object storage client |
| `@neondatabase/serverless` | 1.0.2 | Neon serverless Postgres (optional) |
| `@prisma/client` | 5.22.0 | ORM for database management |

### 2.3 AI & Machine Learning

| Package | Version | Purpose |
|---------|---------|---------|
| `ai` | 5.0.87 | Vercel AI SDK for streaming responses |
| `@ai-sdk/openai` | 2.0.62 | OpenAI provider for AI SDK |
| `openai` | 6.8.0 | OpenAI API client |
| `zod` | 4.1.12 | Schema validation for AI inputs |

### 2.4 UI Components & Styling

#### Styling Foundation
| Package | Version | Purpose |
|---------|---------|---------|
| `tailwindcss` | 3.4.14 | Utility-first CSS framework |
| `autoprefixer` | 10.4.20 | CSS vendor prefixing |
| `postcss` | 8.4.47 | CSS transformations |
| `class-variance-authority` | 0.7.1 | Component variant management |
| `clsx` | 2.1.1 | Conditional className utilities |
| `tailwind-merge` | 2.6.0 | Tailwind class merging |

#### Component Libraries
| Package | Version | Purpose |
|---------|---------|---------|
| `@radix-ui/react-checkbox` | 1.3.3 | Accessible checkbox components |
| `@tremor/react` | 3.18.3 | Analytics dashboard components |
| `lucide-react` | 0.454.0 | Modern icon library (1000+ icons) |
| `framer-motion` | 12.23.24 | Animation library |

#### Visualization Libraries
| Package | Version | Purpose |
|---------|---------|---------|
| `neovis.js` | 2.1.0 | Neo4j graph visualization |
| `recharts` | 2.13.3 | Composable charting library |
| `chart.js` | 4.5.1 | Canvas-based charts |
| `react-chartjs-2` | 5.3.1 | React wrapper for Chart.js |

### 2.5 Authentication & Security

| Package | Version | Purpose |
|---------|---------|---------|
| `next-auth` | 4.24.10 | Authentication for Next.js |
| `uuid` | 13.0.0 | UUID generation |
| `@types/uuid` | 10.0.0 | TypeScript types for UUID |

### 2.6 Testing & Quality Assurance

| Package | Version | Purpose |
|---------|---------|---------|
| `@playwright/test` | 1.56.1 | End-to-end testing |
| `jest` | 30.2.0 | Unit testing framework |
| `@jest/globals` | 30.2.0 | Jest global utilities |
| `ts-jest` | 29.4.5 | TypeScript support for Jest |
| `supertest` | 7.1.4 | HTTP testing |
| `@types/supertest` | 6.0.3 | TypeScript types for Supertest |

### 2.7 Development Tools

| Package | Version | Purpose |
|---------|---------|---------|
| `eslint` | 9.14.0 | Code linting |
| `eslint-config-next` | 15.0.3 | Next.js ESLint configuration |
| `prisma` | 5.22.0 | Database schema management |
| `ts-node` | 10.9.2 | TypeScript execution |

---

## 3. Project Structure

### 3.1 Directory Layout

```
web_interface/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with WaveBackground
│   ├── page.tsx                 # Homepage dashboard
│   ├── globals.css              # Global styles
│   │
│   ├── api/                     # API Routes (Next.js 15 Route Handlers)
│   │   ├── health/             # Health check endpoint
│   │   ├── search/             # Hybrid search (Neo4j + Qdrant)
│   │   ├── chat/               # AI chat endpoint
│   │   ├── customers/          # Customer management
│   │   ├── tags/               # Tag management
│   │   ├── upload/             # File upload (MinIO)
│   │   ├── analytics/          # Analytics endpoints
│   │   │   ├── metrics/        # Metrics aggregation
│   │   │   ├── timeseries/     # Time-series data
│   │   │   └── export/         # Data export
│   │   ├── activity/           # Activity tracking
│   │   ├── pipeline/           # Data pipeline management
│   │   │   ├── process/        # Pipeline processing
│   │   │   └── status/[jobId]/ # Job status tracking
│   │   └── observability/      # System observability
│   │       ├── performance/    # Performance metrics
│   │       └── system/         # System health
│   │
│   ├── dashboard/              # Main dashboard page
│   ├── graph/                  # Neo4j graph visualization
│   ├── search/                 # Search interface
│   ├── chat/                   # AI chat interface
│   └── settings/               # Settings page
│
├── components/                  # React Components
│   ├── ModernNav.tsx           # Navigation component
│   ├── WaveBackground.tsx      # Animated background
│   │
│   ├── dashboard/              # Dashboard components
│   │   ├── MetricsCard.tsx
│   │   ├── QuickActions.tsx
│   │   ├── RecentActivity.tsx
│   │   └── SystemHealth.tsx
│   │
│   ├── animations/             # Animation components
│   │   ├── AnimatedCard.tsx
│   │   ├── WaveBackground.tsx
│   │   └── AnimationExamples.tsx
│   │
│   ├── search/                 # Search components
│   │   └── SearchResults.tsx
│   │
│   ├── chat/                   # Chat components
│   │   ├── ChatMessage.tsx
│   │   └── SuggestedActions.tsx
│   │
│   ├── layout/                 # Layout components
│   │   └── Navigation.tsx
│   │
│   └── ui/                     # Shadcn UI components
│       ├── card.tsx
│       ├── button.tsx
│       ├── input.tsx
│       ├── badge.tsx
│       ├── label.tsx
│       ├── alert.tsx
│       ├── dialog.tsx
│       └── wave-background.tsx
│
├── lib/                        # Utility Libraries
│   ├── utils.ts               # General utilities
│   ├── design-tokens.ts       # Design system tokens
│   ├── neo4j-enhanced.ts      # Neo4j client with retry logic
│   ├── ai-orchestrator.ts     # AI orchestration layer
│   ├── hybrid-search.ts       # Neo4j + Qdrant hybrid search
│   │
│   └── observability/         # Observability utilities
│       ├── index.ts
│       ├── agent-tracker.ts
│       ├── component-tracker.ts
│       └── performance-monitor.ts
│
├── hooks/                      # React Hooks
│   └── [custom hooks]
│
├── styles/                     # Additional styles
├── public/                     # Static assets
├── tests/                      # Test files
├── scripts/                    # Utility scripts
├── docs/                       # Documentation
│
├── next.config.ts             # Next.js configuration
├── tailwind.config.ts         # Tailwind CSS configuration
├── tsconfig.json              # TypeScript configuration
├── postcss.config.mjs         # PostCSS configuration
├── .eslintrc.json            # ESLint configuration
├── jest.config.js            # Jest configuration
├── package.json              # Dependencies & scripts
└── .env.example              # Environment variables template
```

### 3.2 Key Architectural Patterns

#### App Router Structure (Next.js 15)
- **Server Components by Default:** All components are React Server Components unless marked with `'use client'`
- **File-based Routing:** Pages defined by folder structure
- **Route Handlers:** API routes using `route.ts` files
- **Layouts:** Nested layouts with `layout.tsx`
- **Loading States:** `loading.tsx` for suspense boundaries
- **Error Boundaries:** `error.tsx` for error handling

#### Component Organization
- **UI Layer:** Atomic design with shadcn/ui components
- **Feature Components:** Domain-specific components (dashboard, search, chat)
- **Layout Components:** Navigation and structural components
- **Animation Components:** Framer Motion powered animations

---

## 4. TypeScript Configuration

### 4.1 Compiler Options (`tsconfig.json`)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,                    // Strict type checking
    "noEmit": true,                    // No JS output (Next.js handles)
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]                   // Path alias for imports
    }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts"
  ],
  "exclude": ["node_modules"]
}
```

### 4.2 Type Safety Features
- **Strict Mode Enabled:** Full TypeScript strict mode
- **Path Aliases:** `@/` maps to project root
- **Next.js Plugin:** Enhanced type checking for App Router
- **Incremental Compilation:** Faster development builds

---

## 5. Tailwind CSS Configuration

### 5.1 Design System Overview

The application uses a custom **VulnCheck Dark Theme** with OKLCH color space for perceptually uniform colors.

### 5.2 Color System (OKLCH)

#### Brand Colors
```css
vulncheck-emerald-500: oklch(69.6% 0.17 162.48)  /* Primary accent */
vulncheck-emerald-600: oklch(64.2% 0.17 162.48)  /* Hover state */
vulncheck-emerald-400: oklch(74.6% 0.17 162.48)  /* Lighter accent */
```

#### Background Levels
```css
vulncheck-bg-primary:   oklch(12.9% 0.042 264.695)  /* slate-950 */
vulncheck-bg-secondary: oklch(20.8% 0.042 265.755)  /* slate-900 */
vulncheck-bg-tertiary:  oklch(25% 0.042 265)
vulncheck-bg-elevated:  oklch(30% 0.042 265)
```

#### Severity Colors
```css
critical: oklch(65% 0.24 25)   /* Red */
high:     oklch(72% 0.18 45)   /* Orange */
medium:   oklch(78% 0.15 85)   /* Yellow */
low:      oklch(72% 0.15 240)  /* Blue */
info:     oklch(70% 0.14 162)  /* Emerald */
```

### 5.3 Custom Utilities

#### Glass Effect
```css
.glass-effect {
  background: oklch(25% 0.042 265 / 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid oklch(45% 0.018 265 / 0.2);
}
```

#### Text Gradient
```css
.text-gradient-cyber {
  background: linear-gradient(135deg,
    oklch(74.6% 0.17 162.48),
    oklch(64.2% 0.17 162.48)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### 5.4 Animation System

#### Keyframe Animations
- `wave`: Floating wave animation (10s, 15s, 7s variants)
- `pulse-slow`: Slow pulsing effect (3s)
- `skeleton`: Loading skeleton animation (1.5s)
- `fade-in`: Fade in transition (0.3s)
- `slide-up`: Slide up with fade (0.3s)
- `slide-down`: Slide down with fade (0.3s)

#### Box Shadows
- `shadow-vc-sm/md/lg/xl`: Elevation shadows
- `shadow-glow-emerald`: Emerald glow effect
- `shadow-glow-critical`: Critical alert glow

### 5.5 Custom Spacing & Typography

```typescript
spacing: {
  'vc-1': '0.25rem',
  'vc-2': '0.5rem',
  'vc-4': '1rem',
  'vc-8': '2rem',
  'vc-16': '4rem'
}

fontSize: {
  'vc-xs': ['0.75rem', { lineHeight: '1rem', letterSpacing: '0.05em' }],
  'vc-base': ['1rem', { lineHeight: '1.5rem' }],
  'vc-2xl': ['1.5rem', { lineHeight: '2rem' }]
}
```

---

## 6. Backend Integration Architecture

### 6.1 Neo4j Graph Database

**Purpose:** Knowledge graph storage for cybersecurity entities and relationships

#### Connection Configuration
```typescript
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg
NEO4J_DATABASE=neo4j
```

#### Use Cases
- CVE vulnerability tracking
- Threat actor relationship mapping
- Malware family genealogy
- Attack technique taxonomy (MITRE ATT&CK)
- Campaign and indicator tracking
- Entity relationship visualization

#### Client Implementation (`lib/neo4j-enhanced.ts`)
- Connection pooling with retry logic
- Automatic reconnection on failure
- Query timeout handling
- Transaction management

### 6.2 Qdrant Vector Database

**Purpose:** Semantic search and similarity matching

#### Connection Configuration
```typescript
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=
```

#### Use Cases
- Semantic document search
- Similar CVE discovery
- Threat intelligence similarity
- Natural language query processing
- Document embedding storage
- Hybrid search with Neo4j

#### Client Implementation (`lib/hybrid-search.ts`)
- Vector embedding generation
- Collection management
- Similarity search
- Hybrid Neo4j + Qdrant queries

### 6.3 MySQL Relational Database

**Purpose:** Structured data storage and transactional operations

#### Connection Configuration
```typescript
MYSQL_HOST=openspg-mysql
MYSQL_PORT=3306
MYSQL_DATABASE=openspg
MYSQL_USER=root
MYSQL_PASSWORD=openspg
```

#### Use Cases
- User account management
- Activity logging
- Tag management
- Customer data
- Metrics aggregation
- Time-series analytics

#### ORM: Prisma
- Type-safe database queries
- Schema migrations
- Relationship management
- Query optimization

### 6.4 MinIO Object Storage

**Purpose:** S3-compatible object storage for files and documents

#### Connection Configuration
```typescript
MINIO_ENDPOINT=http://openspg-minio:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false
```

#### Use Cases
- Document upload storage
- PDF file management
- Report generation storage
- Analytics export storage
- Backup file storage

#### Client Implementation
- Bucket management
- Pre-signed URLs for secure downloads
- Multipart uploads for large files
- File metadata management

### 6.5 OpenSPG Server Integration

**Purpose:** Knowledge graph processing and enrichment

#### Connection Configuration
```typescript
OPENSPG_SERVER_URL=http://openspg-server:8887
```

#### Use Cases
- Document processing pipeline
- Entity extraction
- Relationship inference
- Knowledge graph construction
- Data enrichment

---

## 7. API Architecture

### 7.1 Route Handler Pattern (Next.js 15)

All API routes use Next.js 15 Route Handlers with the following structure:

```typescript
// app/api/[endpoint]/route.ts
export async function GET(request: Request) { }
export async function POST(request: Request) { }
export async function PUT(request: Request) { }
export async function DELETE(request: Request) { }
```

### 7.2 API Endpoints

#### Health & Status
- `GET /api/health` - System health check

#### Search & Discovery
- `POST /api/search` - Hybrid search (Neo4j + Qdrant)
- `GET /api/entities?type=[type]` - Entity listing by type

#### AI & Chat
- `POST /api/chat` - AI chat endpoint (streaming responses)

#### Data Management
- `GET /api/customers` - List customers
- `POST /api/customers` - Create customer
- `GET /api/customers/[id]` - Get customer by ID
- `PUT /api/customers/[id]` - Update customer
- `DELETE /api/customers/[id]` - Delete customer

#### Tags & Taxonomy
- `GET /api/tags` - List tags
- `POST /api/tags` - Create tag
- `POST /api/tags/assign` - Assign tag to entity
- `DELETE /api/tags/[id]` - Delete tag

#### Analytics
- `GET /api/analytics/metrics` - Aggregated metrics
- `GET /api/analytics/timeseries` - Time-series data
- `GET /api/analytics/export` - Export analytics data

#### Activity Tracking
- `GET /api/activity/recent` - Recent activity feed

#### Pipeline Management
- `POST /api/pipeline/process` - Start document processing
- `GET /api/pipeline/status/[jobId]` - Check job status

#### Observability
- `GET /api/observability/performance` - Performance metrics
- `GET /api/observability/system` - System metrics

#### File Upload
- `POST /api/upload` - Upload files to MinIO

---

## 8. Authentication & Security

### 8.1 NextAuth Configuration

**Package:** `next-auth@4.24.10`

#### Environment Variables
```env
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=change-me-in-production
```

#### Features
- JWT-based authentication
- Session management
- OAuth provider support
- Credential provider
- Server-side session validation

### 8.2 Security Measures

#### Headers
- `poweredByHeader: false` - Hide framework identity
- Content Security Policy (recommended to implement)
- CORS configuration via `allowedOrigins`

#### Input Validation
- Zod schema validation
- Type safety with TypeScript
- SQL injection prevention via Prisma

#### Data Protection
- Environment variable isolation
- Secure password storage
- API key rotation support

---

## 9. Performance Optimization

### 9.1 Build Optimizations

- **Standalone Output:** Optimized for Docker deployment
- **Compression:** gzip enabled
- **Tree Shaking:** Automatic dead code elimination
- **Code Splitting:** Automatic route-based splitting
- **Image Optimization:** Next.js Image component with remote patterns

### 9.2 Runtime Optimizations

- **React Server Components:** Reduce client-side JavaScript
- **Streaming SSR:** Progressive page rendering
- **Incremental Static Regeneration:** Static page updates without rebuild
- **Connection Pooling:** Database connection reuse
- **Caching Strategy:** API route caching (to be implemented)

### 9.3 Monitoring (`lib/observability/`)

- **Performance Monitor:** Track render times and API latency
- **Agent Tracker:** Monitor background jobs
- **Component Tracker:** Track component lifecycle

---

## 10. Development Workflow

### 10.1 Scripts

```json
{
  "dev": "next dev",              // Start development server (port 3000)
  "build": "next build",          // Production build
  "start": "next start",          // Start production server
  "lint": "next lint",            // Run ESLint
  "typecheck": "tsc --noEmit"     // Type checking without output
}
```

### 10.2 Testing Strategy

#### Unit Testing (Jest)
- Configuration: `jest.config.js`
- Framework: `@jest/globals@30.2.0`
- TypeScript support: `ts-jest@29.4.5`

#### E2E Testing (Playwright)
- Configuration: `playwright.config.ts` (to be created)
- Framework: `@playwright/test@1.56.1`

#### API Testing (Supertest)
- HTTP endpoint testing
- Integration tests for API routes

### 10.3 Code Quality

#### ESLint Configuration
```json
{
  "extends": "next/core-web-vitals"
}
```

#### TypeScript Strict Mode
- All strict checks enabled
- No implicit any
- Strict null checks

---

## 11. Deployment Architecture

### 11.1 Docker Configuration

**Build Target:** Standalone output for optimized Docker images

#### Recommended Dockerfile Structure
```dockerfile
FROM node:20-alpine AS base
FROM base AS deps
# Install dependencies
FROM base AS builder
# Build Next.js application
FROM base AS runner
# Run application with minimal footprint
```

### 11.2 Environment Configuration

**Production Checklist:**
- [ ] Generate secure `NEXTAUTH_SECRET`
- [ ] Configure production database URLs
- [ ] Set up SSL for MinIO (`MINIO_USE_SSL=true`)
- [ ] Configure CORS origins
- [ ] Set up monitoring and logging
- [ ] Configure backup strategies

### 11.3 Scaling Considerations

- **Horizontal Scaling:** Stateless Next.js instances
- **Database Connection Pooling:** Configure max connections
- **CDN Integration:** Static asset delivery
- **Load Balancing:** Behind reverse proxy (Traefik, nginx)

---

## 12. Known Issues & Technical Debt

### 12.1 Current Limitations

1. **vis-network Server-Side Rendering:** Excluded from server bundle due to browser-only dependencies
2. **Static Stats:** Homepage stats currently hardcoded (to be replaced with API)
3. **Error Boundaries:** Need comprehensive error handling implementation
4. **Authentication:** NextAuth configured but not fully integrated
5. **Testing Coverage:** E2E tests not yet implemented

### 12.2 Planned Improvements

1. Implement comprehensive error boundaries
2. Add loading states for all data fetching
3. Implement API response caching
4. Add retry logic to all external service calls
5. Implement comprehensive logging system
6. Add performance monitoring dashboard
7. Implement automated testing suite

---

## 13. Technology Stack Summary

| Category | Technologies |
|----------|-------------|
| **Framework** | Next.js 15, React 18, TypeScript 5.6 |
| **Styling** | Tailwind CSS 3.4, OKLCH color system, Framer Motion |
| **UI Components** | Radix UI, Tremor, shadcn/ui, Lucide icons |
| **Databases** | Neo4j 5.25, Qdrant, MySQL (via Prisma) |
| **Storage** | MinIO (S3-compatible) |
| **AI/ML** | Vercel AI SDK, OpenAI API |
| **Visualization** | Neovis.js, Recharts, Chart.js |
| **Testing** | Jest, Playwright, Supertest |
| **Authentication** | NextAuth.js |
| **Build Tools** | Webpack (via Next.js), ESLint, PostCSS |

---

## 14. Quick Start Guide

### 14.1 Development Setup

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Configure environment variables
# Edit .env.local with your database credentials

# Start development server
npm run dev

# Open browser
http://localhost:3000
```

### 14.2 Production Build

```bash
# Type check
npm run typecheck

# Lint code
npm run lint

# Build for production
npm run build

# Start production server
npm start
```

---

## 15. Additional Resources

### 15.1 Documentation Links
- Next.js 15: https://nextjs.org/docs
- Tailwind CSS: https://tailwindcss.com/docs
- Neo4j Driver: https://neo4j.com/docs/javascript-manual/
- Qdrant Client: https://qdrant.tech/documentation/
- Vercel AI SDK: https://sdk.vercel.ai/docs

### 15.2 Project Documentation
- API Documentation: `/docs/API.md` (to be created)
- Component Library: `/docs/COMPONENTS.md` (to be created)
- Database Schema: `/docs/DATABASE_SCHEMA.md` (to be created)

---

**Document End**

*This specification reflects the current state of the AEON Digital Twin web interface as of November 4, 2025.*
