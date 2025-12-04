# E15: Vendor Equipment Lifecycle Management

## Phase B2 - Supply Chain

**Version:** 1.7.0
**Status:** COMPLETE
**Implementation Period:** Days 21-32 of MVP (December 2025)
**Total Tests:** 155/155 Passed (Day 12)

---

## Executive Summary

E15 implements comprehensive vendor equipment tracking and lifecycle management within the NER11 Gold Model. This enables EOL/EOS monitoring, vendor risk assessment, supply chain vulnerability tracking, maintenance scheduling, and **semantic search** for critical infrastructure assets.

### Key Achievements

| Metric | Target | Status |
|--------|--------|--------|
| Customer Isolation | 100% | ✅ Complete |
| Vendor Risk Scoring | 0-10 Scale | ✅ Implemented |
| Equipment Lifecycle | EOL/EOS Tracking | ✅ Implemented |
| Semantic Search | sentence-transformers | ✅ Implemented (Day 3) |
| Similarity Matching | Vendor/Equipment | ✅ Implemented (Day 3) |
| CVE Vulnerability Tracking | Qdrant + CVSS | ✅ Implemented (Day 4) |
| CVE Semantic Search | Natural Language | ✅ Implemented (Day 4) |
| EOL/EOS Alerting System | Severity-based | ✅ Implemented (Day 5) |
| Contract Expiration Alerts | Multi-tenant | ✅ Implemented (Day 5) |
| Lifecycle Dashboard | Aggregated | ✅ Implemented (Day 5) |
| Batch Import Operations | Vendor/Equipment | ✅ Implemented (Day 6) |
| Export Operations | CSV/Dict formats | ✅ Implemented (Day 6) |
| Dashboard Summary | Comprehensive Metrics | ✅ Implemented (Day 6) |
| Vendor Analytics | Per-vendor Metrics | ✅ Implemented (Day 6) |
| Lifecycle Reports | Timeline Planning | ✅ Implemented (Day 6) |
| Maintenance Windows | Scheduling System | ✅ Implemented (Day 7) |
| Predictive Maintenance | Algorithm-based | ✅ Implemented (Day 8) |
| Work Order Management | CRUD Operations | ✅ Implemented (Day 9) |
| Integration Tests | Pass | ✅ 155/155 |
| Neo4j Schema | Complete | ✅ Verified |
| Qdrant Collection | Created | ✅ Verified (384d vectors) |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    API Request Layer                         │
│  X-Customer-ID: CUST-001  │  X-Access-Level: write          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   VendorEquipmentService                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ - Vendor CRUD with customer isolation               │   │
│  │ - Equipment lifecycle management                    │   │
│  │ - Support contract tracking                         │   │
│  │ - Supply chain vulnerability flagging               │   │
│  │ - Maintenance schedule generation                   │   │
│  │ - Semantic search (sentence-transformers)           │   │
│  │ - Similarity matching & replacement finder          │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│       Neo4j           │           │       Qdrant          │
│  ┌─────────────────┐  │           │  ┌─────────────────┐  │
│  │ :Vendor         │  │           │  │ vendor_equipment│  │
│  │ :EquipmentModel │  │           │  │ collection      │  │
│  │ :SupportContract│  │           │  │ (384d vectors)  │  │
│  └─────────────────┘  │           │  └─────────────────┘  │
└───────────────────────┘           └───────────────────────┘
```

---

## Core Components

### 1. Vendor Model (`api/vendor_equipment/vendor_models.py`)

```python
from api.vendor_equipment import Vendor, VendorRiskLevel, SupportStatus

# Create a vendor
vendor = Vendor(
    vendor_id="VENDOR-CISCO-001",
    name="Cisco Systems",
    customer_id="CUST-001",
    risk_score=3.5,  # Automatically calculates risk_level
    support_status=SupportStatus.ACTIVE,
    country="USA",
    industry_focus=["IT", "Network"],
    supply_chain_tier=1,
    total_cves=156,
    avg_cvss_score=6.2,
)

# Risk level is automatically calculated
print(vendor.risk_level)  # VendorRiskLevel.MEDIUM
```

### Risk Level Calculation

| Risk Score | Risk Level |
|------------|------------|
| 0.0 - 3.0  | LOW |
| 3.1 - 6.0  | MEDIUM |
| 6.1 - 8.0  | HIGH |
| 8.1 - 10.0 | CRITICAL |

### 2. Equipment Model

```python
from api.vendor_equipment import EquipmentModel, LifecycleStatus, Criticality
from datetime import date, timedelta

today = date.today()

equipment = EquipmentModel(
    model_id="EQ-CISCO-ASA5500",
    vendor_id="VENDOR-CISCO-001",
    model_name="ASA 5500 Series",
    customer_id="CUST-001",
    product_line="Security Appliances",
    eol_date=today + timedelta(days=90),  # Approaching EOL
    eos_date=today + timedelta(days=180),
    criticality=Criticality.CRITICAL,
    category="firewall",
    deployed_count=15,
    vulnerability_count=8,
)

# Lifecycle status automatically calculated
print(equipment.lifecycle_status)  # LifecycleStatus.APPROACHING_EOL
print(equipment.days_to_eol())     # 90
```

### Lifecycle Status Calculation

| Condition | Status |
|-----------|--------|
| Past EOS date | `EOS` |
| Past EOL date | `EOL` |
| Within 180 days of EOL | `APPROACHING_EOL` |
| Otherwise | `CURRENT` |

### 3. Support Contract

```python
from api.vendor_equipment import SupportContract, ServiceLevel
from datetime import date, timedelta

today = date.today()

contract = SupportContract(
    contract_id="CONTRACT-001",
    vendor_id="VENDOR-CISCO-001",
    customer_id="CUST-001",
    start_date=today - timedelta(days=180),
    end_date=today + timedelta(days=180),
    service_level=ServiceLevel.PREMIUM,
    response_time_sla=4,  # hours
    coverage=["security_patches", "firmware_updates", "24/7_support"],
    annual_cost=50000.0,
)

# Status automatically calculated
print(contract.status)           # "active"
print(contract.days_remaining()) # 180
print(contract.is_expiring_soon()) # False (not within renewal reminder period)
```

---

## API Endpoints

### Vendor Endpoints

```
POST   /api/v2/vendor-equipment/vendors          - Create vendor
GET    /api/v2/vendor-equipment/vendors          - Search vendors
GET    /api/v2/vendor-equipment/vendors/{id}     - Get vendor by ID
GET    /api/v2/vendor-equipment/vendors/high-risk - Get high-risk vendors
GET    /api/v2/vendor-equipment/vendors/{id}/risk-summary - Get risk summary
```

### Equipment Endpoints

```
POST   /api/v2/vendor-equipment/equipment        - Create equipment
GET    /api/v2/vendor-equipment/equipment        - Search equipment
GET    /api/v2/vendor-equipment/equipment/{id}   - Get equipment by ID
GET    /api/v2/vendor-equipment/equipment/approaching-eol - Get approaching EOL
GET    /api/v2/vendor-equipment/equipment/eol    - Get past EOL equipment
```

### Maintenance & Vulnerability Endpoints

```
GET    /api/v2/vendor-equipment/maintenance-schedule - Prioritized schedule
POST   /api/v2/vendor-equipment/vulnerabilities/flag - Flag supply chain vuln
```

### Maintenance Window Endpoints (Day 10)

```
POST   /api/v2/vendor-equipment/maintenance-windows          - Create window
GET    /api/v2/vendor-equipment/maintenance-windows          - List windows
GET    /api/v2/vendor-equipment/maintenance-windows/{id}     - Get window by ID
DELETE /api/v2/vendor-equipment/maintenance-windows/{id}     - Delete window
POST   /api/v2/vendor-equipment/maintenance-windows/check-conflict - Check conflicts
```

### Predictive Maintenance Endpoints (Day 10-11)

```
GET    /api/v2/vendor-equipment/predictive-maintenance/{equipment_id} - Predict maintenance
GET    /api/v2/vendor-equipment/predictive-maintenance/forecast       - Get forecast
```

### Work Order Endpoints (Day 11)

```
POST   /api/v2/vendor-equipment/work-orders                - Create work order
GET    /api/v2/vendor-equipment/work-orders                - List work orders
GET    /api/v2/vendor-equipment/work-orders/{id}           - Get work order by ID
PATCH  /api/v2/vendor-equipment/work-orders/{id}/status    - Update status
GET    /api/v2/vendor-equipment/work-orders/summary        - Get summary
```

### Required Headers

| Header | Required | Description |
|--------|----------|-------------|
| `X-Customer-ID` | Yes | Customer identifier for isolation |
| `X-Namespace` | No | Customer namespace |
| `X-User-ID` | No | User ID for audit trail |
| `X-Access-Level` | No | Access level (read/write/admin) |

---

## Neo4j Schema

### Nodes

```cypher
// Vendor node
CREATE (v:Vendor {
  vendor_id: string,
  name: string,
  customer_id: string,
  risk_score: float,     // 0.0-10.0
  risk_level: string,    // 'low', 'medium', 'high', 'critical'
  support_status: string,
  country: string,
  industry_focus: [string],
  supply_chain_tier: int,  // 1=direct, 2=indirect, 3=tertiary
  total_cves: int,
  avg_cvss_score: float
});

// Equipment Model node
CREATE (em:EquipmentModel {
  model_id: string,
  vendor_id: string,
  model_name: string,
  customer_id: string,
  product_line: string,
  eol_date: date,
  eos_date: date,
  lifecycle_status: string,
  criticality: string,
  category: string,
  deployed_count: int,
  vulnerability_count: int
});

// Support Contract node
CREATE (sc:SupportContract {
  contract_id: string,
  vendor_id: string,
  customer_id: string,
  start_date: date,
  end_date: date,
  service_level: string,
  response_time_sla: int,
  coverage: [string],
  status: string,
  annual_cost: float
});
```

### Relationships

```cypher
(Vendor)-[:MANUFACTURES]->(EquipmentModel)
(Vendor)-[:HAS_CONTRACT]->(SupportContract)
(SupportContract)-[:COVERS]->(EquipmentModel)
(Vendor)-[:AFFECTED_BY]->(CVE)
(EquipmentModel)-[:VULNERABLE_TO]->(CVE)
```

### Indexes

```cypher
-- Customer isolation indexes
CREATE INDEX vendor_customer_id FOR (v:Vendor) ON (v.customer_id);
CREATE INDEX equipment_customer_id FOR (em:EquipmentModel) ON (em.customer_id);
CREATE INDEX contract_customer_id FOR (sc:SupportContract) ON (sc.customer_id);

-- Query optimization indexes
CREATE INDEX vendor_risk_score FOR (v:Vendor) ON (v.risk_score);
CREATE INDEX equipment_eol_date FOR (em:EquipmentModel) ON (em.eol_date);
CREATE INDEX equipment_lifecycle FOR (em:EquipmentModel) ON (em.lifecycle_status);
```

---

## Qdrant Collection

### Collection Configuration

```python
collection_name = "ner11_vendor_equipment"
vector_size = 384  # sentence-transformers/all-MiniLM-L6-v2
distance = Distance.COSINE
```

### Payload Structure

```json
{
  "vendor_id": "VENDOR-001",
  "name": "Cisco Systems",
  "customer_id": "CUST-001",
  "entity_type": "vendor",
  "risk_score": 3.5,
  "risk_level": "medium",
  "support_status": "active",
  "country": "USA",
  "industry_focus": ["IT", "Network"],
  "supply_chain_tier": 1,
  "total_cves": 156,
  "avg_cvss_score": 6.2
}
```

### Customer Isolation Filter

```python
from qdrant_client.models import Filter, FieldCondition, MatchAny

# Include SYSTEM entities
filter_with_system = Filter(
    must=[
        FieldCondition(
            key="customer_id",
            match=MatchAny(any=["CUST-001", "SYSTEM"])
        )
    ]
)
```

---

## Supply Chain Vulnerability Tracking (Day 4)

### CVE Record Storage

CVE vulnerabilities are stored in Qdrant with semantic embeddings for natural language search:

```python
from api.vendor_equipment import CVERecord, VulnerabilityAlert
from datetime import date

# CVERecord dataclass with auto-severity calculation
cve = CVERecord(
    cve_id="CVE-2024-12345",
    cvss_score=9.8,
    severity="",  # Auto-calculated from CVSS: critical
    description="Remote code execution vulnerability",
    affected_vendor_id="VENDOR-CISCO-001",
    affected_equipment_ids=["MODEL-001", "MODEL-002"],
    published_date=date(2024, 12, 1),
)

# Severity auto-calculation:
# - critical: CVSS >= 9.0
# - high: CVSS >= 7.0
# - medium: CVSS >= 4.0
# - low: CVSS < 4.0
```

### Flagging a Vendor Vulnerability

When a supply chain vulnerability is discovered, it's stored in Qdrant and returns a VulnerabilityAlert:

```python
# Flag vulnerability - stores CVE in Qdrant
alert = service.flag_vendor_vulnerability(
    vendor_id="VENDOR-SOLARWINDS-001",
    cve_id="CVE-2020-10148",
    cvss_score=9.8,
    description="SolarWinds Orion API authentication bypass",
    published_date=date(2020, 12, 13),
)

# VulnerabilityAlert contains impact analysis
print(f"CVE: {alert.cve_id}")
print(f"Vendor: {alert.vendor_name}")
print(f"Severity: {alert.severity}")
print(f"Affected Equipment: {alert.affected_equipment_count}")
print(f"Critical Equipment: {alert.critical_equipment_affected}")
print(f"Recommendation: {alert.recommendation}")
```

### Retrieving Vendor CVEs

```python
# Get all CVEs for a vendor
vendor_cves = service.get_vendor_cves("VENDOR-CISCO-001")

# Filter by minimum CVSS score
high_cves = service.get_vendor_cves("VENDOR-CISCO-001", min_cvss=7.0)

# Filter by severity
critical_cves = service.get_vendor_cves("VENDOR-CISCO-001", severity="critical")

for cve in vendor_cves:
    print(f"{cve.cve_id}: {cve.severity} ({cve.cvss_score})")
```

### Semantic CVE Search

Search CVEs using natural language queries:

```python
# Find SQL-related vulnerabilities
sql_cves = service.search_cves("SQL injection database attack")

# Find authentication bypass issues
auth_cves = service.search_cves("authentication bypass remote access")

for cve in sql_cves:
    print(f"{cve.cve_id}: {cve.description}")
```

### Critical Vulnerability Dashboard

```python
# Get all critical and high severity vulnerabilities with impact analysis
critical_alerts = service.get_critical_vulnerabilities(limit=20)

for alert in critical_alerts:
    print(f"🚨 {alert.cve_id} ({alert.severity})")
    print(f"   Vendor: {alert.vendor_name}")
    print(f"   CVSS: {alert.cvss_score}")
    print(f"   Equipment Affected: {alert.affected_equipment_count}")
    print(f"   Action: {alert.recommendation}")
```

### Maintenance Schedule Generation

Prioritized by:
1. EOL proximity (highest priority)
2. Vulnerability count
3. Criticality level

```python
# Get maintenance schedule
schedule = service.get_maintenance_schedule(limit=50)

for equipment_result, recommendation in schedule:
    print(f"{equipment_result.equipment.model_name}: {recommendation}")
```

---

## Semantic Search (Day 3)

### EmbeddingService

The embedding service provides 384-dimensional semantic vectors using sentence-transformers:

```python
from api.vendor_equipment import EmbeddingService, get_embedding_service

# Get singleton instance
embedding_service = get_embedding_service()

# Encode text for search
query_vector = embedding_service.encode("network security equipment")

# Encode vendor data
vendor_vector = embedding_service.encode_vendor({
    "name": "Cisco Systems",
    "industry_focus": ["IT", "Network"],
    "country": "USA",
})

# Calculate similarity
similarity = embedding_service.similarity(query_vector, vendor_vector)
print(f"Similarity: {similarity:.2f}")  # 0.0-1.0
```

### Semantic Search Methods

```python
from api.vendor_equipment import VendorEquipmentService

service = VendorEquipmentService()

# Natural language search across vendors and equipment
results = service.semantic_search(
    query="enterprise network switches",
    entity_type="equipment",  # Optional: "vendor" or "equipment"
    limit=10,
    min_score=0.5,
)

for result in results:
    print(f"{result.name} ({result.entity_type}): {result.score:.2f}")
```

### Similarity Matching

```python
# Find similar vendors
similar_vendors = service.find_similar_vendors(
    vendor_id="VENDOR-CISCO-001",
    limit=5,
    min_score=0.6,
)

# Find similar equipment
similar_equipment = service.find_similar_equipment(
    model_id="EQ-CATALYST-9000",
    limit=5,
    min_score=0.6,
)

# Find replacement candidates for EOL equipment
replacements = service.find_replacement_candidates(
    model_id="EQ-ASA-5500",  # EOL equipment
    exclude_eol=True,        # Only show current equipment
    limit=5,
)

for match in replacements:
    print(f"Replacement: {match.match_name} (similarity: {match.similarity_score:.2f})")
```

---

## EOL/EOS Alerting System (Day 5)

### Alert Severity Levels

| Severity | Days Remaining | Action Required |
|----------|---------------|-----------------|
| CRITICAL | < 7 days or past due | Immediate action |
| HIGH | 7-30 days | Action required |
| WARNING | 30-90 days | Planning needed |
| INFO | > 90 days | Informational |

### Alert Types

```python
from api.vendor_equipment.vendor_models import AlertType

# Equipment lifecycle alerts
AlertType.EOL_APPROACHING  # Equipment approaching end-of-life
AlertType.EOL_PAST         # Equipment past end-of-life
AlertType.EOS_APPROACHING  # Equipment approaching end-of-support
AlertType.EOS_PAST         # Equipment past end-of-support

# Contract alerts
AlertType.CONTRACT_EXPIRING  # Support contract expiring soon
AlertType.CONTRACT_EXPIRED   # Support contract expired

# Risk alerts
AlertType.VENDOR_RISK_INCREASED    # Vendor risk score increased
AlertType.VULNERABILITY_DETECTED   # New vulnerability detected
```

### EOLAlert Dataclass

```python
from api.vendor_equipment import EOLAlert, AlertType, AlertSeverity
from datetime import date

# Create an alert manually
alert = EOLAlert(
    alert_id="ALERT-001",
    alert_type=AlertType.EOL_APPROACHING,
    severity=AlertSeverity.WARNING,
    customer_id="CUST-001",
    entity_type="equipment_model",
    entity_id="MODEL-ROUTER-001",
    entity_name="Catalyst 6500 Series",
    message="Catalyst 6500 Series reaches End of Life in 60 days",
    days_remaining=60,
    target_date=date(2025, 3, 1),
    vendor_id="VENDOR-CISCO-001",
    vendor_name="Cisco Systems",
    affected_asset_count=25,
    recommended_action="Plan migration to Catalyst 9000 Series",
)

# Convert to API response
alert_dict = alert.to_dict()

# Store in Qdrant
payload = alert.to_qdrant_payload()
```

### Factory Methods

```python
from api.vendor_equipment.vendor_models import EOLAlert, EquipmentModel, SupportContract

# Create alert from equipment model
equipment = EquipmentModel(...)
eol_alert = EOLAlert.from_equipment_model(
    model=equipment,
    alert_type=AlertType.EOL_APPROACHING,
    vendor_name="Cisco Systems",
)

# Create alert from support contract
contract = SupportContract(...)
contract_alert = EOLAlert.from_support_contract(
    contract=contract,
    vendor_name="Palo Alto Networks",
)
```

### Get EOL/EOS Alerts

Query equipment approaching or past lifecycle milestones:

```python
from api.vendor_equipment import VendorEquipmentService

service = VendorEquipmentService()

# Get all EOL/EOS alerts within 180 days
alerts = service.get_eol_alerts(days_ahead=180)

# Filter by severity
critical_alerts = service.get_eol_alerts(severity_filter="critical")

# Exclude past due (only approaching)
future_alerts = service.get_eol_alerts(include_past_due=False)

for alert in alerts:
    print(f"🚨 {alert.severity.value.upper()}: {alert.entity_name}")
    print(f"   {alert.message}")
    print(f"   Target: {alert.target_date}")
    print(f"   Affected Assets: {alert.affected_asset_count}")
    if alert.recommended_action:
        print(f"   Action: {alert.recommended_action}")
```

### Get Contract Expiration Alerts

Query support contracts approaching expiration:

```python
# Get contracts expiring within 90 days
contract_alerts = service.get_contract_expiration_alerts(days_ahead=90)

# Include expired contracts
all_alerts = service.get_contract_expiration_alerts(include_expired=True)

for alert in contract_alerts:
    print(f"📋 {alert.entity_name}")
    print(f"   Status: {alert.alert_type.value}")
    print(f"   Days Remaining: {alert.days_remaining}")
    print(f"   Vendor: {alert.vendor_name}")
```

### Lifecycle Dashboard

Get all alerts in a single aggregated view:

```python
# Get comprehensive lifecycle dashboard
dashboard = service.get_all_lifecycle_alerts()

print(f"Total Alerts: {dashboard['total_alerts']}")
print(f"Critical: {dashboard['total_critical']}")
print(f"High: {dashboard['total_high']}")

# Process EOL alerts
for alert in dashboard['eol_alerts']:
    print(f"EOL: {alert.entity_name} - {alert.severity.value}")

# Process contract alerts
for alert in dashboard['contract_alerts']:
    print(f"Contract: {alert.entity_name} - {alert.severity.value}")

# Filter by severity
critical_dashboard = service.get_all_lifecycle_alerts(severity_filter="critical")
```

### Vendor Risk Summary

Get comprehensive risk metrics for a vendor:

```python
# Get vendor risk summary with EOL and CVE data
summary = service.get_vendor_risk_summary("VENDOR-CISCO-001")

if summary:
    print(f"Vendor: {summary.vendor_name}")
    print(f"Risk Score: {summary.risk_score} ({summary.risk_level})")
    print(f"Total Equipment: {summary.total_equipment}")
    print(f"Equipment at EOL: {summary.equipment_at_eol}")
    print(f"Approaching EOL: {summary.equipment_approaching_eol}")
    print(f"Critical CVEs: {summary.critical_cve_count}")
    print(f"High CVEs: {summary.high_cve_count}")
```

---

## Test Coverage

### Test Categories (155/155 Passed)

| Category | Tests | Status |
|----------|-------|--------|
| Vendor Model | 7 | ✅ |
| Equipment Model | 5 | ✅ |
| Support Contract | 4 | ✅ |
| Customer Isolation | 5 | ✅ |
| Vendor Equipment Service | 4 | ✅ |
| Lifecycle Queries | 3 | ✅ |
| Data Conversion | 4 | ✅ |
| Security Validation | 5 | ✅ |
| Neo4j Live Integration | 5 | ✅ |
| Qdrant Live Integration | 4 | ✅ |
| End-to-End Integration | 1 | ✅ |
| Embedding Service | 14 | ✅ (Day 3) |
| Semantic Search Dataclasses | 2 | ✅ (Day 3) |
| Semantic Search Service | 4 | ✅ (Day 3) |
| Semantic Search Live Integration | 2 | ✅ (Day 3) |
| Global Embedding Service | 2 | ✅ (Day 3) |
| CVE Record Dataclass | 3 | ✅ (Day 4) |
| Vulnerability Alert Dataclass | 1 | ✅ (Day 4) |
| CVE Service Methods | 5 | ✅ (Day 4) |
| CVE Live Integration | 3 | ✅ (Day 4) |
| EOL Alert Dataclass | 6 | ✅ (Day 5) |
| Alert Enums | 2 | ✅ (Day 5) |
| Alerting Service Methods | 4 | ✅ (Day 5) |
| Alerting Live Integration | 3 | ✅ (Day 5) |
| Batch Import Methods | 4 | ✅ (Day 6) |
| Batch Import Vendors | 2 | ✅ (Day 6) |
| Batch Import Equipment | 2 | ✅ (Day 6) |
| Export Operations | 4 | ✅ (Day 6) |
| Reporting Methods | 3 | ✅ (Day 6) |
| Dashboard Summary | 2 | ✅ (Day 6) |
| Vendor Analytics | 2 | ✅ (Day 6) |
| Lifecycle Report | 3 | ✅ (Day 6) |
| MaintenanceWindow Dataclass | 5 | ✅ (Day 7) |
| MaintenanceWindow Service | 6 | ✅ (Day 7) |
| MaintenancePrediction Dataclass | 3 | ✅ (Day 8) |
| Predictive Maintenance Service | 4 | ✅ (Day 8) |
| WorkOrder Dataclasses | 9 | ✅ (Day 9) |
| WorkOrder Service | 8 | ✅ (Day 9) |

### Running Tests

```bash
# Run all E15 integration tests
python3 -m pytest tests/integration/test_vendor_equipment_integration.py -v

# Run specific test category
python3 -m pytest tests/integration/test_vendor_equipment_integration.py::TestVendorModel -v

# Run with coverage
python3 -m pytest tests/integration/ --cov=api/vendor_equipment --cov-report=html
```

---

## File Structure

```
5_NER11_Gold_Model/
├── api/
│   ├── __init__.py
│   ├── customer_isolation/           # Phase B1
│   │   ├── __init__.py
│   │   ├── customer_context.py
│   │   ├── isolated_semantic_service.py
│   │   └── semantic_router.py
│   └── vendor_equipment/             # Phase B2 - E15
│       ├── __init__.py
│       ├── vendor_models.py          # Vendor, EquipmentModel, SupportContract
│       ├── vendor_service.py         # VendorEquipmentService + semantic search
│       ├── embedding_service.py      # EmbeddingService (Day 3)
│       └── vendor_router.py          # FastAPI endpoints
├── scripts/
│   └── vendor_equipment_schema.py    # Neo4j schema migration
├── tests/
│   └── integration/
│       ├── test_customer_isolation_integration.py  # Phase B1 tests
│       └── test_vendor_equipment_integration.py    # Phase B2 tests (71 tests)
└── docs/
    ├── CUSTOMER_LABELS_IMPLEMENTATION_GUIDE.md    # Phase B1
    ├── CUSTOMER_LABELS_SECURITY_AUDIT.md          # Phase B1
    └── E15_VENDOR_EQUIPMENT_IMPLEMENTATION.md     # This document
```

---

## Security Considerations

### Input Validation

- Empty/whitespace IDs are rejected
- Values are automatically trimmed
- Risk scores must be 0.0-10.0

### Customer Isolation

- All operations require customer context
- Queries are filtered by customer_id
- SYSTEM entities accessible when `include_system=True`

### Access Control

- `READ`: Search and retrieve only
- `WRITE`: Create/update vendors and equipment
- `ADMIN`: Full access including delete

---

## Integration with CUSTOMER_LABELS (Phase B1)

E15 builds on CUSTOMER_LABELS for multi-tenant isolation:

```python
from api.customer_isolation import CustomerContextManager, CustomerAccessLevel

# Set customer context (from Phase B1)
CustomerContextManager.create_context(
    customer_id="CUST-001",
    namespace="acme_corp",
    access_level=CustomerAccessLevel.WRITE,
)

# Use E15 vendor equipment service
service = VendorEquipmentService()
vendors = service.search_vendors(VendorSearchRequest(query="cisco"))
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-04 | Initial implementation - Day 1 complete |
| 1.1.0 | 2025-12-04 | Day 2 - Live database integration, 47/47 tests passing |
| 1.2.0 | 2025-12-04 | Day 3 - Semantic search with sentence-transformers, 71/71 tests |
| 1.3.0 | 2025-12-04 | Day 4 - CVE vulnerability tracking with Qdrant storage, semantic CVE search, VulnerabilityAlert impact analysis, 83/83 tests |
| 1.4.0 | 2025-12-04 | Day 5 - EOL/EOS alerting system with severity levels, contract expiration alerts, lifecycle dashboard, vendor risk summary, 98/98 tests |
| 1.5.0 | 2025-12-04 | Day 6 - Batch import/export operations, dashboard summary, vendor analytics, lifecycle reports with timeline planning, 120/120 tests |
| 1.6.0 | 2025-12-04 | Day 7-9 - Maintenance scheduling system, predictive maintenance algorithms, work order management with status tracking, 155/155 tests |
| 1.7.0 | 2025-12-04 | Day 10-12 - FastAPI router endpoints for maintenance windows, predictive maintenance, work orders; final integration tests complete |

---

## Maintenance Scheduling (Days 7-9)

### Maintenance Window Types

```python
from api.vendor_equipment import MaintenanceWindowType

MaintenanceWindowType.SCHEDULED    # Planned maintenance window
MaintenanceWindowType.EMERGENCY    # Urgent unplanned maintenance
MaintenanceWindowType.RECURRING    # Repeating maintenance schedule
MaintenanceWindowType.BLACKOUT     # No maintenance allowed (freeze period)
```

### MaintenanceWindow Dataclass

```python
from api.vendor_equipment import MaintenanceWindow, MaintenanceWindowType
from datetime import datetime, timedelta

# Create a maintenance window
window = MaintenanceWindow(
    window_id="MW-001",
    name="Weekend Maintenance",
    customer_id="CUST-001",
    window_type=MaintenanceWindowType.SCHEDULED,
    start_time=datetime(2025, 1, 15, 22, 0),  # 10 PM
    end_time=datetime(2025, 1, 16, 6, 0),     # 6 AM
    affected_equipment_ids=["EQ-001", "EQ-002"],
    recurrence_pattern="weekly",  # Optional for recurring windows
)

# Check if currently in window
is_active = window.is_in_window()

# Convert to API response
window_dict = window.to_dict()

# Store in Qdrant
payload = window.to_qdrant_payload()
```

### Maintenance Window Service Methods

```python
from api.vendor_equipment import VendorEquipmentService, MaintenanceWindowType

service = VendorEquipmentService()

# Create maintenance window
window_id = service.create_maintenance_window(window)

# Get window by ID
window = service.get_maintenance_window("MW-001")

# List windows with optional filters
windows = service.list_maintenance_windows(
    window_type=MaintenanceWindowType.SCHEDULED,
    equipment_id="EQ-001",  # Filter by affected equipment
)

# Delete maintenance window
deleted = service.delete_maintenance_window("MW-001")

# Check for scheduling conflicts
conflicts = service.check_maintenance_conflict(
    proposed_start=datetime(2025, 1, 15, 23, 0),
    proposed_end=datetime(2025, 1, 16, 3, 0),
    equipment_ids=["EQ-001"],
)
```

### Predictive Maintenance

The predictive maintenance system uses equipment age, maintenance history, and criticality to predict future maintenance needs:

```python
from api.vendor_equipment import MaintenancePrediction

# Predict maintenance for equipment
predictions = service.predict_maintenance(
    equipment_id="EQ-001",
    days_ahead=90,  # Look 90 days ahead
)

# Returns list of MaintenancePrediction objects
for prediction in predictions:
    print(f"Equipment: {prediction.equipment_name}")
    print(f"Predicted Date: {prediction.predicted_date}")
    print(f"Confidence: {prediction.confidence_score:.2f}")
    print(f"Risk Level: {prediction.risk_level}")
    print(f"Maintenance Type: {prediction.maintenance_type}")
    print(f"Recommendation: {prediction.recommendation}")
```

### Maintenance Forecast

Get a comprehensive maintenance forecast:

```python
# Get maintenance forecast for next 6 months
forecast = service.get_maintenance_forecast(months_ahead=6)

print(f"Forecast Months: {forecast['forecast_months']}")
print(f"Generated: {forecast['generated_at']}")

# Monthly breakdown
for month in forecast['monthly_breakdown']:
    print(f"{month['month']}: {month['predicted_maintenance_count']} items")
```

### Work Order Management

Create and track maintenance work orders:

```python
from api.vendor_equipment import (
    MaintenanceWorkOrder,
    WorkOrderStatus,
    WorkOrderPriority,
)
from datetime import datetime, timedelta

# Create a work order
work_order = MaintenanceWorkOrder(
    work_order_id="WO-001",
    customer_id="CUST-001",
    equipment_id="EQ-001",
    equipment_name="Cisco ASA 5500",
    title="Quarterly Maintenance",
    description="Perform quarterly maintenance checks",
    priority=WorkOrderPriority.HIGH,
    status=WorkOrderStatus.PENDING,
    scheduled_start=datetime.now() + timedelta(days=7),
    scheduled_end=datetime.now() + timedelta(days=7, hours=4),
    assigned_technician="John Smith",
    maintenance_window_id="MW-001",  # Optional link to window
)

# Check if overdue
is_overdue = work_order.is_overdue()

# Get duration (if started and completed)
hours = work_order.get_duration_hours()

# Convert to API response
wo_dict = work_order.to_dict()
```

### Work Order Service Methods

```python
# Create work order
work_order_id = service.create_work_order(work_order)

# Get work order by ID
wo = service.get_work_order("WO-001")

# List work orders with filters
orders = service.list_work_orders(
    status=WorkOrderStatus.PENDING,
    priority=WorkOrderPriority.HIGH,
    equipment_id="EQ-001",
)

# Update work order status
updated = service.update_work_order_status(
    work_order_id="WO-001",
    new_status=WorkOrderStatus.IN_PROGRESS,
    notes="Starting maintenance",
)

# Get work order summary
summary = service.get_work_order_summary()

print(f"Total Work Orders: {summary['total']}")
print(f"By Status: {summary['status_breakdown']}")
print(f"By Priority: {summary['priority_breakdown']}")
```

---

## Batch Operations (Day 6)

### Batch Import Vendors

Import multiple vendors in a single operation with duplicate detection:

```python
from api.vendor_equipment import VendorEquipmentService

service = VendorEquipmentService()

# Batch import vendors
vendors_data = [
    {
        "vendor_id": "VENDOR-NEW-001",
        "name": "New Vendor Corp",
        "risk_score": 3.5,
        "country": "USA",
    },
    {
        "vendor_id": "VENDOR-NEW-002",
        "name": "Another Vendor LLC",
        "risk_score": 2.0,
        "country": "Germany",
    },
]

result = service.batch_import_vendors(vendors_data, skip_duplicates=True)

print(f"Imported: {result['imported_count']}")
print(f"Skipped: {result['skipped_count']}")
print(f"Errors: {result['error_count']}")
print(f"Imported IDs: {result['imported_ids']}")
```

### Batch Import Equipment

```python
# Batch import equipment
equipment_data = [
    {
        "model_id": "EQ-NEW-001",
        "vendor_id": "VENDOR-CISCO-001",
        "model_name": "Catalyst 9300",
        "category": "switch",
        "criticality": "high",
    },
    {
        "model_id": "EQ-NEW-002",
        "vendor_id": "VENDOR-CISCO-001",
        "model_name": "ASR 9000",
        "category": "router",
        "criticality": "critical",
    },
]

result = service.batch_import_equipment(equipment_data)
print(f"Imported: {result['imported_count']}")
```

### Export Vendors

Export vendors with optional equipment and CVE data:

```python
# Export all vendors as list of dicts
vendors = service.export_vendors(format="dict")

# Export with equipment included
vendors_full = service.export_vendors(
    format="dict",
    include_equipment=True,
    include_cves=True,
)

# Export as CSV-ready format
vendors_csv = service.export_vendors(format="csv")
```

### Export Equipment

Export equipment with optional filters:

```python
# Export all equipment
equipment = service.export_equipment()

# Filter by vendor
cisco_equipment = service.export_equipment(vendor_id="VENDOR-CISCO-001")

# Filter by lifecycle status
eol_equipment = service.export_equipment(lifecycle_status="eol")

# Export as CSV format
equipment_csv = service.export_equipment(format="csv")
```

---

## Reporting and Analytics (Day 6)

### Dashboard Summary

Get comprehensive metrics for the vendor equipment inventory:

```python
# Get dashboard summary
dashboard = service.get_dashboard_summary()

print(f"Customer: {dashboard['customer_id']}")
print(f"Total Vendors: {dashboard['summary']['total_vendors']}")
print(f"Total Equipment: {dashboard['summary']['total_equipment']}")
print(f"Active Contracts: {dashboard['summary']['active_contracts']}")

# Equipment by lifecycle status
for status, count in dashboard['equipment_by_lifecycle'].items():
    print(f"  {status}: {count}")

# Equipment by criticality
for level, count in dashboard['equipment_by_criticality'].items():
    print(f"  {level}: {count}")

# CVE severity distribution
for severity, count in dashboard['cves_by_severity'].items():
    print(f"  {severity}: {count}")

# Alert counts
print(f"Critical Alerts: {dashboard['alerts']['critical']}")
print(f"High Alerts: {dashboard['alerts']['high']}")
```

### Vendor Analytics

Get per-vendor analytics including equipment counts and risk metrics:

```python
# Get analytics for all vendors
analytics = service.get_vendor_analytics()

for vendor in analytics:
    print(f"\n{vendor['vendor_name']} ({vendor['vendor_id']})")
    print(f"  Risk Score: {vendor['risk_score']} ({vendor['risk_level']})")
    print(f"  Equipment Count: {vendor['equipment_count']}")
    print(f"  EOL Equipment: {vendor['equipment_at_eol']}")
    print(f"  CVE Count: {vendor['cve_count']}")
    print(f"  Critical CVEs: {vendor['critical_cve_count']}")
    print(f"  Active Contracts: {vendor['active_contracts']}")

# Get analytics for specific vendor
cisco_analytics = service.get_vendor_analytics(vendor_id="VENDOR-CISCO-001")
```

### Lifecycle Report

Generate comprehensive lifecycle planning reports with timeline:

```python
# Generate lifecycle report for next 180 days
report = service.get_lifecycle_report(days_ahead=180)

print(f"Report Date: {report['report_date']}")
print(f"Look-ahead: {report['look_ahead_days']} days")

# Summary statistics
print(f"\nSummary:")
print(f"  Equipment at Risk: {report['summary']['equipment_at_risk']}")
print(f"  Contracts Expiring: {report['summary']['contracts_expiring']}")
print(f"  Critical Actions: {report['summary']['critical_actions']}")
print(f"  High Priority Actions: {report['summary']['high_priority_actions']}")

# Timeline breakdown by month
print(f"\nTimeline:")
for period in report['timeline']:
    print(f"  {period['period']}:")
    print(f"    EOL Equipment: {period['eol_count']}")
    print(f"    EOS Equipment: {period['eos_count']}")
    print(f"    Expiring Contracts: {period['contracts_expiring']}")

# Contract alerts
print(f"\nContract Alerts:")
for alert in report['contract_alerts']:
    print(f"  {alert.entity_name}: {alert.days_remaining} days remaining")

# Recommendations
print(f"\nRecommendations:")
for rec in report['recommendations']:
    print(f"  - {rec}")
```

---

## References

- [TASKMASTER Master Index](../../../1_AEON_DT_CyberSecurity_Wiki_Current/Application_Rationalization_2025_12_3/taskmaster/00_TASKMASTER_MASTER_INDEX.md)
- [E15 Task Specification](../../../1_AEON_DT_CyberSecurity_Wiki_Current/Application_Rationalization_2025_12_3/taskmaster/03_TASK_SPECIFICATIONS.md#e15-vendor-equipment-tracking)
- [CUSTOMER_LABELS Implementation Guide](./CUSTOMER_LABELS_IMPLEMENTATION_GUIDE.md)
