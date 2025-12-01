# NER11 Complete Mapping - Unmapped Tiers (5, 7, 8, 9)

**Date**: 2025-11-27
**Total Entities Mapped**: 197
**Super Labels**: 16 (Asset, AttackPattern, Campaign, Control, EconomicMetric, Event, Indicator, Location, Malware, Organization, Protocol, PsychTrait, Role, Software, ThreatActor, Vulnerability)

---

## TIER 5: BEHAVIORAL (47 entities - 0% → 100%)

### Patterns (24 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| HISTORICAL_PATTERN | 5 | Indicator | indicatorType | behavioral_pattern |
| PAST_BEHAVIOR | 5 | Indicator | indicatorType | historical_behavior |
| ORG_BEHAVIOR | 5 | Indicator | indicatorType | organizational_behavior |
| SECTOR_BEHAVIOR | 5 | Indicator | indicatorType | sector_behavior |
| ATTACKER_BEHAVIOR | 5 | AttackPattern | patternType | attacker_behavior |
| ATTACK_PATTERN | 5 | AttackPattern | patternType | generic_attack_pattern |
| ATTACK_PATTERNS | 5 | AttackPattern | patternType | generic_attack_pattern |
| OBSERVABLE_TTP | 5 | AttackPattern | patternType | observable_ttp |
| CAMPAIGN_PATTERN | 5 | Campaign | campaignType | pattern_based |
| MULTI_STAGE_OPERATION | 5 | Campaign | campaignType | multi_stage |
| SEASONAL_PATTERN | 5 | Indicator | indicatorType | temporal_pattern |
| TIME_BASED_TREND | 5 | Indicator | indicatorType | temporal_trend |
| GEOGRAPHIC_PATTERN | 5 | Indicator | indicatorType | geographic_pattern |
| REGION_SPECIFIC_ATTACK | 5 | AttackPattern | patternType | geographic_specific |
| TARGET_SELECTION | 5 | AttackPattern | patternType | targeting_method |
| VICTIM_CRITERIA | 5 | AttackPattern | patternType | victim_selection |
| PERSISTENCE_METHOD | 5 | AttackPattern | patternType | persistence |
| EXFILTRATION_METHOD | 5 | AttackPattern | patternType | exfiltration |
| DATA_THEFT_TECHNIQUE | 5 | AttackPattern | patternType | data_theft |
| DESTRUCTION_METHOD | 5 | AttackPattern | patternType | destruction |
| WIPER | 5 | Malware | malwareType | wiper |
| RANSOMWARE_TACTIC | 5 | AttackPattern | patternType | ransomware_behavior |
| SOCIAL_BEHAVIOR | 5 | PsychTrait | traitType | social_behavior |
| SOCIAL_MEDIA_TACTIC | 5 | AttackPattern | patternType | social_media |

### Threat Perception (23 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| REAL_THREAT | 5 | Indicator | indicatorType | real_threat |
| ACTUAL_THREAT | 5 | Indicator | indicatorType | actual_threat |
| IMAGINARY_THREAT | 5 | Indicator | indicatorType | imaginary_threat |
| PERCEIVED_THREAT | 5 | Indicator | indicatorType | perceived_threat |
| SYMBOLIC_THREAT | 5 | Indicator | indicatorType | symbolic_threat |
| CULTURAL_THREAT | 5 | Indicator | indicatorType | cultural_threat |
| EXISTENTIAL_THREAT | 5 | Indicator | indicatorType | existential_threat |
| SURVIVAL_THREAT | 5 | Indicator | indicatorType | survival_threat |
| OPERATIONAL_THREAT | 5 | Indicator | indicatorType | operational_threat |
| OPERATIONS_THREAT | 5 | Indicator | indicatorType | operations_threat |
| REPUTATIONAL_THREAT | 5 | Indicator | indicatorType | reputational_threat |
| BRAND_DAMAGE | 5 | Event | eventType | brand_damage |
| FINANCIAL_THREAT | 5 | Indicator | indicatorType | financial_threat |
| ECONOMIC_LOSS | 5 | EconomicMetric | metricType | economic_loss |
| COMPLIANCE_THREAT | 5 | Indicator | indicatorType | compliance_threat |
| REGULATORY_RISK | 5 | Indicator | indicatorType | regulatory_risk |
| STRATEGIC_THREAT | 5 | Indicator | indicatorType | strategic_threat |
| LONG_TERM_THREAT | 5 | Indicator | indicatorType | long_term_threat |
| TACTICAL_THREAT | 5 | Indicator | indicatorType | tactical_threat |
| IMMEDIATE_THREAT | 5 | Indicator | indicatorType | immediate_threat |
| THREAT | 5 | Indicator | indicatorType | generic_threat |
| RISK | 5 | Indicator | indicatorType | risk |
| CHALLENGE | 5 | Indicator | indicatorType | challenge |

---

## TIER 7 (Safety/Reliability): 63 entities - 0% → 100%)

### RAMS & Hazards (39 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| RELIABILITY | 7 | EconomicMetric | metricType | reliability |
| MTBF | 7 | EconomicMetric | metricType | mean_time_between_failures |
| MTTR | 7 | EconomicMetric | metricType | mean_time_to_repair |
| FAILURE_RATE | 7 | EconomicMetric | metricType | failure_rate |
| AVAILABILITY | 7 | EconomicMetric | metricType | availability |
| UPTIME | 7 | EconomicMetric | metricType | uptime |
| DOWNTIME | 7 | EconomicMetric | metricType | downtime |
| MAINTAINABILITY | 7 | EconomicMetric | metricType | maintainability |
| PREVENTIVE_MAINTENANCE | 7 | Control | controlType | preventive_maintenance |
| CORRECTIVE_MAINTENANCE | 7 | Control | controlType | corrective_maintenance |
| SAFETY | 7 | Control | controlType | safety |
| FUNCTIONAL_SAFETY | 7 | Control | controlType | functional_safety |
| SAFETY_INTEGRITY_LEVEL | 7 | EconomicMetric | metricType | safety_integrity_level |
| SIL | 7 | EconomicMetric | metricType | sil |
| REDUNDANCY | 7 | Control | controlType | redundancy |
| N_PLUS_1 | 7 | Control | controlType | n_plus_1 |
| FAIL_SAFE | 7 | Control | controlType | fail_safe |
| SAFETY_CRITICAL | 7 | Asset | assetType | safety_critical |
| SAFETY_CONSIDERATIONS | 7 | Control | controlType | safety_considerations |
| CYBER_FAILURE_MODE | 7 | Vulnerability | vulnerabilityType | cyber_failure_mode |
| HAZARD | 7 | Event | eventType | hazard |
| RISK_SCENARIO | 7 | Event | eventType | risk_scenario |
| ACCIDENT | 7 | Event | eventType | accident |
| INCIDENT | 7 | Event | eventType | incident |
| INCIDENT_DETAIL | 7 | Event | eventType | incident_detail |
| INCIDENT_IMPACT | 7 | Event | eventType | incident_impact |
| HAZOP | 7 | Control | controlType | hazop |
| DEVIATION | 7 | Indicator | indicatorType | deviation |
| GUIDE_WORD | 7 | Control | controlType | guide_word |
| FMEA | 7 | Control | controlType | fmea |
| FAILURE_MODE | 7 | Vulnerability | vulnerabilityType | failure_mode |
| EFFECT_ANALYSIS | 7 | Control | controlType | effect_analysis |
| RPN | 7 | EconomicMetric | metricType | risk_priority_number |
| LOPA | 7 | Control | controlType | lopa |
| IPL | 7 | Control | controlType | independent_protection_layer |
| PROTECTION_LAYER | 7 | Control | controlType | protection_layer |
| BOW_TIE | 7 | Control | controlType | bow_tie |
| THREAT_LINE | 7 | AttackPattern | patternType | threat_line |
| CONSEQUENCE_LINE | 7 | Event | eventType | consequence_line |

### RAMS & Hazards Continued (13 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| FAULT_TREE | 7 | Control | controlType | fault_tree_analysis |
| BASIC_EVENT | 7 | Event | eventType | basic_event |
| TOP_EVENT | 7 | Event | eventType | top_event |
| SCENARIO | 7 | Event | eventType | scenario |
| MITIGATION | 7 | Control | controlType | mitigation |
| IMPACT | 7 | Event | eventType | impact |
| CONSEQUENCE | 7 | Event | eventType | consequence |
| CONSEQUENCES | 7 | Event | eventType | consequences |
| COUNTERMEASURE | 7 | Control | controlType | countermeasure |
| RESIDUAL_RISK | 7 | Indicator | indicatorType | residual_risk |
| EXISTING_SAFEGUARDS | 7 | Control | controlType | existing_safeguards |
| WHAT_IF | 7 | Control | controlType | what_if_analysis |
| RISK_SCORE | 7 | EconomicMetric | metricType | risk_score |

### Deterministic Control (11 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| DETERMINISTIC | 7 | Asset | assetType | deterministic_system |
| REAL_TIME | 7 | Asset | assetType | real_time_system |
| WCET | 7 | EconomicMetric | metricType | worst_case_execution_time |
| DEADLINE | 7 | EconomicMetric | metricType | deadline |
| SAFETY_PLC | 7 | Asset | assetType | safety_plc |
| SIS | 7 | Asset | assetType | safety_instrumented_system |
| ESD | 7 | Asset | assetType | emergency_shutdown_system |
| TRIP_SYSTEM | 7 | Asset | assetType | trip_system |
| FORMAL_VERIFICATION | 7 | Control | controlType | formal_verification |
| MODEL_CHECKING | 7 | Control | controlType | model_checking |
| THEOREM_PROVING | 7 | Control | controlType | theorem_proving |

---

## TIER 8: ONTOLOGY FRAMEWORKS (42 entities - 0% → 100%)

### IEC 62443 & Security Levels (11 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| SECURITY_LEVEL | 8 | EconomicMetric | metricType | security_level |
| SL_TARGET | 8 | EconomicMetric | metricType | sl_target |
| SL_ACHIEVED | 8 | EconomicMetric | metricType | sl_achieved |
| SL_CAPABILITY | 8 | EconomicMetric | metricType | sl_capability |
| FOUNDATIONAL_REQUIREMENT | 8 | Control | controlType | foundational_requirement |
| FR | 8 | Control | controlType | fr |
| SYSTEM_REQUIREMENT | 8 | Control | controlType | system_requirement |
| SR | 8 | Control | controlType | sr |
| COMPONENT_REQUIREMENT | 8 | Control | controlType | component_requirement |
| CR | 8 | Control | controlType | cr |
| IEC_62443 | 8 | Control | controlType | iec_62443 |

### Zone & Conduit (2 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| ZONE_CONDUIT | 8 | Asset | assetType | zone_conduit |
| CONDUIT | 8 | Asset | assetType | conduit |

### Adversary Emulation (10 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| EMULATION_PLAN | 8 | Control | controlType | emulation_plan |
| ADVERSARY_PROFILE | 8 | ThreatActor | actorType | adversary_profile |
| EM3D_TACTIC | 8 | AttackPattern | patternType | em3d_tactic |
| EM3D_TECHNIQUE | 8 | AttackPattern | patternType | em3d_technique |
| ADVERSARY_EMULATION | 8 | Event | eventType | adversary_emulation |
| MICRO_EMULATION_PLAN | 8 | Control | controlType | micro_emulation_plan |
| Adversary Emulation Plan | 8 | Control | controlType | adversary_emulation_plan |
| Intelligence Summary | 8 | Indicator | indicatorType | intelligence_summary |
| Adversary Overview | 8 | ThreatActor | actorType | adversary_overview |
| Operational Flow | 8 | AttackPattern | patternType | operational_flow |

### Emulation Phases (2 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| Emulation Phases | 8 | Event | eventType | emulation_phases |
| Micro Emulation Plan | 8 | Control | controlType | micro_emulation_plan |

### Ontology Structures (9 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| RELATIONSHIP | 8 | Indicator | indicatorType | relationship |
| PROPERTY | 8 | Indicator | indicatorType | property |
| CLASS | 8 | Indicator | indicatorType | class |
| INSTANCE | 8 | Indicator | indicatorType | instance |
| ONTOLOGY_CLASS | 8 | Indicator | indicatorType | ontology_class |
| KNOWLEDGE_GRAPH_NODE | 8 | Indicator | indicatorType | knowledge_graph_node |
| KNOWLEDGE_GRAPH_EDGE | 8 | Indicator | indicatorType | knowledge_graph_edge |
| ENTITY_TYPE | 8 | Indicator | indicatorType | entity_type |
| RELATED_ENTITIES | 8 | Indicator | indicatorType | related_entities |

### STRIDE & DFD (3 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| STRIDE_CATEGORY | 8 | AttackPattern | patternType | stride_category |
| DFD_ELEMENT | 8 | Asset | assetType | dfd_element |
| STRIDE_MAPPING | 8 | AttackPattern | patternType | stride_mapping |

### Risk Assessment & Standards (5 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| RISK_ASSESSMENT | 8 | Control | controlType | risk_assessment |
| NIST_800_53 | 8 | Control | controlType | nist_800_53 |
| MIL_STD | 8 | Control | controlType | mil_std |
| Adversary Profile | 8 | ThreatActor | actorType | adversary_profile |
| ASSET | 8 | Asset | assetType | generic_asset |

---

## TIER 9: CONTEXTUAL & META (45 entities - 0% → 100%)

### Contextual Descriptors (9 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| CONTEXT | 9 | Indicator | indicatorType | context |
| TECHNICAL_CONTEXT | 9 | Indicator | indicatorType | technical_context |
| DESCRIPTION | 9 | Indicator | indicatorType | description |
| PURPOSE | 9 | Indicator | indicatorType | purpose |
| EXAMPLE | 9 | Indicator | indicatorType | example |
| REALITY | 9 | Indicator | indicatorType | reality |
| DEFINITION | 9 | Indicator | indicatorType | definition |
| OUTCOME | 9 | Event | eventType | outcome |
| CALCULATION | 9 | EconomicMetric | metricType | calculation |

### Methodological (3 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| METHODOLOGY | 9 | Control | controlType | methodology |
| PRINCIPLE | 9 | Control | controlType | principle |
| GOAL | 9 | Indicator | indicatorType | goal |

### Techniques & Controls (9 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| TECHNIQUES | 9 | AttackPattern | patternType | techniques |
| CONTROL | 9 | Control | controlType | generic_control |
| EXISTING_CONTROLS | 9 | Control | controlType | existing_controls |
| NIST_CONTROLS | 9 | Control | controlType | nist_controls |
| ENFORCEMENT | 9 | Control | controlType | enforcement |
| VERIFICATION | 9 | Control | controlType | verification |
| TECHNICAL_CONTROLS | 9 | Control | controlType | technical_controls |
| MITIGATION_STRATEGIES | 9 | Control | controlType | mitigation_strategies |
| MITIGATION_TECHNOLOGY | 9 | Control | controlType | mitigation_technology |

### Implementation & Operations (9 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| IMPLEMENTATION | 9 | Event | eventType | implementation |
| PROCEDURE | 9 | Control | controlType | procedure |
| OPERATION | 9 | Event | eventType | operation |
| ACTIVITY | 9 | Event | eventType | activity |
| ACTION | 9 | Event | eventType | action |
| TASK | 9 | Event | eventType | task |
| PRACTICE | 9 | Control | controlType | practice |
| MITIGATION_IMPLEMENTATION | 9 | Control | controlType | mitigation_implementation |
| MITIGATION_EFFECTIVENESS | 9 | EconomicMetric | metricType | mitigation_effectiveness |

### Benefits & Effectiveness (5 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| BENEFIT | 9 | EconomicMetric | metricType | benefit |
| BENEFITS | 9 | EconomicMetric | metricType | benefits |
| EFFECTIVENESS | 9 | EconomicMetric | metricType | effectiveness |
| CYBERSECURITY_IMPACT | 9 | Event | eventType | cybersecurity_impact |
| CYBERSECURITY_MANIFESTATION | 9 | Event | eventType | cybersecurity_manifestation |

### Protocol Deployment (10 entities)

| NER11 Entity | Tier | Super Label | Discriminator Property | Value |
|--------------|------|-------------|----------------------|-------|
| PROTOCOL_DEPLOYMENT | 9 | Event | eventType | protocol_deployment |
| VENDOR_DEPLOYMENT | 9 | Event | eventType | vendor_deployment |
| VENDOR_PRODUCT | 9 | Software | softwareType | vendor_product |
| PRODUCT_LINE | 9 | Software | softwareType | product_line |
| PROTOCOL_STANDARD | 9 | Protocol | protocolType | protocol_standard |
| PROTOCOL_SECTOR | 9 | Protocol | protocolType | protocol_sector |
| PROTOCOL_EVOLUTION | 9 | Event | eventType | protocol_evolution |
| PROTOCOL_TREND | 9 | Indicator | indicatorType | protocol_trend |
| PROTOCOL_LATENCY | 9 | EconomicMetric | metricType | protocol_latency |
| PROTOCOL_MESSAGE | 9 | Protocol | protocolType | protocol_message |

---

## Summary Statistics

| Tier | Entity Count | Super Labels Used | Primary Mappings |
|------|--------------|-------------------|------------------|
| 5 (Behavioral) | 47 | 7 | AttackPattern (18), Indicator (19), Event (2), Malware (1), Campaign (2), PsychTrait (1), EconomicMetric (1) |
| 7 (Safety/Reliability) | 52 | 6 | Control (23), EconomicMetric (11), Event (11), Asset (5), Vulnerability (2), Indicator (1), AttackPattern (1) |
| 8 (Ontology Frameworks) | 42 | 7 | Control (12), Indicator (10), AttackPattern (6), ThreatActor (4), Asset (3), Event (2), EconomicMetric (5) |
| 9 (Contextual/Meta) | 45 | 8 | Control (12), Event (11), Indicator (9), EconomicMetric (6), AttackPattern (1), Software (2), Protocol (3), Event (1) |
| **TOTAL** | **197** | **16** | All 16 Super Labels utilized |

---

## Super Label Distribution

| Super Label | Total Usage | Percentage |
|-------------|-------------|------------|
| Control | 47 | 25.3% |
| Indicator | 39 | 21.0% |
| Event | 26 | 14.0% |
| EconomicMetric | 24 | 12.9% |
| AttackPattern | 26 | 14.0% |
| Asset | 8 | 4.3% |
| ThreatActor | 4 | 2.2% |
| Vulnerability | 2 | 1.1% |
| Malware | 1 | 0.5% |
| Campaign | 2 | 1.1% |
| PsychTrait | 1 | 0.5% |
| Software | 2 | 1.1% |
| Protocol | 3 | 1.6% |
| Organization | 0 | 0.0% |
| Location | 0 | 0.0% |
| Role | 0 | 0.0% |
