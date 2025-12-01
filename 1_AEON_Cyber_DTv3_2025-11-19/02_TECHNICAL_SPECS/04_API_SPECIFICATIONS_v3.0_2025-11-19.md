# API Specifications - AEON Cyber DT v3.0

**File**: 04_API_SPECIFICATIONS_v3.0_2025-11-19.md
**Created**: 2025-11-19 11:47:00 UTC
**Modified**: 2025-11-19 11:47:00 UTC
**Version**: v3.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete API specifications for REST, GraphQL, and WebSocket interfaces
**Status**: ACTIVE

## Document Overview

This document provides comprehensive API specifications for the AEON Cyber Digital Twin v3.0, including REST API, GraphQL API, and WebSocket real-time interfaces.

---

## Architecture Overview

### API Stack
- **REST API**: Resource-oriented operations, bulk operations
- **GraphQL API**: Flexible querying, graph traversal, complex analytics
- **WebSocket API**: Real-time updates, streaming analytics, alert notifications

### Technology Stack
- **Framework**: Node.js with Express/Fastify
- **GraphQL**: Apollo Server
- **WebSocket**: Socket.IO / native WebSocket
- **Authentication**: JWT with OAuth 2.0
- **Rate Limiting**: Redis-backed token bucket
- **API Gateway**: Kong / AWS API Gateway

---

## REST API Specification

### Base URL
```
Production: https://api.aeon-cyber.com/v3
Staging: https://api-staging.aeon-cyber.com/v3
Development: http://localhost:3000/api/v3
```

### Authentication

#### JWT Authentication
```http
POST /auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "SecurePassword123!",
  "mfaCode": "123456"
}

Response 200 OK:
{
  "accessToken": "eyJhbGciOiJSUzI1NiIs...",
  "refreshToken": "eyJhbGciOiJSUzI1NiIs...",
  "expiresIn": 3600,
  "tokenType": "Bearer",
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "roles": ["analyst", "viewer"]
  }
}
```

#### Token Refresh
```http
POST /auth/refresh
Content-Type: application/json
Authorization: Bearer {refreshToken}

Response 200 OK:
{
  "accessToken": "eyJhbGciOiJSUzI1NiIs...",
  "expiresIn": 3600
}
```

### Request Headers (All Endpoints)
```http
Authorization: Bearer {accessToken}
Content-Type: application/json
X-Request-ID: {uuid}
X-API-Version: v3
```

---

## CVE API Endpoints

### Get CVE by ID
```http
GET /cves/{cveId}

Parameters:
  cveId: string (required) - CVE identifier (e.g., CVE-2024-1234)

Response 200 OK:
{
  "data": {
    "id": "cve-uuid",
    "cveId": "CVE-2024-1234",
    "description": "Buffer overflow vulnerability...",
    "publishedDate": "2024-01-15T10:00:00Z",
    "lastModifiedDate": "2024-01-16T14:30:00Z",
    "cvssV3Score": 9.8,
    "cvssV3Vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    "baseSeverity": "CRITICAL",
    "attackVector": "NETWORK",
    "attackComplexity": "LOW",
    "privilegesRequired": "NONE",
    "userInteraction": "NONE",
    "scope": "UNCHANGED",
    "confidentialityImpact": "HIGH",
    "integrityImpact": "HIGH",
    "availabilityImpact": "HIGH",
    "references": [
      "https://nvd.nist.gov/vuln/detail/CVE-2024-1234",
      "https://vendor.com/security/advisories/2024-1234"
    ],
    "cweIds": ["CWE-120", "CWE-787"],
    "affectedSoftware": [
      {
        "vendor": "ExampleCorp",
        "product": "WebServer",
        "versionStartIncluding": "2.0.0",
        "versionEndExcluding": "2.5.1"
      }
    ]
  },
  "meta": {
    "requestId": "req-uuid",
    "timestamp": "2024-01-20T12:00:00Z"
  }
}
```

### Search CVEs
```http
GET /cves?severity={severity}&publishedAfter={date}&limit={limit}&offset={offset}

Query Parameters:
  severity: string (optional) - Filter by severity (LOW, MEDIUM, HIGH, CRITICAL)
  publishedAfter: date (optional) - ISO 8601 date (e.g., 2024-01-01)
  publishedBefore: date (optional) - ISO 8601 date
  cvssMinScore: float (optional) - Minimum CVSS score (0.0-10.0)
  cvssMaxScore: float (optional) - Maximum CVSS score
  hasExploit: boolean (optional) - Filter CVEs with known exploits
  keyword: string (optional) - Full-text search in description
  limit: integer (optional, default: 100, max: 1000)
  offset: integer (optional, default: 0)
  sortBy: string (optional, default: publishedDate) - Field to sort by
  sortOrder: string (optional, default: desc) - asc or desc

Response 200 OK:
{
  "data": [
    { /* CVE object */ },
    { /* CVE object */ }
  ],
  "meta": {
    "total": 1523,
    "limit": 100,
    "offset": 0,
    "requestId": "req-uuid",
    "timestamp": "2024-01-20T12:00:00Z"
  },
  "links": {
    "self": "/cves?severity=CRITICAL&limit=100&offset=0",
    "next": "/cves?severity=CRITICAL&limit=100&offset=100",
    "prev": null
  }
}
```

### Get CVE Relationships
```http
GET /cves/{cveId}/relationships

Query Parameters:
  relationshipType: string (optional) - Filter by type (exploits, demonstrates, affects)
  depth: integer (optional, default: 1, max: 3) - Traversal depth

Response 200 OK:
{
  "data": {
    "cveId": "CVE-2024-1234",
    "relationships": {
      "exploits": [
        {
          "cweId": "CWE-120",
          "cweName": "Buffer Copy without Checking Size of Input",
          "exploitabilityScore": 0.95
        }
      ],
      "demonstrates": [
        {
          "capecId": "CAPEC-100",
          "capecName": "Overflow Buffers",
          "applicabilityScore": 0.88,
          "likelihood": "HIGH"
        }
      ],
      "affects": [
        {
          "softwareId": "soft-uuid",
          "vendor": "ExampleCorp",
          "product": "WebServer",
          "versionRange": "2.0.0 - 2.5.0"
        }
      ]
    }
  },
  "meta": {
    "requestId": "req-uuid",
    "timestamp": "2024-01-20T12:00:00Z"
  }
}
```

---

## Asset API Endpoints

### List Assets
```http
GET /assets?assetType={type}&criticality={level}&status={status}&limit={limit}

Query Parameters:
  assetType: string (optional) - Filter by type (SERVER, WORKSTATION, NETWORK_DEVICE, etc.)
  criticality: string (optional) - Filter by criticality (CRITICAL, HIGH, MEDIUM, LOW)
  status: string (optional) - Filter by status (ACTIVE, INACTIVE, DECOMMISSIONED)
  department: string (optional) - Filter by department name
  location: string (optional) - Filter by location
  riskScoreMin: float (optional) - Minimum risk score
  riskScoreMax: float (optional) - Maximum risk score
  hasVulnerabilities: boolean (optional) - Assets with open vulnerabilities
  limit: integer (optional, default: 100, max: 1000)
  offset: integer (optional, default: 0)

Response 200 OK:
{
  "data": [
    {
      "id": "asset-uuid",
      "assetId": "ASSET-001",
      "name": "Web Server 01",
      "assetType": "SERVER",
      "criticality": "HIGH",
      "status": "ACTIVE",
      "ipAddress": "10.0.1.100",
      "hostname": "web01.example.com",
      "department": "IT Operations",
      "location": "DC-East-01",
      "operatingSystem": "Ubuntu 22.04 LTS",
      "riskScore": 7.2,
      "vulnerabilityCount": 15,
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-20T10:00:00Z"
    }
  ],
  "meta": {
    "total": 542,
    "limit": 100,
    "offset": 0
  }
}
```

### Get Asset Vulnerabilities
```http
GET /assets/{assetId}/vulnerabilities

Query Parameters:
  status: string (optional) - Filter by status (OPEN, MITIGATED, REMEDIATED)
  severity: string (optional) - Filter by severity
  limit: integer (optional, default: 100)
  offset: integer (optional, default: 0)

Response 200 OK:
{
  "data": {
    "assetId": "ASSET-001",
    "assetName": "Web Server 01",
    "vulnerabilities": [
      {
        "cveId": "CVE-2024-1234",
        "severity": "CRITICAL",
        "cvssScore": 9.8,
        "status": "OPEN",
        "detectedDate": "2024-01-15T08:30:00Z",
        "assetRiskScore": 8.5,
        "affectedComponent": "Apache HTTP Server 2.4.49",
        "remediationPlan": "Upgrade to version 2.4.52",
        "targetRemediationDate": "2024-01-30"
      }
    ],
    "summary": {
      "total": 15,
      "critical": 2,
      "high": 5,
      "medium": 6,
      "low": 2,
      "open": 12,
      "mitigated": 2,
      "remediated": 1
    }
  }
}
```

### Get Asset Attack Paths
```http
GET /assets/{assetId}/attack-paths

Query Parameters:
  maxHops: integer (optional, default: 3, max: 5) - Maximum path length
  severityMin: string (optional, default: MEDIUM) - Minimum vulnerability severity
  includeZones: boolean (optional, default: true) - Include network zone information

Response 200 OK:
{
  "data": {
    "assetId": "ASSET-001",
    "attackPaths": [
      {
        "pathId": "path-uuid",
        "riskScore": 9.2,
        "pathLength": 2,
        "zones": ["EXTERNAL", "DMZ", "INTERNAL"],
        "nodes": [
          {
            "assetId": "ASSET-EDGE-01",
            "assetName": "Edge Router",
            "zone": "EXTERNAL",
            "vulnerabilities": ["CVE-2024-5678"]
          },
          {
            "assetId": "ASSET-001",
            "assetName": "Web Server 01",
            "zone": "INTERNAL",
            "vulnerabilities": ["CVE-2024-1234"]
          }
        ],
        "edges": [
          {
            "from": "ASSET-EDGE-01",
            "to": "ASSET-001",
            "connectionType": "NETWORK",
            "protocol": "HTTPS",
            "port": 443
          }
        ]
      }
    ]
  }
}
```

---

## Threat Intelligence API Endpoints

### Get Threat Actors
```http
GET /threat-actors?status={status}&actorType={type}&limit={limit}

Query Parameters:
  status: string (optional) - Filter by status (ACTIVE, DORMANT, DISBANDED)
  actorType: string (optional) - Filter by type (NATION_STATE, CYBERCRIMINAL, HACKTIVIST)
  nationality: string (optional) - Filter by nationality
  limit: integer (optional, default: 100)
  offset: integer (optional, default: 0)

Response 200 OK:
{
  "data": [
    {
      "id": "actor-uuid",
      "actorId": "TA-001",
      "name": "APT29",
      "aliases": ["Cozy Bear", "The Dukes"],
      "actorType": "NATION_STATE",
      "sophisticationLevel": "ADVANCED",
      "primaryMotivation": "ESPIONAGE",
      "nationality": "Russia",
      "status": "ACTIVE",
      "firstSeen": "2008-01-01T00:00:00Z",
      "lastSeen": "2024-01-15T00:00:00Z",
      "primaryTargets": ["GOVERNMENT", "DEFENSE", "ENERGY"],
      "campaigns": 47,
      "knownVictims": 150
    }
  ]
}
```

### Get Threat Actor TTPs
```http
GET /threat-actors/{actorId}/ttps

Response 200 OK:
{
  "data": {
    "actorId": "TA-001",
    "actorName": "APT29",
    "tactics": [
      {
        "tacticId": "TA0001",
        "tacticName": "Initial Access",
        "techniques": [
          {
            "techniqueId": "T1566",
            "techniqueName": "Phishing",
            "frequency": "FREQUENT",
            "firstObserved": "2015-03-01T00:00:00Z",
            "lastObserved": "2024-01-10T00:00:00Z",
            "observationCount": 234
          }
        ]
      }
    ],
    "tools": [
      {
        "toolName": "HAMMERTOSS",
        "toolType": "BACKDOOR",
        "firstSeen": "2015-07-01T00:00:00Z"
      }
    ]
  }
}
```

### Search Indicators
```http
GET /indicators?type={type}&value={value}&status={status}

Query Parameters:
  type: string (optional) - Filter by type (IP, DOMAIN, URL, FILE_HASH, EMAIL)
  value: string (optional) - Search by indicator value
  status: string (optional) - Filter by status (ACTIVE, INACTIVE, REVOKED)
  severity: string (optional) - Filter by severity
  validOnly: boolean (optional, default: true) - Only valid (non-expired) indicators
  confidenceMin: float (optional) - Minimum confidence score (0.0-1.0)
  limit: integer (optional, default: 100)
  offset: integer (optional, default: 0)

Response 200 OK:
{
  "data": [
    {
      "id": "ind-uuid",
      "indicatorId": "IND-001",
      "value": "192.0.2.1",
      "type": "IP",
      "category": "C2",
      "severity": "HIGH",
      "confidenceScore": 0.92,
      "validFrom": "2024-01-01T00:00:00Z",
      "validUntil": "2024-03-01T00:00:00Z",
      "isExpired": false,
      "tlpMarking": "AMBER",
      "relatedCampaigns": ["CAMP-001"],
      "relatedActors": ["TA-001"],
      "hitCount": 47
    }
  ]
}
```

---

## Alert API Endpoints

### List Alerts
```http
GET /alerts?status={status}&severity={severity}&limit={limit}

Query Parameters:
  status: string (optional) - Filter by status (NEW, IN_PROGRESS, RESOLVED, CLOSED)
  severity: string (optional) - Filter by severity
  alertType: string (optional) - Filter by type (INTRUSION, MALWARE, POLICY_VIOLATION)
  assignedTo: string (optional) - Filter by assigned user
  detectionTimeAfter: datetime (optional) - Filter by detection time
  detectionTimeBefore: datetime (optional) - Filter by detection time
  truePositive: boolean (optional) - Filter true/false positives
  limit: integer (optional, default: 100)
  offset: integer (optional, default: 0)

Response 200 OK:
{
  "data": [
    {
      "id": "alert-uuid",
      "alertId": "ALERT-001",
      "title": "Critical CVE Exploitation Detected",
      "description": "Exploitation attempt detected for CVE-2024-1234",
      "alertType": "INTRUSION",
      "severity": "CRITICAL",
      "status": "NEW",
      "detectionTime": "2024-01-20T11:45:00Z",
      "detectionSource": "IDS",
      "affectedAssets": ["ASSET-001"],
      "sourceIp": "203.0.113.1",
      "destinationIp": "10.0.1.100",
      "riskScore": 9.5,
      "truePositive": null,
      "assignedTo": null
    }
  ]
}
```

### Update Alert Status
```http
PATCH /alerts/{alertId}
Content-Type: application/json

{
  "status": "IN_PROGRESS",
  "assignedTo": "analyst@example.com",
  "priority": 1,
  "analystNotes": "Investigating exploitation attempt..."
}

Response 200 OK:
{
  "data": {
    "id": "alert-uuid",
    "alertId": "ALERT-001",
    "status": "IN_PROGRESS",
    "assignedTo": "analyst@example.com",
    "priority": 1,
    "updatedAt": "2024-01-20T12:00:00Z"
  }
}
```

---

## Bulk Operations API

### Bulk Import CVEs
```http
POST /bulk/cves
Content-Type: application/json

{
  "cves": [
    {
      "cveId": "CVE-2024-1234",
      "description": "...",
      "publishedDate": "2024-01-15T10:00:00Z",
      /* ... other CVE properties */
    }
  ],
  "options": {
    "updateExisting": true,
    "validateSchema": true,
    "batchSize": 1000
  }
}

Response 202 Accepted:
{
  "data": {
    "jobId": "job-uuid",
    "status": "PROCESSING",
    "totalRecords": 5000,
    "estimatedCompletionTime": "2024-01-20T12:30:00Z"
  },
  "links": {
    "status": "/bulk/jobs/job-uuid"
  }
}
```

### Check Bulk Job Status
```http
GET /bulk/jobs/{jobId}

Response 200 OK:
{
  "data": {
    "jobId": "job-uuid",
    "jobType": "CVE_IMPORT",
    "status": "COMPLETED",
    "startTime": "2024-01-20T12:00:00Z",
    "endTime": "2024-01-20T12:25:00Z",
    "totalRecords": 5000,
    "processedRecords": 5000,
    "successfulRecords": 4987,
    "failedRecords": 13,
    "errors": [
      {
        "recordId": "CVE-2024-9999",
        "error": "Duplicate CVE ID",
        "severity": "WARNING"
      }
    ]
  }
}
```

---

## GraphQL API Specification

### GraphQL Endpoint
```
POST /graphql
Content-Type: application/json
Authorization: Bearer {accessToken}
```

### Schema Definition (Partial)

```graphql
type Query {
  # CVE Queries
  cve(cveId: String!): CVE
  cves(filter: CVEFilter, pagination: Pagination, sort: Sort): CVEConnection!

  # Asset Queries
  asset(assetId: String!): Asset
  assets(filter: AssetFilter, pagination: Pagination): AssetConnection!

  # Threat Intelligence
  threatActor(actorId: String!): ThreatActor
  threatActors(filter: ThreatActorFilter): [ThreatActor!]!

  # Alert Queries
  alert(alertId: String!): Alert
  alerts(filter: AlertFilter, pagination: Pagination): AlertConnection!

  # Analytics
  vulnerabilityTrends(timeRange: TimeRange!): [VulnerabilityTrend!]!
  riskDashboard(organizationId: String!): RiskDashboard!
  attackPathAnalysis(assetId: String!, maxDepth: Int): [AttackPath!]!
}

type Mutation {
  # Asset Management
  createAsset(input: CreateAssetInput!): Asset!
  updateAsset(assetId: String!, input: UpdateAssetInput!): Asset!
  deleteAsset(assetId: String!): Boolean!

  # Alert Management
  updateAlertStatus(alertId: String!, status: AlertStatus!): Alert!
  assignAlert(alertId: String!, assignee: String!): Alert!

  # Mitigation
  createMitigation(input: CreateMitigationInput!): Mitigation!
  applyMitigation(mitigationId: String!, cveId: String!): Boolean!
}

type Subscription {
  # Real-time Updates
  newAlert(filter: AlertFilter): Alert!
  alertStatusChanged(alertId: String): Alert!
  assetVulnerabilityChanged(assetId: String): AssetVulnerabilityUpdate!
  threatIntelUpdate(severity: Severity): ThreatIntelUpdate!
}

# Types
type CVE {
  id: ID!
  cveId: String!
  description: String!
  publishedDate: DateTime!
  lastModifiedDate: DateTime!
  cvssV3Score: Float
  cvssV3Vector: String
  baseSeverity: Severity!

  # Relationships
  cwes: [CWE!]! @relationship(type: "EXPLOITS")
  capecs: [CAPEC!]! @relationship(type: "DEMONSTRATES")
  affectedSoftware: [Software!]! @relationship(type: "AFFECTS")
  mitigations: [Mitigation!]! @relationship(type: "MITIGATES", direction: IN)
  exploits: [Exploit!]! @relationship(type: "EXPLOITED_BY", direction: IN)

  # Computed Fields
  exploitAvailable: Boolean!
  weaponized: Boolean!
  patchAvailable: Boolean!
}

type Asset {
  id: ID!
  assetId: String!
  name: String!
  assetType: AssetType!
  criticality: Criticality!
  status: AssetStatus!
  ipAddress: String
  hostname: String
  riskScore: Float

  # Relationships
  vulnerabilities(status: VulnerabilityStatus): [AssetVulnerability!]!
  software: [Software!]! @relationship(type: "RUNS")
  connectedAssets(depth: Int): [Asset!]! @relationship(type: "CONNECTS_TO")
  department: Department @relationship(type: "BELONGS_TO")
  controls: [Control!]! @relationship(type: "PROTECTS", direction: IN)

  # Computed Fields
  criticalVulnerabilityCount: Int!
  exposureScore: Float!
}

type ThreatActor {
  id: ID!
  actorId: String!
  name: String!
  actorType: ThreatActorType!
  sophisticationLevel: SophisticationLevel
  status: ThreatActorStatus!

  # Relationships
  campaigns: [Campaign!]! @relationship(type: "ATTRIBUTED_TO", direction: IN)
  techniques: [MitreTechnique!]! @relationship(type: "USES_TECHNIQUE")
  malware: [Malware!]! @relationship(type: "USES")

  # Analytics
  ttps: [TTPMapping!]!
  targetProfile: TargetProfile!
}

# Input Types
input CVEFilter {
  severity: [Severity!]
  publishedAfter: DateTime
  publishedBefore: DateTime
  cvssScoreMin: Float
  cvssScoreMax: Float
  hasExploit: Boolean
  keyword: String
}

input Pagination {
  limit: Int = 100
  offset: Int = 0
}

input Sort {
  field: String!
  order: SortOrder = DESC
}

# Enums
enum Severity {
  LOW
  MEDIUM
  HIGH
  CRITICAL
}

enum AssetType {
  SERVER
  WORKSTATION
  NETWORK_DEVICE
  DATABASE
  APPLICATION
  MOBILE
  IOT
}

enum AlertStatus {
  NEW
  IN_PROGRESS
  RESOLVED
  CLOSED
  FALSE_POSITIVE
}
```

### Example GraphQL Queries

```graphql
# Query 1: Get CVE with relationships
query GetCVEDetails($cveId: String!) {
  cve(cveId: $cveId) {
    cveId
    description
    cvssV3Score
    baseSeverity
    cwes {
      cweId
      name
      description
    }
    affectedSoftware {
      vendor
      product
      version
    }
    mitigations {
      name
      effectivenessRating
      implementationSteps
    }
    exploitAvailable
    weaponized
  }
}

# Query 2: Asset vulnerability analysis
query AssetVulnerabilityAnalysis($assetId: String!) {
  asset(assetId: $assetId) {
    name
    assetType
    criticality
    riskScore
    vulnerabilities(status: OPEN) {
      cve {
        cveId
        baseSeverity
        cvssV3Score
      }
      status
      detectedDate
      assetRiskScore
    }
    criticalVulnerabilityCount
    exposureScore
  }
}

# Query 3: Threat actor TTPs
query ThreatActorTTPs($actorId: String!) {
  threatActor(actorId: $actorId) {
    name
    actorType
    sophisticationLevel
    techniques {
      techniqueId
      name
      tactics {
        tacticName
      }
    }
    campaigns {
      name
      startDate
      status
    }
    malware {
      name
      malwareType
    }
  }
}

# Mutation: Update alert status
mutation UpdateAlert($alertId: String!, $status: AlertStatus!) {
  updateAlertStatus(alertId: $alertId, status: $status) {
    alertId
    status
    updatedAt
  }
}

# Subscription: New critical alerts
subscription OnNewCriticalAlert {
  newAlert(filter: { severity: CRITICAL }) {
    alertId
    title
    severity
    detectionTime
    affectedAssets {
      name
      assetType
    }
  }
}
```

---

## WebSocket API Specification

### WebSocket Connection
```
wss://api.aeon-cyber.com/v3/ws
```

### Authentication
```javascript
// Client connection with JWT
const socket = io('wss://api.aeon-cyber.com/v3/ws', {
  auth: {
    token: 'Bearer eyJhbGciOiJSUzI1NiIs...'
  }
});
```

### Event Types

#### Subscribe to Alerts
```javascript
// Client subscribes to alert stream
socket.emit('subscribe', {
  channel: 'alerts',
  filter: {
    severity: ['HIGH', 'CRITICAL'],
    status: ['NEW', 'IN_PROGRESS']
  }
});

// Server sends new alerts
socket.on('alert:new', (data) => {
  console.log('New alert:', data);
  // {
  //   alertId: 'ALERT-001',
  //   title: 'Critical CVE Exploitation Detected',
  //   severity: 'CRITICAL',
  //   detectionTime: '2024-01-20T12:00:00Z'
  // }
});
```

#### Subscribe to Asset Updates
```javascript
// Subscribe to specific asset
socket.emit('subscribe', {
  channel: 'asset:ASSET-001',
  events: ['vulnerability:new', 'vulnerability:resolved', 'risk:changed']
});

// Receive asset updates
socket.on('asset:vulnerability:new', (data) => {
  // {
  //   assetId: 'ASSET-001',
  //   cveId: 'CVE-2024-5678',
  //   severity: 'HIGH',
  //   detectedDate: '2024-01-20T12:05:00Z'
  // }
});
```

#### Real-time Analytics Stream
```javascript
// Subscribe to vulnerability trends
socket.emit('subscribe', {
  channel: 'analytics:vulnerability-trends',
  interval: 60000 // Update every 60 seconds
});

socket.on('analytics:vulnerability-trends', (data) => {
  // {
  //   timestamp: '2024-01-20T12:00:00Z',
  //   trends: {
  //     new_cves_last_hour: 23,
  //     critical_count: 5,
  //     high_count: 12,
  //     trending_cwes: ['CWE-79', 'CWE-89']
  //   }
  // }
});
```

---

## Rate Limiting

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1706097600
```

### Rate Limit Tiers
- **Free Tier**: 100 requests/hour
- **Standard Tier**: 1,000 requests/hour
- **Professional Tier**: 10,000 requests/hour
- **Enterprise Tier**: Unlimited (with fair use policy)

### Rate Limit Response
```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1706097600
Retry-After: 3600

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please retry after 3600 seconds.",
    "retryAfter": 3600
  }
}
```

---

## Error Responses

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "fieldName",
      "reason": "Specific reason for error"
    },
    "requestId": "req-uuid",
    "timestamp": "2024-01-20T12:00:00Z"
  }
}
```

### Common Error Codes
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (missing or invalid authentication)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (resource does not exist)
- `409` - Conflict (resource already exists)
- `422` - Unprocessable Entity (validation failed)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error
- `503` - Service Unavailable (maintenance or overload)

---

## API Versioning

### Version Strategy
- URL-based versioning: `/v3/`
- Header-based version override: `X-API-Version: v3`
- Deprecation notice period: 6 months minimum
- Support for N-1 versions (v2 and v3 concurrently)

### Version Deprecation Headers
```http
X-API-Deprecated: true
X-API-Deprecation-Date: 2025-01-01
X-API-Sunset-Date: 2025-07-01
X-API-Successor-Version: v4
Link: <https://api.aeon-cyber.com/v4/cves>; rel="successor-version"
```

---

## Performance Targets

### API Performance SLAs
- **P50 Latency**: < 100ms (single resource GET)
- **P95 Latency**: < 500ms
- **P99 Latency**: < 1000ms
- **Availability**: 99.9% uptime
- **Throughput**: 10,000 requests/second (production cluster)

### GraphQL Performance
- **Simple Query P50**: < 150ms
- **Complex Query P50**: < 500ms
- **Subscription Latency**: < 50ms (event delivery)

### WebSocket Performance
- **Connection Establishment**: < 100ms
- **Event Delivery Latency**: < 50ms
- **Concurrent Connections**: 100,000+ (per cluster)

---

## Version History

- v3.0.0 (2025-11-19): Complete API specification with GraphQL and WebSocket
- v2.5.0 (2025-11-11): Added threat intelligence endpoints
- v2.0.0 (2025-11-01): Initial comprehensive API specification

---

**Document Classification**: TECHNICAL SPECIFICATION
**Confidentiality**: INTERNAL USE
**Review Cycle**: Quarterly
**Next Review**: 2026-02-19
