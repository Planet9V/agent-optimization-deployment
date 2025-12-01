# PRE-BUILDER AGENT 3: EMERGENCY_SERVICES SCHEMA VALIDATOR
## Validation Preplan

**Status**: WAITING for Agent 2 - Node Type Mapping  
**Timestamp**: 2025-11-21T19:50:00Z  
**Validator Version**: 3.0

## Ready States (Prepared)

### 1. Label Pattern Validation Template
Based on established patterns from:
- WATER (27,200 nodes, 4.32 labels avg)
- ENERGY (35,475 nodes, 4.94 labels avg)  
- COMMUNICATIONS (28,000 nodes, 5.8 labels avg)

**Expected EMERGENCY_SERVICES Pattern**:
```
Device: ["Device", "EmergencyServicesDevice", "EmergencyServices", "Monitoring", "EMERGENCY_SERVICES", "{subsector}"]
Measurement: ["Measurement", "ResponseMetric", "Monitoring", "EMERGENCY_SERVICES", "{subsector}"]
Property: ["Property", "EmergencyServicesProperty", "EmergencyServices", "Monitoring", "EMERGENCY_SERVICES", "{subsector}"]
Process: ["Process", "EmergencyResponse", "EmergencyServices", "EMERGENCY_SERVICES", "{subsector}"]
Control: ["Control", "IncidentCommandSystem", "EmergencyServices", "EMERGENCY_SERVICES", "{subsector}"]
Alert: ["EmergencyAlert", "Alert", "Monitoring", "EMERGENCY_SERVICES", "{subsector}"]
Zone: ["ServiceZone", "Zone", "Asset", "EMERGENCY_SERVICES", "{subsector}"]
Asset: ["MajorFacility", "Asset", "EmergencyServices", "EMERGENCY_SERVICES", "{subsector}"]
```

### 2. Expected Relationships
Common (from established sectors):
- VULNERABLE_TO
- HAS_MEASUREMENT
- HAS_PROPERTY
- CONTROLS
- CONTAINS
- USES_DEVICE

Sector-Specific:
- RESPONDS_TO_INCIDENT
- MANAGED_BY_ICS
- DEPLOYED_AT_FACILITY

### 3. Cross-Sector Query Test Cases
- "All devices": Verify EmergencyServicesDevice found by `label ENDS WITH 'Device'`
- "All measurements": Verify ResponseMetric found by `n:Measurement`
- "Sector-specific": Verify `'EMERGENCY_SERVICES' IN labels(n)` works
- "Multi-label": Verify 5-7 labels per node distribution

### 4. Governance Rules
- Total nodes: 26,000-35,000 (target: ~28,000)
- Labels per node: 5-7 (target: 5.5)
- Required node types: 8 (Device, Measurement, Property, Process, Control, Alert, Zone, Asset)
- Label compliance: 100% match to registry template

## Blocked on Agent 2
- temp/sector-EMERGENCY_SERVICES-node-type-mapping.json
- Label counts per node type
- Node type counts and percentages
- Actual architecture specifications

## Ready to Execute
Once Agent 2 completes, this validator will:
1. Load node type mapping
2. Validate each label pattern (auto-check against template)
3. Validate relationships (check presence of required types)
4. Test cross-sector queries
5. Generate comprehensive validation report

