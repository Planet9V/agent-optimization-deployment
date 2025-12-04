# Phase B3 API Reference - Threat Intelligence, Risk Scoring & Remediation

**Document ID**: API_PHASE_B3_REFERENCE_2025-12-04
**Generated**: 2025-12-04 19:30:00 UTC
**Status**: PRODUCTION READY
**Phase**: B3 - Advanced Security Intelligence

---

## Overview

Phase B3 adds three new API modules with 82 endpoints for threat intelligence correlation, risk scoring, and remediation workflow management.

### New APIs Summary

| API | Path | Endpoints | Purpose |
|-----|------|-----------|---------|
| E04 Threat Intelligence | `/api/v2/threat-intel` | 27 | APT tracking, MITRE ATT&CK, IOCs |
| E05 Risk Scoring | `/api/v2/risk` | 26 | Multi-factor risk, asset criticality |
| E06 Remediation Workflow | `/api/v2/remediation` | 29 | Fix tracking, SLA management |

**Total Phase B3 Endpoints**: 82

---

## E04: Threat Intelligence Correlation API

### Base Path
```
/api/v2/threat-intel
```

### Threat Actor Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/actors` | Create threat actor |
| GET | `/actors/{actor_id}` | Get threat actor by ID |
| GET | `/actors/search` | Search threat actors |
| GET | `/actors/active` | Get active threat actors |
| GET | `/actors/by-sector/{sector}` | Get actors targeting sector |
| GET | `/actors/{actor_id}/campaigns` | Get actor's campaigns |
| GET | `/actors/{actor_id}/cves` | Get CVEs used by actor |

### Campaign Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/campaigns` | Create campaign |
| GET | `/campaigns/{campaign_id}` | Get campaign details |
| GET | `/campaigns/search` | Search campaigns |
| GET | `/campaigns/active` | Get active campaigns |
| GET | `/campaigns/{campaign_id}/iocs` | Get campaign IOCs |

### MITRE ATT&CK Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/mitre/mappings` | Create MITRE mapping |
| GET | `/mitre/mappings/entity/{entity_type}/{entity_id}` | Get mappings for entity |
| GET | `/mitre/techniques/{technique_id}/actors` | Get actors using technique |
| GET | `/mitre/coverage` | Get detection coverage summary |
| GET | `/mitre/gaps` | Get coverage gaps |

### IOC Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/iocs` | Create IOC |
| POST | `/iocs/bulk` | Bulk import IOCs |
| GET | `/iocs/search` | Search IOCs |
| GET | `/iocs/active` | Get active IOCs |
| GET | `/iocs/by-type/{ioc_type}` | Get IOCs by type |

### Feed Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/feeds` | Create feed |
| GET | `/feeds` | List feeds |
| PUT | `/feeds/{feed_id}/refresh` | Trigger feed refresh |

### Dashboard

| Method | Path | Description |
|--------|------|-------------|
| GET | `/dashboard/summary` | Threat intel summary |

### TypeScript Interfaces

```typescript
// Threat Actor Types
type ActorType = 'apt' | 'criminal' | 'hacktivist' | 'state_sponsored' | 'insider' | 'unknown';
type ActorMotivation = 'espionage' | 'financial' | 'disruption' | 'destruction' | 'ideological';
type CampaignStatus = 'active' | 'concluded' | 'suspected';

interface ThreatActor {
  threat_actor_id: string;
  customer_id: string;
  name: string;
  aliases: string[];
  actor_type: ActorType;
  motivation: ActorMotivation;
  origin_country?: string;
  target_sectors: string[];
  target_regions: string[];
  active_since?: string;  // ISO date
  last_seen?: string;     // ISO date
  confidence_level: number;  // 0-1
  ttps: string[];         // MITRE ATT&CK IDs
  malware_used: string[];
  associated_campaigns: string[];
  associated_cves: string[];
  is_active: boolean;
  threat_score: number;   // 0-10 calculated
}

interface ThreatCampaign {
  campaign_id: string;
  customer_id: string;
  name: string;
  description?: string;
  threat_actor_id: string;
  start_date?: string;
  end_date?: string;
  status: CampaignStatus;
  target_sectors: string[];
  target_regions: string[];
  target_organizations: string[];
  attack_vectors: string[];
  objectives: string[];
  associated_cves: string[];
  iocs: IOC[];
  is_active: boolean;
  duration_days?: number;
}

interface MITREMapping {
  mapping_id: string;
  customer_id: string;
  entity_type: string;
  entity_id: string;
  technique_id: string;     // T1xxx
  tactic: string[];
  technique_name: string;
  sub_technique_id?: string;
  sub_technique_name?: string;
  detection_coverage: number;  // 0-1
  mitigation_status: 'not_covered' | 'partial' | 'covered' | 'monitoring_only';
  evidence: string[];
  confidence_score: number;
}

type IOCType = 'ip' | 'domain' | 'url' | 'hash_md5' | 'hash_sha1' | 'hash_sha256' | 'email' | 'file_name';

interface IOC {
  ioc_id: string;
  customer_id: string;
  ioc_type: IOCType;
  value: string;
  first_seen?: string;
  last_seen?: string;
  confidence: number;  // 0-1
  is_active: boolean;
  associated_campaigns: string[];
  associated_actors: string[];
  source?: string;
  threat_score: number;  // 0-10 calculated
}
```

---

## E05: Risk Scoring Engine API

### Base Path
```
/api/v2/risk
```

### Risk Score Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/scores` | Calculate and store risk score |
| GET | `/scores/{entity_type}/{entity_id}` | Get risk score for entity |
| GET | `/scores/high-risk` | Get high/critical risk entities |
| GET | `/scores/trending` | Get entities with degrading trends |
| GET | `/scores/search` | Search by risk criteria |
| POST | `/scores/recalculate/{entity_type}/{entity_id}` | Force recalculation |
| GET | `/scores/history/{entity_type}/{entity_id}` | Get score history |

### Asset Criticality Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/assets/criticality` | Set asset criticality |
| GET | `/assets/{asset_id}/criticality` | Get asset criticality |
| GET | `/assets/mission-critical` | Get mission-critical assets |
| GET | `/assets/by-criticality/{level}` | Get assets by criticality level |
| PUT | `/assets/{asset_id}/criticality` | Update criticality |
| GET | `/assets/criticality/summary` | Criticality distribution |

### Exposure Score Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/exposure` | Calculate exposure score |
| GET | `/exposure/{asset_id}` | Get asset exposure |
| GET | `/exposure/internet-facing` | Get internet-facing assets |
| GET | `/exposure/high-exposure` | Get high exposure assets |
| GET | `/exposure/attack-surface` | Attack surface summary |

### Aggregation Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/aggregation/by-vendor` | Risk aggregated by vendor |
| GET | `/aggregation/by-sector` | Risk aggregated by sector |
| GET | `/aggregation/by-asset-type` | Risk aggregated by asset type |
| GET | `/aggregation/{type}/{id}` | Get specific aggregation |

### Dashboard

| Method | Path | Description |
|--------|------|-------------|
| GET | `/dashboard/summary` | Risk dashboard summary |
| GET | `/dashboard/risk-matrix` | Risk matrix data |

### TypeScript Interfaces

```typescript
type RiskLevel = 'low' | 'medium' | 'high' | 'critical';
type RiskTrend = 'improving' | 'stable' | 'degrading';
type CriticalityLevel = 'low' | 'medium' | 'high' | 'critical' | 'mission_critical';
type BusinessImpact = 'minimal' | 'moderate' | 'significant' | 'severe' | 'catastrophic';
type DataClassification = 'public' | 'internal' | 'confidential' | 'restricted' | 'top_secret';

interface RiskScore {
  risk_score_id: string;
  customer_id: string;
  entity_type: string;
  entity_id: string;
  entity_name: string;
  overall_score: number;      // 0-10
  risk_level: RiskLevel;
  vulnerability_score: number; // 0-10
  threat_score: number;       // 0-10
  exposure_score: number;     // 0-10
  asset_score: number;        // 0-10
  calculation_date: string;
  confidence: number;         // 0-1
  contributing_factors: RiskFactor[];
  trend: RiskTrend;
  previous_score?: number;
  score_change?: number;
  is_critical: boolean;
  is_high_risk: boolean;
}

interface RiskFactor {
  factor_id: string;
  factor_type: 'vulnerability' | 'threat' | 'exposure' | 'asset' | 'compliance';
  name: string;
  description?: string;
  weight: number;     // 0-1
  score: number;      // 0-10
  evidence: string[];
  remediation_available: boolean;
}

interface AssetCriticality {
  asset_id: string;
  customer_id: string;
  asset_name: string;
  asset_type: string;
  criticality_level: CriticalityLevel;
  criticality_score: number;  // 0-10
  business_impact: BusinessImpact;
  data_classification: DataClassification;
  availability_requirement: 'standard' | 'important' | 'essential' | 'critical';
  dependencies: string[];
  dependent_services: string[];
  recovery_time_objective_hours?: number;
  recovery_point_objective_hours?: number;
  is_mission_critical: boolean;
  has_strict_rto: boolean;
}

interface ExposureScore {
  exposure_id: string;
  customer_id: string;
  asset_id: string;
  asset_name: string;
  external_exposure: boolean;
  internet_facing: boolean;
  open_ports: number[];
  exposed_services: string[];
  exposure_score: number;  // 0-10
  attack_surface_area: 'minimal' | 'limited' | 'moderate' | 'extensive' | 'critical';
  network_segment?: string;
  security_controls: string[];
  last_scan_date?: string;
  is_high_exposure: boolean;
  open_port_count: number;
}
```

---

## E06: Remediation Workflow API

### Base Path
```
/api/v2/remediation
```

### Task Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tasks` | Create remediation task |
| GET | `/tasks/{task_id}` | Get task details |
| GET | `/tasks/search` | Search tasks |
| GET | `/tasks/open` | Get open tasks |
| GET | `/tasks/overdue` | Get overdue tasks |
| GET | `/tasks/by-priority/{priority}` | Get tasks by priority |
| GET | `/tasks/by-status/{status}` | Get tasks by status |
| PUT | `/tasks/{task_id}/status` | Update task status |
| PUT | `/tasks/{task_id}/assign` | Assign task |
| GET | `/tasks/{task_id}/history` | Get task action history |

### Plan Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/plans` | Create remediation plan |
| GET | `/plans/{plan_id}` | Get plan details |
| GET | `/plans` | List plans |
| GET | `/plans/active` | Get active plans |
| PUT | `/plans/{plan_id}/status` | Update plan status |
| GET | `/plans/{plan_id}/progress` | Get plan progress |

### SLA Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/sla/policies` | Create SLA policy |
| GET | `/sla/policies` | List SLA policies |
| GET | `/sla/policies/{policy_id}` | Get SLA policy |
| PUT | `/sla/policies/{policy_id}` | Update SLA policy |
| GET | `/sla/breaches` | Get SLA breaches |
| GET | `/sla/at-risk` | Get tasks at risk of SLA breach |

### Metrics Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/metrics/summary` | Get remediation metrics summary |
| GET | `/metrics/mttr` | Mean time to remediate |
| GET | `/metrics/sla-compliance` | SLA compliance rate |
| GET | `/metrics/backlog` | Vulnerability backlog |
| GET | `/metrics/trends` | Remediation trends |

### Dashboard

| Method | Path | Description |
|--------|------|-------------|
| GET | `/dashboard/summary` | Remediation dashboard |
| GET | `/dashboard/workload` | Team workload distribution |

### TypeScript Interfaces

```typescript
type TaskType = 'patch' | 'upgrade' | 'configuration' | 'workaround' | 'mitigation' | 'replacement';
type TaskStatus = 'open' | 'in_progress' | 'pending_verification' | 'verified' | 'closed' | 'wont_fix' | 'false_positive';
type TaskPriority = 'low' | 'medium' | 'high' | 'critical' | 'emergency';
type SLAStatus = 'within_sla' | 'at_risk' | 'breached';

interface RemediationTask {
  task_id: string;
  customer_id: string;
  title: string;
  description?: string;
  vulnerability_id?: string;
  cve_id?: string;
  asset_ids: string[];
  task_type: TaskType;
  status: TaskStatus;
  priority: TaskPriority;
  severity_source: number;  // Original CVSS
  due_date?: string;
  assigned_to?: string;
  assigned_team?: string;
  created_by?: string;
  sla_deadline?: string;
  sla_status: SLAStatus;
  start_date?: string;
  completion_date?: string;
  verification_date?: string;
  effort_estimate_hours?: number;
  actual_effort_hours?: number;
  notes?: string;
  verification_notes?: string;
  is_overdue: boolean;
  is_critical_priority: boolean;
  is_completed: boolean;
}

interface RemediationPlan {
  plan_id: string;
  customer_id: string;
  name: string;
  description?: string;
  status: 'draft' | 'active' | 'completed' | 'cancelled';
  task_ids: string[];
  total_tasks: number;
  completed_tasks: number;
  start_date?: string;
  target_completion_date?: string;
  actual_completion_date?: string;
  owner?: string;
  stakeholders: string[];
  risk_reduction_target?: number;
  actual_risk_reduction?: number;
  completion_percentage: number;
  is_completed: boolean;
  is_on_track: boolean;
}

interface SLAPolicy {
  policy_id: string;
  customer_id: string;
  name: string;
  description?: string;
  severity_thresholds: {
    critical: number;  // hours
    high: number;
    medium: number;
    low: number;
  };
  escalation_levels: EscalationLevel[];
  working_hours_only: boolean;
  timezone: string;
  business_critical_multiplier: number;
  active: boolean;
}

interface EscalationLevel {
  level: number;
  threshold_percentage: number;  // % of SLA elapsed
  notify_roles: string[];
  notify_emails: string[];
  action: 'notify' | 'escalate_manager' | 'escalate_executive' | 'auto_assign';
}

interface RemediationMetrics {
  metrics_id: string;
  customer_id: string;
  period_start: string;
  period_end: string;
  total_tasks: number;
  completed_tasks: number;
  open_tasks: number;
  overdue_tasks: number;
  mttr_hours: number;  // Mean time to remediate
  mttr_by_severity: Record<string, number>;
  sla_compliance_rate: number;  // 0-1
  sla_breaches: number;
  tasks_by_status: Record<string, number>;
  tasks_by_priority: Record<string, number>;
  vulnerability_backlog: number;
  completion_rate: number;
  overdue_rate: number;
}
```

---

## Authentication

All Phase B3 endpoints require the `X-Customer-ID` header:

```typescript
headers: {
  'X-Customer-ID': 'your-customer-id'  // REQUIRED
}
```

---

## React Integration Example

```tsx
// hooks/useRiskScoring.ts
import { useState, useEffect } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function useHighRiskEntities(customerId: string) {
  const [entities, setEntities] = useState<RiskScore[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/api/v2/risk/scores/high-risk`, {
      headers: { 'X-Customer-ID': customerId }
    })
      .then(res => res.json())
      .then(data => setEntities(data.results))
      .finally(() => setLoading(false));
  }, [customerId]);

  return { entities, loading };
}

// hooks/useRemediationTasks.ts
export function useOverdueTasks(customerId: string) {
  const [tasks, setTasks] = useState<RemediationTask[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/api/v2/remediation/tasks/overdue`, {
      headers: { 'X-Customer-ID': customerId }
    })
      .then(res => res.json())
      .then(data => setTasks(data.results))
      .finally(() => setLoading(false));
  }, [customerId]);

  return { tasks, loading };
}

// hooks/useThreatActors.ts
export function useActiveThreatActors(customerId: string, sector?: string) {
  const [actors, setActors] = useState<ThreatActor[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    const url = sector
      ? `${API_BASE}/api/v2/threat-intel/actors/by-sector/${sector}`
      : `${API_BASE}/api/v2/threat-intel/actors/active`;

    fetch(url, { headers: { 'X-Customer-ID': customerId } })
      .then(res => res.json())
      .then(data => setActors(data.results))
      .finally(() => setLoading(false));
  }, [customerId, sector]);

  return { actors, loading };
}
```

---

## Qdrant Collections

| Collection | Vectors | Purpose |
|------------|---------|---------|
| `ner11_threat_intel` | 384-dim | Threat actors, campaigns, IOCs |
| `ner11_risk_scoring` | 384-dim | Risk scores, criticality, exposure |
| `ner11_remediation` | 384-dim | Tasks, plans, actions |

All use `sentence-transformers/all-MiniLM-L6-v2` for embeddings.

---

## Test Coverage

| API | Tests | Status |
|-----|-------|--------|
| E04 Threat Intelligence | 85/85 | PASSING |
| E05 Risk Scoring | 85/85 | PASSING |
| E06 Remediation Workflow | 85/85 | PASSING |

**Total Phase B3**: 255 tests passing

---

## Combined API Summary (Phases B1-B3)

| Phase | APIs | Endpoints | Tests |
|-------|------|-----------|-------|
| B1 | Customer Semantic Search | 5 | 17 |
| B2 | E15 Vendor + E03 SBOM | 60 | 209 |
| B3 | E04 Threat + E05 Risk + E06 Remediation | 82 | 255 |
| **Total** | **8 APIs** | **147 endpoints** | **481 tests** |

---

**Document**: API_PHASE_B3_REFERENCE_2025-12-04
**Generated**: 2025-12-04 19:30:00 UTC
**AEON Digital Twin Cybersecurity Platform**
