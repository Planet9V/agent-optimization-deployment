# Dashboard UI Design Reference

## Overview

Reference dashboard design for AEON Digital Twin Cybersecurity platform front-end interface.

**Source**: `Dashboard_Sample.png`
**Theme**: Dark mode cybersecurity threat intelligence dashboard
**Purpose**: Layout and component reference for future front-end development

## Key Design Elements

### 1. Top Metrics Bar
- **6 Key Performance Indicators (KPIs)**:
  - Threat Actors: 20 (↑ 5%, 24h trend)
  - Intrusion Sets: 903 (↑ 38%, 24h trend)
  - Campaigns: 750 (↑ 27%, 24h trend)
  - Malware: 6.62K (↑ 2013, 24h trend)
  - Indicators: 430.62K (↑ 107149, 24h trend)
  - Observables: 460.65K (↑ 326265, 24h trend)
- **Design**: Card-based layout with dark background, large numbers, percentage changes, timeframe indicators
- **Color coding**: Green for positive trends

### 2. Geographic Visualizations
- **Three world/regional maps**:
  1. Targeted Regions (bar chart + regions highlighted)
  2. Targeted Countries (North America highlighted - Canada, USA, Mexico)
  3. Targeted Countries (World map - Europe, Asia, Middle East, Africa highlighted)
- **Design**: Orange/amber outlines on dark blue maps, country names labeled
- **Interactive**: Downloadable data (↓ icon)

### 3. Bar Chart Visualizations

#### Targeted Regions (Left)
- Horizontal bar charts showing geographic targeting
- Asia, Europe, Eastern Asia, Americas, etc.
- Scale: 0 to 1.2K

#### Targeted Countries (Left-Center)
- Horizontal bar charts by country
- Japan, Germany, United Kingdom, United States, France, India, etc.
- Scale: 0 to 1.6K

#### Targeted Sectors (Bottom-Left)
- Horizontal bar charts by industry
- Manufacturing, Government and Facilities, Finance, Technologies, Telecommunications, Health, etc.
- Scale: 0 to 1.8K

#### Targeted Sectors Timeline (Bottom-Center)
- Line graph showing trends over time (February to December)
- Multiple colored lines: Finance, Energy, Transport, Governments & Administration, Health
- Y-axis: 0 to 1.2K
- X-axis: Months (Feb-Dec)

### 4. Active Threat Data

#### Active Intrusion Sets (Top-Right)
- Horizontal bar chart
- APT29, FIN7, Lazarus Group, Wizard Spider, Sandworm Team, APT41, APT28, APT1, TEMP-Veles, etc.
- Scale: 0 to 1.2K
- Orange/red color scheme

#### Active Malware (Top-Right)
- Donut chart visualization
- Color-coded segments with legend:
  - TRICKBOT (turquoise)
  - EMOTET (blue)
  - Agent Tesla (cyan)
  - BADRABBIT (teal)
  - CLOP (turquoise)
  - Various others: TORSHOP, DARKSIDE, COBALT Strike, Wannabe, etc.
- Labeled percentages around the ring

### 5. Vulnerability and Tool Tracking

#### Active Vulnerabilities (Bottom-Right)
- List format with CVE IDs and counts
- CVE-2017-11882: 214
- CVE-2012-0158: 157
- CVE-2017-0199: 145
- CVE-2021-27065: 138
- CVE-2021-26855: 131
- CVE-2019-11510: 128
- CVE-2019-0708: 122

#### Active Tools (Bottom-Right)
- Donut chart similar to malware
- POWERSHELL (red ~62%)
- COMdowm (blue ~6.2%)
- LOG.exe (light blue ~5.3%)
- TOR (pink ~18.7%)
- Other segments: SILENTTRINITY, Royal Road, DMS

### 6. Regional Activity

#### Targeted Regions (Bottom-Center)
- Bar chart showing activity by continent over time
- Africa, Asia, Europe, North America, South America
- Timeline: Feb 1, 2023 to Nov 20, 2023
- Y-axis scale showing regional targeting intensity

### 7. Latest Activity Sections

#### Latest Campaigns (Bottom-Left)
- Timestamp: May 24, 2023 at 10:18:27 AM
- Campaign card: "FATA MORGANA"
- Description: "TortoiseShell's campaign which focuses on shipping and logistics companies based in Israel, aligning"

#### Latest Reports (Bottom-Center)
- List format with document icons
- Report entries:
  1. "Ranion Ransomware - Quai a..." (Feb 28, AlienVault, codeupace, NEW)
  2. "Iranian APT Imperial Kitten ba..." (Feb 28, Orange Cyber, campaigns, NEW, ORANGE)
  3. "CARBON SPIDER Embraces Bi..." (Feb 28, AlienVault, backdoor, NEW, TICKULAS)

#### Active TTPs (Bottom-Right)
- Graph showing TTP activity over time
- Multiple colored lines tracking different TTPs
- IDs shown: [T1547.001] Registry Run, [T1053.005] Powershell, [T1005] Brute Force, [T1110] System..., [T1082] Command and...

### 8. Data Sources (Bottom-Right)
- List of indicator sources with counts
- [+] sekoia: 170.49K
- [+] riskiq: 94.5K
- [+] alienaualt: 56.35K

## Color Scheme

### Primary Colors
- **Background**: Very dark blue/black (#0A0E1A approximate)
- **Cards**: Slightly lighter dark blue (#151A2E approximate)
- **Accent**: Orange/amber for highlights (#FF8C42 approximate)

### Chart Colors
- **Bar charts**: Blue gradient (#4A90E2 to #67B7F7)
- **Maps**: Orange outlines (#FF8C42) on dark blue background
- **Active threats**: Orange/red spectrum (#FF6B35 to #FF8C42)
- **Donut charts**: Multi-color spectrum (turquoise, blue, cyan, pink, red)

### Text Colors
- **Primary text**: White (#FFFFFF)
- **Secondary text**: Light gray (#8B9DC3)
- **Numbers**: White with high contrast
- **Trends**: Green for positive (#4ADE80), red for negative (if shown)

## Typography

- **Headers**: Sans-serif, bold, all caps for section titles
- **Numbers**: Large, bold for KPIs
- **Body text**: Regular sans-serif for descriptions
- **Labels**: Small, uppercase for categories

## Layout Structure

### Grid System
- **Top row**: 6 KPI cards (equal width)
- **Second row**: 3 map visualizations + 2 data panels
- **Third row**: 2 bar charts + 1 line graph + 2 data visualizations
- **Fourth row**: 3 list/activity sections + 1 graph

### Card Design
- Consistent padding
- Dark background with subtle borders
- Download icons (↓) in top-right of data panels
- Rounded corners (subtle)

## Interactive Elements

### Icons
- **Download**: ↓ symbol for data export
- **Document**: 📄 icon for reports
- **Expand**: Likely expandable cards (not shown in static image)

### Visual Indicators
- **Trend arrows**: ↑ for increases
- **Color coding**: Severity/importance via color
- **Hover states**: Likely interactive (not visible in static)

## Component Patterns

### 1. KPI Card
```
┌─────────────────┐
│ LABEL           │
│ 123.45K  ↑ 27% │
│         (24h)   │
└─────────────────┘
```

### 2. List with Bar Chart
```
┌──────────────────────────┐
│ TITLE              ↓     │
├──────────────────────────┤
│ Item 1    ████████  800  │
│ Item 2    ██████    600  │
│ Item 3    ████      400  │
└──────────────────────────┘
```

### 3. Map Visualization
```
┌──────────────────────────┐
│ TITLE              ↓     │
├──────────────────────────┤
│     [World Map]          │
│   with highlighted       │
│   regions/countries      │
└──────────────────────────┘
```

### 4. Donut Chart
```
┌──────────────────────────┐
│ TITLE              ↓     │
├──────────────────────────┤
│      ╱─────╲             │
│    ─╱   ○   ╲─   Legend │
│    │         │   • Item1 │
│    ╲─────────╱   • Item2 │
└──────────────────────────┘
```

## Responsive Considerations

- **Desktop-first design**: Optimized for large screens
- **Grid-based layout**: Allows responsive reflow
- **Card system**: Individual cards can stack on smaller screens
- **Data density**: High information density suitable for analyst workflows

## Accessibility Notes

- **Contrast**: High contrast for readability in dark mode
- **Color independence**: Should not rely solely on color for meaning
- **Text size**: Numbers and labels should be legible
- **Interactive elements**: Clear hit targets for controls

## Implementation Recommendations

### Technology Stack Suggestions
- **Framework**: React or Vue.js for component-based architecture
- **Charts**: D3.js, Chart.js, or Recharts for visualizations
- **Maps**: Leaflet or Mapbox for geographic visualizations
- **State Management**: Redux or Vuex for complex data flows
- **Styling**: Tailwind CSS or styled-components for dark theme

### Component Library
- Reusable KPI card component
- Bar chart component with customizable orientation
- Map component with overlay support
- Donut/pie chart component
- List component with inline visualizations
- Timeline/line graph component

### Data Requirements
- Real-time or near-real-time data updates
- WebSocket connections for live updates
- Efficient data aggregation for large datasets
- Caching strategy for performance
- Export functionality for all data panels

## Future Enhancements

- **Drill-down**: Click through from high-level to detailed views
- **Filtering**: Interactive filters by date range, region, threat type
- **Alerts**: Visual indicators for critical threats
- **Customization**: User-configurable dashboard layouts
- **Dark/Light mode toggle**: Theme switching capability
- **Export**: PDF/PNG export of dashboard or individual panels
- **Collaboration**: Shared views and annotations

## Reference for Implementation

When implementing the front-end dashboard:
1. Start with the KPI card component (simplest, most reusable)
2. Build the layout grid system
3. Implement individual chart components
4. Integrate with backend APIs
5. Add interactivity and state management
6. Optimize performance for large datasets
7. Test across different screen sizes
8. Implement real-time updates

This dashboard serves as an excellent reference for a professional-grade threat intelligence platform UI.
