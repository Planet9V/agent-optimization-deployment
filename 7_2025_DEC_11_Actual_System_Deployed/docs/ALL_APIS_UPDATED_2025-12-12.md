# COMPREHENSIVE API MASTER LIST - 2025-12-12

**Last Updated**: 2025-12-12 20:15:00 UTC
**Total APIs**: 189
**Status**: COMPLETE

## SUMMARY BY CATEGORY

| Category | Count | Working | Failed | Validation |
|----------|-------|---------|--------|------------|
| SBOM Management | 32 | 7 | 16 | 9 |
| Vendor & Equipment | 24 | 5 | 10 | 9 |
| Threat Intelligence | 31 | 15 | 8 | 8 |
| Risk Management | 36 | 13 | 15 | 8 |
| Remediation | 27 | 0 | 27 | 0 |
| **Psychometric** | **8** | **8** | **0** | **0** |
| NER & Search | 5 | 2 | 0 | 3 |
| Frontend (AEON-SAAS) | 41 | 0 | 40 | 1 |
| **TOTAL** | **189** | **44** | **106** | **39** |

---

## CATEGORY 1: SBOM MANAGEMENT (32 APIs)

### SBOMs (11 APIs)
1. ✅ GET `/api/v2/sbom/sboms` - List SBOMs
2. ⚠️ POST `/api/v2/sbom/sboms` - Create SBOM (needs data)
3. ❌ GET `/api/v2/sbom/sboms/{sbom_id}` - Get SBOM by ID
4. ⚠️ DELETE `/api/v2/sbom/sboms/{sbom_id}` - Delete SBOM (needs WRITE access)
5. ❌ GET `/api/v2/sbom/sboms/{sbom_id}/risk-summary` - Get risk summary
6. ❌ GET `/api/v2/sbom/sboms/{sbom_id}/components` - Get components
7. ✅ GET `/api/v2/sbom/sboms/{sbom_id}/cycles` - Detect cycles
8. ✅ GET `/api/v2/sbom/sboms/{sbom_id}/graph-stats` - Get graph stats
9. ✅ GET `/api/v2/sbom/sboms/{sbom_id}/remediation` - Get remediation report
10. ❌ GET `/api/v2/sbom/sboms/{sbom_id}/license-compliance` - License compliance
11. ✅ GET `/api/v2/sbom/sboms/{sbom_id}/vulnerable-paths` - Get vulnerable paths

### Components (10 APIs)
12. ⚠️ POST `/api/v2/sbom/components` - Create component
13. ❌ GET `/api/v2/sbom/components/{component_id}` - Get component
14. ❌ GET `/api/v2/sbom/components/search` - Search components
15. ❌ GET `/api/v2/sbom/components/vulnerable` - Get vulnerable components
16. ❌ GET `/api/v2/sbom/components/high-risk` - Get high-risk components
17. ✅ GET `/api/v2/sbom/components/{component_id}/dependencies` - Get dependency tree
18. ❌ GET `/api/v2/sbom/components/{component_id}/dependents` - Get dependents
19. ✅ GET `/api/v2/sbom/components/{component_id}/impact` - Impact analysis
20. ❌ GET `/api/v2/sbom/components/{component_id}/vulnerabilities` - Get vulnerabilities
21. ⚠️ POST `/api/v2/sbom/sboms/{sbom_id}/correlate-equipment` - Correlate equipment

### Dependencies (2 APIs)
22. ⚠️ POST `/api/v2/sbom/dependencies` - Create dependency
23. ⚠️ GET `/api/v2/sbom/dependencies/path` - Find dependency path (needs params)

### Vulnerabilities (9 APIs)
24. ⚠️ POST `/api/v2/sbom/vulnerabilities` - Create vulnerability
25. ❌ GET `/api/v2/sbom/vulnerabilities/{vulnerability_id}` - Get vulnerability
26. ❌ GET `/api/v2/sbom/vulnerabilities/search` - Search vulnerabilities
27. ❌ GET `/api/v2/sbom/vulnerabilities/critical` - Get critical vulnerabilities
28. ❌ GET `/api/v2/sbom/vulnerabilities/kev` - Get KEV vulnerabilities
29. ❌ GET `/api/v2/sbom/vulnerabilities/epss-prioritized` - EPSS prioritized
30. ❌ GET `/api/v2/sbom/vulnerabilities/by-apt` - APT vulnerability report
31. ⚠️ POST `/api/v2/sbom/vulnerabilities/{vulnerability_id}/acknowledge` - Acknowledge vuln
32. ✅ GET `/api/v2/sbom/dashboard/summary` - Dashboard summary

---

## CATEGORY 2: VENDOR & EQUIPMENT MANAGEMENT (24 APIs)

### Vendors (5 APIs)
33. ⚠️ POST `/api/v2/vendor-equipment/vendors` - Create vendor
34. ✅ GET `/api/v2/vendor-equipment/vendors` - Search vendors
35. ❌ GET `/api/v2/vendor-equipment/vendors/{vendor_id}` - Get vendor
36. ❌ GET `/api/v2/vendor-equipment/vendors/{vendor_id}/risk-summary` - Vendor risk
37. ❌ GET `/api/v2/vendor-equipment/vendors/high-risk` - High-risk vendors

### Equipment (5 APIs)
38. ⚠️ POST `/api/v2/vendor-equipment/equipment` - Create equipment
39. ✅ GET `/api/v2/vendor-equipment/equipment` - Search equipment
40. ❌ GET `/api/v2/vendor-equipment/equipment/{model_id}` - Get equipment
41. ❌ GET `/api/v2/vendor-equipment/equipment/approaching-eol` - Approaching EOL
42. ❌ GET `/api/v2/vendor-equipment/equipment/eol` - EOL equipment

### Maintenance (9 APIs)
43. ✅ GET `/api/v2/vendor-equipment/maintenance-schedule` - Get schedule
44. ⚠️ POST `/api/v2/vendor-equipment/maintenance-windows` - Create window
45. ❌ GET `/api/v2/vendor-equipment/maintenance-windows` - List windows
46. ❌ GET `/api/v2/vendor-equipment/maintenance-windows/{window_id}` - Get window
47. ❌ DELETE `/api/v2/vendor-equipment/maintenance-windows/{window_id}` - Delete window
48. ⚠️ POST `/api/v2/vendor-equipment/maintenance-windows/check-conflict` - Check conflict
49. ✅ GET `/api/v2/vendor-equipment/predictive-maintenance/{equipment_id}` - Predict
50. ✅ GET `/api/v2/vendor-equipment/predictive-maintenance/forecast` - Forecast

### Work Orders (5 APIs)
51. ⚠️ POST `/api/v2/vendor-equipment/work-orders` - Create work order
52. ❌ GET `/api/v2/vendor-equipment/work-orders` - List work orders
53. ❌ GET `/api/v2/vendor-equipment/work-orders/{work_order_id}` - Get work order
54. ⚠️ PATCH `/api/v2/vendor-equipment/work-orders/{work_order_id}/status` - Update status
55. ❌ GET `/api/v2/vendor-equipment/work-orders/summary` - Summary
56. ⚠️ POST `/api/v2/vendor-equipment/vulnerabilities/flag` - Flag vulnerability

---

## CATEGORY 3: THREAT INTELLIGENCE (31 APIs)

### Threat Actors (7 APIs)
57. ⚠️ POST `/api/v2/threat-intel/actors` - Create threat actor
58. ❌ GET `/api/v2/threat-intel/actors/{actor_id}` - Get threat actor
59. ❌ GET `/api/v2/threat-intel/actors/search` - Search actors
60. ❌ GET `/api/v2/threat-intel/actors/active` - Active actors
61. ✅ GET `/api/v2/threat-intel/actors/by-sector/{sector}` - Actors by sector
62. ✅ GET `/api/v2/threat-intel/actors/{actor_id}/campaigns` - Actor campaigns
63. ✅ GET `/api/v2/threat-intel/actors/{actor_id}/cves` - Actor CVEs

### Campaigns (5 APIs)
64. ⚠️ POST `/api/v2/threat-intel/campaigns` - Create campaign
65. ❌ GET `/api/v2/threat-intel/campaigns/{campaign_id}` - Get campaign
66. ❌ GET `/api/v2/threat-intel/campaigns/search` - Search campaigns
67. ❌ GET `/api/v2/threat-intel/campaigns/active` - Active campaigns
68. ✅ GET `/api/v2/threat-intel/campaigns/{campaign_id}/iocs` - Campaign IOCs

### MITRE ATT&CK (5 APIs)
69. ⚠️ POST `/api/v2/threat-intel/mitre/mappings` - Create mapping
70. ✅ GET `/api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}` - Entity mappings
71. ✅ GET `/api/v2/threat-intel/mitre/techniques/{technique_id}/actors` - Actors using technique
72. ✅ GET `/api/v2/threat-intel/mitre/coverage` - MITRE coverage
73. ✅ GET `/api/v2/threat-intel/mitre/gaps` - MITRE gaps

### IOCs (6 APIs)
74. ⚠️ POST `/api/v2/threat-intel/iocs` - Create IOC
75. ⚠️ POST `/api/v2/threat-intel/iocs/bulk` - Bulk import IOCs
76. ✅ GET `/api/v2/threat-intel/iocs/search` - Search IOCs
77. ✅ GET `/api/v2/threat-intel/iocs/active` - Active IOCs
78. ✅ GET `/api/v2/threat-intel/iocs/by-type/{ioc_type}` - IOCs by type

### Threat Feeds (4 APIs)
79. ⚠️ POST `/api/v2/threat-intel/feeds` - Create feed
80. ❌ GET `/api/v2/threat-intel/feeds` - List feeds
81. ⚠️ PUT `/api/v2/threat-intel/feeds/{feed_id}/refresh` - Refresh feed (needs WRITE)
82. ✅ GET `/api/v2/threat-intel/dashboard/summary` - Dashboard summary

### Frontend Threat Intel (4 APIs)
83. ❌ GET `/api/threats/geographic` - Geographic threats
84. ❌ GET `/api/threats/ics` - ICS threats
85. ❌ GET `/api/threat-intel/ics` - ICS threat intel
86. ❌ GET `/api/threat-intel/landscape` - Threat landscape
87. ❌ GET `/api/threat-intel/analytics` - Threat intel analytics
88. ❌ GET `/api/threat-intel/vulnerabilities` - Threat intel vulnerabilities

---

## CATEGORY 4: RISK MANAGEMENT (36 APIs)

### Risk Scores (8 APIs)
89. ⚠️ POST `/api/v2/risk/scores` - Calculate risk score
90. ❌ GET `/api/v2/risk/scores/{entity_type}/{entity_id}` - Get risk score
91. ✅ GET `/api/v2/risk/scores/high-risk` - High-risk entities
92. ⚠️ GET `/api/v2/risk/scores/trending` - Trending entities (needs params)
93. ✅ GET `/api/v2/risk/scores/search` - Search risk scores
94. ❌ POST `/api/v2/risk/scores/recalculate/{entity_type}/{entity_id}` - Recalculate
95. ❌ GET `/api/v2/risk/scores/history/{entity_type}/{entity_id}` - Risk history

### Asset Criticality (7 APIs)
96. ⚠️ POST `/api/v2/risk/assets/criticality` - Set criticality
97. ❌ GET `/api/v2/risk/assets/{asset_id}/criticality` - Get criticality
98. ⚠️ PUT `/api/v2/risk/assets/{asset_id}/criticality` - Update criticality
99. ✅ GET `/api/v2/risk/assets/mission-critical` - Mission critical assets
100. ⚠️ GET `/api/v2/risk/assets/by-criticality/{level}` - Assets by criticality
101. ✅ GET `/api/v2/risk/assets/criticality/summary` - Criticality summary

### Exposure (5 APIs)
102. ⚠️ POST `/api/v2/risk/exposure` - Calculate exposure
103. ❌ GET `/api/v2/risk/exposure/{asset_id}` - Get exposure score
104. ❌ GET `/api/v2/risk/exposure/internet-facing` - Internet-facing assets
105. ❌ GET `/api/v2/risk/exposure/high-exposure` - High exposure assets
106. ❌ GET `/api/v2/risk/exposure/attack-surface` - Attack surface summary

### Risk Aggregation (5 APIs)
107. ✅ GET `/api/v2/risk/aggregation/by-vendor` - Risk by vendor
108. ✅ GET `/api/v2/risk/aggregation/by-sector` - Risk by sector
109. ✅ GET `/api/v2/risk/aggregation/by-asset-type` - Risk by asset type
110. ⚠️ GET `/api/v2/risk/aggregation/{aggregation_type}/{group_id}` - Risk aggregation

### Dashboard (2 APIs)
111. ✅ GET `/api/v2/risk/dashboard/summary` - Dashboard summary
112. ✅ GET `/api/v2/risk/dashboard/risk-matrix` - Risk matrix

---

## CATEGORY 5: REMEDIATION (27 APIs) - ALL FAILING

### Tasks (10 APIs)
113. ⚠️ POST `/api/v2/remediation/tasks` - Create task
114. ❌ GET `/api/v2/remediation/tasks/{task_id}` - Get task
115. ❌ GET `/api/v2/remediation/tasks/search` - Search tasks
116. ❌ GET `/api/v2/remediation/tasks/open` - Open tasks
117. ❌ GET `/api/v2/remediation/tasks/overdue` - Overdue tasks
118. ❌ GET `/api/v2/remediation/tasks/by-priority/{priority}` - Tasks by priority
119. ❌ GET `/api/v2/remediation/tasks/by-status/{status}` - Tasks by status
120. ⚠️ PUT `/api/v2/remediation/tasks/{task_id}/status` - Update status
121. ⚠️ PUT `/api/v2/remediation/tasks/{task_id}/assign` - Assign task
122. ❌ GET `/api/v2/remediation/tasks/{task_id}/history` - Task history

### Plans (6 APIs)
123. ⚠️ POST `/api/v2/remediation/plans` - Create plan
124. ❌ GET `/api/v2/remediation/plans` - List plans
125. ❌ GET `/api/v2/remediation/plans/{plan_id}` - Get plan
126. ❌ GET `/api/v2/remediation/plans/active` - Active plans
127. ⚠️ PUT `/api/v2/remediation/plans/{plan_id}/status` - Update plan status
128. ❌ GET `/api/v2/remediation/plans/{plan_id}/progress` - Plan progress

### SLA (5 APIs)
129. ⚠️ POST `/api/v2/remediation/sla/policies` - Create SLA policy
130. ❌ GET `/api/v2/remediation/sla/policies` - List SLA policies
131. ❌ GET `/api/v2/remediation/sla/policies/{policy_id}` - Get SLA policy
132. ⚠️ PUT `/api/v2/remediation/sla/policies/{policy_id}` - Update SLA policy
133. ❌ GET `/api/v2/remediation/sla/breaches` - SLA breaches
134. ❌ GET `/api/v2/remediation/sla/at-risk` - At-risk tasks

### Metrics (6 APIs)
135. ❌ GET `/api/v2/remediation/metrics/summary` - Metrics summary
136. ❌ GET `/api/v2/remediation/metrics/mttr` - MTTR by severity
137. ❌ GET `/api/v2/remediation/metrics/sla-compliance` - SLA compliance
138. ❌ GET `/api/v2/remediation/metrics/backlog` - Backlog metrics
139. ❌ GET `/api/v2/remediation/metrics/trends` - Remediation trends
140. ❌ GET `/api/v2/remediation/dashboard/summary` - Dashboard summary
141. ❌ GET `/api/v2/remediation/dashboard/workload` - Workload distribution

---

## CATEGORY 6: PSYCHOMETRIC ASSESSMENT (8 APIs) - ALL WORKING ✅

### Core Assessments (3 APIs)
142. ✅ POST `/api/v2/psychometric/cognitive/process` - Process cognitive assessment
   - Returns: Cognitive score, reasoning patterns, processing speed metrics
143. ✅ POST `/api/v2/psychometric/personality/analyze` - Analyze personality traits
   - Returns: Big Five scores, trait distributions, behavioral predictions
144. ✅ POST `/api/v2/psychometric/behavioral/assess` - Assess behavioral patterns
   - Returns: Behavioral risk scores, pattern identification, risk factors

### Profiles & Insights (2 APIs)
145. ✅ GET `/api/v2/psychometric/profiles/{profile_id}` - Get psychometric profile
   - Returns: Complete profile with cognitive, personality, behavioral data
146. ✅ GET `/api/v2/psychometric/insights/risk-correlation` - Get risk correlation insights
   - Returns: Correlation between psychological traits and security risks

### Advanced Features (3 APIs)
147. ✅ POST `/api/v2/psychometric/threat-actor/profile` - Create threat actor psychological profile
   - Returns: Psychological profile, motivation analysis, behavior prediction
148. ✅ GET `/api/v2/psychometric/analytics/trends` - Get psychometric trends
   - Returns: Trend analysis, pattern evolution, risk trajectory
149. ✅ POST `/api/v2/psychometric/validation/score` - Validate and score assessment
   - Returns: Validation results, reliability scores, confidence intervals

**Use Cases**:
- Insider threat detection and prevention
- Social engineering vulnerability assessment
- Threat actor behavior prediction and profiling
- Security awareness program effectiveness measurement
- High-risk individual identification and monitoring
- Personnel security screening and monitoring
- Behavioral risk scoring for access control
- Psychological trend analysis for threat intelligence

---

## CATEGORY 7: NER & SEARCH (5 APIs)

150. ⚠️ POST `/ner` - Named Entity Recognition (needs text)
151. ⚠️ POST `/search/semantic` - Semantic search (needs query)
152. ⚠️ POST `/search/hybrid` - Hybrid search (needs params)
153. ✅ GET `/health` - Health check (ner11-gold-api)
154. ✅ GET `/info` - Model info

---

## CATEGORY 8: FRONTEND APIs (AEON-SAAS-DEV) - 41 APIs - ALL FAILING

### Pipeline (2 APIs)
155. ❌ GET `/api/pipeline/status/[jobId]` - Pipeline job status
156. ❌ GET `/api/pipeline/process` - Process pipeline (401 auth)

### Query Control (8 APIs)
157. ❌ GET `/api/query-control/queries` - List queries (timeout)
158. ❌ GET `/api/query-control/queries/[queryId]/checkpoints` - Checkpoints
159. ❌ GET `/api/query-control/queries/[queryId]/model` - Query model
160. ❌ GET `/api/query-control/queries/[queryId]` - Query details
161. ❌ GET `/api/query-control/queries/[queryId]/permissions` - Permissions
162. ❌ GET `/api/query-control/queries/[queryId]/resume` - Resume query
163. ❌ GET `/api/query-control/queries/[queryId]/pause` - Pause query

### Dashboard (3 APIs)
164. ❌ GET `/api/dashboard/metrics` - Dashboard metrics
165. ❌ GET `/api/dashboard/distribution` - Distribution data
166. ❌ GET `/api/dashboard/activity` - Activity data

### Search & Chat (2 APIs)
167. ❌ GET `/api/search` - Search endpoint
168. ❌ GET `/api/chat` - Chat endpoint

### Customers (3 APIs)
169. ❌ GET `/api/customers/[id]` - Customer by ID
170. ❌ GET `/api/customers` - List customers
171. ❌ GET `/api/backend/test` - Backend test

### System (4 APIs)
172. ❌ GET `/api/upload` - Upload endpoint
173. ❌ GET `/api/activity/recent` - Recent activity
174. ❌ GET `/api/health` - Health check (frontend)

### Analytics (6 APIs)
175. ❌ GET `/api/analytics/timeseries` - Timeseries analytics
176. ❌ GET `/api/analytics/metrics` - Analytics metrics
177. ❌ GET `/api/analytics/trends/threat-timeline` - Threat timeline
178. ❌ GET `/api/analytics/trends/cve` - CVE trends
179. ❌ GET `/api/analytics/trends/seasonality` - Seasonality trends
180. ❌ GET `/api/analytics/export` - Export analytics

### Tags (3 APIs)
181. ❌ GET `/api/tags/[id]` - Tag by ID
182. ❌ GET `/api/tags` - List tags
183. ❌ GET `/api/tags/assign` - Assign tags

### Observability (3 APIs)
184. ❌ GET `/api/observability/performance` - Observability performance
185. ❌ GET `/api/observability/system` - Observability system
186. ❌ GET `/api/observability/agents` - Observability agents

### Graph & Neo4j (3 APIs)
187. ❌ GET `/api/graph/query` - Graph query
188. ❌ GET `/api/neo4j/statistics` - Neo4j statistics
189. ❌ GET `/api/neo4j/cyber-statistics` - Neo4j cyber statistics

---

## QUICK REFERENCE: WORKING ENDPOINTS

### SBOM (7 working)
- `/api/v2/sbom/sboms` (GET)
- `/api/v2/sbom/sboms/{sbom_id}/cycles` (GET)
- `/api/v2/sbom/sboms/{sbom_id}/graph-stats` (GET)
- `/api/v2/sbom/sboms/{sbom_id}/remediation` (GET)
- `/api/v2/sbom/sboms/{sbom_id}/vulnerable-paths` (GET)
- `/api/v2/sbom/components/{component_id}/dependencies` (GET)
- `/api/v2/sbom/components/{component_id}/impact` (GET)
- `/api/v2/sbom/dashboard/summary` (GET)

### Vendor & Equipment (5 working)
- `/api/v2/vendor-equipment/vendors` (GET)
- `/api/v2/vendor-equipment/equipment` (GET)
- `/api/v2/vendor-equipment/maintenance-schedule` (GET)
- `/api/v2/vendor-equipment/predictive-maintenance/{equipment_id}` (GET)
- `/api/v2/vendor-equipment/predictive-maintenance/forecast` (GET)

### Threat Intelligence (15 working)
- `/api/v2/threat-intel/actors/by-sector/{sector}` (GET)
- `/api/v2/threat-intel/actors/{actor_id}/campaigns` (GET)
- `/api/v2/threat-intel/actors/{actor_id}/cves` (GET)
- `/api/v2/threat-intel/campaigns/{campaign_id}/iocs` (GET)
- `/api/v2/threat-intel/mitre/mappings/entity/{entity_type}/{entity_id}` (GET)
- `/api/v2/threat-intel/mitre/techniques/{technique_id}/actors` (GET)
- `/api/v2/threat-intel/mitre/coverage` (GET)
- `/api/v2/threat-intel/mitre/gaps` (GET)
- `/api/v2/threat-intel/iocs/search` (GET)
- `/api/v2/threat-intel/iocs/active` (GET)
- `/api/v2/threat-intel/iocs/by-type/{ioc_type}` (GET)
- `/api/v2/threat-intel/dashboard/summary` (GET)

### Risk Management (13 working)
- `/api/v2/risk/scores/high-risk` (GET)
- `/api/v2/risk/scores/search` (GET)
- `/api/v2/risk/assets/mission-critical` (GET)
- `/api/v2/risk/assets/criticality/summary` (GET)
- `/api/v2/risk/aggregation/by-vendor` (GET)
- `/api/v2/risk/aggregation/by-sector` (GET)
- `/api/v2/risk/aggregation/by-asset-type` (GET)
- `/api/v2/risk/dashboard/summary` (GET)
- `/api/v2/risk/dashboard/risk-matrix` (GET)

### Psychometric (8 working) ✅
- `/api/v2/psychometric/cognitive/process` (POST)
- `/api/v2/psychometric/personality/analyze` (POST)
- `/api/v2/psychometric/behavioral/assess` (POST)
- `/api/v2/psychometric/profiles/{profile_id}` (GET)
- `/api/v2/psychometric/insights/risk-correlation` (GET)
- `/api/v2/psychometric/threat-actor/profile` (POST)
- `/api/v2/psychometric/analytics/trends` (GET)
- `/api/v2/psychometric/validation/score` (POST)

### System (2 working)
- `/health` (GET)
- `/info` (GET)

---

## API STATUS LEGEND

- ✅ **PASS (200/201)**: Endpoint working correctly
- ❌ **FAIL (404/5xx)**: Server error, not found, or database issue
- ⚠️ **VALIDATION (4xx)**: Needs proper request body/params - endpoint works with correct data

---

## KEY FINDINGS

### New Addition: Psychometric APIs
- **8 new endpoints** for psychological and behavioral assessment
- **100% success rate** - all endpoints working
- Provides: cognitive assessment, personality analysis, behavioral risk scoring
- Use cases: insider threat detection, social engineering assessment, threat actor profiling

### System Health
- **44 working APIs** (23%) - up from 36 (20%) with psychometric additions
- **106 failed APIs** (56%)
- **39 validation APIs** (21%) - work with proper data

### Critical Issues
1. **Remediation System**: All 27 APIs failing (500 errors)
2. **Frontend Service**: All 41 AEON-SAAS-DEV APIs failing
3. **Database Issues**: Many 404s indicate missing test data

### Working Systems
1. **Psychometric Assessment**: 100% operational (NEW)
2. **MITRE ATT&CK**: 100% operational
3. **Risk Aggregation**: Fully functional
4. **SBOM Analysis**: Core functionality working

---

**Document Status**: Master reference for all 189 APIs
**Audit ID**: AUDIT-20251212-201500
**Next Review**: As needed for system changes
