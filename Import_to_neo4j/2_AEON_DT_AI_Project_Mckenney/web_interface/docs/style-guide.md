# VulnCheck-Inspired Design System
## AEON Digital Twin Style Guide v1.0

---

## Table of Contents
1. [Color Palette](#color-palette)
2. [Typography](#typography)
3. [Component Patterns](#component-patterns)
4. [Animations & Transitions](#animations--transitions)
5. [Spacing & Layout](#spacing--layout)
6. [Icon System](#icon-system)
7. [Status Colors](#status-colors)

---

## Color Palette

### Base Colors (OKLCH Color Space)

#### Background Colors
```css
/* Primary Background */
slate-950: oklch(12.9% 0.042 264.695)  /* #020617 equivalent */
RGB: rgb(2, 6, 23)
Usage: Main application background, body

/* Secondary Background */
slate-900: oklch(20.8% 0.042 265.755)  /* #0f172a equivalent */
RGB: rgb(15, 23, 42)
Usage: Navigation bar, card backgrounds, elevated surfaces

/* Tertiary Background */
slate-800: oklch(27.8% 0.013 260.031)  /* #1e293b equivalent */
RGB: rgb(30, 41, 59)
Usage: Secondary cards, dropdown menus, input fields
```

#### Accent Colors
```css
/* Emerald (Primary Brand Color) */
emerald-500: oklch(69.6% 0.17 162.48)  /* #10b981 equivalent */
RGB: rgb(16, 185, 129)
Usage: Primary actions, links, highlights, brand identity

emerald-400: oklch(74.6% 0.17 162.48)  /* #34d399 equivalent */
RGB: rgb(52, 211, 153)
Usage: Hover states, active elements, glow effects

emerald-600: oklch(64.2% 0.17 162.48)  /* #059669 equivalent */
RGB: rgb(5, 150, 105)
Usage: Pressed states, darker accents
```

#### Text Colors
```css
/* Primary Text */
slate-50: oklch(98.3% 0.003 264.052)  /* #f8fafc equivalent */
RGB: rgb(248, 250, 252)
Usage: Primary headings, body text, high emphasis

/* Secondary Text */
slate-300: oklch(86.5% 0.016 254.604)  /* #cbd5e1 equivalent */
RGB: rgb(203, 213, 225)
Usage: Subheadings, descriptions, medium emphasis

/* Tertiary Text */
slate-400: oklch(71.2% 0.019 256.802)  /* #94a3b8 equivalent */
RGB: rgb(148, 163, 184)
Usage: Placeholder text, disabled states, low emphasis

/* Muted Text */
slate-500: oklch(56.1% 0.016 257.417)  /* #64748b equivalent */
RGB: rgb(100, 116, 139)
Usage: Timestamps, metadata, subtle information
```

#### Border Colors
```css
/* Default Border */
border-default: oklch(35% 0.015 265)
Alpha variant: rgba(16, 185, 129, 0.2)
Usage: Standard card borders, input fields

/* Strong Border */
border-strong: oklch(45% 0.018 265)
Alpha variant: rgba(16, 185, 129, 0.4)
Usage: Hover states, active borders, focus indicators

/* Emerald Border */
border-emerald: oklch(69.6% 0.17 162.48)
Alpha variant: rgba(16, 185, 129, 0.6)
Usage: Focus states, primary highlights
```

### Severity Color System

#### Critical
```css
/* Critical Red */
DEFAULT: oklch(65% 0.24 25)  /* #ef4444 equivalent */
RGB: rgb(239, 68, 68)
Background: oklch(20% 0.08 25) → rgba(239, 68, 68, 0.2)
Border: oklch(40% 0.15 25) → rgba(239, 68, 68, 0.3)
Usage: Critical vulnerabilities, urgent alerts, error states
```

#### High
```css
/* High Orange */
DEFAULT: oklch(72% 0.18 45)  /* #fb923c equivalent */
RGB: rgb(251, 146, 60)
Background: oklch(20% 0.06 45) → rgba(251, 146, 60, 0.2)
Border: oklch(45% 0.12 45) → rgba(251, 146, 60, 0.3)
Usage: High severity issues, important warnings
```

#### Medium
```css
/* Medium Yellow */
DEFAULT: oklch(78% 0.15 85)  /* #eab308 equivalent */
RGB: rgb(234, 179, 8)
Background: oklch(22% 0.05 85) → rgba(234, 179, 8, 0.2)
Border: oklch(50% 0.10 85) → rgba(234, 179, 8, 0.3)
Usage: Medium severity, caution states
```

#### Low
```css
/* Low Green */
DEFAULT: oklch(72% 0.15 240)  /* #22c55e equivalent */
RGB: rgb(34, 197, 94)
Background: oklch(20% 0.05 240) → rgba(34, 197, 94, 0.2)
Border: oklch(45% 0.10 240) → rgba(34, 197, 94, 0.3)
Usage: Low severity, informational states
```

#### Info
```css
/* Info Emerald */
DEFAULT: oklch(70% 0.14 162)
RGB: rgb(16, 185, 129)
Background: oklch(20% 0.05 162) → rgba(16, 185, 129, 0.2)
Border: oklch(45% 0.10 162) → rgba(16, 185, 129, 0.3)
Usage: General information, neutral notifications
```

---

## Typography

### Font Stack
```css
/* System Font Stack */
font-family:
  -apple-system,
  BlinkMacSystemFont,
  'Segoe UI',
  'Roboto',
  'Oxygen',
  'Ubuntu',
  'Cantarell',
  'Fira Sans',
  'Droid Sans',
  'Helvetica Neue',
  sans-serif;

/* Features */
font-feature-settings: "cv11", "ss01";
font-variation-settings: "opsz" auto;
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

### Type Scale
```css
/* VulnCheck Type Scale */
.text-vc-xs: 0.75rem (12px) / line-height: 1rem / letter-spacing: 0.05em
.text-vc-sm: 0.875rem (14px) / line-height: 1.25rem
.text-vc-base: 1rem (16px) / line-height: 1.5rem
.text-vc-lg: 1.125rem (18px) / line-height: 1.75rem
.text-vc-xl: 1.25rem (20px) / line-height: 1.75rem
.text-vc-2xl: 1.5rem (24px) / line-height: 2rem
```

### Font Weights
```css
.font-normal: 400
.font-medium: 500
.font-semibold: 600
.font-bold: 700
```

### Usage Examples
```tsx
// Page Titles
<h1 className="text-vc-2xl font-bold text-slate-50">
  AEON Digital Twin
</h1>

// Section Headers
<h2 className="text-vc-xl font-semibold text-slate-50">
  Threat Intelligence
</h2>

// Card Titles
<h3 className="text-vc-lg font-semibold text-slate-50">
  Vulnerability Summary
</h3>

// Body Text
<p className="text-vc-base text-slate-300">
  Description text goes here
</p>

// Metadata
<span className="text-vc-sm text-slate-500">
  Last updated: 2 hours ago
</span>

// Labels
<label className="text-vc-xs uppercase tracking-wider text-slate-400">
  Status
</label>
```

---

## Component Patterns

### Cards

#### Basic Card
```tsx
<div className="modern-card">
  <h3 className="text-vc-lg font-semibold text-slate-50 mb-2">
    Card Title
  </h3>
  <p className="text-vc-base text-slate-300">
    Card content goes here
  </p>
</div>
```

**CSS Definition:**
```css
.modern-card {
  position: relative;
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.modern-card:hover {
  border-color: rgba(16, 185, 129, 0.4);
  box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
  transform: translateY(-4px);
}
```

#### Glass Effect Card
```tsx
<div className="glass-effect rounded-xl p-6">
  <h3 className="text-vc-lg font-semibold text-slate-50">
    Glass Card
  </h3>
</div>
```

**CSS Definition:**
```css
.glass-effect {
  background: oklch(25% 0.042 265 / 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid oklch(45% 0.018 265 / 0.2);
}
```

### Buttons

#### Primary Button
```tsx
<button className="modern-button">
  <Zap className="h-5 w-5" />
  <span>Primary Action</span>
</button>
```

**CSS Definition:**
```css
.modern-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: oklch(69.6% 0.17 162.48); /* emerald-500 */
  color: oklch(12.9% 0.042 264.695); /* slate-950 */
  font-weight: 600;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.modern-button:hover {
  background: oklch(74.6% 0.17 162.48); /* emerald-400 */
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
}

.modern-button:active {
  transform: scale(0.95);
}
```

#### Secondary Button
```tsx
<button className="modern-button-secondary">
  <Shield className="h-5 w-5" />
  <span>Secondary Action</span>
</button>
```

**CSS Definition:**
```css
.modern-button-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: oklch(27.8% 0.013 260.031); /* slate-800 */
  color: oklch(98.3% 0.003 264.052); /* slate-50 */
  font-weight: 600;
  border-radius: 0.5rem;
  border: 1px solid rgba(16, 185, 129, 0.3);
  transition: all 0.3s ease;
}

.modern-button-secondary:hover {
  background: oklch(37.1% 0.015 257.287); /* slate-700 */
  border-color: rgba(16, 185, 129, 0.5);
}
```

### Input Fields

#### Modern Input
```tsx
<input
  type="text"
  placeholder="Enter text..."
  className="modern-input"
/>
```

**CSS Definition:**
```css
.modern-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  color: oklch(98.3% 0.003 264.052); /* slate-50 */
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(16, 185, 129, 0.2);
  transition: all 0.3s ease;
}

.modern-input::placeholder {
  color: oklch(56.1% 0.016 257.417); /* slate-500 */
}

.modern-input:focus {
  outline: none;
  border-color: rgba(16, 185, 129, 0.6);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
```

### Dropdown Menus

#### Modern Dropdown
```tsx
<div className="modern-dropdown">
  <Link href="/analytics/threats" className="modern-dropdown-item">
    <Zap className="h-4 w-4 text-red-400" />
    <span>Threat Intelligence</span>
  </Link>
  <Link href="/analytics/trends" className="modern-dropdown-item">
    <BarChart3 className="h-4 w-4 text-emerald-400" />
    <span>Trend Analysis</span>
  </Link>
</div>
```

**CSS Definition:**
```css
.modern-dropdown {
  position: absolute;
  z-index: 50;
  margin-top: 0.5rem;
  padding: 0.5rem 0;
  border-radius: 0.75rem;
  min-width: 200px;
  background: rgba(30, 41, 59, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(16, 185, 129, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modern-dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: oklch(86.5% 0.016 254.604); /* slate-300 */
  transition: all 0.2s ease;
  cursor: pointer;
}

.modern-dropdown-item:hover {
  background: rgba(16, 185, 129, 0.1);
  color: oklch(74.6% 0.17 162.48); /* emerald-400 */
}
```

### Status Badges

#### Critical Badge
```tsx
<span className="badge-critical">
  <AlertTriangle className="h-3 w-3" />
  Critical
</span>
```

**CSS Definition:**
```css
.badge-critical {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  color: oklch(65% 0.24 25); /* red-400 */
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}
```

#### High Badge
```tsx
<span className="badge-high">
  <AlertCircle className="h-3 w-3" />
  High
</span>
```

**CSS Definition:**
```css
.badge-high {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  color: oklch(72% 0.18 45); /* orange-400 */
  background: rgba(251, 146, 60, 0.2);
  border: 1px solid rgba(251, 146, 60, 0.3);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}
```

#### Medium Badge
```tsx
<span className="badge-medium">
  <Info className="h-3 w-3" />
  Medium
</span>
```

**CSS Definition:**
```css
.badge-medium {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  color: oklch(78% 0.15 85); /* yellow-400 */
  background: rgba(234, 179, 8, 0.2);
  border: 1px solid rgba(234, 179, 8, 0.3);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}
```

#### Low Badge
```tsx
<span className="badge-low">
  <CheckCircle className="h-3 w-3" />
  Low
</span>
```

**CSS Definition:**
```css
.badge-low {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  color: oklch(72% 0.15 240); /* green-400 */
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.3);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}
```

### Navigation

#### Modern Navigation Bar
```tsx
<nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-emerald-500/20">
  <div className="max-w-7xl mx-auto px-6">
    <div className="flex items-center justify-between h-16">
      {/* Logo */}
      <Link href="/" className="flex items-center space-x-3 group">
        <div className="relative">
          <Shield className="h-8 w-8 text-emerald-500 group-hover:text-emerald-400 transition-colors duration-300" />
          <div className="absolute inset-0 blur-lg bg-emerald-500/20 group-hover:bg-emerald-500/30 transition-all duration-300" />
        </div>
        <span className="text-xl font-bold text-slate-50 group-hover:text-emerald-400 transition-colors duration-300">
          AEON Digital Twin
        </span>
      </Link>

      {/* Nav Links */}
      <div className="flex items-center space-x-1">
        <Link
          href="/dashboard"
          className="flex items-center space-x-2 px-4 py-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
        >
          <Activity className="h-5 w-5" />
          <span className="font-medium">Dashboard</span>
        </Link>
      </div>
    </div>
  </div>
</nav>
```

---

## Animations & Transitions

### Transition Durations
```css
/* Fast transitions */
.duration-vc-fast: 150ms

/* Base transitions */
.duration-vc-base: 200ms

/* Slow transitions */
.duration-vc-slow: 300ms
```

### Fade In Animation
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}
```

**Usage:**
```tsx
<div className="fade-in">
  Content that fades in
</div>
```

### Wave Animation
```css
@keyframes wave {
  0%, 100% {
    transform: translateX(0) translateY(0);
  }
  25% {
    transform: translateX(-5%) translateY(5%);
  }
  50% {
    transform: translateX(-10%) translateY(0);
  }
  75% {
    transform: translateX(-5%) translateY(-5%);
  }
}

.wave-background {
  position: fixed;
  inset: 0;
  z-index: -10;
  overflow: hidden;
  background: linear-gradient(to bottom right,
    oklch(12.9% 0.042 264.695),
    oklch(20.8% 0.042 265.755),
    oklch(12.9% 0.042 264.695)
  );
}

.wave-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0.3;
  animation: wave 20s ease-in-out infinite;
}
```

### Pulse Animation (Critical Items)
```css
@keyframes pulseCritical {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.pulse-critical {
  animation: pulseCritical 2s ease-in-out infinite;
}
```

**Usage:**
```tsx
<div className="pulse-critical">
  <AlertTriangle className="h-5 w-5 text-red-400" />
</div>
```

### Hover Effects
```css
/* Card hover lift */
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
}

/* Button hover glow */
.hover-glow:hover {
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
}

/* Scale on active */
.active-scale:active {
  transform: scale(0.95);
}
```

---

## Spacing & Layout

### Spacing Scale
```css
/* VulnCheck Spacing System */
.space-vc-1: 0.25rem (4px)
.space-vc-2: 0.5rem (8px)
.space-vc-3: 0.75rem (12px)
.space-vc-4: 1rem (16px)
.space-vc-6: 1.5rem (24px)
.space-vc-8: 2rem (32px)
.space-vc-12: 3rem (48px)
.space-vc-16: 4rem (64px)
```

### Border Radius
```css
/* VulnCheck Border Radius */
.rounded-vc-sm: 0.25rem (4px)
.rounded-vc-md: 0.5rem (8px)
.rounded-vc-lg: 0.75rem (12px)
.rounded-vc-xl: 1rem (16px)
```

### Layout Grid
```tsx
// Standard container
<div className="max-w-7xl mx-auto px-6">
  {/* Content */}
</div>

// Grid layouts
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Grid items */}
</div>

// Flex layouts
<div className="flex items-center justify-between gap-4">
  {/* Flex items */}
</div>
```

### Box Shadows
```css
/* VulnCheck Shadow System */
.shadow-vc-sm: 0 1px 2px 0 oklch(0% 0 0 / 0.3)
.shadow-vc-md: 0 4px 6px -1px oklch(0% 0 0 / 0.4), 0 2px 4px -1px oklch(0% 0 0 / 0.3)
.shadow-vc-lg: 0 10px 15px -3px oklch(0% 0 0 / 0.5), 0 4px 6px -2px oklch(0% 0 0 / 0.4)
.shadow-vc-xl: 0 20px 25px -5px oklch(0% 0 0 / 0.6), 0 10px 10px -5px oklch(0% 0 0 / 0.5)

/* Glow shadows */
.shadow-glow-emerald: 0 0 20px oklch(69.6% 0.17 162.48 / 0.3)
.shadow-glow-critical: 0 0 20px oklch(65% 0.24 25 / 0.3)
```

---

## Icon System

### Icon Library
Using **Lucide React** for consistent icon design

### Icon Sizes
```tsx
// Extra Small (12px)
<Icon className="h-3 w-3" />

// Small (16px)
<Icon className="h-4 w-4" />

// Medium (20px)
<Icon className="h-5 w-5" />

// Large (24px)
<Icon className="h-6 w-6" />

// Extra Large (32px)
<Icon className="h-8 w-8" />
```

### Common Icons
```tsx
import {
  Shield,        // Security, protection
  Database,      // Data, storage
  Search,        // Search functionality
  Activity,      // Dashboard, monitoring
  BarChart3,     // Analytics, charts
  Zap,          // Performance, actions
  FileText,     // Documents, reports
  AlertTriangle, // Critical warnings
  AlertCircle,   // High warnings
  Info,         // Information, medium
  CheckCircle,   // Success, low severity
  ChevronDown,   // Dropdown indicators
} from 'lucide-react';
```

### Icon Colors by Context
```tsx
// Critical/Danger
<AlertTriangle className="h-5 w-5 text-red-400" />

// Warning/High
<AlertCircle className="h-5 w-5 text-orange-400" />

// Caution/Medium
<Info className="h-5 w-5 text-yellow-400" />

// Success/Low
<CheckCircle className="h-5 w-5 text-green-400" />

// Brand/Primary
<Shield className="h-5 w-5 text-emerald-500" />

// Neutral
<Database className="h-5 w-5 text-slate-400" />
```

### Icon with Glow Effect
```tsx
<div className="relative">
  <Shield className="h-8 w-8 text-emerald-500" />
  <div className="absolute inset-0 blur-lg bg-emerald-500/20" />
</div>
```

---

## Status Colors

### Severity Mapping
```tsx
// Critical - Red
severity: "critical" → text-red-400, bg-red-400/20, border-red-400/30

// High - Orange
severity: "high" → text-orange-400, bg-orange-400/20, border-orange-400/30

// Medium - Yellow
severity: "medium" → text-yellow-400, bg-yellow-400/20, border-yellow-400/30

// Low - Green
severity: "low" → text-green-400, bg-green-400/20, border-green-400/30

// Info - Emerald
severity: "info" → text-emerald-400, bg-emerald-400/20, border-emerald-400/30
```

### Status Indicator Component
```tsx
const StatusIndicator = ({ severity }: { severity: string }) => {
  const statusConfig = {
    critical: {
      icon: AlertTriangle,
      className: "badge-critical",
      label: "Critical"
    },
    high: {
      icon: AlertCircle,
      className: "badge-high",
      label: "High"
    },
    medium: {
      icon: Info,
      className: "badge-medium",
      label: "Medium"
    },
    low: {
      icon: CheckCircle,
      className: "badge-low",
      label: "Low"
    }
  };

  const config = statusConfig[severity];
  const Icon = config.icon;

  return (
    <span className={config.className}>
      <Icon className="h-3 w-3" />
      {config.label}
    </span>
  );
};
```

---

## Scrollbar Styling

### Custom Scrollbar
```css
/* Scrollbar track */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(30, 41, 59, 0.5);
}

/* Scrollbar thumb */
::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.3);
  border-radius: 9999px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(16, 185, 129, 0.5);
}
```

---

## Best Practices

### 1. Consistent Use of OKLCH
Always use OKLCH color space for better perceptual uniformity:
```css
✅ CORRECT: oklch(69.6% 0.17 162.48)
❌ AVOID: #10b981 (use OKLCH equivalent)
```

### 2. Backdrop Blur for Glassmorphism
Apply backdrop-blur for modern glass effects:
```tsx
<div className="bg-slate-800/80 backdrop-blur-md">
  Glass effect content
</div>
```

### 3. Transition All Interactive Elements
```tsx
<button className="transition-all duration-300 hover:scale-105">
  Interactive Button
</button>
```

### 4. Use Semantic Color Names
```tsx
✅ CORRECT: className="bg-vulncheck-bg-primary"
✅ CORRECT: className="text-emerald-500"
❌ AVOID: className="bg-[#020617]"
```

### 5. Consistent Spacing
Use VulnCheck spacing scale for consistency:
```tsx
✅ CORRECT: className="space-vc-4 gap-vc-6"
❌ AVOID: className="space-4 gap-6" (use custom scale)
```

### 6. Icon + Text Alignment
```tsx
<div className="flex items-center gap-2">
  <Icon className="h-5 w-5" />
  <span>Label Text</span>
</div>
```

### 7. Responsive Design
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* Responsive grid */}
</div>
```

---

## Code Examples

### Complete Card Component
```tsx
import { Shield, AlertTriangle } from 'lucide-react';

const ThreatCard = ({ title, severity, description }) => {
  return (
    <div className="modern-card hover-lift">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <Shield className="h-6 w-6 text-emerald-500" />
          <h3 className="text-vc-lg font-semibold text-slate-50">
            {title}
          </h3>
        </div>
        <span className={`badge-${severity}`}>
          <AlertTriangle className="h-3 w-3" />
          {severity}
        </span>
      </div>
      <p className="text-vc-base text-slate-300">
        {description}
      </p>
    </div>
  );
};
```

### Complete Form Component
```tsx
const SearchForm = () => {
  return (
    <form className="modern-card">
      <label className="block text-vc-sm text-slate-400 mb-2">
        Search Query
      </label>
      <input
        type="text"
        placeholder="Enter search terms..."
        className="modern-input mb-4"
      />
      <div className="flex gap-3">
        <button type="submit" className="modern-button flex-1">
          <Search className="h-5 w-5" />
          Search
        </button>
        <button type="reset" className="modern-button-secondary">
          Clear
        </button>
      </div>
    </form>
  );
};
```

---

## Version History
- **v1.0** (2025-01-04): Initial VulnCheck-inspired design system documentation

---

**Generated by:** AEON Digital Twin Design Team
**Last Updated:** 2025-01-04
