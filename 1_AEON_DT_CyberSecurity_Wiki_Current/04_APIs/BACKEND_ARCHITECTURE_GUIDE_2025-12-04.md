# AEON Cyber Digital Twin - Backend Architecture Guide

**File:** BACKEND_ARCHITECTURE_GUIDE_2025-12-04.md
**Created:** 2025-12-04
**Purpose:** Complete backend architecture guide for new developers
**Status:** COMPREHENSIVE ONBOARDING DOCUMENT

---

## 🎯 For Developers New to This Codebase

This guide assumes **ZERO prior knowledge** of the AEON backend. By the end, you'll understand the complete architecture, how to run it locally, and where to find everything you need.

---

## 📁 1. FOLDER STRUCTURE & KEY DIRECTORIES

### Project Root: `/5_NER11_Gold_Model/`

The entire backend lives in this directory. Here's what each folder contains:

```
/5_NER11_Gold_Model/
├── api/                          # ⭐ ALL REST API modules (Phase B1-B5)
│   ├── __init__.py              # API package initialization & imports
│   ├── dependencies.py          # Shared FastAPI dependencies (Qdrant, customer context)
│   ├── customer_isolation/      # Phase B1: Multi-tenant customer isolation
│   │   ├── customer_context.py  # CustomerContext class & access levels
│   │   ├── isolated_semantic_service.py  # Customer-aware semantic search
│   │   └── semantic_router.py   # Customer isolation API endpoints
│   ├── sbom_analysis/           # Phase B2: E03 SBOM dependency tracking
│   │   ├── sbom_router.py       # FastAPI routes
│   │   ├── sbom_service.py      # Business logic
│   │   └── sbom_models.py       # Pydantic schemas
│   ├── vendor_equipment/        # Phase B2: E15 Vendor equipment lifecycle
│   ├── threat_intelligence/     # Phase B3: E04 Threat intel correlation
│   ├── risk_scoring/            # Phase B3: E05 Risk scoring engine
│   ├── remediation/             # Phase B3: E06 Remediation workflows
│   ├── compliance_mapping/      # Phase B4: E07 Compliance frameworks
│   ├── automated_scanning/      # Phase B4: E08 Scanning & testing
│   ├── alert_management/        # Phase B4: E09 Alert management
│   ├── economic_impact/         # Phase B5: E10 Economic impact modeling
│   ├── demographics/            # Phase B5: E11 Demographics baseline
│   └── prioritization/          # Phase B5: E12 Prioritization & urgency
│
├── serve_model.py               # ⭐ MAIN API ENTRY POINT (FastAPI app)
├── docker/
│   ├── Dockerfile               # Container image specification
│   ├── docker-compose.yml       # Multi-container orchestration
│   └── requirements.txt         # Python dependencies
│
├── models/                      # NER11 ML model files (spaCy)
├── pipelines/                   # Entity embedding & semantic search
├── utils/                       # Context augmentation, model validation
├── tests/                       # Unit & integration tests
│   ├── api/                     # API endpoint tests
│   └── integration/             # End-to-end tests
│
├── docs/                        # Technical documentation
├── logs/                        # Application logs & results
├── examples/                    # Usage examples
├── config/                      # Configuration files
└── neo4j_migrations/            # Database schema migrations
```

### 🔑 Key File Patterns

Every API module follows this **CONSISTENT STRUCTURE**:

```
/api/{feature_name}/
├── __init__.py           # Module exports
├── {feature}_router.py   # FastAPI routes (HTTP endpoints)
├── {feature}_service.py  # Business logic (Qdrant/Neo4j operations)
└── {feature}_models.py   # Pydantic schemas (request/response validation)
```

**Example: Threat Intelligence**
- `/api/threat_intelligence/threat_router.py` → HTTP routes
- `/api/threat_intelligence/threat_service.py` → Business logic
- `/api/threat_intelligence/threat_models.py` → Data schemas

---

## 🛠️ 2. TECHNOLOGY STACK

### Core Backend Framework

```yaml
API_Framework:
  name: FastAPI
  version: "0.100+"
  description: "Modern Python REST API framework with automatic OpenAPI docs"
  why: "Async support, automatic validation, interactive API docs at /docs"

Validation:
  name: Pydantic
  version: "2.0+"
  description: "Data validation using Python type hints"
  why: "Type safety, automatic request/response validation, clear error messages"
```

### Databases

```yaml
Vector_Database:
  name: Qdrant
  url: "http://openspg-qdrant:6333"
  description: "Vector database for semantic search"
  use_cases:
    - Embedding storage (384-dimensional sentence-transformer vectors)
    - Semantic similarity search
    - Customer-isolated collections
  collections: "One per customer (e.g., 'CUST-001_entities')"

Graph_Database:
  name: Neo4j
  url: "bolt://openspg-neo4j:7687"
  credentials:
    user: "neo4j"
    password: "neo4j@openspg"
  description: "Graph database for relationships"
  use_cases:
    - Knowledge graph storage (1.1M+ nodes, 232K+ relationships)
    - Graph traversal (IDENTIFIES_THREAT, GOVERNS, RELATED_TO)
    - MITRE ATT&CK mappings
  web_ui: "http://localhost:7474"

Relational_Database:
  name: PostgreSQL
  url: "aeon-postgres-dev:5432"
  description: "Structured data storage"
  use_cases:
    - Compliance frameworks
    - Audit logs
    - User management (planned)
```

### Containerization

```yaml
Container_Runtime:
  name: Docker
  compose_version: "3.8"
  description: "Container orchestration"

API_Container:
  name: "ner11-gold-api"
  image: "ner11-gold-api:latest"
  port: "8000"
  gpu_support: true  # NVIDIA GPU for ML model inference
  base_image: "nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04"
  network: "aeon-net"  # Shared Docker network
```

### Python Stack

```python
# From docker/requirements.txt
dependencies = {
    "spacy[cuda11x]": "NER model framework",
    "spacy-transformers": "Transformer-based NER",
    "torch": "Deep learning backend",
    "fastapi": "REST API framework",
    "uvicorn": "ASGI server",
    "neo4j": "Neo4j driver",
    "sentence-transformers": "Text embeddings (384-dim)",
    "qdrant-client": "Vector DB client",
    "pydantic": "Data validation",
    "numpy": "Numerical operations",
    "pandas": "Data manipulation",
}
```

---

## 🏗️ 3. ARCHITECTURE OVERVIEW

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATIONS                       │
│  (Frontend UI, Postman, curl, Python scripts, etc.)        │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/REST API
                        │ X-Customer-ID header required
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              NER11 GOLD API (FastAPI)                        │
│              Container: ner11-gold-api:8000                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ serve_model.py → FastAPI app initialization          │  │
│  │ api/__init__.py → Import all API routers            │  │
│  │ api/dependencies.py → Shared dependencies            │  │
│  └──────────────────────────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────┴───────────────────────┐           │
│  │                                              │           │
│  ▼                                              ▼           │
│  Customer Isolation Layer              API Router Layer    │
│  - CustomerContext                     - Phase B1-B5 APIs  │
│  - Access verification                 - 251+ endpoints    │
│  - Multi-tenant isolation              - Pydantic models   │
└───┬────────────────────────────────┬───────────────────────┘
    │                                │
    ▼                                ▼
┌──────────────────────┐    ┌──────────────────────┐
│  Qdrant (Vector DB)  │    │   Neo4j (Graph DB)   │
│  openspg-qdrant:6333 │    │ openspg-neo4j:7687   │
│                      │    │                      │
│ • 384-dim embeddings │    │ • 1.1M+ nodes        │
│ • Customer isolated  │    │ • 232K+ relationships│
│ • Semantic search    │    │ • MITRE ATT&CK       │
│ • 670+ entities      │    │ • Knowledge graph    │
└──────────────────────┘    └──────────────────────┘
```

### Request Flow Example

**Scenario:** Frontend searches for "ransomware attacks on energy sector"

```
1. CLIENT → API
   POST http://localhost:8000/api/v2/threat-intel/search/semantic
   Headers: { "X-Customer-ID": "CUST-001" }
   Body: { "query": "ransomware attacks", "limit": 10 }

2. API → Customer Isolation (dependencies.py)
   - verify_customer_access() validates X-Customer-ID
   - Creates CustomerContext with access level
   - Passes context to router

3. ROUTER → SERVICE (threat_router.py → threat_service.py)
   - ThreatIntelligenceService receives CustomerContext
   - Applies customer isolation filter

4. SERVICE → Qdrant
   - Query customer-specific collection: "CUST-001_threat_actors"
   - Semantic search using 384-dim embeddings
   - Returns top 10 similar threat actors

5. SERVICE → Neo4j
   - Graph expansion: find related campaigns, IOCs, techniques
   - MITRE ATT&CK mapping via relationships
   - Returns graph context

6. SERVICE → API → CLIENT
   - Combines Qdrant results + Neo4j relationships
   - Returns JSON with threat intel + graph context
   - Response time: <450ms
```

### Multi-Tenant Customer Isolation

**WHY**: Multiple organizations use the same API, each needs isolated data

**HOW**: Every request requires `X-Customer-ID` header

```python
# From api/dependencies.py
async def verify_customer_access(
    x_customer_id: str = Header(..., alias="X-Customer-ID")
) -> CustomerContext:
    """
    Creates customer context for request-level isolation.

    Returns:
        CustomerContext with customer_id, namespace, access_level

    Raises:
        HTTPException 422 if customer ID missing/invalid
    """
```

**Customer Types:**

```yaml
Regular_Customer:
  example: "CUST-001"
  namespace: "acme-corp"
  data_access: "Only their own data"
  qdrant_collection: "CUST-001_entities"
  neo4j_label: "(:Entity {customer_id: 'CUST-001'})"

SYSTEM_Customer:
  example: "SYSTEM"
  namespace: "shared"
  data_access: "Baseline data shared across all customers"
  use_cases:
    - CVEs (Common Vulnerabilities)
    - CWEs (Weakness Enumeration)
    - CAPECs (Attack Patterns)
    - MITRE ATT&CK techniques
```

**Data Isolation Model:**

```
Customer CUST-001 sees:
├── CUST-001 data (their private entities)
└── SYSTEM data (shared CVEs, CWEs, CAPECs)

Customer CUST-002 sees:
├── CUST-002 data (their private entities)
└── SYSTEM data (shared CVEs, CWEs, CAPECs)

Customers CANNOT see each other's private data!
```

---

## 🚀 4. ALL PHASES COMPLETED (B1-B5)

### Phase B1: Customer Isolation (Foundation)

```yaml
Purpose: "Multi-tenant customer isolation for semantic search"
Status: ✅ OPERATIONAL
Key_Files:
  - api/customer_isolation/customer_context.py
  - api/dependencies.py
Features:
  - CustomerContext dataclass
  - Access levels: READ, WRITE, ADMIN
  - X-Customer-ID header validation
  - Namespace isolation
```

### Phase B2: SBOM & Vendor Equipment (63 endpoints)

```yaml
E03_SBOM_Analysis:
  prefix: "/api/v2/sbom"
  endpoints: 31
  features:
    - Component dependency tracking
    - Vulnerability correlation
    - License compliance
    - Supply chain analysis

E15_Vendor_Equipment:
  prefix: "/api/v2/vendor-equipment"
  endpoints: 32
  features:
    - Equipment lifecycle management
    - Vendor tracking
    - Patch management
    - EOL/EOS alerts
```

### Phase B3: Threat Intelligence & Risk (68 endpoints)

```yaml
E04_Threat_Intelligence:
  prefix: "/api/v2/threat-intel"
  endpoints: 24
  features:
    - Threat actor tracking
    - Campaign correlation
    - IOC (Indicators of Compromise)
    - MITRE ATT&CK mappings

E05_Risk_Scoring:
  prefix: "/api/v2/risk"
  endpoints: 22
  features:
    - CVSS scoring
    - Business impact assessment
    - Attack surface analysis
    - Risk aggregation

E06_Remediation:
  prefix: "/api/v2/remediation"
  endpoints: 22
  features:
    - Workflow automation
    - Patch management
    - Mitigation tracking
    - Playbook execution
```

### Phase B4: Compliance & Monitoring (62 endpoints)

```yaml
E07_Compliance_Mapping:
  prefix: "/api/v2/compliance"
  endpoints: 22
  features:
    - Framework mapping (NIST, ISO, CIS)
    - Control tracking
    - Audit reporting
    - Gap analysis

E08_Automated_Scanning:
  prefix: "/api/v2/scanning"
  endpoints: 20
  features:
    - Vulnerability scanning
    - Configuration testing
    - Schedule management
    - Result aggregation

E09_Alert_Management:
  prefix: "/api/v2/alerts"
  endpoints: 20
  features:
    - Alert creation & routing
    - Severity classification
    - Notification management
    - Alert lifecycle
```

### Phase B5: Economic Impact & Prioritization (58 endpoints)

```yaml
E10_Economic_Impact:
  prefix: "/api/v2/economic-impact"
  endpoints: 20
  features:
    - Financial impact modeling
    - Cost-benefit analysis
    - ROI calculations
    - Budget optimization

E11_Demographics:
  prefix: "/api/v2/demographics"
  endpoints: 18
  features:
    - Psychohistory baseline data
    - Population modeling
    - Threat landscape analysis
    - Sector profiling

E12_Prioritization:
  prefix: "/api/v2/prioritization"
  endpoints: 20
  features:
    - Risk-based ranking
    - Urgency scoring
    - Resource allocation
    - Decision support
```

### TOTAL IMPLEMENTATION STATUS

```
Phase B1: CUSTOMER_LABELS          →  Foundation
Phase B2: E03 + E15                →  63 endpoints ✅
Phase B3: E04 + E05 + E06          →  68 endpoints ✅
Phase B4: E07 + E08 + E09          →  62 endpoints ✅
Phase B5: E10 + E11 + E12          →  58 endpoints ✅
────────────────────────────────────────────────────
TOTAL:                                251+ endpoints
```

---

## 🏃 5. HOW TO RUN LOCALLY

### Prerequisites

```bash
# Required:
- Docker & Docker Compose
- NVIDIA GPU (for ML model inference)
- 8GB+ available RAM
- Python 3.10+ (for development)
```

### Step 1: Verify Docker Containers

```bash
# Check all required containers are running
docker ps

# Expected containers:
# - ner11-gold-api:8000       (FastAPI backend)
# - openspg-qdrant:6333       (Vector database)
# - openspg-neo4j:7687        (Graph database)
# - aeon-postgres-dev:5432    (PostgreSQL)
```

**Not running?** Start them:

```bash
cd /path/to/5_NER11_Gold_Model/docker
docker-compose up -d
```

### Step 2: Test API Connectivity

```bash
# Test main API health
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "version": "3.3.0"}

# Test interactive API documentation
open http://localhost:8000/docs  # macOS
xdg-open http://localhost:8000/docs  # Linux
start http://localhost:8000/docs  # Windows
```

### Step 3: Test Customer Isolation Endpoint

```bash
# Semantic search with customer isolation
curl -X POST http://localhost:8000/api/v2/customer-isolation/search/semantic \
  -H "Content-Type: application/json" \
  -H "X-Customer-ID: CUST-001" \
  -d '{
    "query": "ransomware attacks",
    "limit": 5
  }'

# Expected: JSON with 5 semantically similar entities from CUST-001's data
```

### Step 4: Test Phase B2-B5 APIs

```bash
# Test SBOM Analysis (Phase B2)
curl -X GET http://localhost:8000/api/v2/sbom/components \
  -H "X-Customer-ID: CUST-001"

# Test Threat Intelligence (Phase B3)
curl -X GET http://localhost:8000/api/v2/threat-intel/actors \
  -H "X-Customer-ID: CUST-001"

# Test Compliance (Phase B4)
curl -X GET http://localhost:8000/api/v2/compliance/frameworks \
  -H "X-Customer-ID: CUST-001"

# Test Economic Impact (Phase B5)
curl -X GET http://localhost:8000/api/v2/economic-impact/scenarios \
  -H "X-Customer-ID: CUST-001"
```

### Step 5: Access Database UIs

```bash
# Qdrant Vector Database Dashboard
open http://localhost:6333/dashboard

# Neo4j Graph Database Browser
open http://localhost:7474
# Login: neo4j / neo4j@openspg
```

### Step 6: Run Tests

```bash
# Navigate to backend directory
cd /path/to/5_NER11_Gold_Model

# Install test dependencies (if not in container)
pip install pytest pytest-asyncio httpx

# Run all tests
pytest tests/

# Run specific test suite
pytest tests/api/test_economic_impact.py
pytest tests/integration/test_threat_intel_integration.py
```

---

## 🔧 6. API PATTERNS

All 251+ endpoints follow these **CONSISTENT PATTERNS**:

### URL Structure

```
http://localhost:8000/api/v2/{feature}/{endpoint}

Examples:
/api/v2/sbom/components              → SBOM component list
/api/v2/threat-intel/actors          → Threat actor list
/api/v2/risk/scores                  → Risk scores
/api/v2/compliance/frameworks        → Compliance frameworks
/api/v2/economic-impact/scenarios    → Economic scenarios
```

### Required Headers

```http
X-Customer-ID: CUST-001    # REQUIRED for all endpoints
Content-Type: application/json
```

### Authentication (Future)

```http
Authorization: Bearer <JWT_TOKEN>    # Planned for production
X-Customer-ID: CUST-001             # Still required
```

### Request/Response Pattern

**Request:**

```json
POST /api/v2/threat-intel/search/semantic
Headers: { "X-Customer-ID": "CUST-001" }

{
  "query": "ransomware attacks on healthcare",
  "limit": 10,
  "filters": {
    "actor_type": "RANSOMWARE",
    "target_sectors": ["healthcare"]
  }
}
```

**Response:**

```json
{
  "results": [
    {
      "entity": "LockBit",
      "type": "RANSOMWARE",
      "score": 0.92,
      "metadata": {
        "campaigns": ["Operation HealthHack"],
        "target_sectors": ["healthcare"],
        "mitre_techniques": ["T1486", "T1490"]
      }
    }
  ],
  "total": 47,
  "page": 1,
  "customer_id": "CUST-001"
}
```

### Error Responses

```json
// 422 Unprocessable Entity (missing X-Customer-ID)
{
  "detail": "X-Customer-ID header is required and cannot be empty"
}

// 403 Forbidden (access denied)
{
  "detail": "Customer CUST-001 does not have WRITE access"
}

// 404 Not Found
{
  "detail": "Entity not found: ACTOR-123"
}

// 500 Internal Server Error
{
  "detail": "Database connection failed",
  "error_id": "ERR-20251204-001"
}
```

### Vector Embeddings

**All semantic search uses 384-dimensional sentence-transformer embeddings:**

```python
# Embedding model: sentence-transformers/all-MiniLM-L6-v2
embedding_dim = 384
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Example embedding
text = "ransomware attack on healthcare"
embedding = model.encode(text)  # Returns 384-dim vector

# Stored in Qdrant collections:
# - CUST-001_entities
# - CUST-002_entities
# - SYSTEM_entities (shared baseline)
```

### Graph Relationships

**Neo4j relationship types used across APIs:**

```cypher
// Threat relationships
(:ThreatActor)-[:USES]->(:Technique)
(:ThreatActor)-[:TARGETS]->(:Sector)
(:Campaign)-[:ATTRIBUTES_TO]->(:ThreatActor)

// SBOM relationships
(:Component)-[:DEPENDS_ON]->(:Component)
(:Component)-[:HAS_VULNERABILITY]->(:CVE)
(:Vendor)-[:PRODUCES]->(:Component)

// Compliance relationships
(:Control)-[:MAPS_TO]->(:Framework)
(:Asset)-[:COMPLIES_WITH]->(:Control)
(:Vulnerability)-[:VIOLATES]->(:Control)

// Risk relationships
(:Asset)-[:HAS_RISK]->(:RiskScore)
(:Vulnerability)-[:AFFECTS]->(:Asset)
(:Mitigation)-[:REDUCES]->(:Risk)
```

---

## 📚 7. KEY FILES TO UNDERSTAND FIRST

### 1. `/5_NER11_Gold_Model/serve_model.py` (Main API Entry Point)

**Purpose:** FastAPI application initialization

**What it does:**
- Initializes FastAPI app
- Loads NER11 spaCy model
- Connects to Qdrant (vector DB)
- Connects to Neo4j (graph DB)
- Registers all API routers from `api/__init__.py`
- Provides health check endpoint

**Key code:**

```python
from fastapi import FastAPI
from api import (
    vendor_router,
    sbom_router,
    threat_router,
    risk_router,
    # ... all other routers
)

app = FastAPI(
    title="NER11 Gold Standard API",
    version="3.3.0"
)

# Register all routers
app.include_router(vendor_router)
app.include_router(sbom_router)
app.include_router(threat_router)
# ... all B1-B5 routers
```

### 2. `/5_NER11_Gold_Model/api/__init__.py` (API Package Init)

**Purpose:** Central import hub for all API modules

**What it does:**
- Imports all routers from Phase B1-B5
- Imports all service classes
- Imports customer isolation components
- Provides `__all__` for clean exports

**Key code:**

```python
from .customer_isolation import (
    CustomerContext,
    CustomerIsolatedSemanticService,
)

# Phase B2 APIs
from .vendor_equipment import vendor_router, VendorEquipmentService
from .sbom_analysis import sbom_router, SBOMAnalysisService

# Phase B3 APIs
from .threat_intelligence import threat_router, ThreatIntelligenceService
from .risk_scoring import risk_router, RiskScoringService
from .remediation import remediation_router, RemediationService

# Phase B4 APIs
from .compliance_mapping import compliance_router, ComplianceService
from .automated_scanning import scanning_router, ScanningService
from .alert_management import alert_router, AlertService

# Phase B5 APIs
from .economic_impact import router as economic_router
from .demographics import demographics_router, DemographicsService
from .prioritization import router as prioritization_router
```

### 3. `/5_NER11_Gold_Model/api/dependencies.py` (Shared Dependencies)

**Purpose:** FastAPI dependency injection for customer context & database clients

**What it does:**
- Provides `get_qdrant_client()` dependency
- Provides `verify_customer_access()` dependency
- Validates X-Customer-ID header
- Creates CustomerContext for requests
- Provides admin access verification

**Key code:**

```python
from fastapi import Header, HTTPException, Depends
from qdrant_client import QdrantClient
from .customer_isolation import CustomerContext

@lru_cache()
def get_qdrant_client() -> QdrantClient:
    """Get cached Qdrant client (singleton)."""
    return QdrantClient(url="http://localhost:6333")

async def verify_customer_access(
    x_customer_id: str = Header(..., alias="X-Customer-ID")
) -> CustomerContext:
    """
    Verify customer and create context.
    Used in ALL API endpoints as dependency.
    """
    if not x_customer_id:
        raise HTTPException(422, "X-Customer-ID required")

    return CustomerContextManager.create_context(
        customer_id=x_customer_id
    )
```

**Usage in routers:**

```python
from fastapi import APIRouter, Depends
from ..dependencies import verify_customer_access
from ..customer_isolation import CustomerContext

router = APIRouter()

@router.post("/api/v2/threat-intel/search")
async def search(
    request: SearchRequest,
    context: CustomerContext = Depends(verify_customer_access)
):
    """
    context.customer_id automatically populated from X-Customer-ID header
    """
    # Use context.customer_id for isolation
    results = service.search(request, context)
    return results
```

### 4. `/5_NER11_Gold_Model/api/customer_isolation/customer_context.py`

**Purpose:** Customer context dataclass for multi-tenant isolation

**What it does:**
- Defines `CustomerContext` dataclass
- Defines `CustomerAccessLevel` enum (READ, WRITE, ADMIN)
- Provides `CustomerContextManager` for context creation
- Validates customer IDs

**Key code:**

```python
from dataclasses import dataclass
from enum import Enum

class CustomerAccessLevel(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

@dataclass
class CustomerContext:
    customer_id: str          # "CUST-001"
    namespace: str            # "acme-corp"
    access_level: CustomerAccessLevel
    include_system: bool = True  # Include SYSTEM baseline data
```

### 5. `/5_NER11_Gold_Model/docker/Dockerfile` (Container Specification)

**Purpose:** Defines the API container image

**Key components:**

```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Install Python 3.10
RUN apt-get update && apt-get install -y python3.10 python3-pip

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Download spaCy NER models
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download en_core_web_trf

# Expose API port
EXPOSE 8000

# Run FastAPI server
CMD ["python3", "serve_model.py"]
```

### 6. `/5_NER11_Gold_Model/docker/docker-compose.yml` (Container Orchestration)

**Purpose:** Defines multi-container setup

**Key configuration:**

```yaml
services:
  ner11-gold-api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ../:/app  # Mount entire project directory
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia  # GPU support
              count: all
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - MODEL_PATH=models/ner11_v3/model-best
    networks:
      - aeon-net  # Shared network with Qdrant/Neo4j

networks:
  aeon-net:
    external: true  # Must already exist
```

### 7. Example Router: `/api/threat_intelligence/threat_router.py`

**Purpose:** Shows standard API router pattern

**Structure:**

```python
from fastapi import APIRouter, Depends
from ..dependencies import verify_customer_access
from ..customer_isolation import CustomerContext
from .threat_service import ThreatIntelligenceService
from .threat_models import (
    ThreatActorSearchRequest,
    ThreatActorResponse,
)

router = APIRouter(
    prefix="/api/v2/threat-intel",
    tags=["threat-intelligence"]
)

service = ThreatIntelligenceService()

@router.post("/search/semantic")
async def search_threat_actors(
    request: ThreatActorSearchRequest,
    context: CustomerContext = Depends(verify_customer_access)
) -> ThreatActorResponse:
    """
    Semantic search for threat actors using Qdrant embeddings.

    Args:
        request: Search parameters (query, limit, filters)
        context: Auto-injected customer context from X-Customer-ID

    Returns:
        ThreatActorResponse with matching actors + graph context
    """
    return await service.semantic_search(request, context)
```

---

## 🧪 8. DEVELOPMENT WORKFLOW

### Making Changes

```bash
# 1. Create feature branch
git checkout -b feature/new-api-endpoint

# 2. Make changes to API modules
# Example: Add new endpoint to threat_router.py

# 3. Run tests locally
pytest tests/api/test_threat_intel.py

# 4. Test in container
docker-compose restart ner11-gold-api

# 5. Test with curl
curl -X POST http://localhost:8000/api/v2/threat-intel/new-endpoint \
  -H "X-Customer-ID: CUST-001" \
  -d '{"test": "data"}'

# 6. Commit changes
git add api/threat_intelligence/
git commit -m "feat(threat-intel): Add new endpoint for X"

# 7. Push and create PR
git push origin feature/new-api-endpoint
```

### Adding a New API Module

**Example: Adding E13 Network Traffic Analysis**

```bash
# 1. Create module directory
mkdir -p api/network_traffic

# 2. Create required files
touch api/network_traffic/__init__.py
touch api/network_traffic/network_router.py
touch api/network_traffic/network_service.py
touch api/network_traffic/network_models.py

# 3. Implement router (network_router.py)
from fastapi import APIRouter, Depends
from ..dependencies import verify_customer_access

router = APIRouter(
    prefix="/api/v2/network-traffic",
    tags=["network-analysis"]
)

@router.get("/flows")
async def get_flows(
    context: CustomerContext = Depends(verify_customer_access)
):
    # Implementation here
    pass

# 4. Export in api/__init__.py
from .network_traffic import router as network_router

__all__ = [
    # ... existing exports
    "network_router",
]

# 5. Register in serve_model.py
from api import network_router
app.include_router(network_router)

# 6. Write tests
# tests/api/test_network_traffic.py

# 7. Run tests
pytest tests/api/test_network_traffic.py
```

### Debugging Tips

```bash
# View container logs
docker logs ner11-gold-api --tail 100 -f

# Check Qdrant collections
curl http://localhost:6333/collections

# Query Neo4j directly
docker exec -it openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg"
# Then run: MATCH (n) RETURN count(n);

# Interactive API testing
open http://localhost:8000/docs  # Swagger UI
```

---

## 🎓 9. LEARNING PATH

**For developers completely new to this codebase:**

### Week 1: Foundation

```yaml
Day 1-2: Setup & Exploration
  - Get Docker containers running
  - Test all endpoints with curl
  - Explore Swagger docs at /docs
  - Read serve_model.py

Day 3-4: Customer Isolation
  - Read customer_context.py
  - Read dependencies.py
  - Understand X-Customer-ID flow
  - Test with different customer IDs

Day 5: API Patterns
  - Pick one module (e.g., threat_intelligence)
  - Read router → service → models
  - Trace one request from endpoint to database
```

### Week 2: Deep Dive

```yaml
Day 6-7: Databases
  - Learn Qdrant vector search
  - Learn Neo4j graph queries
  - Understand embedding generation
  - Run example queries

Day 8-9: Service Layer
  - Read service implementations
  - Understand Qdrant operations
  - Understand Neo4j operations
  - Trace customer isolation in queries

Day 10: Testing
  - Read existing tests
  - Write your first test
  - Run test suite
  - Debug test failures
```

### Week 3: Contribution

```yaml
Day 11-12: Simple Feature
  - Add new query filter
  - Add new endpoint parameter
  - Write tests
  - Submit PR

Day 13-14: Module Enhancement
  - Enhance existing module
  - Add new business logic
  - Update documentation

Day 15: Code Review
  - Review PRs from team
  - Give feedback
  - Learn from others' code
```

---

## 🔗 10. RELATED DOCUMENTATION

```
/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/
├── 00_API_STATUS_AND_ROADMAP.md         # High-level API status
├── 00_FRONTEND_QUICK_START.md           # Frontend integration guide
├── API_PHASE_B5_CAPABILITIES_2025-12-04.md  # Phase B5 details
└── BACKEND_ARCHITECTURE_GUIDE_2025-12-04.md  # This document

/5_NER11_Gold_Model/
├── README.md                            # Project overview
├── docs/
│   ├── E10_ECONOMIC_IMPACT_API.md      # E10 API specification
│   ├── E11_DEMOGRAPHICS_INTERFACES.ts  # E11 TypeScript types
│   └── E12_PRIORITIZATION_IMPLEMENTATION.md  # E12 details
└── examples/                            # Usage examples
```

---

## 🆘 GETTING HELP

**When stuck:**

1. **Check Logs:** `docker logs ner11-gold-api --tail 100`
2. **Test Databases:** Verify Qdrant/Neo4j are responding
3. **Swagger UI:** http://localhost:8000/docs for interactive testing
4. **Read Tests:** Check `tests/` for usage examples
5. **Ask Team:** Share error messages and what you've tried

**Common Issues:**

```yaml
Issue: "Connection refused to Qdrant"
Fix: docker-compose up -d qdrant
Check: curl http://localhost:6333/collections

Issue: "X-Customer-ID header is required"
Fix: Add header to all API requests
Example: curl -H "X-Customer-ID: CUST-001" ...

Issue: "GPU not available"
Fix: Check NVIDIA Docker runtime installed
Check: docker run --rm --gpus all nvidia/cuda:11.8.0-base nvidia-smi

Issue: "Module not found: api.threat_intelligence"
Fix: Check Python path and __init__.py files
Check: ls -la api/threat_intelligence/
```

---

## ✅ QUICK REFERENCE CARD

**Copy this to your desk!**

```
┌─────────────────────────────────────────────────────┐
│         AEON BACKEND QUICK REFERENCE                │
├─────────────────────────────────────────────────────┤
│ API URL:        http://localhost:8000               │
│ API Docs:       http://localhost:8000/docs          │
│ Qdrant:         http://localhost:6333/dashboard     │
│ Neo4j:          http://localhost:7474               │
│                 (neo4j / neo4j@openspg)             │
├─────────────────────────────────────────────────────┤
│ Main Files:                                         │
│ • serve_model.py              FastAPI app           │
│ • api/__init__.py             Router imports        │
│ • api/dependencies.py         Shared deps           │
│ • api/{module}/router.py      HTTP endpoints        │
│ • api/{module}/service.py     Business logic        │
│ • api/{module}/models.py      Pydantic schemas      │
├─────────────────────────────────────────────────────┤
│ Test Endpoint:                                      │
│ curl -X POST http://localhost:8000/api/v2/... \    │
│   -H "X-Customer-ID: CUST-001" \                    │
│   -H "Content-Type: application/json" \             │
│   -d '{"query": "test"}'                            │
├─────────────────────────────────────────────────────┤
│ Debug:                                              │
│ docker logs ner11-gold-api --tail 100 -f            │
│ docker exec -it openspg-neo4j cypher-shell          │
│ curl http://localhost:6333/collections              │
├─────────────────────────────────────────────────────┤
│ Run Tests:                                          │
│ pytest tests/                                       │
│ pytest tests/api/test_{module}.py                   │
└─────────────────────────────────────────────────────┘
```

---

## 📊 API ENDPOINT SUMMARY

**251+ Endpoints Across All Phases:**

```
Phase B1: Customer Isolation
└── /api/v2/customer-isolation/*              (Foundation)

Phase B2: SBOM & Vendor (63 endpoints)
├── /api/v2/sbom/*                            (31 endpoints)
└── /api/v2/vendor-equipment/*                (32 endpoints)

Phase B3: Threat Intelligence & Risk (68 endpoints)
├── /api/v2/threat-intel/*                    (24 endpoints)
├── /api/v2/risk/*                            (22 endpoints)
└── /api/v2/remediation/*                     (22 endpoints)

Phase B4: Compliance & Monitoring (62 endpoints)
├── /api/v2/compliance/*                      (22 endpoints)
├── /api/v2/scanning/*                        (20 endpoints)
└── /api/v2/alerts/*                          (20 endpoints)

Phase B5: Economic & Prioritization (58 endpoints)
├── /api/v2/economic-impact/*                 (20 endpoints)
├── /api/v2/demographics/*                    (18 endpoints)
└── /api/v2/prioritization/*                  (20 endpoints)
```

---

## 🎯 NEXT STEPS

**Now that you understand the architecture:**

1. ✅ **Get Local Environment Running** (Section 5)
2. ✅ **Test All Phase B1-B5 APIs** (Section 5.4)
3. ✅ **Read Key Files** (Section 7)
4. ✅ **Pick One Module to Deep Dive** (Week 2)
5. ✅ **Make Your First Contribution** (Section 8)

**Questions?** Check logs, read tests, ask team!

---

**Document Version:** 1.0.0
**Last Updated:** 2025-12-04
**Next Review:** When Phase B6+ begins
**Maintained By:** AEON Backend Team

---

*Welcome to the AEON backend! You've got this! 🚀*
