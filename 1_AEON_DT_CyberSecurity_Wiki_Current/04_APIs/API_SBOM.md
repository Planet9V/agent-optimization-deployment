# AEON Cyber Digital Twin - SBOM Analysis API Documentation

**File:** API_SBOM.md
**Created:** 2025-11-30
**Version:** 1.0.0
**Status:** COMPLETE
**Enhancement:** E3 - SBOM Dependency Analysis
**Document Length:** 800+ lines

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [API Overview](#api-overview)
3. [Authentication & Security](#authentication--security)
4. [SBOM Upload Endpoint](#sbom-upload-endpoint)
5. [Package Details Endpoint](#package-details-endpoint)
6. [Package Vulnerabilities Endpoint](#package-vulnerabilities-endpoint)
7. [Dependency Tree Endpoint](#dependency-tree-endpoint)
8. [SBOM Analysis Endpoint](#sbom-analysis-endpoint)
9. [Supply Chain Risk Endpoint](#supply-chain-risk-endpoint)
10. [Request/Response Schemas](#requestresponse-schemas)
11. [Neo4j Cypher Queries](#neo4j-cypher-queries)
12. [Frontend Integration](#frontend-integration)
13. [Error Handling](#error-handling)

---

## Executive Summary

The **SBOM Analysis API** provides comprehensive Software Bill of Materials ingestion, dependency analysis, and vulnerability correlation for the AEON Cyber Digital Twin. This API enables security teams to:

- **Ingest SBOMs**: Parse CycloneDX, SPDX, and native package manager formats
- **Analyze Dependencies**: Map transitive dependencies with version constraint resolution
- **Correlate CVEs**: Link packages to 316K+ CVE database with EPSS scoring
- **Assess Supply Chain Risk**: Identify abandoned packages, typosquatting, compromises
- **Generate Remediation Plans**: Prioritized upgrade paths with breaking change analysis

**Key Statistics**:
- **Supported Formats**: CycloneDX 1.4/1.5, SPDX 2.3, package.json, requirements.txt, Gemfile.lock
- **Package Ecosystems**: npm, PyPI, Go modules, Maven, NuGet, RubyGems
- **CVE Sources**: NVD (216K), OSV (110K), GHSA (45K)
- **Real-time Scoring**: CVSS 3.1 + EPSS + Exploit Maturity

---

## API Overview

### Base URL
```
https://api.aeon-dt.local/api/v1/sbom
```

### API Endpoints

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/upload` | POST | Upload and parse SBOM file | 2-10 seconds |
| `/packages/{packageId}` | GET | Package metadata and details | 300-500ms |
| `/packages/{packageId}/vulnerabilities` | GET | CVEs affecting package | 500-800ms |
| `/packages/{packageId}/dependencies` | GET | Dependency tree with depth | 1-3 seconds |
| `/analyze` | POST | Full supply chain analysis | 5-30 seconds |
| `/risk/{applicationId}` | GET | Supply chain risk assessment | 2-5 seconds |

### Rate Limiting

```
Rate Limit: 50 requests per minute per API key
Burst Limit: 5 requests per second
Headers:
  X-RateLimit-Limit: 50
  X-RateLimit-Remaining: 42
  X-RateLimit-Reset: 1732472400
```

---

## Authentication & Security

### API Key Authentication

All requests must include an API key:

```bash
curl -H "X-API-Key: your_api_key_here" \
  https://api.aeon-dt.local/api/v1/sbom/packages/npm:react:18.2.0
```

### OAuth 2.0 Bearer Token

```bash
curl -H "Authorization: Bearer your_jwt_token" \
  https://api.aeon-dt.local/api/v1/sbom/analyze
```

### Security Considerations

- **HTTPS Only**: TLS 1.3 encryption required
- **File Size Limit**: SBOM uploads limited to 50MB
- **Malware Scanning**: Uploaded files scanned before processing
- **Audit Logging**: All operations logged with user context

---

## SBOM Upload Endpoint

### Endpoint Definition

```
POST /api/v1/sbom/upload
```

### Purpose

Upload and parse SBOM files in various formats. Returns parsed package list with initial vulnerability scan.

### Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | Yes | `multipart/form-data` or `application/json` |
| `X-API-Key` | Yes | API authentication key |
| `X-SBOM-Format` | No | Override auto-detection: `cyclonedx`, `spdx`, `npm`, `pip` |

### Request Body (multipart/form-data)

```bash
curl -X POST \
  "https://api.aeon-dt.local/api/v1/sbom/upload" \
  -H "X-API-Key: your_api_key_here" \
  -F "sbom=@cyclonedx-sbom.json" \
  -F "application_id=aeon-backend-v1.0.0" \
  -F "scan_vulnerabilities=true"
```

### Request Body (JSON)

```json
{
  "sbom_content": "base64-encoded-sbom-content",
  "format": "cyclonedx",
  "application_id": "aeon-backend-v1.0.0",
  "scan_vulnerabilities": true,
  "resolve_transitive": true
}
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T14:30:00Z",
  "sbom_id": "sbom_2025_11_30_abc123",
  "application_id": "aeon-backend-v1.0.0",
  "format_detected": "cyclonedx-1.5",
  "parsing_summary": {
    "total_packages": 359,
    "direct_dependencies": 47,
    "transitive_dependencies": 312,
    "ecosystems": {
      "npm": 287,
      "native": 72
    }
  },
  "vulnerability_scan": {
    "critical": 2,
    "high": 8,
    "medium": 23,
    "low": 41,
    "total_cves": 74
  },
  "risk_score": 7.2,
  "risk_level": "HIGH",
  "packages": [
    {
      "package_id": "npm:express:4.18.1",
      "name": "express",
      "version": "4.18.1",
      "ecosystem": "npm",
      "is_direct": true,
      "transitive_depth": 0,
      "vulnerability_count": 1,
      "highest_severity": "high"
    }
  ]
}
```

---

## Package Details Endpoint

### Endpoint Definition

```
GET /api/v1/sbom/packages/{packageId}
```

### Purpose

Retrieve detailed metadata for a specific package including maintainer info, release history, and security status.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `packageId` | string | URL-encoded package identifier (e.g., `npm:react:18.2.0`) |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_history` | boolean | false | Include version release history |
| `include_maintainers` | boolean | true | Include maintainer details |
| `include_downloads` | boolean | false | Include download statistics |

### Example Request

```bash
curl -X GET \
  "https://api.aeon-dt.local/api/v1/sbom/packages/npm%3Areact%3A18.2.0?include_history=true" \
  -H "X-API-Key: your_api_key_here"
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T14:35:00Z",
  "package": {
    "package_id": "npm:react:18.2.0",
    "name": "react",
    "version": "18.2.0",
    "ecosystem": "npm",
    "license": "MIT",
    "homepage": "https://react.dev",
    "repository": "https://github.com/facebook/react",
    "description": "React is a JavaScript library for building user interfaces.",
    "published_date": "2022-06-14T00:00:00Z",
    "metadata": {
      "maintainers": [
        {
          "username": "facebook/react-team",
          "verified": true,
          "packages_count": 47
        }
      ],
      "downloads": {
        "weekly": 18500000,
        "monthly": 75000000
      }
    },
    "security_status": {
      "deprecated": false,
      "has_advisories": false,
      "cve_count": 0,
      "last_security_review": "2025-11-25T00:00:00Z"
    },
    "supply_chain_signals": {
      "typosquatting_risk": "low",
      "maintenance_status": "active",
      "last_release_days_ago": 45,
      "commit_frequency": "weekly"
    }
  }
}
```

---

## Package Vulnerabilities Endpoint

### Endpoint Definition

```
GET /api/v1/sbom/packages/{packageId}/vulnerabilities
```

### Purpose

Retrieve all CVEs affecting a specific package version with severity scores and remediation paths.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `packageId` | string | URL-encoded package identifier |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_cvss` | number | 0 | Minimum CVSS score filter |
| `include_remediation` | boolean | true | Include fix recommendations |
| `include_epss` | boolean | true | Include EPSS exploit probability |

### Example Request

```bash
curl -X GET \
  "https://api.aeon-dt.local/api/v1/sbom/packages/npm%3Aaxios%3A0.21.1/vulnerabilities?min_cvss=5.0" \
  -H "X-API-Key: your_api_key_here"
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T14:40:00Z",
  "package_id": "npm:axios:0.21.1",
  "vulnerability_count": 2,
  "vulnerabilities": [
    {
      "cve_id": "CVE-2021-43565",
      "title": "Axios SSRF via Redirect",
      "description": "Axios version 0.21.1 allows SSRF attacks via URL redirect handling",
      "severity": "high",
      "cvss_score": 7.5,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
      "epss_score": 0.89,
      "epss_percentile": 89,
      "exploit_maturity": "functional",
      "discovered_date": "2021-10-15",
      "public_date": "2021-10-20",
      "sources": ["NVD", "GHSA", "OSV"],
      "remediation": {
        "recommended_version": "0.26.1",
        "path_available": true,
        "breaking_changes": false,
        "upgrade_effort_hours": 0.5
      },
      "intelligence_links": {
        "stix_indicators": ["attack-pattern--3731bda3-55e8-4a4e-8e38-bf01a35303ba"],
        "threat_actors": [],
        "campaigns": []
      }
    }
  ],
  "remediation_summary": {
    "fixable_count": 2,
    "no_fix_count": 0,
    "total_upgrade_effort_hours": 1.0
  }
}
```

---

## Dependency Tree Endpoint

### Endpoint Definition

```
GET /api/v1/sbom/packages/{packageId}/dependencies
```

### Purpose

Retrieve the complete dependency tree for a package with transitive depth tracking.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `packageId` | string | URL-encoded package identifier |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_depth` | number | 5 | Maximum transitive depth to traverse |
| `include_vulnerabilities` | boolean | false | Include CVE counts per dependency |
| `format` | string | tree | Output format: `tree`, `flat`, `graph` |

### Example Request

```bash
curl -X GET \
  "https://api.aeon-dt.local/api/v1/sbom/packages/npm%3Aexpress%3A4.18.1/dependencies?max_depth=3&include_vulnerabilities=true" \
  -H "X-API-Key: your_api_key_here"
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T14:45:00Z",
  "package_id": "npm:express:4.18.1",
  "total_dependencies": 56,
  "max_depth_reached": 3,
  "dependency_tree": {
    "name": "express",
    "version": "4.18.1",
    "vulnerability_count": 0,
    "children": [
      {
        "name": "body-parser",
        "version": "1.20.0",
        "depth": 1,
        "vulnerability_count": 1,
        "highest_severity": "high",
        "children": [
          {
            "name": "bytes",
            "version": "3.1.2",
            "depth": 2,
            "vulnerability_count": 0,
            "children": []
          }
        ]
      }
    ]
  },
  "vulnerability_summary": {
    "total_vulnerable_packages": 3,
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 0
  }
}
```

---

## SBOM Analysis Endpoint

### Endpoint Definition

```
POST /api/v1/sbom/analyze
```

### Purpose

Perform comprehensive supply chain analysis including vulnerability correlation, risk scoring, and remediation planning.

### Request Body

```json
{
  "sbom_id": "sbom_2025_11_30_abc123",
  "analysis_options": {
    "vulnerability_scan": true,
    "license_analysis": true,
    "supply_chain_risk": true,
    "threat_intelligence": true,
    "remediation_planning": true
  },
  "prioritization": {
    "method": "risk_score",
    "include_epss": true,
    "include_exploit_maturity": true
  }
}
```

### Example Request

```bash
curl -X POST \
  "https://api.aeon-dt.local/api/v1/sbom/analyze" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "sbom_id": "sbom_2025_11_30_abc123",
    "analysis_options": {
      "vulnerability_scan": true,
      "supply_chain_risk": true,
      "remediation_planning": true
    }
  }'
```

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T14:50:00Z",
  "analysis_id": "analysis_2025_11_30_xyz789",
  "sbom_id": "sbom_2025_11_30_abc123",
  "application_id": "aeon-backend-v1.0.0",
  "summary": {
    "total_packages": 359,
    "direct_dependencies": 47,
    "transitive_dependencies": 312,
    "total_vulnerabilities": 74,
    "risk_score": 7.2,
    "risk_level": "HIGH"
  },
  "vulnerability_analysis": {
    "by_severity": {
      "critical": 2,
      "high": 8,
      "medium": 23,
      "low": 41
    },
    "by_exploitability": {
      "actively_exploited": 3,
      "poc_available": 12,
      "theoretical": 59
    },
    "top_vulnerabilities": [
      {
        "cve_id": "CVE-2021-23337",
        "package": "lodash:4.17.20",
        "severity": "critical",
        "cvss_score": 9.8,
        "epss_score": 0.94,
        "remediation": "Upgrade to 4.17.21"
      }
    ]
  },
  "supply_chain_risk": {
    "abandoned_packages": 3,
    "typosquatting_risk": "low",
    "compromised_packages": 0,
    "unmaintained_packages": 7,
    "license_issues": 0
  },
  "remediation_plan": {
    "total_actions": 12,
    "estimated_hours": 18,
    "phases": [
      {
        "phase": 1,
        "name": "Critical Patches",
        "actions": 2,
        "estimated_hours": 4,
        "vulnerabilities_fixed": 2,
        "packages": [
          {
            "package": "lodash",
            "current": "4.17.20",
            "target": "4.17.21",
            "breaking_changes": false
          }
        ]
      },
      {
        "phase": 2,
        "name": "High Severity",
        "actions": 8,
        "estimated_hours": 12,
        "vulnerabilities_fixed": 8
      }
    ]
  },
  "threat_intelligence": {
    "apt_campaigns_targeting": 2,
    "threat_actors": ["APT29", "FIN7"],
    "stix_indicators": 15
  }
}
```

---

## Supply Chain Risk Endpoint

### Endpoint Definition

```
GET /api/v1/sbom/risk/{applicationId}
```

### Purpose

Get aggregate supply chain risk assessment for an application.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `applicationId` | string | Application identifier |

### Response Format

```json
{
  "success": true,
  "timestamp": "2025-11-30T15:00:00Z",
  "application_id": "aeon-backend-v1.0.0",
  "risk_assessment": {
    "overall_score": 7.2,
    "risk_level": "HIGH",
    "factors": {
      "vulnerability_exposure": 8.5,
      "supply_chain_health": 6.2,
      "maintenance_status": 7.8,
      "threat_landscape": 6.5
    }
  },
  "key_risks": [
    {
      "type": "CRITICAL_CVE",
      "description": "2 critical CVEs with active exploitation",
      "impact": "HIGH",
      "action_required": true
    },
    {
      "type": "ABANDONED_DEPENDENCY",
      "description": "3 packages with no updates in 2+ years",
      "impact": "MEDIUM",
      "action_required": true
    }
  ],
  "recommendations": [
    {
      "priority": 1,
      "action": "Upgrade lodash to 4.17.21",
      "impact": "Fixes CVE-2021-23337 (critical)",
      "effort": "LOW"
    }
  ]
}
```

---

## Neo4j Cypher Queries

### Package Node Schema

```cypher
// Package Node Structure
CREATE (pkg:Package:SBOM {
  package_id: "npm:express:4.18.1",
  name: "express",
  ecosystem: "npm",
  version: "4.18.1",
  license: "MIT",
  repository: "https://github.com/expressjs/express",
  first_seen: datetime("2025-11-30T00:00:00Z"),
  deprecated: false,
  maintenance_status: "active"
})
```

### Get Package Vulnerabilities

```cypher
// Get all CVEs affecting a package
MATCH (pkg:Package {package_id: $packageId})
MATCH (pkg)-[:HAS_VULNERABILITY]->(cve:CVE)
RETURN cve.id AS cve_id,
       cve.cvss_score AS cvss,
       cve.epss_score AS epss,
       cve.description AS description,
       cve.severity AS severity
ORDER BY cve.cvss_score DESC
```

### Get Dependency Tree

```cypher
// Get transitive dependencies to depth N
MATCH path = (root:Package {package_id: $packageId})
              -[:DEPENDS_ON*1..5]->(dep:Package)
RETURN root.name AS root,
       [n IN nodes(path) | n.name] AS dependency_chain,
       length(path) AS depth
ORDER BY depth ASC
```

### Supply Chain Risk Analysis

```cypher
// Identify abandoned packages in dependency tree
MATCH (app:Application {id: $appId})-[:USES_SBOM]->(sbom:SBOM)
MATCH (sbom)-[:CONTAINS]->(pkg:Package)
WHERE pkg.last_release < datetime() - duration('P730D')
RETURN pkg.name AS package,
       pkg.version AS version,
       pkg.last_release AS last_update,
       duration.between(pkg.last_release, datetime()).days AS days_since_update
ORDER BY days_since_update DESC
```

### CVE Correlation with EPSS

```cypher
// Get high-risk CVEs with EPSS > 0.5
MATCH (pkg:Package)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.epss_score > 0.5
RETURN pkg.package_id AS package,
       cve.id AS cve_id,
       cve.cvss_score AS cvss,
       cve.epss_score AS epss,
       CASE
         WHEN cve.epss_score > 0.9 THEN 'CRITICAL'
         WHEN cve.epss_score > 0.7 THEN 'HIGH'
         WHEN cve.epss_score > 0.5 THEN 'MEDIUM'
         ELSE 'LOW'
       END AS risk_category
ORDER BY cve.epss_score DESC
```

---

## Frontend Integration

### JavaScript/TypeScript SDK

```typescript
import { AeonSBOMClient } from '@aeon-dt/sbom-client';

const client = new AeonSBOMClient({
  baseUrl: 'https://api.aeon-dt.local/api/v1',
  apiKey: process.env.AEON_API_KEY
});

// Upload SBOM
const uploadResult = await client.upload({
  file: sbomFile,
  applicationId: 'my-app-v1.0.0',
  scanVulnerabilities: true
});

// Get package vulnerabilities
const vulns = await client.getPackageVulnerabilities(
  'npm:express:4.18.1',
  { minCvss: 5.0, includeRemediation: true }
);

// Run full analysis
const analysis = await client.analyze({
  sbomId: uploadResult.sbom_id,
  analysisOptions: {
    vulnerabilityScan: true,
    supplyChainRisk: true,
    remediationPlanning: true
  }
});
```

### React Integration Example

```tsx
import { useSBOMAnalysis } from '@aeon-dt/react-hooks';

function SBOMDashboard({ applicationId }: { applicationId: string }) {
  const { data, isLoading, error } = useSBOMAnalysis(applicationId);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorDisplay error={error} />;

  return (
    <div className="sbom-dashboard">
      <RiskScoreCard score={data.risk_score} level={data.risk_level} />
      <VulnerabilitySummary vulnerabilities={data.vulnerability_analysis} />
      <RemediationPlan plan={data.remediation_plan} />
      <SupplyChainHealth risks={data.supply_chain_risk} />
    </div>
  );
}
```

---

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "SBOM_PARSE_ERROR",
    "message": "Failed to parse SBOM: Invalid CycloneDX format",
    "details": {
      "line": 45,
      "expected": "component",
      "found": "unknown_element"
    }
  },
  "timestamp": "2025-11-30T15:10:00Z"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `SBOM_PARSE_ERROR` | 400 | Invalid SBOM format or structure |
| `PACKAGE_NOT_FOUND` | 404 | Package not in database |
| `ANALYSIS_TIMEOUT` | 408 | Analysis exceeded time limit |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `ECOSYSTEM_NOT_SUPPORTED` | 400 | Package ecosystem not supported |
| `FILE_TOO_LARGE` | 413 | SBOM file exceeds 50MB limit |

---

## Related Documentation

- `API_VULNERABILITIES.md` - CVE database and prioritization
- `API_STIX.md` - Threat intelligence correlation
- `02_Databases/Neo4j-Graph-Database.md` - Graph database access
- `Enhancement_03_SBOM_Analysis/README.md` - Full enhancement specification

---

**Status:** COMPLETE | **Version:** 1.0.0 | **Last Update:** 2025-11-30
