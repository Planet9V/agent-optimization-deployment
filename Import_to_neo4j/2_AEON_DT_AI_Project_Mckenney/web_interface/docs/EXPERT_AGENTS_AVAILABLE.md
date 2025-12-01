# Expert Agents Available

**Project:** AEON DT AI Project
**Version:** 1.0.0
**Last Updated:** 2025-11-03

## Overview

This project has access to specialized expert agents through the Claude-Flow and RUV-Swarm coordination systems. These experts can be spawned individually or in coordinated teams to handle specific development tasks.

## Available Expert Agents

### 🗄️ Neo4j Expert
**Specialization:** Neo4j database development and optimization

**Capabilities:**
- Database schema design and modeling
- Index strategy and performance tuning
- Connection pool optimization
- Neo4j Aura deployment
- Security and authentication setup
- Migration strategies

**When to Request:**
- "Design a Neo4j schema for [domain]"
- "Optimize Neo4j database performance"
- "Setup Neo4j connection with authentication"
- "Plan Neo4j migration strategy"

**Example Request:**
```
Spawn Neo4j expert to design a graph schema for construction project management
with entities for projects, phases, contractors, and materials.
```

---

### 🔍 Cypher Query Expert
**Specialization:** Advanced Cypher query writing and optimization

**Capabilities:**
- Complex Cypher query design
- Query performance optimization
- EXPLAIN/PROFILE analysis
- Pattern matching strategies
- Subquery optimization
- Index utilization

**When to Request:**
- "Optimize this slow Cypher query"
- "Write a query to find [complex pattern]"
- "Analyze query execution plan"
- "Refactor inefficient Cypher"

**Example Request:**
```
Spawn Cypher expert to optimize the project dependencies query and reduce
execution time from 5s to under 1s.
```

---

### ⚛️ Next.js Expert
**Specialization:** Next.js 15 App Router development

**Capabilities:**
- App Router architecture
- Server/Client Components
- React Server Actions
- API Routes and middleware
- Performance optimization
- TypeScript integration

**When to Request:**
- "Build a Next.js page for [feature]"
- "Implement authentication with middleware"
- "Optimize page load performance"
- "Setup API routes for [functionality]"

**Example Request:**
```
Spawn Next.js expert to build a dashboard page with server-side data fetching
from Neo4j and client-side interactivity.
```

---

### 🎨 Tailwind Expert
**Specialization:** Tailwind CSS styling and design systems

**Capabilities:**
- Responsive design
- Custom theme configuration
- Component styling
- Dark mode implementation
- Design system creation
- Accessibility styling

**When to Request:**
- "Create responsive layout for [component]"
- "Implement dark mode theme"
- "Build design system with Tailwind"
- "Style component library"

**Example Request:**
```
Spawn Tailwind expert to create a responsive card grid layout with hover effects
and dark mode support for the project listing page.
```

---

### 🌐 Neovis Expert
**Specialization:** Neovis.js graph visualization

**Capabilities:**
- Neovis configuration
- Graph rendering optimization
- Custom styling and themes
- Interactive features
- React/Next.js integration
- Performance tuning for large graphs

**When to Request:**
- "Build interactive graph visualization"
- "Integrate Neovis with Next.js"
- "Customize graph appearance"
- "Optimize graph rendering performance"

**Example Request:**
```
Spawn Neovis expert to create an interactive project dependency graph with
click-to-expand nodes and custom color-coding by status.
```

---

### 📊 D3 Expert
**Specialization:** Custom D3.js visualizations

**Capabilities:**
- Custom visualizations
- Force-directed layouts
- Data-driven animations
- SVG optimization
- Interactive data exploration
- React integration

**When to Request:**
- "Create custom [type] visualization"
- "Build force-directed graph layout"
- "Implement animated data transitions"
- "Design interactive data exploration"

**Example Request:**
```
Spawn D3 expert to create a custom timeline visualization showing project phases
with animated transitions between milestones.
```

---

### 🧮 Graph Algorithm Expert
**Specialization:** Neo4j Graph Data Science algorithms

**Capabilities:**
- Neo4j GDS library
- Community detection
- Centrality calculations
- Pathfinding algorithms
- Similarity analysis
- Link prediction

**When to Request:**
- "Implement [graph algorithm]"
- "Find communities in network"
- "Calculate node importance"
- "Build recommendation system"

**Example Request:**
```
Spawn Graph Algorithm expert to implement PageRank to identify the most critical
contractors in the project network.
```

---

### 📈 Data Visualization Expert
**Specialization:** Dashboards and analytics

**Capabilities:**
- Dashboard design
- Chart library integration
- Real-time data visualization
- Analytics UI patterns
- Performance metrics
- Responsive charts

**When to Request:**
- "Build analytics dashboard"
- "Create chart components"
- "Implement real-time metrics"
- "Design data exploration UI"

**Example Request:**
```
Spawn Data Visualization expert to build a project analytics dashboard with
budget tracking, timeline charts, and resource utilization metrics.
```

---

## Capability Matrix

| Task Type | Primary Expert | Supporting Experts |
|-----------|---------------|-------------------|
| Database Schema | neo4j-expert | cypher-query-expert |
| Query Optimization | cypher-query-expert | neo4j-expert |
| Web Pages | nextjs-expert | tailwind-expert |
| Graph Visualization | neovis-expert | d3-expert, cypher-query-expert |
| Custom Charts | d3-expert | data-visualization-expert |
| Dashboard | data-visualization-expert | nextjs-expert, tailwind-expert |
| Algorithms | graph-algorithm-expert | cypher-query-expert |
| Styling | tailwind-expert | nextjs-expert |
| Full-Stack Feature | nextjs-expert | neo4j-expert, tailwind-expert, cypher-query-expert |

## Example Use Cases

### Use Case 1: Project Dependencies Viewer
**Goal:** Build an interactive dependency graph for construction projects

**Expert Team:**
1. **Neo4j Expert:** Design schema for projects, phases, dependencies
2. **Cypher Query Expert:** Write optimized queries for dependency chains
3. **Neovis Expert:** Create interactive graph visualization
4. **Next.js Expert:** Integrate into web application

**Request Example:**
```
Coordinate expert team to build project dependencies viewer:
- Neo4j schema design
- Dependency traversal queries
- Interactive graph visualization
- Next.js integration with real-time updates
```

---

### Use Case 2: Construction Analytics Dashboard
**Goal:** Build comprehensive dashboard for project analytics

**Expert Team:**
1. **Cypher Query Expert:** Aggregation queries for metrics
2. **Data Visualization Expert:** Chart components and layouts
3. **Next.js Expert:** Server-side data fetching and routing
4. **Tailwind Expert:** Responsive dashboard styling

**Request Example:**
```
Build analytics dashboard with expert coordination:
- Budget tracking over time
- Resource utilization charts
- Project timeline visualizations
- Responsive layout with dark mode
```

---

### Use Case 3: Contractor Network Analysis
**Goal:** Analyze contractor relationships and identify key players

**Expert Team:**
1. **Graph Algorithm Expert:** Implement centrality algorithms
2. **Cypher Query Expert:** Efficient data retrieval for algorithms
3. **D3 Expert:** Custom network visualization
4. **Data Visualization Expert:** Metrics and summary statistics

**Request Example:**
```
Analyze contractor network using graph algorithms:
- Calculate contractor centrality (PageRank, Betweenness)
- Detect communities of frequent collaborators
- Visualize network with custom D3 force layout
- Display metrics dashboard with key insights
```

---

### Use Case 4: Database Performance Optimization
**Goal:** Improve Neo4j query performance for large datasets

**Expert Team:**
1. **Neo4j Expert:** Analyze database configuration and indexes
2. **Cypher Query Expert:** Profile and optimize slow queries
3. **Graph Algorithm Expert:** Implement efficient algorithms

**Request Example:**
```
Optimize Neo4j database performance:
- Audit current schema and indexes
- Profile slow queries with EXPLAIN/PROFILE
- Refactor queries with better patterns
- Add strategic indexes
- Implement efficient GDS algorithms
```

---

### Use Case 5: Project Timeline Visualization
**Goal:** Create interactive timeline for project phases

**Expert Team:**
1. **Cypher Query Expert:** Query temporal data efficiently
2. **D3 Expert:** Build custom timeline visualization
3. **Next.js Expert:** Integrate with App Router
4. **Tailwind Expert:** Style timeline components

**Request Example:**
```
Create interactive project timeline:
- Query project phases and milestones
- Custom D3 timeline with zoom and pan
- Color-code by status
- Integrate into Next.js page
- Responsive design with Tailwind
```

---

## How to Request Experts

### Single Expert Request
```
Spawn [expert-name] to [specific task with details]
```

**Example:**
```
Spawn Neo4j expert to design a schema for tracking construction materials,
suppliers, and orders with efficient querying in mind.
```

### Multi-Expert Coordination
```
Coordinate expert team for [goal]:
- [Expert 1]: [specific responsibility]
- [Expert 2]: [specific responsibility]
- [Expert 3]: [specific responsibility]
```

**Example:**
```
Coordinate expert team to build project dependencies feature:
- Neo4j expert: Design dependency schema
- Cypher expert: Write traversal queries
- Neovis expert: Create interactive visualization
- Next.js expert: Integrate into dashboard
```

### Parallel Execution
```
Execute in parallel:
- [Expert 1]: [independent task]
- [Expert 2]: [independent task]
- [Expert 3]: [independent task]
```

**Example:**
```
Execute in parallel:
- Cypher expert: Optimize existing queries
- Tailwind expert: Refactor component styles
- Data Viz expert: Add new chart types
```

### Sequential Pipeline
```
Execute sequentially:
1. [Expert 1]: [task providing foundation]
2. [Expert 2]: [task depending on #1]
3. [Expert 3]: [task depending on #2]
```

**Example:**
```
Execute sequentially:
1. Graph Algorithm expert: Implement community detection
2. Cypher expert: Create queries to run algorithm
3. D3 expert: Visualize community results
```

---

## Integration with Project

### Current Project Structure
```
web_interface/
├── app/              # Next.js App Router
├── components/       # React components
├── lib/             # Utilities and Neo4j client
├── public/          # Static assets
└── docs/            # Documentation
```

### Expert Access Points
- **Next.js Expert:** Works in `app/` and `components/`
- **Neo4j Expert:** Works on `lib/neo4j.ts` and schema
- **Cypher Expert:** Creates queries in `lib/queries/`
- **Tailwind Expert:** Styles components and updates `tailwind.config.js`
- **Visualization Experts:** Create components in `components/visualizations/`

---

## Best Practices

1. **Be Specific:** Provide detailed requirements for better results
2. **Define Success:** Specify what "done" looks like
3. **Coordinate Related Tasks:** Use multi-expert teams for complex features
4. **Sequential When Dependent:** Pipeline tasks with dependencies
5. **Parallel When Independent:** Speed up by running independent tasks together
6. **Review and Iterate:** Experts can refine based on feedback

---

## Coordination Systems

### Claude-Flow
- Swarm initialization and topology
- Agent spawning and coordination
- Task orchestration
- Memory management

### RUV-Swarm
- Advanced neural coordination
- Decentralized autonomous agents
- Knowledge sharing
- Adaptive learning

Both systems work together to provide intelligent expert coordination with learning capabilities.

---

## Getting Started

### Basic Request Pattern
1. Identify the task or feature
2. Determine which expert(s) are needed
3. Provide specific requirements
4. Specify coordination needs (parallel/sequential)
5. Define success criteria

### Example First Request
```
I need help building a project listing page.

Coordinate expert team:
- Neo4j expert: Verify schema can support project listing with filters
- Cypher expert: Write efficient query for paginated project list with search
- Next.js expert: Build /projects page with server-side data fetching
- Tailwind expert: Create responsive card layout for project cards

Requirements:
- Pagination (20 per page)
- Search by name, location, status
- Sort by date, budget, name
- Mobile-responsive card grid
- Loading states and error handling
```

---

## Support and Questions

For questions about:
- **Expert capabilities:** Review this document
- **Coordination patterns:** See `/home/jim/.claude/swarm/expert-coordination-guide.md`
- **Technical details:** Check `/home/jim/.claude/swarm/expert-registry.json`

---

**Ready to leverage expert agents for your development tasks!**
