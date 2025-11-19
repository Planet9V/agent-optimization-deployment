# VulnCheck Style Guide - Quick Reference

## 🎨 Core Colors

### Backgrounds
- **Primary**: `bg-slate-950` - oklch(12.9% 0.042 264.695)
- **Secondary**: `bg-slate-900` - oklch(20.8% 0.042 265.755)
- **Elevated**: `bg-slate-800` - oklch(27.8% 0.013 260.031)

### Accent
- **Brand**: `text-emerald-500` / `bg-emerald-500` - oklch(69.6% 0.17 162.48)
- **Hover**: `text-emerald-400` - oklch(74.6% 0.17 162.48)

### Text
- **Primary**: `text-slate-50` - oklch(98.3% 0.003 264.052)
- **Secondary**: `text-slate-300` - oklch(86.5% 0.016 254.604)
- **Muted**: `text-slate-500` - oklch(56.1% 0.016 257.417)

---

## 🚨 Severity Colors

| Severity | Class | Color | Usage |
|----------|-------|-------|-------|
| Critical | `badge-critical` | `text-red-400` | Urgent, dangerous |
| High | `badge-high` | `text-orange-400` | Important warnings |
| Medium | `badge-medium` | `text-yellow-400` | Caution states |
| Low | `badge-low` | `text-green-400` | Informational |

---

## 📦 Component Classes

### Cards
```tsx
<div className="modern-card">
  {/* Auto hover effects, glassmorphism */}
</div>
```

### Buttons
```tsx
<button className="modern-button">Primary</button>
<button className="modern-button-secondary">Secondary</button>
```

### Inputs
```tsx
<input className="modern-input" placeholder="..." />
```

### Dropdowns
```tsx
<div className="modern-dropdown">
  <a className="modern-dropdown-item">Item</a>
</div>
```

---

## ✨ Effects

### Glass Effect
```tsx
<div className="glass-effect rounded-xl p-6">
  {/* Glassmorphism */}
</div>
```

### Glow
```tsx
<div className="glow-emerald">
  {/* Emerald glow shadow */}
</div>
```

### Animations
```tsx
<div className="fade-in">Fades in</div>
<div className="pulse-critical">Pulses</div>
<div className="wave-background">Animated waves</div>
```

---

## 📐 Spacing

| Class | Size |
|-------|------|
| `space-vc-1` | 0.25rem (4px) |
| `space-vc-2` | 0.5rem (8px) |
| `space-vc-4` | 1rem (16px) |
| `space-vc-6` | 1.5rem (24px) |
| `space-vc-8` | 2rem (32px) |

---

## 🔤 Typography

| Class | Size | Usage |
|-------|------|-------|
| `text-vc-xs` | 0.75rem | Labels, tags |
| `text-vc-sm` | 0.875rem | Metadata, captions |
| `text-vc-base` | 1rem | Body text |
| `text-vc-lg` | 1.125rem | Card titles |
| `text-vc-xl` | 1.25rem | Section headers |
| `text-vc-2xl` | 1.5rem | Page titles |

---

## 🎭 Icons (Lucide React)

```tsx
import {
  Shield,        // Security
  Database,      // Data
  Search,        // Search
  Activity,      // Monitoring
  BarChart3,     // Analytics
  Zap,          // Actions
  AlertTriangle, // Critical
  AlertCircle,   // High
  Info,         // Medium
  CheckCircle,   // Low/Success
} from 'lucide-react';
```

**Sizes**: `h-3 w-3` (12px), `h-4 w-4` (16px), `h-5 w-5` (20px), `h-6 w-6` (24px), `h-8 w-8` (32px)

---

## 🎯 Common Patterns

### Status Badge
```tsx
<span className="badge-critical">
  <AlertTriangle className="h-3 w-3" />
  Critical
</span>
```

### Card with Icon Header
```tsx
<div className="modern-card">
  <div className="flex items-center gap-3 mb-4">
    <Shield className="h-6 w-6 text-emerald-500" />
    <h3 className="text-vc-lg font-semibold text-slate-50">
      Title
    </h3>
  </div>
  <p className="text-vc-base text-slate-300">
    Content
  </p>
</div>
```

### Button with Icon
```tsx
<button className="modern-button">
  <Zap className="h-5 w-5" />
  <span>Action</span>
</button>
```

### Nav Link
```tsx
<Link
  href="/path"
  className="flex items-center space-x-2 px-4 py-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
>
  <Icon className="h-5 w-5" />
  <span className="font-medium">Label</span>
</Link>
```

---

## 📚 Full Documentation
See: `/docs/style-guide.md`

**Memory Key**: `vulncheck-style-guide`
