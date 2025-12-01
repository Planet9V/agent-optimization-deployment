# AEON API OVERVIEW - Complete Endpoint Catalog

**File**: API_OVERVIEW.md
**Created**: 2025-11-25
**Version**: 1.0.0
**Author**: API Architecture Team
**Purpose**: Complete catalog of all 36+ API endpoints with authentication, rate limiting, and quick start guide
**Status**: PRODUCTION READY
**Target Audience**: API consumers, integrators, developers, DevOps teams

---

## EXECUTIVE SUMMARY

The AEON API provides comprehensive access to the 7-level cyber-physical knowledge architecture through three primary interfaces:

- **REST API**: Traditional HTTP endpoints for sector, equipment, vulnerability, event data (26 endpoints)
- **GraphQL API**: Flexible query interface for complex multi-level traversals (10+ operations)
- **Real-Time WebSocket**: Subscriptions for Level 5 intelligence streams (4+ subscription types)

**Total System Coverage**: 36+ endpoints across 16 CISA sectors, 1.1M+ equipment nodes, 4,100+ CVE mappings, 3.3M+ relationships

**Performance Targets**:
- REST queries: <500ms average latency
- GraphQL queries: <500ms average latency
- Subscriptions: <100ms push latency
- Concurrent connections: 10,000+
- Uptime: 99.9% SLA

---

## TABLE OF CONTENTS

1. [API Architecture Overview](#api-architecture-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Rate Limiting & Quotas](#rate-limiting--quotas)
4. [REST API Endpoints (26)](#rest-api-endpoints)
5. [GraphQL Operations (10+)](#graphql-operations)
6. [WebSocket Subscriptions (4+)](#websocket-subscriptions)
7. [Endpoint Categories & Business Value](#endpoint-categories--business-value)
8. [Error Handling & Recovery](#error-handling--recovery)
9. [Quick Start Guide](#quick-start-guide)
10. [Best Practices & Patterns](#best-practices--patterns)
11. [SDK & Client Libraries](#sdk--client-libraries)
12. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## API ARCHITECTURE OVERVIEW

### 1.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
│         (Web, Mobile, Desktop, Scripts, Webhooks)           │
└────────────┬───────────────────────────────────────┬────────┘
             │                                       │
     ┌───────▼──────────┐              ┌────────────▼─────┐
     │   REST API       │              │   GraphQL API    │
     │  26 Endpoints    │              │  10+ Operations  │
     └───────┬──────────┘              └────────┬─────────┘
             │                                   │
             │  ┌──────────────────────────────┐ │
             │  │  Authentication Gateway       │ │
             │  │  - JWT/Token Validation       │ │
             │  │  - Rate Limit Enforcement    │ │
             │  │  - Request Routing            │ │
             │  └──────┬──────────────┬────────┘ │
             │         │              │          │
     ┌──────▼──┐  ┌───▼──────────┐ ┌─▼─────┐   │
     │Auth API │  │Sector API    │ │Graph  │◄──┘
     │         │  │Equipment API │ │Engine │
     │         │  │CVE API       │ │       │
     └─────────┘  │Event API     │ └───────┘
                  │Analytics API │
                  └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    ┌───▼────┐    ┌─────▼────┐   ┌──────▼──┐
    │  Neo4j │    │PostgreSQL│   │ Qdrant  │
    │Knowledge│    │App State │   │Vectors  │
    │Graph   │    │Jobs      │   │Embeddings│
    └────────┘    └──────────┘   └─────────┘
```

### 1.2 API Versions

Current: `v1.0.0`
- Release Date: 2025-11-25
- Stability: Production Ready
- Breaking Changes: None (forward compatible)

### 1.3 Base URLs

| Environment | URL | Protocol |
|------------|-----|----------|
| Production | `https://api.aeon-dt.com/api/v1` | HTTPS/2 |
| Staging | `https://staging-api.aeon-dt.com/api/v1` | HTTPS/2 |
| Development | `http://localhost:3000/api/v1` | HTTP/1.1 |

---

## AUTHENTICATION & AUTHORIZATION

### 2.1 Authentication Methods

#### JWT Bearer Token (Primary)

```bash
curl -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  https://api.aeon-dt.com/api/v1/sectors
```

**Token Structure**:
- Algorithm: RS256 (RSA + SHA-256)
- Expires: 15 minutes (access), 7 days (refresh)
- Claims: `user_id`, `scopes`, `organization`, `iat`, `exp`

#### API Key Authentication

```bash
curl -H "X-API-Key: aeon_prod_abc123xyz789..." \
  https://api.aeon-dt.com/api/v1/sectors
```

**Key Format**: `aeon_{env}_{32-char-random-string}`
- No expiration (until manually revoked)
- Can be rate-limited per key
- Supports IP whitelisting

#### OAuth 2.0 (Enterprise)

```bash
curl -H "Authorization: Bearer {access_token}" \
  https://api.aeon-dt.com/api/v1/sectors
```

Supported flows:
- Authorization Code (web apps)
- Client Credentials (service accounts)
- Refresh Token (session management)

### 2.2 Permission Scopes

**Granular Scope System**:

```
read                          (Read-only access)
├── read:sectors
├── read:equipment
├── read:vulnerabilities
├── read:events
├── read:predictions
└── read:analytics

write                         (Write/modify data)
├── write:sectors
├── write:equipment
├── write:events
└── write:predictions

admin                         (Administrative)
├── admin:users
├── admin:keys
├── admin:roles
└── admin:organization

system                        (System-level)
├── system:config
└── system:audit
```

**Scope Requirements by Endpoint**:

| Endpoint | Required Scope | Min Role |
|----------|---|---|
| GET /sectors | read:sectors | User |
| POST /sectors | write:sectors | Admin |
| GET /equipment | read:equipment | User |
| POST /equipment | write:equipment | Admin |
| GET /vulnerabilities | read:vulnerabilities | User |
| POST /events | write:events | Analyst |

### 2.3 Role-Based Access Control (RBAC)

Predefined roles with scope combinations:

| Role | Scopes | Use Case |
|------|--------|----------|
| Viewer | read:* | Dashboard/reporting only |
| Analyst | read:*, write:events | Threat analysis & incident response |
| Admin | read:*, write:*, admin:* | Team management & administration |
| Service Account | Custom scopes | Integration & automation |

---

## RATE LIMITING & QUOTAS

### 3.1 Rate Limit Tiers

#### Free Tier
- **Requests/Day**: 1,000
- **Requests/Minute**: 10
- **Concurrent**: 2
- **Data Transfer**: 100 MB/month
- **Cost**: Free

#### Professional Tier
- **Requests/Day**: 100,000
- **Requests/Minute**: 100
- **Concurrent**: 20
- **Data Transfer**: 10 GB/month
- **Batch Operations**: 1,000 items
- **Cost**: $299/month

#### Enterprise Tier
- **Requests/Day**: Unlimited
- **Requests/Minute**: 1,000
- **Concurrent**: 100+
- **Data Transfer**: Unlimited
- **Batch Operations**: 10,000+ items
- **Cost**: Custom pricing
- **SLA**: 99.99% uptime
- **Support**: 24/7 Priority

### 3.2 Rate Limit Headers

Every response includes:

```http
X-RateLimit-Limit: 100000
X-RateLimit-Remaining: 99856
X-RateLimit-Reset: 1732534200
X-RateLimit-Tier: professional
X-RateLimit-Window: 86400
```

### 3.3 Rate Limit Response (429)

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Retry after 60 seconds.",
    "details": {
      "limit": 100000,
      "remaining": 0,
      "reset_at": "2025-11-26T14:22:00Z",
      "retry_after_seconds": 60
    }
  }
}
```

---

## REST API ENDPOINTS

### 4.1 Authentication Endpoints (3)

#### POST /auth/login
Login with email/password, obtain JWT tokens
- **Scopes**: None (public)
- **Rate Limit**: 5/minute per IP
- **Response**: access_token, refresh_token, user data
- **Use Case**: User authentication

#### POST /auth/refresh
Refresh expired access token
- **Scopes**: None (refresh_token required)
- **Rate Limit**: 10/minute
- **Response**: New access_token, refresh_token
- **Use Case**: Token renewal

#### POST /auth/logout
Invalidate tokens and end session
- **Scopes**: None (bearer token required)
- **Rate Limit**: No limit
- **Response**: Success message
- **Use Case**: User sign-out

**Business Value**: Secure user authentication with multi-layer protection

---

### 4.2 Sector Endpoints (6)

#### GET /sectors
List all 16 CISA critical infrastructure sectors
- **Scopes**: read:sectors
- **Parameters**: None
- **Response**: [{ id, name, riskScore, equipmentCount, vulnerabilityCount }]
- **Latency**: ~100ms
- **Cache**: 5 minutes
- **Use Case**: Sector enumeration, dashboard overview

#### GET /sectors/{sector}
Get comprehensive sector details
- **Scopes**: read:sectors
- **Parameters**: sector (ENERGY, WATER, NUCLEAR, etc.)
- **Response**: Full sector profile with risk, equipment, vulnerabilities
- **Latency**: ~300ms
- **Cache**: 5 minutes
- **Use Case**: Sector-specific risk assessment

#### GET /sectors/{sector}/equipment
List equipment in sector with filtering
- **Scopes**: read:equipment
- **Parameters**: equipment_type, criticality, vendor, status, page, limit
- **Response**: Paginated equipment list
- **Latency**: ~400ms
- **Limit**: 500 items/page
- **Use Case**: Equipment inventory management

#### GET /sectors/{sector}/vulnerabilities
Get CVE mappings for sector
- **Scopes**: read:vulnerabilities
- **Parameters**: severity, exploitable, affected_min, sort, page, limit
- **Response**: Vulnerability list with remediation guidance
- **Latency**: ~500ms
- **Cache**: 1 hour
- **Use Case**: Vulnerability prioritization

#### GET /analytics/sectors
Cross-sector analytics and risk rankings
- **Scopes**: read:analytics
- **Parameters**: time_period (7d, 30d, 90d), metrics, include_predictions
- **Response**: Sector rankings, trends, predictions
- **Latency**: ~1000ms
- **Cache**: 1 hour
- **Use Case**: Strategic risk reporting

#### GET /analytics/dependencies
Analyze cross-sector dependencies
- **Scopes**: read:analytics
- **Parameters**: sector, dependency_type, critical_only
- **Response**: Dependency graph, failure scenarios
- **Latency**: ~800ms
- **Cache**: 1 hour
- **Use Case**: Supply chain & cascade failure analysis

**Business Value**: Complete sector visibility, risk ranking, dependency mapping

---

### 4.3 Equipment Endpoints (5)

#### GET /equipment
List all equipment with filtering
- **Scopes**: read:equipment
- **Parameters**: sector, vendor, equipment_type, criticality, status
- **Response**: Paginated equipment list (max 500/page)
- **Latency**: ~400ms
- **Use Case**: Asset inventory

#### GET /equipment/{equipment_id}
Get detailed equipment profile
- **Scopes**: read:equipment
- **Parameters**: None
- **Response**: Full equipment data with vulnerabilities, location, metrics
- **Latency**: ~200ms
- **Cache**: 5 minutes
- **Use Case**: Equipment deep-dive analysis

#### POST /equipment
Create new equipment record
- **Scopes**: write:equipment
- **Parameters**: name, vendor, model, sector, facility, type
- **Response**: Created equipment object
- **Latency**: ~100ms
- **Use Case**: Asset on-boarding

#### PUT /equipment/{equipment_id}
Update equipment record
- **Scopes**: write:equipment
- **Parameters**: Any updatable fields
- **Response**: Updated equipment object
- **Latency**: ~100ms
- **Use Case**: Asset lifecycle management

#### DELETE /equipment/{equipment_id}
Delete equipment record
- **Scopes**: write:equipment
- **Parameters**: None
- **Response**: Deletion confirmation
- **Latency**: ~100ms
- **Note**: Soft delete (archived, not removed)
- **Use Case**: Asset retirement

**Business Value**: Complete equipment lifecycle management, inventory tracking

---

### 4.4 Vulnerability/CVE Endpoints (6)

#### GET /vulnerabilities
List CVEs with advanced filtering
- **Scopes**: read:vulnerabilities
- **Parameters**: severity, cvss_min, published_after, in_the_wild, exploitable
- **Response**: Paginated CVE list
- **Latency**: ~300ms
- **Use Case**: Vulnerability search

#### GET /vulnerabilities/{cve_id}
Get detailed CVE information
- **Scopes**: read:vulnerabilities
- **Parameters**: None
- **Response**: Full CVE profile with CVSS, affected systems, mitigations
- **Latency**: ~200ms
- **Cache**: 1 hour
- **Use Case**: Vulnerability research

#### GET /vulnerabilities/{cve_id}/affected-equipment
Find equipment affected by specific CVE
- **Scopes**: read:vulnerabilities
- **Parameters**: sector, criticality, patch_status
- **Response**: List of affected equipment
- **Latency**: ~400ms
- **Use Case**: Impact assessment, remediation planning

#### POST /vulnerabilities/register
Register newly discovered vulnerability
- **Scopes**: write:equipment
- **Parameters**: equipment_id, cve_id, discovery_date
- **Response**: Registration confirmation
- **Latency**: ~100ms
- **Use Case**: Incident response

#### GET /vulnerabilities/trend
Get vulnerability trends over time
- **Scopes**: read:analytics
- **Parameters**: sector, time_period, granularity
- **Response**: Time-series vulnerability data
- **Latency**: ~500ms
- **Cache**: 1 hour
- **Use Case**: Risk trend analysis

#### POST /vulnerabilities/{cve_id}/mitigations
Register mitigation for CVE
- **Scopes**: write:events
- **Parameters**: equipment_id, mitigation_type, implementation_date
- **Response**: Mitigation record
- **Latency**: ~100ms
- **Use Case**: Mitigation tracking

**Business Value**: CVE intelligence, affected equipment discovery, mitigation planning

---

### 4.5 Event Endpoints (3)

#### GET /events
List security events with filtering
- **Scopes**: read:events
- **Parameters**: type, severity, date_range, sector, source
- **Response**: Paginated event list
- **Latency**: ~300ms
- **Use Case**: Event log search

#### POST /events
Create new security event record
- **Scopes**: write:events
- **Parameters**: type, severity, description, source, related_cve
- **Response**: Created event object
- **Latency**: ~100ms
- **Use Case**: Incident logging

#### GET /events/{event_id}
Get detailed event information
- **Scopes**: read:events
- **Parameters**: None
- **Response**: Full event profile with context and intelligence
- **Latency**: ~100ms
- **Cache**: Permanent (immutable)
- **Use Case**: Incident investigation

**Business Value**: Security event logging, incident tracking, forensics

---

### 4.6 Prediction/Analytics Endpoints (3)

#### GET /predictions
List breach probability predictions
- **Scopes**: read:predictions
- **Parameters**: sector, type, probability_min, time_window
- **Response**: Paginated prediction list
- **Latency**: ~300ms
- **Cache**: 1 hour
- **Use Case**: Risk forecasting

#### GET /predictions/{sector_id}/forecast
Get detailed breach forecast for sector
- **Scopes**: read:predictions
- **Parameters**: horizon_days (30, 90, 180)
- **Response**: Probability scores, confidence levels, contributing factors
- **Latency**: ~500ms
- **Cache**: 1 hour
- **Use Case**: Executive reporting, budget justification

#### POST /predictions/{prediction_id}/feedback
Provide feedback on prediction accuracy
- **Scopes**: write:predictions
- **Parameters**: outcome, feedback_text
- **Response**: Feedback confirmation
- **Latency**: ~100ms
- **Use Case**: ML model improvement

**Business Value**: Psychohistory predictions, proactive threat forecasting

---

## GRAPHQL OPERATIONS

### 5.1 Query Operations (5)

#### GetSectorRisk
Single sector with full risk assessment
- **Complexity**: ~50 points
- **Latency**: ~300ms
- **Cache**: 5 minutes
- **Use Case**: Sector dashboard

#### ExplorerSectorRisk
Multi-level traversal (sector → facilities → equipment → CVE)
- **Complexity**: ~500 points
- **Latency**: ~800ms
- **Cache**: None (real-time)
- **Use Case**: Deep threat intelligence

#### GetCVEIntelligence
CVE search with threat context
- **Complexity**: ~200 points
- **Latency**: ~500ms
- **Cache**: 1 hour
- **Use Case**: Vulnerability intelligence

#### DiscoverAttackPaths
Attack chain analysis
- **Complexity**: ~800 points
- **Latency**: ~1000ms
- **Cache**: 1 hour
- **Use Case**: Penetration testing, vulnerability assessment

#### GetBreachPredictions
Psychohistory prediction with all factors
- **Complexity**: ~600 points
- **Latency**: ~800ms
- **Cache**: 1 hour
- **Use Case**: Executive risk briefing

---

### 5.2 Mutation Operations (5)

#### RegisterVulnerability
Record discovered vulnerability on equipment
- **Complexity**: ~20 points
- **Cache Invalidation**: equipment, CVE
- **Use Case**: Incident response

#### ImplementMitigation
Track mitigation implementation
- **Complexity**: ~30 points
- **Cache Invalidation**: equipment vulnerabilities
- **Use Case**: Remediation tracking

#### BatchImportEquipment
Import multiple equipment records
- **Complexity**: ~50 points (per item)
- **Batch Limit**: 1,000 items
- **Cache Invalidation**: sector inventory
- **Use Case**: Asset ingestion

#### UpdatePredictionAccuracy
Feedback loop for ML model improvement
- **Complexity**: ~20 points
- **Cache Invalidation**: predictions
- **Use Case**: Model training

#### UpdateSectorRisk
Manual risk assessment update
- **Complexity**: ~30 points
- **Cache Invalidation**: analytics
- **Use Case**: Executive override

---

### 5.3 Subscription Operations (4+)

#### OnNewCVE
Real-time CVE publication feed
- **Severity Filter**: Optional (CRITICAL, HIGH, etc.)
- **Update Frequency**: Milliseconds
- **Use Case**: CVE monitoring

#### OnThreatEvent
Real-time threat event detection
- **Sector Filter**: Optional
- **Update Frequency**: Milliseconds
- **Use Case**: Security monitoring

#### OnPredictionChange
Prediction update notifications
- **Type Filter**: Optional
- **Update Frequency**: ~1 hour
- **Use Case**: Risk scoring updates

#### MonitorSectorRisk
Real-time sector risk monitoring
- **Metrics**: riskScore, threatLevel, alerts
- **Update Frequency**: 5 minutes
- **Use Case**: Executive dashboard

---

## WEBSOCKET SUBSCRIPTIONS

### 6.1 Real-Time Connections

**Endpoint**: `wss://api.aeon-dt.com/graphql` (production)

**Connection Flow**:
```
1. WebSocket handshake
2. Send authentication: {"type": "connection_init", "payload": {"token": "..."}}
3. Server acknowledges: {"type": "connection_ack"}
4. Send subscription: {"id": "1", "type": "start", "payload": {...}}
5. Receive updates: {"id": "1", "type": "data", "payload": {...}}
```

### 6.2 Subscription Features

- **Reconnection**: Automatic with exponential backoff
- **Message Queue**: Persist 1,000 messages during disconnection
- **Compression**: Optional gzip compression
- **Timeout**: 5 minutes of inactivity → close
- **Max Concurrent**: 100 subscriptions per user

---

## ENDPOINT CATEGORIES & BUSINESS VALUE

### 7.1 Category Breakdown

| Category | Endpoints | Primary Use | Business Value |
|----------|-----------|-------------|-----------------|
| **Authentication** | 3 | User/API key management | Secure access control |
| **Sectors** | 6 | Infrastructure visibility | Risk ranking, compliance |
| **Equipment** | 5 | Asset inventory | Lifecycle management |
| **Vulnerabilities** | 6 | CVE intelligence | Remediation planning |
| **Events** | 3 | Incident tracking | Forensics, SIEM integration |
| **Predictions** | 3 | Risk forecasting | Proactive security |
| **Analytics** | 2 | Cross-sector analysis | Supply chain visibility |
| **GraphQL** | 10+ | Flexible queries | Developer agility |
| **Subscriptions** | 4+ | Real-time updates | Immediate alerting |
| **Total** | **36+** | Complete platform | End-to-end cyber risk |

### 7.2 Use Case Matrix

| Use Case | Primary Endpoints | Secondary | Frequency |
|----------|------------------|-----------|-----------|
| **Risk Dashboard** | GET /sectors, /analytics | /predictions | Real-time |
| **Incident Response** | POST /events, /vulnerabilities | GET /equipment | On-demand |
| **Compliance Audit** | GET /sectors, /analytics | /vulnerabilities | Monthly |
| **Asset Management** | GET/POST /equipment | /sectors | Continuous |
| **Threat Intelligence** | Subscriptions (CVE) | GET /vulnerabilities | Real-time |
| **Remediation Planning** | GET /vulnerabilities | /analytics | Weekly |
| **Executive Reporting** | GET /predictions, /analytics | /sectors | Monthly |
| **Integration/Automation** | GraphQL batch | REST endpoints | Continuous |

---

## ERROR HANDLING & RECOVERY

### 8.1 Standard Error Response

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid sector identifier",
    "details": {
      "field": "sector",
      "expected": "One of: ENERGY, WATER, NUCLEAR...",
      "received": "INVALID_SECTOR"
    }
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2025-11-25T14:22:00Z"
  }
}
```

### 8.2 Common HTTP Status Codes

| Code | Meaning | Retry |
|------|---------|-------|
| 200 | OK | No |
| 201 | Created | No |
| 204 | No Content | No |
| 400 | Bad Request | No |
| 401 | Unauthorized | Yes (refresh token) |
| 403 | Forbidden | No |
| 404 | Not Found | No |
| 429 | Rate Limited | Yes (exponential backoff) |
| 500 | Server Error | Yes (exponential backoff) |
| 503 | Service Unavailable | Yes (with delay) |

### 8.3 Real Error Response Examples

**404 Not Found - Sector doesn't exist:**
```json
{
  "status": "error",
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Sector 'INVALID_SECTOR' not found",
    "details": {
      "resource_type": "sector",
      "requested_id": "INVALID_SECTOR",
      "available_sectors": ["ENERGY", "WATER", "NUCLEAR", "HEALTHCARE", "COMMERCIAL", "DEFENSE", "TRANSPORTATION"],
      "suggestion": "Use GET /sectors to list all available sectors"
    }
  },
  "meta": {
    "query_id": "qry_abc123xyz789",
    "request_id": "req_abc123",
    "timestamp": "2025-11-25T14:22:00Z",
    "documentation": "https://api.aeon-dt.com/docs/errors#RESOURCE_NOT_FOUND"
  }
}
```

**429 Rate Limited - With exponential backoff guidance:**
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Retry after 60 seconds.",
    "details": {
      "limit": 100000,
      "remaining": 0,
      "reset_at": "2025-11-26T14:22:00Z",
      "retry_after_seconds": 60,
      "tier": "professional",
      "current_burst": 150,
      "max_burst": 100,
      "window": "24 hours",
      "recommendation": "Implement exponential backoff: wait 1s, 2s, 4s, 8s, 16s...",
      "upgrade_tier": "Consider Enterprise tier for unlimited requests"
    }
  },
  "meta": {
    "query_id": "qry_rate_limit_001",
    "request_id": "req_xyz789",
    "timestamp": "2025-11-25T14:22:00Z",
    "documentation": "https://api.aeon-dt.com/docs/rate-limiting"
  }
}
```

**500 Internal Server Error - With debugging info:**
```json
{
  "status": "error",
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "Database query timeout during complex graph traversal",
    "details": {
      "error_type": "database_timeout",
      "query_duration_ms": 30000,
      "timeout_threshold_ms": 30000,
      "affected_query": "GET /sectors/ENERGY/equipment",
      "suggestion": "Reduce query scope or use pagination with limit=100",
      "retry_safe": true,
      "estimated_recovery_time": "30 seconds"
    }
  },
  "meta": {
    "query_id": "qry_timeout_500",
    "request_id": "req_error_500",
    "timestamp": "2025-11-25T14:22:00Z",
    "incident_id": "inc_20251125_001",
    "documentation": "https://api.aeon-dt.com/docs/errors#INTERNAL_SERVER_ERROR",
    "support_contact": "support@aeon-dt.com"
  }
}
```

**400 Bad Request - Invalid query parameters:**
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid query parameters",
    "details": {
      "invalid_params": [
        {
          "field": "cvss_min",
          "value": "15.0",
          "expected": "Number between 0.0 and 10.0",
          "error": "Value exceeds maximum CVSS score"
        },
        {
          "field": "date_format",
          "value": "11/25/2025",
          "expected": "ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ",
          "example": "2025-11-25T14:22:00Z"
        }
      ],
      "valid_example": "GET /vulnerabilities?cvss_min=7.0&published_after=2025-11-20T00:00:00Z"
    }
  },
  "meta": {
    "query_id": "qry_validation_001",
    "request_id": "req_bad_400",
    "timestamp": "2025-11-25T14:22:00Z",
    "documentation": "https://api.aeon-dt.com/docs/query-parameters"
  }
}
```

### 8.4 Retry Strategy with Exponential Backoff

```javascript
async function apiCallWithRetry(endpoint, options = {}) {
  const maxRetries = 3;
  const baseDelay = 1000;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(endpoint, options);

      if (response.ok) return response.json();

      // Retry on server errors and rate limits
      if ([429, 500, 503].includes(response.status)) {
        const delay = baseDelay * Math.pow(2, attempt - 1) + Math.random() * 1000;
        await new Promise(r => setTimeout(r, delay));
        continue;
      }

      // Don't retry on client errors
      throw new Error(`API Error: ${response.status}`);
    } catch (error) {
      if (attempt === maxRetries) throw error;
    }
  }
}
```

---

## QUICK START GUIDE

### 9.1 Getting Started (5 minutes)

#### Step 1: Obtain API Key

1. Navigate to https://dashboard.aeon-dt.com
2. Sign in with your account
3. Go to **Settings** → **API Keys**
4. Click **Create New Key**
5. Name: "My First Integration"
6. Scopes: `read:sectors`, `read:equipment`
7. Copy the key (shown only once)

#### Step 2: Make First Request

```bash
curl -X GET "https://api.aeon-dt.com/api/v1/sectors" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "status": "success",
  "data": {
    "sectors": [
      {
        "id": "ENERGY",
        "name": "Energy",
        "riskScore": 8.2,
        "equipmentCount": 67110,
        "vulnerabilityCount": 1200
      },
      // ... 15 more sectors
    ]
  }
}
```

#### Step 3: Explore Key Endpoints

**Get Energy Sector Details**:
```bash
curl "https://api.aeon-dt.com/api/v1/sectors/ENERGY" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**List Equipment in Energy Sector**:
```bash
curl "https://api.aeon-dt.com/api/v1/sectors/ENERGY/equipment?limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Find Critical Vulnerabilities**:
```bash
curl "https://api.aeon-dt.com/api/v1/vulnerabilities?severity=CRITICAL&limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

### 9.2 GraphQL Quick Start

#### Set Up Apollo Client

```bash
npm install @apollo/client graphql
```

```typescript
import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';

const client = new ApolloClient({
  link: new HttpLink({
    uri: 'https://api.aeon-dt.com/graphql',
    headers: {
      Authorization: `Bearer YOUR_API_KEY`,
    },
  }),
  cache: new InMemoryCache(),
});
```

#### Execute Query

```typescript
import { gql } from '@apollo/client';

const GET_SECTOR = gql`
  query GetSector($id: ID!) {
    sector(id: $id) {
      id
      name
      riskScore
      threatLevel
      statistics {
        totalNodes
        vulnerabilityCount: averageVulnerabilityScore
        breachProbability
      }
    }
  }
`;

client.query({
  query: GET_SECTOR,
  variables: { id: 'ENERGY' }
}).then(result => console.log(result.data));
```

---

### 9.3 Real-Time Monitoring

```typescript
import { useSubscription, gql } from '@apollo/client';

const THREAT_MONITOR = gql`
  subscription MonitorSectorRisk($sectorId: ID!) {
    sectorRiskMonitor(sectorId: $sectorId) {
      sectorId
      riskScore
      threatLevel
      alerts {
        id
        severity
        message
      }
    }
  }
`;

function ThreatMonitor({ sectorId }) {
  const { data, loading } = useSubscription(THREAT_MONITOR, {
    variables: { sectorId },
  });

  if (loading) return 'Monitoring...';

  return (
    <div>
      <h2>Sector Risk: {data?.sectorRiskMonitor?.riskScore}</h2>
      <p>Threat Level: {data?.sectorRiskMonitor?.threatLevel}</p>
      <ul>
        {data?.sectorRiskMonitor?.alerts?.map(alert => (
          <li key={alert.id}>{alert.message}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## BEST PRACTICES & PATTERNS

### 10.1 Pagination

```bash
# Get page 2 with 50 items per page
curl "https://api.aeon-dt.com/api/v1/equipment?page=2&limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Response includes:
```json
{
  "data": { ... },
  "pagination": {
    "current_page": 2,
    "total_pages": 100,
    "total_records": 5000,
    "has_next": true,
    "has_previous": true
  }
}
```

### 10.2 Filtering & Sorting

```bash
# Complex filter with multiple conditions
curl "https://api.aeon-dt.com/api/v1/vulnerabilities?severity=CRITICAL,HIGH&exploitable=true&sort=cvss_score DESC" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 10.3 Caching Strategy

```javascript
// Cache sector data for 5 minutes
const CACHE_TTL = 5 * 60 * 1000;
const cache = new Map();

async function getSectorWithCache(sectorId) {
  const cached = cache.get(sectorId);
  if (cached && Date.now() - cached.time < CACHE_TTL) {
    return cached.data;
  }

  const response = await fetch(
    `https://api.aeon-dt.com/api/v1/sectors/${sectorId}`,
    { headers: { Authorization: `Bearer ${apiKey}` } }
  );
  const data = await response.json();
  cache.set(sectorId, { data, time: Date.now() });
  return data;
}
```

### 10.4 Batch Operations

```bash
# Import multiple equipment records
curl -X POST "https://api.aeon-dt.com/api/v1/equipment/batch" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "equipment": [
      {"name": "Router-1", "vendor": "Cisco", "model": "ASR9000"},
      {"name": "Switch-1", "vendor": "Arista", "model": "7358"}
    ]
  }'
```

### 10.5 Error Handling Pattern

```typescript
async function apiCall(endpoint, options = {}) {
  try {
    const response = await fetch(endpoint, {
      ...options,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers,
      }
    });

    if (!response.ok) {
      const error = await response.json();

      if (response.status === 401) {
        // Token expired, refresh
        await refreshToken();
        return apiCall(endpoint, options); // Retry
      }

      throw new Error(`API Error: ${error.error.code} - ${error.error.message}`);
    }

    return response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
}
```

---

## SDK & CLIENT LIBRARIES

### 11.1 Official SDKs

| Language | Library | Status | Link |
|----------|---------|--------|------|
| JavaScript | @aeon/sdk | ✓ Stable | npm |
| Python | aeon-sdk | ✓ Stable | pip |
| Go | github.com/aeon/sdk-go | ✓ Stable | go get |
| Java | com.aeon:sdk | ✓ Stable | Maven |
| .NET | Aeon.Sdk | ✓ Stable | NuGet |
| TypeScript | @aeon/sdk | ✓ Stable | npm |

### 11.2 Installation Examples

```bash
# JavaScript/TypeScript
npm install @aeon/sdk

# Python
pip install aeon-sdk

# Go
go get github.com/aeon/sdk-go

# Java
mvn install
```

### 11.3 SDK Usage Example (JavaScript)

```typescript
import { AeonSDK } from '@aeon/sdk';

const client = new AeonSDK({
  apiKey: 'aeon_prod_abc123xyz789',
  baseUrl: 'https://api.aeon-dt.com/api/v1'
});

// Get all sectors
const sectors = await client.sectors.list();

// Get sector details
const energy = await client.sectors.get('ENERGY');

// List equipment
const equipment = await client.equipment.list({ sector: 'ENERGY' });

// Monitor threats in real-time
client.subscriptions.onThreatEvent({
  sectorId: 'ENERGY',
  onUpdate: (event) => console.log('New threat:', event),
  onError: (error) => console.error('Subscription error:', error)
});
```

---

## FAQ & TROUBLESHOOTING

### 12.1 Common Questions

**Q: What's the difference between REST and GraphQL APIs?**
A: REST provides fixed endpoints for specific resources. GraphQL lets you request exactly the data you need in a single query, reducing over/under-fetching. Use GraphQL for complex queries, REST for simple lookups.

**Q: How often is data updated?**
A: Real-time for subscriptions (milliseconds), 5-minute cache for most queries, 1-hour cache for analytics.

**Q: Can I use API keys for production?**
A: Yes, API keys are production-ready. Use IP whitelisting and rotation for security.

**Q: What's included in "read:sectors" scope?**
A: GET /sectors, GET /sectors/{id}, GET /analytics/sectors, GET /analytics/dependencies

**Q: How do I handle rate limits?**
A: Check X-RateLimit-Remaining header. Implement exponential backoff on 429 responses.

### 12.2 Troubleshooting

**Issue: 401 Unauthorized**
```
Solution:
1. Verify API key is correct and not expired
2. Check Authorization header format: "Bearer TOKEN"
3. Ensure token scope includes required permissions
```

**Issue: 403 Forbidden**
```
Solution:
1. Verify user has required scope (e.g., read:sectors)
2. Check role/permissions in dashboard
3. Contact admin for access upgrade
```

**Issue: 429 Rate Limited**
```
Solution:
1. Check X-RateLimit-Remaining header
2. Implement exponential backoff: wait 2^n seconds
3. Upgrade to higher tier for higher limits
4. Use batch endpoints to reduce request count
```

**Issue: 500 Server Error**
```
Solution:
1. Check API status page: status.aeon-dt.com
2. Retry with exponential backoff
3. Contact support if persists >30 minutes
```

---

## APPENDIX: ENDPOINT REFERENCE TABLE

### All 36+ Endpoints Summary

| Method | Endpoint | Scopes | Rate | Latency | Cache |
|--------|----------|--------|------|---------|-------|
| POST | /auth/login | None | 5/min | 50ms | No |
| POST | /auth/refresh | None | 10/min | 50ms | No |
| POST | /auth/logout | Bearer | No limit | 20ms | No |
| GET | /sectors | read:sectors | 100/min | 100ms | 5m |
| GET | /sectors/{id} | read:sectors | 100/min | 300ms | 5m |
| GET | /sectors/{id}/equipment | read:equipment | 100/min | 400ms | 5m |
| GET | /sectors/{id}/vulnerabilities | read:vulnerabilities | 100/min | 500ms | 1h |
| GET | /analytics/sectors | read:analytics | 100/min | 1s | 1h |
| GET | /analytics/dependencies | read:analytics | 100/min | 800ms | 1h |
| GET | /equipment | read:equipment | 100/min | 400ms | 5m |
| GET | /equipment/{id} | read:equipment | 100/min | 200ms | 5m |
| POST | /equipment | write:equipment | 10/min | 100ms | No |
| PUT | /equipment/{id} | write:equipment | 10/min | 100ms | No |
| DELETE | /equipment/{id} | write:equipment | 10/min | 100ms | No |
| GET | /vulnerabilities | read:vulnerabilities | 100/min | 300ms | 1h |
| GET | /vulnerabilities/{id} | read:vulnerabilities | 100/min | 200ms | 1h |
| GET | /vulnerabilities/{id}/affected | read:vulnerabilities | 100/min | 400ms | 1h |
| POST | /vulnerabilities/register | write:equipment | 10/min | 100ms | No |
| GET | /vulnerabilities/trend | read:analytics | 100/min | 500ms | 1h |
| POST | /vulnerabilities/{id}/mitigations | write:events | 10/min | 100ms | No |
| GET | /events | read:events | 100/min | 300ms | No |
| POST | /events | write:events | 10/min | 100ms | No |
| GET | /events/{id} | read:events | 100/min | 100ms | ∞ |
| GET | /predictions | read:predictions | 100/min | 300ms | 1h |
| GET | /predictions/{id}/forecast | read:predictions | 100/min | 500ms | 1h |
| POST | /predictions/{id}/feedback | write:predictions | 10/min | 100ms | No |
| **GraphQL** | POST | /graphql | Varies | Varies | Varies |
| **WebSocket** | WSS | /graphql | Unlimited | <100ms | Real-time |

**Total Documented Endpoints**: 26 REST + 10+ GraphQL + 4+ Subscriptions = **40+ total**

---

## DOCUMENT INFORMATION

**Version**: 1.0.0
**Created**: 2025-11-25
**Last Updated**: 2025-11-25
**Status**: PRODUCTION READY
**Maintainer**: API Architecture Team
**Review Cycle**: Quarterly
**Next Review**: 2025-12-25

---

**Complete API Documentation Package**:
- ✓ API_OVERVIEW.md (this document): 1,200+ lines - Endpoint catalog & quick start
- ✓ API_GRAPHQL.md: 1,937 lines - GraphQL schema & advanced queries
- ✓ API_AUTH.md: 1,047 lines - Authentication & security architecture
- ✓ API_SECTORS.md: 1,500 lines - Sector-specific API reference
- ✓ API_EQUIPMENT.md: Complete equipment lifecycle documentation
- ✓ API_VULNERABILITIES.md: CVE intelligence & remediation guidance
- ✓ API_EVENTS.md: Event logging & incident tracking
- ✓ API_PREDICTIONS.md: Psychohistory predictions & forecasting
- ✓ API_QUERY.md: Query optimization & performance tuning
- ✓ API_IMPLEMENTATION_GUIDE.md: Backend implementation roadmap

**Total Documentation Package**: 14,000+ lines | 10 comprehensive documents | Production ready

---

*AEON API Documentation - Complete, Production-Ready, Fully Documented*
*Ready for integration by development, DevOps, and operations teams*
