# AEON Cyber Digital Twin - Safety Compliance API Documentation

**File:** API_SAFETY_COMPLIANCE.md
**Created:** 2025-11-30
**Version:** 1.0.0
**Status:** COMPLETE
**Enhancements:** E7 (IEC 62443), E8 (RAMS Reliability), E9 (FMEA Hazard)
**Document Length:** 1000+ lines

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [API Overview](#api-overview)
3. [IEC 62443 Safety Zones API](#iec-62443-safety-zones-api)
4. [Foundational Requirements API](#foundational-requirements-api)
5. [Security Level Gap Analysis API](#security-level-gap-analysis-api)
6. [RAMS Reliability API](#rams-reliability-api)
7. [FMEA Failure Modes API](#fmea-failure-modes-api)
8. [Conduit Security API](#conduit-security-api)
9. [Compliance Assessment API](#compliance-assessment-api)
10. [Neo4j Cypher Queries](#neo4j-cypher-queries)
11. [Frontend Integration](#frontend-integration)
12. [Error Handling](#error-handling)

---

## Executive Summary

The **Safety Compliance API** provides comprehensive industrial safety and reliability analysis for the AEON Cyber Digital Twin. This API integrates three critical enhancement areas:

**E7 - IEC 62443 Industrial Safety**:
- Security zone modeling (Purdue Levels 0-4)
- Security Levels (SL1-SL4) target vs achieved analysis
- Foundational Requirements (FR1-FR7) compliance tracking
- Conduit security assessment

**E8 - RAMS Reliability**:
- Mean Time Between Failures (MTBF)
- Mean Time To Repair (MTTR)
- Availability calculations
- Safety Integrity Level (SIL) ratings

**E9 - FMEA Hazard Analysis**:
- Failure Mode Effects Analysis
- Risk Priority Number (RPN) scoring
- Criticality assessment
- Mitigation recommendations

**Key Statistics**:
- **29,774+ Industrial Equipment** nodes with safety data
- **5 Purdue Levels** (0-4) with zone classification
- **4 Security Levels** (SL1-SL4) per IEC 62443
- **7 Foundational Requirements** (FR1-FR7) tracked
- **SIL Ratings** (SIL1-SIL4) for safety-critical systems

---

## API Overview

### Base URL
```
https://api.aeon-dt.local/api/v1/safety
```

### API Endpoints

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/zones` | GET | List all safety zones | 1-2 seconds |
| `/zones/{zoneId}` | GET | Zone details and equipment | 500-800ms |
| `/zones/{zoneId}/gap-analysis` | GET | SL-T vs SL-A gap analysis | 2-4 seconds |
| `/requirements` | GET | Foundational requirements list | 300-500ms |
| `/requirements/{frId}/controls` | GET | FR control implementation status | 1-2 seconds |
| `/rams/equipment/{equipmentId}` | GET | RAMS metrics for equipment | 500-800ms |
| `/rams/sector/{sectorId}` | GET | Sector-wide reliability metrics | 2-4 seconds |
| `/fmea/equipment/{equipmentId}/failure-modes` | GET | FMEA failure modes | 1-3 seconds |
| `/fmea/rpn-scores` | GET | RPN scoring across assets | 2-5 seconds |
| `/conduits` | GET | List conduit connections | 1-2 seconds |
| `/conduits/{conduitId}` | GET | Conduit security details | 500-800ms |
| `/compliance/assess` | POST | Run compliance assessment | 5-15 seconds |

---

## IEC 62443 Safety Zones API

### List Safety Zones

```
GET /api/v1/safety/zones
```

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `purdue_level` | number | all | Filter by Purdue level (0-4) |
| `compliance_status` | string | all | Filter: `COMPLIANT`, `NON_COMPLIANT`, `PARTIAL` |
| `min_risk_score` | number | 0 | Minimum risk score filter |
| `sector` | string | all | Filter by sector |

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:00:00Z",
  "total_zones": 47,
  "zones": [
    {
      "zone_id": "ZONE-L0-PROCESS-001",
      "name": "Chemical Reactor Process Control",
      "purdue_level": 0,
      "security_level_target": 4,
      "security_level_achieved": 3,
      "security_level_gap": 1,
      "criticality": "SAFETY_CRITICAL",
      "compliance_status": "NON_COMPLIANT",
      "asset_count": 234,
      "sil_rating": 3,
      "risk_score": 8.7,
      "last_assessment": "2025-11-20T00:00:00Z",
      "next_assessment": "2026-02-20T00:00:00Z"
    },
    {
      "zone_id": "ZONE-L1-CONTROL-001",
      "name": "PLC Control Network",
      "purdue_level": 1,
      "security_level_target": 3,
      "security_level_achieved": 3,
      "security_level_gap": 0,
      "criticality": "HIGH",
      "compliance_status": "COMPLIANT",
      "asset_count": 89,
      "risk_score": 5.2,
      "last_assessment": "2025-11-15T00:00:00Z"
    }
  ],
  "summary": {
    "by_purdue_level": {
      "level_0": 5,
      "level_1": 12,
      "level_2": 8,
      "level_3": 15,
      "level_4": 7
    },
    "compliance_breakdown": {
      "compliant": 28,
      "non_compliant": 12,
      "partial": 7
    },
    "average_gap": 0.8
  }
}
```

### Get Zone Details

```
GET /api/v1/safety/zones/{zoneId}
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:05:00Z",
  "zone": {
    "zone_id": "ZONE-L0-PROCESS-001",
    "name": "Chemical Reactor Process Control",
    "description": "Safety-critical process control for chemical reactor systems",
    "purdue_level": 0,
    "security_levels": {
      "target": 4,
      "achieved": 3,
      "gap": 1,
      "gap_description": "Missing SL4 controls: HSM authentication, quantum-safe crypto"
    },
    "criticality": {
      "rating": "SAFETY_CRITICAL",
      "consequence_of_loss": "CATASTROPHIC",
      "safety_instrumented": true,
      "sil_rating": 3
    },
    "equipment": {
      "total_count": 234,
      "certified_count": 198,
      "non_compliant_count": 36,
      "by_type": {
        "PLCs": 45,
        "RTUs": 23,
        "Sensors": 156,
        "Actuators": 10
      }
    },
    "allowed_protocols": ["Modbus Serial", "HART", "Profibus"],
    "external_connectivity": false,
    "foundational_requirements": {
      "FR1_compliance": 85,
      "FR2_compliance": 90,
      "FR3_compliance": 78,
      "FR4_compliance": 65,
      "FR5_compliance": 95,
      "FR6_compliance": 72,
      "FR7_compliance": 88
    },
    "risk_assessment": {
      "risk_score": 8.7,
      "threat_likelihood": 7.5,
      "vulnerability_severity": 8.0,
      "consequence_impact": 9.0,
      "mitigation_priority": "URGENT"
    },
    "connected_zones": [
      {
        "zone_id": "ZONE-L1-CONTROL-001",
        "conduit_id": "CONDUIT-L0-L1-001",
        "direction": "upstream"
      }
    ],
    "assessments": {
      "last_performed": "2025-11-20T00:00:00Z",
      "next_scheduled": "2026-02-20T00:00:00Z",
      "assessor": "Industrial Security Consulting",
      "findings_count": 12
    }
  }
}
```

### Security Level Gap Analysis

```
GET /api/v1/safety/zones/{zoneId}/gap-analysis
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:10:00Z",
  "zone_id": "ZONE-L0-PROCESS-001",
  "gap_analysis": {
    "target_level": 4,
    "achieved_level": 3,
    "gap_severity": "HIGH",
    "remediation_cost_usd": 125000,
    "remediation_time_days": 90,
    "gaps_by_requirement": [
      {
        "requirement_id": "FR1",
        "requirement_name": "Identification and Authentication Control",
        "target_controls": 12,
        "implemented_controls": 8,
        "gap_count": 4,
        "missing_controls": [
          "HSM-based cryptographic authentication",
          "Continuous authentication monitoring",
          "Zero-trust architecture implementation",
          "Quantum-resistant authentication"
        ],
        "remediation_cost_usd": 45000,
        "remediation_priority": "CRITICAL"
      },
      {
        "requirement_id": "FR4",
        "requirement_name": "Data Confidentiality",
        "target_controls": 8,
        "implemented_controls": 5,
        "gap_count": 3,
        "missing_controls": [
          "End-to-end encryption",
          "Hardware security modules",
          "Quantum-safe cryptography"
        ],
        "remediation_cost_usd": 35000,
        "remediation_priority": "HIGH"
      }
    ],
    "equipment_gaps": [
      {
        "equipment_id": "HMI-LEGACY-001",
        "equipment_name": "Legacy HMI Panel",
        "current_sl": 1,
        "required_sl": 4,
        "gap": 3,
        "remediation": "REPLACE",
        "replacement_model": "Siemens HMI Comfort Panel",
        "cost_usd": 4500
      }
    ],
    "remediation_roadmap": {
      "phase_1": {
        "duration_days": 30,
        "cost_usd": 45000,
        "description": "Implement HSM and PKI infrastructure",
        "risk_reduction": 2.5
      },
      "phase_2": {
        "duration_days": 45,
        "cost_usd": 55000,
        "description": "Replace legacy equipment and implement encryption",
        "risk_reduction": 1.8
      },
      "phase_3": {
        "duration_days": 15,
        "cost_usd": 25000,
        "description": "Zero-trust architecture finalization",
        "risk_reduction": 0.7
      }
    }
  }
}
```

---

## Foundational Requirements API

### List Foundational Requirements

```
GET /api/v1/safety/requirements
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:15:00Z",
  "foundational_requirements": [
    {
      "requirement_id": "FR1",
      "name": "Identification and Authentication Control",
      "description": "Control access through identification and authentication of users/devices",
      "controls_by_level": {
        "SL1": ["Unique user IDs", "Password authentication", "Basic ACLs"],
        "SL2": ["MFA", "Device certificates", "Account lockout", "Password policy"],
        "SL3": ["Hardware tokens", "PKI", "Biometrics", "PAM"],
        "SL4": ["HSM", "Continuous auth", "Zero-trust", "Quantum-safe"]
      },
      "overall_compliance": 72.5,
      "zones_compliant": 28,
      "zones_non_compliant": 19
    },
    {
      "requirement_id": "FR2",
      "name": "Use Control",
      "description": "Enforce authorization of user and device activities",
      "controls_by_level": {
        "SL1": ["Role-based access control"],
        "SL2": ["Least privilege", "Permission auditing"],
        "SL3": ["Separation of duties", "Session monitoring"],
        "SL4": ["Dynamic access control", "Behavior-based auth"]
      },
      "overall_compliance": 78.3
    },
    {
      "requirement_id": "FR3",
      "name": "System Integrity",
      "description": "Ensure IACS integrity and prevent unauthorized changes",
      "overall_compliance": 65.8
    },
    {
      "requirement_id": "FR4",
      "name": "Data Confidentiality",
      "description": "Protect information from unauthorized disclosure",
      "overall_compliance": 58.2
    },
    {
      "requirement_id": "FR5",
      "name": "Restricted Data Flow",
      "description": "Segment networks and control information flow",
      "overall_compliance": 82.1
    },
    {
      "requirement_id": "FR6",
      "name": "Timely Response to Events",
      "description": "Detect and respond to security events promptly",
      "overall_compliance": 69.4
    },
    {
      "requirement_id": "FR7",
      "name": "Resource Availability",
      "description": "Ensure availability of IACS resources",
      "overall_compliance": 85.7
    }
  ]
}
```

### Get FR Control Status

```
GET /api/v1/safety/requirements/{frId}/controls
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:20:00Z",
  "requirement_id": "FR1",
  "requirement_name": "Identification and Authentication Control",
  "control_status": {
    "by_zone": [
      {
        "zone_id": "ZONE-L0-PROCESS-001",
        "zone_name": "Chemical Reactor Process Control",
        "target_level": 4,
        "implemented_controls": [
          "Unique user IDs",
          "Password authentication",
          "MFA",
          "Device certificates",
          "Hardware tokens",
          "PKI"
        ],
        "missing_controls": [
          "HSM cryptographic auth",
          "Continuous auth monitoring",
          "Zero-trust implementation",
          "Quantum-safe methods"
        ],
        "compliance_percentage": 66.7,
        "remediation_cost_usd": 45000
      }
    ],
    "aggregate_statistics": {
      "total_controls_required": 156,
      "total_controls_implemented": 113,
      "overall_compliance": 72.4,
      "total_remediation_cost_usd": 892000
    }
  }
}
```

---

## RAMS Reliability API

### Equipment RAMS Metrics

```
GET /api/v1/safety/rams/equipment/{equipmentId}
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:25:00Z",
  "equipment_id": "PLC-SIEMENS-001",
  "equipment_name": "Siemens S7-1500 PLC",
  "rams_metrics": {
    "reliability": {
      "mtbf_hours": 87600,
      "mtbf_description": "10 years expected operation",
      "failure_rate_per_million_hours": 11.4,
      "reliability_at_8760h": 0.905
    },
    "availability": {
      "target_uptime_percent": 99.95,
      "actual_uptime_percent": 99.92,
      "downtime_hours_ytd": 7.0,
      "availability_class": "HIGH_AVAILABILITY"
    },
    "maintainability": {
      "mttr_hours": 2.5,
      "spare_parts_availability": "IN_STOCK",
      "maintenance_contract": true,
      "remote_diagnostics": true,
      "predictive_maintenance": true
    },
    "safety": {
      "sil_rating": 3,
      "sil_certified": true,
      "certification_body": "TUV SUD",
      "certification_expiry": "2027-06-15T00:00:00Z",
      "pfd_avg": 0.0001,
      "safe_failure_fraction": 0.92
    },
    "failure_history": {
      "total_failures": 3,
      "last_failure": "2025-08-15T14:30:00Z",
      "failure_causes": [
        {"cause": "Power surge", "count": 2},
        {"cause": "Firmware bug", "count": 1}
      ]
    },
    "maintenance_schedule": {
      "next_scheduled": "2025-12-15T00:00:00Z",
      "type": "Preventive",
      "estimated_downtime_hours": 4
    }
  }
}
```

### Sector RAMS Summary

```
GET /api/v1/safety/rams/sector/{sectorId}
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:30:00Z",
  "sector_id": "energy",
  "sector_name": "Energy Sector",
  "rams_summary": {
    "total_equipment": 4521,
    "reliability_metrics": {
      "average_mtbf_hours": 52560,
      "lowest_mtbf_equipment": "RTU-LEGACY-042",
      "highest_failure_rate_type": "Legacy RTUs"
    },
    "availability_metrics": {
      "sector_availability": 99.87,
      "equipment_below_target": 23,
      "total_downtime_hours_ytd": 1247
    },
    "maintainability_metrics": {
      "average_mttr_hours": 4.2,
      "equipment_with_contracts": 4102,
      "predictive_maintenance_enabled": 2847
    },
    "safety_metrics": {
      "sil1_equipment": 1234,
      "sil2_equipment": 2156,
      "sil3_equipment": 987,
      "sil4_equipment": 144,
      "uncertified_equipment": 347
    },
    "risk_equipment": [
      {
        "equipment_id": "RTU-LEGACY-042",
        "issue": "MTBF below threshold",
        "mtbf_hours": 8760,
        "recommendation": "Replace with modern RTU"
      }
    ]
  }
}
```

---

## FMEA Failure Modes API

### Equipment Failure Modes

```
GET /api/v1/safety/fmea/equipment/{equipmentId}/failure-modes
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:35:00Z",
  "equipment_id": "PLC-SIEMENS-001",
  "equipment_name": "Siemens S7-1500 PLC",
  "fmea_analysis": {
    "analysis_date": "2025-11-20T00:00:00Z",
    "analyst": "Safety Engineering Team",
    "total_failure_modes": 12,
    "high_rpn_count": 3,
    "failure_modes": [
      {
        "failure_mode_id": "FM-001",
        "mode": "CPU Overload",
        "potential_effect": "Control loop timing violation, process instability",
        "severity": 8,
        "potential_cause": "Excessive scan cycle load, memory leak",
        "occurrence": 4,
        "current_controls": ["CPU load monitoring", "Watchdog timer"],
        "detection": 6,
        "rpn": 192,
        "rpn_category": "HIGH",
        "recommended_actions": [
          "Implement task prioritization",
          "Add redundant CPU module",
          "Deploy load balancing"
        ],
        "action_responsibility": "Control Systems Engineering",
        "target_completion": "2026-01-15T00:00:00Z"
      },
      {
        "failure_mode_id": "FM-002",
        "mode": "Communication Loss",
        "potential_effect": "Loss of remote monitoring, delayed response",
        "severity": 7,
        "potential_cause": "Network failure, cable damage, switch failure",
        "occurrence": 5,
        "current_controls": ["Redundant network paths", "Heartbeat monitoring"],
        "detection": 3,
        "rpn": 105,
        "rpn_category": "MEDIUM",
        "recommended_actions": [
          "Add third network path",
          "Implement ring topology"
        ]
      },
      {
        "failure_mode_id": "FM-003",
        "mode": "Power Supply Failure",
        "potential_effect": "Complete PLC shutdown, process stoppage",
        "severity": 9,
        "potential_cause": "Power surge, component aging, heat damage",
        "occurrence": 2,
        "current_controls": ["Dual power supply", "UPS backup"],
        "detection": 2,
        "rpn": 36,
        "rpn_category": "LOW"
      }
    ],
    "rpn_summary": {
      "high_rpn_threshold": 150,
      "medium_rpn_threshold": 75,
      "modes_above_high": 3,
      "modes_medium": 5,
      "modes_low": 4,
      "average_rpn": 98.5
    },
    "criticality_matrix": {
      "catastrophic_probable": 0,
      "catastrophic_occasional": 1,
      "critical_probable": 2,
      "critical_occasional": 3,
      "marginal_probable": 4,
      "marginal_occasional": 2
    }
  }
}
```

### RPN Scores Across Assets

```
GET /api/v1/safety/fmea/rpn-scores
```

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_rpn` | number | 0 | Minimum RPN filter |
| `sector` | string | all | Filter by sector |
| `equipment_type` | string | all | Filter by equipment type |
| `sort` | string | rpn_desc | Sort order |

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:40:00Z",
  "total_failure_modes": 1247,
  "high_rpn_count": 89,
  "rpn_distribution": {
    "high": { "min": 150, "count": 89 },
    "medium": { "min": 75, "max": 149, "count": 312 },
    "low": { "max": 74, "count": 846 }
  },
  "top_rpn_items": [
    {
      "equipment_id": "HMI-LEGACY-042",
      "equipment_name": "Legacy HMI Panel",
      "sector": "Water",
      "failure_mode": "Unauthorized Access",
      "rpn": 336,
      "severity": 8,
      "occurrence": 7,
      "detection": 6,
      "risk_category": "CRITICAL"
    },
    {
      "equipment_id": "RTU-FIELD-015",
      "equipment_name": "Remote Terminal Unit",
      "sector": "Energy",
      "failure_mode": "Firmware Corruption",
      "rpn": 288,
      "severity": 9,
      "occurrence": 4,
      "detection": 8,
      "risk_category": "CRITICAL"
    }
  ],
  "sector_summary": [
    {
      "sector": "Energy",
      "average_rpn": 87.3,
      "high_rpn_count": 34,
      "total_failure_modes": 423
    },
    {
      "sector": "Water",
      "average_rpn": 92.1,
      "high_rpn_count": 28,
      "total_failure_modes": 312
    }
  ]
}
```

---

## Conduit Security API

### List Conduits

```
GET /api/v1/safety/conduits
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:45:00Z",
  "total_conduits": 156,
  "conduits": [
    {
      "conduit_id": "CONDUIT-ESP-001",
      "name": "DMZ to SCADA Network",
      "type": "ELECTRONIC_SECURITY_PERIMETER",
      "source_zone": "ZONE-L4-ENTERPRISE",
      "destination_zone": "ZONE-L2-SCADA",
      "security_level": 3,
      "encryption": true,
      "monitoring": true,
      "compliance_status": "COMPLIANT",
      "vulnerability_count": 0
    },
    {
      "conduit_id": "CONDUIT-L1-L2-001",
      "name": "PLC to SCADA",
      "type": "INTERNAL",
      "source_zone": "ZONE-L1-CONTROL",
      "destination_zone": "ZONE-L2-SCADA",
      "security_level": 2,
      "encryption": false,
      "monitoring": true,
      "compliance_status": "NON_COMPLIANT",
      "vulnerability_count": 3,
      "compliance_gap": "Encryption required for SL3"
    }
  ]
}
```

### Get Conduit Details

```
GET /api/v1/safety/conduits/{conduitId}
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:50:00Z",
  "conduit": {
    "conduit_id": "CONDUIT-ESP-001",
    "name": "DMZ to SCADA Network",
    "type": "ELECTRONIC_SECURITY_PERIMETER",
    "source_zone": "ZONE-L4-ENTERPRISE",
    "destination_zone": "ZONE-L2-SCADA",
    "physical_security": {
      "location": "LOCKED_TELECOM_ROOM",
      "cable_type": "FIBER_OPTIC",
      "cable_monitoring": true
    },
    "network_security": {
      "firewall": "Palo Alto PA-5220",
      "firewall_rules": 47,
      "ids_ips": "Snort 3.0",
      "deep_packet_inspection": true,
      "security_level_required": 3,
      "security_level_implemented": 3
    },
    "protocol_security": {
      "allowed_protocols": ["HTTPS", "SSH", "OPC UA Secure"],
      "denied_protocols": ["Telnet", "FTP", "HTTP"],
      "encryption_required": true,
      "encryption_standard": "TLS 1.3",
      "certificate_based_auth": true
    },
    "monitoring": {
      "packet_capture": true,
      "netflow_export": true,
      "siem_integration": "Splunk",
      "alert_threshold": "MEDIUM"
    },
    "performance": {
      "bandwidth_mbps": 1000,
      "utilization_percent": 23.5,
      "latency_ms": 2.3,
      "packet_loss_percent": 0.01
    },
    "compliance": {
      "iec62443_compliant": true,
      "last_audit": "2025-10-15T00:00:00Z",
      "audit_findings": 0,
      "next_audit": "2026-01-15T00:00:00Z"
    },
    "vulnerabilities": []
  }
}
```

---

## Compliance Assessment API

### Run Compliance Assessment

```
POST /api/v1/safety/compliance/assess
```

#### Request Body

```json
{
  "scope": {
    "zones": ["ZONE-L0-PROCESS-001", "ZONE-L1-CONTROL-001"],
    "assessment_type": "FULL"
  },
  "standards": ["IEC62443", "NIST_CSF"],
  "include_recommendations": true,
  "include_cost_estimates": true
}
```

#### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:00:00Z",
  "assessment_id": "ASSESS-2025-11-30-001",
  "compliance_report": {
    "overall_score": 72.4,
    "compliance_level": "PARTIAL",
    "by_standard": {
      "IEC62443": {
        "score": 71.8,
        "fr_scores": {
          "FR1": 66.7,
          "FR2": 78.3,
          "FR3": 65.8,
          "FR4": 58.2,
          "FR5": 82.1,
          "FR6": 69.4,
          "FR7": 85.7
        }
      },
      "NIST_CSF": {
        "score": 73.0,
        "category_scores": {
          "Identify": 78.5,
          "Protect": 68.2,
          "Detect": 72.1,
          "Respond": 71.5,
          "Recover": 75.2
        }
      }
    },
    "gap_summary": {
      "total_gaps": 47,
      "critical_gaps": 8,
      "high_gaps": 15,
      "medium_gaps": 24
    },
    "recommendations": [
      {
        "priority": 1,
        "gap": "Missing HSM authentication in Zone L0",
        "recommendation": "Implement hardware security modules for SL4 compliance",
        "cost_usd": 45000,
        "effort_days": 30,
        "risk_reduction": 2.5
      }
    ],
    "total_remediation_cost_usd": 892000,
    "total_remediation_days": 180
  }
}
```

---

## Neo4j Cypher Queries

### Safety Zone Schema

```cypher
// Safety Zone Node
CREATE (zone:SafetyZone:IEC62443 {
  zone_id: "ZONE-L0-PROCESS-001",
  name: "Chemical Reactor Process Control",
  purdue_level: 0,
  security_level_target: 4,
  security_level_achieved: 3,
  security_level_gap: 1,
  criticality: "SAFETY_CRITICAL",
  sil_rating: 3,
  risk_score: 8.7,
  compliance_status: "NON_COMPLIANT"
})
```

### Get Zones with Gaps

```cypher
MATCH (zone:SafetyZone)
WHERE zone.security_level_gap > 0
RETURN zone.zone_id AS zone_id,
       zone.name AS name,
       zone.security_level_target AS target,
       zone.security_level_achieved AS achieved,
       zone.security_level_gap AS gap,
       zone.risk_score AS risk
ORDER BY zone.security_level_gap DESC, zone.risk_score DESC
```

### RAMS Equipment Query

```cypher
MATCH (e:Equipment)-[:HAS_RAMS_METRICS]->(rams:RAMSMetrics)
WHERE rams.mtbf_hours < 17520  // Below 2-year threshold
RETURN e.device_id AS equipment,
       e.name AS name,
       rams.mtbf_hours AS mtbf,
       rams.mttr_hours AS mttr,
       rams.availability_percent AS availability,
       rams.sil_rating AS sil
ORDER BY rams.mtbf_hours ASC
```

### FMEA High RPN Query

```cypher
MATCH (e:Equipment)-[:HAS_FAILURE_MODE]->(fm:FailureMode)
WHERE fm.rpn >= 150
RETURN e.device_id AS equipment,
       fm.mode AS failure_mode,
       fm.severity AS severity,
       fm.occurrence AS occurrence,
       fm.detection AS detection,
       fm.rpn AS rpn,
       fm.recommended_actions AS actions
ORDER BY fm.rpn DESC
```

### Conduit Vulnerability Query

```cypher
MATCH (c:Conduit)-[:HAS_VULNERABILITY]->(v:CVE)
RETURN c.conduit_id AS conduit,
       c.source_zone AS source,
       c.destination_zone AS destination,
       count(v) AS vuln_count,
       max(v.cvss_score) AS max_cvss
ORDER BY vuln_count DESC
```

---

## Frontend Integration

### TypeScript SDK

```typescript
import { AeonSafetyClient } from '@aeon-dt/safety-client';

const client = new AeonSafetyClient({
  baseUrl: 'https://api.aeon-dt.local/api/v1',
  apiKey: process.env.AEON_API_KEY
});

// Get zones with gaps
const zones = await client.getZones({
  complianceStatus: 'NON_COMPLIANT',
  minRiskScore: 7.0
});

// Run gap analysis
const gapAnalysis = await client.getGapAnalysis('ZONE-L0-PROCESS-001');

// Get RAMS metrics
const rams = await client.getRAMSMetrics('PLC-SIEMENS-001');

// Get FMEA failure modes
const fmea = await client.getFailureModes('PLC-SIEMENS-001');

// Run compliance assessment
const assessment = await client.runComplianceAssessment({
  zones: ['ZONE-L0-PROCESS-001'],
  standards: ['IEC62443'],
  includeRecommendations: true
});
```

### React Dashboard Example

```tsx
import { useSafetyZones, useGapAnalysis } from '@aeon-dt/react-hooks';

function SafetyDashboard() {
  const { zones, isLoading } = useSafetyZones({
    complianceStatus: 'NON_COMPLIANT'
  });

  return (
    <div className="safety-dashboard">
      <ComplianceOverview zones={zones} />
      <ZoneGapMatrix zones={zones} />
      <RemediationRoadmap zones={zones} />
      <RAMSSummary />
      <FMEARiskMatrix />
    </div>
  );
}
```

---

## Error Handling

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `ZONE_NOT_FOUND` | 404 | Safety zone not found |
| `EQUIPMENT_NOT_FOUND` | 404 | Equipment not in database |
| `INVALID_PURDUE_LEVEL` | 400 | Invalid Purdue level (must be 0-4) |
| `INVALID_SL` | 400 | Invalid security level (must be 1-4) |
| `ASSESSMENT_TIMEOUT` | 408 | Compliance assessment timeout |

---

## Related Documentation

- `API_EQUIPMENT.md` - Equipment details and relationships
- `API_VULNERABILITIES.md` - CVE database
- `02_Databases/Neo4j-Graph-Database.md` - Graph database access
- `Enhancement_07_IEC62443_Safety/README.md` - IEC 62443 specification
- `Enhancement_08_RAMS_Reliability/` - RAMS enhancement
- `Enhancement_09_FMEA_Hazard/` - FMEA enhancement

---

**Status:** COMPLETE | **Version:** 1.0.0 | **Last Update:** 2025-11-30
