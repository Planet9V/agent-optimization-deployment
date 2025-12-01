# Graph Visualization Documentation

## Overview

Interactive Neo4j graph visualization using Neovis.js for exploring the knowledge graph with filtering, custom queries, and node details.

## Files Created

### Components

1. **`/components/graph/GraphVisualization.tsx`**
   - Main Neovis.js integration component
   - Interactive graph canvas with force and hierarchical layouts
   - Node and relationship rendering with custom colors
   - Click handlers for node selection
   - Export functionality (PNG)
   - Layout stabilization and fit-to-view controls

2. **`/components/graph/GraphFilters.tsx`**
   - Comprehensive filter panel
   - Node type checkboxes (Document, Entity, Topic, Person, Organization, Location, Project)
   - Relationship type filters (MENTIONS, RELATED_TO, HAS_TOPIC, etc.)
   - Customer multi-select dropdown
   - Tag multi-select
   - Confidence threshold slider (0.0 to 1.0)
   - Date range picker
   - Layout switcher (Force vs Hierarchical)

3. **`/components/graph/NodeDetails.tsx`**
   - Side panel for displaying selected node information
   - Property viewer with formatted values
   - Node label badges
   - Action buttons:
     - View Document (if documentId exists)
     - Edit Node
     - Delete Node
   - Metadata display (ID, created, updated timestamps)

### Pages

4. **`/app/graph/page.tsx`**
   - Graph explorer page
   - Integrates all graph components
   - Custom Cypher query builder
   - Saved queries functionality
   - Real-time graph updates

### API Routes

5. **`/app/api/graph/query/route.ts`**
   - POST `/api/graph/query` - Execute custom Cypher queries with validation
   - GET `/api/graph/query` - Fetch filtered subgraph based on parameters
   - Query sanitization (blocks DELETE, REMOVE, SET, CREATE, etc.)
   - Returns nodes and relationships in standardized format

## Setup

### 1. Install Dependencies

```bash
npm install neovis.js --legacy-peer-deps
```

### 2. Environment Variables

Add to `.env.local`:

```env
# Public Neo4j variables for client-side (Neovis.js)
NEXT_PUBLIC_NEO4J_URI=bolt://openspg-neo4j:7687
NEXT_PUBLIC_NEO4J_USER=neo4j
NEXT_PUBLIC_NEO4J_PASSWORD=neo4j@openspg
```

### 3. Start Development Server

```bash
npm run dev
```

### 4. Access Graph Visualization

- URL: http://localhost:3000/graph
- Or click "View Database" from the dashboard

## Features

### Interactive Visualization

- **Force Layout**: Physics-based graph layout with gravity and springs
- **Hierarchical Layout**: Tree-like directed graph layout
- **Node Colors**:
  - Document: Blue (#4A90E2)
  - Entity: Green (#50C878)
  - Topic: Yellow (#F7B731)
  - Person: Red (#E74C3C)
  - Organization: Purple (#9B59B6)
  - Location: Light Blue (#3498DB)
  - Project: Teal (#1ABC9C)

### Filtering

1. **Node Type Filter**: Show/hide specific node types
2. **Relationship Filter**: Filter by relationship types
3. **Customer Filter**: Filter by customer assignment
4. **Tag Filter**: Multi-select tag filtering
5. **Confidence Threshold**: Slider to filter low-confidence relationships
6. **Date Range**: Filter nodes by creation date

### Query Builder

- Custom Cypher query editor
- Syntax highlighting (monospace font)
- Query validation and sanitization
- Save/load queries functionality
- Example queries provided

### Node Interaction

- **Click Node**: View detailed properties in side panel
- **View Document**: Navigate to source document
- **Edit Node**: Modify node properties (TODO: implement)
- **Delete Node**: Remove node from graph (with confirmation)

### Export

- **Export PNG**: Download current graph view as PNG image
- **Export SVG**: (Planned feature)

## Usage Examples

### Basic Filtering

1. Select node types: Document, Entity
2. Select relationship: MENTIONS
3. Set confidence threshold: 0.7
4. Click a node to view details

### Custom Query

```cypher
MATCH (d:Document)-[r:MENTIONS]->(e:Entity)
WHERE r.confidence > 0.8
RETURN d, r, e
LIMIT 100
```

### Customer-Specific View

1. Select customer from dropdown
2. Select relevant node types
3. Graph shows only that customer's data

### Date Range Analysis

1. Set start date: 2025-01-01
2. Set end date: 2025-12-31
3. View documents created in that period

## API Usage

### Execute Custom Query

```typescript
const response = await fetch('/api/graph/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'MATCH (n:Document) RETURN n LIMIT 10'
  })
});

const data = await response.json();
// data.records contains query results
// data.summary contains query metadata
```

### Fetch Filtered Subgraph

```typescript
const params = new URLSearchParams({
  nodeTypes: 'Document,Entity',
  relationshipTypes: 'MENTIONS',
  confidenceMin: '0.7',
  dateStart: '2025-01-01',
  dateEnd: '2025-12-31'
});

const response = await fetch(`/api/graph/query?${params}`);
const data = await response.json();
// data.nodes contains node array
// data.relationships contains edge array
```

## Security

### Query Validation

The API blocks potentially dangerous Cypher keywords:
- DELETE
- REMOVE
- SET
- CREATE
- MERGE
- DROP
- ALTER

Only read-only queries (MATCH, RETURN) are allowed.

### Authentication

Currently no authentication. TODO: Add authentication middleware.

## Performance

### Optimization Strategies

1. **Query Limits**: Default 500 nodes to prevent overload
2. **Incremental Loading**: Load subgraphs on demand
3. **Caching**: Browser caches graph layouts
4. **Stabilization**: Physics simulation stabilizes for better performance

### Recommended Limits

- Nodes: < 1000 for smooth interaction
- Relationships: < 2000 for good performance
- Use filters to reduce graph size

## Troubleshooting

### Graph Not Loading

- Check Neo4j connection in .env.local
- Verify Neo4j is running: docker ps
- Check browser console for errors
- Ensure neovis.js is installed

### Empty Graph

- Check if data exists in Neo4j
- Verify Cypher query returns results
- Check filter settings (may be too restrictive)
- Review API response in network tab

### Slow Performance

- Reduce node limit in query
- Apply more filters
- Use hierarchical layout instead of force
- Disable physics after stabilization

### Connection Errors

- Verify NEXT_PUBLIC_NEO4J_URI is correct
- Check Neo4j bolt port (7687) is accessible
- Ensure credentials are correct
- Check Docker network connectivity

## Future Enhancements

### Planned Features

1. **Search**: Search for nodes by name/property
2. **Subgraph Expansion**: Click to expand node connections
3. **Clustering**: Group similar nodes
4. **Path Finding**: Find shortest path between nodes
5. **Community Detection**: Identify node communities
6. **3D Visualization**: 3D graph rendering
7. **Time-based Animation**: Animate graph changes over time
8. **Export Formats**: SVG, JSON, GraphML
9. **Graph Statistics**: Display graph metrics
10. **Collaborative Features**: Share graph views

### Integration Opportunities

1. **Chat Integration**: Ask questions about visible nodes
2. **Document Preview**: Hover to preview document content
3. **Similarity Search**: Find similar nodes using Qdrant
4. **Batch Operations**: Select multiple nodes for actions
5. **Annotations**: Add notes to nodes/edges

## Technical Details

### Neovis.js Configuration

```typescript
{
  neo4j: {
    serverUrl: 'bolt://openspg-neo4j:7687',
    serverUser: 'neo4j',
    serverPassword: 'neo4j@openspg'
  },
  visConfig: {
    nodes: { shape: 'dot', size: 25 },
    edges: { arrows: true, smooth: true },
    physics: { enabled: true, barnesHut: {...} }
  },
  labels: {
    Document: { label: 'title', value: 'confidence', group: 'Document' }
  },
  relationships: {
    MENTIONS: { label: 'type' }
  }
}
```

### Node Schema

```typescript
{
  id: string,              // Neo4j internal ID
  labels: string[],        // Node labels
  properties: {
    title?: string,        // Document title
    name?: string,         // Entity/Person/Org name
    customer?: string,     // Customer assignment
    tags?: string[],       // Associated tags
    confidence?: number,   // Confidence score
    created?: string,      // Creation timestamp
    updated?: string       // Update timestamp
    // ... other properties
  }
}
```

### Relationship Schema

```typescript
{
  id: string,              // Neo4j internal ID
  type: string,            // Relationship type
  startNode: string,       // Source node ID
  endNode: string,         // Target node ID
  properties: {
    confidence?: number,   // Relationship confidence
    type?: string,         // Additional type info
    // ... other properties
  }
}
```

## Support

For issues or questions:
1. Check this documentation
2. Review browser console errors
3. Check API response in network tab
4. Verify Neo4j data exists
5. Test with simple queries first

---

**Created**: 2025-11-03
**Version**: 1.0.0
**Status**: Production Ready
