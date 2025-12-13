# AEON ICE - Unimplemented API Catalog

**Document ID**: UNIMPLEMENTED_API_CATALOG_2025-12-12
**Generated**: 2025-12-12
**Total APIs**: 196
**Source**: Phase B2, B3, B4, B5 Documentation

---

## Executive Summary

### API Distribution by Phase

| Phase | Enhancement | Endpoints | Status |
|-------|-------------|-----------|--------|
| **B2** | E15 Vendor Equipment | 28 | ✅ IMPLEMENTED |
| **B2** | E03 SBOM Analysis | 32 | ✅ IMPLEMENTED |
| **B2** | Semantic Search | 5 | ✅ IMPLEMENTED |
| **B3** | E04 Threat Intelligence | 27 | ❌ NOT IMPLEMENTED |
| **B3** | E05 Risk Scoring | 26 | ❌ NOT IMPLEMENTED |
| **B3** | E06 Remediation Workflow | 29 | ❌ NOT IMPLEMENTED |
| **B4** | E07 Compliance Mapping | 30 | ❌ NOT IMPLEMENTED |
| **B4** | E08 Automated Scanning | 30 | ❌ NOT IMPLEMENTED |
| **B4** | E09 Alert Management | 30 | ❌ NOT IMPLEMENTED |
| **B5** | E10 Economic Impact | 26 | ❌ NOT IMPLEMENTED |
| **B5** | E11 Demographics | 24 | ❌ NOT IMPLEMENTED |
| **B5** | E12 Prioritization | 28 | ❌ NOT IMPLEMENTED |
| **TOTAL** | **12 APIs** | **315** | **65 IMPLEMENTED, 250 NOT IMPLEMENTED** |

---

## Phase B3: Advanced Security Intelligence (82 Endpoints - NOT IMPLEMENTED)

### E04: Threat Intelligence Correlation API (27 endpoints)

**Base Path**: `/api/v2/threat-intel`
**Purpose**: Correlate APT groups, campaigns, MITRE ATT&CK, and IOCs

#### APT Tracking (7 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/actors` | Create threat actor | `{actor_type, name, motivation, origin_country}` | `{threat_actor_id, threat_score}` |
| `GET` | `/actors/{actor_id}` | Get threat actor details | - | `{threat_actor_id, name, aliases, ttps}` |
| `GET` | `/actors/search` | Search threat actors | `?query=<text>&limit=10` | `{total_results, results[]}` |
| `GET` | `/actors/by-sector/{sector}` | Actors targeting sector | - | `{results[{threat_actor_id, target_sectors}]}` |
| `GET` | `/actors/active` | Get active threat actors | `?limit=20` | `{results[{is_active, last_activity}]}` |
| `GET` | `/actors/{actor_id}/ttps` | Get actor TTPs | - | `{ttps[], mitre_techniques[]}` |
| `GET` | `/actors/{actor_id}/campaigns` | Get actor campaigns | - | `{campaigns[{campaign_id, target_sectors}]}` |

#### Campaign Management (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/campaigns` | Create campaign | `{name, threat_actors[], start_date, target_sectors[]}` | `{campaign_id, status}` |
| `GET` | `/campaigns/{campaign_id}` | Get campaign details | - | `{campaign_id, threat_actors[], iocs[]}` |
| `GET` | `/campaigns/active` | Get active campaigns | `?limit=20` | `{results[{campaign_id, is_active}]}` |
| `GET` | `/campaigns/by-sector/{sector}` | Campaigns by sector | - | `{results[{target_sectors[]}]}` |
| `GET` | `/campaigns/{campaign_id}/timeline` | Campaign timeline | - | `{events[{date, activity}]}` |

#### MITRE ATT&CK (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/mitre/techniques` | Map MITRE technique | `{technique_id, tactic, detection_rules[]}` | `{technique_id, coverage_status}` |
| `GET` | `/mitre/techniques/{technique_id}` | Get technique details | - | `{technique_id, tactic, sub_techniques[]}` |
| `GET` | `/mitre/coverage` | Get detection coverage | - | `{total_techniques, covered, coverage_percentage}` |
| `GET` | `/mitre/gaps` | Identify coverage gaps | - | `{uncovered_techniques[], critical_gaps[]}` |
| `GET` | `/mitre/techniques/by-actor/{actor_id}` | Actor's techniques | - | `{actor_id, techniques[]}` |

#### IOC Management (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/iocs` | Create IOC | `{ioc_type, value, threat_actor_id, confidence}` | `{ioc_id, reputation_score}` |
| `GET` | `/iocs/{ioc_id}` | Get IOC details | - | `{ioc_id, ioc_type, value, first_seen}` |
| `GET` | `/iocs/search` | Search IOCs | `?value=<ip>&type=IP` | `{results[{ioc_type, value}]}` |
| `GET` | `/iocs/by-campaign/{campaign_id}` | IOCs by campaign | - | `{campaign_id, iocs[]}` |
| `GET` | `/iocs/recent` | Recent IOCs | `?hours=24&limit=50` | `{results[{ioc_id, detected_at}]}` |

#### Threat Feeds (3 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/feeds` | Register threat feed | `{feed_name, feed_url, feed_type, update_frequency}` | `{feed_id, status}` |
| `GET` | `/feeds` | List threat feeds | - | `{feeds[{feed_id, last_update}]}` |
| `POST` | `/feeds/{feed_id}/sync` | Sync threat feed | - | `{synced_items, new_iocs}` |

#### Dashboard (2 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/summary` | Threat intel summary | - | `{total_actors, active_campaigns, critical_iocs}` |
| `GET` | `/dashboard/trending` | Trending threats | `?timeframe=7d` | `{trending_actors[], emerging_campaigns[]}` |

---

### E05: Risk Scoring Engine API (26 endpoints)

**Base Path**: `/api/v2/risk`
**Purpose**: Multi-factor risk calculation, asset criticality, exposure scoring

#### Risk Scoring (7 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/scores/calculate` | Calculate risk score | `{entity_id, vulnerability_score, threat_score, exposure_score}` | `{risk_score, risk_level}` |
| `GET` | `/scores/{entity_id}` | Get risk score | - | `{entity_id, risk_score, risk_level, factors[]}` |
| `GET` | `/scores/high-risk` | Get high-risk entities | `?threshold=7.5&limit=50` | `{results[{entity_id, risk_score}]}` |
| `GET` | `/scores/by-category/{category}` | Risk scores by category | - | `{category, avg_risk_score, entities[]}` |
| `POST` | `/scores/recalculate` | Recalculate all scores | - | `{recalculated_count, avg_score}` |
| `GET` | `/scores/trending` | Risk score trends | `?period=30d` | `{trending_up[], trending_down[]}` |
| `GET` | `/scores/{entity_id}/history` | Risk score history | - | `{entity_id, history[{date, score}]}` |

#### Asset Criticality (6 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/assets/criticality` | Set asset criticality | `{asset_id, criticality_level, rto_hours, impact_level}` | `{asset_id, criticality_level}` |
| `GET` | `/assets/{asset_id}/criticality` | Get asset criticality | - | `{asset_id, criticality_level, rto_hours}` |
| `GET` | `/assets/mission-critical` | Mission-critical assets | - | `{results[{asset_id, criticality_level}]}` |
| `GET` | `/assets/by-criticality/{level}` | Assets by criticality | - | `{criticality_level, assets[]}` |
| `POST` | `/assets/{asset_id}/classify` | Classify asset | `{data_classification, business_impact}` | `{asset_id, classification}` |
| `GET` | `/assets/criticality/distribution` | Criticality distribution | - | `{mission_critical, critical, high, medium, low}` |

#### Exposure Scoring (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/exposure/calculate` | Calculate exposure | `{asset_id, internet_facing, attack_surface}` | `{exposure_score, exposure_level}` |
| `GET` | `/exposure/{asset_id}` | Get exposure score | - | `{asset_id, exposure_score, attack_surface}` |
| `GET` | `/exposure/internet-facing` | Internet-facing assets | - | `{results[{asset_id, exposure_score}]}` |
| `GET` | `/exposure/by-zone` | Exposure by network zone | `?zone=DMZ` | `{zone, avg_exposure, assets[]}` |
| `GET` | `/exposure/high-risk` | High exposure assets | `?threshold=7.0` | `{results[{asset_id, exposure_score}]}` |

#### Risk Aggregation (4 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/aggregate/by-vendor` | Risk by vendor | - | `{vendors[{vendor_id, avg_risk}]}` |
| `GET` | `/aggregate/by-sector` | Risk by sector | - | `{sectors[{sector, avg_risk}]}` |
| `GET` | `/aggregate/by-type` | Risk by entity type | - | `{entity_types[{type, avg_risk}]}` |
| `GET` | `/aggregate/customer-wide` | Customer-wide risk | - | `{total_entities, avg_risk_score, distribution}` |

#### Dashboard (4 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/summary` | Risk dashboard summary | - | `{total_entities, critical_count, avg_risk_score}` |
| `GET` | `/dashboard/risk-matrix` | Risk matrix view | - | `{matrix[{likelihood, impact, entities[]}]}` |
| `GET` | `/dashboard/heat-map` | Risk heat map | - | `{zones[{zone_name, risk_level}]}` |
| `GET` | `/dashboard/kpis` | Risk KPIs | - | `{kpis[{metric, value, threshold}]}` |

---

### E06: Remediation Workflow API (29 endpoints)

**Base Path**: `/api/v2/remediation`
**Purpose**: Track remediation tasks, SLA compliance, MTTR metrics

#### Task Management (11 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/tasks` | Create remediation task | `{title, cve_id, priority, asset_ids[], assigned_to}` | `{task_id, sla_deadline}` |
| `GET` | `/tasks/{task_id}` | Get task details | - | `{task_id, status, priority, sla_status}` |
| `GET` | `/tasks` | List tasks | `?status=open&priority=critical` | `{results[{task_id, status}]}` |
| `PUT` | `/tasks/{task_id}` | Update task | `{status, progress_notes}` | `{task_id, status}` |
| `DELETE` | `/tasks/{task_id}` | Delete task | - | `{deleted: true}` |
| `GET` | `/tasks/overdue` | Get overdue tasks | - | `{results[{task_id, days_overdue}]}` |
| `GET` | `/tasks/by-priority/{priority}` | Tasks by priority | - | `{priority, tasks[]}` |
| `POST` | `/tasks/{task_id}/assign` | Assign task | `{assigned_to}` | `{task_id, assigned_to}` |
| `POST` | `/tasks/{task_id}/complete` | Complete task | `{completion_notes}` | `{task_id, status: "verified"}` |
| `GET` | `/tasks/by-asset/{asset_id}` | Tasks for asset | - | `{asset_id, tasks[]}` |
| `GET` | `/tasks/by-cve/{cve_id}` | Tasks for CVE | - | `{cve_id, tasks[]}` |

#### Plan Management (6 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/plans` | Create remediation plan | `{name, tasks[], phases[]}` | `{plan_id, total_tasks}` |
| `GET` | `/plans/{plan_id}` | Get plan details | - | `{plan_id, tasks[], completion_percentage}` |
| `GET` | `/plans` | List plans | `?status=active` | `{results[{plan_id, status}]}` |
| `PUT` | `/plans/{plan_id}` | Update plan | `{tasks[], phases[]}` | `{plan_id, updated_at}` |
| `DELETE` | `/plans/{plan_id}` | Delete plan | - | `{deleted: true}` |
| `GET` | `/plans/{plan_id}/progress` | Get plan progress | - | `{plan_id, completion_percentage, tasks_completed}` |

#### SLA Management (6 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/sla/policies` | Create SLA policy | `{severity, deadline_hours, escalation_levels[]}` | `{policy_id}` |
| `GET` | `/sla/policies` | List SLA policies | - | `{policies[{severity, deadline_hours}]}` |
| `GET` | `/sla/compliance` | Get SLA compliance | `?period=30d` | `{compliance_rate, breaches}` |
| `GET` | `/sla/breaches` | SLA breaches | - | `{results[{task_id, breach_hours}]}` |
| `GET` | `/sla/at-risk` | Tasks at SLA risk | - | `{results[{task_id, remaining_hours}]}` |
| `POST` | `/sla/{task_id}/extend` | Extend SLA deadline | `{extension_hours, reason}` | `{new_deadline}` |

#### Metrics (4 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/metrics/summary` | Remediation metrics | `?period=30d` | `{total_tasks, mttr_hours, sla_compliance_rate}` |
| `GET` | `/metrics/mttr` | Mean time to remediate | `?by_severity=true` | `{overall_mttr, by_severity{critical, high}}` |
| `GET` | `/metrics/backlog` | Backlog analysis | - | `{total_open, aging_buckets{}}` |
| `GET` | `/metrics/velocity` | Remediation velocity | `?period=7d` | `{tasks_per_day, completion_rate}` |

#### Dashboard (2 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/summary` | Remediation dashboard | - | `{open_tasks, overdue_tasks, sla_compliance}` |
| `GET` | `/dashboard/workload` | Team workload | - | `{teams[{team, open_tasks, avg_age}]}` |

---

## Phase B4: Compliance & Automation (90 Endpoints - NOT IMPLEMENTED)

### E07: Compliance Mapping API (30 endpoints)

**Base Path**: `/api/v2/compliance`
**Purpose**: Map regulatory compliance (NERC CIP, NIST CSF, ISO 27001)

#### Controls (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/controls` | Create compliance control | `{control_id, framework, requirements[], evidence[]}` | `{control_id, implementation_status}` |
| `GET` | `/controls/{control_id}` | Get control details | - | `{control_id, framework, maturity_level}` |
| `GET` | `/controls` | List controls | `?framework=NERC_CIP&status=implemented` | `{results[]}` |
| `PUT` | `/controls/{control_id}` | Update control | `{implementation_status, maturity_level}` | `{control_id, updated_at}` |
| `DELETE` | `/controls/{control_id}` | Delete control | - | `{deleted: true}` |

#### Mappings (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/mappings` | Create framework mapping | `{source_framework, target_framework, control_mappings[]}` | `{mapping_id}` |
| `GET` | `/mappings/{framework_a}/{framework_b}` | Get cross-framework mappings | - | `{mappings[{source_control, target_control}]}` |
| `GET` | `/mappings/validate` | Validate mappings | `?mapping_id=<id>` | `{valid: true, conflicts[]}` |
| `GET` | `/mappings/gaps` | Identify mapping gaps | `?framework=NIST_CSF` | `{unmapped_controls[]}` |
| `POST` | `/mappings/auto-map` | Auto-generate mappings | `{source_framework, target_framework}` | `{auto_mappings[], confidence_scores[]}` |

#### Assessments (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/assessments` | Create assessment | `{assessment_name, framework, scope{}, schedule{}}` | `{assessment_id, status}` |
| `GET` | `/assessments/{assessment_id}` | Get assessment details | - | `{assessment_id, controls_count, completion_percentage}` |
| `GET` | `/assessments` | List assessments | `?status=scheduled` | `{results[]}` |
| `PUT` | `/assessments/{assessment_id}` | Update assessment | `{status, findings[]}` | `{assessment_id, updated_at}` |
| `GET` | `/assessments/{assessment_id}/progress` | Assessment progress | - | `{completion_percentage, controls_assessed}` |

#### Evidence (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/evidence` | Upload evidence | `{control_id, document_type, file_data}` | `{evidence_id, upload_date}` |
| `GET` | `/evidence/{evidence_id}` | Get evidence details | - | `{evidence_id, control_id, document_type}` |
| `GET` | `/evidence/by-control/{control_id}` | Evidence for control | - | `{control_id, evidence_documents[]}` |
| `DELETE` | `/evidence/{evidence_id}` | Delete evidence | - | `{deleted: true}` |
| `GET` | `/evidence/expiring` | Expiring evidence | `?days=30` | `{results[{evidence_id, expiration_date}]}` |

#### Gaps (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/gaps` | Identify compliance gaps | `?framework=ISO_27001` | `{gaps[{control_id, gap_type}]}` |
| `GET` | `/gaps/by-framework/{framework}` | Gaps by framework | - | `{framework, gaps[]}` |
| `POST` | `/gaps/{gap_id}/remediate` | Create remediation task | `{assigned_to, due_date}` | `{remediation_task_id}` |
| `GET` | `/gaps/critical` | Critical gaps | - | `{results[{gap_id, risk_level}]}` |
| `GET` | `/gaps/trending` | Gap trends | `?period=90d` | `{closing_rate, new_gaps}` |

#### Dashboard (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/posture` | Compliance posture | `?frameworks=NERC_CIP,NIST_CSF` | `{overall_compliance, frameworks[]}` |
| `GET` | `/dashboard/summary` | Dashboard summary | - | `{frameworks_assessed, controls_total, compliance_score}` |
| `GET` | `/dashboard/maturity` | Maturity model | `?framework=NIST_CSF` | `{average_level, distribution{}}` |
| `GET` | `/dashboard/timeline` | Assessment timeline | - | `{upcoming_assessments[], overdue[]}` |
| `GET` | `/dashboard/executive` | Executive summary | - | `{compliance_score, key_findings[], recommendations[]}` |

---

### E08: Automated Scanning API (30 endpoints)

**Base Path**: `/api/v2/scanning`
**Purpose**: Orchestrate vulnerability scanning (Nessus, Qualys, OpenVAS, Nuclei)

#### Profiles (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/profiles` | Create scan profile | `{name, scanner, scan_type, settings{}}` | `{profile_id}` |
| `GET` | `/profiles/{profile_id}` | Get profile details | - | `{profile_id, scanner, settings{}}` |
| `GET` | `/profiles` | List scan profiles | `?scanner=NESSUS` | `{results[]}` |
| `PUT` | `/profiles/{profile_id}` | Update profile | `{settings{}}` | `{profile_id, updated_at}` |
| `DELETE` | `/profiles/{profile_id}` | Delete profile | - | `{deleted: true}` |

#### Schedules (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/schedules` | Create scan schedule | `{name, profile_id, cron_expression, targets{}}` | `{schedule_id}` |
| `GET` | `/schedules/{schedule_id}` | Get schedule details | - | `{schedule_id, next_run, frequency}` |
| `GET` | `/schedules` | List schedules | `?status=active` | `{results[]}` |
| `PUT` | `/schedules/{schedule_id}` | Update schedule | `{cron_expression, enabled}` | `{schedule_id}` |
| `DELETE` | `/schedules/{schedule_id}` | Delete schedule | - | `{deleted: true}` |

#### Jobs (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/jobs/start` | Start scan job | `{scan_name, scanner, profile_id, targets{}}` | `{job_id, status}` |
| `GET` | `/jobs/{job_id}` | Get job status | - | `{job_id, status, progress_percentage}` |
| `GET` | `/jobs` | List scan jobs | `?status=running` | `{results[]}` |
| `POST` | `/jobs/{job_id}/cancel` | Cancel scan job | - | `{job_id, status: "cancelled"}` |
| `GET` | `/jobs/{job_id}/progress` | Real-time progress | - | `{job_id, scanned_hosts, findings_count}` |

#### Findings (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/findings` | List findings | `?severity=CRITICAL,HIGH&status=OPEN` | `{results[]}` |
| `GET` | `/findings/{finding_id}` | Get finding details | - | `{finding_id, severity, cvss_score}` |
| `POST` | `/findings/{finding_id}/acknowledge` | Acknowledge finding | `{notes}` | `{finding_id, status: "acknowledged"}` |
| `GET` | `/findings/by-job/{job_id}` | Findings by job | - | `{job_id, findings[]}` |
| `GET` | `/findings/deduplication` | Deduplicate findings | `?job_ids=<ids>` | `{unique_findings, duplicates_removed}` |

#### Targets (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/targets` | Create target group | `{name, networks[], exclusions[]}` | `{target_id}` |
| `GET` | `/targets/{target_id}` | Get target details | - | `{target_id, networks[], estimated_hosts}` |
| `GET` | `/targets` | List targets | - | `{results[]}` |
| `PUT` | `/targets/{target_id}` | Update targets | `{networks[], exclusions[]}` | `{target_id}` |
| `DELETE` | `/targets/{target_id}` | Delete target group | - | `{deleted: true}` |

#### Dashboard (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/summary` | Scanning dashboard | - | `{active_scans, total_findings, critical_count}` |
| `GET` | `/dashboard/coverage` | Scan coverage | - | `{assets_scanned, last_scan_date, coverage_percentage}` |
| `GET` | `/dashboard/trends` | Finding trends | `?period=30d` | `{new_findings[], remediated[]}` |
| `GET` | `/dashboard/scanners` | Scanner status | - | `{scanners[{scanner, status, last_scan}]}` |
| `GET` | `/dashboard/performance` | Scan performance | - | `{avg_scan_duration, success_rate}` |

---

### E09: Alert Management API (30 endpoints)

**Base Path**: `/api/v2/alerts`
**Purpose**: Centralized security alert management and escalation

#### Alerts (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/alerts` | Create alert | `{alert_name, severity, category, source{}, details{}}` | `{alert_id, status}` |
| `GET` | `/alerts/{alert_id}` | Get alert details | - | `{alert_id, severity, status, sla_deadline}` |
| `GET` | `/alerts` | List alerts | `?severity=CRITICAL&status=NEW` | `{results[]}` |
| `PUT` | `/alerts/{alert_id}` | Update alert | `{status, notes}` | `{alert_id, updated_at}` |
| `POST` | `/alerts/{alert_id}/acknowledge` | Acknowledge alert | `{acknowledged_by, notes}` | `{alert_id, status: "acknowledged"}` |

#### Rules (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/rules` | Create alert rule | `{rule_name, conditions[], actions[]}` | `{rule_id}` |
| `GET` | `/rules/{rule_id}` | Get rule details | - | `{rule_id, conditions[], enabled}` |
| `GET` | `/rules` | List alert rules | `?enabled=true` | `{results[]}` |
| `PUT` | `/rules/{rule_id}` | Update rule | `{conditions[], actions[]}` | `{rule_id}` |
| `DELETE` | `/rules/{rule_id}` | Delete rule | - | `{deleted: true}` |

#### Notifications (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/notifications/channels` | Create notification channel | `{channel_type, configuration{}}` | `{channel_id}` |
| `GET` | `/notifications/channels` | List channels | - | `{channels[{channel_type, status}]}` |
| `POST` | `/notifications/send` | Send notification | `{alert_id, channel_ids[], message}` | `{sent: true, delivery_status[]}` |
| `GET` | `/notifications/{notification_id}/delivery` | Get delivery status | - | `{notification_id, status, delivered_at}` |
| `POST` | `/notifications/test` | Test channel | `{channel_id}` | `{test_successful: true}` |

#### Escalations (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/escalations/policies` | Create escalation policy | `{policy_name, trigger_conditions{}, levels[]}` | `{policy_id}` |
| `GET` | `/escalations/policies` | List policies | - | `{policies[]}` |
| `GET` | `/escalations/{alert_id}` | Get alert escalation | - | `{alert_id, current_level, next_escalation}` |
| `POST` | `/escalations/{alert_id}/escalate` | Manual escalate | `{escalation_level, notify[]}` | `{alert_id, escalated_to}` |
| `GET` | `/escalations/pending` | Pending escalations | - | `{results[{alert_id, escalation_due}]}` |

#### Correlations (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/correlations/rules` | Create correlation rule | `{rule_name, pattern{}, time_window}` | `{rule_id}` |
| `GET` | `/correlations/{alert_id}` | Get correlated alerts | - | `{alert_id, related_alerts[]}` |
| `POST` | `/correlations/group` | Group alerts into incident | `{alert_ids[], incident_name}` | `{incident_id}` |
| `GET` | `/correlations/patterns` | Detected patterns | `?timeframe=24h` | `{patterns[{pattern_type, alert_count}]}` |
| `GET` | `/correlations/incidents` | List incidents | `?status=open` | `{incidents[{incident_id, alert_count}]}` |

#### Dashboard (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/summary` | Alert dashboard | `?timeframe=24h` | `{total_alerts, by_severity{}, sla_performance{}}` |
| `GET` | `/dashboard/real-time` | Real-time alerts | - | `{active_alerts[], recent_escalations[]}` |
| `GET` | `/dashboard/metrics` | Alert metrics | `?period=7d` | `{mttr, sla_compliance, false_positive_rate}` |
| `GET` | `/dashboard/sources` | Alert sources | - | `{sources[{source, count, critical_count}]}` |
| `GET` | `/dashboard/trends` | Alert trends | `?period=30d` | `{trend_data[], busiest_hour}` |

---

## Phase B5: Advanced Analytics & Reporting (78 Endpoints - NOT IMPLEMENTED)

### E10: Economic Impact Modeling API (26 endpoints)

**Base Path**: `/api/v2/economic-impact`
**Purpose**: ROI calculations, cost analysis, financial impact

#### Cost Analysis (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/costs/summary` | Cost summary dashboard | `?period=30d` | `{total_costs, by_category{}, period}` |
| `GET` | `/costs/by-category` | Costs by category | - | `{categories[{category, cost, percentage}]}` |
| `GET` | `/costs/{entity_id}/breakdown` | Entity cost breakdown | - | `{entity_id, direct_costs, indirect_costs}` |
| `POST` | `/costs/calculate` | Calculate scenario costs | `{scenario_type, factors{}}` | `{total_cost, direct, indirect, opportunity}` |
| `GET` | `/costs/historical` | Historical cost trends | `?period=90d` | `{trend_data[], direction}` |

#### ROI Calculations (6 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/roi/summary` | ROI summary | - | `{avg_roi, best_performers[], worst_performers[]}` |
| `GET` | `/roi/{investment_id}` | ROI details | - | `{investment_id, roi_percentage, npv, irr}` |
| `POST` | `/roi/calculate` | Calculate ROI | `{name, initial_investment, annual_benefits, years}` | `{roi_percentage, npv, irr, payback_period}` |
| `GET` | `/roi/by-category` | ROI by category | - | `{categories[{category, avg_roi}]}` |
| `GET` | `/roi/projections` | Future projections | `?years=5` | `{projections[{year, projected_roi}]}` |
| `POST` | `/roi/comparison` | Compare investments | `{investment_ids[]}` | `{comparison[{investment_id, roi, npv}]}` |

#### Business Value (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/value/metrics` | Business value metrics | - | `{metrics[{metric, value, unit}]}` |
| `GET` | `/value/{asset_id}/assessment` | Asset value assessment | - | `{asset_id, business_value, criticality}` |
| `POST` | `/value/calculate` | Calculate business value | `{asset_id, factors{}}` | `{business_value, confidence}` |
| `GET` | `/value/risk-adjusted` | Risk-adjusted value | - | `{assets[{asset_id, risk_adjusted_value}]}` |
| `GET` | `/value/by-sector` | Value by sector | - | `{sectors[{sector, total_value}]}` |

#### Impact Modeling (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/impact/model` | Model financial impact | `{scenario_type, variables{}}` | `{total_impact, direct, indirect}` |
| `GET` | `/impact/scenarios` | List scenarios | - | `{scenarios[{scenario_id, type}]}` |
| `POST` | `/impact/simulate` | Monte Carlo simulation | `{scenario_id, iterations}` | `{expected_impact, confidence_range}` |
| `GET` | `/impact/{scenario_id}/results` | Simulation results | - | `{scenario_id, results{}, confidence_intervals}` |
| `GET` | `/impact/historical` | Historical impacts | - | `{incidents[{incident_id, actual_cost, estimated}]}` |

#### Dashboard (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/summary` | Economic dashboard | - | `{total_costs, roi_metrics, value_metrics}` |
| `GET` | `/dashboard/trends` | Economic trends | `?period=90d` | `{cost_trends[], roi_trends[]}` |
| `GET` | `/dashboard/kpis` | Economic KPIs | - | `{kpis[{kpi, value, target}]}` |
| `GET` | `/dashboard/alerts` | Economic alerts | - | `{alerts[{alert_type, severity}]}` |
| `GET` | `/dashboard/executive` | Executive summary | - | `{key_metrics{}, recommendations[]}` |

---

### E11: Demographics Baseline API (24 endpoints)

**Base Path**: `/api/v2/demographics`
**Purpose**: Population analytics, workforce modeling, organizational structure

#### Population Metrics (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/population/summary` | Population summary | - | `{total_population, growth_rate, stability_index}` |
| `GET` | `/population/distribution` | Distribution metrics | - | `{by_age_group{}, by_tenure{}, by_department{}}` |
| `GET` | `/population/{org_unit_id}/profile` | Org unit profile | - | `{org_unit_id, demographics{}, trends{}}` |
| `GET` | `/population/trends` | Population trends | `?period=90d` | `{historical[], forecast[]}` |
| `POST` | `/population/query` | Custom query | `{filters{}, metrics[]}` | `{results[], aggregations{}}` |

#### Workforce Analytics (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/workforce/composition` | Workforce composition | - | `{by_role{}, by_department{}, turnover_rate}` |
| `GET` | `/workforce/skills` | Skills inventory | - | `{skills[{skill, count}], critical_skills[], gaps[]}` |
| `GET` | `/workforce/turnover` | Turnover analysis | - | `{turnover_rate, predictions[], high_risk[]}` |
| `GET` | `/workforce/{team_id}/profile` | Team profile | - | `{team_id, cohesion_score, diversity_index}` |
| `GET` | `/workforce/capacity` | Capacity analysis | - | `{total_capacity, utilization, overutilized[]}` |

#### Organization Structure (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/organization/hierarchy` | Org hierarchy | - | `{root_unit, children[recursive]}` |
| `GET` | `/organization/units` | List org units | - | `{units[{unit_id, employee_count}]}` |
| `GET` | `/organization/{unit_id}/details` | Unit details | - | `{unit_id, demographics{}, parent, children[]}` |
| `GET` | `/organization/relationships` | Inter-unit relationships | - | `{relationships[{from_unit, to_unit, type}]}` |
| `POST` | `/organization/analyze` | Org structure analysis | - | `{span_of_control, depth, bottlenecks[]}` |

#### Role Analysis (4 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/roles/distribution` | Role distribution | - | `{roles[{role, count, security_relevant}]}` |
| `GET` | `/roles/{role_id}/demographics` | Role demographics | - | `{role_id, demographics{}, avg_tenure}` |
| `GET` | `/roles/security-relevant` | Security-relevant roles | - | `{roles[{role, access_level}]}` |
| `GET` | `/roles/access-patterns` | Access patterns | - | `{normal_patterns[], anomalies[]}` |

#### Dashboard (5 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/summary` | Demographics dashboard | - | `{population_metrics{}, workforce_metrics{}}` |
| `GET` | `/dashboard/baseline` | Baseline metrics | - | `{stability_index, diversity_score, succession_coverage}` |
| `GET` | `/dashboard/indicators` | Key indicators | - | `{indicators[{name, value, threshold}]}` |
| `GET` | `/dashboard/alerts` | Demographic alerts | - | `{alerts[{alert_type, severity}]}` |
| `GET` | `/dashboard/trends` | Trend analysis | `?period=90d` | `{trends[], forecasts[]}` |

---

### E12: NOW-NEXT-NEVER Prioritization API (28 endpoints)

**Base Path**: `/api/v2/prioritization`
**Purpose**: Risk-adjusted prioritization framework

#### NOW Category (6 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/now/items` | NOW priority items | `?limit=50` | `{results[{item_id, priority_score}]}` |
| `GET` | `/now/summary` | NOW summary | - | `{total_now, critical_count, sla_breaches}` |
| `GET` | `/now/{item_id}/details` | NOW item details | - | `{item_id, urgency_factors[], deadline}` |
| `POST` | `/now/escalate` | Escalate to NOW | `{entity_id, reason}` | `{item_id, priority_category: "NOW"}` |
| `GET` | `/now/sla-status` | NOW SLA status | - | `{within_sla, at_risk, breached}` |
| `POST` | `/now/complete` | Complete NOW item | `{item_id, completion_notes}` | `{item_id, status: "completed"}` |

#### NEXT Category (6 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/next/items` | NEXT priority items | `?limit=100` | `{results[{item_id, priority_score}]}` |
| `GET` | `/next/summary` | NEXT summary | - | `{total_next, avg_priority_score}` |
| `GET` | `/next/{item_id}/details` | NEXT item details | - | `{item_id, risk_factors[], scheduled_for}` |
| `POST` | `/next/schedule` | Schedule for NEXT | `{entity_id, scheduled_date}` | `{item_id, priority_category: "NEXT"}` |
| `GET` | `/next/queue` | NEXT queue | `?order_by=priority_score` | `{queue[{item_id, position}]}` |
| `POST` | `/next/promote` | Promote to NOW | `{item_id, reason}` | `{item_id, priority_category: "NOW"}` |

#### NEVER Category (4 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/never/items` | NEVER priority items | - | `{results[{item_id, priority_score}]}` |
| `GET` | `/never/summary` | NEVER summary | - | `{total_never, accepted_risks}` |
| `POST` | `/never/classify` | Classify as NEVER | `{entity_id, justification}` | `{item_id, priority_category: "NEVER"}` |
| `POST` | `/never/reconsider` | Reconsider NEVER item | `{item_id}` | `{item_id, new_category}` |

#### Priority Scoring (6 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `POST` | `/score/calculate` | Calculate priority | `{entity_type, urgency_factors[], risk_factors[]}` | `{priority_score, priority_category}` |
| `GET` | `/score/{entity_id}/breakdown` | Score breakdown | - | `{entity_id, urgency, risk, impact, effort, roi}` |
| `GET` | `/score/factors` | List scoring factors | - | `{factors[{category, factors[]}]}` |
| `POST` | `/score/weights` | Configure weights | `{urgency_weight, risk_weight, impact_weight}` | `{weights{}, updated_at}` |
| `GET` | `/score/thresholds` | Priority thresholds | - | `{now_threshold, next_threshold}` |
| `POST` | `/score/batch` | Batch calculate | `{entities[]}` | `{results[{entity_id, priority_score}]}` |

#### Dashboard (6 endpoints)

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| `GET` | `/dashboard/summary` | Prioritization dashboard | - | `{now_count, next_count, never_count}` |
| `GET` | `/dashboard/distribution` | Priority distribution | - | `{distribution{now, next, never}}` |
| `GET` | `/dashboard/trends` | Priority trends | `?period=30d` | `{trending_up[], trending_down[]}` |
| `GET` | `/dashboard/efficiency` | Remediation efficiency | - | `{completion_rate, avg_time_to_remediate}` |
| `GET` | `/dashboard/backlog` | Backlog analysis | - | `{total_backlog, aging_buckets{}}` |
| `GET` | `/dashboard/executive` | Executive view | - | `{critical_now[], key_metrics{}}` |

---

## Storage Requirements

### Qdrant Collections Required

| Collection | Purpose | Dimensions | Phase |
|------------|---------|------------|-------|
| `ner11_threat_intel` | Threat actors, campaigns, IOCs | 384 | B3 |
| `ner11_risk_scoring` | Risk scores and criticality | 384 | B3 |
| `ner11_remediation` | Remediation tasks and actions | 384 | B3 |
| `compliance_controls` | Compliance control similarity | 384 | B4 |
| `scan_findings` | Vulnerability finding dedup | 384 | B4 |
| `security_alerts` | Alert correlation | 384 | B4 |
| `ner11_economic_impact` | Economic models | 384 | B5 |
| `ner11_demographics` | Population analytics | 384 | B5 |
| `ner11_prioritization` | Priority scoring | 384 | B5 |

**Total Collections**: 9 new collections (6 existing from B1/B2)

---

## Implementation Priority

### Tier 1 - Critical (30 days)
- E04 Threat Intelligence (27 endpoints)
- E05 Risk Scoring (26 endpoints)
- E12 Prioritization (28 endpoints)

### Tier 2 - High Priority (45 days)
- E06 Remediation Workflow (29 endpoints)
- E09 Alert Management (30 endpoints)

### Tier 3 - Compliance (60 days)
- E07 Compliance Mapping (30 endpoints)
- E08 Automated Scanning (30 endpoints)

### Tier 4 - Analytics (75 days)
- E10 Economic Impact (26 endpoints)
- E11 Demographics (24 endpoints)

---

## Integration Requirements

### Cross-API Dependencies

```
E03 SBOM → E04 Threat Intel (CVE → APT Groups)
E03 SBOM → E05 Risk (Component vulns → Risk factors)
E04 Threat Intel → E06 Remediation (Campaign IOCs → Tasks)
E05 Risk → E06 Remediation (High-risk → Prioritized tasks)
E08 Scanning → E05 Risk (Findings → Risk calculation)
E09 Alerts → E04 Threat Intel (Alert enrichment)
E09 Alerts → E06 Remediation (Auto-create tasks)
E07 Compliance → E03 SBOM (Component compliance)
E10 Economic → E12 Prioritization (ROI factors)
E11 Demographics → E12 Prioritization (Capacity)
E05 Risk → E12 Prioritization (Risk factors)
```

---

## Document Metadata

**Total Unimplemented APIs**: 250
**Phases Covered**: B3, B4, B5
**Qdrant Collections Required**: 9
**Estimated Implementation**: 75 days (phased)
**Storage Location**: Qdrant namespace `aeon-ice`, key `api-catalog`

**Generated**: 2025-12-12
**For**: AEON ICE Project Team
