# CUSTOMER_LABELS Implementation Guide

## Phase B1: Multi-Tenant Customer Isolation

**Version:** 1.0.0
**Status:** ✅ COMPLETE
**Implementation Period:** Days 1-5 (December 2025)
**Total Tests:** 17/17 Passed

---

## Executive Summary

CUSTOMER_LABELS provides multi-tenant data isolation for NER11 Gold Model, ensuring each customer's threat intelligence data remains completely isolated while sharing common reference data (SYSTEM entities like CVEs, CWEs, CAPECs).

### Key Achievements

| Metric | Target | Achieved |
|--------|--------|----------|
| Customer Isolation | 100% | ✅ 100% |
| SYSTEM Entity Access | Configurable | ✅ include_system flag |
| Integration Tests | Pass | ✅ 17/17 |
| Neo4j Support | Yes | ✅ Verified |
| Qdrant Support | Yes | ✅ Verified |
| Thread Safety | Yes | ✅ ContextVar-based |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    API Request Layer                         │
│  X-Customer-ID: CUST-001  │  X-Namespace: acme_corp         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   CustomerContext                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ customer_id: "CUST-001"                              │   │
│  │ namespace: "acme_corp"                               │   │
│  │ access_level: READ | WRITE | ADMIN                   │   │
│  │ include_system: true | false                         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│      Neo4j Filter     │           │     Qdrant Filter     │
│  WHERE customer_id    │           │  MatchAny(customer_id │
│  IN ['CUST-001',      │           │    = ['CUST-001',     │
│       'SYSTEM']       │           │         'SYSTEM'])    │
└───────────────────────┘           └───────────────────────┘
```

---

## Core Components

### 1. CustomerContext (`api/customer_isolation/customer_context.py`)

The central context object for request-scoped customer isolation.

```python
from api.customer_isolation import CustomerContext, CustomerAccessLevel

# Create context for a customer
context = CustomerContext(
    customer_id="CUST-001",
    namespace="acme_corp",
    access_level=CustomerAccessLevel.READ,
    include_system=True,  # Include shared CVEs, CWEs, CAPECs
    user_id="user-123",   # For audit trail
)

# Get customer IDs for filtering
customer_ids = context.get_customer_ids()
# Returns: ["CUST-001", "SYSTEM"]

# Check permissions
if context.can_write():
    # Perform write operation
    pass
```

### 2. CustomerContextManager

Thread-safe context management using Python's `contextvars`.

```python
from api.customer_isolation import CustomerContextManager

# Set context for current request
CustomerContextManager.set_context(context)

# Get context (returns None if not set)
current_context = CustomerContextManager.get_context()

# Require context (raises ValueError if not set)
required_context = CustomerContextManager.require_context()

# Clear context after request
CustomerContextManager.clear_context()
```

### 3. CustomerIsolatedSemanticService

Semantic search with automatic customer filtering.

```python
from api.customer_isolation import (
    CustomerIsolatedSemanticService,
    CustomerSemanticSearchRequest,
)

# Create service
service = CustomerIsolatedSemanticService(
    qdrant_url="http://localhost:6333",
    collection_name="ner11_gold_entities",
)

# Create search request
request = CustomerSemanticSearchRequest(
    query="ransomware attack",
    customer_id="CUST-001",
    limit=10,
    include_system=True,
    label_filter="MALWARE",  # Optional Tier 1 filter
    fine_grained_filter="RANSOMWARE",  # Optional Tier 2 filter
)

# Execute isolated search
response = service.search(request)

for result in response.results:
    print(f"{result.entity}: {result.score} (system={result.is_system})")
```

---

## API Endpoints

### Semantic Search Endpoint

```
POST /api/v2/search/semantic
```

**Headers:**
- `X-Customer-ID` (required): Customer identifier
- `X-Namespace` (optional): Customer namespace
- `X-User-ID` (optional): User identifier for audit

**Query Parameters:**
- `query` (required): Search query text
- `limit` (optional): Max results (1-100, default 10)
- `include_system` (optional): Include SYSTEM entities (default true)
- `label_filter` (optional): Tier 1 NER label filter
- `fine_grained_filter` (optional): Tier 2 fine-grained type
- `confidence_threshold` (optional): Min confidence (0-1)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v2/search/semantic?query=ransomware&limit=10" \
  -H "X-Customer-ID: CUST-001" \
  -H "X-Namespace: acme_corp"
```

**Response:**
```json
{
  "query": "ransomware",
  "customer_id": "CUST-001",
  "namespace": "acme_corp",
  "total_results": 5,
  "results": [
    {
      "entity": "WannaCry",
      "ner_label": "MALWARE",
      "fine_grained_type": "RANSOMWARE",
      "score": 0.95,
      "confidence": 0.98,
      "customer_id": "CUST-001",
      "is_system": false
    },
    {
      "entity": "CVE-2017-0144",
      "ner_label": "CVE",
      "fine_grained_type": "CVE",
      "score": 0.88,
      "confidence": 1.0,
      "customer_id": "SYSTEM",
      "is_system": true
    }
  ]
}
```

---

## Neo4j Integration

### Customer Isolation Query Pattern

```cypher
// Query entities for a specific customer including SYSTEM
MATCH (e:Entity)
WHERE e.customer_id IN ['CUST-001', 'SYSTEM']
RETURN e.name, e.ner_label, e.customer_id
ORDER BY e.confidence DESC
LIMIT 100;

// Query entities for customer ONLY (no SYSTEM)
MATCH (e:Entity)
WHERE e.customer_id = 'CUST-001'
RETURN e.name, e.ner_label
ORDER BY e.confidence DESC;

// Count entities per customer
MATCH (e:Entity)
RETURN e.customer_id, count(e) as entity_count
ORDER BY entity_count DESC;
```

### Recommended Indexes

```cypher
// Customer ID index for fast filtering
CREATE INDEX entity_customer_id IF NOT EXISTS
FOR (e:Entity) ON (e.customer_id);

// Composite index for common queries
CREATE INDEX entity_customer_label IF NOT EXISTS
FOR (e:Entity) ON (e.customer_id, e.ner_label);
```

---

## Qdrant Integration

### Customer Filter Pattern

```python
from qdrant_client.models import Filter, FieldCondition, MatchAny, MatchValue

# Include SYSTEM entities
filter_with_system = Filter(
    must=[
        FieldCondition(
            key="customer_id",
            match=MatchAny(any=["CUST-001", "SYSTEM"])
        )
    ]
)

# Exclude SYSTEM entities
filter_without_system = Filter(
    must=[
        FieldCondition(
            key="customer_id",
            match=MatchValue(value="CUST-001")
        )
    ]
)

# Execute search with filter
results = client.search(
    collection_name="ner11_gold_entities",
    query_vector=embedding,
    query_filter=filter_with_system,
    limit=10,
)
```

---

## Security Considerations

### 1. Input Validation

CustomerContext validates all inputs:
- Empty/whitespace customer_id is rejected
- Empty/whitespace namespace is rejected
- Values are automatically trimmed

```python
# These will raise ValueError
CustomerContext(customer_id="", namespace="test")      # Empty
CustomerContext(customer_id="  ", namespace="test")   # Whitespace
CustomerContext(customer_id="CUST-001", namespace="") # Empty namespace
```

### 2. Thread Isolation

Customer context uses `contextvars` for thread-safe isolation:
- Each request gets its own context
- Parallel requests cannot interfere
- Context is automatically cleared after request

### 3. Access Levels

Three access levels control operations:
- `READ`: Search and retrieve only
- `WRITE`: Search + create/update entities
- `ADMIN`: Full access including delete

```python
# Check before write operations
if not context.can_write():
    raise PermissionError("Write access required")
```

### 4. Audit Trail

All operations can be audited:

```python
audit_dict = context.to_audit_dict()
# Returns:
# {
#     "customer_id": "CUST-001",
#     "namespace": "acme_corp",
#     "access_level": "read",
#     "user_id": "user-123",
#     "session_id": null,
#     "include_system": true,
#     "timestamp": "2025-12-04T04:15:00.000Z"
# }
```

---

## Test Coverage

### Integration Tests (17/17 Passed)

| Category | Tests | Status |
|----------|-------|--------|
| Neo4j Customer Isolation | 5 | ✅ |
| Qdrant Customer Filtering | 4 | ✅ |
| Cross-Service Isolation | 3 | ✅ |
| Security Validation | 3 | ✅ |
| Data Leakage Prevention | 2 | ✅ |

### Running Tests

```bash
# Run all integration tests
python3 -m pytest tests/integration/test_customer_isolation_integration.py -v

# Run specific test category
python3 -m pytest tests/integration/test_customer_isolation_integration.py::TestNeo4jCustomerIsolation -v

# Run with coverage
python3 -m pytest tests/ --cov=api/customer_isolation --cov-report=html
```

---

## File Structure

```
5_NER11_Gold_Model/
├── api/
│   ├── __init__.py                    # Package exports
│   └── customer_isolation/
│       ├── __init__.py                # Module exports
│       ├── customer_context.py        # CustomerContext, CustomerContextManager
│       ├── isolated_semantic_service.py  # CustomerIsolatedSemanticService
│       └── semantic_router.py         # FastAPI router
├── tests/
│   ├── test_customer_semantic_search.py  # Unit tests (15 tests)
│   └── integration/
│       ├── __init__.py
│       └── test_customer_isolation_integration.py  # Integration tests (17 tests)
└── docs/
    └── CUSTOMER_LABELS_IMPLEMENTATION_GUIDE.md  # This document
```

---

## Migration Guide

### For Existing Entities

To add customer_id to existing entities:

**Neo4j:**
```cypher
// Tag all existing entities as SYSTEM (shared data)
MATCH (e:Entity)
WHERE e.customer_id IS NULL
SET e.customer_id = 'SYSTEM'
RETURN count(e) as migrated_count;
```

**Qdrant:**
```python
# Update existing points with customer_id
from qdrant_client.models import SetPayload

client.set_payload(
    collection_name="ner11_gold_entities",
    payload={"customer_id": "SYSTEM"},
    points=Filter(
        must_not=[
            FieldCondition(key="customer_id", match=MatchValue(value=""))
        ]
    ),
)
```

### For New Integrations

1. Always include `customer_id` in entity creation
2. Use `CustomerContext` for all search operations
3. Set appropriate access levels based on user role
4. Log audit trails for compliance

---

## Troubleshooting

### Common Issues

**1. "Customer context required" Error**
```python
# Solution: Ensure context is set before operations
context = CustomerContextManager.create_context(
    customer_id=request.headers.get("X-Customer-ID"),
    namespace=request.headers.get("X-Namespace"),
)
```

**2. Empty Search Results**
- Check if entities have `customer_id` field set
- Verify `include_system` is True if expecting shared data
- Confirm customer_id matches exactly (case-sensitive)

**3. Seeing Other Customer's Data**
- This should NEVER happen if filters are applied
- Check that `query_filter` is being passed to search
- Verify filter construction in logs

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-04 | Initial release - Phase B1 complete |

---

## References

- [TASKMASTER Master Index](../../../1_AEON_DT_CyberSecurity_Wiki_Current/Application_Rationalization_2025_12_3/taskmaster/00_TASKMASTER_MASTER_INDEX.md)
- [Integration Patterns Guide](../../../1_AEON_DT_CyberSecurity_Wiki_Current/Application_Rationalization_2025_12_3/guides/INTEGRATION_PATTERNS.md)
- [Phase B1 Blotter](../../../1_AEON_DT_CyberSecurity_Wiki_Current/Application_Rationalization_2025_12_3/blotter/BLOTTER.md)
