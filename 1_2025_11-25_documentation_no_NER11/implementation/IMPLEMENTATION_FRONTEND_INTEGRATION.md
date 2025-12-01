# WAVE 4 Implementation: Frontend Integration Architecture

**Document**: IMPLEMENTATION_FRONTEND_INTEGRATION.md
**Created**: 2025-11-25 22:30:00 UTC
**Version**: v1.0.0
**Status**: ACTIVE

## Executive Summary

This document defines the Next.js frontend architecture for WAVE 4, implementing a modern, responsive, and performant web interface for knowledge graph exploration, threat intelligence analysis, and infrastructure monitoring. The frontend leverages React 18 with TypeScript, TailwindCSS, and Apollo Client for seamless GraphQL integration.

**Target**: 900 lines of detailed frontend specifications and implementation patterns.

---

## Table of Contents

1. [Frontend Architecture](#frontend-architecture)
2. [Project Structure](#project-structure)
3. [Component Design](#component-design)
4. [State Management](#state-management)
5. [API Integration](#api-integration)
6. [UI/UX Implementation](#uiux-implementation)
7. [Performance Optimization](#performance-optimization)
8. [Testing Strategy](#testing-strategy)
9. [Deployment](#deployment)

---

## Frontend Architecture

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Next.js | 14+ | React framework with SSR |
| Language | TypeScript | 5.0+ | Type safety |
| UI Library | React | 18+ | Component library |
| Styling | TailwindCSS | 3.4+ | Utility-first CSS |
| GraphQL Client | Apollo Client | 3.8+ | GraphQL data fetching |
| State Management | Zustand | 4.4+ | Lightweight state store |
| Forms | React Hook Form | 7.5+ | Form management |
| Data Visualization | D3.js/Visx | Latest | Graph visualization |
| Charts | Recharts | 2.10+ | Chart library |
| Icons | Heroicons | 2.0+ | Icon library |
| Testing | Vitest/Testing Library | Latest | Test framework |
| Build Tool | Turborepo | Latest | Monorepo management |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│            Next.js Application (14.0+)                  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Pages & Layouts (App Router)               │ │
│  │  ┌──────────────┐  ┌──────────────┐               │ │
│  │  │ Dashboard    │  │ Knowledge    │  ...          │ │
│  │  │ Layout       │  │ Graph View   │               │ │
│  │  └──────────────┘  └──────────────┘               │ │
│  └────────────────────────────────────────────────────┘ │
│                            ↓                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │           React Components (Reusable)             │ │
│  │  ┌──────────────┐  ┌──────────────┐               │ │
│  │  │ KnowledgeGraph │ │ ThreatAnalysis │            │ │
│  │  │ Visualizer   │  │ Panel        │  ...          │ │
│  │  └──────────────┘  └──────────────┘               │ │
│  └────────────────────────────────────────────────────┘ │
│                            ↓                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │        Apollo Client (GraphQL Integration)         │ │
│  │              ↓ REST API Client                     │ │
│  └────────────────────────────────────────────────────┘ │
│                            ↓                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │      Backend API (FastAPI - Port 8000)            │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

### Directory Layout

```
frontend/
├── app/
│   ├── layout.tsx                   # Root layout
│   ├── page.tsx                     # Home page
│   ├── dashboard/
│   │   ├── layout.tsx
│   │   ├── page.tsx                 # Dashboard main
│   │   ├── knowledge-graph/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── threat-intelligence/
│   │   │   ├── page.tsx
│   │   │   ├── actors/
│   │   │   ├── campaigns/
│   │   │   ├── indicators/
│   │   │   └── layout.tsx
│   │   ├── infrastructure/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/
│   │   │   └── layout.tsx
│   │   ├── analytics/
│   │   │   ├── page.tsx
│   │   │   └── layout.tsx
│   │   └── admin/
│   │       ├── page.tsx
│   │       └── users/
│   │
│   ├── auth/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── callback/
│   │       └── page.tsx
│   │
│   └── api/
│       └── auth/
│           └── [...nextauth].ts
│
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Footer.tsx
│   │   └── Navigation.tsx
│   │
│   ├── dashboard/
│   │   ├── OverviewCard.tsx
│   │   ├── MetricsPanel.tsx
│   │   ├── RecentActivity.tsx
│   │   └── QuickActions.tsx
│   │
│   ├── knowledge-graph/
│   │   ├── GraphVisualization.tsx
│   │   ├── NodeDetails.tsx
│   │   ├── RelationshipPanel.tsx
│   │   ├── SearchBar.tsx
│   │   └── PathFinder.tsx
│   │
│   ├── threat-intel/
│   │   ├── ThreatActorCard.tsx
│   │   ├── CampaignTimeline.tsx
│   │   ├── IndicatorList.tsx
│   │   ├── ThreatMap.tsx
│   │   └── RiskMatrix.tsx
│   │
│   ├── common/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   ├── Table.tsx
│   │   ├── Pagination.tsx
│   │   ├── Loading.tsx
│   │   ├── ErrorBoundary.tsx
│   │   └── Toast.tsx
│   │
│   └── icons/
│       └── CustomIcons.tsx
│
├── hooks/
│   ├── useApi.ts                    # API hook
│   ├── useGraphQL.ts                # GraphQL hook
│   ├── useAuth.ts                   # Authentication hook
│   ├── usePagination.ts             # Pagination hook
│   ├── useLocalStorage.ts           # Local storage hook
│   └── useDebounce.ts               # Debounce hook
│
├── services/
│   ├── api.ts                       # API client
│   ├── graphql-client.ts            # GraphQL client setup
│   ├── auth.ts                      # Auth service
│   ├── storage.ts                   # Local storage service
│   └── analytics.ts                 # Analytics service
│
├── store/
│   ├── index.ts                     # Zustand store
│   ├── slices/
│   │   ├── auth.ts
│   │   ├── graph.ts
│   │   ├── threat-intel.ts
│   │   ├── ui.ts
│   │   └── cache.ts
│   └── middleware/
│       └── persistence.ts
│
├── types/
│   ├── index.ts                     # Global types
│   ├── api.ts                       # API types
│   ├── domain.ts                    # Domain types
│   ├── graph.ts                     # Graph types
│   └── threat.ts                    # Threat intel types
│
├── utils/
│   ├── cn.ts                        # Class name utility
│   ├── format.ts                    # Formatting utilities
│   ├── date.ts                      # Date utilities
│   ├── validation.ts                # Validation utilities
│   └── constants.ts                 # Application constants
│
├── styles/
│   ├── globals.css                  # Global styles
│   ├── variables.css                # CSS variables
│   └── animations.css               # Animation definitions
│
├── public/
│   ├── images/
│   ├── fonts/
│   └── icons/
│
├── __tests__/
│   ├── unit/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── services/
│   ├── integration/
│   │   ├── pages/
│   │   ├── components/
│   │   └── flows/
│   └── e2e/
│       └── scenarios/
│
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
├── .env.local.example
└── README.md
```

---

## Component Design

### Core Component Architecture

```typescript
// components/common/Card.tsx

import React, { ReactNode } from 'react';
import { cn } from '@/utils/cn';

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  onClick,
  hoverable = false,
}) => {
  return (
    <div
      className={cn(
        'rounded-lg border border-gray-200 bg-white p-6 shadow-sm',
        'dark:border-gray-800 dark:bg-gray-950',
        hoverable && 'cursor-pointer transition-all hover:shadow-md',
        className
      )}
      onClick={onClick}
    >
      {children}
    </div>
  );
};

// components/knowledge-graph/GraphVisualization.tsx

import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { useGraphStore } from '@/store/slices/graph';

interface GraphVisualizationProps {
  nodeId?: string;
  depth?: number;
  interactive?: boolean;
}

export const GraphVisualization: React.FC<GraphVisualizationProps> = ({
  nodeId,
  depth = 2,
  interactive = true,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const { nodes, edges, fetchSubgraph } = useGraphStore();

  useEffect(() => {
    if (!nodeId) return;

    const loadGraph = async () => {
      setLoading(true);
      await fetchSubgraph(nodeId, depth);
      setLoading(false);
    };

    loadGraph();
  }, [nodeId, depth, fetchSubgraph]);

  useEffect(() => {
    if (!containerRef.current || nodes.length === 0) return;

    // D3 visualization setup
    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    const svg = d3.select(containerRef.current)
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    // Create force simulation
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(edges).id((d: any) => d.id))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2));

    // Add links
    const link = svg.append('g')
      .selectAll('line')
      .data(edges)
      .enter()
      .append('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6);

    // Add nodes
    const node = svg.append('g')
      .selectAll('circle')
      .data(nodes)
      .enter()
      .append('circle')
      .attr('r', 5)
      .attr('fill', (d: any) => getNodeColor(d.type))
      .call(interactive ? drag(simulation) : () => {});

    // Add labels
    const labels = svg.append('g')
      .selectAll('text')
      .data(nodes)
      .enter()
      .append('text')
      .text((d: any) => d.label)
      .attr('font-size', '12px')
      .attr('text-anchor', 'middle');

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      labels
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y - 10);
    });

    return () => {
      svg.remove();
      simulation.stop();
    };
  }, [nodes, edges, interactive]);

  if (loading) {
    return <div className="flex items-center justify-center h-full">Loading graph...</div>;
  }

  return <div ref={containerRef} className="w-full h-full" />;
};

function drag(simulation: any) {
  function dragstarted(event: any, d: any) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event: any, d: any) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragended(event: any, d: any) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  return d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended);
}

function getNodeColor(type: string): string {
  const colors: Record<string, string> = {
    ThreatActor: '#ef4444',
    Infrastructure: '#3b82f6',
    CVE: '#f59e0b',
    Campaign: '#8b5cf6',
    DetectionSignature: '#10b981',
  };
  return colors[type] || '#6b7280';
}
```

### Form Components with React Hook Form

```typescript
// components/forms/SearchForm.tsx

import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/common/Button';

const searchSchema = z.object({
  query: z.string().min(1, 'Search query required').max(100),
  searchType: z.enum(['text', 'graph', 'threat']),
  limit: z.number().min(1).max(100),
});

type SearchFormData = z.infer<typeof searchSchema>;

interface SearchFormProps {
  onSubmit: (data: SearchFormData) => Promise<void>;
  isLoading?: boolean;
}

export const SearchForm: React.FC<SearchFormProps> = ({
  onSubmit,
  isLoading = false,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SearchFormData>({
    resolver: zodResolver(searchSchema),
    defaultValues: {
      query: '',
      searchType: 'text',
      limit: 20,
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Search Query
        </label>
        <input
          {...register('query')}
          type="text"
          placeholder="Enter search term..."
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
        {errors.query && (
          <p className="mt-1 text-sm text-red-600">{errors.query.message}</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Search Type
          </label>
          <select
            {...register('searchType')}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          >
            <option value="text">Text Search</option>
            <option value="graph">Graph Search</option>
            <option value="threat">Threat Search</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Results Limit
          </label>
          <input
            {...register('limit', { valueAsNumber: true })}
            type="number"
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          />
        </div>
      </div>

      <Button type="submit" disabled={isLoading} className="w-full">
        {isLoading ? 'Searching...' : 'Search'}
      </Button>
    </form>
  );
};
```

---

## State Management

### Zustand Store Implementation

```typescript
// store/index.ts

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { authSlice } from './slices/auth';
import { graphSlice } from './slices/graph';
import { threatIntelSlice } from './slices/threat-intel';
import { uiSlice } from './slices/ui';
import { cacheSlice } from './slices/cache';

export const useStore = create(
  devtools(
    persist(
      (...args) => ({
        ...authSlice(...args),
        ...graphSlice(...args),
        ...threatIntelSlice(...args),
        ...uiSlice(...args),
        ...cacheSlice(...args),
      }),
      {
        name: 'app-store',
        partialize: (state) => ({
          auth: state.auth,
          cache: state.cache,
        }),
      }
    ),
    { name: 'App Store' }
  )
);

// store/slices/graph.ts

import { StateCreator } from 'zustand';

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties: Record<string, any>;
}

export interface GraphEdge {
  source: string;
  target: string;
  type: string;
  properties: Record<string, any>;
}

export interface GraphState {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedNodeId: string | null;
  fetchSubgraph: (nodeId: string, depth: number) => Promise<void>;
  setSelectedNode: (nodeId: string | null) => void;
  clearGraph: () => void;
}

export const graphSlice: StateCreator<GraphState> = (set, get) => ({
  nodes: [],
  edges: [],
  selectedNodeId: null,

  fetchSubgraph: async (nodeId: string, depth: number) => {
    try {
      const response = await fetch(
        `/api/v1/knowledge-graph/nodes/${nodeId}/relationships?depth=${depth}`
      );
      const data = await response.json();

      set({
        nodes: data.nodes,
        edges: data.edges,
      });
    } catch (error) {
      console.error('Failed to fetch subgraph:', error);
    }
  },

  setSelectedNode: (nodeId: string | null) => {
    set({ selectedNodeId: nodeId });
  },

  clearGraph: () => {
    set({ nodes: [], edges: [], selectedNodeId: null });
  },
});

// store/slices/auth.ts

export interface AuthState {
  token: string | null;
  user: any | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: any) => void;
}

export const authSlice: StateCreator<AuthState> = (set) => ({
  token: null,
  user: null,
  isAuthenticated: false,

  login: async (email: string, password: string) => {
    try {
      const response = await fetch('/api/v1/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const { token, user } = await response.json();

      localStorage.setItem('token', token);
      set({
        token,
        user,
        isAuthenticated: true,
      });
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    set({
      token: null,
      user: null,
      isAuthenticated: false,
    });
  },

  setUser: (user: any) => {
    set({ user, isAuthenticated: true });
  },
});
```

---

## API Integration

### GraphQL Client Setup

```typescript
// services/graphql-client.ts

import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { getMainDefinition } from '@apollo/client/utilities';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';

const httpLink = new HttpLink({
  uri: `${process.env.NEXT_PUBLIC_API_URL}/graphql`,
  credentials: 'include',
  headers: {
    Authorization: `Bearer ${localStorage.getItem('token')}`,
  },
});

const wsLink = new GraphQLWsLink(
  createClient({
    url: `${process.env.NEXT_PUBLIC_WS_URL}/graphql`,
    connectionParams: {
      authToken: localStorage.getItem('token'),
    },
  })
);

const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink
);

export const apolloClient = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
    },
  },
});
```

### REST API Client with Hooks

```typescript
// hooks/useApi.ts

import { useState, useCallback } from 'react';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
}

export function useApi<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const request = useCallback(
    async (options: RequestOptions = {}) => {
      setLoading(true);
      setError(null);

      try {
        const token = localStorage.getItem('token');
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}${url}`,
          {
            method: options.method || 'GET',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
              ...options.headers,
            },
            body: options.body ? JSON.stringify(options.body) : undefined,
          }
        );

        if (!response.ok) {
          throw new Error(`API error: ${response.statusText}`);
        }

        const result = await response.json();
        setData(result);
        return result;
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        setError(error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [url]
  );

  return { data, loading, error, request };
}
```

---

## UI/UX Implementation

### Responsive Design with TailwindCSS

```typescript
// components/dashboard/DashboardLayout.tsx

import React, { ReactNode } from 'react';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';

interface DashboardLayoutProps {
  children: ReactNode;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
}) => {
  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-950">
      {/* Sidebar - Hidden on mobile, visible on md+ */}
      <div className="hidden md:flex md:w-64 md:flex-col">
        <Sidebar />
      </div>

      {/* Main content area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />

        {/* Page content - Responsive padding */}
        <main className="flex-1 overflow-auto">
          <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
```

### Dark Mode Support

```typescript
// app/layout.tsx

'use client';

import { ThemeProvider } from 'next-themes';
import React, { ReactNode } from 'react';

interface RootLayoutProps {
  children: ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}

// components/layout/ThemeToggle.tsx

import { useTheme } from 'next-themes';
import { MoonIcon, SunIcon } from '@heroicons/react/24/outline';

export const ThemeToggle = () => {
  const { theme, setTheme } = useTheme();

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="rounded-lg p-2 hover:bg-gray-100 dark:hover:bg-gray-800"
    >
      {theme === 'dark' ? (
        <SunIcon className="h-5 w-5" />
      ) : (
        <MoonIcon className="h-5 w-5" />
      )}
    </button>
  );
};
```

---

## Performance Optimization

### Code Splitting and Lazy Loading

```typescript
// components/knowledge-graph/index.tsx

import dynamic from 'next/dynamic';

const GraphVisualization = dynamic(
  () => import('./GraphVisualization').then((mod) => mod.GraphVisualization),
  {
    loading: () => <div>Loading visualization...</div>,
    ssr: false,
  }
);

// Usage in page
export default function KnowledgeGraphPage() {
  return <GraphVisualization nodeId="node-123" />;
}
```

### Image Optimization

```typescript
// components/common/OptimizedImage.tsx

import Image from 'next/image';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
}

export const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  width = 400,
  height = 300,
}) => {
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      placeholder="blur"
      blurDataURL="data:image/webp;base64,..."
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      priority={false}
    />
  );
};
```

### Performance Monitoring

```typescript
// utils/performance.ts

import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

export function reportWebVitals(metric: any) {
  if (process.env.NODE_ENV === 'production') {
    // Send to analytics service
    console.log(metric);

    if ('name' in metric) {
      const body = JSON.stringify(metric);
      navigator.sendBeacon('/api/metrics', body);
    }
  }
}

// app/layout.tsx
export function reportWebVitals(metric: any) {
  reportWebVitals(metric);
}
```

---

## Testing Strategy

### Component Testing with Vitest

```typescript
// __tests__/unit/components/Card.test.tsx

import { render, screen } from '@testing-library/react';
import { Card } from '@/components/common/Card';
import { describe, it, expect } from 'vitest';

describe('Card Component', () => {
  it('renders children correctly', () => {
    render(<Card>Test Content</Card>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('applies custom className', () => {
    const { container } = render(
      <Card className="custom-class">Content</Card>
    );
    const card = container.querySelector('.custom-class');
    expect(card).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Card onClick={handleClick}>Click me</Card>);
    screen.getByText('Click me').click();
    expect(handleClick).toHaveBeenCalled();
  });
});
```

### Integration Testing

```typescript
// __tests__/integration/pages/dashboard.test.tsx

import { render, screen, waitFor } from '@testing-library/react';
import DashboardPage from '@/app/dashboard/page';
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('Dashboard Page', () => {
  beforeEach(() => {
    vi.mock('@/services/api', () => ({
      fetchDashboardData: vi.fn().mockResolvedValue({
        nodes: 100,
        relationships: 500,
      }),
    }));
  });

  it('displays dashboard overview', async () => {
    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText(/nodes/i)).toBeInTheDocument();
    });
  });
});
```

---

## Deployment

### Next.js Configuration

```typescript
// next.config.js

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  compress: true,
  poweredByHeader: false,
  swcMinify: true,

  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },

  headers: async () => [
    {
      source: '/(.*)',
      headers: [
        {
          key: 'X-Content-Type-Options',
          value: 'nosniff',
        },
        {
          key: 'X-Frame-Options',
          value: 'DENY',
        },
        {
          key: 'X-XSS-Protection',
          value: '1; mode=block',
        },
      ],
    },
  ],

  rewrites: async () => ({
    beforeFiles: [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
    ],
  }),

  redirects: async () => [
    {
      source: '/',
      destination: '/dashboard',
      permanent: false,
    },
  ],
};

module.exports = nextConfig;
```

### Docker Deployment

```dockerfile
# Dockerfile

FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

---

## Summary

This Frontend Integration implementation provides:

✅ **Modern Next.js Architecture** with App Router
✅ **Component-Driven Development** with reusable components
✅ **State Management** with Zustand
✅ **API Integration** with REST and GraphQL
✅ **Responsive Design** with TailwindCSS
✅ **Performance Optimization** with code splitting and lazy loading
✅ **Comprehensive Testing** with Vitest
✅ **Production-Ready Deployment** configurations

**Line Count**: ~900 lines of specifications and code patterns

---

**Document Version**: v1.0.0
**Last Updated**: 2025-11-25
**Status**: Implementation Ready
