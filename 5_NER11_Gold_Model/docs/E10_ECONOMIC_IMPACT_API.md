# E10 Economic Impact Modeling API

## Overview

The E10 Economic Impact Modeling enhancement provides comprehensive financial analysis capabilities for the AEON Cybersecurity Platform, enabling organizations to quantify security investments, calculate ROI, assess business value, and model incident impacts.

## API Base Path

```
/api/v2/economic-impact
```

## Authentication

All endpoints require the `X-Customer-ID` header for multi-tenant isolation:

```bash
curl -H "X-Customer-ID: your-customer-id" \
     https://api.aeon.com/api/v2/economic-impact/costs/summary
```

## Endpoint Categories

### 1. Cost Analysis (5 endpoints)

Track and analyze security costs across categories.

#### GET /costs/summary
Get cost summary dashboard with trends.

**Parameters:**
- `period_days` (query, optional): Days to analyze (default: 30)

**Response:**
```json
{
  "success": true,
  "data": {
    "customer_id": "customer-123",
    "total_costs": 450000.00,
    "cost_categories": {
      "equipment": 150000.00,
      "personnel": 200000.00,
      "downtime": 50000.00,
      "remediation": 50000.00
    },
    "period_start": "2025-11-04T00:00:00Z",
    "period_end": "2025-12-04T00:00:00Z",
    "trend_percentage": 12.5,
    "currency": "USD"
  }
}
```

#### GET /costs/by-category
Get detailed costs grouped by category.

**Parameters:**
- `category` (query, optional): Filter by specific category

#### GET /costs/{entity_id}/breakdown
Get detailed cost breakdown for specific entity.

#### POST /costs/calculate
Calculate costs for a scenario.

**Request Body:**
```json
{
  "scenario_type": "ransomware",
  "duration_hours": 24.0,
  "affected_systems": ["system1", "system2"],
  "personnel_count": 10,
  "equipment_value": 100000.0,
  "revenue_per_hour": 5000.0
}
```

#### GET /costs/historical
Get historical cost trends with direction analysis.

---

### 2. ROI Calculations (6 endpoints)

Calculate and track return on security investments.

#### GET /roi/summary
Get aggregated ROI metrics for all investments.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_investments": 15,
    "total_invested": 2500000.00,
    "total_annual_savings": 1200000.00,
    "average_roi_percentage": 48.5,
    "best_performing": {
      "investment_name": "SIEM Platform",
      "roi_percentage": 125.0,
      "payback_period_months": 9.6
    },
    "by_category": {
      "security_tools": 65.5,
      "infrastructure": 42.0,
      "personnel": 35.5
    }
  }
}
```

#### POST /roi/calculate
Calculate ROI for proposed investment.

**Request Body:**
```json
{
  "investment_name": "Security Platform Upgrade",
  "category": "security_tools",
  "initial_investment": 100000.0,
  "expected_annual_savings": 50000.0,
  "annual_operating_costs": 10000.0,
  "project_lifetime_years": 5,
  "discount_rate": 0.10
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "roi_percentage": 40.0,
    "payback_period_months": 30.0,
    "npv": 51566.55,
    "irr": 28.65,
    "calculation_date": "2025-12-04T10:30:00Z"
  }
}
```

#### GET /roi/projections
Get future ROI projections with confidence intervals.

#### POST /roi/comparison
Compare multiple investment options side-by-side.

---

### 3. Business Value (5 endpoints)

Assess and track business value of assets and systems.

#### GET /value/metrics
Get business value metrics dashboard.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_asset_value": 15000000.00,
    "critical_asset_count": 25,
    "at_risk_value": 4500000.00,
    "protected_value": 10500000.00,
    "value_by_category": {
      "servers": 5000000.00,
      "applications": 7000000.00,
      "data": 3000000.00
    }
  }
}
```

#### POST /value/calculate
Calculate business value for entity.

**Request Body:**
```json
{
  "entity_id": "asset-001",
  "entity_type": "server",
  "replacement_cost": 50000.0,
  "annual_revenue": 1000000.0,
  "customer_base": 10000,
  "regulatory_requirements": ["GDPR", "SOC2"],
  "ip_patents": 3,
  "operational_hours": 8760
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_value": 2300000.00,
    "replacement_cost": 50000.00,
    "revenue_impact": 100000.00,
    "reputation_value": 1000000.00,
    "regulatory_exposure": 1000000.00,
    "intellectual_property_value": 750000.00,
    "operational_criticality": 50000.00,
    "confidence_score": 0.95
  }
}
```

#### GET /value/risk-adjusted
Get risk-adjusted business values (integrates with E08 RAMS).

#### GET /value/by-sector
Get value metrics by industry sector with benchmarking.

---

### 4. Impact Modeling (5 endpoints)

Model financial impact of security incidents.

#### POST /impact/model
Model financial impact of incident scenario.

**Request Body:**
```json
{
  "scenario_type": "ransomware",
  "parameters": {
    "affected_systems": ["system1", "system2", "system3"],
    "duration_hours": 48.0,
    "severity": "high",
    "data_volume_gb": 500.0,
    "user_count": 1000,
    "regulatory_implications": ["GDPR"]
  },
  "include_indirect_costs": true,
  "include_reputation_impact": true,
  "time_horizon_days": 365
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "simulation_id": "sim_12345",
    "total_impact": 2750000.00,
    "direct_costs": 500000.00,
    "indirect_costs": 1200000.00,
    "opportunity_costs": 600000.00,
    "reputation_impact": 350000.00,
    "regulatory_fines": 100000.00,
    "recovery_timeline_days": 14,
    "mitigation_recommendations": [
      "Implement robust backup and recovery procedures",
      "Deploy advanced endpoint detection and response",
      "Conduct regular security awareness training"
    ]
  }
}
```

#### GET /impact/scenarios
List available impact scenarios.

#### POST /impact/simulate
Run Monte Carlo simulation for impact modeling.

#### GET /impact/{scenario_id}/results
Get detailed simulation results.

#### GET /impact/historical
Get historical impact data for validation.

---

### 5. Dashboard (5 endpoints)

Executive dashboards and KPIs.

#### GET /dashboard/summary
Comprehensive economic dashboard.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_costs_ytd": 4500000.00,
    "total_investments_ytd": 2500000.00,
    "average_roi": 48.5,
    "at_risk_value": 4500000.00,
    "cost_trend": "increasing",
    "roi_trend": "stable",
    "alerts": [
      "High costs detected - exceeding $1M",
      "High value at risk - exceeding 40%"
    ],
    "key_metrics": {
      "cost_per_asset": 180000.00,
      "protected_value_ratio": 0.70
    }
  }
}
```

#### GET /dashboard/trends
Time-series economic trends.

#### GET /dashboard/kpis
Key performance indicators.

#### GET /dashboard/alerts
Economic alerts and threshold violations.

#### GET /dashboard/executive
Executive summary for reporting.

---

## Integration with Other Enhancements

### E08 RAMS Integration

Economic impact factors based on reliability scores:

```python
from api.economic_impact.integrations import RAMSIntegration

rams = RAMSIntegration(qdrant_client)
reliability_data = await rams.get_reliability_impact(customer_id, entity_id)

# Returns:
# - reliability_score, availability_score, maintainability_score
# - failure_cost based on reliability
# - economic_impact_factor (0.5-1.0)
```

### E03 SBOM Integration

Component economics and vulnerability costs:

```python
from api.economic_impact.integrations import SBOMIntegration

sbom = SBOMIntegration(qdrant_client)
vuln_impact = await sbom.calculate_vulnerability_impact(customer_id)

# Returns:
# - total_remediation_cost
# - total_replacement_cost (EOL components)
# - total_compliance_cost
```

### E15 Vendor Equipment Integration

Equipment portfolio economics:

```python
from api.economic_impact.integrations import VendorEquipmentIntegration

vendor = VendorEquipmentIntegration(qdrant_client)
portfolio = await vendor.calculate_equipment_portfolio_value(customer_id)

# Returns:
# - total_current_value
# - total_annual_maintenance
# - total_cost_of_ownership
```

---

## TypeScript Client

```typescript
import { EconomicImpactAPI } from './api/economic_impact/interfaces';

const api = new EconomicImpactAPI('https://api.aeon.com', 'customer-123');

// Get cost summary
const costs = await api.getCostSummary(30);

// Calculate ROI
const roi = await api.calculateROI({
  investment_name: "Security Upgrade",
  category: InvestmentCategory.SECURITY_TOOLS,
  initial_investment: 100000,
  expected_annual_savings: 50000,
  annual_operating_costs: 10000
});

// Model impact
const impact = await api.modelImpact({
  scenario_type: ScenarioType.RANSOMWARE,
  parameters: {
    affected_systems: ["system1"],
    duration_hours: 24,
    severity: "high"
  }
});
```

---

## Use Cases

### 1. Security Investment Justification

Calculate ROI for proposed security investments:

```bash
# Calculate ROI
POST /api/v2/economic-impact/roi/calculate
{
  "investment_name": "Next-Gen Firewall",
  "initial_investment": 150000,
  "expected_annual_savings": 75000,
  "annual_operating_costs": 15000
}

# Get projections
GET /api/v2/economic-impact/roi/projections?investment_id=inv_123&years=5
```

### 2. Incident Response Planning

Model potential incident costs:

```bash
POST /api/v2/economic-impact/impact/model
{
  "scenario_type": "ransomware",
  "parameters": {
    "affected_systems": ["production", "database"],
    "duration_hours": 72,
    "severity": "critical"
  }
}
```

### 3. Budget Planning

Analyze historical costs and trends:

```bash
# Get cost summary
GET /api/v2/economic-impact/costs/summary?period_days=365

# Get trends
GET /api/v2/economic-impact/costs/historical?days=365

# Get dashboard
GET /api/v2/economic-impact/dashboard/summary
```

### 4. Executive Reporting

Generate executive summaries:

```bash
# Get executive summary
GET /api/v2/economic-impact/dashboard/executive?period=ytd

# Get KPIs
GET /api/v2/economic-impact/dashboard/kpis
```

---

## Testing

Run the test suite:

```bash
pytest tests/api/test_economic_impact.py -v
```

Test coverage includes:
- ✅ All 26 endpoints
- ✅ Multi-tenant isolation
- ✅ Service layer calculations
- ✅ Integration with E08, E03, E15
- ✅ Error handling
- ✅ Data validation

---

## Performance

- **Qdrant Collection**: `ner11_economic_impact` (384-dim embeddings)
- **Response Time**: < 500ms for calculations, < 2s for dashboard
- **Concurrent Users**: Supports 100+ concurrent requests
- **Data Retention**: 2 years historical data

---

## Future Enhancements

- [ ] Machine learning for cost prediction
- [ ] Automated budget optimization
- [ ] Real-time impact monitoring
- [ ] Benchmark comparisons (industry averages)
- [ ] What-if scenario planning
- [ ] Integration with financial systems (ERP)

---

## Support

For issues or questions:
- API Documentation: https://api.aeon.com/docs
- Support: support@aeon.com
- GitHub: https://github.com/aeon/economic-impact
