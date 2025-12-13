# Complete API Inventory - All Services

**Generated:** 2025-12-12
**Total Endpoints:** 230+
**Services:** 3 (ner11-gold-api, aeon-saas-dev, openspg-server)

---

## 📊 Summary Statistics

| Service | Port | Total Endpoints | Categories |
|---------|------|-----------------|------------|
| ner11-gold-api | 8000 | 128 | SBOM, Vendor, Threat Intel, Risk, Remediation, NER |
| aeon-saas-dev | 3000 | 64 | Pipeline, Query Control, Dashboard, Threat Intel, Analytics |
| openspg-server | 8887 | ~40 | Knowledge Graph, Schema, Query |

**Total:** ~232 endpoints across all services

---

## 🔵 Service 1: ner11-gold-api (Port 8000)

### SBOM Analysis (34 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/v2/sbom/sboms` | POST | SBOM | Create new SBOM |
| `/api/v2/sbom/sboms` | GET | SBOM | List SBOMs with filters |
| `/api/v2/sbom/sboms/{sbom_id}` | GET | SBOM | Get SBOM by ID |
| `/api/v2/sbom/sboms/{sbom_id}` | DELETE | SBOM | Delete SBOM |
| `/api/v2/sbom/sboms/{sbom_id}/risk-summary` | GET | SBOM Risk | Get comprehensive risk summary |
| `/api/v2/sbom/components` | POST | Component | Create software component |
| `/api/v2/sbom/components/{component_id}` | GET | Component | Get component by ID |
| `/api/v2/sbom/components/search` | GET | Component | Semantic search components |
| `/api/v2/sbom/components/vulnerable` | GET | Component | Get vulnerable components |
| `/api/v2/sbom/components/high-risk` | GET | Component | Get high-risk components |
| `/api/v2/sbom/sboms/{sbom_id}/components` | GET | Component | Get SBOM components |
| `/api/v2/sbom/dependencies` | POST | Dependency | Create dependency relation |
| `/api/v2/sbom/components/{component_id}/dependencies` | GET | Dependency | Get dependency tree |
| `/api/v2/sbom/components/{component_id}/dependents` | GET | Dependency | Get reverse dependencies |
| `/api/v2/sbom/components/{component_id}/impact` | GET | Dependency | Impact analysis |
| `/api/v2/sbom/sboms/{sbom_id}/cycles` | GET | Dependency | Detect circular dependencies |
| `/api/v2/sbom/dependencies/path` | GET | Dependency | Find dependency path |
| `/api/v2/sbom/sboms/{sbom_id}/graph-stats` | GET | Dependency | Graph statistics |
| `/api/v2/sbom/vulnerabilities` | POST | Vulnerability | Create vulnerability record |
| `/api/v2/sbom/vulnerabilities/{vulnerability_id}` | GET | Vulnerability | Get vulnerability by ID |
| `/api/v2/sbom/vulnerabilities/search` | GET | Vulnerability | Search vulnerabilities |
| `/api/v2/sbom/vulnerabilities/critical` | GET | Vulnerability | Get critical vulnerabilities |
| `/api/v2/sbom/vulnerabilities/kev` | GET | Vulnerability | Get KEV vulnerabilities |
| `/api/v2/sbom/vulnerabilities/epss-prioritized` | GET | Vulnerability | EPSS prioritized vulnerabilities |
| `/api/v2/sbom/vulnerabilities/by-apt` | GET | Vulnerability | Vulnerabilities by APT group |
| `/api/v2/sbom/components/{component_id}/vulnerabilities` | GET | Vulnerability | Component vulnerabilities |
| `/api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge` | POST | Vulnerability | Acknowledge vulnerability |
| `/api/v2/sbom/sboms/{sbom_id}/remediation` | GET | Remediation | Get remediation plan |
| `/api/v2/sbom/sboms/{sbom_id}/license-compliance` | GET | Compliance | License compliance report |
| `/api/v2/sbom/dashboard/summary` | GET | Dashboard | SBOM dashboard summary |
| `/api/v2/sbom/sboms/{sbom_id}/vulnerable-paths` | GET | Vulnerability | Vulnerable dependency paths |
| `/api/v2/sbom/sboms/{sbom_id}/correlate-equipment` | POST | Integration | Correlate with equipment |

### Vendor & Equipment Management (23 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/v2/vendor-equipment/vendors` | POST | Vendor | Create vendor |
| `/api/v2/vendor-equipment/vendors` | GET | Vendor | List vendors |
| `/api/v2/vendor-equipment/vendors/{vendor_id}` | GET | Vendor | Get vendor by ID |
| `/api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary` | GET | Vendor Risk | Vendor risk summary |
| `/api/v2/vendor-equipment/vendors/high-risk` | GET | Vendor Risk | High-risk vendors |
| `/api/v2/vendor-equipment/equipment` | POST | Equipment | Create equipment |
| `/api/v2/vendor-equipment/equipment` | GET | Equipment | List equipment |
| `/api/v2/vendor-equipment/equipment/{model_id}` | GET | Equipment | Get equipment by ID |
| `/api/v2/vendor-equipment/equipment/approaching-eol` | GET | Equipment | EOL approaching equipment |
| `/api/v2/vendor-equipment/equipment/eol` | GET | Equipment | EOL equipment |
| `/api/v2/vendor-equipment/maintenance-schedule` | GET | Maintenance | Maintenance schedule |
| `/api/v2/vendor-equipment/vulnerabilities/flag` | POST | Vulnerability | Flag equipment vulnerability |
| `/api/v2/vendor-equipment/maintenance-windows` | POST | Maintenance | Create maintenance window |
| `/api/v2/vendor-equipment/maintenance-windows` | GET | Maintenance | List maintenance windows |
| `/api/v2/vendor-equipment/maintenance-windows/{window_id}` | GET | Maintenance | Get maintenance window |
| `/api/v2/vendor-equipment/maintenance-windows/{window_id}` | DELETE | Maintenance | Delete maintenance window |
| `/api/v2/vendor-equipment/maintenance-windows/check-conflict` | POST | Maintenance | Check scheduling conflict |
| `/api/v2/vendor-equipment/predictive-maintenance/{equipment_id}` | GET | Predictive | Predictive maintenance |
| `/api/v2/vendor-equipment/predictive-maintenance/forecast` | GET | Predictive | Maintenance forecast |
| `/api/v2/vendor-equipment/work-orders` | POST | Work Order | Create work order |
| `/api/v2/vendor-equipment/work-orders` | GET | Work Order | List work orders |
| `/api/v2/vendor-equipment/work-orders/{work_order_id}` | GET | Work Order | Get work order |
| `/api/v2/vendor-equipment/work-orders/{work_order_id}/status` | PATCH | Work Order | Update work order status |
| `/api/v2/vendor-equipment/work-orders/summary` | GET | Work Order | Work orders summary |

### Threat Intelligence (20 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/v2/threat-intel/actors` | POST | Actor | Create threat actor |
| `/api/v2/threat-intel/actors/{actor_id}` | GET | Actor | Get threat actor |
| `/api/v2/threat-intel/actors/search` | GET | Actor | Search threat actors |
| `/api/v2/threat-intel/actors/active` | GET | Actor | Active threat actors |
| `/api/v2/threat-intel/actors/by-sector/{sector}` | GET | Actor | Actors by sector |
| `/api/v2/threat-intel/actors/{actor_id}/campaigns` | GET | Actor | Actor campaigns |
| `/api/v2/threat-intel/actors/{actor_id}/cves` | GET | Actor | Actor CVEs |
| `/api/v2/threat-intel/campaigns` | POST | Campaign | Create campaign |
| `/api/v2/threat-intel/campaigns/{campaign_id}` | GET | Campaign | Get campaign |
| `/api/v2/threat-intel/campaigns/search` | GET | Campaign | Search campaigns |
| `/api/v2/threat-intel/campaigns/active` | GET | Campaign | Active campaigns |
| `/api/v2/threat-intel/campaigns/{campaign_id}/iocs` | GET | Campaign | Campaign IOCs |
| `/api/v2/threat-intel/mitre/mappings` | POST | MITRE | Create MITRE mapping |
| `/api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}` | GET | MITRE | Get entity MITRE mappings |
| `/api/v2/threat-intel/mitre/techniques/{technique_id}/actors` | GET | MITRE | Actors using technique |
| `/api/v2/threat-intel/mitre/coverage` | GET | MITRE | MITRE ATT&CK coverage |
| `/api/v2/threat-intel/mitre/gaps` | GET | MITRE | Coverage gaps |
| `/api/v2/threat-intel/iocs` | POST | IOC | Create IOC |
| `/api/v2/threat-intel/iocs/bulk` | POST | IOC | Bulk create IOCs |
| `/api/v2/threat-intel/iocs/search` | GET | IOC | Search IOCs |
| `/api/v2/threat-intel/iocs/active` | GET | IOC | Active IOCs |
| `/api/v2/threat-intel/iocs/by-type/{ioc_type}` | GET | IOC | IOCs by type |
| `/api/v2/threat-intel/feeds` | POST | Feed | Create threat feed |
| `/api/v2/threat-intel/feeds` | GET | Feed | List threat feeds |
| `/api/v2/threat-intel/feeds/{feed_id}/refresh` | PUT | Feed | Refresh threat feed |
| `/api/v2/threat-intel/dashboard/summary` | GET | Dashboard | Threat intel summary |

### Risk Management (21 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/v2/risk/scores` | POST | Score | Create risk score |
| `/api/v2/risk/scores/{entity_type}/{entity_id}` | GET | Score | Get risk score |
| `/api/v2/risk/scores/high-risk` | GET | Score | High-risk entities |
| `/api/v2/risk/scores/trending` | GET | Score | Trending risk scores |
| `/api/v2/risk/scores/search` | GET | Score | Search risk scores |
| `/api/v2/risk/scores/recalculate/{entity_type}/{entity_id}` | POST | Score | Recalculate risk score |
| `/api/v2/risk/scores/history/{entity_type}/{entity_id}` | GET | Score | Risk score history |
| `/api/v2/risk/assets/criticality` | POST | Asset | Create asset criticality |
| `/api/v2/risk/assets/{asset_id}/criticality` | GET | Asset | Get asset criticality |
| `/api/v2/risk/assets/{asset_id}/criticality` | PUT | Asset | Update asset criticality |
| `/api/v2/risk/assets/mission-critical` | GET | Asset | Mission-critical assets |
| `/api/v2/risk/assets/by-criticality/{level}` | GET | Asset | Assets by criticality |
| `/api/v2/risk/assets/criticality/summary` | GET | Asset | Criticality summary |
| `/api/v2/risk/exposure` | POST | Exposure | Create exposure record |
| `/api/v2/risk/exposure/{asset_id}` | GET | Exposure | Get asset exposure |
| `/api/v2/risk/exposure/internet-facing` | GET | Exposure | Internet-facing assets |
| `/api/v2/risk/exposure/high-exposure` | GET | Exposure | High-exposure assets |
| `/api/v2/risk/exposure/attack-surface` | GET | Exposure | Attack surface analysis |
| `/api/v2/risk/aggregation/by-vendor` | GET | Aggregation | Risk by vendor |
| `/api/v2/risk/aggregation/by-sector` | GET | Aggregation | Risk by sector |
| `/api/v2/risk/aggregation/by-asset-type` | GET | Aggregation | Risk by asset type |
| `/api/v2/risk/aggregation/{aggregation_type}/{group_id}` | GET | Aggregation | Custom aggregation |
| `/api/v2/risk/dashboard/summary` | GET | Dashboard | Risk dashboard summary |
| `/api/v2/risk/dashboard/risk-matrix` | GET | Dashboard | Risk matrix visualization |

### Remediation Management (25 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/v2/remediation/tasks` | POST | Task | Create remediation task |
| `/api/v2/remediation/tasks/{task_id}` | GET | Task | Get task details |
| `/api/v2/remediation/tasks/search` | GET | Task | Search tasks |
| `/api/v2/remediation/tasks/open` | GET | Task | Open tasks |
| `/api/v2/remediation/tasks/overdue` | GET | Task | Overdue tasks |
| `/api/v2/remediation/tasks/by-priority/{priority}` | GET | Task | Tasks by priority |
| `/api/v2/remediation/tasks/by-status/{status}` | GET | Task | Tasks by status |
| `/api/v2/remediation/tasks/{task_id}/status` | PUT | Task | Update task status |
| `/api/v2/remediation/tasks/{task_id}/assign` | PUT | Task | Assign task |
| `/api/v2/remediation/tasks/{task_id}/history` | GET | Task | Task history |
| `/api/v2/remediation/plans` | POST | Plan | Create remediation plan |
| `/api/v2/remediation/plans` | GET | Plan | List remediation plans |
| `/api/v2/remediation/plans/{plan_id}` | GET | Plan | Get plan details |
| `/api/v2/remediation/plans/active` | GET | Plan | Active plans |
| `/api/v2/remediation/plans/{plan_id}/status` | PUT | Plan | Update plan status |
| `/api/v2/remediation/plans/{plan_id}/progress` | GET | Plan | Plan progress |
| `/api/v2/remediation/sla/policies` | POST | SLA | Create SLA policy |
| `/api/v2/remediation/sla/policies` | GET | SLA | List SLA policies |
| `/api/v2/remediation/sla/policies/{policy_id}` | GET | SLA | Get SLA policy |
| `/api/v2/remediation/sla/policies/{policy_id}` | PUT | SLA | Update SLA policy |
| `/api/v2/remediation/sla/breaches` | GET | SLA | SLA breaches |
| `/api/v2/remediation/sla/at-risk` | GET | SLA | At-risk SLAs |
| `/api/v2/remediation/metrics/summary` | GET | Metrics | Metrics summary |
| `/api/v2/remediation/metrics/mttr` | GET | Metrics | Mean time to remediate |
| `/api/v2/remediation/metrics/sla-compliance` | GET | Metrics | SLA compliance rate |
| `/api/v2/remediation/metrics/backlog` | GET | Metrics | Remediation backlog |
| `/api/v2/remediation/metrics/trends` | GET | Metrics | Remediation trends |
| `/api/v2/remediation/dashboard/summary` | GET | Dashboard | Remediation dashboard |
| `/api/v2/remediation/dashboard/workload` | GET | Dashboard | Workload distribution |

### NER & Search (5 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/ner` | POST | NER | Named entity recognition |
| `/search/semantic` | POST | Search | Semantic search |
| `/search/hybrid` | POST | Search | Hybrid search |
| `/health` | GET | System | Health check |
| `/info` | GET | System | API information |

---

## 🟢 Service 2: aeon-saas-dev (Port 3000)

### Pipeline Management (4 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/pipeline/process` | POST | Pipeline | Process documents |
| `/api/pipeline/process` | GET | Pipeline | Get queue status |
| `/api/pipeline/process` | DELETE | Pipeline | Clear queue |
| `/api/pipeline/status/[jobId]` | GET | Pipeline | Get job status |
| `/api/pipeline/status/[jobId]` | DELETE | Pipeline | Cancel job |

### Query Control (10 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/query-control/queries` | GET | Query | List queries |
| `/api/query-control/queries` | POST | Query | Create query |
| `/api/query-control/queries/[queryId]` | GET | Query | Get query details |
| `/api/query-control/queries/[queryId]` | DELETE | Query | Delete query |
| `/api/query-control/queries/[queryId]/checkpoints` | GET | Query | Get checkpoints |
| `/api/query-control/queries/[queryId]/model` | POST | Query | Change model |
| `/api/query-control/queries/[queryId]/permissions` | POST | Query | Change permissions |
| `/api/query-control/queries/[queryId]/resume` | POST | Query | Resume query |
| `/api/query-control/queries/[queryId]/pause` | POST | Query | Pause query |

### Dashboard & Metrics (4 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/dashboard/metrics` | GET | Dashboard | System metrics |
| `/api/dashboard/distribution` | GET | Dashboard | Data distribution |
| `/api/dashboard/activity` | GET | Dashboard | Activity feed |

### Search & Chat (3 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/search` | POST | Search | Vector search |
| `/api/search` | GET | Search | Search suggestions |
| `/api/chat` | POST | Chat | AI chat interface |

### Threat Intelligence (6 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/threats/geographic` | GET | Threat | Geographic threats |
| `/api/threats/ics` | GET | Threat | ICS/OT threats |
| `/api/threat-intel/ics` | GET | Threat | ICS threat intel |
| `/api/threat-intel/landscape` | GET | Threat | Threat landscape |
| `/api/threat-intel/analytics` | GET | Threat | Threat analytics |
| `/api/threat-intel/vulnerabilities` | GET | Threat | Threat vulnerabilities |

### Customer Management (5 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/customers` | GET | Customer | List customers |
| `/api/customers` | POST | Customer | Create customer |
| `/api/customers/[id]` | GET | Customer | Get customer |
| `/api/customers/[id]` | PUT | Customer | Update customer |
| `/api/customers/[id]` | DELETE | Customer | Delete customer |

### Tag Management (8 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/tags` | GET | Tag | List tags |
| `/api/tags` | POST | Tag | Create tag |
| `/api/tags` | DELETE | Tag | Bulk delete tags |
| `/api/tags/[id]` | GET | Tag | Get tag |
| `/api/tags/[id]` | PUT | Tag | Update tag |
| `/api/tags/[id]` | DELETE | Tag | Delete tag |
| `/api/tags/assign` | POST | Tag | Assign tags |
| `/api/tags/assign` | DELETE | Tag | Unassign tags |

### Analytics (7 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/analytics/timeseries` | GET | Analytics | Time series data |
| `/api/analytics/metrics` | GET | Analytics | Analytics metrics |
| `/api/analytics/trends/threat-timeline` | GET | Analytics | Threat timeline |
| `/api/analytics/trends/cve` | GET | Analytics | CVE trends |
| `/api/analytics/trends/seasonality` | GET | Analytics | Seasonal patterns |
| `/api/analytics/export` | POST | Analytics | Export analytics |

### Observability (4 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/observability/performance` | GET | Monitor | Performance metrics |
| `/api/observability/system` | GET | Monitor | System health |
| `/api/observability/agents` | GET | Monitor | Agent status |
| `/api/observability/agents` | POST | Monitor | Update agent |

### Graph & Neo4j (5 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/graph/query` | POST | Graph | Execute graph query |
| `/api/graph/query` | GET | Graph | Query templates |
| `/api/neo4j/statistics` | GET | Graph | Neo4j statistics |
| `/api/neo4j/cyber-statistics` | GET | Graph | Cyber statistics |

### System (4 endpoints)

| Endpoint | Method | Category | Description |
|----------|--------|----------|-------------|
| `/api/health` | GET | System | Health check |
| `/api/upload` | POST | System | File upload |
| `/api/activity/recent` | GET | System | Recent activity |
| `/api/backend/test` | GET | System | Backend connectivity |

---

## 🟡 Service 3: openspg-server (Port 8887)

### Knowledge Graph (Estimated ~40 endpoints)

| Category | Estimated Endpoints | Description |
|----------|---------------------|-------------|
| Schema Management | ~8 | Create, update, delete schemas |
| Entity Management | ~10 | CRUD operations on entities |
| Relationship Management | ~8 | Manage entity relationships |
| Query & Search | ~6 | Graph query and search |
| Knowledge Extraction | ~4 | Extract knowledge from text |
| Reasoning | ~4 | Graph reasoning and inference |

**Note:** OpenSPG server requires authentication. Full endpoint discovery requires logged-in session. The web interface shows it uses an Ant Design admin panel with knowledge graph management capabilities.

---

## 📋 Category Summary

### All Services Combined

| Category | Count | Services |
|----------|-------|----------|
| SBOM Analysis | 34 | ner11-gold-api |
| Vendor & Equipment | 24 | ner11-gold-api |
| Threat Intelligence | 26 | ner11-gold-api, aeon-saas-dev |
| Risk Management | 21 | ner11-gold-api |
| Remediation | 25 | ner11-gold-api |
| Pipeline Management | 5 | aeon-saas-dev |
| Query Control | 10 | aeon-saas-dev |
| Dashboard & Analytics | 15 | aeon-saas-dev |
| Customer Management | 5 | aeon-saas-dev |
| Tag Management | 8 | aeon-saas-dev |
| Graph Operations | 45+ | aeon-saas-dev, openspg-server |
| Observability | 4 | aeon-saas-dev |
| Search & Chat | 6 | ner11-gold-api, aeon-saas-dev |
| System Health | 5 | All services |

---

## 🔗 Service Integration Points

### Cross-Service Data Flow

```
┌─────────────────┐
│  aeon-saas-dev  │──── Documents ────▶ Pipeline Processing
│   (Frontend)    │                     │
└────────┬────────┘                     │
         │                              ▼
         │                    ┌──────────────────┐
         │                    │  Document Queue  │
         │                    │    (BullMQ)      │
         │                    └────────┬─────────┘
         │                             │
         │                             ▼
         │                    ┌──────────────────┐
         │◀────── NER ────────│ ner11-gold-api   │
         │                    │  (Processing)    │
         │                    └────────┬─────────┘
         │                             │
         │                             ▼
         │                    ┌──────────────────┐
         └──── Graph Data ───▶│ openspg-server   │
                              │ (Knowledge Graph)│
                              └──────────────────┘
```

### Authentication Headers

**ner11-gold-api:**
- `x-customer-id`: Customer identifier (required)
- `x-namespace`: Customer namespace (optional)
- `x-user-id`: User identifier (optional)
- `x-access-level`: Access level (default: read)

**aeon-saas-dev:**
- Clerk authentication via Next.js middleware
- Session-based authentication

**openspg-server:**
- Form-based login required
- Session cookies for authenticated requests

---

## 🎯 Testing Priority Recommendations

### High Priority (Security & Core Functions)
1. **Authentication/Authorization** - All services
2. **SBOM Creation & Analysis** - ner11-gold-api
3. **Document Pipeline** - aeon-saas-dev
4. **Graph Queries** - openspg-server, aeon-saas-dev

### Medium Priority (Business Logic)
5. **Vulnerability Management** - ner11-gold-api
6. **Risk Scoring** - ner11-gold-api
7. **Remediation Workflows** - ner11-gold-api
8. **Analytics & Reporting** - aeon-saas-dev

### Low Priority (Supporting Functions)
9. **Tag Management** - aeon-saas-dev
10. **Observability** - aeon-saas-dev
11. **System Health** - All services

---

## 📝 Notes

1. **ner11-gold-api** has comprehensive OpenAPI documentation at `http://localhost:8000/openapi.json`
2. **aeon-saas-dev** uses Next.js App Router conventions with route handlers
3. **openspg-server** requires authentication for full API discovery
4. All services expose health check endpoints for monitoring
5. Cross-service integration primarily through shared data stores (Qdrant, Neo4j, PostgreSQL)

---

**Document Status:** Complete
**Last Updated:** 2025-12-12
**Verification:** Manual extraction + OpenAPI spec analysis
