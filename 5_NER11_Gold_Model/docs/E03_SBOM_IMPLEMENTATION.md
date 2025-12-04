# E03: SBOM Dependency & Vulnerability Tracking

## Implementation Documentation

**Version**: 1.5.0
**Status**: IN PROGRESS (Days 1-6 Complete)
**Start Date**: 2025-12-04
**Estimated Duration**: 12 days

---

## Overview

E03 SBOM (Software Bill of Materials) Dependency & Vulnerability Tracking provides comprehensive software component analysis, dependency graph management, and vulnerability correlation for the NER11 Gold Model.

### Business Value

- **Software Visibility**: Complete inventory of software components in operational systems
- **Vulnerability Management**: CVE tracking with CVSS and EPSS scoring
- **License Compliance**: Risk-based license analysis and policy enforcement
- **Dependency Analysis**: Direct and transitive dependency graph visualization
- **APT Linkage**: Connection to threat actor groups using vulnerabilities

---

## Architecture

### Entity Model

```
                    ┌─────────────────┐
                    │      SBOM       │
                    │ (Bill of Mat.)  │
                    └────────┬────────┘
                             │ contains
                             ▼
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ Equipment   │◄───►│   Software      │◄───►│ Software         │
│ Model (E15) │     │   Component     │     │ Vulnerability    │
└─────────────┘     └────────┬────────┘     └──────────────────┘
                             │ depends_on                │
                             ▼                           │
                    ┌─────────────────┐                  │
                    │  Dependency     │                  │
                    │  Relation       │◄─────────────────┘
                    └─────────────────┘         affects
```

### Data Models

| Model | Purpose | Qdrant Collection |
|-------|---------|-------------------|
| `SoftwareComponent` | Individual package with purl/cpe | `ner11_sbom` |
| `SBOM` | Bill of materials document | `ner11_sbom` |
| `SoftwareVulnerability` | CVE with CVSS/EPSS | `ner11_sbom` |
| `DependencyRelation` | Component relationships | `ner11_sbom` |
| `LicenseComplianceResult` | License analysis | `ner11_sbom` |

---

## Implementation Status

### Day 1: Core Models ✅ COMPLETE

**Files Created**:
- `api/sbom_analysis/__init__.py` - Module exports
- `api/sbom_analysis/sbom_models.py` - Core data models

**Enums Implemented**:
| Enum | Values | Purpose |
|------|--------|---------|
| `SBOMFormat` | CYCLONEDX, SPDX, SWID, SYFT, CUSTOM | SBOM format types |
| `ComponentType` | APPLICATION, LIBRARY, FRAMEWORK, etc. | Component classification |
| `LicenseType` | MIT, APACHE_2, GPL_2, GPL_3, etc. | License identifiers |
| `LicenseRisk` | LOW, MEDIUM, HIGH, CRITICAL | License compliance risk |
| `DependencyType` | DIRECT, TRANSITIVE, OPTIONAL, DEV, etc. | Dependency types |
| `DependencyScope` | COMPILE, RUNTIME, TEST, etc. | Dependency scope |
| `VulnerabilitySeverity` | NONE, LOW, MEDIUM, HIGH, CRITICAL | CVSS severity |
| `ExploitMaturity` | UNPROVEN, POC, FUNCTIONAL, WEAPONIZED | Exploit status |
| `RemediationType` | PATCH, UPGRADE, WORKAROUND, NO_FIX | Fix availability |
| `ComponentStatus` | ACTIVE, DEPRECATED, VULNERABLE, EOL | Component status |

**Dataclasses Implemented**:

1. **SoftwareComponent** (34 fields)
   - Package identification: `purl`, `cpe`, `name`, `version`
   - License: `license_type`, `license_expression`, `license_risk`
   - Vulnerability summary: `vulnerability_count`, `critical_vuln_count`, `max_cvss_score`, `epss_score`
   - Methods: `generate_purl()`, `has_vulnerabilities`, `is_high_risk`
   - Serialization: `to_dict()`, `to_qdrant_payload()`

2. **SBOM** (28 fields)
   - Format: `format`, `format_version`, `spec_version`
   - Counts: `total_components`, `direct_dependencies`, `transitive_dependencies`
   - Vulnerability summary: `total_vulnerabilities`, `critical_count`, etc.
   - Methods: `vulnerability_density`, `has_vulnerabilities`
   - Serialization: `to_dict()`, `to_qdrant_payload()`

3. **SoftwareVulnerability** (39 fields)
   - CVE: `cve_id`, `cvss_v3_score`, `cvss_v3_vector`
   - EPSS: `epss_score`, `epss_percentile`
   - Exploitability: `exploit_maturity`, `in_the_wild`, `cisa_kev`
   - APT linkage: `apt_groups`, `malware_families`
   - Remediation: `remediation_type`, `fixed_version`, `patch_url`
   - Methods: `is_critical`, `is_exploitable`, `has_fix`
   - Serialization: `to_dict()`, `to_qdrant_payload()`

4. **DependencyRelation** (18 fields)
   - Graph: `source_component_id`, `target_component_id`
   - Type: `dependency_type`, `scope`, `depth`
   - Methods: `is_direct`
   - Serialization: `to_dict()`, `to_qdrant_payload()`

5. **LicenseComplianceResult** (16 fields)
   - Compliance: `is_compliant`, `compliant_count`, `non_compliant_count`
   - Issues: `copyleft_violations`, `license_conflicts`
   - Policy: `allowed_licenses`, `denied_licenses`

6. **DependencyGraphNode** (12 fields)
   - Tree: `component_id`, `depth`, `children`
   - Metrics: `dependents_count`, `dependencies_count`

**Validation**: All models import and create successfully

---

### Day 2: Service Methods ✅ COMPLETE

**Files Created**:
- `api/sbom_analysis/sbom_service.py` - Service layer with Qdrant integration

**Request/Response Dataclasses** (10 types):
| Type | Purpose |
|------|---------|
| `ComponentSearchRequest` | Component search parameters |
| `ComponentSearchResult` | Component search result with score |
| `VulnerabilitySearchRequest` | Vulnerability search parameters |
| `VulnerabilitySearchResult` | Vulnerability result with score |
| `SBOMSearchRequest` | SBOM search parameters |
| `SBOMSearchResult` | SBOM search result with score |
| `DependencyPath` | Path in dependency graph |
| `ImpactAnalysis` | Component impact metrics |
| `RiskSummary` | Comprehensive risk summary |

**SBOMAnalysisService Class**:
- **Collection**: `ner11_sbom` with 384-dimension vectors
- **Embedding**: sentence-transformers/all-MiniLM-L6-v2
- **Customer Isolation**: Full multi-tenant via CustomerContext

**SBOM Operations** (4 methods):
- `create_sbom()` - Create new SBOM with embedding
- `get_sbom()` - Get SBOM by ID
- `list_sboms()` - List with format filter
- `delete_sbom()` - Delete SBOM and components

**Component Operations** (6 methods):
- `create_component()` - Create with embedding
- `get_component()` - Get by ID
- `search_components()` - Semantic + filter search
- `get_components_by_sbom()` - All components for SBOM
- `get_vulnerable_components()` - Components above CVSS threshold
- `get_high_risk_components()` - Critical/high risk components

**Vulnerability Operations** (6 methods):
- `create_vulnerability()` - Create CVE record
- `get_vulnerability()` - Get by ID
- `search_vulnerabilities()` - Semantic + filter search
- `get_vulnerabilities_by_component()` - All vulns for component
- `get_critical_vulnerabilities()` - CISA KEV + in-the-wild + CVSS >= 9.0
- `get_vulnerabilities_by_apt()` - Filter by APT group

**Dependency Operations** (3 methods):
- `create_dependency()` - Create dependency relation
- `get_dependencies()` - What component depends on
- `get_dependents()` - What depends on component

**Analytics** (3 methods):
- `get_sbom_risk_summary()` - Comprehensive risk metrics
- `get_license_compliance()` - License policy compliance
- `get_dashboard_summary()` - Customer-wide dashboard

**Validation**: All service classes and methods import successfully

### Day 3: Dependency Graph ✅ COMPLETE

**Methods Implemented (8 total)**:

| Method | Purpose |
|--------|---------|
| `build_dependency_tree()` | Build recursive dependency tree with depth control |
| `get_transitive_closure()` | Get all transitive deps/dependents (BFS) |
| `get_impact_analysis()` | Calculate component vulnerability impact |
| `detect_cycles()` | Find circular dependencies using DFS |
| `find_shortest_path()` | BFS shortest path between components |
| `get_dependency_depth_analysis()` | Depth distribution statistics |
| `get_vulnerable_paths()` | Find paths to vulnerable components |
| `get_dependency_graph_stats()` | Comprehensive graph metrics |

**Key Features**:
- **Circular Reference Detection**: Prevents infinite recursion in tree building
- **Bidirectional Traversal**: Both "dependencies" and "dependents" directions
- **Vulnerability Propagation**: Tracks CVSS through dependency chains
- **Graph Metrics**: Density, in/out degree, root/leaf nodes
- **Deep Dependency Tracking**: Identifies components with deep transitive chains

**Algorithms**:
- DFS for cycle detection (Tarjan-style)
- BFS for shortest path finding
- Recursive tree building with memoization

**Validation**: All 8 methods import and compile successfully

### Day 4: Vulnerability Correlation ✅ COMPLETE

**Methods Implemented (10 total)**:

| Method | Purpose |
|--------|---------|
| `match_cve_to_component()` | Create CVE-component association with full metadata |
| `bulk_match_cves()` | Batch CVE matching with error handling |
| `get_epss_prioritized_vulns()` | EPSS-sorted vulnerabilities (exploit probability) |
| `get_kev_vulnerabilities()` | CISA Known Exploited Vulnerabilities |
| `get_exploitable_vulnerabilities()` | Filter by exploit maturity level |
| `get_apt_vulnerability_report()` | APT group vulnerability grouping |
| `correlate_vulns_with_equipment()` | Link SBOMs to E15 equipment |
| `get_vulnerability_timeline()` | Discovery date timeline |
| `acknowledge_vulnerability()` | Mark vulns as reviewed/risk-accepted |
| `get_remediation_report()` | Remediation recommendations with priority |

**Key Features**:
- **CVSS to Severity Mapping**: Automatic severity assignment from score
- **Exploit Maturity Detection**: Auto-sets maturity based on KEV/exploit status
- **EPSS Prioritization**: Sort by exploit probability, not just CVSS
- **APT Group Tracking**: Link vulnerabilities to threat actor groups
- **E15 Integration**: Correlate software vulns with physical equipment
- **Remediation Guidance**: Prioritized recommendations with KEV focus

**Validation**: All 10 methods import and compile successfully

### Day 5: FastAPI Endpoints ✅ COMPLETE

**Files Created**:
- `api/sbom_analysis/sbom_router.py` - FastAPI router with 32 endpoints

**Pydantic Models** (21 total):

| Category | Models |
|----------|--------|
| SBOM | `SBOMCreate`, `SBOMResponse`, `SBOMSearchResponse`, `SBOMRiskSummaryResponse` |
| Component | `ComponentCreate`, `ComponentResponse`, `ComponentSearchResponse` |
| Dependency | `DependencyCreate`, `DependencyResponse`, `DependencyTreeResponse`, `DependencyGraphStatsResponse`, `DependencyPathResponse`, `ImpactAnalysisResponse` |
| Vulnerability | `VulnerabilityCreate`, `VulnerabilityResponse`, `VulnerabilitySearchResponse`, `VulnerabilityAcknowledgeRequest`, `APTReportResponse`, `RemediationReportResponse` |
| License | `LicenseComplianceResponse` |
| Dashboard | `DashboardSummaryResponse` |

**API Endpoints** (32 total):

| Category | Endpoint | Method | Purpose |
|----------|----------|--------|---------|
| **SBOM** | `/api/v2/sbom/sboms` | POST | Create new SBOM |
| | `/api/v2/sbom/sboms/{id}` | GET | Get SBOM by ID |
| | `/api/v2/sbom/sboms` | GET | List/search SBOMs |
| | `/api/v2/sbom/sboms/{id}` | DELETE | Delete SBOM |
| | `/api/v2/sbom/sboms/{id}/risk-summary` | GET | SBOM risk summary |
| **Component** | `/api/v2/sbom/components` | POST | Create component |
| | `/api/v2/sbom/components/{id}` | GET | Get component |
| | `/api/v2/sbom/components/search` | GET | Semantic search |
| | `/api/v2/sbom/components/vulnerable` | GET | Vulnerable components |
| | `/api/v2/sbom/components/high-risk` | GET | High-risk components |
| | `/api/v2/sbom/sboms/{id}/components` | GET | Components by SBOM |
| **Dependency** | `/api/v2/sbom/dependencies` | POST | Create dependency |
| | `/api/v2/sbom/components/{id}/dependencies` | GET | Dependency tree |
| | `/api/v2/sbom/components/{id}/dependents` | GET | Reverse dependencies |
| | `/api/v2/sbom/components/{id}/impact` | GET | Impact analysis |
| | `/api/v2/sbom/sboms/{id}/cycles` | GET | Detect cycles |
| | `/api/v2/sbom/dependencies/path` | GET | Shortest path |
| | `/api/v2/sbom/sboms/{id}/graph-stats` | GET | Graph statistics |
| **Vulnerability** | `/api/v2/sbom/vulnerabilities` | POST | Create vulnerability |
| | `/api/v2/sbom/vulnerabilities/{id}` | GET | Get vulnerability |
| | `/api/v2/sbom/vulnerabilities/search` | GET | Semantic search |
| | `/api/v2/sbom/vulnerabilities/critical` | GET | Critical vulns |
| | `/api/v2/sbom/vulnerabilities/kev` | GET | CISA KEV vulns |
| | `/api/v2/sbom/vulnerabilities/epss-prioritized` | GET | EPSS-prioritized |
| | `/api/v2/sbom/vulnerabilities/by-apt` | GET | APT group report |
| | `/api/v2/sbom/components/{id}/vulnerabilities` | GET | Vulns by component |
| | `/api/v2/sbom/vulnerabilities/{id}/acknowledge` | POST | Acknowledge CVE |
| | `/api/v2/sbom/sboms/{id}/remediation` | GET | Remediation report |
| **License** | `/api/v2/sbom/sboms/{id}/license-compliance` | GET | License compliance |
| **Dashboard** | `/api/v2/sbom/dashboard/summary` | GET | Customer dashboard |
| | `/api/v2/sbom/sboms/{id}/vulnerable-paths` | GET | Vulnerable paths |
| | `/api/v2/sbom/sboms/{id}/correlate-equipment` | POST | E15 correlation |

**Key Features**:
- **Customer Isolation**: All endpoints require `X-Customer-ID` header
- **Semantic Search**: Vector-based component and vulnerability search
- **Dependency Visualization**: Tree and graph endpoints
- **EPSS Prioritization**: Exploit probability ranking
- **CISA KEV Integration**: Known exploited vulnerability tracking
- **APT Group Tracking**: Threat actor association
- **E15 Integration**: Equipment-SBOM correlation

**Validation**: Router syntax valid with 21 Pydantic models and 32 async endpoints

### Day 6: Integration Tests ✅ COMPLETE

**Files Created**:
- `tests/integration/test_sbom_integration.py` - 54 comprehensive tests

**Test Coverage** (54 tests across 10 test classes):

| Test Class | Tests | Coverage |
|------------|-------|----------|
| `TestSBOMModel` | 6 | SBOM creation, validation, serialization |
| `TestSoftwareComponentModel` | 8 | Component with purl, license risk, vulnerability counts |
| `TestSoftwareVulnerabilityModel` | 8 | CVE, CVSS/EPSS scoring, severity auto-calculation |
| `TestDependencyRelationModel` | 4 | Dependency types, scopes, source/target refs |
| `TestDependencyGraphNodeModel` | 2 | Tree structure, children count |
| `TestLicenseComplianceResultModel` | 2 | Compliance checking, violation tracking |
| `TestServiceModels` | 6 | Search requests, paths, impact analysis, risk summary |
| `TestCustomerIsolation` | 4 | Multi-tenant via customer_id on all models |
| `TestEnums` | 10 | All 10 enums with value validation |
| `TestIntegrationSummary` | 4 | Module exports, version checks |

**Key Test Features**:
- **Auto-Validation Testing**: License risk auto-calculated from type (MIT→LOW, GPL→HIGH)
- **Severity Calculation**: CVSS score maps to correct severity
- **Customer Isolation**: All models include `customer_id` for multi-tenancy
- **purl Generation**: Automatic Package URL creation
- **Serialization**: `to_dict()` and `to_qdrant_payload()` coverage
- **Conditional Imports**: Router import gracefully handles missing FastAPI

**Test Execution**:
```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python -m pytest tests/integration/test_sbom_integration.py -v
# Result: 54 passed, 152 warnings in 0.63s
```

**Technical Notes**:
- Made router import conditional in `__init__.py` to allow tests without FastAPI
- All dataclass field signatures aligned with actual model implementations
- Service dataclass fields verified against `sbom_service.py`

---

## Package URL (purl) Format

```
pkg:<type>/<namespace>/<name>@<version>?<qualifiers>#<subpath>
```

**Examples**:
- `pkg:npm/lodash@4.17.21`
- `pkg:pypi/requests@2.28.0`
- `pkg:maven/org.apache.commons/commons-lang3@3.12.0`
- `pkg:nuget/Newtonsoft.Json@13.0.1`
- `pkg:deb/debian/curl@7.74.0-1.3`

---

## CVSS/EPSS Integration

### CVSS v3 Severity Mapping

| Score Range | Severity |
|-------------|----------|
| 0.0 | None |
| 0.1 - 3.9 | Low |
| 4.0 - 6.9 | Medium |
| 7.0 - 8.9 | High |
| 9.0 - 10.0 | Critical |

### EPSS (Exploit Prediction Scoring System)

- **Score**: Probability of exploitation in next 30 days (0.0 - 1.0)
- **Percentile**: Ranking among all CVEs
- High EPSS with low CVSS = prioritize
- Low EPSS with high CVSS = lower urgency

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-04 | Day 1: Core models and dataclasses |
| 1.1.0 | 2025-12-04 | Day 2: SBOMAnalysisService with Qdrant integration |
| 1.2.0 | 2025-12-04 | Day 3: Dependency graph analysis (8 methods) |
| 1.3.0 | 2025-12-04 | Day 4: Vulnerability correlation (10 methods) |
| 1.4.0 | 2025-12-04 | Day 5: FastAPI router (32 endpoints, 21 Pydantic models) |
| 1.5.0 | 2025-12-04 | Day 6: Integration tests (54 tests, conditional imports) |

---

## Dependencies

- **E15 Vendor Equipment** (COMPLETE): Equipment model linkage
- **E07 IEC 62443** (COMPLETE): Safety zone correlation
- **Customer Labels** (COMPLETE): Multi-tenant isolation

## Enables

- **E10 Economic Impact**: Vulnerability cost modeling
- **E12 NOW-NEXT-NEVER**: Risk-based prioritization
- **E13 Attack Paths**: Vulnerability exploitation paths
