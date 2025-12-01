# AEON Digital Twin: Technical Specifications

**File**: 01_TECHNICAL_SPECS.md
**Created**: 2025-11-12 05:45:00 UTC
**Modified**: 2025-11-12 05:45:00 UTC
**Version**: 1.0.0
**Author**: AEON Development Team
**Purpose**: Comprehensive technical specifications for AEON Digital Twin implementation
**Status**: ACTIVE - AUTHORITATIVE TECHNICAL REFERENCE

**References**:
- Constitution: `/00_AEON_CONSTITUTION.md`
- Architecture: `/01_ARCHITECTURE/01_COMPREHENSIVE_ARCHITECTURE.md`
- PRD: `/02_REQUIREMENTS/01_PRODUCT_REQUIREMENTS.md`

---

## Table of Contents

1. [API Specifications](#section-1-api-specifications)
2. [Database Schemas](#section-2-database-schemas)
3. [Data Models and Classes](#section-3-data-models-and-classes)
4. [Integration Specifications](#section-4-integration-specifications)
5. [Algorithm Specifications](#section-5-algorithm-specifications)
6. [Performance Specifications](#section-6-performance-specifications)
7. [Security Specifications](#section-7-security-specifications)
8. [Deployment Specifications](#section-8-deployment-specifications)
9. [Testing Specifications](#section-9-testing-specifications)
10. [Monitoring Specifications](#section-10-monitoring-specifications)

---

## Section 1: API Specifications

### 1.1 RESTful API Overview

**Base URL**: `https://api.aeon-dt.com/v1`
**Authentication**: Bearer JWT tokens (Clerk-issued)
**Content-Type**: `application/json`
**Rate Limits**: 10,000 requests/hour per API key

**OpenAPI Version**: 3.0.3
**Specification File**: `/backend/openapi.yaml`

### 1.2 Core Endpoints

#### 1.2.1 CVE Scoring Endpoint

**Endpoint**: `POST /api/v1/score_cve`

**Description**: Score a single CVE using Bayesian probabilistic attack chain analysis

**Request**:
```json
{
  "cve_id": "CVE-2024-1234",
  "customer_context": {
    "industry_sector": "healthcare",
    "equipment_types": ["windows_server", "linux_workstation"],
    "geographic_region": "north_america"
  },
  "options": {
    "monte_carlo_samples": 10000,
    "confidence_level": 0.95,
    "include_chains": true
  }
}
```

**Response** (200 OK):
```json
{
  "cve_id": "CVE-2024-1234",
  "overall_probability": 0.78,
  "confidence_interval": {
    "lower": 0.72,
    "upper": 0.84,
    "level": 0.95
  },
  "primary_tactic": {
    "id": "TA0002",
    "name": "Execution",
    "probability": 0.65
  },
  "chains": [
    {
      "path": ["CVE-2024-1234", "CWE-79", "CAPEC-63", "T1059", "TA0002"],
      "probability": 0.45,
      "edge_probabilities": [0.95, 0.80, 0.75, 0.85]
    },
    {
      "path": ["CVE-2024-1234", "CWE-79", "CAPEC-18", "T1059", "TA0002"],
      "probability": 0.33,
      "edge_probabilities": [0.95, 0.60, 0.70, 0.85]
    }
  ],
  "customer_modifier": 1.2,
  "data_quality": {
    "chain_completeness": 0.85,
    "data_freshness_days": 2,
    "cwe_confidence": 0.95
  },
  "execution_time_ms": 1847,
  "computed_at": "2025-11-12T05:45:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid CVE ID format
  ```json
  {"error": "Invalid CVE ID", "detail": "CVE ID must match CVE-YYYY-NNNNN"}
  ```
- `404 Not Found`: CVE not in database
  ```json
  {"error": "CVE not found", "cve_id": "CVE-2024-9999"}
  ```
- `429 Too Many Requests`: Rate limit exceeded
  ```json
  {"error": "Rate limit exceeded", "retry_after_seconds": 3600}
  ```
- `500 Internal Server Error`: Scoring failure
  ```json
  {"error": "Scoring failed", "detail": "Neo4j connection timeout"}
  ```

**Performance Requirements**:
- p50 latency: < 1 second
- p99 latency: < 2 seconds
- Timeout: 5 seconds

**TASKMASTER Reference**: TASK-2025-11-12-013

---

#### 1.2.2 Batch CVE Scoring Endpoint

**Endpoint**: `POST /api/v1/score_batch`

**Description**: Score multiple CVEs in parallel (up to 1,000 per request)

**Request**:
```json
{
  "cve_ids": ["CVE-2024-1", "CVE-2024-2", "CVE-2024-3"],
  "customer_context": {
    "industry_sector": "finance",
    "equipment_types": ["linux_server"]
  },
  "options": {
    "parallel_workers": 8,
    "monte_carlo_samples": 5000,
    "include_chains": false
  }
}
```

**Response** (200 OK):
```json
{
  "total_cves": 3,
  "successful": 3,
  "failed": 0,
  "execution_time_ms": 4523,
  "results": [
    {
      "cve_id": "CVE-2024-1",
      "overall_probability": 0.82,
      "confidence_interval": {"lower": 0.78, "upper": 0.86},
      "primary_tactic": {"id": "TA0001", "name": "Initial Access"}
    },
    {
      "cve_id": "CVE-2024-2",
      "overall_probability": 0.65,
      "confidence_interval": {"lower": 0.60, "upper": 0.70},
      "primary_tactic": {"id": "TA0006", "name": "Credential Access"}
    },
    {
      "cve_id": "CVE-2024-3",
      "overall_probability": 0.43,
      "confidence_interval": {"lower": 0.38, "upper": 0.48},
      "primary_tactic": {"id": "TA0003", "name": "Persistence"}
    }
  ],
  "errors": []
}
```

**Performance Requirements**:
- 1,000 CVEs in < 60 seconds
- Parallel workers: 8 (configurable)

---

#### 1.2.3 Equipment Import Endpoint

**Endpoint**: `POST /api/v1/equipment/import`

**Description**: Import customer equipment inventory (CSV or JSON)

**Request** (multipart/form-data):
```
POST /api/v1/equipment/import
Content-Type: multipart/form-data

file: equipment_list.csv
customer_id: cust_12345
auto_match_cpe: true
```

**CSV Format**:
```csv
hostname,software,version,location,criticality
web-server-01,Apache HTTP Server,2.4.54,DMZ,high
db-server-01,PostgreSQL,14.5,internal,critical
workstation-42,Microsoft Windows 10,21H2,internal,low
```

**Response** (200 OK):
```json
{
  "customer_id": "cust_12345",
  "total_assets": 3,
  "matched_assets": 3,
  "unmatched_assets": 0,
  "cpe_matches": [
    {
      "hostname": "web-server-01",
      "software": "Apache HTTP Server",
      "matched_cpe": "cpe:2.3:a:apache:http_server:2.4.54",
      "confidence": 0.98
    },
    {
      "hostname": "db-server-01",
      "software": "PostgreSQL",
      "matched_cpe": "cpe:2.3:a:postgresql:postgresql:14.5",
      "confidence": 1.0
    },
    {
      "hostname": "workstation-42",
      "software": "Microsoft Windows 10",
      "matched_cpe": "cpe:2.3:o:microsoft:windows_10:-",
      "confidence": 0.92
    }
  ],
  "execution_time_ms": 2341
}
```

**Error Responses**:
- `400 Bad Request`: Invalid CSV format
- `413 Payload Too Large`: > 10,000 assets in single request

**TASKMASTER Reference**: TASK-2025-11-12-017

---

#### 1.2.4 Attack Surface Calculation Endpoint

**Endpoint**: `GET /api/v1/attack_surface/{customer_id}`

**Description**: Calculate total CVE exposure for a customer's equipment

**Request**:
```
GET /api/v1/attack_surface/cust_12345?location=DMZ&criticality=high
```

**Response** (200 OK):
```json
{
  "customer_id": "cust_12345",
  "total_assets": 150,
  "filtered_assets": 25,
  "total_cves": 1247,
  "high_risk_cves": 43,
  "risk_heatmap": {
    "TA0001": {"count": 234, "avg_probability": 0.72, "equipment": ["web-server-01", "web-server-02"]},
    "TA0002": {"count": 189, "avg_probability": 0.65, "equipment": ["app-server-03"]},
    "TA0003": {"count": 156, "avg_probability": 0.58, "equipment": ["db-server-01"]}
  },
  "top_vulnerable_assets": [
    {
      "hostname": "web-server-01",
      "cve_count": 87,
      "risk_score": 0.84,
      "top_cves": ["CVE-2024-1", "CVE-2024-5"]
    },
    {
      "hostname": "app-server-03",
      "cve_count": 62,
      "risk_score": 0.76,
      "top_cves": ["CVE-2024-3"]
    }
  ],
  "execution_time_ms": 7832,
  "computed_at": "2025-11-12T06:00:00Z"
}
```

**Performance Requirements**:
- 10,000 assets: < 10 seconds

**TASKMASTER Reference**: TASK-2025-11-12-019

---

#### 1.2.5 Mitigation Recommendation Endpoint

**Endpoint**: `GET /api/v1/mitigations/{cve_id}`

**Description**: Get ATT&CK mitigations for a CVE

**Request**:
```
GET /api/v1/mitigations/CVE-2024-1234?equipment_type=windows_server
```

**Response** (200 OK):
```json
{
  "cve_id": "CVE-2024-1234",
  "techniques": [
    {
      "id": "T1059",
      "name": "Command and Scripting Interpreter",
      "mitigations": [
        {
          "id": "M1038",
          "name": "Execution Prevention",
          "description": "Block execution of scripts from untrusted sources",
          "implementation": "Configure AppLocker or WDAC policies",
          "equipment_specific": true
        },
        {
          "id": "M1049",
          "name": "Antivirus/Antimalware",
          "description": "Use AV to detect malicious scripts",
          "implementation": "Deploy Windows Defender ATP",
          "equipment_specific": true
        }
      ]
    }
  ],
  "patching_guidance": {
    "vendor": "Microsoft",
    "patch_id": "KB5028244",
    "release_date": "2024-08-08",
    "advisory_url": "https://msrc.microsoft.com/...",
    "testing_required": true
  },
  "compensating_controls": [
    "Network segmentation: isolate vulnerable servers",
    "WAF rule: block PowerShell command injection patterns"
  ],
  "total_mitigations": 2,
  "execution_time_ms": 423
}
```

**TASKMASTER Reference**: TASK-2025-11-12-020

---

#### 1.2.6 Detection Rule Generation Endpoint

**Endpoint**: `POST /api/v1/detections/generate`

**Description**: Auto-generate SIEM/EDR rules for a CVE

**Request**:
```json
{
  "cve_id": "CVE-2024-1234",
  "rule_formats": ["splunk", "sigma", "kql"],
  "equipment_types": ["windows_server", "linux_server"]
}
```

**Response** (200 OK):
```json
{
  "cve_id": "CVE-2024-1234",
  "techniques": ["T1059"],
  "rules": [
    {
      "format": "splunk",
      "rule": "index=windows EventCode=4688 CommandLine=*powershell* | where CommandLine LIKE \"%IEX%\" OR CommandLine LIKE \"%Invoke-Expression%\"",
      "severity": "high",
      "false_positive_rate": "medium"
    },
    {
      "format": "sigma",
      "rule": "title: Suspicious PowerShell Execution\nstatus: experimental\nlogsource:\n  product: windows\n  service: sysmon\ndetection:\n  selection:\n    EventID: 1\n    Image|endswith: '\\\\powershell.exe'\n    CommandLine|contains:\n      - 'IEX'\n      - 'Invoke-Expression'\n  condition: selection",
      "severity": "high"
    },
    {
      "format": "kql",
      "rule": "DeviceProcessEvents | where ProcessCommandLine has_any ('IEX', 'Invoke-Expression') and FileName =~ 'powershell.exe'",
      "severity": "high"
    }
  ],
  "testing_guidance": "Test with benign PowerShell scripts to tune false positives",
  "deployment_priority": "high",
  "execution_time_ms": 1205
}
```

**TASKMASTER Reference**: TASK-2025-11-12-021

---

#### 1.2.7 Priority Action Planner Endpoint

**Endpoint**: `GET /api/v1/priority_actions/{customer_id}`

**Description**: Generate ranked remediation to-do list

**Request**:
```
GET /api/v1/priority_actions/cust_12345?timeframe=quarterly
```

**Response** (200 OK):
```json
{
  "customer_id": "cust_12345",
  "timeframe": "quarterly",
  "total_actions": 43,
  "high_priority": 12,
  "actions": [
    {
      "rank": 1,
      "cve_id": "CVE-2024-1",
      "risk_score": 0.92,
      "cvss_base": 9.8,
      "equipment_affected": ["web-server-01", "web-server-02"],
      "action": "Patch Apache HTTP Server to version 2.4.55",
      "effort": "low",
      "estimated_hours": 2,
      "deadline": "2025-11-20",
      "dependencies": ["Schedule maintenance window"],
      "mitigation_id": "M1051"
    },
    {
      "rank": 2,
      "cve_id": "CVE-2024-5",
      "risk_score": 0.87,
      "cvss_base": 7.5,
      "equipment_affected": ["db-server-01"],
      "action": "Upgrade PostgreSQL to version 14.7",
      "effort": "medium",
      "estimated_hours": 8,
      "deadline": "2025-12-01",
      "dependencies": ["Database backup", "Application downtime approval"],
      "mitigation_id": "M1051"
    }
  ],
  "execution_time_ms": 5234,
  "computed_at": "2025-11-12T06:15:00Z"
}
```

**TASKMASTER Reference**: TASK-2025-11-12-022

---

### 1.3 WebSocket API (Real-time Updates)

**Endpoint**: `wss://api.aeon-dt.com/v1/ws`

**Use Case**: Real-time CVE score updates, job progress notifications

**Connection**:
```javascript
const ws = new WebSocket('wss://api.aeon-dt.com/v1/ws');
ws.send(JSON.stringify({
  "action": "subscribe",
  "channels": ["cve_scores", "job_progress"],
  "customer_id": "cust_12345"
}));

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.channel === "cve_scores") {
    console.log("New CVE score:", data.payload);
  }
};
```

**Message Format**:
```json
{
  "channel": "cve_scores",
  "event": "score_updated",
  "payload": {
    "cve_id": "CVE-2024-1234",
    "overall_probability": 0.78,
    "timestamp": "2025-11-12T06:30:00Z"
  }
}
```

---

## Section 2: Database Schemas

### 2.1 PostgreSQL Schema

**Database**: `aeon` (on `aeon-postgres-dev`, port 5432)

#### 2.1.1 Job Persistence Schema

```sql
-- ====================================
-- Job Persistence Tables
-- Purpose: Track all long-running jobs with 100% reliability
-- TASKMASTER Reference: TASK-2025-11-12-002
-- ====================================

CREATE TABLE jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_name VARCHAR(255) NOT NULL,
    job_type VARCHAR(100) NOT NULL CHECK (job_type IN (
        'cvss_ingestion', 'attack_update', 'scoring_batch',
        'equipment_import', 'chain_validation', 'gnn_training'
    )),
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'running', 'completed', 'failed', 'retrying'
    )),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN (
        'critical', 'high', 'medium', 'low'
    )),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    retries INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    error_message TEXT,
    metadata JSONB,
    created_by VARCHAR(255),

    -- Indexes
    INDEX idx_jobs_status (status),
    INDEX idx_jobs_type (job_type),
    INDEX idx_jobs_created (created_at DESC)
);

CREATE TABLE job_steps (
    step_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    step_name VARCHAR(255) NOT NULL,
    step_order INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'running', 'completed', 'failed', 'skipped'
    )),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    output JSONB,
    error_message TEXT,

    -- Unique constraint: each step_order unique per job
    UNIQUE (job_id, step_order),
    INDEX idx_job_steps_job (job_id),
    INDEX idx_job_steps_status (status)
);

CREATE TABLE job_logs (
    log_id BIGSERIAL PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    step_id UUID REFERENCES job_steps(step_id) ON DELETE CASCADE,
    log_level VARCHAR(20) NOT NULL CHECK (log_level IN (
        'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    )),
    message TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB,

    INDEX idx_job_logs_job (job_id),
    INDEX idx_job_logs_timestamp (timestamp DESC),
    INDEX idx_job_logs_level (log_level)
);

-- ====================================
-- Retry Logic Function
-- ====================================

CREATE OR REPLACE FUNCTION retry_failed_job(p_job_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    v_retries INTEGER;
    v_max_retries INTEGER;
BEGIN
    -- Get current retry count
    SELECT retries, max_retries INTO v_retries, v_max_retries
    FROM jobs WHERE job_id = p_job_id;

    -- Check if retries exhausted
    IF v_retries >= v_max_retries THEN
        UPDATE jobs SET status = 'failed', error_message = 'Max retries exhausted'
        WHERE job_id = p_job_id;
        RETURN FALSE;
    END IF;

    -- Increment retry count and reset to pending
    UPDATE jobs
    SET status = 'retrying', retries = retries + 1, started_at = NULL
    WHERE job_id = p_job_id;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- ====================================
-- Example Usage
-- ====================================

-- Create a CVE ingestion job
INSERT INTO jobs (job_name, job_type, priority, metadata)
VALUES (
    'Daily CVE Ingestion 2025-11-12',
    'cvss_ingestion',
    'high',
    '{"source": "NVD", "date_range": "2025-11-11 to 2025-11-12"}'
) RETURNING job_id;

-- Add steps to job
INSERT INTO job_steps (job_id, step_name, step_order)
VALUES
    ('uuid-from-above', 'Fetch CVEs from NVD API', 1),
    ('uuid-from-above', 'Parse CVE JSON', 2),
    ('uuid-from-above', 'Insert into Neo4j', 3),
    ('uuid-from-above', 'Validate semantic chains', 4);
```

#### 2.1.2 Customer Management Schema

```sql
-- ====================================
-- Customer and Equipment Tables
-- TASKMASTER Reference: TASK-2025-11-12-017
-- ====================================

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    industry_sector VARCHAR(100) CHECK (industry_sector IN (
        'healthcare', 'finance', 'energy', 'manufacturing',
        'technology', 'retail', 'government', 'education'
    )),
    geographic_region VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB,

    INDEX idx_customers_sector (industry_sector)
);

CREATE TABLE equipment (
    equipment_id BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    hostname VARCHAR(255) NOT NULL,
    software_name VARCHAR(500) NOT NULL,
    software_version VARCHAR(100),
    cpe_match VARCHAR(500),
    cpe_confidence DECIMAL(3,2),
    location VARCHAR(100) CHECK (location IN ('internal', 'DMZ', 'external')),
    criticality VARCHAR(20) CHECK (criticality IN ('critical', 'high', 'medium', 'low')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB,

    UNIQUE (customer_id, hostname, software_name),
    INDEX idx_equipment_customer (customer_id),
    INDEX idx_equipment_cpe (cpe_match),
    INDEX idx_equipment_criticality (criticality)
);

CREATE TABLE equipment_cve_mapping (
    mapping_id BIGSERIAL PRIMARY KEY,
    equipment_id BIGINT NOT NULL REFERENCES equipment(equipment_id) ON DELETE CASCADE,
    cve_id VARCHAR(20) NOT NULL,
    discovered_at TIMESTAMP DEFAULT NOW(),
    risk_score DECIMAL(4,2),

    UNIQUE (equipment_id, cve_id),
    INDEX idx_mapping_equipment (equipment_id),
    INDEX idx_mapping_cve (cve_id),
    INDEX idx_mapping_risk (risk_score DESC)
);
```

#### 2.1.3 Audit and Compliance Schema

```sql
-- ====================================
-- Audit Logging (Constitutional mandate)
-- ====================================

CREATE TABLE audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    request_body JSONB,
    response_status INTEGER,

    INDEX idx_audit_user (user_id),
    INDEX idx_audit_timestamp (timestamp DESC),
    INDEX idx_audit_action (action)
);

-- Function to log API calls
CREATE OR REPLACE FUNCTION log_api_call(
    p_user_id VARCHAR(255),
    p_action VARCHAR(100),
    p_resource_type VARCHAR(100),
    p_resource_id VARCHAR(255),
    p_ip_address INET,
    p_request_body JSONB,
    p_response_status INTEGER
) RETURNS VOID AS $$
BEGIN
    INSERT INTO audit_log (user_id, action, resource_type, resource_id, ip_address, request_body, response_status)
    VALUES (p_user_id, p_action, p_resource_type, p_resource_id, p_ip_address, p_request_body, p_response_status);
END;
$$ LANGUAGE plpgsql;
```

---

### 2.2 Neo4j Schema (Cypher)

**Database**: Neo4j 5.26 (bolt://172.18.0.5:7687)

#### 2.2.1 Node Labels and Properties

```cypher
// ====================================
// CVE Nodes
// ====================================
CREATE CONSTRAINT cve_id_unique IF NOT EXISTS
FOR (c:CVE) REQUIRE c.id IS UNIQUE;

// Example CVE node
CREATE (:CVE {
    id: "CVE-2024-1234",
    description: "Buffer overflow in Apache HTTP Server...",
    published_date: datetime("2024-08-08T12:00:00Z"),
    modified_date: datetime("2024-08-10T15:30:00Z"),
    cvss_v3_score: 9.8,
    cvss_v3_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    cwe_ids: ["CWE-79", "CWE-89"],
    references: ["https://nvd.nist.gov/...", "https://apache.org/security/..."]
});

// ====================================
// CWE Nodes
// ====================================
CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS
FOR (w:CWE) REQUIRE w.id IS UNIQUE;

CREATE (:CWE {
    id: "CWE-79",
    name: "Improper Neutralization of Input During Web Page Generation",
    description: "Cross-Site Scripting (XSS)",
    abstraction: "Base",
    likelihood: "High"
});

// ====================================
// CAPEC Nodes
// ====================================
CREATE CONSTRAINT capec_id_unique IF NOT EXISTS
FOR (c:CAPEC) REQUIRE c.id IS UNIQUE;

CREATE (:CAPEC {
    id: "CAPEC-63",
    name: "Cross-Site Scripting (XSS)",
    description: "Injection of malicious scripts into web pages...",
    likelihood_of_attack: "High",
    typical_severity: "Very High"
});

// ====================================
// ATT&CK Technique Nodes
// ====================================
CREATE CONSTRAINT technique_id_unique IF NOT EXISTS
FOR (t:Technique) REQUIRE t.id IS UNIQUE;

CREATE (:Technique {
    id: "T1059",
    name: "Command and Scripting Interpreter",
    description: "Adversaries may abuse command and script interpreters...",
    platforms: ["Windows", "Linux", "macOS"],
    data_sources: ["Process monitoring", "Script execution logs"]
});

// ====================================
// ATT&CK Tactic Nodes
// ====================================
CREATE CONSTRAINT tactic_id_unique IF NOT EXISTS
FOR (t:Tactic) REQUIRE t.id IS UNIQUE;

CREATE (:Tactic {
    id: "TA0002",
    name: "Execution",
    description: "The adversary is trying to run malicious code"
});

// ====================================
// Mitigation Nodes
// ====================================
CREATE (:Mitigation {
    id: "M1038",
    name: "Execution Prevention",
    description: "Block execution of code on a system through application control"
});

// ====================================
// Detection Nodes
// ====================================
CREATE (:Detection {
    id: "DS0009",
    name: "Process",
    description: "Instances of computer programs executed by the OS",
    data_component: "Process Creation"
});
```

#### 2.2.2 Relationship Types

```cypher
// ====================================
// Semantic Chain Relationships
// TASKMASTER Reference: TASK-2025-11-12-005 through 008
// ====================================

// CVE → CWE (from NVD data)
MATCH (cve:CVE {id: "CVE-2024-1234"}), (cwe:CWE {id: "CWE-79"})
CREATE (cve)-[:HAS_CWE {
    confidence: 0.95,
    source: "NVD",
    discovered_at: datetime()
}]->(cwe);

// CWE → CAPEC (from CAPEC database)
MATCH (cwe:CWE {id: "CWE-79"}), (capec:CAPEC {id: "CAPEC-63"})
CREATE (cwe)-[:MAPS_TO_CAPEC {
    confidence: 0.80,
    source: "MITRE_CAPEC",
    mapping_type: "primary"
}]->(capec);

// CAPEC → Technique (from ATT&CK STIX)
MATCH (capec:CAPEC {id: "CAPEC-63"}), (tech:Technique {id: "T1059"})
CREATE (capec)-[:MAPS_TO_TECHNIQUE {
    confidence: 0.75,
    source: "ATT&CK_STIX",
    technique_subtypes: ["PowerShell", "JavaScript"]
}]->(tech);

// Technique → Tactic (from ATT&CK kill_chain_phases)
MATCH (tech:Technique {id: "T1059"}), (tactic:Tactic {id: "TA0002"})
CREATE (tech)-[:BELONGS_TO_TACTIC {
    confidence: 1.0,
    source: "ATT&CK"
}]->(tactic);

// Technique → Mitigation
MATCH (tech:Technique {id: "T1059"}), (mit:Mitigation {id: "M1038"})
CREATE (tech)-[:MITIGATED_BY]->(mit);

// Technique → Detection
MATCH (tech:Technique {id: "T1059"}), (det:Detection {id: "DS0009"})
CREATE (tech)-[:DETECTED_BY]->(det);
```

#### 2.2.3 Index Creation

```cypher
// ====================================
// Performance Indexes
// ====================================

CREATE INDEX cve_published_date IF NOT EXISTS
FOR (c:CVE) ON (c.published_date);

CREATE INDEX cve_cvss_score IF NOT EXISTS
FOR (c:CVE) ON (c.cvss_v3_score);

CREATE INDEX technique_platforms IF NOT EXISTS
FOR (t:Technique) ON (t.platforms);

// ====================================
// Full-Text Search Indexes
// ====================================

CREATE FULLTEXT INDEX cve_description_search IF NOT EXISTS
FOR (c:CVE) ON EACH [c.description];

CREATE FULLTEXT INDEX technique_name_search IF NOT EXISTS
FOR (t:Technique) ON EACH [t.name, t.description];
```

#### 2.2.4 Cypher Query Examples

**Query 1: Full Semantic Chain for a CVE**
```cypher
MATCH path = (cve:CVE {id: "CVE-2024-1234"})-[:HAS_CWE]->(:CWE)
             -[:MAPS_TO_CAPEC]->(:CAPEC)
             -[:MAPS_TO_TECHNIQUE]->(:Technique)
             -[:BELONGS_TO_TACTIC]->(tactic:Tactic)
RETURN cve.id AS cve_id,
       [node IN nodes(path) | labels(node)[0] + ":" + node.id] AS chain_path,
       tactic.name AS primary_tactic,
       length(path) AS chain_length;
```

**Query 2: All CVEs Leading to a Specific Tactic**
```cypher
MATCH (cve:CVE)-[:HAS_CWE*]->(:CWE)-[:MAPS_TO_CAPEC*]->(:CAPEC)
      -[:MAPS_TO_TECHNIQUE*]->(:Technique)-[:BELONGS_TO_TACTIC]->(tactic:Tactic {id: "TA0001"})
RETURN DISTINCT cve.id, cve.cvss_v3_score
ORDER BY cve.cvss_v3_score DESC
LIMIT 100;
```

**Query 3: Chain Completeness Validation**
```cypher
// Count CVEs with complete chains
MATCH (cve:CVE)
OPTIONAL MATCH path = (cve)-[:HAS_CWE]->(:CWE)-[:MAPS_TO_CAPEC]->(:CAPEC)
                      -[:MAPS_TO_TECHNIQUE]->(:Technique)-[:BELONGS_TO_TACTIC]->(:Tactic)
WITH cve, path
WHERE path IS NOT NULL
RETURN COUNT(DISTINCT cve) AS cves_with_complete_chains;

// Total CVE count
MATCH (cve:CVE)
RETURN COUNT(cve) AS total_cves;

// Calculate percentage
// completeness = cves_with_complete_chains / total_cves * 100
```

**Query 4: GNN Link Prediction Training Data**
```cypher
// Export edges for GNN training
MATCH (source)-[rel]->(target)
WHERE type(rel) IN ['HAS_CWE', 'MAPS_TO_CAPEC', 'MAPS_TO_TECHNIQUE', 'BELONGS_TO_TACTIC']
RETURN id(source) AS source_id,
       id(target) AS target_id,
       type(rel) AS relationship_type,
       properties(rel) AS edge_properties
LIMIT 1000000;
```

---

### 2.3 MySQL Schema (OpenSPG)

**Database**: `openspg` (on `openspg-mysql`, port 3306)

#### 2.3.1 Existing Tables (Reference)

```sql
-- OpenSPG operational metadata (33 tables)
-- These tables already exist; DO NOT modify

SHOW TABLES;
/*
+----------------------------+
| Tables_in_openspg          |
+----------------------------+
| kg_builder_job             |
| kg_builder_model           |
| kg_concept                 |
| kg_concept_instance        |
| kg_entity_type             |
| kg_property                |
| kg_relation_type           |
| kg_schema_draft            |
| ... (25 more tables)       |
+----------------------------+
*/

-- Example: Query OpenSPG job status
SELECT job_id, job_name, status, created_at
FROM kg_builder_job
WHERE status = 'running'
ORDER BY created_at DESC;
```

---

### 2.4 Qdrant Schema

**Qdrant Instance**: http://172.18.0.6:6333

#### 2.4.1 Collection Definitions

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(url="http://172.18.0.6:6333")

# ====================================
# Collection 1: Agent Memory
# TASKMASTER Reference: Constitution Article IV
# ====================================

client.create_collection(
    collection_name="agent_memory",
    vectors_config=VectorParams(
        size=768,  # BERT-base embedding dimension
        distance=Distance.COSINE
    )
)

# Example memory point
client.upsert(
    collection_name="agent_memory",
    points=[
        PointStruct(
            id=hash("ml_engineer_decision_001"),
            vector=[0.1, 0.2, ..., 0.768],  # BERT embedding
            payload={
                "agent_id": "ml_engineer",
                "task_id": "TASK-2025-11-12-010",
                "memory_type": "decision",
                "timestamp": "2025-11-12T06:15:00Z",
                "content": "Chose Laplace smoothing (alpha=1.0) for Bayesian prior estimation",
                "related_agents": ["data_pipeline_engineer", "qa_engineer"],
                "tags": ["bayesian", "smoothing", "phase_2"],
                "confidence": 0.92
            }
        )
    ]
)

# ====================================
# Collection 2: Task History
# ====================================

client.create_collection(
    collection_name="task_history",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

# Example task completion record
client.upsert(
    collection_name="task_history",
    points=[
        PointStruct(
            id=hash("TASK-2025-11-12-010"),
            vector=[0.3, 0.1, ..., 0.768],
            payload={
                "task_id": "TASK-2025-11-12-010",
                "status": "COMPLETED",
                "completion_timestamp": "2026-03-20T14:30:00Z",
                "deliverables": ["src/intelligence/scorer.py", "tests/test_scorer.py"],
                "success_metrics": {
                    "accuracy": 0.87,
                    "latency_p99": 1.8,
                    "test_coverage": 0.91
                },
                "lessons_learned": "Monte Carlo simulation needed GPU for 10K samples (CPU took 45s)",
                "next_actions": ["Deploy to staging", "Run load tests with 1M CVEs"]
            }
        )
    ]
)

# ====================================
# Collection 3: Semantic Chains (Cache)
# ====================================

client.create_collection(
    collection_name="semantic_chains",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

# Example cached semantic chain
client.upsert(
    collection_name="semantic_chains",
    points=[
        PointStruct(
            id=hash("CVE-2024-1234_chain"),
            vector=[0.5, 0.4, ..., 0.768],
            payload={
                "cve_id": "CVE-2024-1234",
                "chain_paths": [
                    {
                        "path": ["CVE-2024-1234", "CWE-79", "CAPEC-63", "T1059", "TA0002"],
                        "probability": 0.45,
                        "edge_confidences": [0.95, 0.80, 0.75, 0.85]
                    },
                    {
                        "path": ["CVE-2024-1234", "CWE-79", "CAPEC-18", "T1059", "TA0002"],
                        "probability": 0.33,
                        "edge_confidences": [0.95, 0.60, 0.70, 0.85]
                    }
                ],
                "overall_probability": 0.78,
                "primary_tactic": "TA0002",
                "computed_at": "2025-11-15T10:00:00Z",
                "ttl": "2025-12-15T10:00:00Z",
                "customer_modifier": 1.0
            }
        )
    ]
)
```

#### 2.4.2 Vector Search Examples

```python
# Search for similar agent decisions
results = client.search(
    collection_name="agent_memory",
    query_vector=bert_model.encode("How should I handle zero-count edges in Bayesian model?"),
    limit=5,
    score_threshold=0.7,
    query_filter={
        "must": [
            {"key": "tags", "match": {"value": "bayesian"}},
            {"key": "confidence", "range": {"gte": 0.8}}
        ]
    }
)

for hit in results:
    print(f"Similar decision: {hit.payload['content']}")
    print(f"Similarity: {hit.score}, Agent: {hit.payload['agent_id']}")

# Retrieve cached semantic chains
chain_results = client.search(
    collection_name="semantic_chains",
    query_vector=bert_model.encode("CVE-2024-1234 attack chain"),
    limit=1,
    query_filter={"must": [{"key": "cve_id", "match": {"value": "CVE-2024-1234"}}]}
)

if chain_results and chain_results[0].score > 0.9:
    cached_chain = chain_results[0].payload
    print(f"Cache hit! Probability: {cached_chain['overall_probability']}")
else:
    print("Cache miss, computing semantic chain from Neo4j...")
```

---

## Section 3: Data Models and Classes

### 3.1 AttackChainScorer Class

**File**: `backend/src/intelligence/attack_chain_scorer.py`

```python
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from scipy import stats
from neo4j import GraphDatabase

@dataclass
class ChainPath:
    """Represents a single semantic chain path"""
    nodes: List[str]  # e.g., ["CVE-2024-1234", "CWE-79", "CAPEC-63", "T1059", "TA0002"]
    edge_probabilities: List[float]  # P(CWE|CVE), P(CAPEC|CWE), P(Technique|CAPEC), P(Tactic|Technique)
    overall_probability: float  # Product of edge probabilities

@dataclass
class CVEScore:
    """Complete CVE risk score with confidence intervals"""
    cve_id: str
    overall_probability: float
    confidence_interval: Tuple[float, float]  # (lower, upper)
    primary_tactic: Dict[str, str]  # {"id": "TA0002", "name": "Execution", "probability": 0.65}
    chains: List[ChainPath]
    customer_modifier: float  # Sector/equipment adjustment (default 1.0)
    data_quality: Dict[str, float]  # {"chain_completeness": 0.85, "cwe_confidence": 0.95}
    execution_time_ms: int
    computed_at: str  # ISO 8601 timestamp

class AttackChainScorer:
    """
    Bayesian probabilistic attack chain scoring engine

    Formula:
    P(Tactic | CVE) = Σ P(Tactic | Technique) × P(Technique | CAPEC)
                      × P(CAPEC | CWE) × P(CWE | CVE)

    TASKMASTER Reference: TASK-2025-11-12-010
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://172.18.0.5:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "${NEO4J_PASSWORD}",
        laplace_alpha: float = 1.0,
        monte_carlo_samples: int = 10000
    ):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.laplace_alpha = laplace_alpha  # Smoothing parameter for zero counts
        self.monte_carlo_samples = monte_carlo_samples

    def score_cve(
        self,
        cve_id: str,
        customer_context: Optional[Dict] = None
    ) -> CVEScore:
        """
        Score a single CVE using Bayesian chain analysis

        Args:
            cve_id: CVE identifier (e.g., "CVE-2024-1234")
            customer_context: {
                "industry_sector": "healthcare",
                "equipment_types": ["windows_server"],
                "geographic_region": "north_america"
            }

        Returns:
            CVEScore with probability, confidence interval, and chains
        """
        start_time = time.time()

        # Step 1: Query Neo4j for all semantic chains
        chains = self._get_semantic_chains(cve_id)

        if not chains:
            raise ValueError(f"No semantic chains found for {cve_id}")

        # Step 2: Calculate edge probabilities from graph frequencies
        for chain in chains:
            chain.edge_probabilities = self._calculate_edge_probabilities(chain.nodes)
            chain.overall_probability = np.prod(chain.edge_probabilities)

        # Step 3: Sum probabilities across all chains (grouped by tactic)
        tactic_probabilities = self._aggregate_by_tactic(chains)

        # Step 4: Apply customer-specific priors
        customer_modifier = self._get_customer_modifier(customer_context)
        adjusted_probabilities = {
            tactic: prob * customer_modifier
            for tactic, prob in tactic_probabilities.items()
        }

        # Step 5: Run Monte Carlo for confidence intervals
        primary_tactic_id = max(adjusted_probabilities, key=adjusted_probabilities.get)
        ci_lower, ci_upper = self._monte_carlo_confidence_interval(
            chains,
            primary_tactic_id
        )

        # Step 6: Construct response
        execution_time_ms = int((time.time() - start_time) * 1000)

        return CVEScore(
            cve_id=cve_id,
            overall_probability=adjusted_probabilities[primary_tactic_id],
            confidence_interval=(ci_lower, ci_upper),
            primary_tactic={
                "id": primary_tactic_id,
                "name": self._get_tactic_name(primary_tactic_id),
                "probability": adjusted_probabilities[primary_tactic_id]
            },
            chains=chains,
            customer_modifier=customer_modifier,
            data_quality=self._assess_data_quality(cve_id, chains),
            execution_time_ms=execution_time_ms,
            computed_at=datetime.utcnow().isoformat() + "Z"
        )

    def _get_semantic_chains(self, cve_id: str) -> List[ChainPath]:
        """Query Neo4j for all paths from CVE to Tactic"""
        query = """
        MATCH path = (cve:CVE {id: $cve_id})-[:HAS_CWE]->(:CWE)
                     -[:MAPS_TO_CAPEC]->(:CAPEC)
                     -[:MAPS_TO_TECHNIQUE]->(:Technique)
                     -[:BELONGS_TO_TACTIC]->(tactic:Tactic)
        RETURN [node IN nodes(path) | node.id] AS chain_nodes
        LIMIT 100
        """

        with self.driver.session() as session:
            result = session.run(query, cve_id=cve_id)
            chains = [
                ChainPath(nodes=record["chain_nodes"], edge_probabilities=[], overall_probability=0.0)
                for record in result
            ]

        return chains

    def _calculate_edge_probabilities(self, nodes: List[str]) -> List[float]:
        """
        Calculate P(target | source) for each edge using Laplace smoothing

        Example:
        P(CWE-79 | CVE-2024-1234) = (count(CVE-2024-1234 → CWE-79) + alpha)
                                     / (count(all CVE-2024-1234 edges) + alpha * num_cwe)
        """
        edge_probs = []

        for i in range(len(nodes) - 1):
            source_id, target_id = nodes[i], nodes[i+1]

            # Query Neo4j for edge frequency
            query = """
            MATCH (source {id: $source_id})-[r]->(target {id: $target_id})
            RETURN COUNT(r) AS edge_count
            """

            with self.driver.session() as session:
                result = session.run(query, source_id=source_id, target_id=target_id)
                edge_count = result.single()["edge_count"]

            # Get total outgoing edges from source
            total_query = """
            MATCH (source {id: $source_id})-[r]->()
            RETURN COUNT(r) AS total_edges
            """

            with self.driver.session() as session:
                result = session.run(total_query, source_id=source_id)
                total_edges = result.single()["total_edges"]

            # Laplace smoothing
            num_possible_targets = self._get_num_nodes_of_type(self._get_node_type(target_id))
            prob = (edge_count + self.laplace_alpha) / (total_edges + self.laplace_alpha * num_possible_targets)
            edge_probs.append(prob)

        return edge_probs

    def _monte_carlo_confidence_interval(
        self,
        chains: List[ChainPath],
        tactic_id: str,
        confidence_level: float = 0.95
    ) -> Tuple[float, float]:
        """
        Monte Carlo simulation for confidence intervals

        Algorithm:
        1. For each chain, sample edge probabilities from Beta distributions
        2. Compute overall probability for this sample
        3. Repeat 10,000 times
        4. Calculate Wilson Score confidence interval
        """
        samples = []

        for _ in range(self.monte_carlo_samples):
            sample_prob = 0.0

            for chain in chains:
                if chain.nodes[-1] == tactic_id:
                    # Sample each edge probability from Beta(alpha, beta)
                    sampled_edges = [
                        np.random.beta(a=prob * 100, b=(1 - prob) * 100)  # Beta parameters from edge prob
                        for prob in chain.edge_probabilities
                    ]
                    sample_prob += np.prod(sampled_edges)

            samples.append(sample_prob)

        # Wilson Score interval
        samples = np.array(samples)
        mean = np.mean(samples)
        z = stats.norm.ppf(1 - (1 - confidence_level) / 2)  # z-score for 95% CI
        n = len(samples)

        denominator = 1 + z**2 / n
        center = (mean + z**2 / (2 * n)) / denominator
        margin = z * np.sqrt(mean * (1 - mean) / n + z**2 / (4 * n**2)) / denominator

        return (max(0, center - margin), min(1, center + margin))

    def _get_customer_modifier(self, customer_context: Optional[Dict]) -> float:
        """
        Adjust probabilities based on customer industry/equipment

        Examples:
        - Healthcare + Ransomware tactics: 1.3x
        - Finance + Credential Access: 1.5x
        - Windows Server + certain techniques: 1.2x
        """
        if not customer_context:
            return 1.0

        modifier = 1.0

        # Industry sector adjustments
        sector_modifiers = {
            "healthcare": {"TA0040": 1.3},  # Impact (ransomware)
            "finance": {"TA0006": 1.5},     # Credential Access
            "energy": {"TA0040": 1.4}       # Impact
        }

        sector = customer_context.get("industry_sector")
        if sector in sector_modifiers:
            # Apply sector modifier (simplified; in production, match against primary tactic)
            modifier *= 1.1  # Baseline increase for sector targeting

        return modifier

    def _assess_data_quality(self, cve_id: str, chains: List[ChainPath]) -> Dict[str, float]:
        """Assess confidence in data completeness and freshness"""
        return {
            "chain_completeness": len(chains) / 5.0 if chains else 0.0,  # Assume 5 chains = complete
            "data_freshness_days": self._get_cve_age_days(cve_id),
            "cwe_confidence": 0.95  # From NVD data quality
        }

    def _get_cve_age_days(self, cve_id: str) -> int:
        """Calculate days since CVE was last modified"""
        query = "MATCH (cve:CVE {id: $cve_id}) RETURN cve.modified_date AS modified"

        with self.driver.session() as session:
            result = session.run(query, cve_id=cve_id)
            modified_date = result.single()["modified"]
            return (datetime.now() - modified_date).days

    # ... (Additional helper methods)
```

---

### 3.2 GNN Link Predictor Class

**File**: `backend/src/intelligence/gnn_link_predictor.py`

```python
import torch
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool
from torch_geometric.data import Data
from typing import Tuple

class GNNLinkPredictor(torch.nn.Module):
    """
    Graph Attention Network for link prediction

    Architecture:
    - Input: Node features (128-dim Node2Vec embeddings)
    - 3 GAT layers with 128 hidden dimensions
    - Output: Binary link prediction (exists / does not exist)

    TASKMASTER Reference: TASK-2025-11-12-014
    """

    def __init__(
        self,
        in_channels: int = 128,
        hidden_channels: int = 128,
        out_channels: int = 64,
        num_layers: int = 3,
        heads: int = 4,
        dropout: float = 0.3
    ):
        super(GNNLinkPredictor, self).__init__()

        self.num_layers = num_layers
        self.convs = torch.nn.ModuleList()

        # First GAT layer
        self.convs.append(GATConv(in_channels, hidden_channels, heads=heads, concat=True, dropout=dropout))

        # Intermediate GAT layers
        for _ in range(num_layers - 2):
            self.convs.append(GATConv(hidden_channels * heads, hidden_channels, heads=heads, concat=True, dropout=dropout))

        # Final GAT layer
        self.convs.append(GATConv(hidden_channels * heads, out_channels, heads=1, concat=False, dropout=dropout))

        # Link prediction MLP
        self.link_predictor = torch.nn.Sequential(
            torch.nn.Linear(out_channels * 2, 64),
            torch.nn.ReLU(),
            torch.nn.Dropout(dropout),
            torch.nn.Linear(64, 1),
            torch.nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through GAT layers

        Args:
            x: Node features [num_nodes, in_channels]
            edge_index: Edge connectivity [2, num_edges]

        Returns:
            Node embeddings [num_nodes, out_channels]
        """
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index)
            if i < self.num_layers - 1:
                x = F.elu(x)
                x = F.dropout(x, p=0.3, training=self.training)

        return x

    def predict_link(self, z: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        """
        Predict probability of link existence

        Args:
            z: Node embeddings from forward() [num_nodes, out_channels]
            edge_index: Candidate edges to score [2, num_candidate_edges]

        Returns:
            Link probabilities [num_candidate_edges, 1]
        """
        # Concatenate source and target node embeddings
        src_embeddings = z[edge_index[0]]
        dst_embeddings = z[edge_index[1]]
        edge_embeddings = torch.cat([src_embeddings, dst_embeddings], dim=-1)

        # Predict link probability
        link_probs = self.link_predictor(edge_embeddings)

        return link_probs

    def train_step(
        self,
        data: Data,
        optimizer: torch.optim.Optimizer,
        pos_edge_index: torch.Tensor,
        neg_edge_index: torch.Tensor
    ) -> float:
        """
        Single training step

        Args:
            data: PyG Data object with x (features) and edge_index
            optimizer: Adam or similar
            pos_edge_index: Positive edges (ground truth) [2, num_pos]
            neg_edge_index: Negative edges (non-existent) [2, num_neg]

        Returns:
            Training loss (float)
        """
        self.train()
        optimizer.zero_grad()

        # Forward pass
        z = self.forward(data.x, data.edge_index)

        # Predict positive and negative edges
        pos_pred = self.predict_link(z, pos_edge_index).squeeze()
        neg_pred = self.predict_link(z, neg_edge_index).squeeze()

        # Binary cross-entropy loss
        pos_loss = F.binary_cross_entropy(pos_pred, torch.ones_like(pos_pred))
        neg_loss = F.binary_cross_entropy(neg_pred, torch.zeros_like(neg_pred))
        loss = pos_loss + neg_loss

        # Backpropagation
        loss.backward()
        optimizer.step()

        return loss.item()

    def evaluate(
        self,
        data: Data,
        pos_edge_index: torch.Tensor,
        neg_edge_index: torch.Tensor
    ) -> Tuple[float, float, float]:
        """
        Evaluate model on test set

        Returns:
            (precision, recall, f1_score)
        """
        self.eval()

        with torch.no_grad():
            z = self.forward(data.x, data.edge_index)

            pos_pred = self.predict_link(z, pos_edge_index).squeeze()
            neg_pred = self.predict_link(z, neg_edge_index).squeeze()

            # Threshold at 0.5
            pos_correct = (pos_pred > 0.5).sum().item()
            neg_correct = (neg_pred <= 0.5).sum().item()

            precision = pos_correct / (pos_correct + (len(neg_pred) - neg_correct))
            recall = pos_correct / len(pos_pred)
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return precision, recall, f1
```

**Training Script**:
```python
# File: backend/src/intelligence/train_gnn.py

from gnn_link_predictor import GNNLinkPredictor
from torch_geometric.data import Data
import torch

# Load Neo4j graph data
def load_neo4j_graph() -> Data:
    """Export Neo4j edges and node features to PyG Data"""
    # ... (implementation: query Neo4j, convert to PyG format)
    pass

# Train model
data = load_neo4j_graph()
model = GNNLinkPredictor(in_channels=128, hidden_channels=128)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    loss = model.train_step(data, optimizer, pos_edges, neg_edges)
    if epoch % 10 == 0:
        precision, recall, f1 = model.evaluate(data, test_pos_edges, test_neg_edges)
        print(f"Epoch {epoch}: Loss={loss:.4f}, Precision={precision:.4f}, Recall={recall:.4f}, F1={f1:.4f}")

# Save model
torch.save(model.state_dict(), "models/gnn_link_predictor_v1.pt")
```

---

## Section 4: Integration Specifications

### 4.1 NVD API Integration

**API Endpoint**: `https://services.nvd.nist.gov/rest/json/cves/2.0`
**Authentication**: API Key (environment variable: `NVD_API_KEY`)
**Rate Limits**: 50 requests per 30 seconds (with API key), 5 requests per 30 seconds (without)

**Integration Flow**:
```python
# File: backend/src/integrations/nvd_integration.py

import requests
import time
from typing import List, Dict
from datetime import datetime, timedelta

class NVDIntegration:
    """
    NVD CVE data ingestion with rate limiting and retry logic

    TASKMASTER Reference: TASK-2025-11-12-002
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.requests_per_30s = 50
        self.request_timestamps = []

    def fetch_cves_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        Fetch all CVEs published within date range

        Args:
            start_date: Start of range (e.g., 2025-11-11)
            end_date: End of range (e.g., 2025-11-12)

        Returns:
            List of CVE dictionaries from NVD API
        """
        cves = []
        start_index = 0
        results_per_page = 2000

        while True:
            # Rate limiting
            self._wait_if_rate_limited()

            # API request
            params = {
                "pubStartDate": start_date.strftime("%Y-%m-%dT00:00:00.000"),
                "pubEndDate": end_date.strftime("%Y-%m-%dT23:59:59.999"),
                "startIndex": start_index,
                "resultsPerPage": results_per_page
            }

            headers = {"apiKey": self.api_key}

            try:
                response = requests.get(
                    self.base_url,
                    params=params,
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()

                data = response.json()
                vulnerabilities = data.get("vulnerabilities", [])

                if not vulnerabilities:
                    break

                cves.extend(vulnerabilities)
                start_index += results_per_page

                # Track request timestamp for rate limiting
                self.request_timestamps.append(time.time())

            except requests.exceptions.RequestException as e:
                # Log error, retry with exponential backoff
                self._handle_error(e, start_index)
                break

        return cves

    def _wait_if_rate_limited(self):
        """Ensure we don't exceed 50 requests per 30 seconds"""
        now = time.time()

        # Remove timestamps older than 30 seconds
        self.request_timestamps = [
            ts for ts in self.request_timestamps
            if now - ts < 30
        ]

        # Wait if we've hit the rate limit
        if len(self.request_timestamps) >= self.requests_per_30s:
            oldest_request = min(self.request_timestamps)
            wait_time = 30 - (now - oldest_request)
            if wait_time > 0:
                time.sleep(wait_time + 0.1)

    def parse_cve(self, cve_data: Dict) -> Dict:
        """
        Extract relevant fields from NVD CVE JSON

        Returns:
            {
                "cve_id": "CVE-2024-1234",
                "description": "Buffer overflow...",
                "published_date": "2024-08-08T12:00:00Z",
                "cvss_v3_score": 9.8,
                "cvss_v3_vector": "CVSS:3.1/AV:N/...",
                "cwe_ids": ["CWE-79", "CWE-89"]
            }
        """
        cve = cve_data["cve"]

        return {
            "cve_id": cve["id"],
            "description": cve["descriptions"][0]["value"],
            "published_date": cve["published"],
            "modified_date": cve["lastModified"],
            "cvss_v3_score": self._extract_cvss_score(cve),
            "cvss_v3_vector": self._extract_cvss_vector(cve),
            "cwe_ids": self._extract_cwe_ids(cve),
            "references": [ref["url"] for ref in cve.get("references", [])]
        }

    def _extract_cwe_ids(self, cve: Dict) -> List[str]:
        """Extract CWE IDs from problemtype field"""
        cwe_ids = []

        for problem in cve.get("weaknesses", []):
            for desc in problem.get("description", []):
                value = desc.get("value", "")
                if value.startswith("CWE-"):
                    cwe_ids.append(value)

        return cwe_ids if cwe_ids else ["CWE-NVD-noinfo"]
```

---

### 4.2 MITRE ATT&CK Integration

**Data Source**: ATT&CK STIX 2.1 JSON (https://github.com/mitre/cti)
**Update Frequency**: Quarterly (or when new ATT&CK version released)

**Integration Flow**:
```python
# File: backend/src/integrations/attack_integration.py

import requests
import json
from typing import List, Dict

class AttackIntegration:
    """
    MITRE ATT&CK STIX data importer

    TASKMASTER Reference: TASK-2025-11-12-003
    """

    def __init__(self):
        self.stix_url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

    def fetch_attack_data(self) -> Dict:
        """Download latest ATT&CK STIX bundle"""
        response = requests.get(self.stix_url, timeout=60)
        response.raise_for_status()
        return response.json()

    def parse_techniques(self, stix_data: Dict) -> List[Dict]:
        """
        Extract techniques from STIX bundle

        Returns:
            [{
                "id": "T1059",
                "name": "Command and Scripting Interpreter",
                "tactics": ["execution"],
                "platforms": ["Windows", "Linux"],
                "capec_ids": ["CAPEC-88"]
            }, ...]
        """
        techniques = []

        for obj in stix_data["objects"]:
            if obj["type"] == "attack-pattern":
                technique = {
                    "id": self._get_external_id(obj),
                    "name": obj["name"],
                    "description": obj.get("description", ""),
                    "tactics": [phase["phase_name"] for phase in obj.get("kill_chain_phases", [])],
                    "platforms": obj.get("x_mitre_platforms", []),
                    "data_sources": obj.get("x_mitre_data_sources", []),
                    "capec_ids": self._extract_capec_refs(obj)
                }
                techniques.append(technique)

        return techniques

    def _extract_capec_refs(self, attack_obj: Dict) -> List[str]:
        """Find CAPEC references in external_references"""
        capec_ids = []

        for ref in attack_obj.get("external_references", []):
            if ref.get("source_name") == "capec":
                capec_ids.append(f"CAPEC-{ref['external_id']}")

        return capec_ids
```

---

### 4.3 Clerk Authentication Integration

**Service**: Clerk.com (https://clerk.com)
**Authentication Flow**: JWT tokens
**CRITICAL**: **NEVER BREAK CLERK AUTH** (Constitutional mandate)

**Frontend Integration** (Next.js):
```typescript
// File: frontend/src/middleware.ts

import { authMiddleware } from "@clerk/nextjs";

export default authMiddleware({
  publicRoutes: ["/", "/api/health", "/docs"],
  ignoredRoutes: ["/api/webhooks/(.*)"]
});

export const config = {
  matcher: ["/((?!.+\\.[\\w]+$|_next).*)", "/", "/(api|trpc)(.*)"],
};
```

**Backend API Protection** (FastAPI):
```python
# File: backend/src/auth/clerk_auth.py

from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import requests
from typing import Dict

security = HTTPBearer()

class ClerkAuth:
    """
    Clerk JWT token validation

    Constitutional Rule: NEVER DISABLE OR BYPASS THIS
    """

    def __init__(self, clerk_secret_key: str):
        self.clerk_secret_key = clerk_secret_key
        self.clerk_jwks_url = "https://clerk.aeon-dt.com/.well-known/jwks.json"

    async def verify_token(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Dict:
        """
        Verify Clerk JWT token

        Returns:
            {"user_id": "user_xxx", "email": "user@example.com"}

        Raises:
            HTTPException(401) if invalid
        """
        token = credentials.credentials

        try:
            # Fetch JWKS (cache this in production)
            jwks = requests.get(self.clerk_jwks_url).json()

            # Decode and verify JWT
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = self._get_rsa_key(jwks, unverified_header["kid"])

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience="http://localhost:3000"  # Update for production
            )

            return {
                "user_id": payload["sub"],
                "email": payload.get("email")
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    def _get_rsa_key(self, jwks: Dict, kid: str) -> Dict:
        """Find RSA key from JWKS by key ID"""
        for key in jwks["keys"]:
            if key["kid"] == kid:
                return {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        raise HTTPException(status_code=401, detail="Invalid token key ID")
```

---

### 4.4 Docker Compose Service Integration

**File**: `/docker-compose.yml`

```yaml
version: '3.8'

services:
  # ====================================
  # Neo4j Knowledge Graph
  # ====================================
  openspg-neo4j:
    image: neo4j:5.26-community
    container_name: openspg-neo4j
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
      - NEO4J_apoc_export_file_enabled=true
      - NEO4J_apoc_import_file_enabled=true
    volumes:
      - neo4j_data:/data
    networks:
      - aeon_network
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "${NEO4J_PASSWORD}", "RETURN 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  # ====================================
  # PostgreSQL Application Database
  # ====================================
  aeon-postgres-dev:
    image: postgres:16
    container_name: aeon-postgres-dev
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=aeon
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - aeon_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ====================================
  # Qdrant Vector Store
  # ====================================
  openspg-qdrant:
    image: qdrant/qdrant:v1.7.4
    container_name: openspg-qdrant
    ports:
      - "6333:6333"  # HTTP API
      - "6334:6334"  # gRPC
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - aeon_network
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 5

  # ====================================
  # Next.js Frontend (with Clerk Auth)
  # ====================================
  aeon-saas-dev:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: aeon-saas-dev
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@aeon-postgres-dev:5432/aeon
      - NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${CLERK_PUBLISHABLE_KEY}
      - CLERK_SECRET_KEY=${CLERK_SECRET_KEY}
      - NEO4J_URI=bolt://openspg-neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
    depends_on:
      - aeon-postgres-dev
      - openspg-neo4j
    networks:
      - aeon_network
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ====================================
  # FastAPI Backend
  # ====================================
  aeon-backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: aeon-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@aeon-postgres-dev:5432/aeon
      - NEO4J_URI=bolt://openspg-neo4j:7687
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - QDRANT_URL=http://openspg-qdrant:6333
      - CLERK_SECRET_KEY=${CLERK_SECRET_KEY}
      - NVD_API_KEY=${NVD_API_KEY}
    depends_on:
      - aeon-postgres-dev
      - openspg-neo4j
      - openspg-qdrant
    networks:
      - aeon_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  aeon_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.18.0.0/16

volumes:
  neo4j_data:
  postgres_data:
  qdrant_data:
```

---

## Section 5: Algorithm Specifications

### 5.1 Bayesian Probability Calculation

**Algorithm**: Conditional probability chain multiplication with Laplace smoothing

**Mathematical Formulation**:
```
P(Tactic | CVE) = Σ [P(Tactic | Technique) × P(Technique | CAPEC)
                     × P(CAPEC | CWE) × P(CWE | CVE)]
```

**Edge Probability Estimation**:
```
P(target | source) = (count(source → target) + α) / (count(all source edges) + α × |target_type|)

Where:
- α = Laplace smoothing parameter (default: 1.0)
- |target_type| = total number of nodes of target type
```

**Example Calculation**:
```
CVE-2024-1234 has 2 semantic chains to TA0002 (Execution):

Chain 1: CVE-2024-1234 → CWE-79 → CAPEC-63 → T1059 → TA0002
  P(CWE-79 | CVE-2024-1234) = 1.0 (only CWE for this CVE)
  P(CAPEC-63 | CWE-79) = 0.80 (CWE-79 maps to 5 CAPECs, CAPEC-63 appears 4 times)
  P(T1059 | CAPEC-63) = 0.75 (CAPEC-63 maps to 4 techniques)
  P(TA0002 | T1059) = 0.85 (T1059 belongs to Execution + 1 other tactic)

  Chain probability = 1.0 × 0.80 × 0.75 × 0.85 = 0.51

Chain 2: CVE-2024-1234 → CWE-79 → CAPEC-18 → T1059 → TA0002
  Edge probabilities: [1.0, 0.60, 0.70, 0.85]
  Chain probability = 1.0 × 0.60 × 0.70 × 0.85 = 0.36

Overall P(TA0002 | CVE-2024-1234) = 0.51 + 0.36 = 0.87
```

---

### 5.2 Monte Carlo Confidence Interval

**Algorithm**: Beta distribution sampling with Wilson Score interval

**Process**:
1. For each edge in chain, model probability as Beta(α, β)
   - α = observed edge count + 1
   - β = (total source edges - observed edge count) + 1

2. Sample 10,000 times:
   - Draw edge probability from Beta(α, β) for each edge
   - Multiply to get chain probability
   - Sum across all chains

3. Calculate Wilson Score 95% confidence interval:
   ```
   CI = (p̂ + z²/2n ± z√[p̂(1-p̂)/n + z²/4n²]) / (1 + z²/n)

   Where:
   - p̂ = sample mean probability
   - z = 1.96 (for 95% CI)
   - n = 10,000 (number of samples)
   ```

**Pseudocode**:
```python
def monte_carlo_confidence_interval(chains, num_samples=10000):
    samples = []

    for _ in range(num_samples):
        sample_prob = 0.0

        for chain in chains:
            # Sample each edge from Beta distribution
            sampled_edges = []
            for edge_prob in chain.edge_probabilities:
                alpha = edge_prob * 100  # Scale for Beta
                beta = (1 - edge_prob) * 100
                sampled_edge = np.random.beta(alpha, beta)
                sampled_edges.append(sampled_edge)

            # Multiply to get chain probability
            chain_prob = np.prod(sampled_edges)
            sample_prob += chain_prob

        samples.append(sample_prob)

    # Wilson Score interval
    p_hat = np.mean(samples)
    z = 1.96
    n = len(samples)

    denominator = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denominator
    margin = z * np.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2)) / denominator

    return (center - margin, center + margin)
```

---

### 5.3 GNN Link Prediction Algorithm

**Model**: 3-layer Graph Attention Network (GAT)

**Architecture**:
```
Input: Node features [num_nodes, 128] from Node2Vec embeddings
       Edge index [2, num_edges] from Neo4j relationships

Layer 1: GAT(128 → 128, heads=4, concat=True) → [num_nodes, 512]
         + ELU activation
         + Dropout(0.3)

Layer 2: GAT(512 → 128, heads=4, concat=True) → [num_nodes, 512]
         + ELU activation
         + Dropout(0.3)

Layer 3: GAT(512 → 64, heads=1, concat=False) → [num_nodes, 64]

Link Prediction MLP:
  Concatenate source + target embeddings → [128]
  Linear(128 → 64) + ReLU + Dropout(0.3)
  Linear(64 → 1) + Sigmoid → [probability]
```

**Training Algorithm**:
```
1. Split edges: 80% train, 10% validation, 10% test

2. Generate negative edges (non-existent links):
   - Sample random node pairs
   - Ensure they're not in true edge set
   - Match number of positive edges (1:1 ratio)

3. Training loop (100 epochs):
   For each epoch:
     a. Forward pass: compute node embeddings
     b. Predict positive and negative edges
     c. Loss = BCE(positive_pred, 1) + BCE(negative_pred, 0)
     d. Backpropagation + Adam optimizer
     e. Every 10 epochs: evaluate on validation set

4. Final evaluation on test set:
   - Threshold predictions at 0.5
   - Calculate: Precision, Recall, F1
   - Target: Precision ≥ 90%, Recall ≥ 85%
```

---

## Section 6: Performance Specifications

### 6.1 API Performance Requirements

| Endpoint | p50 Latency | p99 Latency | Timeout | Throughput |
|----------|-------------|-------------|---------|------------|
| POST /score_cve | < 1s | < 2s | 5s | 100 req/s |
| POST /score_batch | < 30s (for 1000 CVEs) | < 60s | 120s | 10 batch/s |
| GET /attack_surface | < 5s | < 10s | 30s | 20 req/s |
| GET /mitigations | < 200ms | < 500ms | 2s | 200 req/s |
| POST /equipment/import | < 5s (1000 assets) | < 15s | 60s | 5 req/s |

### 6.2 Database Performance

**Neo4j**:
- Query time (10-hop): < 500ms (p99)
- Cypher full-table scan: < 2s for 570K nodes
- Write throughput: 10,000 edges/second
- Memory: 16 GB RAM allocated

**PostgreSQL**:
- Query time (indexed): < 50ms
- Bulk insert: 5,000 rows/second
- Connection pool: 20 concurrent connections

**Qdrant**:
- Vector search (1000 vectors): < 100ms
- Insertion: 1,000 vectors/second
- Memory: 8 GB RAM for 1M vectors

### 6.3 Machine Learning Performance

**AttackChainScorer**:
- Single CVE scoring: < 2s (p99)
- Monte Carlo simulation (10K samples): < 3s
- Batch scoring (1000 CVEs): < 60s

**GNN Training**:
- Training time (100 epochs, 3.3M edges): < 4 hours on NVIDIA V100
- Inference time (single link prediction): < 10ms
- Model size: < 200 MB

### 6.4 Scalability Targets

**Year 1** (2025-2026):
- CVEs in Neo4j: 200,000
- Customers: 100
- Equipment records: 500,000
- API requests/day: 100,000

**Year 3** (2027-2028):
- CVEs: 500,000
- Customers: 1,000
- Equipment: 10,000,000
- API requests/day: 1,000,000

---

## Section 7: Security Specifications

### 7.1 Authentication and Authorization

**Authentication**: Clerk JWT tokens
- Token expiration: 1 hour
- Refresh tokens: 30 days
- Multi-factor authentication: Optional (enforced for admin roles)

**Authorization**: Role-Based Access Control (RBAC)

| Role | Permissions |
|------|-------------|
| **Admin** | All operations, user management, system configuration |
| **Analyst** | Read CVE data, score CVEs, generate reports, manage own equipment |
| **Read-Only** | View dashboards, read reports (no writes) |

**API Key Management**:
- Stored encrypted in PostgreSQL using `pgcrypto`
- Scoped to customer_id (multi-tenant isolation)
- Rate limited: 10,000 requests/hour
- Audit logging: All API calls logged with user_id, timestamp, IP

### 7.2 Data Encryption

**At Rest**:
- PostgreSQL: Transparent Data Encryption (TDE) with `pgcrypto`
- Neo4j: Encrypted EBS volumes (AWS) or LUKS (on-prem)
- Qdrant: Filesystem encryption
- MinIO: Server-side encryption (SSE-S3)

**In Transit**:
- All connections use TLS 1.3
- Certificate management: Let's Encrypt (auto-renewal)
- Internal Docker network: TLS mutual authentication

**Secrets Management**:
- Environment variables stored in Kubernetes Secrets (base64-encoded)
- Production: AWS Secrets Manager or HashiCorp Vault
- Never commit secrets to Git (pre-commit hook validation)

### 7.3 Input Validation

**CVE ID Validation**:
```python
import re

CVE_PATTERN = re.compile(r'^CVE-\d{4}-\d{4,7}$')

def validate_cve_id(cve_id: str):
    if not CVE_PATTERN.match(cve_id):
        raise ValueError(f"Invalid CVE ID format: {cve_id}")
```

**SQL Injection Prevention**:
- Always use parameterized queries (SQLAlchemy ORM, psycopg2 with `%s`)
- NEVER string concatenation for SQL

**Cypher Injection Prevention**:
```python
# ✅ SAFE: Parameterized query
query = "MATCH (cve:CVE {id: $cve_id}) RETURN cve"
session.run(query, cve_id=user_input)

# ❌ UNSAFE: String concatenation
query = f"MATCH (cve:CVE {{id: '{user_input}'}}) RETURN cve"
```

**XSS Prevention** (Frontend):
- React: Auto-escapes by default
- Sanitize user input with `DOMPurify` library
- Content Security Policy (CSP) headers

### 7.4 Audit Logging

**All operations logged to PostgreSQL `audit_log` table**:
```sql
INSERT INTO audit_log (user_id, action, resource_type, resource_id, ip_address, request_body, response_status)
VALUES ('user_123', 'score_cve', 'CVE', 'CVE-2024-1234', '192.168.1.10', '{"cve_id": "CVE-2024-1234"}', 200);
```

**Retention**: 1 year (configurable)
**Access**: Admin role only

---

## Section 8: Deployment Specifications

### 8.1 Development Environment

**Prerequisites**:
- Docker 24+ and Docker Compose 2.20+
- Node.js 20+ (for frontend)
- Python 3.11+ (for backend)
- Git 2.40+

**Setup Commands**:
```bash
# Clone repository
git clone https://github.com/aeon-dt/aeon-platform.git
cd aeon-platform

# Copy environment template
cp .env.example .env

# Edit .env with your secrets
vim .env

# Start all services
docker-compose up -d

# Initialize databases
docker exec aeon-postgres-dev psql -U postgres -d aeon -f /sql/init.sql
docker exec openspg-neo4j cypher-shell -u neo4j -p ${NEO4J_PASSWORD} -f /cypher/init.cypher

# Verify health
curl http://localhost:8000/api/health
curl http://localhost:3000/api/health
```

### 8.2 Staging Environment

**Infrastructure**: AWS (or Azure/GCP equivalent)

**Resources**:
- EC2 Instances: 3x t3.xlarge (4 vCPU, 16 GB RAM)
- RDS PostgreSQL: db.m6g.large (2 vCPU, 8 GB RAM)
- Neo4j: Self-hosted on EC2 m5.2xlarge (8 vCPU, 32 GB RAM)
- ELB: Application Load Balancer
- S3: Backups and static assets

**Deployment Process**:
```bash
# Build Docker images
docker build -t aeon-backend:staging ./backend
docker build -t aeon-frontend:staging ./frontend

# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REGISTRY}
docker push ${ECR_REGISTRY}/aeon-backend:staging
docker push ${ECR_REGISTRY}/aeon-frontend:staging

# Deploy with Docker Compose (or Kubernetes)
ssh ec2-user@staging.aeon-dt.com
docker-compose -f docker-compose.staging.yml pull
docker-compose -f docker-compose.staging.yml up -d

# Run smoke tests
curl https://staging.aeon-dt.com/api/health
pytest tests/integration/test_smoke.py
```

### 8.3 Production Environment (Kubernetes)

**Cluster**: AWS EKS (3 nodes: m5.2xlarge)

**Manifests** (`k8s/`):
```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aeon-backend
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aeon-backend
  template:
    metadata:
      labels:
        app: aeon-backend
    spec:
      containers:
      - name: backend
        image: ${ECR_REGISTRY}/aeon-backend:${VERSION}
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: aeon-secrets
              key: database_url
        - name: NEO4J_URI
          value: "bolt://neo4j-service:7687"
        resources:
          requests:
            cpu: "1"
            memory: "4Gi"
          limits:
            cpu: "2"
            memory: "8Gi"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Deployment**:
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres-statefulset.yaml
kubectl apply -f k8s/neo4j-statefulset.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n production
kubectl logs -f deployment/aeon-backend -n production

# Rollback if needed
kubectl rollout undo deployment/aeon-backend -n production
```

---

## Section 9: Testing Specifications

### 9.1 Unit Testing

**Framework**: pytest (backend), Jest (frontend)

**Coverage Target**: ≥ 80%

**Example Test** (AttackChainScorer):
```python
# File: backend/tests/test_attack_chain_scorer.py

import pytest
from src.intelligence.attack_chain_scorer import AttackChainScorer

@pytest.fixture
def scorer():
    return AttackChainScorer(
        neo4j_uri="bolt://localhost:7687",
        laplace_alpha=1.0,
        monte_carlo_samples=1000  # Reduced for test speed
    )

def test_score_cve_with_complete_chain(scorer):
    """Test scoring for CVE with complete semantic chain"""
    result = scorer.score_cve("CVE-2024-1234")

    assert result.cve_id == "CVE-2024-1234"
    assert 0.0 <= result.overall_probability <= 1.0
    assert len(result.chains) > 0
    assert result.confidence_interval[0] < result.confidence_interval[1]
    assert result.execution_time_ms > 0

def test_score_cve_invalid_id(scorer):
    """Test error handling for invalid CVE ID"""
    with pytest.raises(ValueError, match="No semantic chains found"):
        scorer.score_cve("CVE-9999-INVALID")

def test_monte_carlo_confidence_interval(scorer):
    """Test confidence interval calculation"""
    chains = [
        ChainPath(
            nodes=["CVE-2024-1", "CWE-79", "CAPEC-63", "T1059", "TA0002"],
            edge_probabilities=[0.95, 0.80, 0.75, 0.85],
            overall_probability=0.51
        )
    ]

    ci_lower, ci_upper = scorer._monte_carlo_confidence_interval(chains, "TA0002")

    assert ci_lower < 0.51 < ci_upper
    assert ci_upper - ci_lower < 0.2  # Reasonable interval width
```

### 9.2 Integration Testing

**Framework**: pytest with Docker fixtures

**Example Test** (Full Scoring Pipeline):
```python
# File: backend/tests/integration/test_scoring_pipeline.py

import pytest
import requests

@pytest.fixture(scope="module")
def api_base_url():
    """Assumes Docker Compose is running"""
    return "http://localhost:8000"

def test_full_scoring_pipeline(api_base_url):
    """Test end-to-end CVE scoring via API"""
    # Step 1: Score a CVE
    response = requests.post(
        f"{api_base_url}/api/v1/score_cve",
        json={
            "cve_id": "CVE-2024-1234",
            "customer_context": {"industry_sector": "healthcare"},
            "options": {"monte_carlo_samples": 1000}
        },
        headers={"Authorization": "Bearer test_token"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["cve_id"] == "CVE-2024-1234"
    assert "overall_probability" in data
    assert "chains" in data
    assert data["execution_time_ms"] < 3000  # p99 target

    # Step 2: Verify result stored in Qdrant cache
    # ... (query Qdrant to check cached result)
```

### 9.3 Performance Testing

**Framework**: Locust (Python load testing)

**Example Test**:
```python
# File: backend/tests/performance/locustfile.py

from locust import HttpUser, task, between

class AEONUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def score_single_cve(self):
        """Score single CVE (weighted task: 5x more likely)"""
        self.client.post(
            "/api/v1/score_cve",
            json={"cve_id": "CVE-2024-1234"},
            headers={"Authorization": "Bearer test_token"}
        )

    @task(1)
    def batch_score(self):
        """Batch score 100 CVEs"""
        cve_ids = [f"CVE-2024-{i:04d}" for i in range(1, 101)]
        self.client.post(
            "/api/v1/score_batch",
            json={"cve_ids": cve_ids},
            headers={"Authorization": "Bearer test_token"}
        )

# Run: locust -f locustfile.py --host=http://localhost:8000 --users=100 --spawn-rate=10
```

### 9.4 End-to-End Testing

**Framework**: Playwright (browser automation)

**Example Test** (Frontend):
```typescript
// File: frontend/tests/e2e/cve_scoring.spec.ts

import { test, expect } from '@playwright/test';

test('User can score a CVE and view results', async ({ page }) => {
  // Login (assumes Clerk test credentials)
  await page.goto('http://localhost:3000/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'TestPassword123');
  await page.click('button[type="submit"]');

  // Navigate to CVE scoring page
  await page.goto('http://localhost:3000/score');

  // Enter CVE ID
  await page.fill('input[name="cve_id"]', 'CVE-2024-1234');
  await page.click('button:has-text("Score CVE")');

  // Wait for results
  await page.waitForSelector('.score-result', { timeout: 5000 });

  // Verify result display
  const probability = await page.textContent('.overall-probability');
  expect(parseFloat(probability)).toBeGreaterThan(0);
  expect(parseFloat(probability)).toBeLessThan(1);

  // Verify confidence interval shown
  await expect(page.locator('.confidence-interval')).toBeVisible();

  // Verify primary tactic shown
  await expect(page.locator('.primary-tactic')).toContainText('TA00');
});
```

---

## Section 10: Monitoring Specifications

### 10.1 Application Metrics (Prometheus)

**Metrics to Track**:
```yaml
# API Request Metrics
http_requests_total{method, endpoint, status_code}
http_request_duration_seconds{method, endpoint, quantile}

# Database Metrics
neo4j_query_duration_seconds{query_type, quantile}
postgres_connections_active
qdrant_vector_search_latency_ms{collection, quantile}

# Business Metrics
cve_scores_generated_total
semantic_chains_completed_total
equipment_imported_total

# Error Metrics
api_errors_total{endpoint, error_type}
job_failures_total{job_type}
```

**Prometheus Configuration** (`prometheus.yml`):
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'aeon-backend'
    static_configs:
      - targets: ['backend:8000']

  - job_name: 'neo4j'
    static_configs:
      - targets: ['openspg-neo4j:2004']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
```

### 10.2 Dashboards (Grafana)

**Dashboard: API Performance**
- Panels:
  - Request rate (req/s) over time
  - Latency heatmap (p50, p90, p99, p99.9)
  - Error rate (%) by endpoint
  - Top 10 slowest endpoints

**Dashboard: Database Health**
- Panels:
  - Neo4j query performance
  - PostgreSQL connection pool usage
  - Qdrant vector search latency
  - Database disk usage

**Dashboard: Business KPIs**
- Panels:
  - CVEs scored today
  - Average scoring time
  - Semantic chain completeness (%)
  - McKenney's 8 questions answerability

### 10.3 Alerting (PagerDuty)

**Critical Alerts**:
```yaml
groups:
  - name: critical_alerts
    interval: 1m
    rules:
      - alert: APIDown
        expr: up{job="aeon-backend"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "AEON Backend API is down"

      - alert: DatabaseConnectionFailure
        expr: postgres_connections_active < 1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "PostgreSQL connection pool empty"

      - alert: HighErrorRate
        expr: rate(api_errors_total[5m]) > 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "API error rate > 10 errors/min"

      - alert: ClerkAuthFailure
        expr: rate(auth_failures_total[1m]) > 5
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "CLERK AUTH FAILURE (Constitutional violation!)"
```

### 10.4 Log Aggregation (ELK Stack)

**Elasticsearch Indices**:
- `aeon-backend-logs-*`: FastAPI application logs
- `aeon-frontend-logs-*`: Next.js logs
- `aeon-audit-logs-*`: PostgreSQL audit logs (from `audit_log` table)

**Logstash Pipeline**:
```conf
input {
  file {
    path => "/var/log/aeon/backend.log"
    type => "backend"
  }
}

filter {
  if [type] == "backend" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
    }
    date {
      match => [ "timestamp", "ISO8601" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "aeon-backend-logs-%{+YYYY.MM.dd}"
  }
}
```

**Kibana Dashboards**:
- Error log analysis (group by error type)
- Slow query logs (queries > 1s)
- User activity logs (API calls per user)

---

## Appendix A: Environment Variables

**Required Environment Variables** (`.env` file):
```bash
# PostgreSQL
POSTGRES_PASSWORD=CHANGEME_strong_password_123

# Neo4j
NEO4J_PASSWORD=CHANGEME_neo4j_password_456

# Clerk Authentication
CLERK_PUBLISHABLE_KEY=pk_test_XXXXXXXXXXXXX
CLERK_SECRET_KEY=sk_test_YYYYYYYYYYYYYYY

# NVD API
NVD_API_KEY=your_nvd_api_key_here

# Qdrant (optional, uses default if not set)
QDRANT_API_KEY=

# AWS (for production)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
```

---

## Appendix B: Code Structure

```
aeon-platform/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── score_cve.py
│   │   │   │   ├── batch_score.py
│   │   │   │   └── equipment.py
│   │   │   └── dependencies.py
│   │   ├── intelligence/
│   │   │   ├── attack_chain_scorer.py
│   │   │   ├── gnn_link_predictor.py
│   │   │   └── train_gnn.py
│   │   ├── integrations/
│   │   │   ├── nvd_integration.py
│   │   │   └── attack_integration.py
│   │   ├── auth/
│   │   │   └── clerk_auth.py
│   │   └── main.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── performance/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── middleware.ts
│   ├── Dockerfile
│   └── package.json
├── k8s/
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── ingress.yaml
├── docker-compose.yml
├── .env.example
└── README.md
```

---

**Document Control**:
- **Approved By**: [Pending technical review]
- **Review Cycle**: Quarterly
- **Next Review**: 2026-02-12
- **Change Log**:
  - v1.0.0 (2025-11-12): Initial technical specifications

**END OF TECHNICAL SPECIFICATIONS**

