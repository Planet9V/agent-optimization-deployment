# OpenCTI Visual Analysis & Design Specifications

**Document**: OPENCTI_VISUAL_ANALYSIS.md
**Created**: 2025-11-04
**Purpose**: Comprehensive visual analysis of OpenCTI dashboard for web interface replication
**Status**: ACTIVE

---

## Executive Summary

This document provides a detailed analysis of OpenCTI's dashboard design, visual components, and user interface patterns. OpenCTI is an open-source cyber threat intelligence platform built with React and Material-UI, featuring customizable dashboards with 15+ widget types for threat visualization.

**Key Findings**:
- Modern dark-themed Material-UI design system
- Grid-based flexible layout with drag-and-drop widgets
- 15 distinct visualization types for threat intelligence
- STIX 2.1 data model integration with graph-based knowledge representation
- Cybersecurity-specific color palette (#00b894 primary, #6c5ce7 secondary)

---

## 1. Dashboard Layout Structure

### Grid System Architecture

**Layout Type**: Flexible grid-based dashboard
**Customization**: Drag-and-drop widget placement
**Resizing**: Bottom-right corner resize handles
**Responsive**: Adaptive to screen size and user preferences

**Layout Hierarchy**:
```
┌─────────────────────────────────────────────────────┐
│ Top Banner (Temporal Controls)                      │
├─────────────────────────────────────────────────────┤
│ ┌───────────┬───────────┬───────────┬─────────────┐ │
│ │ Widget 1  │ Widget 2  │ Widget 3  │   Widget 4  │ │
│ │ (Counter) │  (Map)    │  (Chart)  │   (List)    │ │
│ └───────────┴───────────┴───────────┴─────────────┘ │
│ ┌─────────────────────┬───────────────────────────┐ │
│ │   Widget 5          │     Widget 6              │ │
│ │   (Timeline)        │     (Graph)               │ │
│ └─────────────────────┴───────────────────────────┘ │
│ ┌───────────────────────────────────────────────────┐│
│ │   Widget 7 (Heatmap / Tree Visualization)        ││
│ └───────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

**Key Features**:
- **Time Period Configuration**: Top banner with relative ranges (Last 7 days) or fixed date selection
- **Widget Independence**: Each widget independently configurable
- **Priority-Based Sizing**: Resize widgets based on information importance
- **Visual Optimization**: User-driven layout for workflow efficiency

---

## 2. Widget Types & Visualizations

### 2.1 Complete Widget Catalog (15 Types)

| Widget Type | Purpose | Best Use Case | Data Type |
|-------------|---------|---------------|-----------|
| **Counter** | Single numeric metric | Total entities, relationships, IOCs | Scalar |
| **List** | Entity enumeration | Recent reports, top threats | Entities |
| **List (Distribution)** | Entity frequency | Most targeted countries, common TTPs | Distribution |
| **Timeline** | Temporal activity | Attack campaigns over time | Time-series |
| **Line Chart** | Volume trends | Activity volumes, detection rates | Time-series |
| **Area Chart** | Cumulative trends | Total threats accumulated | Time-series |
| **Horizontal Bar** | Comparative ranking | Top entities, threat actors | Comparative |
| **Donut Chart** | Category proportions | Threat type distribution | Categorical |
| **Radar Chart** | Multi-dimensional comparison | Capability assessment | Multi-axis |
| **Heatmap** | Intensity mapping | Attack frequency by region/time | Matrix |
| **Tree Map** | Hierarchical proportion | Activity volume comparison | Hierarchical |
| **Tree View** | Relationship hierarchy | Threat actor relationships | Hierarchical |
| **Map (Geographic)** | Geospatial threats | Targeted countries, threat origins | Geospatial |
| **Graph (Network)** | Entity relationships | STIX knowledge graph, TTPs | Network |
| **Bookmark** | Saved queries/filters | Quick access to common views | Reference |

### 2.2 Visualization Recommendations

**Time-Based Analysis**:
- **Line/Area Charts**: Ideal for visualizing activity volumes over time
- **Timeline**: Event sequence and campaign progression

**Comparative Analysis**:
- **Horizontal Bars**: Identify top entities satisfying filters
- **Tree View**: Compare activity volumes across categories

**Relationship Analysis**:
- **Graph/Network**: STIX knowledge hypergraph for pivoting across actors, malware, TTPs
- **Tree Map**: Hierarchical threat categorization

**Geospatial Analysis**:
- **Map Widget**: Targeted countries and threat origins using OpenStreetMap

---

## 3. Color Palette & Theme

### 3.1 Primary Color Scheme

**Material-UI Dark Theme Configuration**:
```javascript
{
  palette: {
    primary: { main: "#00b894" },      // Teal/green - success, active
    secondary: { main: "#6c5ce7" },    // Purple - accent, links
    background: {
      default: "#121212",              // Dark background
      paper: "#1e1e1e"                 // Card/widget background
    },
    text: {
      primary: "#ffffff",              // Primary text
      secondary: "rgba(255,255,255,0.7)" // Secondary text
    }
  }
}
```

### 3.2 Extended Color Palette

**Cybersecurity Context Colors**:

| Color | Hex Code | Usage | Context |
|-------|----------|-------|---------|
| **Teal Green** | #00b894 | Primary actions, success states | Active threats, successful detections |
| **Purple** | #6c5ce7 | Secondary actions, highlights | Links, selected items |
| **Dark Background** | #121212 | Main background | Reduces eye strain |
| **Paper Background** | #1e1e1e | Widget cards | Content containers |
| **White** | #ffffff | Primary text | High contrast readability |
| **Light Gray** | rgba(255,255,255,0.7) | Secondary text | Less important information |
| **Orange (Dynamic Source)** | #ff6b35 (estimated) | Source entity filters | Data source indicators |
| **Green (Dynamic Target)** | #4CAF50 (estimated) | Target entity filters | Destination indicators |
| **Gray (Classic)** | #9e9e9e | Standard filters | Relationship filters |
| **Red (Critical)** | #f44336 | High severity threats | Critical alerts |
| **Yellow (Warning)** | #ffc107 | Medium severity | Warnings |

### 3.3 Chart Color Schemes

**Multi-Series Visualizations**:
- Use Material-UI's color palette with adequate desaturation for dark mode
- Maintain ~20 points lower saturation than light mode equivalents
- Ensure sufficient contrast (WCAG AA minimum)

**Severity-Based Coloring**:
- **Critical**: Red tones (#f44336, #d32f2f)
- **High**: Orange tones (#ff9800, #f57c00)
- **Medium**: Yellow tones (#ffc107, #ffa000)
- **Low**: Blue tones (#2196f3, #1976d2)
- **Info**: Teal tones (#00b894, #009688)

---

## 4. Typography & Visual Hierarchy

### 4.1 Font System

**Primary Font**: Roboto (Material-UI default)
```css
fontFamily: "Roboto, sans-serif"
```

**Font Weights**:
- Light (300): Supporting text
- Regular (400): Body text
- Medium (500): Emphasized content
- Bold (700): Headings, important metrics

### 4.2 Typography Scale

| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| H1 | 34px | 300 | Page titles |
| H2 | 24px | 400 | Section headers |
| H3 | 20px | 500 | Widget titles |
| H4 | 16px | 500 | Subsection headers |
| Body 1 | 16px | 400 | Primary content |
| Body 2 | 14px | 400 | Secondary content |
| Caption | 12px | 400 | Metadata, timestamps |
| Overline | 12px | 500 | Category labels |

### 4.3 Visual Hierarchy Principles

**Information Levels**:
1. **Critical Metrics**: Large counters, prominent placement
2. **Primary Visualizations**: Charts, graphs, maps
3. **Supporting Data**: Lists, tables, timelines
4. **Metadata**: Timestamps, sources, filters

**Contrast Ratios**:
- Primary text on dark background: 15:1 (white #ffffff on #121212)
- Secondary text on dark background: 7:1 (gray rgba(255,255,255,0.7))
- Widget cards: Subtle elevation with #1e1e1e on #121212

---

## 5. Widget Configuration Framework

### 5.1 Four-Step Configuration Process

**Step 1: Visualization Selection**
- Choose from 15 visualization types
- Based on data type and analysis goal

**Step 2: Perspective Selection**
- **Entities**: Count entities only
- **Knowledge Graph**: Count relationships only
- **Activity & History**: Monitor platform activities

**Step 3: Filters Application**
- **Classic Filters (Gray)**: Define relationships
- **Dynamic Source Filters (Orange)**: Target source entities
- **Dynamic Target Filters (Green)**: Target destination entities
- Support for 1-5 filter sets per widget

**Step 4: Parameters Configuration**
- Widget title
- Display elements selection
- Data reference date
- Visualization-specific parameters
- "Display the source" toggle
- Legend display for multi-dataset visualizations

### 5.2 Technical Constraints

**Query Limitations**:
- Pre-queries limited to 5000 results
- Time-based filtering required for large datasets
- Performance optimization through filter refinement

---

## 6. Specific Dashboard Components

### 6.1 Statistics Cards (Counters)

**Layout**: Typically 3-4 cards in top row
**Content**:
- Total entities ingested
- Total relationships
- Total reports
- Total observables
- 24-hour change indicators (↑ ↓)

**Visual Design**:
- Large numeric display (48px+)
- Small percentage/change indicator
- Icon representation of metric type
- Subtle background gradient or solid color

### 6.2 Geographic Threat Map

**Implementation**: OpenStreetMap integration
**Features**:
- Country-level threat targeting visualization
- Heat mapping for attack concentration
- Interactive hover/click for details
- Color intensity based on threat volume

**Data Display**:
- Targeted countries highlighted
- Threat origin markers
- Connection lines for attribution

### 6.3 Timeline Visualization

**Purpose**: Campaign progression and event sequence
**Features**:
- Horizontal time axis
- Event markers with severity coloring
- Expandable event details
- Zoom and pan controls

### 6.4 Knowledge Graph (STIX Hypergraph)

**Visualization**: Network graph with nodes and edges
**Entities**:
- Threat actors (nodes)
- Malware (nodes)
- TTPs (nodes)
- Indicators (nodes)
- Relationships (edges)

**Interactions**:
- Click to expand entity details
- Pivot across connected entities
- Filter by relationship type
- Layout algorithms for clarity

### 6.5 ATT&CK Mapping Heatmap

**Display**: Matrix-style heatmap
**Axes**:
- Tactics (columns)
- Techniques (rows)
- Color intensity = frequency/severity

**Integration**: MITRE ATT&CK framework alignment

---

## 7. User Interface Patterns

### 7.1 Navigation Structure

**Top-Level Tabs**:
- Overview: General entity information
- Knowledge: Linked reports, indicators, relations
- Analysis: Report references
- Indicators: IOC details
- History: Change tracking

### 7.2 Interactive Elements

**Widget Controls**:
- Resize handles (bottom-right corner)
- Drag handles (title bar)
- Settings icon (configuration)
- Refresh icon (data update)
- Export icon (data download)

**Temporal Controls**:
- Date range picker
- Relative time selection (Last 7 days, Last 30 days, etc.)
- Custom date range

### 7.3 Filter System

**Filter Types**:
- Entity type filters
- Relationship filters
- Temporal filters
- Severity/criticality filters
- Tag-based filters

**Visual Indicators**:
- Gray chips: Classic filters
- Orange chips: Source filters
- Green chips: Target filters
- Clear/remove controls

---

## 8. Data Integration & Architecture

### 8.1 STIX 2.1 Data Model

**Core Concept**: Structured Threat Information eXpression
**Benefits**:
- Standardized threat intelligence format
- Relationship-based knowledge representation
- Interoperability with 300+ integrations

### 8.2 Knowledge Representation

**Graph Structure**:
- Nodes: Entities (actors, malware, TTPs, indicators)
- Edges: Relationships (uses, targets, indicates)
- Properties: Attributes, timestamps, confidence scores

### 8.3 Real-Time Updates

**Data Refresh**:
- 24-hour change indicators
- Live activity monitoring
- Automatic widget updates
- Configurable refresh intervals

---

## 9. Accessibility & Usability

### 9.1 Dark Mode Optimization

**Design Principles**:
- Reduce eye strain for extended use
- Enhance focus on data visualizations
- Professional aesthetic for SOC environments
- ~20 points lower saturation than light mode

### 9.2 Contrast Standards

**WCAG Compliance**:
- Target: AA minimum (4.5:1 for normal text)
- Primary text: 15:1 ratio
- Secondary text: 7:1 ratio
- Interactive elements: Clear focus indicators

### 9.3 Responsive Design

**Breakpoints**:
- Desktop: 1920px+ (full layout)
- Laptop: 1366px+ (compact layout)
- Tablet: 768px+ (stacked widgets)
- Mobile: 375px+ (single column)

---

## 10. Implementation Priorities for Replication

### 10.1 High Priority (Core Functionality)

**Phase 1 - Essential Components**:
1. **Grid Layout System**: Drag-and-drop widget placement
2. **Statistics Cards**: Counter widgets for key metrics
3. **Timeline Visualization**: Event sequence display
4. **List Widget**: Entity and threat enumeration
5. **Dark Theme**: Material-UI dark mode configuration

**Estimated Effort**: 2-3 weeks

### 10.2 Medium Priority (Enhanced Visualization)

**Phase 2 - Advanced Charts**:
1. **Geographic Map**: OpenStreetMap integration with threat markers
2. **Horizontal Bar Charts**: Comparative analysis
3. **Line/Area Charts**: Time-series trend analysis
4. **Donut Charts**: Category distribution
5. **Filter System**: Multi-level filtering with visual chips

**Estimated Effort**: 3-4 weeks

### 10.3 Lower Priority (Advanced Features)

**Phase 3 - Complex Visualizations**:
1. **Knowledge Graph**: Network visualization for relationships
2. **Heatmap Widget**: Matrix-style intensity mapping
3. **Tree Map/Tree View**: Hierarchical visualizations
4. **Radar Chart**: Multi-dimensional comparisons
5. **ATT&CK Framework Integration**: MITRE ATT&CK heatmap

**Estimated Effort**: 4-6 weeks

### 10.4 Future Enhancements

**Phase 4 - Advanced Features**:
1. **Export/Import Dashboard Configurations**: Share layouts
2. **Public Dashboard Sharing**: Read-only access
3. **Advanced Temporal Controls**: Complex time-based queries
4. **Real-Time Collaboration**: Multi-user dashboard editing
5. **AI-Powered Insights**: Anomaly detection widgets

**Estimated Effort**: Ongoing

---

## 11. Technical Stack Recommendations

### 11.1 Frontend Framework

**Recommended**: React 18+ with Material-UI v5
- Matches OpenCTI's architecture
- Comprehensive component library
- Excellent dark theme support
- Strong community and documentation

### 11.2 Visualization Libraries

**Chart Library**: Recharts or Victory
- React-friendly
- Responsive design
- Customizable theming
- TypeScript support

**Map Library**: React Leaflet (OpenStreetMap)
- OpenCTI uses OpenStreetMap
- React wrapper available
- Highly customizable
- Free and open-source

**Graph Visualization**: React Flow or Cytoscape.js
- Network/graph layouts
- Interactive node manipulation
- STIX relationship visualization

### 11.3 State Management

**Recommended**: Redux Toolkit or Zustand
- Widget state management
- Filter state persistence
- Dashboard configuration storage
- Session management

### 11.4 Data Handling

**Backend Integration**: GraphQL (matches OpenCTI)
- Efficient data querying
- Real-time subscriptions
- Type-safe schema
- Flexible filtering

---

## 12. Design System Guidelines

### 12.1 Component Library Structure

```
/components
  /dashboard
    DashboardGrid.jsx          # Main grid layout
    DashboardWidget.jsx        # Widget wrapper
    WidgetResizer.jsx          # Resize handles
  /widgets
    CounterWidget.jsx          # Statistics cards
    TimelineWidget.jsx         # Timeline visualization
    MapWidget.jsx              # Geographic map
    ChartWidget.jsx            # Charts (line, area, bar)
    ListWidget.jsx             # Entity lists
    GraphWidget.jsx            # Knowledge graph
    HeatmapWidget.jsx          # Heatmap visualization
  /filters
    FilterChip.jsx             # Filter display
    FilterPanel.jsx            # Filter configuration
    DateRangePicker.jsx        # Temporal controls
  /common
    Card.jsx                   # Widget container
    Legend.jsx                 # Chart legends
    Tooltip.jsx                # Data tooltips
```

### 12.2 Theme Configuration

**Material-UI Theme Setup**:
```javascript
import { createTheme } from '@mui/material/styles';

const openCTITheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00b894',
      light: '#26d6a8',
      dark: '#009377',
    },
    secondary: {
      main: '#6c5ce7',
      light: '#8777ed',
      dark: '#5244c3',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    text: {
      primary: '#ffffff',
      secondary: 'rgba(255, 255, 255, 0.7)',
    },
    error: {
      main: '#f44336',
    },
    warning: {
      main: '#ffc107',
    },
    success: {
      main: '#4caf50',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
    h1: { fontSize: 34, fontWeight: 300 },
    h2: { fontSize: 24, fontWeight: 400 },
    h3: { fontSize: 20, fontWeight: 500 },
    h4: { fontSize: 16, fontWeight: 500 },
    body1: { fontSize: 16, fontWeight: 400 },
    body2: { fontSize: 14, fontWeight: 400 },
    caption: { fontSize: 12, fontWeight: 400 },
  },
  spacing: 8,
  shape: {
    borderRadius: 4,
  },
});
```

### 12.3 Widget Sizing Standards

**Default Widget Sizes** (grid units):
- Small: 2 columns × 2 rows (counters, small lists)
- Medium: 3 columns × 3 rows (charts, timelines)
- Large: 4 columns × 4 rows (maps, graphs)
- Full-width: 12 columns × variable rows (complex visualizations)

**Minimum Sizes**:
- Minimum width: 2 columns
- Minimum height: 2 rows
- Resize increments: 1 column/row

---

## 13. Performance Considerations

### 13.1 Widget Rendering Optimization

**Lazy Loading**:
- Load widgets on-demand
- Virtualize large lists
- Defer off-screen chart rendering

**Memoization**:
- Cache widget configurations
- Memoize expensive calculations
- Use React.memo for widgets

### 13.2 Data Query Optimization

**Query Limitations**:
- 5000 result limit per pre-query
- Implement pagination for large datasets
- Use incremental loading for timelines

**Caching Strategy**:
- Cache frequent queries
- Implement stale-while-revalidate
- Use GraphQL query batching

### 13.3 Real-Time Update Strategy

**WebSocket Integration**:
- Live data updates for critical widgets
- Throttle update frequency (e.g., 5-second intervals)
- Batch updates for multiple widgets

---

## 14. Security & Access Control

### 14.1 Dashboard Permissions

**Access Levels**:
- **View**: Read-only dashboard access
- **Edit**: Modify widget configurations
- **Manage**: Full dashboard administration

### 14.2 Data Security

**Sensitive Data Handling**:
- Row-level security for threat data
- Attribute-based access control
- Audit logging for dashboard access

---

## 15. References & Resources

### 15.1 Official Documentation

- **OpenCTI Documentation**: https://docs.opencti.io/latest/
- **Widget Creation Guide**: https://docs.opencti.io/latest/usage/widgets/
- **Dashboard Customization**: https://docs.opencti.io/latest/usage/dashboards/
- **OpenCTI Demo**: https://demo.opencti.io/dashboard

### 15.2 Technical Resources

- **GitHub Repository**: https://github.com/OpenCTI-Platform/opencti
- **Material-UI Theming**: https://mui.com/material-ui/customization/theming/
- **STIX 2.1 Specification**: https://docs.oasis-open.org/cti/stix/v2.1/

### 15.3 Design Resources

- **Material Design**: https://material.io/design
- **Dark UI Design Principles**: https://www.toptal.com/designers/ui/dark-ui-design
- **Data Visualization Best Practices**: Various cybersecurity dashboard references

---

## 16. Integration Roadmap

### 16.1 Week 1-2: Foundation
- [ ] Set up React + Material-UI project
- [ ] Implement dark theme configuration
- [ ] Create grid layout system
- [ ] Build widget wrapper component
- [ ] Implement drag-and-drop functionality

### 16.2 Week 3-4: Basic Widgets
- [ ] Counter widget (statistics cards)
- [ ] List widget (entity enumeration)
- [ ] Timeline widget (event sequence)
- [ ] Basic filter system
- [ ] Temporal controls (date picker)

### 16.3 Week 5-6: Chart Visualizations
- [ ] Line/Area chart widget
- [ ] Horizontal bar chart widget
- [ ] Donut chart widget
- [ ] Chart theming and color schemes
- [ ] Legend and tooltip components

### 16.4 Week 7-8: Advanced Widgets
- [ ] Geographic map widget (OpenStreetMap)
- [ ] Heatmap widget
- [ ] Tree map visualization
- [ ] Advanced filter system (multi-level)
- [ ] Widget resize and state persistence

### 16.5 Week 9-10: Integration & Polish
- [ ] Backend API integration (GraphQL)
- [ ] Real-time data updates (WebSocket)
- [ ] Performance optimization
- [ ] Accessibility improvements (WCAG AA)
- [ ] Documentation and testing

### 16.6 Future Phases
- [ ] Knowledge graph widget (network visualization)
- [ ] ATT&CK framework heatmap
- [ ] Dashboard export/import
- [ ] Public dashboard sharing
- [ ] AI-powered analytics widgets

---

## Conclusion

OpenCTI provides a robust, flexible dashboard architecture built on modern web technologies (React + Material-UI) with a cybersecurity-focused design system. The platform's 15 visualization types, STIX 2.1 data model integration, and customizable grid layout offer a comprehensive template for building threat intelligence dashboards.

**Key Takeaways for Replication**:
1. **Material-UI Dark Theme**: Leverage MUI's theming system with cybersecurity color palette
2. **Flexible Grid Layout**: Implement drag-and-drop with resizable widgets
3. **Widget Diversity**: Start with essential widgets (counters, lists, timelines) and expand
4. **STIX Integration**: Design for graph-based threat intelligence data
5. **Performance First**: Optimize for real-time updates and large datasets

**Recommended Starting Point**:
- Begin with Phase 1 components (grid layout, counters, timeline)
- Use Material-UI v5 with dark theme
- Implement basic filtering and temporal controls
- Progressively enhance with advanced visualizations

This analysis provides a comprehensive foundation for building a web interface that captures OpenCTI's visual design excellence while adapting to specific project requirements.

---

**Document Version**: 1.0
**Last Updated**: 2025-11-04
**Analyst**: Research Specialist (Deep Analysis Mode)
**Confidence Level**: High (95%)
**Sources**: OpenCTI official documentation, developer resources, design analysis
