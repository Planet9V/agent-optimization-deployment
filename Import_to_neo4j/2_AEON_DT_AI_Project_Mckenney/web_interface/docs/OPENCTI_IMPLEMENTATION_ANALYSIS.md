# OpenCTI Implementation Analysis
**Date:** 2025-11-04
**Repository:** https://github.com/OpenCTI-Platform/opencti
**Analysis Focus:** Map visualizations and dashboard components

## Executive Summary

OpenCTI uses **ApexCharts** as their primary visualization library for dashboards and threat maps, with **Leaflet** (via react-leaflet) for geographic/world map displays. They DO NOT use scatter plots on actual world maps - instead they use:
1. **Scatter plot charts** (time-based threat visualization)
2. **Leaflet maps** (geographic location display)
3. **ApexCharts widgets** (comprehensive dashboard charts)

## Core Visualization Libraries

### 1. ApexCharts (Primary Chart Library)
**Version:** `apexcharts: 4.4.0`, `react-apexcharts: 1.7.0`

**Chart Types Used:**
- Scatter plots (threat mapping)
- Donut charts
- Area charts
- Line charts
- Bar charts (horizontal/vertical)
- Radar charts
- Polar area charts
- Heat maps
- Tree maps

**Integration Pattern:**
```tsx
import Chart from '@components/common/charts/Chart';
import { ApexOptions } from 'apexcharts';

// Wrapper component pattern
const WidgetScatter = ({ series, options }: WidgetScatterProps) => {
  const theme = useTheme<Theme>();

  const apexOptions = useMemo(() => {
    return scatterChartOptions({
      ...options,
      theme,
    });
  }, []);

  return (
    <Chart
      options={apexOptions}
      series={series}
      type="scatter"
      width="100%"
      height="100%"
    />
  );
};
```

### 2. Leaflet (Geographic Maps)
**Version:** `leaflet: 1.9.4`, `react-leaflet: 5.0.0`

**Usage:**
- Geographic location visualization
- Country highlighting
- City/position markers
- Mini-maps for location entities

**Integration Pattern:**
```jsx
import { MapContainer, TileLayer, GeoJSON, Marker } from 'react-leaflet';
import L from 'leaflet';

const LocationMiniMap = (props) => {
  return (
    <MapContainer
      center={validatedCenter}
      zoom={zoom}
      attributionControl={false}
      zoomControl={false}
    >
      <TileLayer
        url={
          theme.palette.mode === 'light'
            ? settings.platform_map_tile_server_light
            : settings.platform_map_tile_server_dark
        }
      />
      <GeoJSON data={countries} style={getStyle} />
      {mapPosition && (
        <Marker
          position={mapPosition}
          icon={cityIcon(theme.palette.mode === 'dark')}
        />
      )}
    </MapContainer>
  );
};
```

### 3. Recharts (Secondary)
**Version:** `recharts: 3.2.0`
- Used as secondary/alternative chart library
- Not primary visualization tool

## Threat Map Implementation

### Component: `PirThreatMap.tsx`

**Key Insights:**
1. **NOT a geographic map** - it's a time-series scatter plot
2. X-axis: Time (2 months ago to today)
3. Y-axis: Threat score (0-100)
4. Scatter points represent threat entities grouped by proximity

**Data Structure:**
```typescript
interface PirThreatMapMarker {
  id: string;
  date: string;          // timestamp
  score: number;         // 0-100 threat score
  name: string;          // entity name
  type: string;          // entity_type
}

// Grouped scatter data
const series: ApexPirThreatMapSeries = [
  {
    data: [{
      x: new Date(item.date),    // X: timestamp
      y: item.score,              // Y: threat score
      fillColor: color,           // color by entity type
      meta: {
        group: [/* markers */],   // grouped items
        size: group.length,       // cluster size
      },
    }],
  }
];
```

**Grouping Logic:**
- Groups threats within 18 hours (1080 minutes) and 5 score points
- Displays cluster size as data label
- Color coding by entity type
- Interactive tooltips on hover

### Component Code Snippet:
```tsx
<WidgetScatter
  series={series}
  options={{
    background: theme.palette.background.accent,
    dataPointMouseEnter: (e, _, opts) => {
      const apexSeries = opts.w.config.series[opts.seriesIndex];
      const item = apexSeries.data[opts.dataPointIndex].meta.group;
      setTooltipData(item);
      setTooltipPos({ x: e.offsetX, y: e.offsetY });
    },
    labelsFormatter: (_, opts) => {
      const apexSeries = opts.w.config.series[opts.seriesIndex];
      const item = apexSeries.data[opts.dataPointIndex].meta;
      return item.size > 1 ? item.size : '';
    },
  }}
/>
```

## ApexCharts Configuration Patterns

### Scatter Chart Options (`scatterOptions.ts`)
```typescript
export const scatterChartOptions = ({
  theme,
  background,
  dataPointMouseEnter,
  dataPointMouseLeave,
  labelsFormatter,
}: ScatterChartOptionsArgs): ApexOptions => ({
  chart: {
    type: 'scatter',
    background,
    toolbar: { show: false },
    events: {
      dataPointMouseEnter,
      dataPointMouseLeave,
    },
    zoom: { enabled: false },
  },
  dataLabels: {
    enabled: true,
    background: { enabled: false },
    formatter: labelsFormatter,
  },
  colors: [
    theme.palette.primary.main,
    ...colors(theme.palette.mode === 'dark' ? 400 : 600),
  ],
  xaxis: {
    type: 'datetime',
    min: new Date(monthsAgo(2)).getTime(),
    max: new Date(now()).getTime(),
  },
  yaxis: {
    show: false,
    min: 0,
    max: 100,
  },
  markers: {
    size: 10,
    strokeWidth: 0,
  },
});
```

### Chart Color System
```javascript
// Material UI color palette integration
export const colors = (temp) => [
  C.red[temp],
  C.purple[temp],
  C.pink[temp],
  C.deepPurple[temp],
  C.indigo[temp],
  C.blue[temp],
  C.cyan[temp],
  // ... 20 colors total
];
```

## Dashboard Widget Architecture

### Widget Component Pattern
All dashboard widgets follow a consistent pattern:

```tsx
// Example: WidgetDonut.tsx
const WidgetDonut = ({
  data,
  groupBy,
  withExport = false,
  readonly = false,
}: WidgetDonutProps) => {
  const theme = useTheme<Theme>();
  const chartData = useMemo(() => data.map((n) => n.value), [data]);

  const options: ApexOptions = useMemo(() => {
    const labels = buildWidgetLabelsOption(data, groupBy);
    let chartColors = [];
    // Entity color extraction logic
    if (data.at(0)?.entity?.color) {
      chartColors = data.map((n) => n.entity?.color);
    }

    return donutChartOptions(
      theme,
      labels,
      'bottom',
      false,
      chartColors,
    );
  }, [data, groupBy]);

  return (
    <Chart
      options={options}
      series={chartData}
      type="donut"
      width="100%"
      height="100%"
      withExportPopover={withExport}
      isReadOnly={readonly}
    />
  );
};
```

### Available Widget Types
1. **WidgetScatter** - Scatter plots (threat maps)
2. **WidgetDonut** - Distribution charts
3. **WidgetMultiAreas** - Time-series area charts
4. **WidgetMultiLines** - Multi-line time-series
5. **WidgetHorizontalBars** - Horizontal bar charts
6. **WidgetDistributionList** - List-based distributions
7. **WidgetRadar** - Radar/spider charts
8. **WidgetPolarArea** - Polar area charts
9. **WidgetMultiHeatMap** - Heat map visualizations
10. **WidgetNumber** - Single metric displays
11. **WidgetListCoreObjects** - Object lists
12. **WidgetListRelationships** - Relationship lists

## Geographic Map Implementation

### Leaflet Map Component (`LocationMiniMap.jsx`)

**Features:**
- Configurable tile servers (dark/light themes)
- Country highlighting via GeoJSON
- Custom marker icons
- Coordinate validation
- Responsive map container

**Data Requirements:**
- Latitude/longitude coordinates
- Country ISO3 codes (for highlighting)
- GeoJSON country boundaries (`countries.json`)
- Custom marker icons (PNG assets)

**Tile Server Configuration:**
```javascript
<TileLayer
  url={
    theme.palette.mode === 'light'
      ? settings.platform_map_tile_server_light
      : settings.platform_map_tile_server_dark
  }
/>
```

**Custom Icon System:**
```javascript
const cityIcon = (dark = true) => new L.Icon({
  iconUrl: dark ? fileUri(CityDark) : fileUri(CityLight),
  iconRetinaUrl: dark ? fileUri(CityDark) : fileUri(CityLight),
  iconAnchor: [12, 12],
  popupAnchor: [0, -12],
  iconSize: [25, 25],
});
```

## Integration Strategy for AEON

### Required Dependencies

```json
{
  "dependencies": {
    "apexcharts": "^4.4.0",
    "react-apexcharts": "^1.7.0",
    "leaflet": "^1.9.4",
    "react-leaflet": "^5.0.0",
    "@mui/material": "^6.5.0",
    "@mui/icons-material": "^6.5.0"
  }
}
```

### Implementation Steps

#### 1. Install Dependencies
```bash
npm install apexcharts react-apexcharts leaflet react-leaflet @types/leaflet
```

#### 2. Create Chart Utility Functions
**File:** `src/utils/chartOptions.ts`

```typescript
import { ApexOptions } from 'apexcharts';

export const scatterChartOptions = (
  theme: any,
  options?: {
    background?: string;
    xMin?: number;
    xMax?: number;
    yMin?: number;
    yMax?: number;
  }
): ApexOptions => ({
  chart: {
    type: 'scatter',
    background: options?.background || 'transparent',
    toolbar: { show: false },
    zoom: { enabled: false },
  },
  xaxis: {
    type: 'datetime',
    min: options?.xMin,
    max: options?.xMax,
  },
  yaxis: {
    min: options?.yMin || 0,
    max: options?.yMax || 100,
  },
  markers: {
    size: 10,
  },
  // ... additional options
});
```

#### 3. Create Threat Map Component
**File:** `src/components/ThreatMap.tsx`

```tsx
import React, { useState, useMemo } from 'react';
import { useTheme } from '@mui/material/styles';
import Chart from 'react-apexcharts';
import { scatterChartOptions } from '../utils/chartOptions';

interface ThreatData {
  id: string;
  timestamp: string;
  severity: number;
  name: string;
  type: string;
}

interface ThreatMapProps {
  threats: ThreatData[];
}

export const ThreatMap: React.FC<ThreatMapProps> = ({ threats }) => {
  const theme = useTheme();
  const [tooltip, setTooltip] = useState<any>(null);

  // Group threats by proximity (similar to OpenCTI)
  const series = useMemo(() => {
    const grouped: ThreatData[][] = [];
    // Grouping logic here (18h window, 5 score difference)

    return grouped.map(group => ({
      data: [{
        x: new Date(group[0].timestamp),
        y: group[0].severity,
        fillColor: getColorByType(group[0].type),
        meta: { group, size: group.length },
      }]
    }));
  }, [threats]);

  const options = scatterChartOptions(theme, {
    xMin: Date.now() - (60 * 24 * 60 * 60 * 1000), // 60 days
    xMax: Date.now(),
    yMin: 0,
    yMax: 100,
  });

  return (
    <Chart
      options={options}
      series={series}
      type="scatter"
      height="500px"
    />
  );
};
```

#### 4. Create Geographic Map Component
**File:** `src/components/GeographicMap.tsx`

```tsx
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface Location {
  id: string;
  name: string;
  lat: number;
  lng: number;
  severity: number;
}

interface GeographicMapProps {
  locations: Location[];
}

export const GeographicMap: React.FC<GeographicMapProps> = ({ locations }) => {
  return (
    <MapContainer
      center={[0, 0]}
      zoom={2}
      style={{ height: '600px', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      {locations.map(loc => (
        <Marker key={loc.id} position={[loc.lat, loc.lng]}>
          <Popup>
            <div>
              <strong>{loc.name}</strong>
              <p>Severity: {loc.severity}</p>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};
```

#### 5. Dashboard Widget Components
**File:** `src/components/widgets/ThreatDistribution.tsx`

```tsx
import React from 'react';
import Chart from 'react-apexcharts';
import { useTheme } from '@mui/material/styles';

export const ThreatDistribution: React.FC<{ data: any[] }> = ({ data }) => {
  const theme = useTheme();

  const options = {
    chart: {
      type: 'donut',
      background: theme.palette.background.paper,
    },
    labels: data.map(d => d.label),
    colors: data.map(d => d.color),
    legend: {
      position: 'bottom',
    },
  };

  const series = data.map(d => d.value);

  return <Chart options={options} series={series} type="donut" />;
};
```

### Data Structure Requirements

#### Neo4j Query for Threat Map Data
```cypher
MATCH (t:Threat)
WHERE t.timestamp >= datetime() - duration('P60D')
RETURN
  t.id as id,
  t.timestamp as timestamp,
  t.severity as severity,
  t.name as name,
  t.type as type
ORDER BY t.timestamp DESC
```

#### Neo4j Query for Geographic Data
```cypher
MATCH (t:Threat)-[:LOCATED_AT]->(l:Location)
WHERE l.latitude IS NOT NULL AND l.longitude IS NOT NULL
RETURN
  t.id as id,
  t.name as name,
  l.latitude as lat,
  l.longitude as lng,
  t.severity as severity
```

## Styling and Theme Integration

### MUI Theme Integration
```typescript
// Ensure theme consistency
const theme = useTheme();

// ApexCharts theme configuration
const chartOptions = {
  theme: {
    mode: theme.palette.mode, // 'light' or 'dark'
  },
  chart: {
    foreColor: theme.palette.text.secondary,
    background: theme.palette.background.paper,
  },
};
```

### Custom CSS for Leaflet
```css
/* Ensure Leaflet styles are loaded */
@import 'leaflet/dist/leaflet.css';

/* Custom marker styles */
.custom-marker {
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

/* Dark theme map adjustments */
.dark-theme .leaflet-container {
  background: #1a1a1a;
  filter: invert(1) hue-rotate(180deg);
}

.dark-theme .leaflet-marker-icon,
.dark-theme .leaflet-popup-content-wrapper {
  filter: invert(1) hue-rotate(180deg);
}
```

## Performance Considerations

### Data Optimization
1. **Limit data points:** Max 1000 points on scatter plots
2. **Use data grouping:** Cluster nearby points (18h window, 5 score diff)
3. **Lazy loading:** Load charts only when visible
4. **Memoization:** Cache chart options and series data

```typescript
const series = useMemo(() => {
  return processData(threats);
}, [threats]); // Only recompute when threats change
```

### Leaflet Performance
1. **Marker clustering:** Use `react-leaflet-cluster` for many markers
2. **Tile caching:** Configure tile layer caching
3. **Lazy rendering:** Render map only when container visible

## Key Differences from AEON Requirements

### What OpenCTI Does
- Time-based scatter plot (NOT geographic)
- Separate Leaflet maps for locations
- Focus on temporal threat evolution
- Score-based Y-axis (0-100)

### What AEON Needs
- **True world map visualization** with threats overlaid
- Geographic coordinates (lat/lng) for threats
- Country/region-based aggregation
- Real-time threat updates

### Recommendation for AEON
**Combine both approaches:**

1. **Primary View:** Leaflet world map with threat markers
   - Use `react-leaflet` for base map
   - Custom markers colored by severity
   - Clustering for high-density areas
   - Popup details on click

2. **Secondary View:** Time-series threat chart
   - ApexCharts scatter plot (like OpenCTI)
   - X-axis: Time
   - Y-axis: Threat severity
   - Interactive filtering

3. **Dashboard Widgets:** ApexCharts for analytics
   - Threat distribution (donut)
   - Threat trends (area/line)
   - Top threats (horizontal bars)
   - Heat maps for activity

## Additional Resources

### OpenCTI File Locations
- **Scatter Chart:** `opencti-platform/opencti-front/src/components/dashboard/WidgetScatter.tsx`
- **Chart Options:** `opencti-platform/opencti-front/src/utils/apexCharts/scatterOptions.ts`
- **Chart Utilities:** `opencti-platform/opencti-front/src/utils/Charts.jsx`
- **Leaflet Map:** `opencti-platform/opencti-front/src/private/components/common/location/LocationMiniMap.jsx`
- **Threat Map:** `opencti-platform/opencti-front/src/private/components/pir/pir_overview/pir_threat_map/PirThreatMap.tsx`
- **Data Builder:** `opencti-platform/opencti-front/src/private/components/pir/pir_overview/pir_threat_map/useBuildScatterData.tsx`

### Documentation Links
- ApexCharts: https://apexcharts.com/docs/
- React-ApexCharts: https://github.com/apexcharts/react-apexcharts
- Leaflet: https://leafletjs.com/
- React-Leaflet: https://react-leaflet.js.org/

## Conclusion

OpenCTI provides an excellent reference implementation for:
1. ✅ **Dashboard visualization patterns** (ApexCharts)
2. ✅ **Geographic mapping** (Leaflet)
3. ✅ **Theme integration** (MUI)
4. ✅ **Data grouping algorithms** (threat clustering)

However, they do NOT have a combined world map + threat overlay visualization. AEON will need to build this by combining:
- Leaflet's geographic mapping
- Custom threat markers with severity colors
- Clustering for performance
- ApexCharts for analytical dashboards

The implementation is straightforward with the identified dependencies and patterns above.
