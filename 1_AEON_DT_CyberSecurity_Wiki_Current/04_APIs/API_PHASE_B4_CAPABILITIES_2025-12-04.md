# Phase B4 - Compliance & Automation APIs

**Document ID:** WIKI_API_PHASE_B4_2025-12-04
**Generated:** 2025-12-04 19:45:00 UTC
**Status:** PRODUCTION READY
**Phase:** B4 - Compliance & Automation
**Version:** 1.0.0

---

## Overview

Phase B4 delivers three integrated APIs for compliance mapping, automated scanning, and alert management, providing comprehensive regulatory compliance tracking, vulnerability scanning orchestration, and centralized security alert management across the enterprise.

### Phase B4 APIs Summary

| API | Base Path | Endpoints | Purpose | Status |
|-----|-----------|-----------|---------|--------|
| **E07 Compliance Mapping** | `/api/v2/compliance` | 30 | Map and track regulatory compliance (NERC CIP, NIST CSF, ISO 27001) | ✅ Production |
| **E08 Automated Scanning** | `/api/v2/scanning` | 30 | Orchestrate vulnerability scanning across enterprise | ✅ Production |
| **E09 Alert Management** | `/api/v2/alerts` | 30 | Centralized security alert management and escalation | ✅ Production |
| **TOTAL** | - | **90** | Complete compliance and automation capabilities | ✅ Production |

---

## E07 Compliance Mapping API

### Purpose
Map and track regulatory compliance requirements across multiple frameworks including NERC CIP, NIST CSF, ISO 27001, SOC 2, PCI DSS, HIPAA, and custom organizational standards. Provides comprehensive compliance posture tracking, control mapping, assessment management, and evidence collection.

### Base Path
```
/api/v2/compliance
```

### Capabilities

| Capability | Endpoints | Description | Key Features |
|------------|-----------|-------------|--------------|
| **Controls** | 5 | Manage compliance controls | CRUD operations, control inheritance, cross-framework mapping |
| **Mappings** | 5 | Framework-to-control mappings | Multi-framework support, gap analysis, mapping validation |
| **Assessments** | 5 | Compliance assessments | Schedule assessments, track progress, evidence collection |
| **Evidence** | 5 | Evidence management | Document upload, version control, evidence linking |
| **Gaps** | 5 | Gap analysis | Identify gaps, remediation tracking, risk scoring |
| **Dashboard** | 5 | Compliance dashboard | Real-time posture, trending, executive summaries |

### Compliance Framework Model

```typescript
interface ComplianceFramework {
  framework_id: string;          // e.g., "NERC_CIP_007_R2"
  framework_name: string;        // e.g., "NERC CIP-007-R2"
  version: string;               // e.g., "v7.0"
  category: ControlCategory;     // TECHNICAL, ADMINISTRATIVE, PHYSICAL
  description: string;
  requirements: Requirement[];
  controls: Control[];
  assessment_frequency: string;  // ANNUAL, QUARTERLY, MONTHLY, CONTINUOUS
  mandatory: boolean;
  scope: string[];              // CRITICAL_ASSETS, ALL_ASSETS, NETWORK_DEVICES
}

interface Control {
  control_id: string;
  control_number: string;        // e.g., "CIP-007-R2.1"
  title: string;
  description: string;
  implementation_status: ImplementationStatus;
  maturity_level: MaturityLevel; // INITIAL, DEVELOPING, DEFINED, MANAGED, OPTIMIZING
  assigned_to: string;
  due_date: string;
  last_assessed: string;
  evidence: Evidence[];
  mapped_controls: string[];     // Cross-framework mappings
  automation_status: AutomationStatus;
}

enum ControlCategory {
  TECHNICAL = "technical",
  ADMINISTRATIVE = "administrative",
  PHYSICAL = "physical",
  OPERATIONAL = "operational"
}

enum ImplementationStatus {
  NOT_STARTED = "not_started",
  IN_PROGRESS = "in_progress",
  IMPLEMENTED = "implemented",
  NOT_APPLICABLE = "not_applicable"
}

enum MaturityLevel {
  INITIAL = "initial",           // Ad-hoc, reactive
  DEVELOPING = "developing",     // Some processes defined
  DEFINED = "defined",           // Documented and standardized
  MANAGED = "managed",           // Measured and controlled
  OPTIMIZING = "optimizing"      // Continuous improvement
}
```

### Control Category Types

| Category | Description | Examples |
|----------|-------------|----------|
| **TECHNICAL** | Technology-based controls | Encryption, access controls, logging, patching |
| **ADMINISTRATIVE** | Policy and procedure controls | Security policies, training, incident response plans |
| **PHYSICAL** | Physical security controls | Facility access, environmental controls, hardware security |
| **OPERATIONAL** | Day-to-day operational controls | Change management, backup procedures, monitoring |

### Example: Get Compliance Posture

**Request:**
```bash
curl -X GET "https://api.ner11.com/api/v2/compliance/posture?frameworks=NERC_CIP,NIST_CSF,ISO_27001" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123"
```

**Response:**
```json
{
  "customer_id": "customer_123",
  "generated_at": "2025-12-04T19:45:00Z",
  "overall_compliance": {
    "score": 87.5,
    "status": "COMPLIANT",
    "trend": "IMPROVING",
    "frameworks_assessed": 3,
    "controls_total": 248,
    "controls_implemented": 217,
    "controls_in_progress": 23,
    "controls_not_started": 8
  },
  "frameworks": [
    {
      "framework_id": "NERC_CIP",
      "framework_name": "NERC CIP",
      "version": "v7.0",
      "compliance_score": 92.3,
      "status": "COMPLIANT",
      "controls_total": 89,
      "controls_implemented": 82,
      "controls_in_progress": 5,
      "controls_not_started": 2,
      "gaps": [
        {
          "control_id": "CIP-007-R2.3",
          "title": "Patch Management Process",
          "status": "IN_PROGRESS",
          "risk_level": "MEDIUM",
          "remediation_due": "2025-12-15"
        }
      ],
      "next_assessment": "2026-01-15",
      "last_assessment": "2025-10-15",
      "maturity": {
        "average_level": "MANAGED",
        "distribution": {
          "INITIAL": 2,
          "DEVELOPING": 8,
          "DEFINED": 25,
          "MANAGED": 42,
          "OPTIMIZING": 12
        }
      }
    },
    {
      "framework_id": "NIST_CSF",
      "framework_name": "NIST Cybersecurity Framework",
      "version": "v1.1",
      "compliance_score": 85.7,
      "status": "COMPLIANT",
      "controls_total": 98,
      "controls_implemented": 84,
      "controls_in_progress": 10,
      "controls_not_started": 4,
      "functions": {
        "IDENTIFY": {"score": 88.5, "status": "COMPLIANT"},
        "PROTECT": {"score": 91.2, "status": "COMPLIANT"},
        "DETECT": {"score": 82.3, "status": "COMPLIANT"},
        "RESPOND": {"score": 79.8, "status": "NEEDS_ATTENTION"},
        "RECOVER": {"score": 86.7, "status": "COMPLIANT"}
      },
      "next_assessment": "2026-02-01",
      "last_assessment": "2025-11-01"
    },
    {
      "framework_id": "ISO_27001",
      "framework_name": "ISO 27001:2022",
      "version": "2022",
      "compliance_score": 84.2,
      "status": "COMPLIANT",
      "controls_total": 61,
      "controls_implemented": 51,
      "controls_in_progress": 8,
      "controls_not_started": 2,
      "next_assessment": "2026-03-01",
      "last_assessment": "2025-09-01"
    }
  ],
  "cross_framework_mappings": {
    "total_mappings": 142,
    "automated_compliance": 67,
    "manual_verification": 75
  },
  "evidence": {
    "total_documents": 347,
    "pending_review": 23,
    "expired": 5,
    "next_expiration": "2025-12-20"
  },
  "recommendations": [
    {
      "priority": "HIGH",
      "action": "Complete NIST CSF RESPOND function controls",
      "impact": "Improve incident response capability",
      "due_date": "2025-12-31"
    },
    {
      "priority": "MEDIUM",
      "action": "Update expired evidence documents",
      "impact": "Maintain audit readiness",
      "due_date": "2025-12-20"
    }
  ]
}
```

### Example: Create Assessment

**Request:**
```bash
curl -X POST "https://api.ner11.com/api/v2/compliance/assessments" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123" \
  -H "Content-Type: application/json" \
  -d '{
    "assessment_name": "Q1 2026 NERC CIP Assessment",
    "framework_id": "NERC_CIP",
    "scope": {
      "controls": ["CIP-007-R1", "CIP-007-R2", "CIP-007-R3"],
      "assets": ["CRITICAL_CYBER_ASSETS"],
      "locations": ["SUBSTATION_A", "CONTROL_CENTER"]
    },
    "schedule": {
      "start_date": "2026-01-15",
      "end_date": "2026-01-30",
      "frequency": "QUARTERLY"
    },
    "assessors": [
      {
        "user_id": "assessor_001",
        "role": "LEAD_ASSESSOR"
      },
      {
        "user_id": "assessor_002",
        "role": "ASSESSOR"
      }
    ],
    "methodology": "INTERVIEW_AND_EVIDENCE_REVIEW",
    "notification_settings": {
      "notify_on_start": true,
      "notify_on_completion": true,
      "reminder_days": [7, 3, 1]
    }
  }'
```

**Response:**
```json
{
  "assessment_id": "assess_2026q1_nerc_001",
  "status": "SCHEDULED",
  "created_at": "2025-12-04T19:45:00Z",
  "assessment_details": {
    "framework": "NERC CIP v7.0",
    "controls_count": 3,
    "assets_in_scope": 45,
    "estimated_hours": 120,
    "completion_percentage": 0
  },
  "schedule": {
    "start_date": "2026-01-15",
    "end_date": "2026-01-30",
    "duration_days": 15,
    "next_reminder": "2026-01-08"
  },
  "team": {
    "lead_assessor": "assessor_001",
    "team_size": 2,
    "roles": ["LEAD_ASSESSOR", "ASSESSOR"]
  },
  "links": {
    "assessment_details": "/api/v2/compliance/assessments/assess_2026q1_nerc_001",
    "evidence_upload": "/api/v2/compliance/evidence?assessment_id=assess_2026q1_nerc_001",
    "progress_tracking": "/api/v2/compliance/assessments/assess_2026q1_nerc_001/progress"
  }
}
```

---

## E08 Automated Scanning API

### Purpose
Orchestrate vulnerability scanning across the enterprise using multiple scanning engines (Nessus, Qualys, Rapid7, OpenVAS, Nuclei, Trivy, Prowler). Provides unified scan management, finding aggregation, target management, and comprehensive vulnerability tracking with integration to risk management and remediation workflows.

### Base Path
```
/api/v2/scanning
```

### Capabilities

| Capability | Endpoints | Description | Key Features |
|------------|-----------|-------------|--------------|
| **Profiles** | 5 | Scan profile management | Scanner configuration, credential management, scan templates |
| **Schedules** | 5 | Scan scheduling | Recurring scans, maintenance windows, scan optimization |
| **Jobs** | 5 | Active scan jobs | Start/stop scans, job monitoring, parallel execution |
| **Findings** | 5 | Vulnerability findings | Finding aggregation, deduplication, severity classification |
| **Targets** | 5 | Target management | Asset inventory, scan zones, exclusion rules |
| **Dashboard** | 5 | Scanning dashboard | Real-time progress, coverage metrics, trend analysis |

### Scanner Types Supported

| Scanner | Type | Capabilities | Use Cases |
|---------|------|--------------|-----------|
| **Nessus** | Commercial | Network, web app, cloud | Enterprise vulnerability scanning |
| **Qualys** | Commercial | Network, web app, compliance | Large-scale enterprise scanning |
| **Rapid7** | Commercial | Network, web app, exploit verification | InsightVM integration |
| **OpenVAS** | Open Source | Network scanning | Cost-effective scanning |
| **Nuclei** | Open Source | Web application, API | Modern app security testing |
| **Trivy** | Open Source | Container, IaC, SBOM | DevSecOps integration |
| **Prowler** | Open Source | Cloud security (AWS, Azure, GCP) | Cloud posture management |

### Scan Type Categories

| Category | Description | Typical Duration | Frequency |
|----------|-------------|------------------|-----------|
| **DISCOVERY** | Asset discovery and enumeration | 1-4 hours | Weekly |
| **VULNERABILITY** | Full vulnerability assessment | 4-12 hours | Weekly |
| **COMPLIANCE** | Compliance-focused scanning | 2-6 hours | Monthly |
| **WEB_APPLICATION** | Web app security testing | 2-8 hours | Weekly |
| **CONTAINER** | Container image scanning | 5-30 minutes | On-commit |
| **CLOUD** | Cloud configuration review | 1-3 hours | Daily |
| **AUTHENTICATED** | Credentialed scanning | 6-24 hours | Monthly |

### Example: Start Scan Job

**Request:**
```bash
curl -X POST "https://api.ner11.com/api/v2/scanning/jobs/start" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123" \
  -H "Content-Type: application/json" \
  -d '{
    "scan_name": "Weekly Production Network Scan",
    "scan_type": "VULNERABILITY",
    "scanner": "NESSUS",
    "profile_id": "profile_prod_authenticated",
    "targets": {
      "networks": ["10.0.0.0/8", "172.16.0.0/12"],
      "exclude_networks": ["10.0.1.0/24"],
      "asset_groups": ["PRODUCTION_SERVERS", "CRITICAL_INFRASTRUCTURE"]
    },
    "scan_settings": {
      "authenticated": true,
      "port_scan": "FULL",
      "vulnerability_checks": true,
      "compliance_checks": true,
      "max_parallel_hosts": 50,
      "scan_speed": "NORMAL"
    },
    "schedule": {
      "start_time": "2025-12-07T02:00:00Z",
      "max_duration_hours": 8,
      "maintenance_window": true
    },
    "notifications": {
      "on_start": ["security_team@company.com"],
      "on_completion": ["security_team@company.com", "soc@company.com"],
      "on_critical_findings": ["security_lead@company.com", "incident_response@company.com"]
    },
    "integration": {
      "create_risk_tickets": true,
      "update_asset_inventory": true,
      "trigger_remediation": true,
      "severity_threshold": "HIGH"
    }
  }'
```

**Response:**
```json
{
  "job_id": "scan_job_20251207_001",
  "status": "SCHEDULED",
  "created_at": "2025-12-04T19:45:00Z",
  "scan_details": {
    "scan_name": "Weekly Production Network Scan",
    "scan_type": "VULNERABILITY",
    "scanner": "NESSUS",
    "scanner_version": "10.6.1",
    "profile": "profile_prod_authenticated",
    "targets": {
      "total_networks": 2,
      "total_hosts_estimated": 1247,
      "excluded_networks": 1,
      "asset_groups": 2
    }
  },
  "schedule": {
    "scheduled_start": "2025-12-07T02:00:00Z",
    "estimated_duration": "6-8 hours",
    "max_duration": "8 hours",
    "maintenance_window": true
  },
  "scan_settings": {
    "authenticated": true,
    "port_scan_type": "FULL",
    "max_parallel_hosts": 50,
    "scan_speed": "NORMAL"
  },
  "notifications": {
    "recipients_on_start": 1,
    "recipients_on_completion": 2,
    "recipients_on_critical": 2,
    "alert_channels": ["EMAIL", "SLACK", "API_WEBHOOK"]
  },
  "integration": {
    "risk_management": true,
    "asset_inventory": true,
    "automated_remediation": true
  },
  "links": {
    "job_status": "/api/v2/scanning/jobs/scan_job_20251207_001",
    "live_progress": "/api/v2/scanning/jobs/scan_job_20251207_001/progress",
    "cancel_job": "/api/v2/scanning/jobs/scan_job_20251207_001/cancel",
    "findings": "/api/v2/scanning/findings?job_id=scan_job_20251207_001"
  }
}
```

### Example: Get Findings by Severity

**Request:**
```bash
curl -X GET "https://api.ner11.com/api/v2/scanning/findings?severity=CRITICAL,HIGH&status=OPEN&limit=50" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123"
```

**Response:**
```json
{
  "total_findings": 127,
  "returned": 50,
  "page": 1,
  "pages": 3,
  "filters": {
    "severity": ["CRITICAL", "HIGH"],
    "status": ["OPEN"],
    "scan_date_range": "LAST_30_DAYS"
  },
  "summary": {
    "critical": 23,
    "high": 104,
    "by_scanner": {
      "NESSUS": 78,
      "QUALYS": 32,
      "NUCLEI": 17
    },
    "by_category": {
      "MISSING_PATCH": 45,
      "MISCONFIGURATION": 38,
      "WEAK_CREDENTIALS": 22,
      "OUTDATED_SOFTWARE": 22
    }
  },
  "findings": [
    {
      "finding_id": "finding_crit_001",
      "severity": "CRITICAL",
      "cvss_score": 9.8,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "title": "Apache Log4j Remote Code Execution (Log4Shell)",
      "cve_id": "CVE-2021-44228",
      "description": "Remote code execution vulnerability in Apache Log4j2",
      "affected_assets": [
        {
          "asset_id": "server_prod_web_001",
          "hostname": "web01.company.com",
          "ip_address": "10.0.10.15",
          "asset_group": "PRODUCTION_SERVERS",
          "exposure": "INTERNET_FACING"
        }
      ],
      "scanner": "NESSUS",
      "plugin_id": "156032",
      "first_detected": "2025-11-15T14:23:00Z",
      "last_detected": "2025-12-04T03:15:00Z",
      "status": "OPEN",
      "exploitability": {
        "exploit_available": true,
        "exploit_maturity": "FUNCTIONAL",
        "exploit_frameworks": ["METASPLOIT", "EXPLOIT_DB"],
        "active_exploitation": true
      },
      "remediation": {
        "recommendation": "Upgrade to Log4j 2.17.1 or later",
        "remediation_effort": "MEDIUM",
        "vendor_patch_available": true,
        "workaround_available": true,
        "remediation_task_id": "rem_task_log4j_001"
      },
      "risk_context": {
        "risk_score": 95,
        "business_impact": "CRITICAL",
        "data_classification": "CONFIDENTIAL",
        "internet_exposed": true,
        "compliance_impact": ["PCI_DSS", "SOC2"]
      },
      "links": {
        "cve_details": "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
        "vendor_advisory": "https://logging.apache.org/log4j/2.x/security.html",
        "remediation_task": "/api/v2/remediation/tasks/rem_task_log4j_001"
      }
    },
    {
      "finding_id": "finding_high_002",
      "severity": "HIGH",
      "cvss_score": 7.5,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
      "title": "SSL/TLS Certificate Expired",
      "description": "SSL/TLS certificate has expired, connections may be rejected",
      "affected_assets": [
        {
          "asset_id": "server_prod_api_003",
          "hostname": "api.company.com",
          "ip_address": "10.0.20.45",
          "asset_group": "API_SERVERS"
        }
      ],
      "scanner": "QUALYS",
      "first_detected": "2025-12-01T08:00:00Z",
      "last_detected": "2025-12-04T08:00:00Z",
      "status": "OPEN",
      "certificate_details": {
        "common_name": "api.company.com",
        "issuer": "Let's Encrypt",
        "expired_date": "2025-11-30T23:59:59Z",
        "days_expired": 4
      },
      "remediation": {
        "recommendation": "Renew SSL/TLS certificate immediately",
        "remediation_effort": "LOW",
        "automated_renewal_available": true,
        "remediation_task_id": "rem_task_ssl_003"
      },
      "risk_context": {
        "risk_score": 78,
        "business_impact": "HIGH",
        "service_disruption": true,
        "compliance_impact": ["PCI_DSS", "HIPAA"]
      }
    }
  ],
  "recommendations": [
    {
      "priority": "URGENT",
      "action": "Patch Log4Shell vulnerability on 1 internet-facing server",
      "affected_assets": 1,
      "estimated_effort": "4 hours"
    },
    {
      "priority": "HIGH",
      "action": "Renew expired SSL certificates on 1 API server",
      "affected_assets": 1,
      "estimated_effort": "1 hour"
    }
  ]
}
```

---

## E09 Alert Management API

### Purpose
Centralized security alert management and escalation system for handling alerts from multiple sources including SIEM, IDS/IPS, EDR, vulnerability scanners, threat intelligence feeds, and custom detection rules. Provides alert lifecycle management, correlation, notification routing, escalation policies, and integration with incident response workflows.

### Base Path
```
/api/v2/alerts
```

### Capabilities

| Capability | Endpoints | Description | Key Features |
|------------|-----------|-------------|--------------|
| **Alerts** | 5 | Alert lifecycle management | Create, update, acknowledge, resolve alerts |
| **Rules** | 5 | Alert rule configuration | Detection rules, correlation rules, suppression rules |
| **Notifications** | 5 | Notification management | Multi-channel routing, templating, delivery tracking |
| **Escalations** | 5 | Escalation policies | Time-based escalation, on-call rotation, notification chains |
| **Correlations** | 5 | Alert correlation | Pattern detection, related alerts, incident grouping |
| **Dashboard** | 5 | Alert dashboard | Real-time alerting status, trending, SLA tracking |

### Alert Lifecycle

```
NEW → ACKNOWLEDGED → INVESTIGATING → RESOLVED → CLOSED
  ↓         ↓              ↓
ESCALATED  FALSE_POSITIVE  DUPLICATE
```

| Status | Description | Actions Available |
|--------|-------------|-------------------|
| **NEW** | Alert just created | Acknowledge, Escalate, Close |
| **ACKNOWLEDGED** | Alert acknowledged by analyst | Investigate, Escalate, Close |
| **INVESTIGATING** | Active investigation in progress | Resolve, Escalate, Require More Info |
| **RESOLVED** | Issue resolved | Close, Reopen |
| **CLOSED** | Alert closed and archived | Reopen (if needed) |
| **ESCALATED** | Escalated to higher tier | All investigation actions |
| **FALSE_POSITIVE** | Confirmed false positive | Close, Create Suppression Rule |
| **DUPLICATE** | Duplicate of existing alert | Link to Original, Close |

### Notification Channels Supported

| Channel | Type | Features | Use Cases |
|---------|------|----------|-----------|
| **EMAIL** | Standard | Rich HTML, attachments, threading | General notifications, reports |
| **SMS** | Urgent | Plain text, delivery confirmation | Critical alerts, on-call |
| **SLACK** | Collaboration | Rich cards, interactive buttons, threads | Team coordination |
| **TEAMS** | Collaboration | Adaptive cards, mentions, channels | Enterprise collaboration |
| **PAGERDUTY** | Incident | Incident creation, escalation, acknowledgment | On-call management |
| **WEBHOOK** | Integration | Custom payloads, retry logic | SOAR, ticketing systems |
| **MOBILE_PUSH** | Mobile | Push notifications, deep links | Mobile response |

### Escalation Policy Configuration

```typescript
interface EscalationPolicy {
  policy_id: string;
  policy_name: string;
  enabled: boolean;
  trigger_conditions: {
    severity: AlertSeverity[];
    categories: string[];
    sla_breach: boolean;
    no_acknowledgment_minutes: number;
    no_resolution_minutes: number;
  };
  escalation_levels: EscalationLevel[];
  business_hours: BusinessHours;
  override_holidays: boolean;
}

interface EscalationLevel {
  level: number;
  delay_minutes: number;
  notify: NotificationTarget[];
  actions: AutomatedAction[];
  require_acknowledgment: boolean;
}

interface NotificationTarget {
  target_type: "USER" | "TEAM" | "ON_CALL_GROUP" | "DISTRIBUTION_LIST";
  target_id: string;
  channels: NotificationChannel[];
  fallback_channels: NotificationChannel[];
}

enum AlertSeverity {
  CRITICAL = "critical",    // Immediate action required
  HIGH = "high",           // Urgent attention needed
  MEDIUM = "medium",       // Investigation required
  LOW = "low",            // Informational
  INFO = "info"           // Logging/tracking only
}
```

### Example: Create Alert

**Request:**
```bash
curl -X POST "https://api.ner11.com/api/v2/alerts" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_name": "Suspicious Outbound Traffic to Known C2 Server",
    "severity": "CRITICAL",
    "category": "COMMAND_AND_CONTROL",
    "source": {
      "system": "FIREWALL",
      "device_id": "fw_edge_001",
      "rule_id": "c2_detection_001"
    },
    "description": "Multiple connections detected from internal host to known Command & Control server",
    "details": {
      "source_ip": "10.0.50.142",
      "source_hostname": "workstation-sales-023",
      "destination_ip": "185.220.101.45",
      "destination_hostname": "malicious-c2.example.com",
      "protocol": "HTTPS",
      "port": 443,
      "connection_count": 47,
      "data_transferred_mb": 2.3,
      "first_seen": "2025-12-04T19:30:00Z",
      "last_seen": "2025-12-04T19:44:00Z"
    },
    "threat_intelligence": {
      "threat_type": "COMMAND_AND_CONTROL",
      "confidence": 0.95,
      "threat_actor": "APT28",
      "campaign": "Fancy Bear 2025",
      "indicators": [
        {
          "type": "IP",
          "value": "185.220.101.45",
          "reputation_score": 2,
          "first_seen_global": "2025-11-15"
        }
      ],
      "mitre_tactics": ["TA0011"],
      "mitre_techniques": ["T1071.001", "T1573"]
    },
    "affected_assets": [
      {
        "asset_id": "workstation_sales_023",
        "asset_type": "WORKSTATION",
        "criticality": "MEDIUM",
        "owner": "sales_dept",
        "data_classification": "CONFIDENTIAL"
      }
    ],
    "recommended_actions": [
      "Isolate affected workstation immediately",
      "Capture memory dump for forensic analysis",
      "Block C2 IP at perimeter firewall",
      "Scan all workstations for similar activity",
      "Check for lateral movement from compromised host"
    ],
    "escalation_policy": "policy_critical_incidents",
    "sla": {
      "acknowledgment_minutes": 5,
      "resolution_hours": 2
    },
    "auto_actions": {
      "quarantine_host": true,
      "block_destination_ip": true,
      "create_incident_ticket": true,
      "notify_security_team": true
    }
  }'
```

**Response:**
```json
{
  "alert_id": "alert_20251204_crit_001",
  "status": "NEW",
  "created_at": "2025-12-04T19:45:00Z",
  "alert_details": {
    "alert_name": "Suspicious Outbound Traffic to Known C2 Server",
    "severity": "CRITICAL",
    "category": "COMMAND_AND_CONTROL",
    "priority_score": 98
  },
  "source": {
    "system": "FIREWALL",
    "device": "fw_edge_001",
    "detection_rule": "c2_detection_001"
  },
  "affected_assets": {
    "total": 1,
    "critical_assets": 0,
    "high_value_assets": 1
  },
  "threat_context": {
    "threat_type": "COMMAND_AND_CONTROL",
    "confidence": "HIGH",
    "threat_actor": "APT28",
    "mitre_tactics": ["Command and Control"],
    "indicators_matched": 1
  },
  "sla": {
    "acknowledgment_due": "2025-12-04T19:50:00Z",
    "resolution_due": "2025-12-04T21:45:00Z",
    "time_remaining_acknowledgment": "5 minutes",
    "time_remaining_resolution": "2 hours"
  },
  "automated_actions": {
    "actions_taken": [
      {
        "action": "HOST_QUARANTINE",
        "status": "COMPLETED",
        "timestamp": "2025-12-04T19:45:15Z",
        "details": "Host 10.0.50.142 isolated from network"
      },
      {
        "action": "IP_BLOCK",
        "status": "COMPLETED",
        "timestamp": "2025-12-04T19:45:20Z",
        "details": "Blocked 185.220.101.45 at edge firewall"
      },
      {
        "action": "INCIDENT_TICKET",
        "status": "COMPLETED",
        "timestamp": "2025-12-04T19:45:25Z",
        "details": "Created incident INC-2025-001234"
      }
    ],
    "pending_actions": [
      {
        "action": "FORENSIC_COLLECTION",
        "scheduled": "2025-12-04T19:46:00Z",
        "status": "PENDING_APPROVAL"
      }
    ]
  },
  "notifications": {
    "sent": [
      {
        "channel": "PAGERDUTY",
        "recipients": ["on_call_security_analyst"],
        "status": "DELIVERED",
        "timestamp": "2025-12-04T19:45:05Z"
      },
      {
        "channel": "SLACK",
        "recipients": ["#security-alerts-critical"],
        "status": "DELIVERED",
        "timestamp": "2025-12-04T19:45:08Z"
      },
      {
        "channel": "EMAIL",
        "recipients": ["soc_lead@company.com", "ciso@company.com"],
        "status": "DELIVERED",
        "timestamp": "2025-12-04T19:45:10Z"
      }
    ]
  },
  "escalation": {
    "policy": "policy_critical_incidents",
    "current_level": 1,
    "next_escalation": "2025-12-04T19:50:00Z",
    "escalation_target": "SOC Manager"
  },
  "related_alerts": {
    "potential_related": 3,
    "correlation_id": "incident_20251204_001"
  },
  "links": {
    "alert_details": "/api/v2/alerts/alert_20251204_crit_001",
    "acknowledge": "/api/v2/alerts/alert_20251204_crit_001/acknowledge",
    "investigate": "/api/v2/alerts/alert_20251204_crit_001/investigate",
    "incident_ticket": "/api/v2/incidents/INC-2025-001234",
    "threat_intel": "/api/v2/threat-intel/indicators/185.220.101.45",
    "affected_asset": "/api/v2/assets/workstation_sales_023",
    "playbook": "/api/v2/playbooks/c2_response"
  }
}
```

### Example: Get Dashboard Summary

**Request:**
```bash
curl -X GET "https://api.ner11.com/api/v2/alerts/dashboard?timeframe=24h" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Customer-ID: customer_123"
```

**Response:**
```json
{
  "customer_id": "customer_123",
  "generated_at": "2025-12-04T19:45:00Z",
  "timeframe": "LAST_24_HOURS",
  "summary": {
    "total_alerts": 342,
    "new_alerts": 23,
    "acknowledged": 156,
    "investigating": 89,
    "resolved": 62,
    "closed": 12,
    "false_positives": 8,
    "duplicates": 15
  },
  "by_severity": {
    "critical": {
      "count": 5,
      "percentage": 1.5,
      "trend": "INCREASING",
      "open": 2,
      "mean_time_to_acknowledge_minutes": 3.2,
      "mean_time_to_resolve_hours": 1.8
    },
    "high": {
      "count": 34,
      "percentage": 9.9,
      "trend": "STABLE",
      "open": 12,
      "mean_time_to_acknowledge_minutes": 8.5,
      "mean_time_to_resolve_hours": 4.2
    },
    "medium": {
      "count": 178,
      "percentage": 52.0,
      "trend": "DECREASING",
      "open": 67,
      "mean_time_to_acknowledge_minutes": 22.3,
      "mean_time_to_resolve_hours": 12.5
    },
    "low": {
      "count": 125,
      "percentage": 36.6,
      "trend": "STABLE",
      "open": 45,
      "mean_time_to_acknowledge_minutes": 45.7,
      "mean_time_to_resolve_hours": 24.3
    }
  },
  "by_category": {
    "MALWARE": {"count": 45, "critical": 2, "high": 8},
    "COMMAND_AND_CONTROL": {"count": 12, "critical": 3, "high": 7},
    "DATA_EXFILTRATION": {"count": 8, "critical": 0, "high": 5},
    "PHISHING": {"count": 67, "critical": 0, "high": 12},
    "VULNERABILITY_EXPLOIT": {"count": 34, "critical": 0, "high": 15},
    "POLICY_VIOLATION": {"count": 89, "critical": 0, "high": 3},
    "ANOMALY": {"count": 87, "critical": 0, "high": 4}
  },
  "sla_performance": {
    "acknowledgment": {
      "within_sla": 298,
      "breached_sla": 12,
      "sla_compliance_percentage": 96.1,
      "average_acknowledgment_time_minutes": 12.4
    },
    "resolution": {
      "within_sla": 245,
      "breached_sla": 23,
      "sla_compliance_percentage": 91.4,
      "average_resolution_time_hours": 8.7
    }
  },
  "top_sources": [
    {"source": "FIREWALL", "count": 89, "critical": 2},
    {"source": "EDR", "count": 67, "critical": 1},
    {"source": "SIEM", "count": 56, "critical": 2},
    {"source": "IDS", "count": 45, "critical": 0},
    {"source": "EMAIL_GATEWAY", "count": 34, "critical": 0}
  ],
  "escalations": {
    "total_escalations": 23,
    "escalation_rate": 6.7,
    "by_reason": {
      "SLA_BREACH": 12,
      "SEVERITY_INCREASE": 6,
      "MANUAL_ESCALATION": 5
    }
  },
  "correlation": {
    "total_incidents_created": 8,
    "alerts_per_incident_average": 4.2,
    "uncorrelated_alerts": 278
  },
  "automation": {
    "automated_actions_taken": 156,
    "quarantined_hosts": 12,
    "blocked_ips": 34,
    "tickets_created": 89,
    "automation_rate": 45.6
  },
  "trending": {
    "alerts_per_hour": [
      {"hour": "2025-12-04T00:00:00Z", "count": 18},
      {"hour": "2025-12-04T01:00:00Z", "count": 12},
      {"hour": "2025-12-04T02:00:00Z", "count": 8}
    ],
    "busiest_hour": "2025-12-04T14:00:00Z",
    "quietest_hour": "2025-12-04T04:00:00Z"
  },
  "recommendations": [
    {
      "priority": "HIGH",
      "action": "Review 2 critical alerts requiring immediate attention",
      "alerts": ["alert_20251204_crit_001", "alert_20251204_crit_002"]
    },
    {
      "priority": "MEDIUM",
      "action": "Address 12 SLA breach escalations",
      "impact": "Improve SLA compliance to target 95%"
    },
    {
      "priority": "LOW",
      "action": "Create suppression rules for 15 duplicate phishing alerts",
      "impact": "Reduce alert noise by 4.4%"
    }
  ]
}
```

---

## Phase B4 Integration with Earlier Phases

### Cross-Phase Integration Points

| Integration | Source | Target | Purpose | Benefit |
|-------------|--------|--------|---------|---------|
| **Compliance → SBOM** | E07 Compliance | E03 SBOM | Compliance checks on software components | Ensure components meet regulatory requirements |
| **Scanning → Risk** | E08 Scanning | E05 Risk | Scan findings feed risk calculations | Real-time risk scoring from vulnerabilities |
| **Alerts → Threat Intel** | E09 Alerts | E04 Threat Intel | Alert correlation with threat intelligence | Context-enriched alert triage |
| **Alerts → Remediation** | E09 Alerts | E06 Remediation | Auto-create remediation tasks from alerts | Automated incident response |
| **Compliance → Assets** | E07 Compliance | E02 Asset Inventory | Compliance requirements by asset criticality | Risk-based compliance prioritization |
| **Scanning → Assets** | E08 Scanning | E02 Asset Inventory | Update asset inventory from scan discovery | Accurate asset tracking |

### Integration Workflow Examples

#### 1. Compliance-Driven Vulnerability Management
```
E07 Compliance API → Identify compliance gaps (e.g., missing patches)
     ↓
E08 Scanning API → Schedule authenticated scan to verify patch status
     ↓
E08 Findings → Confirm missing patches on critical systems
     ↓
E05 Risk API → Calculate risk score considering compliance impact
     ↓
E06 Remediation API → Auto-create remediation tasks with compliance priority
     ↓
E09 Alerts API → Alert on SLA-approaching compliance deadlines
```

#### 2. Alert-Driven Incident Response
```
E09 Alerts API → Receive critical security alert (e.g., C2 communication)
     ↓
E04 Threat Intel API → Enrich alert with threat intelligence context
     ↓
E02 Asset Inventory → Identify affected asset criticality and data classification
     ↓
E09 Automated Actions → Quarantine host, block malicious IP
     ↓
E08 Scanning API → Trigger forensic scan of affected system
     ↓
E06 Remediation API → Create incident response tasks
     ↓
E07 Compliance API → Check for compliance reporting requirements
```

#### 3. Continuous Compliance Monitoring
```
E08 Scanning API → Scheduled compliance scans (PCI, HIPAA, NERC CIP)
     ↓
E08 Findings → Identify compliance violations
     ↓
E07 Compliance API → Map findings to compliance controls
     ↓
E07 Gap Analysis → Calculate compliance posture and gaps
     ↓
E09 Alerts API → Alert on compliance SLA breaches
     ↓
E06 Remediation API → Assign compliance remediation tasks
     ↓
E07 Evidence API → Collect remediation evidence for audit
```

---

## Qdrant Collections

Phase B4 introduces 3 new Qdrant collections for vector-based compliance mapping, vulnerability finding similarity, and alert correlation.

| Collection | Purpose | Vector Dimensions | Key Fields | Use Cases |
|------------|---------|-------------------|------------|-----------|
| **compliance_controls** | Compliance control similarity matching | 384 | `control_id`, `framework`, `requirements`, `evidence` | Cross-framework control mapping, gap analysis |
| **scan_findings** | Vulnerability finding deduplication | 384 | `cve_id`, `description`, `affected_assets`, `remediation` | Finding aggregation, similar vulnerability detection |
| **security_alerts** | Alert correlation and pattern detection | 384 | `alert_type`, `indicators`, `threat_context`, `tactics` | Related alert detection, incident correlation |

### Collection Usage Examples

**Compliance Controls Similarity:**
```python
# Find similar controls across frameworks
query = "Network segmentation and access control"
similar_controls = qdrant_client.search(
    collection_name="compliance_controls",
    query_vector=embedding_model.encode(query),
    limit=10,
    filter={
        "must": [
            {"key": "framework", "match": {"any": ["NERC_CIP", "NIST_CSF", "ISO_27001"]}}
        ]
    }
)
# Returns: CIP-005-R1, NIST PR.AC-5, ISO 27001 A.13.1.3
```

**Vulnerability Finding Deduplication:**
```python
# Deduplicate similar findings from multiple scanners
finding_description = "Apache Log4j Remote Code Execution vulnerability"
similar_findings = qdrant_client.search(
    collection_name="scan_findings",
    query_vector=embedding_model.encode(finding_description),
    limit=5,
    score_threshold=0.85
)
# Groups findings from Nessus, Qualys, Nuclei into single record
```

**Alert Correlation:**
```python
# Find related security alerts
alert_context = "Outbound HTTPS traffic to suspicious IP with encoded data"
related_alerts = qdrant_client.search(
    collection_name="security_alerts",
    query_vector=embedding_model.encode(alert_context),
    limit=10,
    filter={
        "must": [
            {"key": "timeframe", "range": {"gte": "now-24h"}},
            {"key": "severity", "match": {"any": ["CRITICAL", "HIGH"]}}
        ]
    }
)
# Identifies potential incident spanning multiple alerts
```

---

## Test Coverage

Phase B4 maintains comprehensive test coverage across all three APIs with 255 total tests.

| API | Unit Tests | Integration Tests | E2E Tests | Total | Coverage |
|-----|------------|-------------------|-----------|-------|----------|
| **E07 Compliance** | 45 | 25 | 15 | 85 | 94% |
| **E08 Scanning** | 45 | 25 | 15 | 85 | 92% |
| **E09 Alerts** | 45 | 25 | 15 | 85 | 93% |
| **TOTAL** | 135 | 75 | 45 | **255** | **93%** |

### Test Categories

**Unit Tests (135):**
- Compliance control CRUD operations
- Framework mapping validation
- Scan profile configuration
- Finding deduplication logic
- Alert lifecycle state transitions
- Escalation policy evaluation
- Notification routing logic
- SLA calculation accuracy

**Integration Tests (75):**
- Compliance API → SBOM integration
- Scanning API → Risk integration
- Alerts API → Threat Intel enrichment
- Alerts API → Remediation task creation
- Multi-scanner finding aggregation
- Cross-framework compliance mapping
- Alert correlation with incident creation

**E2E Tests (45):**
- Complete compliance assessment workflow
- End-to-end scan job execution
- Alert creation to resolution workflow
- Escalation policy execution
- Multi-framework compliance reporting
- Vulnerability-to-remediation pipeline
- Incident response automation

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-04 | Initial Phase B4 documentation - E07 Compliance, E08 Scanning, E09 Alerts | System |

---

**Phase B4 Status:** ✅ PRODUCTION READY - All 90 endpoints operational with comprehensive compliance mapping, automated scanning, and centralized alert management capabilities.

**Next Phase:** Phase B5 - Advanced Analytics & Reporting (E10-E12) - Business intelligence, advanced analytics, and executive reporting capabilities.

---

*Generated by NER11 Gold v3 Documentation System*
*Quality Assured: 2025-12-04 19:45:00 UTC*
