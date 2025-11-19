# Search Facets Implementation

## Overview
Added VulnCheck-inspired severity and type filter facets to the search interface.

## Changes Made

### 1. Frontend (app/search/page.tsx)

#### New State Variables
```typescript
const [selectedSeverities, setSelectedSeverities] = useState<string[]>([]);
const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
```

#### Filter Options
```typescript
const availableSeverities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'];
const availableTypes = ['CVE', 'CWE', 'Threat Actor', 'Malware', 'ICS Asset'];
```

#### UI Components
Added two new filter sections in the sidebar:
- **Severity Filter**: Checkbox group for CRITICAL, HIGH, MEDIUM, LOW
- **Type Filter**: Checkbox group for CVE, CWE, Threat Actor, Malware, ICS Asset

Both sections use VulnCheck-inspired dark slate styling:
- Background: `bg-slate-900/80`
- Text: `text-slate-400`
- Rounded corners: `rounded-lg`
- Padding: `p-3`

#### State Management
```typescript
const handleSeverityToggle = (severity: string) => {
  setSelectedSeverities(prev =>
    prev.includes(severity) ? prev.filter(s => s !== severity) : [...prev, severity]
  );
};

const handleTypeToggle = (type: string) => {
  setSelectedTypes(prev =>
    prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
  );
};
```

#### Search API Integration
Added new parameters to search request:
```typescript
if (selectedSeverities.length > 0) {
  requestBody.severities = selectedSeverities;
}

if (selectedTypes.length > 0) {
  requestBody.types = selectedTypes;
}
```

### 2. Backend API (app/api/search/route.ts)

#### Request Parameter Extraction
```typescript
const {
  // ... existing params
  severities,
  types,
} = body;
```

#### Filter Integration
```typescript
if (severities && Array.isArray(severities) && severities.length > 0) {
  searchOptions.filters.severities = severities;
}

if (types && Array.isArray(types) && types.length > 0) {
  searchOptions.filters.types = types;
}
```

### 3. Search Library (lib/hybrid-search.ts)

#### Interface Updates
```typescript
export interface SearchFilters {
  // ... existing filters
  severities?: string[];
  types?: string[];
}
```

#### Neo4j Full-Text Search
Added Cypher query conditions:

**Severity Filter** (maps to CVSS score ranges):
```cypher
AND (
  (node.cvss_score >= 9.0 AND node.cvss_score <= 10.0) OR  -- CRITICAL
  (node.cvss_score >= 7.0 AND node.cvss_score < 9.0) OR    -- HIGH
  (node.cvss_score >= 4.0 AND node.cvss_score < 7.0) OR    -- MEDIUM
  (node.cvss_score >= 0.0 AND node.cvss_score < 4.0)       -- LOW
)
```

**Type Filter**:
```cypher
AND labels(node)[0] IN $types
```

#### Qdrant Semantic Search
Added filter conditions:

**Severity Filter**:
```typescript
{
  should: [
    { key: 'cvss_score', range: { gte: 9.0, lte: 10.0 } },  // CRITICAL
    { key: 'cvss_score', range: { gte: 7.0, lt: 9.0 } },    // HIGH
    { key: 'cvss_score', range: { gte: 4.0, lt: 7.0 } },    // MEDIUM
    { key: 'cvss_score', range: { gte: 0.0, lt: 4.0 } }     // LOW
  ]
}
```

**Type Filter**:
```typescript
{
  key: 'type',
  match: { any: filters.types }
}
```

## CVSS Severity Mapping

| Severity | CVSS Range |
|----------|------------|
| CRITICAL | 9.0 - 10.0 |
| HIGH     | 7.0 - 8.9  |
| MEDIUM   | 4.0 - 6.9  |
| LOW      | 0.0 - 3.9  |

## UI Layout

The filters are organized in the left sidebar:
1. **Quick Filters** (New)
   - Severity
   - Type
2. **Advanced Filters** (Existing)
   - Node Type
   - CVSS Severity Range
   - MITRE ATT&CK Tactic

## Features

### Multi-Select
- Users can select multiple severities (e.g., CRITICAL + HIGH)
- Users can select multiple types (e.g., CVE + CWE)
- Filters are combined with OR logic within each category
- Categories are combined with AND logic

### Clear Filters
- Clear button resets all filters including new severity and type facets
- Active filter count includes new facets

### State Preservation
- Filter state persists during search operations
- Filters are included in all search modes (fulltext, semantic, hybrid)

## Testing

### TypeScript Validation
✅ No TypeScript errors (`npm run typecheck`)

### Manual Testing Checklist
- [ ] Severity filter UI renders correctly
- [ ] Type filter UI renders correctly
- [ ] Selecting severities updates state
- [ ] Selecting types updates state
- [ ] Search request includes severity filters
- [ ] Search request includes type filters
- [ ] Neo4j queries filter by CVSS score ranges
- [ ] Qdrant queries filter by CVSS score ranges
- [ ] Clear filters button resets new facets
- [ ] Active filter count includes new facets

## Future Enhancements

1. **Dynamic Filter Counts**: Show result counts next to each filter option
2. **Filter Badges**: Display active filters as removable badges
3. **Filter Presets**: Save common filter combinations
4. **Export Filtered Results**: Allow exporting search results with active filters
5. **Filter Analytics**: Track most-used filter combinations
