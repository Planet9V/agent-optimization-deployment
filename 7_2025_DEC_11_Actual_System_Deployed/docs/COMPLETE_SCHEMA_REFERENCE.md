# Complete Neo4j Schema Reference - AEON OXOT System

**Database**: bolt://localhost:7687
**Generated**: 2025-12-12
**Total Labels**: 631
**Total Relationship Types**: 183
**Total Nodes**: ~1,000,000+

---

## Table of Contents

1. [Hierarchical Structure](#hierarchical-structure)
2. [Super Labels (17 Categories)](#super-labels)
3. [Complete Label Reference (631 Labels)](#complete-label-reference)
4. [Complete Relationship Types (183 Types)](#complete-relationship-types)
5. [Property Schemas by Major Label](#property-schemas)
6. [Label Counts and Statistics](#label-statistics)
7. [Relationship Counts and Statistics](#relationship-statistics)

---

## Hierarchical Structure

The schema uses a **4-tier hierarchical classification system**:

```
TIER 1 (Domain) → TIER 2 (Category) → FINE_GRAINED_TYPE (Specific) → LABEL (Implementation)
```

### Tier 1 Categories (5 Total)

| Tier 1 | Node Count | Description |
|--------|-----------|-------------|
| TECHNICAL | 349,342 | Technical security elements (vulnerabilities, threats, techniques) |
| CONTEXTUAL | 302,188 | Measurements, monitoring data, time series |
| ASSET | 201,969 | Physical and digital assets, infrastructure components |
| OPERATIONAL | 67,491 | Controls, processes, operations |
| ORGANIZATIONAL | 56,159 | Organizations, entities, roles |

### Tier 2 Categories (17 Super Labels)

| Super Label | Node Count | Tier 1 | Description |
|-------------|-----------|--------|-------------|
| Vulnerability | 314,538 | TECHNICAL | CVEs, weaknesses, security flaws |
| Measurement | 297,158 | CONTEXTUAL | Sensor data, metrics, monitoring |
| Asset | 200,275 | ASSET | Devices, equipment, infrastructure |
| Control | 65,199 | OPERATIONAL | Security controls, mitigations |
| Organization | 56,144 | ORGANIZATIONAL | Companies, entities, vendors |
| Indicator | 11,601 | TECHNICAL | IOCs, threat indicators |
| ThreatActor | 10,599 | TECHNICAL | APT groups, malware, attackers |
| Protocol | 8,776 | TECHNICAL | Network protocols, communications |
| Location | 4,830 | ORGANIZATIONAL | Geographic locations, facilities |
| Technique | 3,526 | TECHNICAL | ATT&CK techniques, TTPs |
| Event | 2,291 | CONTEXTUAL | Incidents, activities, logs |
| Software | 1,694 | TECHNICAL | Software components, applications |
| Malware | 302 | TECHNICAL | Malicious software families |
| PsychTrait | 161 | ORGANIZATIONAL | Cognitive biases, behaviors |
| EconomicMetric | 39 | CONTEXTUAL | Economic indicators |
| Role | 15 | ORGANIZATIONAL | Job roles, positions |
| Campaign | 1 | TECHNICAL | Threat campaigns |

---

## Super Labels

### 17 Super Label Categories with Discriminators

Each super label uses **property discriminators** to route to specific sub-types:

#### 1. Vulnerability (314,538 nodes)
**Discriminator Property**: `fine_grained_type`
- `vulnerability` (313,561) - General vulnerabilities
- `cve` (533) - Specific CVE entries
- `cwe` (105) - CWE weakness types
- `CVE` (196) - Alternative CVE format

**Key Properties**:
- `cvssV2BaseScore`, `cvssV31BaseSeverity`
- `epss_score`, `epss_percentile` (exploit prediction)
- `priority_tier`, `priority_calculated_at`
- `cpe_vendors`, `cpe_products`, `cpe_uris`
- `published_date`, `modified_date`
- `kaggle_enriched`, `cpe_enriched`

#### 2. Measurement (297,158 nodes)
**Discriminator Property**: `measurement_type`
- `generic`, `uptime`, `performance`, `temperature`, `radiation`, etc.

**Key Properties**:
- `value`, `unit`, `quality`
- `timestamp`, `subsector`
- `measurementType`, `node_type`
- Sector-specific: `nfpa_compliant`, `equipment_id`, `incident_id`

#### 3. Asset (200,275 nodes)
**Discriminator Property**: `assetClass`, `device_type`
- `device`, `protocol`, `equipment`, `software`

**Key Properties**:
- `device_name`, `device_type`, `manufacturer`, `model`
- `ip_address`, `install_date`, `status`
- `assetClass`, `protocolType`, `node_type`

#### 4. Control (65,199 nodes)
**Discriminator Property**: `controlType`
- `generic`, `mitigation`, `safeguard`

**Key Properties**:
- `name`, `description`, `controlType`
- `stix_id` (for ATT&CK mitigations)

#### 5. ThreatActor (10,599 nodes)
**Discriminator Property**: `fine_grained_type`, `actorType`
- `malware` (768), `threatactor` (8,258), `apt_group` (24)

**Key Properties**:
- `name`, `aliases`, `description`
- `malwareFamily`, `actorType`
- `sophistication`, `primary_motivation`
- `active_since`, `confidence`, `status`
- `uco_class`, `uco_uri` (UCO ontology)
- `validation_status`, `tagged_date`

#### 6. Indicator (11,601 nodes)
**Discriminator Property**: `indicatorType`
- `Domain`, `IP`, `Hash`, `URL`, etc.

**Key Properties**:
- `indicatorValue`, `indicatorType`, `indicatorId`
- `threat_level`, `confidence`
- `firstSeen`, `lastSeen`
- `validation_status`, `tagging_method`

#### 7. Technique (3,526 nodes)
**Discriminator Property**: `fine_grained_type`
- `technique` (4,269), `attack_technique` (42)

**Key Properties**:
- `name`, `description`, `stix_id`
- `tactics` (array of tactic IDs)
- `domain` (enterprise, ics, mobile)
- `is_subtechnique` (boolean)
- `taxonomy` (MITRE ATT&CK, ICS, etc.)

---

## Complete Label Reference

### All 631 Labels (Alphabetical)

```
1. APISource
2. APT_GROUP
3. ATTACK_Group
4. ATTACK_Software
5. ATTACK_Tactic
6. ATTACK_Technique
7. ATT_CK_Tactic
8. ATT_CK_Technique
9. Access_Control
10. ActivityTracking
11. Adversary
12. Aerospace_Defense
13. Aggregator
14. Agriculture
15. AgricultureMetric
16. AgricultureProcess
17. AirQualityStation
18. Alert
19. AlertRule
20. AlertSystem
21. Ambulance
22. AnalystDiscourse
23. AnalyticsApp
24. AnalyticsStream
25. Animal
26. AnimalHealth
27. AnimalMonitor
28. Application
29. ArchiveSystem
30. Artifact
31. Assessment
32. Asset
33. Attack
34. AttackPattern
35. AttackTactic
36. AttackTechnique
37. AttackTimeline
38. AttackVector
39. Attestation
40. BAS
41. BEHAVIORAL
42. Banking
43. Barn
44. BatchStream
45. Behavioral_Pattern
46. BotNetwork
47. Build
48. BuildSystem
49. BuildTool
50. Build_Info
51. CAD
52. CADWorkstation
53. CAMPAIGN
54. CAPEC
55. CAPECCategory
56. CAPEC_Category
57. CCTV
58. CHEMICAL
59. COMMERCIAL_FACILITIES
60. COMMUNICATIONS
61. CVE
62. CWE
63. CWECategory
64. CWE_Category
65. Campaign
66. CapitalMarkets
67. CascadeEvent
68. CertificationExpiration
69. ChemicalAlert
70. ChemicalControl
71. ChemicalEquipment
72. ChemicalMeasurement
73. ChemicalProcess
74. ChemicalProperty
75. ChemicalZone
76. Classified
77. CloudAccount
78. CloudStorageAccount
79. Cloud_Infrastructure
80. CognitiveBias
81. Cognitive_Bias
82. ColdChain
83. ColdChainBreak
84. ColdChainTemp
85. ColdStorage
86. ColdStorageCenter
87. ColdStorageControl
88. Combine
89. Command
90. CommercialAsset
91. CommercialControl
92. CommercialLocation
93. CommercialMitigation
94. CommercialProcess
95. CommercialStandard
96. CommercialThreat
97. CommercialVulnerability
98. CommunicationLatency
99. Communications
100. CommunicationsAlert
101. CommunicationsDevice
102. CommunicationsProperty
103. CommunicationsZone
104. Compliance
105. ComplianceCertification
106. Component
107. ConfidenceScore
108. Configuration
109. ContainerImage
110. ContainerInstance
111. Control
112. ConveyorSystem
113. CourseOfAction
114. Critical
115. CriticalInfrastructure
116. Critical_Infrastructure_Sector
117. Crop
118. CropField
119. CropProduction
120. CropYield
121. CrossInfrastructureDependency
122. Customer
123. CustomerImpact
124. CybersecurityKB_AttackTactic
125. CybersecurityKB_AttackTechnique
126. CybersecurityKB_Campaign
127. CybersecurityKB_CourseOfAction
128. CybersecurityKB_Malware
129. CybersecurityKB_ThreatActor
130. CybersecurityKB_Tool
131. Cybersecurity_Attack
132. DairyFacility
133. DamsEquipment
134. DamsIncident
135. DamsMitigation
136. DamsProcess
137. DamsStandard
138. DamsThreat
139. DamsVulnerability
140. Dashboard
141. DataCenterFacility
142. DataConsumer
143. DataFlow
144. DataProcessor
145. DataSource
146. Data_Centers
147. Database
148. DatabaseSource
149. Datastore
150. DefenseAlert
151. DefenseControl
152. DefenseDevice
153. DefenseMeasurement
154. DefenseProcess
155. DefenseProperty
156. DefenseZone
157. Dependency
158. DependencyLink
159. DependencyPath
160. DependencyTree
161. DeploymentRegistry
162. DeploymentZone
163. Detection
164. DetectionSignature
165. Device
166. DigitalTwinState
167. DiscoursePosition
168. Dispatch
169. DispatchCenter
170. DispatchZone
171. DisruptionEvent
172. DistributedEnergyResource
173. Document
174. Domain
175. EMB3D
176. EMB3DMitigation
177. EMB3DProperty
178. EMB3DThreat
179. EMB3D_Mitigation
180. EMB3D_Property
181. EMB3D_Threat
182. EMERGENCY_SERVICES
183. EMS
184. EMSDistrict
185. EMSStation
186. ENERGY
187. EOC
188. EconomicMetric
189. EmailAddress
190. EmergencyAlert
191. EmergencyEquipment
192. EmergencyResponse
193. EmergencyServicesDevice
194. EmergencyServicesProperty
195. Emergency_Systems
196. Enclosure
197. Energy
198. EnergyDevice
199. EnergyManagementSystem
200. EnergyProperty
201. Energy_Distribution
202. Energy_Generation
203. Energy_Transmission
204. Enricher
205. Entity
206. EnvironmentalControl
207. Equipment
208. EquipmentFailure
209. EquipmentModel
210. EquipmentPerformance
211. EquipmentReadiness
212. EquipmentSpec
213. EquipmentStatus
214. EquipmentYard
215. Event
216. EventCorrelation
217. EventProcessor
218. EventStore
219. EventStream
220. Evidence
221. Exploit
222. FINANCIAL_SERVICES
223. FMIS
224. FOOD_AGRICULTURE
225. Facility
226. FacilityCapacity
227. FacilityCertification
228. FailurePropagation
229. Farm
230. FarmHeadquarters
231. FarmManagementSystem
232. FarmZone
233. FeedDelivery
234. FeedIntake
235. FeedMixer
236. Field
237. FieldCharacteristics
238. File
239. FinancialAlert
240. FinancialControl
241. FinancialProcess
242. FinancialServicesDevice
243. FinancialServicesProperty
244. FinancialZone
245. FireApparatus
246. FireContainment
247. FireDistrict
248. FireServices
249. FireStation
250. FireSuppression
251. Fire_Safety
252. Firmware
253. FirstResponse
254. FoodAgricultureAlert
255. FoodAgricultureDevice
256. FoodAgricultureProperty
257. FoodProcessing
258. FoodProduct
259. FoodSafety
260. FoodSafetyHazard
261. FoodSafetyMonitor
262. FoodSafetyViolation
263. Function
264. FutureThreat
265. GOVERNMENT_FACILITIES
266. Geography
267. GeopoliticalEvent
268. Governance
269. GovernmentAlert
270. GovernmentControl
271. GovernmentDevice
272. GovernmentMeasurement
273. GovernmentProcess
274. GovernmentProperty
275. GovernmentZone
276. GrainBin
277. GrainBinHazard
278. GrainBinMonitor
279. GrainDryer
280. GrainElevator
281. GrainStorage
282. GreenhouseComplex
283. Ground_Systems
284. HMISession
285. HVAC
286. HVAC_BMS
287. Harvesting
288. Hash
289. HazmatAlert
290. HazmatResponse
291. HealthMetric
292. HealthMonitor
293. Health_Monitor
294. Healthcare
295. HealthcareAlert
296. HealthcareControl
297. HealthcareDevice
298. HealthcareMeasurement
299. HealthcareProcess
300. HealthcareProperty
301. HealthcareZone
302. HeatExchangeEquipment
303. HerdComposition
304. HistoricalPattern
305. HistoricalSnapshot
306. HospitalDiversion
307. Human
308. Humidity
309. Hypervisor
310. HystericDiscourse
311. ICS
312. ICS_Asset
313. ICS_FRAMEWORK
314. ICS_Protocol
315. ICS_THREAT_INTEL
316. ICS_Tactic
317. ICS_Technique
318. INFORMATION_TECHNOLOGY
319. IPAddress
320. IT
321. ITAlert
322. ITControl
323. ITDevice
324. ITMeasurement
325. ITProcess
326. ITProperty
327. ITZone
328. IT_Hardware
329. IT_INFRASTRUCTURE
330. IT_Infrastructure
331. IT_Software
332. Identity
333. ImaginaryRegister
334. ImpactAssessment
335. ImplementationPattern
336. Incident
337. IncidentCommand
338. IncidentCommandSystem
339. IncidentDispatch
340. IncidentResolution
341. Indicator
342. InformationEvent
343. InformationStream
344. Infrastructure
345. Insider_Threat_Indicator
346. IntegrationStream
347. IntelligenceSource
348. Intelligence_Analysis
349. IntrusionSet
350. Intrusion_Detection
351. Investigation
352. Investigation_Case
353. Irrigation
354. IrrigationControl
355. IrrigationController
356. IrrigationFlow
357. IrrigationMalfunction
358. IrrigationZone
359. KEV
360. KnowledgeBaseStats
361. KubernetesCluster
362. LOG_ANALYSIS
363. LawEnforcement
364. Level5
365. Library
366. License
367. LicenseCompliance
368. LicensePolicy
369. Livestock
370. LivestockBarn
371. LivestockFeeding
372. LivestockManagement
373. Location
374. LogSource
375. MALWARE
376. MLModel
377. MaintenanceSchedule
378. MajorAsset
379. MajorChemicalAsset
380. MajorFacility
381. MajorHealthcareAsset
382. MajorManufacturingAsset
383. MaliciousPackage
384. Malware
385. ManufacturingAlert
386. ManufacturingControl
387. ManufacturingEquipment
388. ManufacturingMeasurement
389. ManufacturingProcess
390. ManufacturingProperty
391. ManufacturingZone
392. MassCasualty
393. MasterDiscourse
394. Measurement
395. MeatProcessingPlant
396. MedicalTreatment
397. Metadata
398. Middleware
399. MilkProduction
400. Milking
401. MilkingSystem
402. Mitigation
403. MobileCommand
404. MobileDevice
405. Monitoring
406. Motivation_Factor
407. MutualAid
408. MutualAidCoordination
409. MutualAidRequest
410. MutualAidZone
411. NATION_STATE
412. NERCCIPStandard
413. Naval_Systems
414. NetworkDevice
415. NetworkManagementSystem
416. NetworkMeasurement
417. NetworkSegment
418. Notification
419. Nuclear
420. NuclearAlert
421. NuclearDevice
422. NuclearProperty
423. NuclearZone
424. Nutrients
425. OWASPCategory
426. Observable
427. OfficerSafety
428. OperatingSystem
429. OperationalMetric
430. OperationalParameter
431. Organization
432. P25Radio
433. PHYSICAL_SECURITY
434. PLCStateChange
435. Package
436. PackagingSystem
437. ParkingSpace
438. Pasture
439. PatientTransport
440. PaymentSystems
441. PerformanceMetric
442. PeripheralDevice
443. Personality_Trait
444. PersonnelAvailability
445. PersonnelCertification
446. PestControl
447. PestOutbreak
448. PhysicalAccessControl
449. PhysicalActuator
450. PhysicalSensor
451. PhysicalServer
452. PhysicsConstraint
453. PipingAndValves
454. Planter
455. Planting
456. PoliceDistrict
457. PoliceStation
458. PoliceVehicle
459. PrecisionAg
460. Process
461. ProcessControlSystems
462. ProcessLoop
463. ProcessingArea
464. ProcessingLine
465. ProcessingPlant
466. ProcessingSCADA
467. Project
468. PropagationRule
469. Property
470. Protocol
471. Provenance
472. PsychTrait
473. PsychologicalPattern
474. PumpsAndCompressors
475. QualityControl
476. QualityMetric
477. RTUCommunication
478. RadiationMeasurement
479. ReactorControlSystem
480. ReactorProcess
481. Reactors
482. RealRegister
483. RealTimeStream
484. Region
485. Register
486. Registry
487. Relationship
488. RemediationPlan
489. RescueOperation
490. ResourceAllocation
491. ResourceAvailability
492. ResourceInventory
493. ResourceManagement
494. ResourceShortage
495. ResponseMetric
496. ResponseTime
497. RevenueModel
498. Role
499. Router
500. RoutingProcess
501. SAREF
502. SAREF_Actuator
503. SAREF_Core
504. SAREF_Device
505. SAREF_Measurement
506. SBOM
507. SBOMStandard
508. SBOMTool
509. SCADA
510. SCADAEvent
511. SCADASystem
512. SECTOR_DEFENSE_INDUSTRIAL_BASE
513. SLA
514. SOCIAL_MEDIA
515. STIX_Cyber_Observable
516. STIX_Domain_Object
517. STIX_Object
518. SafetyAndMonitoringSystems
519. SafetyFunction
520. SafetyInterlock
521. Sanitation
522. SanitationSystem
523. Satellite_Systems
524. Sector
525. SecurityStream
526. Sensor
527. SensorSource
528. SeparationEquipment
529. Server
530. ServerlessFunction
531. Service
532. ServiceLevel
533. ServiceZone
534. SleepAnalysis
535. Smart_City
536. SocialMediaAccount
537. SocialMediaPost
538. SocialNetwork
539. Social_Engineering_Tactic
540. Social_Media_Intelligence
541. Software
542. SoftwareComponent
543. SoftwareLicense
544. Software_Component
545. SoilMeasurement
546. SoilMoisture
547. SoilSensor
548. Sprayer
549. Standard
550. State
551. StateDeviation
552. StorageArray
553. StorageTanks
554. StreetLight
555. Substation
556. SupportContract
557. Surveillance
558. SurveillanceSystem
559. SymbolicRegister
560. System
561. SystemResilience
562. TARGET_SECTOR
563. TEST
564. THREAT_INTEL_SHARING
565. TOOL
566. TTP
567. Tactic
568. Tag
569. Technique
570. Telecom_Infrastructure
571. Temperature
572. TemporalEvent
573. TemporalPattern
574. Threat
575. ThreatActor
576. ThreatActorSocialProfile
577. ThreatFeed
578. ThreatModel
579. Threat_Actor_Analysis
580. TimeSeries
581. TimeSeriesAnalysis
582. Tool
583. Tractor
584. TrafficLight
585. TrafficSensor
586. TrainingFacility
587. TrainingLevel
588. TransactionMetric
589. Transformer
590. TransmissionLine
591. Transportation
592. TreatmentEffectiveness
593. TreatmentProcess
594. UCOClass
595. UCO_Observable
596. URL
597. UnitOfMeasure
598. UniversityDiscourse
599. VULNERABILITY
600. Validator
601. Vendor
602. VentilationController
603. VersionedNode
604. VirtualMachine
605. VirtualMachineInstance
606. VirtualNetwork
607. Virtualization
608. Vulnerability
609. VulnerabilityAttestation
610. WATER
611. WasteContainer
612. WasteManager
613. WaterAlert
614. WaterDevice
615. WaterProperty
616. WaterZone
617. Water_Distribution
618. Water_Treatment
619. Weakness
620. WearableDevice
621. WearableSecurity
622. WeatherData
623. WeatherStation
624. WeatherWarning
625. WebApplication
626. WhatIfScenario
627. Workflow
628. Workstation
629. Zone
```

---

## Complete Relationship Types

### All 183 Relationship Types (Alphabetical)

```
1. ACTIVATES_BIAS
2. AFFECTS
3. AFFECTS_SECTOR
4. AFFECTS_SYSTEM
5. ANALYZES_SECTOR
6. APPLIES_TO
7. ATTRIBUTED_TO
8. BASED_ON_PATTERN
9. BELONGS_TO
10. BELONGS_TO_TACTIC
11. CANALSOBE
12. CANFOLLOW
13. CANPRECEDE
14. CASCADES_TO
15. CHAINS_TO
16. CHILDOF
17. CHILD_OF
18. CLASSIFIED_BY
19. COLLABORATES_WITH
20. COMPATIBLE_WITH
21. COMPLIES_WITH
22. COMPLIES_WITH_NERC_CIP
23. COMPOSED_OF
24. CONDUCTS
25. CONNECTED_TO_GRID
26. CONNECTED_TO_SEGMENT
27. CONNECTS_SUBSTATIONS
28. CONNECTS_TO
29. CONSUMES_FROM
30. CONTAINS
31. CONTAINS_ENTITY
32. CONTAINS_EQUIPMENT
33. CONTAINS_EVIDENCE
34. CONTAINS_ICS_TECHNIQUE
35. CONTRIBUTES_TO
36. CONTROLLED_BY
37. CONTROLLED_BY_EMS
38. CONTROLS
39. CORRELATES_WITH
40. DELIVERS_TO
41. DEPENDS_CRITICALLY_ON
42. DEPENDS_ON
43. DEPENDS_ON_ENERGY
44. DEPLOYED_AT
45. DEPLOYED_IN
46. DEPLOYS
47. DEPLOYS_ASSET
48. DETECTS
49. DETECTS_VULNERABILITY
50. EMB3D_REL
51. EMPHASIZES_REGISTER
52. ENABLES_LATERAL_MOVEMENT
53. ENABLES_TECHNIQUE
54. EQUIVALENT_TO_STIX
55. EVOLVES_TO
56. EXECUTES
57. EXECUTES_PROCESS
58. EXHIBITS_PATTERN
59. EXHIBITS_PERSONALITY_TRAIT
60. EXHIBITS_REGISTER
61. EXPLOITED_BY
62. EXPLOITED_VIA
63. EXPLOITS
64. EXPLOITS_PROTOCOL
65. EXTENDS_SAREF_DEVICE
66. GENERATED
67. GENERATES
68. GENERATES_MEASUREMENT
69. GOVERNS
70. GRANTS_PHYSICAL_ACCESS_TO
71. HAS_ASSESSMENT
72. HAS_BIAS
73. HAS_COMMAND
74. HAS_COMPONENT
75. HAS_CONTROL
76. HAS_ENERGY_PROPERTY
77. HAS_FUNCTION
78. HAS_MEASUREMENT
79. HAS_ORGANIZATION
80. HAS_PROPERTY
81. HAS_SYSTEM
82. HAS_TAG
83. HAS_THREAT_MODEL
84. HAS_VULNERABILITY
85. HAS_ZONE
86. HOSTS
87. HOUSES_EQUIPMENT
88. IDENTIFIES_THREAT
89. IMPACTS
90. IMPLEMENTS
91. IMPLEMENTS_TECHNIQUE
92. INCLUDES_COMPONENT
93. INDICATES
94. INFLUENCES_BEHAVIOR
95. INSTALLED_AT_SUBSTATION
96. INSTALLED_ON
97. INSTANCE_OF
98. INTEGRATES_WITH
99. INVOLVES
100. IN_REGION
101. ISOLATES
102. IS_TYPE_OF
103. IS_WEAKNESS_TYPE
104. LEADS_TO
105. LEVERAGES
106. LOCATED_AT
107. LOCATED_IN
108. MANAGES_EQUIPMENT
109. MANIFESTS_IN_DISCOURSE
110. MAPS_TO_ATTACK
111. MAPS_TO_OWASP
112. MAPS_TO_STIX
113. MAY_DEPLOY
114. MEASURES
115. METADATA_FOR
116. MITIGATED_BY
117. MITIGATES
118. MONITORS
119. MONITORS_EQUIPMENT
120. MOTIVATES
121. OFFERS_SERVICE
122. OPERATES_IN
123. OPERATES_IN_REGISTER
124. OPERATES_ON
125. ORCHESTRATES_CAMPAIGN
126. OWNED_BY
127. OWNS
128. OWNS_EQUIPMENT
129. PARTICIPATES_IN
130. PART_OF
131. PART_OF_CAMPAIGN
132. PEEROF
133. PHYSICALLY_LOCATED_IN
134. POSITIONED_IN
135. PROCESSES_EVENT
136. PROCESSES_THROUGH
137. PROFILES
138. PROPAGATES_FROM
139. PROPAGATES_TO
140. PROTECTED_BY
141. PROTECTS
142. PROVIDES
143. PUBLISHES
144. REDUNDANT_WITH
145. REFERENCES
146. RELATED_TO
147. RELATES_TO
148. RELATIONSHIP
149. RELEASES_GUIDANCE
150. REPORTS_TO
151. REQUIRES
152. REQUIRES_DATA_SOURCE
153. REQUIRES_STANDARD
154. ROUTES_THROUGH
155. ROUTES_TO
156. RUNS_SOFTWARE
157. SBOM_CONTAINS
158. SHARED_WITH
159. SIMULATES
160. SUBPROPERTY_OF
161. SUBTECHNIQUE_OF
162. SUB_TECHNIQUE_OF
163. SUCCESSOR_OF
164. SUPERSEDED_BY
165. SUPPORTS
166. SUPPORTS_PROTOCOL
167. TARGETS
168. TARGETS_ICS_ASSET
169. TARGETS_SECTOR
170. THREATENS
171. TRACKED_BY
172. TRACKS_PROCESS
173. TRIGGERED_BY
174. TRIGGERS
175. USES
176. USES_ATTACK_PATTERN
177. USES_DEVICE
178. USES_PROTOCOL
179. USES_SOFTWARE
180. USES_TACTIC
181. USES_TECHNIQUE
182. USES_TTP
183. VULNERABLE_TO
```

---

## Property Schemas

### Standard Hierarchy Properties (All Nodes)

**Every node** in the system includes these standard properties:

```javascript
{
  // Hierarchical Classification
  tier1: String,           // Domain: TECHNICAL, CONTEXTUAL, ASSET, OPERATIONAL, ORGANIZATIONAL
  tier2: String,           // Category/Super Label
  super_label: String,     // Same as tier2
  fine_grained_type: String, // Specific type discriminator
  hierarchy_path: String,  // Full path: "tier1/tier2/specific"
  tier: Integer,           // Numeric tier level (1-3)

  // Identity
  id: String,              // Unique identifier
  name: String,            // Human-readable name (when applicable)

  // Metadata
  node_type: String,       // Implementation label type
}
```

### CVE/Vulnerability Schema

```javascript
{
  // Standard Hierarchy
  tier1: "TECHNICAL",
  tier2: "Vulnerability",
  super_label: "Vulnerability",
  fine_grained_type: "vulnerability" | "cve" | "cwe",
  hierarchy_path: "TECHNICAL/Vulnerability/...",

  // Identity
  id: String,              // CVE ID (e.g., "CVE-1999-0095")

  // Vulnerability Details
  description: String,
  vulnType: "cve" | "cwe",

  // CVSS Scoring
  cvssV2BaseScore: Float,
  cvssV31BaseSeverity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",

  // EPSS (Exploit Prediction Scoring System)
  epss_score: Float,       // 0.0 - 1.0
  epss_percentile: Float,  // 0.0 - 1.0
  epss_date: Date,
  epss_updated: DateTime,
  epss_last_updated: DateTime,

  // Priority Calculation
  priority_tier: "NEVER" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  priority_calculated_at: DateTime,

  // CPE (Common Platform Enumeration)
  cpe_uris: [String],      // Array of CPE URIs
  cpe_vendors: [String],   // Affected vendors
  cpe_products: [String],  // Affected products
  cpe_enriched: DateTime,  // When CPE data was added

  // Dates
  published_date: DateTime,
  modified_date: DateTime,
  kaggle_enriched: DateTime,
}
```

**Example CVE Node**:
```javascript
{
  tier1: "TECHNICAL",
  tier2: "Vulnerability",
  super_label: "Vulnerability",
  fine_grained_type: "vulnerability",
  hierarchy_path: "TECHNICAL/Vulnerability/Unknown",
  tier: 1,

  id: "CVE-1999-0095",
  description: "The debug command in Sendmail is enabled...",
  vulnType: "cve",

  cvssV2BaseScore: 10.0,
  cvssV31BaseSeverity: "HIGH",

  epss_score: 0.0838,
  epss_percentile: 0.91934,
  epss_date: "2025-11-02",
  epss_updated: "2025-11-02T04:27:11.978Z",
  epss_last_updated: "2025-11-02T17:21:46.323344Z",

  priority_tier: "NEVER",
  priority_calculated_at: "2025-11-02T17:40:03.653Z",

  cpe_uris: ["cpe:2.3:a:eric_allman:sendmail:5.58:*:*:*:*:*:*:*"],
  cpe_vendors: ["Eric Allman"],
  cpe_products: ["Sendmail"],
  cpe_enriched: "2025-11-02T16:02:17.988Z",

  published_date: "1988-10-01T04:00Z",
  modified_date: "2025-04-03T01:03:51.193Z",
  kaggle_enriched: "2025-12-12T05:20:17.975Z"
}
```

### Measurement Schema

```javascript
{
  // Standard Hierarchy
  tier1: "CONTEXTUAL",
  tier2: "Measurement",
  super_label: "Measurement",
  fine_grained_type: "measurement",
  hierarchy_path: "CONTEXTUAL/Measurement/...",

  // Identity
  id: String,

  // Measurement Data
  value: Float | Integer,
  unit: String,            // %, degrees, count, etc.
  quality: "poor" | "fair" | "good" | "excellent",
  timestamp: DateTime,

  // Classification
  measurement_type: String, // uptime, temperature, pressure, etc.
  measurementType: String,  // generic, specific type
  node_type: String,       // Implementation label

  // Context
  subsector: String,       // Critical infrastructure subsector

  // Sector-Specific Properties (when applicable)
  equipment_id: String,
  incident_id: String,
  severity_level: String,
  location: String,
  metric_value: Float,
  unit_of_measure: String,
  nfpa_compliant: Boolean,
}
```

**Example Measurement Node**:
```javascript
{
  tier1: "CONTEXTUAL",
  tier2: "Measurement",
  super_label: "Measurement",
  fine_grained_type: "measurement",
  hierarchy_path: "CONTEXTUAL/Measurement/Unknown",
  tier: 3,

  id: "COMM_MEAS_Telecom_Infrastructure_000000",

  value: 95.69717299683165,
  unit: "%",
  quality: "poor",
  timestamp: "2025-11-21T08:56:07.316543",

  measurement_type: "uptime",
  measurementType: "generic",
  node_type: "NetworkMeasurement",

  subsector: "Telecom_Infrastructure"
}
```

### Asset Schema

```javascript
{
  // Standard Hierarchy
  tier1: "ASSET",
  tier2: "Asset",
  super_label: "Asset",
  fine_grained_type: "asset" | "protocol" | "device",
  hierarchy_path: "ASSET/Asset/...",

  // Identity
  id: String,
  device_name: String,

  // Device Details
  device_type: String,     // Cell_Tower, Router, PLC, etc.
  manufacturer: String,
  model: String,
  status: "operational" | "degraded" | "offline" | "maintenance",

  // Classification
  assetClass: "device" | "software" | "protocol",
  protocolType: String,    // For protocol assets
  node_type: String,       // Implementation label

  // Network
  ip_address: String,

  // Lifecycle
  install_date: DateTime,

  // Context
  subsector: String,
}
```

**Example Asset Node**:
```javascript
{
  tier1: "ASSET",
  tier2: "Asset",
  super_label: "Asset",
  fine_grained_type: "protocol",
  hierarchy_path: "ASSET/Asset/Unknown",
  tier: 2,

  id: "COMM_DEV_Telecom_Infrastructure_000000",
  device_name: "Cell_Tower_Telecom_Infrastructure_0",

  device_type: "Cell_Tower",
  manufacturer: "Huawei",
  model: "MODEL_2750",
  status: "degraded",

  assetClass: "device",
  protocolType: "generic",
  node_type: "CommunicationsDevice",

  ip_address: "147.43.122.2",
  install_date: "2019-03-21T18:56:07.404833",

  subsector: "Telecom_Infrastructure"
}
```

### ThreatActor Schema

```javascript
{
  // Standard Hierarchy
  tier1: "TECHNICAL",
  tier2: "ThreatActor",
  super_label: "ThreatActor",
  fine_grained_type: "malware" | "threatactor" | "apt_group",
  hierarchy_path: "TECHNICAL/ThreatActor/...",

  // Identity
  id: String,              // STIX ID or custom
  name: String,
  aliases: [String],       // Array of alternative names

  // Classification
  type: "malware" | "threat-actor" | "intrusion-set",
  actorType: String,       // generic_threat_actor, etc.
  malwareFamily: String,   // For malware types

  // Attribution
  sophistication: String,  // low, medium, high, advanced
  primary_motivation: String,
  active_since: Date,
  confidence: String,      // low, medium, high
  status: String,          // active, inactive, unknown

  // Details
  description: String,
  labels: [String],        // STIX labels

  // Ontology Integration
  uco_class: String,       // UCO class URI
  uco_uri: String,         // Full UCO URI
  namespace: String,       // Source namespace

  // Metadata
  created: DateTime,
  modified: DateTime,
  created_by: String,

  // Validation
  validation_status: "VALIDATED" | "PENDING" | "REJECTED",
  tagging_method: "automatic" | "manual" | "retroactive",
  tagged_date: DateTime,
  uco_enriched_date: DateTime,
}
```

**Example ThreatActor Node (Malware)**:
```javascript
{
  tier1: "TECHNICAL",
  tier2: "ThreatActor",
  super_label: "ThreatActor",
  fine_grained_type: "malware",
  hierarchy_path: "TECHNICAL/ThreatActor/HDoor",
  tier: 1,

  id: "malware--007b44b6-e4c5-480b-b5b9-56f2081b1b7b",
  name: "HDoor",
  aliases: ["HDoor", "Custom HDoor"],

  type: "malware",
  actorType: "generic_threat_actor",
  malwareFamily: "generic_malware",

  description: "[HDoor](https://attack.mitre.org/software/S0061) is malware that has been customized and used by the [Naikon](https://attack.mitre.org/groups/G0019) group.",
  labels: ["malware"],

  uco_class: "uco:Malware",
  uco_uri: "http://purl.org/cyber/uco#Malware",
  namespace: "CybersecurityKB",

  created: "2017-05-31T21:32:40.801Z",
  modified: "2025-04-16T20:37:51.573Z",
  created_by: "AEON_INTEGRATION_WAVE4",

  validation_status: "VALIDATED",
  tagging_method: "retroactive",
  tagged_date: "2025-10-31T21:39:27.510Z",
  uco_enriched_date: "2025-10-27T19:25:16.459Z"
}
```

### Control Schema

```javascript
{
  // Standard Hierarchy
  tier1: "OPERATIONAL",
  tier2: "Control",
  super_label: "Control",
  fine_grained_type: "control",
  hierarchy_path: "OPERATIONAL/Control/...",

  // Identity
  id: String,              // Technique ID or custom
  name: String,

  // Details
  description: String,
  controlType: "generic" | "mitigation" | "safeguard",

  // ATT&CK Integration
  stix_id: String,         // STIX course-of-action ID
}
```

### Indicator Schema

```javascript
{
  // Standard Hierarchy
  tier1: "TECHNICAL",
  tier2: "Indicator",
  super_label: "Indicator",
  fine_grained_type: "indicator",
  hierarchy_path: "TECHNICAL/Indicator/...",

  // Identity
  indicatorId: String,
  indicatorValue: String,  // The actual IOC value

  // Classification
  indicatorType: "Domain" | "IP" | "Hash" | "URL" | "Email",
  threat_level: "Low" | "Medium" | "High" | "Critical",
  confidence: "Low" | "Medium" | "High",

  // Temporal
  firstSeen: DateTime,
  lastSeen: DateTime,

  // Metadata
  created_by: String,
  validation_status: "VALIDATED" | "PENDING",
  tagging_method: String,
  tagged_date: DateTime,
}
```

### Technique Schema

```javascript
{
  // Standard Hierarchy
  tier1: "TECHNICAL",
  tier2: "Technique",
  super_label: "Technique",
  fine_grained_type: "technique" | "attack_technique",
  hierarchy_path: "TECHNICAL/Technique/...",

  // Identity
  id: String,              // ATT&CK ID
  name: String,

  // Details
  description: String,

  // ATT&CK Integration
  stix_id: String,
  tactics: [String],       // Array of tactic IDs
  domain: "enterprise" | "ics" | "mobile",
  taxonomy: String,        // MITRE ATT&CK, ICS, etc.

  // Classification
  is_subtechnique: Boolean,
  patternType: String,

  // Metadata
  updated_at: DateTime,
}
```

### Relationship Property Schema

Relationships can have properties that describe the relationship:

```javascript
{
  // Impact Relationships
  impact_type: String,           // performance_degradation, outage, etc.
  impact_severity: String,       // minor, moderate, severe, critical
  mitigation_available: Boolean,
  workaround_exists: Boolean,
  recovery_time_estimate: String,

  // Metadata
  created: DateTime,
  source: String,               // Where this relationship came from
  confidence: Float,            // 0.0 - 1.0
}
```

---

## Label Statistics

### Top 100 Labels by Node Count

| Rank | Label | Count | Super Label | Description |
|------|-------|-------|-------------|-------------|
| 1 | CVE | 316,552 | Vulnerability | Common Vulnerabilities and Exposures |
| 2 | Vulnerability | 314,538 | Vulnerability | General vulnerability nodes |
| 3 | Measurement | 297,858 | Measurement | Sensor/monitoring measurements |
| 4 | Asset | 206,075 | Asset | Physical and digital assets |
| 5 | Monitoring | 181,704 | Measurement | Monitoring data |
| 6 | SBOM | 140,000 | Asset | Software Bill of Materials |
| 7 | ManufacturingMeasurement | 72,800 | Measurement | Manufacturing sector data |
| 8 | Control | 66,391 | Control | Security controls |
| 9 | Property | 61,700 | - | Property definitions |
| 10 | Organization | 56,144 | Organization | Companies, vendors |
| 11 | Entity | 55,569 | Organization | Business entities |
| 12 | Software_Component | 55,000 | Asset | Software components (SBOM) |
| 13 | TimeSeries | 51,000 | Measurement | Time series data |
| 14 | SoftwareComponent | 50,000 | Asset | Software components |
| 15 | Device | 48,400 | Asset | Physical devices |
| 16 | Equipment | 48,288 | Asset | Industrial equipment |
| 17 | COMMUNICATIONS | 40,759 | - | Communications sector |
| 18 | Dependency | 40,000 | Asset | SBOM dependencies |
| 19 | Relationship | 40,000 | - | Generic relationships |
| 20 | SECTOR_DEFENSE_INDUSTRIAL_BASE | 38,800 | - | Defense sector |
| 21 | ENERGY | 35,475 | - | Energy sector |
| 22 | Process | 34,504 | - | Business processes |
| 23 | CHEMICAL | 32,200 | - | Chemical sector |
| 24 | Compliance | 30,400 | - | Compliance data |
| 25 | CriticalInfrastructure | 28,100 | - | Critical infrastructure |
| 26-50 | ... | ... | ... | (See full data above) |

### Sector Distribution

Critical infrastructure sectors represented:

| Sector | Node Count | Labels |
|--------|-----------|--------|
| COMMUNICATIONS | 40,759 | COMMUNICATIONS, Telecom_Infrastructure, Data_Centers, NetworkMeasurement |
| SECTOR_DEFENSE_INDUSTRIAL_BASE | 38,800 | DefenseMeasurement, DefenseProperty, DefenseDevice |
| ENERGY | 35,475 | Energy_Transmission, Energy_Distribution, EnergyDevice, EnergyProperty |
| CHEMICAL | 32,200 | ChemicalEquipment, ChemicalProcess, Reactors |
| EMERGENCY_SERVICES | 28,000 | ResponseMetric, EmergencyEquipment, EmergencyResponse |
| FOOD_AGRICULTURE | 28,000 | AgricultureMetric, FoodSafety, Agriculture |
| Healthcare | 28,000 | HealthcareMeasurement, HealthcareDevice, HealthcareProcess |
| INFORMATION_TECHNOLOGY | 28,000 | ITMeasurement, ITDevice, IT_Infrastructure |
| FINANCIAL_SERVICES | 28,000 | TransactionMetric, Banking, CapitalMarkets, PaymentSystems |
| COMMERCIAL_FACILITIES | 28,000 | CommercialAsset, CommercialProcess |
| WATER | 27,200 | Water_Treatment, WaterDevice, WaterProperty |
| GOVERNMENT_FACILITIES | 27,000 | GovernmentProcess, GovernmentDevice, GovernmentMeasurement |

---

## Relationship Statistics

### Top 50 Relationship Types by Count

| Rank | Relationship | Count | Description |
|------|--------------|-------|-------------|
| 1 | IMPACTS | 4,780,563 | Impact relationships (vulnerabilities → assets) |
| 2 | VULNERABLE_TO | 3,117,735 | Asset vulnerability relationships |
| 3 | INSTALLED_ON | 968,125 | Software/equipment installation |
| 4 | TRACKS_PROCESS | 344,256 | Process monitoring |
| 5 | MONITORS_EQUIPMENT | 289,233 | Equipment monitoring |
| 6 | CONSUMES_FROM | 289,050 | Resource consumption |
| 7 | PROCESSES_THROUGH | 270,203 | Process flow |
| 8 | MITIGATES | 250,782 | Control mitigation |
| 9 | CHAINS_TO | 225,358 | Attack chain progression |
| 10 | IS_WEAKNESS_TYPE | 225,144 | CWE classification |
| 11 | DELIVERS_TO | 216,126 | Delivery relationships |
| 12 | MONITORS | 195,265 | General monitoring |
| 13 | MEASURES | 165,400 | Measurement relationships |
| 14 | USES_SOFTWARE | 149,949 | Software usage |
| 15 | HAS_MEASUREMENT | 117,936 | Measurement associations |
| 16 | GOVERNS | 53,862 | Governance relationships |
| 17 | RELATED_TO | 49,232 | General relationships |
| 18 | HAS_PROPERTY | 42,052 | Property associations |
| 19 | HAS_ENERGY_PROPERTY | 30,000 | Energy property links |
| 20 | BASED_ON_PATTERN | 29,970 | Pattern-based relationships |
| 21-50 | ... | ... | (See full data above) |

### Relationship Categories

| Category | Relationships | Total Count |
|----------|---------------|-------------|
| **Impact & Vulnerability** | IMPACTS, VULNERABLE_TO, EXPLOITS, THREATENS, DETECTS_VULNERABILITY | 8,000,000+ |
| **Monitoring & Measurement** | MONITORS, MEASURES, HAS_MEASUREMENT, GENERATES_MEASUREMENT, TRACKS_PROCESS | 1,100,000+ |
| **Control & Mitigation** | MITIGATES, MITIGATED_BY, CONTROLS, PROTECTED_BY, DETECTS | 280,000+ |
| **Infrastructure** | INSTALLED_ON, INSTALLED_AT_SUBSTATION, CONNECTED_TO_GRID, DELIVERS_TO | 1,200,000+ |
| **ATT&CK Taxonomy** | USES_TECHNIQUE, USES_TACTIC, BELONGS_TO_TACTIC, CHAINS_TO, MAPS_TO_ATTACK | 240,000+ |
| **SBOM & Dependencies** | DEPENDS_ON, CONTAINS, REQUIRES, INCLUDES_COMPONENT | 40,000+ |
| **Threat Intelligence** | ATTRIBUTED_TO, USES_ATTACK_PATTERN, TARGETS, IDENTIFIES_THREAT | 35,000+ |

---

## Usage Patterns

### Common Query Patterns

#### 1. Find all CVEs affecting a specific vendor
```cypher
MATCH (cve:CVE)-[:IMPACTS]->(asset)
WHERE 'Cisco' IN cve.cpe_vendors
RETURN cve.id, cve.cvssV31BaseSeverity, cve.epss_score
ORDER BY cve.epss_score DESC
LIMIT 100
```

#### 2. Get measurement time series for a sector
```cypher
MATCH (m:Measurement)
WHERE m.subsector = 'Energy_Transmission'
  AND m.timestamp > datetime('2025-01-01')
RETURN m.timestamp, m.value, m.unit, m.measurement_type
ORDER BY m.timestamp
```

#### 3. Find threat actors using specific techniques
```cypher
MATCH (ta:ThreatActor)-[:USES_TECHNIQUE]->(t:Technique)
WHERE t.name CONTAINS 'Spearphishing'
RETURN ta.name, ta.sophistication, collect(t.name) as techniques
```

#### 4. Get vulnerability chain of attack
```cypher
MATCH path = (start:Technique)-[:CHAINS_TO*1..5]->(end:Technique)
WHERE start.name = 'Initial Access'
RETURN path
LIMIT 10
```

#### 5. Find assets vulnerable to high-severity CVEs
```cypher
MATCH (asset:Asset)-[:VULNERABLE_TO]->(cve:CVE)
WHERE cve.cvssV31BaseSeverity = 'CRITICAL'
  AND cve.epss_score > 0.7
RETURN asset.device_name, asset.manufacturer,
       count(cve) as critical_cves,
       avg(cve.epss_score) as avg_exploit_prob
ORDER BY critical_cves DESC
```

---

## Property Discriminators Reference

### Fine-Grained Type Values (Top 50)

| Type | Count | Super Label | Usage |
|------|-------|-------------|-------|
| vulnerability | 313,561 | Vulnerability | General vulnerabilities |
| measurement | 297,858 | Measurement | Sensor/monitoring data |
| asset | 201,008 | Asset | General assets |
| control | 16,745 | Control | Security controls |
| protocol | 12,633 | Protocol/Asset | Network protocols |
| threatactor | 8,258 | ThreatActor | Threat actors |
| technique | 4,269 | Technique | ATT&CK techniques |
| event | 2,229 | Event | Security events |
| indicator | 1,575 | Indicator | IOCs |
| software | 818 | Software | Software products |
| malware | 768 | ThreatActor | Malware families |
| cve | 533 | Vulnerability | Specific CVEs |
| campaign | 163 | Campaign | Threat campaigns |
| ... | ... | ... | ... |

### Measurement Type Values

| Measurement Type | Count | Sectors |
|------------------|-------|---------|
| uptime | ~27,000 | Communications, IT |
| temperature | ~18,000 | Nuclear, Energy, Manufacturing |
| pressure | ~15,000 | Chemical, Energy |
| performance | ~12,000 | IT, Communications |
| radiation | ~18,000 | Nuclear |
| transaction | ~17,000 | Financial Services |
| response_time | ~17,000 | Emergency Services |
| quality | ~10,000 | Manufacturing, Food & Agriculture |

### Asset Class Values

| Asset Class | Count | Description |
|-------------|-------|-------------|
| device | ~150,000 | Physical devices (sensors, controllers, equipment) |
| protocol | ~12,000 | Network protocols and communications |
| software | ~55,000 | Software components (SBOM) |
| equipment | ~48,000 | Industrial equipment |

---

## Schema Evolution Notes

### Enrichment Timestamps

The schema includes multiple enrichment timestamps showing when data was added/updated:

- `kaggle_enriched` - Kaggle dataset enrichment date
- `cpe_enriched` - CPE (Common Platform Enumeration) enrichment
- `epss_updated` - EPSS score update timestamp
- `uco_enriched_date` - UCO ontology integration date
- `tagged_date` - When validation tagging occurred

### Validation Status

Many nodes include validation tracking:

```javascript
{
  validation_status: "VALIDATED" | "PENDING" | "REJECTED",
  tagging_method: "automatic" | "manual" | "retroactive",
  created_by: "AEON_INTEGRATION_WAVE4" | other sources,
}
```

This enables quality control and provenance tracking across the knowledge graph.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Nodes** | ~1,000,000+ |
| **Total Labels** | 631 |
| **Total Relationship Types** | 183 |
| **Super Labels (Categories)** | 17 |
| **Tier 1 Categories** | 5 |
| **Critical Infrastructure Sectors** | 16 |
| **CVE/Vulnerability Nodes** | 316,552 |
| **Measurement Nodes** | 297,858 |
| **Asset Nodes** | 206,075 |
| **SBOM Nodes** | 140,000 |
| **Relationships** | ~8,000,000+ |

---

**Generated**: 2025-12-12
**Database**: bolt://localhost:7687 (neo4j/neo4j@openspg)
**Schema Version**: Production (AEON OXOT System)
