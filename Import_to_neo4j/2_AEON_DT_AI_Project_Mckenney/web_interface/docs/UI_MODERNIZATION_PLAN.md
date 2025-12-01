# AEON UI Modernization Plan
**Date:** 2025-11-04
**Inspired by:** VulnCheck.com, OpenCTI
**Focus:** Frontend only - NO backend changes

---

## 🎨 Design System Enhancements

### Color System (VulnCheck-inspired)
**Implement OKLCH color space for modern, accessible colors:**

```css
/* Primary Palette - Emerald/Green for cybersecurity theme */
--emerald-50: oklch(98% 0.02 155);
--emerald-100: oklch(95% 0.05 155);
--emerald-500: oklch(65% 0.15 155);
--emerald-600: oklch(55% 0.18 155);
--emerald-900: oklch(30% 0.12 155);

/* Severity Colors */
--critical: oklch(60% 0.25 25);    /* Red for critical */
--high: oklch(70% 0.18 45);        /* Orange for high */
--medium: oklch(80% 0.15 85);      /* Yellow for medium */
--low: oklch(85% 0.10 140);        /* Green for low */
--info: oklch(70% 0.15 240);       /* Blue for info */

/* Dark Mode Support */
--bg-dark: oklch(18% 0.01 260);
--surface-dark: oklch(22% 0.01 260);
--text-dark: oklch(92% 0.01 260);
```

### Typography
- Modern font stack: Inter, system-ui, -apple-system
- Clear hierarchy: h1 (2.5rem), h2 (2rem), h3 (1.5rem)
- Improved readability: line-height 1.6, letter-spacing optimized

### Component Updates
1. **Cards**: Subtle shadows, rounded corners (12px), hover effects
2. **Buttons**: Gradient backgrounds on hover, trailing icons
3. **Badges**: Color-coded severity (Critical/High/Medium/Low)
4. **Icons**: SVG-based, consistent sizing, semantic colors

---

## 📊 New Features

### 1. Time-Series Analytics Dashboard
**Location:** New route `/analytics/trends`

**Features:**
- CVE discovery trends over time (line chart)
- Threat actor activity timeline (area chart)
- Attack campaign seasonality (heatmap)
- Vulnerability patching metrics (bar chart)
- Interactive date range selector
- Export to CSV/PNG functionality

**Technology:**
- Chart.js or Recharts for visualizations
- Time-series queries from Neo4j
- Aggregation by day/week/month/quarter

**Queries:**
```cypher
// CVE trends by month
MATCH (cve:CVE)
WHERE cve.published_date IS NOT NULL
WITH date(cve.published_date) as pub_date, count(cve) as cve_count
RETURN pub_date.year as year, pub_date.month as month, cve_count
ORDER BY year, month

// Threat actor activity timeline
MATCH (actor:ThreatActor)-[:CONDUCTS]->(campaign:Campaign)
WHERE campaign.start_date IS NOT NULL
RETURN actor.name, campaign.start_date, campaign.end_date, campaign.name
ORDER BY campaign.start_date DESC
```

---

### 2. Comprehensive Threat Intelligence Dashboard (POC)
**Location:** New route `/threat-intel`

**Sections:**
1. **Threat Landscape Overview**
   - Active threat actors (map visualization)
   - Recent campaigns (timeline)
   - Top targeted industries (pie chart)
   - Attack technique frequency (treemap)

2. **Vulnerability Intelligence**
   - Critical CVEs this month (table)
   - CVSS score distribution (histogram)
   - Exploit availability (badges)
   - Patch status tracking (progress bars)

3. **Attack Analytics**
   - MITRE ATT&CK heatmap (tactics × techniques)
   - Kill chain progression (sankey diagram)
   - IOC correlation (network graph)
   - Malware family relationships (force-directed graph)

4. **ICS/SCADA Focus**
   - Critical infrastructure vulnerabilities
   - Sector-specific threats
   - Asset exposure scores
   - Recommended mitigations

**Technology:**
- D3.js for advanced visualizations
- React-force-graph for network diagrams
- Nivo for statistical charts
- Tremor for dashboard layout

---

### 3. Enhanced Navigation System
**Inspired by OpenCTI sidebar navigation**

**Structure:**
```
📊 Dashboard (home)
├─ Overview
└─ Threat Intelligence

🔍 Analysis
├─ Threats
│  ├─ Threat Actors
│  ├─ Campaigns
│  └─ Incidents
├─ Arsenal
│  ├─ Malware
│  ├─ Attack Patterns
│  └─ Tools
└─ Observations
   ├─ Indicators (IOCs)
   └─ Observables

📈 Data
├─ Vulnerabilities (CVEs)
├─ Weaknesses (CWEs)
├─ Entities
└─ Relationships

🔎 Search
├─ Global Search
└─ Advanced Filters

📊 Analytics
├─ Trends
├─ Statistics
└─ Reports

⚙️ Settings
├─ Profile
├─ Customers
└─ Tags
```

**Implementation:**
- Collapsible sidebar with icons
- Active route highlighting
- Breadcrumb navigation
- Quick search in sidebar

---

### 4. Modern Component Library

**Create reusable components:**

1. **SeverityBadge.tsx**
```tsx
<SeverityBadge severity="critical" />
// Renders: Red badge with "CRITICAL" and 🔴 icon
```

2. **ThreatActorCard.tsx**
```tsx
<ThreatActorCard
  name="APT28"
  aliases={["Fancy Bear", "Sofacy"]}
  campaigns={12}
  lastActivity="2025-11-01"
/>
```

3. **CVECard.tsx**
```tsx
<CVECard
  id="CVE-2024-12345"
  cvss={9.8}
  description="..."
  affectedProducts={["Windows", "Linux"]}
/>
```

4. **TimelineChart.tsx**
```tsx
<TimelineChart
  data={campaignData}
  xAxis="date"
  yAxis="count"
  colors={["emerald", "blue"]}
/>
```

---

## 🎯 Implementation Phases

### Phase 1: Design System (1-2 hours)
- [ ] Create `/styles/design-system.css` with OKLCH colors
- [ ] Update Tailwind config with custom colors
- [ ] Create color utility classes
- [ ] Test dark mode support

### Phase 2: Navigation Enhancement (1 hour)
- [ ] Create new sidebar component
- [ ] Implement collapsible sections
- [ ] Add breadcrumb component
- [ ] Update route structure

### Phase 3: Time-Series Dashboard (2 hours)
- [ ] Create `/app/analytics/trends/page.tsx`
- [ ] Add CVE discovery trends chart
- [ ] Add threat actor activity timeline
- [ ] Add campaign seasonality heatmap
- [ ] Implement date range filters

### Phase 4: Threat Intel Dashboard POC (3 hours)
- [ ] Create `/app/threat-intel/page.tsx`
- [ ] Add threat landscape overview section
- [ ] Add vulnerability intelligence section
- [ ] Add attack analytics section
- [ ] Add ICS/SCADA focus section

### Phase 5: Component Modernization (2 hours)
- [ ] Update existing cards with new design
- [ ] Add severity badges throughout
- [ ] Improve button styling
- [ ] Add loading skeletons
- [ ] Enhance error states

### Phase 6: Testing & Polish (1 hour)
- [ ] Test all routes work
- [ ] Verify backend untouched
- [ ] Check responsive design
- [ ] Validate accessibility
- [ ] Update documentation

---

## 📁 File Structure

```
/web_interface/
├─ app/
│  ├─ analytics/
│  │  └─ trends/
│  │     └─ page.tsx          # NEW: Time-series dashboard
│  ├─ threat-intel/
│  │  └─ page.tsx              # NEW: Threat intelligence POC
│  └─ ... (existing pages)
├─ components/
│  ├─ ui/                      # shadcn/ui components
│  ├─ threat-intel/            # NEW: Threat intel components
│  │  ├─ SeverityBadge.tsx
│  │  ├─ ThreatActorCard.tsx
│  │  ├─ CVECard.tsx
│  │  └─ TimelineChart.tsx
│  ├─ navigation/              # NEW: Enhanced navigation
│  │  ├─ Sidebar.tsx
│  │  └─ Breadcrumb.tsx
│  └─ ... (existing)
├─ styles/
│  ├─ design-system.css        # NEW: Modern color system
│  └─ globals.css
└─ ... (existing)
```

---

## 🚫 Backend Protection

**RULES TO PREVENT BACKEND CHANGES:**
1. ✅ Only modify files in `/web_interface/app/` and `/web_interface/components/`
2. ✅ Only create new API routes if absolutely necessary (for new data queries)
3. ❌ NEVER modify `/agents/` (except already modified `ner_agent.py`)
4. ❌ NEVER modify docker files
5. ❌ NEVER modify database schema
6. ❌ NEVER modify Neo4j, Qdrant, MySQL configurations
7. ✅ All new features use existing API endpoints or read-only queries

---

## 📊 Success Metrics

1. **Visual Impact**: Modern, professional appearance matching VulnCheck quality
2. **Usability**: Clear navigation, intuitive organization like OpenCTI
3. **Performance**: No degradation in load times
4. **Functionality**: All existing features work + new features added
5. **Backend Safety**: Zero backend files modified (except safe frontend additions)

---

**Status:** READY TO IMPLEMENT
**Next Step:** Phase 1 - Design System
