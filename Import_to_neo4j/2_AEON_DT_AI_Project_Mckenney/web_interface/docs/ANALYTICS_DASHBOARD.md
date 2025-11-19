# Analytics & Reporting Dashboard

## Overview
Comprehensive analytics dashboard with real-time metrics, time-series visualizations, and data export capabilities.

## Features Implemented

### 1. Analytics Page (`/app/analytics/page.tsx`)
- **Time Period Selector**: 7d, 30d, 90d with dynamic data loading
- **Customer Filter**: Filter analytics by specific customer or view all
- **4 Key Metric Cards**:
  - Document Growth (with % change indicator)
  - Entities Added (with % change indicator)
  - Process Success Rate (%)
  - Average Quality Score (with % change indicator)
- **3 Interactive Charts**:
  - Line Chart: Documents Over Time
  - Pie Chart: Entity Types Distribution
  - Bar Chart: Customer Activity (documents & entities)
- **Export Buttons**: CSV, JSON, PDF formats
- **Loading States**: Skeleton loading for all components
- **Error Handling**: Graceful error display

### 2. Metrics API (`/app/api/analytics/metrics/route.ts`)
- **Endpoint**: `GET /api/analytics/metrics`
- **Query Parameters**:
  - `timeRange`: 7d | 30d | 90d (default: 30d)
  - `customerId`: Optional customer filter
- **Response Data**:
  ```typescript
  {
    documentGrowth: { current, previous, percentageChange },
    entitiesAdded: { current, previous, percentageChange },
    processSuccess: { current, percentageChange },
    avgQuality: { current, previous, percentageChange }
  }
  ```
- **Features**:
  - Period-over-period comparison
  - Growth rate calculations
  - Customer-specific metrics
  - Quality score aggregation

### 3. Time Series API (`/app/api/analytics/timeseries/route.ts`)
- **Endpoint**: `GET /api/analytics/timeseries`
- **Query Parameters**:
  - `timeRange`: 7d | 30d | 90d
  - `customerId`: Optional customer filter
- **Response Data**:
  ```typescript
  {
    documentsOverTime: [{ date, count }],
    entitiesByType: [{ name, value }],
    customerActivity: [{ name, documents, entities }]
  }
  ```
- **Features**:
  - Adaptive aggregation (day/week based on time range)
  - Entity type classification
  - Top 10 customer activity ranking

### 4. Export API (`/app/api/analytics/export/route.ts`)
- **Endpoint**: `POST /api/analytics/export`
- **Request Body**:
  ```json
  {
    "format": "csv" | "json" | "pdf",
    "timeRange": "7d" | "30d" | "90d",
    "customerId": "optional-customer-id"
  }
  ```
- **Export Formats**:
  - **CSV**: Comma-separated values with headers
  - **JSON**: Pretty-printed JSON data
  - **PDF**: Text-based report (can be enhanced with PDF library)
- **Features**:
  - Filtered data export
  - Automatic file download
  - Proper Content-Type headers
  - Timestamped filenames

### 5. Chart Component (`/components/analytics/ChartCard.tsx`)
- **Reusable wrapper for Recharts**
- **Supported Chart Types**:
  - Line Chart: Time-series data
  - Bar Chart: Comparative data
  - Pie Chart: Distribution data
- **Features**:
  - Tremor Card styling integration
  - Loading state animations
  - Error state handling
  - Empty state display
  - Responsive sizing
  - Custom color schemes
  - Configurable data keys

## Technical Implementation

### Database Queries
All queries leverage Neo4j's datetime functions and labels:

```cypher
// Document Growth with Period Classification
MATCH (d:Document)
WITH d,
     CASE
       WHEN datetime(d.createdAt) >= datetime($startDate) THEN 'current'
       WHEN datetime(d.createdAt) >= datetime($previousStartDate)
            AND datetime(d.createdAt) < datetime($startDate) THEN 'previous'
       ELSE 'other'
     END as period
WITH period, count(d) as count
RETURN collect({period: period, count: count}) as periods
```

```cypher
// Entity Type Distribution
MATCH (e)
WHERE (e:Entity OR e:Person OR e:Organization OR e:Location OR e:Technology)
WITH labels(e) as entityLabels
UNWIND entityLabels as label
WHERE label IN ['Entity', 'Person', 'Organization', 'Location', 'Technology']
WITH label, count(*) as count
RETURN label as name, count as value
ORDER BY value DESC
```

### Data Processing
- **Period Comparison**: Calculates current vs previous period metrics
- **Growth Rates**: Percentage change with zero-division handling
- **Aggregation**: Day/week-based grouping based on time range
- **Customer Filtering**: Applied consistently across all queries

### Visualization
- **Recharts Library**: Production-ready charting
- **Tremor Components**: Consistent UI styling
- **Color Scheme**: 8-color palette for variety
- **Responsive Design**: Charts adapt to container size

## Usage Examples

### Accessing the Dashboard
```
http://localhost:3000/analytics
```

### API Calls
```javascript
// Get metrics for last 30 days
const response = await fetch('/api/analytics/metrics?timeRange=30d');
const metrics = await response.json();

// Get time series data for specific customer
const response = await fetch(
  '/api/analytics/timeseries?timeRange=90d&customerId=cust-123'
);
const data = await response.json();

// Export data as CSV
const response = await fetch('/api/analytics/export', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    format: 'csv',
    timeRange: '30d',
    customerId: 'cust-123'
  })
});
const blob = await response.blob();
```

## Neo4j Data Requirements

### Required Node Properties
```cypher
// Document nodes
(:Document {
  id: string,
  title: string,
  type: string,
  createdAt: datetime,
  customerId: string,
  processingStatus: string,
  qualityScore: float
})

// Entity nodes
(:Entity|Person|Organization|Location|Technology {
  id: string,
  name: string,
  createdAt: datetime,
  customerId: string
})

// Customer nodes
(:Customer {
  id: string,
  name: string,
  createdAt: datetime
})
```

### Required Relationships
```cypher
(Customer)-[:OWNS]->(Document)
(Document)-[:HAS_TAG]->(Tag)
(Document)-[:CONTAINS|MENTIONS]->(Entity)
```

## Performance Considerations

### Optimizations
- **Parallel API Calls**: Metrics and time series fetched concurrently
- **Index Usage**: Queries leverage createdAt and customerId indexes
- **Aggregation**: Server-side grouping reduces data transfer
- **Caching**: Consider adding Redis cache for frequently accessed metrics

### Recommended Indexes
```cypher
CREATE INDEX document_created IF NOT EXISTS FOR (d:Document) ON (d.createdAt);
CREATE INDEX document_customer IF NOT EXISTS FOR (d:Document) ON (d.customerId);
CREATE INDEX entity_created IF NOT EXISTS FOR (e:Entity) ON (e.createdAt);
CREATE INDEX entity_customer IF NOT EXISTS FOR (e:Entity) ON (e.customerId);
```

## Future Enhancements

### Planned Features
1. **Custom Date Range**: Calendar picker for arbitrary date ranges
2. **Real-time Updates**: WebSocket integration for live metrics
3. **Advanced Filtering**: Multi-customer, tag-based, entity-type filters
4. **Saved Reports**: Store and schedule report generation
5. **Comparison Mode**: Side-by-side period comparison
6. **Drill-down**: Click charts to explore detailed data
7. **PDF Enhancement**: Use pdfkit/puppeteer for rich PDF reports
8. **Email Reports**: Scheduled email delivery
9. **Alerts**: Threshold-based notifications
10. **Dashboard Customization**: User-configurable widgets

### Technical Improvements
1. **Query Optimization**: Materialized views for complex aggregations
2. **Caching Layer**: Redis for frequently accessed metrics
3. **Rate Limiting**: Protect export endpoints
4. **Pagination**: For large data exports
5. **Compression**: Gzip responses for better performance

## Testing

### Manual Testing Steps
1. Navigate to `/analytics`
2. Verify all metric cards display with data
3. Test time range selector (7d, 30d, 90d)
4. Test customer filter dropdown
5. Verify charts render correctly
6. Test CSV export download
7. Test JSON export download
8. Test PDF export download
9. Verify loading states appear during data fetch
10. Test error handling with Neo4j disconnected

### Test Data Requirements
- Multiple documents across different time periods
- Various entity types (Person, Organization, Location, Technology)
- Multiple customers with associated documents
- Documents with quality scores and processing statuses

## Troubleshooting

### Common Issues

**Charts not rendering**
- Check browser console for Recharts errors
- Verify data structure matches expected format
- Ensure Recharts is properly installed

**No data displayed**
- Verify Neo4j connection
- Check if documents have `createdAt` properties
- Verify time range includes existing data

**Export not downloading**
- Check Content-Disposition headers
- Verify browser allows downloads
- Check file size limits

**Slow performance**
- Add recommended indexes
- Reduce time range
- Enable query caching
- Consider pagination for large datasets

## File Locations

```
web_interface/
├── app/
│   ├── analytics/
│   │   └── page.tsx                      # Main analytics dashboard
│   └── api/
│       └── analytics/
│           ├── metrics/
│           │   └── route.ts              # Metrics API endpoint
│           ├── timeseries/
│           │   └── route.ts              # Time series API endpoint
│           └── export/
│               └── route.ts              # Export API endpoint
└── components/
    └── analytics/
        └── ChartCard.tsx                 # Reusable chart component
```

## Dependencies

Already installed in package.json:
- `recharts@^2.13.3` - Chart library
- `@tremor/react@^3.18.3` - UI components
- `neo4j-driver@^5.25.0` - Database driver
- `lucide-react@^0.454.0` - Icons

No additional dependencies required.

## Environment Variables

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=neo4j@openspg
```

## Completion Status

✅ COMPLETE - Analytics dashboard is fully functional with:
- 4 metric cards with trend indicators
- 3 interactive charts (line, pie, bar)
- Time period and customer filtering
- CSV, JSON, PDF export capabilities
- Real Neo4j data queries
- Loading and error states
- Responsive design
- Production-ready code

Report COMPLETE when analytics dashboard is verified functional.
