# AEON Web Interface

**Version**: 1.0 (Phase 1 - Streamlit Prototype)
**Created**: 2025-11-03

A web-based interface for managing the AEON Automated Document Ingestion System.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Running Neo4j instance (openspg-neo4j at bolt://localhost:7687)
- AEON system installed (parent directory)

### Installation

```bash
# Navigate to web interface directory
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface

# Install dependencies
pip install -r requirements.txt

# Set Neo4j password (if not already set)
export NEO4J_PASSWORD="neo4j@openspg"
```

### Launch

```bash
# Start the web interface
streamlit run app.py
```

The interface will open automatically at **http://localhost:8501**

---

## 🔌 Backend API

**API Version:** 3.3.0
**Base URL:** http://localhost:8000
**Total Endpoints:** 230
**Documentation:** [Complete API Reference](./docs/COMPLETE_API_REFERENCE.md) | [Quick Start Guide](./docs/API_QUICK_START.md)

### API Categories

| Phase | Category | Endpoints |
|-------|----------|-----------|
| **B2** | SBOM Management | 33 |
| **B2** | Vendor & Equipment | 19 |
| **B3** | Threat Intelligence | 25 |
| **B3** | Risk Management | 27 |
| **B3** | Remediation | 26 |
| **B4** | Compliance | 21 |
| **B5** | Alerts | 19 |
| **B5** | Demographics | 24 |
| **B5** | Economic Analysis | 27 |
| - | Psychometric | 8 |
| - | Search | 3 |
| - | Health | 1 |

**Quick Example:**
```bash
# Check API health
curl http://localhost:8000/health

# List SBOMs
curl -H "X-Customer-ID: customer123" \
     http://localhost:8000/api/v2/sbom/sboms
```

See [API Quick Start](./docs/API_QUICK_START.md) for more examples.

---

## 📋 Features

### Dashboard (app.py)
- **Real-time System Status**: Monitor orchestrator running/stopped state
- **Processing Statistics**: Live pipeline metrics (discovered, converted, classified, ingested)
- **Database Statistics**: Document/entity/relationship counts
- **Visual Analytics**: Sector distribution and entity type charts
- **Recent Documents**: View latest processed documents
- **Quick Actions**: Start/stop monitoring with one click

### Documents Page
- **Browse Documents**: Paginated document listing
- **Search**: Full-text search across titles and content
- **Filter**: By sector, subsector, document type
- **Document Details**: View content, metadata, and extracted entities
- **Entity Exploration**: See all entities extracted from each document

### Entities Page
- **Entity Browser**: Explore all extracted entities
- **Search**: Find entities by name or type
- **Filter**: By entity type (VENDOR, PROTOCOL, STANDARD, etc.)
- **Entity Network**: Visualize top entities as interactive graph
- **Document Links**: See which documents contain each entity
- **Global Search**: Search across both documents and entities

### Analytics Page
- **Comprehensive Metrics**: System-wide statistics
- **Processing Pipeline**: Visual pipeline progress
- **Distribution Charts**: Sector and entity type breakdowns
- **Top Entities**: Most frequently occurring entities
- **Data Export**: Download statistics as CSV/JSON

### System Control Page
- **Orchestrator Management**: Start/stop document monitoring
- **Configuration View**: See all system settings
- **Connection Tests**: Verify Neo4j connectivity
- **Health Monitoring**: System status and error logs
- **Quick Start Guide**: Built-in documentation

---

## 🏗️ Architecture

### Directory Structure

```
web_interface/
├── app.py                      # Main dashboard (entry point)
├── pages/
│   ├── 1_Documents.py          # Document browser
│   ├── 2_Entities.py           # Entity explorer
│   ├── 3_Analytics.py          # Analytics dashboard
│   └── 4_System.py             # System control
├── utils/
│   ├── neo4j_connector.py      # Neo4j connection & queries
│   ├── orchestrator_control.py # Orchestrator lifecycle management
│   └── visualizations.py       # Chart generation utilities
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Integration Points

**Neo4j Database**:
- URI: `bolt://localhost:7687`
- Container: `openspg-neo4j`
- Shared with OpenSPG and AEON ingestion

**AEON Orchestrator**:
- Thread-safe lifecycle management
- Real-time status monitoring
- Reads from `config/main_config.yaml`

**Configuration**:
- Uses existing AEON configuration
- No duplicate settings needed
- Environment variable for password

---

## 🔧 Configuration

### Environment Variables

```bash
# Required
export NEO4J_PASSWORD="neo4j@openspg"

# Optional (defaults shown)
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
```

### Streamlit Configuration

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
port = 8501
headless = false
```

---

## 📊 Usage Guide

### Starting Document Ingestion

1. Navigate to **System Control** page (⚙️)
2. Click **🚀 Start Monitoring**
3. Orchestrator begins watching configured directories
4. Return to **Dashboard** to monitor progress

### Browsing Documents

1. Navigate to **Documents** page (📄)
2. Use search box to find specific documents
3. Apply filters (sector, subsector, type)
4. Click document expander to view details
5. Click "View Entities" to see extracted entities

### Exploring Entities

1. Navigate to **Entities** page (🔍)
2. Filter by entity type (VENDOR, PROTOCOL, etc.)
3. Click entity expander for details
4. Click "Show Documents" to see related documents
5. Use Global Search for cross-entity-document queries

### Viewing Analytics

1. Navigate to **Analytics** page (📊)
2. View system overview metrics
3. Explore distribution charts
4. Check top entities list
5. Export data as CSV or JSON

---

## 🎯 Features by Page

| Page | Key Features |
|------|-------------|
| **Dashboard** | System status, processing stats, recent documents, quick start/stop |
| **Documents** | Search, filter, browse, view content, see entities |
| **Entities** | Browse entities, filter by type, network graph, find documents |
| **Analytics** | Metrics, charts, top entities, data export |
| **System** | Start/stop monitoring, config view, health checks, documentation |

---

## 🔍 Troubleshooting

### Cannot Connect to Neo4j

**Problem**: "Unable to connect to Neo4j database"

**Solutions**:
1. Verify Neo4j container is running: `docker ps | grep openspg-neo4j`
2. Check password: `echo $NEO4J_PASSWORD`
3. Test connection: `docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"`
4. Verify port 7687 is accessible: `netstat -tuln | grep 7687`

### Orchestrator Won't Start

**Problem**: Click "Start Monitoring" but nothing happens

**Solutions**:
1. Check error message in UI
2. Verify config file exists: `ls ../config/main_config.yaml`
3. Check watch directories are valid
4. Review orchestrator logs for errors

### No Documents Showing

**Problem**: Database shows 0 documents

**Solutions**:
1. Start monitoring first (System Control → Start Monitoring)
2. Check watch directories have files
3. Wait for pipeline to process (check queue size)
4. Verify ingestion completed (Dashboard → Processing Stats)

### Pages Won't Load

**Problem**: Clicking page links causes errors

**Solutions**:
1. Ensure all page files are in `pages/` directory
2. Check file permissions: `ls -la pages/`
3. Restart Streamlit: Ctrl+C and `streamlit run app.py`
4. Clear Streamlit cache: `streamlit cache clear`

---

## 🚀 Performance Tips

### For Large Datasets

- Use pagination (adjust "Results per page")
- Apply filters before searching
- Use specific entity type filters
- Export data for offline analysis

### For Slow Queries

- Create Neo4j indexes (see main AEON docs)
- Reduce page sizes
- Filter by specific sectors/types
- Use Global Search sparingly

---

## 📈 Future Enhancements (Phase 2)

Planned for FastAPI + Vue.js production version:

- **Real-time Updates**: WebSocket for live status
- **Drag-and-Drop Upload**: Upload documents directly via UI
- **Classification Review**: Correct low-confidence classifications
- **Entity Graph Visualization**: Interactive relationship graphs
- **Batch Operations**: Reprocess multiple documents
- **User Authentication**: Role-based access control
- **RESTful API**: External integrations
- **Docker Deployment**: Containerized web service

---

## 🤝 Contributing

This is Phase 1 (Streamlit Prototype). For production deployment, Phase 2 (FastAPI + Vue.js) will be implemented.

---

## 📞 Support

For issues related to:
- **Web Interface**: Check this README and troubleshooting section
- **AEON System**: See parent directory documentation
- **Neo4j**: Consult Neo4j documentation and DOCKER_INFRASTRUCTURE.md

---

## 📝 Version History

- **v1.0** (2025-11-03): Initial Streamlit prototype release
  - Dashboard with live monitoring
  - Document browser with search
  - Entity explorer with network graph
  - Analytics dashboard with export
  - System control with configuration view

---

## 🎯 Quick Reference

**Start Web Interface**:
```bash
cd web_interface && streamlit run app.py
```

**Install Dependencies**:
```bash
pip install -r requirements.txt
```

**Set Environment**:
```bash
export NEO4J_PASSWORD="neo4j@openspg"
```

**Access URL**:
- Local: http://localhost:8501
- Network: http://<your-ip>:8501

---

*AEON Web Interface - Phase 1 (Streamlit Prototype)*
*Simple, Fast, Effective Document Management*
