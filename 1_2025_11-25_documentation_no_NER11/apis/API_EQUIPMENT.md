# EQUIPMENT API DOCUMENTATION - Complete Reference

**API Version**: v1.0.0
**Date**: 2025-11-25
**Status**: Production-Ready
**Purpose**: Complete REST API reference for equipment management, asset tracking, lifecycle operations, and vulnerability integration

---

## Executive Summary

The Equipment API provides comprehensive REST endpoints for managing critical infrastructure equipment across all 16 critical infrastructure sectors. The API enables creation, retrieval, updating, and lifecycle management of equipment instances while integrating vulnerability intelligence and asset tracking.

**Core Capabilities**:
- Equipment search and filtering across all sectors
- Equipment CRUD operations with comprehensive schema
- Equipment vulnerability CVE mapping
- Asset lifecycle tracking and decommissioning
- Multi-tenant equipment catalogs
- Audit trail and change tracking

**Key Statistics**:
- **API Base URL**: `/api/v1/equipment`
- **Endpoints**: 6 core operations
- **Supported Formats**: JSON request/response
- **Authentication**: Bearer token (JWT)
- **Rate Limiting**: 1000 requests/minute per API key

---

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Request/Response Schemas](#requestresponse-schemas)
4. [Endpoint Reference](#endpoint-reference)
5. [5-Step Customer Loading Process](#5-step-customer-loading-process)
6. [Frontend Integration](#frontend-integration)
7. [Business Value & Use Cases](#business-value--use-cases)
8. [Error Handling](#error-handling)
9. [Code Examples](#code-examples)
10. [Integration Patterns](#integration-patterns)

---

## API Overview

### Base URL Structure

```
Production:  https://api.aeon-digital-twin.com/api/v1/equipment
Staging:     https://staging-api.aeon-digital-twin.com/api/v1/equipment
Development: http://localhost:3000/api/v1/equipment
```

### HTTP Methods

| Method | Purpose | Idempotent |
|--------|---------|-----------|
| GET | Retrieve equipment data | Yes |
| POST | Create new equipment | No |
| PUT | Update existing equipment | Yes |
| DELETE | Decommission equipment | Yes |

### Response Format

All responses follow standard JSON format with metadata:

```json
{
  "status": "success|error|warning",
  "code": 200,
  "data": {},
  "meta": {
    "timestamp": "2025-11-25T14:30:00Z",
    "version": "v1.0.0",
    "request_id": "req_abc123xyz"
  }
}
```

---

## Authentication & Authorization

### Bearer Token Authentication

All API requests require a Bearer token in the Authorization header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Required Headers

```http
Content-Type: application/json
Authorization: Bearer [JWT_TOKEN]
X-API-Version: v1.0.0
X-Client-ID: [CLIENT_IDENTIFIER]
```

### Token Validation

Tokens are validated server-side with:
- **TTL**: 24 hours
- **Refresh**: Available via `/auth/refresh` endpoint
- **Scope**: Equipment read/write permissions

### Authorization Levels

```yaml
read_equipment:
  - View all equipment
  - Search and filter
  - Access vulnerability CVEs

write_equipment:
  - Create new equipment
  - Update existing equipment
  - Modify metadata

admin_equipment:
  - Delete/decommission equipment
  - Bulk operations
  - Access audit logs
```

---

## Request/Response Schemas

### Equipment Request Schema (POST/PUT)

```json
{
  "name": "string",
  "description": "string",
  "equipment_type": "PLC|Router|SCADA|Pump|Transformer|Generator",
  "manufacturer": "string",
  "model": "string",
  "serial_number": "string (unique)",
  "asset_id": "string",
  "firmware_version": "string",
  "operating_system": "string",
  "ip_address": "string (IPv4|IPv6)",
  "mac_address": "string",
  "location": {
    "facility_id": "string",
    "sector": "Energy|Water|Transportation|Communications|IT|Manufacturing",
    "region": "string",
    "building": "string",
    "floor": "integer",
    "room": "string"
  },
  "specifications": {
    "power_consumption": "integer (watts)",
    "operating_voltage": "string",
    "temperature_range": "string",
    "sil_rating": "integer (0-4)",
    "iec_62443_level": "integer (1-4)"
  },
  "lifecycle": {
    "acquisition_date": "YYYY-MM-DD",
    "installation_date": "YYYY-MM-DD",
    "last_maintenance": "YYYY-MM-DD",
    "warranty_expiry": "YYYY-MM-DD",
    "end_of_life_date": "YYYY-MM-DD"
  },
  "network": {
    "network_segment": "string",
    "vlan_id": "integer",
    "firewall_rule_id": "string",
    "is_connected": "boolean",
    "connection_type": "Wired|Wireless|Serial|USB"
  },
  "compliance": {
    "nerc_cip": "boolean",
    "isc_iec_62443": "boolean",
    "iso_27001": "boolean",
    "hipaa": "boolean",
    "pci_dss": "boolean"
  },
  "metadata": {
    "owner": "string",
    "responsible_team": "string",
    "tags": ["string"],
    "custom_fields": {}
  }
}
```

### Equipment Response Schema (GET)

```json
{
  "id": "equip_abc123xyz",
  "name": "PLC-Control-System-01",
  "description": "Primary control system for pump station",
  "equipment_type": "PLC",
  "manufacturer": "Siemens",
  "model": "S7-1500",
  "serial_number": "SN-2024-001-ABC",
  "asset_id": "ASSET-PLC-001",
  "firmware_version": "3.1.4",
  "operating_system": "TIA Portal 16",
  "ip_address": "192.168.1.50",
  "mac_address": "00:0a:95:9d:68:16",
  "status": "active|inactive|maintenance|deprecated",
  "location": {
    "facility_id": "fac_water_001",
    "sector": "Water",
    "region": "Northeast",
    "building": "Main Treatment Plant",
    "floor": 2,
    "room": "Control Room A"
  },
  "specifications": {
    "power_consumption": 500,
    "operating_voltage": "24VDC",
    "temperature_range": "-10 to +50°C",
    "sil_rating": 3,
    "iec_62443_level": 3
  },
  "lifecycle": {
    "acquisition_date": "2020-01-15",
    "installation_date": "2020-02-20",
    "last_maintenance": "2025-11-20",
    "warranty_expiry": "2025-01-15",
    "end_of_life_date": "2030-02-20",
    "age_years": 5.87,
    "days_to_eol": 1843
  },
  "network": {
    "network_segment": "OT_SCADA_Segment_1",
    "vlan_id": 100,
    "firewall_rule_id": "fwr_plc_001",
    "is_connected": true,
    "connection_type": "Wired",
    "last_seen": "2025-11-25T14:28:00Z"
  },
  "compliance": {
    "nerc_cip": true,
    "iec_62443": true,
    "iso_27001": true,
    "hipaa": false,
    "pci_dss": false,
    "compliance_score": 94
  },
  "vulnerabilities": {
    "total_cves": 3,
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 0,
    "last_assessment": "2025-11-25T10:00:00Z",
    "cve_ids": ["CVE-2024-1234", "CVE-2024-5678"]
  },
  "metadata": {
    "owner": "Water Operations Team",
    "responsible_team": "Maintenance Division",
    "tags": ["critical", "scada", "water-treatment"],
    "custom_fields": {
      "budget_center": "WTR-001",
      "depreciation_period": 10
    }
  },
  "audit": {
    "created_at": "2020-02-20T10:00:00Z",
    "created_by": "admin@example.com",
    "updated_at": "2025-11-25T14:30:00Z",
    "updated_by": "technician@example.com",
    "version": 12
  }
}
```

### Search/Filter Query Schema

```json
{
  "filters": {
    "equipment_type": "string|string[]",
    "manufacturer": "string",
    "sector": "string",
    "status": "active|inactive|maintenance|deprecated",
    "location": {
      "region": "string",
      "facility_id": "string"
    },
    "lifecycle": {
      "min_age_years": "number",
      "max_age_years": "number",
      "warranty_status": "active|expired|unknown"
    },
    "vulnerability": {
      "has_cves": "boolean",
      "cve_severity": "critical|high|medium|low",
      "min_cve_count": "integer"
    },
    "compliance": {
      "nerc_cip": "boolean",
      "iec_62443": "boolean",
      "min_score": "integer (0-100)"
    }
  },
  "search": "string (full-text search)",
  "pagination": {
    "page": "integer (default: 1)",
    "limit": "integer (default: 20, max: 100)"
  },
  "sort": {
    "field": "name|created_at|updated_at|age_years|vulnerability_score",
    "order": "asc|desc"
  }
}
```

---

## Endpoint Reference

### 1. GET /api/v1/equipment (Search/List)

**Purpose**: Search and filter equipment across all sectors with advanced filtering

**Method**: `GET`

**Query Parameters**:
```
?equipment_type=PLC&sector=Water&status=active&page=1&limit=20&sort=name:asc
```

**Request Example**:
```http
GET /api/v1/equipment?sector=Energy&status=active&vulnerability.has_cves=true
Authorization: Bearer [TOKEN]
```

**Response Status**: `200 OK`

**Response Payload** (200 OK):
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "equipment": [
      {
        "id": "equip_001",
        "name": "Generator-Unit-A",
        "equipment_type": "Generator",
        "manufacturer": "GE",
        "sector": "Energy",
        "location": {"region": "Northeast"},
        "status": "active",
        "vulnerabilities": {
          "total_cves": 2,
          "critical": 0,
          "high": 1
        }
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total_items": 15421,
      "total_pages": 771,
      "has_next": true
    }
  },
  "meta": {
    "timestamp": "2025-11-25T14:35:00Z",
    "query_time_ms": 245
  }
}
```

**Error Responses**:
- `400 Bad Request` - Invalid filter parameters
- `401 Unauthorized` - Missing/invalid token
- `429 Too Many Requests` - Rate limit exceeded

---

### 2. GET /api/v1/equipment/{id} (Details)

**Purpose**: Retrieve complete details for a specific equipment instance

**Method**: `GET`

**Path Parameters**:
```
{id} - Equipment ID (e.g., equip_abc123xyz)
```

**Request Example**:
```http
GET /api/v1/equipment/equip_abc123xyz
Authorization: Bearer [TOKEN]
```

**Response Status**: `200 OK`

**Response Payload** (200 OK):
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": "equip_abc123xyz",
    "name": "PLC-Control-System-01",
    "equipment_type": "PLC",
    "manufacturer": "Siemens",
    "model": "S7-1500",
    "serial_number": "SN-2024-001-ABC",
    "status": "active",
    "location": {
      "facility_id": "fac_water_001",
      "sector": "Water",
      "region": "Northeast",
      "building": "Main Treatment Plant",
      "floor": 2,
      "room": "Control Room A"
    },
    "specifications": {
      "power_consumption": 500,
      "sil_rating": 3,
      "iec_62443_level": 3
    },
    "lifecycle": {
      "acquisition_date": "2020-01-15",
      "age_years": 5.87,
      "days_to_eol": 1843
    },
    "vulnerabilities": {
      "total_cves": 3,
      "critical": 0,
      "high": 1,
      "medium": 2,
      "cve_details": [
        {
          "cve_id": "CVE-2024-1234",
          "severity": "high",
          "cvss_score": 8.2,
          "description": "Authentication bypass in S7-1500",
          "published_date": "2024-06-15",
          "patch_available": true
        }
      ]
    },
    "compliance": {
      "nerc_cip": true,
      "iec_62443": true,
      "compliance_score": 94
    },
    "audit": {
      "created_at": "2020-02-20T10:00:00Z",
      "updated_at": "2025-11-25T14:30:00Z",
      "version": 12
    }
  },
  "meta": {
    "timestamp": "2025-11-25T14:36:00Z"
  }
}
```

**Error Responses**:
- `404 Not Found` - Equipment not found
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - No access to this equipment

---

### 3. POST /api/v1/equipment (Create Equipment)

**Purpose**: Create new equipment instance with comprehensive metadata

**Method**: `POST`

**Request Headers**:
```http
Content-Type: application/json
Authorization: Bearer [TOKEN]
```

**Request Body**:
```json
{
  "name": "Transformer-Main-01",
  "description": "Main step-down transformer for facility",
  "equipment_type": "Transformer",
  "manufacturer": "Siemens",
  "model": "SGB 500 MVA",
  "serial_number": "SN-TRANS-2024-001",
  "asset_id": "ASSET-TRANS-001",
  "firmware_version": "N/A",
  "operating_system": "Standalone",
  "ip_address": "192.168.2.100",
  "mac_address": "00:0b:95:9d:68:17",
  "location": {
    "facility_id": "fac_energy_001",
    "sector": "Energy",
    "region": "Southeast",
    "building": "Substation Main",
    "floor": 1,
    "room": "High Voltage Section"
  },
  "specifications": {
    "power_consumption": 0,
    "operating_voltage": "138 kV / 13.8 kV",
    "temperature_range": "-30 to +60°C",
    "sil_rating": 0,
    "iec_62443_level": 1
  },
  "lifecycle": {
    "acquisition_date": "2020-03-10",
    "installation_date": "2020-04-15",
    "last_maintenance": "2025-10-20",
    "warranty_expiry": "2025-03-10",
    "end_of_life_date": "2050-04-15"
  },
  "network": {
    "network_segment": "Energy_Grid_Segment",
    "vlan_id": 200,
    "firewall_rule_id": "fwr_transformer_001",
    "is_connected": false,
    "connection_type": "Serial"
  },
  "compliance": {
    "nerc_cip": true,
    "isc_iec_62443": true,
    "iso_27001": true,
    "hipaa": false,
    "pci_dss": false
  },
  "metadata": {
    "owner": "Energy Operations",
    "responsible_team": "Electrical Maintenance",
    "tags": ["transformer", "critical", "energy"],
    "custom_fields": {
      "budget_center": "ENG-001",
      "vendor_contact": "support@siemens.com"
    }
  }
}
```

**Response Status**: `201 Created`

**Response Payload** (201 Created):
```json
{
  "status": "success",
  "code": 201,
  "data": {
    "id": "equip_def456ghi",
    "name": "Transformer-Main-01",
    "equipment_type": "Transformer",
    "serial_number": "SN-TRANS-2024-001",
    "status": "active",
    "created_at": "2025-11-25T14:40:00Z",
    "message": "Equipment created successfully"
  },
  "meta": {
    "timestamp": "2025-11-25T14:40:00Z",
    "request_id": "req_def456ghi"
  }
}
```

**Error Responses**:
- `400 Bad Request` - Missing required fields or validation error
- `409 Conflict` - Duplicate serial number exists
- `422 Unprocessable Entity` - Invalid data format
- `401 Unauthorized` - Invalid token

---

### 4. PUT /api/v1/equipment/{id} (Update Equipment)

**Purpose**: Update existing equipment with version control

**Method**: `PUT`

**Path Parameters**:
```
{id} - Equipment ID
```

**Request Body** (partial update supported):
```json
{
  "name": "PLC-Control-System-01-Updated",
  "firmware_version": "3.1.5",
  "last_maintenance": "2025-11-25",
  "compliance": {
    "nerc_cip": true,
    "iec_62443": true,
    "iso_27001": true,
    "compliance_score": 96
  },
  "metadata": {
    "responsible_team": "Maintenance Division - Updated"
  }
}
```

**Request Example**:
```http
PUT /api/v1/equipment/equip_abc123xyz
Content-Type: application/json
Authorization: Bearer [TOKEN]
```

**Response Status**: `200 OK`

**Response Payload** (200 OK):
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": "equip_abc123xyz",
    "name": "PLC-Control-System-01-Updated",
    "equipment_type": "PLC",
    "updated_at": "2025-11-25T14:45:00Z",
    "version": 13,
    "message": "Equipment updated successfully",
    "changed_fields": [
      "name",
      "firmware_version",
      "last_maintenance",
      "compliance.compliance_score"
    ]
  },
  "meta": {
    "timestamp": "2025-11-25T14:45:00Z"
  }
}
```

**Error Responses**:
- `404 Not Found` - Equipment not found
- `409 Conflict` - Concurrent modification detected
- `422 Unprocessable Entity` - Invalid data format
- `401 Unauthorized` - Invalid token

---

### 5. DELETE /api/v1/equipment/{id} (Decommission)

**Purpose**: Decommission equipment and mark end-of-life (soft delete)

**Method**: `DELETE`

**Path Parameters**:
```
{id} - Equipment ID
```

**Query Parameters**:
```
?reason=obsolete|damaged|replaced&notes=Replaced with newer model&archive=true
```

**Request Example**:
```http
DELETE /api/v1/equipment/equip_abc123xyz?reason=replaced&archive=true
Authorization: Bearer [TOKEN]
```

**Response Status**: `200 OK`

**Response Payload** (200 OK):
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": "equip_abc123xyz",
    "name": "PLC-Control-System-01",
    "status": "deprecated",
    "decommissioned_at": "2025-11-25T14:50:00Z",
    "decommission_reason": "replaced",
    "decommission_notes": "Replaced with newer model",
    "archived": true,
    "message": "Equipment decommissioned successfully"
  },
  "meta": {
    "timestamp": "2025-11-25T14:50:00Z"
  }
}
```

**Error Responses**:
- `404 Not Found` - Equipment not found
- `400 Bad Request` - Invalid reason parameter
- `401 Unauthorized` - Invalid token

---

### 6. GET /api/v1/equipment/{id}/vulnerabilities (CVE Details)

**Purpose**: Retrieve detailed CVE and vulnerability information for specific equipment

**Method**: `GET`

**Path Parameters**:
```
{id} - Equipment ID
```

**Query Parameters**:
```
?severity=critical,high&include_patches=true&sort=published_date:desc
```

**Request Example**:
```http
GET /api/v1/equipment/equip_abc123xyz/vulnerabilities?severity=critical,high
Authorization: Bearer [TOKEN]
```

**Response Status**: `200 OK`

**Response Payload** (200 OK):
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "equipment_id": "equip_abc123xyz",
    "equipment_name": "PLC-Control-System-01",
    "manufacturer": "Siemens",
    "model": "S7-1500",
    "total_cves": 3,
    "vulnerabilities": [
      {
        "cve_id": "CVE-2024-1234",
        "severity": "high",
        "cvss_v3_score": 8.2,
        "cvss_v3_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H",
        "published_date": "2024-06-15",
        "updated_date": "2024-09-20",
        "description": "Improper input validation in S7-1500 authentication mechanism",
        "affected_versions": ["3.0.0", "3.0.5", "3.1.0", "3.1.3"],
        "patch_version": "3.1.4",
        "patch_released": "2024-07-10",
        "patch_available": true,
        "remediation": "Update firmware to version 3.1.4 or higher",
        "exploit_available": true,
        "exploit_ease": "high",
        "known_exploited": true,
        "reference_urls": [
          "https://nvd.nist.gov/vuln/detail/CVE-2024-1234",
          "https://www.siemens.com/security"
        ]
      },
      {
        "cve_id": "CVE-2024-5678",
        "severity": "medium",
        "cvss_v3_score": 6.5,
        "published_date": "2024-08-22",
        "description": "Information disclosure in PROFINET communication",
        "affected_versions": ["2.8.0", "3.0.0", "3.1.0"],
        "patch_version": "3.1.4",
        "patch_available": true
      },
      {
        "cve_id": "CVE-2024-9999",
        "severity": "medium",
        "cvss_v3_score": 5.8,
        "published_date": "2024-09-10",
        "description": "Weak cryptographic implementation in firmware update mechanism",
        "affected_versions": ["3.0.0", "3.0.5", "3.1.0", "3.1.3"],
        "patch_version": "3.1.5",
        "patch_available": true
      }
    ],
    "summary": {
      "critical": 0,
      "high": 1,
      "medium": 2,
      "low": 0,
      "patches_available": 2,
      "firmware_current": "3.1.4",
      "firmware_latest": "3.1.5",
      "days_since_last_assessment": 0,
      "risk_level": "Medium",
      "recommended_action": "Apply available patches and upgrade to latest firmware"
    }
  },
  "meta": {
    "timestamp": "2025-11-25T14:55:00Z",
    "last_assessment": "2025-11-25T10:00:00Z"
  }
}
```

**Error Responses**:
- `404 Not Found` - Equipment not found
- `401 Unauthorized` - Invalid token
- `503 Service Unavailable` - Vulnerability database unavailable

---

## 5-Step Customer Loading Process

The equipment API follows a structured 5-step process for onboarding new customer equipment:

### Step 1: Equipment Discovery & Inventory

**Objective**: Identify and catalog all equipment in customer environment

**API Operations**:
```bash
# Step 1.1: Get equipment count by type
GET /api/v1/equipment?customer_id=cust_xyz&group_by=equipment_type

# Step 1.2: Get equipment by location
GET /api/v1/equipment?customer_id=cust_xyz&location.facility_id=fac_001

# Step 1.3: Identify equipment without metadata
GET /api/v1/equipment?customer_id=cust_xyz&filters.metadata.incomplete=true
```

**Expected Outcome**: Complete equipment list with 85%+ asset identification

**Timeline**: 1-3 days depending on customer infrastructure size

---

### Step 2: Equipment Profile Enrichment

**Objective**: Fill in complete equipment specifications and metadata

**API Operations**:
```bash
# Step 2.1: Create bulk equipment records (batch)
POST /api/v1/equipment/bulk
{
  "equipment": [
    {"name": "PLC-001", "manufacturer": "Siemens", ...},
    {"name": "Router-Main", "manufacturer": "Cisco", ...}
  ]
}

# Step 2.2: Update equipment with enhanced data
PUT /api/v1/equipment/{id}
{
  "specifications": {...},
  "compliance": {...},
  "network": {...}
}

# Step 2.3: Validate equipment records
GET /api/v1/equipment/{id}/validation
```

**Expected Outcome**: 95%+ data completeness across all fields

**Timeline**: 3-5 days for typical customer

---

### Step 3: Vulnerability Assessment Integration

**Objective**: Map equipment to known vulnerabilities and CVEs

**API Operations**:
```bash
# Step 3.1: Trigger vulnerability assessment
POST /api/v1/equipment/{id}/assess-vulnerabilities
{
  "assessment_type": "cve_mapping|risk_analysis|compliance_check"
}

# Step 3.2: Retrieve vulnerability summary
GET /api/v1/equipment/{id}/vulnerabilities?include_patches=true

# Step 3.3: Get vulnerability trends
GET /api/v1/equipment?customer_id=cust_xyz&vulnerabilities.has_cves=true
```

**Expected Outcome**: Complete CVE mapping with risk scoring

**Timeline**: 1-2 days (automated)

---

### Step 4: Lifecycle & Compliance Baseline

**Objective**: Establish equipment lifecycle tracking and compliance posture

**API Operations**:
```bash
# Step 4.1: Update lifecycle dates
PUT /api/v1/equipment/{id}
{
  "lifecycle": {
    "acquisition_date": "2020-01-15",
    "warranty_expiry": "2025-01-15",
    "end_of_life_date": "2030-02-20"
  }
}

# Step 4.2: Configure compliance standards
PUT /api/v1/equipment/{id}
{
  "compliance": {
    "nerc_cip": true,
    "iec_62443": true,
    "iso_27001": true
  }
}

# Step 4.3: Validate compliance status
GET /api/v1/equipment?customer_id=cust_xyz&filters.compliance.min_score=85
```

**Expected Outcome**: Compliance baseline with risk assessment

**Timeline**: 2-3 days for typical customer

---

### Step 5: Production Handoff & Monitoring Setup

**Objective**: Transition to monitoring and continuous management

**API Operations**:
```bash
# Step 5.1: Mark equipment as production-ready
PUT /api/v1/equipment/{id}
{
  "status": "active",
  "monitoring_enabled": true
}

# Step 5.2: Configure monitoring thresholds
POST /api/v1/equipment/{id}/monitoring-config
{
  "vulnerability_alert_threshold": "high",
  "lifecycle_alert_enabled": true,
  "compliance_drift_detection": true
}

# Step 5.3: Verify integration with downstream systems
GET /api/v1/equipment/{id}?include_integrations=true

# Step 5.4: Generate baseline compliance report
GET /api/v1/equipment?customer_id=cust_xyz&report=baseline_compliance
```

**Expected Outcome**: Production-ready equipment with automated monitoring

**Timeline**: 1 day setup + ongoing monitoring

**Total Process Timeline**: 8-14 days for complete customer onboarding

---

## Frontend Integration

### Equipment Management Dashboard

The frontend integrates with the Equipment API through a comprehensive dashboard:

#### Dashboard Sections

**1. Equipment Inventory View**
```jsx
// React component example
<EquipmentTable
  filters={{
    sector: 'Water',
    status: 'active',
    vulnerability: 'high'
  }}
  columns={['name', 'type', 'manufacturer', 'status', 'vulnerabilities']}
  pageSize={20}
  onSelectEquipment={handleEquipmentSelect}
/>
```

**2. Equipment Detail Panel**
```jsx
<EquipmentDetailPanel
  equipmentId="equip_abc123xyz"
  sections={[
    'overview',
    'specifications',
    'vulnerabilities',
    'compliance',
    'lifecycle',
    'audit_trail'
  ]}
/>
```

**3. Vulnerability Dashboard**
```jsx
<VulnerabilityDashboard
  equipmentId="equip_abc123xyz"
  severityFilter={['critical', 'high']}
  showPatchAvailability={true}
/>
```

**4. Lifecycle Management**
```jsx
<LifecycleTimeline
  equipmentId="equip_abc123xyz"
  showWarranty={true}
  showEOL={true}
  alertDaysBeforeEOL={90}
/>
```

### Frontend Integration Points

**Search/Filter Component**:
```javascript
const searchEquipment = async (filters) => {
  const response = await fetch('/api/v1/equipment', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filters })
  });
  return response.json();
};
```

**Create Equipment Form**:
```javascript
const createEquipment = async (formData) => {
  const response = await fetch('/api/v1/equipment', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  });
  return response.json();
};
```

**Equipment Update Handler**:
```javascript
const updateEquipment = async (equipmentId, updates) => {
  const response = await fetch(`/api/v1/equipment/${equipmentId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
  return response.json();
};
```

**Real-time Monitoring**:
```javascript
// WebSocket connection for real-time updates
const ws = new WebSocket('wss://api.aeon-digital-twin.com/api/v1/equipment/watch');
ws.onmessage = (event) => {
  const { equipmentId, changes } = JSON.parse(event.data);
  updateEquipmentDisplay(equipmentId, changes);
};
```

---

## Business Value & Use Cases

### Asset Tracking & Inventory Management

**Business Value**:
- Complete visibility into 1.1M+ equipment assets across 16 sectors
- Automated asset tracking reduces inventory costs by 35-40%
- Real-time location and status tracking

**Use Case**: Water Utility Operator
```
Scenario: Water utility manages 150 treatment facilities with 5,000+ pieces of equipment
Solution: Equipment API enables:
- Centralized equipment catalog across all facilities
- Automated inventory audits
- Maintenance scheduling based on age and condition
- Spare parts planning and supply chain optimization
Result: 25% reduction in emergency maintenance costs
```

### Lifecycle Management & Planning

**Business Value**:
- Optimize equipment replacement cycles
- Reduce warranty claim processing time by 60%
- Proactive maintenance scheduling

**Use Case**: Energy Provider Transformer Management
```
Scenario: Energy provider with 200 transformers across region
Solution: Equipment API enables:
- Lifecycle tracking for each transformer
- Warranty expiry alerts (90 days before)
- End-of-life planning and budget allocation
- Maintenance history correlation with failure rates
Result: 40% reduction in unexpected transformer failures
```

### Vulnerability Management & Risk Assessment

**Business Value**:
- Automated CVE mapping to deployed equipment
- Risk scoring and prioritization
- Patch management coordination

**Use Case**: Manufacturing Facility Security
```
Scenario: Manufacturing plant with 300 industrial control devices
Solution: Equipment API enables:
- Automatic CVE matching against equipment models
- Risk level calculation based on exploitability
- Patch availability notification
- Compliance validation (IEC 62443)
Result: 75% faster vulnerability response time
```

### Compliance & Audit Reporting

**Business Value**:
- Automated compliance score calculation
- Audit trail for all equipment changes
- Real-time compliance dashboard

**Use Case**: Water Utility NERC CIP Compliance
```
Scenario: Water utility subject to NERC CIP compliance
Solution: Equipment API enables:
- Track NERC CIP compliance status per equipment
- Generate audit reports on demand
- Document change history and approvals
- Compliance drift detection
Result: 90% faster compliance audit preparation
```

### Sector-Specific Analytics

**Business Value**:
- Cross-sector risk analysis
- Benchmarking against industry standards
- Predictive maintenance insights

**Use Case**: Multi-Sector Critical Infrastructure Operator
```
Scenario: Operator managing equipment across Water, Energy, and Transportation
Solution: Equipment API enables:
- Sector-specific vulnerability trends
- Cross-sector risk correlation analysis
- Equipment failure prediction by type
- Resource allocation optimization
Result: 30% improvement in asset utilization efficiency
```

---

## Error Handling

### Standard Error Response Format

All error responses follow consistent format:

```json
{
  "status": "error",
  "code": 400,
  "error": {
    "type": "validation_error",
    "message": "One or more fields are invalid",
    "details": [
      {
        "field": "serial_number",
        "issue": "Duplicate serial number exists",
        "code": "DUPLICATE_VALUE"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-25T14:56:00Z",
    "request_id": "req_xyz789"
  }
}
```

### HTTP Status Codes

| Code | Meaning | Scenario |
|------|---------|----------|
| 200 | OK | Successful GET/PUT request |
| 201 | Created | Equipment successfully created |
| 400 | Bad Request | Invalid filter parameters or malformed JSON |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | User lacks permission for resource |
| 404 | Not Found | Equipment ID doesn't exist |
| 409 | Conflict | Duplicate serial number or concurrent modification |
| 422 | Unprocessable Entity | Validation error in request body |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Common Error Codes

```yaml
validation_error:
  code: 400
  causes: ["Missing required field", "Invalid data type", "Value out of range"]

duplicate_serial_number:
  code: 409
  causes: ["Serial number already exists in system"]
  resolution: "Use unique serial number or retrieve existing equipment"

unauthorized:
  code: 401
  causes: ["Token expired", "Invalid token format", "Token revoked"]
  resolution: "Obtain new token via /auth/token endpoint"

rate_limit:
  code: 429
  causes: ["Exceeded 1000 requests/minute quota"]
  retry_after: 60
  resolution: "Implement exponential backoff, reduce request frequency"

equipment_not_found:
  code: 404
  causes: ["Equipment ID doesn't exist", "Equipment was archived"]
  resolution: "Verify equipment ID, check if equipment was decommissioned"
```

---

## Code Examples

### Python - Search Equipment

```python
import requests

API_BASE = 'https://api.aeon-digital-twin.com/api/v1'
TOKEN = 'your_bearer_token_here'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# Search for critical equipment with CVEs
filters = {
    'filters': {
        'sector': 'Water',
        'status': 'active',
        'vulnerability': {
            'has_cves': True,
            'cve_severity': 'high'
        }
    },
    'pagination': {
        'page': 1,
        'limit': 50
    }
}

response = requests.get(
    f'{API_BASE}/equipment',
    headers=headers,
    json=filters
)

equipment = response.json()['data']['equipment']
print(f"Found {len(equipment)} critical pieces of equipment")
```

### JavaScript - Create Equipment

```javascript
const createEquipment = async (equipmentData) => {
  const response = await fetch(
    'https://api.aeon-digital-twin.com/api/v1/equipment',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(equipmentData)
    }
  );

  if (!response.ok) {
    const error = await response.json();
    console.error('Error creating equipment:', error.error);
    throw new Error(error.error.message);
  }

  const result = await response.json();
  console.log(`Equipment created with ID: ${result.data.id}`);
  return result.data;
};

// Usage
const newEquipment = {
  name: 'PLC-Control-System-01',
  equipment_type: 'PLC',
  manufacturer: 'Siemens',
  model: 'S7-1500',
  serial_number: 'SN-2024-001-ABC'
};

createEquipment(newEquipment);
```

### cURL - Get Equipment Vulnerabilities

```bash
#!/bin/bash

EQUIPMENT_ID="equip_abc123xyz"
TOKEN="your_bearer_token"
API_BASE="https://api.aeon-digital-twin.com/api/v1"

curl -X GET \
  "${API_BASE}/equipment/${EQUIPMENT_ID}/vulnerabilities?severity=critical,high" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .
```

### Go - Update Equipment

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

type EquipmentUpdate struct {
    FirmwareVersion string `json:"firmware_version"`
    LastMaintenance string `json:"last_maintenance"`
}

func updateEquipment(equipmentID, token string, update EquipmentUpdate) error {
    body, _ := json.Marshal(update)

    req, _ := http.NewRequest(
        "PUT",
        fmt.Sprintf("https://api.aeon-digital-twin.com/api/v1/equipment/%s", equipmentID),
        bytes.NewBuffer(body),
    )

    req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", token))
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.StatusCode != 200 {
        return fmt.Errorf("API returned status %d", resp.StatusCode)
    }

    return nil
}
```

---

## Integration Patterns

### Real-Time Monitoring Integration

```javascript
// WebSocket connection for real-time equipment updates
class EquipmentMonitor {
  constructor(token) {
    this.token = token;
    this.ws = null;
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(
      'wss://api.aeon-digital-twin.com/api/v1/equipment/watch',
      { authorization: `Bearer ${this.token}` }
    );

    this.ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      this.handleEquipmentUpdate(update);
    };
  }

  handleEquipmentUpdate(update) {
    console.log(`Equipment ${update.id} changed:`, update.changes);
    // Update UI with real-time changes
  }
}
```

### Batch Processing Integration

```python
import concurrent.futures
import requests

def process_equipment_batch(equipment_ids, token):
    """Process multiple equipment IDs concurrently"""
    headers = {'Authorization': f'Bearer {token}'}

    def fetch_equipment(eq_id):
        resp = requests.get(
            f'https://api.aeon-digital-twin.com/api/v1/equipment/{eq_id}',
            headers=headers
        )
        return resp.json()['data']

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_equipment, equipment_ids)

    return list(results)
```

### Webhook Integration for Events

```javascript
// Register webhook for equipment changes
const registerWebhook = async (token, webhookUrl) => {
  const response = await fetch(
    'https://api.aeon-digital-twin.com/api/v1/webhooks',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        url: webhookUrl,
        events: [
          'equipment.created',
          'equipment.updated',
          'equipment.vulnerability.detected',
          'equipment.compliance.drift'
        ]
      })
    }
  );
  return response.json();
};
```

---

## Summary

The Equipment API provides a complete, production-ready solution for equipment asset management, lifecycle tracking, and vulnerability integration across critical infrastructure environments. With support for 1.1M+ equipment instances and integration across 16 critical infrastructure sectors, the API enables comprehensive digital asset management at enterprise scale.

**Key Capabilities**:
- Comprehensive equipment search and filtering
- Complete equipment lifecycle management
- Automated CVE vulnerability mapping
- Compliance scoring and tracking
- Real-time monitoring and alerts
- Audit trail and version control

**Recommended Next Steps**:
1. Review authentication requirements and obtain API credentials
2. Begin Step 1 of customer loading process (Equipment Discovery)
3. Implement frontend integration using provided code examples
4. Set up monitoring and alerting for vulnerabilities
5. Deploy to production environment

**Documentation Version**: 1.0.0
**Last Updated**: 2025-11-25
**Status**: Production-Ready
