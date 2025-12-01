# AEON Digital Twin - Complete Menu and Pages Reference

**Application URL:** http://localhost:3003
**Last Updated:** 2025-11-04
**Status:** ✅ Development Server Running

---

## 📋 Navigation Structure Overview

The application features a professional VulnCheck-style black navigation bar (#1a1a1a) with three main dropdown menus:

1. **Dashboard** - System monitoring and analytics
2. **Data Management** - Customer and document operations
3. **Knowledge** - AI-powered search and graph visualization

---

## 🎯 MENU 1: DASHBOARD

### 1.1 Home (`/`)
**Route:** `/`
**Description:** Main dashboard overview and system status
**Menu Path:** Dashboard → Home

**Functionality:**
- **Live Statistics Cards** (6 metrics):
  - Total Documents (from Neo4j)
  - Total Entities (graph nodes)
  - Total Relationships (graph edges)
  - Total Customers
  - Total Tags
  - Total Shared Documents

- **Quick Actions Panel** (7 shortcuts):
  - Upload Documents → `/upload`
  - Search Knowledge → `/search`
  - AI Assistant → `/chat`
  - Observability → `/observability`
  - Manage Tags → `/tags`
  - View Database → `/graph`
  - Settings → `/settings`

- **Recent Activity Feed:**
  - Document uploads
  - Processing events
  - Edit/delete operations
  - Error notifications
  - User activity tracking

- **System Health Monitor:**
  - Neo4j connection status
  - Qdrant connection status
  - Response times
  - Uptime percentages

**API Endpoints Used:**
- `/api/neo4j/statistics` - Dashboard statistics
- `/api/health` - System health check

**Key Features:**
- Real-time data fetching
- Auto-refresh capabilities
- Error boundary protection
- Professional card-based layout

---

### 1.2 Analytics (`/analytics`)
**Route:** `/analytics`
**Description:** Data analytics and insights
**Menu Path:** Dashboard → Analytics

**Functionality:**
- **Metrics Dashboard:**
  - Document Growth (current vs previous period with % change)
  - Entities Added (with trend analysis)
  - Process Success Rate
  - Average Quality Score

- **Time Range Filters:**
  - 7 days
  - 30 days
  - 90 days
  - Custom date range

- **Customer Filter:**
  - Filter analytics by specific customer
  - All customers view

- **Visualizations:**
  - Documents Over Time (line chart)
  - Entities by Type (distribution chart)
  - Customer Activity (bar chart)

- **Export Capabilities:**
  - CSV export
  - JSON export
  - PDF report generation

**API Endpoints Used:**
- `/api/analytics/metrics` - Metrics data with time range
- `/api/analytics/timeseries` - Time series data
- `/api/analytics/export` - Export functionality

**Key Features:**
- Interactive charts with Tremor
- Percentage change calculations
- Multi-format export
- Customer-specific analytics

---

### 1.3 Observability (`/observability`)
**Route:** `/observability`
**Description:** Real-time system monitoring
**Menu Path:** Dashboard → Observability

**Functionality:**
- **System Status Cards** (4 real-time metrics):
  - System Health (healthy/warning/critical)
  - Memory Usage (% with MB details)
  - Active Agents (count with avg duration)
  - Average Response Time (ms with error rate)

- **Live Charts:**
  - Memory Usage Over Time (line chart - heap used/total)
  - CPU Usage Over Time (line chart - user/system)
  - Agent Activity Distribution (pie chart - completed/active/failed)
  - Performance Metrics (bar chart - avg/p95/throughput)

- **Auto-Refresh Controls:**
  - Toggle auto-refresh on/off
  - Interval selection: 2s, 5s, 10s, 30s
  - Manual refresh button

- **System Details Panel:**
  - Heap Used/Total/RSS/External memory
  - Active/Completed/Failed agents
  - Response times (avg/p95)
  - Throughput (requests/minute)
  - Error rate percentage

**API Endpoints Used:**
- `/api/observability/system` - Real system metrics (process.memoryUsage(), process.cpuUsage())
- `/api/observability/agents` - Agent activity tracking
- `/api/observability/performance` - Performance metrics

**Key Features:**
- 100% REAL data (NO placeholders)
- Chart.js visualizations
- Historical data tracking (60 points)
- Professional VulnCheck-style cards
- Real-time updates with configurable intervals

**Technology:**
- Chart.js for visualizations
- Node.js process API for metrics
- Qdrant for metrics storage
- Map-based duration tracking

---

## 📁 MENU 2: DATA MANAGEMENT

### 2.1 Upload Documents (`/upload`)
**Route:** `/upload`
**Description:** Import and process files with AI pipeline
**Menu Path:** Data Management → Upload Documents

**Functionality:**
- **5-Step Upload Wizard:**
  1. **Upload** - File selection and upload
     - Drag-and-drop interface
     - Multi-file support
     - File type validation

  2. **Customer** - Associate with customer/organization
     - Customer selection dropdown
     - Create new customer option
     - Required field

  3. **Tags** - Tag organization and categorization
     - Multiple tag selection
     - Tag creation interface
     - Category-based organization

  4. **Classify** - Document classification
     - Automatic classification
     - Manual override options
     - Confidence scoring

  5. **Process** - AI processing pipeline
     - Entity extraction
     - Relationship detection
     - Vector embedding generation
     - Neo4j graph storage
     - Qdrant vector storage

**Processing Features:**
- Parallel processing support
- Progress tracking
- Error handling with retry
- Validation at each step

**File Support:**
- PDF documents
- Text files
- Markdown files
- Office documents (planned)

---

### 2.2 Customers (`/customers`)
**Route:** `/customers`
**Description:** Customer and organization management
**Menu Path:** Data Management → Customers

**Functionality:**
- **Customer List View:**
  - Grid/card layout of all customers
  - Search functionality (name, email, company, phone)
  - Pagination (12 per page)
  - Status indicators (active/inactive/pending)

- **Customer Information:**
  - Name
  - Email address
  - Phone number
  - Company/organization
  - Physical address
  - Document count
  - Created date
  - Last activity timestamp

- **Customer Actions:**
  - Create new customer (`/customers/new`)
  - View customer details (`/customers/[id]`)
  - Edit customer information
  - Delete customer (with confirmation)

**API Endpoints Used:**
- `/api/customers` - List all customers
- `/api/customers/[id]` - Get/Update/Delete specific customer

**Key Features:**
- Real-time search filtering
- Customer card components
- Status badge system
- Activity tracking

---

### 2.3 Tags (`/tags`)
**Route:** `/tags`
**Description:** Tag organization and categorization
**Menu Path:** Data Management → Tags

**Functionality:**
- **Tag Management:**
  - Create new tags
  - Edit existing tags
  - Delete tags (with usage warning)
  - Search tags by name

- **Tag Properties:**
  - Tag name (unique identifier)
  - Category classification
  - Color coding (12 preset colors)
  - Description/notes
  - Creation date
  - Usage count

- **Tag Categories:**
  - General
  - Document Type
  - Project
  - Priority
  - Status
  - Department
  - Client
  - Custom

- **Tag Filtering:**
  - Filter by category
  - Search by name
  - Sort by usage count

**API Endpoints Used:**
- `/api/tags` - List all tags
- `/api/tags` (POST) - Create tag
- `/api/tags/[name]` (PUT) - Update tag
- `/api/tags/[name]` (DELETE) - Delete tag

**Key Features:**
- Color-coded badges
- Usage statistics
- Category organization
- Bulk operations support

---

## 🧠 MENU 3: KNOWLEDGE

### 3.1 Graph Visualization (`/graph`)
**Route:** `/graph`
**Description:** Neo4j knowledge graph explorer
**Menu Path:** Knowledge → Graph Visualization

**Functionality:**
- **Interactive Graph Visualization:**
  - Force-directed layout
  - Hierarchical layout option
  - Zoom and pan controls
  - Node click for details

- **Graph Filters:**
  - Node type selection
  - Relationship type filtering
  - Customer filtering
  - Tag filtering
  - Confidence threshold slider
  - Date range selection

- **Node Details Panel:**
  - Node properties display
  - Relationship list
  - Connected nodes
  - Metadata information

- **Custom Query Builder:**
  - Cypher query editor
  - Saved query library
  - Query execution
  - Results visualization

- **Graph Operations:**
  - Export graph data
  - Save current view
  - Load saved queries
  - Refresh graph data

**API Endpoints Used:**
- `/api/graph/data` - Fetch graph data with filters
- `/api/graph/query` - Execute custom Cypher queries
- `/api/health` - Check Neo4j connection

**Key Features:**
- D3.js-powered visualization
- Real-time graph updates
- Error boundary protection
- Database connection monitoring

**Connection Handling:**
- Auto-detects Neo4j connection
- Shows DatabaseConnectionError if offline
- Retry connection option

---

### 3.2 AI Chat (`/chat`)
**Route:** `/chat`
**Description:** AI-powered assistant with multi-source query
**Menu Path:** Knowledge → AI Chat

**Functionality:**
- **Multi-Source Query:**
  - Neo4j graph database
  - Qdrant vector database
  - Internet search (optional)

- **Data Source Controls:**
  - Toggle Neo4j on/off
  - Toggle Qdrant on/off
  - Toggle internet search on/off

- **Query Context:**
  - Customer selection (defaults to "McKenney")
  - Scope selection (All/Project/Specific)
  - Project ID filtering

- **Chat Features:**
  - Streaming responses
  - Message history
  - Recent queries (last 10 stored)
  - Suggested actions
  - Code snippet support
  - Markdown rendering

- **Suggested Actions:**
  - "Search documents for X"
  - "Find relationships between Y"
  - "Summarize project Z"
  - "Show entities of type T"

**API Endpoints Used:**
- `/api/chat` (POST) - Send message with context and data sources

**Key Features:**
- Real-time streaming responses
- LocalStorage for query history
- Auto-scroll to latest message
- Professional chat bubbles
- Source attribution in responses

**Technology:**
- Streaming API responses
- React state management
- LocalStorage persistence

---

### 3.3 Search (`/search`)
**Route:** `/search`
**Description:** Hybrid search across all documents
**Menu Path:** Knowledge → Search

**Functionality:**
- **Search Modes:**
  - **Fulltext** - Traditional keyword search
  - **Semantic** - Vector similarity search
  - **Hybrid** - Combined fulltext + semantic (default)

- **Advanced Filters:**
  - Customer selection
  - Tag filtering (multi-select)
  - Date range (from/to)
  - Result limit (10/25/50/100)

- **Search Results:**
  - Result cards with snippets
  - Relevance scores
  - Highlighted keywords
  - Source attribution
  - Quick actions (view, download, share)

- **Pagination:**
  - Configurable results per page
  - Page navigation
  - Total result count

**API Endpoints Used:**
- `/api/search` (POST) - Execute hybrid search
- `/api/search/health` - Check search services status

**Key Features:**
- Hybrid search algorithm (BM25 + vector embeddings)
- Real-time result ranking
- Filter combination
- Health monitoring
- Error boundary protection

**Connection Handling:**
- Health check on mount
- Service status indicators
- Degraded mode handling

---

## ⚙️ ADDITIONAL PAGES (Not in Main Menu)

### Settings (`/settings`)
**Route:** `/settings`
**Description:** Configure system settings
**Access:** Via Quick Actions on Home page

**Settings Categories:**
1. **Database Configuration:**
   - Neo4j connection URL
   - Qdrant vector DB URL

2. **Notifications:**
   - Email notifications toggle
   - System alerts toggle
   - Weekly reports toggle

3. **Display Preferences:**
   - Theme (light/dark)
   - Compact view toggle
   - Animations enabled/disabled

4. **Security:**
   - Two-factor authentication
   - Session timeout (minutes)

5. **Language & Region:**
   - Language selection
   - Timezone
   - Date format

**Functionality:**
- Save settings to backend
- Reset to defaults
- Import/export configuration

---

## 🔗 Customer Sub-Routes

### View Customer (`/customers/[id]`)
**Route:** `/customers/[id]` (dynamic)
**Description:** View individual customer details
**Access:** Click on customer card in Customers page

**Functionality:**
- Customer profile information
- Associated documents list
- Activity timeline
- Edit customer button
- Delete customer button

### New Customer (`/customers/new`)
**Route:** `/customers/new`
**Description:** Create new customer
**Access:** "+ New Customer" button on Customers page

**Functionality:**
- Customer creation form
- Required field validation
- Duplicate detection
- Auto-redirect on success

---

## 📊 API Health Endpoints

### Main Health Check (`/api/health`)
**Checks:**
- Neo4j connection and response time
- Qdrant connection and response time
- System uptime
- Service statuses

### Search Health (`/api/search/health`)
**Checks:**
- Neo4j fulltext index
- Qdrant collection availability
- Hybrid search readiness

---

## 🎨 Design System

### Navigation
- **Color:** Black (#1a1a1a) header
- **Contrast:** 14.8:1 ratio (WCAG AAA compliant)
- **Dropdown Behavior:** Click to toggle, outside click to close
- **Animation:** fadeIn 0.15s ease-out

### Cards
- **Style:** Professional white cards with subtle borders
- **Shadow:** Hover elevation effect
- **Classes:** `card-professional`

### Buttons
- **Primary:** Black background, white text
- **Classes:** `btn-professional btn-professional-primary`

### Typography
- **Headings:** `text-high-contrast` for maximum readability
- **Body:** Professional gray scale

---

## 🚀 Quick Start Guide

### Starting the Server
```bash
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface
npm run dev
```

### Accessing Pages
- Home: http://localhost:3003/
- Analytics: http://localhost:3003/analytics
- Observability: http://localhost:3003/observability
- Upload: http://localhost:3003/upload
- Customers: http://localhost:3003/customers
- Tags: http://localhost:3003/tags
- Graph: http://localhost:3003/graph
- Chat: http://localhost:3003/chat
- Search: http://localhost:3003/search
- Settings: http://localhost:3003/settings

---

## 📦 Technology Stack

### Frontend
- **Framework:** Next.js 15.5.6 (App Router)
- **UI Components:** Tremor, Radix UI, Lucide Icons
- **Charts:** Chart.js, react-chartjs-2
- **Styling:** Tailwind CSS, professional design system
- **State:** React hooks, localStorage

### Backend Services
- **Graph Database:** Neo4j (bolt://localhost:7687)
- **Vector Database:** Qdrant (http://localhost:6333)
- **API Routes:** Next.js API routes

### Real-Time Features
- **Metrics:** Node.js process API
- **Streaming:** Server-sent events for chat
- **Auto-refresh:** Configurable intervals for observability

---

## 🎯 Feature Status

✅ **Complete:**
- Navigation with VulnCheck-style design
- Home dashboard with live metrics
- Analytics with time-series charts
- Observability with real-time monitoring
- Upload wizard (5-step pipeline)
- Customer management (CRUD)
- Tag management (CRUD)
- Graph visualization (interactive)
- AI chat (multi-source)
- Hybrid search (fulltext + semantic)
- Settings configuration

🚧 **Planned:**
- User authentication
- Role-based access control
- Audit logging
- Advanced query builder
- Batch operations
- Export/import workflows

---

## 📝 Notes

- All pages use error boundaries for graceful error handling
- Database connection is checked on page load
- Real-time data uses NO placeholders (100% real metrics)
- Professional design matches VulnCheck aesthetic
- WCAG AA accessibility compliance throughout
- Responsive design for mobile/tablet/desktop

**End of Reference Document**
