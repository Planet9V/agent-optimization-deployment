# Equipment Core API Documentation

**File**: EQUIPMENT_API_DOCUMENTATION.md
**Created**: 2025-12-12 05:00:00 UTC
**Version**: v1.0.0
**Status**: PRODUCTION READY
**Sprint**: Sprint 1 - Tier 1 APIs

---

## Overview

The Equipment Core API provides comprehensive equipment asset management capabilities for the AEON Cybersecurity Platform, including lifecycle tracking, vendor relationships, EOL management, and risk assessment.

### API Summary

| Endpoint | Method | ICE Score | Description |
|----------|--------|-----------|-------------|
| `/api/v2/equipment` | POST | 7.29 | Create equipment records with vendor linking |
| `/api/v2/equipment/{id}` | GET | 9.0 | Retrieve equipment details with vulnerabilities |
| `/api/v2/equipment/summary` | GET | 8.0 | Equipment statistics by sector/vendor/status |
| `/api/v2/equipment/eol-report` | GET | 6.4 | EOL risk assessment and timeline analysis |

**Total Endpoints**: 4 core + 3 utility = 7 endpoints
**Average ICE Score**: 7.66

---

## Table of Contents

1. [Authentication & Authorization](#authentication--authorization)
2. [Data Models](#data-models)
3. [API Endpoints](#api-endpoints)
4. [Usage Examples](#usage-examples)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)
7. [Integration Patterns](#integration-patterns)

---

## Authentication & Authorization

### Multi-Tenant Access Control

All equipment endpoints enforce multi-tenant isolation:

```typescript
// Frontend authentication
import { useAuth } from '@clerk/nextjs';

const { getToken } = useAuth();
const token = await getToken();

// Include in all requests
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### Customer ID Injection

Customer ID is automatically injected from authentication token. No need to include `customer_id` in request bodies.

---

## Data Models

### Core Equipment Model

```typescript
interface Equipment {
  // Identification
  equipment_id: string;
  name: string;
  equipment_type: EquipmentType;
  manufacturer: string;
  model: string;
  serial_number?: string;
  asset_tag?: string;

  // Classification
  sector: string;  // energy, finance, healthcare, etc.
  location?: string;

  // Vendor Relationship
  vendor_id?: string;
  vendor_name?: string;

  // Lifecycle Status
  status: EquipmentStatus;
  purchase_date?: string;  // ISO 8601
  warranty_expiry?: string;
  eol_date?: string;
  eos_date?: string;
  days_until_eol?: number;
  days_until_eos?: number;

  // Technical Details
  firmware_version?: string;
  os_version?: string;
  ip_address?: string;
  mac_address?: string;

  // Risk Assessment
  vulnerability_count: number;
  critical_vulnerability_count: number;
  high_vulnerability_count: number;
  risk_score: number;  // 0-10
  risk_level: RiskLevel;
  eol_risk_level: RiskLevel;

  // SBOM Integration
  sbom_component_ids: string[];
  software_count: number;

  // Metadata
  description?: string;
  tags: string[];
  metadata: Record<string, any>;

  // Audit
  customer_id: string;
  created_at: string;
  updated_at: string;
  last_scan_date?: string;
  last_seen_online?: string;
}
```

### Enums

```typescript
enum EquipmentType {
  NETWORK_DEVICE = 'network_device',
  SERVER = 'server',
  WORKSTATION = 'workstation',
  MOBILE_DEVICE = 'mobile_device',
  IOT_DEVICE = 'iot_device',
  SECURITY_APPLIANCE = 'security_appliance',
  STORAGE_DEVICE = 'storage_device',
  INFRASTRUCTURE = 'infrastructure'
}

enum EquipmentStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  MAINTENANCE = 'maintenance',
  DECOMMISSIONED = 'decommissioned',
  PENDING_DEPLOYMENT = 'pending_deployment',
  EOL_WARNING = 'eol_warning',      // <180 days to EOL
  EOL_CRITICAL = 'eol_critical'     // <90 days to EOL
}

enum RiskLevel {
  CRITICAL = 'critical',  // 8.0-10.0
  HIGH = 'high',          // 6.0-7.9
  MEDIUM = 'medium',      // 4.0-5.9
  LOW = 'low',            // 2.0-3.9
  NONE = 'none'           // 0.0-1.9
}
```

### Equipment Summary Model

```typescript
interface EquipmentSummary {
  total_equipment: number;
  by_status: Record<string, number>;
  by_type: Record<string, number>;
  by_sector: Record<string, number>;
  by_vendor: Record<string, number>;
  by_risk_level: Record<string, number>;

  // EOL Statistics
  total_eol_approaching: number;   // <180 days
  total_eol_critical: number;      // <90 days
  total_past_eol: number;

  // Vulnerability Statistics
  total_with_vulnerabilities: number;
  total_with_critical_vulnerabilities: number;
  avg_risk_score: number;

  // Maintenance Statistics
  total_active: number;
  total_maintenance: number;
  total_decommissioned: number;

  customer_id: string;
  generated_at: string;
}
```

### EOL Report Model

```typescript
interface EOLReport {
  report_id: string;
  customer_id: string;
  generated_at: string;

  // Summary Statistics
  total_equipment_reviewed: number;
  total_eol_approaching: number;
  total_eol_critical: number;
  total_past_eol: number;
  total_past_eos: number;

  // Risk Breakdown
  critical_risk_count: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;

  // Equipment List
  equipment: EOLEquipment[];

  // Analysis by Category
  by_sector: Record<string, number>;
  by_type: Record<string, number>;
  by_vendor: Record<string, number>;

  // Action Requirements
  immediate_action_required: number;
  planning_required: number;
}

interface EOLEquipment {
  equipment_id: string;
  name: string;
  equipment_type: EquipmentType;
  manufacturer: string;
  model: string;
  sector: string;
  vendor_name?: string;

  eol_date?: string;
  eos_date?: string;
  days_until_eol?: number;
  days_until_eos?: number;

  status: EquipmentStatus;
  eol_risk_level: RiskLevel;

  vulnerability_count: number;
  critical_vulnerability_count: number;
  risk_score: number;

  replacement_available: boolean;
  migration_plan_exists: boolean;
  business_impact: string;
  location?: string;
}
```

---

## API Endpoints

### 1. Create Equipment

**POST** `/api/v2/equipment`

Create new equipment record with vendor linking and lifecycle management.

#### Request Body

```typescript
{
  name: string;
  equipment_type: EquipmentType;
  manufacturer: string;
  model: string;
  serial_number?: string;
  asset_tag?: string;
  location?: string;
  sector: string;

  vendor_id?: string;           // Link to vendor
  purchase_date?: string;       // ISO 8601
  warranty_expiry?: string;
  eol_date?: string;
  eos_date?: string;

  firmware_version?: string;
  os_version?: string;
  ip_address?: string;
  mac_address?: string;
  description?: string;
  tags?: string[];
  metadata?: Record<string, any>;
}
```

#### Response

```typescript
{
  equipment_id: string;
  // ... all equipment fields
  status: EquipmentStatus;      // Auto-calculated
  days_until_eol: number;       // Auto-calculated
  eol_risk_level: RiskLevel;    // Auto-calculated
  vendor_name?: string;         // From vendor link
}
```

#### Status Codes

- `201 Created`: Equipment created successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing/invalid authentication
- `500 Internal Server Error`: Server error

#### Example

```typescript
const response = await fetch('/api/v2/equipment', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: "Core Router - Building A",
    equipment_type: "network_device",
    manufacturer: "Cisco",
    model: "ISR4451-X",
    serial_number: "FDO2345X1Y2",
    sector: "energy",
    vendor_id: "vendor_cisco_001",
    eol_date: "2026-08-15",
    tags: ["critical", "core-network"]
  })
});

const equipment = await response.json();
console.log(`Created equipment: ${equipment.equipment_id}`);
```

---

### 2. Get Equipment Details

**GET** `/api/v2/equipment/{equipment_id}`

Retrieve comprehensive equipment details including vendor, vulnerabilities, and SBOM components.

#### Path Parameters

- `equipment_id`: Unique equipment identifier

#### Response

```typescript
Equipment  // Full equipment object with all fields
```

#### Status Codes

- `200 OK`: Equipment retrieved
- `404 Not Found`: Equipment not found
- `401 Unauthorized`: Missing/invalid authentication

#### Example

```typescript
const response = await fetch(`/api/v2/equipment/${equipmentId}`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const equipment = await response.json();

console.log(`Risk Score: ${equipment.risk_score}`);
console.log(`Days until EOL: ${equipment.days_until_eol}`);
console.log(`Vulnerabilities: ${equipment.critical_vulnerability_count} critical`);
```

---

### 3. Get Equipment Summary

**GET** `/api/v2/equipment/summary`

Retrieve equipment statistics aggregated by sector, vendor, status, and risk level.

#### Response

```typescript
EquipmentSummary  // Statistics object
```

#### Status Codes

- `200 OK`: Summary generated
- `404 Not Found`: No equipment found
- `401 Unauthorized`: Missing/invalid authentication

#### Example

```typescript
const response = await fetch('/api/v2/equipment/summary', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const summary = await response.json();

console.log(`Total Equipment: ${summary.total_equipment}`);
console.log(`EOL Approaching: ${summary.total_eol_approaching}`);
console.log(`Average Risk Score: ${summary.avg_risk_score}`);

// Breakdown by sector
Object.entries(summary.by_sector).forEach(([sector, count]) => {
  console.log(`${sector}: ${count} devices`);
});
```

---

### 4. Get EOL Report

**GET** `/api/v2/equipment/eol-report`

Generate comprehensive end-of-life analysis report with risk assessment.

#### Query Parameters

- `eol_threshold_days` (optional, default: 180): Days until EOL threshold
- `include_past_eol` (optional, default: true): Include past-EOL equipment
- `sector` (optional): Filter by sector
- `equipment_type` (optional): Filter by equipment type
- `min_risk_level` (optional): Minimum risk level (low, medium, high, critical)

#### Response

```typescript
EOLReport  // Complete EOL analysis report
```

#### Status Codes

- `200 OK`: Report generated
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Missing/invalid authentication

#### Example

```typescript
const response = await fetch(
  '/api/v2/equipment/eol-report?eol_threshold_days=90&min_risk_level=high',
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);

const report = await response.json();

console.log(`EOL Report: ${report.report_id}`);
console.log(`Immediate Action Required: ${report.immediate_action_required}`);

// Process high-risk equipment
report.equipment
  .filter(eq => eq.eol_risk_level === 'critical')
  .forEach(eq => {
    console.log(`CRITICAL: ${eq.name} - ${eq.days_until_eol} days until EOL`);
  });
```

---

## Usage Examples

### React Hooks

```typescript
// hooks/useEquipment.ts
import { useAuth } from '@clerk/nextjs';
import useSWR from 'swr';

export function useEquipment(equipmentId: string) {
  const { getToken } = useAuth();

  const fetcher = async (url: string) => {
    const token = await getToken();
    const res = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) throw new Error('Failed to fetch');
    return res.json();
  };

  const { data, error, mutate } = useSWR(
    `/api/v2/equipment/${equipmentId}`,
    fetcher
  );

  return {
    equipment: data,
    isLoading: !error && !data,
    isError: error,
    refresh: mutate
  };
}

export function useEquipmentSummary() {
  const { getToken } = useAuth();

  const fetcher = async (url: string) => {
    const token = await getToken();
    const res = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return res.json();
  };

  return useSWR('/api/v2/equipment/summary', fetcher);
}

export function useEOLReport(params?: {
  threshold?: number;
  sector?: string;
}) {
  const { getToken } = useAuth();

  const queryString = new URLSearchParams({
    ...(params?.threshold && { eol_threshold_days: params.threshold.toString() }),
    ...(params?.sector && { sector: params.sector })
  }).toString();

  const fetcher = async (url: string) => {
    const token = await getToken();
    const res = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return res.json();
  };

  return useSWR(
    `/api/v2/equipment/eol-report?${queryString}`,
    fetcher,
    { refreshInterval: 300000 }  // Refresh every 5 minutes
  );
}
```

### Dashboard Component Example

```typescript
// components/EquipmentDashboard.tsx
import { useEquipmentSummary, useEOLReport } from '@/hooks/useEquipment';

export default function EquipmentDashboard() {
  const { data: summary } = useEquipmentSummary();
  const { data: eolReport } = useEOLReport({ threshold: 90 });

  if (!summary) return <Loading />;

  return (
    <div className="dashboard">
      {/* Total Equipment */}
      <Card>
        <h3>Total Equipment</h3>
        <p className="text-3xl">{summary.total_equipment}</p>
      </Card>

      {/* EOL Status */}
      <Card className="border-red-500">
        <h3>EOL Critical</h3>
        <p className="text-3xl text-red-600">
          {summary.total_eol_critical}
        </p>
        <span className="text-sm">Action required</span>
      </Card>

      {/* Risk Distribution */}
      <Card>
        <h3>Risk Distribution</h3>
        <RiskChart data={summary.by_risk_level} />
      </Card>

      {/* EOL Report */}
      {eolReport && (
        <Card>
          <h3>EOL Report</h3>
          <p>Immediate Action: {eolReport.immediate_action_required}</p>
          <Button onClick={() => downloadReport(eolReport)}>
            Download Report
          </Button>
        </Card>
      )}

      {/* By Sector */}
      <Card>
        <h3>Equipment by Sector</h3>
        <SectorChart data={summary.by_sector} />
      </Card>
    </div>
  );
}
```

---

## Error Handling

### Error Response Format

```typescript
{
  detail: string;
  status_code: number;
  error_code?: string;
}
```

### Common Errors

#### 400 Bad Request
```json
{
  "detail": "Invalid equipment_type: invalid_type",
  "status_code": 400
}
```

#### 404 Not Found
```json
{
  "detail": "Equipment eq_12345 not found",
  "status_code": 404
}
```

#### 401 Unauthorized
```json
{
  "detail": "Invalid or expired authentication token",
  "status_code": 401
}
```

### Error Handling Pattern

```typescript
async function fetchEquipment(id: string) {
  try {
    const response = await fetch(`/api/v2/equipment/${id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Unknown error');
    }

    return await response.json();
  } catch (error) {
    console.error('Equipment fetch failed:', error);
    throw error;
  }
}
```

---

## Best Practices

### 1. EOL Monitoring

```typescript
// Check EOL status regularly
const checkEOLStatus = (equipment: Equipment) => {
  if (equipment.status === 'eol_critical') {
    // Alert administrators
    sendAlert({
      type: 'critical',
      message: `${equipment.name} has ${equipment.days_until_eol} days until EOL`
    });
  }
};
```

### 2. Risk Assessment

```typescript
// Prioritize equipment by risk
const prioritizeEquipment = (equipment: Equipment[]) => {
  return equipment.sort((a, b) => {
    // Sort by risk level, then by days until EOL
    if (a.risk_score !== b.risk_score) {
      return b.risk_score - a.risk_score;
    }
    return (a.days_until_eol || 999) - (b.days_until_eol || 999);
  });
};
```

### 3. Vendor Management

```typescript
// Always link equipment to vendors
const createEquipmentWithVendor = async (data: EquipmentCreate) => {
  // Ensure vendor exists first
  const vendor = await ensureVendorExists(data.manufacturer);

  // Create equipment with vendor link
  return await fetch('/api/v2/equipment', {
    method: 'POST',
    body: JSON.stringify({
      ...data,
      vendor_id: vendor.vendor_id
    })
  });
};
```

### 4. Bulk Operations

```typescript
// Use bulk endpoint for multiple equipment
const importEquipment = async (equipmentList: EquipmentCreate[]) => {
  // Process in batches of 100
  const batches = chunk(equipmentList, 100);

  for (const batch of batches) {
    const response = await fetch('/api/v2/equipment/bulk', {
      method: 'POST',
      body: JSON.stringify(batch)
    });

    const result = await response.json();
    console.log(`Created ${result.created_count} equipment`);

    // Handle errors
    if (result.errors.length > 0) {
      console.error('Errors:', result.errors);
    }
  }
};
```

---

## Integration Patterns

### Integration with SBOM API

```typescript
// Link equipment to SBOM components
const linkEquipmentSBOM = async (equipmentId: string) => {
  // 1. Get equipment details
  const equipment = await fetch(`/api/v2/equipment/${equipmentId}`);

  // 2. Query SBOM for equipment
  const sbomComponents = await fetch(
    `/api/v2/sbom/equipment/${equipmentId}`
  );

  // 3. Display combined view
  return {
    equipment,
    software: sbomComponents,
    vulnerabilities: sbomComponents.flatMap(c => c.vulnerabilities)
  };
};
```

### Integration with Vendor API

```typescript
// Get equipment with full vendor details
const getEquipmentWithVendor = async (equipmentId: string) => {
  const equipment = await fetch(`/api/v2/equipment/${equipmentId}`);

  if (equipment.vendor_id) {
    const vendor = await fetch(`/api/v2/vendors/${equipment.vendor_id}`);
    return { ...equipment, vendor };
  }

  return equipment;
};
```

### Integration with Alert Management

```typescript
// Create alert for EOL equipment
const monitorEOLEquipment = async () => {
  const report = await fetch('/api/v2/equipment/eol-report?eol_threshold_days=90');

  // Create alerts for critical equipment
  for (const equipment of report.equipment) {
    if (equipment.eol_risk_level === 'critical') {
      await fetch('/api/v2/alerts', {
        method: 'POST',
        body: JSON.stringify({
          type: 'equipment_eol',
          severity: 'critical',
          title: `Equipment approaching EOL: ${equipment.name}`,
          description: `${equipment.days_until_eol} days until end-of-life`,
          metadata: { equipment_id: equipment.equipment_id }
        })
      });
    }
  }
};
```

---

## Performance Considerations

### Caching Strategy

```typescript
// Cache equipment summary for 5 minutes
const { data: summary } = useSWR(
  '/api/v2/equipment/summary',
  fetcher,
  {
    refreshInterval: 300000,  // 5 minutes
    revalidateOnFocus: false
  }
);

// Cache individual equipment for 1 minute
const { data: equipment } = useSWR(
  `/api/v2/equipment/${id}`,
  fetcher,
  {
    refreshInterval: 60000,  // 1 minute
    dedupingInterval: 10000  // Don't refetch within 10 seconds
  }
);
```

### Pagination

```typescript
// List equipment with pagination
const listEquipment = async (page: number, limit: number = 100) => {
  const skip = page * limit;
  return await fetch(
    `/api/v2/equipment?skip=${skip}&limit=${limit}`
  );
};
```

---

## Qdrant Storage

Equipment implementation and coordination metadata will be stored in Qdrant collection:

**Collection**: `aeon-sprint1/equipment-apis`

**Metadata**:
- Implementation files
- API specifications
- Test results
- Coordination with PM and SBOM dev
- EOL calculation logic
- Risk assessment algorithms

---

## Support

For issues or questions:
- Documentation: `/docs/EQUIPMENT_API_DOCUMENTATION.md`
- API Reference: `/api/v2/equipment/docs` (OpenAPI/Swagger)
- Support: AEON Platform Team

---

**Status**: PRODUCTION READY
**Version**: v1.0.0
**Last Updated**: 2025-12-12
