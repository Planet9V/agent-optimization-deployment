# vis-network Build Error: Technical Analysis & Solutions

**File:** vis-network-build-error-analysis.md
**Created:** 2025-11-04
**Author:** Research Agent (SuperClaude)
**Purpose:** Root cause analysis and solutions for "ReferenceError: self is not defined" in Next.js SSG builds
**Status:** ACTIVE

---

## Executive Summary

The `vis-network` library causes a **"ReferenceError: self is not defined"** error during Next.js static site generation (SSG) because it relies on browser-specific global objects (`self`, `window`) that are unavailable in Node.js server-side build environments. This document provides comprehensive root cause analysis and three production-ready solutions.

**Critical Finding:** vis-network uses HTML Canvas for rendering and depends on browser APIs, making it incompatible with server-side execution without proper isolation.

---

## 1. Root Cause Analysis

### 1.1 What is the "self" Global?

**Browser Context:**
- `self` is a browser global that references the `Window` object
- Available in: Web Workers, Service Workers, and main browser thread
- Used for: Cross-context compatibility (works in workers where `window` is undefined)

**Node.js Context:**
- `self` **does not exist** in Node.js runtime
- Node.js uses `global` instead of `window`/`self`
- Build processes execute in Node.js, not browser environment

**Technical Pattern:**
```javascript
// Universal global detection pattern
const globalObject = (typeof self === 'object' && self.self === self && self) ||
                     (typeof global === 'object' && global.global === global && global)
```

### 1.2 Why vis-network Fails During SSG Build

**vis-network Architecture:**
- **Rendering Engine:** HTML Canvas (browser-only API)
- **External Dependencies:**
  - Hammer.js v2 (touch/gesture library, requires DOM)
  - Moment.js (included in default bundle)
- **Module System:** CommonJS (require/module.exports)
- **Build Process:** Expects browser globals at initialization

**Next.js Build Process:**
1. **Build Time (Node.js):**
   - Next.js executes all imports and top-level code in Node.js
   - Pages are pre-rendered to generate static HTML
   - vis-network attempts to access `self` → **ERROR**

2. **Runtime (Browser):**
   - Client receives pre-rendered HTML
   - React hydrates the page
   - vis-network would work here, but build already failed

**Error Location:**
```
ReferenceError: self is not defined
  at node_modules/vis-network/dist/vis-network.js:initialization
  during: next build (SSG phase)
```

### 1.3 Next.js Rendering Modes Impact

| Rendering Mode | Build Environment | vis-network Compatibility | Explanation |
|----------------|-------------------|--------------------------|-------------|
| **SSG** (Static Site Generation) | Node.js at build time | ❌ **FAILS** | Executes all imports during `next build`, encounters `self` reference |
| **SSR** (Server-Side Rendering) | Node.js on each request | ❌ **FAILS** | Server attempts to render component with browser APIs on every request |
| **CSR** (Client-Side Rendering) | Browser only | ✅ **WORKS** | Component loads only in browser, `self` is available |
| **ISR** (Incremental Static Regeneration) | Node.js at revalidation | ❌ **FAILS** | Similar to SSG, regenerates pages server-side |

**Key Insight:** vis-network is **client-side only** and requires CSR or CSR-like isolation.

---

## 2. Three Production-Ready Solutions

### Solution 1: Dynamic Import with SSR Disabled (RECOMMENDED)

**Approach:** Use Next.js `dynamic()` to load component only on client-side.

**Implementation:**

```javascript
// components/NetworkVisualization.jsx (Client Component)
'use client' // Required in Next.js App Router

import { useEffect, useRef } from 'react'

export default function NetworkVisualization({ data }) {
  const containerRef = useRef(null)

  useEffect(() => {
    // Import vis-network ONLY in browser
    import('vis-network').then((module) => {
      const { Network } = module

      const network = new Network(
        containerRef.current,
        data,
        options
      )

      return () => network.destroy()
    })
  }, [data])

  return (
    <div
      ref={containerRef}
      style={{ width: '100%', height: '600px' }}
    />
  )
}
```

```javascript
// app/page.jsx (Parent Component)
import dynamic from 'next/dynamic'

// Dynamic import with SSR disabled
const NetworkVisualization = dynamic(
  () => import('@/components/NetworkVisualization'),
  {
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center h-96">
        <p className="text-gray-500">Loading network visualization...</p>
      </div>
    )
  }
)

export default function Page() {
  return (
    <div>
      <h1>Network Graph</h1>
      <NetworkVisualization data={networkData} />
    </div>
  )
}
```

**Pros:**
- ✅ Zero webpack configuration required
- ✅ Built-in Next.js feature (stable API)
- ✅ Graceful loading states with `loading` prop
- ✅ Works with both App Router and Pages Router
- ✅ No build-time execution of vis-network code
- ✅ Automatic code splitting (smaller initial bundle)

**Cons:**
- ⚠️ No server-side rendering for this component (SEO impact)
- ⚠️ Component not visible until JavaScript loads
- ⚠️ Slight delay before visualization appears
- ⚠️ Cannot use in Server Components directly

**Production Considerations:**
- **SEO:** If network visualization is critical content, consider pre-rendering a static image/screenshot
- **Performance:** Use `loading` prop to show skeleton/placeholder
- **Accessibility:** Ensure loading state is announced to screen readers

---

### Solution 2: Conditional Import with Browser Check

**Approach:** Check for browser environment before importing vis-network.

**Implementation:**

```javascript
// lib/network-loader.js
export async function loadNetwork() {
  // Only import in browser
  if (typeof window === 'undefined') {
    return null
  }

  const { Network } = await import('vis-network')
  return Network
}
```

```javascript
// components/NetworkVisualization.jsx
'use client'

import { useEffect, useRef, useState } from 'react'
import { loadNetwork } from '@/lib/network-loader'

export default function NetworkVisualization({ data }) {
  const containerRef = useRef(null)
  const [isReady, setIsReady] = useState(false)

  useEffect(() => {
    let network = null

    loadNetwork().then((Network) => {
      if (!Network) return // Server-side, skip

      network = new Network(
        containerRef.current,
        data,
        options
      )
      setIsReady(true)
    })

    return () => {
      if (network) network.destroy()
    }
  }, [data])

  return (
    <div
      ref={containerRef}
      className={isReady ? 'visible' : 'loading'}
      style={{ width: '100%', height: '600px' }}
    >
      {!isReady && <p>Loading visualization...</p>}
    </div>
  )
}
```

**Pros:**
- ✅ Fine-grained control over loading logic
- ✅ Can implement custom loading strategies
- ✅ Works with SSR pages (component gracefully skips on server)
- ✅ No external dependencies beyond vis-network

**Cons:**
- ⚠️ More boilerplate code required
- ⚠️ Manual state management for loading
- ⚠️ Still requires `'use client'` directive (not truly server-compatible)
- ⚠️ Potential for race conditions if not carefully managed

**Use Case:** When you need custom loading logic or want to avoid `dynamic()` for some reason.

---

### Solution 3: Webpack Configuration (Advanced)

**Approach:** Configure webpack to exclude vis-network from server bundle.

**Implementation:**

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    if (isServer) {
      // Exclude vis-network from server bundle
      config.externals = [
        ...config.externals,
        {
          'vis-network': 'vis-network',
          'vis-data': 'vis-data'
        }
      ]
    }

    // Optional: Alias for client-side
    config.resolve.alias = {
      ...config.resolve.alias,
      'vis-network': 'vis-network/peer',
    }

    // Ensure proper global object for universal code
    config.output = {
      ...config.output,
      globalObject: 'this', // Instead of 'window' or 'self'
    }

    return config
  },
}

module.exports = nextConfig
```

```javascript
// components/NetworkVisualization.jsx
'use client'

import { useEffect, useRef } from 'react'
// Normal import - webpack handles the server/client split
import { Network } from 'vis-network'

export default function NetworkVisualization({ data }) {
  const containerRef = useRef(null)

  useEffect(() => {
    const network = new Network(
      containerRef.current,
      data,
      options
    )

    return () => network.destroy()
  }, [data])

  return (
    <div
      ref={containerRef}
      style={{ width: '100%', height: '600px' }}
    />
  )
}
```

**Pros:**
- ✅ Cleaner component code (normal imports)
- ✅ Centralized configuration
- ✅ Can apply to multiple problematic libraries
- ✅ More control over bundling strategy
- ✅ Works with tree-shaking optimizations

**Cons:**
- ⚠️ More complex configuration
- ⚠️ Requires understanding of webpack internals
- ⚠️ Potential for breaking changes in Next.js webpack updates
- ⚠️ Still requires `'use client'` for actual component
- ⚠️ May cause issues with other build optimizations

**Use Case:** Large applications with many client-only libraries requiring consistent handling.

---

## 3. Recommended Solution Comparison

### Quick Decision Matrix

| Criterion | Dynamic Import (Solution 1) | Browser Check (Solution 2) | Webpack Config (Solution 3) |
|-----------|---------------------------|---------------------------|----------------------------|
| **Ease of Implementation** | ⭐⭐⭐⭐⭐ Easiest | ⭐⭐⭐ Moderate | ⭐⭐ Complex |
| **Maintainability** | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐ Good | ⭐⭐ Requires expertise |
| **Performance** | ⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Excellent |
| **Flexibility** | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Very flexible | ⭐⭐⭐⭐⭐ Maximum control |
| **Risk Level** | ⭐⭐⭐⭐⭐ Very Low | ⭐⭐⭐ Low | ⭐⭐ Medium-High |
| **Next.js Version Compatibility** | ⭐⭐⭐⭐⭐ Stable API | ⭐⭐⭐⭐ Stable | ⭐⭐⭐ May break |

### Production Recommendation

**For Most Projects: Use Solution 1 (Dynamic Import)**

**Rationale:**
1. **Official Next.js Pattern:** `dynamic()` with `ssr: false` is the documented approach
2. **Zero Configuration:** Works out of the box, no webpack modifications
3. **Future-Proof:** Less likely to break with Next.js updates
4. **Clear Intent:** Code explicitly shows "client-only" behavior
5. **Built-in Features:** Loading states, error boundaries, code splitting

**When to Use Alternatives:**

- **Solution 2:** Complex loading logic, need custom fallback behavior
- **Solution 3:** Multiple client-only libraries, require centralized configuration, advanced optimization needs

---

## 4. Implementation Best Practices

### 4.1 Loading States

**Provide meaningful feedback during load:**

```javascript
const NetworkVisualization = dynamic(
  () => import('@/components/NetworkVisualization'),
  {
    ssr: false,
    loading: () => (
      <div className="animate-pulse">
        <div className="h-96 bg-gray-200 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <svg className="animate-spin h-8 w-8 text-blue-500 mx-auto mb-4" />
            <p className="text-gray-600">Loading interactive network...</p>
          </div>
        </div>
      </div>
    )
  }
)
```

### 4.2 Error Handling

**Gracefully handle load failures:**

```javascript
'use client'

import { useEffect, useRef, useState } from 'react'

export default function NetworkVisualization({ data }) {
  const [error, setError] = useState(null)

  useEffect(() => {
    import('vis-network')
      .then((module) => {
        // Initialize network
      })
      .catch((err) => {
        console.error('Failed to load vis-network:', err)
        setError('Unable to load visualization. Please refresh.')
      })
  }, [])

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded p-4">
        <p className="text-red-700">{error}</p>
      </div>
    )
  }

  return <div ref={containerRef} />
}
```

### 4.3 Performance Optimization

**Optimize bundle size:**

```javascript
// Import only what you need
import('vis-network').then((module) => {
  const { Network } = module
  // Use Network class
})

// Or use direct path imports (if supported)
import('vis-network/standalone/esm/vis-network').then(...)
```

### 4.4 SEO Considerations

**For SEO-critical content, provide static fallback:**

```javascript
export default function Page() {
  return (
    <div>
      <h1>Project Network Visualization</h1>

      {/* Static content for crawlers */}
      <noscript>
        <img
          src="/static/network-preview.png"
          alt="Project network graph showing 150 nodes and 300 connections"
        />
      </noscript>

      {/* Dynamic visualization for users */}
      <NetworkVisualization data={data} />

      {/* Text alternative for accessibility */}
      <details className="mt-4">
        <summary>View network data as text</summary>
        <ul>
          {data.nodes.map(node => (
            <li key={node.id}>{node.label}</li>
          ))}
        </ul>
      </details>
    </div>
  )
}
```

---

## 5. Testing Strategy

### 5.1 Build Testing

**Ensure builds complete successfully:**

```bash
# Test production build
npm run build

# Look for errors in output
# ✅ Success: "Compiled successfully"
# ❌ Failure: "ReferenceError: self is not defined"
```

### 5.2 Runtime Testing

**Test in multiple environments:**

1. **Development Mode:**
   ```bash
   npm run dev
   # Visit page with network visualization
   # Verify: Component loads without errors
   ```

2. **Production Preview:**
   ```bash
   npm run build && npm run start
   # Visit page
   # Verify: Loads correctly, no hydration errors
   ```

3. **Static Export (if using):**
   ```bash
   npm run build
   # Check: out/ directory contains static files
   # No runtime errors during generation
   ```

### 5.3 Browser Compatibility

**Test across browsers:**

| Browser | Expected Behavior |
|---------|------------------|
| Chrome/Edge | ✅ Full support |
| Firefox | ✅ Full support |
| Safari | ✅ Full support (test iOS too) |
| Mobile browsers | ✅ Touch interactions work (hammer.js) |

---

## 6. Common Pitfalls & Solutions

### Pitfall 1: Hydration Mismatch

**Problem:** Server renders placeholder, client renders different content.

**Solution:**
```javascript
const [mounted, setMounted] = useState(false)

useEffect(() => {
  setMounted(true)
}, [])

if (!mounted) return <LoadingPlaceholder />
return <NetworkVisualization />
```

### Pitfall 2: Memory Leaks

**Problem:** Network instance not cleaned up on unmount.

**Solution:**
```javascript
useEffect(() => {
  let network = null

  import('vis-network').then((module) => {
    network = new module.Network(...)
  })

  return () => {
    if (network) {
      network.destroy() // CRITICAL: Clean up
    }
  }
}, [])
```

### Pitfall 3: Using in Server Components

**Problem:** Trying to use vis-network in Server Component.

**Solution:**
```javascript
// ❌ WRONG: Server Component
export default function ServerComponent() {
  return <NetworkVisualization /> // Will fail
}

// ✅ CORRECT: Wrap in Client Component or use dynamic
'use client'
export default function ClientWrapper() {
  return <NetworkVisualization />
}
```

---

## 7. Alternative Libraries (If vis-network Doesn't Work)

If vis-network proves too problematic, consider these SSR-friendly alternatives:

| Library | SSR Support | Features | Bundle Size |
|---------|-------------|----------|-------------|
| **Cytoscape.js** | ✅ Good | Graph theory, layouts | ~380KB |
| **React Flow** | ✅ Excellent | React-native, type-safe | ~150KB |
| **D3.js** | ✅ Excellent | Maximum flexibility | ~250KB |
| **Sigma.js** | ⚠️ Moderate | WebGL rendering | ~200KB |

**Recommendation:** If rebuilding is an option, **React Flow** offers the best Next.js integration.

---

## 8. References & Further Reading

### Official Documentation
- [Next.js Dynamic Import](https://nextjs.org/docs/pages/guides/lazy-loading)
- [vis-network Documentation](https://visjs.github.io/vis-network/docs/network/)
- [Next.js Rendering Modes](https://nextjs.org/docs/app/building-your-application/rendering)

### Community Resources
- [Stack Overflow: ReferenceError self is not defined](https://stackoverflow.com/questions/66096260/why-am-i-getting-referenceerror-self-is-not-defined)
- [Next.js SSR Best Practices](https://nextjs.org/docs/app/building-your-application/rendering/server-components)

### Key Concepts
- **SSG vs SSR vs CSR:** [Understanding Next.js Rendering Methods](https://medium.com/@narayanansundar02/understanding-next-js-rendering-methods-ssr-csr-ssg-and-isr-7764dedabbe6)
- **Browser Globals in Node.js:** [window-or-global npm package](https://www.npmjs.com/package/window-or-global)

---

## 9. Summary & Action Items

### Key Takeaways

1. **Root Cause:** vis-network requires browser globals (`self`, `window`) unavailable in Node.js SSG builds
2. **Best Solution:** Use `next/dynamic` with `ssr: false` for simplicity and maintainability
3. **Next.js Modes:** Only CSR (client-side rendering) works directly with vis-network
4. **Implementation:** Wrap component in dynamic import, provide loading state, handle cleanup

### Immediate Action Items

- [ ] Implement Solution 1 (Dynamic Import) in existing components
- [ ] Add loading states for better UX
- [ ] Test production build to verify fix
- [ ] Add error boundaries for graceful failure handling
- [ ] Document pattern for team (link to this document)

### Long-Term Considerations

- [ ] Evaluate if vis-network is best long-term choice
- [ ] Consider React Flow or Cytoscape.js for better SSR support
- [ ] Monitor bundle size impact of client-only rendering
- [ ] Implement static fallbacks for SEO if needed

---

**Document Version:** 1.0
**Last Updated:** 2025-11-04
**Next Review:** 2025-12-04 or when Next.js 15 releases
