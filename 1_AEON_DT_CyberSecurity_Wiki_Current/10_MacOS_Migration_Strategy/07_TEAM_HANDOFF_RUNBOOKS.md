# AEON Digital Twin macOS - Team Handoff & Operational Runbooks

**File:** 07_TEAM_HANDOFF_RUNBOOKS.md
**Created:** 2025-12-04 15:45:00 UTC
**Version:** 1.0.0
**Purpose:** Comprehensive team onboarding, operational procedures, and knowledge transfer for macOS development environment
**Status:** COMPLETE - Ready for Team Implementation

---

## 📋 Quick Navigation

- [Team Onboarding (5-Day Plan)](#5-day-team-onboarding-plan)
- [Role-Specific Training](#role-specific-training-paths)
- [Daily Startup Runbook](#daily-startup-runbook)
- [Service Management](#service-management-procedures)
- [Backup & Recovery](#backup-and-recovery-procedures)
- [Incident Response](#incident-response-playbooks)
- [Knowledge Base](#knowledge-base-location-guide)

---

## 5-Day Team Onboarding Plan

### Day 1: Environment Setup & Architecture Overview (Full Day - 8 hours)

**Morning (9 AM - 12 PM): Environment Setup**

Tasks:
1. Clone project from git bundle or GitHub
   ```bash
   git clone ~/Projects/aeon-dt-migration/aeon-dt.bundle aeon-dt
   cd aeon-dt
   git remote add origin https://github.com/your-org/aeon-dt.git
   ```

2. Install dependencies
   ```bash
   # Backend
   cd 5_NER11_Gold_Model
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Frontend
   cd 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1
   npm install
   ```

3. Verify environment
   ```bash
   # Check versions
   python --version  # Expected: 3.11+
   npm --version    # Expected: 18+
   git --version    # Expected: 2.40+
   docker --version # Expected: 24+
   ```

4. Grant system access
   - GitHub SSH keys setup and testing
   - Docker registry credentials
   - Database access credentials (provide securely)
   - API keys for external services

**Success Criteria:** All tools installed, SSH keys configured, can access GitHub

---

**Afternoon (1 PM - 5 PM): Architecture Overview**

Tasks:
1. Architecture study (1-1.5 hours)
   - Read: `00_MIGRATION_MASTER_PLAN.md` - Overall strategy
   - Read: `ARCHITECTURE_OVERVIEW.md` if available - System design
   - Watch: Architecture walkthrough video (if available)

2. Service exploration (1.5-2 hours)
   ```bash
   # Start all services
   docker-compose -f docker-compose.databases.yml up -d

   # Verify running
   docker ps
   # Expected: 9 containers running

   # Check service status
   curl http://localhost:8000/health
   curl http://localhost:7474  # Neo4j browser
   ```

3. Database exploration
   ```bash
   # Neo4j - explore node types
   docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
     "MATCH (n) RETURN DISTINCT labels(n) as entity_type, COUNT(*) as count LIMIT 20"

   # MySQL - explore tables
   docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" -e \
     "USE openspg; SHOW TABLES; SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES;"
   ```

4. API documentation review
   - Location: `04_APIs/00_API_STATUS_AND_ROADMAP.md`
   - Review: 251+ endpoints across 11 modules
   - Understand: API categories and dependencies

**Success Criteria:** Can navigate architecture, explain service purpose, understand API structure

---

### Day 2: Service Startup & API Testing (Full Day - 8 hours)

**Morning (9 AM - 12 PM): Service Startup**

Tasks:
1. Complete service startup (30 min)
   ```bash
   # Following: Daily Startup Runbook (below)
   docker-compose -f docker-compose.databases.yml up -d

   # Verify all healthy
   docker ps --format "table {{.Names}}\t{{.Status}}"
   # Expected: All containers HEALTHY or RUNNING
   ```

2. Verify database connectivity (30 min)
   ```bash
   # Neo4j
   docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
     "MATCH (n) RETURN COUNT(n) as total_nodes"
   # Expected: 20739 nodes

   # MySQL
   docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" \
     -e "SELECT COUNT(*) as table_count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='openspg';"
   # Expected: 18+ tables

   # Qdrant
   curl -X GET http://localhost:6333/health
   # Expected: {"status":"ok"}
   ```

3. NER11 model verification (1 hour)
   ```bash
   cd 5_NER11_Gold_Model
   source venv/bin/activate

   python -c "
   import spacy
   from spacy_ke import build_extractor

   nlp = spacy.load('ner11')
   doc = nlp('APT-28 exploited Windows vulnerability CVE-2023-123456')
   print('Entities extracted:')
   for ent in doc.ents:
     print(f'  {ent.text} -> {ent.label_}')
   "
   # Expected: Correct NER labels assigned
   ```

**Success Criteria:** All services running, databases healthy, model loads and works

---

**Afternoon (1 PM - 5 PM): API Testing**

Tasks:
1. API health check (30 min)
   ```bash
   # Test core endpoints
   curl http://localhost:8000/health
   curl http://localhost:8000/api/v1/endpoints  # List all endpoints

   # Expected: Returns JSON with status "healthy" and endpoint list
   ```

2. NER11 API testing (1.5 hours)
   ```bash
   # Test extraction endpoint
   curl -X POST http://localhost:8000/api/v1/ner11/extract \
     -H "Content-Type: application/json" \
     -d '{
       "text": "APT-28 targeted Microsoft Exchange servers with vulnerability CVE-2021-27065",
       "labels": ["THREAT_ACTOR", "ENTITY", "VULNERABILITY"]
     }'
   # Expected: Returns extracted entities with confidence scores
   ```

3. Phase B3-B5 API testing (1.5 hours)
   ```bash
   # Test Threat Intelligence API (Phase B3)
   curl http://localhost:8000/api/v1/threat-intelligence/indicators

   # Test Risk Scoring API (Phase B3)
   curl http://localhost:8000/api/v1/risk/score-entity -X POST

   # Test Compliance API (Phase B4)
   curl http://localhost:8000/api/v1/compliance/frameworks

   # Test Demographics API (Phase B5)
   curl http://localhost:8000/api/v1/demographics/sector-analysis
   ```

4. Frontend verification (30 min)
   ```bash
   # Build and serve frontend
   cd 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1
   npm run build
   # Expected: Build completes successfully

   npm run dev
   # Open http://localhost:3000 in browser
   # Expected: Dashboard loads with data
   ```

**Success Criteria:** All APIs responding, NER11 extracts entities correctly, frontend displays data

---

### Day 3: Code Repository & Development Workflow (Full Day - 8 hours)

**Morning (9 AM - 12 PM): Repository Navigation**

Tasks:
1. Repository structure exploration (1 hour)
   ```bash
   # Understand directory layout
   tree -L 2 -I 'node_modules|__pycache__|.git' ~/Projects/aeon-dt

   # Key directories:
   # 5_NER11_Gold_Model/ - Backend API and models
   # 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1/ - Frontend
   # 04_APIs/ - API documentation
   # 10_MacOS_Migration_Strategy/ - Migration guides (this project)
   ```

2. API code walkthrough (1 hour)
   ```bash
   # Backend code structure
   cd 5_NER11_Gold_Model
   find api -name "*.py" -type f | head -20

   # Review key modules
   cat api/__init__.py  # Module structure
   cat api/threat_intelligence/threat_models.py  # Example models
   ```

3. Frontend code walkthrough (1 hour)
   ```bash
   # Frontend code structure
   cd 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1
   find src -name "*.tsx" -type f | head -20

   # Review key components
   ls src/components/
   # Common: Dashboard, Charts, DataTable, Forms
   ```

**Success Criteria:** Can navigate repository, find API code, understand component structure

---

**Afternoon (1 PM - 5 PM): Development Workflow**

Tasks:
1. Git branch strategy (1 hour)
   ```bash
   # Current branches
   git branch -a

   # Understanding strategy
   # main/master - Production-ready code
   # develop - Development branch for next release
   # feature/* - New features
   # bugfix/* - Bug fixes
   # hotfix/* - Critical production fixes
   ```

2. Create feature branch and make changes (2 hours)
   ```bash
   # Create branch
   git checkout -b feature/test-onboarding

   # Make a small test change
   echo "# Test feature" > TEST_ONBOARDING.md

   # Stage and commit
   git add TEST_ONBOARDING.md
   git commit -m "feat(onboarding): Add test file for verification

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

   # Verify
   git log --oneline -5
   ```

3. Pull request process (1 hour)
   ```bash
   # Push branch
   git push -u origin feature/test-onboarding

   # Create PR (requires GitHub CLI or web interface)
   gh pr create --title "Test onboarding feature" \
     --body "Verification that new team member can create PR"

   # Request reviewers (at least 2)
   # Wait for approvals (typically 24-48 hours)
   # Merge when approved
   ```

4. Commit message standards (30 min)
   - Format: `<type>(<scope>): <description>`
   - Types: feat, fix, docs, refactor, test, perf, ci, chore
   - Scopes: specific component/module
   - Must include co-author and Claude Code attribution
   - Examples reviewed in guide

**Success Criteria:** Can create branch, make changes, create PR with proper formatting

---

### Day 4: Database Schema & Data Pipeline (Full Day - 8 hours)

**Morning (9 AM - 12 PM): Neo4j Schema Exploration**

Tasks:
1. Neo4j schema exploration (2 hours)
   ```bash
   # Launch Neo4j browser
   open http://localhost:7474  # macOS
   # Username: neo4j
   # Password: neo4j@openspg

   # Explore schema
   CALL db.schema.visualization()

   # List all node labels
   CALL db.labels()

   # List relationships
   CALL db.relationshipTypes()
   ```

2. Query commonly used entities (2 hours)
   ```bash
   # Threat actors
   MATCH (ta:THREAT_ACTOR) RETURN ta.name, COUNT(ta) LIMIT 10

   # Vulnerabilities
   MATCH (v:VULNERABILITY) RETURN v.cve_id, v.severity LIMIT 10

   # Sector analysis
   MATCH (s:SECTOR)-[:OPERATES_IN]->(c:COUNTRY)
   RETURN s.name, COUNT(c) ORDER BY COUNT(c) DESC LIMIT 10

   # Attack patterns
   MATCH (ta:THREAT_ACTOR)-[:USES]->(t:TECHNIQUE)
   RETURN ta.name, COLLECT(t.name) LIMIT 5
   ```

3. Create bookmarks for common queries
   ```bash
   # Save these queries in Neo4j for quick access
   # Threat Actor Profile - common search
   # Vulnerability Impact Analysis
   # Sector Risk Summary
   ```

**Success Criteria:** Can navigate Neo4j, execute Cypher queries, understand data structure

---

**Afternoon (1 PM - 5 PM): Data Pipeline**

Tasks:
1. Document ingestion pipeline walkthrough (2 hours)
   ```bash
   # Review pipeline code
   cat 5_NER11_Gold_Model/api/ingestion/document_processor.py

   # Understand stages:
   # 1. Document upload/retrieval
   # 2. Text extraction (PDF, HTML, etc.)
   # 3. NER entity extraction (NER11 model)
   # 4. Entity linking (map to existing entities)
   # 5. Graph storage (Neo4j)
   # 6. Vector embedding (Qdrant)
   ```

2. Test ingestion with sample document (2 hours)
   ```bash
   # Create test document
   cat > test_threat_report.txt << 'EOF'
   THREAT ALERT: APT-28 has been observed targeting government agencies
   in the United States. The group uses spear-phishing emails with
   malicious attachments. Affected software: Microsoft Office versions
   2016 and earlier. Vulnerability: CVE-2023-123456
   EOF

   # Call ingestion API
   curl -X POST http://localhost:8000/api/v1/ingest \
     -F "document=@test_threat_report.txt"

   # Verify entities created in Neo4j
   MATCH (n) WHERE n.source = "test_threat_report" RETURN n
   ```

3. Embedding verification (1 hour)
   ```bash
   # Check Qdrant vector embeddings
   curl -X GET http://localhost:6333/collections

   # Verify semantic search works
   curl -X POST http://localhost:8000/api/v1/semantic-search \
     -H "Content-Type: application/json" \
     -d '{"query": "attack techniques using email", "limit": 10}'
   ```

**Success Criteria:** Can understand pipeline, execute ingestion, verify entities in databases

---

### Day 5: Monitoring, Incident Response & Assessment (Full Day - 8 hours)

**Morning (9 AM - 12 PM): Monitoring Setup**

Tasks:
1. Monitoring infrastructure setup (1.5 hours)
   ```bash
   # Start monitoring stack
   docker-compose -f docker-compose.monitoring.yml up -d

   # Access Prometheus
   open http://localhost:9090  # Metrics

   # Access Grafana
   open http://localhost:3000  # Dashboards
   # Default: admin / admin

   # Access logs
   open http://localhost:3100/api/prom/label/__name__/values  # Loki
   ```

2. Key metrics overview (1 hour)
   ```bash
   # Dashboard tour in Grafana
   # Key dashboards to understand:
   # - System Overview (CPU, Memory, Disk)
   # - API Performance (Response times, error rates)
   # - Database Health (Neo4j, MySQL connection pools)
   # - Application Logs (Loki)
   ```

3. Alert configuration (1 hour)
   ```bash
   # Understand alert levels
   # - P0: Critical (system down, data loss risk)
   # - P1: High (degraded performance, features impaired)
   # - P2: Medium (non-critical issues, manual intervention)
   # - P3: Low (informational, trends to monitor)
   ```

**Success Criteria:** Can access monitoring, understand dashboards, identify alerts

---

**Afternoon (1 PM - 4:30 PM): Incident Response & Training**

Tasks:
1. Incident response procedures (1.5 hours)
   ```bash
   # Review key playbooks
   # - API Not Responding
   # - Database Connection Issues
   # - Disk Space Problems
   # - Model Loading Failures

   # Key escalation contacts
   # P0: Immediate (within 15 min) - DevOps Lead
   # P1: High priority (within 1 hour) - Tech Lead
   # P2: Normal priority (within 4 hours) - Component Owner
   # P3: Low priority (next business day) - Team
   ```

2. Practice incident response (1 hour)
   ```bash
   # Simulate failure scenarios
   # Scenario 1: Stop Neo4j and diagnose
   docker stop openspg-neo4j

   # Test API response
   curl http://localhost:8000/health
   # Should show degraded status

   # Follow troubleshooting guide to restart
   docker start openspg-neo4j

   # Scenario 2: Disk space issue (simulation only)
   # Understand cleanup procedures without executing
   ```

3. Knowledge sharing & documentation (30 min)
   ```bash
   # Review key documentation
   # - This onboarding guide
   # - Migration strategy documents
   # - API status and roadmap
   # - Troubleshooting guide

   # Understand documentation locations
   # - Project wiki: 1_AEON_DT_CyberSecurity_Wiki_Current/
   # - API docs: 04_APIs/
   # - Code comments and docstrings
   ```

---

**4 PM - 5:30 PM: Competency Assessment**

**Backend Developer Assessment** (if applicable):
- [ ] Implement new API endpoint (90 min)
  - Create endpoint in FastAPI
  - Add database query (Cypher or SQL)
  - Write tests with pytest
  - Document with docstrings

- [ ] Optimize slow query (45 min)
  - Profile existing Cypher query
  - Add indexes
  - Verify improvement

- [ ] Write integration test (30 min)
  - Test full API workflow
  - Verify database state
  - Check error handling

**Frontend Developer Assessment** (if applicable):
- [ ] Build React component (90 min)
  - Create component from design spec
  - Integrate with API
  - Add TypeScript types
  - Write unit tests

**DevOps Assessment** (if applicable):
- [ ] Deploy service update (120 min)
  - Build Docker image
  - Push to registry
  - Update docker-compose
  - Verify running and healthy
  - Check logs for errors

**Pass Criteria:** 3/3 tasks complete with acceptable quality

**Conditional:** 2/3 tasks complete → Requires mentoring continuation

**Fail:** <2 tasks complete → Extended training required before independent work

---

## Role-Specific Training Paths

### Backend Developer Path (3-4 weeks)

**Week 1: API Architecture & FastAPI**
- [ ] FastAPI fundamentals (decorators, path parameters, request bodies)
- [ ] Create 3 new endpoints with full CRUD operations
- [ ] Database integration (Cypher + SQL)
- [ ] Input validation with Pydantic v2
- [ ] Error handling and status codes
- [ ] Testing with pytest (unit tests)

**Week 2: Neo4j Database Optimization**
- [ ] Cypher query writing patterns
- [ ] Index creation and query optimization
- [ ] Relationship patterns and traversal
- [ ] Transaction handling
- [ ] Performance profiling
- [ ] Backup and restore procedures

**Week 3: NER11 Model Integration**
- [ ] Model architecture and training
- [ ] Inference pipeline
- [ ] Fine-tuning for custom entities
- [ ] Evaluation metrics (precision, recall, F1)
- [ ] Performance optimization
- [ ] Version management

**Week 4: Testing & Deployment**
- [ ] Integration testing (API + Database)
- [ ] End-to-end testing
- [ ] Performance testing (load, stress)
- [ ] Security testing (injection, auth)
- [ ] CI/CD pipeline
- [ ] Monitoring and alerting

**Validation:** Implement 2-3 new endpoints → Phase B6 features

---

### Frontend Developer Path (3-4 weeks)

**Week 1: Next.js & React Architecture**
- [ ] Next.js project structure
- [ ] React components and hooks
- [ ] TypeScript interfaces and types
- [ ] Styling (CSS Modules, Tailwind)
- [ ] State management (Context/Redux)
- [ ] Build and development tools

**Week 2: Component Development**
- [ ] Build 5+ reusable components
- [ ] Dashboard layout and data visualization
- [ ] Chart components (react-chart-js)
- [ ] Data tables with sorting/filtering
- [ ] Form components with validation
- [ ] Loading states and error boundaries

**Week 3: API Integration**
- [ ] Fetch vs axios patterns
- [ ] Error handling and retries
- [ ] Authentication/authorization UI
- [ ] Real-time updates (if applicable)
- [ ] Caching strategies
- [ ] Performance optimization

**Week 4: Testing & Deployment**
- [ ] Unit testing (Jest, React Testing Library)
- [ ] Integration testing
- [ ] Visual regression testing
- [ ] Accessibility testing (WCAG)
- [ ] Performance testing (Lighthouse)
- [ ] CI/CD for frontend

**Validation:** Build UI for Phase B6 features → Component library expansion

---

## Daily Startup Runbook

**Estimated Time: 3-5 minutes**

```bash
# 1. Docker services startup (2 min)
docker-compose -f docker-compose.databases.yml up -d
docker-compose -f docker-compose.monitoring.yml up -d

# 2. Verify services health (1 min)
echo "Checking service health..."
docker ps --format "table {{.Names}}\t{{.Status}}"

# Check critical endpoints
curl -s http://localhost:8000/health | jq '.status'
curl -s http://localhost:7474/ > /dev/null && echo "Neo4j: OK" || echo "Neo4j: DOWN"
curl -s http://localhost:6333/health | jq '.status'

# 3. Backend environment (1 min)
cd 5_NER11_Gold_Model
source venv/bin/activate  # or . venv/Scripts/activate on Windows

# 4. Frontend environment (30 sec)
cd 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1
npm run dev &

# 5. Verification (1 min)
echo "Services online:"
- API: http://localhost:8000/health
- Neo4j: http://localhost:7474/
- Frontend: http://localhost:3000
- Monitoring: http://localhost:3000 (Grafana)

echo "All systems ready for development!"
```

---

## Service Management Procedures

### Starting Services

```bash
# Start all databases
docker-compose -f docker-compose.databases.yml up -d

# Start backend API
cd 5_NER11_Gold_Model
source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend
cd 1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1
npm run dev

# Start monitoring (optional for development)
docker-compose -f docker-compose.monitoring.yml up -d
```

### Stopping Services Gracefully

```bash
# Graceful shutdown preserves data
docker-compose down  # Stops all containers, preserves volumes
# OR
docker-compose -f docker-compose.databases.yml stop  # Stops without removing

# Verify stopped
docker ps  # Should show no running containers
```

### Restarting Specific Service

```bash
# Example: Restart Neo4j
docker restart openspg-neo4j

# Wait for health check
sleep 10
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n)"
# Expected: 20739
```

---

## Backup and Recovery Procedures

### Daily Automated Backup

```bash
# Database backup script (run daily at 2 AM)
#!/bin/bash
BACKUP_DIR="/var/backups/aeon-dt"
DATE=$(date +%Y%m%d_%H%M%S)

# Neo4j backup
docker exec openspg-neo4j neo4j-admin dump \
  --to-path=/var/lib/neo4j/data/dumps/$DATE \
  --database=neo4j

# MySQL backup
docker exec openspg-mysql mysqldump \
  -u root -p"${MYSQL_PASSWORD}" \
  --all-databases \
  --single-transaction \
  --quick > $BACKUP_DIR/mysql_$DATE.sql

# Qdrant backup (if applicable)
# Verify backups
ls -lh $BACKUP_DIR/
```

### Weekly Offsite Backup

```bash
# Copy to external drive
cp -r /var/backups/aeon-dt /Volumes/ExternalDrive/aeon-dt-backup-$(date +%Y%m%d)

# Verify backup integrity
sha256sum /var/backups/aeon-dt/* > backup_checksums.txt
sha256sum -c backup_checksums.txt  # Should all pass
```

### Recovery from Backup

```bash
# Restore Neo4j
docker stop openspg-neo4j
docker volume rm openspg-neo4j
docker start openspg-neo4j
docker exec openspg-neo4j neo4j-admin load \
  --from-path=/var/lib/neo4j/data/dumps/latest \
  --database=neo4j \
  --force

# Restore MySQL
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" < mysql_backup.sql

# Verify restoration
# See Phase 6: Validation procedures
```

---

## Incident Response Playbooks

### Playbook 1: API Not Responding

**Response Time Target: 15 minutes**

```bash
# Step 1: Diagnosis (2 min)
curl -v http://localhost:8000/health
# Connection refused? Port issue?
# Timeout? Service might be stuck
# 500 error? Internal service error

# Step 2: Check service status (1 min)
docker logs openspg-server --tail=50 | grep -i "error\|exception"
docker ps | grep openspg-server

# Step 3: Attempt restart (3 min)
docker restart openspg-server
sleep 5
curl http://localhost:8000/health
# If responsive, continue monitoring
# If not, proceed to Step 4

# Step 4: Deep diagnosis (4 min)
docker logs openspg-server | head -100
# Look for: out of memory, database connection error, config error
# Check database connectivity
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "MATCH (n) RETURN COUNT(n)"
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" -e "SELECT 1"

# Step 5: Escalate if needed (5 min)
# P0 issue persists → Escalate to DevOps Lead
# Provide:
# - API error logs (last 50 lines)
# - Database status
# - System resources (docker stats)
# - Recent changes made
```

### Playbook 2: Database Connection Issues

**Response Time Target: 10 minutes**

```bash
# Step 1: Identify affected database (2 min)
# Neo4j test
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN COUNT(n)" 2>&1

# MySQL test
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" \
  -e "SELECT 1" 2>&1

# Step 2: Check container health (1 min)
docker ps | grep -E "openspg-(neo4j|mysql)"
# Status should be UP or HEALTHY

# Step 3: Restart database (3 min)
# Neo4j restart
docker restart openspg-neo4j
sleep 15  # Wait for Neo4j to initialize
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "MATCH (n) RETURN COUNT(n)"

# MySQL restart
docker restart openspg-mysql
sleep 5
docker exec openspg-mysql mysql -u root -p"${MYSQL_PASSWORD}" -e "SELECT 1"

# Step 4: Check application connections (2 min)
# Restart API service to reset connection pools
docker restart openspg-server
sleep 5
curl http://localhost:8000/health

# Step 5: Escalate if needed (2 min)
# Database still not responding → Escalate to Database Admin
# Provide:
# - Container logs
# - Error messages
# - Last working state
```

### Playbook 3: Disk Space Issues

**Response Time Target: 10 minutes**

```bash
# Step 1: Check disk usage (1 min)
df -h /
# Expected: <80% used
# Critical: >90% used → Immediate action needed

# Step 2: Identify large files (2 min)
du -sh /var/lib/docker/volumes/*
du -sh ~/.docker/

# Step 3: Clean unnecessary files (3 min)
# Clean Docker images
docker image prune -a -f  # Remove unused images
# Clean container logs
for log in /var/lib/docker/containers/*/*-json.log; do
  truncate -s 0 "$log"
done

# Clean old backups (>7 days)
find /var/backups/aeon-dt -mtime +7 -delete

# Step 4: Verify recovered space (1 min)
df -h /
# Should be significantly lower

# Step 5: Monitor going forward (3 min)
# Set up disk space alerts
# - Warning: 70% used
# - Critical: 85% used
# - Auto-cleanup: >90% used
```

### Playbook 4: Model Loading Failures

**Response Time Target: 15 minutes**

```bash
# Step 1: Test model load (2 min)
cd 5_NER11_Gold_Model
source venv/bin/activate
python -c "
import spacy
try:
    nlp = spacy.load('ner11')
    print('Model loaded successfully')
except Exception as e:
    print(f'Error: {e}')
"

# Step 2: Check model files (2 min)
ls -lh models/ner11/
# Should contain: model-best, meta.json, tokenizer, vocab, config.cfg

# Step 3: Verify model integrity (3 min)
tar -tzf backups/ner11_model_backup.tar.gz > /dev/null
# If archive corrupted, restore from backup

# Step 4: Reinstall dependencies (3 min)
pip install spacy torch
python -m spacy download en_core_web_sm  # Test installation

# Step 5: Restore from backup (3 min)
rm -rf models/ner11
tar -xzf backups/ner11_model_backup.tar.gz -C models/
python -c "import spacy; nlp = spacy.load('ner11'); print('Restored successfully')"

# Step 6: Escalate if needed (2 min)
# If model still won't load:
# - Check Python version (should be 3.10+)
# - Check dependencies (torch, spacy versions)
# - Escalate to ML Engineer
```

---

## Knowledge Base Location Guide

### Primary Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Architecture Overview | `ARCHITECTURE_OVERVIEW.md` | System design and components |
| API Status & Roadmap | `04_APIs/00_API_STATUS_AND_ROADMAP.md` | API endpoints and status |
| Migration Guides | `10_MacOS_Migration_Strategy/` | Complete migration documentation |
| Operations Manual | `13_Procedures/01_NER11_OPERATIONS_PROCEDURES_v1.0_2025-12-03.md` | Detailed operational procedures |
| This Onboarding | `10_MacOS_Migration_Strategy/07_TEAM_HANDOFF_RUNBOOKS.md` | New member onboarding |

### Quick Reference Commands

```bash
# Service startup
docker-compose -f docker-compose.databases.yml up -d

# Health check
curl http://localhost:8000/health | jq '.status'

# Database query
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "MATCH (n) RETURN COUNT(n)"

# Model test
python -c "import spacy; nlm = spacy.load('ner11'); print('OK')"

# Logs inspection
docker logs openspg-server --tail=50

# Container status
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Common Queries & Procedures

**Neo4j:**
- Entity search by type
- Relationship traversal
- Impact analysis queries

**MySQL:**
- Schema inspection
- Data integrity checks
- Backup/restore

**Frontend:**
- Component navigation
- State management patterns
- API integration examples

---

## Handoff Procedures (When Team Changes)

### Knowledge Transfer Checklist (2 Weeks Before Transition)

**Week 1: Documentation Sprint**
- [ ] Document all current work in progress
- [ ] Create "tribal knowledge" document (quirks, gotchas, workarounds)
- [ ] Update runbooks with recent changes
- [ ] Create handoff documentation for successor
- [ ] Code review and approval of documentation

**Week 2: Knowledge Transfer Sessions**
- [ ] Day 1: Architecture walkthrough and design decisions
- [ ] Day 2-3: Code walkthrough with pair programming
- [ ] Day 4: Operations and troubleshooting procedures
- [ ] Day 5: Q&A and transition wrap-up

### Documentation Completion Requirements

Before departure, provide:
1. **Code Ownership Matrix** - What you owned and who to ask
2. **Known Issues Document** - Current problems and workarounds
3. **Future Work Roadmap** - Planned improvements and blockers
4. **External Dependencies** - Services, keys, contacts
5. **Incident History** - What broke before and how it was fixed

### Access Revocation

- [ ] GitHub team membership transfer
- [ ] Docker registry credentials revoked
- [ ] Database credentials changed (if applicable)
- [ ] Email forwarding set up (30 days)
- [ ] Calendar access removed
- [ ] On-call pager updated

---

## Key Principles

✅ **Documentation is sacred** - Update guides as systems change
✅ **Share knowledge freely** - Help new team members succeed
✅ **Automate everything** - Reduce manual procedures
✅ **Monitor continuously** - Catch problems early
✅ **Practice incident response** - Be ready when issues occur

---

**Status:** COMPLETE - Ready for team implementation
**Last Updated:** 2025-12-04 15:45:00 UTC
**Version:** 1.0.0

🚀 Begin with 5-Day Onboarding Plan for all new team members
