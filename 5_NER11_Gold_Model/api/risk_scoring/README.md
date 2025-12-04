# E05: Risk Scoring Engine API - Data Models

**Status**: ✅ Complete  
**Created**: 2025-12-04  
**Version**: 1.0.0

## Overview

Multi-factor risk scoring models for comprehensive risk assessment across assets, vulnerabilities, threats, and exposures.

## Data Models

### 1. RiskScore
**Purpose**: Multi-factor risk calculation for entities

**Key Features**:
- Composite risk scoring (0.0-10.0 scale)
- Component scores: vulnerability, threat, exposure, asset
- Risk level classification (LOW, MEDIUM, HIGH, CRITICAL)
- Trend analysis with previous score comparison
- Contributing factors tracking
- Confidence scoring (0.0-1.0)

**Use Cases**:
- Overall entity risk assessment
- Risk trend monitoring
- Risk-based prioritization
- Compliance reporting

### 2. RiskFactor
**Purpose**: Individual risk factor contributing to overall score

**Key Features**:
- Factor types: VULNERABILITY, THREAT, EXPOSURE, ASSET, COMPLIANCE
- Weight and score (0.0-10.0)
- Evidence tracking
- Remediation availability

**Use Cases**:
- Risk factor decomposition
- Evidence-based risk scoring
- Remediation planning

### 3. AssetCriticality
**Purpose**: Asset criticality assessment for risk calculation

**Key Features**:
- Criticality levels: LOW → MISSION_CRITICAL
- Business impact classification
- Data classification (PUBLIC → TOP_SECRET)
- Availability requirements (STANDARD → CRITICAL)
- Dependency tracking
- RTO/RPO objectives

**Use Cases**:
- Asset prioritization
- Business impact analysis
- Recovery planning
- Risk weighting

### 4. ExposureScore
**Purpose**: Attack surface exposure assessment

**Key Features**:
- External/internet-facing detection
- Open ports and exposed services
- Attack surface area classification
- Network segment context
- Security controls tracking
- Scan metadata

**Use Cases**:
- Attack surface management
- Exposure reduction
- Network security assessment
- Perimeter monitoring

### 5. RiskAggregation
**Purpose**: Aggregated risk for entity groups

**Key Features**:
- Aggregation types: VENDOR, SECTOR, ASSET_TYPE, DEPARTMENT
- Statistical risk metrics (avg, max, min)
- Entity counts and distributions
- High-risk and critical counts
- Trend analysis

**Use Cases**:
- Portfolio risk management
- Vendor risk reporting
- Department risk overview
- Executive dashboards

## Enumerations

### Risk Classification
- **RiskLevel**: LOW, MEDIUM, HIGH, CRITICAL
- **RiskFactorType**: VULNERABILITY, THREAT, EXPOSURE, ASSET, COMPLIANCE
- **RiskTrend**: IMPROVING, STABLE, DEGRADING

### Asset Criticality
- **CriticalityLevel**: LOW, MEDIUM, HIGH, CRITICAL, MISSION_CRITICAL
- **BusinessImpact**: MINIMAL, MODERATE, SIGNIFICANT, SEVERE, CATASTROPHIC
- **DataClassification**: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, TOP_SECRET
- **AvailabilityRequirement**: STANDARD, IMPORTANT, ESSENTIAL, CRITICAL

### Exposure Assessment
- **AttackSurfaceArea**: MINIMAL, LIMITED, MODERATE, EXTENSIVE, CRITICAL

### Aggregation
- **AggregationType**: VENDOR, SECTOR, ASSET_TYPE, DEPARTMENT

## Implementation Details

### File Structure
```
api/risk_scoring/
├── __init__.py          # Public API exports
└── risk_models.py       # Data model implementations
```

### Line Counts
- `__init__.py`: 49 lines
- `risk_models.py`: 610 lines
- **Total**: 659 lines

### Key Design Patterns

1. **Multi-Factor Scoring**: RiskScore combines 4 component scores
2. **Automatic Classification**: Risk levels auto-calculated from numeric scores
3. **Trend Analysis**: Score change tracking and trend calculation
4. **Evidence Tracking**: Supporting evidence for risk factors
5. **Qdrant Integration**: Full vector DB payload support

### Validation Rules

- All IDs and customer_id required (multi-tenant isolation)
- Scores must be 0.0-10.0 range
- Confidence must be 0.0-1.0 range
- Factor weights must be 0.0-1.0
- Auto-calculation of risk levels from scores

### Serialization Support

All models include:
- `to_dict()`: Full API response format
- `to_qdrant_payload()`: Optimized vector DB format

## Testing

✅ All models tested and validated:
- Import verification
- Model instantiation
- Property calculations
- Serialization methods
- Validation rules

## Integration Points

### Dependencies
- **E02**: Asset classification data
- **E03**: Vulnerability data from SBOM
- **E04**: Threat intelligence data
- **E06**: Network topology data

### Consumers
- **E07**: Risk-based alerting
- **E13**: Compliance scoring
- **E14**: Security metrics
- **Dashboard**: Risk visualization

## Usage Examples

### Risk Score Calculation
```python
from api.risk_scoring import RiskScore, RiskFactor, RiskLevel

# Create risk factors
vuln_factor = RiskFactor(
    factor_id="RF001",
    factor_type=RiskFactorType.VULNERABILITY,
    name="Critical CVE",
    description="CVE-2024-1234",
    weight=0.8,
    score=9.5
)

# Calculate overall risk
risk = RiskScore(
    risk_score_id="RS001",
    customer_id="CUST001",
    entity_type="asset",
    entity_id="ASSET001",
    entity_name="Production Server",
    overall_score=8.5,
    vulnerability_score=9.0,
    threat_score=7.5,
    exposure_score=8.0,
    asset_score=9.5,
    contributing_factors=[vuln_factor]
)

# Check risk level
if risk.is_critical:
    print(f"CRITICAL risk detected: {risk.entity_name}")
```

### Asset Criticality Assessment
```python
from api.risk_scoring import AssetCriticality, CriticalityLevel

criticality = AssetCriticality(
    asset_id="ASSET001",
    customer_id="CUST001",
    asset_name="Production Database",
    asset_type="database",
    criticality_score=9.5,
    business_impact=BusinessImpact.CATASTROPHIC,
    data_classification=DataClassification.RESTRICTED,
    recovery_time_objective_hours=2.0
)

if criticality.is_mission_critical:
    print("Mission-critical asset requires immediate attention")
```

### Exposure Assessment
```python
from api.risk_scoring import ExposureScore

exposure = ExposureScore(
    exposure_id="EXP001",
    customer_id="CUST001",
    asset_id="ASSET001",
    asset_name="Web Server",
    external_exposure=True,
    internet_facing=True,
    open_ports=[80, 443],
    exposure_score=7.5,
    security_controls=["WAF", "Firewall"]
)

if exposure.is_high_exposure:
    print(f"High exposure detected: {exposure.open_port_count} open ports")
```

### Risk Aggregation
```python
from api.risk_scoring import RiskAggregation, AggregationType

aggregation = RiskAggregation(
    aggregation_id="AGG001",
    customer_id="CUST001",
    aggregation_type=AggregationType.VENDOR,
    group_name="Vendor ABC",
    group_id="VENDOR001",
    average_risk_score=6.5,
    entity_count=10,
    high_risk_count=3
)

print(f"Vendor risk: {aggregation.high_risk_percentage:.1f}% high risk")
```

## Next Steps

1. **API Endpoints** (Day 2-3): Implement FastAPI endpoints
2. **Risk Calculation** (Day 4-5): Risk scoring algorithms
3. **Qdrant Integration** (Day 6-7): Vector storage and retrieval
4. **Testing** (Day 8-9): Comprehensive test suite
5. **Documentation** (Day 10): API documentation and guides

## Notes

- Follow existing model patterns from E03 (SBOM) and E15 (Vendor)
- Multi-tenant isolation via customer_id on all models
- Auto-calculation of risk levels from numeric scores
- Trend analysis requires previous score tracking
- Evidence tracking for audit and compliance
