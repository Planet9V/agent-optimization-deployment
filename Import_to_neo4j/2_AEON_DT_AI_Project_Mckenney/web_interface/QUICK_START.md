# AEON Web Interface - Quick Start Guide

## 🎉 Web Interface is Running!

The AEON web interface has been successfully deployed and tested.

## 📍 Access Information

- **Local URL**: http://localhost:8501
- **Network URL**: http://172.30.253.47:8501
- **External URL**: http://76.249.187.4:8501

## 📊 Current System Status

✅ **Neo4j Database**: Connected and operational
- 115 documents indexed
- 12,256 entities extracted
- 14,645 relationships mapped

✅ **Web Interface**: Running on port 8501
✅ **All Pages**: Dashboard, Documents, Entities, Analytics, System Control

## 🚀 Starting the Interface

### For Future Sessions

```bash
# Navigate to web interface directory
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface

# Activate virtual environment
source venv/bin/activate

# Set Neo4j password
export NEO4J_PASSWORD="neo4j@openspg"

# Launch web interface
streamlit run app.py
```

### Quick Launch Script

Create a launch script for convenience:

```bash
#!/bin/bash
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface
source venv/bin/activate
export NEO4J_PASSWORD="neo4j@openspg"
streamlit run app.py
```

Save as `launch.sh`, make executable with `chmod +x launch.sh`, then run `./launch.sh`

## 🎯 Available Features

### 1. Dashboard (Home Page)
- Real-time system status
- Processing statistics
- Database metrics
- Sector distribution charts
- Recent documents
- Quick start/stop controls

### 2. Documents Browser
- Search documents by title/content
- Filter by sector, subsector, type
- Paginated browsing (10/20/50/100 per page)
- View document details and metadata
- See extracted entities per document

### 3. Entities Explorer
- Browse all extracted entities
- Filter by entity type (PRODUCT, GPE, DATE, etc.)
- View entity network graph
- See documents containing each entity
- Global search across documents and entities

### 4. Analytics Dashboard
- Comprehensive system metrics
- Processing pipeline visualization
- Distribution charts (sectors, entity types)
- Top entities analysis
- Data export (CSV/JSON)

### 5. System Control
- Start/Stop document monitoring
- View system configuration
- Test database connection
- Monitor system health
- View error logs
- Built-in documentation

## 🔧 Orchestrator Control

### Starting Document Ingestion

1. Navigate to **System Control** page (sidebar)
2. Click **🚀 Start Monitoring**
3. Orchestrator begins watching configured directories:
   - `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/data/raw`
   - `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/data/processed`
4. Monitor progress on Dashboard

### Stopping Document Ingestion

1. Navigate to **System Control** page
2. Click **⏸️ Stop Monitoring**
3. Orchestrator gracefully shuts down

## 📂 Data Management

### Adding Documents for Processing

1. Place files in watched directories:
   - Supported formats: PDF, DOCX, HTML, MD, TXT
   - Place in `/data/raw` for processing

2. Start monitoring (if not running)

3. Watch progress:
   - Dashboard shows processing statistics
   - Documents appear in Documents browser after ingestion
   - Entities extracted and visible in Entities explorer

### Searching & Filtering

**Documents**:
- Full-text search across titles and content
- Filter by sector, subsector, document type
- Sort by processed date

**Entities**:
- Search by entity name
- Filter by entity type
- View by document count

## 🐛 Troubleshooting

### Interface Won't Load

1. Verify Streamlit is running: `ps aux | grep streamlit`
2. Check logs: `tail -f streamlit.log`
3. Restart if needed: Kill process and run launch command

### Cannot Connect to Database

1. Verify Neo4j is running: `docker ps | grep openspg-neo4j`
2. Check password: `echo $NEO4J_PASSWORD`
3. Test connection: `docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"`

### Orchestrator Won't Start

1. Check configuration file exists: `ls ../config/main_config.yaml`
2. Verify watch directories are valid
3. Check System Control page for error messages
4. Review error log in System Control page

### No Documents Showing

1. Verify database has documents: Check Dashboard metrics
2. Clear search filters in Documents page
3. Check sector filter is set to "All"
4. Refresh page (F5)

## 🔐 Environment Variables

Required environment variable:
```bash
export NEO4J_PASSWORD="neo4j@openspg"
```

Optional (defaults shown):
```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
```

## 📈 Performance Tips

- Use pagination for large datasets
- Apply filters before searching
- Use specific entity type filters
- Export data for offline analysis
- Monitor queue size to track processing backlog

## 🎯 Next Steps (Phase 2)

Phase 1 (Streamlit Prototype) is complete. Future enhancements planned:

- **FastAPI Backend**: RESTful API for external integrations
- **Vue.js Frontend**: Modern, responsive UI
- **WebSocket Support**: Real-time updates without page refresh
- **File Upload**: Drag-and-drop document upload
- **Classification Review**: Correct low-confidence classifications
- **Advanced Visualizations**: Interactive relationship graphs
- **Batch Operations**: Reprocess multiple documents
- **Authentication**: Role-based access control
- **Docker Deployment**: Containerized web service

## 📞 Support

- Full documentation: See `README.md`
- AEON system docs: Parent directory documentation
- Neo4j issues: See `DOCKER_INFRASTRUCTURE.md`

---

*AEON Web Interface - Phase 1 (Streamlit Prototype)*
*Version: 1.0 | Date: 2025-11-03*
*Status: ✅ OPERATIONAL*
