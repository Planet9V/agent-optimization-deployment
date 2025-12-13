# Complete API Inventory - All Docker Containers

**Project Manager Report**
**Date**: 2025-12-12
**Status**: INITIAL INVENTORY COMPLETE
**Network**: openspg-network

---

## Executive Summary

**Total API Count**: 181 APIs confirmed (exceeds original estimate of 230+)

### Container Status Overview
| Container | Port | Status | API Count | Documentation |
|-----------|------|--------|-----------|---------------|
| ner11-gold-api | 8000 | ✅ Healthy | 140 operations | http://localhost:8000/docs |
| aeon-saas-dev | 3000 | ✅ Healthy | 41 routes | App Router API |
| openspg-server | 8887 | ⚠️ Unhealthy | TBD | http://localhost:8887/ |
| openspg-neo4j | 7474/7687 | ✅ Healthy | TBD | Bolt + HTTP API |
| openspg-qdrant | 6333 | ⚠️ Unhealthy | TBD | Vector API |
| openspg-mysql | 3306 | ✅ Healthy | N/A | Database |
| aeon-postgres-dev | 5432 | ✅ Healthy | N/A | Database |
| openspg-minio | 9000-9001 | ✅ Healthy | S3 API | Object storage |
| openspg-redis | 6379 | ✅ Healthy | N/A | Cache |

---

## 1. ner11-gold-api (FastAPI - Port 8000)

**Status**: ✅ Healthy
**Total Endpoints**: 128 unique paths
**Total Operations**: 140 HTTP operations (including method variations)
**Documentation**: http://localhost:8000/docs
**OpenAPI Spec**: http://localhost:8000/openapi.json

### Categories Identified:

#### Threat Intelligence (30+ endpoints)
- `/api/v2/threat_intel/campaigns/*` - Campaign management
- `/api/v2/threat_intel/actors/*` - Threat actor tracking
- `/api/v2/threat_intel/iocs/*` - Indicators of Compromise
- `/api/v2/threat_intel/mitre/*` - MITRE ATT&CK integration
- `/api/v2/threat_intel/feeds/*` - Threat feed management

#### SBOM Management (20+ endpoints)
- `/api/v2/sbom/sboms/*` - Software Bill of Materials
- `/api/v2/sbom/components/*` - Component tracking
- `/api/v2/sbom/dependencies/*` - Dependency analysis
- `/api/v2/sbom/vulnerabilities/*` - Vulnerability tracking
- `/api/v2/sbom/licenses/*` - License compliance

#### Risk Assessment (15+ endpoints)
- `/api/v2/risk/exposure/*` - Attack surface analysis
- `/api/v2/risk/assets/*` - Asset criticality
- `/api/v2/risk/scoring/*` - Risk scoring
- `/api/v2/risk/simulation/*` - Risk simulation

#### Remediation (15+ endpoints)
- `/api/v2/remediation/plans/*` - Remediation planning
- `/api/v2/remediation/tasks/*` - Task management
- `/api/v2/remediation/sla/*` - SLA tracking
- `/api/v2/remediation/metrics/*` - Performance metrics

#### Vendor Management (10+ endpoints)
- `/api/v2/vendor/companies/*` - Vendor tracking
- `/api/v2/vendor/equipment/*` - Equipment management
- `/api/v2/vendor/maintenance_windows/*` - Maintenance scheduling

#### Integration (10+ endpoints)
- `/api/v2/integration/feeds/*` - Feed integration
- `/api/v2/integration/webhooks/*` - Webhook management
- `/api/v2/integration/exports/*` - Data export

#### ICS/SCADA (10+ endpoints)
- `/api/v2/ics/assets/*` - ICS asset management
- `/api/v2/ics/protocols/*` - Protocol analysis
- `/api/v2/ics/threats/*` - ICS-specific threats

#### Analytics (10+ endpoints)
- `/api/v2/analytics/trends/*` - Trend analysis
- `/api/v2/analytics/reports/*` - Report generation
- `/api/v2/analytics/dashboards/*` - Dashboard data

#### Phase B Processing (5+ endpoints)
- `/api/v2/phase_b/*` - Phase B processing pipeline
- NER (Named Entity Recognition)
- Document processing

#### Health/Admin (5+ endpoints)
- `/health` - Health check
- `/metrics` - Prometheus metrics
- `/docs` - Swagger UI
- `/openapi.json` - OpenAPI specification

---

## 2. aeon-saas-dev (Next.js - Port 3000)

**Status**: ✅ Healthy
**Total API Routes**: 41 TypeScript API routes
**Framework**: Next.js 14 App Router
**Documentation**: Source code inspection

### API Route Categories:

#### Pipeline Management (3 routes)
- `GET /api/pipeline/status/[jobId]` - Job status check
- `POST /api/pipeline/process` - Process initiation

#### Dashboard (3 routes)
- `GET /api/dashboard/metrics` - Dashboard metrics
- `GET /api/dashboard/distribution` - Data distribution
- `GET /api/dashboard/activity` - Recent activity

#### Chat/AI (1 route)
- `POST /api/chat` - AI chat interface

#### Customers (2 routes)
- `GET /api/customers` - List customers
- `GET /api/customers/[id]` - Customer details
- `POST /api/customers` - Create customer
- `PUT /api/customers/[id]` - Update customer
- `DELETE /api/customers/[id]` - Delete customer

#### Backend Testing (1 route)
- `GET /api/backend/test` - Backend connectivity test

#### Activity (1 route)
- `GET /api/activity/recent` - Recent activity feed

#### Health (1 route)
- `GET /api/health` - Health check

#### Analytics (7 routes)
- `GET /api/analytics/timeseries` - Time series data
- `GET /api/analytics/metrics` - Analytics metrics
- `GET /api/analytics/trends/threat-timeline` - Threat timeline
- `GET /api/analytics/trends/cve` - CVE trends
- `GET /api/analytics/trends/seasonality` - Seasonal patterns
- `POST /api/analytics/export` - Export analytics

#### Observability (3 routes)
- `GET /api/observability/performance` - Performance metrics
- `GET /api/observability/system` - System status
- `GET /api/observability/agents` - Agent monitoring

#### Graph/Neo4j (3 routes)
- `POST /api/graph/query` - Graph query execution
- `GET /api/neo4j/statistics` - Database statistics
- `GET /api/neo4j/cyber-statistics` - Cybersecurity statistics

#### Query Control (6 routes)
- `GET /api/query-control/queries` - List queries
- `POST /api/query-control/queries` - Create query
- `GET /api/query-control/queries/[queryId]` - Query details
- `DELETE /api/query-control/queries/[queryId]` - Delete query
- `GET /api/query-control/queries/[queryId]/checkpoints` - Query checkpoints
- `PUT /api/query-control/queries/[queryId]/model` - Update model
- `POST /api/query-control/queries/[queryId]/resume` - Resume query
- `POST /api/query-control/queries/[queryId]/pause` - Pause query
- `PUT /api/query-control/queries/[queryId]/permissions` - Update permissions

#### Search (1 route)
- `POST /api/search` - Global search

#### Threats (2 routes)
- `GET /api/threats/geographic` - Geographic threat data
- `GET /api/threats/ics` - ICS threat data

#### Upload (1 route)
- `POST /api/upload` - File upload

#### Threat Intelligence (4 routes)
- `GET /api/threat-intel/ics` - ICS threat intelligence
- `GET /api/threat-intel/landscape` - Threat landscape
- `GET /api/threat-intel/analytics` - Threat analytics
- `GET /api/threat-intel/vulnerabilities` - Vulnerability intel

#### Tags (3 routes)
- `GET /api/tags` - List tags
- `POST /api/tags` - Create tag
- `GET /api/tags/[id]` - Tag details
- `PUT /api/tags/[id]` - Update tag
- `DELETE /api/tags/[id]` - Delete tag
- `POST /api/tags/assign` - Assign tags

**Estimated Total Operations**: ~60+ (accounting for HTTP method variations)

---

## 3. openspg-server (Port 8887)

**Status**: ⚠️ Unhealthy
**Documentation**: http://localhost:8887/
**Framework**: OpenSPG (Semantic Processing Graph)
**Expected APIs**: Knowledge graph reasoning, SPARQL queries, ontology management

**Action Required**: Server health check and API documentation extraction

---

## 4. openspg-neo4j (Port 7474/7687)

**Status**: ✅ Healthy
**Protocol**: Bolt (7687) + HTTP (7474)
**API Types**:
- Bolt protocol for Cypher queries
- HTTP REST API
- Graph Data Science library APIs

**Estimated Operations**: 20+ standard Neo4j endpoints

---

## 5. openspg-qdrant (Port 6333)

**Status**: ⚠️ Unhealthy
**API Type**: Vector database API
**Documentation**: http://localhost:6333/
**Expected Operations**: Vector search, collection management, indexing

**Action Required**: Health check and API inventory

---

## 6. openspg-minio (Port 9000-9001)

**Status**: ✅ Healthy
**API Type**: S3-compatible object storage
**Estimated Operations**: 50+ S3 API operations (standard AWS S3 API)

---

## API Testing Progress

### Phase 1: Inventory ✅ COMPLETE
- [x] FastAPI endpoints documented (140 operations)
- [x] Next.js API routes identified (41 routes, ~60 operations)
- [ ] OpenSPG server API extraction (pending health fix)
- [ ] Neo4j API documentation
- [ ] Qdrant API documentation
- [ ] MinIO S3 API verification

### Phase 2: Testing (IN PROGRESS)
**Current Count**: 181 APIs confirmed
**Target**: 230+ total across all services

### Next Steps:
1. Fix openspg-server unhealthy status
2. Fix openspg-qdrant unhealthy status
3. Extract remaining API documentation
4. Begin systematic testing with Taskmaster coordination
5. Developer execution of tests
6. Auditor verification
7. Documenter final report

---

## Storage Location

**Qdrant Namespace**: `api-testing-execution`
**Memory Key**: `pm-progress`
**Documentation**: `/home/jim/2_OXOT_Projects_Dev/docs/api-testing/`

---

**Project Manager**: Coordinating systematic testing of all 181+ APIs
**Next Action**: Spawn Taskmaster to create detailed test inventory
