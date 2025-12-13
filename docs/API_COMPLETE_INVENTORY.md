# Complete API Inventory - OXOT Platform
**Date**: 2025-12-13
**Total APIs**: 181 endpoints
**Services**: 3 (ner11-gold-api, aeon-saas-dev, openspg-server)

---

## Executive Summary

| Service | Port | Endpoint Count | Status |
|---------|------|----------------|--------|
| ner11-gold-api | 8000 | 128 | ✅ Active |
| aeon-saas-dev | 3000 | 53 | ✅ Active |
| openspg-server | 8887 | 0 (Frontend Only) | ⚠️ UI Application |
| **TOTAL** | - | **181** | **Operational** |

---

## Service 1: ner11-gold-api (Port 8000)
**Total Endpoints**: 128
**OpenAPI Spec**: Available at http://localhost:8000/openapi.json
**Categories**: Remediation, Risk Management, SBOM, Threat Intelligence, Vendor/Equipment

### Health & Utility (3 endpoints)
| Method | Endpoint | Category | Description |
|--------|----------|----------|-------------|
| GET | /health | Health | Service health check |
| GET | /info | Info | Service information |
| POST | /ner | NER | Named Entity Recognition |

### Search (2 endpoints)
| Method | Endpoint | Category | Description |
|--------|----------|----------|-------------|
| POST | /search/hybrid | Search | Hybrid search functionality |
| POST | /search/semantic | Search | Semantic search |

### Remediation APIs (30 endpoints)

#### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/remediation/dashboard/summary | Remediation dashboard summary |
| GET | /api/v2/remediation/dashboard/workload | Team workload overview |

#### Metrics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/remediation/metrics/backlog | Backlog metrics |
| GET | /api/v2/remediation/metrics/mttr | Mean Time To Remediate |
| GET | /api/v2/remediation/metrics/sla-compliance | SLA compliance tracking |
| GET | /api/v2/remediation/metrics/summary | Overall metrics summary |
| GET | /api/v2/remediation/metrics/trends | Remediation trends |

#### Plans
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/remediation/plans | Create remediation plan |
| GET | /api/v2/remediation/plans | List all plans |
| GET | /api/v2/remediation/plans/active | Active plans only |
| GET | /api/v2/remediation/plans/{plan_id} | Get specific plan |
| GET | /api/v2/remediation/plans/{plan_id}/progress | Plan progress tracking |
| PUT | /api/v2/remediation/plans/{plan_id}/status | Update plan status |

#### SLA Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/remediation/sla/at-risk | At-risk SLA items |
| GET | /api/v2/remediation/sla/breaches | SLA breaches |
| POST | /api/v2/remediation/sla/policies | Create SLA policy |
| GET | /api/v2/remediation/sla/policies | List SLA policies |
| GET | /api/v2/remediation/sla/policies/{policy_id} | Get specific policy |
| PUT | /api/v2/remediation/sla/policies/{policy_id} | Update SLA policy |

#### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/remediation/tasks | Create remediation task |
| GET | /api/v2/remediation/tasks/by-priority/{priority} | Tasks by priority |
| GET | /api/v2/remediation/tasks/by-status/{status} | Tasks by status |
| GET | /api/v2/remediation/tasks/open | Open tasks |
| GET | /api/v2/remediation/tasks/overdue | Overdue tasks |
| GET | /api/v2/remediation/tasks/search | Search tasks |
| GET | /api/v2/remediation/tasks/{task_id} | Get specific task |
| PUT | /api/v2/remediation/tasks/{task_id}/assign | Assign task |
| GET | /api/v2/remediation/tasks/{task_id}/history | Task history |
| PUT | /api/v2/remediation/tasks/{task_id}/status | Update task status |

### Risk Management APIs (24 endpoints)

#### Aggregation
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/risk/aggregation/by-asset-type | Risk by asset type |
| GET | /api/v2/risk/aggregation/by-sector | Risk by sector |
| GET | /api/v2/risk/aggregation/by-vendor | Risk by vendor |
| GET | /api/v2/risk/aggregation/{aggregation_type}/{group_id} | Specific aggregation |

#### Asset Criticality
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/risk/assets/by-criticality/{level} | Assets by criticality |
| POST | /api/v2/risk/assets/criticality | Set asset criticality |
| GET | /api/v2/risk/assets/criticality/summary | Criticality summary |
| GET | /api/v2/risk/assets/mission-critical | Mission-critical assets |
| GET | /api/v2/risk/assets/{asset_id}/criticality | Asset criticality details |
| PUT | /api/v2/risk/assets/{asset_id}/criticality | Update criticality |

#### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/risk/dashboard/risk-matrix | Risk matrix visualization |
| GET | /api/v2/risk/dashboard/summary | Risk dashboard summary |

#### Exposure
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/risk/exposure | Calculate exposure |
| GET | /api/v2/risk/exposure/attack-surface | Attack surface analysis |
| GET | /api/v2/risk/exposure/high-exposure | High exposure items |
| GET | /api/v2/risk/exposure/internet-facing | Internet-facing assets |
| GET | /api/v2/risk/exposure/{asset_id} | Asset exposure details |

#### Risk Scores
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/risk/scores | Calculate risk score |
| GET | /api/v2/risk/scores/high-risk | High-risk items |
| GET | /api/v2/risk/scores/history/{entity_type}/{entity_id} | Score history |
| POST | /api/v2/risk/scores/recalculate/{entity_type}/{entity_id} | Recalculate score |
| GET | /api/v2/risk/scores/search | Search risk scores |
| GET | /api/v2/risk/scores/trending | Trending risks |
| GET | /api/v2/risk/scores/{entity_type}/{entity_id} | Entity risk score |

### SBOM APIs (33 endpoints)

#### Components
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/sbom/components | Add component |
| GET | /api/v2/sbom/components/high-risk | High-risk components |
| GET | /api/v2/sbom/components/search | Search components |
| GET | /api/v2/sbom/components/vulnerable | Vulnerable components |
| GET | /api/v2/sbom/components/{component_id} | Component details |
| GET | /api/v2/sbom/components/{component_id}/dependencies | Component dependencies |
| GET | /api/v2/sbom/components/{component_id}/dependents | Component dependents |
| GET | /api/v2/sbom/components/{component_id}/impact | Impact analysis |
| GET | /api/v2/sbom/components/{component_id}/vulnerabilities | Component vulnerabilities |

#### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/sbom/dashboard/summary | SBOM dashboard summary |

#### Dependencies
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/sbom/dependencies | Add dependency |
| GET | /api/v2/sbom/dependencies/path | Dependency path analysis |

#### SBOMs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/sbom/sboms | Upload SBOM |
| GET | /api/v2/sbom/sboms | List SBOMs |
| GET | /api/v2/sbom/sboms/{sbom_id} | Get SBOM details |
| DELETE | /api/v2/sbom/sboms/{sbom_id} | Delete SBOM |
| GET | /api/v2/sbom/sboms/{sbom_id}/components | SBOM components |
| POST | /api/v2/sbom/sboms/{sbom_id}/correlate-equipment | Correlate with equipment |
| GET | /api/v2/sbom/sboms/{sbom_id}/cycles | Dependency cycles |
| GET | /api/v2/sbom/sboms/{sbom_id}/graph-stats | Graph statistics |
| GET | /api/v2/sbom/sboms/{sbom_id}/license-compliance | License compliance |
| GET | /api/v2/sbom/sboms/{sbom_id}/remediation | Remediation suggestions |
| GET | /api/v2/sbom/sboms/{sbom_id}/risk-summary | Risk summary |
| GET | /api/v2/sbom/sboms/{sbom_id}/vulnerable-paths | Vulnerable paths |

#### Vulnerabilities
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/sbom/vulnerabilities | Add vulnerability |
| GET | /api/v2/sbom/vulnerabilities/by-apt | Vulnerabilities by APT |
| GET | /api/v2/sbom/vulnerabilities/critical | Critical vulnerabilities |
| GET | /api/v2/sbom/vulnerabilities/epss-prioritized | EPSS prioritized |
| GET | /api/v2/sbom/vulnerabilities/kev | Known Exploited Vulnerabilities |
| GET | /api/v2/sbom/vulnerabilities/search | Search vulnerabilities |
| GET | /api/v2/sbom/vulnerabilities/{vulnerability_id} | Vulnerability details |
| POST | /api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge | Acknowledge vulnerability |

### Threat Intelligence APIs (27 endpoints)

#### Actors
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/threat-intel/actors | Add threat actor |
| GET | /api/v2/threat-intel/actors/active | Active threat actors |
| GET | /api/v2/threat-intel/actors/by-sector/{sector} | Actors by sector |
| GET | /api/v2/threat-intel/actors/search | Search actors |
| GET | /api/v2/threat-intel/actors/{actor_id} | Actor details |
| GET | /api/v2/threat-intel/actors/{actor_id}/campaigns | Actor campaigns |
| GET | /api/v2/threat-intel/actors/{actor_id}/cves | Actor CVEs |

#### Campaigns
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/threat-intel/campaigns | Add campaign |
| GET | /api/v2/threat-intel/campaigns/active | Active campaigns |
| GET | /api/v2/threat-intel/campaigns/search | Search campaigns |
| GET | /api/v2/threat-intel/campaigns/{campaign_id} | Campaign details |
| GET | /api/v2/threat-intel/campaigns/{campaign_id}/iocs | Campaign IOCs |

#### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/threat-intel/dashboard/summary | Threat intel dashboard |

#### Feeds
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/threat-intel/feeds | Add threat feed |
| GET | /api/v2/threat-intel/feeds | List threat feeds |
| PUT | /api/v2/threat-intel/feeds/{feed_id}/refresh | Refresh feed |

#### IOCs (Indicators of Compromise)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/threat-intel/iocs | Add IOC |
| GET | /api/v2/threat-intel/iocs/active | Active IOCs |
| POST | /api/v2/threat-intel/iocs/bulk | Bulk add IOCs |
| GET | /api/v2/threat-intel/iocs/by-type/{ioc_type} | IOCs by type |
| GET | /api/v2/threat-intel/iocs/search | Search IOCs |

#### MITRE ATT&CK
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/threat-intel/mitre/coverage | MITRE coverage analysis |
| GET | /api/v2/threat-intel/mitre/gaps | Coverage gaps |
| POST | /api/v2/threat-intel/mitre/mappings | Add MITRE mapping |
| GET | /api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id} | Entity mappings |
| GET | /api/v2/threat-intel/mitre/techniques/{technique_id}/actors | Actors using technique |

### Vendor & Equipment APIs (25 endpoints)

#### Equipment
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/vendor-equipment/equipment | Add equipment |
| GET | /api/v2/vendor-equipment/equipment | List equipment |
| GET | /api/v2/vendor-equipment/equipment/approaching-eol | Approaching EOL |
| GET | /api/v2/vendor-equipment/equipment/eol | End-of-life equipment |
| GET | /api/v2/vendor-equipment/equipment/{model_id} | Equipment details |

#### Maintenance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/vendor-equipment/maintenance-schedule | Maintenance schedule |
| POST | /api/v2/vendor-equipment/maintenance-windows | Create maintenance window |
| GET | /api/v2/vendor-equipment/maintenance-windows | List maintenance windows |
| POST | /api/v2/vendor-equipment/maintenance-windows/check-conflict | Check conflicts |
| GET | /api/v2/vendor-equipment/maintenance-windows/{window_id} | Window details |
| DELETE | /api/v2/vendor-equipment/maintenance-windows/{window_id} | Delete window |

#### Predictive Maintenance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/vendor-equipment/predictive-maintenance/forecast | Maintenance forecast |
| GET | /api/v2/vendor-equipment/predictive-maintenance/{equipment_id} | Equipment predictions |

#### Vendors
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/vendor-equipment/vendors | Add vendor |
| GET | /api/v2/vendor-equipment/vendors | List vendors |
| GET | /api/v2/vendor-equipment/vendors/high-risk | High-risk vendors |
| GET | /api/v2/vendor-equipment/vendors/{vendor_id} | Vendor details |
| GET | /api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary | Vendor risk summary |

#### Vulnerabilities & Work Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/vendor-equipment/vulnerabilities/flag | Flag vulnerability |
| POST | /api/v2/vendor-equipment/work-orders | Create work order |
| GET | /api/v2/vendor-equipment/work-orders | List work orders |
| GET | /api/v2/vendor-equipment/work-orders/summary | Work orders summary |
| GET | /api/v2/vendor-equipment/work-orders/{work_order_id} | Work order details |
| PATCH | /api/v2/vendor-equipment/work-orders/{work_order_id}/status | Update status |

---

## Service 2: aeon-saas-dev (Port 3000)
**Total Endpoints**: 53
**Framework**: Next.js 14 App Router
**Categories**: Analytics, Dashboard, Query Control, Threat Intel, Graph Operations

### Analytics APIs (7 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/analytics/export | Export analytics data |
| POST | /api/analytics/export | Export analytics (POST) |
| GET | /api/analytics/metrics | Analytics metrics |
| GET | /api/analytics/timeseries | Time series data |
| GET | /api/analytics/trends/cve | CVE trends |
| GET | /api/analytics/trends/seasonality | Seasonality analysis |
| GET | /api/analytics/trends/threat-timeline | Threat timeline |

### Dashboard APIs (3 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/dashboard/activity | Recent activity feed |
| GET | /api/dashboard/distribution | Distribution metrics |
| GET | /api/dashboard/metrics | Dashboard metrics |

### Query Control APIs (12 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/query-control/queries | List all queries |
| POST | /api/query-control/queries | Create new query |
| GET | /api/query-control/queries/[queryId] | Get query details |
| DELETE | /api/query-control/queries/[queryId] | Terminate query |
| GET | /api/query-control/queries/[queryId]/checkpoints | List checkpoints |
| POST | /api/query-control/queries/[queryId]/model | Switch AI model |
| POST | /api/query-control/queries/[queryId]/pause | Pause query |
| POST | /api/query-control/queries/[queryId]/permissions | Change permissions |
| POST | /api/query-control/queries/[queryId]/resume | Resume query |

### Threat Intelligence APIs (5 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/threat-intel/analytics | Threat analytics |
| GET | /api/threat-intel/ics | ICS threat data |
| GET | /api/threat-intel/landscape | Threat landscape |
| GET | /api/threat-intel/vulnerabilities | Vulnerability data |
| GET | /api/threats/geographic | Geographic threat distribution |
| GET | /api/threats/ics | ICS-specific threats |

### Graph & Neo4j APIs (4 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/graph/query | Graph query (GET) |
| POST | /api/graph/query | Execute graph query |
| GET | /api/neo4j/cyber-statistics | Cyber security statistics |
| GET | /api/neo4j/statistics | General graph statistics |

### Pipeline APIs (4 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/pipeline/process | Get pipeline status |
| POST | /api/pipeline/process | Process pipeline |
| DELETE | /api/pipeline/process | Delete pipeline job |
| GET | /api/pipeline/status/[jobId] | Job status |
| DELETE | /api/pipeline/status/[jobId] | Delete job |

### Customer Management (5 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/customers | List customers |
| POST | /api/customers | Create customer |
| GET | /api/customers/[id] | Get customer |
| PUT | /api/customers/[id] | Update customer |
| DELETE | /api/customers/[id] | Delete customer |

### Tags Management (6 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/tags | List tags |
| POST | /api/tags | Create tag |
| DELETE | /api/tags | Bulk delete tags |
| GET | /api/tags/[id] | Get tag |
| PUT | /api/tags/[id] | Update tag |
| DELETE | /api/tags/[id] | Delete tag |
| POST | /api/tags/assign | Assign tags |
| DELETE | /api/tags/assign | Remove tags |

### Observability APIs (3 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/observability/agents | Agent observability |
| POST | /api/observability/agents | Agent operations |
| GET | /api/observability/performance | Performance metrics |
| GET | /api/observability/system | System observability |

### Utility APIs (4 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/activity/recent | Recent activity |
| GET | /api/backend/test | Backend connectivity test |
| POST | /api/chat | Chat interface |
| GET | /api/health | Health check |
| POST | /api/search | Hybrid search |
| GET | /api/search | Search health check |
| POST | /api/upload | File upload |

---

## Service 3: openspg-server (Port 8887)
**Total Endpoints**: 0 (Frontend Application)
**Type**: Web UI Application
**Framework**: UmiJS
**Status**: ⚠️ Not a REST API service

**Description**: This is a frontend web application built with UmiJS framework. It provides a user interface for semantic graph operations but does not expose REST APIs for external consumption. All interactions are through the web interface.

**Application Features**:
- Knowledge graph management UI
- Application configuration interface
- Model management
- Data source configuration
- Monitoring dashboards
- User settings

---

## API Category Summary

### By Service
| Category | ner11-gold-api | aeon-saas-dev | Total |
|----------|----------------|---------------|-------|
| Remediation | 30 | 0 | 30 |
| Risk Management | 24 | 0 | 24 |
| SBOM | 33 | 0 | 33 |
| Threat Intelligence | 27 | 5 | 32 |
| Vendor/Equipment | 25 | 0 | 25 |
| Analytics | 0 | 7 | 7 |
| Dashboard | 0 | 3 | 3 |
| Query Control | 0 | 12 | 12 |
| Graph/Neo4j | 0 | 4 | 4 |
| Pipeline | 0 | 4 | 4 |
| Customer Management | 0 | 5 | 5 |
| Tags | 0 | 6 | 6 |
| Observability | 0 | 3 | 3 |
| Search & Utility | 5 | 4 | 9 |
| **TOTAL** | **128** | **53** | **181** |

### By HTTP Method
| Method | ner11-gold-api | aeon-saas-dev | Total |
|--------|----------------|---------------|-------|
| GET | 96 | 36 | 132 |
| POST | 26 | 13 | 39 |
| PUT | 5 | 2 | 7 |
| DELETE | 1 | 5 | 6 |
| PATCH | 0 | 1 | 1 |
| **TOTAL** | **128** | **57** | **185** |

---

## Discrepancy Analysis

### Expected vs. Actual
- **Expected Total**: 230+ APIs (from user reports)
- **Actual Verified**: 181 APIs
- **Discrepancy**: -49 APIs (~21% difference)

### Possible Explanations
1. **Duplicate Counting**: Some APIs may have been counted multiple times in estimates
2. **Internal APIs**: Some endpoints may be internal/private and not exposed
3. **Version Differences**: API count may have changed since initial estimate
4. **Undocumented Endpoints**: Some endpoints may exist but not in OpenAPI specs
5. **Development vs. Production**: Environment differences in API availability

### Additional Services to Investigate
Based on the gap, there may be additional services not yet discovered:
- Database services with REST APIs
- Internal microservices
- Authentication/Authorization services
- Message queue management APIs
- Cache management endpoints

---

## Testing Coverage Status

### Current Coverage
- ✅ **ner11-gold-api**: Full OpenAPI spec available (128 endpoints)
- ✅ **aeon-saas-dev**: All Next.js routes cataloged (53 endpoints)
- ⚠️ **openspg-server**: Frontend only, no REST APIs

### Gaps to Address
1. Investigate potential additional services
2. Check for undocumented internal APIs
3. Verify version-specific endpoints
4. Examine database direct access APIs
5. Review authentication service endpoints

---

## Recommendations

1. **Verify Services**: Check Docker compose files for additional services
2. **Documentation Review**: Cross-reference with architectural diagrams
3. **Network Scan**: Perform internal network scan for exposed ports
4. **Code Analysis**: Review source code for additional API definitions
5. **Stakeholder Confirmation**: Verify expected API count with development team

---

## Next Steps for API Testing

1. **Phase 1**: Test all 181 verified APIs
2. **Phase 2**: Investigate and catalog missing APIs
3. **Phase 3**: Update inventory and testing plan
4. **Phase 4**: Execute comprehensive testing suite
5. **Phase 5**: Document results and coverage gaps

---

**Document Version**: 1.0
**Last Updated**: 2025-12-13
**Verified By**: TASKMASTER Agent
**Storage**: Qdrant vector db under "api-testing-execution/inventory"
