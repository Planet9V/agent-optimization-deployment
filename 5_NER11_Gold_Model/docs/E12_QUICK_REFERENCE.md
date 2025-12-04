# E12 Prioritization API Quick Reference

## Base URL
```
http://localhost:8000/api/v2/prioritization
```

## Authentication Headers
```
X-Customer-ID: customer-001     # Required
X-Access-Level: read|write|admin # Optional, default: read
X-Namespace: customer-namespace  # Optional
X-User-ID: user-123             # Optional
```

## Quick Start Examples

### 1. Calculate Priority Score
```bash
POST /score/calculate

{
  "entity_type": "vulnerability",
  "entity_id": "CVE-2024-1234",
  "entity_name": "SQL Injection",
  "urgency_factors": [{
    "factor_type": "exploit_available",
    "weight": 1.0,
    "value": 9.0,
    "description": "Public exploit"
  }],
  "risk_factors": [{
    "factor_type": "vulnerability",
    "weight": 1.0,
    "value": 9.2,
    "description": "CVSS 9.8"
  }]
}

Response: PriorityItem with category and score
```

### 2. Get NOW Items
```bash
GET /now/items?limit=50

Response: List of urgent items requiring immediate action
```

### 3. Get Dashboard
```bash
GET /dashboard/summary

Response: {
  "total_items": 147,
  "distribution": {"NOW": 23, "NEXT": 89, "NEVER": 35},
  "sla_breached": 2,
  "sla_at_risk": 8
}
```

## Endpoint Categories

### NOW (6 endpoints)
- `GET /now/items` - List NOW items
- `GET /now/summary` - NOW summary stats
- `GET /now/{item_id}/details` - Item details
- `POST /now/escalate` - Escalate to NOW
- `GET /now/sla-status` - Filter by SLA
- `POST /now/complete` - Mark complete

### NEXT (6 endpoints)
- `GET /next/items` - List NEXT items
- `GET /next/summary` - NEXT summary stats
- `GET /next/{item_id}/details` - Item details
- `POST /next/schedule` - Schedule for NEXT
- `GET /next/queue` - Ordered queue
- `POST /next/promote` - Promote to NOW

### NEVER (4 endpoints)
- `GET /never/items` - List NEVER items
- `GET /never/summary` - NEVER summary
- `POST /never/classify` - Mark as NEVER
- `POST /never/reconsider` - Reconsider item

### Scoring (6 endpoints)
- `POST /score/calculate` - Calculate priority
- `GET /score/{entity_id}/breakdown` - Score details
- `GET /score/factors` - List factors
- `POST /score/weights` - Configure weights
- `GET /score/thresholds` - Get thresholds
- `POST /score/batch` - Batch calculate

### Dashboard (6 endpoints)
- `GET /dashboard/summary` - Main dashboard
- `GET /dashboard/distribution` - Category counts
- `GET /dashboard/trends` - Historical trends
- `GET /dashboard/efficiency` - Efficiency metrics
- `GET /dashboard/backlog` - Backlog analysis
- `GET /dashboard/executive` - Executive view

## Priority Categories

| Category | Score Range | SLA | Use Case |
|----------|-------------|-----|----------|
| NOW | >= 70.0 | 24h | Immediate action required |
| NEXT | 40.0-69.9 | 7d | Planned for next cycle |
| NEVER | < 40.0 | None | Low priority/deferred |

## Scoring Factors

### Default Weights
- Risk: 30%
- Urgency: 25%
- Impact: 25%
- Effort: 10%
- ROI: 10%

### Urgency Types
- `exploit_available` - Public exploit exists
- `active_campaign` - Active attack campaign
- `compliance_deadline` - Regulatory deadline
- `business_critical` - Critical business impact
- `sla_breach` - SLA at risk
- `regulatory` - Regulatory requirement

### Risk Types
- `vulnerability` - Vulnerability score
- `threat` - Threat level
- `exposure` - Attack surface exposure
- `asset` - Asset criticality

### Economic Types
- `roi` - Return on investment
- `cost_savings` - Cost reduction
- `risk_reduction_value` - Risk mitigation value

## SLA Status

| Status | Description | Action |
|--------|-------------|--------|
| `within_sla` | On track | Monitor |
| `at_risk` | < 4h remaining | Escalate |
| `breached` | Past deadline | Immediate action |

## Common Workflows

### Create and Escalate
```bash
# 1. Calculate priority
POST /score/calculate {...}
# Returns: item_id

# 2. If needed, escalate
POST /now/escalate {"item_id": "...", "reason": "..."}
```

### Monitor SLA
```bash
# 1. Check at-risk items
GET /now/sla-status?status=at_risk

# 2. Get summary
GET /dashboard/summary
```

### Sprint Planning
```bash
# 1. Get NEXT queue
GET /next/queue?limit=50

# 2. Promote urgent items
POST /next/promote {item_id}
```

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request |
| 403 | Forbidden (access level) |
| 404 | Not found |
| 501 | Not implemented |

## Files Location

```
api/prioritization/
├── __init__.py    - Module exports
├── schemas.py     - Data models (380 lines)
├── service.py     - Business logic (467 lines)
└── router.py      - API endpoints (991 lines)
```

## Integration

### With E05 Risk Scoring
```python
# Import risk factors from E05
risk_factors = get_risk_factors_from_e05(vulnerability_id)
prioritization.calculate_priority_score(..., risk_factors=risk_factors)
```

### With E10 Economic
```python
# Import economic factors from E10
economic_factors = get_economic_analysis(remediation_id)
prioritization.calculate_priority_score(..., economic_factors=economic_factors)
```

## Qdrant Collection

- **Name:** `ner11_prioritization`
- **Vector Size:** 384 dimensions
- **Distance:** Cosine similarity
- **Auto-created:** Yes (on first use)

## Testing

```bash
# Test priority calculation
curl -X POST http://localhost:8000/api/v2/prioritization/score/calculate \
  -H "X-Customer-ID: test-customer" \
  -H "Content-Type: application/json" \
  -d @test_priority_request.json

# Test dashboard
curl http://localhost:8000/api/v2/prioritization/dashboard/summary \
  -H "X-Customer-ID: test-customer"
```

## Documentation

- **Full Implementation:** E12_PRIORITIZATION_IMPLEMENTATION.md
- **API Reference:** This file
- **Architecture:** ENHANCEMENT_IMPLEMENTATION_ORDER.json

---

**Quick Links:**
- [Full Implementation Guide](./E12_PRIORITIZATION_IMPLEMENTATION.md)
- [AEON Enhancement Order](./ENHANCEMENT_IMPLEMENTATION_ORDER.json)
- [NER11 Architecture](./NER11_ARCHITECTURE_ANALYSIS.md)
