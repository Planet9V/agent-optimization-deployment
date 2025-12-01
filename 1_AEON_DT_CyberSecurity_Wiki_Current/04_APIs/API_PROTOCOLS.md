# AEON Cyber Digital Twin - Industrial Protocol Analysis API Documentation

**File:** API_PROTOCOLS.md
**Created:** 2025-11-30
**Version:** 1.0.0
**Status:** COMPLETE
**Enhancement:** E16 - Industrial Protocol Security Analysis
**Document Length:** 700+ lines

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [API Overview](#api-overview)
3. [Protocol Catalog Endpoint](#protocol-catalog-endpoint)
4. [Protocol Details Endpoint](#protocol-details-endpoint)
5. [Protocol Vulnerabilities Endpoint](#protocol-vulnerabilities-endpoint)
6. [Protocol Equipment Endpoint](#protocol-equipment-endpoint)
7. [Protocol Hardening Endpoint](#protocol-hardening-endpoint)
8. [Protocol Risk Assessment Endpoint](#protocol-risk-assessment-endpoint)
9. [Neo4j Cypher Queries](#neo4j-cypher-queries)
10. [Frontend Integration](#frontend-integration)
11. [Error Handling](#error-handling)

---

## Executive Summary

The **Industrial Protocol Analysis API** provides comprehensive security assessment of industrial control system protocols for the AEON Cyber Digital Twin. This API enables security teams to:

- **Catalog Protocols**: Track all industrial protocols in use across the organization
- **Assess Vulnerabilities**: Identify protocol-specific CVEs and weaknesses
- **Map Equipment**: Determine which equipment uses vulnerable protocols
- **Recommend Hardening**: Provide protocol-specific security configurations
- **Prioritize Modernization**: Guide protocol upgrade and replacement decisions

**Supported Protocols (11 Total)**:

| Protocol | Type | Security Level | CVE Count |
|----------|------|----------------|-----------|
| Modbus TCP/RTU | Field Bus | LOW | 47 |
| DNP3 | SCADA | MEDIUM | 31 |
| OPC UA | Industrial | HIGH | 12 |
| PROFINET | Ethernet/IP | MEDIUM | 28 |
| EtherNet/IP | Ethernet/IP | MEDIUM | 35 |
| BACnet | Building | LOW | 19 |
| HART | Field Bus | LOW | 8 |
| IEC 61850 | Power Grid | MEDIUM | 22 |
| S7comm | Proprietary | LOW | 41 |
| FINS | Proprietary | LOW | 15 |
| CIP | Industrial | MEDIUM | 24 |

---

## API Overview

### Base URL
```
https://api.aeon-dt.local/api/v1/protocols
```

### API Endpoints

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/` | GET | List all protocols | 300-500ms |
| `/{protocolId}` | GET | Protocol details | 200-400ms |
| `/{protocolId}/vulnerabilities` | GET | Protocol CVEs | 500-800ms |
| `/{protocolId}/equipment` | GET | Equipment using protocol | 1-3 seconds |
| `/{protocolId}/hardening` | GET | Security recommendations | 300-500ms |
| `/risk-assessment` | POST | Multi-protocol risk analysis | 2-5 seconds |

---

## Protocol Catalog Endpoint

### Endpoint Definition

```
GET /api/v1/protocols
```

### Purpose

List all industrial protocols tracked in the system with security posture summary.

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | string | all | Filter: `fieldbus`, `ethernet`, `scada`, `proprietary` |
| `security_level` | string | all | Filter: `LOW`, `MEDIUM`, `HIGH` |
| `has_vulnerabilities` | boolean | all | Filter by CVE presence |

### Example Request

```bash
curl -X GET \
  "https://api.aeon-dt.local/api/v1/protocols?type=ethernet&security_level=MEDIUM" \
  -H "X-API-Key: your_api_key_here"
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:30:00Z",
  "total_protocols": 11,
  "protocols": [
    {
      "protocol_id": "modbus",
      "name": "Modbus TCP/RTU",
      "type": "fieldbus",
      "security_level": "LOW",
      "has_authentication": false,
      "has_encryption": false,
      "vulnerability_count": 47,
      "equipment_count": 2341,
      "risk_score": 8.2
    },
    {
      "protocol_id": "dnp3",
      "name": "DNP3 (Distributed Network Protocol)",
      "type": "scada",
      "security_level": "MEDIUM",
      "has_authentication": true,
      "has_encryption": true,
      "encryption_optional": true,
      "vulnerability_count": 31,
      "equipment_count": 892,
      "risk_score": 6.5
    },
    {
      "protocol_id": "opc-ua",
      "name": "OPC Unified Architecture",
      "type": "industrial",
      "security_level": "HIGH",
      "has_authentication": true,
      "has_encryption": true,
      "certificate_based": true,
      "vulnerability_count": 12,
      "equipment_count": 1456,
      "risk_score": 4.2
    },
    {
      "protocol_id": "profinet",
      "name": "PROFINET",
      "type": "ethernet",
      "security_level": "MEDIUM",
      "has_authentication": true,
      "has_encryption": false,
      "vulnerability_count": 28,
      "equipment_count": 1823,
      "risk_score": 6.8
    },
    {
      "protocol_id": "ethernet-ip",
      "name": "EtherNet/IP",
      "type": "ethernet",
      "security_level": "MEDIUM",
      "has_authentication": true,
      "has_encryption": false,
      "vulnerability_count": 35,
      "equipment_count": 2156,
      "risk_score": 7.1
    },
    {
      "protocol_id": "bacnet",
      "name": "BACnet",
      "type": "building",
      "security_level": "LOW",
      "has_authentication": false,
      "has_encryption": false,
      "vulnerability_count": 19,
      "equipment_count": 3421,
      "risk_score": 7.8
    },
    {
      "protocol_id": "hart",
      "name": "HART Protocol",
      "type": "fieldbus",
      "security_level": "LOW",
      "has_authentication": false,
      "has_encryption": false,
      "vulnerability_count": 8,
      "equipment_count": 4521,
      "risk_score": 5.5
    },
    {
      "protocol_id": "iec61850",
      "name": "IEC 61850",
      "type": "power",
      "security_level": "MEDIUM",
      "has_authentication": true,
      "has_encryption": true,
      "vulnerability_count": 22,
      "equipment_count": 678,
      "risk_score": 6.2
    },
    {
      "protocol_id": "s7comm",
      "name": "S7comm (Siemens S7)",
      "type": "proprietary",
      "security_level": "LOW",
      "has_authentication": false,
      "has_encryption": false,
      "vulnerability_count": 41,
      "equipment_count": 1567,
      "risk_score": 8.5
    },
    {
      "protocol_id": "fins",
      "name": "FINS (Omron)",
      "type": "proprietary",
      "security_level": "LOW",
      "has_authentication": false,
      "has_encryption": false,
      "vulnerability_count": 15,
      "equipment_count": 892,
      "risk_score": 7.2
    },
    {
      "protocol_id": "cip",
      "name": "Common Industrial Protocol",
      "type": "industrial",
      "security_level": "MEDIUM",
      "has_authentication": true,
      "has_encryption": false,
      "vulnerability_count": 24,
      "equipment_count": 1345,
      "risk_score": 6.5
    }
  ],
  "security_summary": {
    "high_security": 1,
    "medium_security": 5,
    "low_security": 5,
    "total_vulnerabilities": 282,
    "average_risk_score": 6.77
  }
}
```

---

## Protocol Details Endpoint

### Endpoint Definition

```
GET /api/v1/protocols/{protocolId}
```

### Purpose

Get comprehensive details about a specific industrial protocol.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `protocolId` | string | Protocol identifier (e.g., `modbus`, `opc-ua`) |

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:35:00Z",
  "protocol": {
    "protocol_id": "modbus",
    "name": "Modbus TCP/RTU",
    "full_name": "Modular Digital Bus Protocol",
    "type": "fieldbus",
    "standard": "IEC 61158, IEC 61784-2",
    "description": "Serial communication protocol for PLCs, widely used in industrial environments",
    "history": {
      "developed_by": "Modicon (Schneider Electric)",
      "year_introduced": 1979,
      "current_version": "Modbus/TCP 1.1b3"
    },
    "variants": [
      {
        "name": "Modbus RTU",
        "transport": "Serial (RS-232/RS-485)",
        "ports": ["N/A - Serial"]
      },
      {
        "name": "Modbus ASCII",
        "transport": "Serial",
        "ports": ["N/A - Serial"]
      },
      {
        "name": "Modbus TCP",
        "transport": "TCP/IP",
        "ports": ["502/TCP"]
      },
      {
        "name": "Modbus UDP",
        "transport": "UDP/IP",
        "ports": ["502/UDP"]
      }
    ],
    "security_profile": {
      "security_level": "LOW",
      "has_authentication": false,
      "has_encryption": false,
      "has_integrity_check": true,
      "integrity_method": "CRC-16",
      "known_weaknesses": [
        "No authentication - any device can issue commands",
        "No encryption - commands transmitted in plaintext",
        "No authorization - no role-based access control",
        "Susceptible to replay attacks",
        "Vulnerable to man-in-the-middle attacks"
      ],
      "secure_variant": {
        "name": "Modbus/TCP Security (TLS)",
        "standard": "Modbus Organization specification",
        "adoption_rate": 12.3
      }
    },
    "technical_details": {
      "addressing": "Unit ID (1-247)",
      "max_data_size": "252 bytes per message",
      "function_codes": 127,
      "common_functions": [
        {"code": 1, "name": "Read Coils"},
        {"code": 2, "name": "Read Discrete Inputs"},
        {"code": 3, "name": "Read Holding Registers"},
        {"code": 4, "name": "Read Input Registers"},
        {"code": 5, "name": "Write Single Coil"},
        {"code": 6, "name": "Write Single Register"},
        {"code": 15, "name": "Write Multiple Coils"},
        {"code": 16, "name": "Write Multiple Registers"}
      ]
    },
    "statistics": {
      "equipment_count": 2341,
      "vulnerability_count": 47,
      "sectors_using": ["Energy", "Water", "Manufacturing", "Chemical"],
      "risk_score": 8.2
    }
  }
}
```

---

## Protocol Vulnerabilities Endpoint

### Endpoint Definition

```
GET /api/v1/protocols/{protocolId}/vulnerabilities
```

### Purpose

Get all CVEs and vulnerabilities associated with a specific protocol.

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_cvss` | number | 0 | Minimum CVSS score |
| `exploited` | boolean | all | Filter by active exploitation |
| `limit` | number | 50 | Maximum results |

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:40:00Z",
  "protocol_id": "modbus",
  "protocol_name": "Modbus TCP/RTU",
  "vulnerability_count": 47,
  "vulnerabilities": [
    {
      "cve_id": "CVE-2022-30540",
      "title": "Modbus Server Remote Code Execution",
      "description": "Buffer overflow in Modbus TCP server implementation allows remote code execution",
      "severity": "critical",
      "cvss_score": 9.8,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "epss_score": 0.87,
      "exploit_available": true,
      "exploit_maturity": "functional",
      "affected_products": [
        "Schneider Electric Modicon M340",
        "Schneider Electric Modicon M580"
      ],
      "remediation": {
        "patch_available": true,
        "recommended_version": "Firmware v3.20",
        "workaround": "Network isolation, firewall rules"
      },
      "attack_vectors": [
        "T0855 - Unauthorized Command Message",
        "T0866 - Exploitation of Remote Services"
      ]
    },
    {
      "cve_id": "CVE-2021-22765",
      "title": "Modbus Function Code Injection",
      "description": "Improper input validation allows injection of malicious function codes",
      "severity": "high",
      "cvss_score": 8.6,
      "epss_score": 0.65,
      "exploit_available": true,
      "affected_products": [
        "Multiple Modbus implementations"
      ]
    }
  ],
  "vulnerability_summary": {
    "by_severity": {
      "critical": 5,
      "high": 18,
      "medium": 19,
      "low": 5
    },
    "by_exploit_status": {
      "actively_exploited": 3,
      "poc_available": 12,
      "theoretical": 32
    },
    "average_cvss": 7.2
  }
}
```

---

## Protocol Equipment Endpoint

### Endpoint Definition

```
GET /api/v1/protocols/{protocolId}/equipment
```

### Purpose

List all equipment that uses a specific protocol.

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sector` | string | all | Filter by sector |
| `criticality` | string | all | Filter: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `has_vulnerabilities` | boolean | all | Filter by vulnerable status |

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:45:00Z",
  "protocol_id": "modbus",
  "protocol_name": "Modbus TCP/RTU",
  "equipment_count": 2341,
  "equipment": [
    {
      "equipment_id": "PLC-MODICON-001",
      "name": "Modicon M340 PLC",
      "manufacturer": "Schneider Electric",
      "model": "BMXP342020",
      "sector": "Energy",
      "criticality": "HIGH",
      "protocol_variant": "Modbus TCP",
      "port": 502,
      "firmware_version": "V3.10",
      "vulnerability_count": 3,
      "highest_cvss": 9.8,
      "hardening_status": "PARTIAL",
      "secure_variant_enabled": false
    },
    {
      "equipment_id": "RTU-FIELD-042",
      "name": "Field RTU",
      "manufacturer": "ABB",
      "model": "RTU560",
      "sector": "Water",
      "criticality": "MEDIUM",
      "protocol_variant": "Modbus RTU",
      "vulnerability_count": 2,
      "highest_cvss": 7.5,
      "hardening_status": "NONE"
    }
  ],
  "sector_distribution": {
    "Energy": 892,
    "Water": 567,
    "Manufacturing": 456,
    "Chemical": 234,
    "Other": 192
  },
  "criticality_distribution": {
    "CRITICAL": 234,
    "HIGH": 678,
    "MEDIUM": 987,
    "LOW": 442
  }
}
```

---

## Protocol Hardening Endpoint

### Endpoint Definition

```
GET /api/v1/protocols/{protocolId}/hardening
```

### Purpose

Get security hardening recommendations for a specific protocol.

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:50:00Z",
  "protocol_id": "modbus",
  "protocol_name": "Modbus TCP/RTU",
  "security_level": "LOW",
  "hardening_recommendations": {
    "network_controls": [
      {
        "priority": 1,
        "control": "Network Segmentation",
        "description": "Isolate Modbus networks in dedicated VLAN with firewall controls",
        "implementation": {
          "steps": [
            "Create dedicated VLAN for Modbus devices",
            "Configure firewall rules allowing only authorized IP addresses",
            "Block port 502 from corporate network",
            "Implement ingress/egress filtering"
          ],
          "effort_hours": 16,
          "cost_usd": 5000,
          "risk_reduction": 3.5
        },
        "att_ck_mitigations": ["M1030 - Network Segmentation"]
      },
      {
        "priority": 2,
        "control": "Intrusion Detection",
        "description": "Deploy Modbus-aware IDS to detect anomalous function codes",
        "implementation": {
          "tools": ["Snort with Modbus preprocessor", "Suricata", "Claroty", "Nozomi"],
          "effort_hours": 24,
          "cost_usd": 15000,
          "risk_reduction": 2.0
        }
      }
    ],
    "protocol_controls": [
      {
        "priority": 1,
        "control": "Enable Modbus/TCP Security",
        "description": "Upgrade to Modbus/TCP with TLS encryption",
        "applicability": "Devices supporting secure variant only",
        "implementation": {
          "steps": [
            "Verify device support for Modbus/TCP Security",
            "Generate and deploy TLS certificates",
            "Configure mutual authentication",
            "Update firewall rules for port 802"
          ],
          "effort_hours": 40,
          "cost_usd": 25000,
          "risk_reduction": 4.0
        }
      },
      {
        "priority": 2,
        "control": "Function Code Whitelisting",
        "description": "Configure firewall to allow only required function codes",
        "implementation": {
          "allowed_codes": [1, 2, 3, 4],
          "blocked_codes": [5, 6, 15, 16, 43],
          "rationale": "Block write operations unless required"
        }
      }
    ],
    "monitoring_controls": [
      {
        "priority": 1,
        "control": "Protocol Logging",
        "description": "Log all Modbus transactions to SIEM",
        "data_to_capture": [
          "Source/destination IP",
          "Unit ID",
          "Function code",
          "Register addresses",
          "Timestamp"
        ]
      },
      {
        "priority": 2,
        "control": "Anomaly Detection",
        "description": "Baseline normal Modbus traffic patterns",
        "alert_on": [
          "Unexpected function codes",
          "Unusual traffic volume",
          "New source IP addresses",
          "Off-hours activity"
        ]
      }
    ],
    "replacement_recommendations": {
      "recommended": true,
      "target_protocol": "OPC UA",
      "rationale": "OPC UA provides built-in security (authentication, encryption, authorization)",
      "migration_complexity": "HIGH",
      "estimated_cost_usd": 250000,
      "estimated_time_months": 18
    }
  },
  "compliance_mappings": {
    "IEC62443": {
      "FR1": "Implement device authentication",
      "FR4": "Enable encryption for data confidentiality",
      "FR5": "Segment Modbus networks"
    },
    "NERC_CIP": {
      "CIP-005": "Electronic Security Perimeters",
      "CIP-007": "System Security Management"
    }
  }
}
```

---

## Protocol Risk Assessment Endpoint

### Endpoint Definition

```
POST /api/v1/protocols/risk-assessment
```

### Purpose

Perform multi-protocol risk assessment across the organization.

### Request Body

```json
{
  "protocols": ["modbus", "dnp3", "s7comm"],
  "sectors": ["energy", "water"],
  "include_recommendations": true
}
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:55:00Z",
  "assessment_id": "PROTO-ASSESS-001",
  "overall_risk_score": 7.4,
  "protocol_risks": [
    {
      "protocol_id": "s7comm",
      "risk_score": 8.5,
      "risk_factors": [
        "No authentication",
        "No encryption",
        "High CVE count (41)",
        "Active exploitation observed"
      ],
      "equipment_at_risk": 1567,
      "critical_equipment_count": 234
    },
    {
      "protocol_id": "modbus",
      "risk_score": 8.2,
      "risk_factors": [
        "No authentication",
        "No encryption",
        "Widely deployed (2341 devices)"
      ],
      "equipment_at_risk": 2341,
      "critical_equipment_count": 456
    },
    {
      "protocol_id": "dnp3",
      "risk_score": 6.5,
      "risk_factors": [
        "Optional security features often disabled",
        "Complex configuration"
      ],
      "equipment_at_risk": 892,
      "critical_equipment_count": 123
    }
  ],
  "prioritized_actions": [
    {
      "priority": 1,
      "action": "Migrate S7comm devices to S7comm+",
      "risk_reduction": 2.8,
      "cost_usd": 150000
    },
    {
      "priority": 2,
      "action": "Enable DNP3 Secure Authentication",
      "risk_reduction": 1.5,
      "cost_usd": 25000
    },
    {
      "priority": 3,
      "action": "Segment Modbus networks",
      "risk_reduction": 2.2,
      "cost_usd": 35000
    }
  ]
}
```

---

## Neo4j Cypher Queries

### Protocol Schema

```cypher
CREATE (p:Protocol {
  protocol_id: "modbus",
  name: "Modbus TCP/RTU",
  type: "fieldbus",
  security_level: "LOW",
  has_authentication: false,
  has_encryption: false,
  vulnerability_count: 47,
  risk_score: 8.2
})
```

### Equipment by Protocol

```cypher
MATCH (e:Equipment)-[:USES_PROTOCOL]->(p:Protocol {protocol_id: $protocolId})
RETURN e.device_id AS equipment_id,
       e.name AS name,
       e.manufacturer AS manufacturer,
       e.criticality AS criticality,
       e.sector AS sector
ORDER BY e.criticality DESC
```

### Protocol Vulnerabilities

```cypher
MATCH (p:Protocol {protocol_id: $protocolId})-[:HAS_VULNERABILITY]->(cve:CVE)
RETURN cve.id AS cve_id,
       cve.cvss_score AS cvss,
       cve.description AS description,
       cve.exploit_available AS exploitable
ORDER BY cve.cvss_score DESC
```

### High-Risk Protocol Equipment

```cypher
MATCH (e:Equipment)-[:USES_PROTOCOL]->(p:Protocol)
WHERE p.security_level = 'LOW' AND e.criticality IN ['CRITICAL', 'HIGH']
RETURN e.device_id AS equipment,
       p.protocol_id AS protocol,
       p.vulnerability_count AS vulns,
       e.sector AS sector
ORDER BY p.vulnerability_count DESC
```

---

## Frontend Integration

### TypeScript SDK

```typescript
import { AeonProtocolClient } from '@aeon-dt/protocol-client';

const client = new AeonProtocolClient({
  baseUrl: 'https://api.aeon-dt.local/api/v1',
  apiKey: process.env.AEON_API_KEY
});

// List protocols
const protocols = await client.listProtocols({
  securityLevel: 'LOW'
});

// Get protocol details
const modbus = await client.getProtocol('modbus');

// Get vulnerabilities
const vulns = await client.getProtocolVulnerabilities('modbus', {
  minCvss: 7.0
});

// Get hardening recommendations
const hardening = await client.getHardeningRecommendations('modbus');

// Run risk assessment
const risk = await client.assessRisk({
  protocols: ['modbus', 'dnp3', 's7comm'],
  sectors: ['energy']
});
```

---

## Error Handling

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `PROTOCOL_NOT_FOUND` | 404 | Protocol not in catalog |
| `INVALID_PROTOCOL_TYPE` | 400 | Invalid protocol type filter |
| `ASSESSMENT_TIMEOUT` | 408 | Risk assessment timed out |

---

## Related Documentation

- `API_EQUIPMENT.md` - Equipment details
- `API_SAFETY_COMPLIANCE.md` - IEC 62443 compliance
- `API_VULNERABILITIES.md` - CVE database
- `Enhancement_16_Protocol_Analysis/` - Full enhancement specification

---

**Status:** COMPLETE | **Version:** 1.0.0 | **Last Update:** 2025-11-30
