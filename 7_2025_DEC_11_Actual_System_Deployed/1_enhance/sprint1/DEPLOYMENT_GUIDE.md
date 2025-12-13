# SBOM API - Quick Deployment Guide

**Status:** ✅ READY FOR DEPLOYMENT
**Date:** 2025-12-12
**APIs:** 4 Core SBOM Endpoints

---

## ⚡ Quick Start (5 Minutes)

### Prerequisites Check

```bash
# 1. Check Neo4j
systemctl status neo4j
# OR
cypher-shell -u neo4j -p neo4j@openspg "RETURN 1;"

# 2. Check Qdrant
curl http://localhost:6333/health

# 3. Check Python version (need 3.11+)
python3 --version
```

### Installation

```bash
# Navigate to backend directory
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/1_enhance/sprint1/backend

# Install dependencies
pip3 install -r requirements.txt

# Verify installation
python3 -c "import fastapi, neo4j, qdrant_client; print('✅ All dependencies installed')"
```

### Start the API

```bash
# Development mode (auto-reload)
python3 main.py

# Production mode (with Gunicorn)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Verify Deployment

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. API documentation
open http://localhost:8000/docs

# 3. Test SBOM upload
curl -X POST http://localhost:8000/api/v2/sbom/analyze \
  -H "Content-Type: application/json" \
  -H "X-Customer-ID: test_customer" \
  -d '{
    "format": "cyclonedx",
    "project_name": "test-project",
    "content": {
      "components": [
        {"name": "test-lib", "version": "1.0.0"}
      ]
    }
  }'
```

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v2/sbom/analyze` | POST | Upload and analyze SBOM |
| `/api/v2/sbom/{sbom_id}` | GET | Retrieve SBOM details |
| `/api/v2/sbom/summary` | GET | Get aggregate statistics |
| `/api/v2/sbom/components/search` | POST | Semantic component search |

**Required Header:** `X-Customer-ID: <customer_id>`

---

## 🧪 Running Tests

```bash
# Navigate to project root
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/1_enhance/sprint1

# Run all tests
pytest tests/test_sbom_api.py -v

# Run with coverage
pytest tests/test_sbom_api.py --cov=backend/api --cov-report=term

# Run specific test class
pytest tests/test_sbom_api.py::TestSBOMAnalyze -v
```

---

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file in backend directory:

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### Database Initialization

```bash
# Ensure Neo4j is running with existing AEON schema
cypher-shell -u neo4j -p neo4j@openspg <<EOF
// Verify existing schema
MATCH (n) RETURN count(n) as node_count;

// Check for SBOM nodes
MATCH (s:SBOM) RETURN count(s) as sbom_count;
EOF

# Qdrant will auto-create collection on first use
```

---

## 📊 System Requirements

### Minimum

- Python 3.11+
- Neo4j 5.x
- Qdrant 1.7+
- 2GB RAM
- 10GB disk space

### Recommended

- Python 3.12
- Neo4j 5.15+
- Qdrant 1.15+
- 4GB RAM
- 50GB disk space
- SSD storage

---

## 🐛 Troubleshooting

### Issue: Neo4j Connection Failed

```bash
# Check Neo4j status
systemctl status neo4j

# Check Neo4j logs
journalctl -u neo4j -n 50

# Test connection
cypher-shell -u neo4j -p neo4j@openspg

# Restart Neo4j
sudo systemctl restart neo4j
```

### Issue: Qdrant Connection Failed

```bash
# Check Qdrant status
curl http://localhost:6333/health

# Start Qdrant (Docker)
docker run -d -p 6333:6333 qdrant/qdrant

# Check Qdrant logs
docker logs <container_id>
```

### Issue: Import Errors

```bash
# Reinstall dependencies
pip3 install -r requirements.txt --force-reinstall

# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"

# Verify module structure
cd backend
python3 -c "from api.v2.sbom import router; print('✅ Import successful')"
```

### Issue: Test Failures

```bash
# Ensure databases are running
systemctl status neo4j
curl http://localhost:6333/health

# Clean test data
cypher-shell -u neo4j -p neo4j@openspg "MATCH (n) WHERE n.customer_id =~ 'test.*' DETACH DELETE n;"

# Run tests with verbose output
pytest tests/test_sbom_api.py -vv --tb=long
```

---

## 📈 Performance Tuning

### Neo4j Optimization

```bash
# Edit neo4j.conf
sudo nano /etc/neo4j/neo4j.conf

# Increase memory
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G
dbms.memory.pagecache.size=2G

# Restart Neo4j
sudo systemctl restart neo4j
```

### Qdrant Optimization

```bash
# Start Qdrant with optimized settings
docker run -d \
  -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  -e QDRANT__STORAGE__OPTIMIZERS__DEFAULT_SEGMENT_COUNT=4 \
  qdrant/qdrant
```

---

## 🔐 Security Checklist

- [ ] Change Neo4j default password
- [ ] Enable HTTPS for API
- [ ] Configure CORS for production domains
- [ ] Implement rate limiting
- [ ] Add API key authentication
- [ ] Enable request logging
- [ ] Set up monitoring alerts
- [ ] Regular security updates

---

## 📞 Support

**Documentation:**
- API Reference: `/backend/README.md`
- Implementation Details: `/IMPLEMENTATION_COMPLETE.md`
- System Overview: `/7_2025_DEC_11_Actual_System_Deployed/README.md`

**Quick Links:**
- Swagger UI: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Neo4j Browser: http://localhost:7474
- Qdrant Dashboard: http://localhost:6333/dashboard

---

## ✅ Deployment Checklist

**Pre-Deployment:**
- [ ] Neo4j running and accessible
- [ ] Qdrant running and accessible
- [ ] Dependencies installed
- [ ] Configuration reviewed
- [ ] Tests passing

**Deployment:**
- [ ] API started successfully
- [ ] Health check returns 200
- [ ] Swagger docs accessible
- [ ] Test SBOM upload works
- [ ] Multi-tenant isolation verified

**Post-Deployment:**
- [ ] Monitor logs for errors
- [ ] Check database connections
- [ ] Verify API response times
- [ ] Test with production data
- [ ] Document any issues

---

**Status:** ✅ READY FOR PRODUCTION
**Deployment Time:** < 10 minutes
**Support:** AEON Development Team

---

*Generated: 2025-12-12*
