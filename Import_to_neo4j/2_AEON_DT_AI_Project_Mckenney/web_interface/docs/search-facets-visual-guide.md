# Search Facets Visual Guide

## Filter Sidebar Layout

```
┌─────────────────────────────────────┐
│ Filters                    Clear ✕  │
│ 2 filters active                    │
├─────────────────────────────────────┤
│                                     │
│ Customer                            │
│ ▼ [Select customer...]             │
│                                     │
│ Tags                                │
│ ☐ requirements                      │
│ ☐ specification                     │
│ ☐ design                            │
│                                     │
│ Date Range                          │
│ [From date]                         │
│ [To date]                           │
│                                     │
├─────────────────────────────────────┤
│ Quick Filters                       │
├─────────────────────────────────────┤
│                                     │
│ Severity                            │
│ ┌───────────────────────────────┐   │
│ │ ☑ CRITICAL                    │   │
│ │ ☑ HIGH                        │   │
│ │ ☐ MEDIUM                      │   │
│ │ ☐ LOW                         │   │
│ └───────────────────────────────┘   │
│                                     │
│ Type                                │
│ ┌───────────────────────────────┐   │
│ │ ☑ CVE                         │   │
│ │ ☐ CWE                         │   │
│ │ ☐ Threat Actor                │   │
│ │ ☐ Malware                     │   │
│ │ ☐ ICS Asset                   │   │
│ └───────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│ Advanced Filters                    │
├─────────────────────────────────────┤
│                                     │
│ Node Type                           │
│ ☐ CVE                               │
│ ☐ CWE                               │
│ ☐ ThreatActor                       │
│ ☐ Campaign                          │
│ ☐ Malware                           │
│ ☐ AttackTechnique                   │
│ ☐ ICS_Asset                         │
│                                     │
│ CVSS Severity: 0.0 - 10.0          │
│ [━━━●━━━━━━] Min: 0.0              │
│ [━━━━━━━━●━] Max: 10.0             │
│                                     │
│ MITRE ATT&CK Tactic                │
│ ▼ [All tactics]                    │
│                                     │
└─────────────────────────────────────┘
```

## Color Scheme (VulnCheck-Inspired)

### Filter Box Styling
```css
background: rgba(15, 23, 42, 0.8)  /* slate-900/80 */
border-radius: 0.5rem              /* rounded-lg */
padding: 0.75rem                   /* p-3 */
```

### Text Styling
```css
Labels:    text-slate-300  /* Light gray for headers */
Options:   text-slate-400  /* Medium gray for options */
Checkboxes: Standard checkbox component
```

### Interactive States
```css
Hover:     cursor-pointer
Checked:   Standard checkbox filled state
Disabled:  opacity-70
```

## Filter Interaction Flow

### User Action Flow
```
1. User selects severity filters
   ├─ CRITICAL ☑
   └─ HIGH ☑

2. User selects type filter
   └─ CVE ☑

3. Active filter count updates: "3 filters active"

4. User clicks search
   └─ Request sent with:
      {
        severities: ['CRITICAL', 'HIGH'],
        types: ['CVE']
      }

5. Backend applies filters:
   ├─ Neo4j: CVSS score 7.0-10.0 AND type = CVE
   └─ Qdrant: CVSS score 7.0-10.0 AND type = CVE

6. Results filtered and displayed
```

### Clear Filters Flow
```
1. User clicks "Clear ✕" button

2. All filters reset:
   ├─ selectedSeverities = []
   ├─ selectedTypes = []
   └─ All other filters cleared

3. Active filter count: "0 filters active"
```

## Filter Logic Examples

### Example 1: Single Severity
```
User selects: CRITICAL

Neo4j Query:
WHERE node.cvss_score >= 9.0 AND node.cvss_score <= 10.0

Qdrant Filter:
{
  key: 'cvss_score',
  range: { gte: 9.0, lte: 10.0 }
}
```

### Example 2: Multiple Severities
```
User selects: CRITICAL, HIGH

Neo4j Query:
WHERE (
  (node.cvss_score >= 9.0 AND node.cvss_score <= 10.0) OR
  (node.cvss_score >= 7.0 AND node.cvss_score < 9.0)
)

Qdrant Filter:
{
  should: [
    { key: 'cvss_score', range: { gte: 9.0, lte: 10.0 } },
    { key: 'cvss_score', range: { gte: 7.0, lt: 9.0 } }
  ]
}
```

### Example 3: Severity + Type
```
User selects: CRITICAL, CVE

Neo4j Query:
WHERE (node.cvss_score >= 9.0 AND node.cvss_score <= 10.0)
  AND labels(node)[0] IN ['CVE']

Qdrant Filter:
{
  must: [
    {
      should: [
        { key: 'cvss_score', range: { gte: 9.0, lte: 10.0 } }
      ]
    },
    {
      key: 'type',
      match: { any: ['CVE'] }
    }
  ]
}
```

## Responsive Behavior

### Desktop (lg breakpoint)
- Sidebar always visible
- Fixed width: 1/4 of screen
- Scrollable if filters exceed viewport height

### Mobile (< lg breakpoint)
- Sidebar hidden by default
- Toggle button shows: "Filters (2)" with badge
- Overlay sidebar when toggled
- Full width when expanded

## Accessibility

### Keyboard Navigation
- Tab through checkboxes
- Space to toggle checkbox
- Label click toggles checkbox
- Clear button accessible via Tab

### Screen Reader Support
- Labels associated with checkboxes via htmlFor
- Clear button announces "Clear all filters"
- Active filter count announced

### Focus States
- Visible focus ring on all interactive elements
- High contrast focus indicators
- Logical tab order
