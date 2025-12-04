# AEON Digital Twin - Team Onboarding & Knowledge Transfer Procedures

**File**: 02_TEAM_ONBOARDING_KNOWLEDGE_TRANSFER_v1.0_2025-12-04.md
**Created**: 2025-12-04 11:45:00 UTC
**Modified**: 2025-12-04 11:45:00 UTC
**Version**: v1.0.0
**Author**: AEON Architecture Team
**Purpose**: Comprehensive onboarding and knowledge transfer for new team members
**Status**: ACTIVE

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              AEON DIGITAL TWIN - TEAM ONBOARDING PROCEDURES                  ║
║                                                                              ║
║   ┌────────────────────────────────────────────────────────────────────┐    ║
║   │  COMPREHENSIVE TRAINING: 5-Day Onboarding + Role-Specific Paths    │    ║
║   │  KNOWLEDGE BASE: Migration guides, APIs, operations procedures      │    ║
║   │  VALIDATION: Hands-on exercises, competency assessments             │    ║
║   └────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Table of Contents

1. [New Team Member Onboarding (5-Day Plan)](#1-new-team-member-onboarding-5-day-plan)
2. [Role-Specific Training Paths](#2-role-specific-training-paths)
3. [Knowledge Base Access](#3-knowledge-base-access)
4. [Hands-On Training Exercises](#4-hands-on-training-exercises)
5. [Competency Validation](#5-competency-validation)
6. [Ongoing Learning Program](#6-ongoing-learning-program)
7. [Handoff Procedures](#7-handoff-procedures)

---

## 1. New Team Member Onboarding (5-Day Plan)

### Overview

**Duration**: 5 working days (40 hours)
**Format**: Combination of self-paced reading, hands-on exercises, and mentored sessions
**Success Criteria**: Team member can independently execute common development tasks by end of Day 5

---

### Day 1: Environment Setup & Architecture Overview

**Objective**: Complete development environment setup and understand system architecture

#### Morning (9:00 AM - 12:00 PM): Environment Setup

**Location**: Follow migration guides in `10_MacOS_Migration_Strategy/`

**Tasks**:
1. **macOS Environment Setup** (2 hours)
   ```bash
   # Follow migration documentation
   cat 10_MacOS_Migration_Strategy/00_MIGRATION_MASTER_PLAN_2025-12-04.md

   # Install required software
   - Docker Desktop (or OrbStack for M1/M2/M3 Macs)
   - Homebrew
   - Python 3.11
   - Node.js 18+
   - Git
   - Visual Studio Code
   ```

2. **Access Provisioning** (30 minutes)
   - GitHub repository access
   - Neo4j database credentials
   - Docker Hub credentials (if private images)
   - Internal documentation access
   - Team communication channels (Slack/Teams)

3. **Tool Installation Verification** (30 minutes)
   ```bash
   # Verify installations
   docker --version          # Docker 24.x.x
   python3 --version         # Python 3.11.x
   node --version            # v18.x.x
   npm --version             # 9.x.x
   git --version             # 2.x.x

   # Clone repository
   git clone https://github.com/Planet9V/agent-optimization-deployment.git
   cd agent-optimization-deployment
   git checkout gap-002-clean-VERIFIED
   ```

#### Afternoon (1:00 PM - 5:00 PM): Architecture Overview

**Location**: Read `ARCHITECTURE_OVERVIEW.md` and API documentation

**Tasks**:
1. **System Architecture Study** (2 hours)
   ```bash
   # Read architecture documentation
   cat ARCHITECTURE_OVERVIEW.md
   cat 00_MAIN_INDEX.md
   cat 00_STATUS_DASHBOARD.md

   # Key concepts to understand:
   - Graph-based digital twin architecture
   - 16 CISA critical infrastructure sectors
   - Neo4j database with 1.1M+ nodes
   - NER11 Gold Standard entity recognition model
   - API architecture (251+ endpoints planned, 79 implemented)
   ```

2. **Database Schema Exploration** (1 hour)
   ```bash
   # Start Neo4j (if not running)
   docker start openspg-neo4j

   # Connect to Neo4j Browser
   open http://localhost:7474
   # Credentials: neo4j / neo4j@openspg

   # Execute exploration queries
   # See: 02_Databases/QUERIES_LIBRARY.md
   MATCH (n) RETURN labels(n), count(n) LIMIT 20
   ```

3. **API Documentation Review** (1 hour)
   ```bash
   # Review API capabilities
   cat 04_APIs/00_API_STATUS_AND_ROADMAP.md
   cat 04_APIs/00_FRONTEND_QUICK_START.md

   # Current status:
   - 79 REST endpoints IMPLEMENTED (Phase B2-B5)
   - NER11 semantic/hybrid search OPERATIONAL
   - 172+ endpoints PLANNED (specifications complete)
   ```

**Success Criteria**:
- ✅ Development environment fully configured
- ✅ Can access all critical systems (Neo4j, GitHub, Docker)
- ✅ Understands high-level system architecture
- ✅ Can navigate documentation structure

---

### Day 2: Service Startup & API Testing

**Objective**: Start all services and successfully test API endpoints

#### Morning (9:00 AM - 12:00 PM): Service Startup

**Location**: Follow `13_Procedures/01_NER11_OPERATIONS_PROCEDURES_v1.0_2025-12-03.md`

**Tasks**:
1. **Infrastructure Services** (1 hour)
   ```bash
   # Start Neo4j
   docker start openspg-neo4j
   docker logs -f openspg-neo4j | grep -m1 "Started"

   # Start Qdrant vector database
   docker start qdrant
   curl http://localhost:6333/health

   # Start MySQL (OpenSPG metadata)
   docker start openspg-mysql

   # Start MinIO (object storage)
   docker start openspg-minio

   # Verify all containers
   docker ps --format "table {{.Names}}\t{{.Status}}"
   ```

2. **NER11 API Service** (1 hour)
   ```bash
   cd 5_NER11_Gold_Model
   source venv/bin/activate

   # Set environment variables
   export MODEL_PATH="models/ner11_v3/model-best"
   export NEO4J_URI="bolt://localhost:7687"
   export NEO4J_USER="neo4j"
   export NEO4J_PASSWORD="neo4j@openspg"
   export QDRANT_HOST="localhost"
   export QDRANT_PORT="6333"

   # Start API server
   uvicorn serve_model:app --host 0.0.0.0 --port 8000
   ```

3. **Health Verification** (30 minutes)
   ```bash
   # NER11 API health check
   curl http://localhost:8000/health | python3 -m json.tool

   # Expected response:
   # {
   #   "status": "healthy",
   #   "ner_model_custom": "loaded",
   #   "model_checksum": "verified",
   #   "semantic_search": "available",
   #   "neo4j_graph": "connected"
   # }

   # Neo4j health check
   docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' \
     "MATCH (n) RETURN count(n) as total_nodes"

   # Expected: 1,100,000+ nodes
   ```

#### Afternoon (1:00 PM - 5:00 PM): API Testing Walkthrough

**Location**: Use `04_APIs/` documentation and test tools

**Tasks**:
1. **NER11 Entity Extraction Testing** (1 hour)
   ```bash
   # Test entity recognition
   curl -X POST http://localhost:8000/ner \
     -H "Content-Type: application/json" \
     -d '{"text": "APT29 exploited CVE-2024-12345 using T1566.001 phishing technique"}'

   # Expected entities: APT29 (APT_GROUP), CVE-2024-12345 (CVE), T1566.001 (TECHNIQUE)
   ```

2. **Semantic Search Testing** (1 hour)
   ```bash
   # Test semantic search
   curl -X POST http://localhost:8000/search/semantic \
     -H "Content-Type: application/json" \
     -d '{"query": "ransomware attacks on critical infrastructure", "fine_grained_filter": "RANSOMWARE"}'

   # Test hybrid search (semantic + graph expansion)
   curl -X POST http://localhost:8000/search/hybrid \
     -H "Content-Type: application/json" \
     -d '{"query": "APT29 malware", "expand_graph": true, "hop_depth": 2}'
   ```

3. **Phase B2-B5 API Testing** (2 hours)
   ```bash
   # Test SBOM API (Phase B2)
   curl http://localhost:8000/api/v2/sbom/components

   # Test Threat Intelligence API (Phase B3)
   curl http://localhost:8000/api/v2/threat-intel/actors

   # Test Compliance API (Phase B4)
   curl http://localhost:8000/api/v2/compliance/frameworks

   # Test Economic Impact API (Phase B5)
   curl http://localhost:8000/api/v2/economic-impact/assessments
   ```

**Success Criteria**:
- ✅ All Docker containers running and healthy
- ✅ NER11 API operational and returning entities
- ✅ Semantic and hybrid search working
- ✅ Phase B2-B5 APIs responding correctly
- ✅ Can troubleshoot basic service issues

---

### Day 3: Code Repository & Development Workflow

**Objective**: Understand code organization and Git procedures

#### Morning (9:00 AM - 12:00 PM): Repository Structure

**Location**: Explore repository structure and documentation

**Tasks**:
1. **Repository Navigation** (2 hours)
   ```bash
   # Main project directories
   ls -la 1_AEON_DT_CyberSecurity_Wiki_Current/

   # Key directories:
   - 00_Index/                    # Documentation index
   - 01_ARCHITECTURE/             # System architecture
   - 02_Databases/                # Neo4j schemas and queries
   - 04_APIs/                     # API specifications (17 files)
   - 05_NER11_Gold_Model/         # ML model and API implementation
   - 10_MacOS_Migration_Strategy/ # Environment setup guides
   - 13_Procedures/               # Operations procedures (THIS FILE)

   # Code structure
   - 5_NER11_Gold_Model/
     - api/                       # FastAPI implementation (79 endpoints)
     - models/ner11_v3/           # Trained NER11 model
     - training_data/             # Training datasets
     - utils/                     # Helper functions
     - tests/                     # Test suites
   ```

2. **API Code Walkthrough** (1 hour)
   ```bash
   # Review Phase B5 implementation (most recent)
   cat 5_NER11_Gold_Model/api/economic_impact/__init__.py
   cat 5_NER11_Gold_Model/api/demographics/__init__.py
   cat 5_NER11_Gold_Model/api/prioritization/__init__.py

   # Review main API server
   cat 5_NER11_Gold_Model/serve_model.py

   # Review NER model implementation
   cat 5_NER11_Gold_Model/utils/context_augmentation.py
   ```

#### Afternoon (1:00 PM - 5:00 PM): Git Workflow

**Location**: Practice Git procedures

**Tasks**:
1. **Git Branch Strategy** (1 hour)
   ```bash
   # View current branch
   git branch -a

   # Current working branch: gap-002-clean-VERIFIED
   # Main branches:
   - main (production)
   - gap-002-clean-VERIFIED (current development)
   - Feature branches: feature/[name]
   - Bug fix branches: fix/[issue]

   # Create feature branch
   git checkout -b feature/my-first-task
   ```

2. **Commit Conventions** (1 hour)
   ```bash
   # Review recent commits for style
   git log --oneline -10

   # Commit message format:
   # <type>(<scope>): <subject>
   #
   # <body>
   # <footer>

   # Examples:
   feat(phase-b5): Add E10 Economic Impact API
   fix(hybrid-search): Fix graph expansion bug in Cypher query
   docs(api): Update API_STATUS_AND_ROADMAP.md with Phase B5
   test(ner11): Add integration tests for entity extraction
   ```

3. **Pull Request Process** (1 hour)
   ```bash
   # Make a small change
   echo "# New documentation section" >> docs/test.md
   git add docs/test.md
   git commit -m "docs(test): Add test documentation section"

   # Push to remote
   git push origin feature/my-first-task

   # Create PR via GitHub UI
   # - Title: Clear description of changes
   # - Description: What changed, why, how to test
   # - Reviewers: Request code review
   # - Link to related issues
   ```

**Success Criteria**:
- ✅ Understands repository structure
- ✅ Can navigate code and documentation
- ✅ Knows Git branch strategy
- ✅ Can create feature branch, commit, push, create PR
- ✅ Understands commit message conventions

---

### Day 4: Database Schema & Data Pipeline

**Objective**: Understand Neo4j data model and ingestion workflows

#### Morning (9:00 AM - 12:00 PM): Database Schema Deep Dive

**Location**: Use Neo4j Browser and query library

**Tasks**:
1. **Schema Exploration** (2 hours)
   ```cypher
   # Connect to Neo4j Browser: http://localhost:7474

   # View node labels
   CALL db.labels() YIELD label
   RETURN label ORDER BY label

   # View relationship types
   CALL db.relationshipTypes() YIELD relationshipType
   RETURN relationshipType ORDER BY relationshipType

   # Sample queries from QUERIES_LIBRARY.md
   # 1. Sector overview
   MATCH (s:Sector)
   RETURN s.name, s.description, s.node_count
   ORDER BY s.node_count DESC

   # 2. Equipment vulnerabilities
   MATCH (e:Equipment)-[:HAS_VULNERABILITY]->(v:CVE)
   WHERE v.baseScore > 7.0
   RETURN e.name, v.cveId, v.baseScore
   LIMIT 20

   # 3. MITRE ATT&CK techniques
   MATCH (t:Technique)-[:PART_OF]->(tactic:Tactic)
   RETURN tactic.name, count(t) as technique_count
   ORDER BY technique_count DESC
   ```

2. **NER11 Hierarchical Labels** (1 hour)
   ```cypher
   # Explore hierarchical NER11 labels
   MATCH (n)
   WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_')
   RETURN DISTINCT labels(n) AS hierarchical_labels, count(n) AS count
   ORDER BY count DESC
   LIMIT 20

   # Three-tier hierarchy:
   # - Broad: 60 labels (e.g., THREAT_ACTOR, MALWARE, VULNERABILITY)
   # - Fine-grained: 566 types (e.g., APT_GROUP, RANSOMWARE, CVE)
   # - Instance: Individual entities (e.g., APT29, WannaCry, CVE-2024-1234)
   ```

#### Afternoon (1:00 PM - 5:00 PM): Data Ingestion Pipeline

**Location**: Review ingestion scripts and run examples

**Tasks**:
1. **Document Ingestion Process** (2 hours)
   ```bash
   cd 5_NER11_Gold_Model

   # Review ingestion scripts
   ls -la scripts/
   # - ingest_wiki_documents.py        # Single/batch document ingestion
   # - rate_limited_ingest.py           # Rate-limited batch ingestion
   # - chunked_ingest.py                # Large document chunking

   # Test single document ingestion
   python scripts/ingest_wiki_documents.py \
     --wiki-root "../1_AEON_DT_CyberSecurity_Wiki_Current" \
     --file "04_APIs/00_API_STATUS_AND_ROADMAP.md"

   # Monitor Qdrant entity count
   curl -s http://localhost:6333/collections/ner11_entities_hierarchical | \
     python3 -c "import sys,json; print(json.load(sys.stdin)['result']['points_count'])"
   ```

2. **Embedding Service** (1 hour)
   ```bash
   # Review embedding pipeline
   cat pipelines/entity_embedding_service_hierarchical.py

   # Key concepts:
   # - Sentence transformers for semantic embeddings
   # - Qdrant vector storage (384-dimensional vectors)
   # - Hierarchical label filtering
   # - Graph-based re-ranking
   ```

**Success Criteria**:
- ✅ Can execute Cypher queries independently
- ✅ Understands Neo4j schema structure
- ✅ Knows NER11 hierarchical labeling system
- ✅ Can run document ingestion scripts
- ✅ Understands embedding and vector search pipeline

---

### Day 5: Monitoring, Incident Response & Team Communication

**Objective**: Learn monitoring tools and incident response procedures

#### Morning (9:00 AM - 12:00 PM): Monitoring & Alerting Setup

**Location**: Configure monitoring and review operational procedures

**Tasks**:
1. **Health Monitoring Setup** (1 hour)
   ```bash
   # Create health monitoring script
   cat > ~/health_monitor.sh << 'EOF'
   #!/bin/bash
   LOG_FILE="$HOME/aeon_health_$(date +%Y%m%d).log"

   # NER11 API health
   HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
   STATUS=$(echo $HEALTH | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null)

   TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

   if [ "$STATUS" = "healthy" ]; then
     echo "$TIMESTAMP - OK - API healthy" >> $LOG_FILE
   else
     echo "$TIMESTAMP - ALERT - API status: $STATUS" >> $LOG_FILE
   fi

   # Neo4j health
   NEO4J=$(docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1" 2>/dev/null)
   if [ -z "$NEO4J" ]; then
     echo "$TIMESTAMP - ALERT - Neo4j not responding" >> $LOG_FILE
   fi
   EOF

   chmod +x ~/health_monitor.sh

   # Test monitoring
   ~/health_monitor.sh
   cat ~/aeon_health_$(date +%Y%m%d).log
   ```

2. **Performance Metrics** (1 hour)
   ```bash
   # Qdrant collection stats
   curl -s http://localhost:6333/collections/ner11_entities_hierarchical | python3 -c "
   import sys, json
   d = json.load(sys.stdin)
   r = d.get('result', {})
   print(f\"Qdrant Entities: {r.get('points_count', 0):,}\")
   print(f\"Indexed Vectors: {r.get('indexed_vectors_count', 0):,}\")
   "

   # Neo4j statistics
   docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "
   MATCH (n) RETURN labels(n)[0] as label, count(n) as count
   ORDER BY count DESC LIMIT 10
   "
   ```

3. **Incident Response Training** (1 hour)
   ```bash
   # Review incident procedures
   cat 13_Procedures/01_NER11_OPERATIONS_PROCEDURES_v1.0_2025-12-03.md

   # Section 7: Troubleshooting Procedures
   # Section 10: Emergency Procedures

   # Practice common scenarios:
   # 1. API not responding → Check logs, restart service
   # 2. Model not loading → Verify checksums, restore from backup
   # 3. Neo4j connection failed → Check container, restart
   # 4. Qdrant collection corrupted → Restore from snapshot
   ```

#### Afternoon (1:00 PM - 5:00 PM): Team Communication & Final Assessment

**Location**: Team meeting room / video call

**Tasks**:
1. **Team Communication Protocols** (1 hour)
   - Daily standup format
   - Slack/Teams channels organization
   - Code review expectations
   - Documentation standards
   - Escalation procedures

2. **Knowledge Sharing Sessions** (1 hour)
   - Weekly architecture discussions
   - Lessons learned from incidents
   - New feature demonstrations
   - Security vulnerability awareness

3. **Final Competency Assessment** (2 hours)
   - Deploy a test API endpoint end-to-end
   - Query Neo4j database and interpret results
   - Train NER11 model on sample text
   - Create simple API integration test
   - Diagnose and resolve simulated service failure

   (See Section 5: Competency Validation for detailed assessment)

**Success Criteria**:
- ✅ Monitoring configured and operational
- ✅ Understands incident response procedures
- ✅ Knows team communication channels
- ✅ Passes final competency assessment
- ✅ Ready for independent development work

---

## 2. Role-Specific Training Paths

### Backend Developer Path (3-4 weeks)

**Prerequisites**: Completed 5-day general onboarding

**Week 1: API Architecture & Implementation**
- Deep dive into FastAPI framework
- RESTful API design patterns
- OpenAPI/Swagger documentation
- Authentication and authorization (JWT, OAuth)
- Rate limiting and caching strategies

**Hands-On Tasks**:
```bash
# Implement new API endpoint
1. Review specification in 04_APIs/
2. Create FastAPI route in 5_NER11_Gold_Model/api/
3. Implement request/response models (Pydantic)
4. Add validation and error handling
5. Write unit tests
6. Update OpenAPI documentation
7. Deploy and test
```

**Week 2: Database Optimization**
- Neo4j Cypher query optimization
- Index strategy and creation
- Query profiling and analysis
- Transaction management
- Backup and recovery procedures

**Hands-On Tasks**:
```cypher
-- Optimize slow query
1. PROFILE slow query to identify bottlenecks
2. Create appropriate indexes
3. Refactor query for better performance
4. Benchmark improvements
5. Document optimization in code comments
```

**Week 3: Model Integration**
- NER11 Gold Standard model architecture
- Training pipeline and data preparation
- Model inference and optimization
- Embedding generation and vector search
- Model validation and testing

**Hands-On Tasks**:
```bash
# Fine-tune NER11 model
1. Prepare custom training data
2. Run training script with validation
3. Evaluate model performance
4. Deploy updated model
5. Test entity extraction accuracy
```

**Week 4: Testing & Deployment**
- Unit testing with pytest
- Integration testing strategies
- API testing with curl/Postman
- Docker containerization
- CI/CD pipeline setup

**Validation**:
- ✅ Implement 2-3 new API endpoints
- ✅ Optimize at least 1 slow database query
- ✅ Fine-tune NER11 model on custom data
- ✅ Write comprehensive test suite (>80% coverage)
- ✅ Successfully deploy feature to staging

---

### Frontend Developer Path (3-4 weeks)

**Prerequisites**: Completed 5-day general onboarding

**Week 1: Frontend Architecture**
- Next.js application structure
- React component design patterns
- State management (React Context, Zustand)
- TypeScript type definitions
- API client implementation

**Hands-On Tasks**:
```typescript
// Create dashboard component
1. Review API specification
2. Define TypeScript interfaces from API schemas
3. Create React component with mock data
4. Implement API client
5. Add loading and error states
6. Write component tests
```

**Week 2: Build Process & Tooling**
- Vite/Next.js build configuration
- Hot module replacement (HMR)
- Code splitting and lazy loading
- Environment variable management
- Development vs production builds

**Hands-On Tasks**:
```bash
# Optimize build performance
1. Analyze bundle size
2. Implement code splitting
3. Configure lazy loading for routes
4. Optimize images and assets
5. Benchmark build time improvements
```

**Week 3: API Integration**
- RESTful API consumption patterns
- Error handling and retry logic
- Request caching strategies
- Real-time updates (WebSockets/SSE)
- Authentication flow implementation

**Hands-On Tasks**:
```typescript
// Implement API integration
1. Create API client with fetch/axios
2. Add error handling and retry logic
3. Implement request caching
4. Handle authentication tokens
5. Add loading indicators
6. Test error scenarios
```

**Week 4: Testing & Deployment**
- Jest unit testing
- React Testing Library
- E2E testing with Playwright
- Component documentation (Storybook)
- Frontend deployment pipeline

**Validation**:
- ✅ Build 2-3 complete UI components
- ✅ Integrate with backend APIs successfully
- ✅ Implement authentication flow
- ✅ Write component tests (>70% coverage)
- ✅ Deploy feature to staging environment

---

### DevOps Path (2-3 weeks)

**Prerequisites**: Completed 5-day general onboarding

**Week 1: Container Orchestration**
- Docker container lifecycle
- Docker Compose multi-service setup
- Volume management and persistence
- Network configuration
- Container health checks

**Hands-On Tasks**:
```bash
# Create production-ready docker-compose
1. Review existing docker-compose.yml
2. Add health checks for all services
3. Configure volume persistence
4. Set up network isolation
5. Implement restart policies
6. Document configuration
```

**Week 2: Monitoring & Logging**
- Log aggregation (ELK stack or alternatives)
- Metrics collection (Prometheus/Grafana)
- Alert configuration
- Performance monitoring
- Incident response automation

**Hands-On Tasks**:
```bash
# Set up monitoring stack
1. Deploy Prometheus and Grafana
2. Configure metrics exporters
3. Create dashboards for key metrics
4. Set up alerting rules
5. Test alert notifications
```

**Week 3: Deployment & Scaling**
- CI/CD pipeline configuration
- Blue-green deployment strategy
- Horizontal scaling techniques
- Load balancing configuration
- Disaster recovery planning

**Hands-On Tasks**:
```bash
# Implement CI/CD pipeline
1. Create GitHub Actions workflow
2. Add automated testing
3. Configure staging deployment
4. Implement production deployment
5. Add rollback mechanism
```

**Validation**:
- ✅ Deploy full stack using Docker Compose
- ✅ Configure monitoring and alerting
- ✅ Set up CI/CD pipeline
- ✅ Successfully execute disaster recovery drill
- ✅ Document deployment procedures

---

### Data Scientist Path (3-4 weeks)

**Prerequisites**: Completed 5-day general onboarding

**Week 1: NER11 Model Architecture**
- Transformer-based NER models
- spaCy framework and custom training
- Entity recognition labels and hierarchy
- Training data preparation
- Model evaluation metrics

**Hands-On Tasks**:
```python
# Prepare custom training data
1. Collect domain-specific text samples
2. Annotate entities using spaCy format
3. Split data into train/dev/test sets
4. Validate annotation consistency
5. Document labeling guidelines
```

**Week 2: Training Pipeline**
- Model training configuration
- Hyperparameter tuning
- Learning rate scheduling
- Early stopping and checkpointing
- Model versioning and registry

**Hands-On Tasks**:
```bash
# Train custom NER model
cd 5_NER11_Gold_Model

# Configure training
python -m spacy init config config.cfg --lang en --pipeline ner

# Train model
python -m spacy train config.cfg \
  --output models/custom_v1 \
  --paths.train training_data/train.spacy \
  --paths.dev training_data/dev.spacy

# Evaluate model
python -m spacy evaluate models/custom_v1/model-best \
  training_data/test.spacy
```

**Week 3: Evaluation & Optimization**
- Precision, recall, F1-score analysis
- Confusion matrix interpretation
- Error analysis and iteration
- Model compression techniques
- Inference optimization

**Hands-On Tasks**:
```python
# Evaluate and optimize model
1. Generate evaluation report
2. Analyze false positives/negatives
3. Identify labeling inconsistencies
4. Retrain with improved data
5. Compare model versions
6. Select best performing model
```

**Week 4: Dataset Management**
- Data versioning (DVC)
- Annotation quality control
- Active learning strategies
- Synthetic data generation
- Data augmentation techniques

**Validation**:
- ✅ Train custom NER model on domain data
- ✅ Achieve >85% F1-score on test set
- ✅ Optimize model inference speed
- ✅ Document training pipeline
- ✅ Create reproducible training script

---

### QA/Testing Path (2-3 weeks)

**Prerequisites**: Completed 5-day general onboarding

**Week 1: Test Automation**
- pytest framework and fixtures
- Test data management
- Mocking and stubbing
- Test coverage measurement
- Regression test suites

**Hands-On Tasks**:
```python
# Create comprehensive test suite
1. Review API specification
2. Write unit tests for core functions
3. Create integration tests for API endpoints
4. Add edge case tests
5. Measure test coverage
6. Document test scenarios
```

**Week 2: Performance Testing**
- Load testing tools (Locust, JMeter)
- Performance benchmarking
- Stress testing strategies
- Database query profiling
- API response time analysis

**Hands-On Tasks**:
```python
# Performance test suite
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_semantic_search(self):
        self.client.post("/search/semantic", json={
            "query": "ransomware attacks",
            "fine_grained_filter": "RANSOMWARE"
        })

    @task
    def test_entity_extraction(self):
        self.client.post("/ner", json={
            "text": "APT29 exploited CVE-2024-1234"
        })

# Run: locust -f performance_test.py --host http://localhost:8000
```

**Week 3: Security Testing**
- OWASP Top 10 vulnerability testing
- SQL injection testing
- XSS (Cross-Site Scripting) testing
- Authentication bypass testing
- API security best practices

**Hands-On Tasks**:
```bash
# Security testing checklist
1. Test authentication endpoints for bypass
2. Validate input sanitization
3. Check for SQL injection vulnerabilities
4. Test rate limiting effectiveness
5. Verify CORS configuration
6. Document security findings
```

**Validation**:
- ✅ Create comprehensive test suite (>90% coverage)
- ✅ Set up automated regression tests
- ✅ Perform load testing and document results
- ✅ Conduct security audit and report findings
- ✅ Integrate tests into CI/CD pipeline

---

## 3. Knowledge Base Access

### Documentation Locations

**Critical Documentation**:
```
📁 Project Root
├── 📄 ARCHITECTURE_OVERVIEW.md         # System architecture
├── 📄 00_MAIN_INDEX.md                 # Master documentation index
├── 📄 00_STATUS_DASHBOARD.md           # Current project status
├── 📁 00_Index/                        # Quick reference guides
├── 📁 01_ARCHITECTURE/                 # Architecture diagrams
├── 📁 02_Databases/
│   ├── 📄 QUERIES_LIBRARY.md           # Neo4j query examples
│   └── 📄 SCHEMA_DOCUMENTATION.md      # Database schema
├── 📁 04_APIs/
│   ├── 📄 00_API_STATUS_AND_ROADMAP.md # API implementation status
│   ├── 📄 00_FRONTEND_QUICK_START.md   # Frontend integration guide
│   ├── 📄 API_PHASE_B2_CAPABILITIES_2025-12-04.md  # E15, E03 APIs
│   ├── 📄 API_PHASE_B3_CAPABILITIES_2025-12-04.md  # E04, E05, E06 APIs
│   ├── 📄 API_PHASE_B4_CAPABILITIES_2025-12-04.md  # E07, E08, E09 APIs
│   └── 📄 API_PHASE_B5_CAPABILITIES_2025-12-04.md  # E10, E11, E12 APIs
├── 📁 10_MacOS_Migration_Strategy/
│   ├── 📄 00_MIGRATION_MASTER_PLAN_2025-12-04.md   # Environment setup
│   ├── 📄 01_PRE_MIGRATION_CHECKLIST.md            # Setup checklist
│   └── 📄 05_VALIDATION_PROCEDURES.md              # Validation steps
└── 📁 13_Procedures/
    ├── 📄 01_NER11_OPERATIONS_PROCEDURES_v1.0_2025-12-03.md  # Operations manual
    └── 📄 02_TEAM_ONBOARDING_KNOWLEDGE_TRANSFER_v1.0_2025-12-04.md  # THIS FILE
```

**NER11 Model Documentation**:
```
📁 5_NER11_Gold_Model/
├── 📄 README.md                        # Model overview
├── 📁 docs/
│   ├── 📄 QUICK_REFERENCE.txt          # Quick commands
│   ├── 📄 E10_DELIVERABLES.md          # Economic Impact API
│   ├── 📄 E11_DEMOGRAPHICS_IMPLEMENTATION.md  # Demographics API
│   └── 📄 E12_PRIORITIZATION_IMPLEMENTATION.md  # Prioritization API
└── 📁 api/                             # API implementation
    ├── 📁 sbom/                        # E15 SBOM APIs
    ├── 📁 vendor_equipment/            # E03 Vendor APIs
    ├── 📁 threat_intelligence/         # E04 Threat Intel APIs
    ├── 📁 risk_scoring/                # E05 Risk APIs
    ├── 📁 remediation/                 # E06 Remediation APIs
    ├── 📁 compliance/                  # E07 Compliance APIs
    ├── 📁 scanning/                    # E08 Scanning APIs
    ├── 📁 alerts/                      # E09 Alerts APIs
    ├── 📁 economic_impact/             # E10 Economic APIs
    ├── 📁 demographics/                # E11 Demographics APIs
    └── 📁 prioritization/              # E12 Prioritization APIs
```

### Quick Reference Cards

**API Quick Reference** (see `04_APIs/00_FRONTEND_QUICK_START.md`):
- 79 IMPLEMENTED endpoints (Phase B2-B5)
- 172 PLANNED endpoints (specifications ready)
- Request/response examples for all endpoints
- Authentication and error handling

**Database Quick Reference** (see `02_Databases/QUERIES_LIBRARY.md`):
- Common Cypher query patterns
- Schema exploration queries
- Performance optimization tips
- Index creation guidelines

**Operations Runbook** (see `13_Procedures/01_NER11_OPERATIONS_PROCEDURES_v1.0_2025-12-03.md`):
- Service startup procedures
- Health monitoring commands
- Troubleshooting procedures
- Emergency recovery steps

---

## 4. Hands-On Training Exercises

### Exercise 1: Deploy and Run a Single API Endpoint End-to-End

**Objective**: Demonstrate ability to deploy a complete API feature

**Duration**: 2-3 hours

**Steps**:
1. **Specification Review**
   ```bash
   # Read API specification
   cat 04_APIs/API_PHASE_B5_CAPABILITIES_2025-12-04.md
   # Focus on Economic Impact API (E10)
   ```

2. **Implement Test Endpoint**
   ```python
   # File: 5_NER11_Gold_Model/api/test_exercise.py
   from fastapi import APIRouter, HTTPException
   from pydantic import BaseModel

   router = APIRouter(prefix="/api/v2/test", tags=["Exercise"])

   class TestRequest(BaseModel):
       message: str

   class TestResponse(BaseModel):
       echo: str
       status: str

   @router.post("/echo", response_model=TestResponse)
   async def test_echo(request: TestRequest):
       """Test endpoint for training exercise"""
       return TestResponse(
           echo=request.message,
           status="success"
       )
   ```

3. **Register Endpoint**
   ```python
   # File: 5_NER11_Gold_Model/serve_model.py
   from api.test_exercise import router as test_router

   app.include_router(test_router)
   ```

4. **Start Server and Test**
   ```bash
   cd 5_NER11_Gold_Model
   source venv/bin/activate
   uvicorn serve_model:app --host 0.0.0.0 --port 8000 --reload

   # Test endpoint
   curl -X POST http://localhost:8000/api/v2/test/echo \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello AEON!"}'

   # Expected response:
   # {"echo": "Hello AEON!", "status": "success"}
   ```

5. **Write Unit Test**
   ```python
   # File: 5_NER11_Gold_Model/tests/test_exercise.py
   from fastapi.testclient import TestClient
   from serve_model import app

   client = TestClient(app)

   def test_echo_endpoint():
       response = client.post(
           "/api/v2/test/echo",
           json={"message": "Test message"}
       )
       assert response.status_code == 200
       data = response.json()
       assert data["echo"] == "Test message"
       assert data["status"] == "success"
   ```

6. **Run Test**
   ```bash
   pytest tests/test_exercise.py -v
   ```

**Success Criteria**:
- ✅ Endpoint implemented according to specification
- ✅ Server starts without errors
- ✅ Endpoint responds correctly to test requests
- ✅ Unit test passes
- ✅ OpenAPI documentation auto-generated
- ✅ Code follows project conventions

---

### Exercise 2: Query Neo4j Database and Interpret Results

**Objective**: Demonstrate proficiency with Cypher queries and data interpretation

**Duration**: 1-2 hours

**Tasks**:

1. **Sector Analysis Query**
   ```cypher
   // Connect to Neo4j Browser: http://localhost:7474

   // Query 1: Count equipment by sector
   MATCH (e:Equipment)
   WHERE e.sector IS NOT NULL
   RETURN e.sector AS sector_name,
          count(e) AS equipment_count,
          avg(e.risk_score) AS avg_risk
   ORDER BY equipment_count DESC
   LIMIT 10

   // Expected output: Table with sector names, counts, average risk scores
   ```

2. **Vulnerability Impact Query**
   ```cypher
   // Query 2: High-severity CVEs and affected equipment
   MATCH (e:Equipment)-[:HAS_VULNERABILITY]->(v:CVE)
   WHERE v.baseScore >= 7.0
   RETURN v.cveId AS vulnerability,
          v.baseScore AS severity,
          count(DISTINCT e) AS affected_equipment,
          collect(DISTINCT e.sector)[0..3] AS affected_sectors
   ORDER BY v.baseScore DESC
   LIMIT 20
   ```

3. **Attack Path Discovery**
   ```cypher
   // Query 3: Find attack paths using MITRE ATT&CK
   MATCH path = (t:Technique)-[:TARGETS]->(e:Equipment)-[:DEPENDS_ON*1..2]->(critical:Equipment)
   WHERE critical.criticality = "CRITICAL"
   RETURN t.technique_id AS technique,
          t.name AS technique_name,
          e.name AS entry_point,
          critical.name AS critical_target,
          length(path) AS path_length
   ORDER BY path_length ASC
   LIMIT 10
   ```

4. **Performance Profiling**
   ```cypher
   // Query 4: Profile a query to check performance
   PROFILE
   MATCH (e:Equipment)-[:HAS_VULNERABILITY]->(v:CVE)
   WHERE v.baseScore > 7.0
   RETURN count(e) AS high_risk_equipment

   // Interpret EXPLAIN output:
   // - Look for "Index Seek" (good) vs "All Nodes Scan" (bad)
   // - Check "db hits" and "rows" estimates
   // - Identify bottlenecks
   ```

**Success Criteria**:
- ✅ All queries execute successfully
- ✅ Can interpret query results accurately
- ✅ Can explain PROFILE output
- ✅ Identifies opportunities for query optimization
- ✅ Can create appropriate indexes

---

### Exercise 3: Train and Validate NER11 Model on New Text

**Objective**: Demonstrate ability to extend NER11 model with new training data

**Duration**: 2-3 hours

**Tasks**:

1. **Prepare Training Data**
   ```python
   # File: training_exercise.py
   import spacy
   from spacy.training import Example

   # Sample training data (real data would be larger)
   TRAIN_DATA = [
       ("APT29 used Cobalt Strike in the attack", {
           "entities": [(0, 5, "APT_GROUP"), (11, 24, "MALWARE")]
       }),
       ("The CVE-2024-9999 vulnerability affects Windows systems", {
           "entities": [(4, 17, "CVE"), (40, 47, "OS")]
       }),
       ("Ransomware group LockBit targeted healthcare sector", {
           "entities": [(17, 24, "RANSOMWARE"), (34, 44, "SECTOR")]
       })
   ]

   # Load base model
   nlp = spacy.load("models/ner11_v3/model-best")

   # Create training examples
   examples = []
   for text, annots in TRAIN_DATA:
       doc = nlp.make_doc(text)
       example = Example.from_dict(doc, annots)
       examples.append(example)

   print(f"Created {len(examples)} training examples")
   ```

2. **Fine-Tune Model**
   ```python
   # Update NER component
   ner = nlp.get_pipe("ner")

   # Add any new labels
   for _, annots in TRAIN_DATA:
       for ent in annots["entities"]:
           label = ent[2]
           if label not in ner.labels:
               ner.add_label(label)

   # Train
   from spacy.training import Example
   import random

   optimizer = nlp.resume_training()

   for epoch in range(10):
       random.shuffle(examples)
       losses = {}

       for example in examples:
           nlp.update([example], sgd=optimizer, losses=losses)

       print(f"Epoch {epoch+1}: Loss = {losses['ner']:.4f}")

   # Save updated model
   nlp.to_disk("models/exercise_model")
   ```

3. **Validate Model**
   ```python
   # Test model on new text
   test_text = "APT41 deployed WannaCry ransomware exploiting CVE-2017-0144"

   doc = nlp(test_text)

   print("Extracted entities:")
   for ent in doc.ents:
       print(f"  - {ent.text}: {ent.label_} (confidence: {ent._.score:.2f})")

   # Expected entities:
   # - APT41: APT_GROUP
   # - WannaCry: RANSOMWARE
   # - CVE-2017-0144: CVE
   ```

4. **Evaluate Performance**
   ```python
   # Create test set
   TEST_DATA = [
       ("APT28 used T1566.001 phishing technique", {
           "entities": [(0, 5, "APT_GROUP"), (11, 21, "TECHNIQUE")]
       })
   ]

   # Evaluate
   from spacy.scorer import Scorer

   scorer = Scorer()
   test_examples = [Example.from_dict(nlp.make_doc(text), annots)
                    for text, annots in TEST_DATA]

   scores = scorer.score(test_examples)
   print(f"Precision: {scores['ents_p']:.2f}")
   print(f"Recall: {scores['ents_r']:.2f}")
   print(f"F1-Score: {scores['ents_f']:.2f}")
   ```

**Success Criteria**:
- ✅ Training data prepared in correct format
- ✅ Model fine-tuned successfully
- ✅ New entities correctly extracted
- ✅ Model evaluation metrics >80% F1-score
- ✅ Updated model saved and deployable

---

### Exercise 4: Create a Simple API Endpoint and Integrate with Frontend

**Objective**: Full-stack integration exercise

**Duration**: 3-4 hours

**Backend Task**:
```python
# File: 5_NER11_Gold_Model/api/user_stats.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/v2/user", tags=["User Stats"])

class UserStatsResponse(BaseModel):
    total_queries: int
    total_entities_found: int
    top_entity_types: List[dict]
    recent_searches: List[str]

@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats():
    """Get user query statistics"""
    # Mock implementation (would query database in real scenario)
    return UserStatsResponse(
        total_queries=142,
        total_entities_found=1537,
        top_entity_types=[
            {"type": "APT_GROUP", "count": 45},
            {"type": "CVE", "count": 38},
            {"type": "MALWARE", "count": 32}
        ],
        recent_searches=[
            "ransomware attacks",
            "APT29 malware",
            "critical vulnerabilities"
        ]
    )

# Register in serve_model.py
from api.user_stats import router as user_stats_router
app.include_router(user_stats_router)
```

**Frontend Task**:
```typescript
// File: frontend/src/components/UserStatsCard.tsx
import React, { useEffect, useState } from 'react';

interface EntityType {
  type: string;
  count: number;
}

interface UserStats {
  total_queries: number;
  total_entities_found: number;
  top_entity_types: EntityType[];
  recent_searches: string[];
}

export function UserStatsCard() {
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/v2/user/stats')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch stats');
        return res.json();
      })
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading stats...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!stats) return null;

  return (
    <div className="user-stats-card">
      <h2>Your Search Statistics</h2>
      <div className="stats-grid">
        <div className="stat">
          <span className="stat-label">Total Queries</span>
          <span className="stat-value">{stats.total_queries}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Entities Found</span>
          <span className="stat-value">{stats.total_entities_found}</span>
        </div>
      </div>

      <h3>Top Entity Types</h3>
      <ul>
        {stats.top_entity_types.map(et => (
          <li key={et.type}>{et.type}: {et.count}</li>
        ))}
      </ul>

      <h3>Recent Searches</h3>
      <ul>
        {stats.recent_searches.map((search, idx) => (
          <li key={idx}>{search}</li>
        ))}
      </ul>
    </div>
  );
}
```

**Integration Test**:
```typescript
// File: frontend/src/components/__tests__/UserStatsCard.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { UserStatsCard } from '../UserStatsCard';

global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({
      total_queries: 142,
      total_entities_found: 1537,
      top_entity_types: [
        { type: "APT_GROUP", count: 45 }
      ],
      recent_searches: ["ransomware attacks"]
    })
  })
) as jest.Mock;

test('renders user stats correctly', async () => {
  render(<UserStatsCard />);

  await waitFor(() => {
    expect(screen.getByText('142')).toBeInTheDocument();
    expect(screen.getByText('1537')).toBeInTheDocument();
    expect(screen.getByText('APT_GROUP: 45')).toBeInTheDocument();
  });
});
```

**Success Criteria**:
- ✅ Backend endpoint returns correct data
- ✅ Frontend component fetches and displays data
- ✅ Error handling works (loading, error states)
- ✅ Integration test passes
- ✅ UI matches design specifications
- ✅ Component is reusable and properly typed

---

### Exercise 5: Diagnose and Resolve a Simulated Service Failure

**Objective**: Demonstrate troubleshooting skills and incident response

**Duration**: 1-2 hours

**Scenario 1: API Unresponsive**

**Symptoms**:
```bash
curl http://localhost:8000/health
# No response, connection timeout
```

**Diagnosis Steps**:
```bash
# 1. Check if API process is running
ps aux | grep uvicorn
# If not found → API crashed

# 2. Check Docker containers
docker ps -a | grep ner11
# If container stopped → Container issue

# 3. Check port availability
lsof -i :8000
# If port blocked → Port conflict

# 4. Review logs
tail -50 logs/api_$(date +%Y%m%d).log
# Look for error messages
```

**Resolution**:
```bash
# Option 1: Restart API
cd 5_NER11_Gold_Model
source venv/bin/activate
uvicorn serve_model:app --host 0.0.0.0 --port 8000

# Option 2: Kill conflicting process
kill -9 $(lsof -t -i:8000)
uvicorn serve_model:app --host 0.0.0.0 --port 8000

# Option 3: Use alternative port
uvicorn serve_model:app --host 0.0.0.0 --port 8001

# Verify resolution
curl http://localhost:8000/health
```

**Scenario 2: Neo4j Connection Failed**

**Symptoms**:
```bash
curl http://localhost:8000/health
# Response: {"neo4j_graph": "not_connected"}
```

**Diagnosis Steps**:
```bash
# 1. Check Neo4j container status
docker ps | grep neo4j
# If not listed → Container stopped

# 2. Check Neo4j logs
docker logs --tail 50 openspg-neo4j
# Look for startup errors

# 3. Test direct connection
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1"
# If fails → Neo4j not ready or credentials wrong

# 4. Check network connectivity
nc -zv localhost 7687
# If connection refused → Port not accessible
```

**Resolution**:
```bash
# Option 1: Start Neo4j container
docker start openspg-neo4j
# Wait 30 seconds for Neo4j to start
sleep 30
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1"

# Option 2: Restart Neo4j
docker restart openspg-neo4j
sleep 30

# Option 3: Check environment variables
echo $NEO4J_URI
echo $NEO4J_PASSWORD
# Verify they match container configuration

# Verify resolution
curl http://localhost:8000/health | python3 -m json.tool
```

**Scenario 3: Model Checksum Verification Failed**

**Symptoms**:
```bash
curl http://localhost:8000/health
# Response: {"model_checksum": "not_verified"}
```

**Diagnosis Steps**:
```bash
# 1. Check model files exist
ls -la models/ner11_v3/model-best/
ls -la models/ner11_v3/model-best/ner/

# 2. Verify checksums
cd models/ner11_v3/model-best
md5sum meta.json
# Expected: 0710e14d78a87d54866208cc6a5c8de3

md5sum ner/model
# Expected: f326672a81a00c54be06422aae07ecf1

# 3. Run validation script
cd ../../..
python utils/model_validator.py --model ner11_v3 --checksum-only
```

**Resolution**:
```bash
# If checksums mismatch → Model corrupted

# Option 1: Restore from backup
BACKUP_PATH="/mnt/d/1_Apps_to_Build/AEON_Cyber_Digital_Twin_backups/ner11_v3_20251203"
rm -rf models/ner11_v3
cp -r "$BACKUP_PATH/ner11_v3" models/

# Option 2: Re-extract from archive
cd ..
tar xzf NER11_Gold_Model.tar.gz -C 5_NER11_Gold_Model/

# Verify restoration
cd 5_NER11_Gold_Model
python utils/model_validator.py --model ner11_v3 --checksum-only

# Restart API
pkill -f "uvicorn serve_model"
uvicorn serve_model:app --host 0.0.0.0 --port 8000

# Verify resolution
curl http://localhost:8000/health | python3 -m json.tool
```

**Success Criteria**:
- ✅ Correctly diagnosed root cause of failure
- ✅ Followed systematic troubleshooting process
- ✅ Resolved issue using appropriate method
- ✅ Verified resolution with health checks
- ✅ Documented steps taken for knowledge base

---

## 5. Competency Validation

### Backend Developer Competency Checklist

**Technical Skills Assessment**:

| Skill | Assessment Method | Pass Criteria |
|-------|-------------------|---------------|
| **FastAPI Proficiency** | Implement 2 new API endpoints | Endpoints work correctly, follow conventions |
| **Cypher Query Optimization** | Optimize 1 slow query | >50% performance improvement |
| **Neo4j Schema Design** | Design schema for new feature | Schema normalized, indexed appropriately |
| **Model Integration** | Fine-tune NER11 on custom data | >80% F1-score on test set |
| **Testing** | Write test suite for feature | >80% code coverage, all tests pass |
| **Git Workflow** | Create feature branch, PR | Follows conventions, passes review |
| **Documentation** | Document new feature | Clear, complete, follows standards |

**Code Quality Standards**:
```python
# Review checklist
✅ Code follows PEP 8 style guide
✅ Type hints used for all functions
✅ Docstrings present and complete
✅ Error handling comprehensive
✅ Logging appropriate and informative
✅ No hardcoded values (use config)
✅ Security best practices followed
✅ Performance considerations addressed
```

**Validation Exercise** (Day 5 Afternoon):
```bash
# 1. Implement new API endpoint
Task: Create endpoint for sector risk trend analysis
Time: 90 minutes
Pass: Endpoint functional, tested, documented

# 2. Query optimization challenge
Task: Optimize provided slow Cypher query
Time: 45 minutes
Pass: >50% performance improvement

# 3. Integration test
Task: Write integration test for new endpoint
Time: 30 minutes
Pass: Test passes, covers edge cases

# Scoring:
- 3/3 tasks complete: PASS - Ready for independent work
- 2/3 tasks complete: CONDITIONAL - Needs mentoring for specific areas
- <2 tasks complete: FAIL - Requires extended training
```

---

### Frontend Developer Competency Checklist

**Technical Skills Assessment**:

| Skill | Assessment Method | Pass Criteria |
|-------|-------------------|---------------|
| **React/Next.js** | Build dashboard component | Component functional, follows patterns |
| **TypeScript** | Define interfaces from API specs | Types correct, no `any` usage |
| **API Integration** | Integrate with backend API | Successful data fetch, error handling |
| **State Management** | Implement form with validation | State managed correctly |
| **Testing** | Write component tests | >70% coverage, tests pass |
| **Responsive Design** | Create mobile-responsive layout | Works on mobile/tablet/desktop |
| **Performance** | Optimize component rendering | No unnecessary re-renders |

**Code Quality Standards**:
```typescript
// Review checklist
✅ TypeScript strict mode enabled
✅ No `any` types (use proper types)
✅ Components properly typed
✅ Props interfaces defined
✅ Hooks used correctly
✅ Error boundaries implemented
✅ Loading states handled
✅ Accessibility standards met (WCAG 2.1 Level AA)
```

**Validation Exercise** (Day 5 Afternoon):
```bash
# 1. Build user stats dashboard
Task: Create component displaying user statistics
Time: 90 minutes
Pass: Component renders correctly, data fetched

# 2. API integration
Task: Integrate component with backend API
Time: 45 minutes
Pass: Successful integration, error handling works

# 3. Component testing
Task: Write tests for dashboard component
Time: 30 minutes
Pass: Tests pass, cover main scenarios

# Scoring:
- 3/3 tasks complete: PASS - Ready for independent work
- 2/3 tasks complete: CONDITIONAL - Needs mentoring for specific areas
- <2 tasks complete: FAIL - Requires extended training
```

---

### DevOps Competency Checklist

**Technical Skills Assessment**:

| Skill | Assessment Method | Pass Criteria |
|-------|-------------------|---------------|
| **Docker Compose** | Create multi-service setup | All services start, communicate correctly |
| **Monitoring** | Set up Prometheus/Grafana | Metrics collected, dashboards functional |
| **CI/CD** | Create GitHub Actions workflow | Pipeline runs successfully |
| **Incident Response** | Resolve simulated outage | Issue diagnosed and resolved quickly |
| **Backup/Recovery** | Execute disaster recovery drill | System restored successfully |
| **Documentation** | Document deployment process | Clear, complete, reproducible |

**Code Quality Standards**:
```yaml
# Review checklist
✅ docker-compose.yml properly structured
✅ Health checks configured
✅ Volumes for persistence
✅ Network isolation implemented
✅ Environment variables externalized
✅ Resource limits set
✅ Restart policies configured
✅ Logging properly configured
```

**Validation Exercise** (Day 5 Afternoon):
```bash
# 1. Deploy full stack
Task: Use Docker Compose to deploy all services
Time: 60 minutes
Pass: All services healthy and connected

# 2. Configure monitoring
Task: Set up basic monitoring dashboard
Time: 45 minutes
Pass: Metrics visible, alerts configured

# 3. Disaster recovery drill
Task: Simulate database failure and recover
Time: 45 minutes
Pass: System restored to working state

# Scoring:
- 3/3 tasks complete: PASS - Ready for independent work
- 2/3 tasks complete: CONDITIONAL - Needs mentoring for specific areas
- <2 tasks complete: FAIL - Requires extended training
```

---

### Data Scientist Competency Checklist

**Technical Skills Assessment**:

| Skill | Assessment Method | Pass Criteria |
|-------|-------------------|---------------|
| **NER Model Training** | Train custom NER model | Model converges, >80% F1-score |
| **Data Preparation** | Annotate training data | Consistent labels, proper format |
| **Model Evaluation** | Analyze model performance | Interpret metrics correctly |
| **Error Analysis** | Identify model weaknesses | Actionable improvement recommendations |
| **Inference Optimization** | Optimize model speed | >30% inference speedup |
| **Documentation** | Document training pipeline | Reproducible, clear methodology |

**Code Quality Standards**:
```python
# Review checklist
✅ Training data properly formatted
✅ Train/dev/test split appropriate
✅ Hyperparameters documented
✅ Evaluation metrics comprehensive
✅ Model versioning implemented
✅ Reproducibility ensured (seeds set)
✅ Performance benchmarks documented
✅ Error analysis thorough
```

**Validation Exercise** (Day 5 Afternoon):
```bash
# 1. Prepare training data
Task: Annotate 50 examples with entities
Time: 45 minutes
Pass: Consistent labels, correct format

# 2. Train model
Task: Fine-tune NER11 on custom data
Time: 60 minutes
Pass: Model trains successfully, >80% F1

# 3. Error analysis
Task: Analyze model errors and recommend improvements
Time: 45 minutes
Pass: Clear analysis, actionable recommendations

# Scoring:
- 3/3 tasks complete: PASS - Ready for independent work
- 2/3 tasks complete: CONDITIONAL - Needs mentoring for specific areas
- <2 tasks complete: FAIL - Requires extended training
```

---

### QA/Testing Competency Checklist

**Technical Skills Assessment**:

| Skill | Assessment Method | Pass Criteria |
|-------|-------------------|---------------|
| **Unit Testing** | Write pytest test suite | >90% coverage, tests pass |
| **Integration Testing** | Test API endpoints end-to-end | All scenarios covered |
| **Performance Testing** | Load test API with Locust | Identify bottlenecks, recommendations |
| **Security Testing** | Perform OWASP Top 10 audit | Vulnerabilities identified, documented |
| **Automation** | Create automated regression suite | Tests run in CI/CD pipeline |
| **Bug Reporting** | Document found issues | Clear reproduction steps, severity rating |

**Code Quality Standards**:
```python
# Review checklist
✅ Test coverage >90%
✅ Tests independent (no interdependencies)
✅ Fixtures properly used
✅ Mocking appropriate
✅ Test data realistic
✅ Edge cases covered
✅ Performance tests included
✅ Security tests comprehensive
```

**Validation Exercise** (Day 5 Afternoon):
```bash
# 1. Write test suite
Task: Create comprehensive tests for API endpoint
Time: 60 minutes
Pass: >90% coverage, all tests pass

# 2. Performance testing
Task: Load test API and identify bottlenecks
Time: 45 minutes
Pass: Report with findings and recommendations

# 3. Security audit
Task: Test for common vulnerabilities
Time: 45 minutes
Pass: Complete audit report

# Scoring:
- 3/3 tasks complete: PASS - Ready for independent work
- 2/3 tasks complete: CONDITIONAL - Needs mentoring for specific areas
- <2 tasks complete: FAIL - Requires extended training
```

---

## 6. Ongoing Learning Program

### Weekly Knowledge-Sharing Sessions

**Format**: 1-hour sessions every Friday afternoon

**Week 1-4: Architecture Series**
- Week 1: Neo4j graph database design patterns
- Week 2: NER11 model architecture and training
- Week 3: API design best practices
- Week 4: Frontend architecture and state management

**Week 5-8: Advanced Topics**
- Week 5: Performance optimization techniques
- Week 6: Security hardening and vulnerability management
- Week 7: Scalability and high availability
- Week 8: Disaster recovery and business continuity

**Presenter Rotation**:
- Each team member presents once per quarter
- Encourages knowledge sharing and public speaking skills
- Topics can be recent work, lessons learned, or research

---

### Code Review Standards and Best Practices

**Review Process**:
```yaml
Pull Request Requirements:
  required_reviewers: 2
  minimum_approval: 2
  automated_checks:
    - linting (pass)
    - unit_tests (pass)
    - coverage_threshold: 80%
    - security_scan (pass)

Code Review Checklist:
  functionality:
    - ✅ Code works as specified
    - ✅ Edge cases handled
    - ✅ Error handling comprehensive

  quality:
    - ✅ Follows style guide
    - ✅ No code duplication
    - ✅ Functions single-purpose
    - ✅ Naming clear and descriptive

  security:
    - ✅ Input validation present
    - ✅ No hardcoded secrets
    - ✅ SQL injection prevention
    - ✅ XSS protection

  performance:
    - ✅ No obvious bottlenecks
    - ✅ Database queries optimized
    - ✅ Caching where appropriate

  testing:
    - ✅ Tests cover new code
    - ✅ Tests are meaningful
    - ✅ Edge cases tested

  documentation:
    - ✅ Docstrings present
    - ✅ Comments explain why, not what
    - ✅ API docs updated
```

**Review Guidelines**:
- ✅ Be kind and constructive
- ✅ Ask questions rather than making demands
- ✅ Explain reasoning for suggestions
- ✅ Acknowledge good code
- ✅ Focus on learning, not gatekeeping
- ✅ Respond to reviews within 24 hours

---

### Performance Optimization Opportunities

**Quarterly Performance Review**:
- Review application metrics
- Identify bottlenecks
- Plan optimization sprints
- Document improvements

**Common Optimization Areas**:
```yaml
Backend:
  - Database query optimization (add indexes)
  - Caching layer implementation (Redis)
  - API response pagination
  - Background task processing (Celery)

Frontend:
  - Code splitting and lazy loading
  - Image optimization
  - Bundle size reduction
  - Render optimization (React.memo, useMemo)

Infrastructure:
  - Container resource allocation
  - Load balancing configuration
  - CDN setup for static assets
  - Database replication for read scaling
```

---

### Security Training and Vulnerability Awareness

**Monthly Security Reviews**:
- Review recent CVEs relevant to stack
- Update dependencies with security patches
- Conduct security audits
- Practice incident response scenarios

**Security Training Topics**:
```yaml
Month 1: OWASP Top 10 Overview
Month 2: SQL Injection Prevention
Month 3: XSS and CSRF Protection
Month 4: Authentication and Authorization Best Practices
Month 5: Secure API Design
Month 6: Container Security
Month 7: Secrets Management
Month 8: Incident Response Procedures
Month 9: Data Privacy and Compliance (GDPR, CCPA)
Month 10: Supply Chain Security
Month 11: Penetration Testing Basics
Month 12: Security Review (Year in Review)
```

**Security Resources**:
- OWASP documentation: https://owasp.org/
- CVE database: https://cve.mitre.org/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- Internal security wiki: `05_Security/`

---

### Tool and Version Updates Communication

**Update Notification Process**:
```yaml
Critical Security Updates:
  notification: Immediate (Slack alert)
  timeline: Apply within 24 hours
  testing: Smoke tests only

Major Version Updates:
  notification: 2 weeks advance notice
  timeline: Apply within 1 sprint
  testing: Full regression suite

Minor Updates:
  notification: Sprint planning
  timeline: Next sprint
  testing: Automated tests

Deprecation Notices:
  notification: 6 months advance
  timeline: Before EOL
  migration_plan: Required
```

**Update Tracking**:
```bash
# Dependency version tracking
cat package.json  # Frontend dependencies
cat requirements.txt  # Backend dependencies
docker images  # Container image versions

# Check for updates
npm outdated
pip list --outdated
docker images --filter "dangling=true"

# Update log
cat UPDATES_LOG.md
# Format:
# - Date: YYYY-MM-DD
# - Component: [Package name]
# - Old version: X.Y.Z
# - New version: A.B.C
# - Breaking changes: Yes/No
# - Migration notes: [Steps taken]
```

---

## 7. Handoff Procedures

### Knowledge Transfer Checklist (When Team Member Changes Roles or Leaves)

**2 Weeks Before Transition**:

**Week 1: Documentation Sprint**
```yaml
Day 1-2: Document Current Work
  - ✅ List all active projects and status
  - ✅ Document pending tasks and blockers
  - ✅ Identify critical knowledge gaps

Day 3-4: Create Handoff Documentation
  - ✅ Code ownership map (which files you own)
  - ✅ Tribal knowledge documentation
  - ✅ Known issues and workarounds
  - ✅ Ongoing initiatives and roadmap

Day 5: Review and Feedback
  - ✅ Peer review of handoff docs
  - ✅ Identify missing information
  - ✅ Schedule knowledge transfer sessions
```

**Week 2: Knowledge Transfer Sessions**
```yaml
Day 1: Architecture and Design Decisions
  - 2-hour session with successor
  - Walk through system architecture
  - Explain design rationale
  - Demo critical flows

Day 2-3: Code Walkthrough
  - Pair programming sessions
  - Review critical code sections
  - Explain complex algorithms
  - Demonstrate debugging techniques

Day 4: Operations and Troubleshooting
  - Review operational procedures
  - Practice incident response scenarios
  - Share debugging tips and tricks
  - Demonstrate monitoring tools

Day 5: Final Q&A and Transition
  - Open Q&A session
  - Address remaining questions
  - Introduce to external stakeholders
  - Final checklist review
```

---

### Documentation Completion Requirements

**Mandatory Documentation**:

1. **Code Ownership Document**
   ```markdown
   # Code Ownership Transfer

   ## Transferring From
   Name: [Your name]
   Role: [Your role]
   Transition Date: YYYY-MM-DD

   ## Transferring To
   Name: [Successor name]
   Role: [Successor role]
   Start Date: YYYY-MM-DD

   ## Code Owned
   - 5_NER11_Gold_Model/api/economic_impact/
   - 5_NER11_Gold_Model/api/demographics/
   - 5_NER11_Gold_Model/api/prioritization/

   ## Critical Knowledge
   - Economic impact scoring algorithm (api/economic_impact/scoring.py)
   - Demographics data normalization (api/demographics/utils.py)
   - Prioritization ranking logic (api/prioritization/engine.py)

   ## Known Issues
   - Issue #123: Scoring algorithm slow for large datasets
     Workaround: Use caching for repeated queries
   - Issue #456: Demographics data missing for some sectors
     Workaround: Fall back to national averages

   ## Ongoing Work
   - Feature: Automated scoring updates (PR #789, 60% complete)
   - Refactoring: Demographics API restructure (design phase)

   ## Contact Information
   - Email: [your.email@company.com]
   - Slack: @yourname
   - Available for questions until: [date + 3 months]
   ```

2. **Tribal Knowledge Document**
   ```markdown
   # Tribal Knowledge - [Component Name]

   ## Things You Won't Find in the Code

   ### Why We Use Economic Impact Scoring v2
   - v1 had issues with seasonal fluctuations
   - v2 normalizes data using 3-year moving average
   - Decision made in Architecture Review 2025-10-15

   ### Database Query Quirks
   - Neo4j queries timeout if >50K results
   - Always add LIMIT to exploratory queries
   - Use pagination for large result sets

   ### Deployment Gotchas
   - NER11 model must be loaded before API starts
   - Qdrant collection must exist before ingestion
   - Neo4j needs 30 seconds warm-up time

   ### External Dependencies
   - Economic data from Bureau of Labor Statistics API
   - Demographics from Census Bureau API
   - Rate limits: 100 requests/hour

   ### Who to Ask
   - Neo4j queries: @database-team
   - NER11 model: @ml-team
   - Frontend integration: @frontend-team
   ```

3. **Runbook Updates**
   ```markdown
   # Operational Procedures Updates

   ## New Procedures Added
   - Economic Impact API Deployment (13_Procedures/E10_deployment.md)
   - Demographics Data Refresh (13_Procedures/E11_data_refresh.md)

   ## Updated Procedures
   - API Startup: Added E10/E11/E12 service checks
   - Health Monitoring: Added economic impact metrics

   ## Deprecated Procedures
   - Old economic scoring (v1) - removed 2025-12-01
   ```

---

### Access Revocation Procedures

**On Last Day of Work**:

**Morning**:
```yaml
1. Final Documentation Review
   - ✅ All handoff docs complete
   - ✅ Successor has copy of all documents
   - ✅ No pending commits or PRs

2. Knowledge Transfer Session
   - ✅ Final Q&A with successor
   - ✅ Introduce to key contacts
   - ✅ Share access to external resources

3. Code Cleanup
   - ✅ Commit all work in progress
   - ✅ Close or transfer open PRs
   - ✅ Update issue assignments
```

**Afternoon**:
```yaml
4. Access Transfer
   - ✅ Transfer code ownership in GitHub
   - ✅ Update CODEOWNERS file
   - ✅ Transfer project management tools access

5. System Access
   - ✅ Export personal configurations
   - ✅ Document custom scripts
   - ✅ Backup local work

6. Final Checklist
   - ✅ All tasks transferred or documented
   - ✅ Successor has all access needed
   - ✅ No orphaned work
```

**IT/Security Actions** (Completed by IT after last day):
```yaml
Access Revocation:
  - GitHub repository access: Revoked EOD
  - Neo4j database access: Revoked EOD
  - Docker Hub: Revoked EOD
  - Internal documentation: Revoked EOD+1
  - Email forwarding: Set up for 30 days
  - Slack account: Deactivated EOD+7

Archival:
  - Local machine backup: Retained 90 days
  - Email archive: Retained per policy
  - Documents: Transferred to team drive
```

---

### Code Ownership Transition

**GitHub Code Ownership Update**:
```bash
# Update CODEOWNERS file
# File: .github/CODEOWNERS

# Economic Impact API
/5_NER11_Gold_Model/api/economic_impact/ @new-owner @backup-owner

# Demographics API
/5_NER11_Gold_Model/api/demographics/ @new-owner @backup-owner

# Prioritization API
/5_NER11_Gold_Model/api/prioritization/ @new-owner @backup-owner

# Documentation
/docs/E10_*.md @new-owner
/docs/E11_*.md @new-owner
/docs/E12_*.md @new-owner

# Commit and push
git add .github/CODEOWNERS
git commit -m "chore: Update CODEOWNERS for team transition"
git push origin main
```

**Issue and PR Transfer**:
```bash
# Transfer open issues
# Via GitHub UI:
# 1. Go to Issues tab
# 2. Filter: assignee:old-owner is:open
# 3. Bulk re-assign to new-owner

# Transfer open PRs
# Via GitHub UI:
# 1. Go to Pull Requests tab
# 2. Filter: author:old-owner is:open
# 3. Update assignee and reviewers
# 4. Add transition note in PR description
```

---

### Incident Escalation Reassignment

**Update Escalation Matrix**:
```yaml
# File: 13_Procedures/ESCALATION_MATRIX.md

Level 1: On-Call Engineer
  Primary: on-call-rotation@company.com
  Response: 30 minutes

Level 2: Component Owners
  Economic Impact API: @new-owner
  Demographics API: @new-owner
  Prioritization API: @new-owner
  Response: 2 hours

Level 3: Tech Lead
  Contact: tech-lead@company.com
  Response: 4 hours

Level 4: Engineering Manager
  Contact: eng-manager@company.com
  Response: Same business day
```

**PagerDuty/On-Call Updates**:
```bash
# Update on-call schedule
# 1. Remove departing team member from rotation
# 2. Add new team member to rotation
# 3. Update escalation policies
# 4. Test alert delivery

# Verify updates
# 1. Trigger test alert
# 2. Confirm new owner receives alert
# 3. Confirm response procedures documented
```

---

## Appendix A: Quick Reference Commands

**Daily Development Commands**:
```bash
# Start development environment
docker start openspg-neo4j openspg-mysql qdrant
cd 5_NER11_Gold_Model
source venv/bin/activate
uvicorn serve_model:app --host 0.0.0.0 --port 8000 --reload

# Run tests
pytest tests/ -v --cov=api --cov-report=html

# Check code quality
flake8 api/
mypy api/

# Git workflow
git checkout -b feature/my-task
git add .
git commit -m "feat(api): Add new endpoint"
git push origin feature/my-task

# Database queries
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg'

# Check API health
curl http://localhost:8000/health | python3 -m json.tool
```

**Troubleshooting Commands**:
```bash
# Check service status
docker ps -a
ps aux | grep uvicorn

# View logs
docker logs --tail 50 openspg-neo4j
tail -50 logs/api_$(date +%Y%m%d).log

# Restart services
docker restart openspg-neo4j
pkill -f "uvicorn serve_model"
uvicorn serve_model:app --host 0.0.0.0 --port 8000

# Verify connections
curl http://localhost:8000/health
curl http://localhost:6333/health
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "RETURN 1"
```

---

## Appendix B: Contact List

**Team Roles and Contacts**:
```yaml
Engineering Manager:
  Name: [Manager Name]
  Email: manager@company.com
  Slack: @manager
  Responsibilities: Team oversight, resource allocation

Tech Lead:
  Name: [Tech Lead Name]
  Email: tech-lead@company.com
  Slack: @tech-lead
  Responsibilities: Architecture, technical direction

Backend Team Lead:
  Name: [Backend Lead]
  Email: backend-lead@company.com
  Slack: @backend-lead
  Responsibilities: API development, database management

Frontend Team Lead:
  Name: [Frontend Lead]
  Email: frontend-lead@company.com
  Slack: @frontend-lead
  Responsibilities: UI/UX, frontend architecture

DevOps Lead:
  Name: [DevOps Lead]
  Email: devops-lead@company.com
  Slack: @devops-lead
  Responsibilities: Infrastructure, deployment, monitoring

Data Science Lead:
  Name: [Data Science Lead]
  Email: ds-lead@company.com
  Slack: @ds-lead
  Responsibilities: ML models, training pipelines

QA Lead:
  Name: [QA Lead]
  Email: qa-lead@company.com
  Slack: @qa-lead
  Responsibilities: Testing, quality assurance
```

**External Contacts**:
```yaml
Infrastructure Support:
  Contact: infrastructure@company.com
  Hours: 24/7
  Use: Server issues, network problems

Security Team:
  Contact: security@company.com
  Hours: Business hours + on-call
  Use: Security incidents, vulnerability reports

IT Help Desk:
  Contact: helpdesk@company.com
  Hours: 8 AM - 6 PM EST
  Use: Access issues, software installation
```

---

## Appendix C: Training Resources

**Internal Resources**:
- Architecture Wiki: `ARCHITECTURE_OVERVIEW.md`
- API Documentation: `04_APIs/`
- Database Queries: `02_Databases/QUERIES_LIBRARY.md`
- Operations Procedures: `13_Procedures/`
- Migration Guides: `10_MacOS_Migration_Strategy/`

**External Learning**:

**Neo4j**:
- Official Documentation: https://neo4j.com/docs/
- GraphAcademy (Free courses): https://graphacademy.neo4j.com/
- Cypher Query Language Guide: https://neo4j.com/docs/cypher-manual/

**FastAPI**:
- Official Tutorial: https://fastapi.tiangolo.com/tutorial/
- Best Practices: https://fastapi.tiangolo.com/tutorial/bigger-applications/

**spaCy / NER11**:
- spaCy Documentation: https://spacy.io/usage
- Custom NER Training: https://spacy.io/usage/training#ner

**Docker**:
- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/

**React / Next.js**:
- React Docs: https://react.dev/
- Next.js Docs: https://nextjs.org/docs

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2025-12-04 | Initial comprehensive onboarding and knowledge transfer procedures |

---

**Document End**
