# AEON Digital Twin - Frontend UI Technical Specification

**Document Version:** 2.0.0
**Created:** 2025-01-04
**Project:** AEON Cybersecurity Intelligence Platform
**Framework:** Next.js 15 with App Router
**Purpose:** Complete UI architecture and component specification

---

## Executive Summary

This document provides a comprehensive technical specification for building the AEON Digital Twin frontend user interface. The application is a modern cybersecurity intelligence platform built with Next.js 15, featuring real-time threat visualization, AI-powered analysis, and multi-database integration. The UI implements a VulnCheck-inspired dark theme with OKLCH color space for optimal visual consistency.

**Key Technologies:**
- **Frontend Framework:** Next.js 15.0.3 (React 18.3.1, TypeScript 5.6.3)
- **Styling:** Tailwind CSS 3.4.14 with OKLCH color system
- **UI Libraries:** shadcn/ui, Tremor React, Lucide icons
- **AI Integration:** Vercel AI SDK 5.0.87 with streaming support
- **Visualization:** Neovis.js, Recharts, Chart.js
- **Backend Integration:** Neo4j, Qdrant, MySQL, MinIO, OpenSPG

---

## Table of Contents

1. [Framework Architecture](#framework-architecture)
2. [Project Structure](#project-structure)
3. [Page Specifications](#page-specifications)
4. [Component Library](#component-library)
5. [State Management](#state-management)
6. [Data Fetching Patterns](#data-fetching-patterns)
7. [Routing & Navigation](#routing--navigation)
8. [Performance Optimization](#performance-optimization)
9. [TypeScript Configuration](#typescript-configuration)
10. [Build Configuration](#build-configuration)
11. [Deployment Specification](#deployment-specification)

---

## 1. Framework Architecture

### 1.1 Next.js 15 App Router

The application uses Next.js 15's App Router with the following architectural patterns:

#### Server Components (Default)
All components are React Server Components by default, enabling:
- Zero-bundle JavaScript for non-interactive components
- Direct backend access without API routes
- Improved performance and SEO
- Automatic code splitting

#### Client Components (Opt-in)
Components marked with `'use client'` for:
- Interactive UI elements (buttons, forms, modals)
- Browser-only libraries (vis-network, chart.js)
- State management hooks (useState, useContext)
- Event handlers and effects

#### Streaming and Suspense
```typescript
// Streaming pattern for long-running queries
import { Suspense } from 'react';

export default async function ThreatPage() {
  return (
    <Suspense fallback={<ThreatSkeleton />}>
      <ThreatData />
    </Suspense>
  );
}
```

### 1.2 Technology Stack

#### Core Dependencies
```json
{
  "next": "15.0.3",
  "react": "18.3.1",
  "react-dom": "18.3.1",
  "typescript": "5.6.3"
}
```

#### Styling & UI
```json
{
  "tailwindcss": "3.4.14",
  "@tremor/react": "3.18.3",
  "@radix-ui/react-checkbox": "1.3.3",
  "lucide-react": "0.454.0",
  "framer-motion": "12.23.24",
  "class-variance-authority": "0.7.1",
  "clsx": "2.1.1",
  "tailwind-merge": "2.6.0"
}
```

#### AI & Backend Integration
```json
{
  "ai": "5.0.87",
  "@ai-sdk/openai": "2.0.62",
  "openai": "6.8.0",
  "neo4j-driver": "5.25.0",
  "@qdrant/js-client-rest": "1.15.1",
  "mysql2": "3.11.3",
  "@prisma/client": "5.22.0",
  "minio": "8.0.1"
}
```

#### Visualization
```json
{
  "neovis.js": "2.1.0",
  "recharts": "2.13.3",
  "chart.js": "4.5.1",
  "react-chartjs-2": "5.3.1"
}
```

---

## 2. Project Structure

### 2.1 Directory Organization

```
/web_interface/
├── app/                           # Next.js 15 App Router
│   ├── layout.tsx                 # Root layout
│   ├── page.tsx                   # Homepage (/)
│   ├── globals.css                # Global styles
│   │
│   ├── api/                       # API Route Handlers
│   │   ├── health/route.ts        # Health check endpoint
│   │   ├── search/route.ts        # Hybrid search (Neo4j + Qdrant)
│   │   ├── chat/route.ts          # AI chat with streaming
│   │   ├── customers/
│   │   │   ├── route.ts           # CRUD operations
│   │   │   └── [id]/route.ts      # Single customer
│   │   ├── tags/
│   │   │   ├── route.ts           # Tag management
│   │   │   └── assign/route.ts    # Assign tags to entities
│   │   ├── upload/route.ts        # File upload to MinIO
│   │   ├── analytics/
│   │   │   ├── metrics/route.ts   # Aggregated metrics
│   │   │   ├── timeseries/route.ts # Time-series data
│   │   │   └── export/route.ts    # Data export
│   │   ├── activity/
│   │   │   └── recent/route.ts    # Activity feed
│   │   ├── pipeline/
│   │   │   ├── process/route.ts   # Start processing
│   │   │   └── status/[jobId]/route.ts # Job status
│   │   └── observability/
│   │       ├── performance/route.ts
│   │       └── system/route.ts
│   │
│   ├── dashboard/page.tsx         # Main dashboard
│   ├── customers/page.tsx         # Customer management
│   ├── upload/page.tsx            # File upload interface
│   ├── tags/page.tsx              # Tag management
│   ├── graph/page.tsx             # Graph visualization
│   ├── chat/page.tsx              # AI chat interface
│   ├── search/page.tsx            # Search interface
│   └── analytics/page.tsx         # Analytics dashboard
│
├── components/                    # React Components
│   ├── ModernNav.tsx              # Navigation bar
│   ├── WaveBackground.tsx         # Animated background
│   │
│   ├── dashboard/                 # Dashboard components
│   │   ├── MetricsCard.tsx
│   │   ├── QuickActions.tsx
│   │   ├── RecentActivity.tsx
│   │   └── SystemHealth.tsx
│   │
│   ├── animations/                # Animation components
│   │   ├── AnimatedCard.tsx
│   │   └── AnimationExamples.tsx
│   │
│   ├── search/                    # Search components
│   │   ├── SearchBar.tsx
│   │   ├── SearchResults.tsx
│   │   └── SearchFilters.tsx
│   │
│   ├── chat/                      # Chat components
│   │   ├── ChatMessage.tsx
│   │   ├── ChatInput.tsx
│   │   └── SuggestedActions.tsx
│   │
│   ├── graph/                     # Graph visualization
│   │   ├── GraphVisualization.tsx
│   │   ├── GraphControls.tsx
│   │   └── GraphLegend.tsx
│   │
│   └── ui/                        # shadcn/ui components
│       ├── card.tsx
│       ├── button.tsx
│       ├── input.tsx
│       ├── badge.tsx
│       ├── label.tsx
│       ├── alert.tsx
│       ├── dialog.tsx
│       ├── dropdown-menu.tsx
│       ├── checkbox.tsx
│       └── wave-background.tsx
│
├── lib/                           # Utility Libraries
│   ├── utils.ts                   # General utilities
│   ├── design-tokens.ts           # Design system tokens
│   ├── neo4j-enhanced.ts          # Neo4j client
│   ├── qdrant-client.ts           # Qdrant client
│   ├── ai-orchestrator.ts         # AI orchestration
│   ├── hybrid-search.ts           # Hybrid search logic
│   │
│   └── observability/             # Monitoring utilities
│       ├── index.ts
│       ├── agent-tracker.ts
│       ├── component-tracker.ts
│       └── performance-monitor.ts
│
├── hooks/                         # Custom React Hooks
│   ├── use-debounce.ts
│   ├── use-search.ts
│   ├── use-chat.ts
│   └── use-graph-data.ts
│
├── types/                         # TypeScript Type Definitions
│   ├── api.ts
│   ├── graph.ts
│   ├── search.ts
│   └── chat.ts
│
├── public/                        # Static Assets
│   ├── images/
│   └── icons/
│
├── next.config.ts                 # Next.js configuration
├── tailwind.config.ts             # Tailwind CSS config
├── tsconfig.json                  # TypeScript config
├── package.json                   # Dependencies
└── Dockerfile                     # Docker production build
```

### 2.2 File Naming Conventions

- **Pages:** `page.tsx` (Next.js App Router convention)
- **Layouts:** `layout.tsx` (wraps page content)
- **Loading States:** `loading.tsx` (automatic suspense boundaries)
- **Error Boundaries:** `error.tsx` (automatic error handling)
- **Route Handlers:** `route.ts` (API endpoints)
- **Components:** PascalCase (e.g., `ModernNav.tsx`, `SearchBar.tsx`)
- **Utilities:** kebab-case (e.g., `neo4j-enhanced.ts`, `design-tokens.ts`)
- **Hooks:** camelCase with `use-` prefix (e.g., `use-debounce.ts`)

---

## 3. Page Specifications

### 3.1 Homepage (`app/page.tsx`)

**Purpose:** Landing page with cybersecurity intelligence overview

**Layout:**
- Wave background animation
- Navigation bar
- Hero section with key metrics
- Feature cards grid (6 cards)
- Quick actions section

**Components:**
```tsx
import { ModernNav } from '@/components/ModernNav';
import { WaveBackground } from '@/components/WaveBackground';
import { MetricsCard } from '@/components/dashboard/MetricsCard';
import { Shield, Database, Activity, Zap, FileText, Search } from 'lucide-react';

export default function HomePage() {
  return (
    <>
      <WaveBackground />
      <ModernNav />
      <main className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-slate-50 mb-4">
            AEON Digital Twin
          </h1>
          <p className="text-xl text-slate-300">
            Cybersecurity Intelligence Platform
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <MetricsCard
            icon={Shield}
            title="Vulnerabilities"
            value="12,458"
            trend="+2.3%"
            severity="critical"
          />
          {/* Additional metric cards */}
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
          {/* Feature cards */}
        </div>
      </main>
    </>
  );
}
```

**Data Sources:**
- Static content for initial load
- Client-side fetch for real-time metrics
- Server Components for SEO-critical content

### 3.2 Dashboard (`app/dashboard/page.tsx`)

**Purpose:** Main operational dashboard with real-time data

**Layout:**
- Metrics overview (4 cards)
- Time-series charts (2 charts)
- Recent activity feed
- Quick actions
- System health indicators

**Components:**
```tsx
import { Suspense } from 'react';
import { MetricsCard } from '@/components/dashboard/MetricsCard';
import { QuickActions } from '@/components/dashboard/QuickActions';
import { RecentActivity } from '@/components/dashboard/RecentActivity';
import { SystemHealth } from '@/components/dashboard/SystemHealth';

export default async function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <h1 className="text-3xl font-bold text-slate-50 mb-8">Dashboard</h1>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Suspense fallback={<MetricsSkeleton />}>
          <MetricsOverview />
        </Suspense>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Suspense fallback={<ChartSkeleton />}>
          <ThreatTrendChart />
        </Suspense>
        <Suspense fallback={<ChartSkeleton />}>
          <SeverityDistributionChart />
        </Suspense>
      </div>

      {/* Activity and Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Suspense fallback={<ActivitySkeleton />}>
            <RecentActivity />
          </Suspense>
        </div>
        <div>
          <QuickActions />
          <SystemHealth />
        </div>
      </div>
    </div>
  );
}
```

**Data Fetching:**
- Server Components fetch initial data
- Client Components poll for updates
- WebSocket for real-time notifications

### 3.3 Graph Visualization (`app/graph/page.tsx`)

**Purpose:** Interactive Neo4j knowledge graph visualization

**⚠️ CRITICAL:** This page requires special handling due to vis-network SSR incompatibility.

**Implementation:**
```tsx
'use client';

import dynamic from 'next/dynamic';
import { Loader2 } from 'lucide-react';

// Dynamic import with SSR disabled to prevent build errors
const GraphVisualization = dynamic(
  () => import('@/components/graph/GraphVisualization'),
  {
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-emerald-500" />
        <span className="ml-3 text-slate-300">Loading graph...</span>
      </div>
    ),
  }
);

export default function GraphPage() {
  return (
    <div className="h-screen flex flex-col">
      <div className="flex-1">
        <GraphVisualization />
      </div>
    </div>
  );
}
```

**GraphVisualization Component:**
```tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import { Network } from 'vis-network';
import { GraphControls } from './GraphControls';
import { GraphLegend } from './GraphLegend';

export default function GraphVisualization() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [network, setNetwork] = useState<Network | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Fetch graph data
    fetch('/api/graph/data')
      .then(res => res.json())
      .then(data => {
        const options = {
          // vis-network configuration
          nodes: {
            shape: 'dot',
            size: 16,
            font: { color: '#f8fafc', size: 14 },
            borderWidth: 2,
          },
          edges: {
            color: { color: '#10b981', opacity: 0.4 },
            width: 2,
          },
          physics: {
            stabilization: { iterations: 200 },
          },
        };

        const networkInstance = new Network(
          containerRef.current!,
          data,
          options
        );

        setNetwork(networkInstance);
      });

    return () => {
      network?.destroy();
    };
  }, []);

  return (
    <div className="relative w-full h-full">
      <div ref={containerRef} className="w-full h-full" />
      <GraphControls network={network} />
      <GraphLegend />
    </div>
  );
}
```

### 3.4 Search Interface (`app/search/page.tsx`)

**Purpose:** Hybrid search combining Neo4j graph and Qdrant vector search

**Layout:**
- Search bar with filters
- Search results grid
- Faceted filters sidebar
- Pagination

**Implementation:**
```tsx
'use client';

import { useState } from 'react';
import { SearchBar } from '@/components/search/SearchBar';
import { SearchResults } from '@/components/search/SearchResults';
import { SearchFilters } from '@/components/search/SearchFilters';
import { useSearch } from '@/hooks/use-search';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({});
  const { results, isLoading, error } = useSearch(query, filters);

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <h1 className="text-3xl font-bold text-slate-50 mb-8">Search</h1>

      <SearchBar
        value={query}
        onChange={setQuery}
        placeholder="Search vulnerabilities, threats, indicators..."
      />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mt-8">
        <div className="lg:col-span-1">
          <SearchFilters filters={filters} onChange={setFilters} />
        </div>

        <div className="lg:col-span-3">
          <SearchResults
            results={results}
            isLoading={isLoading}
            error={error}
          />
        </div>
      </div>
    </div>
  );
}
```

### 3.5 AI Chat Interface (`app/chat/page.tsx`)

**Purpose:** Conversational AI for threat intelligence queries

**Implementation:**
```tsx
'use client';

import { useChat } from 'ai/react';
import { ChatMessage } from '@/components/chat/ChatMessage';
import { ChatInput } from '@/components/chat/ChatInput';
import { SuggestedActions } from '@/components/chat/SuggestedActions';

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    streamMode: 'text',
  });

  return (
    <div className="max-w-4xl mx-auto px-6 py-8 h-screen flex flex-col">
      <h1 className="text-3xl font-bold text-slate-50 mb-8">AI Assistant</h1>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.length === 0 && <SuggestedActions />}
        {messages.map(message => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isLoading && <ChatMessage.Loading />}
      </div>

      {/* Input */}
      <ChatInput
        value={input}
        onChange={handleInputChange}
        onSubmit={handleSubmit}
        disabled={isLoading}
      />
    </div>
  );
}
```

### 3.6 Additional Pages

**Customers Page (`app/customers/page.tsx`):**
- Customer list with search and filters
- CRUD operations (Create, Read, Update, Delete)
- Customer details view
- Associated tags and metadata

**Upload Page (`app/upload/page.tsx`):**
- Drag-and-drop file upload
- Progress indicators
- File type validation
- MinIO integration for storage

**Tags Page (`app/tags/page.tsx`):**
- Tag management interface
- Tag creation and deletion
- Tag assignment to entities
- Tag hierarchy visualization

**Analytics Page (`app/analytics/page.tsx`):**
- Advanced analytics dashboard
- Customizable charts and metrics
- Export functionality
- Time-range selection

---

## 4. Component Library

### 4.1 Core UI Components (shadcn/ui)

#### Card Component
```tsx
// components/ui/card.tsx
import { cn } from '@/lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn(
        'modern-card',
        'bg-slate-800/80 backdrop-blur-md',
        'border border-emerald-500/20',
        'rounded-xl p-6',
        'transition-all duration-300',
        'hover:border-emerald-500/40',
        'hover:shadow-lg hover:shadow-emerald-500/10',
        'hover:-translate-y-1',
        className
      )}
      {...props}
    />
  );
}
```

#### Button Component
```tsx
// components/ui/button.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 rounded-lg font-semibold transition-all duration-300',
  {
    variants: {
      variant: {
        primary: 'bg-emerald-500 text-slate-950 hover:bg-emerald-400 hover:shadow-lg hover:shadow-emerald-500/30',
        secondary: 'bg-slate-800 text-slate-50 border border-emerald-500/30 hover:bg-slate-700 hover:border-emerald-500/50',
        ghost: 'text-slate-300 hover:bg-emerald-500/10 hover:text-emerald-400',
        danger: 'bg-red-500 text-slate-50 hover:bg-red-400',
      },
      size: {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-base',
        lg: 'px-6 py-3 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  );
}
```

#### Input Component
```tsx
// components/ui/input.tsx
import { cn } from '@/lib/utils';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export function Input({ className, ...props }: InputProps) {
  return (
    <input
      className={cn(
        'w-full px-4 py-2.5 rounded-lg',
        'bg-slate-800/50 border border-emerald-500/20',
        'text-slate-50 placeholder:text-slate-500',
        'focus:outline-none focus:border-emerald-500/60',
        'focus:ring-4 focus:ring-emerald-500/10',
        'transition-all duration-200',
        className
      )}
      {...props}
    />
  );
}
```

#### Badge Component
```tsx
// components/ui/badge.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold',
  {
    variants: {
      severity: {
        critical: 'bg-red-400/20 text-red-400 border border-red-400/30',
        high: 'bg-orange-400/20 text-orange-400 border border-orange-400/30',
        medium: 'bg-yellow-400/20 text-yellow-400 border border-yellow-400/30',
        low: 'bg-green-400/20 text-green-400 border border-green-400/30',
        info: 'bg-emerald-400/20 text-emerald-400 border border-emerald-400/30',
      },
    },
    defaultVariants: {
      severity: 'info',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, severity, children, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ severity }), className)} {...props}>
      {children}
    </span>
  );
}
```

### 4.2 Dashboard Components

#### MetricsCard Component
```tsx
// components/dashboard/MetricsCard.tsx
import { Card } from '@/components/ui/card';
import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MetricsCardProps {
  icon: LucideIcon;
  title: string;
  value: string | number;
  trend?: string;
  severity?: 'critical' | 'high' | 'medium' | 'low' | 'info';
}

export function MetricsCard({
  icon: Icon,
  title,
  value,
  trend,
  severity = 'info',
}: MetricsCardProps) {
  const iconColors = {
    critical: 'text-red-400',
    high: 'text-orange-400',
    medium: 'text-yellow-400',
    low: 'text-green-400',
    info: 'text-emerald-500',
  };

  return (
    <Card>
      <div className="flex items-start justify-between mb-4">
        <div className={cn('p-3 rounded-lg bg-slate-900/50', iconColors[severity])}>
          <Icon className="h-6 w-6" />
        </div>
        {trend && (
          <span className="text-sm text-slate-400">{trend}</span>
        )}
      </div>
      <h3 className="text-sm font-medium text-slate-400 mb-1">{title}</h3>
      <p className="text-3xl font-bold text-slate-50">{value}</p>
    </Card>
  );
}
```

### 4.3 Animation Components

#### WaveBackground Component
```tsx
// components/WaveBackground.tsx
'use client';

export function WaveBackground() {
  return (
    <div className="fixed inset-0 z-0 overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="absolute inset-0">
        <div
          className="absolute w-full h-full opacity-30"
          style={{
            background: 'radial-gradient(circle at 20% 50%, oklch(69.6% 0.17 162.48 / 0.15), transparent 50%)',
            animation: 'wave 20s ease-in-out infinite',
          }}
        />
        <div
          className="absolute w-full h-full opacity-30"
          style={{
            background: 'radial-gradient(circle at 80% 50%, oklch(69.6% 0.17 162.48 / 0.1), transparent 50%)',
            animation: 'wave 25s ease-in-out infinite reverse',
          }}
        />
      </div>
    </div>
  );
}
```

---

## 5. State Management

### 5.1 Client-Side State (React Hooks)

For client-side interactivity, use React hooks:

```tsx
import { useState, useEffect } from 'react';

// Local component state
function SearchBar() {
  const [query, setQuery] = useState('');

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
    />
  );
}
```

### 5.2 Server State (React Query Pattern)

For data fetching and caching:

```tsx
// hooks/use-search.ts
import { useState, useEffect } from 'react';

export function useSearch(query: string, filters: any) {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!query) return;

    setIsLoading(true);
    fetch('/api/search', {
      method: 'POST',
      body: JSON.stringify({ query, filters }),
    })
      .then(res => res.json())
      .then(data => {
        setResults(data.results);
        setIsLoading(false);
      })
      .catch(err => {
        setError(err);
        setIsLoading(false);
      });
  }, [query, filters]);

  return { results, isLoading, error };
}
```

### 5.3 Global State (Context API)

For app-wide state (theme, user preferences):

```tsx
// contexts/ThemeContext.tsx
'use client';

import { createContext, useContext, useState, ReactNode } from 'react';

type Theme = 'dark' | 'light';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('dark');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```

---

## 6. Data Fetching Patterns

### 6.1 Server Components (Async/Await)

```tsx
// Server Component - automatic data fetching
async function DashboardMetrics() {
  const metrics = await fetch('http://localhost:3000/api/metrics', {
    cache: 'no-store', // Always fetch fresh data
  }).then(res => res.json());

  return (
    <div>
      {metrics.map(metric => (
        <MetricsCard key={metric.id} {...metric} />
      ))}
    </div>
  );
}
```

### 6.2 Client Components (useEffect)

```tsx
'use client';

function RealtimeMetrics() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('/api/metrics')
        .then(res => res.json())
        .then(setData);
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return <MetricsDisplay data={data} />;
}
```

### 6.3 Streaming with AI SDK

```tsx
'use client';

import { useChat } from 'ai/react';

export function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
    streamMode: 'text',
  });

  return (
    <div>
      {messages.map(msg => (
        <div key={msg.id}>{msg.content}</div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  );
}
```

---

## 7. Routing & Navigation

### 7.1 File-Based Routing

Next.js 15 uses the `app/` directory for routing:

```
app/
├── page.tsx                 → /
├── dashboard/page.tsx       → /dashboard
├── search/page.tsx          → /search
├── graph/page.tsx           → /graph
├── chat/page.tsx            → /chat
└── api/
    └── health/route.ts      → /api/health
```

### 7.2 Navigation Component

```tsx
// components/ModernNav.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Activity, Search, MessageSquare, Network } from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: Activity },
  { href: '/search', label: 'Search', icon: Search },
  { href: '/chat', label: 'Chat', icon: MessageSquare },
  { href: '/graph', label: 'Graph', icon: Network },
];

export function ModernNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-emerald-500/20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-xl font-bold text-slate-50">
            AEON Digital Twin
          </Link>

          <div className="flex items-center space-x-1">
            {navItems.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className={cn(
                  'flex items-center space-x-2 px-4 py-2 rounded-lg',
                  'text-slate-300 hover:text-emerald-400',
                  'hover:bg-emerald-500/10 transition-all duration-200',
                  pathname === href && 'text-emerald-400 bg-emerald-500/10'
                )}
              >
                <Icon className="h-5 w-5" />
                <span className="font-medium">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}
```

### 7.3 Programmatic Navigation

```tsx
'use client';

import { useRouter } from 'next/navigation';

function SearchForm() {
  const router = useRouter();

  const handleSubmit = (query: string) => {
    router.push(`/search?q=${encodeURIComponent(query)}`);
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

---

## 8. Performance Optimization

### 8.1 Code Splitting

Automatic route-based code splitting with Next.js:

```tsx
// Each page is automatically code-split
import DashboardPage from './app/dashboard/page';
import SearchPage from './app/search/page';
```

### 8.2 Dynamic Imports

For heavy client-side libraries:

```tsx
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  ssr: false,
  loading: () => <Skeleton />,
});
```

### 8.3 Image Optimization

```tsx
import Image from 'next/image';

<Image
  src="/threat-map.png"
  alt="Threat Map"
  width={800}
  height={600}
  priority={true} // Above-the-fold images
/>
```

### 8.4 Font Optimization

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

---

## 9. TypeScript Configuration

### 9.1 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### 9.2 Type Definitions

```typescript
// types/api.ts
export interface SearchResult {
  id: string;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  timestamp: string;
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
  meta?: {
    total: number;
    page: number;
    perPage: number;
  };
}
```

---

## 10. Build Configuration

### 10.1 next.config.ts

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,

  webpack: (config) => {
    config.externals = [...config.externals, 'vis-network', 'vis-data'];
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      net: false,
      tls: false,
    };
    return config;
  },

  images: {
    remotePatterns: [
      { protocol: 'http', hostname: 'localhost' },
      { protocol: 'http', hostname: 'openspg-minio' },
    ],
  },

  experimental: {
    serverActions: {
      allowedOrigins: ['localhost:3000', 'aeon-ui:3000'],
    },
  },
};

export default nextConfig;
```

### 10.2 Build Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  }
}
```

---

## 11. Deployment Specification

### 11.1 Docker Production Build

```dockerfile
# Multi-stage Dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV OPENAI_API_KEY="sk-dummy-key"
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

### 11.2 Environment Variables

```bash
# Production .env
OPENAI_API_KEY=sk-prod-key
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=secure-password
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=secure-key
DATABASE_URL=mysql://user:pass@mysql:3306/aeon_db
MINIO_ENDPOINT=minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=secure-secret
MINIO_USE_SSL=false
OPENSPG_URL=http://openspg:8887
NEXT_PUBLIC_APP_NAME=AEON Digital Twin
```

---

## Appendix A: Component Index

### Core UI Components (30+ components)
- Card, Button, Input, Badge, Label
- Alert, Dialog, Dropdown Menu, Checkbox
- Wave Background

### Dashboard Components
- MetricsCard, QuickActions, RecentActivity, SystemHealth

### Search Components
- SearchBar, SearchResults, SearchFilters

### Chat Components
- ChatMessage, ChatInput, SuggestedActions

### Graph Components
- GraphVisualization, GraphControls, GraphLegend

### Animation Components
- AnimatedCard, AnimationExamples

---

**Document Status:** COMPLETE
**Last Updated:** 2025-01-04
**Version:** 2.0.0
**Target Directory:** `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Front End UI Builder`
