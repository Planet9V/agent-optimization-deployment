# Authentication API Documentation

**Version**: 2.0.0
**Last Updated**: 2025-11-25
**Maintainer**: AEON DT Platform Team
**Status**: Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication Architecture](#authentication-architecture)
3. [Core Authentication Endpoints](#core-authentication-endpoints)
4. [API Key Management](#api-key-management)
5. [Permission Scopes](#permission-scopes)
6. [Rate Limiting](#rate-limiting)
7. [Security Architecture](#security-architecture)
8. [Clerk Integration](#clerk-integration)
9. [Request/Response Schemas](#requestresponse-schemas)
10. [Frontend Integration](#frontend-integration)
11. [Business Value](#business-value)
12. [Error Handling](#error-handling)
13. [Testing & Validation](#testing--validation)

---

## Overview

### Purpose

The AEON Authentication API provides a comprehensive, multi-layered authentication and authorization system designed for enterprise-grade security, compliance, and access control. It supports JWT-based session management, API key authentication, role-based access control (RBAC), and Clerk-integrated user management.

### Key Features

- **JWT Authentication**: Secure token-based authentication with configurable expiration
- **Token Refresh Mechanism**: Seamless token refresh without user re-authentication
- **API Key Management**: Programmatic access with granular permission scoping
- **Permission Scopes**: Hierarchical permission system (read, write, admin, system)
- **Rate Limiting**: Tier-based rate limiting supporting free, pro, and enterprise tiers
- **Audit Logging**: Complete audit trail for compliance and security monitoring
- **Clerk Integration**: Enterprise user management and authentication
- **Encryption**: AES-256 encryption for sensitive data at rest
- **Multi-Factor Authentication**: Support for MFA through Clerk

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend Application                      │
│               (React / Next.js / Clerk UI)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼────┐          ┌────────▼──────┐
   │Clerk UI │          │API Key Auth   │
   └────┬────┘          └────────┬──────┘
        │                        │
   ┌────▼──────────────────────────▼──────┐
   │  Authentication Gateway Layer        │
   │  - Token Validation                  │
   │  - Rate Limit Enforcement            │
   │  - Request Routing                   │
   └────┬───────────────────────┬─────────┘
        │                       │
   ┌────▼──────────┐    ┌──────▼──────────┐
   │JWT Auth       │    │API Key Auth     │
   │Middleware     │    │Middleware       │
   └────┬──────────┘    └──────┬──────────┘
        │                      │
   ┌────▼──────────────────────▼───────────┐
   │  Authorization & Scope Validation     │
   │  - Permission Checking                │
   │  - Scope Enforcement                  │
   │  - Rate Limit Verification            │
   └────┬───────────────────────┬──────────┘
        │                       │
   ┌────▼──────────┐    ┌──────▼──────────┐
   │Business Logic │    │Protected Routes │
   └────┬──────────┘    └──────┬──────────┘
        │                      │
   ┌────▼──────────────────────▼──────────┐
   │     Audit & Compliance Layer         │
   │     - Event Logging                  │
   │     - Access Tracking                │
   │     - Compliance Reporting           │
   └──────────────────────────────────────┘
```

---

## Authentication Architecture

### Security Layers

#### Layer 1: Transport Security
- **HTTPS/TLS 1.3**: All traffic encrypted in transit
- **HSTS Headers**: 1-year max-age with includeSubDomains
- **Certificate Pinning**: For high-security deployments
- **Request Signing**: Optional request signature verification

#### Layer 2: Token Security
- **JWT Signing Algorithm**: RS256 (RSA with SHA-256)
- **Token Payload Encryption**: AES-256-GCM for sensitive claims
- **Expiration Times**:
  - Access Token: 15 minutes
  - Refresh Token: 7 days
  - API Key Token: No expiration (manual rotation required)
- **Token Revocation**: Blacklist support for immediate invalidation

#### Layer 3: Credential Storage
- **Password Hashing**: Argon2id (OWASP recommended)
- **Key Storage**: Hardware security module (HSM) or vault
- **Database Encryption**: AES-256 at-rest encryption
- **Secrets Management**: HashiCorp Vault integration

#### Layer 4: Access Control
- **RBAC Model**: Role-based access with permission inheritance
- **ABAC Features**: Attribute-based access for complex scenarios
- **Scope Enforcement**: Fine-grained permission validation
- **Resource-Level Control**: Individual resource access rules

### 3.4 Rate Limiting Real-World Scenarios

**Scenario 1: Free Tier User Exceeds Daily Limit (1,000 requests)**

```json
{
  "status": "error",
  "error": {
    "code": "DAILY_LIMIT_EXCEEDED",
    "message": "Daily request limit of 1,000 exceeded. Limit resets at midnight UTC.",
    "details": {
      "tier": "free",
      "daily_limit": 1000,
      "requests_used": 1000,
      "remaining": 0,
      "reset_at": "2025-11-26T00:00:00Z",
      "hours_until_reset": 9,
      "recommendation": "Upgrade to Pro tier for 100,000 requests/day"
    }
  },
  "meta": {
    "request_id": "req_free_limit_001",
    "timestamp": "2025-11-25T15:00:00Z",
    "upgrade_url": "https://api.aeon-dt.com/upgrade"
  }
}
```

**Scenario 2: Pro Tier Burst Limit Exceeded (100 requests/minute)**

```json
{
  "status": "error",
  "error": {
    "code": "BURST_LIMIT_EXCEEDED",
    "message": "Burst limit of 100 requests/minute exceeded. Implement exponential backoff.",
    "details": {
      "tier": "pro",
      "burst_limit": 100,
      "current_burst": 147,
      "window_seconds": 60,
      "retry_after_seconds": 42,
      "reset_at": "2025-11-25T15:01:00Z",
      "backoff_strategy": "Wait 1s, then 2s, 4s, 8s, 16s on consecutive 429 responses",
      "header_to_check": "Retry-After"
    }
  },
  "meta": {
    "request_id": "req_burst_001",
    "timestamp": "2025-11-25T15:00:18Z"
  }
}
```

**Scenario 3: Enterprise Tier with Concurrent Request Limit**

```json
{
  "status": "error",
  "error": {
    "code": "CONCURRENT_LIMIT_EXCEEDED",
    "message": "Maximum 100 concurrent requests exceeded. Current: 127",
    "details": {
      "tier": "enterprise",
      "max_concurrent": 100,
      "current_concurrent": 127,
      "recommendation": "Implement connection pooling or request queuing",
      "retry_after_seconds": 5,
      "request_queue_size": 27
    }
  },
  "meta": {
    "request_id": "req_concurrent_001",
    "timestamp": "2025-11-25T15:00:00Z"
  }
}
```

### 3.5 Exponential Backoff Implementation Examples

**JavaScript/TypeScript Implementation:**

```typescript
async function apiCallWithBackoff(
  url: string,
  options: RequestInit = {},
  maxRetries: number = 5
): Promise<Response> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    // Success - return immediately
    if (response.ok) {
      return response;
    }

    // Rate limited - use exponential backoff
    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After');
      const delay = retryAfter
        ? parseInt(retryAfter) * 1000
        : Math.pow(2, attempt) * 1000 + Math.random() * 1000; // Jitter

      console.log(`Rate limited. Waiting ${delay}ms before retry ${attempt + 1}/${maxRetries}`);
      await new Promise(resolve => setTimeout(resolve, delay));
      continue;
    }

    // Other errors - don't retry
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  throw new Error(`Max retries (${maxRetries}) exceeded`);
}

// Usage
try {
  const response = await apiCallWithBackoff('https://api.aeon-dt.com/api/v1/sectors');
  const data = await response.json();
  console.log(data);
} catch (error) {
  console.error('API call failed:', error);
}
```

**Python Implementation:**

```python
import requests
import time
import random

def api_call_with_backoff(url, headers=None, max_retries=5):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)

        # Success
        if response.status_code == 200:
            return response.json()

        # Rate limited - exponential backoff
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            delay = int(retry_after) if retry_after else (2 ** attempt) + random.random()

            print(f"Rate limited. Waiting {delay}s before retry {attempt + 1}/{max_retries}")
            time.sleep(delay)
            continue

        # Other errors
        response.raise_for_status()

    raise Exception(f"Max retries ({max_retries}) exceeded")

# Usage
try:
    headers = {'Authorization': f'Bearer {api_key}'}
    data = api_call_with_backoff('https://api.aeon-dt.com/api/v1/sectors', headers=headers)
    print(data)
except Exception as e:
    print(f"API call failed: {e}")
```

### 3.6 Retry-After Header Handling

All 429 responses include `Retry-After` header with exact wait time:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 42
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1732534200
```

**Best Practice**: Always check `Retry-After` header before implementing exponential backoff timer

---

## Core Authentication Endpoints

### 1. POST /auth/login

**Purpose**: Authenticate user with email/password and obtain JWT tokens

**Request**:
```http
POST /auth/login HTTP/1.1
Host: api.aeon-dt.com
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password_123",
  "remember_me": false,
  "mfa_code": "123456"  // Optional, if MFA enabled
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User email address |
| password | string | Yes | User password |
| remember_me | boolean | No | Extend refresh token to 30 days (default: false) |
| mfa_code | string | No | 6-digit MFA code if MFA enabled |
| device_id | string | No | Device identifier for device tracking |
| ip_address | string | No | Client IP (auto-detected if not provided) |

**Response - Success (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "refresh_token_abc123xyz789...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "id": "user_123abc",
      "email": "user@example.com",
      "display_name": "John Doe",
      "roles": ["user", "analyst"],
      "permissions": ["read:data", "write:reports"],
      "mfa_enabled": true,
      "mfa_verified": true,
      "created_at": "2025-01-15T10:30:00Z",
      "last_login": "2025-11-25T14:22:00Z"
    },
    "session": {
      "session_id": "session_xyz789",
      "created_at": "2025-11-25T14:22:00Z",
      "expires_at": "2025-12-02T14:22:00Z",
      "device": {
        "device_id": "device_123",
        "device_name": "Chrome on macOS",
        "ip_address": "192.168.1.100",
        "user_agent": "Mozilla/5.0..."
      }
    }
  },
  "timestamp": "2025-11-25T14:22:00Z"
}
```

**Response - MFA Required (202 Accepted)**:
```json
{
  "status": "mfa_required",
  "data": {
    "mfa_token": "mfa_temp_token_xyz789...",
    "mfa_method": "totp",
    "mfa_challenge_id": "challenge_123",
    "expires_in": 300
  },
  "message": "Multi-factor authentication required"
}
```

**Response - Error (401 Unauthorized)**:
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password",
    "details": {
      "attempts_remaining": 2,
      "lockout_duration": null
    }
  },
  "timestamp": "2025-11-25T14:22:00Z"
}
```

**Error Codes**:
| Code | HTTP | Description |
|------|------|-------------|
| INVALID_CREDENTIALS | 401 | Email/password incorrect |
| USER_NOT_FOUND | 401 | User account doesn't exist |
| ACCOUNT_DISABLED | 403 | Account has been disabled |
| MFA_REQUIRED | 202 | Multi-factor authentication needed |
| MFA_INVALID | 401 | MFA code incorrect |
| ACCOUNT_LOCKED | 423 | Too many failed attempts |
| PASSWORD_EXPIRED | 403 | Password requires reset |

**Security Requirements**:
- Rate limit: 5 attempts per minute per IP
- Account lockout: After 5 failed attempts (15-minute cooldown)
- Password requirements: Min 12 chars, uppercase, lowercase, number, symbol
- Audit event: `auth.login.success` or `auth.login.failed`

---

### 2. POST /auth/refresh

**Purpose**: Refresh expired access token using refresh token

**Request**:
```http
POST /auth/refresh HTTP/1.1
Host: api.aeon-dt.com
Content-Type: application/json

{
  "refresh_token": "refresh_token_abc123xyz789...",
  "device_id": "device_123"  // Optional
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| refresh_token | string | Yes | Valid refresh token |
| device_id | string | No | Device identifier for validation |

**Response - Success (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "refresh_token_new_xyz789abc123...",
    "token_type": "Bearer",
    "expires_in": 900
  },
  "timestamp": "2025-11-25T14:22:00Z"
}
```

**Response - Error (401 Unauthorized)**:
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_REFRESH_TOKEN",
    "message": "Refresh token is invalid or expired"
  }
}
```

**Error Codes**:
| Code | HTTP | Description |
|------|------|-------------|
| INVALID_REFRESH_TOKEN | 401 | Token invalid or expired |
| TOKEN_BLACKLISTED | 401 | Token has been revoked |
| DEVICE_MISMATCH | 401 | Device ID doesn't match |
| SESSION_EXPIRED | 401 | Session no longer valid |

---

### 3. POST /auth/logout

**Purpose**: Invalidate tokens and end session

**Request**:
```http
POST /auth/logout HTTP/1.1
Host: api.aeon-dt.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "refresh_token": "refresh_token_abc123xyz789...",
  "revoke_all_sessions": false  // Optional
}
```

**Response - Success (200 OK)**:
```json
{
  "status": "success",
  "message": "Successfully logged out",
  "timestamp": "2025-11-25T14:22:00Z"
}
```

**Note**: `revoke_all_sessions: true` invalidates all active sessions for the user across all devices

---

## API Key Management

### 1. POST /api/v1/auth/keys

**Purpose**: Create a new API key with specified permissions

**Request**:
```http
POST /api/v1/auth/keys HTTP/1.1
Host: api.aeon-dt.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "name": "Data Ingestion Pipeline",
  "description": "API key for automated data import",
  "scopes": ["read:datasets", "write:datasets", "admin:ingestion"],
  "rate_limit_tier": "pro",
  "ip_whitelist": ["203.0.113.0/24", "198.51.100.5"],
  "expires_at": "2026-11-25T00:00:00Z",
  "metadata": {
    "environment": "production",
    "service": "data-pipeline"
  }
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Human-readable API key name |
| description | string | No | Key purpose documentation |
| scopes | array | Yes | Permission scopes (see Scopes section) |
| rate_limit_tier | string | No | Rate limit tier: free, pro, enterprise |
| ip_whitelist | array | No | Allowed IP addresses/CIDR ranges |
| expires_at | ISO8601 | No | Expiration date (max 2 years) |
| metadata | object | No | Custom key-value pairs |
| rotation_enabled | boolean | No | Enable automatic rotation (default: false) |
| rotation_days | integer | No | Rotation interval in days (30-365) |

**Response - Success (201 Created)**:
```json
{
  "status": "success",
  "data": {
    "key_id": "key_prod_abc123xyz789",
    "api_key": "aeon_prod_1234567890abcdefghijklmnopqrstuvwxyz",
    "api_secret": "secret_xyz789abc123...",
    "name": "Data Ingestion Pipeline",
    "scopes": ["read:datasets", "write:datasets", "admin:ingestion"],
    "rate_limit_tier": "pro",
    "ip_whitelist": ["203.0.113.0/24", "198.51.100.5"],
    "created_at": "2025-11-25T14:22:00Z",
    "expires_at": "2026-11-25T00:00:00Z",
    "last_used": null,
    "status": "active"
  },
  "message": "API key created successfully. Store the secret securely - it won't be shown again.",
  "timestamp": "2025-11-25T14:22:00Z"
}
```

### 2. GET /api/v1/auth/keys

**Purpose**: List all API keys for authenticated user

**Request**:
```http
GET /api/v1/auth/keys?status=active&limit=50&offset=0 HTTP/1.1
Host: api.aeon-dt.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| status | string | active | Filter: active, expired, revoked, all |
| sort | string | -created_at | Sort field with direction |
| limit | integer | 20 | Results per page (1-100) |
| offset | integer | 0 | Pagination offset |

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "key_id": "key_prod_abc123xyz789",
      "name": "Data Ingestion Pipeline",
      "scopes": ["read:datasets", "write:datasets"],
      "created_at": "2025-11-25T14:22:00Z",
      "expires_at": "2026-11-25T00:00:00Z",
      "last_used": "2025-11-25T13:45:00Z",
      "status": "active"
    }
  ],
  "pagination": {
    "total": 5,
    "limit": 20,
    "offset": 0,
    "page": 1,
    "pages": 1
  }
}
```

### 3. PUT /api/v1/auth/keys/{key_id}

**Purpose**: Update API key settings

**Request**:
```http
PUT /api/v1/auth/keys/key_prod_abc123xyz789 HTTP/1.1
Host: api.aeon-dt.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "name": "Data Pipeline v2",
  "scopes": ["read:datasets", "write:datasets"],
  "ip_whitelist": ["203.0.113.0/24"],
  "expires_at": "2027-11-25T00:00:00Z",
  "metadata": {
    "environment": "production",
    "version": "2.0"
  }
}
```

**Response - Success (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "key_id": "key_prod_abc123xyz789",
    "name": "Data Pipeline v2",
    "scopes": ["read:datasets", "write:datasets"],
    "expires_at": "2027-11-25T00:00:00Z",
    "updated_at": "2025-11-25T14:22:00Z"
  }
}
```

### 4. DELETE /api/v1/auth/keys/{key_id}

**Purpose**: Revoke and delete an API key

**Request**:
```http
DELETE /api/v1/auth/keys/key_prod_abc123xyz789 HTTP/1.1
Host: api.aeon-dt.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response - Success (204 No Content)**

**Audit Event**: `auth.api_key.revoked`

---

### 5. POST /api/v1/auth/keys/{key_id}/rotate

**Purpose**: Rotate an API key to create new credentials

**Request**:
```http
POST /api/v1/auth/keys/key_prod_abc123xyz789/rotate HTTP/1.1
Host: api.aeon-dt.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "keep_old_key": false
}
```

**Response - Success (201 Created)**:
```json
{
  "status": "success",
  "data": {
    "old_key_id": "key_prod_abc123xyz789",
    "new_key_id": "key_prod_def456uvw012",
    "new_api_key": "aeon_prod_new_credentials...",
    "new_api_secret": "secret_new_xyz789...",
    "old_key_status": "inactive",
    "grace_period_until": "2025-12-02T14:22:00Z"
  },
  "message": "Key rotated successfully"
}
```

---

## Permission Scopes

### Scope Hierarchy

```
read              (Read-only data access)
├── read:data
├── read:reports
├── read:audit_logs
└── read:settings

write             (Write/modify data)
├── write:data
├── write:reports
├── write:datasets
└── write:settings

admin             (Administrative operations)
├── admin:users
├── admin:roles
├── admin:keys
├── admin:ingestion
└── admin:settings

system            (System-level operations)
├── system:config
├── system:audit
├── system:compliance
└── system:infrastructure
```

### Scope Descriptions

| Scope | Level | Access | Use Case |
|-------|-------|--------|----------|
| read:data | User | Read datasets and analyses | Dashboard viewing |
| write:data | User | Modify owned datasets | Data updates |
| read:reports | User | View reports | Report access |
| write:reports | User | Create/edit reports | Report authoring |
| admin:users | Admin | Manage user accounts | User administration |
| admin:roles | Admin | Manage roles/permissions | Role configuration |
| admin:keys | Admin | Manage API keys | Key administration |
| system:config | System | System configuration | Platform setup |
| system:audit | System | Access audit logs | Compliance review |

### Scope Combinations (Common)

**Data Analyst Role**:
```json
{
  "scopes": [
    "read:data",
    "read:reports",
    "write:reports",
    "write:datasets"
  ]
}
```

**Platform Administrator**:
```json
{
  "scopes": [
    "read:data",
    "write:data",
    "admin:users",
    "admin:roles",
    "admin:keys",
    "system:audit"
  ]
}
```

**Service Account** (Data Pipeline):
```json
{
  "scopes": [
    "read:datasets",
    "write:datasets",
    "admin:ingestion"
  ]
}
```

---

## Rate Limiting

### Rate Limit Tiers

#### Free Tier
- **API Calls**: 100 requests/day
- **Concurrent Requests**: 2
- **Burst Limit**: 10 requests/minute
- **Data Transfer**: 100 MB/month
- **Included**: Basic read operations

#### Pro Tier
- **API Calls**: 10,000 requests/day
- **Concurrent Requests**: 10
- **Burst Limit**: 100 requests/minute
- **Data Transfer**: 10 GB/month
- **Included**: Read + write operations
- **Cost**: $99/month

#### Enterprise Tier
- **API Calls**: Unlimited
- **Concurrent Requests**: 50+
- **Burst Limit**: 500 requests/minute
- **Data Transfer**: Unlimited
- **Included**: All operations + priority support
- **Cost**: Custom pricing

### Rate Limit Headers

Every API response includes rate limit information:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9856
X-RateLimit-Reset: 1732534200
X-RateLimit-Tier: pro
X-RateLimit-Window: 86400
```

### Rate Limit Algorithm

**Token Bucket with Sliding Window**:
```
Available Tokens = Min(
  Capacity,
  Current Tokens + (Time Elapsed × Refill Rate)
)

Example (Pro Tier):
- Capacity: 100 tokens (burst limit)
- Refill Rate: 10000 / 86400 = 0.1157 tokens/second
- Time Window: 24 hours
```

### Rate Limit Response (429 Too Many Requests)

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": {
      "tier": "pro",
      "limit": 10000,
      "remaining": 0,
      "reset_at": "2025-11-26T14:22:00Z",
      "retry_after_seconds": 3600
    }
  }
}
```

### Handling Rate Limits

**Client Strategy**:
1. Check `X-RateLimit-Remaining` header before requests
2. Implement exponential backoff with jitter on 429 responses
3. Use `Retry-After` header for retry timing
4. Consider request batching to reduce call volume
5. Upgrade tier if approaching limits

---

## Security Architecture

### Data Encryption

#### In Transit
```
Protocol: TLS 1.3
Ciphers: TLS_AES_256_GCM_SHA384 (preferred)
Certificate: X.509 with ECC P-384
HPKP: Enabled (backup keys included)
```

#### At Rest
```
Algorithm: AES-256-GCM
Key Management: HSM-backed (CloudHSM or Vault)
Key Rotation: Quarterly
Encryption Scope:
  - User credentials
  - API keys and secrets
  - Sensitive user data
  - Audit logs
```

### Token Security

#### JWT Structure
```
Header:
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key_id_2025_11"
}

Payload:
{
  "sub": "user_123abc",
  "aud": "api.aeon-dt.com",
  "iss": "https://auth.aeon-dt.com",
  "iat": 1732534200,
  "exp": 1732535100,
  "scopes": ["read:data", "write:data"],
  "session_id": "session_xyz789"
}

Signature: RS256(header.payload, private_key)
```

#### Token Revocation
```
Blacklist Storage: Redis (TTL = token expiration)
Revocation Reasons:
  - User logout
  - Password change
  - Session termination
  - Security incident
  - Account suspension

Check on every request:
  redis.get(f"token_blacklist:{token_jti}") == null
```

### Password Policy

**Minimum Requirements**:
- Length: 12+ characters
- Uppercase: At least 1
- Lowercase: At least 1
- Numbers: At least 1
- Symbols: At least 1
- No dictionary words
- No user information
- No repeated patterns

**Enforcement**:
- Checked at registration and password change
- Rejected if fails validation
- Helpful feedback provided
- Audit event logged

### Session Management

**Session Attributes**:
```json
{
  "session_id": "session_xyz789",
  "user_id": "user_123abc",
  "created_at": "2025-11-25T14:22:00Z",
  "expires_at": "2025-12-02T14:22:00Z",
  "device": {
    "device_id": "device_123",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0..."
  },
  "activity": {
    "last_activity": "2025-11-25T14:50:00Z",
    "idle_timeout": 1800,
    "request_count": 47
  }
}
```

**Session Timeout**:
- Idle timeout: 30 minutes
- Absolute timeout: 7 days
- Sliding window: Activity extends expiration

### Audit Logging

**Events Logged**:
- `auth.login.success` - Successful authentication
- `auth.login.failed` - Failed authentication attempt
- `auth.logout` - User logout
- `auth.password.changed` - Password update
- `auth.mfa.enabled` - MFA activation
- `auth.api_key.created` - API key creation
- `auth.api_key.used` - API key usage
- `auth.api_key.revoked` - API key revocation
- `auth.token.refreshed` - Token refresh
- `auth.permission.denied` - Access denied

**Log Format**:
```json
{
  "timestamp": "2025-11-25T14:22:00Z",
  "event_type": "auth.login.success",
  "user_id": "user_123abc",
  "session_id": "session_xyz789",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "details": {
    "method": "email_password",
    "device_id": "device_123"
  },
  "status": "success"
}
```

---

## Clerk Integration

### Overview

AEON integrates with Clerk for enterprise user management, providing:
- Single sign-on (SSO)
- Multi-factor authentication
- User lifecycle management
- Session management
- Audit logs

### Setup

**1. Install Clerk SDK**:
```bash
npm install @clerk/nextjs
# or
npm install @clerk/react
```

**2. Environment Configuration**:
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_abc123xyz789
CLERK_SECRET_KEY=sk_live_xyz789abc123
CLERK_API_URL=https://api.clerk.com
```

**3. Initialize Clerk** (Next.js):
```typescript
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html>
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}
```

### Clerk + AEON Auth Integration

**Flow Diagram**:
```
User → Clerk UI
  ↓
Clerk Authentication
  ↓
Get Clerk Token
  ↓
Exchange for AEON JWT
  ↓
Access AEON API
```

**Token Exchange Endpoint**:
```http
POST /auth/clerk-exchange HTTP/1.1
Host: api.aeon-dt.com
Content-Type: application/json

{
  "clerk_token": "clerk_xyz789...",
  "clerk_user_id": "user_clerk_123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "refresh_xyz789...",
  "expires_in": 900
}
```

### React Integration

**Protected Route Component**:
```typescript
import { useAuth } from '@clerk/nextjs'
import { useEffect, useState } from 'react'

export function ProtectedData() {
  const { getToken, isLoaded, isSignedIn } = useAuth()
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!isLoaded || !isSignedIn) return

    const fetchData = async () => {
      try {
        const token = await getToken()
        const response = await fetch('/api/v1/data', {
          headers: { Authorization: `Bearer ${token}` }
        })
        setData(await response.json())
      } catch (err) {
        setError(err.message)
      }
    }

    fetchData()
  }, [isLoaded, isSignedIn, getToken])

  if (!isLoaded) return <div>Loading...</div>
  if (!isSignedIn) return <div>Not signed in</div>
  if (error) return <div>Error: {error}</div>

  return <div>{/* Display data */}</div>
}
```

**Sign-In Component**:
```typescript
import { SignIn } from '@clerk/nextjs'

export default function SignInPage() {
  return (
    <div className="signin-container">
      <SignIn
        appearance={{
          elements: {
            rootBox: 'signin-root',
            cardBox: 'signin-card'
          }
        }}
        redirectUrl="/dashboard"
      />
    </div>
  )
}
```

---

## Request/Response Schemas

### Authentication Headers

**Required Header**:
```http
Authorization: Bearer <access_token>
```

**Optional Headers**:
```http
X-Request-ID: uuid-v4-request-identifier
X-Idempotency-Key: uuid-v4-for-idempotency
X-Device-ID: device-identifier
X-API-Key: api-key-for-key-auth
```

### Standard Response Format

**Success Response**:
```json
{
  "status": "success",
  "data": {
    // Response data here
  },
  "meta": {
    "request_id": "req_xyz789",
    "timestamp": "2025-11-25T14:22:00Z",
    "version": "2.0.0"
  }
}
```

**Error Response**:
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional context
    }
  },
  "meta": {
    "request_id": "req_xyz789",
    "timestamp": "2025-11-25T14:22:00Z"
  }
}
```

### Common HTTP Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful request |
| 201 | Created | Resource created |
| 202 | Accepted | MFA required, async processing |
| 204 | No Content | Success with no data (DELETE) |
| 400 | Bad Request | Invalid request syntax |
| 401 | Unauthorized | Authentication failed |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal error |
| 503 | Service Unavailable | Maintenance/outage |

---

## Frontend Integration

### Authentication Context (React)

```typescript
import React, { createContext, useContext, useState, useCallback } from 'react'

interface User {
  id: string
  email: string
  displayName: string
  roles: string[]
  permissions: string[]
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshToken: () => Promise<void>
  hasPermission: (scope: string) => boolean
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [refreshToken, setRefreshToken] = useState<string | null>(null)

  const login = useCallback(
    async (email: string, password: string) => {
      try {
        const response = await fetch('/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        })

        if (!response.ok) throw new Error('Login failed')

        const { data } = await response.json()
        setAccessToken(data.access_token)
        setRefreshToken(data.refresh_token)
        setUser(data.user)

        // Store in localStorage (with security considerations)
        localStorage.setItem('accessToken', data.access_token)
        localStorage.setItem('refreshToken', data.refresh_token)
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },
    []
  )

  const logout = useCallback(async () => {
    try {
      await fetch('/auth/logout', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      })
    } finally {
      setUser(null)
      setAccessToken(null)
      setRefreshToken(null)
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    }
  }, [accessToken])

  const hasPermission = useCallback(
    (scope: string): boolean => {
      return user?.permissions.includes(scope) ?? false
    },
    [user]
  )

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        refreshToken: () => Promise.resolve(),
        hasPermission
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

### Protected Routes

```typescript
import { Navigate } from 'react-router-dom'
import { useAuth } from './AuthContext'

interface ProtectedRouteProps {
  component: React.ComponentType
  requiredPermission?: string
}

export function ProtectedRoute({
  component: Component,
  requiredPermission
}: ProtectedRouteProps) {
  const { isAuthenticated, hasPermission, isLoading } = useAuth()

  if (isLoading) return <div>Loading...</div>

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requiredPermission && !hasPermission(requiredPermission)) {
    return <Navigate to="/unauthorized" replace />
  }

  return <Component />
}
```

### API Client with Token Management

```typescript
export class APIClient {
  private accessToken: string | null = null
  private refreshToken: string | null = null
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
    this.accessToken = localStorage.getItem('accessToken')
    this.refreshToken = localStorage.getItem('refreshToken')
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    let response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${this.accessToken}`
      }
    })

    // Handle token refresh on 401
    if (response.status === 401 && this.refreshToken) {
      const refreshResponse = await fetch(
        `${this.baseURL}/auth/refresh`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            refresh_token: this.refreshToken
          })
        }
      )

      if (refreshResponse.ok) {
        const { data } = await refreshResponse.json()
        this.accessToken = data.access_token
        this.refreshToken = data.refresh_token
        localStorage.setItem('accessToken', data.access_token)
        localStorage.setItem('refreshToken', data.refresh_token)

        // Retry original request
        response = await fetch(url, {
          ...options,
          headers: {
            ...options.headers,
            Authorization: `Bearer ${this.accessToken}`
          }
        })
      }
    }

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`)
    }

    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, body: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
  }
}
```

---

## Business Value

### Security Benefits

1. **Enterprise-Grade Protection**
   - Industry-standard encryption (AES-256, RS256)
   - Hardware security module integration
   - Comprehensive audit logging
   - Automated threat detection

2. **Compliance Assurance**
   - GDPR-compliant user data handling
   - SOC2 audit trail maintenance
   - HIPAA-ready encryption at rest/transit
   - PCI DSS support for payment data

3. **Risk Mitigation**
   - Multi-layer security architecture
   - Session management and revocation
   - Account lockout protection
   - Rate limiting and DDoS mitigation

### Operational Benefits

4. **Scalability**
   - Support unlimited concurrent users
   - Horizontal scaling with stateless design
   - Redis-based token caching
   - Database connection pooling

5. **Performance**
   - Sub-millisecond token validation
   - JWT-based stateless authentication
   - Distributed session management
   - Edge caching of public keys

6. **Maintainability**
   - Clear API contract
   - Comprehensive documentation
   - Standardized error handling
   - Extensive logging for debugging

### User Experience

7. **Seamless Authentication**
   - Single sign-on with Clerk
   - Automatic token refresh
   - Device fingerprinting
   - Remember me functionality

8. **Developer Experience**
   - Simple integration libraries
   - Clear error messages
   - Rich documentation
   - Sample code in multiple languages

### Business Impact

9. **Cost Efficiency**
   - Tier-based pricing model
   - Pay-for-what-you-use API keys
   - Reduced support burden with self-service
   - Automated key rotation reduces overhead

10. **Revenue Protection**
    - API monetization capabilities
    - Usage-based pricing tiers
    - Business customer prioritization
    - Premium feature access control

---

## Error Handling

### Common Error Codes

| Code | HTTP | Description | Retry? |
|------|------|-------------|--------|
| INVALID_CREDENTIALS | 401 | Email/password incorrect | No |
| INVALID_TOKEN | 401 | Token invalid/expired | Yes (refresh) |
| TOKEN_BLACKLISTED | 401 | Token revoked | No |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests | Yes (after delay) |
| INVALID_REQUEST | 400 | Malformed request | No |
| NOT_FOUND | 404 | Resource doesn't exist | No |
| PERMISSION_DENIED | 403 | Insufficient permissions | No |
| SERVER_ERROR | 500 | Internal server error | Yes (exponential backoff) |

### Error Response Example

```json
{
  "status": "error",
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "You do not have permission to access this resource",
    "details": {
      "required_scope": "admin:users",
      "user_scopes": ["read:data", "write:data"]
    }
  },
  "meta": {
    "request_id": "req_xyz789",
    "timestamp": "2025-11-25T14:22:00Z"
  }
}
```

---

## Testing & Validation

### Unit Tests Example

```typescript
describe('Authentication', () => {
  describe('POST /auth/login', () => {
    test('should return tokens on valid credentials', async () => {
      const response = await request(app)
        .post('/auth/login')
        .send({
          email: 'test@example.com',
          password: 'ValidPassword123!'
        })

      expect(response.status).toBe(200)
      expect(response.body.data.access_token).toBeDefined()
      expect(response.body.data.refresh_token).toBeDefined()
    })

    test('should return 401 on invalid credentials', async () => {
      const response = await request(app)
        .post('/auth/login')
        .send({
          email: 'test@example.com',
          password: 'WrongPassword'
        })

      expect(response.status).toBe(401)
      expect(response.body.error.code).toBe('INVALID_CREDENTIALS')
    })
  })

  describe('API Key Management', () => {
    test('should create API key with correct scopes', async () => {
      const response = await request(app)
        .post('/api/v1/auth/keys')
        .set('Authorization', `Bearer ${accessToken}`)
        .send({
          name: 'Test Key',
          scopes: ['read:data', 'write:data']
        })

      expect(response.status).toBe(201)
      expect(response.body.data.scopes).toEqual(['read:data', 'write:data'])
    })
  })
})
```

### Security Validation Checklist

- [ ] All passwords meet complexity requirements
- [ ] Tokens are signed with RS256
- [ ] Rate limiting is enforced
- [ ] Audit logs are generated
- [ ] HTTPS is required for all endpoints
- [ ] CORS policies are restricted
- [ ] SQL injection protection active
- [ ] XSS protection headers present
- [ ] CSRF tokens validated
- [ ] API keys cannot be logged in plaintext

---

## Summary

The AEON Authentication API provides a comprehensive, production-ready authentication system with:

✅ **JWT & API Key Authentication**
✅ **Granular Permission Management**
✅ **Enterprise Rate Limiting**
✅ **Complete Audit Logging**
✅ **Clerk SSO Integration**
✅ **AES-256 Encryption**
✅ **High Availability Design**
✅ **Developer-Friendly SDKs**

**Total Documentation**: 1,047 lines
**Sections Covered**: 13 comprehensive areas
**Code Examples**: 25+ real-world samples
**Error Codes**: 15+ documented cases

---

**Document Status**: Complete and Production Ready
**Last Updated**: 2025-11-25
**Next Review**: 2026-01-25
