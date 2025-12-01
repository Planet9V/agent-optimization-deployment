# AEON Sectors API Documentation

**File**: API_SECTORS.md
**Created**: 2025-11-25
**Version**: 1.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete API reference for CISA critical infrastructure sectors
**Status**: ACTIVE - Production Ready Design

---

## TABLE OF CONTENTS

1. [Overview](#overview)
2. [API Endpoints](#api-endpoints)
3. [Request/Response Schemas](#requestresponse-schemas)
4. [Frontend Integration](#frontend-integration)
5. [Business Value](#business-value)
6. [Example Queries](#example-queries)
7. [Implementation Patterns](#implementation-patterns)

---

## OVERVIEW

The Sectors API provides programmatic access to AEON's comprehensive critical infrastructure knowledge base. The system integrates 16 CISA-designated critical infrastructure sectors with detailed equipment catalogs, vulnerability intelligence, and cross-sector dependencies.

### Key Capabilities

- **Sector Enumeration**: List all 16 critical infrastructure sectors with statistics
- **Sector Details**: Deep-dive analysis including equipment, vulnerabilities, risk metrics
- **Equipment Management**: Query sector-specific equipment with full lifecycle tracking
- **Vulnerability Intelligence**: CVE mapping to sectors and equipment
- **Cross-Sector Analytics**: Dependency analysis and risk propagation
- **Compliance Tracking**: NIST, IEC-62443, and sector-specific regulations

### System Scale

| Metric | Value |
|--------|-------|
| Total Sectors | 16 CISA-designated |
| Total Equipment Nodes | 1,067,754+ |
| Total CVE Mappings | 4,100+ |
| Total Relationships | 11,998,401+ |
| Cross-sector Dependencies | 540+ (documented) |
| Real-time Data Streams | 5+ (CVE, MITRE ATT&CK, News) |

### 16 Critical Infrastructure Sectors

1. **Chemical Sector** - Chemical facilities and process control systems
2. **Commercial Facilities** - Retail, entertainment, hospitality
3. **Communications** - Telecom, data centers, satellite systems
4. **Defense** - Military bases and command systems
5. **Dams** - Water control and monitoring systems
6. **Emergency Services** - 911 centers, fire, EMS
7. **Energy** - Power generation, transmission, distribution
8. **Financial Services** - Banks, trading, payment systems
9. **Food & Agriculture** - Farms, processing, distribution
10. **Government Facilities** - Federal, state, local government
11. **Healthcare** - Hospitals, medical devices, health IT
12. **IT** - Cloud infrastructure, managed services
13. **Manufacturing** - Industrial automation, supply chain
14. **Nuclear Reactors** - Nuclear plants and safety systems
15. **Transportation** - Aviation, maritime, rail, highway
16. **Water & Wastewater** - Treatment, distribution, monitoring

---

## API ENDPOINTS

### 1. LIST ALL SECTORS

**Endpoint**: `GET /api/v1/sectors`

**Description**: Retrieve list of all 16 CISA critical infrastructure sectors with summary statistics.

**Query Parameters**:
```
None (base endpoint returns all sectors)
```

**Response**:
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:30:45Z",
  "data": {
    "total": 16,
    "sectors": [
      {
        "id": "WATER",
        "name": "Water and Wastewater Systems",
        "description": "Public water systems, wastewater treatment and distribution",
        "equipment_count": 33555,
        "vulnerabilities_count": 600,
        "facilities_count": 8500,
        "critical_equipment_count": 1250,
        "compliance_frameworks": ["NIST", "AWWA", "EPA"],
        "risk_score": 7.8,
        "data_freshness": "2025-11-25T14:00:00Z"
      },
      {
        "id": "ENERGY",
        "name": "Energy",
        "description": "Electric power generation, transmission, distribution and natural gas",
        "equipment_count": 67110,
        "vulnerabilities_count": 1200,
        "facilities_count": 15000,
        "critical_equipment_count": 2800,
        "compliance_frameworks": ["NIST", "NERC", "FERC"],
        "risk_score": 8.2,
        "data_freshness": "2025-11-25T14:00:00Z"
      },
      // ... 14 more sectors
    ]
  },
  "meta": {
    "api_version": "1.0.0",
    "execution_time_ms": 125
  }
}
```

**Status Codes**:
- `200 OK` - Successful retrieval
- `500 Internal Server Error` - Database connection issue

---

### 2. GET SECTOR DETAILS

**Endpoint**: `GET /api/v1/sectors/{sector}`

**Description**: Retrieve comprehensive details for a specific sector including equipment, vulnerabilities, risk metrics, and compliance information.

**Path Parameters**:
```
sector (string, required) - Sector identifier (WATER, ENERGY, NUCLEAR, TRANSPORTATION, COMMUNICATIONS,
                             HEALTHCARE, FINANCIAL, FOOD_AGRICULTURE, GOVERNMENT, EMERGENCY_SERVICES,
                             CHEMICAL, MANUFACTURING, DEFENSE, DAMS, IT, COMMERCIAL)
```

**Query Parameters**:
```
include_vulnerabilities (boolean, optional) - Include full CVE details (default: true)
include_equipment (boolean, optional) - Include equipment list (default: false, use endpoint 3)
limit_equipment (integer, optional) - Limit equipment results (default: 50, max: 500)
risk_level_filter (string, optional) - Filter by risk level: LOW, MEDIUM, HIGH, CRITICAL
```

**Response**:
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:35:22Z",
  "data": {
    "sector": {
      "id": "ENERGY",
      "name": "Energy",
      "full_description": "Electricity, natural gas, and petroleum infrastructure including generation, transmission, distribution, and storage",
      "sector_overview": {
        "total_equipment": 67110,
        "total_facilities": 15000,
        "critical_equipment": 2800,
        "critical_facilities": 450,
        "total_vulnerabilities": 1200,
        "employees_affected": 750000,
        "gdp_impact_percent": 18.5
      },
      "risk_assessment": {
        "overall_risk_score": 8.2,
        "threat_level": "CRITICAL",
        "vulnerability_density": 0.018,
        "exposure_level": "HIGH",
        "threat_trend": "INCREASING",
        "predicted_incident_probability": 0.42,
        "predicted_incident_timeframe_days": 31
      },
      "equipment_breakdown": {
        "total": 67110,
        "by_type": {
          "SCADA_System": 450,
          "Power_Plant": 125,
          "Transformer": 8900,
          "Substation": 340,
          "Smart_Meter": 45000,
          "Communication_Network": 12000,
          "Control_Center": 295
        },
        "by_criticality": {
          "CRITICAL": 2800,
          "HIGH": 8500,
          "MEDIUM": 35000,
          "LOW": 20810
        },
        "by_vendor": {
          "Siemens": 12000,
          "ABB": 9500,
          "Schneider_Electric": 11000,
          "GE_Power": 8500,
          "Other": 26110
        }
      },
      "vulnerability_summary": {
        "total": 1200,
        "critical": 120,
        "high": 240,
        "medium": 480,
        "low": 360,
        "exploitable_in_30_days": 85,
        "known_exploits": 234,
        "zero_day_estimates": 12
      },
      "compliance_framework": {
        "frameworks": [
          {
            "name": "NIST Cybersecurity Framework",
            "maturity_level": 3,
            "last_assessment": "2025-10-15",
            "compliance_percentage": 68,
            "critical_gaps": 8
          },
          {
            "name": "NERC CIP",
            "maturity_level": 2,
            "last_assessment": "2025-10-01",
            "compliance_percentage": 72,
            "critical_gaps": 5
          },
          {
            "name": "FERC 622",
            "maturity_level": 3,
            "last_assessment": "2025-09-30",
            "compliance_percentage": 75,
            "critical_gaps": 3
          }
        ],
        "primary_requirements": ["Incident Response", "Access Control", "Network Segmentation"]
      },
      "dependencies": {
        "outbound_dependencies": {
          "FINANCIAL": 180,
          "COMMUNICATIONS": 450,
          "GOVERNMENT": 120,
          "WATER": 85
        },
        "inbound_dependencies": {
          "MANUFACTURING": 250,
          "TRANSPORTATION": 95,
          "EMERGENCY_SERVICES": 110
        },
        "critical_paths": 12,
        "single_point_failures": 8
      },
      "threat_intelligence": {
        "active_threats": 34,
        "attributed_groups": [
          {
            "name": "Sandworm",
            "country": "RU",
            "last_activity": "2025-11-20",
            "targeting_tactics": ["ICS_Exploitation", "Lateral_Movement", "Persistence"]
          },
          {
            "name": "Turla",
            "country": "RU",
            "last_activity": "2025-11-15",
            "targeting_tactics": ["Espionage", "Data_Exfiltration"]
          }
        ],
        "recent_incidents": 7,
        "incident_trend_30_days": "STABLE",
        "breach_probability_12_months": 0.67
      },
      "recommended_actions": [
        {
          "priority": "CRITICAL",
          "action": "Patch SCADA systems for CVE-2024-3156",
          "affected_equipment": 450,
          "estimated_downtime_hours": 8,
          "estimated_risk_reduction": 0.12
        },
        {
          "priority": "HIGH",
          "action": "Implement network segmentation for communication systems",
          "affected_equipment": 8900,
          "estimated_cost_usd": 2500000,
          "estimated_risk_reduction": 0.18
        }
      ]
    }
  },
  "meta": {
    "api_version": "1.0.0",
    "execution_time_ms": 340
  }
}
```

**Status Codes**:
- `200 OK` - Successful retrieval
- `404 Not Found` - Sector not found
- `400 Bad Request` - Invalid sector identifier

**Example Requests**:
```bash
# Basic sector details
curl "https://api.aeon.cyber/api/v1/sectors/ENERGY"

# With vulnerability filter
curl "https://api.aeon.cyber/api/v1/sectors/WATER?risk_level_filter=CRITICAL"

# Without equipment details
curl "https://api.aeon.cyber/api/v1/sectors/NUCLEAR?include_equipment=false"
```

---

### 3. GET SECTOR EQUIPMENT

**Endpoint**: `GET /api/v1/sectors/{sector}/equipment`

**Description**: Retrieve detailed equipment catalog for a specific sector with filtering and sorting options.

**Path Parameters**:
```
sector (string, required) - Sector identifier
```

**Query Parameters**:
```
equipment_type (string, optional) - Filter by equipment type (SCADA, PLC, IED, Router, etc.)
criticality (string, optional) - CRITICAL, HIGH, MEDIUM, LOW
vendor (string, optional) - Filter by manufacturer (Siemens, ABB, Schneider, etc.)
status (string, optional) - OPERATIONAL, MAINTENANCE, RETIRED, UNKNOWN
page (integer, optional) - Pagination page number (default: 1)
limit (integer, optional) - Results per page (default: 50, max: 500)
sort (string, optional) - Sort field: risk_score, install_date, last_update (default: risk_score DESC)
search (string, optional) - Free-text search in equipment name, model
```

**Response**:
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:40:15Z",
  "data": {
    "sector": "ENERGY",
    "equipment_list": [
      {
        "equipment_id": "EQ-ENERGY-00001",
        "equipment_type": "SCADA_System",
        "name": "Eastern Grid Master Control System",
        "manufacturer": "Siemens",
        "model": "SICAM PQM",
        "status": "OPERATIONAL",
        "criticality": "CRITICAL",
        "install_date": "2015-03-20",
        "last_firmware_update": "2024-08-15",
        "location": {
          "facility_id": "FAC-ENERGY-001",
          "facility_name": "Eastern Regional Control Center",
          "state": "PA",
          "city": "Pittsburgh",
          "latitude": 40.4406,
          "longitude": -79.9959,
          "region": "Northeast Grid"
        },
        "technical_specifications": {
          "protocol": "MODBUS_TCP",
          "ports": 3,
          "network_connections": 12,
          "supported_devices": 450,
          "cpu": "Intel Xeon E5",
          "ram_gb": 64,
          "storage_gb": 2000,
          "os": "Windows Server 2016"
        },
        "vulnerability_summary": {
          "total_cves": 18,
          "critical": 3,
          "high": 5,
          "medium": 7,
          "low": 3,
          "exploitable_without_auth": 2,
          "known_public_exploits": 4
        },
        "risk_assessment": {
          "risk_score": 8.6,
          "risk_level": "CRITICAL",
          "threat_likelihood": "HIGH",
          "impact_if_compromised": "SEVERE",
          "predicted_breach_probability": 0.58,
          "days_to_expected_breach": 45
        },
        "compliance_status": {
          "NIST_compliant": false,
          "NERC_CIP_compliant": false,
          "IEC_62443_level": 1,
          "outstanding_requirements": 12
        },
        "related_cves": [
          "CVE-2024-1850",
          "CVE-2024-2156",
          "CVE-2023-4598"
        ],
        "remediation_status": "IN_PROGRESS",
        "patch_available": true,
        "next_security_assessment": "2025-12-15"
      },
      {
        "equipment_id": "EQ-ENERGY-00002",
        "equipment_type": "Power_Plant",
        "name": "Westbrook Thermal Generation Station",
        "manufacturer": "GE Power",
        "model": "9HA.02",
        "status": "OPERATIONAL",
        "criticality": "CRITICAL",
        "install_date": "2008-06-10",
        "last_firmware_update": "2024-02-28",
        "location": {
          "facility_id": "FAC-ENERGY-002",
          "facility_name": "Westbrook Power Complex",
          "state": "TX",
          "city": "Dallas",
          "latitude": 32.7767,
          "longitude": -96.7970,
          "region": "Texas Grid"
        },
        "capacity_mw": 500,
        "fuel_type": "Natural_Gas",
        "uptime_percent_30_days": 98.2,
        "technical_specifications": {
          "turbine_model": "GE 7HA.02",
          "efficiency_percent": 61.4,
          "emission_controls": ["SCR", "SNCR"],
          "control_system": "Mark VIe"
        },
        "vulnerability_summary": {
          "total_cves": 25,
          "critical": 5,
          "high": 8,
          "medium": 10,
          "low": 2,
          "exploitable_without_auth": 3,
          "known_public_exploits": 6
        },
        "risk_assessment": {
          "risk_score": 8.4,
          "risk_level": "CRITICAL",
          "threat_likelihood": "HIGH",
          "impact_if_compromised": "SEVERE",
          "predicted_breach_probability": 0.52,
          "days_to_expected_breach": 52
        },
        "related_cves": [
          "CVE-2024-0945",
          "CVE-2023-5678",
          "CVE-2023-4456"
        ]
      }
      // ... additional equipment records
    ],
    "pagination": {
      "total_records": 67110,
      "total_pages": 1343,
      "current_page": 1,
      "per_page": 50,
      "has_next": true
    },
    "filters_applied": {
      "sector": "ENERGY",
      "criticality": null,
      "equipment_type": null,
      "status": "OPERATIONAL"
    }
  },
  "meta": {
    "api_version": "1.0.0",
    "execution_time_ms": 520
  }
}
```

**Status Codes**:
- `200 OK` - Successful retrieval
- `404 Not Found` - Sector not found
- `400 Bad Request` - Invalid parameters

---

### 4. GET SECTOR VULNERABILITIES

**Endpoint**: `GET /api/v1/sectors/{sector}/vulnerabilities`

**Description**: Retrieve CVE vulnerability data mapped to sector equipment with priority and remediation guidance.

**Path Parameters**:
```
sector (string, required) - Sector identifier
```

**Query Parameters**:
```
severity (string, optional) - CRITICAL, HIGH, MEDIUM, LOW (comma-separated for multiple)
sort (string, optional) - cvss_score DESC, publish_date DESC, affected_equipment COUNT DESC
page (integer, optional) - Pagination page (default: 1)
limit (integer, optional) - Results per page (default: 50, max: 500)
affected_equipment_min (integer, optional) - Filter by minimum equipment affected count
exploitable (boolean, optional) - Filter to easily exploitable CVEs (default: false)
```

**Response**:
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:45:30Z",
  "data": {
    "sector": "ENERGY",
    "vulnerabilities": [
      {
        "cve_id": "CVE-2024-3156",
        "title": "Siemens SICAM PQM Remote Code Execution",
        "description": "A remote code execution vulnerability in Siemens SICAM PQM SCADA system allows authenticated attackers to execute arbitrary code through specially crafted MODBUS TCP packets",
        "cvss_v3_1": {
          "base_score": 9.8,
          "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
          "severity": "CRITICAL",
          "attack_complexity": "LOW",
          "privileges_required": "NONE",
          "user_interaction": "NONE",
          "scope": "UNCHANGED"
        },
        "cwe_ids": ["CWE-78", "CWE-94"],
        "published_date": "2024-03-15",
        "modified_date": "2024-09-20",
        "availability_status": "PUBLISHED",
        "known_exploits": true,
        "exploit_maturity": "ACTIVE",
        "affected_equipment_in_sector": {
          "total": 450,
          "by_status": {
            "PATCHED": 0,
            "UNPATCHED": 450,
            "IN_PROGRESS": 0,
            "NOT_APPLICABLE": 0
          }
        },
        "affected_vendors": [
          {
            "vendor": "Siemens",
            "products": ["SICAM PQM"],
            "affected_versions": ["5.0 to 5.2"],
            "fixed_version": "5.3",
            "patch_available": true,
            "patch_date": "2024-04-20"
          }
        ],
        "sector_impact": {
          "potential_consequence": "CRITICAL - RCE on 450 SCADA systems controlling power grid",
          "risk_to_sector": "HIGH",
          "estimated_impact_mw": 15000,
          "estimated_users_affected": 2500000
        },
        "remediation": {
          "priority": "CRITICAL",
          "recommended_action": "Patch to version 5.3 or implement network segmentation",
          "estimated_patch_time_hours": 8,
          "estimated_downtime_hours": 4,
          "estimated_cost_usd": 125000,
          "mitigation_steps": [
            "Isolate affected systems on air-gapped network",
            "Implement strict network access controls",
            "Monitor for suspicious MODBUS TCP traffic",
            "Update SIEM rules for exploitation attempts"
          ]
        },
        "references": [
          "https://www.cisa.gov/news-events/alerts/2024/03/15/...",
          "https://nvd.nist.gov/vuln/detail/CVE-2024-3156"
        ],
        "sectors_affected": ["ENERGY", "WATER"],
        "related_threat_groups": ["Sandworm", "Turla"],
        "intelligence_links": [
          {
            "type": "MITRE_ATT_CK",
            "technique_id": "T1190",
            "technique_name": "Exploit Public-Facing Application"
          },
          {
            "type": "MITRE_ATT_CK",
            "technique_id": "T1561",
            "technique_name": "Disk Wipe"
          }
        ]
      },
      {
        "cve_id": "CVE-2024-2156",
        "title": "ABB AC500 Authentication Bypass",
        "description": "An authentication bypass vulnerability in ABB AC500 PLC allows attackers to bypass authentication checks",
        "cvss_v3_1": {
          "base_score": 8.2,
          "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
          "severity": "HIGH"
        },
        "published_date": "2024-02-10",
        "affected_equipment_in_sector": {
          "total": 340,
          "by_status": {
            "PATCHED": 120,
            "UNPATCHED": 220,
            "IN_PROGRESS": 0,
            "NOT_APPLICABLE": 0
          }
        },
        "remediation": {
          "priority": "HIGH",
          "recommended_action": "Apply patch immediately to 220 unpatched systems",
          "estimated_patch_time_hours": 6,
          "estimated_downtime_hours": 2
        }
      }
      // ... additional CVEs
    ],
    "summary": {
      "total_vulnerabilities": 1200,
      "by_severity": {
        "CRITICAL": 120,
        "HIGH": 240,
        "MEDIUM": 480,
        "LOW": 360
      },
      "exploitable_in_30_days": 85,
      "estimated_patch_time_months": 6,
      "estimated_remediation_cost_usd": 2850000,
      "sector_risk_change_30_days": "+2.4%"
    },
    "pagination": {
      "total_records": 1200,
      "total_pages": 24,
      "current_page": 1,
      "per_page": 50
    }
  },
  "meta": {
    "api_version": "1.0.0",
    "execution_time_ms": 640
  }
}
```

**Status Codes**:
- `200 OK` - Successful retrieval
- `404 Not Found` - Sector not found
- `400 Bad Request` - Invalid parameters

---

### 5. GET SECTOR ANALYTICS

**Endpoint**: `GET /api/v1/analytics/sectors`

**Description**: Retrieve aggregated analytics and trends across all sectors for comparative risk assessment.

**Query Parameters**:
```
time_period (string, optional) - 7d, 30d, 90d, 1y (default: 30d)
metrics (string, optional) - Comma-separated: risk_trend, vulnerability_density, incident_rate, etc.
sector_comparison (boolean, optional) - Include sector-to-sector comparison (default: false)
include_predictions (boolean, optional) - Include ML predictions (default: true)
```

**Response**:
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:50:00Z",
  "data": {
    "period": "30d",
    "generated_at": "2025-11-25T14:50:00Z",
    "sector_rankings": {
      "by_risk_score": [
        {
          "rank": 1,
          "sector": "ENERGY",
          "risk_score": 8.2,
          "change_30_days": "+0.5",
          "threat_level": "CRITICAL",
          "incident_count_30_days": 7,
          "critical_vulnerabilities": 120,
          "exposed_equipment_percent": 62.5
        },
        {
          "rank": 2,
          "sector": "NUCLEAR",
          "risk_score": 8.1,
          "change_30_days": "+0.2",
          "threat_level": "CRITICAL",
          "incident_count_30_days": 3,
          "critical_vulnerabilities": 95,
          "exposed_equipment_percent": 58.2
        },
        {
          "rank": 3,
          "sector": "WATER",
          "risk_score": 7.8,
          "change_30_days": "+1.2",
          "threat_level": "CRITICAL",
          "incident_count_30_days": 5,
          "critical_vulnerabilities": 78,
          "exposed_equipment_percent": 55.8
        }
        // ... remaining 13 sectors
      ],
      "by_vulnerability_density": [
        {
          "sector": "ENERGY",
          "vulnerability_per_equipment": 0.018,
          "trend": "INCREASING"
        }
        // ...
      ],
      "by_threat_trend": [
        {
          "sector": "WATER",
          "trend_direction": "INCREASING",
          "incidents_30_days": 5,
          "incidents_60_days": 8,
          "change_percent": "-37.5%"
        }
        // ...
      ]
    },
    "cross_sector_metrics": {
      "average_risk_score": 7.45,
      "median_risk_score": 7.6,
      "std_deviation": 0.58,
      "highest_risk_sector": "ENERGY",
      "lowest_risk_sector": "COMMERCIAL",
      "sectors_with_increasing_risk": 11,
      "sectors_with_decreasing_risk": 5
    },
    "vulnerability_trends": {
      "new_cves_30_days": 245,
      "critical_cves_30_days": 34,
      "exploited_in_wild": 12,
      "zero_day_estimates": 8,
      "patch_lag_average_days": 18,
      "sectors_with_unpatched_critical": 14
    },
    "incident_analytics": {
      "total_incidents_30_days": 47,
      "incident_trend": "INCREASING",
      "incident_change_percent": "+15.2%",
      "confirmed_breaches": 3,
      "attributed_threat_groups": 8,
      "most_targeted_sector": "ENERGY",
      "least_targeted_sector": "COMMERCIAL"
    },
    "compliance_status": {
      "sectors_meeting_nist_csf": 4,
      "sectors_meeting_iec_62443": 2,
      "average_maturity_level": 2.3,
      "critical_compliance_gaps": 48,
      "estimated_remediation_cost_usd": 28500000
    },
    "predictions": {
      "prediction_model": "AEON_McKenney_Psychohistory_ML_v2",
      "model_accuracy_percent": 87.3,
      "predicted_incidents_next_30_days": 62,
      "predicted_critical_breaches_next_90_days": 8,
      "sectors_highest_incident_risk": [
        {
          "sector": "ENERGY",
          "predicted_breach_probability": 0.67,
          "predicted_timeframe_days": 35,
          "confidence_percent": 89.2
        },
        {
          "sector": "NUCLEAR",
          "predicted_breach_probability": 0.58,
          "predicted_timeframe_days": 42,
          "confidence_percent": 86.5
        }
      ]
    },
    "recommendations": {
      "immediate_actions": [
        {
          "priority": "CRITICAL",
          "sector": "ENERGY",
          "action": "Patch CVE-2024-3156 on all 450 SCADA systems",
          "estimated_impact": "Risk reduction: 12%"
        }
      ],
      "strategic_initiatives": [
        {
          "priority": "HIGH",
          "initiative": "Cross-sector dependency mapping",
          "affected_sectors": 16,
          "estimated_cost_usd": 2500000,
          "expected_risk_reduction_percent": 8.5
        }
      ]
    }
  },
  "meta": {
    "api_version": "1.0.0",
    "execution_time_ms": 1250
  }
}
```

---

### 6. GET CROSS-SECTOR DEPENDENCIES

**Endpoint**: `GET /api/v1/analytics/dependencies`

**Description**: Analyze dependencies between sectors to understand risk propagation and cascading failure scenarios.

**Query Parameters**:
```
sector (string, optional) - Filter dependencies for specific sector
dependency_type (string, optional) - DIRECT, INDIRECT, SUPPLY_CHAIN, DATA_FLOW
critical_only (boolean, optional) - Show only critical paths (default: false)
show_strength (boolean, optional) - Include dependency strength metrics (default: true)
```

**Response**:
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:55:30Z",
  "data": {
    "total_dependencies": 540,
    "total_critical_paths": 68,
    "total_single_point_failures": 23,
    "dependency_graph": {
      "nodes": 16,
      "edges": 340,
      "connectivity_factor": 0.91
    },
    "sector_dependencies": [
      {
        "source_sector": "ENERGY",
        "dependencies": [
          {
            "target_sector": "COMMUNICATIONS",
            "dependency_type": "OPERATIONAL_CONTROL",
            "critical": true,
            "dependency_count": 450,
            "failure_impact": {
              "description": "Loss of SCADA command and control",
              "energy_systems_affected": 450,
              "users_affected_millions": 2.5,
              "estimated_recovery_hours": 48
            },
            "mitigation_status": "PARTIAL",
            "mitigation_measures": [
              "Dedicated fiber optic control channels",
              "Redundant communication pathways"
            ]
          },
          {
            "target_sector": "FINANCIAL",
            "dependency_type": "BILLING_SETTLEMENT",
            "critical": false,
            "dependency_count": 15,
            "failure_impact": {
              "description": "Billing system interruption",
              "energy_systems_affected": 0,
              "financial_impact_per_day_usd": 5000000,
              "estimated_recovery_hours": 4
            }
          },
          {
            "target_sector": "WATER",
            "dependency_type": "PUMP_POWER_SUPPLY",
            "critical": true,
            "dependency_count": 85,
            "failure_impact": {
              "description": "Water supply interruption",
              "water_systems_affected": 85,
              "users_affected_millions": 15.2,
              "estimated_recovery_hours": 72
            }
          },
          {
            "target_sector": "EMERGENCY_SERVICES",
            "dependency_type": "POWER_FOR_911",
            "critical": true,
            "dependency_count": 110,
            "failure_impact": {
              "description": "911 systems and emergency response compromised",
              "emergency_centers_affected": 2100,
              "estimated_recovery_hours": 8
            }
          }
        ],
        "inbound_dependencies": [
          {
            "source_sector": "MANUFACTURING",
            "dependency_type": "EQUIPMENT_SUPPLY",
            "dependency_count": 250
          },
          {
            "source_sector": "TRANSPORTATION",
            "dependency_type": "FUEL_TRANSPORT",
            "dependency_count": 95
          }
        ]
      },
      {
        "source_sector": "COMMUNICATIONS",
        "dependencies": [
          {
            "target_sector": "FINANCIAL",
            "dependency_type": "PAYMENT_INFRASTRUCTURE",
            "critical": true,
            "dependency_count": 280,
            "failure_impact": {
              "description": "Financial transaction system failure",
              "systems_affected": 15000,
              "daily_transaction_impact_billion_usd": 1.2
            }
          },
          {
            "target_sector": "GOVERNMENT",
            "dependency_type": "CLASSIFIED_COMMUNICATIONS",
            "critical": true,
            "dependency_count": 150
          }
        ]
      }
      // ... remaining sector dependencies
    ],
    "critical_failure_scenarios": [
      {
        "scenario_id": "CASCADE_001",
        "description": "Energy outage cascades to Communications (48-72 hours)",
        "probability": 0.34,
        "affected_sectors": ["ENERGY", "COMMUNICATIONS", "WATER", "EMERGENCY_SERVICES"],
        "estimated_users_affected_millions": 25,
        "estimated_economic_impact_billion_usd": 45,
        "recovery_time_hours": 72,
        "mitigation_priority": "CRITICAL"
      },
      {
        "scenario_id": "CASCADE_002",
        "description": "Communications failure cascades to Financial (24-36 hours)",
        "probability": 0.28,
        "affected_sectors": ["COMMUNICATIONS", "FINANCIAL", "GOVERNMENT"],
        "estimated_economic_impact_billion_usd": 120,
        "recovery_time_hours": 36,
        "mitigation_priority": "CRITICAL"
      }
    ],
    "resilience_recommendations": [
      {
        "recommendation": "Implement sector-level redundancy",
        "priority": "CRITICAL",
        "estimated_cost_usd": 8500000,
        "expected_resilience_improvement_percent": 25
      },
      {
        "recommendation": "Establish cross-sector communication protocols",
        "priority": "HIGH",
        "estimated_cost_usd": 2000000,
        "expected_resilience_improvement_percent": 15
      }
    ]
  },
  "meta": {
    "api_version": "1.0.0",
    "execution_time_ms": 890
  }
}
```

---

## REQUEST/RESPONSE SCHEMAS

### Common Response Structure

All API responses follow this envelope structure:

```typescript
interface ApiResponse<T> {
  success: boolean;           // true if successful, false otherwise
  timestamp: string;          // ISO 8601 timestamp of response
  data: T;                   // Response payload (varies by endpoint)
  error?: ApiError;          // Present only on errors
  meta: {
    api_version: string;     // Current API version (1.0.0)
    execution_time_ms: number; // Time to execute query
  };
}

interface ApiError {
  code: string;              // Error code (INVALID_SECTOR, DB_ERROR, etc.)
  message: string;           // Human-readable error message
  details?: Record<string, any>; // Additional error details
}
```

### Equipment Object Schema

```typescript
interface Equipment {
  equipment_id: string;
  equipment_type: string;
  name: string;
  manufacturer: string;
  model: string;
  status: "OPERATIONAL" | "MAINTENANCE" | "RETIRED" | "UNKNOWN";
  criticality: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  install_date: string;      // ISO 8601 date
  last_firmware_update: string;

  location: {
    facility_id: string;
    facility_name: string;
    state: string;
    city: string;
    latitude: number;
    longitude: number;
    region: string;
  };

  technical_specifications: Record<string, any>;

  vulnerability_summary: {
    total_cves: number;
    critical: number;
    high: number;
    medium: number;
    low: number;
    exploitable_without_auth: number;
    known_public_exploits: number;
  };

  risk_assessment: {
    risk_score: number;        // 0-10 scale
    risk_level: string;
    threat_likelihood: string;
    impact_if_compromised: string;
    predicted_breach_probability: number; // 0-1
    days_to_expected_breach: number;
  };

  compliance_status: {
    NIST_compliant: boolean;
    NERC_CIP_compliant?: boolean;
    IEC_62443_level: number;
    outstanding_requirements: number;
  };

  related_cves: string[];
  remediation_status: string;
  patch_available: boolean;
  next_security_assessment: string;
}
```

### CVE Object Schema

```typescript
interface CVE {
  cve_id: string;
  title: string;
  description: string;

  cvss_v3_1: {
    base_score: number;
    vector_string: string;
    severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
    attack_complexity: string;
    privileges_required: string;
    user_interaction: string;
    scope: string;
  };

  cwe_ids: string[];
  published_date: string;
  modified_date: string;
  availability_status: string;
  known_exploits: boolean;
  exploit_maturity: string;

  affected_equipment_in_sector: {
    total: number;
    by_status: {
      PATCHED: number;
      UNPATCHED: number;
      IN_PROGRESS: number;
      NOT_APPLICABLE: number;
    };
  };

  affected_vendors: VendorAffected[];
  sector_impact: SectorImpact;
  remediation: RemediationGuidance;
  references: string[];
  sectors_affected: string[];
  related_threat_groups: string[];
  intelligence_links: IntelligenceLink[];
}
```

### Pagination Schema

```typescript
interface Pagination {
  total_records: number;
  total_pages: number;
  current_page: number;
  per_page: number;
  has_next: boolean;
  has_previous?: boolean;
}
```

---

## FRONTEND INTEGRATION

### React Components for Sector Dashboard

```typescript
// SectorListComponent.tsx
import React from 'react';
import { SectorCard } from './SectorCard';

interface SectorListProps {
  sectors: Sector[];
  onSectorSelect: (sector: Sector) => void;
}

export const SectorListComponent: React.FC<SectorListProps> = ({
  sectors,
  onSectorSelect,
}) => {
  return (
    <div className="sector-grid">
      {sectors.map((sector) => (
        <SectorCard
          key={sector.id}
          sector={sector}
          onClick={() => onSectorSelect(sector)}
        />
      ))}
    </div>
  );
};

// SectorDetailComponent.tsx
interface SectorDetailProps {
  sectorId: string;
}

export const SectorDetailComponent: React.FC<SectorDetailProps> = ({
  sectorId,
}) => {
  const [sector, setSector] = React.useState<SectorDetail | null>(null);
  const [vulnerabilities, setVulnerabilities] = React.useState<CVE[]>([]);
  const [equipment, setEquipment] = React.useState<Equipment[]>([]);

  React.useEffect(() => {
    // Fetch sector details
    fetch(`/api/v1/sectors/${sectorId}`)
      .then((res) => res.json())
      .then((data) => setSector(data.data.sector));
  }, [sectorId]);

  return (
    <div className="sector-detail">
      <SectorOverviewCard sector={sector} />
      <RiskAssessmentPanel sector={sector} />
      <VulnerabilityList sector={sectorId} />
      <EquipmentCatalog sector={sectorId} />
      <ComplianceStatus sector={sector} />
      <DependencyMap sector={sectorId} />
    </div>
  );
};

// VulnerabilityListComponent.tsx
interface VulnerabilityListProps {
  sectorId: string;
  severity?: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
}

export const VulnerabilityListComponent: React.FC<VulnerabilityListProps> = ({
  sectorId,
  severity,
}) => {
  const [vulnerabilities, setVulnerabilities] = React.useState<CVE[]>([]);
  const [page, setPage] = React.useState(1);

  React.useEffect(() => {
    let url = `/api/v1/sectors/${sectorId}/vulnerabilities?page=${page}`;
    if (severity) url += `&severity=${severity}`;

    fetch(url)
      .then((res) => res.json())
      .then((data) => setVulnerabilities(data.data.vulnerabilities));
  }, [sectorId, page, severity]);

  return (
    <div className="vulnerability-list">
      {vulnerabilities.map((cve) => (
        <CVECard key={cve.cve_id} cve={cve} />
      ))}
      <Pagination
        total={vulnerabilities.length}
        currentPage={page}
        onPageChange={setPage}
      />
    </div>
  );
};

// SectorAnalyticsDashboard.tsx
export const SectorAnalyticsDashboard: React.FC = () => {
  const [analytics, setAnalytics] = React.useState<SectorAnalytics | null>(null);

  React.useEffect(() => {
    fetch('/api/v1/analytics/sectors?time_period=30d')
      .then((res) => res.json())
      .then((data) => setAnalytics(data.data));
  }, []);

  return (
    <div className="analytics-dashboard">
      <RiskRankingsChart rankings={analytics?.sector_rankings} />
      <VulnerabilityTrendsChart trends={analytics?.vulnerability_trends} />
      <IncidentAnalyticsChart incidents={analytics?.incident_analytics} />
      <PredictionsPanel predictions={analytics?.predictions} />
      <RecommendationsPanel recommendations={analytics?.recommendations} />
    </div>
  );
};

// DependencyMapComponent.tsx
export const DependencyMapComponent: React.FC<{ sectorId: string }> = ({
  sectorId,
}) => {
  const [dependencies, setDependencies] = React.useState<Dependencies | null>(null);

  React.useEffect(() => {
    fetch(`/api/v1/analytics/dependencies?sector=${sectorId}`)
      .then((res) => res.json())
      .then((data) => setDependencies(data.data));
  }, [sectorId]);

  return (
    <div className="dependency-map">
      <NetworkGraph dependencies={dependencies?.sector_dependencies} />
      <FailureScenariosList scenarios={dependencies?.critical_failure_scenarios} />
      <ResilienceRecommendations
        recommendations={dependencies?.resilience_recommendations}
      />
    </div>
  );
};
```

### Integration Patterns

**1. Real-time Updates**:
```typescript
// WebSocket subscription for sector risk updates
const ws = new WebSocket('wss://api.aeon.cyber/ws/v1/sectors/ENERGY/risk-updates');
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('Risk score updated:', update.risk_score);
};
```

**2. Caching Strategy**:
```typescript
// Cache sector data for 5 minutes
const CACHE_TTL_MS = 5 * 60 * 1000;
const cache = new Map<string, CachedResponse>();

async function fetchSectorWithCache(sectorId: string) {
  const cached = cache.get(sectorId);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.data;
  }

  const response = await fetch(`/api/v1/sectors/${sectorId}`);
  const data = await response.json();
  cache.set(sectorId, { data, timestamp: Date.now() });
  return data;
}
```

---

## BUSINESS VALUE

### Risk Assessment & Prioritization

The Sectors API enables rapid risk assessment across critical infrastructure:

**Scenario 1: Executive Risk Briefing**
- Query `/api/v1/analytics/sectors` to get sector risk rankings
- Identify top 5 highest-risk sectors in 30 seconds
- Present predicted incident probability for next 90 days
- Estimate financial and operational impact
- **Value**: Data-driven security posture communication to board

**Scenario 2: Sector-Specific Remediation Planning**
- Call `/api/v1/sectors/{sector}/vulnerabilities` with CRITICAL filter
- Identify 450 SCADA systems affected by CVE-2024-3156
- Estimate 8-hour patching window + $125K cost
- Plan phased deployment to minimize downtime
- **Value**: Precise vulnerability remediation prioritization

**Scenario 3: Compliance Gap Analysis**
- Query `/api/v1/sectors/{sector}` for NIST/IEC-62443 compliance
- Identify 12 outstanding requirements for power generation sector
- Map to specific equipment and vulnerabilities
- Calculate remediation cost and timeline
- **Value**: Compliance roadmap with concrete deliverables

### Cross-Sector Dependency Analysis

**Scenario**: Cascading Failure Prevention
- Call `/api/v1/analytics/dependencies` to get critical failure scenarios
- Identify that Energy sector failure cascades to Water in 48-72 hours
- Assess impact: 25M users affected, $45B economic loss
- Implement redundancy at critical dependency points
- **Value**: Preventing catastrophic cascading failures

### Threat Intelligence Integration

**Scenario**: Active Threat Response
- Monitor `/api/v1/sectors/{sector}/vulnerabilities` for Sandworm-targeted CVEs
- Cross-reference with MITRE ATT&CK techniques
- Alert on any exploitation in the wild
- Recommend immediate mitigation actions
- **Value**: Rapid response to active exploitation attempts

---

## EXAMPLE QUERIES

### Query 1: Get Top-5 Risk Sectors

```bash
curl -s "https://api.aeon.cyber/api/v1/analytics/sectors?time_period=30d&sector_comparison=true" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.sector_rankings.by_risk_score | .[0:5]'
```

**Output**: Top 5 sectors ranked by current risk score with 30-day trends

### Query 2: Find All Unpatched Critical SCADA Systems

```bash
curl -s "https://api.aeon.cyber/api/v1/sectors/ENERGY/equipment?equipment_type=SCADA_System&criticality=CRITICAL&status=OPERATIONAL" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.equipment_list[] | select(.vulnerability_summary.critical > 0)'
```

**Output**: SCADA systems in ENERGY sector with unpatched critical CVEs

### Query 3: Analyze Energy Sector Dependencies

```bash
curl -s "https://api.aeon.cyber/api/v1/analytics/dependencies?sector=ENERGY&critical_only=true" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.critical_failure_scenarios[]'
```

**Output**: All critical failure scenarios for Energy sector

### Query 4: Compare Vulnerability Trends Across Sectors

```bash
curl -s "https://api.aeon.cyber/api/v1/analytics/sectors?metrics=vulnerability_density,incident_rate&time_period=90d" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data | {by_vulnerability_density, by_threat_trend}'
```

**Output**: Vulnerability density and threat trends for all sectors over 90 days

### Query 5: Get Remediation Guidance for Sector

```bash
curl -s "https://api.aeon.cyber/api/v1/sectors/WATER/vulnerabilities?severity=CRITICAL,HIGH&exploitable=true" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.vulnerabilities[] | {cve_id, title, remediation}'
```

**Output**: Remediable high-priority vulnerabilities with action plans

---

## IMPLEMENTATION PATTERNS

### Authentication

All endpoints require Bearer token authentication:

```bash
Authorization: Bearer <JWT_TOKEN>
```

### Error Handling

Standardized error responses:

```json
{
  "success": false,
  "timestamp": "2025-11-25T15:00:00Z",
  "error": {
    "code": "INVALID_SECTOR",
    "message": "Sector 'INVALID' not found",
    "details": {
      "valid_sectors": [
        "WATER", "ENERGY", "NUCLEAR", "TRANSPORTATION",
        "COMMUNICATIONS", "HEALTHCARE", "FINANCIAL",
        "FOOD_AGRICULTURE", "GOVERNMENT", "EMERGENCY_SERVICES",
        "CHEMICAL", "MANUFACTURING", "DEFENSE", "DAMS", "IT", "COMMERCIAL"
      ]
    }
  },
  "meta": {
    "api_version": "1.0.0",
    "execution_time_ms": 45
  }
}
```

### Rate Limiting

- 1,000 requests per minute per API key
- 10,000 requests per hour per API key
- Response headers include `X-RateLimit-Remaining` and `X-RateLimit-Reset`

### Pagination

All list endpoints support cursor-based pagination:

```
?page=1&limit=50
```

Maximum limit: 500 records per request

### Performance Optimization

For large result sets, use filtering:

```bash
# Bad: Returns all 67,110 Energy equipment
GET /api/v1/sectors/ENERGY/equipment

# Good: Returns filtered 450 critical SCADA systems
GET /api/v1/sectors/ENERGY/equipment?equipment_type=SCADA_System&criticality=CRITICAL
```

---

## APPENDIX: SECTOR DEFINITIONS

### All 16 CISA Critical Infrastructure Sectors

Complete sector identifiers and descriptions for API integration:

| ID | Name | Description |
|----|------|-------------|
| WATER | Water & Wastewater Systems | Public and private water systems including collection, treatment, storage, and distribution |
| ENERGY | Energy | Electricity and natural gas systems including generation, transmission, and distribution |
| NUCLEAR | Nuclear Reactors, Materials & Waste | Nuclear power and research facilities |
| TRANSPORTATION | Transportation Systems | Aviation, maritime, rail, and highway transportation systems |
| COMMUNICATIONS | Communications | Telecommunications, broadcasting, and information technology infrastructure |
| HEALTHCARE | Healthcare & Public Health | Hospitals, medical providers, and public health organizations |
| FINANCIAL | Financial Services | Banking, investment, and payment systems |
| FOOD_AGRICULTURE | Food & Agriculture | Food production, processing, and distribution systems |
| GOVERNMENT | Government Facilities | Federal, state, and local government operations |
| EMERGENCY_SERVICES | Emergency Services | 911 centers, fire departments, and emergency medical services |
| CHEMICAL | Chemical Sector | Chemical manufacturing and hazardous material facilities |
| MANUFACTURING | Manufacturing | Industrial facilities and supply chain operations |
| DEFENSE | Defense Industrial Base | Military installations and defense contractors |
| DAMS | Dams | Water management and hydroelectric facilities |
| IT | Information Technology | Cloud providers and IT service companies |
| COMMERCIAL | Commercial Facilities | Retail, entertainment, and hospitality venues |

---

**Document Complete**: 2025-11-25
**API Version**: 1.0.0
**Status**: PRODUCTION READY
