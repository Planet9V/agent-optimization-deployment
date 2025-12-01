# AEON Cyber Digital Twin - Attack Path Modeling API Documentation

**File:** API_ATTACK_PATHS.md
**Created:** 2025-11-30
**Version:** 1.0.0
**Status:** COMPLETE
**Enhancement:** E13 - Attack Path Enumeration & Modeling
**Document Length:** 750+ lines

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [API Overview](#api-overview)
3. [Path Enumeration Endpoint](#path-enumeration-endpoint)
4. [Shortest Path Endpoint](#shortest-path-endpoint)
5. [Path Probability Endpoint](#path-probability-endpoint)
6. [Path Mitigations Endpoint](#path-mitigations-endpoint)
7. [Attack Surface Endpoint](#attack-surface-endpoint)
8. [Sector Attack Paths Endpoint](#sector-attack-paths-endpoint)
9. [Neo4j Cypher Queries](#neo4j-cypher-queries)
10. [Frontend Integration](#frontend-integration)
11. [Error Handling](#error-handling)

---

## Executive Summary

The **Attack Path Modeling API** provides comprehensive multi-hop attack path enumeration and risk assessment for the AEON Cyber Digital Twin. This API enables security teams to:

- **Enumerate Attack Paths**: Discover all possible attack chains up to 20 hops
- **Calculate Probabilities**: Assess likelihood of successful attack traversal
- **Identify Chokepoints**: Find critical mitigation points in attack chains
- **Prioritize Mitigations**: Rank countermeasures by impact on path disruption
- **Visualize Attack Surface**: Map entry points to high-value targets

**Key Capabilities**:
- **20-Hop Maximum Depth**: Comprehensive path enumeration
- **316K+ CVEs**: Vulnerability-based path generation
- **691 ATT&CK Techniques**: Technique-based path modeling
- **Probability Scoring**: Combined CVSS × EPSS × Difficulty factors
- **Real-time Path Analysis**: Sub-second shortest path queries

**McKenney Questions Addressed**:
- **Q5**: How will they get in? (Attack path enumeration)
- **Q6**: What is the impact? (Path consequence analysis)
- **Q8**: What should we patch first? (Mitigation prioritization)

---

## API Overview

### Base URL
```
https://api.aeon-dt.local/api/v1/attack-paths
```

### API Endpoints

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/enumerate` | POST | Enumerate all paths from source to target | 2-30 seconds |
| `/from/{sourceId}/to/{targetId}` | GET | Shortest path between nodes | 500ms-2s |
| `/{pathId}/probability` | GET | Attack success probability | 300-500ms |
| `/{pathId}/mitigations` | GET | Mitigation recommendations | 500ms-1s |
| `/attack-surface/{targetId}` | GET | All entry points to target | 2-10 seconds |
| `/sector/{sectorId}/paths` | GET | Sector-specific attack paths | 5-30 seconds |

### Rate Limiting

```
Rate Limit: 30 requests per minute per API key
Burst Limit: 3 requests per second
Headers:
  X-RateLimit-Limit: 30
  X-RateLimit-Remaining: 27
  X-RateLimit-Reset: 1732472400
```

---

## Path Enumeration Endpoint

### Endpoint Definition

```
POST /api/v1/attack-paths/enumerate
```

### Purpose

Enumerate all possible attack paths from entry point(s) to target(s) with configurable depth and filtering.

### Request Body

```json
{
  "source": {
    "type": "entry_point",
    "ids": ["INTERNET", "ZONE-L4-ENTERPRISE"],
    "any_external": true
  },
  "target": {
    "type": "asset",
    "ids": ["PLC-REACTOR-001", "HMI-CONTROL-001"],
    "criticality_min": "HIGH"
  },
  "options": {
    "max_depth": 10,
    "max_paths": 100,
    "include_probabilities": true,
    "include_techniques": true,
    "filter_by_exploitability": true,
    "min_cvss": 5.0,
    "require_known_exploit": false
  }
}
```

### Example Request

```bash
curl -X POST \
  "https://api.aeon-dt.local/api/v1/attack-paths/enumerate" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {"type": "entry_point", "any_external": true},
    "target": {"type": "asset", "criticality_min": "CRITICAL"},
    "options": {"max_depth": 8, "max_paths": 50}
  }'
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:00:00Z",
  "enumeration_id": "enum_2025_11_30_abc123",
  "query_time_ms": 4523,
  "summary": {
    "total_paths_found": 47,
    "paths_returned": 47,
    "max_depth_reached": 8,
    "unique_entry_points": 5,
    "unique_targets": 3,
    "average_path_length": 5.2,
    "shortest_path_length": 3,
    "longest_path_length": 8
  },
  "attack_paths": [
    {
      "path_id": "path_001",
      "entry_point": "INTERNET",
      "target": "PLC-REACTOR-001",
      "path_length": 5,
      "probability": 0.23,
      "risk_score": 8.7,
      "path_nodes": [
        {
          "step": 1,
          "node_id": "FIREWALL-PERIMETER",
          "node_type": "Network Device",
          "vulnerability": "CVE-2024-12345",
          "cvss": 7.8,
          "technique": "T1190 - Exploit Public-Facing Application"
        },
        {
          "step": 2,
          "node_id": "WEB-SERVER-DMZ",
          "node_type": "Server",
          "vulnerability": "CVE-2024-23456",
          "cvss": 8.2,
          "technique": "T1059 - Command and Scripting Interpreter"
        },
        {
          "step": 3,
          "node_id": "JUMP-HOST-001",
          "node_type": "Workstation",
          "vulnerability": "CVE-2024-34567",
          "cvss": 6.5,
          "technique": "T1021 - Remote Services"
        },
        {
          "step": 4,
          "node_id": "HISTORIAN-001",
          "node_type": "SCADA Server",
          "vulnerability": "CVE-2024-45678",
          "cvss": 7.2,
          "technique": "T1078 - Valid Accounts"
        },
        {
          "step": 5,
          "node_id": "PLC-REACTOR-001",
          "node_type": "PLC",
          "vulnerability": "CVE-2024-56789",
          "cvss": 9.1,
          "technique": "T0831 - Manipulation of Control"
        }
      ],
      "techniques_used": [
        "T1190", "T1059", "T1021", "T1078", "T0831"
      ],
      "cves_exploited": [
        "CVE-2024-12345", "CVE-2024-23456", "CVE-2024-34567",
        "CVE-2024-45678", "CVE-2024-56789"
      ],
      "chokepoints": [
        {
          "node_id": "JUMP-HOST-001",
          "reason": "Single path traversal point",
          "mitigation_impact": "HIGH"
        }
      ]
    }
  ],
  "entry_point_statistics": {
    "INTERNET": {
      "paths_count": 23,
      "avg_path_length": 5.8,
      "highest_risk_path": "path_001"
    },
    "ZONE-L4-ENTERPRISE": {
      "paths_count": 24,
      "avg_path_length": 4.2,
      "highest_risk_path": "path_012"
    }
  },
  "technique_frequency": [
    {"technique": "T1078", "count": 34, "percentage": 72.3},
    {"technique": "T1021", "count": 28, "percentage": 59.6},
    {"technique": "T1059", "count": 21, "percentage": 44.7}
  ]
}
```

---

## Shortest Path Endpoint

### Endpoint Definition

```
GET /api/v1/attack-paths/from/{sourceId}/to/{targetId}
```

### Purpose

Find the shortest attack path between any two nodes in the graph.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sourceId` | string | Source node identifier |
| `targetId` | string | Target node identifier |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_depth` | number | 20 | Maximum path depth |
| `include_alternatives` | boolean | false | Return top 5 alternative paths |
| `weight_by` | string | hops | Weight by: `hops`, `cvss`, `probability` |

### Example Request

```bash
curl -X GET \
  "https://api.aeon-dt.local/api/v1/attack-paths/from/INTERNET/to/PLC-REACTOR-001?include_alternatives=true&weight_by=cvss" \
  -H "X-API-Key: your_api_key_here"
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:05:00Z",
  "source": "INTERNET",
  "target": "PLC-REACTOR-001",
  "shortest_path": {
    "path_id": "shortest_001",
    "path_length": 4,
    "total_cvss": 32.3,
    "probability": 0.31,
    "nodes": [
      {
        "id": "INTERNET",
        "type": "Entry Point",
        "transition": {
          "method": "Exploit Public Application",
          "vulnerability": "CVE-2024-12345",
          "cvss": 7.8,
          "technique": "T1190"
        }
      },
      {
        "id": "VPN-GATEWAY",
        "type": "Network Device",
        "transition": {
          "method": "Credential Theft",
          "vulnerability": "CVE-2024-23456",
          "cvss": 8.5,
          "technique": "T1078"
        }
      },
      {
        "id": "ENGINEERING-WS",
        "type": "Workstation",
        "transition": {
          "method": "Protocol Exploitation",
          "vulnerability": "CVE-2024-34567",
          "cvss": 7.2,
          "technique": "T0886"
        }
      },
      {
        "id": "PLC-REACTOR-001",
        "type": "PLC",
        "transition": null
      }
    ]
  },
  "alternative_paths": [
    {
      "path_id": "alt_001",
      "path_length": 5,
      "total_cvss": 28.7,
      "probability": 0.18,
      "summary": "Via DMZ → Historian → Control Network"
    },
    {
      "path_id": "alt_002",
      "path_length": 6,
      "total_cvss": 35.2,
      "probability": 0.12,
      "summary": "Via Corporate → IT/OT Boundary → SCADA"
    }
  ],
  "path_comparison": {
    "fastest": "shortest_001",
    "highest_probability": "shortest_001",
    "lowest_detection_risk": "alt_002"
  }
}
```

---

## Path Probability Endpoint

### Endpoint Definition

```
GET /api/v1/attack-paths/{pathId}/probability
```

### Purpose

Calculate detailed probability of successful attack traversal along a specific path.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `pathId` | string | Attack path identifier |

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:10:00Z",
  "path_id": "path_001",
  "probability_analysis": {
    "overall_probability": 0.23,
    "confidence_interval": {
      "low": 0.15,
      "high": 0.31
    },
    "step_probabilities": [
      {
        "step": 1,
        "node": "FIREWALL-PERIMETER",
        "individual_probability": 0.78,
        "cumulative_probability": 0.78,
        "factors": {
          "cvss_factor": 0.78,
          "epss_factor": 0.65,
          "exploit_availability": 0.90,
          "patch_status": 0.85,
          "detection_evasion": 0.70
        }
      },
      {
        "step": 2,
        "node": "WEB-SERVER-DMZ",
        "individual_probability": 0.65,
        "cumulative_probability": 0.51,
        "factors": {
          "cvss_factor": 0.82,
          "epss_factor": 0.71,
          "exploit_availability": 0.95,
          "patch_status": 0.60,
          "detection_evasion": 0.55
        }
      },
      {
        "step": 3,
        "node": "JUMP-HOST-001",
        "individual_probability": 0.55,
        "cumulative_probability": 0.28,
        "factors": {
          "cvss_factor": 0.65,
          "epss_factor": 0.45,
          "exploit_availability": 0.80,
          "patch_status": 0.70,
          "detection_evasion": 0.60
        }
      },
      {
        "step": 4,
        "node": "HISTORIAN-001",
        "individual_probability": 0.60,
        "cumulative_probability": 0.17,
        "factors": {
          "cvss_factor": 0.72,
          "epss_factor": 0.58,
          "exploit_availability": 0.85,
          "patch_status": 0.65,
          "detection_evasion": 0.65
        }
      },
      {
        "step": 5,
        "node": "PLC-REACTOR-001",
        "individual_probability": 0.75,
        "cumulative_probability": 0.23,
        "factors": {
          "cvss_factor": 0.91,
          "epss_factor": 0.82,
          "exploit_availability": 0.70,
          "patch_status": 0.90,
          "detection_evasion": 0.80
        }
      }
    ],
    "risk_drivers": [
      {
        "factor": "High EPSS on final target",
        "impact": "HIGH",
        "contribution": 0.25
      },
      {
        "factor": "Unpatched web server",
        "impact": "HIGH",
        "contribution": 0.20
      }
    ],
    "detection_analysis": {
      "average_detection_probability": 0.45,
      "weakest_detection_point": "JUMP-HOST-001",
      "overall_stealth_rating": "MEDIUM"
    }
  }
}
```

---

## Path Mitigations Endpoint

### Endpoint Definition

```
GET /api/v1/attack-paths/{pathId}/mitigations
```

### Purpose

Get prioritized mitigation recommendations for disrupting an attack path.

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:15:00Z",
  "path_id": "path_001",
  "mitigations": {
    "summary": {
      "total_mitigations": 12,
      "critical_mitigations": 3,
      "total_cost_usd": 125000,
      "path_disruption_potential": 0.89
    },
    "prioritized_actions": [
      {
        "priority": 1,
        "mitigation_id": "MIT-001",
        "type": "PATCH",
        "target_node": "WEB-SERVER-DMZ",
        "target_vulnerability": "CVE-2024-23456",
        "description": "Apply security patch for web server RCE vulnerability",
        "effectiveness": {
          "probability_reduction": 0.35,
          "paths_disrupted": 23,
          "path_disruption_percentage": 48.9
        },
        "implementation": {
          "cost_usd": 500,
          "effort_hours": 4,
          "downtime_required": true,
          "downtime_hours": 2,
          "risk_level": "LOW"
        },
        "att_ck_mitigations": ["M1051 - Update Software"]
      },
      {
        "priority": 2,
        "mitigation_id": "MIT-002",
        "type": "NETWORK_SEGMENTATION",
        "target_node": "JUMP-HOST-001",
        "description": "Implement micro-segmentation to isolate jump host",
        "effectiveness": {
          "probability_reduction": 0.28,
          "paths_disrupted": 34,
          "path_disruption_percentage": 72.3
        },
        "implementation": {
          "cost_usd": 15000,
          "effort_hours": 40,
          "downtime_required": false,
          "risk_level": "MEDIUM"
        },
        "att_ck_mitigations": ["M1030 - Network Segmentation"]
      },
      {
        "priority": 3,
        "mitigation_id": "MIT-003",
        "type": "ACCESS_CONTROL",
        "target_node": "HISTORIAN-001",
        "description": "Implement MFA and privileged access management",
        "effectiveness": {
          "probability_reduction": 0.22,
          "paths_disrupted": 28,
          "path_disruption_percentage": 59.6
        },
        "implementation": {
          "cost_usd": 25000,
          "effort_hours": 80,
          "downtime_required": false,
          "risk_level": "LOW"
        },
        "att_ck_mitigations": ["M1032 - Multi-factor Authentication"]
      }
    ],
    "chokepoint_analysis": [
      {
        "node_id": "JUMP-HOST-001",
        "chokepoint_score": 0.85,
        "paths_through": 34,
        "recommended_controls": [
          "Network isolation",
          "Enhanced logging",
          "Behavior monitoring"
        ]
      }
    ],
    "cost_benefit_analysis": {
      "total_investment_usd": 125000,
      "risk_reduction_percentage": 78.5,
      "roi_ratio": 3.2,
      "payback_period_months": 8
    }
  }
}
```

---

## Attack Surface Endpoint

### Endpoint Definition

```
GET /api/v1/attack-paths/attack-surface/{targetId}
```

### Purpose

Map all entry points that can reach a high-value target asset.

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:20:00Z",
  "target_id": "PLC-REACTOR-001",
  "target_name": "Chemical Reactor PLC",
  "attack_surface": {
    "total_entry_points": 12,
    "total_paths": 47,
    "average_path_depth": 5.2,
    "entry_points": [
      {
        "entry_point_id": "INTERNET",
        "entry_type": "External Network",
        "paths_count": 15,
        "shortest_path_length": 4,
        "highest_probability": 0.31,
        "risk_level": "CRITICAL"
      },
      {
        "entry_point_id": "VPN-GATEWAY",
        "entry_type": "Remote Access",
        "paths_count": 12,
        "shortest_path_length": 3,
        "highest_probability": 0.42,
        "risk_level": "CRITICAL"
      },
      {
        "entry_point_id": "CORPORATE-WIFI",
        "entry_type": "Wireless",
        "paths_count": 8,
        "shortest_path_length": 5,
        "highest_probability": 0.18,
        "risk_level": "HIGH"
      },
      {
        "entry_point_id": "USB-WORKSTATION",
        "entry_type": "Physical Access",
        "paths_count": 6,
        "shortest_path_length": 2,
        "highest_probability": 0.55,
        "risk_level": "HIGH"
      },
      {
        "entry_point_id": "SUPPLIER-NETWORK",
        "entry_type": "Third Party",
        "paths_count": 4,
        "shortest_path_length": 6,
        "highest_probability": 0.12,
        "risk_level": "MEDIUM"
      }
    ],
    "surface_reduction_recommendations": [
      {
        "action": "Disable unused VPN accounts",
        "surface_reduction": 25.5,
        "effort": "LOW"
      },
      {
        "action": "Implement USB device control",
        "surface_reduction": 12.8,
        "effort": "MEDIUM"
      }
    ]
  }
}
```

---

## Sector Attack Paths Endpoint

### Endpoint Definition

```
GET /api/v1/attack-paths/sector/{sectorId}/paths
```

### Purpose

Get comprehensive attack path analysis for an entire sector.

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T16:25:00Z",
  "sector_id": "energy",
  "sector_name": "Energy Sector",
  "sector_analysis": {
    "total_critical_assets": 234,
    "total_paths_to_critical": 1247,
    "average_path_length": 5.8,
    "most_exposed_assets": [
      {
        "asset_id": "SUBSTATION-001",
        "asset_name": "Regional Substation Control",
        "paths_count": 89,
        "highest_risk_score": 9.2
      }
    ],
    "common_attack_vectors": [
      {
        "vector": "Spearphishing → Lateral Movement → OT Access",
        "frequency": 34,
        "average_probability": 0.28
      },
      {
        "vector": "VPN Compromise → Engineering WS → PLC",
        "frequency": 28,
        "average_probability": 0.35
      }
    ],
    "sector_risk_score": 7.8,
    "critical_chokepoints": [
      {
        "node_id": "IT-OT-GATEWAY",
        "paths_through": 456,
        "mitigation_priority": "CRITICAL"
      }
    ]
  }
}
```

---

## Neo4j Cypher Queries

### Attack Path Enumeration

```cypher
// Enumerate attack paths up to 20 hops
MATCH path = (source:EntryPoint)-[:CAN_EXPLOIT|CONNECTS_TO|PIVOTS_TO*1..20]->(target:Asset)
WHERE target.criticality = 'CRITICAL'
  AND source.type = 'EXTERNAL'
WITH path,
     [n IN nodes(path) | n.id] AS node_ids,
     [r IN relationships(path) | r.vulnerability] AS vulns,
     reduce(prob = 1.0, r IN relationships(path) | prob * r.success_probability) AS path_probability
RETURN node_ids AS path_nodes,
       length(path) AS path_length,
       vulns AS vulnerabilities_exploited,
       path_probability
ORDER BY path_probability DESC
LIMIT 100
```

### Shortest Path Query

```cypher
// Find shortest attack path
MATCH (source {id: $sourceId}), (target {id: $targetId})
MATCH path = shortestPath((source)-[:CAN_EXPLOIT|CONNECTS_TO|PIVOTS_TO*1..20]->(target))
WITH path,
     [n IN nodes(path) | {id: n.id, type: labels(n)[0]}] AS path_nodes,
     [r IN relationships(path) | {
       vulnerability: r.vulnerability,
       cvss: r.cvss_score,
       technique: r.att_ck_technique
     }] AS transitions
RETURN path_nodes, transitions, length(path) AS hops
```

### Chokepoint Detection

```cypher
// Find nodes that appear in most attack paths
MATCH path = (source:EntryPoint)-[:CAN_EXPLOIT*1..10]->(target:Asset {criticality: 'CRITICAL'})
WITH nodes(path) AS path_nodes
UNWIND path_nodes AS node
WITH node, count(*) AS path_count
WHERE path_count > 5
RETURN node.id AS chokepoint,
       labels(node)[0] AS type,
       path_count AS paths_through
ORDER BY path_count DESC
LIMIT 10
```

### Path Probability Calculation

```cypher
// Calculate cumulative attack probability
MATCH path = (source {id: $sourceId})-[rels:CAN_EXPLOIT*1..20]->(target {id: $targetId})
WITH path,
     reduce(prob = 1.0, r IN rels |
       prob * (r.cvss_score/10) * coalesce(r.epss_score, 0.5) *
       CASE WHEN r.exploit_available THEN 0.9 ELSE 0.5 END
     ) AS success_probability
RETURN [n IN nodes(path) | n.id] AS path,
       success_probability
ORDER BY success_probability DESC
```

---

## Frontend Integration

### TypeScript SDK

```typescript
import { AeonAttackPathClient } from '@aeon-dt/attack-path-client';

const client = new AeonAttackPathClient({
  baseUrl: 'https://api.aeon-dt.local/api/v1',
  apiKey: process.env.AEON_API_KEY
});

// Enumerate attack paths
const paths = await client.enumeratePaths({
  source: { type: 'entry_point', anyExternal: true },
  target: { type: 'asset', criticalityMin: 'CRITICAL' },
  options: { maxDepth: 10, maxPaths: 50 }
});

// Get shortest path
const shortest = await client.getShortestPath(
  'INTERNET',
  'PLC-REACTOR-001',
  { includeAlternatives: true }
);

// Get mitigations
const mitigations = await client.getPathMitigations('path_001');

// Get attack surface
const surface = await client.getAttackSurface('PLC-REACTOR-001');
```

### React Visualization

```tsx
import { useAttackPaths, AttackPathGraph } from '@aeon-dt/react-attack-paths';

function AttackPathViewer({ targetId }: { targetId: string }) {
  const { paths, isLoading } = useAttackPaths({
    target: targetId,
    maxDepth: 8
  });

  return (
    <div className="attack-path-viewer">
      <AttackPathGraph
        paths={paths}
        highlightChokepoints={true}
        onNodeClick={(node) => showNodeDetails(node)}
        onPathClick={(path) => showMitigations(path)}
      />
      <PathStatistics paths={paths} />
      <MitigationPanel paths={paths} />
    </div>
  );
}
```

---

## Error Handling

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `NODE_NOT_FOUND` | 404 | Source or target node not found |
| `PATH_NOT_FOUND` | 404 | No path exists between nodes |
| `PATH_ID_INVALID` | 400 | Invalid path identifier |
| `DEPTH_EXCEEDED` | 400 | Requested depth exceeds maximum (20) |
| `ENUMERATION_TIMEOUT` | 408 | Path enumeration timed out |
| `TOO_MANY_PATHS` | 413 | Result set too large |

---

## Related Documentation

- `API_VULNERABILITIES.md` - CVE database for path generation
- `API_EQUIPMENT.md` - Asset details
- `API_STIX.md` - ATT&CK technique mapping
- `02_Databases/Neo4j-Graph-Database.md` - Graph traversal
- `Enhancement_13_Attack_Paths/` - Full enhancement specification

---

**Status:** COMPLETE | **Version:** 1.0.0 | **Last Update:** 2025-11-30
