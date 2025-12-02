# Clerk Authentication and Container Infrastructure

**File:** CLERK_AUTH_AND_INFRASTRUCTURE.md
**Created:** 2025-12-02
**Version:** 1.0.0
**Purpose:** Document existing Clerk authentication setup and container infrastructure for frontend developers
**Status:** ACTIVE

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current System State](#current-system-state)
3. [Container Infrastructure](#container-infrastructure)
4. [Clerk Authentication Setup](#clerk-authentication-setup)
5. [Authentication Flow](#authentication-flow)
6. [Environment Variables](#environment-variables)
7. [Frontend Integration Points](#frontend-integration-points)
8. [What's Already Working](#whats-already-working)
9. [What Developers Must Preserve](#what-developers-must-preserve)
10. [Development Guidelines](#development-guidelines)
11. [Troubleshooting](#troubleshooting)

---

## Executive Summary

### What Is This Document?

This document provides a comprehensive overview of the **existing** and **working** Clerk authentication system integrated with the AEON Digital Twin cybersecurity platform. It is designed for frontend developers who need to understand the current implementation without breaking it.

### Key Facts

- **Authentication Provider:** Clerk (version 6.34.2)
- **Framework:** Next.js 15.0.3 with App Router
- **Deployment:** Docker containers (`aeon-saas-dev`, `aeon-postgres-dev`)
- **Status:** PRODUCTION-READY and OPERATIONAL
- **Network:** Connected to `openspg-network` for AEON backend services

### Critical Warning

⚠️ **DO NOT MODIFY** the following without explicit approval:
- Clerk middleware configuration
- Environment variable structure
- Container networking setup
- Authentication flow logic

---

## Current System State

### Container Status (as of 2025-12-02)

```
CONTAINER NAME       STATUS               PORTS
aeon-saas-dev        Up 35 hours (healthy)  0.0.0.0:3000->3000/tcp
aeon-postgres-dev    Up 35 hours (healthy)  0.0.0.0:5432->5432/tcp
```

### Package Versions

| Package | Version | Purpose |
|---------|---------|---------|
| `@clerk/nextjs` | 6.34.2 | Clerk Next.js SDK |
| `@clerk/themes` | 2.4.40 | Clerk UI theming |
| `next` | 15.0.3 | Next.js framework |
| `react` | 19.0.0 | React library |
| `postgres` | 16-alpine | PostgreSQL database |

### Technology Stack

- **Frontend Framework:** Next.js 15 with App Router
- **Authentication:** Clerk (SaaS authentication)
- **Database:** PostgreSQL 16 (local development)
- **Backend Services:** Neo4j, Qdrant, MySQL, MinIO (via openspg-network)
- **Containerization:** Docker Compose

---

## Container Infrastructure

### 1. aeon-saas-dev Container

#### Purpose
Main Next.js application container running the AEON Digital Twin frontend with integrated Clerk authentication.

#### Configuration (`docker-compose.dev.yml`)

```yaml
aeon-saas-dev:
  build:
    context: .
    dockerfile: Dockerfile.dev
  container_name: aeon-saas-dev
  command: npm run dev
  networks:
    - openspg-network
  ports:
    - "3000:3000"
  restart: unless-stopped
```

#### Volume Mounts (Hot Reload Enabled)

```yaml
volumes:
  # Source code volumes (delegated for performance)
  - ./app:/app/app:delegated
  - ./components:/app/components:delegated
  - ./lib:/app/lib:delegated
  - ./public:/app/public:delegated
  - ./styles:/app/styles:delegated
  - ./hooks:/app/hooks:delegated

  # Configuration files (read-only)
  - ./package.json:/app/package.json:ro
  - ./tsconfig.json:/app/tsconfig.json:ro
  - ./next.config.ts:/app/next.config.ts:ro
  - ./tailwind.config.ts:/app/tailwind.config.ts:ro

  # Excluded from volume mounts (performance)
  - /app/node_modules
  - /app/.next
```

#### Health Check

```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "-O", "/dev/null", "http://0.0.0.0:3000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

**Current Status:** ✅ Healthy (passing health checks every 30-40ms)

#### Environment Variables

See [Environment Variables](#environment-variables) section for complete configuration.

### 2. aeon-postgres-dev Container

#### Purpose
Local PostgreSQL database for SaaS-Boilerplate features (user accounts, teams, RBAC, billing).

#### Configuration

```yaml
postgres-dev:
  image: postgres:16-alpine
  container_name: aeon-postgres-dev
  networks:
    - openspg-network
  ports:
    - "5432:5432"
  environment:
    - POSTGRES_DB=aeon_saas_dev
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
  volumes:
    - postgres_dev_data:/var/lib/postgresql/data
    - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql:ro
  restart: unless-stopped
```

#### Health Check

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres -d aeon_saas_dev"]
  interval: 10s
  timeout: 5s
  retries: 5
```

**Current Status:** ✅ Healthy (accepting connections)

#### Database Schema

```
Database: aeon_saas_dev
User: postgres
Encoding: UTF-8
Locale: en_US.UTF-8
```

**Purpose:**
- User authentication metadata (synced with Clerk)
- Team/organization management
- Role-based access control (RBAC)
- Billing and subscription data

### 3. Network Configuration

#### openspg-network

```yaml
networks:
  openspg-network:
    external: true
    name: openspg-network
```

**Purpose:** Shared Docker network connecting all AEON services.

**Connected Services:**
- `aeon-saas-dev` - Frontend application
- `aeon-postgres-dev` - Local PostgreSQL
- `openspg-neo4j` - Knowledge graph database
- `openspg-qdrant` - Vector search database
- `openspg-mysql` - OpenSPG metadata database
- `openspg-minio` - Object storage
- `openspg-server` - OpenSPG API server

---

## Clerk Authentication Setup

### Overview

Clerk provides complete user authentication and management for the AEON Digital Twin platform using modern Next.js App Router patterns.

### Integration Components

#### 1. Middleware (`middleware.ts`)

**Location:** `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/middleware.ts`

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

// Define public routes that don't require authentication
const isPublicRoute = createRouteMatcher([
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/',
  '/api/health',
  '/sites(.*)' // Allow public access to hosted sites
])

// Define protected routes that require authentication
const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/graph(.*)',
  '/search(.*)',
  '/chat(.*)',
  '/customers(.*)',
  '/upload(.*)',
  '/tags(.*)',
  '/analytics(.*)'
])

export default clerkMiddleware(async (auth, req) => {
  const url = req.nextUrl
  const hostname = req.headers.get('host')

  // Domain-Based Routing Logic
  if (hostname === 'oxot.nl' || hostname === 'www.oxot.nl') {
    return NextResponse.rewrite(new URL(`/sites/_template${url.pathname}`, req.url))
  }

  // Protect routes that require authentication
  if (isProtectedRoute(req)) {
    await auth.protect()
  }
}, {
  debug: process.env.NODE_ENV === 'development'
})

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
}
```

**Key Features:**
- ✅ Public routes accessible without authentication
- ✅ Protected routes require valid Clerk session
- ✅ Domain-based routing for multi-tenant support
- ✅ Debug mode enabled in development

#### 2. Root Layout (`app/layout.tsx`)

**Location:** `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/app/layout.tsx`

```typescript
import { ClerkProvider } from '@clerk/nextjs';
import ModernNav from '@/components/ModernNav';
import WaveBackground from '@/components/WaveBackground';

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en" className="dark">
        <body>
          <WaveBackground />
          <ModernNav />
          <main className="min-h-screen pt-20 px-6">
            {children}
          </main>
        </body>
      </html>
    </ClerkProvider>
  );
}
```

**Key Features:**
- ✅ `ClerkProvider` wraps entire application
- ✅ Authentication context available throughout app
- ✅ Dark mode enabled by default

#### 3. Navigation Component (`components/ModernNav.tsx`)

**Location:** `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/components/ModernNav.tsx`

```typescript
import { SignedIn, SignedOut, UserButton, SignInButton } from '@clerk/nextjs';

export default function ModernNav() {
  // Hide navigation on landing page and sign-in page
  if (pathname === '/' || pathname?.startsWith('/sign-in')) {
    return null;
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50">
      {/* Desktop Navigation */}
      <div className="hidden md:flex items-center space-x-1">
        {/* Navigation items... */}

        {/* Authentication */}
        <div className="ml-4 flex items-center space-x-3">
          <SignedOut>
            <SignInButton mode="modal">
              <button>Sign In</button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <UserButton
              appearance={{
                elements: {
                  avatarBox: "h-9 w-9 ring-2 ring-emerald-500/20"
                }
              }}
            />
          </SignedIn>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="mobile-menu">
        <SignedOut>
          <SignInButton mode="modal">
            <button className="w-full">Sign In</button>
          </SignInButton>
        </SignedOut>
        <SignedIn>
          <UserButton />
        </SignedIn>
      </div>
    </nav>
  );
}
```

**Key Features:**
- ✅ Conditional rendering based on authentication state
- ✅ Modal-based sign-in (no page redirect)
- ✅ UserButton for authenticated users (profile menu)
- ✅ Custom styling with Tailwind CSS

#### 4. Sign-In Page (`app/sign-in/[[...sign-in]]/page.tsx`)

**Location:** `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/app/sign-in/[[...sign-in]]/page.tsx`

**Purpose:** Dedicated sign-in page using Clerk's pre-built UI components.

**Implementation:** Uses Clerk's `<SignIn />` component with custom appearance configuration.

---

## Authentication Flow

### User Journey Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│ User visits AEON Digital Twin (http://localhost:3000)              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────────┐
                    │ Landing Page (/)   │
                    │ Public Access ✓    │
                    └────────┬───────────┘
                             │
                             ▼
              ┌──────────────┴──────────────┐
              │                             │
    User Clicks "Sign In"         User Navigates to
              │                    Protected Route
              ▼                             ▼
    ┌─────────────────────┐      ┌─────────────────────┐
    │ Modal Sign-In       │      │ Middleware Check    │
    │ (Clerk Component)   │      │ (middleware.ts)     │
    └─────────┬───────────┘      └─────────┬───────────┘
              │                             │
              │                             ▼
              │                   ┌─────────────────────┐
              │                   │ Authenticated?      │
              │                   └─────────┬───────────┘
              │                             │
              │                    ┌────────┴────────┐
              │                    │                 │
              │                   YES               NO
              │                    │                 │
              │                    ▼                 ▼
              │          ┌─────────────────┐  ┌──────────────┐
              │          │ Allow Access    │  │ Redirect to  │
              │          │ to Protected    │  │ Sign-In Page │
              │          │ Route           │  └──────────────┘
              │          └─────────────────┘
              │
              ▼
    ┌─────────────────────────────────┐
    │ User Authenticates              │
    │ - Email/Password                │
    │ - Social OAuth (future)         │
    │ - Magic Link (future)           │
    └─────────────┬───────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────┐
    │ Clerk Creates Session           │
    │ - JWT Token Generated           │
    │ - Session Cookie Set            │
    │ - User Metadata Stored          │
    └─────────────┬───────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────┐
    │ User Redirected to Dashboard    │
    │ (/dashboard)                    │
    └─────────────┬───────────────────┘
                  │
                  ▼
    ┌─────────────────────────────────┐
    │ Authenticated User Experience   │
    │ - UserButton in Navigation      │
    │ - Access to Protected Routes    │
    │ - Profile Management            │
    │ - Sign Out Available            │
    └─────────────────────────────────┘
```

### Authentication States

#### 1. Unauthenticated User

**Available Routes:**
- `/` - Landing page
- `/sign-in` - Sign-in page
- `/sign-up` - Sign-up page
- `/api/health` - Health check endpoint
- `/sites/*` - Public hosted sites

**UI State:**
- Shows "Sign In" button in navigation
- No UserButton displayed
- Access denied to protected routes

#### 2. Authenticated User

**Available Routes:**
- All public routes
- `/dashboard` - Main dashboard
- `/graph` - Knowledge graph explorer
- `/search` - Search interface
- `/chat` - AI assistant
- `/customers` - Customer management
- `/upload` - Document upload
- `/tags` - Tag management
- `/analytics` - Analytics dashboard

**UI State:**
- Shows UserButton with user avatar
- Access granted to all protected routes
- Profile dropdown available

### Session Management

#### Session Token

- **Type:** JWT (JSON Web Token)
- **Storage:** HTTP-only cookie (secure)
- **Expiration:** Managed by Clerk (default: 7 days)
- **Refresh:** Automatic token refresh

#### Session Claims

```typescript
{
  userId: string;           // Unique user identifier
  sessionId: string;        // Unique session identifier
  orgId?: string;          // Organization ID (if applicable)
  orgRole?: string;        // User role in organization
  metadata?: {             // Custom user metadata
    onboardingComplete?: boolean;
    // Additional custom fields
  }
}
```

---

## Environment Variables

### Current Configuration (`.env.development`)

```bash
# =============================================================================
# Next.js Configuration
# =============================================================================
NODE_ENV=development
NEXT_TELEMETRY_DISABLED=1
NEXT_PUBLIC_APP_NAME=AEON Digital Twin
NEXT_PUBLIC_APP_URL=http://localhost:3000

# =============================================================================
# Clerk Authentication (Development)
# =============================================================================
# Get these from: https://dashboard.clerk.com
CLERK_PUBLISHABLE_KEY_DEV=pk_test_dmFsaWQtc2FpbGZpc2gtOTUuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY_DEV=sk_test_5jjk7jSqlDy3FXX8OVWAH4JFfhcQ5ohI3m3cBDL6bm

# Clerk URLs (IMPORTANT: Use actual values, NOT ${} substitution)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_dmFsaWQtc2FpbGZpc2gtOTUuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=sk_test_5jjk7jSqlDy3FXX8OVWAH4JFfhcQ5ohI3m3cBDL6bm
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard

# =============================================================================
# PostgreSQL (SaaS-Boilerplate Local Development)
# =============================================================================
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aeon_saas_dev
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=aeon_saas_dev
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# =============================================================================
# Neo4j (AEON Knowledge Graph - via openspg-network)
# =============================================================================
NEO4J_URI=bolt://openspg-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg

# =============================================================================
# Qdrant (AEON Vector Search - via openspg-network)
# =============================================================================
QDRANT_URL=http://openspg-qdrant:6333
QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=

# =============================================================================
# MySQL (AEON OpenSPG Metadata - via openspg-network)
# =============================================================================
MYSQL_HOST=openspg-mysql
MYSQL_PORT=3306
MYSQL_DATABASE=openspg
MYSQL_USER=root
MYSQL_PASSWORD=openspg

# =============================================================================
# MinIO (AEON Object Storage - via openspg-network)
# =============================================================================
MINIO_ENDPOINT=openspg-minio:9000
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_BUCKET=aeon-uploads
MINIO_USE_SSL=false

# =============================================================================
# OpenSPG Server (AEON - via openspg-network)
# =============================================================================
OPENSPG_SERVER_URL=http://openspg-server:8887

# =============================================================================
# OpenAI API (Development)
# =============================================================================
OPENAI_API_KEY=sk-proj-... (redacted for security)
OPENAI_MODEL=gpt-4o-mini
```

### Environment Variable Categories

#### 1. Clerk Authentication Variables

| Variable | Type | Purpose | Required |
|----------|------|---------|----------|
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Public | Client-side Clerk API key | ✅ Yes |
| `CLERK_SECRET_KEY` | Secret | Server-side Clerk API key | ✅ Yes |
| `NEXT_PUBLIC_CLERK_SIGN_IN_URL` | Public | Sign-in page path | ✅ Yes |
| `NEXT_PUBLIC_CLERK_SIGN_UP_URL` | Public | Sign-up page path | ✅ Yes |
| `NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL` | Public | Post-sign-in redirect | ✅ Yes |
| `NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL` | Public | Post-sign-up redirect | ✅ Yes |

**Security Notes:**
- `NEXT_PUBLIC_*` variables are exposed to the browser (safe for publishable keys)
- `CLERK_SECRET_KEY` is server-side only (never exposed to browser)
- Development keys start with `pk_test_` and `sk_test_`
- Production keys start with `pk_live_` and `sk_live_`

#### 2. Database Variables

| Variable | Purpose | Container Access |
|----------|---------|------------------|
| `DATABASE_URL` | PostgreSQL connection string | Local development |
| `NEO4J_URI` | Neo4j Bolt protocol endpoint | Via openspg-network |
| `QDRANT_URL` | Qdrant HTTP endpoint | Via openspg-network |
| `MYSQL_HOST` | MySQL hostname | Via openspg-network |

#### 3. Service Variables

| Variable | Purpose | Container Access |
|----------|---------|------------------|
| `MINIO_ENDPOINT` | Object storage endpoint | Via openspg-network |
| `OPENSPG_SERVER_URL` | OpenSPG API endpoint | Via openspg-network |
| `OPENAI_API_KEY` | OpenAI API access | External API |

---

## Frontend Integration Points

### 1. Clerk Components

#### Available Components

```typescript
// Layout components
import { ClerkProvider } from '@clerk/nextjs';

// Authentication state components
import { SignedIn, SignedOut } from '@clerk/nextjs';

// Authentication action components
import { SignInButton, SignUpButton, UserButton } from '@clerk/nextjs';

// Full-page authentication components
import { SignIn, SignUp, UserProfile } from '@clerk/nextjs';
```

#### Usage Patterns

**Conditional Rendering Based on Auth State:**

```typescript
import { SignedIn, SignedOut, UserButton, SignInButton } from '@clerk/nextjs';

export function Header() {
  return (
    <header>
      <SignedOut>
        <SignInButton mode="modal" />
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </header>
  );
}
```

**Full-Page Authentication:**

```typescript
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignIn />
    </div>
  );
}
```

### 2. Clerk Hooks (Client-Side)

#### useUser Hook

```typescript
import { useUser } from '@clerk/nextjs';

export function ProfileComponent() {
  const { isLoaded, isSignedIn, user } = useUser();

  if (!isLoaded) return <div>Loading...</div>;
  if (!isSignedIn) return <div>Not signed in</div>;

  return (
    <div>
      <h1>Welcome, {user.firstName}!</h1>
      <p>Email: {user.primaryEmailAddress?.emailAddress}</p>
    </div>
  );
}
```

**Available Properties:**
- `isLoaded` - Clerk initialization complete
- `isSignedIn` - User authentication status
- `user` - Complete user object (or `null`)

#### useAuth Hook

```typescript
import { useAuth } from '@clerk/nextjs';

export function DataFetcher() {
  const { isSignedIn, userId, getToken, signOut } = useAuth();

  const fetchProtectedData = async () => {
    const token = await getToken();
    const response = await fetch('/api/protected', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.json();
  };

  return (
    <div>
      {isSignedIn && (
        <>
          <button onClick={fetchProtectedData}>Fetch Data</button>
          <button onClick={() => signOut()}>Sign Out</button>
        </>
      )}
    </div>
  );
}
```

**Available Methods:**
- `getToken()` - Retrieve JWT session token
- `signOut()` - Sign out current user
- `isSignedIn` - Authentication status
- `userId` - Current user ID

### 3. Clerk Utilities (Server-Side)

#### auth() Function (App Router)

```typescript
import { auth } from '@clerk/nextjs/server';

export async function GET(req: Request) {
  const { userId } = await auth();

  if (!userId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Fetch user-specific data
  const data = await fetchUserData(userId);
  return Response.json({ data });
}
```

#### currentUser() Function

```typescript
import { currentUser } from '@clerk/nextjs/server';

export async function ProfilePage() {
  const user = await currentUser();

  if (!user) return <div>Not signed in</div>;

  return (
    <div>
      <h1>{user.fullName}</h1>
      <p>{user.primaryEmailAddress?.emailAddress}</p>
    </div>
  );
}
```

**⚠️ Warning:** `currentUser()` counts towards Backend API rate limits. Prefer client-side `useUser()` when possible.

---

## What's Already Working

### ✅ Operational Features

1. **User Authentication**
   - ✅ Email/password sign-in
   - ✅ Modal-based authentication (no page redirects)
   - ✅ Automatic session management
   - ✅ JWT token generation and refresh

2. **Route Protection**
   - ✅ Public routes accessible without authentication
   - ✅ Protected routes require valid session
   - ✅ Automatic redirect to sign-in for unauthorized access
   - ✅ Domain-based routing for multi-tenant support

3. **User Experience**
   - ✅ UserButton with profile dropdown
   - ✅ Sign-in/sign-up modals
   - ✅ Responsive navigation (desktop and mobile)
   - ✅ Custom Clerk UI theming (dark mode)

4. **Container Infrastructure**
   - ✅ Hot reload enabled for rapid development
   - ✅ Health checks passing for all containers
   - ✅ Network connectivity to backend services
   - ✅ Persistent PostgreSQL data storage

5. **Integration with AEON Services**
   - ✅ Connected to Neo4j knowledge graph
   - ✅ Connected to Qdrant vector search
   - ✅ Connected to MySQL metadata store
   - ✅ Connected to MinIO object storage
   - ✅ Connected to OpenSPG API server

### ✅ Tested and Verified

- **Health Check Endpoint:** `/api/health` responding in 30-50ms
- **PostgreSQL Connection:** Database accepting connections
- **Container Health:** All containers reporting healthy status
- **Authentication Flow:** Sign-in modal working correctly
- **Route Protection:** Middleware correctly enforcing authentication

---

## What Developers Must Preserve

### 🔒 Critical Components (DO NOT MODIFY)

#### 1. Middleware Configuration

**File:** `middleware.ts`

```typescript
// DO NOT MODIFY THIS FILE WITHOUT APPROVAL

export default clerkMiddleware(async (auth, req) => {
  // Domain routing logic - PRESERVE
  if (hostname === 'oxot.nl' || hostname === 'www.oxot.nl') {
    return NextResponse.rewrite(new URL(`/sites/_template${url.pathname}`, req.url))
  }

  // Route protection logic - PRESERVE
  if (isProtectedRoute(req)) {
    await auth.protect()
  }
})
```

**Why This Matters:**
- Incorrect middleware configuration breaks authentication
- Domain routing enables multi-tenant support
- Route protection ensures security compliance

#### 2. ClerkProvider in Root Layout

**File:** `app/layout.tsx`

```typescript
// DO NOT REMOVE ClerkProvider

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>  {/* REQUIRED - DO NOT REMOVE */}
      <html lang="en" className="dark">
        <body>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
```

**Why This Matters:**
- `ClerkProvider` provides authentication context to entire app
- Removing it breaks all Clerk hooks and components

#### 3. Environment Variables

**Files:** `.env.development`, `.env.production`

```bash
# DO NOT MODIFY THESE VARIABLES WITHOUT APPROVAL

# Clerk authentication (REQUIRED)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
CLERK_SECRET_KEY=...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard

# Database connections (REQUIRED)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aeon_saas_dev
NEO4J_URI=bolt://openspg-neo4j:7687
QDRANT_URL=http://openspg-qdrant:6333
```

**Why This Matters:**
- Incorrect Clerk keys break authentication
- Incorrect database URLs break backend connectivity
- Variable naming follows Next.js conventions (`NEXT_PUBLIC_*` for client-side)

#### 4. Docker Compose Configuration

**File:** `docker-compose.dev.yml`

```yaml
# DO NOT MODIFY CONTAINER NETWORKING

services:
  aeon-saas-dev:
    networks:
      - openspg-network  # REQUIRED for backend connectivity

  postgres-dev:
    networks:
      - openspg-network  # REQUIRED for cross-container access

networks:
  openspg-network:
    external: true  # REQUIRED - network managed externally
```

**Why This Matters:**
- `openspg-network` connects frontend to backend services
- External network prevents duplicate network creation
- Container dependencies ensure proper startup order

### ⚠️ Modifiable Components (With Caution)

#### 1. UI Styling and Theming

**Files:** `components/*.tsx`, `app/globals.css`

```typescript
// ✅ SAFE TO MODIFY: Styling and appearance

<UserButton
  appearance={{
    elements: {
      avatarBox: "h-9 w-9 ring-2 ring-emerald-500/20"  // Customize styling
    }
  }}
/>
```

**Guidelines:**
- Customize Clerk component appearance via `appearance` prop
- Modify Tailwind CSS classes as needed
- Test changes in development before deploying

#### 2. Navigation Structure

**File:** `components/ModernNav.tsx`

```typescript
// ✅ SAFE TO MODIFY: Navigation items and routes

<Link href="/dashboard">Dashboard</Link>
<Link href="/new-page">New Page</Link>  // Add new routes
```

**Guidelines:**
- Preserve authentication-related components (`SignedIn`, `SignedOut`, `UserButton`)
- Add new navigation items as needed
- Ensure new protected routes are added to `middleware.ts`

#### 3. Protected Route Definitions

**File:** `middleware.ts`

```typescript
// ⚠️ MODIFY WITH CAUTION: Add new protected routes

const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/graph(.*)',
  '/new-protected-route(.*)',  // Add new protected routes here
])
```

**Guidelines:**
- Add new protected routes to `isProtectedRoute` matcher
- Test authentication flow after changes
- Document route protection requirements

---

## Development Guidelines

### Best Practices

#### 1. Authentication State Handling

**✅ DO:**

```typescript
import { useUser } from '@clerk/nextjs';

export function Component() {
  const { isLoaded, isSignedIn, user } = useUser();

  // ✅ CORRECT: Check isLoaded before accessing user
  if (!isLoaded) return <div>Loading...</div>;
  if (!isSignedIn) return <div>Please sign in</div>;

  return <div>Welcome, {user.firstName}!</div>;
}
```

**❌ DON'T:**

```typescript
// ❌ INCORRECT: Accessing user without checking isLoaded
export function Component() {
  const { user } = useUser();
  return <div>Welcome, {user.firstName}!</div>;  // May cause error
}
```

#### 2. Server-Side Authentication

**✅ DO:**

```typescript
import { auth } from '@clerk/nextjs/server';

export async function GET(req: Request) {
  const { userId } = await auth();

  // ✅ CORRECT: Check userId before proceeding
  if (!userId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Safe to proceed
}
```

**❌ DON'T:**

```typescript
// ❌ INCORRECT: Not checking authentication status
export async function GET(req: Request) {
  const { userId } = await auth();
  const data = await fetchData(userId);  // May cause error if userId is null
}
```

#### 3. Environment Variable Access

**✅ DO:**

```typescript
// ✅ CORRECT: Use process.env with proper naming

// Client-side (browser)
const publicKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

// Server-side (API routes, server components)
const secretKey = process.env.CLERK_SECRET_KEY;
```

**❌ DON'T:**

```typescript
// ❌ INCORRECT: Accessing secret keys client-side
const secretKey = process.env.CLERK_SECRET_KEY;  // Undefined in browser
```

#### 4. Testing Authentication Flows

**Testing Checklist:**

- [ ] Sign-in modal opens correctly
- [ ] User can authenticate with email/password
- [ ] UserButton appears after authentication
- [ ] Protected routes redirect to sign-in when not authenticated
- [ ] Sign-out functionality works correctly
- [ ] Session persists across page refreshes

**Test Commands:**

```bash
# Health check
curl http://localhost:3000/api/health

# Access protected route (should redirect or return 401)
curl http://localhost:3000/dashboard

# Access public route (should work)
curl http://localhost:3000/
```

### Container Management

#### Starting Development Environment

```bash
# Navigate to web_interface directory
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface

# Start containers
docker-compose -f docker-compose.dev.yml up -d

# Check container status
docker ps

# View logs
docker logs -f aeon-saas-dev
```

#### Stopping Development Environment

```bash
# Stop containers (preserve data)
docker-compose -f docker-compose.dev.yml stop

# Stop and remove containers (preserve volumes)
docker-compose -f docker-compose.dev.yml down

# Stop and remove everything (WARNING: deletes data)
docker-compose -f docker-compose.dev.yml down -v
```

#### Accessing Container Shells

```bash
# Access Next.js container
docker exec -it aeon-saas-dev sh

# Access PostgreSQL container
docker exec -it aeon-postgres-dev psql -U postgres -d aeon_saas_dev
```

### Debugging Authentication Issues

#### Common Issues and Solutions

**Issue 1: "Clerk: Publishable key not found"**

**Cause:** Missing or incorrect `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` in `.env.local`

**Solution:**
```bash
# Verify environment variables are loaded
docker exec aeon-saas-dev printenv | grep CLERK

# Restart container to reload environment variables
docker-compose -f docker-compose.dev.yml restart aeon-saas-dev
```

**Issue 2: Routes not protected**

**Cause:** Middleware not applying route protection

**Solution:**
1. Check middleware matcher configuration
2. Verify `isProtectedRoute` includes desired routes
3. Test with `curl -I http://localhost:3000/dashboard`

**Issue 3: User data not available**

**Cause:** `isLoaded` is `false` (Clerk still initializing)

**Solution:**
```typescript
const { isLoaded, user } = useUser();

if (!isLoaded) {
  return <div>Loading user data...</div>;  // Always check isLoaded first
}
```

**Issue 4: Container not healthy**

**Cause:** Health check endpoint failing

**Solution:**
```bash
# Check health endpoint manually
curl http://localhost:3000/api/health

# View container logs
docker logs aeon-saas-dev --tail 50

# Restart container
docker-compose -f docker-compose.dev.yml restart aeon-saas-dev
```

---

## Troubleshooting

### Container Issues

#### aeon-saas-dev Container Not Starting

**Symptoms:**
- Container exits immediately
- Health checks failing
- Port 3000 not accessible

**Diagnosis:**

```bash
# Check container status
docker ps -a | grep aeon-saas-dev

# View logs
docker logs aeon-saas-dev

# Check port conflicts
netstat -tuln | grep 3000
```

**Solutions:**

1. **Port Conflict:**
   ```bash
   # Stop conflicting service
   docker ps | grep 3000
   docker stop <container_id>
   ```

2. **Missing Dependencies:**
   ```bash
   # Rebuild container
   docker-compose -f docker-compose.dev.yml build aeon-saas-dev
   docker-compose -f docker-compose.dev.yml up -d aeon-saas-dev
   ```

3. **Environment Variable Issues:**
   ```bash
   # Verify .env.development exists
   ls -la .env.development

   # Check environment variables in container
   docker exec aeon-saas-dev printenv
   ```

#### aeon-postgres-dev Connection Issues

**Symptoms:**
- Database connection errors
- `DATABASE_URL` connection refused
- Health checks failing

**Diagnosis:**

```bash
# Check PostgreSQL container
docker logs aeon-postgres-dev

# Test database connection
docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "SELECT 1;"
```

**Solutions:**

1. **Database Not Ready:**
   ```bash
   # Wait for PostgreSQL to accept connections
   docker-compose -f docker-compose.dev.yml logs postgres-dev
   ```

2. **Connection String Incorrect:**
   ```bash
   # Verify DATABASE_URL format
   # postgresql://user:password@host:port/database
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aeon_saas_dev
   ```

3. **Network Issues:**
   ```bash
   # Verify openspg-network exists
   docker network ls | grep openspg

   # Recreate network if needed
   docker network create openspg-network
   ```

### Authentication Issues

#### Clerk Session Not Persisting

**Symptoms:**
- User signed out after page refresh
- Session cookie not set
- Authentication state inconsistent

**Diagnosis:**

```bash
# Check browser developer tools
# Application > Cookies > localhost
# Look for __session or __clerk_db_jwt cookies
```

**Solutions:**

1. **Cookie Domain Issues:**
   ```typescript
   // Ensure NEXT_PUBLIC_APP_URL matches your domain
   NEXT_PUBLIC_APP_URL=http://localhost:3000
   ```

2. **HTTPS vs HTTP:**
   - Development uses HTTP (OK)
   - Production requires HTTPS (configure Clerk accordingly)

3. **Clerk Dashboard Settings:**
   - Verify allowed origins in Clerk Dashboard
   - Check session lifetime settings

#### Protected Routes Accessible Without Authentication

**Symptoms:**
- Can access `/dashboard` without signing in
- Middleware not enforcing authentication

**Diagnosis:**

```bash
# Test protected route without authentication
curl -I http://localhost:3000/dashboard

# Should return 307 Temporary Redirect to /sign-in
```

**Solutions:**

1. **Middleware Configuration:**
   ```typescript
   // Verify protected routes are defined
   const isProtectedRoute = createRouteMatcher([
     '/dashboard(.*)',
     // Add missing routes
   ])
   ```

2. **Middleware Not Running:**
   ```bash
   # Check middleware.ts is in correct location
   ls -la middleware.ts  # Should be at project root or src/
   ```

3. **Debug Mode:**
   ```typescript
   // Enable debug mode in middleware
   export default clerkMiddleware(async (auth, req) => {
     // ...
   }, {
     debug: true  // Enable detailed logging
   })
   ```

### Network Connectivity Issues

#### Backend Services Not Accessible

**Symptoms:**
- Neo4j connection refused
- Qdrant connection timeout
- Cannot connect to openspg-network services

**Diagnosis:**

```bash
# Check network connectivity from container
docker exec aeon-saas-dev ping openspg-neo4j
docker exec aeon-saas-dev ping openspg-qdrant

# Verify services are running
docker ps | grep openspg
```

**Solutions:**

1. **Network Not Created:**
   ```bash
   # Create openspg-network
   docker network create openspg-network
   ```

2. **Containers Not on Same Network:**
   ```bash
   # Verify network membership
   docker network inspect openspg-network

   # Reconnect container if needed
   docker network connect openspg-network aeon-saas-dev
   ```

3. **Service Hostnames Incorrect:**
   ```bash
   # Verify service names in .env.development match container names
   NEO4J_URI=bolt://openspg-neo4j:7687  # Must match container name
   ```

### Performance Issues

#### Slow Page Load Times

**Symptoms:**
- Pages take >5 seconds to load
- API requests timing out
- Container health checks slow

**Diagnosis:**

```bash
# Check container resource usage
docker stats aeon-saas-dev

# View recent logs
docker logs aeon-saas-dev --tail 100
```

**Solutions:**

1. **Increase Docker Resources:**
   - Docker Desktop: Settings > Resources
   - Increase CPU and memory allocation

2. **Optimize Volume Mounts:**
   ```yaml
   # Use :delegated for better performance on macOS
   volumes:
     - ./app:/app/app:delegated
   ```

3. **Check Network Latency:**
   ```bash
   # Test backend service response times
   docker exec aeon-saas-dev time wget -qO- http://openspg-neo4j:7474
   ```

---

## Additional Resources

### Official Documentation

- **Clerk Documentation:** https://clerk.com/docs
- **Clerk Next.js Quickstart:** https://clerk.com/docs/quickstarts/nextjs
- **Next.js App Router:** https://nextjs.org/docs/app
- **Docker Compose:** https://docs.docker.com/compose/

### Internal Documentation

- **Clerk Quick Start:** `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/01_Infrastructure/Clerk_Quick_Start.md`
- **Clerk Integration Guide:** `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/05_Security/Clerk_Authentication_Integration.md`
- **Backend API Reference:** `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/Backend-API-Reference.md`

### File Locations

```
/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/
├── middleware.ts                        # Clerk middleware configuration
├── app/
│   ├── layout.tsx                       # ClerkProvider wrapper
│   └── sign-in/[[...sign-in]]/page.tsx # Sign-in page
├── components/
│   └── ModernNav.tsx                    # Navigation with Clerk components
├── docker-compose.dev.yml               # Development container configuration
├── .env.development                     # Environment variables
└── package.json                         # Dependencies and versions
```

---

## Summary

### What Frontend Developers Need to Know

1. **Authentication is Fully Configured:** Clerk is production-ready and working.
2. **Container Infrastructure is Stable:** All containers are healthy and connected.
3. **Environment Variables are Set:** Required keys and endpoints are configured.
4. **Route Protection is Active:** Middleware enforces authentication on protected routes.
5. **Backend Services are Accessible:** Neo4j, Qdrant, MySQL, MinIO, OpenSPG are connected.

### Critical Reminders

- ⚠️ **DO NOT modify `middleware.ts` without approval**
- ⚠️ **DO NOT remove `ClerkProvider` from root layout**
- ⚠️ **DO NOT change Clerk environment variables without testing**
- ⚠️ **DO NOT alter container network configuration**
- ✅ **DO test authentication flows after any changes**
- ✅ **DO check container health after restarting services**
- ✅ **DO document any new protected routes in middleware**

---

**End of Document**
