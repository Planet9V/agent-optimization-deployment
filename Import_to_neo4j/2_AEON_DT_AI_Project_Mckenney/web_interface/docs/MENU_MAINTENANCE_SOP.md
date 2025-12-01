# Menu Maintenance Standard Operating Procedure (SOP)

**Document Version**: 2.0
**Last Updated**: 2025-11-04
**Applies To**: AEON Digital Twin Platform
**Primary Component**: `/components/navigation/ModernNav.tsx`
**Status**: PRODUCTION READY

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture Deep Dive](#architecture-deep-dive)
3. [Adding Menu Items](#adding-menu-items)
4. [Removing Menu Items](#removing-menu-items)
5. [Modifying Dropdowns](#modifying-dropdowns)
6. [Creating New Pages](#creating-new-pages)
7. [Testing Procedures](#testing-procedures)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Best Practices](#best-practices)
10. [Version Control Workflow](#version-control-workflow)
11. [Quick Reference](#quick-reference)

---

## Overview

### Purpose
This SOP provides comprehensive, step-by-step instructions for maintaining the navigation menu system in the AEON Digital Twin platform. It ensures consistency, quality, and maintainability across all menu-related operations.

### Current Menu Structure (As of Nov 2025)

```
Navigation Bar
├── Dashboard (/)
├── Analytics ▼
│   ├── Trends (/analytics/trends)
│   ├── Metrics (/analytics/metrics)
│   └── Reports (/analytics/reports)
├── Threat Intel ▼
│   ├── Vulnerabilities (/threat-intel/vulnerabilities)
│   ├── Threat Actors (/threat-intel/actors)
│   └── Campaigns (/threat-intel/campaigns)
├── Search ▼
│   ├── Full-text Search (/search/fulltext)
│   ├── Semantic Search (/search/semantic)
│   └── Hybrid Search (/search/hybrid)
├── Graph Explorer (/graph)
└── Settings (/settings)
```

### Key Files & Locations

| File | Purpose | Location |
|------|---------|----------|
| ModernNav.tsx | Main navigation component | `/components/navigation/` |
| NavDropdown.tsx | Dropdown menu component | `/components/navigation/` |
| MobileMenu.tsx | Mobile responsive menu | `/components/navigation/` |
| Page files | Route destinations | `/app/{route}/page.tsx` |

### Technology Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript + React
- **Icons**: Lucide React
- **Styling**: Tailwind CSS
- **State Management**: React Hooks (useState, useRef, useEffect)

---

## Architecture Deep Dive

### Component Hierarchy

```
ModernNav (Parent)
├── Logo/Brand Section
├── Desktop Navigation
│   ├── Simple Links (Dashboard, Graph, Settings)
│   └── NavDropdown Components (Analytics, Threat Intel, Search)
│       └── Dropdown Items (Links)
├── Mobile Menu Button
└── MobileMenu Component
    └── Mobile Versions of All Navigation Items
```

### State Management

#### ModernNav.tsx State
```typescript
const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
```
- **Type**: `boolean`
- **Purpose**: Controls mobile menu visibility
- **Managed by**: Mobile menu button toggle

#### NavDropdown.tsx State
```typescript
const [isOpen, setIsOpen] = useState(false);
const dropdownRef = useRef<HTMLDivElement>(null);
```
- **isOpen Type**: `boolean`
- **Purpose**: Controls dropdown visibility (one per dropdown)
- **Trigger**: Click, hover (onMouseEnter), or click-outside
- **Behavior**: Each dropdown manages its own state independently

### Data Flow

```
User Action (click/hover)
    ↓
Event Handler (onClick/onMouseEnter)
    ↓
State Update (setIsOpen/setMobileMenuOpen)
    ↓
Conditional Rendering ({isOpen && <dropdown>})
    ↓
DOM Update (dropdown appears/disappears)
```

### Event Handling Mechanisms

#### Desktop Dropdown Events
```typescript
// Open on click
onClick={() => setIsOpen(!isOpen)}

// Open on hover
onMouseEnter={() => setIsOpen(true)}

// Close on mouse leave
onMouseLeave={() => setIsOpen(false)}

// Close on outside click (via useEffect)
useEffect(() => {
  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  };
  document.addEventListener('mousedown', handleClickOutside);
  return () => document.removeEventListener('mousedown', handleClickOutside);
}, []);
```

### CSS Architecture

#### Key Tailwind Classes
```typescript
// Navigation bar container
"bg-slate-950 border-b border-slate-800 sticky top-0 z-50"

// Desktop link (simple)
"group flex items-center px-3 py-2 rounded-md text-sm font-medium
 text-slate-100 hover:text-emerald-500 hover:bg-slate-900
 transition-all duration-200"

// Dropdown button (same as link + chevron animation)
"group flex items-center px-3 py-2 rounded-md text-sm font-medium
 text-slate-100 hover:text-emerald-500 hover:bg-slate-900
 transition-all duration-200"

// Dropdown container
"absolute left-0 mt-1 w-56 rounded-md shadow-lg bg-slate-900
 ring-1 ring-slate-800 ring-opacity-50 divide-y divide-slate-800
 animate-in fade-in-0 zoom-in-95 duration-200"

// Dropdown item
"group flex items-center px-4 py-3 text-sm text-slate-100
 hover:text-emerald-500 hover:bg-slate-800 transition-colors duration-150"
```

---

## Adding Menu Items

### Adding a Simple Top-Level Link

#### When to Use
- Standalone features that don't need dropdown grouping
- High-traffic destinations (Dashboard, Settings)
- Single-page tools (Graph Explorer)

#### Step-by-Step Procedure

**Step 1: Verify Page Exists**
```bash
# Check if page file exists
ls -la app/your-route/page.tsx

# If it doesn't exist, see "Creating New Pages" section first
```

**Step 2: Import Required Icon**
```typescript
// At top of ModernNav.tsx (line ~2)
import { Home, TrendingUp, Shield, Search, Network, Settings,
         YourNewIcon } from 'lucide-react';
//       ^^^^^^^^^^^^ Add your new icon here
```

**Step 3: Add Link Component**
```typescript
// Inside Desktop Navigation section (around line 42)
{/* Your New Feature */}
<a
  href="/your-route"
  className="group flex items-center px-3 py-2 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-all duration-200"
>
  <YourNewIcon className="w-4 h-4 mr-2" />
  Your Label
</a>
```

**Step 4: Add to Mobile Menu**
```typescript
// In MobileMenu.tsx, add similar link structure
<a
  href="/your-route"
  className="block px-3 py-2 rounded-md text-base font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900"
  onClick={onClose}
>
  <div className="flex items-center">
    <YourNewIcon className="w-5 h-5 mr-3" />
    Your Label
  </div>
</a>
```

#### Real-World Example: Adding "Reports" as Top-Level

```typescript
// 1. Import icon
import { FileText } from 'lucide-react';

// 2. Add to desktop navigation (after Settings)
{/* Reports */}
<a
  href="/reports"
  className="group flex items-center px-3 py-2 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-all duration-200"
>
  <FileText className="w-4 h-4 mr-2" />
  Reports
</a>

// 3. Create page file at /app/reports/page.tsx (see "Creating New Pages")
```

---

### Adding an Item to an Existing Dropdown

#### When to Use
- Feature logically belongs to existing category
- Not important enough for top-level
- Related to other items in dropdown

#### Step-by-Step Procedure

**Step 1: Locate Dropdown Data Array**
```typescript
// In ModernNav.tsx, find the relevant array (around line 9-25)
const analyticsItems = [
  { label: 'Trends', href: '/analytics/trends' },
  { label: 'Metrics', href: '/analytics/metrics' },
  { label: 'Reports', href: '/analytics/reports' },
  // Add new item here
];
```

**Step 2: Add New Item to Array**
```typescript
const analyticsItems = [
  { label: 'Trends', href: '/analytics/trends' },
  { label: 'Metrics', href: '/analytics/metrics' },
  { label: 'Reports', href: '/analytics/reports' },
  { label: 'Dashboards', href: '/analytics/dashboards' }, // NEW
];
```

**Step 3: Verify Dropdown Renders Correctly**
The `NavDropdown` component automatically renders all items in the array:
```typescript
{items.map((item, index) => (
  <a key={index} href={item.href} /* ... */>
    {item.label}
  </a>
))}
```

**No additional code needed!** The dropdown will automatically include your new item.

#### Real-World Example: Adding "Incidents" to Threat Intel Dropdown

```typescript
// BEFORE
const threatIntelItems = [
  { label: 'Vulnerabilities', href: '/threat-intel/vulnerabilities' },
  { label: 'Threat Actors', href: '/threat-intel/actors' },
  { label: 'Campaigns', href: '/threat-intel/campaigns' },
];

// AFTER
const threatIntelItems = [
  { label: 'Vulnerabilities', href: '/threat-intel/vulnerabilities' },
  { label: 'Threat Actors', href: '/threat-intel/actors' },
  { label: 'Campaigns', href: '/threat-intel/campaigns' },
  { label: 'Incidents', href: '/threat-intel/incidents' }, // NEW
];

// Also create page file: /app/threat-intel/incidents/page.tsx
```

---

## Removing Menu Items

### Removing a Top-Level Link

#### Pre-Removal Checklist
- [ ] Verify no critical functionality depends on this route
- [ ] Check for external links pointing to this page
- [ ] Review analytics to ensure low/no traffic
- [ ] Confirm with stakeholders
- [ ] Plan deprecation notice if needed

#### Step-by-Step Procedure

**Step 1: Remove Link Component**
```typescript
// BEFORE
<a href="/old-feature" className="...">
  <OldIcon className="w-4 h-4 mr-2" />
  Old Feature
</a>

// AFTER (delete entire <a> block)
```

**Step 2: Remove Icon Import (if unique)**
```typescript
// BEFORE
import { Home, OldIcon, Settings } from 'lucide-react';

// AFTER
import { Home, Settings } from 'lucide-react';
```

**Step 3: Remove from Mobile Menu**
```typescript
// Find and delete corresponding mobile menu link
```

**Step 4: Handle Page File**
```bash
# Option 1: Delete (if completely unused)
rm app/old-feature/page.tsx

# Option 2: Create redirect (if external links exist)
# See "Creating Redirects" section
```

---

### Removing an Item from a Dropdown

#### Step-by-Step Procedure

**Step 1: Locate Array and Remove Item**
```typescript
// BEFORE
const searchItems = [
  { label: 'Full-text Search', href: '/search/fulltext' },
  { label: 'Semantic Search', href: '/search/semantic' },
  { label: 'Old Search', href: '/search/old' }, // REMOVE THIS
  { label: 'Hybrid Search', href: '/search/hybrid' },
];

// AFTER
const searchItems = [
  { label: 'Full-text Search', href: '/search/fulltext' },
  { label: 'Semantic Search', href: '/search/semantic' },
  { label: 'Hybrid Search', href: '/search/hybrid' },
];
```

**Step 2: Test Dropdown Renders Correctly**
```bash
npm run dev
# Navigate to page, open dropdown, verify item is gone
```

---

## Modifying Dropdowns

### Creating a New Dropdown

#### When to Create New Dropdown
- You have 3+ related features to group
- Features form a logical workflow category
- Top-level menu is getting crowded (>7 items)

#### Step-by-Step Procedure

**Step 1: Create Items Array**
```typescript
// In ModernNav.tsx, add new array
const investigateItems = [
  { label: 'Forensics', href: '/investigate/forensics' },
  { label: 'Timeline', href: '/investigate/timeline' },
  { label: 'Evidence', href: '/investigate/evidence' },
];
```

**Step 2: Import Icon for Dropdown Button**
```typescript
import { Home, TrendingUp, Shield, Search, Network, Settings,
         Target } from 'lucide-react';
//       ^^^^^^ Icon for new dropdown
```

**Step 3: Add NavDropdown Component**
```typescript
{/* Desktop Navigation */}
<div className="ml-10 flex items-center space-x-1">
  {/* ... existing items ... */}

  {/* Investigate Dropdown - NEW */}
  <NavDropdown
    label="Investigate"
    icon={<Target className="w-4 h-4" />}
    items={investigateItems}
  />

  {/* ... rest of items ... */}
</div>
```

**Step 4: Add to Mobile Menu**
```typescript
// In MobileMenu.tsx, pass new array as prop
<MobileMenu
  isOpen={mobileMenuOpen}
  onClose={() => setMobileMenuOpen(false)}
  analyticsItems={analyticsItems}
  threatIntelItems={threatIntelItems}
  searchItems={searchItems}
  investigateItems={investigateItems} // NEW
/>

// Then render in MobileMenu component using same pattern
```

#### Complete Example: Adding "Tools" Dropdown

```typescript
// Step 1: Create items array
const toolsItems = [
  { label: 'IP Lookup', href: '/tools/ip-lookup' },
  { label: 'Hash Checker', href: '/tools/hash-checker' },
  { label: 'Decoder', href: '/tools/decoder' },
];

// Step 2: Import icon
import { Wrench } from 'lucide-react';

// Step 3: Add NavDropdown
<NavDropdown
  label="Tools"
  icon={<Wrench className="w-4 h-4" />}
  items={toolsItems}
/>

// Step 4: Create page files
// /app/tools/ip-lookup/page.tsx
// /app/tools/hash-checker/page.tsx
// /app/tools/decoder/page.tsx
```

---

### Renaming a Dropdown

#### Step-by-Step Procedure

**Step 1: Update Array Name**
```typescript
// BEFORE
const analyticsItems = [...];

// AFTER
const insightsItems = [...]; // Renamed
```

**Step 2: Update NavDropdown Props**
```typescript
// BEFORE
<NavDropdown
  label="Analytics"
  icon={<TrendingUp className="w-4 h-4" />}
  items={analyticsItems}
/>

// AFTER
<NavDropdown
  label="Insights"  // Updated label
  icon={<TrendingUp className="w-4 h-4" />}
  items={insightsItems}  // Updated array reference
/>
```

**Step 3: Update Mobile Menu**
```typescript
// Update prop name and references in MobileMenu component
```

---

### Removing a Dropdown

#### Pre-Removal Checklist
- [ ] Confirm all dropdown items can be safely removed or relocated
- [ ] Check if any items should be promoted to top-level
- [ ] Verify no critical workflows disrupted

#### Step-by-Step Procedure

**Step 1: Decide Item Fate**
- **Delete**: Remove items completely
- **Relocate**: Move to different dropdown
- **Promote**: Make top-level links

**Step 2: Remove Items Array**
```typescript
// Delete this:
const oldDropdownItems = [
  { label: 'Item 1', href: '/old/item1' },
  { label: 'Item 2', href: '/old/item2' },
];
```

**Step 3: Remove NavDropdown Component**
```typescript
// Delete this:
<NavDropdown
  label="Old Dropdown"
  icon={<OldIcon className="w-4 h-4" />}
  items={oldDropdownItems}
/>
```

**Step 4: Remove Icon Import (if unique)**

**Step 5: Remove from Mobile Menu**

---

## Creating New Pages

### Page Creation Workflow

```
1. Determine Route → 2. Create Page File → 3. Add to Menu → 4. Test Navigation
```

### Next.js App Router File Structure

```
app/
├── your-feature/              # Route: /your-feature
│   ├── page.tsx              # Main page component
│   ├── loading.tsx           # (Optional) Loading state
│   ├── error.tsx             # (Optional) Error boundary
│   └── layout.tsx            # (Optional) Layout wrapper
├── nested/
│   └── route/                # Route: /nested/route
│       └── page.tsx
└── [dynamic]/                # Route: /dynamic/:id
    └── page.tsx
```

### Page Template (Standard)

```typescript
'use client';

import { useState, useEffect } from 'react';
import { YourIcon } from 'lucide-react';

export default function YourPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch data on mount
    const fetchData = async () => {
      try {
        const response = await fetch('/api/your-endpoint');
        if (!response.ok) throw new Error('Failed to fetch');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center mb-2">
            <YourIcon className="h-8 w-8 text-emerald-500 mr-3" />
            <h1 className="text-3xl font-bold text-slate-50">
              Your Page Title
            </h1>
          </div>
          <p className="text-slate-400">
            Your page description and purpose
          </p>
        </div>

        {/* Content */}
        <div className="space-y-6">
          {/* Your content components */}
        </div>
      </div>
    </div>
  );
}
```

### Page Template (Simple - No Data Fetching)

```typescript
import { YourIcon } from 'lucide-react';

export default function SimpleYourPage() {
  return (
    <div className="min-h-screen bg-slate-950 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center mb-6">
          <YourIcon className="h-8 w-8 text-emerald-500 mr-3" />
          <h1 className="text-3xl font-bold text-slate-50">
            Your Page Title
          </h1>
        </div>

        <div className="bg-slate-900 rounded-lg p-6 border border-slate-800">
          <p className="text-slate-300">
            Your static content here
          </p>
        </div>
      </div>
    </div>
  );
}
```

### Real-World Example: Creating "/tools/ip-lookup" Page

```bash
# Step 1: Create directory and file
mkdir -p app/tools/ip-lookup
touch app/tools/ip-lookup/page.tsx
```

```typescript
// Step 2: Implement page
'use client';

import { useState } from 'react';
import { Globe, Search } from 'lucide-react';

export default function IPLookupPage() {
  const [ip, setIp] = useState('');
  const [result, setResult] = useState(null);

  const handleLookup = async () => {
    const response = await fetch(`/api/tools/ip-lookup?ip=${ip}`);
    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="min-h-screen bg-slate-950 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center mb-6">
          <Globe className="h-8 w-8 text-emerald-500 mr-3" />
          <h1 className="text-3xl font-bold text-slate-50">
            IP Address Lookup
          </h1>
        </div>

        <div className="bg-slate-900 rounded-lg p-6 border border-slate-800">
          <div className="flex gap-4 mb-6">
            <input
              type="text"
              value={ip}
              onChange={(e) => setIp(e.target.value)}
              placeholder="Enter IP address"
              className="flex-1 bg-slate-800 text-slate-100 px-4 py-2 rounded-lg border border-slate-700 focus:border-emerald-500 focus:outline-none"
            />
            <button
              onClick={handleLookup}
              className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
            >
              <Search className="h-4 w-4" />
              Lookup
            </button>
          </div>

          {result && (
            <div className="bg-slate-800 rounded-lg p-4">
              <pre className="text-slate-300 text-sm">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
```

```typescript
// Step 3: Add to menu (see "Adding Menu Items" section)
const toolsItems = [
  { label: 'IP Lookup', href: '/tools/ip-lookup' },
];
```

---

### Creating Redirects

#### When to Create Redirects
- Old menu structure being replaced
- Routes being renamed but external links exist
- Legacy URLs need to be preserved

#### Method 1: Page-Level Redirect (Recommended)

```typescript
// Create page at old route: /app/old-route/page.tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function OldRoutePage() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/new-route');
  }, [router]);

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400">Redirecting...</div>
    </div>
  );
}
```

#### Method 2: Next.js Config Redirect

```javascript
// In next.config.js
module.exports = {
  async redirects() {
    return [
      {
        source: '/old-route',
        destination: '/new-route',
        permanent: true, // 308 permanent redirect
      },
      {
        source: '/analytics/threats',
        destination: '/threat-intel',
        permanent: true,
      },
    ];
  },
};
```

---

## Testing Procedures

### Pre-Deployment Testing Checklist

#### Visual Testing
- [ ] **Menu Appearance**: All items visible and properly styled
- [ ] **Icon Rendering**: Icons display correctly at proper sizes
- [ ] **Hover Effects**: Hover states work (color change, background)
- [ ] **Active States**: Current page highlighted (if implemented)
- [ ] **Spacing**: Consistent padding and margins
- [ ] **Typography**: Font sizes and weights consistent

#### Functional Testing
- [ ] **Link Navigation**: All links navigate to correct pages
- [ ] **Dropdown Opening**: Dropdowns open on click and hover
- [ ] **Dropdown Closing**: Dropdowns close on outside click
- [ ] **Single Dropdown**: Only one dropdown open at a time
- [ ] **Mobile Menu**: Hamburger menu toggles correctly
- [ ] **Mobile Navigation**: All items accessible on mobile
- [ ] **Keyboard Navigation**: Tab, Enter, Escape keys work

#### Page Verification
- [ ] **Page Existence**: All linked pages exist (no 404s)
- [ ] **Page Loading**: Pages load without errors
- [ ] **Authentication**: Protected pages enforce auth
- [ ] **API Endpoints**: Backend endpoints respond correctly
- [ ] **Error States**: Error handling works properly

#### Responsive Testing
- [ ] **Desktop** (1920px+): Full navigation visible
- [ ] **Laptop** (1280px-1919px): Navigation fits properly
- [ ] **Tablet** (768px-1279px): Mobile menu activates
- [ ] **Mobile** (375px-767px): Touch-friendly menu works

#### Browser Compatibility
- [ ] **Chrome/Edge**: Latest version
- [ ] **Firefox**: Latest version
- [ ] **Safari**: Latest version (macOS/iOS)
- [ ] **Mobile Browsers**: Chrome Mobile, Safari iOS

### Testing Commands

```bash
# TypeScript compilation check
npm run typecheck

# Linting
npm run lint

# Build production bundle (catches build-time errors)
npm run build

# Development server (for manual testing)
npm run dev

# Visit in browser
open http://localhost:3000
```

### Manual Testing Procedure

**Step 1: Visual Inspection**
```bash
# Start dev server
npm run dev

# Open browser
open http://localhost:3000

# Check:
# - Menu renders correctly
# - All items visible
# - Styling matches design
```

**Step 2: Click Through Every Link**
```
Test Matrix:
┌─────────────────────┬──────────────┬─────────────┬─────────┐
│ Menu Item           │ Expected URL │ Page Loads? │ Status  │
├─────────────────────┼──────────────┼─────────────┼─────────┤
│ Dashboard           │ /dashboard   │ ✅          │ PASS    │
│ Analytics > Trends  │ /analytics/  │ ✅          │ PASS    │
│                     │   trends     │             │         │
│ ...                 │ ...          │ ...         │ ...     │
└─────────────────────┴──────────────┴─────────────┴─────────┘
```

**Step 3: Test Dropdown Behavior**
```
Test Cases:
1. Click dropdown button → Opens
2. Click outside → Closes
3. Hover on button → Opens
4. Mouse leave dropdown → Closes
5. Click dropdown item → Navigates and closes
6. Open dropdown A, then click dropdown B → A closes, B opens
```

**Step 4: Mobile Testing**
```bash
# Option 1: Chrome DevTools
# Open DevTools > Toggle Device Toolbar (Cmd+Shift+M)
# Test responsive breakpoints

# Option 2: Real Device
# Find local network IP
ifconfig | grep "inet "
# Open http://YOUR_IP:3000 on mobile device
```

**Step 5: Keyboard Navigation**
```
Test Cases:
1. Tab → Focus moves through menu items
2. Enter → Activates focused link/button
3. Escape → Closes open dropdown
4. Arrow keys → (Future enhancement)
```

### Automated Testing (Future Enhancement)

```typescript
// Example E2E test with Playwright (future implementation)
import { test, expect } from '@playwright/test';

test.describe('Navigation Menu', () => {
  test('should open and close dropdowns', async ({ page }) => {
    await page.goto('http://localhost:3000');

    // Click Analytics dropdown
    await page.click('text=Analytics');

    // Verify dropdown is visible
    await expect(page.locator('a:has-text("Trends")')).toBeVisible();

    // Click outside
    await page.click('body');

    // Verify dropdown is closed
    await expect(page.locator('a:has-text("Trends")')).not.toBeVisible();
  });

  test('should navigate to dashboard', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('text=Dashboard');
    await expect(page).toHaveURL('/dashboard');
  });
});
```

---

## Troubleshooting Guide

### Issue: Dropdown Doesn't Open

#### Symptoms
- Clicking dropdown button has no effect
- Dropdown never appears

#### Diagnosis Steps
```typescript
// 1. Check state is being set
console.log('isOpen before:', isOpen);
onClick={() => {
  const newState = !isOpen;
  console.log('Setting isOpen to:', newState);
  setIsOpen(newState);
}}

// 2. Check conditional render
{isOpen && (
  <div>Dropdown content</div>
)}
// If isOpen is true, does <div> appear in DOM?

// 3. Check CSS isn't hiding it
// Use browser DevTools to inspect element
```

#### Common Causes & Fixes

**Cause 1: State not updating**
```typescript
// WRONG: Using state variable instead of setter
onClick={() => isOpen = !isOpen} // ❌

// RIGHT: Using setter function
onClick={() => setIsOpen(!isOpen)} // ✅
```

**Cause 2: Missing conditional render**
```typescript
// WRONG: Dropdown always exists, just hidden
<div className={isOpen ? 'visible' : 'hidden'}> // ❌

// RIGHT: Conditional rendering
{isOpen && <div>...</div>} // ✅
```

**Cause 3: CSS z-index issue**
```typescript
// Ensure dropdown has higher z-index than surrounding elements
className="absolute ... z-50" // Add z-index
```

---

### Issue: Multiple Dropdowns Open Simultaneously

#### Symptoms
- Clicking one dropdown doesn't close others
- Multiple dropdowns visible at once

#### Diagnosis
This is actually **expected behavior** in the current implementation! Each `NavDropdown` component manages its own state independently.

#### If Single-Dropdown-at-a-Time Desired

**Solution: Lift State to Parent Component**

```typescript
// In ModernNav.tsx
const [openDropdown, setOpenDropdown] = useState<string | null>(null);

const handleDropdownToggle = (dropdownName: string) => {
  setOpenDropdown(openDropdown === dropdownName ? null : dropdownName);
};

// Pass to NavDropdown
<NavDropdown
  label="Analytics"
  icon={<TrendingUp />}
  items={analyticsItems}
  isOpen={openDropdown === 'analytics'}
  onToggle={() => handleDropdownToggle('analytics')}
/>

// Update NavDropdown.tsx to use props instead of internal state
interface NavDropdownProps {
  label: string;
  icon: ReactNode;
  items: Array<{ label: string; href: string }>;
  isOpen: boolean; // Now controlled by parent
  onToggle: () => void; // Parent controls state
}

const NavDropdown: React.FC<NavDropdownProps> = ({
  label, icon, items, isOpen, onToggle
}) => {
  return (
    <div className="relative">
      <button onClick={onToggle} /* ... */>
        {/* ... */}
      </button>
      {isOpen && (
        <div /* ... */>
          {/* dropdown content */}
        </div>
      )}
    </div>
  );
};
```

---

### Issue: Dropdown Doesn't Close on Outside Click

#### Symptoms
- Dropdown stays open when clicking elsewhere
- Must click dropdown button to close

#### Diagnosis
```typescript
// Check if useEffect click handler is set up
useEffect(() => {
  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  };

  document.addEventListener('mousedown', handleClickOutside);
  return () => {
    document.removeEventListener('mousedown', handleClickOutside);
  };
}, []);
```

#### Common Causes & Fixes

**Cause 1: Missing useRef**
```typescript
// WRONG: No ref attached
const NavDropdown = () => {
  // Missing: const dropdownRef = useRef<HTMLDivElement>(null);
  return <div>...</div>;
};

// RIGHT: Ref attached to container
const NavDropdown = () => {
  const dropdownRef = useRef<HTMLDivElement>(null);
  return <div ref={dropdownRef}>...</div>;
};
```

**Cause 2: Event listener not cleaned up**
```typescript
// WRONG: Memory leak - no cleanup
useEffect(() => {
  document.addEventListener('mousedown', handleClickOutside);
}, []);

// RIGHT: Cleanup function returns cleanup
useEffect(() => {
  document.addEventListener('mousedown', handleClickOutside);
  return () => document.removeEventListener('mousedown', handleClickOutside);
}, []);
```

**Cause 3: Dropdown not in DOM when clicking**
```typescript
// Ensure dropdown is child of element with dropdownRef
<div ref={dropdownRef}> {/* Ref here */}
  <button>...</button>
  {isOpen && <div>Dropdown</div>} {/* Dropdown inside ref */}
</div>
```

---

### Issue: Menu Item Link Doesn't Navigate

#### Symptoms
- Clicking link has no effect
- URL doesn't change

#### Diagnosis Steps
```bash
# 1. Check browser console for errors
# Open DevTools Console tab

# 2. Check if link is rendered
# Inspect element in DevTools

# 3. Check href attribute value
# Should match existing route
```

#### Common Causes & Fixes

**Cause 1: Wrong link type**
```typescript
// WRONG in Next.js App Router: Using Next.js 12 Link
import Link from 'next/link';
<Link href="/page"><a>Text</a></Link> // ❌

// RIGHT: Standard <a> tag or Next.js 13+ Link
<a href="/page">Text</a> // ✅
// OR
import Link from 'next/link';
<Link href="/page">Text</Link> // ✅
```

**Cause 2: Typo in href**
```typescript
// Check route matches page file
<a href="/dashbord">Dashboard</a> // ❌ Typo
<a href="/dashboard">Dashboard</a> // ✅

// Verify page exists
ls app/dashboard/page.tsx
```

**Cause 3: onClick preventing default**
```typescript
// WRONG: Preventing navigation
onClick={(e) => {
  e.preventDefault(); // ❌ Blocks navigation
  doSomething();
}}

// RIGHT: Don't prevent default for links
onClick={(e) => {
  doSomething(); // ✅ Navigation still works
}}
```

---

### Issue: Icon Not Displaying

#### Symptoms
- Blank space where icon should be
- Icon name appears as text

#### Diagnosis Steps
```bash
# 1. Check browser console for errors
# Look for import errors

# 2. Check Lucide React icon exists
# Visit https://lucide.dev/icons to verify icon name

# 3. Check import statement
```

#### Common Causes & Fixes

**Cause 1: Icon not imported**
```typescript
// WRONG: Using icon without import
<FileText className="w-4 h-4" /> // ❌ FileText undefined

// RIGHT: Import from lucide-react
import { FileText } from 'lucide-react'; // ✅
<FileText className="w-4 h-4" />
```

**Cause 2: Wrong icon name**
```typescript
// WRONG: Icon doesn't exist in Lucide
import { FileIcon } from 'lucide-react'; // ❌ No "FileIcon"

// RIGHT: Correct icon name from Lucide docs
import { FileText } from 'lucide-react'; // ✅
```

**Cause 3: Missing className**
```typescript
// WRONG: No size classes (icon may be invisible)
<FileText /> // ❌

// RIGHT: Size classes applied
<FileText className="w-4 h-4" /> // ✅
```

---

### Issue: Hover Effects Not Working

#### Symptoms
- No color change on hover
- No background change on hover

#### Diagnosis
```bash
# Check browser DevTools > Elements
# Hover over element and check applied styles
```

#### Common Causes & Fixes

**Cause 1: Missing Tailwind hover classes**
```typescript
// WRONG: No hover classes
<a className="text-slate-100 bg-slate-900"> // ❌

// RIGHT: Hover classes included
<a className="text-slate-100 hover:text-emerald-500 bg-slate-900 hover:bg-slate-800"> // ✅
```

**Cause 2: CSS specificity issue**
```typescript
// If custom CSS overrides Tailwind
// Check for conflicting styles in globals.css
```

**Cause 3: Transition not defined**
```typescript
// WRONG: Instant change (no smooth transition)
<a className="text-slate-100 hover:text-emerald-500"> // ❌

// RIGHT: Transition defined
<a className="text-slate-100 hover:text-emerald-500 transition-colors duration-200"> // ✅
```

---

### Issue: Page Shows 404 After Clicking Menu

#### Symptoms
- "404 | Page Not Found" appears
- Valid route but page doesn't load

#### Diagnosis Steps
```bash
# 1. Check page file exists at correct location
ls app/your-route/page.tsx

# 2. Check Next.js app directory structure
# Route /your-route requires /app/your-route/page.tsx

# 3. Restart dev server (sometimes needed)
npm run dev
```

#### Common Causes & Fixes

**Cause 1: Page file doesn't exist**
```bash
# Create missing page file
mkdir -p app/your-route
touch app/your-route/page.tsx
# Add page content (see "Creating New Pages")
```

**Cause 2: Wrong file name**
```bash
# WRONG: Various incorrect names
app/your-route/Your-Route.tsx     # ❌
app/your-route/index.tsx          # ❌
app/your-route/YourRoute.tsx      # ❌

# RIGHT: Must be named "page.tsx"
app/your-route/page.tsx           # ✅
```

**Cause 3: Route mismatch**
```typescript
// Link href:
<a href="/your-route">Link</a>

// File must be at:
app/your-route/page.tsx           // ✅

// Not at:
app/yourroute/page.tsx            // ❌ Mismatch
app/your_route/page.tsx           // ❌ Mismatch
```

**Cause 4: TypeScript compilation error**
```bash
# Check for errors in page file
npm run typecheck

# Fix any TypeScript errors in page.tsx
```

---

### Issue: Mobile Menu Not Working

#### Symptoms
- Hamburger icon doesn't toggle menu
- Mobile menu doesn't appear

#### Diagnosis
```typescript
// Check state in ModernNav.tsx
const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
console.log('mobileMenuOpen:', mobileMenuOpen);

// Check button onClick
onClick={() => setMobileMenuOpen(!mobileMenuOpen)}

// Check MobileMenu receives correct props
<MobileMenu
  isOpen={mobileMenuOpen}
  onClose={() => setMobileMenuOpen(false)}
  /* ... */
/>
```

#### Common Causes & Fixes

**Cause 1: State not updating**
```typescript
// WRONG: Incorrect state update
onClick={() => mobileMenuOpen = !mobileMenuOpen} // ❌

// RIGHT: Use setter function
onClick={() => setMobileMenuOpen(!mobileMenuOpen)} // ✅
```

**Cause 2: MobileMenu component not receiving props**
```typescript
// Check MobileMenu.tsx props interface
interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
  analyticsItems: Array<{ label: string; href: string }>;
  /* ... */
}

// Ensure all required props passed from ModernNav
```

**Cause 3: CSS hiding mobile menu incorrectly**
```typescript
// Check responsive classes
<div className="md:hidden"> {/* Hamburger button */}
  {/* Should be visible on mobile */}
</div>

<div className="hidden md:block"> {/* Desktop nav */}
  {/* Should be hidden on mobile */}
</div>
```

---

## Best Practices

### Code Organization Principles

#### Import Organization
```typescript
// ✅ GOOD: Organized by source
// 1. React imports
import React, { useState, useEffect, useRef } from 'react';

// 2. Next.js imports
import Link from 'next/link';
import { useRouter } from 'next/navigation';

// 3. External libraries (alphabetical)
import { ChevronDown, Home, Search, Settings } from 'lucide-react';

// 4. Internal components (alphabetical)
import MobileMenu from './MobileMenu';
import NavDropdown from './NavDropdown';

// 5. Types (if separate file)
import type { NavItem } from '@/types/navigation';
```

#### Component Structure
```typescript
// ✅ GOOD: Logical order
const MyComponent = () => {
  // 1. Hooks (useState, useEffect, etc.)
  const [state, setState] = useState();
  const ref = useRef();

  useEffect(() => {
    // Side effects
  }, []);

  // 2. Computed values
  const computedValue = state ? 'yes' : 'no';

  // 3. Event handlers
  const handleClick = () => {
    setState(newValue);
  };

  // 4. Render logic
  return (
    <div>
      {/* JSX */}
    </div>
  );
};
```

#### Array Organization
```typescript
// ✅ GOOD: Alphabetical by label (easier to find)
const menuItems = [
  { label: 'Analytics', href: '/analytics' },
  { label: 'Dashboard', href: '/dashboard' },
  { label: 'Reports', href: '/reports' },
  { label: 'Search', href: '/search' },
];

// ⚠️ ACCEPTABLE: Logical workflow order (if workflow is clear)
const menuItems = [
  { label: 'Collect', href: '/collect' },
  { label: 'Analyze', href: '/analyze' },
  { label: 'Report', href: '/report' },
];
```

---

### Icon Selection Guidelines

#### Icon Library
Use **Lucide React** exclusively for consistency:
```bash
# Browse icons at:
https://lucide.dev/icons

# Import syntax:
import { IconName } from 'lucide-react';
```

#### Size Standards
```typescript
// Desktop top-level/dropdown buttons
<Icon className="w-4 h-4" />   // 16px × 16px

// Desktop dropdown items (same size)
<Icon className="w-4 h-4" />

// Mobile menu items (slightly larger)
<Icon className="w-5 h-5" />   // 20px × 20px

// Page headers (large)
<Icon className="h-8 w-8" />   // 32px × 32px
```

#### Color Standards
```typescript
// Top-level menu items (default state)
className="text-slate-100 hover:text-emerald-500"

// Dropdown items (default state)
className="text-slate-100 hover:text-emerald-500"

// Primary actions/features (explicit color)
className="text-emerald-500"  // Main brand color

// Secondary features
className="text-blue-400"     // Blue accent

// Warning/alerts
className="text-amber-400"    // Amber for warnings

// Danger/critical
className="text-red-400"      // Red for critical items
```

#### Icon Selection by Category
```typescript
// Navigation & Wayfinding
Home         // Dashboard, home page
Menu         // Mobile menu toggle
ChevronDown  // Dropdown indicator
ChevronRight // Sub-menu indicator
ArrowLeft    // Back navigation

// Analysis & Insights
TrendingUp   // Analytics, trends
BarChart3    // Charts, reporting
PieChart     // Data visualization
Activity     // Monitoring, health

// Security & Threat Intelligence
Shield       // Security features
AlertTriangle // Warnings, threats
Bug          // Vulnerabilities
Target       // Threat intel, targeting
Lock         // Authentication, permissions

// Search & Discovery
Search       // Search functionality
Filter       // Filtering options
Database     // Data sources, graph

// Tools & Actions
Settings     // Configuration, settings
Upload       // File upload
Download     // Export, download
Plus         // Add new item
Edit         // Edit/modify
Trash2       // Delete

// Communication
MessageSquare // Chat, AI assistant
Bell          // Notifications
Mail          // Email features

// Users & Accounts
User          // User profile
Users         // Customer management
Building      // Organizations
```

---

### Naming Conventions

#### Component Files
```typescript
// ✅ GOOD: PascalCase for components
ModernNav.tsx
NavDropdown.tsx
MobileMenu.tsx

// ❌ AVOID
modern-nav.tsx      // kebab-case
modernNav.tsx       // camelCase
modern_nav.tsx      // snake_case
```

#### Variables & Functions
```typescript
// ✅ GOOD: camelCase for variables/functions
const mobileMenuOpen = useState(false);
const handleDropdownToggle = () => {};
const analyticsItems = [];

// ❌ AVOID
const mobile_menu_open  // snake_case
const HandleDropdownToggle  // PascalCase (reserved for components)
```

#### Routes & URLs
```typescript
// ✅ GOOD: kebab-case for URLs
/threat-intel
/analytics/trends
/tools/ip-lookup

// ❌ AVOID
/threatIntel        // camelCase
/threat_intel       // snake_case
/ThreatIntel        // PascalCase
```

#### Array Variables
```typescript
// ✅ GOOD: Plural for arrays, descriptive
const analyticsItems = [];
const threatIntelItems = [];
const navigationLinks = [];

// ❌ AVOID
const analytics = [];      // Not clear it's an array
const items = [];          // Too generic
const analyticsArray = []; // Redundant "Array" suffix
```

---

### Menu Design Principles

#### Logical Grouping Strategies

**Strategy 1: Workflow-Based**
```
Collect → Process → Analyze → Report
```
Example: Security Operations workflow
```
├── Ingest (collect data)
├── Investigate (process & search)
├── Analyze (trends & insights)
└── Report (export & share)
```

**Strategy 2: Feature-Based**
```
Group by technical capability
```
Example: Data tools
```
├── Search (various search types)
├── Visualization (graphs, maps)
└── Management (CRUD operations)
```

**Strategy 3: User Role-Based**
```
Group by job function
```
Example: Enterprise platform
```
├── Analyst Tools (search, investigate)
├── Manager Tools (reports, dashboards)
└── Admin Tools (settings, users)
```

#### Top-Level Item Guidelines

**Reserve Top-Level For:**
1. **High-traffic destinations** (Dashboard, Home)
2. **Flagship features** (Threat Intelligence, Analytics)
3. **Critical actions** (Search if primary function)
4. **Standalone tools** (Graph Explorer)
5. **Universal needs** (Settings)

**Move to Dropdown If:**
- Feature is related to 2+ other features
- Not accessed frequently by all users
- Part of a logical workflow sequence
- Helps reduce top-level clutter (>7 items)

#### Dropdown Design Rules

**Golden Rules:**
1. **Maximum Depth**: 1 level (no nested dropdowns)
2. **Item Count**: 3-7 items per dropdown (optimal 5)
3. **Logical Grouping**: Items must be related
4. **Clear Labels**: Descriptive, not vague
5. **Consistent Icons**: Related visual language

**When to Split Dropdown:**
```
❌ BAD: Overloaded dropdown
Analytics ▼
├── CVE Trends
├── Threat Timelines
├── Seasonality
├── Vulnerability Reports
├── Incident Reports
├── Compliance Reports
└── Custom Reports

✅ GOOD: Split into logical groups
Analytics ▼
├── CVE Trends
├── Threat Timelines
└── Seasonality

Reports ▼
├── Vulnerabilities
├── Incidents
├── Compliance
└── Custom
```

---

### Accessibility Best Practices

#### Semantic HTML
```typescript
// ✅ GOOD: Proper semantic elements
<nav>                        // Navigation wrapper
  <a href="...">Link</a>     // Links for navigation
  <button>Dropdown</button>  // Buttons for actions
</nav>

// ❌ AVOID: Non-semantic divs
<div onClick={navigate}>     // Div as link
  <span>Link</span>
</div>
```

#### ARIA Attributes
```typescript
// ✅ GOOD: ARIA for dynamic elements
<button
  aria-expanded={isOpen}           // Indicates dropdown state
  aria-haspopup="true"             // Indicates it opens a menu
  aria-label="Open analytics menu" // Screen reader text
>
  Analytics
</button>

<div
  role="menu"                      // Indicates dropdown is a menu
  aria-orientation="vertical"      // Menu orientation
>
  <a role="menuitem">Item</a>     // Each item is a menu item
</div>
```

#### Keyboard Navigation
```typescript
// ✅ GOOD: Keyboard-accessible
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Button
</button>

// Focus management
useEffect(() => {
  if (isOpen) {
    // Focus first item when dropdown opens
    dropdownRef.current?.querySelector('a')?.focus();
  }
}, [isOpen]);
```

#### Screen Reader Considerations
```typescript
// ✅ GOOD: Hidden but accessible text
<button>
  <Menu className="h-6 w-6" />
  <span className="sr-only">Open menu</span>
  {/* "sr-only" is Tailwind for screen-reader-only */}
</button>

// Skip link for keyboard users
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-0 focus:left-0 bg-emerald-500 text-white p-4"
>
  Skip to main content
</a>
```

---

### Performance Optimization

#### Code Splitting
```typescript
// ✅ GOOD: Lazy load heavy components
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false, // Don't render on server
});
```

#### Memoization
```typescript
// ✅ GOOD: Memoize expensive computations
import { useMemo } from 'react';

const filteredItems = useMemo(() => {
  return items.filter(item => item.visible);
}, [items]);

// ✅ GOOD: Memoize callback functions
import { useCallback } from 'react';

const handleClick = useCallback(() => {
  setIsOpen(!isOpen);
}, [isOpen]);
```

#### Event Handler Optimization
```typescript
// ❌ BAD: Creating new function on every render
<button onClick={() => handleClick(item.id)}>
  Click
</button>

// ✅ GOOD: Stable function reference
const handleItemClick = useCallback((id: string) => {
  handleClick(id);
}, [handleClick]);

<button onClick={() => handleItemClick(item.id)}>
  Click
</button>
```

#### CSS Performance
```typescript
// ✅ GOOD: Use Tailwind's built-in transitions
className="transition-colors duration-200"  // Smooth, optimized

// ⚠️ CAUTION: Animating expensive properties
className="transition-all"  // Can be janky on low-end devices
// Instead, specify specific properties:
className="transition-[color,background-color] duration-200"
```

---

### Documentation Standards

#### Code Comments
```typescript
// ✅ GOOD: Comment WHY, not WHAT
// Close all dropdowns when navigating to prevent orphaned menus
const handleLinkClick = () => {
  setOpenDropdown(null);
};

// ❌ BAD: Obvious comment
// This function sets the open dropdown to null
const handleLinkClick = () => {
  setOpenDropdown(null);
};
```

#### Inline Documentation
```typescript
// ✅ GOOD: Document complex logic
/**
 * Handles click outside dropdown to auto-close.
 * Uses ref to check if click target is outside the dropdown container.
 * Prevents closing when clicking on dropdown button itself.
 */
useEffect(() => {
  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  };
  document.addEventListener('mousedown', handleClickOutside);
  return () => document.removeEventListener('mousedown', handleClickOutside);
}, []);
```

#### File Headers
```typescript
// ✅ GOOD: File purpose and dependencies
/**
 * ModernNav.tsx
 *
 * Main navigation component for AEON Digital Twin platform.
 * Handles desktop and mobile navigation with dropdown menus.
 *
 * Dependencies:
 * - NavDropdown: Dropdown menu component
 * - MobileMenu: Mobile responsive menu
 * - lucide-react: Icon library
 *
 * Last Modified: 2025-11-04
 */
```

#### Update Documentation After Changes
```typescript
// ✅ REQUIRED: Update these files after menu changes
/docs/MENU_MAINTENANCE_SOP.md         // This SOP document
/docs/MENU_VERIFICATION_COMPLETE.md   // Menu structure reference
// Add comments in code for complex changes
```

---

## Version Control Workflow

### Git Workflow for Menu Changes

#### Branch Naming Convention
```bash
# Pattern: menu/<action>-<feature>
menu/add-reports-page
menu/remove-old-analytics
menu/restructure-dropdowns
menu/fix-mobile-navigation
```

#### Commit Message Standards

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature (new menu item, dropdown)
- `fix`: Bug fix (broken link, dropdown issue)
- `refactor`: Code restructure (no functional change)
- `style`: Styling changes (hover effects, colors)
- `docs`: Documentation only
- `test`: Adding tests

**Examples:**
```bash
# Adding new menu item
git commit -m "feat(menu): Add Reports page to top-level navigation

- Created /app/reports/page.tsx with dashboard view
- Added Reports link to ModernNav.tsx
- Imported FileText icon from lucide-react
- Updated mobile menu with Reports link
- Tested all navigation paths

Closes #123"

# Fixing dropdown issue
git commit -m "fix(menu): Fix Analytics dropdown not closing on outside click

- Added useEffect with click-outside detection
- Implemented dropdownRef for boundary checking
- Added cleanup function to prevent memory leaks
- Tested across Chrome, Firefox, Safari

Fixes #456"

# Restructuring menu
git commit -m "refactor(menu): Reorganize navigation into workflow-based dropdowns

- Created Investigate dropdown (Search, Graph, AI Assistant)
- Created Analyze dropdown (Trends, Reports, Observability)
- Created Manage dropdown (Documents, Customers, Tags)
- Promoted Threat Intelligence to top-level
- Updated all documentation

BREAKING CHANGE: Menu structure completely reorganized.
Users may need guidance to find moved features."
```

#### Complete Git Workflow

**Step 1: Create Feature Branch**
```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b menu/add-tools-dropdown

# Verify branch
git branch
# * menu/add-tools-dropdown
#   main
```

**Step 2: Make Changes**
```bash
# Edit files
code components/navigation/ModernNav.tsx

# Create new pages
mkdir -p app/tools/ip-lookup
code app/tools/ip-lookup/page.tsx

# Test changes
npm run dev
# Manually test navigation
npm run build
# Verify build succeeds
```

**Step 3: Stage and Commit**
```bash
# Check status
git status
# Shows modified files

# Stage related files together
git add components/navigation/ModernNav.tsx
git add app/tools/ip-lookup/page.tsx
git add app/tools/hash-checker/page.tsx
git add docs/MENU_MAINTENANCE_SOP.md

# Commit with detailed message
git commit -m "feat(menu): Add Tools dropdown with IP Lookup and Hash Checker

- Created Tools dropdown with 2 utility pages
- Implemented /tools/ip-lookup page with geolocation API
- Implemented /tools/hash-checker page with VirusTotal integration
- Added Wrench icon from lucide-react
- Updated navigation documentation
- Tested all links and functionality

Features:
- IP address geolocation lookup
- File hash reputation checking
- Mobile-responsive design
- Error handling for API failures

Related: #789"
```

**Step 4: Push to Remote**
```bash
# Push branch to remote
git push -u origin menu/add-tools-dropdown
```

**Step 5: Create Pull Request**
```bash
# Option 1: GitHub CLI
gh pr create \
  --title "Add Tools dropdown with utility pages" \
  --body "Adds new Tools dropdown with IP Lookup and Hash Checker utilities. See commit message for details."

# Option 2: GitHub Web UI
# Go to repository → Pull Requests → New Pull Request
```

**Step 6: Code Review & Merge**
```bash
# After PR approval, merge to main
git checkout main
git pull origin main

# Delete feature branch
git branch -d menu/add-tools-dropdown
git push origin --delete menu/add-tools-dropdown
```

---

### Handling Merge Conflicts

#### Common Conflict Scenarios

**Scenario 1: Multiple people editing ModernNav.tsx**
```bash
# Conflict in ModernNav.tsx
<<<<<<< HEAD (your branch)
<NavDropdown
  label="Tools"
  icon={<Wrench />}
  items={toolsItems}
/>
=======
<NavDropdown
  label="Utilities"
  icon={<Tool />}
  items={utilityItems}
/>
>>>>>>> main (main branch)
```

**Resolution:**
```bash
# 1. Understand both changes
# Your branch: Added "Tools" dropdown
# Main branch: Added "Utilities" dropdown

# 2. Decide resolution
# Option A: Keep both (if different functionality)
# Option B: Choose one (if duplicates)
# Option C: Merge into one (combine both)

# 3. Edit file to resolve
<NavDropdown
  label="Tools"
  icon={<Wrench />}
  items={[...toolsItems, ...utilityItems]}
/>

# 4. Mark as resolved
git add components/navigation/ModernNav.tsx
git commit -m "merge: Resolve Tools/Utilities dropdown conflict"
```

---

### Rollback Procedures

#### Scenario: Need to Undo Recent Menu Changes

**Option 1: Revert Single Commit**
```bash
# Find commit hash
git log --oneline
# a1b2c3d feat(menu): Add Tools dropdown
# e4f5g6h fix(menu): Fix dropdown closing

# Revert specific commit (creates new commit)
git revert a1b2c3d

# Push revert
git push origin main
```

**Option 2: Reset to Previous State (Destructive)**
```bash
# WARNING: This discards commits permanently

# Find commit to reset to
git log --oneline
# e4f5g6h fix(menu): Fix dropdown closing (keep this)
# a1b2c3d feat(menu): Add Tools dropdown (discard this)

# Reset to commit e4f5g6h
git reset --hard e4f5g6h

# Force push (DANGEROUS - coordinate with team)
git push origin main --force
```

**Option 3: Create Hotfix Branch**
```bash
# For production emergencies

# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/remove-broken-tools-menu

# Make fix
code components/navigation/ModernNav.tsx

# Commit and push
git add components/navigation/ModernNav.tsx
git commit -m "hotfix(menu): Remove broken Tools dropdown

Temporarily removing Tools dropdown due to API failures.
Will re-add after backend fix is deployed.

Incident: #999"

git push origin hotfix/remove-broken-tools-menu

# Create emergency PR and merge immediately
gh pr create --title "HOTFIX: Remove broken Tools dropdown" --body "Emergency removal of broken feature"
```

---

## Quick Reference

### Common Tasks Cheat Sheet

```bash
# ═══════════════════════════════════════════════════
# DEVELOPMENT WORKFLOW
# ═══════════════════════════════════════════════════

# Start development
npm run dev                  # Start dev server (http://localhost:3000)
npm run typecheck            # Check TypeScript errors
npm run lint                 # Check code quality
npm run build                # Test production build

# ═══════════════════════════════════════════════════
# ADDING MENU ITEMS
# ═══════════════════════════════════════════════════

# Top-level link
1. Import icon: import { IconName } from 'lucide-react';
2. Add <a href="/route">...</a> in ModernNav.tsx
3. Create page: app/route/page.tsx

# Dropdown item
1. Add to array: { label: 'Label', href: '/route' }
2. Create page: app/route/page.tsx

# New dropdown
1. Create array: const items = [{ label, href }, ...];
2. Import icon: import { Icon } from 'lucide-react';
3. Add <NavDropdown label="Label" icon={<Icon />} items={items} />
4. Create pages for all items

# ═══════════════════════════════════════════════════
# FILE LOCATIONS
# ═══════════════════════════════════════════════════

components/navigation/ModernNav.tsx    # Main navigation
components/navigation/NavDropdown.tsx  # Dropdown component
components/navigation/MobileMenu.tsx   # Mobile menu
app/{route}/page.tsx                   # Page files
docs/MENU_MAINTENANCE_SOP.md           # This document

# ═══════════════════════════════════════════════════
# GIT WORKFLOW
# ═══════════════════════════════════════════════════

git checkout -b menu/add-feature      # Create branch
# ... make changes ...
git add -A                            # Stage all changes
git commit -m "feat(menu): Message"   # Commit with message
git push -u origin menu/add-feature   # Push branch
gh pr create                          # Create pull request

# ═══════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════

# Manual testing checklist
[ ] All links navigate correctly
[ ] Dropdowns open/close properly
[ ] Mobile menu works
[ ] No 404 errors
[ ] No console errors
[ ] TypeScript compiles (npm run typecheck)
[ ] Build succeeds (npm run build)

# ═══════════════════════════════════════════════════
# TROUBLESHOOTING
# ═══════════════════════════════════════════════════

# Dropdown not opening
→ Check onClick={() => setIsOpen(!isOpen)}
→ Check {isOpen && <dropdown>}
→ Check state is defined

# Link not navigating
→ Check href="/correct-route"
→ Check page exists: ls app/route/page.tsx
→ Check no onClick preventing default

# Icon not showing
→ Check import { Icon } from 'lucide-react'
→ Check <Icon className="w-4 h-4" />
→ Check icon name exists at lucide.dev

# Page 404
→ Check page.tsx exists at correct path
→ Check route matches href exactly
→ Restart dev server: npm run dev

# Mobile menu not working
→ Check useState for mobileMenuOpen
→ Check button onClick
→ Check MobileMenu receives isOpen prop
```

---

### Code Templates Quick Access

#### Simple Top-Level Link
```typescript
<a
  href="/route"
  className="group flex items-center px-3 py-2 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-all duration-200"
>
  <Icon className="w-4 h-4 mr-2" />
  Label
</a>
```

#### Dropdown Array
```typescript
const dropdownItems = [
  { label: 'Item 1', href: '/route1' },
  { label: 'Item 2', href: '/route2' },
  { label: 'Item 3', href: '/route3' },
];
```

#### NavDropdown Usage
```typescript
<NavDropdown
  label="Dropdown Label"
  icon={<Icon className="w-4 h-4" />}
  items={dropdownItems}
/>
```

#### Basic Page Template
```typescript
'use client';

import { Icon } from 'lucide-react';

export default function Page() {
  return (
    <div className="min-h-screen bg-slate-950 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center mb-6">
          <Icon className="h-8 w-8 text-emerald-500 mr-3" />
          <h1 className="text-3xl font-bold text-slate-50">
            Page Title
          </h1>
        </div>

        <div className="bg-slate-900 rounded-lg p-6 border border-slate-800">
          {/* Content */}
        </div>
      </div>
    </div>
  );
}
```

---

### Lucide Icon Reference (Common Navigation Icons)

```typescript
// Core Navigation
Home            // Dashboard, home page
Menu            // Mobile hamburger menu
X               // Close mobile menu
ChevronDown     // Dropdown indicator (rotates when open)
ChevronRight    // Sub-item or "go to" indicator

// Features & Tools
Search          // Search functionality
TrendingUp      // Analytics, trends, growth
Shield          // Security, threat intelligence
Database        // Data management, graph
Network         // Graph explorer, connections
Settings        // Configuration, preferences
FileText        // Reports, documents
Upload          // File upload
Tag             // Tagging system
MessageSquare   // Chat, AI assistant

// Analysis & Insights
BarChart3       // Charts, analytics
PieChart        // Data visualization
Activity        // Monitoring, health, observability
Eye             // Observability, viewing
Target          // Targeting, focus, threat intel

// Actions & CRUD
Plus            // Add new item
Edit            // Edit existing item
Trash2          // Delete item
Save            // Save changes
Download        // Export, download

// Users & Access
User            // User profile
Users           // Customer management, teams
Building        // Organizations, companies
Lock            // Authentication, security

// Alerts & Status
AlertTriangle   // Warnings, alerts
AlertCircle     // Information, notices
Bug             // Bugs, vulnerabilities
CheckCircle     // Success, completed
XCircle         // Error, failed

// Tools & Utilities
Wrench          // Tools, utilities
Tool            // Tools (alternate)
Globe           // Internet, external
Clock           // Time, history, recency
Filter          // Filtering, refining
```

Full icon library: https://lucide.dev/icons

---

## Appendix: Advanced Topics

### State Management Alternatives (Future Enhancement)

If the application grows and menu state becomes complex, consider:

```typescript
// Option 1: Context API (for deeply nested components)
import { createContext, useContext } from 'react';

const MenuContext = createContext();

export const MenuProvider = ({ children }) => {
  const [openDropdown, setOpenDropdown] = useState(null);
  return (
    <MenuContext.Provider value={{ openDropdown, setOpenDropdown }}>
      {children}
    </MenuContext.Provider>
  );
};

// Option 2: Zustand (lightweight state management)
import create from 'zustand';

const useMenuStore = create((set) => ({
  openDropdown: null,
  setOpenDropdown: (dropdown) => set({ openDropdown: dropdown }),
}));
```

---

### Animation Enhancements (Future Enhancement)

```typescript
// Advanced dropdown animations with Framer Motion
import { motion, AnimatePresence } from 'framer-motion';

<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.2 }}
    >
      {/* Dropdown content */}
    </motion.div>
  )}
</AnimatePresence>
```

---

### Internationalization (Future Enhancement)

```typescript
// Menu labels with i18n
import { useTranslation } from 'next-i18next';

const ModernNav = () => {
  const { t } = useTranslation('navigation');

  return (
    <a href="/dashboard">
      <Home className="w-4 h-4 mr-2" />
      {t('dashboard')} {/* Translated label */}
    </a>
  );
};
```

---

### Analytics Integration (Future Enhancement)

```typescript
// Track navigation events
import { trackEvent } from '@/lib/analytics';

const handleNavClick = (label, href) => {
  trackEvent('navigation', 'click', label);
  // Navigation happens automatically via <a> tag
};

<a
  href={href}
  onClick={() => handleNavClick('Dashboard', '/dashboard')}
>
  Dashboard
</a>
```

---

## Document Control & Maintenance

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | 2025-11-04 | API Documentation Specialist | Complete rewrite with real implementation details, code examples, comprehensive troubleshooting |
| 1.0 | 2025-11-04 | Development Team | Initial SOP creation |

### Next Review Date
**2025-12-04** (30 days from last update)

### Document Owner
Development Team - AEON Digital Twin Platform

### Feedback & Improvements
For suggestions to improve this SOP:
1. Create issue in project repository
2. Tag with `documentation` and `menu-navigation`
3. Include specific section and improvement suggestion

---

## Contact & Support

### For Questions About:
- **Menu Functionality**: Check this SOP first, then consult team lead
- **Design Decisions**: Refer to design system documentation
- **Technical Bugs**: Create bug report in issue tracker
- **Process Improvements**: Propose changes via PR to this document

### Related Documentation
- `/docs/MENU_VERIFICATION_COMPLETE.md` - Current menu structure reference
- `/docs/DESIGN_SYSTEM.md` - UI/UX guidelines (if exists)
- `/docs/COMPONENT_LIBRARY.md` - Reusable components (if exists)

---

**End of Standard Operating Procedure**

*This document is maintained as part of the AEON Digital Twin Platform documentation suite.*
