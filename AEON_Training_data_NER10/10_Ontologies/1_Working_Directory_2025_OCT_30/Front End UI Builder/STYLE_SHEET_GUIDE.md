# AEON Digital Twin - Style Sheet & Design System Guide

**Document Version:** 2.0.0
**Created:** 2025-01-04
**Design System:** VulnCheck-Inspired Dark Theme
**Color Space:** OKLCH (Perceptually Uniform)
**Purpose:** Complete styling specification for consistent UI implementation

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Color System (OKLCH)](#color-system-oklch)
3. [Typography](#typography)
4. [Component Styling](#component-styling)
5. [Animation System](#animation-system)
6. [Spacing & Layout](#spacing--layout)
7. [Icon System](#icon-system)
8. [Tailwind Configuration](#tailwind-configuration)
9. [Global CSS](#global-css)
10. [Best Practices](#best-practices)

---

## 1. Design Philosophy

### 1.1 Core Principles

**Dark-First Design:**
- Deep slate backgrounds (OKLCH-based) for reduced eye strain
- High contrast text for readability
- Emerald accents for brand identity and CTAs

**Cybersecurity Aesthetic:**
- Professional and technical appearance
- Severity-based color coding (Critical/High/Medium/Low)
- Glass morphism effects for depth
- Subtle animations for engagement without distraction

**Accessibility:**
- WCAG 2.1 AA compliant contrast ratios
- Perceptually uniform colors (OKLCH) for consistency
- Clear visual hierarchy
- Keyboard navigation support

### 1.2 Design Inspiration

**Primary Inspiration:** VulnCheck.com
- Dark slate background with emerald accents
- Professional cybersecurity UI patterns
- Modern glassmorphism effects
- Severity-based color coding

---

## 2. Color System (OKLCH)

### 2.1 Why OKLCH?

OKLCH (Oklab Lightness Chroma Hue) provides:
- **Perceptual Uniformity:** Colors with same lightness appear equally bright
- **Consistent Visual Weight:** Easier to maintain hierarchy
- **Better Gradients:** Smooth color transitions
- **Accessibility:** Predictable contrast ratios

### 2.2 Background Colors

```css
/* Primary Background (Body) */
--bg-primary: oklch(12.9% 0.042 264.695);
/* Equivalent to slate-950: #020617 */
/* RGB: rgb(2, 6, 23) */
/* Usage: Main application background, body element */

/* Secondary Background (Cards, Navigation) */
--bg-secondary: oklch(20.8% 0.042 265.755);
/* Equivalent to slate-900: #0f172a */
/* RGB: rgb(15, 23, 42) */
/* Usage: Navigation bar, card backgrounds, elevated surfaces */

/* Tertiary Background (Inputs, Dropdowns) */
--bg-tertiary: oklch(27.8% 0.013 260.031);
/* Equivalent to slate-800: #1e293b */
/* RGB: rgb(30, 41, 59) */
/* Usage: Input fields, dropdown menus, secondary cards */

/* Elevated Background (Modals, Popovers) */
--bg-elevated: oklch(37.1% 0.015 257.287);
/* Equivalent to slate-700: #334155 */
/* RGB: rgb(51, 65, 85) */
/* Usage: Modal backgrounds, popovers, tooltips */
```

### 2.3 Brand Colors (Emerald Accent)

```css
/* Primary Emerald (Brand Color) */
--emerald-500: oklch(69.6% 0.17 162.48);
/* Equivalent to emerald-500: #10b981 */
/* RGB: rgb(16, 185, 129) */
/* Usage: Primary CTAs, links, brand accents, focus states */

/* Lighter Emerald (Hover State) */
--emerald-400: oklch(74.6% 0.17 162.48);
/* Equivalent to emerald-400: #34d399 */
/* RGB: rgb(52, 211, 153) */
/* Usage: Hover states, active elements, glow effects */

/* Darker Emerald (Pressed State) */
--emerald-600: oklch(64.2% 0.17 162.48);
/* Equivalent to emerald-600: #059669 */
/* RGB: rgb(5, 150, 105) */
/* Usage: Pressed button states, darker accents */

/* Emerald with Alpha (Overlays) */
--emerald-500-alpha-10: oklch(69.6% 0.17 162.48 / 0.1);
--emerald-500-alpha-20: oklch(69.6% 0.17 162.48 / 0.2);
--emerald-500-alpha-40: oklch(69.6% 0.17 162.48 / 0.4);
/* Usage: Background overlays, hover states, subtle highlights */
```

### 2.4 Text Colors

```css
/* Primary Text (High Emphasis) */
--text-primary: oklch(98.3% 0.003 264.052);
/* Equivalent to slate-50: #f8fafc */
/* RGB: rgb(248, 250, 252) */
/* Usage: Headings, primary body text, high emphasis content */

/* Secondary Text (Medium Emphasis) */
--text-secondary: oklch(86.5% 0.016 254.604);
/* Equivalent to slate-300: #cbd5e1 */
/* RGB: rgb(203, 213, 225) */
/* Usage: Subheadings, descriptions, medium emphasis */

/* Tertiary Text (Low Emphasis) */
--text-tertiary: oklch(71.2% 0.019 256.802);
/* Equivalent to slate-400: #94a3b8 */
/* RGB: rgb(148, 163, 184) */
/* Usage: Placeholder text, disabled states, low emphasis */

/* Muted Text (Metadata) */
--text-muted: oklch(56.1% 0.016 257.417);
/* Equivalent to slate-500: #64748b */
/* RGB: rgb(100, 116, 139) */
/* Usage: Timestamps, metadata, subtle information */
```

### 2.5 Severity Colors (Cybersecurity)

```css
/* Critical Severity (Red) */
--severity-critical: oklch(65% 0.24 25);
/* Equivalent to red-400: #ef4444 */
/* RGB: rgb(239, 68, 68) */
/* Background: oklch(20% 0.08 25) → rgba(239, 68, 68, 0.2) */
/* Border: oklch(40% 0.15 25) → rgba(239, 68, 68, 0.3) */
/* Usage: Critical CVEs, urgent alerts, error states */

/* High Severity (Orange) */
--severity-high: oklch(72% 0.18 45);
/* Equivalent to orange-400: #fb923c */
/* RGB: rgb(251, 146, 60) */
/* Background: oklch(20% 0.06 45) → rgba(251, 146, 60, 0.2) */
/* Border: oklch(45% 0.12 45) → rgba(251, 146, 60, 0.3) */
/* Usage: High severity issues, important warnings */

/* Medium Severity (Yellow) */
--severity-medium: oklch(78% 0.15 85);
/* Equivalent to yellow-400: #eab308 */
/* RGB: rgb(234, 179, 8) */
/* Background: oklch(22% 0.05 85) → rgba(234, 179, 8, 0.2) */
/* Border: oklch(50% 0.10 85) → rgba(234, 179, 8, 0.3) */
/* Usage: Medium severity, caution states */

/* Low Severity (Green) */
--severity-low: oklch(72% 0.15 240);
/* Equivalent to green-400: #22c55e */
/* RGB: rgb(34, 197, 94) */
/* Background: oklch(20% 0.05 240) → rgba(34, 197, 94, 0.2) */
/* Border: oklch(45% 0.10 240) → rgba(34, 197, 94, 0.3) */
/* Usage: Low severity, informational states */

/* Info Severity (Emerald) */
--severity-info: oklch(70% 0.14 162);
/* Similar to emerald but slightly adjusted */
/* RGB: rgb(16, 185, 129) */
/* Background: oklch(20% 0.05 162) → rgba(16, 185, 129, 0.2) */
/* Border: oklch(45% 0.10 162) → rgba(16, 185, 129, 0.3) */
/* Usage: General information, neutral notifications */
```

### 2.6 Border Colors

```css
/* Default Border */
--border-default: oklch(35% 0.015 265);
/* Alpha: rgba(16, 185, 129, 0.2) */
/* Usage: Standard card borders, input fields */

/* Strong Border (Hover/Focus) */
--border-strong: oklch(45% 0.018 265);
/* Alpha: rgba(16, 185, 129, 0.4) */
/* Usage: Hover states, active borders, focus indicators */

/* Emerald Border (Focus States) */
--border-emerald: oklch(69.6% 0.17 162.48);
/* Alpha: rgba(16, 185, 129, 0.6) */
/* Usage: Focus states, primary highlights */
```

---

## 3. Typography

### 3.1 Font Stack

```css
/* System Font Stack for Performance */
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

/* OpenType Features */
font-feature-settings: "cv11", "ss01";
font-variation-settings: "opsz" auto;

/* Font Smoothing */
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

### 3.2 Type Scale

```css
/* VulnCheck Custom Type Scale */
.text-vc-xs {
  font-size: 0.75rem;      /* 12px */
  line-height: 1rem;        /* 16px */
  letter-spacing: 0.05em;   /* Improved readability for small text */
}

.text-vc-sm {
  font-size: 0.875rem;     /* 14px */
  line-height: 1.25rem;     /* 20px */
}

.text-vc-base {
  font-size: 1rem;          /* 16px */
  line-height: 1.5rem;      /* 24px */
}

.text-vc-lg {
  font-size: 1.125rem;      /* 18px */
  line-height: 1.75rem;     /* 28px */
}

.text-vc-xl {
  font-size: 1.25rem;       /* 20px */
  line-height: 1.75rem;     /* 28px */
}

.text-vc-2xl {
  font-size: 1.5rem;        /* 24px */
  line-height: 2rem;        /* 32px */
}

.text-vc-3xl {
  font-size: 1.875rem;      /* 30px */
  line-height: 2.25rem;     /* 36px */
}

.text-vc-4xl {
  font-size: 2.25rem;       /* 36px */
  line-height: 2.5rem;      /* 40px */
}
```

### 3.3 Font Weights

```css
.font-normal { font-weight: 400; }   /* Body text */
.font-medium { font-weight: 500; }   /* Emphasized text */
.font-semibold { font-weight: 600; } /* Subheadings */
.font-bold { font-weight: 700; }     /* Headings */
```

### 3.4 Typography Usage Examples

```tsx
// Page Title
<h1 className="text-vc-4xl font-bold text-slate-50">
  AEON Digital Twin
</h1>

// Section Header
<h2 className="text-vc-2xl font-semibold text-slate-50">
  Threat Intelligence
</h2>

// Card Title
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

## 4. Component Styling

### 4.1 Cards

#### Modern Card (Base Pattern)
```css
.modern-card {
  position: relative;
  border-radius: 0.75rem;       /* 12px */
  padding: 1.5rem;               /* 24px */
  transition: all 0.3s ease;
  background: rgba(30, 41, 59, 0.8);     /* slate-800 with 80% opacity */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(16, 185, 129, 0.2); /* emerald border */
}

.modern-card:hover {
  border-color: rgba(16, 185, 129, 0.4);
  box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
  transform: translateY(-4px);
}
```

#### Glass Effect Card
```css
.glass-effect {
  background: oklch(25% 0.042 265 / 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid oklch(45% 0.018 265 / 0.2);
}
```

#### Card Component (Tailwind)
```tsx
<div className="
  rounded-xl p-6
  bg-slate-800/80 backdrop-blur-md
  border border-emerald-500/20
  transition-all duration-300
  hover:border-emerald-500/40
  hover:shadow-lg hover:shadow-emerald-500/10
  hover:-translate-y-1
">
  <h3 className="text-vc-lg font-semibold text-slate-50 mb-2">
    Card Title
  </h3>
  <p className="text-vc-base text-slate-300">
    Card content
  </p>
</div>
```

### 4.2 Buttons

#### Primary Button
```css
.modern-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: oklch(69.6% 0.17 162.48);  /* emerald-500 */
  color: oklch(12.9% 0.042 264.695);     /* slate-950 text */
  font-weight: 600;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.modern-button:hover {
  background: oklch(74.6% 0.17 162.48);  /* emerald-400 */
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
}

.modern-button:active {
  transform: scale(0.95);
}
```

#### Secondary Button
```css
.modern-button-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: oklch(27.8% 0.013 260.031); /* slate-800 */
  color: oklch(98.3% 0.003 264.052);      /* slate-50 text */
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

#### Button Component (Tailwind)
```tsx
// Primary Button
<button className="
  inline-flex items-center gap-2
  px-6 py-3 rounded-lg
  bg-emerald-500 text-slate-950
  font-semibold
  transition-all duration-300
  hover:bg-emerald-400
  hover:shadow-lg hover:shadow-emerald-500/30
  active:scale-95
">
  <Zap className="h-5 w-5" />
  <span>Primary Action</span>
</button>

// Secondary Button
<button className="
  inline-flex items-center gap-2
  px-6 py-3 rounded-lg
  bg-slate-800 text-slate-50
  border border-emerald-500/30
  font-semibold
  transition-all duration-300
  hover:bg-slate-700
  hover:border-emerald-500/50
  active:scale-95
">
  <Shield className="h-5 w-5" />
  <span>Secondary Action</span>
</button>
```

### 4.3 Input Fields

#### Modern Input
```css
.modern-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  color: oklch(98.3% 0.003 264.052);     /* slate-50 */
  background: rgba(30, 41, 59, 0.5);     /* slate-800 transparent */
  border: 1px solid rgba(16, 185, 129, 0.2);
  transition: all 0.3s ease;
}

.modern-input::placeholder {
  color: oklch(56.1% 0.016 257.417);     /* slate-500 */
}

.modern-input:focus {
  outline: none;
  border-color: rgba(16, 185, 129, 0.6);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
```

#### Input Component (Tailwind)
```tsx
<input
  type="text"
  placeholder="Enter text..."
  className="
    w-full px-4 py-2.5 rounded-lg
    bg-slate-800/50
    border border-emerald-500/20
    text-slate-50 placeholder:text-slate-500
    focus:outline-none
    focus:border-emerald-500/60
    focus:ring-4 focus:ring-emerald-500/10
    transition-all duration-200
  "
/>
```

### 4.4 Status Badges

#### Badge Styles
```css
/* Critical Badge */
.badge-critical {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  color: oklch(65% 0.24 25);             /* red text */
  background: rgba(239, 68, 68, 0.2);    /* red background */
  border: 1px solid rgba(239, 68, 68, 0.3); /* red border */
  border-radius: 9999px;                 /* fully rounded */
  font-size: 0.75rem;
  font-weight: 600;
}

/* High Badge */
.badge-high {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  color: oklch(72% 0.18 45);             /* orange text */
  background: rgba(251, 146, 60, 0.2);
  border: 1px solid rgba(251, 146, 60, 0.3);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Medium Badge */
.badge-medium {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  color: oklch(78% 0.15 85);             /* yellow text */
  background: rgba(234, 179, 8, 0.2);
  border: 1px solid rgba(234, 179, 8, 0.3);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Low Badge */
.badge-low {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  color: oklch(72% 0.15 240);            /* green text */
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.3);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}
```

#### Badge Component (Tailwind)
```tsx
// Critical Badge
<span className="
  inline-flex items-center gap-1.5
  px-2.5 py-1 rounded-full
  bg-red-400/20 text-red-400
  border border-red-400/30
  text-xs font-semibold
">
  <AlertTriangle className="h-3 w-3" />
  Critical
</span>

// High Badge
<span className="
  inline-flex items-center gap-1.5
  px-2.5 py-1 rounded-full
  bg-orange-400/20 text-orange-400
  border border-orange-400/30
  text-xs font-semibold
">
  <AlertCircle className="h-3 w-3" />
  High
</span>
```

### 4.5 Dropdown Menus

#### Modern Dropdown
```css
.modern-dropdown {
  position: absolute;
  z-index: 50;
  margin-top: 0.5rem;
  padding: 0.5rem 0;
  border-radius: 0.75rem;
  min-width: 200px;
  background: rgba(30, 41, 59, 0.95);   /* slate-800 */
  backdrop-filter: blur(12px);
  border: 1px solid rgba(16, 185, 129, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modern-dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: oklch(86.5% 0.016 254.604);    /* slate-300 */
  transition: all 0.2s ease;
  cursor: pointer;
}

.modern-dropdown-item:hover {
  background: rgba(16, 185, 129, 0.1);
  color: oklch(74.6% 0.17 162.48);      /* emerald-400 */
}
```

### 4.6 Navigation Bar

```tsx
// ModernNav Component
<nav className="
  fixed top-0 left-0 right-0 z-50
  bg-slate-900/80 backdrop-blur-md
  border-b border-emerald-500/20
">
  <div className="max-w-7xl mx-auto px-6">
    <div className="flex items-center justify-between h-16">
      {/* Logo */}
      <Link href="/" className="flex items-center space-x-3 group">
        <div className="relative">
          <Shield className="h-8 w-8 text-emerald-500 group-hover:text-emerald-400 transition-colors" />
          <div className="absolute inset-0 blur-lg bg-emerald-500/20 group-hover:bg-emerald-500/30 transition-all" />
        </div>
        <span className="text-xl font-bold text-slate-50 group-hover:text-emerald-400 transition-colors">
          AEON Digital Twin
        </span>
      </Link>

      {/* Nav Links */}
      <div className="flex items-center space-x-1">
        <Link
          href="/dashboard"
          className="
            flex items-center space-x-2
            px-4 py-2 rounded-lg
            text-slate-300
            hover:text-emerald-400
            hover:bg-emerald-500/10
            transition-all duration-200
          "
        >
          <Activity className="h-5 w-5" />
          <span className="font-medium">Dashboard</span>
        </Link>
        {/* Additional nav items */}
      </div>
    </div>
  </div>
</nav>
```

---

## 5. Animation System

### 5.1 Keyframe Animations

```css
/* Wave Animation (Background) */
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

.wave {
  animation: wave 20s ease-in-out infinite;
}

/* Pulse Animation (Critical Items) */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.pulse-critical {
  animation: pulse-slow 2s ease-in-out infinite;
}

/* Fade In Animation */
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

/* Slide Up Animation */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-up {
  animation: slideUp 0.3s ease-out;
}

/* Slide Down Animation */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-down {
  animation: slideDown 0.3s ease-out;
}
```

### 5.2 Transition Durations

```css
/* Fast transitions (interactions) */
.duration-vc-fast {
  transition-duration: 150ms;
}

/* Base transitions (default) */
.duration-vc-base {
  transition-duration: 200ms;
}

/* Slow transitions (animations) */
.duration-vc-slow {
  transition-duration: 300ms;
}
```

### 5.3 Hover Effects

```css
/* Card Hover Lift */
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
}

/* Button Hover Glow */
.hover-glow:hover {
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
}

/* Scale on Active */
.active-scale:active {
  transform: scale(0.95);
}

/* Icon Glow Effect */
.icon-glow {
  position: relative;
}

.icon-glow::before {
  content: '';
  position: absolute;
  inset: 0;
  background: inherit;
  filter: blur(16px);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.icon-glow:hover::before {
  opacity: 0.5;
}
```

### 5.4 WaveBackground Component

```tsx
'use client';

export function WaveBackground() {
  return (
    <div className="fixed inset-0 z-0 overflow-hidden">
      {/* Base gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950" />

      {/* Wave layers */}
      <div className="absolute inset-0">
        {/* Wave 1 */}
        <div
          className="absolute w-full h-full opacity-30"
          style={{
            background: 'radial-gradient(circle at 20% 50%, oklch(69.6% 0.17 162.48 / 0.15), transparent 50%)',
            animation: 'wave 20s ease-in-out infinite',
          }}
        />

        {/* Wave 2 */}
        <div
          className="absolute w-full h-full opacity-30"
          style={{
            background: 'radial-gradient(circle at 80% 50%, oklch(69.6% 0.17 162.48 / 0.1), transparent 50%)',
            animation: 'wave 25s ease-in-out infinite reverse',
          }}
        />

        {/* Wave 3 */}
        <div
          className="absolute w-full h-full opacity-20"
          style={{
            background: 'radial-gradient(circle at 50% 80%, oklch(69.6% 0.17 162.48 / 0.08), transparent 50%)',
            animation: 'wave 15s ease-in-out infinite',
          }}
        />
      </div>
    </div>
  );
}
```

---

## 6. Spacing & Layout

### 6.1 Spacing Scale

```css
/* VulnCheck Custom Spacing */
.space-vc-1 { margin/padding: 0.25rem; }  /* 4px */
.space-vc-2 { margin/padding: 0.5rem; }   /* 8px */
.space-vc-3 { margin/padding: 0.75rem; }  /* 12px */
.space-vc-4 { margin/padding: 1rem; }     /* 16px */
.space-vc-6 { margin/padding: 1.5rem; }   /* 24px */
.space-vc-8 { margin/padding: 2rem; }     /* 32px */
.space-vc-12 { margin/padding: 3rem; }    /* 48px */
.space-vc-16 { margin/padding: 4rem; }    /* 64px */
```

### 6.2 Border Radius

```css
/* VulnCheck Border Radius */
.rounded-vc-sm { border-radius: 0.25rem; }  /* 4px */
.rounded-vc-md { border-radius: 0.5rem; }   /* 8px */
.rounded-vc-lg { border-radius: 0.75rem; }  /* 12px */
.rounded-vc-xl { border-radius: 1rem; }     /* 16px */
```

### 6.3 Box Shadows

```css
/* VulnCheck Shadow System */
.shadow-vc-sm {
  box-shadow: 0 1px 2px 0 oklch(0% 0 0 / 0.3);
}

.shadow-vc-md {
  box-shadow:
    0 4px 6px -1px oklch(0% 0 0 / 0.4),
    0 2px 4px -1px oklch(0% 0 0 / 0.3);
}

.shadow-vc-lg {
  box-shadow:
    0 10px 15px -3px oklch(0% 0 0 / 0.5),
    0 4px 6px -2px oklch(0% 0 0 / 0.4);
}

.shadow-vc-xl {
  box-shadow:
    0 20px 25px -5px oklch(0% 0 0 / 0.6),
    0 10px 10px -5px oklch(0% 0 0 / 0.5);
}

/* Glow Shadows */
.shadow-glow-emerald {
  box-shadow: 0 0 20px oklch(69.6% 0.17 162.48 / 0.3);
}

.shadow-glow-critical {
  box-shadow: 0 0 20px oklch(65% 0.24 25 / 0.3);
}
```

### 6.4 Layout Grids

```tsx
// Standard Container
<div className="max-w-7xl mx-auto px-6">
  {/* Content */}
</div>

// 3-Column Grid (Responsive)
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Grid items */}
</div>

// 4-Column Grid (Dashboard Metrics)
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Metrics cards */}
</div>

// Flex Layout
<div className="flex items-center justify-between gap-4">
  {/* Flex items */}
</div>
```

---

## 7. Icon System

### 7.1 Icon Library

**Primary:** Lucide React (1000+ modern icons)

```bash
npm install lucide-react
```

### 7.2 Icon Sizes

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

### 7.3 Icon Colors by Context

```tsx
import {
  Shield,
  Database,
  Search,
  Activity,
  BarChart3,
  Zap,
  FileText,
  AlertTriangle,
  AlertCircle,
  Info,
  CheckCircle,
  ChevronDown,
} from 'lucide-react';

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

### 7.4 Icon with Glow Effect

```tsx
<div className="relative">
  <Shield className="h-8 w-8 text-emerald-500" />
  <div className="absolute inset-0 blur-lg bg-emerald-500/20" />
</div>
```

---

## 8. Tailwind Configuration

### 8.1 tailwind.config.ts

```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // VulnCheck Custom Colors (OKLCH)
        vulncheck: {
          'bg-primary': 'oklch(12.9% 0.042 264.695)',
          'bg-secondary': 'oklch(20.8% 0.042 265.755)',
          'bg-tertiary': 'oklch(27.8% 0.013 260.031)',
          'bg-elevated': 'oklch(37.1% 0.015 257.287)',

          'emerald-400': 'oklch(74.6% 0.17 162.48)',
          'emerald-500': 'oklch(69.6% 0.17 162.48)',
          'emerald-600': 'oklch(64.2% 0.17 162.48)',

          'text-primary': 'oklch(98.3% 0.003 264.052)',
          'text-secondary': 'oklch(86.5% 0.016 254.604)',
          'text-tertiary': 'oklch(71.2% 0.019 256.802)',
          'text-muted': 'oklch(56.1% 0.016 257.417)',

          'severity-critical': 'oklch(65% 0.24 25)',
          'severity-high': 'oklch(72% 0.18 45)',
          'severity-medium': 'oklch(78% 0.15 85)',
          'severity-low': 'oklch(72% 0.15 240)',
          'severity-info': 'oklch(70% 0.14 162)',
        },
      },
      animation: {
        'wave': 'wave 20s ease-in-out infinite',
        'pulse-slow': 'pulse-slow 3s ease-in-out infinite',
        'skeleton': 'skeleton 1.5s ease-in-out infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
      },
      keyframes: {
        wave: {
          '0%, 100%': { transform: 'translateX(0) translateY(0)' },
          '25%': { transform: 'translateX(-5%) translateY(5%)' },
          '50%': { transform: 'translateX(-10%) translateY(0)' },
          '75%': { transform: 'translateX(-5%) translateY(-5%)' },
        },
        'pulse-slow': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        skeleton: {
          '0%': { opacity: '0.5' },
          '50%': { opacity: '1' },
          '100%': { opacity: '0.5' },
        },
        fadeIn: {
          'from': { opacity: '0', transform: 'translateY(20px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          'from': { opacity: '0', transform: 'translateY(20px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          'from': { opacity: '0', transform: 'translateY(-20px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      spacing: {
        'vc-1': '0.25rem',
        'vc-2': '0.5rem',
        'vc-4': '1rem',
        'vc-8': '2rem',
        'vc-16': '4rem',
      },
      fontSize: {
        'vc-xs': ['0.75rem', { lineHeight: '1rem', letterSpacing: '0.05em' }],
        'vc-sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'vc-base': ['1rem', { lineHeight: '1.5rem' }],
        'vc-lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'vc-xl': ['1.25rem', { lineHeight: '1.75rem' }],
        'vc-2xl': ['1.5rem', { lineHeight: '2rem' }],
      },
      boxShadow: {
        'vc-sm': '0 1px 2px 0 oklch(0% 0 0 / 0.3)',
        'vc-md': '0 4px 6px -1px oklch(0% 0 0 / 0.4), 0 2px 4px -1px oklch(0% 0 0 / 0.3)',
        'vc-lg': '0 10px 15px -3px oklch(0% 0 0 / 0.5), 0 4px 6px -2px oklch(0% 0 0 / 0.4)',
        'vc-xl': '0 20px 25px -5px oklch(0% 0 0 / 0.6), 0 10px 10px -5px oklch(0% 0 0 / 0.5)',
        'glow-emerald': '0 0 20px oklch(69.6% 0.17 162.48 / 0.3)',
        'glow-critical': '0 0 20px oklch(65% 0.24 25 / 0.3)',
      },
    },
  },
  plugins: [],
};

export default config;
```

---

## 9. Global CSS

### 9.1 app/globals.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ===== GLOBAL STYLES ===== */

:root {
  /* Background Colors */
  --bg-primary: oklch(12.9% 0.042 264.695);
  --bg-secondary: oklch(20.8% 0.042 265.755);
  --bg-tertiary: oklch(27.8% 0.013 260.031);

  /* Text Colors */
  --text-primary: oklch(98.3% 0.003 264.052);
  --text-secondary: oklch(86.5% 0.016 254.604);
  --text-tertiary: oklch(71.2% 0.019 256.802);

  /* Brand Colors */
  --emerald-500: oklch(69.6% 0.17 162.48);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background: var(--bg-primary);
  color: var(--text-primary);
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
  font-feature-settings: "cv11", "ss01";
  font-variation-settings: "opsz" auto;
}

/* ===== CUSTOM SCROLLBAR ===== */

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(30, 41, 59, 0.5);
}

::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.3);
  border-radius: 9999px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(16, 185, 129, 0.5);
}

/* ===== CUSTOM UTILITIES ===== */

@layer utilities {
  .glass-effect {
    background: oklch(25% 0.042 265 / 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid oklch(45% 0.018 265 / 0.2);
  }

  .text-gradient-cyber {
    background: linear-gradient(
      135deg,
      oklch(74.6% 0.17 162.48),
      oklch(64.2% 0.17 162.48)
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .modern-card {
    @apply rounded-xl p-6 bg-slate-800/80 backdrop-blur-md border border-emerald-500/20;
    @apply transition-all duration-300;
    @apply hover:border-emerald-500/40 hover:shadow-lg hover:shadow-emerald-500/10 hover:-translate-y-1;
  }
}
```

---

## 10. Best Practices

### 10.1 Consistency Rules

1. **Always Use OKLCH:** Avoid hex colors, use OKLCH equivalents for perceptual uniformity
2. **Backdrop Blur for Glass Effects:** Apply `backdrop-blur-md` for modern glassmorphism
3. **Transition All Interactive Elements:** Add smooth transitions to buttons, cards, inputs
4. **Use Semantic Color Names:** `bg-vulncheck-bg-primary` instead of `bg-[#020617]`
5. **Consistent Spacing:** Use VulnCheck spacing scale (`space-vc-4`) for standardization
6. **Icon + Text Alignment:** Always wrap icon + text in flex container with gap

### 10.2 Accessibility Guidelines

```tsx
// Good: Proper contrast and semantic HTML
<button
  className="bg-emerald-500 text-slate-950"
  aria-label="Submit search query"
>
  <Search className="h-5 w-5" />
  <span>Search</span>
</button>

// Bad: Low contrast
<button className="bg-slate-600 text-slate-500">
  Search
</button>
```

### 10.3 Responsive Design

```tsx
// Mobile-first responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Cards */}
</div>

// Responsive padding
<div className="px-4 md:px-6 lg:px-8">
  {/* Content */}
</div>

// Responsive text size
<h1 className="text-2xl md:text-3xl lg:text-4xl">
  Title
</h1>
```

### 10.4 Performance Tips

1. **Use CSS Transforms:** Prefer `transform` over `top/left` for animations
2. **Minimize Reflows:** Batch DOM operations
3. **Use `will-change` Sparingly:** Only for animations that need it
4. **Optimize Images:** Use Next.js `<Image>` component with proper sizes
5. **Lazy Load Components:** Use `next/dynamic` for heavy client components

---

**Document Status:** COMPLETE
**Last Updated:** 2025-01-04
**Version:** 2.0.0
**Target Directory:** `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Front End UI Builder`
